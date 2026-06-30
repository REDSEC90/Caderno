"""Máquina de estados mínima do microkernel."""
from __future__ import annotations

from enum import Enum


class LifecycleError(RuntimeError):
    """Transição inválida no ciclo de vida do kernel."""


class LifecycleState(str, Enum):
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"


class KernelLifecycle:
    """Controla transições determinísticas de inicialização e execução."""

    def __init__(self) -> None:
        self.state = LifecycleState.CREATED

    def initialize(self) -> None:
        self._transition(LifecycleState.CREATED, LifecycleState.INITIALIZED)

    def start(self) -> None:
        self._transition(LifecycleState.INITIALIZED, LifecycleState.RUNNING)

    def stop(self) -> None:
        if self.state not in (LifecycleState.INITIALIZED, LifecycleState.RUNNING):
            raise LifecycleError(f"não é possível parar a partir de {self.state.value}")
        self.state = LifecycleState.STOPPED

    def _transition(self, expected: LifecycleState, target: LifecycleState) -> None:
        if self.state != expected:
            raise LifecycleError(
                f"transição inválida: {self.state.value} -> {target.value}"
            )
        self.state = target
