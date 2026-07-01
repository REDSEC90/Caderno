"""Testes de integração — propagação de eventos entre componentes.

Cobre: subscribe/publish ponta-a-ponta, history, stats e múltiplos handlers.
"""
from __future__ import annotations

from typing import Any

import pytest

from kernel.contracts.module import ModuleContract
from kernel.core.kernel import MicroKernel
from kernel.events.bus import KernelEvent, KernelEventBus
from kernel.lifecycle.manager import LifecycleState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_kernel() -> MicroKernel:
    return MicroKernel()


def _make_contract(name: str, provides: tuple[str, ...] | None = None) -> ModuleContract:
    cap = provides if provides is not None else (name.replace(".", "_"),)
    return ModuleContract(name=name, provides=cap)


# ---------------------------------------------------------------------------
# Teste 1 — register() publica MODULE_REGISTERED
# ---------------------------------------------------------------------------

class TestRegisterPublicaEvento:
    def test_register_publica_module_registered(self) -> None:
        k = _fresh_kernel()
        recebidos: list[dict] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: recebidos.append(dict(d)))
        k.register(_make_contract("mod.a"))
        assert len(recebidos) == 1
        assert recebidos[0]["name"] == "mod.a"

    def test_register_inclui_versao_no_payload(self) -> None:
        k = _fresh_kernel()
        payloads: list[dict] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: payloads.append(dict(d)))
        k.register(ModuleContract(name="mod.v", provides=("v",), version="2.0.0"))
        assert payloads[0]["version"] == "2.0.0"

    def test_multiplos_registers_geram_multiplos_eventos(self) -> None:
        k = _fresh_kernel()
        nomes: list[str] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: nomes.append(d["name"]))
        k.register(_make_contract("mod.a"))
        k.register(_make_contract("mod.b"))
        k.register(_make_contract("mod.c"))
        assert nomes == ["mod.a", "mod.b", "mod.c"]

    def test_evento_module_registered_tipo_correto(self) -> None:
        k = _fresh_kernel()
        eventos: list[KernelEvent] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: eventos.append(e))
        k.register(_make_contract("mod.a"))
        assert eventos[0] == KernelEvent.MODULE_REGISTERED


# ---------------------------------------------------------------------------
# Teste 2 — start() publica STATE_CHANGED
# ---------------------------------------------------------------------------

class TestStartPublicaEvento:
    def test_start_publica_state_changed_running(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        destinos: list[str] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: destinos.append(d["to"]))
        k.start()
        assert "running" in destinos

    def test_start_inclui_estado_origem_no_payload(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        transicoes: list[dict] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: transicoes.append(dict(d)))
        k.start()
        # última transição: initialized → running
        ultima = transicoes[-1]
        assert ultima["from"] == "initialized"
        assert ultima["to"] == "running"

    def test_stop_publica_state_changed_stopped(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        destinos: list[str] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: destinos.append(d["to"]))
        k.stop()
        assert "stopped" in destinos

    def test_ciclo_completo_gera_multiplas_transicoes(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        transicoes: list[dict] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: transicoes.append(dict(d)))
        k.initialize()
        k.start()
        k.stop()
        destinos = [t["to"] for t in transicoes]
        assert "initialized" in destinos
        assert "running" in destinos
        assert "stopped" in destinos


# ---------------------------------------------------------------------------
# Teste 3 — subscribe + publish ponta-a-ponta
# ---------------------------------------------------------------------------

class TestSubscribePublish:
    def test_subscribe_e_notificado_na_publicacao(self) -> None:
        bus = KernelEventBus()
        recebidos: list[tuple[KernelEvent, dict]] = []
        bus.subscribe(KernelEvent.MODULE_STARTED,
                      lambda e, d: recebidos.append((e, dict(d))))
        bus.publish(KernelEvent.MODULE_STARTED, {"info": "ok"})
        assert len(recebidos) == 1
        assert recebidos[0][0] == KernelEvent.MODULE_STARTED
        assert recebidos[0][1]["info"] == "ok"

    def test_publish_sem_data_entrega_dict_vazio(self) -> None:
        bus = KernelEventBus()
        recebidos: list[dict] = []
        bus.subscribe(KernelEvent.MODULE_STOPPED,
                      lambda e, d: recebidos.append(dict(d)))
        bus.publish(KernelEvent.MODULE_STOPPED)
        assert recebidos == [{}]

    def test_publish_retorna_quantidade_de_handlers_chamados(self) -> None:
        bus = KernelEventBus()
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        n = bus.publish(KernelEvent.STATE_CHANGED, {})
        assert n == 2

    def test_publish_sem_handlers_retorna_zero(self) -> None:
        bus = KernelEventBus()
        assert bus.publish(KernelEvent.CONTRACT_VALIDATED, {}) == 0

    def test_unsubscribe_impede_notificacao(self) -> None:
        bus = KernelEventBus()
        chamadas: list[int] = []
        handler = lambda e, d: chamadas.append(1)  # noqa: E731
        bus.subscribe(KernelEvent.MODULE_STARTED, handler)
        bus.unsubscribe(KernelEvent.MODULE_STARTED, handler)
        bus.publish(KernelEvent.MODULE_STARTED)
        assert chamadas == []


# ---------------------------------------------------------------------------
# Teste 4 — history() acumula eventos corretamente
# ---------------------------------------------------------------------------

