"""Importador — KnowledgeGraph → SQLite.

Contrato (FASE 2):
  Entrada : KnowledgeGraph já resolvido; Path para o arquivo .db (opcional).
  Saída   : ImportResult com contagens e erros.
  Persistência:
    - Inicializa o banco via schema-sqlite-v1.sql se tabelas não existirem.
    - Usa INSERT OR REPLACE para cada entidade (idempotente).
    - Persiste todas as arestas na tabela `relacionamentos`.
    - Persiste arestas N:N em tabelas específicas (receita_ingrediente, etc.).
  Rollback: em caso de erro crítico, a conexão é fechada sem commit.
  Rebuild : executar com banco vazio produz resultado idêntico a qualquer momento
            (o Markdown é a fonte de verdade — ADR-0001).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .ir import KnowledgeGraph

ROOT     = Path(__file__).parent.parent
SCHEMA   = ROOT / 'banco_de_dados' / 'esquemas' / 'schema-sqlite-v1.sql'
DB_PATH  = ROOT / 'banco_de_dados' / 'sqlite' / 'soe-ccg.db'

_TIPO_TABELA = {
    'receita':     'receitas',
    'ingrediente': 'ingredientes',
    'tecnica':     'tecnicas',
    'equipamento': 'equipamentos',
    'execucao':    'execucoes',
    'observacao':  'observacoes',
    'experimento': 'experimentos',
}

_N2N = {
    ('receita',  'ingrediente'): ('receita_ingrediente',  'receita_id',  'ingrediente_id'),
    ('receita',  'tecnica'):     ('receita_tecnica',       'receita_id',  'tecnica_id'),
    ('receita',  'equipamento'): ('receita_equipamento',   'receita_id',  'equipamento_id'),
    ('execucao', 'ingrediente'): ('execucao_ingrediente',  'execucao_id', 'ingrediente_id'),
    ('execucao', 'tecnica'):     ('execucao_tecnica',      'execucao_id', 'tecnica_id'),
    ('execucao', 'equipamento'): ('execucao_equipamento',  'execucao_id', 'equipamento_id'),
}

_PREFIX_TIPO = {
    'REC': 'receita', 'ING': 'ingrediente', 'TEC': 'tecnica',
    'EQP': 'equipamento', 'EXE': 'execucao', 'OBS': 'observacao', 'EXP': 'experimento',
}


@dataclass
class ImportResult:
    inseridos:   int = 0
    atualizados: int = 0
    erros:       list[str] = field(default_factory=list)


def _tipo_from_id(eid: str) -> str | None:
    return _PREFIX_TIPO.get(eid.split('-')[0])


def _row_for(entity) -> dict | None:
    """Constrói o dicionário de colunas para cada tipo de entidade."""
    m  = entity.metadata
    t  = entity.tipo.lower()

    def _str(v: object) -> str | None:
        """Converte qualquer valor para string, garantindo que datas não gerem DeprecationWarning."""
        return str(v) if v is not None else None

    base = dict(
        id=entity.id,
        schema_version=m.get('schema_version', 1),
        versao=m.get('versao', 1),
        status=m.get('status', 'rascunho'),
        autor=m.get('autor', ''),
        criado_em=_str(m.get('criado-em', '')),
        atualizado_em=_str(m.get('atualizado-em', '')),
    )
    if t == 'receita':
        return {**base, 'notas': m.get('notas'),
                'titulo': m.get('titulo', ''), 'descricao': m.get('descricao'),
                'rendimento': m.get('rendimento'), 'tempo_preparo': m.get('tempo-preparo'),
                'modo_de_preparo': m.get('modo-de-preparo', ''),
                'origem': m.get('origem'), 'tags': str(m.get('tags', []))}
    if t == 'ingrediente':
        return {**base, 'notas': m.get('notas'),
                'nome': m.get('nome', ''), 'tipo_ingrediente': m.get('tipo-ingrediente'),
                'descricao': m.get('descricao')}
    if t == 'tecnica':
        return {**base, 'notas': m.get('notas'),
                'nome': m.get('nome', ''), 'tipo_tecnica': m.get('tipo-tecnica'),
                'descricao': m.get('descricao'), 'dificuldade': m.get('dificuldade')}
    if t == 'equipamento':
        return {**base, 'notas': m.get('notas'),
                'nome': m.get('nome', ''), 'tipo_equipamento': m.get('tipo-equipamento'),
                'descricao': m.get('descricao')}
    if t == 'execucao':
        return {**base, 'notas': m.get('notas'),
                'receita_id': m.get('receita-id', ''),
                'data_execucao': _str(m.get('data-execucao', '')),
                'avaliacao_sabor': m.get('avaliacao-sabor'),
                'avaliacao_textura': m.get('avaliacao-textura'),
                'avaliacao_aparencia': m.get('avaliacao-aparencia'),
                'avaliacao_geral': m.get('avaliacao-geral')}
    if t == 'observacao':
        return {**base,
                'conteudo': entity.body,
                'entidade_id': m.get('entidade-referenciada'),
                'entidade_tipo': m.get('tipo-entidade'),
                'relevancia': m.get('relevancia')}
    if t == 'experimento':
        return {**base, 'notas': m.get('notas'),
                'titulo': m.get('titulo', ''), 'hipotese': m.get('hipotese', ''),
                'receita_base_id': m.get('receita-base-id')}
    return None


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text(encoding='utf-8'))
    # Seeds de categorias
    seeds_path = SCHEMA.parent.parent / 'seeds' / 'seed-categorias-v1.sql'
    if seeds_path.exists():
        conn.executescript(seeds_path.read_text(encoding='utf-8'))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relacionamentos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            source    TEXT NOT NULL,
            target    TEXT NOT NULL,
            kind      TEXT NOT NULL,
            origin    TEXT NOT NULL,
            location  TEXT,
            criado_em TEXT NOT NULL
        )
    """)
    conn.commit()


