"""
Motor 1 — Estrutura
Verifica pastas, localização de arquivos, nomes, extensões e arquivos fora do lugar.
"""

from pathlib import Path
from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, DADOS, DOCS, BANCO, SCRIPTS, PREFIXOS, ENTIDADES


DIRETORIOS_ESPERADOS = [
    DADOS / "receitas",
    DADOS / "ingredientes",
    DADOS / "tecnicas",
    DADOS / "equipamentos",
    DADOS / "execucoes",
    DADOS / "observacoes",
    DADOS / "experimentos",
    DOCS / "00-projeto",
    DOCS / "01-dominio" / "templates",
    DOCS / "01-dominio" / "contratos",
    DOCS / "01-dominio" / "esquemas",
    DOCS / "01-dominio" / "catalogos",
    DOCS / "04-padroes",
    DOCS / "99-referencias",
    BANCO / "esquemas",
    BANCO / "seeds",
]

ARQUIVOS_ESPERADOS = [
    DOCS / "00-projeto" / "filosofia-v1.md",
    DOCS / "00-projeto" / "constituicao-v1.md",
    DOCS / "00-projeto" / "principios-v1.md",
    DOCS / "00-projeto" / "glossario-v1.md",
    DOCS / "01-dominio" / "linguagem-soe-ccg-v1.md",
    DOCS / "01-dominio" / "mapa-relacionamentos-v1.md",
    DOCS / "01-dominio" / "separacao-dominios-v1.md",
    DOCS / "04-padroes" / "identificadores-v1.md",
    BANCO / "esquemas" / "schema-sqlite-v1.sql",
    BANCO / "seeds" / "seed-categorias-v1.sql",
]

import re
_NOME_DADOS = re.compile(r"^(REC|ING|TEC|EQP|EXE|OBS|EXP)-\d{6}-.+-v\d+\.md$")


def executar() -> MotorResult:
    resultado = MotorResult(nome="Estrutura")

    # 1. Diretórios esperados existem?
    for d in DIRETORIOS_ESPERADOS:
        if d.exists():
            resultado.resultados.append(AuditResult(
                id="EST-001", motor="Estrutura",
                titulo=f"Diretório existe: {d.relative_to(ROOT)}",
                status=Status.PASS, severidade=Severidade.INFO,
            ))
        else:
            resultado.resultados.append(AuditResult(
                id="EST-001", motor="Estrutura",
                titulo=f"Diretório ausente: {d.relative_to(ROOT)}",
                status=Status.FAIL, severidade=Severidade.ALTA,
                sugestoes=[f"Criar: mkdir -p {d.relative_to(ROOT)}"],
            ))

    # 2. Arquivos críticos existem?
    for f in ARQUIVOS_ESPERADOS:
        if f.exists():
            resultado.resultados.append(AuditResult(
                id="EST-002", motor="Estrutura",
                titulo=f"Arquivo crítico presente: {f.relative_to(ROOT)}",
                status=Status.PASS, severidade=Severidade.INFO,
            ))
        else:
            resultado.resultados.append(AuditResult(
                id="EST-002", motor="Estrutura",
                titulo=f"Arquivo crítico ausente: {f.relative_to(ROOT)}",
                status=Status.FAIL, severidade=Severidade.CRITICA,
            ))

    # 3. Arquivos em dados/ seguem nomenclatura correta?
    for prefixo, diretorio in PREFIXOS.items():
        for arquivo in diretorio.glob("*.md"):
            if not _NOME_DADOS.match(arquivo.name):
                resultado.resultados.append(AuditResult(
                    id="EST-003", motor="Estrutura",
                    titulo=f"Nomenclatura incorreta: {arquivo.relative_to(ROOT)}",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=[f"Padrão esperado: {prefixo}-NNNNNN-slug-vN.md"],
                ))

    # 4. Arquivos com extensão incorreta em dados/?
    for d in PREFIXOS.values():
        for arquivo in d.iterdir():
            if arquivo.is_file() and arquivo.suffix != ".md":
                resultado.resultados.append(AuditResult(
                    id="EST-004", motor="Estrutura",
                    titulo=f"Arquivo não-Markdown em dados/: {arquivo.relative_to(ROOT)}",
                    status=Status.WARN, severidade=Severidade.BAIXA,
                    sugestoes=["Mover para dados/anexos/ ou recursos/"],
                ))

    return resultado
