"""Representação Intermediária (IR) — Grafo de Conhecimento.

Tipos canônicos do SOE-CCG. Imutáveis por contrato (ADR-0002).
Nenhuma lógica de negócio aqui — apenas estrutura de dados.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class EdgeKind(Enum):
    """Tipo semântico de uma aresta. Determina ciclos permitidos (ADR-0002)."""
    STRUCTURAL    = "STRUCTURAL"     # dependência obrigatória — ciclo: PROIBIDO
    COMPOSITIONAL = "COMPOSITIONAL"  # todo/parte             — ciclo: PROIBIDO
    HIERARCHICAL  = "HIERARCHICAL"   # pai/filho              — ciclo: PROIBIDO
    DERIVATION    = "DERIVATION"     # exp. derivado          — ciclo: PROIBIDO
    INFORMATIONAL = "INFORMATIONAL"  # citação/navegação      — ciclo: PERMITIDO
    OPTIONAL      = "OPTIONAL"       # sugestão               — ciclo: PERMITIDO


class EdgeOrigin(Enum):
    """Onde a referência foi encontrada no arquivo-fonte."""
    FRONTMATTER = "FRONTMATTER"  # bloco YAML
    BODY        = "BODY"         # corpo Markdown
    GENERATED   = "GENERATED"   # gerada pelo resolvedor


@dataclass
class Edge:
    source:   str
    target:   str
    kind:     EdgeKind
    origin:   EdgeOrigin
    location: str | None = None  # campo ou linha de origem (debug)


@dataclass
class Entity:
    id:       str
    tipo:     str
    metadata: dict
    body:     str
    outgoing: list[Edge] = field(default_factory=list)
    incoming: list[Edge] = field(default_factory=list)


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity] = field(default_factory=dict)

    def add_entity(self, e: Entity) -> None:
        self.entities[e.id] = e

    def get_entity(self, eid: str) -> Entity | None:
        return self.entities.get(eid)

    def get_edges_by_kind(self, kind: EdgeKind) -> list[Edge]:
        return [
            edge
            for entity in self.entities.values()
            for edge in entity.outgoing
            if edge.kind == kind
        ]
