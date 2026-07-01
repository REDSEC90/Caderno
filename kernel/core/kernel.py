"""Microkernel estrutural do SOE-CCG."""
from __future__ import annotations

from typing import Any

from kernel.contracts.module import ModuleContract
from kernel.events.bus import KernelEvent, KernelEventBus
from kernel.lifecycle import KernelLifecycle, LifecycleState
from kernel.registry import ModuleRegistry
from kernel.services import ServiceRegistry


class MicroKernel:
    """Coordena contratos, registry, ciclo de vida, eventos e serviços."""

    def __init__(self) -> None:
        self.registry = ModuleRegistry()
        self.lifecycle = KernelLifecycle()
        self.events = KernelEventBus()
        self.services = ServiceRegistry()

    @property
    def state(self) -> LifecycleState:
        return self.lifecycle.state

    def register(self, contract: ModuleContract) -> None:
        self.registry.register(contract)
        self.events.publish(
            KernelEvent.MODULE_REGISTERED,
            {"name": contract.name, "version": contract.version},
        )

    def initialize(self) -> None:
        self.registry.validate()
        self.events.publish(KernelEvent.CONTRACT_VALIDATED, {})

        order = self.registry.resolve_order()
        self.events.publish(
            KernelEvent.DEPENDENCY_RESOLVED,
            {"order": [c.name for c in order]},
        )

        prev_state = self.lifecycle.state
        self.lifecycle.initialize()
        self.events.publish(
            KernelEvent.STATE_CHANGED,
            {"from": prev_state.value, "to": self.lifecycle.state.value},
        )

    def start(self) -> None:
        if self.lifecycle.state == LifecycleState.CREATED:
            self.initialize()
        prev_state = self.lifecycle.state
        self.lifecycle.start()
        self.events.publish(
            KernelEvent.STATE_CHANGED,
            {"from": prev_state.value, "to": self.lifecycle.state.value},
        )
        self.events.publish(KernelEvent.MODULE_STARTED, {})

    def stop(self) -> None:
        prev_state = self.lifecycle.state
        self.lifecycle.stop()
        self.events.publish(
            KernelEvent.STATE_CHANGED,
            {"from": prev_state.value, "to": self.lifecycle.state.value},
        )
        self.events.publish(KernelEvent.MODULE_STOPPED, {})

    def startup_order(self) -> tuple[ModuleContract, ...]:
        return tuple(self.registry.resolve_order())

    # ------------------------------------------------------------------
    # API de serviços — delega ao ServiceRegistry com publicação de eventos
    # ------------------------------------------------------------------

    def register_service(self, name: str, instance: Any) -> None:
        """Registra uma instância de serviço e publica SERVICE_REGISTERED.

        Args:
            name: Identificador único do serviço.
            instance: Instância do serviço.

        Raises:
            ServiceError: Propagado diretamente do ServiceRegistry.
        """
        self.services.register_service(name, instance)
        self.events.publish(
            KernelEvent.SERVICE_REGISTERED,
            {"name": name, "type": type(instance).__name__},
        )

    def unregister_service(self, name: str) -> None:
        """Remove um serviço registrado e publica SERVICE_UNREGISTERED.

        Args:
            name: Identificador do serviço a remover.

        Raises:
            ServiceError: Propagado diretamente do ServiceRegistry.
        """
        self.services.unregister_service(name)
        self.events.publish(
            KernelEvent.SERVICE_UNREGISTERED,
            {"name": name},
        )

    def get_service(self, name: str) -> Any:
        """Retorna a instância do serviço registrado.

        Args:
            name: Identificador do serviço.

        Returns:
            Instância do serviço.

        Raises:
            ServiceError: Se o serviço não estiver registrado.
        """
        return self.services.get_service(name)
