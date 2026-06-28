from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ir_v1 import KnowledgeGraph


def resolver(grafo: KnowledgeGraph) -> list[dict]:
    errors = []
    for entity in grafo.entities.values():
        for edge in entity.outgoing:
            target = grafo.get_entity(edge.target)
            if target is not None:
                target.incoming.append(edge)
            else:
                errors.append({
                    'source': edge.source,
                    'target': edge.target,
                    'kind': edge.kind.value,
                    'erro': 'referencia_quebrada',
                })
    return errors
