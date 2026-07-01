"""Testes de contrato — Fase 6: ServiceRegistry.

Cobertura:
- ServiceRegistry: register_service, get_service, list_services,
  has_service, unregister_service, service_health, all_health, stats, reset
- Novos KernelEvents: SERVICE_REGISTERED, SERVICE_UNREGISTERED
- Integração com MicroKernel: register_service, unregister_service, get_service
- Erros e guardas de valor
"""
from __future__ import annotations

import pytest

from kernel import KernelEvent, MicroKernel, ServiceError, ServiceRegistry


# ---------------------------------------------------------------------------
# Fixtures e helpers
# ---------------------------------------------------------------------------


class _Svc:
    """Serviço simples sem método health."""


class _SvcComHealth:
    """Serviço com método health()."""

    def __init__(self, ok: bool = True) -> None:
        self._ok = ok

    def health(self) -> dict:
        if not self._ok:
            raise RuntimeError("serviço degradado")
        return {"status": "ok", "version": "1.0"}


class _SvcHealthFalha:
    """Serviço cujo health() levanta exceção."""

    def health(self) -> None:
        raise RuntimeError("falha interna")


@pytest.fixture
def reg() -> ServiceRegistry:
    return ServiceRegistry()


@pytest.fixture
def svc() -> _Svc:
    return _Svc()


@pytest.fixture
def svc_health() -> _SvcComHealth:
    return _SvcComHealth(ok=True)


# ===========================================================================
# TestServiceRegistryBasico
# ===========================================================================


class TestServiceRegistryBasico:
    def test_register_e_get(self, reg: ServiceRegistry, svc: _Svc) -> None:
        reg.register_service("parser", svc)
        assert reg.get_service("parser") is svc

    def test_register_retorna_instancia_correta(self, reg: ServiceRegistry) -> None:
        a, b = _Svc(), _Svc()
        reg.register_service("a", a)
        reg.register_service("b", b)
        assert reg.get_service("a") is a
        assert reg.get_service("b") is b

    def test_list_services_vazio(self, reg: ServiceRegistry) -> None:
        assert reg.list_services() == []

    def test_list_services_ordenado(self, reg: ServiceRegistry) -> None:
        reg.register_service("zebra", _Svc())
        reg.register_service("alpha", _Svc())
        reg.register_service("medio", _Svc())
        assert reg.list_services() == ["alpha", "medio", "zebra"]

    def test_has_service_falso(self, reg: ServiceRegistry) -> None:
        assert reg.has_service("inexistente") is False

    def test_has_service_verdadeiro(self, reg: ServiceRegistry, svc: _Svc) -> None:
        reg.register_service("x", svc)
        assert reg.has_service("x") is True

    def test_has_service_apos_unregister(self, reg: ServiceRegistry, svc: _Svc) -> None:
        reg.register_service("x", svc)
        reg.unregister_service("x")
        assert reg.has_service("x") is False


# ===========================================================================
# TestServiceRegistryErros
# ===========================================================================


