"""Máquina de estados expandida do microkernel."""
from __future__ import annotations

from enum import Enum


class LifecycleError(RuntimeError):
    """Transição inválida no ciclo de vida do kernel."""


class LifecycleState(str, Enum):
    """Estados do ciclo de vida do Kernel."""
    
    # Estados estáveis
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FAILED = "failed"
    DISABLED = "disabled"
    
    # Estados transitórios
    INITIALIZING = "initializing"
    STARTING = "starting"
    PAUSING = "pausing"
    RESUMING = "resuming"
    STOPPING = "stopping"
    RESTARTING = "restarting"
    RECOVERING = "recovering"


class KernelLifecycle:
    """Controla transições determinísticas de inicialização e execução."""

    # Matriz de transições permitidas
    _TRANSITIONS: dict[LifecycleState, set[LifecycleState]] = {
        LifecycleState.CREATED: {
            LifecycleState.INITIALIZING,
        },
        LifecycleState.INITIALIZING: {
            LifecycleState.INITIALIZED,
            LifecycleState.FAILED,
        },
        LifecycleState.INITIALIZED: {
            LifecycleState.STARTING,
            LifecycleState.STOPPING,
        },
        LifecycleState.STARTING: {
            LifecycleState.RUNNING,
            LifecycleState.FAILED,
        },
        LifecycleState.RUNNING: {
            LifecycleState.PAUSING,
            LifecycleState.STOPPING,
            LifecycleState.FAILED,
        },
        LifecycleState.PAUSING: {
            LifecycleState.PAUSED,
            LifecycleState.FAILED,
        },
        LifecycleState.PAUSED: {
            LifecycleState.RESUMING,
            LifecycleState.STOPPING,
        },
        LifecycleState.RESUMING: {
            LifecycleState.RUNNING,
            LifecycleState.FAILED,
        },
        LifecycleState.STOPPING: {
            LifecycleState.STOPPED,
            LifecycleState.FAILED,
        },
        LifecycleState.STOPPED: {
            LifecycleState.RESTARTING,
            LifecycleState.DISABLED,
        },
        LifecycleState.RESTARTING: {
            LifecycleState.INITIALIZED,
            LifecycleState.FAILED,
        },
        LifecycleState.FAILED: {
            LifecycleState.RECOVERING,
            LifecycleState.DISABLED,
        },
        LifecycleState.RECOVERING: {
            LifecycleState.INITIALIZED,
            LifecycleState.FAILED,
        },
        LifecycleState.DISABLED: set(),  # Estado terminal
    }

    # Estados estáveis (permanecem até ação explícita)
    _STABLE_STATES = {
        LifecycleState.CREATED,
        LifecycleState.INITIALIZED,
        LifecycleState.RUNNING,
        LifecycleState.PAUSED,
        LifecycleState.STOPPED,
        LifecycleState.FAILED,
        LifecycleState.DISABLED,
    }

    def __init__(self) -> None:
        self.state = LifecycleState.CREATED

    # === MÉTODOS PÚBLICOS DE TRANSIÇÃO ===

    def initialize(self) -> None:
        """CREATED → INITIALIZING → INITIALIZED."""
        self._transition_to(LifecycleState.INITIALIZING)
        # Aqui executaria lógica de inicialização
        self._transition_to(LifecycleState.INITIALIZED)

    def start(self) -> None:
        """INITIALIZED → STARTING → RUNNING."""
        self._transition_to(LifecycleState.STARTING)
        # Aqui executaria lógica de start
        self._transition_to(LifecycleState.RUNNING)

    def pause(self) -> None:
        """RUNNING → PAUSING → PAUSED."""
        self._transition_to(LifecycleState.PAUSING)
        # Aqui executaria lógica de pause
        self._transition_to(LifecycleState.PAUSED)

    def resume(self) -> None:
        """PAUSED → RESUMING → RUNNING."""
        self._transition_to(LifecycleState.RESUMING)
        # Aqui executaria lógica de resume
        self._transition_to(LifecycleState.RUNNING)

    def stop(self) -> None:
        """RUNNING/PAUSED/INITIALIZED → STOPPING → STOPPED."""
        self._transition_to(LifecycleState.STOPPING)
        # Aqui executaria lógica de stop
        self._transition_to(LifecycleState.STOPPED)

    def restart(self) -> None:
        """STOPPED → RESTARTING → INITIALIZED."""
        self._transition_to(LifecycleState.RESTARTING)
        # Aqui executaria lógica de restart
        self._transition_to(LifecycleState.INITIALIZED)

    def recover(self) -> None:
        """FAILED → RECOVERING → INITIALIZED."""
        self._transition_to(LifecycleState.RECOVERING)
        # Aqui executaria lógica de recuperação
        self._transition_to(LifecycleState.INITIALIZED)

    def disable(self) -> None:
        """FAILED/STOPPED → DISABLED."""
        self._transition_to(LifecycleState.DISABLED)

    def fail(self, reason: str = "") -> None:
        """Qualquer estado → FAILED."""
        if self.state == LifecycleState.DISABLED:
            raise LifecycleError("Não é possível falhar a partir de DISABLED")
        self.state = LifecycleState.FAILED

    # === MÉTODOS DE CONSULTA ===

    def is_stable(self) -> bool:
        """Retorna True se está em estado estável."""
        return self.state in self._STABLE_STATES

    def is_transitioning(self) -> bool:
        """Retorna True se está em estado transitório."""
        return not self.is_stable()

    def is_operational(self) -> bool:
        """Retorna True se está em RUNNING ou PAUSED."""
        return self.state in (LifecycleState.RUNNING, LifecycleState.PAUSED)

    def is_terminal(self) -> bool:
        """Retorna True se está em DISABLED."""
        return self.state == LifecycleState.DISABLED

    def can_transition_to(self, target: LifecycleState) -> bool:
        """Retorna True se pode transitar para o estado alvo."""
        allowed = self._TRANSITIONS.get(self.state, set())
        return target in allowed

    # === MÉTODOS INTERNOS ===

    def _transition_to(self, target: LifecycleState) -> None:
        """Executa transição validada para o estado alvo."""
        if not self.can_transition_to(target):
            raise LifecycleError(
                f"Transição inválida: {self.state.value} → {target.value}"
            )
        self.state = target