class TestHistory:
    def test_history_acumula_eventos_em_ordem(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        h = k.events.history()
        tipos = [e for e, _ in h]
        assert KernelEvent.MODULE_REGISTERED in tipos
        assert KernelEvent.CONTRACT_VALIDATED in tipos
        assert KernelEvent.STATE_CHANGED in tipos
        assert KernelEvent.MODULE_STARTED in tipos
        assert KernelEvent.MODULE_STOPPED in tipos

    def test_history_filtrado_por_evento(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.register(_make_contract("mod.b"))
        k.initialize()
        h_reg = k.events.history(KernelEvent.MODULE_REGISTERED)
        assert len(h_reg) == 2
        assert all(e == KernelEvent.MODULE_REGISTERED for e, _ in h_reg)

    def test_history_retorna_dados_corretos(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.x"))
        h = k.events.history(KernelEvent.MODULE_REGISTERED)
        assert h[0][1]["name"] == "mod.x"

    def test_history_acumula_apos_multiplos_ciclos(self) -> None:
        bus = KernelEventBus()
        bus.publish(KernelEvent.MODULE_STARTED, {"run": 1})
        bus.publish(KernelEvent.MODULE_STARTED, {"run": 2})
        bus.publish(KernelEvent.MODULE_STOPPED, {"run": 2})
        h_start = bus.history(KernelEvent.MODULE_STARTED)
        h_stop = bus.history(KernelEvent.MODULE_STOPPED)
        assert len(h_start) == 2
        assert len(h_stop) == 1

    def test_clear_history_limpa_registros(self) -> None:
        bus = KernelEventBus()
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.clear_history()
        assert bus.history() == []

    def test_history_nao_afetado_por_modificacao_externa(self) -> None:
        bus = KernelEventBus()
        bus.publish(KernelEvent.STATE_CHANGED, {"to": "running"})
        h1 = bus.history()
        h1.append(("intruso", {}))  # type: ignore[arg-type]
        h2 = bus.history()
        assert len(h2) == 1


# ---------------------------------------------------------------------------
# Teste 5 — stats() reflete handlers e publicações
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_total_handlers_soma_todos(self) -> None:
        bus = KernelEventBus()
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        s = bus.stats()
        assert s["total_handlers"] == 3

    def test_stats_total_events_published(self) -> None:
        bus = KernelEventBus()
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.publish(KernelEvent.STATE_CHANGED)
        s = bus.stats()
        assert s["total_events_published"] == 3

    def test_stats_por_evento_handlers(self) -> None:
        bus = KernelEventBus()
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        s = bus.stats()
        assert s["event_module_registered_handlers"] == 2

    def test_stats_por_evento_publicacoes(self) -> None:
        bus = KernelEventBus()
        bus.publish(KernelEvent.MODULE_STOPPED)
        bus.publish(KernelEvent.MODULE_STOPPED)
        bus.publish(KernelEvent.MODULE_STOPPED)
        s = bus.stats()
        assert s["event_module_stopped_published"] == 3

    def test_stats_apos_ciclo_kernel(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        s = k.events.stats()
        assert s["total_events_published"] > 0
        assert s["event_module_registered_published"] == 1
        assert s["event_module_started_published"] == 1
        assert s["event_module_stopped_published"] == 1


# ---------------------------------------------------------------------------
# Teste 6 — múltiplos handlers no mesmo evento são todos chamados
# ---------------------------------------------------------------------------

class TestMultiplosHandlers:
    def test_dois_handlers_no_mesmo_evento(self) -> None:
        bus = KernelEventBus()
        chamadas: list[int] = []
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: chamadas.append(1))
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: chamadas.append(2))
        bus.publish(KernelEvent.STATE_CHANGED)
        assert chamadas == [1, 2]

    def test_tres_handlers_todos_chamados(self) -> None:
        bus = KernelEventBus()
        ids: list[str] = []
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: ids.append("A"))
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: ids.append("B"))
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: ids.append("C"))
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "test"})
        assert ids == ["A", "B", "C"]

    def test_handler_com_erro_nao_impede_os_demais(self) -> None:
        bus = KernelEventBus()
        chamadas: list[str] = []

        def handler_ruim(e: KernelEvent, d: dict) -> None:
            raise ValueError("erro proposital")

        bus.subscribe(KernelEvent.MODULE_FAILED, handler_ruim)
        bus.subscribe(KernelEvent.MODULE_FAILED, lambda e, d: chamadas.append("ok"))

        with pytest.raises(ValueError):
            bus.publish(KernelEvent.MODULE_FAILED)

        assert chamadas == ["ok"]

    def test_handlers_em_eventos_distintos_sao_independentes(self) -> None:
        k = _fresh_kernel()
        registros: list[str] = []
        starts: list[str] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: registros.append(d["name"]))
        k.events.subscribe(KernelEvent.MODULE_STARTED,
                           lambda e, d: starts.append("started"))
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        assert registros == ["mod.a"]
        assert starts == ["started"]

    def test_handler_recebe_evento_e_dados_corretos(self) -> None:
        bus = KernelEventBus()
        pares: list[tuple[KernelEvent, dict]] = []
        bus.subscribe(KernelEvent.DEPENDENCY_RESOLVED,
                      lambda e, d: pares.append((e, dict(d))))
        bus.publish(KernelEvent.DEPENDENCY_RESOLVED, {"order": ["a", "b"]})
        assert pares[0][0] == KernelEvent.DEPENDENCY_RESOLVED
        assert pares[0][1]["order"] == ["a", "b"]