class TestServiceRegistryErros:
    def test_register_nome_vazio(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não pode ser vazio"):
            reg.register_service("", _Svc())

    def test_register_nome_espacos(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não pode ser vazio"):
            reg.register_service("   ", _Svc())

    def test_register_instancia_none(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não pode ser None"):
            reg.register_service("parser", None)

    def test_register_duplicado(self, reg: ServiceRegistry) -> None:
        reg.register_service("parser", _Svc())
        with pytest.raises(ServiceError, match="já registrado"):
            reg.register_service("parser", _Svc())

    def test_get_inexistente(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não registrado"):
            reg.get_service("inexistente")

    def test_unregister_inexistente(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não registrado"):
            reg.unregister_service("inexistente")

    def test_service_health_inexistente(self, reg: ServiceRegistry) -> None:
        with pytest.raises(ServiceError, match="não registrado"):
            reg.service_health("inexistente")


# ===========================================================================
# TestServiceHealth
# ===========================================================================


class TestServiceHealth:
    def test_health_sem_metodo(self, reg: ServiceRegistry, svc: _Svc) -> None:
        reg.register_service("svc", svc)
        h = reg.service_health("svc")
        assert h["name"] == "svc"
        assert h["registered"] is True
        assert h["type"] == "_Svc"
        assert h["has_health_method"] is False
        assert h["health_result"] is None
        assert h["error"] is None
        assert isinstance(h["uptime_seconds"], float)
        assert h["uptime_seconds"] >= 0.0

    def test_health_com_metodo_ok(self, reg: ServiceRegistry, svc_health: _SvcComHealth) -> None:
        reg.register_service("svc", svc_health)
        h = reg.service_health("svc")
        assert h["has_health_method"] is True
        assert h["health_result"] == {"status": "ok", "version": "1.0"}
        assert h["error"] is None

    def test_health_com_falha(self, reg: ServiceRegistry) -> None:
        reg.register_service("falha", _SvcHealthFalha())
        h = reg.service_health("falha")
        assert h["has_health_method"] is True
        assert h["health_result"] is None
        assert h["error"] is not None
        assert "falha interna" in h["error"]

    def test_all_health_vazio(self, reg: ServiceRegistry) -> None:
        assert reg.all_health() == {}

    def test_all_health_multiplos(self, reg: ServiceRegistry) -> None:
        reg.register_service("a", _Svc())
        reg.register_service("b", _SvcComHealth())
        ah = reg.all_health()
        assert set(ah.keys()) == {"a", "b"}
        assert ah["a"]["has_health_method"] is False
        assert ah["b"]["has_health_method"] is True

    def test_all_health_ordenado(self, reg: ServiceRegistry) -> None:
        reg.register_service("z", _Svc())
        reg.register_service("a", _Svc())
        assert list(reg.all_health().keys()) == ["a", "z"]


# ===========================================================================
# TestServiceRegistryStats
# ===========================================================================


class TestServiceRegistryStats:
    def test_stats_vazio(self, reg: ServiceRegistry) -> None:
        s = reg.stats()
        assert s["total_services"] == 0
        assert s["with_health_method"] == 0
        assert s["without_health_method"] == 0

    def test_stats_apenas_sem_health(self, reg: ServiceRegistry) -> None:
        reg.register_service("a", _Svc())
        reg.register_service("b", _Svc())
        s = reg.stats()
        assert s["total_services"] == 2
        assert s["with_health_method"] == 0
        assert s["without_health_method"] == 2

    def test_stats_misto(self, reg: ServiceRegistry) -> None:
        reg.register_service("sem", _Svc())
        reg.register_service("com", _SvcComHealth())
        s = reg.stats()
        assert s["total_services"] == 2
        assert s["with_health_method"] == 1
        assert s["without_health_method"] == 1

    def test_stats_apenas_com_health(self, reg: ServiceRegistry) -> None:
        reg.register_service("a", _SvcComHealth())
        reg.register_service("b", _SvcComHealth())
        s = reg.stats()
        assert s["total_services"] == 2
        assert s["with_health_method"] == 2
        assert s["without_health_method"] == 0

    def test_stats_todos_sao_int(self, reg: ServiceRegistry) -> None:
        reg.register_service("x", _SvcComHealth())
        for v in reg.stats().values():
            assert isinstance(v, int)


# ===========================================================================
# TestServiceRegistryReset
# ===========================================================================


class TestServiceRegistryReset:
    def test_reset_limpa_tudo(self, reg: ServiceRegistry) -> None:
        reg.register_service("a", _Svc())
        reg.register_service("b", _Svc())
        reg.reset()
        assert reg.list_services() == []
        assert reg.stats()["total_services"] == 0

    def test_reset_permite_reregistro(self, reg: ServiceRegistry) -> None:
        svc = _Svc()
        reg.register_service("x", svc)
        reg.reset()
        reg.register_service("x", svc)  # não deve levantar
        assert reg.has_service("x") is True

    def test_reset_vazio_sem_erro(self, reg: ServiceRegistry) -> None:
        reg.reset()  # não deve levantar


# ===========================================================================
# TestUnregister
# ===========================================================================


class TestUnregister:
    def test_unregister_remove_servico(self, reg: ServiceRegistry) -> None:
        reg.register_service("parser", _Svc())
        reg.unregister_service("parser")
        assert reg.has_service("parser") is False

    def test_unregister_atualiza_list(self, reg: ServiceRegistry) -> None:
        reg.register_service("a", _Svc())
        reg.register_service("b", _Svc())
        reg.unregister_service("a")
        assert reg.list_services() == ["b"]

    def test_unregister_atualiza_stats(self, reg: ServiceRegistry) -> None:
        reg.register_service("x", _Svc())
        assert reg.stats()["total_services"] == 1
        reg.unregister_service("x")
        assert reg.stats()["total_services"] == 0

    def test_unregister_permite_reregistro(self, reg: ServiceRegistry) -> None:
        svc = _Svc()
        reg.register_service("x", svc)
        reg.unregister_service("x")
        reg.register_service("x", svc)  # não deve levantar
        assert reg.has_service("x") is True


# ===========================================================================
# TestKernelEventServicos
# ===========================================================================


class TestKernelEventServicos:
    def test_service_registered_existe(self) -> None:
        assert KernelEvent.SERVICE_REGISTERED == "service_registered"

    def test_service_unregistered_existe(self) -> None:
        assert KernelEvent.SERVICE_UNREGISTERED == "service_unregistered"

    def test_service_registered_e_str(self) -> None:
        assert isinstance(KernelEvent.SERVICE_REGISTERED, str)

    def test_service_unregistered_e_str(self) -> None:
        assert isinstance(KernelEvent.SERVICE_UNREGISTERED, str)

    def test_comparacao_com_string(self) -> None:
        assert KernelEvent.SERVICE_REGISTERED == "service_registered"
        assert KernelEvent.SERVICE_UNREGISTERED == "service_unregistered"


# ===========================================================================
# TestMicroKernelIntegracaoServicos
# ===========================================================================


class TestMicroKernelIntegracaoServicos:
    def test_kernel_tem_services(self) -> None:
        k = MicroKernel()
        assert hasattr(k, "services")
        assert isinstance(k.services, ServiceRegistry)

    def test_register_service_via_kernel(self) -> None:
        k = MicroKernel()
        svc = _Svc()
        k.register_service("parser", svc)
        assert k.services.has_service("parser") is True

    def test_get_service_via_kernel(self) -> None:
        k = MicroKernel()
        svc = _Svc()
        k.register_service("parser", svc)
        assert k.get_service("parser") is svc

    def test_unregister_service_via_kernel(self) -> None:
        k = MicroKernel()
        k.register_service("parser", _Svc())
        k.unregister_service("parser")
        assert k.services.has_service("parser") is False

    def test_register_service_publica_evento(self) -> None:
        k = MicroKernel()
        eventos_capturados: list[dict] = []

        def handler(event: KernelEvent, data: dict) -> None:
            eventos_capturados.append({"event": event, "data": data})

        k.events.subscribe(KernelEvent.SERVICE_REGISTERED, handler)
        k.register_service("parser", _Svc())

        assert len(eventos_capturados) == 1
        ev = eventos_capturados[0]
        assert ev["event"] == KernelEvent.SERVICE_REGISTERED
        assert ev["data"]["name"] == "parser"
        assert ev["data"]["type"] == "_Svc"

    def test_unregister_service_publica_evento(self) -> None:
        k = MicroKernel()
        eventos_capturados: list[dict] = []

        def handler(event: KernelEvent, data: dict) -> None:
            eventos_capturados.append({"event": event, "data": data})

        k.events.subscribe(KernelEvent.SERVICE_UNREGISTERED, handler)
        k.register_service("parser", _Svc())
        k.unregister_service("parser")

        assert len(eventos_capturados) == 1
        ev = eventos_capturados[0]
        assert ev["event"] == KernelEvent.SERVICE_UNREGISTERED
        assert ev["data"]["name"] == "parser"

    def test_register_service_tipo_no_evento(self) -> None:
        k = MicroKernel()
        capturado: list[dict] = []

        def handler(event: KernelEvent, data: dict) -> None:
            capturado.append(data)

        k.events.subscribe(KernelEvent.SERVICE_REGISTERED, handler)
        k.register_service("health_svc", _SvcComHealth())

        assert capturado[0]["type"] == "_SvcComHealth"

    def test_multiplos_servicos_independentes(self) -> None:
        k = MicroKernel()
        a, b, c = _Svc(), _SvcComHealth(), _SvcHealthFalha()
        k.register_service("a", a)
        k.register_service("b", b)
        k.register_service("c", c)
        assert k.services.list_services() == ["a", "b", "c"]
        assert k.get_service("a") is a
        assert k.get_service("b") is b
        assert k.get_service("c") is c

    def test_kernel_lifecycle_e_servicos_independentes(self) -> None:
        """Serviços podem ser registrados sem lifecycle ativo."""
        k = MicroKernel()
        k.register_service("x", _Svc())
        # kernel não precisa estar em RUNNING para registrar serviços
        assert k.state.value == "created"
        assert k.services.has_service("x") is True

    def test_historico_eventos_servico(self) -> None:
        k = MicroKernel()
        k.register_service("a", _Svc())
        k.register_service("b", _Svc())
        k.unregister_service("a")

        hist_reg = k.events.history(KernelEvent.SERVICE_REGISTERED)
        hist_unreg = k.events.history(KernelEvent.SERVICE_UNREGISTERED)

        assert len(hist_reg) == 2
        assert len(hist_unreg) == 1
        assert hist_reg[0][1]["name"] == "a"
        assert hist_reg[1][1]["name"] == "b"
        assert hist_unreg[0][1]["name"] == "a"
