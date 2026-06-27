"""Motor de regras de validação"""
from dataclasses import dataclass
from typing import List, Callable
from enum import Enum

class Severity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Issue:
    type: str
    severity: Severity
    file: str
    message: str
    action: str = ""

class Rule:
    """Regra de validação arquitetural"""
    def __init__(self, name: str, severity: Severity, check: Callable, action: str = ""):
        self.name = name
        self.severity = severity
        self.check = check
        self.action = action
    
    def validate(self, node) -> Issue | None:
        if not self.check(node):
            return Issue(
                type=self.name,
                severity=self.severity,
                file=node.relative,
                message=f"Rule {self.name} violated",
                action=self.action
            )
        return None

# Regras básicas
RULES = [
    Rule(
        "versioned_naming",
        Severity.WARNING,
        lambda n: n.is_versioned if n.category in {"documentation", "schema"} else True,
        "Adicionar sufixo de versão: -v1.md ou -v1.sql"
    ),
    Rule(
        "frontmatter_required",
        Severity.CRITICAL,
        lambda n: n.has_frontmatter if (n.category == "data" and n.path.suffix == ".md") else True,
        "Adicionar frontmatter YAML com metadados obrigatórios"
    ),
]

def validate_node(node, rules: List[Rule]) -> List[Issue]:
    """Valida um nó contra todas as regras"""
    issues = []
    for rule in rules:
        issue = rule.validate(node)
        if issue:
            issues.append(issue)
    return issues
