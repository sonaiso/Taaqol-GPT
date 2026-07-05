"""LAFZI-B1..B6 bounded surface for Lafzi Madlul correspondence.

This module implements the LAFZI-B1 carrier surface plus staged LAFZI-B2/B3/B4/B5
gates and LAFZI-B6 residual audit opened by docs/59. It does not produce
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
LAFZI_B3_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B3_ALLOWED_OUTPUT: str = "SOURCE_IDENTITY_GATE_RESULT"
LAFZI_B4_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B4_ALLOWED_OUTPUT: str = "FORM_STATE_GATE_RESULT"
LAFZI_B5_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B5_ALLOWED_OUTPUT: str = "INTERNAL_WORD_PATH_GATE_RESULT"
LAFZI_B6_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B6_ALLOWED_OUTPUT: str = "LAFZI_RESIDUAL_AUDIT_RESULT"

LAFZI_B1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "WORD_KIND_AMBIGUOUS",
    "SOURCE_IDENTITY_REQUIRED",
    "FORM_STATE_REQUIRED",
    "ISM_PATH_AMBIGUOUS",
    "SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH",
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
    SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH = "SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH"
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


class SourceIdentityCandidate(StrEnum):
    """Source-identity candidate labels licensed by docs/59 §7 for LAFZI-B3."""

    JAMID_ENTITY = "JAMID_ENTITY"
    MUSHTAQ_MASDAR_ROLE = "MUSHTAQ_MASDAR_ROLE"
    MASDAR_ABSTRACT_TRANSFORMATION = "MASDAR_ABSTRACT_TRANSFORMATION"
    PROPER_SELF_DESIGNATION = "PROPER_SELF_DESIGNATION"
    PRONOUN_BUILT_REFERENCE = "PRONOUN_BUILT_REFERENCE"
    DEMONSTRATIVE_PRESENT_REFERENCE = "DEMONSTRATIVE_PRESENT_REFERENCE"
    RELATIVE_LATER_LINK = "RELATIVE_LATER_LINK"
    FIIL_MASDAR_TEMPORAL_IMAGE = "FIIL_MASDAR_TEMPORAL_IMAGE"
    HARF_RELATION_OPERATOR_IDENTITY = "HARF_RELATION_OPERATOR_IDENTITY"
    DEFERRED_SOURCE = "DEFERRED_SOURCE"


class SourceIdentityGateState(StrEnum):
    """LAFZI-B3 SourceIdentityGate state; never LafziMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class FormStateCandidate(StrEnum):
    """Form-state candidate labels licensed by docs/59 §8 for LAFZI-B4."""

    MABNI = "MABNI"
    MURAB_POTENTIAL = "MURAB_POTENTIAL"
    VERB_BUILT_FORM = "VERB_BUILT_FORM"
    IMPERFECT_IRAB_POTENTIAL = "IMPERFECT_IRAB_POTENTIAL"
    DEFERRED = "DEFERRED"


class FormStateGateState(StrEnum):
    """LAFZI-B4 FormStateGate state; never LafziMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class InternalWordPathCandidate(StrEnum):
    """Internal-word-path labels licensed by docs/59 §9 for LAFZI-B5."""

    JAMID = "JAMID"
    MUSHTAQ = "MUSHTAQ"
    MASDAR = "MASDAR"
    PROPER = "PROPER"
    REFERENCE = "REFERENCE"
    BUILT_NAME = "BUILT_NAME"
    FIIL_MASDAR_PATH = "FIIL_MASDAR_PATH"
    FIIL_VALENCY_POTENTIAL_PATH = "FIIL_VALENCY_POTENTIAL_PATH"
    FIIL_VOICE_POTENTIAL_PATH = "FIIL_VOICE_POTENTIAL_PATH"
    FIIL_TEMPORAL_OR_REQUEST_IMAGE_PATH = "FIIL_TEMPORAL_OR_REQUEST_IMAGE_PATH"
    BUILT_OPERATOR = "BUILT_OPERATOR"
    RELATION_NEED = "RELATION_NEED"
    OPERAND_NEED = "OPERAND_NEED"
    NO_INDEPENDENCE = "NO_INDEPENDENCE"
    DEFERRED = "DEFERRED"


class InternalWordPathGateState(StrEnum):
    """LAFZI-B5 InternalWordPathGate state; never LafziMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class LafziResidualAuditState(StrEnum):
    """LAFZI-B6 residual-audit state; never LafziMadlulClosed."""

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
                LafziResidualKind.SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH,
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


_ISM_SOURCE_IDENTITIES: tuple[SourceIdentityCandidate, ...] = (
    SourceIdentityCandidate.JAMID_ENTITY,
    SourceIdentityCandidate.MUSHTAQ_MASDAR_ROLE,
    SourceIdentityCandidate.MASDAR_ABSTRACT_TRANSFORMATION,
    SourceIdentityCandidate.PROPER_SELF_DESIGNATION,
    SourceIdentityCandidate.PRONOUN_BUILT_REFERENCE,
    SourceIdentityCandidate.DEMONSTRATIVE_PRESENT_REFERENCE,
    SourceIdentityCandidate.RELATIVE_LATER_LINK,
)


