"""Parser — Markdown → KnowledgeGraph.

Contrato (FASE 2):
  Entrada : Path para um arquivo .md ou diretório com .md recursivo.
  Saída   : Entity (arquivo único) | KnowledgeGraph (diretório).
  AST     : frontmatter YAML + corpo Markdown; arestas tipadas por (ADR-0002).
  Erros   : ParseError para arquivos ilegíveis; aviso ao stderr para arquivos sem ID.
  Warnings: impressos em stderr com prefixo [WARN].
  Limitações:
    - Não segue links externos.
    - Ignora blocos de código no corpo (não extrai IDs de dentro de ``).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from .ir import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph

_ID_RE = re.compile(r'\b([A-Z]{2,3}-\d{6})\b')
_FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n?(.*)', re.DOTALL)

_COMPOSITIONAL_FIELDS = frozenset({
    'ingredientes', 'tecnicas', 'equipamentos',
    'ingredientes-usados', 'tecnicas-aplicadas', 'equipamentos-usados',
})
_DERIVATION_FIELDS = frozenset({'receita-base-id'})
_TABLE_ROW_RE = re.compile(r'^\s*\|')
_CODE_BLOCK_RE = re.compile(r'```.*?```', re.DOTALL)


class ParseError(Exception):
    pass


def _load_frontmatter(path: Path) -> tuple[dict, str]:
    """Retorna (metadata_dict, body_str). Tenta python-frontmatter, depois regex+yaml."""
    try:
        import frontmatter as pf
        doc = pf.load(str(path))
        return dict(doc.metadata), doc.content
    except ImportError:
        pass
    text = path.read_text(encoding='utf-8')
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    import yaml
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2)


def _is_id(v: object) -> bool:
    return isinstance(v, str) and bool(re.fullmatch(r'[A-Z]{2,3}-\d{6}', v.strip()))


def _edges_from_frontmatter(source_id: str, meta: dict) -> list[Edge]:
    edges: list[Edge] = []
    for key, val in meta.items():
        targets = []
        if isinstance(val, str):
            targets = [val]
        elif isinstance(val, list):
            targets = [str(t) for t in val]

        for t in targets:
            if not _is_id(t):
                continue
            if key in _DERIVATION_FIELDS:
                kind = EdgeKind.DERIVATION
            elif key in _COMPOSITIONAL_FIELDS:
                kind = EdgeKind.COMPOSITIONAL
            else:
                kind = EdgeKind.STRUCTURAL
            edges.append(Edge(source_id, t, kind, EdgeOrigin.FRONTMATTER, key))
    return edges


def _edges_from_body(source_id: str, body: str) -> list[Edge]:
    # Remove blocos de código para não extrair IDs de dentro deles
    clean = _CODE_BLOCK_RE.sub('', body)
    edges: list[Edge] = []
    for line in clean.splitlines():
        for t in _ID_RE.findall(line):
            kind = (EdgeKind.COMPOSITIONAL if _TABLE_ROW_RE.match(line)
                    else EdgeKind.INFORMATIONAL)
            edges.append(Edge(source_id, t, kind, EdgeOrigin.BODY, None))
    return edges


def parse_file(path: Path) -> Entity:
    """Parseia um único arquivo .md e retorna uma Entity."""
    try:
        meta, body = _load_frontmatter(path)
    except Exception as exc:
        raise ParseError(f"Falha ao ler {path}: {exc}") from exc

    entity_id = str(meta.get('id', path.stem))
    tipo = str(meta.get('tipo', entity_id.split('-')[0] if '-' in entity_id else 'UNKNOWN'))
    edges = _edges_from_frontmatter(entity_id, meta) + _edges_from_body(entity_id, body)
    return Entity(id=entity_id, tipo=tipo, metadata=meta, body=body, outgoing=edges)


def parse_directory(path: Path) -> KnowledgeGraph:
    """Parseia recursivamente todos os .md em path e retorna um KnowledgeGraph."""
    graph = KnowledgeGraph()
    for md in sorted(path.rglob('*.md')):
        try:
            graph.add_entity(parse_file(md))
        except ParseError as exc:
            print(f'[WARN] {exc}', file=sys.stderr)
        except Exception as exc:
            print(f'[WARN] {md}: {exc}', file=sys.stderr)
    return graph
