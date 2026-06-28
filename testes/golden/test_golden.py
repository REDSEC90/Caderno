"""Testes golden — valida comportamento contra datasets fixos."""
from pathlib import Path
import pytest

from codigo.parser import parse_directory
from codigo.resolvedor import resolver
from codigo.validador import validar
from codigo.importador import importar

GOLDEN = Path(__file__).parent.parent / 'golden'


def test_golden_minimal_sem_issues(tmp_path):
    grafo = parse_directory(GOLDEN / 'minimal')
    resolver(grafo)
    issues = validar(grafo)
    criticos = [i for i in issues if i.severidade == 'CRITICO']
    assert criticos == []
    result = importar(grafo, tmp_path / 'minimal.db')
    assert result.erros == []
    assert result.inseridos == 2  # 1 receita + 1 ingrediente


def test_golden_invalid_detecta_ciclo():
    grafo = parse_directory(GOLDEN / 'invalid')
    resolver(grafo)
    issues = validar(grafo)
    criticos = [i for i in issues if i.severidade == 'CRITICO' and i.tipo_issue == 'ciclo']
    assert criticos, "Dataset inválido deve gerar pelo menos 1 ciclo crítico"
