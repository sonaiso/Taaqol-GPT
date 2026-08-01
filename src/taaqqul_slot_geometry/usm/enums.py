"""USM local enums (USM-C1/C2 bounded schema surfaces)."""

from enum import StrEnum


class RelationDirection(StrEnum):
    """Typed directional surface for relation contracts."""

    DIRECTED = "DIRECTED"
    UNDIRECTED = "UNDIRECTED"
    BIDIRECTIONAL = "BIDIRECTIONAL"


__all__ = ["RelationDirection"]
