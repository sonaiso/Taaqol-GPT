"""LGE-C2 sentence-slot runtime."""

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
from taaqqul_slot_geometry.lge.c1_surface_token_runtime import LgeC1SurfaceToken

LGE_C2_ALLOWED_OUTPUT: Final[str] = "LGE_C2_SENTENCE_SLOT"
LGE_C2_RANK_CEILING: Final[Rank] = Rank.CANDIDATE
LGE_C2_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "PropositionMeaning",
    "Ifadah",
    "Hukm",
    "Truth",
    "Certainty",
    "Reality",
)


class LgeC2SentenceFamily(StrEnum):
    NOMINAL = "NOMINAL_SENTENCE_SLOT"
    VERBAL = "VERBAL_SENTENCE_SLOT"
    SHIBH_JUMLAH = "SHIBH_JUMLAH_SLOT"


class LgeC2RuntimeStatus(StrEnum):
    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class LgeC2SentenceSlot:
    input_ref: str
    family: LgeC2SentenceFamily
    token_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = LGE_C2_RANK_CEILING
    output: Literal["LGE_C2_SENTENCE_SLOT"] = LGE_C2_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = LGE_C2_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        require_non_empty(
            self.input_ref,
            self.__class__.__name__,
            "input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.family, LgeC2SentenceFamily):
            raise TypeError(
                "LgeC2SentenceSlot.family must be LgeC2SentenceFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        require_non_empty(
            self.token_ref,
            self.__class__.__name__,
            "token_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        validate_residuals(self.residuals, self.__class__.__name__)
        validate_rank(self.rank, self.__class__.__name__, ceiling=LGE_C2_RANK_CEILING)
        if self.output != LGE_C2_ALLOWED_OUTPUT:
            raise TypeError(
                "LgeC2SentenceSlot.output exceeds LGE-C2 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        validate_forbidden_outputs(self.forbidden_outputs, self.__class__.__name__)


@dataclass(frozen=True, slots=True)
class LgeC2RuntimeVerdict:
    status: LgeC2RuntimeStatus
    slot: LgeC2SentenceSlot | None
    residuals: tuple[str, ...]
    trace_ref: str
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, LgeC2RuntimeStatus):
            raise TypeError(
                "LgeC2RuntimeVerdict.status must be LgeC2RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.slot is not None and not isinstance(self.slot, LgeC2SentenceSlot):
            raise TypeError(
                "LgeC2RuntimeVerdict.slot must be LgeC2SentenceSlot or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        validate_residuals(self.residuals, self.__class__.__name__)
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise TypeError(
                "LgeC2RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def prove_lge_c2_sentence_slot(
    *, upstream_token: object, family: LgeC2SentenceFamily, input_ref: str, trace_ref: str
) -> LgeC2RuntimeVerdict:
    if not isinstance(upstream_token, LgeC1SurfaceToken):
        return LgeC2RuntimeVerdict(
            status=LgeC2RuntimeStatus.REFUSED,
            slot=None,
            residuals=("LGE_C1_SURFACE_TOKEN_REQUIRED",),
            trace_ref=trace_ref,
            failure_code=FailureCode.GATE_REQUIRED,
        )
    slot = LgeC2SentenceSlot(
        input_ref=input_ref,
        family=family,
        token_ref=upstream_token.trace_ref,
        trace_ref=trace_ref,
        residuals=("LGE_C2_SURFACE_SLOT_FORMAL_ONLY",),
    )
    return LgeC2RuntimeVerdict(
        status=LgeC2RuntimeStatus.RUNTIME_GATES_CLOSED,
        slot=slot,
        residuals=slot.residuals,
        trace_ref=trace_ref,
        failure_code=None,
    )


__all__ = [
    "LGE_C2_ALLOWED_OUTPUT",
    "LGE_C2_FORBIDDEN_OUTPUTS",
    "LGE_C2_RANK_CEILING",
    "LgeC2RuntimeStatus",
    "LgeC2RuntimeVerdict",
    "LgeC2SentenceFamily",
    "LgeC2SentenceSlot",
    "prove_lge_c2_sentence_slot",
]
