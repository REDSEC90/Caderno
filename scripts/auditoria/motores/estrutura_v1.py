"""
Motor Estrutura v1
Verifica diretórios obrigatórios, nomenclatura de arquivos em dados/ e arquivos críticos.
Usa BASELINE_V1 como referência — resolve nomes com sufixo de versão correto.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

import re
from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import ROOT, DADOS, DOCS, BANCO, PREFIXOS, BASELINE_V1, NOME_DADOS_PATTERN

DIRETORIOS_OBRIGATORIOS = [
    DADOS / "receitas", DADOS / "ingredientes", DADOS / "tecnicas",
    DADOS / "equipamentos", DADOS / "execucoes", DADOS / "observacoes",
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

# Artefatos críticos de nível 1 — ausência bloqueia aprovação
CRITICOS = [
    "filosofia", "constituicao", "principios", "glossario",
    "diagrama-mestre", "schema-sqlite",
]


def executar() -> MotorResult:
    resultado = MotorResult(nome="Estrutura")

    # 1. Diretórios obrigatórios
    for d in DIRETORIOS_OBRIGATORIOS:
        existe = d.exists()
        resultado.resultados.append(AuditResult(
            id="EST-001", motor="Estrutura",
            titulo=f"Diretório {'presente' if existe else 'AUSENTE'}: {d.relative_to(ROOT)}",
            status=Status.PASS if existe else Status.FAIL,
            severidade=Severidade.INFO if existe else Severidade.ALTA,
            sugestoes=[] if existe else [f"mkdir -p {d.relative_to(ROOT)}"],
        ))

    # 2. Artefatos críticos (usando BASELINE_V1 — caminhos reais)
    for chave in CRITICOS:
        caminho = BASELINE_V1[chave]
        existe = caminho.exists()
        resultado.resultados.append(AuditResult(
            id="EST-002", motor="Estrutura",
            titulo=f"Artefato crítico {'presente' if existe else 'AUSENTE'}: {caminho.relative_to(ROOT)}",
            status=Status.PASS if existe else Status.FAIL,
            severidade=Severidade.INFO if existe else Severidade.CRITICA,
        ))

    # 3. Nomenclatura em dados/
    for prefixo, diretorio in PREFIXOS.items():
        if not diretorio.exists():
            continue
        for arquivo in diretorio.glob("*.md"):
            if not NOME_DADOS_PATTERN.match(arquivo.name):
                resultado.resultados.append(AuditResult(
                    id="EST-003", motor="Estrutura",
                    titulo=f"Nomenclatura fora do padrão: {arquivo.name}",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=[str(arquivo.relative_to(ROOT))],
                    sugestoes=[f"Padrão esperado: {prefixo}-NNNNNN-slug-vN.md"],
                ))

    # 4. Arquivos não-Markdown em dados/
    for diretorio in PREFIXOS.values():
        if not diretorio.exists():
            continue
        for arquivo in diretorio.iterdir():
            if arquivo.is_file() and arquivo.suffix != ".md":
                resultado.resultados.append(AuditResult(
                    id="EST-004", motor="Estrutura",
                    titulo=f"Arquivo não-Markdown em dados/: {arquivo.relative_to(ROOT)}",
                    status=Status.WARN, severidade=Severidade.BAIXA,
                    sugestoes=["Mover para dados/anexos/ ou recursos/"],
                ))

    return resultado
