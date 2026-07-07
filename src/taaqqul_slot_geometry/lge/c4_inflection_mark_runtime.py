"""LGE-C4 inflection-mark surface runtime."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.lge._schema_helpers import (
    require_non_empty,
    require_trace_ref,
    validate_forbidden_outputs,
    validate_rank,
    validate_residuals,
)
from taaqqul_slot_geometry.lge.c3_relation_slot_runtime import LgeC3RelationSlot

LGE_C4_ALLOWED_OUTPUT: Final[str] = "LGE_C4_INFLECTION_MARK_SLOT"
LGE_C4_RANK_CEILING: Final[Rank] = Rank.CANDIDATE
LGE_C4_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "SemanticParsing",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Truth",
    "Certainty",
    "Reality",
)


class LgeC4MarkFamily(StrEnum):
    ORIGINAL = "ORIGINAL_INFLECTION_MARKS"
    SUBSIDIARY = "SUBSIDIARY_INFLECTION_MARKS"


class LgeC4RuntimeStatus(StrEnum):
    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class LgeC4InflectionSurface:
    input_ref: str
    family: LgeC4MarkFamily
    relation_slot_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = LGE_C4_RANK_CEILING
    output: Literal["LGE_C4_INFLECTION_MARK_SLOT"] = LGE_C4_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = LGE_C4_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        require_non_empty(
            self.input_ref,
            self.__class__.__name__,
            "input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.family, LgeC4MarkFamily):
            raise TypeError(
                "LgeC4InflectionSurface.family must be LgeC4MarkFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        require_non_empty(
            self.relation_slot_ref,
            self.__class__.__name__,
            "relation_slot_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        validate_residuals(self.residuals, self.__class__.__name__)
        validate_rank(self.rank, self.__class__.__name__, ceiling=LGE_C4_RANK_CEILING)
        if self.output != LGE_C4_ALLOWED_OUTPUT:
            raise TypeError(
                "LgeC4InflectionSurface.output exceeds LGE-C4 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        validate_forbidden_outputs(self.forbidden_outputs, self.__class__.__name__)


@dataclass(frozen=True, slots=True)
class LgeC4RuntimeVerdict:
    status: LgeC4RuntimeStatus
    surface: LgeC4InflectionSurface | None
    residuals: tuple[str, ...]
    trace_ref: str
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, LgeC4RuntimeStatus):
            raise TypeError(
                "LgeC4RuntimeVerdict.status must be LgeC4RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.surface is not None and not isinstance(self.surface, LgeC4InflectionSurface):
            raise TypeError(
                "LgeC4RuntimeVerdict.surface must be LgeC4InflectionSurface or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        validate_residuals(self.residuals, self.__class__.__name__)
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise TypeError(
                "LgeC4RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def prove_lge_c4_inflection_surface(
    *, upstream_slot: object, family: LgeC4MarkFamily, input_ref: str, trace_ref: str
) -> LgeC4RuntimeVerdict:
    if not isinstance(upstream_slot, LgeC3RelationSlot):
        return LgeC4RuntimeVerdict(
            status=LgeC4RuntimeStatus.REFUSED,
            surface=None,
            residuals=("LGE_C3_RELATION_SLOT_REQUIRED",),
            trace_ref=trace_ref,
            failure_code=FailureCode.GATE_REQUIRED,
        )
    surface = LgeC4InflectionSurface(
        input_ref=input_ref,
        family=family,
        relation_slot_ref=upstream_slot.trace_ref,
        trace_ref=trace_ref,
        residuals=("LGE_C4_INFLECTION_MARK_SURFACE_FORMAL_ONLY",),
    )
    return LgeC4RuntimeVerdict(
        status=LgeC4RuntimeStatus.RUNTIME_GATES_CLOSED,
        surface=surface,
        residuals=surface.residuals,
        trace_ref=trace_ref,
        failure_code=None,
    )


__all__ = [
    "LGE_C4_ALLOWED_OUTPUT",
    "LGE_C4_FORBIDDEN_OUTPUTS",
    "LGE_C4_RANK_CEILING",
    "LgeC4InflectionSurface",
    "LgeC4MarkFamily",
    "LgeC4RuntimeStatus",
    "LgeC4RuntimeVerdict",
    "prove_lge_c4_inflection_surface",
]
