"""Testes de integração — ciclo completo do microkernel.

Cobre: bootstrap → register → initialize → start → stop
Verifica estado em cada etapa, persistência de módulos e eventos de lifecycle.
"""
from __future__ import annotations

import pytest

from kernel.bootstrap import bootstrap_system, build_kernel
from kernel.contracts.module import ModuleContract
from kernel.core.kernel import MicroKernel
from kernel.events.bus import KernelEvent
from kernel.lifecycle.manager import LifecycleState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_contract(name: str, provides: tuple[str, ...] | None = None) -> ModuleContract:
    """Cria um ModuleContract mínimo e válido."""
    cap = provides if provides is not None else (name.replace(".", "_"),)
    return ModuleContract(name=name, provides=cap)


def _fresh_kernel() -> MicroKernel:
    """Retorna um MicroKernel novo sem módulos."""
    return MicroKernel()


# ---------------------------------------------------------------------------
# Teste 1 — estado inicial: CREATED
# ---------------------------------------------------------------------------

class TestEstadoInicial:
    def test_kernel_inicia_em_created(self) -> None:
        k = _fresh_kernel()
        assert k.state == LifecycleState.CREATED

    def test_estado_e_lifecycle_state(self) -> None:
        k = _fresh_kernel()
        assert isinstance(k.state, LifecycleState)

    def test_registry_inicia_vazio(self) -> None:
        k = _fresh_kernel()
        assert k.registry.contracts() == ()

    def test_eventos_historico_vazio(self) -> None:
        k = _fresh_kernel()
        assert k.events.history() == []

    def test_services_lista_vazia(self) -> None:
        k = _fresh_kernel()
        assert k.services.list_services() == []


# ---------------------------------------------------------------------------
# Teste 2 — register: módulo persiste no registry
# ---------------------------------------------------------------------------

