"""Testes unitários do importador.py — cobertura completa."""
from pathlib import Path
import sqlite3
import tempfile
import pytest

from codigo.importador import (
    importar, ImportResult, _tipo_from_id, _row_for,
    _TIPO_TABELA, _N2N, _PREFIX_TIPO
)
from codigo.ir import Entity, Edge, EdgeKind, EdgeOrigin, KnowledgeGraph


@pytest.fixture
def temp_db():
    """Cria banco temporário para testes."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    yield db_path
    db_path.unlink(missing_ok=True)


@pytest.fixture
def grafo_simples():
    """Grafo com uma receita e um ingrediente."""
    grafo = KnowledgeGraph()
    
    receita = Entity(
        id='REC-000001',
        tipo='receita',
        metadata={
            'id': 'REC-000001',
            'titulo': 'Pão Simples',
            'versao': 1,
            'status': 'validada',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
            'modo-de-preparo': 'Misturar e assar',
        },
        body='# Pão\n\nInstruções...',
        outgoing=[
            Edge('REC-000001', 'ING-000001', EdgeKind.COMPOSITIONAL, EdgeOrigin.BODY, None)
        ]
    )
    
    ingrediente = Entity(
        id='ING-000001',
        tipo='ingrediente',
        metadata={
            'id': 'ING-000001',
            'nome': 'Farinha de trigo',
            'versao': 1,
            'status': 'ativo',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
        },
        body='',
        outgoing=[]
    )
    
    grafo.add_entity(receita)
    grafo.add_entity(ingrediente)
    return grafo


def test_tipo_from_id():
    """_tipo_from_id extrai tipo do prefixo do ID."""
    assert _tipo_from_id('REC-000001') == 'receita'
    assert _tipo_from_id('ING-000042') == 'ingrediente'
    assert _tipo_from_id('TEC-000003') == 'tecnica'
    assert _tipo_from_id('EQP-999999') == 'equipamento'
    assert _tipo_from_id('EXE-000001') == 'execucao'
    assert _tipo_from_id('OBS-000001') == 'observacao'
    assert _tipo_from_id('EXP-000001') == 'experimento'
    assert _tipo_from_id('XYZ-000001') is None
    assert _tipo_from_id('invalido') is None


def test_row_for_receita():
    """_row_for constrói linha correta para receita."""
    entity = Entity(
        id='REC-000001',
        tipo='receita',
        metadata={
            'id': 'REC-000001',
            'titulo': 'Pão',
            'descricao': 'Pão caseiro',
            'versao': 2,
            'status': 'publicada',
            'autor': 'Chef',
            'criado-em': '2026-01-01',
            'atualizado-em': '2026-06-01',
            'rendimento': '4 porções',
            'tempo-preparo': '30 minutos',
            'modo-de-preparo': 'Misture tudo',
            'origem': 'França',
            'tags': ['pao', 'basico'],
            'notas': 'Receita testada',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['id'] == 'REC-000001'
    assert row['titulo'] == 'Pão'
    assert row['descricao'] == 'Pão caseiro'
    assert row['versao'] == 2
    assert row['status'] == 'publicada'
    assert row['autor'] == 'Chef'
    assert row['rendimento'] == '4 porções'
    assert row['tempo_preparo'] == '30 minutos'
    assert row['modo_de_preparo'] == 'Misture tudo'
    assert row['origem'] == 'França'
    assert row['notas'] == 'Receita testada'
    assert "['pao', 'basico']" in row['tags']


def test_row_for_ingrediente():
    """_row_for constrói linha correta para ingrediente."""
    entity = Entity(
        id='ING-000001',
        tipo='ingrediente',
        metadata={
            'id': 'ING-000001',
            'nome': 'Farinha',
            'tipo-ingrediente': 'grao',
            'descricao': 'Farinha de trigo branca',
            'versao': 1,
            'status': 'ativo',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
            'notas': 'Tipo 1',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['id'] == 'ING-000001'
    assert row['nome'] == 'Farinha'
    assert row['tipo_ingrediente'] == 'grao'
    assert row['descricao'] == 'Farinha de trigo branca'
    assert row['notas'] == 'Tipo 1'


def test_row_for_tecnica():
    """_row_for constrói linha correta para técnica."""
    entity = Entity(
        id='TEC-000001',
        tipo='tecnica',
        metadata={
            'id': 'TEC-000001',
            'nome': 'Fermentação',
            'tipo-tecnica': 'preparo',
            'descricao': 'Fermentação natural',
            'dificuldade': 'média',
            'versao': 1,
            'status': 'ativo',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['nome'] == 'Fermentação'
    assert row['tipo_tecnica'] == 'preparo'
    assert row['dificuldade'] == 'média'


def test_row_for_equipamento():
    """_row_for constrói linha correta para equipamento."""
    entity = Entity(
        id='EQP-000001',
        tipo='equipamento',
        metadata={
            'id': 'EQP-000001',
            'nome': 'Forno',
            'tipo-equipamento': 'cocao',
            'descricao': 'Forno elétrico',
            'versao': 1,
            'status': 'ativo',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['nome'] == 'Forno'
    assert row['tipo_equipamento'] == 'cocao'


def test_row_for_execucao():
    """_row_for constrói linha correta para execução."""
    entity = Entity(
        id='EXE-000001',
        tipo='execucao',
        metadata={
            'id': 'EXE-000001',
            'receita-id': 'REC-000001',
            'data-execucao': '2026-07-01',
            'avaliacao-sabor': 9,
            'avaliacao-textura': 8,
            'avaliacao-aparencia': 7,
            'avaliacao-geral': 8,
            'versao': 1,
            'status': 'consolidada',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
            'notas': 'Ficou ótimo',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['receita_id'] == 'REC-000001'
    assert row['data_execucao'] == '2026-07-01'
    assert row['avaliacao_sabor'] == 9
    assert row['avaliacao_textura'] == 8
    assert row['avaliacao_geral'] == 8


def test_row_for_observacao():
    """_row_for constrói linha correta para observação."""
    entity = Entity(
        id='OBS-000001',
        tipo='observacao',
        metadata={
            'id': 'OBS-000001',
            'entidade-referenciada': 'REC-000001',
            'tipo-entidade': 'receita',
            'relevancia': 'alta',
            'versao': 1,
            'status': 'consolidada',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
        },
        body='Observação importante sobre a receita.',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['entidade_id'] == 'REC-000001'
    assert row['entidade_tipo'] == 'receita'
    assert row['conteudo'] == 'Observação importante sobre a receita.'
    assert row['relevancia'] == 'alta'


def test_row_for_experimento():
    """_row_for constrói linha correta para experimento."""
    entity = Entity(
        id='EXP-000001',
        tipo='experimento',
        metadata={
            'id': 'EXP-000001',
            'titulo': 'Experimento de fermentação',
            'hipotese': 'Fermentação mais longa melhora sabor',
            'receita-base-id': 'REC-000001',
            'versao': 1,
            'status': 'rascunho',
            'autor': 'teste',
            'criado-em': '2026-07-01',
            'atualizado-em': '2026-07-01',
            'notas': 'Primeiro teste',
        },
        body='',
        outgoing=[]
    )
    
    row = _row_for(entity)
    assert row is not None
    assert row['titulo'] == 'Experimento de fermentação'
    assert row['hipotese'] == 'Fermentação mais longa melhora sabor'
    assert row['receita_base_id'] == 'REC-000001'


def test_row_for_tipo_desconhecido():
    """_row_for retorna None para tipo não mapeado."""
    entity = Entity(
        id='UNK-000001',
        tipo='desconhecido',
        metadata={'id': 'UNK-000001'},
        body='',
        outgoing=[]
    )
    
    assert _row_for(entity) is None


def test_importar_insercao_basica(temp_db, grafo_simples):
    """Importar insere entidades novas corretamente."""
    result = importar(grafo_simples, temp_db)
    
    assert result.inseridos == 2
    assert result.atualizados == 0
    assert len(result.erros) == 0
    
    # Verificar que entidades estão no banco
    conn = sqlite3.connect(str(temp_db))
    receitas = conn.execute('SELECT id FROM receitas').fetchall()
    ingredientes = conn.execute('SELECT id FROM ingredientes').fetchall()
    conn.close()
    
    assert len(receitas) == 1
    assert receitas[0][0] == 'REC-000001'
    assert len(ingredientes) == 1
    assert ingredientes[0][0] == 'ING-000001'


def test_importar_atualizacao(temp_db, grafo_simples):
    """Importar atualiza entidades existentes."""
    # Primeira importação
    importar(grafo_simples, temp_db)
    
    # Modificar metadata
    receita = grafo_simples.get_entity('REC-000001')
    receita.metadata['status'] = 'arquivada'
    
    # Segunda importação
    result = importar(grafo_simples, temp_db)
    
    assert result.inseridos == 0
    assert result.atualizados == 2  # receita + ingrediente
    assert len(result.erros) == 0
    
    # Verificar que status foi atualizado
    conn = sqlite3.connect(str(temp_db))
    status = conn.execute('SELECT status FROM receitas WHERE id = ?', ('REC-000001',)).fetchone()
    conn.close()
    
    assert status[0] == 'arquivada'


def test_importar_aresta_n2n(temp_db, grafo_simples):
    """Importar persiste arestas N:N em tabelas específicas."""
    result = importar(grafo_simples, temp_db)
    
    assert len(result.erros) == 0
    
    # Verificar tabela receita_ingrediente
    conn = sqlite3.connect(str(temp_db))
    rows = conn.execute('SELECT receita_id, ingrediente_id FROM receita_ingrediente').fetchall()
    conn.close()
    
    assert len(rows) == 1
    assert rows[0] == ('REC-000001', 'ING-000001')


def test_importar_relacionamentos(temp_db, grafo_simples):
    """Importar persiste todas as arestas na tabela relacionamentos."""
    result = importar(grafo_simples, temp_db)
    
    assert len(result.erros) == 0
    
    conn = sqlite3.connect(str(temp_db))
    rows = conn.execute('SELECT source, target, kind FROM relacionamentos').fetchall()
    conn.close()
    
    assert len(rows) == 1
    assert rows[0][0] == 'REC-000001'
    assert rows[0][1] == 'ING-000001'
    assert rows[0][2] == 'COMPOSITIONAL'


def test_importar_historico_mudanca_status(temp_db, grafo_simples):
    """Importar registra mudança de status no histórico."""
    # Primeira importação
    importar(grafo_simples, temp_db)
    
    # Modificar status
    receita = grafo_simples.get_entity('REC-000001')
    receita.metadata['status'] = 'arquivada'
    
    # Segunda importação
    importar(grafo_simples, temp_db)
    
    # Verificar histórico
    conn = sqlite3.connect(str(temp_db))
    historico = conn.execute(
        'SELECT entidade_id, estado_anterior, estado_novo FROM historico_estados'
    ).fetchall()
    conn.close()
    
    assert len(historico) == 1
    assert historico[0] == ('REC-000001', 'validada', 'arquivada')


def test_importar_idempotencia(temp_db, grafo_simples):
    """Importar é idempotente — múltiplas execuções produzem mesmo resultado."""
    result1 = importar(grafo_simples, temp_db)
    result2 = importar(grafo_simples, temp_db)
    result3 = importar(grafo_simples, temp_db)
    
    # Primeira inseriu, outras atualizaram
    assert result1.inseridos == 2
    assert result2.atualizados == 2
    assert result3.atualizados == 2
    
    # Estado final do banco é idêntico
    conn = sqlite3.connect(str(temp_db))
    count = conn.execute('SELECT COUNT(*) FROM receitas').fetchone()[0]
    conn.close()
    
    assert count == 1


def test_importar_grafo_vazio(temp_db):
    """Importar com grafo vazio não gera erros."""
    grafo = KnowledgeGraph()
    result = importar(grafo, temp_db)
    
    assert result.inseridos == 0
    assert result.atualizados == 0
    assert len(result.erros) == 0
