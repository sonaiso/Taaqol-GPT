"""LGE-C5 style-slot runtime."""

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
from taaqqul_slot_geometry.lge.c4_inflection_mark_runtime import LgeC4InflectionSurface

LGE_C5_ALLOWED_OUTPUT: Final[str] = "LGE_C5_STYLE_SLOT"
LGE_C5_RANK_CEILING: Final[Rank] = Rank.CANDIDATE
LGE_C5_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "SemanticStyleMeaning",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Truth",
    "Certainty",
    "Reality",
)


class LgeC5StyleFamily(StrEnum):
    AKHBAR = "AKHBAR_STYLE_SLOT"
    INSHA = "INSHA_STYLE_SLOT"


class LgeC5RuntimeStatus(StrEnum):
    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class LgeC5StyleSurface:
    input_ref: str
    family: LgeC5StyleFamily
    inflection_surface_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = LGE_C5_RANK_CEILING
    output: Literal["LGE_C5_STYLE_SLOT"] = LGE_C5_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = LGE_C5_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        require_non_empty(
            self.input_ref,
            self.__class__.__name__,
            "input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.family, LgeC5StyleFamily):
            raise TypeError(
                "LgeC5StyleSurface.family must be LgeC5StyleFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        require_non_empty(
            self.inflection_surface_ref,
            self.__class__.__name__,
            "inflection_surface_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        validate_residuals(self.residuals, self.__class__.__name__)
        validate_rank(self.rank, self.__class__.__name__, ceiling=LGE_C5_RANK_CEILING)
        if self.output != LGE_C5_ALLOWED_OUTPUT:
            raise TypeError(
                "LgeC5StyleSurface.output exceeds LGE-C5 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        validate_forbidden_outputs(self.forbidden_outputs, self.__class__.__name__)


@dataclass(frozen=True, slots=True)
class LgeC5RuntimeVerdict:
    status: LgeC5RuntimeStatus
    surface: LgeC5StyleSurface | None
    residuals: tuple[str, ...]
    trace_ref: str
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, LgeC5RuntimeStatus):
            raise TypeError(
                "LgeC5RuntimeVerdict.status must be LgeC5RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.surface is not None and not isinstance(self.surface, LgeC5StyleSurface):
            raise TypeError(
                "LgeC5RuntimeVerdict.surface must be LgeC5StyleSurface or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        validate_residuals(self.residuals, self.__class__.__name__)
        require_trace_ref(self.trace_ref, self.__class__.__name__, "trace_ref")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise TypeError(
                "LgeC5RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def prove_lge_c5_style_surface(
    *, upstream_surface: object, family: LgeC5StyleFamily, input_ref: str, trace_ref: str
) -> LgeC5RuntimeVerdict:
    if not isinstance(upstream_surface, LgeC4InflectionSurface):
        return LgeC5RuntimeVerdict(
            status=LgeC5RuntimeStatus.REFUSED,
            surface=None,
            residuals=("LGE_C4_INFLECTION_SURFACE_REQUIRED",),
            trace_ref=trace_ref,
            failure_code=FailureCode.GATE_REQUIRED,
        )
    surface = LgeC5StyleSurface(
        input_ref=input_ref,
        family=family,
        inflection_surface_ref=upstream_surface.trace_ref,
        trace_ref=trace_ref,
        residuals=("LGE_C5_STYLE_SLOT_FORMAL_ONLY",),
    )
    return LgeC5RuntimeVerdict(
        status=LgeC5RuntimeStatus.RUNTIME_GATES_CLOSED,
        surface=surface,
        residuals=surface.residuals,
        trace_ref=trace_ref,
        failure_code=None,
    )


__all__ = [
    "LGE_C5_ALLOWED_OUTPUT",
    "LGE_C5_FORBIDDEN_OUTPUTS",
    "LGE_C5_RANK_CEILING",
    "LgeC5RuntimeStatus",
    "LgeC5RuntimeVerdict",
    "LgeC5StyleFamily",
    "LgeC5StyleSurface",
    "prove_lge_c5_style_surface",
]
