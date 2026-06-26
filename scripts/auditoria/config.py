"""
Configuração central do FAA.
Todos os caminhos são relativos à raiz do projeto SOE-CCG.
"""

from pathlib import Path

# Raiz do projeto — dois níveis acima de scripts/auditoria/
ROOT = Path(__file__).parent.parent.parent.resolve()

# Diretórios principais
DADOS       = ROOT / "dados"
DOCS        = ROOT / "docs"
BANCO       = ROOT / "banco_de_dados"
SCRIPTS     = ROOT / "scripts"

# Subdiretórios de dados
DADOS_RECEITAS     = DADOS / "receitas"
DADOS_INGREDIENTES = DADOS / "ingredientes"
DADOS_TECNICAS     = DADOS / "tecnicas"
DADOS_EQUIPAMENTOS = DADOS / "equipamentos"
DADOS_EXECUCOES    = DADOS / "execucoes"
DADOS_OBSERVACOES  = DADOS / "observacoes"
DADOS_EXPERIMENTOS = DADOS / "experimentos"

# Documentação de domínio
TEMPLATES   = DOCS / "01-dominio" / "templates"
CONTRATOS   = DOCS / "01-dominio" / "contratos"
ESQUEMAS    = DOCS / "01-dominio" / "esquemas"
CATALOGOS   = DOCS / "01-dominio" / "catalogos"
PADROES     = DOCS / "04-padroes"
REFERENCIAS = DOCS / "99-referencias"

# Esquema SQLite
SCHEMA_SQL  = BANCO / "esquemas" / "schema-sqlite-v1.sql"

# Prefixos de entidade → diretório de dados
PREFIXOS: dict[str, Path] = {
    "REC": DADOS_RECEITAS,
    "ING": DADOS_INGREDIENTES,
    "TEC": DADOS_TECNICAS,
    "EQP": DADOS_EQUIPAMENTOS,
    "EXE": DADOS_EXECUCOES,
    "OBS": DADOS_OBSERVACOES,
    "EXP": DADOS_EXPERIMENTOS,
}

# Entidades e seus artefatos esperados
ENTIDADES = ["receita", "ingrediente", "tecnica", "equipamento", "execucao", "observacao", "experimento"]

# Estados válidos por entidade (espelho dos catálogos)
ESTADOS_VALIDOS: dict[str, list[str]] = {
    "receita":     ["rascunho", "testada", "validada", "publicada", "arquivada"],
    "ingrediente": ["ativo", "descontinuado", "arquivado"],
    "tecnica":     ["ativo", "descontinuado", "arquivado"],
    "equipamento": ["ativo", "descontinuado", "arquivado"],
    "execucao":    ["registrada", "revisada", "consolidada"],
    "observacao":  ["ativo", "arquivado", "obsoleto"],
    "experimento": ["aberto", "concluido", "incorporado", "descartado"],
}

# Metadados obrigatórios em todos os registros
METADADOS_OBRIGATORIOS = ["id", "tipo", "schema-version", "versao", "status", "criado-em", "atualizado-em", "autor"]

# Padrão de ID
import re
ID_PATTERN = re.compile(r"^(REC|ING|TEC|EQP|EXE|OBS|EXP|CAT)-\d{6}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
