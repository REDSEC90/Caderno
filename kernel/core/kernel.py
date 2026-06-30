"""Microkernel estrutural do SOE-CCG."""
from __future__ import annotations

from kernel.contracts.module import ModuleContract
from kernel.lifecycle import KernelLifecycle, LifecycleState
from kernel.registry import ModuleRegistry


class MicroKernel:
    """Coordena contratos, registry e ciclo de vida sem regra de negócio."""

    def __init__(self) -> None:
        self.registry = ModuleRegistry()
        self.lifecycle = KernelLifecycle()

    @property
    def state(self) -> LifecycleState:
        return self.lifecycle.state

    def register(self, contract: ModuleContract) -> None:
        self.registry.register(contract)

    def initialize(self) -> None:
        self.registry.validate()
        self.lifecycle.initialize()

    def start(self) -> None:
        if self.lifecycle.state == LifecycleState.CREATED:
            self.initialize()
        self.lifecycle.start()

    def stop(self) -> None:
        self.lifecycle.stop()

    def startup_order(self) -> tuple[ModuleContract, ...]:
        return tuple(self.registry.resolve_order())
