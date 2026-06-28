"""Testes unitários — Parser (soe_ccg.parser)."""
import textwrap
from pathlib import Path
import pytest
from codigo.parser import parse_file, parse_directory, ParseError
from codigo.ir import EdgeKind, EdgeOrigin


def _write_md(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content), encoding='utf-8')
    return p


def test_parse_file_basico(tmp_path):
    p = _write_md(tmp_path, "REC-000001.md", """\
        ---
        id: REC-000001
        tipo: receita
        titulo: Doce de Leite
        status: rascunho
        autor: teste
        criado-em: 2026-01-01
        atualizado-em: 2026-01-01
        ---
        Receita sem referências.
    """)
    entity = parse_file(p)
    assert entity.id == "REC-000001"
    assert entity.tipo == "receita"
    assert entity.outgoing == []


def test_parse_file_aresta_frontmatter(tmp_path):
    p = _write_md(tmp_path, "REC-000001.md", """\
        ---
        id: REC-000001
        tipo: receita
        ingredientes:
          - ING-000001
          - ING-000002
        ---
        Corpo.
    """)
    entity = parse_file(p)
    kinds = {e.kind for e in entity.outgoing}
    assert EdgeKind.COMPOSITIONAL in kinds
    targets = {e.target for e in entity.outgoing}
    assert "ING-000001" in targets
    assert "ING-000002" in targets


def test_parse_file_aresta_body_informacional(tmp_path):
    p = _write_md(tmp_path, "REC-000001.md", """\
        ---
        id: REC-000001
        tipo: receita
        ---
        Ver técnica TEC-000001 para mais detalhes.
    """)
    entity = parse_file(p)
    assert any(e.kind == EdgeKind.INFORMATIONAL and e.target == "TEC-000001"
               for e in entity.outgoing)


def test_parse_file_aresta_body_tabela_compositional(tmp_path):
    p = _write_md(tmp_path, "REC-000001.md", """\
        ---
        id: REC-000001
        tipo: receita
        ---
        | ingrediente   | qtd |
        |---------------|-----|
        | ING-000001    | 100 |
    """)
    entity = parse_file(p)
    assert any(e.kind == EdgeKind.COMPOSITIONAL and e.target == "ING-000001"
               for e in entity.outgoing)


def test_parse_file_sem_frontmatter(tmp_path):
    p = _write_md(tmp_path, "nota.md", "Sem frontmatter aqui.")
    entity = parse_file(p)
    assert entity.id == "nota"
    assert entity.tipo == "nota"


def test_parse_file_inexistente():
    with pytest.raises(ParseError):
        parse_file(Path("/nao/existe.md"))


def test_parse_file_ids_em_bloco_codigo_ignorados(tmp_path):
    p = _write_md(tmp_path, "REC-000001.md", """\
        ---
        id: REC-000001
        tipo: receita
        ---
        Texto normal.

        ```
        ING-000001 não deve virar aresta
        ```
    """)
    entity = parse_file(p)
    targets = {e.target for e in entity.outgoing}
    assert "ING-000001" not in targets


def test_parse_directory(tmp_path):
    _write_md(tmp_path, "REC-000001.md", "---\nid: REC-000001\ntipo: receita\n---\n")
    _write_md(tmp_path, "ING-000001.md", "---\nid: ING-000001\ntipo: ingrediente\n---\n")
    graph = parse_directory(tmp_path)
    assert "REC-000001" in graph.entities
    assert "ING-000001" in graph.entities


def test_parse_field_receita_base_id_gera_derivation(tmp_path):
    p = _write_md(tmp_path, "EXP-000001.md", """\
        ---
        id: EXP-000001
        tipo: experimento
        receita-base-id: REC-000001
        ---
    """)
    entity = parse_file(p)
    assert any(e.kind == EdgeKind.DERIVATION and e.target == "REC-000001"
               for e in entity.outgoing)
