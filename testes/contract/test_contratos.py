"""Testes de contrato — verifica que os módulos respeitam seus contratos formais."""
import pytest
from codigo.ir import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph
from codigo.resolvedor import resolver, ResolverError
from codigo.validador import validar, ValidationIssue
from codigo.importador import ImportResult


# --- Contrato: resolvedor ---

def test_contrato_resolver_retorna_lista():
    g = KnowledgeGraph()
    result = resolver(g)
    assert isinstance(result, list)


def test_contrato_resolver_error_tem_campos():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "ING-999999", EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER),
    ])
    g = KnowledgeGraph()
    g.add_entity(rec)
    erros = resolver(g)
    assert len(erros) == 1
    e = erros[0]
    assert hasattr(e, 'source')
    assert hasattr(e, 'target')
    assert hasattr(e, 'kind')
    assert hasattr(e, 'erro')


# --- Contrato: validador ---

def test_contrato_validar_retorna_lista():
    g = KnowledgeGraph()
    result = validar(g)
    assert isinstance(result, list)


def test_contrato_validation_issue_tem_campos():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "EXE-000001", EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER),
    ])
    exe = Entity("EXE-000001", "execucao", {}, "", outgoing=[
        Edge("EXE-000001", "REC-000001", EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER),
    ])
    g = KnowledgeGraph()
    g.add_entity(rec)
    g.add_entity(exe)
    issues = validar(g)
    assert len(issues) >= 1
    i = issues[0]
    assert hasattr(i, 'entity_id')
    assert hasattr(i, 'tipo_issue')
    assert hasattr(i, 'severidade')
    assert hasattr(i, 'mensagem')
    assert i.severidade in {'CRITICO', 'AVISO', 'INFO'}


# --- Contrato: importador ---

def test_contrato_import_result_tem_campos(tmp_path):
    from codigo.importador import importar
    g = KnowledgeGraph()
    db = tmp_path / 'test.db'
    result = importar(g, db)
    assert isinstance(result, ImportResult)
    assert hasattr(result, 'inseridos')
    assert hasattr(result, 'atualizados')
    assert hasattr(result, 'erros')
    assert isinstance(result.erros, list)


# --- Contrato: EdgeKind — regras de ciclo ---

def test_contrato_strict_kinds_proibem_ciclo():
    """Todos os kinds que proíbem ciclo devem gerar CRITICO."""
    strict = [EdgeKind.STRUCTURAL, EdgeKind.COMPOSITIONAL,
              EdgeKind.HIERARCHICAL, EdgeKind.DERIVATION]
    for kind in strict:
        a = Entity("REC-000001", "receita", {}, "", outgoing=[
            Edge("REC-000001", "EXE-000001", kind, EdgeOrigin.FRONTMATTER),
        ])
        b = Entity("EXE-000001", "execucao", {}, "", outgoing=[
            Edge("EXE-000001", "REC-000001", kind, EdgeOrigin.FRONTMATTER),
        ])
        g = KnowledgeGraph()
        g.add_entity(a)
        g.add_entity(b)
        issues = validar(g)
        criticos = [i for i in issues if i.severidade == 'CRITICO']
        assert criticos, f"EdgeKind.{kind.name} deveria gerar CRITICO em ciclo"


def test_contrato_loose_kinds_permitem_ciclo():
    """Kinds informativos não devem gerar CRITICO em ciclo."""
    for kind in [EdgeKind.INFORMATIONAL, EdgeKind.OPTIONAL]:
        a = Entity("REC-000001", "receita", {}, "", outgoing=[
            Edge("REC-000001", "OBS-000001", kind, EdgeOrigin.BODY),
        ])
        b = Entity("OBS-000001", "observacao", {}, "", outgoing=[
            Edge("OBS-000001", "REC-000001", kind, EdgeOrigin.BODY),
        ])
        g = KnowledgeGraph()
        g.add_entity(a)
        g.add_entity(b)
        issues = validar(g)
        criticos = [i for i in issues if i.severidade == 'CRITICO']
        assert not criticos, f"EdgeKind.{kind.name} não deveria gerar CRITICO"
