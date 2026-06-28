from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ir_v1 import Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph

ROOT = Path('/home/redsec/Ambiente/SOE-CCG')

_ID_RE = re.compile(r'^[A-Z]{2,3}-\d{6}$')
_COMPOSITIONAL_FIELDS = {
    'ingredientes', 'tecnicas', 'equipamentos',
    'ingredientes-usados', 'tecnicas-aplicadas', 'equipamentos-usados',
}
_TABLE_ROW_RE = re.compile(r'^\s*\|')


def _is_id(v: str) -> bool:
    return bool(_ID_RE.match(v.strip()))


def _load_frontmatter(path: Path) -> tuple[dict, str]:
    try:
        import frontmatter as pf
        doc = pf.load(str(path))
        return dict(doc.metadata), doc.content
    except ImportError:
        pass
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    import yaml
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def _edges_from_frontmatter(source_id: str, meta: dict) -> list[Edge]:
    edges = []
    for key, val in meta.items():
        if key == 'receita-base-id':
            targets = [val] if isinstance(val, str) else (val if isinstance(val, list) else [])
            for t in targets:
                if _is_id(str(t)):
                    edges.append(Edge(source_id, str(t), EdgeKind.DERIVATION, EdgeOrigin.FRONTMATTER, key))
        elif key in _COMPOSITIONAL_FIELDS and isinstance(val, list):
            for t in val:
                if _is_id(str(t)):
                    edges.append(Edge(source_id, str(t), EdgeKind.COMPOSITIONAL, EdgeOrigin.FRONTMATTER, key))
        else:
            if isinstance(val, str) and _is_id(val):
                edges.append(Edge(source_id, val, EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER, key))
            elif isinstance(val, list):
                for t in val:
                    if isinstance(t, str) and _is_id(t):
                        edges.append(Edge(source_id, t, EdgeKind.STRUCTURAL, EdgeOrigin.FRONTMATTER, key))
    return edges


def _edges_from_body(source_id: str, body: str) -> list[Edge]:
    edges = []
    for line in body.splitlines():
        ids_in_line = _ID_RE.findall(line)
        if not ids_in_line:
            continue
        kind = EdgeKind.COMPOSITIONAL if _TABLE_ROW_RE.match(line) else EdgeKind.INFORMATIONAL
        for t in ids_in_line:
            edges.append(Edge(source_id, t, kind, EdgeOrigin.BODY, None))
    return edges


def parse_file(path: Path) -> Entity:
    meta, body = _load_frontmatter(path)
    entity_id = str(meta.get('id', path.stem))
    tipo = str(meta.get('tipo', entity_id.split('-')[0] if '-' in entity_id else 'UNKNOWN'))
    edges = _edges_from_frontmatter(entity_id, meta) + _edges_from_body(entity_id, body)
    return Entity(id=entity_id, tipo=tipo, metadata=meta, body=body, outgoing=edges)


def parse_directory(path: Path) -> KnowledgeGraph:
    graph = KnowledgeGraph()
    for md in path.rglob('*.md'):
        try:
            graph.add_entity(parse_file(md))
        except Exception as e:
            print(f'[WARN] {md}: {e}', file=sys.stderr)
    return graph


if __name__ == '__main__':
    from collections import Counter
    graph = parse_directory(ROOT / 'dados')
    counts = Counter(
        edge.kind
        for e in graph.entities.values()
        for edge in e.outgoing
    )
    print(f'Entidades: {len(graph.entities)}')
    for kind, n in sorted(counts.items(), key=lambda x: x[0].value):
        print(f'  {kind.value}: {n}')
