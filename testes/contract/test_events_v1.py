"""Testes da Fase 5 — KernelEventBus e integração com MicroKernel."""
from __future__ import annotations

from typing import Any

import pytest

from kernel.events import EventHandler, KernelEvent, KernelEventBus
from kernel.contracts.module import ModuleContract
from kernel.core.kernel import MicroKernel


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def bus() -> KernelEventBus:
    return KernelEventBus()


@pytest.fixture()
def kernel() -> MicroKernel:
    return MicroKernel()


# ---------------------------------------------------------------------------
# KernelEvent — enumeração
# ---------------------------------------------------------------------------

class TestKernelEvent:
    def test_todos_os_10_eventos_existem(self) -> None:
        esperados = {
            "module_discovered",
            "module_registered",
            "module_started",
            "module_stopped",
            "module_failed",
            "contract_validated",
            "dependency_resolved",
            "state_changed",
            "service_registered",
            "service_unregistered",
        }
        valores = {e.value for e in KernelEvent}
        assert valores == esperados

    def test_evento_e_str(self) -> None:
        assert isinstance(KernelEvent.MODULE_REGISTERED, str)
        assert KernelEvent.MODULE_REGISTERED == "module_registered"

    def test_comparacao_com_string(self) -> None:
        assert KernelEvent.STATE_CHANGED == "state_changed"


# ---------------------------------------------------------------------------
# subscribe / unsubscribe
# ---------------------------------------------------------------------------

class TestSubscribe:
    def test_subscribe_handler(self, bus: KernelEventBus) -> None:
        calls: list[str] = []

        def handler(event: KernelEvent, data: dict) -> None:
            calls.append(event.value)

        bus.subscribe(KernelEvent.MODULE_REGISTERED, handler)
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "x"})
        assert calls == ["module_registered"]

    def test_subscribe_multiplos_handlers(self, bus: KernelEventBus) -> None:
        calls: list[int] = []
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: calls.append(1))
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: calls.append(2))
        bus.publish(KernelEvent.STATE_CHANGED)
        assert calls == [1, 2]

    def test_subscribe_mesmo_handler_dois_eventos_distintos(
        self, bus: KernelEventBus
    ) -> None:
        calls: list[str] = []

        def handler(event: KernelEvent, data: dict) -> None:
            calls.append(event.value)

        bus.subscribe(KernelEvent.MODULE_STARTED, handler)
        bus.subscribe(KernelEvent.MODULE_STOPPED, handler)
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.publish(KernelEvent.MODULE_STOPPED)
        assert "module_started" in calls
        assert "module_stopped" in calls

    def test_subscribe_duplicado_levanta_erro(self, bus: KernelEventBus) -> None:
        handler: EventHandler = lambda e, d: None
        bus.subscribe(KernelEvent.MODULE_REGISTERED, handler)
        with pytest.raises(ValueError, match="handler já registrado"):
            bus.subscribe(KernelEvent.MODULE_REGISTERED, handler)

    def test_unsubscribe_remove_handler(self, bus: KernelEventBus) -> None:
        calls: list[int] = []
        handler: EventHandler = lambda e, d: calls.append(1)

        bus.subscribe(KernelEvent.MODULE_STARTED, handler)
        bus.unsubscribe(KernelEvent.MODULE_STARTED, handler)
        bus.publish(KernelEvent.MODULE_STARTED)
        assert calls == []

    def test_unsubscribe_handler_nao_registrado_levanta_erro(
        self, bus: KernelEventBus
    ) -> None:
        with pytest.raises(ValueError, match="handler não registrado"):
            bus.unsubscribe(KernelEvent.MODULE_STARTED, lambda e, d: None)

    def test_handlers_for_retorna_tuple(self, bus: KernelEventBus) -> None:
        h1: EventHandler = lambda e, d: None
        h2: EventHandler = lambda e, d: None
        bus.subscribe(KernelEvent.MODULE_REGISTERED, h1)
        bus.subscribe(KernelEvent.MODULE_REGISTERED, h2)
        result = bus.handlers_for(KernelEvent.MODULE_REGISTERED)
        assert isinstance(result, tuple)
        assert h1 in result
        assert h2 in result

    def test_handlers_for_evento_sem_subscritors(self, bus: KernelEventBus) -> None:
        assert bus.handlers_for(KernelEvent.MODULE_DISCOVERED) == ()

    def test_handlers_for_imutavel(self, bus: KernelEventBus) -> None:
        h: EventHandler = lambda e, d: None
        bus.subscribe(KernelEvent.STATE_CHANGED, h)
        snapshot = bus.handlers_for(KernelEvent.STATE_CHANGED)
        # modificar a tupla retornada não afeta o bus
        assert len(snapshot) == 1


