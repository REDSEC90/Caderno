"""
Modelos de dados do FAA v1.
Interface imutável — todos os motores v1 produzem AuditResult.
"""

from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class Severidade(str, Enum):
    INFO    = "INFO"
    BAIXA   = "BAIXA"
    MEDIA   = "MEDIA"
    ALTA    = "ALTA"
    CRITICA = "CRITICA"


@dataclass
class AuditResult:
    id: str
    motor: str
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
        return round(sum(peso[r.status] for r in self.resultados) / len(self.resultados) * 100, 1)


@dataclass
class DecisaoArquitetural:
    """Resultado do motor de baseline — veredicto global do sistema."""
    aprovado: bool
    pontuacao_geral: float
    grupos: dict[str, float]          # grupo → %
    grupos_reprovados: list[str]
    artefatos_ausentes: list[str]
    artefatos_presentes: int
    artefatos_total: int
