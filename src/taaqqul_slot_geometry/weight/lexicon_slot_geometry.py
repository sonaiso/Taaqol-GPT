"""LEXICON-SLOT-L0 bounded lexical slot geometry surface.

This module implements a minimal execution package aligned to docs/100:
* carrier contracts for LexicalSlot / RankVector / LexicalCandidateSet,
* contract-only transition surfaces TC_SR..TC_SD,
* one bounded vertical pilot builder from real source evidence to
  DalalahCandidateSlot with visible residuals.

The module is candidate-only. It does not open semantic/hukm/truth closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    require_non_empty as _require_non_empty,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_rank as _validate_rank,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    TransitionContractId,
    canonical_transition_contract_registry,
)

LEXICON_SLOT_RANK_CEILING: Rank = Rank.CANDIDATE
LEXICON_SLOT_ALLOWED_OUTPUT: str = "DALALAH_CANDIDATE_SLOT"
LEXICON_SLOT_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "FINAL_CONTEXTUAL_MEANING",
    "ONTOLOGICAL_FACT",
    "EMPIRICAL_FACT",
    "IFADAH",
    "HUKM",
    "TRUTH",
    "REALITY_CERTIFICATE",
)
LEXICON_SLOT_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "READING_UNCERTAIN",
    "IDENTITY_CONFLICT",
    "ROOT_UNCERTAIN",
    "SENSE_UNDERDETERMINED",
    "USAGE_EVIDENCE_PARTIAL",
    "SOURCE_DISAGREEMENT",
    "MISSING_CONTEXT_REFERENCE",
    "WORDNET_NO_ENTRY",
    "WORDNET_MULTIPLE_SENSES",
    "WORDNET_POS_MISMATCH",
    "WORDNET_CONTEXT_UNRESOLVED",
    "WORDNET_RELATION_UNQUALIFIED",
    "WORDNET_CROSS_LINGUAL_ONLY",
    "WORDNET_GLOSS_INSUFFICIENT",
    "WORDNET_SOURCE_CONFLICT",
    "WORDNET_FORM_MISMATCH",
    "WORDNET_EXTERNAL_AUTHORITY_LIMIT",
)


class LexicalEntityType(StrEnum):
    """Top-level lexical entity paths allowed by LEXICON-SLOT-L0."""

    ROOT = "ROOT"
    JAMID_STEM = "JAMID_STEM"
    DERIVED_LEXEME = "DERIVED_LEXEME"
    MABNI = "MABNI"
    FUNCTION_UNIT = "FUNCTION_UNIT"
    PROPER_NAME = "PROPER_NAME"
    BORROWED = "BORROWED"
    COMPOUND = "COMPOUND"
    RESIDUAL = "RESIDUAL"


class LexiconResidualKind(StrEnum):
    """Local residual vocabulary for lexicon slot geometry."""

    READING_UNCERTAIN = "READING_UNCERTAIN"
    IDENTITY_CONFLICT = "IDENTITY_CONFLICT"
    ROOT_UNCERTAIN = "ROOT_UNCERTAIN"
    SENSE_UNDERDETERMINED = "SENSE_UNDERDETERMINED"
    USAGE_EVIDENCE_PARTIAL = "USAGE_EVIDENCE_PARTIAL"
    SOURCE_DISAGREEMENT = "SOURCE_DISAGREEMENT"
    MISSING_CONTEXT_REFERENCE = "MISSING_CONTEXT_REFERENCE"
    WORDNET_NO_ENTRY = "WORDNET_NO_ENTRY"
    WORDNET_MULTIPLE_SENSES = "WORDNET_MULTIPLE_SENSES"
    WORDNET_POS_MISMATCH = "WORDNET_POS_MISMATCH"
    WORDNET_CONTEXT_UNRESOLVED = "WORDNET_CONTEXT_UNRESOLVED"
    WORDNET_RELATION_UNQUALIFIED = "WORDNET_RELATION_UNQUALIFIED"
    WORDNET_CROSS_LINGUAL_ONLY = "WORDNET_CROSS_LINGUAL_ONLY"
    WORDNET_GLOSS_INSUFFICIENT = "WORDNET_GLOSS_INSUFFICIENT"
    WORDNET_SOURCE_CONFLICT = "WORDNET_SOURCE_CONFLICT"
    WORDNET_FORM_MISMATCH = "WORDNET_FORM_MISMATCH"
    WORDNET_EXTERNAL_AUTHORITY_LIMIT = "WORDNET_EXTERNAL_AUTHORITY_LIMIT"


class DalalahCandidateKind(StrEnum):
    """Bounded lexical dalalah candidate labels."""

    MUTABAQAH = "MUTABAQAH"
    TADAMMUN = "TADAMMUN"
    ILTIZAM = "ILTIZAM"


@dataclass(frozen=True, slots=True)
class LexiconResidual:
    """Visible residual carried by lexical slot outputs."""

    kind: LexiconResidualKind
    trace_ref: str
    detail: str = ""
    blocking: bool = False
    visibility: Literal["VISIBLE"] = "VISIBLE"

    def __post_init__(self) -> None:
        if not isinstance(self.kind, LexiconResidualKind):
            raise WeightCarrierSchemaError(
                "LexiconResidual.kind must be LexiconResidualKind "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _require_non_empty(self.trace_ref, "LexiconResidual.trace_ref", FailureCode.TRACE_MISSING)
        if self.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                f"LexiconResidual.visibility must be VISIBLE ({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                f"LexiconResidual.blocking must be bool ({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class RankVector:
    """Independent lexical rank channels."""

    r_source: Rank
    r_reading: Rank
    r_identity: Rank
    r_root: Rank
    r_wad: Rank
    r_sense: Rank
    r_usage: Rank
    r_ontology: Rank

    def __post_init__(self) -> None:
        for field_name in (
            "r_source",
            "r_reading",
            "r_identity",
            "r_root",
            "r_wad",
            "r_sense",
            "r_usage",
            "r_ontology",
        ):
            _validate_rank(
                getattr(self, field_name),
                f"RankVector.{field_name}",
                ceiling=LEXICON_SLOT_RANK_CEILING,
            )


@dataclass(frozen=True, slots=True)
class LexicalSlot:
    """Canonical licensed lexical slot carrier."""

    anchor: str
    identity: str
    lexical_type: LexicalEntityType
    domain: str
    boundary: str
    source: str
    operation: str
    invariant: str
    evidence: tuple[str, ...]
    rank_vector: RankVector
    trace_ref: str
    residuals: tuple[LexiconResidual, ...]
    closure: str

    def __post_init__(self) -> None:
        _require_non_empty(self.anchor, "LexicalSlot.anchor", FailureCode.IDENTITY_BROKEN)
        _require_non_empty(self.identity, "LexicalSlot.identity", FailureCode.IDENTITY_BROKEN)
        if not isinstance(self.lexical_type, LexicalEntityType):
            raise WeightCarrierSchemaError(
                "LexicalSlot.lexical_type must be LexicalEntityType "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        _require_non_empty(self.domain, "LexicalSlot.domain", FailureCode.DOMAIN_MISSING)
        _require_non_empty(self.boundary, "LexicalSlot.boundary", FailureCode.BOUNDARY_MISSING)
        _require_non_empty(self.source, "LexicalSlot.source", FailureCode.UNLICENSED_OPENING)
        _require_non_empty(self.operation, "LexicalSlot.operation", FailureCode.UNLICENSED_OPENING)
        _require_non_empty(self.invariant, "LexicalSlot.invariant", FailureCode.BOUNDARY_MISSING)
        if not isinstance(self.evidence, tuple) or not self.evidence:
            raise WeightCarrierSchemaError(
                "LexicalSlot.evidence must be a non-empty tuple "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for evidence_ref in self.evidence:
            _require_non_empty(
                evidence_ref,
                "LexicalSlot.evidence entry",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank_vector, RankVector):
            raise WeightCarrierSchemaError(
                "LexicalSlot.rank_vector must be RankVector "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_non_empty(self.trace_ref, "LexicalSlot.trace_ref", FailureCode.TRACE_MISSING)
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                f"LexicalSlot.residuals must be a tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, LexiconResidual):
                raise WeightCarrierSchemaError(
                    "LexicalSlot.residuals entries must be LexiconResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        _require_non_empty(self.closure, "LexicalSlot.closure", FailureCode.BOUNDARY_MISSING)


@dataclass(frozen=True, slots=True)
class DalalahCandidateSlot:
    """Candidate-only lexical dalalah slot."""

    lexical_slot_ref: str
    candidate_kind: DalalahCandidateKind
    candidate_label: str
    rank: Rank
    residuals: tuple[LexiconResidual, ...]
    trace_ref: str
    forbidden_outputs: tuple[str, ...] = LEXICON_SLOT_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.lexical_slot_ref,
            "DalalahCandidateSlot.lexical_slot_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        if not isinstance(self.candidate_kind, DalalahCandidateKind):
            raise WeightCarrierSchemaError(
                "DalalahCandidateSlot.candidate_kind must be DalalahCandidateKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_non_empty(
            self.candidate_label,
            "DalalahCandidateSlot.candidate_label",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _validate_rank(self.rank, "DalalahCandidateSlot", ceiling=LEXICON_SLOT_RANK_CEILING)
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalalahCandidateSlot.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, LexiconResidual):
                raise WeightCarrierSchemaError(
                    "DalalahCandidateSlot.residuals entries must be LexiconResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        _require_non_empty(
            self.trace_ref,
            "DalalahCandidateSlot.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.forbidden_outputs != LEXICON_SLOT_FORBIDDEN_OUTPUTS:
            raise WeightCarrierSchemaError(
                "DalalahCandidateSlot.forbidden_outputs must preserve "
                "LEXICON_SLOT_FORBIDDEN_OUTPUTS "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )


@dataclass(frozen=True, slots=True)
class LexicalCandidateSet:
    """Lookup output surface: a bounded set of lexical candidates."""

    candidates: tuple[DalalahCandidateSlot, ...]
    identity_proofs: tuple[str, ...]
    placement_evidence: tuple[str, ...]
    usage_scopes: tuple[str, ...]
    rank_vector: RankVector
    residuals: tuple[LexiconResidual, ...]
    traces: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.candidates, tuple) or not self.candidates:
            raise WeightCarrierSchemaError(
                "LexicalCandidateSet.candidates must be a non-empty tuple "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for candidate in self.candidates:
            if not isinstance(candidate, DalalahCandidateSlot):
                raise WeightCarrierSchemaError(
                    "LexicalCandidateSet.candidates entries must be DalalahCandidateSlot "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )
        for field_name, values in (
            ("identity_proofs", self.identity_proofs),
            ("placement_evidence", self.placement_evidence),
            ("usage_scopes", self.usage_scopes),
            ("traces", self.traces),
        ):
            if not isinstance(values, tuple) or not values:
                raise WeightCarrierSchemaError(
                    f"LexicalCandidateSet.{field_name} must be a non-empty tuple "
                    f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
            for value in values:
                _require_non_empty(
                    value,
                    f"LexicalCandidateSet.{field_name} entry",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        if not isinstance(self.rank_vector, RankVector):
            raise WeightCarrierSchemaError(
                "LexicalCandidateSet.rank_vector must be RankVector "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                f"LexicalCandidateSet.residuals must be tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, LexiconResidual):
                raise WeightCarrierSchemaError(
                    "LexicalCandidateSet.residuals entries must be LexiconResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )


@dataclass(frozen=True, slots=True)
class LexicalTransitionContract:
    """Contract-only transition descriptor for lexical slot flow."""

    contract_id: str
    input_slot: str
    output_slot: str
    required_fields: tuple[str, ...]
    allows_multi_candidate: bool
    rank_ceiling: Rank = LEXICON_SLOT_RANK_CEILING

    def __post_init__(self) -> None:
        _require_non_empty(
            self.contract_id,
            "LexicalTransitionContract.contract_id",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.input_slot,
            "LexicalTransitionContract.input_slot",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.output_slot,
            "LexicalTransitionContract.output_slot",
            FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.required_fields, tuple) or not self.required_fields:
            raise WeightCarrierSchemaError(
                "LexicalTransitionContract.required_fields must be a non-empty tuple "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for required in self.required_fields:
            _require_non_empty(
                required,
                "LexicalTransitionContract.required_fields entry",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.allows_multi_candidate, bool):
            raise WeightCarrierSchemaError(
                "LexicalTransitionContract.allows_multi_candidate must be bool "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_rank(
            self.rank_ceiling,
            "LexicalTransitionContract",
            ceiling=LEXICON_SLOT_RANK_CEILING,
        )


def _build_lexical_transition_contract(
    contract_id: TransitionContractId,
) -> LexicalTransitionContract:
    spec = canonical_transition_contract_registry().contract_by_id(contract_id)
    return LexicalTransitionContract(
        contract_id=spec.contract_id.value,
        input_slot=spec.source_slot,
        output_slot=spec.target_slot,
        required_fields=spec.required_fields,
        allows_multi_candidate=spec.allows_multi_candidate,
    )


TC_SR = _build_lexical_transition_contract(TransitionContractId.TC_SR)
TC_RI = _build_lexical_transition_contract(TransitionContractId.TC_RI)
TC_IL = _build_lexical_transition_contract(TransitionContractId.TC_IL)
TC_LW = _build_lexical_transition_contract(TransitionContractId.TC_LW)
TC_WS = _build_lexical_transition_contract(TransitionContractId.TC_WS)
TC_SD = _build_lexical_transition_contract(TransitionContractId.TC_SD)


def build_vertical_lexical_candidate_set_from_source_row(
    row: dict[str, object],
) -> LexicalCandidateSet:
    """Build one bounded source->dalalah candidate set from a lexical evidence row."""

    source_id = str(row.get("id", "")).strip()
    surface = str(row.get("surface", "")).strip()
    root_or_stem = str(row.get("root_or_stem", "")).strip()
    trace_ref = str(row.get("trace_ref", "")).strip()
    source_attestations = row.get("source_attestations", [])

    _require_non_empty(source_id, "row.id", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(surface, "row.surface", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(root_or_stem, "row.root_or_stem", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(trace_ref, "row.trace_ref", FailureCode.TRACE_MISSING)
    if not isinstance(source_attestations, list) or not source_attestations:
        raise WeightCarrierSchemaError(
            "row.source_attestations must be a non-empty list "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )

    evidence_refs = tuple(
        f"{attestation.get('source', 'unknown')}:{attestation.get('entry', surface)}"
        for attestation in source_attestations
        if isinstance(attestation, dict)
    )
    if not evidence_refs:
        raise WeightCarrierSchemaError(
            "row.source_attestations must include dict attestations "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )

    rank_vector = RankVector(
        r_source=Rank.TRACE,
        r_reading=Rank.CANDIDATE,
        r_identity=Rank.CANDIDATE,
        r_root=Rank.CANDIDATE,
        r_wad=Rank.CANDIDATE,
        r_sense=Rank.CANDIDATE,
        r_usage=Rank.CANDIDATE,
        r_ontology=Rank.TRACE,
    )

    residual_kind = (
        LexiconResidualKind.SENSE_UNDERDETERMINED
        if surface == "عين"
        else LexiconResidualKind.USAGE_EVIDENCE_PARTIAL
    )
    residuals = (
        LexiconResidual(
            kind=residual_kind,
            trace_ref=trace_ref,
            detail="Visible lexical residual preserved for downstream context licensing.",
            blocking=False,
        ),
    )

    lexical_slot = LexicalSlot(
        anchor=f"lex-anchor://{source_id}",
        identity=f"lex-identity://{surface}:{root_or_stem}",
        lexical_type=LexicalEntityType.JAMID_STEM,
        domain="LEXICON_LICENSED_BOUNDARY",
        boundary="SOURCE_READING_IDENTITY_WAD_SENSE_USAGE",
        source=f"lex-data://{source_id}",
        operation="SOURCE_TO_LEXICAL_CANDIDATE",
        invariant="LEXICON_CLOSURE_IS_NOT_MEANING_CLOSURE",
        evidence=evidence_refs,
        rank_vector=rank_vector,
        trace_ref=trace_ref,
        residuals=residuals,
        closure="LEXICAL_SENSE_CLOSED",
    )

    candidate = DalalahCandidateSlot(
        lexical_slot_ref=lexical_slot.identity,
        candidate_kind=DalalahCandidateKind.MUTABAQAH,
        candidate_label=surface,
        rank=Rank.CANDIDATE,
        residuals=residuals,
        trace_ref=f"{trace_ref}:dalalah",
    )

    return LexicalCandidateSet(
        candidates=(candidate,),
        identity_proofs=(lexical_slot.identity,),
        placement_evidence=evidence_refs,
        usage_scopes=("LUGHAWI_USAGE",),
        rank_vector=rank_vector,
        residuals=residuals,
        traces=(lexical_slot.trace_ref, candidate.trace_ref),
    )


def build_wordnet_lexical_candidate_set_from_rows(
    rows: tuple[dict[str, object], ...] | list[dict[str, object]],
) -> LexicalCandidateSet:
    """Build a bounded lexical candidate set from WordNet sense rows.

    The output remains candidate-only and preserves provenance/ambiguity.
    """

    if not isinstance(rows, (tuple, list)) or not rows:
        raise WeightCarrierSchemaError(
            "rows must be a non-empty list/tuple "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )

    normalized_rows: tuple[dict[str, object], ...] = tuple(rows)
    for row in normalized_rows:
        if not isinstance(row, dict):
            raise WeightCarrierSchemaError(
                "rows entries must be dict "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )

    query_form_id = str(normalized_rows[0].get("query_form_id", "")).strip()
    query_lemma = str(normalized_rows[0].get("query_lemma", "")).strip()
    query_pos = str(normalized_rows[0].get("query_pos", "")).strip()
    source_id = str(normalized_rows[0].get("source_id", "")).strip()
    source_version = str(normalized_rows[0].get("source_version", "")).strip()

    _require_non_empty(query_form_id, "rows[0].query_form_id", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(query_lemma, "rows[0].query_lemma", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(query_pos, "rows[0].query_pos", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(source_id, "rows[0].source_id", FailureCode.REQUIRED_SLOT_EMPTY)
    _require_non_empty(
        source_version,
        "rows[0].source_version",
        FailureCode.REQUIRED_SLOT_EMPTY,
    )

    for row in normalized_rows:
        row_query = str(row.get("query_form_id", "")).strip()
        row_lemma = str(row.get("query_lemma", "")).strip()
        row_pos = str(row.get("query_pos", "")).strip()
        row_source = str(row.get("source_id", "")).strip()
        row_version = str(row.get("source_version", "")).strip()
        if (
            row_query != query_form_id
            or row_lemma != query_lemma
            or row_pos != query_pos
            or row_source != source_id
            or row_version != source_version
        ):
            raise WeightCarrierSchemaError(
                "rows must share query/source identity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )

    rank_vector = RankVector(
        r_source=Rank.TRACE,
        r_reading=Rank.CANDIDATE,
        r_identity=Rank.CANDIDATE,
        r_root=Rank.CANDIDATE,
        r_wad=Rank.CANDIDATE,
        r_sense=Rank.CANDIDATE,
        r_usage=Rank.CANDIDATE,
        r_ontology=Rank.TRACE,
    )

    first_trace_ref = str(normalized_rows[0].get("trace_ref", "")).strip()
    _require_non_empty(first_trace_ref, "rows[0].trace_ref", FailureCode.TRACE_MISSING)

    residuals: tuple[LexiconResidual, ...] = (
        LexiconResidual(
            kind=LexiconResidualKind.WORDNET_EXTERNAL_AUTHORITY_LIMIT,
            trace_ref=first_trace_ref,
            detail="WordNet is external lexical evidence, not semantic authority.",
            blocking=False,
        ),
    )
    if len(normalized_rows) > 1:
        residuals = residuals + (
            LexiconResidual(
                kind=LexiconResidualKind.WORDNET_MULTIPLE_SENSES,
                trace_ref=first_trace_ref,
                detail="Multiple lexical senses remain visible pending context qualification.",
                blocking=False,
            ),
        )

    lexical_slot = LexicalSlot(
        anchor=f"lex-wordnet-anchor://{query_form_id}",
        identity=f"lex-wordnet-identity://{query_lemma}:{query_pos}",
        lexical_type=LexicalEntityType.DERIVED_LEXEME,
        domain="LEXICON_LICENSED_BOUNDARY",
        boundary="LICENSED_FORM_TO_EXTERNAL_LEXICAL_EVIDENCE",
        source=f"{source_id}:{source_version}",
        operation="WORDNET_SENSE_INVENTORY_TO_DALALAH_CANDIDATES",
        invariant="WORDNET_EVIDENCE_IS_NOT_FINAL_MEANING",
        evidence=tuple(
            f"{source_id}:{str(row.get('synset_id', '')).strip()}" for row in normalized_rows
        ),
        rank_vector=rank_vector,
        trace_ref=first_trace_ref,
        residuals=residuals,
        closure="LEXICAL_SENSE_CANDIDATES_VISIBLE",
    )

    candidates: list[DalalahCandidateSlot] = []
    traces: list[str] = [lexical_slot.trace_ref]
    identity_proofs: list[str] = [lexical_slot.identity]
    usage_scopes: list[str] = [f"WORDNET_POS:{query_pos}"]
    for row in normalized_rows:
        synset_id = str(row.get("synset_id", "")).strip()
        trace_ref = str(row.get("trace_ref", "")).strip()
        _require_non_empty(synset_id, "row.synset_id", FailureCode.REQUIRED_SLOT_EMPTY)
        _require_non_empty(trace_ref, "row.trace_ref", FailureCode.TRACE_MISSING)
        candidate_label = str(row.get("query_lemma", "")).strip()
        lemmas = row.get("lemmas", ())
        if isinstance(lemmas, list) and lemmas:
            first_lemma = str(lemmas[0]).strip()
            if first_lemma:
                candidate_label = first_lemma

        candidate = DalalahCandidateSlot(
            lexical_slot_ref=f"{lexical_slot.identity}:{synset_id}",
            candidate_kind=DalalahCandidateKind.MUTABAQAH,
            candidate_label=candidate_label,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace_ref=f"{trace_ref}:dalalah",
        )
        candidates.append(candidate)
        traces.append(candidate.trace_ref)
        identity_proofs.append(f"{lexical_slot.identity}:{synset_id}")

    return LexicalCandidateSet(
        candidates=tuple(candidates),
        identity_proofs=tuple(identity_proofs),
        placement_evidence=lexical_slot.evidence,
        usage_scopes=tuple(usage_scopes),
        rank_vector=rank_vector,
        residuals=residuals,
        traces=tuple(traces),
    )


__all__ = [
    "LEXICON_SLOT_ALLOWED_OUTPUT",
    "LEXICON_SLOT_FORBIDDEN_OUTPUTS",
    "LEXICON_SLOT_RANK_CEILING",
    "LEXICON_SLOT_RESIDUAL_VOCABULARY",
    "TC_IL",
    "TC_LW",
    "TC_RI",
    "TC_SD",
    "TC_SR",
    "TC_WS",
    "DalalahCandidateKind",
    "DalalahCandidateSlot",
    "LexicalCandidateSet",
    "LexicalEntityType",
    "LexicalSlot",
    "LexicalTransitionContract",
    "LexiconResidual",
    "LexiconResidualKind",
    "RankVector",
    "build_wordnet_lexical_candidate_set_from_rows",
    "build_vertical_lexical_candidate_set_from_source_row",
]
