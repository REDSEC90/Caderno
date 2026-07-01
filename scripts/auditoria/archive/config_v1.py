"""
Configuração central do FAA v1.
Caminhos resolvidos contra os nomes reais dos arquivos (com sufixo de versão).
Este arquivo é imutável após release — não alterar.
"""

import sys
from pathlib import Path
import re

_PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT_FOR_IMPORT))

from kernel.shared.paths import ROOT

DADOS       = ROOT / "dados"
DOCS        = ROOT / "docs"
BANCO       = ROOT / "banco_de_dados"
SCRIPTS     = ROOT / "scripts"

DADOS_RECEITAS     = DADOS / "receitas"
DADOS_INGREDIENTES = DADOS / "ingredientes"
DADOS_TECNICAS     = DADOS / "tecnicas"
DADOS_EQUIPAMENTOS = DADOS / "equipamentos"
DADOS_EXECUCOES    = DADOS / "execucoes"
DADOS_OBSERVACOES  = DADOS / "observacoes"
DADOS_EXPERIMENTOS = DADOS / "experimentos"

TEMPLATES  = DOCS / "01-dominio" / "templates"
CONTRATOS  = DOCS / "01-dominio" / "contratos"
ESQUEMAS   = DOCS / "01-dominio" / "esquemas"
CATALOGOS  = DOCS / "01-dominio" / "catalogos"
PADROES    = DOCS / "04-padroes"
REFERENCIAS= DOCS / "99-referencias"
SCHEMA_SQL = BANCO / "esquemas" / "schema-sqlite-v1.sql"

PREFIXOS: dict[str, Path] = {
    "REC": DADOS_RECEITAS,
    "ING": DADOS_INGREDIENTES,
    "TEC": DADOS_TECNICAS,
    "EQP": DADOS_EQUIPAMENTOS,
    "EXE": DADOS_EXECUCOES,
    "OBS": DADOS_OBSERVACOES,
    "EXP": DADOS_EXPERIMENTOS,
}

ENTIDADES = [
    "receita", "ingrediente", "tecnica", "equipamento",
    "execucao", "observacao", "experimento",
]

ESTADOS_VALIDOS: dict[str, list[str]] = {
    "receita":     ["rascunho", "testada", "validada", "publicada", "arquivada"],
    "ingrediente": ["ativo", "descontinuado", "arquivado"],
    "tecnica":     ["ativo", "descontinuado", "arquivado"],
    "equipamento": ["ativo", "descontinuado", "arquivado"],
    "execucao":    ["registrada", "revisada", "consolidada"],
    "observacao":  ["ativo", "arquivado", "obsoleto"],
    "experimento": ["aberto", "concluido", "incorporado", "descartado"],
}

METADADOS_OBRIGATORIOS = [
    "id", "tipo", "schema-version", "versao", "status",
    "criado-em", "atualizado-em", "autor",
]

