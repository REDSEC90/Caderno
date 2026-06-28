"""
Importador KnowledgeGraph -> SQLite  (SOE-CCG v1)
Recebe um KnowledgeGraph já resolvido. Nunca lê Markdown diretamente.
"""
from __future__ import annotations
import importlib.util
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/redsec/Ambiente/SOE-CCG')
SCHEMA = ROOT / 'banco_de_dados' / 'esquemas' / 'schema-sqlite-v1.sql'
DB_PATH = ROOT / 'banco_de_dados' / 'sqlite' / 'soe-ccg.db'

_TIPO_TABELA = {
    'receita':     'receitas',
    'ingrediente': 'ingredientes',
    'tecnica':     'tecnicas',
    'equipamento': 'equipamentos',
    'execucao':    'execucoes',
    'observacao':  'observacoes',
    'experimento': 'experimentos',
}

_STRUCTURAL_KINDS = {'STRUCTURAL', 'COMPOSITIONAL', 'HIERARCHICAL', 'DERIVATION'}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text(encoding='utf-8'))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relacionamentos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            source     TEXT NOT NULL,
            target     TEXT NOT NULL,
            kind       TEXT NOT NULL,
            origin     TEXT NOT NULL,
            location   TEXT,
            criado_em  TEXT NOT NULL
        )
    """)
    conn.commit()


def _row_receita(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, titulo=m.get('titulo', ''), descricao=m.get('descricao'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'rascunho'),
        rendimento=m.get('rendimento'), tempo_preparo=m.get('tempo-preparo'),
        modo_de_preparo=m.get('modo-de-preparo', ''),
        notas=m.get('notas'), origem=m.get('origem'), autor=m.get('autor', ''),
        tags=str(m.get('tags', [])),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_ingrediente(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, nome=m.get('nome', ''), tipo_ingrediente=m.get('tipo-ingrediente'),
        descricao=m.get('descricao'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'ativo'), notas=m.get('notas'),
        autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_tecnica(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, nome=m.get('nome', ''), tipo_tecnica=m.get('tipo-tecnica'),
        descricao=m.get('descricao'), dificuldade=m.get('dificuldade'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'ativo'), notas=m.get('notas'),
        autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_equipamento(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, nome=m.get('nome', ''), tipo_equipamento=m.get('tipo-equipamento'),
        descricao=m.get('descricao'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'ativo'), notas=m.get('notas'),
        autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_execucao(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, receita_id=m.get('receita-id', ''),
        data_execucao=m.get('data-execucao', ''),
        avaliacao_sabor=m.get('avaliacao-sabor'), avaliacao_textura=m.get('avaliacao-textura'),
        avaliacao_aparencia=m.get('avaliacao-aparencia'), avaliacao_geral=m.get('avaliacao-geral'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'registrada'), notas=m.get('notas'),
        autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_observacao(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, conteudo=e.body,
        entidade_id=m.get('entidade-referenciada'), entidade_tipo=m.get('tipo-entidade'),
        relevancia=m.get('relevancia'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'ativo'), autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


def _row_experimento(e) -> dict:
    m = e.metadata
    return dict(
        id=e.id, titulo=m.get('titulo', ''), hipotese=m.get('hipotese', ''),
        receita_base_id=m.get('receita-base-id'),
        schema_version=m.get('schema_version', 1), versao=m.get('versao', 1),
        status=m.get('status', 'aberto'), notas=m.get('notas'),
        autor=m.get('autor', ''),
        criado_em=m.get('criado-em', ''), atualizado_em=m.get('atualizado-em', ''),
    )


_ROW_BUILDERS = {
    'receita':     _row_receita,
    'ingrediente': _row_ingrediente,
    'tecnica':     _row_tecnica,
    'equipamento': _row_equipamento,
    'execucao':    _row_execucao,
    'observacao':  _row_observacao,
    'experimento': _row_experimento,
}

_N2N_COMPOSITIONAL = {
    ('receita',   'ingrediente'): ('receita_ingrediente',  'receita_id',  'ingrediente_id'),
    ('receita',   'tecnica'):     ('receita_tecnica',       'receita_id',  'tecnica_id'),
    ('receita',   'equipamento'): ('receita_equipamento',   'receita_id',  'equipamento_id'),
    ('execucao',  'ingrediente'): ('execucao_ingrediente',  'execucao_id', 'ingrediente_id'),
    ('execucao',  'tecnica'):     ('execucao_tecnica',      'execucao_id', 'tecnica_id'),
    ('execucao',  'equipamento'): ('execucao_equipamento',  'execucao_id', 'equipamento_id'),
}


def _tipo_from_id(entity_id: str) -> str | None:
    prefix_map = {
        'REC': 'receita', 'ING': 'ingrediente', 'TEC': 'tecnica',
        'EQP': 'equipamento', 'EXE': 'execucao', 'OBS': 'observacao',
        'EXP': 'experimento',
    }
    return prefix_map.get(entity_id.split('-')[0])


def importar(grafo, db_path: Path = DB_PATH) -> dict:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    _init_db(conn)

    inseridos = 0
    atualizados = 0
    erros: list[str] = []
    now = datetime.now(timezone.utc).isoformat()

    # --- Import entities ---
    for entity in grafo.entities.values():
        tipo = entity.tipo.lower()
        builder = _ROW_BUILDERS.get(tipo)
        tabela = _TIPO_TABELA.get(tipo)
        if not builder or not tabela:
            continue
        try:
            row = builder(entity)
            cols = ', '.join(row.keys())
            placeholders = ', '.join(':' + k for k in row.keys())
            # detect insert vs update
            existing = conn.execute(
                f'SELECT id FROM {tabela} WHERE id = :id', {'id': entity.id}
            ).fetchone()
            conn.execute(
                f'INSERT OR REPLACE INTO {tabela} ({cols}) VALUES ({placeholders})', row
            )
            if existing:
                atualizados += 1
            else:
                inseridos += 1
        except Exception as exc:
            erros.append(f'{entity.id}: {exc}')

    conn.commit()

    # --- N:N COMPOSITIONAL edges ---
    for entity in grafo.entities.values():
        src_tipo = entity.tipo.lower()
        for edge in entity.outgoing:
            if edge.kind.value != 'COMPOSITIONAL':
                continue
            tgt_tipo = _tipo_from_id(edge.target)
            mapping = _N2N_COMPOSITIONAL.get((src_tipo, tgt_tipo))
            if not mapping:
                continue
            tabela, col_src, col_tgt = mapping
            extra = {'substituicao': 0} if tabela == 'execucao_ingrediente' else {}
            try:
                row = {col_src: edge.source, col_tgt: edge.target, **extra}
                cols = ', '.join(row.keys())
                placeholders = ', '.join(':' + k for k in row.keys())
                conn.execute(
                    f'INSERT OR REPLACE INTO {tabela} ({cols}) VALUES ({placeholders})', row
                )
            except Exception as exc:
                erros.append(f'N:N {edge.source}->{edge.target}: {exc}')

    conn.commit()

    # --- All edges -> relacionamentos ---
    conn.execute('DELETE FROM relacionamentos')
    for entity in grafo.entities.values():
        for edge in entity.outgoing:
            try:
                conn.execute(
                    'INSERT INTO relacionamentos (source, target, kind, origin, location, criado_em) '
                    'VALUES (:source, :target, :kind, :origin, :location, :criado_em)',
                    {
                        'source': edge.source, 'target': edge.target,
                        'kind': edge.kind.value, 'origin': edge.origin.value,
                        'location': edge.location, 'criado_em': now,
                    }
                )
            except Exception as exc:
                erros.append(f'rel {edge.source}->{edge.target}: {exc}')

    conn.commit()
    conn.close()
    return {'inseridos': inseridos, 'atualizados': atualizados, 'erros': erros}


if __name__ == '__main__':
    codigo = Path(__file__).parent
    ir_mod      = _load_module('ir_v1',        codigo / 'ir-v1.py')
    parser_mod  = _load_module('parser_v1',    codigo / 'parser-v1.py')
    resolvedor  = _load_module('resolvedor_v1', codigo / 'resolvedor-v1.py')

    grafo = parser_mod.parse_directory(ROOT / 'dados')
    erros_resolucao = resolvedor.resolver(grafo)
    resultado = importar(grafo)

    print(f"Inseridos : {resultado['inseridos']}")
    print(f"Atualizados: {resultado['atualizados']}")
    print(f"Erros     : {len(resultado['erros'])}")
    if resultado['erros']:
        for e in resultado['erros']:
            print(f"  [ERRO] {e}")
    if erros_resolucao:
        print(f"Referências quebradas: {len(erros_resolucao)}")
        for e in erros_resolucao:
            print(f"  [REF] {e['source']} -> {e['target']}")
