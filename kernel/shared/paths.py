"""Caminhos canônicos do projeto SOE-CCG."""
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = PROJECT_ROOT

KERNEL = PROJECT_ROOT / "kernel"
KERNEL_DOCS = PROJECT_ROOT / "kernel-docs"
CODIGO = PROJECT_ROOT / "codigo"
DADOS = PROJECT_ROOT / "dados"
DOCS = PROJECT_ROOT / "docs"
BANCO_DE_DADOS = PROJECT_ROOT / "banco_de_dados"
SCRIPTS = PROJECT_ROOT / "scripts"
SCRIPTS_FAA = SCRIPTS / "faa"
SCRIPTS_AUDITORIA = SCRIPTS / "auditoria"
TESTES = PROJECT_ROOT / "testes"
CONSTITUICAO = DOCS / "00-projeto" / "constituicao-v1.md"


def project_path(*parts: str) -> Path:
    """Retorna um caminho absoluto dentro da raiz do projeto."""
    return PROJECT_ROOT.joinpath(*parts)


__all__ = [
    "PROJECT_ROOT",
    "ROOT",
    "KERNEL",
    "KERNEL_DOCS",
    "CODIGO",
    "DADOS",
    "DOCS",
    "BANCO_DE_DADOS",
    "SCRIPTS",
    "SCRIPTS_FAA",
    "SCRIPTS_AUDITORIA",
    "TESTES",
    "CONSTITUICAO",
    "project_path",
]
