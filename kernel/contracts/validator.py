"""Validador de contratos arquiteturais do SOE-CCG."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

from kernel.registry import ModuleRegistry, RegistryError
from kernel.shared.paths import KERNEL_DOCS, PROJECT_ROOT


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str | None = None
    severity: str = "error"


@dataclass
class ValidationResult:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, code: str, message: str, path: str | None = None, severity: str = "error") -> None:
        self.issues.append(ValidationIssue(code=code, message=message, path=path, severity=severity))

    def raise_for_errors(self) -> None:
        if self.ok:
            return
        detail = "; ".join(
            f"{issue.code}: {issue.path + ': ' if issue.path else ''}{issue.message}"
            for issue in self.errors
        )
        raise ArchitectureValidationError(detail)


class ArchitectureValidationError(RuntimeError):
    """Falha em contrato arquitetural enforceable."""


KERNEL_DOCS_REQUIRED = (
    "00_constituicao-v1.md",
    "01_regras_fundamentais-v1.md",
    "02_invariantes-v1.md",
    "03_modelo_dependencias-v1.md",
    "04_regras_modulos-v1.md",
    "05_regras_kernel-v1.md",
    "06_politica_evolucao-v1.md",
    "07_protocolo_agentes-v1.md",
)

ALLOWED_SYS_PATH_ADAPTERS = {
    "kernel/bootstrap.py",
    "scripts/faa/faa",
    "scripts/faa/config.py",
    "scripts/auditoria/auditor.py",
    "scripts/auditoria/config.py",
    "scripts/faa/tests/test_basic.py",
}

ROOT_REDEFINITION = re.compile(
    r"(?m)^\s*(ROOT|PROJECT_ROOT)\s*=\s*Path\(__file__\)"
)


def validate_architecture(root: Path = PROJECT_ROOT) -> ValidationResult:
    result = ValidationResult()
    _validate_kernel_docs(result)
    _validate_default_registry(result)
    _validate_single_root_source(root, result)
    _validate_kernel_isolation(root, result)
    _validate_sys_path_adapters(root, result)
    return result


def assert_architecture_valid(root: Path = PROJECT_ROOT) -> None:
    validate_architecture(root).raise_for_errors()


def _validate_kernel_docs(result: ValidationResult) -> None:
    for filename in KERNEL_DOCS_REQUIRED:
        path = KERNEL_DOCS / filename
        if not path.exists():
            result.add("KDOC-001", "kernel-doc obrigatório ausente", path.relative_to(PROJECT_ROOT).as_posix())


def _validate_default_registry(result: ValidationResult) -> None:
    from kernel.bootstrap import DEFAULT_MODULES

    registry = ModuleRegistry()
    try:
        for contract in DEFAULT_MODULES:
            registry.register(contract)
        registry.validate()
    except RegistryError as exc:
        result.add("REG-001", str(exc))


def _validate_single_root_source(root: Path, result: ValidationResult) -> None:
    for path in _python_files(root):
        relative = path.relative_to(root).as_posix()
        if relative == "kernel/shared/paths.py":
            continue
        if ROOT_REDEFINITION.search(path.read_text(encoding="utf-8")):
            result.add("PATH-001", "ROOT/PROJECT_ROOT redefinido fora de kernel.shared.paths", relative)


def _validate_kernel_isolation(root: Path, result: ValidationResult) -> None:
    kernel_dir = root / "kernel"
    for path in _python_files(kernel_dir):
        relative = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            result.add("PY-001", f"erro de sintaxe: {exc}", relative)
            continue

        for node in ast.walk(tree):
            module = None
            if isinstance(node, ast.ImportFrom):
                module = node.module
            elif isinstance(node, ast.Import) and node.names:
                module = node.names[0].name
            if module is None:
                continue
            top_level = module.split(".", 1)[0]
            if top_level in {"codigo", "scripts"}:
                result.add("KERN-001", f"kernel importa modulo externo proibido: {module}", relative)


def _validate_sys_path_adapters(root: Path, result: ValidationResult) -> None:
    for path in _python_files(root):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError:
            continue

        has_sys_path_insert = any(_is_sys_path_insert(node) for node in ast.walk(tree))
        if has_sys_path_insert and relative not in ALLOWED_SYS_PATH_ADAPTERS:
            result.add("PATH-003", "sys.path adapter fora da lista permitida", relative)
        if has_sys_path_insert and "__import__('pathlib').Path(__file__)" in text:
            result.add("PATH-002", "bootstrap local por __file__ proibido", relative)


def _is_sys_path_insert(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "insert"
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "path"
        and isinstance(func.value.value, ast.Name)
        and func.value.value.id == "sys"
    )


def _python_files(root: Path):
    for path in root.rglob("*.py"):
        parts = set(path.parts)
        if "__pycache__" in parts or ".pytest_cache" in parts:
            continue
        # Ignorar diretórios de archive (contêm material histórico, não ativo)
        if "archive" in parts:
            continue
        yield path


__all__ = [
    "ArchitectureValidationError",
    "ValidationIssue",
    "ValidationResult",
    "assert_architecture_valid",
    "validate_architecture",
]
