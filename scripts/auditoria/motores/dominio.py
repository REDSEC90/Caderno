"""
Motor 3 — Domínio
Verifica se cada entidade possui contrato, template, especificação, esquema e catálogo de estados.
"""

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT, ENTIDADES

ARTEFATOS = {
    "template":      lambda e: DOCS / "01-dominio" / "templates" / f"{e}-v1.md",
    "contrato":      lambda e: DOCS / "01-dominio" / "contratos" / f"contrato-{e}-v1.md",
    "especificacao": lambda e: DOCS / "01-dominio" / f"especificacao-{e}-v1.md",
    "esquema":       lambda e: DOCS / "01-dominio" / "esquemas" / f"esquema-{e}-v1.md",
}


def executar() -> MotorResult:
    resultado = MotorResult(nome="Domínio")

    for entidade in ENTIDADES:
        for artefato, caminho_fn in ARTEFATOS.items():
            caminho = caminho_fn(entidade)
            existe = caminho.exists()
            resultado.resultados.append(AuditResult(
                id="DOM-001", motor="Domínio",
                titulo=f"{entidade}/{artefato}: {'presente' if existe else 'AUSENTE'}",
                status=Status.PASS if existe else Status.FAIL,
                severidade=Severidade.INFO if existe else Severidade.ALTA,
                evidencias=[str(caminho.relative_to(ROOT))],
                sugestoes=[] if existe else [f"Criar {caminho.relative_to(ROOT)}"],
            ))

    # Catálogo de estados consolidado
    estados = DOCS / "01-dominio" / "catalogos" / "estados-todas-entidades-v1.md"
    resultado.resultados.append(AuditResult(
        id="DOM-002", motor="Domínio",
        titulo=f"Catálogo de estados: {'presente' if estados.exists() else 'AUSENTE'}",
        status=Status.PASS if estados.exists() else Status.FAIL,
        severidade=Severidade.INFO if estados.exists() else Severidade.ALTA,
        evidencias=[str(estados.relative_to(ROOT))],
    ))

    # Mapa de relacionamentos
    mapa = DOCS / "01-dominio" / "mapa-relacionamentos-v1.md"
    resultado.resultados.append(AuditResult(
        id="DOM-003", motor="Domínio",
        titulo=f"Mapa de relacionamentos: {'presente' if mapa.exists() else 'AUSENTE'}",
        status=Status.PASS if mapa.exists() else Status.FAIL,
        severidade=Severidade.INFO if mapa.exists() else Severidade.ALTA,
    ))

    return resultado
