from __future__ import annotations

import re

import pytest

from kernel.bootstrap import bootstrap_system
from kernel.contracts import ModuleContract, validate_architecture
from kernel.registry import ModuleRegistry, RegistryError
from kernel.shared.paths import KERNEL_DOCS, PROJECT_ROOT


def test_bootstrap_registra_modulos_padrao() -> None:
    kernel = bootstrap_system()
    contratos = {contract.name: contract for contract in kernel.registry.contracts()}

    assert kernel.state.value == "initialized"
    assert "kernel.paths" in contratos
    assert "runtime.parser" in contratos
    assert "application.cli" in contratos


def test_registry_resolve_dependencias_em_ordem() -> None:
    registry = ModuleRegistry()
    registry.register(ModuleContract(name="b", provides=("b",), requires=("a",)))
    registry.register(ModuleContract(name="a", provides=("a",)))

    assert [contract.name for contract in registry.resolve_order()] == ["a", "b"]


def test_registry_bloqueia_dependencia_ausente() -> None:
    registry = ModuleRegistry()
    registry.register(ModuleContract(name="b", provides=("b",), requires=("a",)))

    with pytest.raises(RegistryError):
        registry.validate()


def test_root_local_nao_e_redefinido_fora_do_kernel_paths() -> None:
    pattern = re.compile(r"^\s*ROOT\s*=\s*Path\(__file__\)", re.MULTILINE)
    offenders: list[str] = []

    for path in PROJECT_ROOT.rglob("*.py"):
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        if relative == "kernel/shared/paths.py":
            continue
        if ".pytest_cache" in relative or "__pycache__" in relative:
            continue
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(relative)

    assert offenders == []


def test_motores_nao_injetam_sys_path_por_file_local() -> None:
    pattern = "__import__('pathlib').Path(__file__)"
    offenders: list[str] = []

    for base in (
        PROJECT_ROOT / "scripts" / "auditoria" / "motores",
        PROJECT_ROOT / "scripts" / "auditoria" / "relatorios",
    ):
        for path in base.glob("*.py"):
            if pattern in path.read_text(encoding="utf-8"):
                offenders.append(path.relative_to(PROJECT_ROOT).as_posix())

    assert offenders == []


def test_kernel_docs_obrigatorios_existem() -> None:
    esperados = {
        "00_constituicao-v1.md",
        "01_regras_fundamentais-v1.md",
        "02_invariantes-v1.md",
        "03_modelo_dependencias-v1.md",
        "04_regras_modulos-v1.md",
        "05_regras_kernel-v1.md",
        "06_politica_evolucao-v1.md",
        "07_protocolo_agentes-v1.md",
    }

    existentes = {path.name for path in KERNEL_DOCS.glob("*.md")}

    assert esperados.issubset(existentes)


def test_kernel_validator_aprova_arquitetura_atual() -> None:
    resultado = validate_architecture()

    assert resultado.errors == []
