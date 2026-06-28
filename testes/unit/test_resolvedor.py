"""Testes unitários — Resolvedor (soe_ccg.resolvedor)."""
from codigo.ir import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph
from codigo.resolvedor import resolver, ResolverError


def _graph(*entities: Entity) -> KnowledgeGraph:
    g = KnowledgeGraph()
    for e in entities:
        g.add_entity(e)
    return g


def test_resolver_sem_erros():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "ING-000001", EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER),
    ])
    ing = Entity("ING-000001", "ingrediente", {}, "")
    g = _graph(rec, ing)
    erros = resolver(g)
    assert erros == []
    assert len(ing.incoming) == 1
    assert ing.incoming[0].source == "REC-000001"


def test_resolver_referencia_quebrada():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "ING-999999", EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER),
    ])
    g = _graph(rec)
    erros = resolver(g)
    assert len(erros) == 1
    assert isinstance(erros[0], ResolverError)
    assert erros[0].target == "ING-999999"
    assert erros[0].erro == "referencia_quebrada"


def test_resolver_nao_cria_incoming_para_targets_faltantes():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "ING-000001", EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER),
    ])
    g = _graph(rec)
    resolver(g)
    assert rec.incoming == []  # nenhum incoming no próprio rec
