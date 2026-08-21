"""Rank-space carriers for GUA transitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


class RankLevel(StrEnum):
    """General rank levels for typed transition contracts."""

    ZERO = "ZERO"
    TRACE = "TRACE"
    CANDIDATE = "CANDIDATE"
    HYPOTHESIS = "HYPOTHESIS"
    PROVEN = "PROVEN"
    CERTIFICATE = "CERTIFICATE"


@dataclass(frozen=True, slots=True)
class RankSpace:
    """Ordered bounded rank space for gate decisions."""

    levels: tuple[RankLevel, ...] = (
        RankLevel.ZERO,
        RankLevel.TRACE,
        RankLevel.CANDIDATE,
        RankLevel.HYPOTHESIS,
        RankLevel.PROVEN,
        RankLevel.CERTIFICATE,
    )

    def __post_init__(self) -> None:
        if not isinstance(self.levels, tuple) or not self.levels:
            raise GuaCoreSchemaError("RankSpace.levels must be a non-empty tuple")
        for level in self.levels:
            if not isinstance(level, RankLevel):
                raise GuaCoreSchemaError("RankSpace.levels entries must be RankLevel")
        if len(set(self.levels)) != len(self.levels):
            raise GuaCoreSchemaError("RankSpace.levels must not contain duplicates")

    def index_of(self, level: RankLevel) -> int:
        """Return the ordinal index of a rank level."""

        if not isinstance(level, RankLevel):
            raise GuaCoreSchemaError("RankSpace.index_of expects RankLevel")
        return self.levels.index(level)