# ---------------------------------------------------------------------------
# publish
# ---------------------------------------------------------------------------

class TestPublish:
    def test_publish_sem_data_passa_dict_vazio(self, bus: KernelEventBus) -> None:
        received: list[dict] = []
        bus.subscribe(KernelEvent.MODULE_STARTED, lambda e, d: received.append(d))
        bus.publish(KernelEvent.MODULE_STARTED)
        assert received == [{}]

    def test_publish_com_data_repassa_copia(self, bus: KernelEventBus) -> None:
        received: list[dict] = []
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: received.append(d))

        original = {"name": "runtime.parser"}
        bus.publish(KernelEvent.MODULE_REGISTERED, original)

        assert received[0]["name"] == "runtime.parser"
        # modificar o dict recebido não altera o original
        received[0]["name"] = "alterado"
        assert original["name"] == "runtime.parser"

    def test_publish_retorna_contagem_de_handlers(self, bus: KernelEventBus) -> None:
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        count = bus.publish(KernelEvent.STATE_CHANGED)
        assert count == 2

    def test_publish_sem_handlers_retorna_zero(self, bus: KernelEventBus) -> None:
        assert bus.publish(KernelEvent.MODULE_FAILED) == 0

    def test_publish_continua_apos_erro_em_handler(
        self, bus: KernelEventBus
    ) -> None:
        calls: list[int] = []

        def handler_com_erro(e: KernelEvent, d: dict) -> None:
            raise RuntimeError("erro intencional")

        def handler_ok(e: KernelEvent, d: dict) -> None:
            calls.append(1)

        bus.subscribe(KernelEvent.MODULE_FAILED, handler_com_erro)
        bus.subscribe(KernelEvent.MODULE_FAILED, handler_ok)

        with pytest.raises(RuntimeError, match="erro intencional"):
            bus.publish(KernelEvent.MODULE_FAILED)

        # handler_ok ainda foi chamado
        assert calls == [1]

    def test_publish_sem_handlers_nao_levanta(self, bus: KernelEventBus) -> None:
        # não deve levantar mesmo sem nenhum handler registrado
        bus.publish(KernelEvent.CONTRACT_VALIDATED, {"ok": True})

    def test_publish_evento_correto_passado_ao_handler(
        self, bus: KernelEventBus
    ) -> None:
        received_events: list[KernelEvent] = []
        bus.subscribe(
            KernelEvent.DEPENDENCY_RESOLVED,
            lambda e, d: received_events.append(e),
        )
        bus.publish(KernelEvent.DEPENDENCY_RESOLVED)
        assert received_events == [KernelEvent.DEPENDENCY_RESOLVED]


# ---------------------------------------------------------------------------
# history
# ---------------------------------------------------------------------------

