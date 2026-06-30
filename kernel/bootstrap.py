"""Bootstrap único do microkernel SOE-CCG."""
from __future__ import annotations

import sys

from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel
from kernel.shared.paths import PROJECT_ROOT


DEFAULT_MODULES: tuple[ModuleContract, ...] = (
    ModuleContract(
        name="runtime.ir",
        provides=("ir",),
        entrypoint="codigo.ir",
        description="Representação intermediária do grafo de conhecimento.",
    ),
    ModuleContract(
        name="runtime.parser",
        provides=("parser",),
        requires=("ir",),
        entrypoint="codigo.parser",
        description="Parser Markdown para KnowledgeGraph.",
    ),
    ModuleContract(
        name="runtime.resolver",
        provides=("resolver",),
        requires=("ir",),
        entrypoint="codigo.resolvedor",
        description="Resolvedor de referências entre entidades.",
    ),
    ModuleContract(
        name="runtime.validator",
        provides=("validator",),
        requires=("ir",),
        entrypoint="codigo.validador",
        description="Validação estrutural do grafo.",
    ),
    ModuleContract(
        name="runtime.importer",
        provides=("importer",),
        requires=("ir",),
        entrypoint="codigo.importador",
        description="Importação determinística para SQLite derivado.",
    ),
    ModuleContract(
        name="application.cli",
        provides=("cli",),
        requires=("parser", "resolver", "validator", "importer"),
        entrypoint="codigo.__main__",
        description="Aplicação terminal do runtime atual.",
    ),
    ModuleContract(
        name="application.faa",
        provides=("faa",),
        requires=("paths",),
        entrypoint="scripts.faa.faa",
        description="Pipeline FAA de auditoria arquitetural.",
    ),
    ModuleContract(
        name="kernel.paths",
        provides=("paths",),
        entrypoint="kernel.shared.paths",
        description="Fonte canônica de paths do projeto.",
    ),
)


def ensure_project_root_on_path() -> None:
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def build_kernel(extra_modules: tuple[ModuleContract, ...] = ()) -> MicroKernel:
    ensure_project_root_on_path()
    kernel = MicroKernel()
    for contract in DEFAULT_MODULES + extra_modules:
        kernel.register(contract)
    kernel.initialize()
    return kernel


def bootstrap_system(extra_modules: tuple[ModuleContract, ...] = ()) -> MicroKernel:
    """Inicializa o microkernel e valida contratos básicos."""
    return build_kernel(extra_modules=extra_modules)


__all__ = [
    "DEFAULT_MODULES",
    "bootstrap_system",
    "build_kernel",
    "ensure_project_root_on_path",
]
