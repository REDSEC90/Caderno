from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class EdgeKind(Enum):
    STRUCTURAL = "STRUCTURAL"
    COMPOSITIONAL = "COMPOSITIONAL"
    HIERARCHICAL = "HIERARCHICAL"
    INFORMATIONAL = "INFORMATIONAL"
    DERIVATION = "DERIVATION"
    OPTIONAL = "OPTIONAL"


class EdgeOrigin(Enum):
    FRONTMATTER = "FRONTMATTER"
    BODY = "BODY"
    GENERATED = "GENERATED"


@dataclass
class Edge:
    source: str
    target: str
    kind: EdgeKind
    origin: EdgeOrigin
    location: str | None = None


@dataclass
class Entity:
    id: str
    tipo: str
    metadata: dict
    body: str
    outgoing: list[Edge] = field(default_factory=list)
    incoming: list[Edge] = field(default_factory=list)


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity] = field(default_factory=dict)

    def add_entity(self, e: Entity) -> None:
        self.entities[e.id] = e

    def get_entity(self, id: str) -> Entity | None:
        return self.entities.get(id)

    def get_edges_by_kind(self, kind: EdgeKind) -> list[Edge]:
        return [
            edge
            for entity in self.entities.values()
            for edge in entity.outgoing
            if edge.kind == kind
        ]
