"""Contrato declarativo para módulos registrados no microkernel."""
from __future__ import annotations

from dataclasses import dataclass, field


class ContractError(ValueError):
    """Erro de contrato detectado antes da inicialização de módulos."""


@dataclass(frozen=True)
class ModuleContract:
    """Descrição estrutural de um módulo sem importar sua implementação."""

    name: str
    version: str = "1"
    provides: tuple[str, ...] = field(default_factory=tuple)
    requires: tuple[str, ...] = field(default_factory=tuple)
    entrypoint: str | None = None
    description: str = ""

    def validate(self) -> None:
        if not self.name:
            raise ContractError("ModuleContract.name é obrigatório")
        if not self.version:
            raise ContractError(f"{self.name}: version é obrigatório")
        if not self.provides:
            raise ContractError(f"{self.name}: provides deve declarar ao menos uma capacidade")
        duplicated = set(self.provides).intersection(self.requires)
        if duplicated:
            names = ", ".join(sorted(duplicated))
            raise ContractError(f"{self.name}: capacidade simultaneamente provides/requires: {names}")
