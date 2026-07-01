"""Inspector: inspeção detalhada do estado do Kernel."""
from __future__ import annotations

from typing import Any


def inspect_kernel(kernel) -> dict[str, Any]:
    """Retorna snapshot completo do estado do Kernel.

    Args:
        kernel: Instância de MicroKernel a ser inspecionada.

    Returns:
        Dicionário com estado completo incluindo:
        - lifecycle: estado atual
        - registry: contratos, dependências, health
        - services: lista, health
        - events: handlers, histórico, estatísticas
    """
    return {
        "lifecycle": {
            "state": kernel.state.value,
        },
        "registry": {
            "contracts": [
                {
                    "name": c.name,
                    "version": c.version,
                    "type": c.type,
                    "category": c.category,
                    "state": c.state,
                    "provides": list(c.provides),
                    "requires": list(c.requires),
                }
                for c in kernel.registry.contracts()
            ],
            "dependency_graph": kernel.registry.dependency_graph(),
            "health": kernel.registry.health(),
            "stats": kernel.registry.stats(),
        },
        "services": {
            "list": kernel.services.list_services(),
            "health": kernel.services.all_health(),
            "stats": kernel.services.stats(),
        },
        "events": {
            "handlers": {
                event_name: len(kernel.events.handlers_for(event_name))
                for event_name in kernel.events.stats().keys()
            },
            "history_size": len(kernel.events.history()),
            "stats": kernel.events.stats(),
        },
    }


def inspect_registry(kernel) -> dict[str, Any]:
    """Inspeciona apenas o ModuleRegistry.

    Args:
        kernel: Instância de MicroKernel.

    Returns:
        Estado completo do registry.
    """
    return {
        "total_modules": len(kernel.registry.contracts()),
        "modules": [c.name for c in kernel.registry.contracts()],
        "dependency_graph": kernel.registry.dependency_graph(),
        "health": kernel.registry.health(),
        "stats": kernel.registry.stats(),
    }


def inspect_services(kernel) -> dict[str, Any]:
    """Inspeciona apenas o ServiceRegistry.

    Args:
        kernel: Instância de MicroKernel.

    Returns:
        Estado completo dos serviços.
    """
    return {
        "services": kernel.services.list_services(),
        "health": kernel.services.all_health(),
        "stats": kernel.services.stats(),
    }


def inspect_events(kernel) -> dict[str, Any]:
    """Inspeciona apenas o KernelEventBus.

    Args:
        kernel: Instância de MicroKernel.

    Returns:
        Estado completo do barramento de eventos.
    """
    from kernel.events.bus import KernelEvent

    return {
        "handlers_by_event": {
            event.value: len(kernel.events.handlers_for(event))
            for event in KernelEvent
        },
        "history": [
            {"event": event.value, "data": data}
            for event, data in kernel.events.history()
        ],
        "stats": kernel.events.stats(),
    }


__all__ = [
    "inspect_kernel",
    "inspect_registry",
    "inspect_services",
    "inspect_events",
]
