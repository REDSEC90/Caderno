"""Testes de integração — pipeline completo: parse → resolver → validar → importar."""
import sqlite3
from pathlib import Path
import pytest

from codigo.parser import parse_directory
from codigo.resolvedor import resolver
from codigo.validador import validar
from codigo.importador import importar


@pytest.fixture
def dados_reais():
    return Path(__file__).parent.parent.parent / 'dados'


@pytest.fixture
def db_temp(tmp_path):
    return tmp_path / 'test.db'


def test_pipeline_dados_reais(dados_reais, db_temp):
    """Pipeline completo sobre dados/ reais deve ter 0 issues críticos."""
    grafo = parse_directory(dados_reais)
    assert len(grafo.entities) > 0

    erros_ref = resolver(grafo)
    issues = validar(grafo)

    criticos = [i for i in issues if i.severidade == 'CRITICO']
    assert criticos == [], f"Issues críticos: {criticos}"

    result = importar(grafo, db_temp)
    assert result.erros == [], f"Erros de importação: {result.erros}"
    assert result.inseridos > 0


def test_pipeline_importacao_idempotente(dados_reais, db_temp):
    """Importar duas vezes deve produzir o mesmo resultado."""
    grafo = parse_directory(dados_reais)
    resolver(grafo)

    r1 = importar(grafo, db_temp)

    # segundo parse + import
    grafo2 = parse_directory(dados_reais)
    resolver(grafo2)
    r2 = importar(grafo2, db_temp)

    assert r2.erros == []
    # segunda vez: tudo atualizado, nada inserido
    assert r2.inseridos == 0
    assert r2.atualizados == r1.inseridos


def test_banco_contem_entidades_esperadas(dados_reais, db_temp):
    grafo = parse_directory(dados_reais)
    resolver(grafo)
    importar(grafo, db_temp)

    conn = sqlite3.connect(str(db_temp))
    ids_receitas = {r[0] for r in conn.execute('SELECT id FROM receitas').fetchall()}
    ids_ing = {r[0] for r in conn.execute('SELECT id FROM ingredientes').fetchall()}
    conn.close()

    assert 'REC-000001' in ids_receitas
    assert 'ING-000001' in ids_ing


def test_banco_relacionamentos_presentes(dados_reais, db_temp):
    grafo = parse_directory(dados_reais)
    resolver(grafo)
    importar(grafo, db_temp)

    conn = sqlite3.connect(str(db_temp))
    count = conn.execute('SELECT COUNT(*) FROM relacionamentos').fetchone()[0]
    conn.close()
    assert count > 0