class TestHistory:
    def test_history_vazio_inicialmente(self, bus: KernelEventBus) -> None:
        assert bus.history() == []

    def test_history_registra_publicacoes(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "a"})
        bus.publish(KernelEvent.STATE_CHANGED, {"from": "created", "to": "initialized"})
        h = bus.history()
        assert len(h) == 2
        assert h[0][0] == KernelEvent.MODULE_REGISTERED
        assert h[1][0] == KernelEvent.STATE_CHANGED

    def test_history_filtra_por_evento(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "a"})
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "b"})
        bus.publish(KernelEvent.STATE_CHANGED)

        filtered = bus.history(KernelEvent.MODULE_REGISTERED)
        assert len(filtered) == 2
        assert all(e == KernelEvent.MODULE_REGISTERED for e, _ in filtered)

    def test_history_retorna_copia(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_STARTED)
        h1 = bus.history()
        h1.append(("extra", {}))  # type: ignore[arg-type]
        h2 = bus.history()
        assert len(h2) == 1

    def test_clear_history(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.clear_history()
        assert bus.history() == []

    def test_clear_history_nao_remove_handlers(self, bus: KernelEventBus) -> None:
        calls: list[int] = []
        bus.subscribe(KernelEvent.MODULE_STARTED, lambda e, d: calls.append(1))
        bus.clear_history()
        bus.publish(KernelEvent.MODULE_STARTED)
        assert calls == [1]

    def test_historico_mesmo_sem_handlers(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_DISCOVERED, {"source": "test"})
        h = bus.history()
        assert len(h) == 1
        assert h[0][1] == {"source": "test"}


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_limpa_handlers_e_historico(self, bus: KernelEventBus) -> None:
        calls: list[int] = []
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: calls.append(1))
        bus.publish(KernelEvent.STATE_CHANGED)
        bus.reset()
        # após reset: handlers removidos e histórico limpo
        assert bus.history() == []
        assert bus.handlers_for(KernelEvent.STATE_CHANGED) == ()
        # nova publicação não chama o handler removido
        bus.publish(KernelEvent.STATE_CHANGED)
        assert calls == [1]  # chamado apenas antes do reset


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_bus_vazio(self, bus: KernelEventBus) -> None:
        s = bus.stats()
        assert s["total_handlers"] == 0
        assert s["total_events_published"] == 0

    def test_stats_conta_handlers(self, bus: KernelEventBus) -> None:
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        bus.subscribe(KernelEvent.MODULE_REGISTERED, lambda e, d: None)
        bus.subscribe(KernelEvent.STATE_CHANGED, lambda e, d: None)
        s = bus.stats()
        assert s["total_handlers"] == 3
        assert s["event_module_registered_handlers"] == 2
        assert s["event_state_changed_handlers"] == 1

    def test_stats_conta_publicacoes(self, bus: KernelEventBus) -> None:
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.publish(KernelEvent.MODULE_STARTED)
        bus.publish(KernelEvent.MODULE_STOPPED)
        s = bus.stats()
        assert s["total_events_published"] == 3
        assert s["event_module_started_published"] == 2
        assert s["event_module_stopped_published"] == 1

    def test_stats_todos_valores_sao_int(self, bus: KernelEventBus) -> None:
        for v in bus.stats().values():
            assert isinstance(v, int)

    def test_stats_tem_entradas_para_todos_os_eventos(
        self, bus: KernelEventBus
    ) -> None:
        s = bus.stats()
        for ev in KernelEvent:
            key = ev.value.replace(".", "_")
            assert f"event_{key}_handlers" in s
            assert f"event_{key}_published" in s


# ---------------------------------------------------------------------------
# Integração: MicroKernel publica eventos
# ---------------------------------------------------------------------------

