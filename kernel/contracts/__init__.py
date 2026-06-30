"""Contratos estruturais governados pelo kernel."""

from .module import ContractError, ModuleContract
from .validator import (
    ArchitectureValidationError,
    ValidationIssue,
    ValidationResult,
    assert_architecture_valid,
    validate_architecture,
)

__all__ = [
    "ArchitectureValidationError",
    "ContractError",
    "ModuleContract",
    "ValidationIssue",
    "ValidationResult",
    "assert_architecture_valid",
    "validate_architecture",
]
