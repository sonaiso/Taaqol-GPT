"""LAFZI-B1 carrier-only surface for Lafzi Madlul correspondence.

This module implements only the LAFZI-B1 surface opened by docs/59:
carrier shapes plus local lafzi residual vocabulary. It does not execute
WordKind/SourceIdentity/FormState/InternalPath gates and does not produce
LafziMadlulClosed or any wadʿī/semantic output.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    require_non_empty as _shared_require_non_empty,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_forbidden_outputs as _shared_validate_forbidden_outputs,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_rank as _shared_validate_rank,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_residual_tuple as _shared_validate_residual_tuple,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

LAFZI_B1_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B2_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B2_ALLOWED_OUTPUT: str = "WORD_KIND_CANDIDATE_GATE_RESULT"

LAFZI_B1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "WORD_KIND_AMBIGUOUS",
    "SOURCE_IDENTITY_REQUIRED",
    "FORM_STATE_REQUIRED",
    "ISM_PATH_AMBIGUOUS",
    "FIIL_MASDAR_REQUIRED",
    "FIIL_TEMPORAL_IMAGE_REQUIRED",
    "HARF_OPERATOR_REQUIRED",
    "REFERENCE_SOURCE_REQUIRED",
    "PROPER_SELF_DESIGNATION_REQUIRED",
    "MUSHTAQ_REQUIRES_MASDAR",
    "MULTIPLE_LAFZI_CANDIDATES",
    "LAFZI_SCOPE_REQUIRED",
    "UNUSED_DAL_NO_LAFZI",
    "LOAN_LAFZI_PATH_REQUIRED",
    "FORBIDDEN_WADI_JUMP",
    "FORBIDDEN_MUTABAQA_JUMP",
    "FORBIDDEN_RELATION_JUMP",
    "FORBIDDEN_HUKM_JUMP",
)

LAFZI_B1_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "LAFZI_MADLUL_CLOSED",
    "WADI_MADLUL",
    "WADI_MADLUL_CLOSED",
    "MUTABAQAH",
    "TADAMMUN",
    "ILTIZAM",
    "RELATION",
    "COMPOSITION",
    "IFADAH",
    "MAFHUM",
    "HUKM",
    "TANZIL",
    "TRUTH",
    "CERTAINTY",
    "REALITY",
)


class LafziResidualKind(StrEnum):
    """Local LAFZI-B1 residual names from docs/59 §11."""

    WORD_KIND_AMBIGUOUS = "WORD_KIND_AMBIGUOUS"
    SOURCE_IDENTITY_REQUIRED = "SOURCE_IDENTITY_REQUIRED"
    FORM_STATE_REQUIRED = "FORM_STATE_REQUIRED"
    ISM_PATH_AMBIGUOUS = "ISM_PATH_AMBIGUOUS"
    FIIL_MASDAR_REQUIRED = "FIIL_MASDAR_REQUIRED"
    FIIL_TEMPORAL_IMAGE_REQUIRED = "FIIL_TEMPORAL_IMAGE_REQUIRED"
    HARF_OPERATOR_REQUIRED = "HARF_OPERATOR_REQUIRED"
    REFERENCE_SOURCE_REQUIRED = "REFERENCE_SOURCE_REQUIRED"
    PROPER_SELF_DESIGNATION_REQUIRED = "PROPER_SELF_DESIGNATION_REQUIRED"
    MUSHTAQ_REQUIRES_MASDAR = "MUSHTAQ_REQUIRES_MASDAR"
    MULTIPLE_LAFZI_CANDIDATES = "MULTIPLE_LAFZI_CANDIDATES"
    LAFZI_SCOPE_REQUIRED = "LAFZI_SCOPE_REQUIRED"
    UNUSED_DAL_NO_LAFZI = "UNUSED_DAL_NO_LAFZI"
    LOAN_LAFZI_PATH_REQUIRED = "LOAN_LAFZI_PATH_REQUIRED"
    FORBIDDEN_WADI_JUMP = "FORBIDDEN_WADI_JUMP"
    FORBIDDEN_MUTABAQA_JUMP = "FORBIDDEN_MUTABAQA_JUMP"
    FORBIDDEN_RELATION_JUMP = "FORBIDDEN_RELATION_JUMP"
    FORBIDDEN_HUKM_JUMP = "FORBIDDEN_HUKM_JUMP"


class MappingState(StrEnum):
    """Correspondence mapping states from docs/59 §3."""

    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"


class LafziMadlulState(StrEnum):
    """Local non-closure state vocabulary for a lafzi candidate."""

    CANDIDATE = "CANDIDATE"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class WordKindCandidate(StrEnum):
    """Word-kind candidate labels licensed by docs/59 §6 for LAFZI-B2."""

    ISM = "ISM"
    FIIL = "FIIL"
    HARF = "HARF"
    AMBIGUOUS = "AMBIGUOUS"
    BLOCKED = "BLOCKED"


class WordKindCandidateGateState(StrEnum):
    """LAFZI-B2 WordKindCandidateGate state; never LafziMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=LAFZI_B1_RANK_CEILING)


