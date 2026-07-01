"""Microkernel estrutural do SOE-CCG."""

from .bootstrap import bootstrap_system
from .contracts import ModuleContract
from .core import MicroKernel
from .events import KernelEvent, KernelEventBus
from .services import ServiceError, ServiceRegistry

__all__ = [
    "KernelEvent",
    "KernelEventBus",
    "MicroKernel",
    "ModuleContract",
    "ServiceError",
    "ServiceRegistry",
    "bootstrap_system",
]