_ISM_FORM_STATES: tuple[FormStateCandidate, ...] = (
    FormStateCandidate.MABNI,
    FormStateCandidate.MURAB_POTENTIAL,
)
_FIIL_FORM_STATES: tuple[FormStateCandidate, ...] = (
    FormStateCandidate.VERB_BUILT_FORM,
    FormStateCandidate.IMPERFECT_IRAB_POTENTIAL,
)
_REFERENCE_IDENTITIES: tuple[SourceIdentityCandidate, ...] = (
    SourceIdentityCandidate.PRONOUN_BUILT_REFERENCE,
    SourceIdentityCandidate.DEMONSTRATIVE_PRESENT_REFERENCE,
    SourceIdentityCandidate.RELATIVE_LATER_LINK,
)
_ISM_INTERNAL_PATHS: tuple[InternalWordPathCandidate, ...] = (
    InternalWordPathCandidate.JAMID,
    InternalWordPathCandidate.MUSHTAQ,
    InternalWordPathCandidate.MASDAR,
    InternalWordPathCandidate.PROPER,
    InternalWordPathCandidate.REFERENCE,
    InternalWordPathCandidate.BUILT_NAME,
)
_FIIL_INTERNAL_PATHS: tuple[InternalWordPathCandidate, ...] = (
    InternalWordPathCandidate.FIIL_MASDAR_PATH,
    InternalWordPathCandidate.FIIL_VALENCY_POTENTIAL_PATH,
    InternalWordPathCandidate.FIIL_VOICE_POTENTIAL_PATH,
    InternalWordPathCandidate.FIIL_TEMPORAL_OR_REQUEST_IMAGE_PATH,
)
_HARF_INTERNAL_PATHS: tuple[InternalWordPathCandidate, ...] = (
    InternalWordPathCandidate.BUILT_OPERATOR,
    InternalWordPathCandidate.RELATION_NEED,
    InternalWordPathCandidate.OPERAND_NEED,
    InternalWordPathCandidate.NO_INDEPENDENCE,
)
_SOURCE_IDENTITY_INTERNAL_PATH_COMPATIBILITY: dict[
    SourceIdentityCandidate, tuple[InternalWordPathCandidate, ...]
] = {
    SourceIdentityCandidate.JAMID_ENTITY: (
        InternalWordPathCandidate.JAMID,
        InternalWordPathCandidate.BUILT_NAME,
    ),
    SourceIdentityCandidate.MUSHTAQ_MASDAR_ROLE: (
        InternalWordPathCandidate.MUSHTAQ,
    ),
    SourceIdentityCandidate.MASDAR_ABSTRACT_TRANSFORMATION: (
        InternalWordPathCandidate.MASDAR,
    ),
    SourceIdentityCandidate.PROPER_SELF_DESIGNATION: (
        InternalWordPathCandidate.PROPER,
    ),
    SourceIdentityCandidate.PRONOUN_BUILT_REFERENCE: (
        InternalWordPathCandidate.REFERENCE,
    ),
    SourceIdentityCandidate.DEMONSTRATIVE_PRESENT_REFERENCE: (
        InternalWordPathCandidate.REFERENCE,
    ),
    SourceIdentityCandidate.RELATIVE_LATER_LINK: (
        InternalWordPathCandidate.REFERENCE,
    ),
    SourceIdentityCandidate.FIIL_MASDAR_TEMPORAL_IMAGE: _FIIL_INTERNAL_PATHS,
    SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY: _HARF_INTERNAL_PATHS,
}
_ISM_SOURCE_PATH_MISMATCH_RESIDUALS: dict[
    tuple[SourceIdentityCandidate, InternalWordPathCandidate],
    LafziResidualKind,
] = {
    (source_identity, internal_path): LafziResidualKind.SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH
    for source_identity in _ISM_SOURCE_IDENTITIES
    for internal_path in _ISM_INTERNAL_PATHS
    if internal_path
    not in _SOURCE_IDENTITY_INTERNAL_PATH_COMPATIBILITY.get(source_identity, ())
}


def _classify_ism_path_residual(
    *,
    source_identity: SourceIdentityCandidate,
    proposed_internal_path: InternalWordPathCandidate,
) -> LafziResidualKind:
    return _ISM_SOURCE_PATH_MISMATCH_RESIDUALS.get(
        (source_identity, proposed_internal_path),
        LafziResidualKind.ISM_PATH_AMBIGUOUS,
    )