def _validate_residuals(residuals: tuple[LafziResidual, ...], owner: str) -> None:
    _shared_validate_residual_tuple(residuals, owner, expected_type=LafziResidual)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _append_residual_once(
    residuals: tuple[LafziResidual, ...],
    *,
    kind: LafziResidualKind,
    trace_ref: str,
    blocking: bool = False,
) -> tuple[LafziResidual, ...]:
    if any(residual.kind is kind for residual in residuals):
        return residuals
    return residuals + (LafziResidual(kind=kind, trace_ref=trace_ref, blocking=blocking),)


@dataclass(frozen=True, slots=True)
class LafziScope:
    """Bounded lafzi scope surface from docs/59 §10."""

    language_scope: str
    register_scope: str
    usage_scope: str
    vocalization_scope: str
    loan_or_native_scope: str
    trace_ref: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.language_scope,
            "LafziScope.language_scope",
            FailureCode.SCOPE_MISSING,
        )
        _require_non_empty(
            self.register_scope,
            "LafziScope.register_scope",
            FailureCode.SCOPE_MISSING,
        )
        _require_non_empty(
            self.usage_scope,
            "LafziScope.usage_scope",
            FailureCode.SCOPE_MISSING,
        )
        _require_non_empty(
            self.vocalization_scope,
            "LafziScope.vocalization_scope",
            FailureCode.SCOPE_MISSING,
        )
        _require_non_empty(
            self.loan_or_native_scope,
            "LafziScope.loan_or_native_scope",
            FailureCode.SCOPE_MISSING,
        )
        _require_non_empty(self.trace_ref, "LafziScope.trace_ref", FailureCode.TRACE_MISSING)


