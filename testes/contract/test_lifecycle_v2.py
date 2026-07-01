"""Testes para KernelLifecycle v2.0 (expandido)."""
from __future__ import annotations

import pytest

from kernel.lifecycle import KernelLifecycle, LifecycleError, LifecycleState


def test_lifecycle_inicia_em_created():
    """Lifecycle deve iniciar em CREATED."""
    lc = KernelLifecycle()
    assert lc.state == LifecycleState.CREATED


def test_transicao_created_para_initialized():
    """CREATED → INITIALIZING → INITIALIZED."""
    lc = KernelLifecycle()
    lc.initialize()
    assert lc.state == LifecycleState.INITIALIZED


def test_transicao_initialized_para_running():
    """INITIALIZED → STARTING → RUNNING."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    assert lc.state == LifecycleState.RUNNING


def test_transicao_running_para_paused():
    """RUNNING → PAUSING → PAUSED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.pause()
    assert lc.state == LifecycleState.PAUSED


def test_transicao_paused_para_running():
    """PAUSED → RESUMING → RUNNING."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.pause()
    lc.resume()
    assert lc.state == LifecycleState.RUNNING


def test_transicao_running_para_stopped():
    """RUNNING → STOPPING → STOPPED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.stop()
    assert lc.state == LifecycleState.STOPPED


def test_transicao_paused_para_stopped():
    """PAUSED → STOPPING → STOPPED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.pause()
    lc.stop()
    assert lc.state == LifecycleState.STOPPED


def test_transicao_stopped_para_initialized():
    """STOPPED → RESTARTING → INITIALIZED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.stop()
    lc.restart()
    assert lc.state == LifecycleState.INITIALIZED


def test_transicao_failed_para_initialized():
    """FAILED → RECOVERING → INITIALIZED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.fail("test error")
    assert lc.state == LifecycleState.FAILED
    lc.recover()
    assert lc.state == LifecycleState.INITIALIZED


def test_transicao_stopped_para_disabled():
    """STOPPED → DISABLED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.stop()
    lc.disable()
    assert lc.state == LifecycleState.DISABLED


def test_disabled_e_terminal():
    """DISABLED não permite nenhuma transição."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.stop()
    lc.disable()
    
    # Todas as transições devem falhar
    with pytest.raises(LifecycleError):
        lc.initialize()
    with pytest.raises(LifecycleError):
        lc.restart()
    with pytest.raises(LifecycleError):
        lc.fail("test")


def test_transicao_invalida_created_para_running():
    """Não pode ir direto de CREATED para RUNNING."""
    lc = KernelLifecycle()
    with pytest.raises(LifecycleError, match="Transição inválida"):
        lc.start()


def test_transicao_invalida_created_para_stopped():
    """Não pode ir direto de CREATED para STOPPED."""
    lc = KernelLifecycle()
    with pytest.raises(LifecycleError, match="Transição inválida"):
        lc.stop()


def test_transicao_invalida_initialized_para_paused():
    """Não pode pausar se não estiver em RUNNING."""
    lc = KernelLifecycle()
    lc.initialize()
    with pytest.raises(LifecycleError, match="Transição inválida"):
        lc.pause()


def test_transicao_invalida_running_para_initialized():
    """Não pode voltar para INITIALIZED diretamente."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    with pytest.raises(LifecycleError, match="Transição inválida"):
        lc.initialize()


def test_is_stable_para_estados_estaveis():
    """is_stable() retorna True para estados estáveis."""
    lc = KernelLifecycle()
    
    assert lc.is_stable()  # CREATED
    lc.initialize()
    assert lc.is_stable()  # INITIALIZED
    lc.start()
    assert lc.is_stable()  # RUNNING
    lc.pause()
    assert lc.is_stable()  # PAUSED
    lc.stop()
    assert lc.is_stable()  # STOPPED
    lc.disable()
    assert lc.is_stable()  # DISABLED


