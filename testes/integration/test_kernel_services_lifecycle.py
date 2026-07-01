"""Testes de integração — serviços e lifecycle do microkernel.

Cobre: registro de serviços, list_services, all_health, stats,
get_service e comportamento após kernel.start().
"""
from __future__ import annotations

import pytest

from kernel.contracts.module import ModuleContract
from kernel.core.kernel import MicroKernel
from kernel.events.bus import KernelEvent
from kernel.lifecycle.manager import LifecycleState
from kernel.services.service_registry import ServiceError


# ---------------------------------------------------------------------------
# Helpers e fixtures
# ---------------------------------------------------------------------------

class _SvcSimples:
    """Serviço sem método health."""


class _SvcComHealth:
    """Serviço com health() que retorna dict."""

    def __init__(self, status: str = "ok") -> None:
        self._status = status

    def health(self) -> dict:
        return {"status": self._status, "ok": self._status == "ok"}


class _SvcHealthFalha:
    """Serviço com health() que levanta exceção."""

    def health(self) -> None:
        raise RuntimeError("serviço degradado")


def _fresh_kernel() -> MicroKernel:
    return MicroKernel()


def _make_contract(name: str) -> ModuleContract:
    return ModuleContract(name=name, provides=(name.replace(".", "_"),))


# ---------------------------------------------------------------------------
# Teste 1 — registrar serviço e verificar list_services()
# ---------------------------------------------------------------------------

class TestListServices:
    def test_registrar_servico_aparece_em_list(self) -> None:
        k = _fresh_kernel()
        k.register_service("parser", _SvcSimples())
        assert "parser" in k.services.list_services()

    def test_multiplos_servicos_em_list_ordenados(self) -> None:
        k = _fresh_kernel()
        k.register_service("zebra", _SvcSimples())
        k.register_service("alpha", _SvcSimples())
        k.register_service("medio", _SvcSimples())
        assert k.services.list_services() == ["alpha", "medio", "zebra"]

    def test_list_services_vazio_inicialmente(self) -> None:
        k = _fresh_kernel()
        assert k.services.list_services() == []

    def test_list_services_apos_unregister(self) -> None:
        k = _fresh_kernel()
        k.register_service("svc_a", _SvcSimples())
        k.register_service("svc_b", _SvcSimples())
        k.unregister_service("svc_a")
        assert k.services.list_services() == ["svc_b"]

    def test_list_services_retorna_lista(self) -> None:
        k = _fresh_kernel()
        assert isinstance(k.services.list_services(), list)


# ---------------------------------------------------------------------------
# Teste 2 — serviço com health() e all_health()
# ---------------------------------------------------------------------------

class TestAllHealth:
    def test_all_health_reflete_servico_com_health(self) -> None:
        k = _fresh_kernel()
        k.register_service("svc_health", _SvcComHealth("ok"))
        ah = k.services.all_health()
        assert "svc_health" in ah
        assert ah["svc_health"]["has_health_method"] is True
        assert ah["svc_health"]["health_result"]["status"] == "ok"

    def test_all_health_reflete_servico_sem_health(self) -> None:
        k = _fresh_kernel()
        k.register_service("svc_simples", _SvcSimples())
        ah = k.services.all_health()
        assert ah["svc_simples"]["has_health_method"] is False
        assert ah["svc_simples"]["health_result"] is None

    def test_all_health_multiplos_servicos(self) -> None:
        k = _fresh_kernel()
        k.register_service("a", _SvcSimples())
        k.register_service("b", _SvcComHealth())
        k.register_service("c", _SvcHealthFalha())
        ah = k.services.all_health()
        assert set(ah.keys()) == {"a", "b", "c"}
        assert ah["a"]["has_health_method"] is False
        assert ah["b"]["has_health_method"] is True
        assert ah["c"]["error"] is not None

    def test_all_health_vazio_sem_servicos(self) -> None:
        k = _fresh_kernel()
        assert k.services.all_health() == {}

    def test_all_health_retorna_dict_ordenado(self) -> None:
        k = _fresh_kernel()
        k.register_service("z", _SvcSimples())
        k.register_service("a", _SvcSimples())
        chaves = list(k.services.all_health().keys())
        assert chaves == ["a", "z"]


# ---------------------------------------------------------------------------
# Teste 3 — stats() após múltiplos registros
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_total_services_zero(self) -> None:
        k = _fresh_kernel()
        assert k.services.stats()["total_services"] == 0

    def test_stats_total_services_apos_registro(self) -> None:
        k = _fresh_kernel()
        k.register_service("a", _SvcSimples())
        k.register_service("b", _SvcSimples())
        k.register_service("c", _SvcComHealth())
        assert k.services.stats()["total_services"] == 3

    def test_stats_with_health_method(self) -> None:
        k = _fresh_kernel()
        k.register_service("sem", _SvcSimples())
        k.register_service("com1", _SvcComHealth())
        k.register_service("com2", _SvcHealthFalha())
        s = k.services.stats()
        assert s["with_health_method"] == 2
        assert s["without_health_method"] == 1

    def test_stats_apos_unregister_atualiza_contagens(self) -> None:
        k = _fresh_kernel()
        k.register_service("a", _SvcSimples())
        k.register_service("b", _SvcSimples())
        k.unregister_service("a")
        assert k.services.stats()["total_services"] == 1

    def test_stats_soma_with_without_igual_total(self) -> None:
        k = _fresh_kernel()
        k.register_service("x", _SvcSimples())
        k.register_service("y", _SvcComHealth())
        s = k.services.stats()
        assert s["with_health_method"] + s["without_health_method"] == s["total_services"]


