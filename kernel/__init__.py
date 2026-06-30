"""Microkernel estrutural do SOE-CCG."""

from .bootstrap import bootstrap_system
from .contracts import ModuleContract
from .core import MicroKernel

__all__ = ["MicroKernel", "ModuleContract", "bootstrap_system"]
