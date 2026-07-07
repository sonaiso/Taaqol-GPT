"""LGE-C3 relation-engineering slot runtime."""

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
from taaqqul_slot_geometry.lge.c2_sentence_slot_runtime import LgeC2SentenceSlot

LGE_C3_ALLOWED_OUTPUT: Final[str] = "LGE_C3_RELATION_SLOT"
LGE_C3_RANK_CEILING: Final[Rank] = Rank.CANDIDATE
LGE_C3_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "SemanticEntailment",
    "Ifadah",
    "Hukm",
    "Truth",
    "Certainty",
    "Reality",
)


class LgeC3RelationFamily(StrEnum):
    ISNADI = "ISNADI_RELATION_SLOT"
    TADAMMUNI = "TADAMMUNI_RELATION_SLOT"
    TAQYIDI = "TAQYIDI_RELATION_SLOT"


class LgeC3RuntimeStatus(StrEnum):
    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class LgeC3RelationSlot:
    input_ref: str
    family: LgeC3RelationFamily
    sentence_slot_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = LGE_C3_RANK_CEILING
    output: Literal["LGE_C3_RELATION_SLOT"] = LGE_C3_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = LGE_C3_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        require_non_empty(
            self.input_ref,
            self.__class__.__name__,
            "input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.family, LgeC3RelationFamily):
            raise TypeError(
                "LgeC3RelationSlot.family must be LgeC3RelationFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        require_non_empty(
            self.sentence_slot_ref,
            self.__class__.__name__,
            "sentence_slot_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        validate_residuals(self.residuals, self.__class__.__name__)
        validate_rank(self.rank, self.__class__.__name__, ceiling=LGE_C3_RANK_CEILING)
        if self.output != LGE_C3_ALLOWED_OUTPUT:
            raise TypeError(
                "LgeC3RelationSlot.output exceeds LGE-C3 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        validate_forbidden_outputs(self.forbidden_outputs, self.__class__.__name__)


@dataclass(frozen=True, slots=True)
class LgeC3RuntimeVerdict:
    status: LgeC3RuntimeStatus
    slot: LgeC3RelationSlot | None
    residuals: tuple[str, ...]
    trace_ref: str
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, LgeC3RuntimeStatus):
            raise TypeError(
                "LgeC3RuntimeVerdict.status must be LgeC3RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.slot is not None and not isinstance(self.slot, LgeC3RelationSlot):
            raise TypeError(
                "LgeC3RuntimeVerdict.slot must be LgeC3RelationSlot or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        validate_residuals(self.residuals, self.__class__.__name__)
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise TypeError(
                "LgeC3RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def prove_lge_c3_relation_slot(
    *, upstream_slot: object, family: LgeC3RelationFamily, input_ref: str, trace_ref: str
) -> LgeC3RuntimeVerdict:
    if not isinstance(upstream_slot, LgeC2SentenceSlot):
        return LgeC3RuntimeVerdict(
            status=LgeC3RuntimeStatus.REFUSED,
            slot=None,
            residuals=("LGE_C2_SENTENCE_SLOT_REQUIRED",),
            trace_ref=trace_ref,
            failure_code=FailureCode.GATE_REQUIRED,
        )
    slot = LgeC3RelationSlot(
        input_ref=input_ref,
        family=family,
        sentence_slot_ref=upstream_slot.trace_ref,
        trace_ref=trace_ref,
        residuals=("LGE_C3_RELATION_ENGINEERING_FORMAL_ONLY",),
    )
    return LgeC3RuntimeVerdict(
        status=LgeC3RuntimeStatus.RUNTIME_GATES_CLOSED,
        slot=slot,
        residuals=slot.residuals,
        trace_ref=trace_ref,
        failure_code=None,
    )


__all__ = [
    "LGE_C3_ALLOWED_OUTPUT",
    "LGE_C3_FORBIDDEN_OUTPUTS",
    "LGE_C3_RANK_CEILING",
    "LgeC3RelationFamily",
    "LgeC3RelationSlot",
    "LgeC3RuntimeStatus",
    "LgeC3RuntimeVerdict",
    "prove_lge_c3_relation_slot",
]
