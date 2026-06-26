-- =============================================================
-- SOE-CCG — Esquema SQLite v1
-- Motor de Conhecimento Gastronômico
-- =============================================================
-- Gerado a partir da Fase 9 — Modelagem Física
-- Pré-requisito: banco criado e PRAGMA foreign_keys = ON
-- =============================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- -------------------------------------------------------------
-- TABELAS PRINCIPAIS
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS receitas (
    id               TEXT PRIMARY KEY,          -- REC-NNNNNN
    titulo           TEXT NOT NULL,
    descricao        TEXT,
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'rascunho'
                         CHECK(status IN ('rascunho','testada','validada','publicada','arquivada')),
    rendimento       TEXT,
    tempo_preparo    TEXT,
    tempo_cozimento  TEXT,
    dificuldade      TEXT CHECK(dificuldade IN ('baixa','media','alta') OR dificuldade IS NULL),
    modo_de_preparo  TEXT NOT NULL,
    notas            TEXT,
    origem           TEXT,
    autor            TEXT NOT NULL,
    tags             TEXT,                       -- JSON array serializado
    criado_em        TEXT NOT NULL,             -- YYYY-MM-DD
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredientes (
    id               TEXT PRIMARY KEY,          -- ING-NNNNNN
    nome             TEXT NOT NULL,
    tipo_ingrediente TEXT,
    unidade_padrao   TEXT,
    descricao        TEXT,
    sazonalidade     TEXT,
    origem           TEXT,
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'ativo'
                         CHECK(status IN ('ativo','descontinuado','arquivado')),
    notas            TEXT,
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tecnicas (
    id               TEXT PRIMARY KEY,          -- TEC-NNNNNN
    nome             TEXT NOT NULL,
    tipo_tecnica     TEXT,
    descricao        TEXT,
    aplicacoes       TEXT,
    dificuldade      TEXT CHECK(dificuldade IN ('baixa','media','alta') OR dificuldade IS NULL),
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'ativo'
                         CHECK(status IN ('ativo','descontinuado','arquivado')),
    notas            TEXT,
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id               TEXT PRIMARY KEY,          -- EQP-NNNNNN
    nome             TEXT NOT NULL,
    tipo_equipamento TEXT,
    descricao        TEXT,
    capacidade       TEXT,
    material         TEXT,
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'ativo'
                         CHECK(status IN ('ativo','descontinuado','arquivado')),
    notas            TEXT,
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS execucoes (
    id               TEXT PRIMARY KEY,          -- EXE-NNNNNN
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    data_execucao    TEXT NOT NULL,             -- YYYY-MM-DD
    hora_inicio      TEXT,
    hora_fim         TEXT,
    tempo_total      TEXT,
    desvios          TEXT,
    resultado        TEXT,
    avaliacao_sabor  TEXT,
    avaliacao_textura TEXT,
    avaliacao_aparencia TEXT,
    avaliacao_geral  TEXT,
    peso_final       TEXT,
    contexto         TEXT,
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'registrada'
                         CHECK(status IN ('registrada','revisada','consolidada')),
    notas            TEXT,
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observacoes (
    id               TEXT PRIMARY KEY,          -- OBS-NNNNNN
    conteudo         TEXT NOT NULL,
    entidade_id      TEXT,                      -- ID da entidade referenciada
    entidade_tipo    TEXT CHECK(entidade_tipo IN
                         ('receita','execucao','ingrediente','tecnica',
                          'equipamento','experimento') OR entidade_tipo IS NULL),
    contexto         TEXT,
    relevancia       TEXT CHECK(relevancia IN ('baixa','media','alta') OR relevancia IS NULL),
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'ativo'
                         CHECK(status IN ('ativo','arquivado','obsoleto')),
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experimentos (
    id               TEXT PRIMARY KEY,          -- EXP-NNNNNN
    titulo           TEXT NOT NULL,
    hipotese         TEXT NOT NULL,
    receita_base_id  TEXT REFERENCES receitas(id),
    variaveis        TEXT,
    processo         TEXT,
    resultado        TEXT,
    conclusao        TEXT,
    incorporado_em   TEXT REFERENCES receitas(id),
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'aberto'
                         CHECK(status IN ('aberto','concluido','incorporado','descartado')),
    notas            TEXT,
    tags             TEXT,
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id               TEXT PRIMARY KEY,          -- CAT-NNNNNN
    nome             TEXT NOT NULL,
    descricao        TEXT,
    schema_version   INTEGER NOT NULL DEFAULT 1,
    versao           INTEGER NOT NULL DEFAULT 1,
    status           TEXT NOT NULL DEFAULT 'ativo',
    autor            TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);

-- -------------------------------------------------------------
-- TABELAS DE RELACIONAMENTO N:N
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS receita_ingrediente (
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    ingrediente_id   TEXT NOT NULL REFERENCES ingredientes(id),
    quantidade       REAL,
    unidade          TEXT,
    notas            TEXT,
    PRIMARY KEY (receita_id, ingrediente_id)
);

CREATE TABLE IF NOT EXISTS receita_tecnica (
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    tecnica_id       TEXT NOT NULL REFERENCES tecnicas(id),
    ordem            INTEGER,
    PRIMARY KEY (receita_id, tecnica_id)
);

CREATE TABLE IF NOT EXISTS receita_equipamento (
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    equipamento_id   TEXT NOT NULL REFERENCES equipamentos(id),
    PRIMARY KEY (receita_id, equipamento_id)
);

CREATE TABLE IF NOT EXISTS receita_categoria (
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    categoria_id     TEXT NOT NULL REFERENCES categorias(id),
    PRIMARY KEY (receita_id, categoria_id)
);

CREATE TABLE IF NOT EXISTS execucao_ingrediente (
    execucao_id      TEXT NOT NULL REFERENCES execucoes(id),
    ingrediente_id   TEXT NOT NULL REFERENCES ingredientes(id),
    quantidade_real  REAL,
    unidade          TEXT,
    substituicao     INTEGER NOT NULL DEFAULT 0,  -- 0=original, 1=substituído
    notas            TEXT,
    PRIMARY KEY (execucao_id, ingrediente_id)
);

CREATE TABLE IF NOT EXISTS execucao_tecnica (
    execucao_id      TEXT NOT NULL REFERENCES execucoes(id),
    tecnica_id       TEXT NOT NULL REFERENCES tecnicas(id),
    PRIMARY KEY (execucao_id, tecnica_id)
);

CREATE TABLE IF NOT EXISTS execucao_equipamento (
    execucao_id      TEXT NOT NULL REFERENCES execucoes(id),
    equipamento_id   TEXT NOT NULL REFERENCES equipamentos(id),
    PRIMARY KEY (execucao_id, equipamento_id)
);

CREATE TABLE IF NOT EXISTS experimento_receita (
    experimento_id   TEXT NOT NULL REFERENCES experimentos(id),
    receita_id       TEXT NOT NULL REFERENCES receitas(id),
    papel            TEXT CHECK(papel IN ('base','originada')) NOT NULL DEFAULT 'originada',
    PRIMARY KEY (experimento_id, receita_id, papel)
);

-- -------------------------------------------------------------
-- TABELA DE HISTÓRICO DE ESTADOS
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS historico_estados (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    entidade_id      TEXT NOT NULL,
    entidade_tipo    TEXT NOT NULL,
    estado_anterior  TEXT,
    estado_novo      TEXT NOT NULL,
    autor            TEXT,
    nota             TEXT,
    registrado_em    TEXT NOT NULL               -- ISO 8601
);

-- -------------------------------------------------------------
-- ÍNDICES PARA PERFORMANCE
-- -------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_receitas_status        ON receitas(status);
CREATE INDEX IF NOT EXISTS idx_receitas_autor         ON receitas(autor);
CREATE INDEX IF NOT EXISTS idx_ingredientes_status    ON ingredientes(status);
CREATE INDEX IF NOT EXISTS idx_tecnicas_status        ON tecnicas(status);
CREATE INDEX IF NOT EXISTS idx_equipamentos_status    ON equipamentos(status);
CREATE INDEX IF NOT EXISTS idx_execucoes_receita      ON execucoes(receita_id);
CREATE INDEX IF NOT EXISTS idx_execucoes_data         ON execucoes(data_execucao);
CREATE INDEX IF NOT EXISTS idx_observacoes_entidade   ON observacoes(entidade_id, entidade_tipo);
CREATE INDEX IF NOT EXISTS idx_experimentos_status    ON experimentos(status);
CREATE INDEX IF NOT EXISTS idx_historico_entidade     ON historico_estados(entidade_id, entidade_tipo);

-- -------------------------------------------------------------
-- VIEWS ÚTEIS
-- -------------------------------------------------------------

-- Receitas ativas com contagem de execuções
CREATE VIEW IF NOT EXISTS vw_receitas_ativas AS
SELECT
    r.id,
    r.titulo,
    r.status,
    r.dificuldade,
    r.autor,
    r.criado_em,
    COUNT(e.id) AS total_execucoes,
    MAX(e.data_execucao) AS ultima_execucao
FROM receitas r
LEFT JOIN execucoes e ON e.receita_id = r.id
WHERE r.status NOT IN ('arquivada')
GROUP BY r.id;

-- Ingredientes mais usados
CREATE VIEW IF NOT EXISTS vw_ingredientes_uso AS
SELECT
    i.id,
    i.nome,
    i.tipo_ingrediente,
    COUNT(DISTINCT ri.receita_id) AS total_receitas,
    COUNT(DISTINCT ei.execucao_id) AS total_execucoes
FROM ingredientes i
LEFT JOIN receita_ingrediente ri ON ri.ingrediente_id = i.id
LEFT JOIN execucao_ingrediente ei ON ei.ingrediente_id = i.id
WHERE i.status = 'ativo'
GROUP BY i.id;

-- -------------------------------------------------------------
-- NOTA DE RECONSTRUÇÃO
-- -------------------------------------------------------------
-- Este banco é derivado de dados/ e pode ser reconstruído a
-- qualquer momento com: scripts/importacao/reconstruir.sh
-- Em caso de conflito entre SQLite e Markdown, o Markdown prevalece.
-- =============================================================
