"""Testes unitários — Validador (soe_ccg.validador)."""
from codigo.ir import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph
from codigo.validador import validar, ValidationIssue


def _graph(*entities: Entity) -> KnowledgeGraph:
    g = KnowledgeGraph()
    for e in entities:
        g.add_entity(e)
    return g


def test_validar_grafo_limpo():
    rec = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "ING-000001", EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER),
    ])
    ing = Entity("ING-000001", "ingrediente", {}, "")
    issues = validar(_graph(rec, ing))
    assert issues == []


def test_validar_detecta_ciclo_estrutural():
    # A -> B -> A (STRUCTURAL)
    a = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "EXE-000001", EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER),
    ])
    b = Entity("EXE-000001", "execucao", {}, "", outgoing=[
        Edge("EXE-000001", "REC-000001", EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER),
    ])
    issues = validar(_graph(a, b))
    criticos = [i for i in issues if i.severidade == "CRITICO"]
    assert len(criticos) >= 1
    assert criticos[0].tipo_issue == "ciclo"


def test_validar_ciclo_informacional_e_info_nao_critico():
    # A -> B (INFORMATIONAL) -> A (INFORMATIONAL) — ciclo informacional permitido
    a = Entity("REC-000001", "receita", {}, "", outgoing=[
        Edge("REC-000001", "OBS-000001", EdgeKind.INFORMATIONAL, EdgeOrigin.BODY),
    ])
    b = Entity("OBS-000001", "observacao", {}, "", outgoing=[
        Edge("OBS-000001", "REC-000001", EdgeKind.INFORMATIONAL, EdgeOrigin.BODY),
    ])
    issues = validar(_graph(a, b))
    criticos = [i for i in issues if i.severidade == "CRITICO"]
    assert criticos == []
    infos = [i for i in issues if i.severidade == "INFO" and i.tipo_issue == "ciclo"]
    assert len(infos) >= 1


def test_validar_entidade_isolada_gera_aviso():
    rec = Entity("REC-000001", "receita", {}, "")  # sem arestas
    issues = validar(_graph(rec))
    avisos = [i for i in issues if i.tipo_issue == "entidade_isolada"]
    assert len(avisos) == 1
    assert avisos[0].entity_id == "REC-000001"
    assert avisos[0].severidade == "AVISO"


def test_validar_ingrediente_isolado_nao_gera_aviso():
    # Ingredientes não são verificados como isolados
    ing = Entity("ING-000001", "ingrediente", {}, "")
    issues = validar(_graph(ing))
    assert all(i.tipo_issue != "entidade_isolada" for i in issues)
