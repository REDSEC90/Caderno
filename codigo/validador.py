"""Validador — verifica invariantes estruturais do KnowledgeGraph.

Contrato (FASE 2):
  Entrada : KnowledgeGraph já resolvido (incoming preenchido).
  Saída   : list[ValidationIssue].
  Invariantes verificados:
    1. Ausência de ciclos em arestas STRUCTURAL/COMPOSITIONAL/HIERARCHICAL/DERIVATION.
    2. Entidades de domínio (REC/EXE/EXP) não devem existir completamente isoladas.
  Erros   : ValidationIssue com severidade CRITICO | AVISO | INFO.
  Warnings: severidade AVISO — não bloqueiam importação.
"""
from __future__ import annotations
from dataclasses import dataclass

from .ir import EdgeKind, KnowledgeGraph

_STRICT_KINDS = frozenset({
    EdgeKind.STRUCTURAL,
    EdgeKind.COMPOSITIONAL,
    EdgeKind.HIERARCHICAL,
    EdgeKind.DERIVATION,
})
_LOOSE_KINDS = frozenset({EdgeKind.INFORMATIONAL, EdgeKind.OPTIONAL})
_DOMAIN_PREFIXES = frozenset({'REC', 'EXE', 'EXP'})


@dataclass
class ValidationIssue:
    entity_id:  str
    tipo_issue: str
    severidade: str   # CRITICO | AVISO | INFO
    mensagem:   str


def _detect_cycles(grafo: KnowledgeGraph, kinds: frozenset[EdgeKind]) -> list[list[str]]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {eid: WHITE for eid in grafo.entities}
    cycles: list[list[str]] = []
    path: list[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        path.append(node)
        entity = grafo.get_entity(node)
        if entity:
            for edge in entity.outgoing:
                if edge.kind not in kinds or edge.target not in color:
                    continue
                if color[edge.target] == GRAY:
                    idx = path.index(edge.target)
                    cycles.append(path[idx:] + [edge.target])
                elif color[edge.target] == WHITE:
                    dfs(edge.target)
        path.pop()
        color[node] = BLACK

    for eid in list(grafo.entities):
        if color[eid] == WHITE:
            dfs(eid)
    return cycles


def validar(grafo: KnowledgeGraph) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for cycle in _detect_cycles(grafo, _STRICT_KINDS):
        issues.append(ValidationIssue(
            entity_id=cycle[0],
            tipo_issue='ciclo',
            severidade='CRITICO',
            mensagem=f'Ciclo estrutural: {" -> ".join(cycle)}',
        ))

    for cycle in _detect_cycles(grafo, _LOOSE_KINDS):
        issues.append(ValidationIssue(
            entity_id=cycle[0],
            tipo_issue='ciclo',
            severidade='INFO',
            mensagem=f'Ciclo informacional (permitido): {" -> ".join(cycle)}',
        ))

    for entity in grafo.entities.values():
        prefix = entity.id.split('-')[0] if '-' in entity.id else entity.tipo.upper()
        if prefix in _DOMAIN_PREFIXES and not entity.outgoing and not entity.incoming:
            issues.append(ValidationIssue(
                entity_id=entity.id,
                tipo_issue='entidade_isolada',
                severidade='AVISO',
                mensagem=f'{entity.id} não possui arestas (entidade isolada)',
            ))

    return issues
