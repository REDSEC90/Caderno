"""
Modelos de dados do FAA — Framework de Auditoria Arquitetural do SOE-CCG.

Todos os motores produzem AuditResult. O agregador consome apenas esta interface.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Status(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class Severidade(str, Enum):
    INFO     = "INFO"
    BAIXA    = "BAIXA"
    MEDIA    = "MEDIA"
    ALTA     = "ALTA"
    CRITICA  = "CRITICA"


@dataclass
class AuditResult:
    id: str                          # Ex: EST-001, DOM-003
    motor: str                       # Nome do motor que gerou
    titulo: str
    status: Status
    severidade: Severidade
    evidencias: list[str] = field(default_factory=list)
    sugestoes: list[str]  = field(default_factory=list)


@dataclass
class MotorResult:
    nome: str
    resultados: list[AuditResult] = field(default_factory=list)

    @property
    def falhas(self) -> list[AuditResult]:
        return [r for r in self.resultados if r.status == Status.FAIL]

    @property
    def avisos(self) -> list[AuditResult]:
        return [r for r in self.resultados if r.status == Status.WARN]

    @property
    def passou(self) -> bool:
        return not self.falhas

    @property
    def pontuacao(self) -> float:
        if not self.resultados:
            return 100.0
        peso = {Status.PASS: 1.0, Status.WARN: 0.5, Status.FAIL: 0.0}
        return sum(peso[r.status] for r in self.resultados) / len(self.resultados) * 100
