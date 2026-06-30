"""
Motor 5 — Contratos
Compara campos obrigatórios definidos no contrato com o template correspondente.
Um campo obrigatório no contrato deve existir no frontmatter do template.
"""

import re
from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT, ENTIDADES
from utils import ler_frontmatter

CONTRATOS_DIR = DOCS / "01-dominio" / "contratos"
TEMPLATES_DIR = DOCS / "01-dominio" / "templates"

# Extrai nomes de campos da tabela de "Campos Obrigatórios" do contrato Markdown
_CAMPO_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")


def _campos_obrigatorios_do_contrato(path) -> list[str]:
    """Lê a seção '## 1. Campos Obrigatórios' e extrai nomes de campos."""
    if not path.exists():
        return []
    texto = path.read_text(encoding="utf-8")
    # Isola a seção de campos obrigatórios
    match = re.search(r"## 1\. Campos Obrigatórios(.+?)## 2\.", texto, re.DOTALL)
    if not match:
        return []
    campos = []
    for linha in match.group(1).splitlines():
        m = _CAMPO_RE.match(linha.strip())
        if m:
            campos.append(m.group(1))
    return campos


def executar() -> MotorResult:
    resultado = MotorResult(nome="Contratos")

    for entidade in ENTIDADES:
        contrato = CONTRATOS_DIR / f"contrato-{entidade}-v1.md"
        template = TEMPLATES_DIR / f"{entidade}-v1.md"

        if not contrato.exists():
            resultado.resultados.append(AuditResult(
                id="CTR-001", motor="Contratos",
                titulo=f"Contrato ausente: contrato-{entidade}-v1.md",
                status=Status.FAIL, severidade=Severidade.CRITICA,
            ))
            continue

        campos_contrato = _campos_obrigatorios_do_contrato(contrato)

        if not campos_contrato:
            resultado.resultados.append(AuditResult(
                id="CTR-002", motor="Contratos",
                titulo=f"Contrato sem campos obrigatórios parseáveis: {entidade}",
                status=Status.WARN, severidade=Severidade.MEDIA,
                evidencias=[str(contrato.relative_to(ROOT))],
            ))
            continue

        meta_template = ler_frontmatter(template) if template.exists() else {}

        # Campos do contrato que são metadados (devem estar no frontmatter do template)
        # Campos de conteúdo como 'nome', 'titulo', 'conteudo' estão no corpo — não no frontmatter
        # Campos que pertencem ao corpo do Markdown, não ao frontmatter
        CAMPOS_CONTEUDO = {
            "nome", "titulo", "conteudo", "hipotese", "modo_de_preparo",
            "modo-de-preparo", "ingredientes", "tecnicas", "equipamentos",
            "variaveis", "processo", "resultado", "conclusao",
        }

        for campo in campos_contrato:
            campo_norm = campo.replace("_", "-")  # normaliza snake_case para kebab-case
            if campo in CAMPOS_CONTEUDO or campo_norm in CAMPOS_CONTEUDO:
                continue  # campo de conteúdo — está no corpo, não no frontmatter
            presente = campo in meta_template or campo_norm in meta_template
            resultado.resultados.append(AuditResult(
                id="CTR-003", motor="Contratos",
                titulo=f"{entidade}: campo obrigatório '{campo}' no template",
                status=Status.PASS if presente else Status.FAIL,
                severidade=Severidade.INFO if presente else Severidade.ALTA,
                evidencias=[
                    str(contrato.relative_to(ROOT)),
                    str(template.relative_to(ROOT)) if template.exists() else "template ausente",
                ],
                sugestoes=[] if presente else [
                    f"Adicionar campo '{campo}' ao frontmatter de {template.name}"
                ],
            ))

    return resultado