class TestRegister:
    def test_register_persiste_contrato(self) -> None:
        k = _fresh_kernel()
        c = _make_contract("mod.a")
        k.register(c)
        assert k.registry.get("mod.a") is c

    def test_register_multiplos_modulos(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.register(_make_contract("mod.b"))
        nomes = {c.name for c in k.registry.contracts()}
        assert {"mod.a", "mod.b"} == nomes

    def test_register_publica_evento_module_registered(self) -> None:
        k = _fresh_kernel()
        capturados: list[str] = []
        k.events.subscribe(KernelEvent.MODULE_REGISTERED,
                           lambda e, d: capturados.append(d["name"]))
        k.register(_make_contract("mod.x"))
        assert "mod.x" in capturados

    def test_register_nao_altera_estado_lifecycle(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        assert k.state == LifecycleState.CREATED


# ---------------------------------------------------------------------------
# Teste 3 — initialize: estado muda para INITIALIZED
# ---------------------------------------------------------------------------

class TestInitialize:
    def test_initialize_muda_estado_para_initialized(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        assert k.state == LifecycleState.INITIALIZED

    def test_initialize_publica_state_changed(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        estados_destino: list[str] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: estados_destino.append(d["to"]))
        k.initialize()
        assert "initialized" in estados_destino

    def test_modulos_persistem_apos_initialize(self) -> None:
        k = _fresh_kernel()
        c = _make_contract("mod.a")
        k.register(c)
        k.initialize()
        assert k.registry.get("mod.a") is c


# ---------------------------------------------------------------------------
# Teste 4 — start: estado muda para RUNNING
# ---------------------------------------------------------------------------

class TestStart:
    def test_start_apos_initialize_muda_estado_para_running(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        assert k.state == LifecycleState.RUNNING

    def test_start_publica_state_changed_para_running(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        estados: list[str] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: estados.append(d["to"]))
        k.start()
        assert "running" in estados

    def test_start_publica_module_started(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        iniciados: list[bool] = []
        k.events.subscribe(KernelEvent.MODULE_STARTED,
                           lambda e, d: iniciados.append(True))
        k.start()
        assert iniciados == [True]

    def test_modulos_persistem_apos_start(self) -> None:
        k = _fresh_kernel()
        c = _make_contract("mod.a")
        k.register(c)
        k.initialize()
        k.start()
        assert k.registry.get("mod.a") is c

    def test_start_a_partir_de_created_faz_initialize_automatico(self) -> None:
        """MicroKernel.start() chama initialize() se estado for CREATED."""
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.start()  # CREATED → (auto-initialize) → RUNNING
        assert k.state == LifecycleState.RUNNING


# ---------------------------------------------------------------------------
# Teste 5 — stop: estado muda para STOPPED
# ---------------------------------------------------------------------------

class TestStop:
    def test_stop_muda_estado_para_stopped(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        assert k.state == LifecycleState.STOPPED

    def test_stop_publica_state_changed_para_stopped(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        estados: list[str] = []
        k.events.subscribe(KernelEvent.STATE_CHANGED,
                           lambda e, d: estados.append(d["to"]))
        k.stop()
        assert "stopped" in estados

    def test_stop_publica_module_stopped(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        parados: list[bool] = []
        k.events.subscribe(KernelEvent.MODULE_STOPPED,
                           lambda e, d: parados.append(True))
        k.stop()
        assert parados == [True]

    def test_modulos_persistem_apos_stop(self) -> None:
        k = _fresh_kernel()
        c = _make_contract("mod.a")
        k.register(c)
        k.initialize()
        k.start()
        k.stop()
        assert k.registry.get("mod.a") is c

    def test_stop_sem_start_a_partir_de_initialized(self) -> None:
        """INITIALIZED → STOPPING → STOPPED é uma transição permitida."""
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.stop()
        assert k.state == LifecycleState.STOPPED


# ---------------------------------------------------------------------------
# Teste 6 — re-start após stop (via restart())
# ---------------------------------------------------------------------------

class TestRestart:
    def test_restart_apos_stop_retorna_initialized(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        k.lifecycle.restart()
        assert k.state == LifecycleState.INITIALIZED

    def test_restart_permite_segundo_start(self) -> None:
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        k.lifecycle.restart()
        k.start()
        assert k.state == LifecycleState.RUNNING

    def test_start_direto_apos_stop_levanta_excecao(self) -> None:
        """STOPPED não permite ir diretamente para STARTING."""
        from kernel.lifecycle.manager import LifecycleError
        k = _fresh_kernel()
        k.register(_make_contract("mod.a"))
        k.initialize()
        k.start()
        k.stop()
        # MicroKernel.start() chama lifecycle.start() que requer INITIALIZED
        # STOPPED → STARTING é inválido (precisa de restart primeiro)
        with pytest.raises(LifecycleError):
            k.start()


# ---------------------------------------------------------------------------
# Teste 7 — bootstrap_system() retorna kernel funcional
# ---------------------------------------------------------------------------

class TestBootstrapSystem:
    def test_bootstrap_system_retorna_microkernel(self) -> None:
        k = bootstrap_system()
        assert isinstance(k, MicroKernel)

    def test_bootstrap_system_estado_initialized(self) -> None:
        k = bootstrap_system()
        assert k.state == LifecycleState.INITIALIZED

    def test_bootstrap_system_tem_modulos_padrao(self) -> None:
        from kernel.bootstrap import DEFAULT_MODULES
        k = bootstrap_system()
        nomes_registrados = {c.name for c in k.registry.contracts()}
        for m in DEFAULT_MODULES:
            assert m.name in nomes_registrados

    def test_bootstrap_system_aceita_modulos_extras(self) -> None:
        extra = _make_contract("extra.modulo")
        k = bootstrap_system(extra_modules=(extra,))
        assert k.registry.get("extra.modulo") is not None

    def test_bootstrap_system_retorna_kernel_funcional_para_start(self) -> None:
        k = bootstrap_system()
        k.start()
        assert k.state == LifecycleState.RUNNING
        k.stop()
        assert k.state == LifecycleState.STOPPED

    def test_bootstrap_system_kernel_independente_por_chamada(self) -> None:
        """Cada chamada retorna uma instância independente."""
        k1 = bootstrap_system()
        k2 = bootstrap_system()
        assert k1 is not k2
        assert k1.registry is not k2.registry