def importar(grafo: KnowledgeGraph, db_path: Path = DB_PATH) -> ImportResult:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    result = ImportResult()
    now    = datetime.now(timezone.utc).isoformat()

    conn = sqlite3.connect(str(db_path), detect_types=0)
    try:
        _init_db(conn)

        # Entidades — ordem topológica: independentes primeiro, depois dependentes
        _ORDER = ['ingrediente', 'tecnica', 'equipamento', 'receita',
                  'execucao', 'observacao', 'experimento']
        ordered = sorted(
            grafo.entities.values(),
            key=lambda e: _ORDER.index(e.tipo.lower()) if e.tipo.lower() in _ORDER else 99
        )
        for entity in ordered:
            tipo   = entity.tipo.lower()
            tabela = _TIPO_TABELA.get(tipo)
            row    = _row_for(entity)
            if not tabela or row is None:
                continue
            try:
                prev = conn.execute(
                    f'SELECT id, status FROM {tabela} WHERE id = :id', {'id': entity.id}
                ).fetchone()
                cols = ', '.join(row.keys())
                ph   = ', '.join(':' + k for k in row.keys())
                conn.execute(f'INSERT OR REPLACE INTO {tabela} ({cols}) VALUES ({ph})', row)
                if prev:
                    result.atualizados += 1
                    # registrar mudança de status no histórico
                    novo_status = row.get('status')
                    if novo_status and prev[1] != novo_status:
                        conn.execute(
                            'INSERT INTO historico_estados '
                            '(entidade_id, entidade_tipo, estado_anterior, estado_novo, registrado_em, autor) '
                            'VALUES (?, ?, ?, ?, ?, ?)',
                            (entity.id, entity.tipo.lower(), prev[1], novo_status, now,
                             entity.metadata.get('autor', 'sistema'))
                        )
                else:
                    result.inseridos += 1
            except Exception as exc:
                result.erros.append(f'{entity.id}: {exc}')
        conn.commit()

        # Arestas N:N
        for entity in grafo.entities.values():
            for edge in entity.outgoing:
                if edge.kind.value != 'COMPOSITIONAL':
                    continue
                tgt_tipo = _tipo_from_id(edge.target)
                mapping  = _N2N.get((entity.tipo.lower(), tgt_tipo))
                if not mapping:
                    continue
                tabela, col_src, col_tgt = mapping
                extra = {'substituicao': 0} if tabela == 'execucao_ingrediente' else {}
                try:
                    row  = {col_src: edge.source, col_tgt: edge.target, **extra}
                    cols = ', '.join(row.keys())
                    ph   = ', '.join(':' + k for k in row.keys())
                    conn.execute(f'INSERT OR REPLACE INTO {tabela} ({cols}) VALUES ({ph})', row)
                except Exception as exc:
                    result.erros.append(f'N:N {edge.source}->{edge.target}: {exc}')
        conn.commit()

        # Todas as arestas → relacionamentos
        conn.execute('DELETE FROM relacionamentos')
        for entity in grafo.entities.values():
            for edge in entity.outgoing:
                try:
                    conn.execute(
                        'INSERT INTO relacionamentos '
                        '(source, target, kind, origin, location, criado_em) '
                        'VALUES (:source, :target, :kind, :origin, :location, :criado_em)',
                        {'source': edge.source, 'target': edge.target,
                         'kind': edge.kind.value, 'origin': edge.origin.value,
                         'location': edge.location, 'criado_em': now}
                    )
                except Exception as exc:
                    result.erros.append(f'rel {edge.source}->{edge.target}: {exc}')
        conn.commit()
    finally:
        conn.close()

    return result
