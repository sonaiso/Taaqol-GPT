"""LGE-C1 surface token carrier runtime."""

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

LGE_C1_ALLOWED_OUTPUT: Final[str] = "LGE_C1_SURFACE_TOKEN"
LGE_C1_RANK_CEILING: Final[Rank] = Rank.CANDIDATE
LGE_C1_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "Meaning",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Truth",
    "Certainty",
    "Reality",
)


class LgeC1TokenFamily(StrEnum):
    LETTER_HARAKA = "LETTER_HARAKA_TOKEN"
    SYLLABLE = "SYLLABLE_TOKEN"
    PHONETIC_ECONOMY = "PHONETIC_ECONOMY_TOKEN"
    TOOLS = "TOOLS_TOKEN"
    BUILT_FORMS = "BUILT_FORMS_TOKEN"
    JAMID_WEIGHT = "JAMID_WEIGHT_TOKEN"
    DERIVED_WEIGHT = "DERIVED_WEIGHT_TOKEN"
    DERIVATIVES = "DERIVATIVES_TOKEN"
    WORD_CLASS_CLOSURE = "WORD_CLASS_CLOSURE_TOKEN"


@dataclass(frozen=True, slots=True)
class LgeC1SurfaceToken:
    input_ref: str
    family: LgeC1TokenFamily
    token: str
    trace_ref: str
    residuals: tuple[str, ...] = ()
    rank: Rank = LGE_C1_RANK_CEILING
    output: Literal["LGE_C1_SURFACE_TOKEN"] = LGE_C1_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = LGE_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        require_non_empty(
            self.input_ref,
            self.__class__.__name__,
            "input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.family, LgeC1TokenFamily):
            raise TypeError(
                "LgeC1SurfaceToken.family must be LgeC1TokenFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        require_non_empty(
            self.token,
            self.__class__.__name__,
            "token",
            FailureCode.BOUNDARY_MISSING,
        )
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        validate_residuals(self.residuals, self.__class__.__name__)
        validate_rank(self.rank, self.__class__.__name__, ceiling=LGE_C1_RANK_CEILING)
        if self.output != LGE_C1_ALLOWED_OUTPUT:
            raise TypeError(
                "LgeC1SurfaceToken.output exceeds LGE-C1 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        validate_forbidden_outputs(self.forbidden_outputs, self.__class__.__name__)


def emit_lge_c1_surface_token(
    *,
    input_ref: str,
    family: LgeC1TokenFamily,
    token: str,
    trace_ref: str,
    residuals: tuple[str, ...] = (),
) -> LgeC1SurfaceToken:
    return LgeC1SurfaceToken(
        input_ref=input_ref,
        family=family,
        token=token,
        trace_ref=trace_ref,
        residuals=residuals,
    )


__all__ = [
    "LGE_C1_ALLOWED_OUTPUT",
    "LGE_C1_FORBIDDEN_OUTPUTS",
    "LGE_C1_RANK_CEILING",
    "LgeC1SurfaceToken",
    "LgeC1TokenFamily",
    "emit_lge_c1_surface_token",
]
