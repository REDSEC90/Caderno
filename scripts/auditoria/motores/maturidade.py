"""
Motor 13 — Maturidade
Pontua cada camada da arquitetura de 0 a 100 com base na presença de artefatos.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT, ENTIDADES, PREFIXOS, BANCO


def _pontuacao(presentes: int, total: int) -> float:
    return round(presentes / total * 100, 1) if total else 0.0


def _camada(id_audit, nome, itens: list[tuple[str, bool]], resultado):
    presentes = sum(1 for _, existe in itens if existe)
    pct = _pontuacao(presentes, len(itens))
    status = Status.PASS if pct >= 80 else (Status.WARN if pct >= 50 else Status.FAIL)
    sev    = Severidade.INFO if status == Status.PASS else (Severidade.MEDIA if status == Status.WARN else Severidade.ALTA)
    ausentes = [nome_item for nome_item, existe in itens if not existe]
    resultado.resultados.append(AuditResult(
        id=id_audit, motor="Maturidade",
        titulo=f"{nome}: {pct:.0f}%",
        status=status, severidade=sev,
        evidencias=[f"Presentes: {presentes}/{len(itens)}"],
        sugestoes=[f"Ausente: {a}" for a in ausentes],
    ))
    return pct


def executar() -> MotorResult:
    resultado = MotorResult(nome="Maturidade")
    pontuacoes = {}

    # Arquitetura (documentos fundacionais)
    arq_itens = [
        ("filosofia.md",    (DOCS / "00-projeto" / "filosofia.md").exists()),
        ("constituicao.md", (DOCS / "00-projeto" / "constituicao.md").exists()),
        ("principios.md",   (DOCS / "00-projeto" / "principios.md").exists()),
        ("glossario.md",    (DOCS / "00-projeto" / "glossario.md").exists()),
        ("linguagem",       (DOCS / "01-dominio" / "linguagem-soe-ccg.md").exists()),
        ("separacao-dominos", (DOCS / "01-dominio" / "separacao-dominios.md").exists()),
    ]
    pontuacoes["Arquitetura"] = _camada("MAT-001", "Arquitetura", arq_itens, resultado)

    # Domínio (entidades completas)
    dom_itens = []
    for e in ENTIDADES:
        dom_itens += [
            (f"{e}/especificacao", (DOCS / "01-dominio" / f"especificacao-{e}.md").exists()),
            (f"{e}/contrato",      (DOCS / "01-dominio" / "contratos" / f"contrato-{e}-v1.md").exists()),
            (f"{e}/template",      (DOCS / "01-dominio" / "templates" / f"{e}-v1.md").exists()),
            (f"{e}/esquema",       (DOCS / "01-dominio" / "esquemas" / f"esquema-{e}-v1.md").exists()),
        ]
    pontuacoes["Domínio"] = _camada("MAT-002", "Domínio", dom_itens, resultado)

    # Documentação
    doc_itens = [
        ("mapa-relacionamentos", (DOCS / "01-dominio" / "mapa-relacionamentos.md").exists()),
        ("estados-todas-entidades", (DOCS / "01-dominio" / "catalogos" / "estados-todas-entidades.md").exists()),
        ("casos-de-uso",  (DOCS / "05-desenvolvimento" / "casos-de-uso.md").exists()),
        ("validacao-arq", (DOCS / "99-referencias" / "validacao-arquitetural-fase12.md").exists()),
        ("spec-freeze",   (DOCS / "99-referencias" / "specification-freeze-v1.md").exists()),
        ("matriz-vaf",    (DOCS / "99-referencias" / "MATRIZ_DE_VALIDACAO_ARQUITETURAL.md").exists()),
        ("estado-sistema",(DOCS / "99-referencias" / "ESTADO_ATUAL_DO_SISTEMA.md").exists()),
    ]
    pontuacoes["Documentação"] = _camada("MAT-003", "Documentação", doc_itens, resultado)

    # Modelagem
    mod_itens = [
        ("schema-sqlite", (BANCO / "esquemas" / "schema-sqlite-v1.sql").exists()),
        ("seed-categorias",(BANCO / "seeds" / "seed-categorias.sql").exists()),
        ("conceitos-fundamentais", (DOCS / "03-modelagem" / "conceitos-fundamentais.md").exists()),
    ]
    pontuacoes["Modelagem"] = _camada("MAT-004", "Modelagem", mod_itens, resultado)

    # Dados canônicos
    dados_itens = [(p, any(d.glob("*.md"))) for p, d in PREFIXOS.items()]
    pontuacoes["Dados"] = _camada("MAT-005", "Dados canônicos", dados_itens, resultado)

    # Código
    codigo_itens = [
        ("parser",     (ROOT / "codigo" / "parser.py").exists()),
        ("validador",  (ROOT / "codigo" / "validador.py").exists()),
        ("importador", (ROOT / "codigo" / "importador.py").exists()),
    ]
    pontuacoes["Código"] = _camada("MAT-006", "Código", codigo_itens, resultado)

    # Pontuação geral
    media = round(sum(pontuacoes.values()) / len(pontuacoes), 1)
    resultado.resultados.append(AuditResult(
        id="MAT-007", motor="Maturidade",
        titulo=f"Pontuação geral de maturidade: {media:.1f}%",
        status=Status.PASS if media >= 80 else (Status.WARN if media >= 50 else Status.FAIL),
        severidade=Severidade.INFO,
        evidencias=[f"{k}: {v:.0f}%" for k, v in pontuacoes.items()],
    ))

    return resultado
