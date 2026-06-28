"""Resolvedor — resolve referências entre entidades no KnowledgeGraph.

Contrato (FASE 2):
  Entrada : KnowledgeGraph com entidades já parseadas (incoming vazio).
  Saída   : lista de ResolverError (referências não resolvidas).
  Resolução:
    - Preenche Entity.incoming para cada aresta cuja target existe no grafo.
    - Referências a entidades fora do grafo geram ResolverError (não exception).
  Ambiguidades: nenhuma — IDs são canônicos e únicos.
  Cache: sem cache externo; grafo em memória é a fonte de verdade.
"""
from __future__ import annotations
from dataclasses import dataclass

from .ir import KnowledgeGraph


@dataclass
class ResolverError:
    source: str
    target: str
    kind:   str
    erro:   str = "referencia_quebrada"


def resolver(grafo: KnowledgeGraph) -> list[ResolverError]:
    """Preenche incoming de cada entidade; retorna lista de referências quebradas."""
    errors: list[ResolverError] = []
    for entity in grafo.entities.values():
        for edge in entity.outgoing:
            target = grafo.get_entity(edge.target)
            if target is not None:
                target.incoming.append(edge)
            else:
                errors.append(ResolverError(
                    source=edge.source,
                    target=edge.target,
                    kind=edge.kind.value,
                ))
    return errors