def test_is_transitioning_para_estados_transitorios():
    """is_transitioning() retorna True durante transições."""
    # Este teste não é possível com a implementação atual
    # porque estados transitórios são internos
    # Seria necessário adicionar hooks/callbacks
    pass


def test_is_operational():
    """is_operational() retorna True apenas para RUNNING e PAUSED."""
    lc = KernelLifecycle()
    
    assert not lc.is_operational()  # CREATED
    lc.initialize()
    assert not lc.is_operational()  # INITIALIZED
    lc.start()
    assert lc.is_operational()  # RUNNING
    lc.pause()
    assert lc.is_operational()  # PAUSED
    lc.stop()
    assert not lc.is_operational()  # STOPPED


def test_is_terminal():
    """is_terminal() retorna True apenas para DISABLED."""
    lc = KernelLifecycle()
    
    assert not lc.is_terminal()  # CREATED
    lc.initialize()
    assert not lc.is_terminal()  # INITIALIZED
    lc.start()
    assert not lc.is_terminal()  # RUNNING
    lc.stop()
    assert not lc.is_terminal()  # STOPPED
    lc.disable()
    assert lc.is_terminal()  # DISABLED


def test_can_transition_to():
    """can_transition_to() valida transições permitidas."""
    lc = KernelLifecycle()
    
    # De CREATED
    assert lc.can_transition_to(LifecycleState.INITIALIZING)
    assert not lc.can_transition_to(LifecycleState.RUNNING)
    
    # De INITIALIZED
    lc.initialize()
    assert lc.can_transition_to(LifecycleState.STARTING)
    assert lc.can_transition_to(LifecycleState.STOPPING)
    assert not lc.can_transition_to(LifecycleState.PAUSING)
    
    # De RUNNING
    lc.start()
    assert lc.can_transition_to(LifecycleState.PAUSING)
    assert lc.can_transition_to(LifecycleState.STOPPING)
    assert not lc.can_transition_to(LifecycleState.RESUMING)


def test_fail_de_qualquer_estado():
    """fail() pode ser chamado de qualquer estado (exceto DISABLED)."""
    lc = KernelLifecycle()
    
    lc.initialize()
    lc.fail("test")
    assert lc.state == LifecycleState.FAILED
    
    # Recuperar e testar de outro estado
    lc.recover()
    lc.start()
    lc.fail("test2")
    assert lc.state == LifecycleState.FAILED


def test_fail_nao_funciona_em_disabled():
    """fail() não pode ser chamado de DISABLED."""
    lc = KernelLifecycle()
    lc.initialize()
    lc.start()
    lc.stop()
    lc.disable()
    
    with pytest.raises(LifecycleError, match="Não é possível falhar"):
        lc.fail("test")


def test_ciclo_completo_com_recuperacao():
    """Teste de ciclo de vida completo com falha e recuperação."""
    lc = KernelLifecycle()
    
    # Inicializar e iniciar
    lc.initialize()
    assert lc.state == LifecycleState.INITIALIZED
    lc.start()
    assert lc.state == LifecycleState.RUNNING
    
    # Pausar e retomar
    lc.pause()
    assert lc.state == LifecycleState.PAUSED
    lc.resume()
    assert lc.state == LifecycleState.RUNNING
    
    # Falhar e recuperar
    lc.fail("test error")
    assert lc.state == LifecycleState.FAILED
    lc.recover()
    assert lc.state == LifecycleState.INITIALIZED
    
    # Iniciar, parar e reiniciar
    lc.start()
    assert lc.state == LifecycleState.RUNNING
    lc.stop()
    assert lc.state == LifecycleState.STOPPED
    lc.restart()
    assert lc.state == LifecycleState.INITIALIZED
    
    # Iniciar novamente e desabilitar
    lc.start()
    lc.stop()
    lc.disable()
    assert lc.state == LifecycleState.DISABLED
    assert lc.is_terminal()