class TestMicroKernelIntegracao:
    def _modulo_basico(self, name: str = "test.modulo") -> ModuleContract:
        return ModuleContract(name=name, provides=(name.replace(".", "_"),))

    def test_kernel_tem_barramento_de_eventos(self, kernel: MicroKernel) -> None:
        assert isinstance(kernel.events, KernelEventBus)

    def test_register_publica_module_registered(self, kernel: MicroKernel) -> None:
        registrados: list[str] = []

        def on_registered(e: KernelEvent, d: dict) -> None:
            registrados.append(d.get("name", ""))

        kernel.events.subscribe(KernelEvent.MODULE_REGISTERED, on_registered)
        kernel.register(self._modulo_basico("runtime.x"))
        assert "runtime.x" in registrados

    def test_initialize_publica_contract_validated(self, kernel: MicroKernel) -> None:
        validated: list[bool] = []
        kernel.events.subscribe(
            KernelEvent.CONTRACT_VALIDATED,
            lambda e, d: validated.append(True),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        assert validated == [True]

    def test_initialize_publica_dependency_resolved(self, kernel: MicroKernel) -> None:
        resolved: list[list] = []
        kernel.events.subscribe(
            KernelEvent.DEPENDENCY_RESOLVED,
            lambda e, d: resolved.append(d.get("order", [])),
        )
        kernel.register(self._modulo_basico("mod.a"))
        kernel.initialize()
        assert len(resolved) == 1
        assert "mod.a" in resolved[0]

    def test_initialize_publica_state_changed(self, kernel: MicroKernel) -> None:
        transicoes: list[dict] = []
        kernel.events.subscribe(
            KernelEvent.STATE_CHANGED,
            lambda e, d: transicoes.append(dict(d)),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        assert len(transicoes) >= 1
        # a última transição deve chegar a "initialized"
        assert transicoes[-1]["to"] == "initialized"

    def test_start_publica_module_started(self, kernel: MicroKernel) -> None:
        iniciados: list[bool] = []
        kernel.events.subscribe(
            KernelEvent.MODULE_STARTED,
            lambda e, d: iniciados.append(True),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        kernel.start()
        assert iniciados == [True]

    def test_start_publica_state_changed_para_running(
        self, kernel: MicroKernel
    ) -> None:
        estados: list[str] = []
        kernel.events.subscribe(
            KernelEvent.STATE_CHANGED,
            lambda e, d: estados.append(d.get("to", "")),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        kernel.start()
        assert "running" in estados

    def test_stop_publica_module_stopped(self, kernel: MicroKernel) -> None:
        parados: list[bool] = []
        kernel.events.subscribe(
            KernelEvent.MODULE_STOPPED,
            lambda e, d: parados.append(True),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        kernel.start()
        kernel.stop()
        assert parados == [True]

    def test_stop_publica_state_changed_para_stopped(
        self, kernel: MicroKernel
    ) -> None:
        estados: list[str] = []
        kernel.events.subscribe(
            KernelEvent.STATE_CHANGED,
            lambda e, d: estados.append(d.get("to", "")),
        )
        kernel.register(self._modulo_basico())
        kernel.initialize()
        kernel.start()
        kernel.stop()
        assert "stopped" in estados

    def test_historico_completo_ciclo_de_vida(self, kernel: MicroKernel) -> None:
        """Ciclo completo register → initialize → start → stop."""
        kernel.register(self._modulo_basico())
        kernel.initialize()
        kernel.start()
        kernel.stop()

        h = kernel.events.history()
        tipos = [e for e, _ in h]

        assert KernelEvent.MODULE_REGISTERED in tipos
        assert KernelEvent.CONTRACT_VALIDATED in tipos
        assert KernelEvent.DEPENDENCY_RESOLVED in tipos
        assert KernelEvent.STATE_CHANGED in tipos
        assert KernelEvent.MODULE_STARTED in tipos
        assert KernelEvent.MODULE_STOPPED in tipos

    def test_multiplos_registros_geram_multiplos_eventos(
        self, kernel: MicroKernel
    ) -> None:
        nomes: list[str] = []
        kernel.events.subscribe(
            KernelEvent.MODULE_REGISTERED,
            lambda e, d: nomes.append(d["name"]),
        )
        kernel.register(ModuleContract(name="mod.a", provides=("a",)))
        kernel.register(ModuleContract(name="mod.b", provides=("b",)))
        assert nomes == ["mod.a", "mod.b"]

    def test_kernel_retrocompativel_sem_subscricao(self) -> None:
        """Kernel funciona normalmente mesmo sem nenhum subscriber."""
        k = MicroKernel()
        k.register(ModuleContract(name="mod.solo", provides=("solo",)))
        k.initialize()
        k.start()
        k.stop()
        assert k.state.value == "stopped"
