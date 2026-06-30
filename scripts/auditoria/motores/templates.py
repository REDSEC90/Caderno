"""
Motor 4 — Templates
Verifica frontmatter, campos obrigatórios e consistência de todos os templates.
"""

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT, ENTIDADES, METADADOS_OBRIGATORIOS
from utils import ler_frontmatter, listar_md

TEMPLATES_DIR = DOCS / "01-dominio" / "templates"


def executar() -> MotorResult:
    resultado = MotorResult(nome="Templates")

    for entidade in ENTIDADES:
        template = TEMPLATES_DIR / f"{entidade}-v1.md"

        if not template.exists():
            resultado.resultados.append(AuditResult(
                id="TPL-001", motor="Templates",
                titulo=f"Template ausente: {entidade}-v1.md",
                status=Status.FAIL, severidade=Severidade.CRITICA,
            ))
            continue

        meta = ler_frontmatter(template)

        if not meta:
            resultado.resultados.append(AuditResult(
                id="TPL-002", motor="Templates",
                titulo=f"Template sem frontmatter: {entidade}-v1.md",
                status=Status.FAIL, severidade=Severidade.ALTA,
                evidencias=[str(template.relative_to(ROOT))],
            ))
            continue

        # Verifica campos obrigatórios
        for campo in METADADOS_OBRIGATORIOS:
            presente = campo in meta
            resultado.resultados.append(AuditResult(
                id="TPL-003", motor="Templates",
                titulo=f"{entidade}: campo '{campo}' no template",
                status=Status.PASS if presente else Status.FAIL,
                severidade=Severidade.INFO if presente else Severidade.ALTA,
                evidencias=[str(template.relative_to(ROOT))],
                sugestoes=[] if presente else [f"Adicionar '{campo}' ao frontmatter de {template.name}"],
            ))

        # Campo 'tipo' deve ter valor fixo correto
        tipo_esperado = entidade
        tipo_real = meta.get("tipo", "")
        if tipo_real != tipo_esperado:
            resultado.resultados.append(AuditResult(
                id="TPL-004", motor="Templates",
                titulo=f"{entidade}: campo 'tipo' incorreto ('{tipo_real}' ≠ '{tipo_esperado}')",
                status=Status.FAIL, severidade=Severidade.MEDIA,
                evidencias=[str(template.relative_to(ROOT))],
            ))

    return resultado
