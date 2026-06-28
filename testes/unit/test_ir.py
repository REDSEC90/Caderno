"""Testes unitários — IR (soe_ccg.ir)."""
import pytest
from codigo.ir import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph


def test_edge_kinds_existem():
    assert EdgeKind.STRUCTURAL.value == "STRUCTURAL"
    assert EdgeKind.INFORMATIONAL.value == "INFORMATIONAL"


def test_knowledge_graph_add_get():
    g = KnowledgeGraph()
    e = Entity(id="REC-000001", tipo="receita", metadata={}, body="")
    g.add_entity(e)
    assert g.get_entity("REC-000001") is e
    assert g.get_entity("XXX-000000") is None


def test_get_edges_by_kind():
    g = KnowledgeGraph()
    e = Entity(id="REC-000001", tipo="receita", metadata={}, body="", outgoing=[
        Edge("REC-000001", "ING-000001", EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER),
        Edge("REC-000001", "TEC-000001", EdgeKind.INFORMATIONAL, EdgeOrigin.BODY),
    ])
    g.add_entity(e)
    comp = g.get_edges_by_kind(EdgeKind.COMPOSITIONAL)
    assert len(comp) == 1
    assert comp[0].target == "ING-000001"
