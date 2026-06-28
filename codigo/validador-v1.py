from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ir_v1 import EdgeKind, KnowledgeGraph

ROOT = Path('/home/redsec/Ambiente/SOE-CCG')

_CRITICAL_KINDS = {EdgeKind.STRUCTURAL, EdgeKind.COMPOSITIONAL, EdgeKind.HIERARCHICAL, EdgeKind.DERIVATION}
_INFO_KINDS = {EdgeKind.INFORMATIONAL, EdgeKind.OPTIONAL}
_RECIPE_TIPOS = {'REC', 'EXE', 'EXP'}


def _detect_cycles(grafo: KnowledgeGraph, kinds: set[EdgeKind]) -> list[list[str]]:
    """DFS cycle detection; returns list of cycles as node sequences."""
    cycles = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {eid: WHITE for eid in grafo.entities}
    path: list[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        path.append(node)
        entity = grafo.get_entity(node)
        if entity:
            for edge in entity.outgoing:
                if edge.kind not in kinds:
                    continue
                t = edge.target
                if t not in color:
                    continue
                if color[t] == GRAY:
                    idx = path.index(t)
                    cycles.append(path[idx:] + [t])
                elif color[t] == WHITE:
                    dfs(t)
        path.pop()
        color[node] = BLACK

    for eid in list(grafo.entities):
        if color[eid] == WHITE:
            dfs(eid)
    return cycles


def validar(grafo: KnowledgeGraph) -> list[dict]:
    issues = []

    for cycle in _detect_cycles(grafo, _CRITICAL_KINDS):
        issues.append({
            'entity_id': cycle[0],
            'tipo_issue': 'ciclo',
            'severidade': 'CRITICO',
            'mensagem': f'Ciclo detectado: {" -> ".join(cycle)}',
        })

    for cycle in _detect_cycles(grafo, _INFO_KINDS):
        issues.append({
            'entity_id': cycle[0],
            'tipo_issue': 'ciclo',
            'severidade': 'INFO',
            'mensagem': f'Ciclo informacional: {" -> ".join(cycle)}',
        })

    for entity in grafo.entities.values():
        tipo_prefix = entity.tipo.upper() if entity.tipo else entity.id.split('-')[0]
        if tipo_prefix in _RECIPE_TIPOS and not entity.outgoing and not entity.incoming:
            issues.append({
                'entity_id': entity.id,
                'tipo_issue': 'entidade_isolada',
                'severidade': 'AVISO',
                'mensagem': f'Entidade {entity.id} sem arestas outgoing nem incoming',
            })

    return issues


if __name__ == '__main__':
    from parser_v1 import parse_directory
    from resolvedor_v1 import resolver

    grafo = parse_directory(ROOT / 'dados')
    erros = resolver(grafo)
    if erros:
        print(f'Referencias quebradas: {len(erros)}')
    issues = validar(grafo)
    if not issues:
        print('Sem issues.')
    for issue in issues:
        print(f'[{issue["severidade"]}] {issue["entity_id"]} ({issue["tipo_issue"]}): {issue["mensagem"]}')