ID_PATTERN   = re.compile(r"^(REC|ING|TEC|EQP|EXE|OBS|EXP|CAT)-\d{6}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NOME_DADOS_PATTERN = re.compile(r"^(REC|ING|TEC|EQP|EXE|OBS|EXP)-\d{6}-.+-v\d+\.md$")

# ─── BASELINE v1 ─────────────────────────────────────────────────────────────
# Ground truth oficial: nome lógico → caminho real no filesystem.
# Arquivos versionados são imutáveis; este mapeamento é a referência canônica.

BASELINE_V1: dict[str, Path] = {
    # Fundação
    "filosofia":              DOCS / "00-projeto" / "filosofia-v1.md",
    "constituicao":           DOCS / "00-projeto" / "constituicao-v1.md",
    "principios":             DOCS / "00-projeto" / "principios-v1.md",
    "glossario":              DOCS / "00-projeto" / "glossario-v1.md",
    "escopo":                 DOCS / "00-projeto" / "escopo-v1.md",
    "objetivos":              DOCS / "00-projeto" / "objetivos-v1.md",
    "visao":                  DOCS / "00-projeto" / "visão-v1.md",
    "roadmap-master":         DOCS / "00-projeto" / "roadmap-master-v1.md",
    # Arquitetura
    "diagrama-mestre":        DOCS / "02-arquitetura" / "diagrama-mestre-v1.md",
    "estrutura-diretorios":   DOCS / "02-arquitetura" / "estrutura-diretorios-v1.md",
    "fluxo-dados":            DOCS / "02-arquitetura" / "fluxo-dados-v1.md",
    "importacao":             DOCS / "02-arquitetura" / "importacao-v1.md",
    "exportacao":             DOCS / "02-arquitetura" / "exportacao-v1.md",
    # Domínio — especificações
    "especificacao-receita":       DOCS / "01-dominio" / "especificacao-receita-v1.md",
    "especificacao-ingrediente":   DOCS / "01-dominio" / "especificacao-ingrediente-v1.md",
    "especificacao-tecnica":       DOCS / "01-dominio" / "especificacao-tecnica-v1.md",
    "especificacao-equipamento":   DOCS / "01-dominio" / "especificacao-equipamento-v1.md",
    "especificacao-execucao":      DOCS / "01-dominio" / "especificacao-execucao-v1.md",
    "especificacao-observacao":    DOCS / "01-dominio" / "especificacao-observacao-v1.md",
    "especificacao-experimento":   DOCS / "01-dominio" / "especificacao-experimento-v1.md",
    "especificacao-registro":      DOCS / "01-dominio" / "especificacao-registro-v1.md",
    # Domínio — contratos
    "contrato-receita":      CONTRATOS / "contrato-receita-v1.md",
    "contrato-ingrediente":  CONTRATOS / "contrato-ingrediente-v1.md",
    "contrato-tecnica":      CONTRATOS / "contrato-tecnica-v1.md",
    "contrato-equipamento":  CONTRATOS / "contrato-equipamento-v1.md",
    "contrato-execucao":     CONTRATOS / "contrato-execucao-v1.md",
    "contrato-observacao":   CONTRATOS / "contrato-observacao-v1.md",
    "contrato-experimento":  CONTRATOS / "contrato-experimento-v1.md",
    # Domínio — templates
    "template-receita":      TEMPLATES / "receita-v1.md",
    "template-ingrediente":  TEMPLATES / "ingrediente-v1.md",
    "template-tecnica":      TEMPLATES / "tecnica-v1.md",
    "template-equipamento":  TEMPLATES / "equipamento-v1.md",
    "template-execucao":     TEMPLATES / "execucao-v1.md",
    "template-observacao":   TEMPLATES / "observacao-v1.md",
    "template-experimento":  TEMPLATES / "experimento-v1.md",
    # Domínio — esquemas
    "esquema-receita":       ESQUEMAS / "esquema-receita-v1.md",
    "esquema-ingrediente":   ESQUEMAS / "esquema-ingrediente-v1.md",
    "esquema-tecnica":       ESQUEMAS / "esquema-tecnica-v1.md",
    "esquema-equipamento":   ESQUEMAS / "esquema-equipamento-v1.md",
    "esquema-execucao":      ESQUEMAS / "esquema-execucao-v1.md",
    "esquema-observacao":    ESQUEMAS / "esquema-observacao-v1.md",
    "esquema-experimento":   ESQUEMAS / "esquema-experimento-v1.md",  # ausência real
    # Linguagem e catálogos
    "linguagem":             DOCS / "01-dominio" / "linguagem-soe-ccg-v1.md",
    "separacao-dominios":    DOCS / "01-dominio" / "separacao-dominios-v1.md",
    "mapa-relacionamentos":  DOCS / "01-dominio" / "mapa-relacionamentos-v1.md",
    "ciclo-de-vida":         DOCS / "01-dominio" / "ciclo-de-vida-v1.md",
    "entidades":             DOCS / "01-dominio" / "entidades-v1.md",
    "estados-todas-entidades": CATALOGOS / "estados-todas-entidades-v1.md",
    "categorias":            CATALOGOS / "categorias-v1.md",
    # Padrões de governança
    "identificadores":       PADROES / "identificadores-v1.md",
    "nomenclatura":          PADROES / "nomenclatura-v1.md",
    "versionamento":         PADROES / "versionamento-v1.md",
    "metadados":             PADROES / "metadados-v1.md",
    "tags":                  PADROES / "tags-v1.md",
    "validacao":             PADROES / "validacao-v1.md",
    "politica-templates":    PADROES / "politica-templates-v1.md",
    "politica-esquemas":     PADROES / "politica-esquemas-v1.md",
    "politica-arquivamento": PADROES / "politica-arquivamento-v1.md",
    "politica-revisao":      PADROES / "politica-revisao-v1.md",
    "politica-conflito":     PADROES / "politica-conflito-v1.md",
    # Modelagem
    "conceitos-fundamentais":DOCS / "03-modelagem" / "conceitos-fundamentais-v1.md",
    "entidades-er":          DOCS / "03-modelagem" / "entidades-er-v1.md",
    "relacionamentos-model": DOCS / "03-modelagem" / "relacionamentos-v1.md",
    "normalizacao":          DOCS / "03-modelagem" / "normalizacao-v1.md",
    "ids-model":             DOCS / "03-modelagem" / "ids-v1.md",
    "sqlite-doc":            DOCS / "03-modelagem" / "sqlite-v1.md",
    # Banco de dados
    "schema-sqlite":         BANCO / "esquemas" / "schema-sqlite-v1.sql",
    "seed-categorias":       BANCO / "seeds" / "seed-categorias-v1.sql",
    # Desenvolvimento e operação
    "casos-de-uso":          DOCS / "05-desenvolvimento" / "casos-de-uso-v1.md",
    "padroes-desenvolvimento": DOCS / "05-desenvolvimento" / "padroes-desenvolvimento-v1.md",
    "guia-operacao":         DOCS / "06-operacao" / "guia-operacao-v1.md",
}

# ─── GRUPOS de maturidade e seus limiares de aprovação ───────────────────────

GRUPOS_BASELINE: dict[str, list[str]] = {
    "fundacao": [
        "filosofia", "constituicao", "principios", "glossario",
        "escopo", "objetivos", "visao",
    ],
    "arquitetura": [
        "diagrama-mestre", "estrutura-diretorios", "fluxo-dados",
    ],
    "dominio_especificacoes": [
        "especificacao-receita", "especificacao-ingrediente", "especificacao-tecnica",
        "especificacao-equipamento", "especificacao-execucao",
        "especificacao-observacao", "especificacao-experimento",
    ],
    "dominio_contratos": [
        "contrato-receita", "contrato-ingrediente", "contrato-tecnica",
        "contrato-equipamento", "contrato-execucao",
        "contrato-observacao", "contrato-experimento",
    ],
    "dominio_templates": [
        "template-receita", "template-ingrediente", "template-tecnica",
        "template-equipamento", "template-execucao",
        "template-observacao", "template-experimento",
    ],
    "dominio_esquemas": [
        "esquema-receita", "esquema-ingrediente", "esquema-tecnica",
        "esquema-equipamento", "esquema-execucao",
        "esquema-observacao", "esquema-experimento",
    ],
    "governanca": [
        "identificadores", "nomenclatura", "versionamento", "metadados",
        "politica-templates", "politica-esquemas", "politica-arquivamento",
        "politica-revisao", "politica-conflito",
    ],
    "modelagem": [
        "conceitos-fundamentais", "entidades-er", "schema-sqlite", "seed-categorias",
    ],
    "linguagem_dominio": [
        "linguagem", "separacao-dominios", "mapa-relacionamentos",
        "ciclo-de-vida", "entidades", "estados-todas-entidades",
    ],
}

# % mínima para PASS em cada grupo
LIMIAR_APROVACAO: dict[str, int] = {
    "fundacao":               100,
    "arquitetura":            100,
    "dominio_especificacoes": 100,
    "dominio_contratos":      100,
    "dominio_templates":      100,
    "dominio_esquemas":        85,   # esquema-experimento pode estar ausente
    "governanca":             100,
    "modelagem":              100,
    "linguagem_dominio":       85,
}