@dataclass(frozen=True, slots=True)
class LafziResidual:
    """Local LAFZI-B1 residual entry with explicit visibility payload."""

    kind: LafziResidualKind
    trace_ref: str
    severity: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    message: str = ""
    blocking: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, LafziResidualKind):
            raise WeightCarrierSchemaError(
                "LafziResidual.kind must be LafziResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_non_empty(self.trace_ref, "LafziResidual.trace_ref", FailureCode.TRACE_MISSING)
        if self.severity not in ("LOW", "MEDIUM", "HIGH"):
            raise WeightCarrierSchemaError(
                "LafziResidual.severity must be LOW|MEDIUM|HIGH "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.message, str):
            raise WeightCarrierSchemaError(
                "LafziResidual.message must be a string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                "LafziResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class LafziMadlulCandidate:
    """Carrier-only lafzi candidate surface (not a closed verdict)."""

    dal_alone_closed_ref: str
    word_kind_candidate_ref: str | None
    source_identity_candidate_ref: str | None
    form_state_candidate_ref: str | None
    internal_word_path_candidate_ref: str | None
    lafzi_scope: LafziScope
    residuals: tuple[LafziResidual, ...]
    state: LafziMadlulState
    trace_ref: str
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.dal_alone_closed_ref,
            "LafziMadlulCandidate.dal_alone_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.trace_ref,
            "LafziMadlulCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.lafzi_scope, LafziScope):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.lafzi_scope must be LafziScope "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        _validate_residuals(self.residuals, "LafziMadlulCandidate")
        if not isinstance(self.state, LafziMadlulState):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.state must be LafziMadlulState "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_rank(self.rank, "LafziMadlulCandidate")
        _validate_forbidden_outputs(self.forbidden_outputs, "LafziMadlulCandidate")

        optional_refs = (
            ("word_kind_candidate_ref", self.word_kind_candidate_ref),
            ("source_identity_candidate_ref", self.source_identity_candidate_ref),
            ("form_state_candidate_ref", self.form_state_candidate_ref),
            ("internal_word_path_candidate_ref", self.internal_word_path_candidate_ref),
        )
        for field_name, value in optional_refs:
            if value is not None:
                _require_non_empty(
                    value,
                    f"LafziMadlulCandidate.{field_name}",
                    FailureCode.TRACE_MISSING,
                )

        residual_kinds = {residual.kind for residual in self.residuals}
        if self.word_kind_candidate_ref is None and (
            LafziResidualKind.WORD_KIND_AMBIGUOUS not in residual_kinds
        ):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.word_kind_candidate_ref missing without visible residual "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.source_identity_candidate_ref is None and not (
            {
                LafziResidualKind.SOURCE_IDENTITY_REQUIRED,
                LafziResidualKind.REFERENCE_SOURCE_REQUIRED,
                LafziResidualKind.PROPER_SELF_DESIGNATION_REQUIRED,
            }
            & residual_kinds
        ):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.source_identity_candidate_ref missing without visible "
                f"residual ({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.form_state_candidate_ref is None and (
            LafziResidualKind.FORM_STATE_REQUIRED not in residual_kinds
        ):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.form_state_candidate_ref missing without visible residual "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.internal_word_path_candidate_ref is None and not (
            {
                LafziResidualKind.ISM_PATH_AMBIGUOUS,
                LafziResidualKind.FIIL_MASDAR_REQUIRED,
                LafziResidualKind.FIIL_TEMPORAL_IMAGE_REQUIRED,
                LafziResidualKind.HARF_OPERATOR_REQUIRED,
                LafziResidualKind.LOAN_LAFZI_PATH_REQUIRED,
                LafziResidualKind.MUSHTAQ_REQUIRES_MASDAR,
            }
            & residual_kinds
        ):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidate.internal_word_path_candidate_ref missing without visible "
                f"residual ({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class LafziMadlulCandidateSet:
    """Carrier-only correspondence set (never LafziMadlulClosed in LAFZI-B1)."""

    dal_alone_closed_ref: str
    mapping_state: MappingState
    candidates: tuple[LafziMadlulCandidate, ...]
    lafzi_scope: LafziScope
    residuals: tuple[LafziResidual, ...]
    trace_ref: str
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.dal_alone_closed_ref,
            "LafziMadlulCandidateSet.dal_alone_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.mapping_state, MappingState):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet.mapping_state must be MappingState "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.candidates, tuple):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet.candidates must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for candidate in self.candidates:
            if not isinstance(candidate, LafziMadlulCandidate):
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet.candidates entries must be LafziMadlulCandidate "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            if candidate.dal_alone_closed_ref != self.dal_alone_closed_ref:
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet candidate dal reference must match set reference "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )
        if not isinstance(self.lafzi_scope, LafziScope):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet.lafzi_scope must be LafziScope "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        _validate_residuals(self.residuals, "LafziMadlulCandidateSet")
        _require_non_empty(
            self.trace_ref,
            "LafziMadlulCandidateSet.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _validate_rank(self.rank, "LafziMadlulCandidateSet")
        _validate_forbidden_outputs(self.forbidden_outputs, "LafziMadlulCandidateSet")

        if not self.candidates:
            if self.mapping_state is not MappingState.BLOCKED:
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet empty candidates require BLOCKED mapping state "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if not any(residual.blocking for residual in self.residuals):
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet BLOCKED empty set requires visible blocking residual "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            return

        if self.mapping_state is MappingState.BLOCKED:
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet BLOCKED mapping must not carry candidates "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )

        if self.mapping_state is MappingState.ONE_TO_ONE and len(self.candidates) != 1:
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet ONE_TO_ONE mapping requires exactly one candidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )

        if len(self.candidates) > 1:
            if self.mapping_state not in (MappingState.ONE_TO_MANY, MappingState.DEFERRED):
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet multiple candidates require ONE_TO_MANY or DEFERRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            if not self.residuals:
                raise WeightCarrierSchemaError(
                    "LafziMadlulCandidateSet multiple candidates require visible residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )

        if self.mapping_state in (MappingState.ONE_TO_MANY, MappingState.DEFERRED) and (
            not self.residuals
        ):
            raise WeightCarrierSchemaError(
                "LafziMadlulCandidateSet ONE_TO_MANY/DEFERRED mappings require visible residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class WordKindCandidateGateResult:
    """Bounded LAFZI-B2 output for WordKindCandidateGate only."""

    state: WordKindCandidateGateState
    candidate_set_ref: str
    word_kind: WordKindCandidate
    residuals: tuple[LafziResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["WORD_KIND_CANDIDATE_GATE_RESULT"] = "WORD_KIND_CANDIDATE_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, WordKindCandidateGateState):
            raise WeightCarrierSchemaError(
                "WordKindCandidateGateResult.state must be WordKindCandidateGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.candidate_set_ref,
            "WordKindCandidateGateResult.candidate_set_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "WordKindCandidateGateResult.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "WordKindCandidateGateResult")
        _validate_rank(self.rank, "WordKindCandidateGateResult")
        _require_non_empty(
            self.trace_ref,
            "WordKindCandidateGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B2_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "WordKindCandidateGateResult.output must stay inside WordKindCandidateGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "WordKindCandidateGateResult")


def prove_word_kind_candidate_gate(
    candidate_set: LafziMadlulCandidateSet,
    *,
    proposed_word_kind: WordKindCandidate,
    trace_ref: str,
) -> WordKindCandidateGateResult:
    """Run LAFZI-B2 WordKindCandidateGate without opening LAFZI-B3 or closure."""

    if not isinstance(candidate_set, LafziMadlulCandidateSet):
        raise WeightCarrierSchemaError(
            "prove_word_kind_candidate_gate requires LafziMadlulCandidateSet "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(proposed_word_kind, WordKindCandidate):
        raise WeightCarrierSchemaError(
            "prove_word_kind_candidate_gate.proposed_word_kind must be WordKindCandidate "
            f"({FailureCode.BOUNDARY_MISSING.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_word_kind_candidate_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = candidate_set.residuals
    has_blocking = any(residual.blocking for residual in residuals)
    if len(candidate_set.candidates) > 1 and not residuals:
        raise WeightCarrierSchemaError(
            "WordKindCandidateGate requires visible residuals for multiple candidates "
            f"({FailureCode.HIDDEN_RESIDUAL.value})"
        )

    if (
        proposed_word_kind is WordKindCandidate.BLOCKED
        or candidate_set.mapping_state is MappingState.BLOCKED
        or has_blocking
        or not candidate_set.candidates
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.UNUSED_DAL_NO_LAFZI,
            trace_ref=trace_ref,
            blocking=True,
        )
        return WordKindCandidateGateResult(
            state=WordKindCandidateGateState.BLOCKED,
            candidate_set_ref=candidate_set.trace_ref,
            word_kind=WordKindCandidate.BLOCKED,
            residuals=residuals,
            rank=LAFZI_B2_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if (
        proposed_word_kind is WordKindCandidate.AMBIGUOUS
        or candidate_set.mapping_state in (MappingState.ONE_TO_MANY, MappingState.DEFERRED)
        or len(candidate_set.candidates) > 1
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.WORD_KIND_AMBIGUOUS,
            trace_ref=trace_ref,
        )
        return WordKindCandidateGateResult(
            state=WordKindCandidateGateState.DEFERRED,
            candidate_set_ref=candidate_set.trace_ref,
            word_kind=WordKindCandidate.AMBIGUOUS,
            residuals=residuals,
            rank=LAFZI_B2_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return WordKindCandidateGateResult(
        state=WordKindCandidateGateState.PROVEN,
        candidate_set_ref=candidate_set.trace_ref,
        word_kind=proposed_word_kind,
        residuals=residuals,
        rank=LAFZI_B2_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "LAFZI_B1_FORBIDDEN_OUTPUTS",
    "LAFZI_B1_RANK_CEILING",
    "LAFZI_B1_RESIDUAL_VOCABULARY",
    "LAFZI_B2_ALLOWED_OUTPUT",
    "LAFZI_B2_RANK_CEILING",
    "LafziMadlulCandidate",
    "LafziMadlulCandidateSet",
    "LafziMadlulState",
    "LafziResidual",
    "LafziResidualKind",
    "LafziScope",
    "MappingState",
    "WordKindCandidate",
    "WordKindCandidateGateResult",
    "WordKindCandidateGateState",
    "prove_word_kind_candidate_gate",
]