# ---------------------------------------------------------------------------
# Teste 4 — get_service() retorna instância correta
# ---------------------------------------------------------------------------

class TestGetService:
    def test_get_service_retorna_instancia_correta(self) -> None:
        k = _fresh_kernel()
        svc = _SvcSimples()
        k.register_service("meu_svc", svc)
        assert k.get_service("meu_svc") is svc

    def test_get_service_distingue_instancias(self) -> None:
        k = _fresh_kernel()
        svc_a = _SvcSimples()
        svc_b = _SvcComHealth()
        k.register_service("a", svc_a)
        k.register_service("b", svc_b)
        assert k.get_service("a") is svc_a
        assert k.get_service("b") is svc_b

    def test_get_service_retorna_mesmo_objeto_em_multiplas_chamadas(self) -> None:
        k = _fresh_kernel()
        svc = _SvcSimples()
        k.register_service("s", svc)
        assert k.get_service("s") is k.get_service("s")

    def test_get_service_via_services_direto(self) -> None:
        k = _fresh_kernel()
        svc = _SvcComHealth("ativo")
        k.register_service("h", svc)
        assert k.services.get_service("h") is svc

    def test_get_service_apos_start_retorna_instancia(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.register_service("svc_x", _SvcSimples())
        k.initialize()
        k.start()
        svc = k.get_service("svc_x")
        assert isinstance(svc, _SvcSimples)


# ---------------------------------------------------------------------------
# Teste 5 — get_service() para nome inexistente
# ---------------------------------------------------------------------------

class TestGetServiceInexistente:
    def test_get_service_inexistente_levanta_service_error(self) -> None:
        k = _fresh_kernel()
        with pytest.raises(ServiceError, match="não registrado"):
            k.get_service("nao_existe")

    def test_get_service_apos_unregister_levanta_erro(self) -> None:
        k = _fresh_kernel()
        k.register_service("temp", _SvcSimples())
        k.unregister_service("temp")
        with pytest.raises(ServiceError):
            k.get_service("temp")

    def test_service_error_e_runtime_error(self) -> None:
        k = _fresh_kernel()
        try:
            k.get_service("inexistente")
        except ServiceError as exc:
            assert isinstance(exc, RuntimeError)

    def test_has_service_falso_para_inexistente(self) -> None:
        k = _fresh_kernel()
        assert k.services.has_service("inexistente") is False

    def test_has_service_verdadeiro_apos_registro(self) -> None:
        k = _fresh_kernel()
        k.register_service("presente", _SvcSimples())
        assert k.services.has_service("presente") is True


# ---------------------------------------------------------------------------
# Teste 6 — serviço acessível após kernel.start()
# ---------------------------------------------------------------------------

class TestServicosAposStart:
    def test_servico_registrado_antes_start_acessivel_depois(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        svc = _SvcComHealth("running")
        k.register_service("runtime_svc", svc)
        k.initialize()
        k.start()
        assert k.get_service("runtime_svc") is svc

    def test_servico_registrado_apos_start_acessivel(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        svc = _SvcSimples()
        k.register_service("novo_svc", svc)
        assert k.get_service("novo_svc") is svc

    def test_servico_acessivel_apos_stop(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        svc = _SvcSimples()
        k.register_service("persistente", svc)
        k.initialize()
        k.start()
        k.stop()
        # serviços persistem mesmo após stop
        assert k.get_service("persistente") is svc

    def test_register_service_publica_evento_service_registered(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        eventos: list[dict] = []
        k.events.subscribe(KernelEvent.SERVICE_REGISTERED,
                           lambda e, d: eventos.append(dict(d)))
        k.register_service("svc_prod", _SvcComHealth())
        assert len(eventos) == 1
        assert eventos[0]["name"] == "svc_prod"

    def test_unregister_service_publica_evento_service_unregistered(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.register_service("svc_temp", _SvcSimples())
        eventos: list[dict] = []
        k.events.subscribe(KernelEvent.SERVICE_UNREGISTERED,
                           lambda e, d: eventos.append(dict(d)))
        k.unregister_service("svc_temp")
        assert len(eventos) == 1
        assert eventos[0]["name"] == "svc_temp"

    def test_lifecycle_e_servicos_sao_independentes(self) -> None:
        """Serviços podem ser registrados em qualquer estado do kernel."""
        k = _fresh_kernel()
        # Registrar serviço com kernel em CREATED
        k.register_service("early_svc", _SvcSimples())
        assert k.state == LifecycleState.CREATED
        assert k.services.has_service("early_svc") is True