@dataclass(frozen=True, slots=True)
class SourceIdentityGateResult:
    """Bounded LAFZI-B3 output for SourceIdentityGate only."""

    state: SourceIdentityGateState
    word_kind_gate_ref: str
    word_kind: WordKindCandidate
    source_identity: SourceIdentityCandidate
    residuals: tuple[LafziResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["SOURCE_IDENTITY_GATE_RESULT"] = "SOURCE_IDENTITY_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, SourceIdentityGateState):
            raise WeightCarrierSchemaError(
                "SourceIdentityGateResult.state must be SourceIdentityGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.word_kind_gate_ref,
            "SourceIdentityGateResult.word_kind_gate_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "SourceIdentityGateResult.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.source_identity, SourceIdentityCandidate):
            raise WeightCarrierSchemaError(
                "SourceIdentityGateResult.source_identity must be SourceIdentityCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "SourceIdentityGateResult")
        _validate_rank(self.rank, "SourceIdentityGateResult")
        _require_non_empty(
            self.trace_ref,
            "SourceIdentityGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B3_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "SourceIdentityGateResult.output must stay inside SourceIdentityGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "SourceIdentityGateResult")


def prove_source_identity_candidate_gate(
    word_kind_result: WordKindCandidateGateResult,
    *,
    proposed_source_identity: SourceIdentityCandidate,
    trace_ref: str,
) -> SourceIdentityGateResult:
    """Run LAFZI-B3 SourceIdentityGate without opening LAFZI-B4 or closure."""

    if not isinstance(word_kind_result, WordKindCandidateGateResult):
        raise WeightCarrierSchemaError(
            "prove_source_identity_candidate_gate requires WordKindCandidateGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(proposed_source_identity, SourceIdentityCandidate):
        raise WeightCarrierSchemaError(
            "prove_source_identity_candidate_gate.proposed_source_identity must be "
            f"SourceIdentityCandidate ({FailureCode.BOUNDARY_MISSING.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_source_identity_candidate_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = word_kind_result.residuals
    has_blocking = any(residual.blocking for residual in residuals)
    if (
        word_kind_result.state is WordKindCandidateGateState.BLOCKED
        or word_kind_result.word_kind is WordKindCandidate.BLOCKED
        or has_blocking
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.UNUSED_DAL_NO_LAFZI,
            trace_ref=trace_ref,
            blocking=True,
        )
        return SourceIdentityGateResult(
            state=SourceIdentityGateState.BLOCKED,
            word_kind_gate_ref=word_kind_result.trace_ref,
            word_kind=word_kind_result.word_kind,
            source_identity=SourceIdentityCandidate.DEFERRED_SOURCE,
            residuals=residuals,
            rank=LAFZI_B3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if (
        word_kind_result.state is WordKindCandidateGateState.DEFERRED
        or word_kind_result.word_kind is WordKindCandidate.AMBIGUOUS
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.SOURCE_IDENTITY_REQUIRED,
            trace_ref=trace_ref,
        )
        return SourceIdentityGateResult(
            state=SourceIdentityGateState.DEFERRED,
            word_kind_gate_ref=word_kind_result.trace_ref,
            word_kind=word_kind_result.word_kind,
            source_identity=SourceIdentityCandidate.DEFERRED_SOURCE,
            residuals=residuals,
            rank=LAFZI_B3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if word_kind_result.word_kind is WordKindCandidate.ISM:
        if proposed_source_identity in _ISM_SOURCE_IDENTITIES:
            return SourceIdentityGateResult(
                state=SourceIdentityGateState.PROVEN,
                word_kind_gate_ref=word_kind_result.trace_ref,
                word_kind=word_kind_result.word_kind,
                source_identity=proposed_source_identity,
                residuals=residuals,
                rank=LAFZI_B3_RANK_CEILING,
                trace_ref=trace_ref,
            )

        if proposed_source_identity is SourceIdentityCandidate.DEFERRED_SOURCE:
            residual_kind = LafziResidualKind.SOURCE_IDENTITY_REQUIRED
        elif proposed_source_identity in (
            SourceIdentityCandidate.PRONOUN_BUILT_REFERENCE,
            SourceIdentityCandidate.DEMONSTRATIVE_PRESENT_REFERENCE,
            SourceIdentityCandidate.RELATIVE_LATER_LINK,
        ):
            residual_kind = LafziResidualKind.REFERENCE_SOURCE_REQUIRED
        elif proposed_source_identity is SourceIdentityCandidate.PROPER_SELF_DESIGNATION:
            residual_kind = LafziResidualKind.PROPER_SELF_DESIGNATION_REQUIRED
        else:
            residual_kind = LafziResidualKind.SOURCE_IDENTITY_REQUIRED

    elif word_kind_result.word_kind is WordKindCandidate.FIIL:
        if proposed_source_identity is SourceIdentityCandidate.FIIL_MASDAR_TEMPORAL_IMAGE:
            return SourceIdentityGateResult(
                state=SourceIdentityGateState.PROVEN,
                word_kind_gate_ref=word_kind_result.trace_ref,
                word_kind=word_kind_result.word_kind,
                source_identity=proposed_source_identity,
                residuals=residuals,
                rank=LAFZI_B3_RANK_CEILING,
                trace_ref=trace_ref,
            )
        residual_kind = LafziResidualKind.FIIL_MASDAR_REQUIRED

    elif word_kind_result.word_kind is WordKindCandidate.HARF:
        if proposed_source_identity is SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY:
            return SourceIdentityGateResult(
                state=SourceIdentityGateState.PROVEN,
                word_kind_gate_ref=word_kind_result.trace_ref,
                word_kind=word_kind_result.word_kind,
                source_identity=proposed_source_identity,
                residuals=residuals,
                rank=LAFZI_B3_RANK_CEILING,
                trace_ref=trace_ref,
            )
        residual_kind = LafziResidualKind.HARF_OPERATOR_REQUIRED
    else:
        residual_kind = LafziResidualKind.SOURCE_IDENTITY_REQUIRED

    residuals = _append_residual_once(residuals, kind=residual_kind, trace_ref=trace_ref)
    return SourceIdentityGateResult(
        state=SourceIdentityGateState.DEFERRED,
        word_kind_gate_ref=word_kind_result.trace_ref,
        word_kind=word_kind_result.word_kind,
        source_identity=SourceIdentityCandidate.DEFERRED_SOURCE,
        residuals=residuals,
        rank=LAFZI_B3_RANK_CEILING,
        trace_ref=trace_ref,
    )


@dataclass(frozen=True, slots=True)
class FormStateGateResult:
    """Bounded LAFZI-B4 output for FormStateGate only."""

    state: FormStateGateState
    source_identity_gate_ref: str
    word_kind: WordKindCandidate
    source_identity: SourceIdentityCandidate
    form_state: FormStateCandidate
    residuals: tuple[LafziResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["FORM_STATE_GATE_RESULT"] = "FORM_STATE_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, FormStateGateState):
            raise WeightCarrierSchemaError(
                "FormStateGateResult.state must be FormStateGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.source_identity_gate_ref,
            "FormStateGateResult.source_identity_gate_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "FormStateGateResult.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.source_identity, SourceIdentityCandidate):
            raise WeightCarrierSchemaError(
                "FormStateGateResult.source_identity must be SourceIdentityCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.form_state, FormStateCandidate):
            raise WeightCarrierSchemaError(
                "FormStateGateResult.form_state must be FormStateCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "FormStateGateResult")
        _validate_rank(self.rank, "FormStateGateResult")
        _require_non_empty(
            self.trace_ref,
            "FormStateGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B4_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "FormStateGateResult.output must stay inside FormStateGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "FormStateGateResult")


def prove_form_state_candidate_gate(
    source_identity_result: SourceIdentityGateResult,
    *,
    proposed_form_state: FormStateCandidate,
    trace_ref: str,
) -> FormStateGateResult:
    """Run LAFZI-B4 FormStateGate without opening LAFZI-B5 or closure."""

    if not isinstance(source_identity_result, SourceIdentityGateResult):
        raise WeightCarrierSchemaError(
            "prove_form_state_candidate_gate requires SourceIdentityGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(proposed_form_state, FormStateCandidate):
        raise WeightCarrierSchemaError(
            "prove_form_state_candidate_gate.proposed_form_state must be "
            f"FormStateCandidate ({FailureCode.BOUNDARY_MISSING.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_form_state_candidate_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = source_identity_result.residuals
    has_blocking = any(residual.blocking for residual in residuals)
    if (
        source_identity_result.state is SourceIdentityGateState.BLOCKED
        or source_identity_result.word_kind is WordKindCandidate.BLOCKED
        or has_blocking
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.UNUSED_DAL_NO_LAFZI,
            trace_ref=trace_ref,
            blocking=True,
        )
        return FormStateGateResult(
            state=FormStateGateState.BLOCKED,
            source_identity_gate_ref=source_identity_result.trace_ref,
            word_kind=source_identity_result.word_kind,
            source_identity=source_identity_result.source_identity,
            form_state=FormStateCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if (
        source_identity_result.state is SourceIdentityGateState.DEFERRED
        or source_identity_result.source_identity is SourceIdentityCandidate.DEFERRED_SOURCE
        or source_identity_result.word_kind is WordKindCandidate.AMBIGUOUS
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.FORM_STATE_REQUIRED,
            trace_ref=trace_ref,
        )
        return FormStateGateResult(
            state=FormStateGateState.DEFERRED,
            source_identity_gate_ref=source_identity_result.trace_ref,
            word_kind=source_identity_result.word_kind,
            source_identity=source_identity_result.source_identity,
            form_state=FormStateCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if source_identity_result.word_kind is WordKindCandidate.ISM:
        if proposed_form_state in _ISM_FORM_STATES:
            return FormStateGateResult(
                state=FormStateGateState.PROVEN,
                source_identity_gate_ref=source_identity_result.trace_ref,
                word_kind=source_identity_result.word_kind,
                source_identity=source_identity_result.source_identity,
                form_state=proposed_form_state,
                residuals=residuals,
                rank=LAFZI_B4_RANK_CEILING,
                trace_ref=trace_ref,
            )
    elif source_identity_result.word_kind is WordKindCandidate.FIIL:
        if proposed_form_state in _FIIL_FORM_STATES:
            return FormStateGateResult(
                state=FormStateGateState.PROVEN,
                source_identity_gate_ref=source_identity_result.trace_ref,
                word_kind=source_identity_result.word_kind,
                source_identity=source_identity_result.source_identity,
                form_state=proposed_form_state,
                residuals=residuals,
                rank=LAFZI_B4_RANK_CEILING,
                trace_ref=trace_ref,
            )
    elif (
        source_identity_result.word_kind is WordKindCandidate.HARF
        and proposed_form_state is FormStateCandidate.MABNI
    ):
        return FormStateGateResult(
            state=FormStateGateState.PROVEN,
            source_identity_gate_ref=source_identity_result.trace_ref,
            word_kind=source_identity_result.word_kind,
            source_identity=source_identity_result.source_identity,
            form_state=proposed_form_state,
            residuals=residuals,
            rank=LAFZI_B4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    residuals = _append_residual_once(
        residuals,
        kind=LafziResidualKind.FORM_STATE_REQUIRED,
        trace_ref=trace_ref,
    )
    return FormStateGateResult(
        state=FormStateGateState.DEFERRED,
        source_identity_gate_ref=source_identity_result.trace_ref,
        word_kind=source_identity_result.word_kind,
        source_identity=source_identity_result.source_identity,
        form_state=FormStateCandidate.DEFERRED,
        residuals=residuals,
        rank=LAFZI_B4_RANK_CEILING,
        trace_ref=trace_ref,
    )


@dataclass(frozen=True, slots=True)
class InternalWordPathGateResult:
    """Bounded LAFZI-B5 output for InternalWordPathGate only."""

    state: InternalWordPathGateState
    form_state_gate_ref: str
    word_kind: WordKindCandidate
    source_identity: SourceIdentityCandidate
    form_state: FormStateCandidate
    internal_word_path: InternalWordPathCandidate
    residuals: tuple[LafziResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["INTERNAL_WORD_PATH_GATE_RESULT"] = "INTERNAL_WORD_PATH_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, InternalWordPathGateState):
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.state must be InternalWordPathGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.form_state_gate_ref,
            "InternalWordPathGateResult.form_state_gate_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.source_identity, SourceIdentityCandidate):
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.source_identity must be SourceIdentityCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.form_state, FormStateCandidate):
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.form_state must be FormStateCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.internal_word_path, InternalWordPathCandidate):
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.internal_word_path must be "
                f"InternalWordPathCandidate ({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "InternalWordPathGateResult")
        _validate_rank(self.rank, "InternalWordPathGateResult")
        _require_non_empty(
            self.trace_ref,
            "InternalWordPathGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B5_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "InternalWordPathGateResult.output must stay inside InternalWordPathGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "InternalWordPathGateResult")


@dataclass(frozen=True, slots=True)
class LafziResidualAuditResult:
    """Bounded LAFZI-B6 output for residual audit only."""

    state: LafziResidualAuditState
    internal_word_path_gate_ref: str
    word_kind: WordKindCandidate
    source_identity: SourceIdentityCandidate
    form_state: FormStateCandidate
    internal_word_path: InternalWordPathCandidate
    residuals: tuple[LafziResidual, ...]
    blocking_residuals: tuple[LafziResidual, ...]
    non_blocking_residuals: tuple[LafziResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["LAFZI_RESIDUAL_AUDIT_RESULT"] = "LAFZI_RESIDUAL_AUDIT_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, LafziResidualAuditState):
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.state must be LafziResidualAuditState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.internal_word_path_gate_ref,
            "LafziResidualAuditResult.internal_word_path_gate_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.source_identity, SourceIdentityCandidate):
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.source_identity must be SourceIdentityCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.form_state, FormStateCandidate):
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.form_state must be FormStateCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.internal_word_path, InternalWordPathCandidate):
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.internal_word_path must be InternalWordPathCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "LafziResidualAuditResult")
        _validate_residuals(self.blocking_residuals, "LafziResidualAuditResult")
        _validate_residuals(self.non_blocking_residuals, "LafziResidualAuditResult")
        _validate_rank(self.rank, "LafziResidualAuditResult")
        _require_non_empty(
            self.trace_ref,
            "LafziResidualAuditResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B6_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.output must stay inside LafziResidualAudit "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "LafziResidualAuditResult")

        for residual in self.blocking_residuals:
            if not residual.blocking:
                raise WeightCarrierSchemaError(
                    "LafziResidualAuditResult.blocking_residuals must be blocking "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        for residual in self.non_blocking_residuals:
            if residual.blocking:
                raise WeightCarrierSchemaError(
                    "LafziResidualAuditResult.non_blocking_residuals must be non-blocking "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )

        expected_residuals = self.blocking_residuals + self.non_blocking_residuals
        if expected_residuals != self.residuals:
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult residual partition must preserve full visible residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )

        if self.state is LafziResidualAuditState.PROVEN and self.residuals:
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.PROVEN cannot carry unresolved residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if self.state is LafziResidualAuditState.DEFERRED and not self.non_blocking_residuals:
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.DEFERRED requires visible non-blocking residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if self.state is LafziResidualAuditState.BLOCKED and not self.blocking_residuals:
            raise WeightCarrierSchemaError(
                "LafziResidualAuditResult.BLOCKED requires visible blocking residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


def prove_internal_word_path_candidate_gate(
    form_state_result: FormStateGateResult,
    *,
    proposed_internal_path: InternalWordPathCandidate,
    trace_ref: str,
) -> InternalWordPathGateResult:
    """Run LAFZI-B5 InternalWordPathGate without opening LAFZI-B6/B7 or closure."""

    if not isinstance(form_state_result, FormStateGateResult):
        raise WeightCarrierSchemaError(
            "prove_internal_word_path_candidate_gate requires FormStateGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(proposed_internal_path, InternalWordPathCandidate):
        raise WeightCarrierSchemaError(
            "prove_internal_word_path_candidate_gate.proposed_internal_path must be "
            f"InternalWordPathCandidate ({FailureCode.BOUNDARY_MISSING.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_internal_word_path_candidate_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = form_state_result.residuals
    has_blocking = any(residual.blocking for residual in residuals)
    if (
        form_state_result.state is FormStateGateState.BLOCKED
        or form_state_result.word_kind is WordKindCandidate.BLOCKED
        or has_blocking
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.UNUSED_DAL_NO_LAFZI,
            trace_ref=trace_ref,
            blocking=True,
        )
        return InternalWordPathGateResult(
            state=InternalWordPathGateState.BLOCKED,
            form_state_gate_ref=form_state_result.trace_ref,
            word_kind=form_state_result.word_kind,
            source_identity=form_state_result.source_identity,
            form_state=form_state_result.form_state,
            internal_word_path=InternalWordPathCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if (
        form_state_result.state is FormStateGateState.DEFERRED
        or form_state_result.source_identity is SourceIdentityCandidate.DEFERRED_SOURCE
        or form_state_result.form_state is FormStateCandidate.DEFERRED
        or form_state_result.word_kind is WordKindCandidate.AMBIGUOUS
    ):
        if form_state_result.word_kind is WordKindCandidate.HARF:
            residual_kind = LafziResidualKind.HARF_OPERATOR_REQUIRED
        elif form_state_result.word_kind is WordKindCandidate.FIIL:
            residual_kind = LafziResidualKind.FIIL_MASDAR_REQUIRED
        else:
            residual_kind = LafziResidualKind.ISM_PATH_AMBIGUOUS
        residuals = _append_residual_once(residuals, kind=residual_kind, trace_ref=trace_ref)
        return InternalWordPathGateResult(
            state=InternalWordPathGateState.DEFERRED,
            form_state_gate_ref=form_state_result.trace_ref,
            word_kind=form_state_result.word_kind,
            source_identity=form_state_result.source_identity,
            form_state=form_state_result.form_state,
            internal_word_path=InternalWordPathCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if form_state_result.word_kind is WordKindCandidate.ISM:
        if proposed_internal_path is InternalWordPathCandidate.MUSHTAQ:
            if (
                form_state_result.source_identity
                is SourceIdentityCandidate.MUSHTAQ_MASDAR_ROLE
            ):
                return InternalWordPathGateResult(
                    state=InternalWordPathGateState.PROVEN,
                    form_state_gate_ref=form_state_result.trace_ref,
                    word_kind=form_state_result.word_kind,
                    source_identity=form_state_result.source_identity,
                    form_state=form_state_result.form_state,
                    internal_word_path=proposed_internal_path,
                    residuals=residuals,
                    rank=LAFZI_B5_RANK_CEILING,
                    trace_ref=trace_ref,
                )
            residuals = _append_residual_once(
                residuals,
                kind=LafziResidualKind.MUSHTAQ_REQUIRES_MASDAR,
                trace_ref=trace_ref,
            )
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.DEFERRED,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=InternalWordPathCandidate.DEFERRED,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )

        if proposed_internal_path is InternalWordPathCandidate.PROPER:
            if form_state_result.source_identity is SourceIdentityCandidate.PROPER_SELF_DESIGNATION:
                return InternalWordPathGateResult(
                    state=InternalWordPathGateState.PROVEN,
                    form_state_gate_ref=form_state_result.trace_ref,
                    word_kind=form_state_result.word_kind,
                    source_identity=form_state_result.source_identity,
                    form_state=form_state_result.form_state,
                    internal_word_path=proposed_internal_path,
                    residuals=residuals,
                    rank=LAFZI_B5_RANK_CEILING,
                    trace_ref=trace_ref,
                )
            residuals = _append_residual_once(
                residuals,
                kind=LafziResidualKind.PROPER_SELF_DESIGNATION_REQUIRED,
                trace_ref=trace_ref,
            )
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.DEFERRED,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=InternalWordPathCandidate.DEFERRED,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )

        if proposed_internal_path is InternalWordPathCandidate.REFERENCE:
            if form_state_result.source_identity in _REFERENCE_IDENTITIES:
                return InternalWordPathGateResult(
                    state=InternalWordPathGateState.PROVEN,
                    form_state_gate_ref=form_state_result.trace_ref,
                    word_kind=form_state_result.word_kind,
                    source_identity=form_state_result.source_identity,
                    form_state=form_state_result.form_state,
                    internal_word_path=proposed_internal_path,
                    residuals=residuals,
                    rank=LAFZI_B5_RANK_CEILING,
                    trace_ref=trace_ref,
                )
            residuals = _append_residual_once(
                residuals,
                kind=LafziResidualKind.REFERENCE_SOURCE_REQUIRED,
                trace_ref=trace_ref,
            )
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.DEFERRED,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=InternalWordPathCandidate.DEFERRED,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )

        if proposed_internal_path in _ISM_INTERNAL_PATHS:
            # Safe default: unmapped identities (or DEFERRED_SOURCE) do not prove any
            # internal path and must stay visible as DEFERRED with residuals.
            compatible_internal_paths = _SOURCE_IDENTITY_INTERNAL_PATH_COMPATIBILITY.get(
                form_state_result.source_identity,
                (),
            )
            if proposed_internal_path in compatible_internal_paths:
                return InternalWordPathGateResult(
                    state=InternalWordPathGateState.PROVEN,
                    form_state_gate_ref=form_state_result.trace_ref,
                    word_kind=form_state_result.word_kind,
                    source_identity=form_state_result.source_identity,
                    form_state=form_state_result.form_state,
                    internal_word_path=proposed_internal_path,
                    residuals=residuals,
                    rank=LAFZI_B5_RANK_CEILING,
                    trace_ref=trace_ref,
                )
            residuals = _append_residual_once(
                residuals,
                kind=_classify_ism_path_residual(
                    source_identity=form_state_result.source_identity,
                    proposed_internal_path=proposed_internal_path,
                ),
                trace_ref=trace_ref,
            )
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.DEFERRED,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=InternalWordPathCandidate.DEFERRED,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )

        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.ISM_PATH_AMBIGUOUS,
            trace_ref=trace_ref,
        )
        return InternalWordPathGateResult(
            state=InternalWordPathGateState.DEFERRED,
            form_state_gate_ref=form_state_result.trace_ref,
            word_kind=form_state_result.word_kind,
            source_identity=form_state_result.source_identity,
            form_state=form_state_result.form_state,
            internal_word_path=InternalWordPathCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if form_state_result.word_kind is WordKindCandidate.FIIL:
        if proposed_internal_path in _FIIL_INTERNAL_PATHS:
            if (
                form_state_result.source_identity
                is not SourceIdentityCandidate.FIIL_MASDAR_TEMPORAL_IMAGE
            ):
                residual_kind = (
                    LafziResidualKind.FIIL_TEMPORAL_IMAGE_REQUIRED
                    if proposed_internal_path
                    is InternalWordPathCandidate.FIIL_TEMPORAL_OR_REQUEST_IMAGE_PATH
                    else LafziResidualKind.FIIL_MASDAR_REQUIRED
                )
                residuals = _append_residual_once(
                    residuals,
                    kind=residual_kind,
                    trace_ref=trace_ref,
                )
                return InternalWordPathGateResult(
                    state=InternalWordPathGateState.DEFERRED,
                    form_state_gate_ref=form_state_result.trace_ref,
                    word_kind=form_state_result.word_kind,
                    source_identity=form_state_result.source_identity,
                    form_state=form_state_result.form_state,
                    internal_word_path=InternalWordPathCandidate.DEFERRED,
                    residuals=residuals,
                    rank=LAFZI_B5_RANK_CEILING,
                    trace_ref=trace_ref,
                )
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.PROVEN,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=proposed_internal_path,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )

        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.FIIL_MASDAR_REQUIRED,
            trace_ref=trace_ref,
        )
        return InternalWordPathGateResult(
            state=InternalWordPathGateState.DEFERRED,
            form_state_gate_ref=form_state_result.trace_ref,
            word_kind=form_state_result.word_kind,
            source_identity=form_state_result.source_identity,
            form_state=form_state_result.form_state,
            internal_word_path=InternalWordPathCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if form_state_result.word_kind is WordKindCandidate.HARF:
        if (
            proposed_internal_path in _HARF_INTERNAL_PATHS
            and form_state_result.source_identity
            is SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY
        ):
            return InternalWordPathGateResult(
                state=InternalWordPathGateState.PROVEN,
                form_state_gate_ref=form_state_result.trace_ref,
                word_kind=form_state_result.word_kind,
                source_identity=form_state_result.source_identity,
                form_state=form_state_result.form_state,
                internal_word_path=proposed_internal_path,
                residuals=residuals,
                rank=LAFZI_B5_RANK_CEILING,
                trace_ref=trace_ref,
            )
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.HARF_OPERATOR_REQUIRED,
            trace_ref=trace_ref,
        )
        return InternalWordPathGateResult(
            state=InternalWordPathGateState.DEFERRED,
            form_state_gate_ref=form_state_result.trace_ref,
            word_kind=form_state_result.word_kind,
            source_identity=form_state_result.source_identity,
            form_state=form_state_result.form_state,
            internal_word_path=InternalWordPathCandidate.DEFERRED,
            residuals=residuals,
            rank=LAFZI_B5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    residuals = _append_residual_once(
        residuals,
        kind=LafziResidualKind.ISM_PATH_AMBIGUOUS,
        trace_ref=trace_ref,
    )
    return InternalWordPathGateResult(
        state=InternalWordPathGateState.DEFERRED,
        form_state_gate_ref=form_state_result.trace_ref,
        word_kind=form_state_result.word_kind,
        source_identity=form_state_result.source_identity,
        form_state=form_state_result.form_state,
        internal_word_path=InternalWordPathCandidate.DEFERRED,
        residuals=residuals,
        rank=LAFZI_B5_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_lafzi_residual_audit(
    internal_word_path_result: InternalWordPathGateResult,
    *,
    trace_ref: str,
) -> LafziResidualAuditResult:
    """Run LAFZI-B6 residual audit without opening LAFZI-B7 closure/handoff."""

    if not isinstance(internal_word_path_result, InternalWordPathGateResult):
        raise WeightCarrierSchemaError(
            "prove_lafzi_residual_audit requires InternalWordPathGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_lafzi_residual_audit.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if internal_word_path_result.output != LAFZI_B5_ALLOWED_OUTPUT:
        raise WeightCarrierSchemaError(
            "prove_lafzi_residual_audit prior result must be LAFZI-B5 output "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    residuals = internal_word_path_result.residuals
    if (
        internal_word_path_result.state is InternalWordPathGateState.BLOCKED
        and not any(residual.blocking for residual in residuals)
    ):
        residuals = _append_residual_once(
            residuals,
            kind=LafziResidualKind.UNUSED_DAL_NO_LAFZI,
            trace_ref=trace_ref,
            blocking=True,
        )

    blocking_residuals = tuple(residual for residual in residuals if residual.blocking)
    non_blocking_residuals = tuple(residual for residual in residuals if not residual.blocking)

    if internal_word_path_result.state is InternalWordPathGateState.BLOCKED or blocking_residuals:
        state = LafziResidualAuditState.BLOCKED
    elif internal_word_path_result.state is InternalWordPathGateState.DEFERRED or residuals:
        state = LafziResidualAuditState.DEFERRED
    else:
        state = LafziResidualAuditState.PROVEN

    return LafziResidualAuditResult(
        state=state,
        internal_word_path_gate_ref=internal_word_path_result.trace_ref,
        word_kind=internal_word_path_result.word_kind,
        source_identity=internal_word_path_result.source_identity,
        form_state=internal_word_path_result.form_state,
        internal_word_path=internal_word_path_result.internal_word_path,
        residuals=residuals,
        blocking_residuals=blocking_residuals,
        non_blocking_residuals=non_blocking_residuals,
        rank=LAFZI_B6_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "LAFZI_B1_FORBIDDEN_OUTPUTS",
    "LAFZI_B1_RANK_CEILING",
    "LAFZI_B1_RESIDUAL_VOCABULARY",
    "LAFZI_B2_ALLOWED_OUTPUT",
    "LAFZI_B2_RANK_CEILING",
    "LAFZI_B3_ALLOWED_OUTPUT",
    "LAFZI_B3_RANK_CEILING",
    "LAFZI_B4_ALLOWED_OUTPUT",
    "LAFZI_B4_RANK_CEILING",
    "LAFZI_B5_ALLOWED_OUTPUT",
    "LAFZI_B5_RANK_CEILING",
    "LAFZI_B6_ALLOWED_OUTPUT",
    "LAFZI_B6_RANK_CEILING",
    "FormStateCandidate",
    "FormStateGateResult",
    "FormStateGateState",
    "InternalWordPathCandidate",
    "InternalWordPathGateResult",
    "InternalWordPathGateState",
    "LafziMadlulCandidate",
    "LafziMadlulCandidateSet",
    "LafziMadlulState",
    "LafziResidualAuditResult",
    "LafziResidualAuditState",
    "LafziResidual",
    "LafziResidualKind",
    "LafziScope",
    "MappingState",
    "SourceIdentityCandidate",
    "SourceIdentityGateResult",
    "SourceIdentityGateState",
    "WordKindCandidate",
    "WordKindCandidateGateResult",
    "WordKindCandidateGateState",
    "prove_form_state_candidate_gate",
    "prove_internal_word_path_candidate_gate",
    "prove_lafzi_residual_audit",
    "prove_source_identity_candidate_gate",
    "prove_word_kind_candidate_gate",
]
