"""DalOnlyCandidate Boundary — PR-15.

PR-15 binding of ``docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md``.
This module introduces:

* :class:`DalBoundaryState` — the two verdict states.
* :class:`DalOnlyCandidate` — the signifier-alone carrier.
* :class:`DalBoundaryVerdict` — the signifier candidacy proof.
* :func:`prove_dal` — the signifier boundary operation consuming only a
  :class:`~taaqqul_slot_geometry.weight.licensing_boundary.LicensingBoundaryVerdict`.

Constitutional invariants (docs/26):

* prove_dal() accepts ONLY a LicensingBoundaryVerdict as prior.
* prove_dal() refuses all earlier-stage carriers.
* DalOnlyCandidate is a signifier identity proof, NOT
  VerbalMadlulCandidate, meaning, ifadah, hukm, or reality.
* No rank promotion beyond DAL_BOUNDARY_RANK_CEILING.
* Residual governance from PR-14 is respected.
* TraceRef remains a reference, not an audit ledger commit.
* No VerbalMadlulCandidate, no DalMadlulBindingCandidate.
* No LexicalMadlul, no meaning, no composition.
* No extra-letter licensing, no ContractableUnitGeometry.
* No new FailureCode members; no new runtime dependencies.
* prove_dal() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.licensing_boundary import (
    LICENSE_BOUNDARY_RANK_CEILING,
    LicensingBoundaryVerdict,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-15 — same as LICENSE_BOUNDARY_RANK_CEILING.
#: No dal boundary verdict may emit a rank above this value (docs/26 §5).
DAL_BOUNDARY_RANK_CEILING: Rank = LICENSE_BOUNDARY_RANK_CEILING

# docs/26 boundary: DAL-only outputs stay at signifier surface and must not
# emit form/meaning/isnad outputs before licensed bridges.
DAL_ONLY_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "ROOT_FORM",
    "PATTERN_FORM",
    "TOOL_FORM",
    "MABNI_FORM",
    "LEXICAL_MEANING",
    "ISNAD",
    "IFADAH",
    "HUKM",
)

# docs/58 / DAL-A1: local residual vocabulary for the signifier-alone atomic
# surface. These names are deliberately local and do not expand FailureCode.
DAL_A1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "RAW_TRACE_NOT_SPEECH",
    "MAKHRAJ_MISSING",
    "SIFAH_MISSING",
    "QADIH_SOUND_DIFF_MISSING",
    "HARAKA_WITHOUT_CARRIER",
    "MADD_WITHOUT_EXTENSION",
    "SHADDA_UNEXPANDED",
    "HAMZA_UNRESOLVED",
    "WASL_HAMZA_UNRESOLVED",
    "SUKUN_COLLISION",
    "SYLLABLE_UNLICENSED",
    "WAQF_UNTESTED",
    "WASL_UNTESTED",
    "UNVOCALIZED_SURFACE",
    "PHONETIC_SEQUENCE_AMBIGUOUS",
    "UNUSED_LAFZ",
    "LOAN_PATH_REQUIRED",
    "DELETION_UNLICENSED",
    "ENERGY_COLLISION",
)

DAL_A1_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "WORD_KIND",
    "ROOT",
    "PATTERN",
    "LICENSED_WEIGHT",
    "LEXICAL_MEANING",
    "VERBAL_MADLUL_CANDIDATE",
    "DAL_MADLUL_BINDING_CANDIDATE",
    "RELATION_CANDIDATE",
    "IFADAH_CANDIDATE",
    "HUKM_CANDIDATE",
    "TANZIL_CANDIDATE",
    "REALITY",
    "ONTOLOGY",
    "LAFZI_MADLUL_GATE",
    "DAL_ALONE_CLOSED",
)

DAL_A1_RANK_CEILING: Rank = Rank.CANDIDATE


class DalResidualKind(StrEnum):
    """Local DAL-A1 residual names from docs/58 §11."""

    RAW_TRACE_NOT_SPEECH = "RAW_TRACE_NOT_SPEECH"
    MAKHRAJ_MISSING = "MAKHRAJ_MISSING"
    SIFAH_MISSING = "SIFAH_MISSING"
    QADIH_SOUND_DIFF_MISSING = "QADIH_SOUND_DIFF_MISSING"
    HARAKA_WITHOUT_CARRIER = "HARAKA_WITHOUT_CARRIER"
    MADD_WITHOUT_EXTENSION = "MADD_WITHOUT_EXTENSION"
    SHADDA_UNEXPANDED = "SHADDA_UNEXPANDED"
    HAMZA_UNRESOLVED = "HAMZA_UNRESOLVED"
    WASL_HAMZA_UNRESOLVED = "WASL_HAMZA_UNRESOLVED"
    SUKUN_COLLISION = "SUKUN_COLLISION"
    SYLLABLE_UNLICENSED = "SYLLABLE_UNLICENSED"
    WAQF_UNTESTED = "WAQF_UNTESTED"
    WASL_UNTESTED = "WASL_UNTESTED"
    UNVOCALIZED_SURFACE = "UNVOCALIZED_SURFACE"
    PHONETIC_SEQUENCE_AMBIGUOUS = "PHONETIC_SEQUENCE_AMBIGUOUS"
    UNUSED_LAFZ = "UNUSED_LAFZ"
    LOAN_PATH_REQUIRED = "LOAN_PATH_REQUIRED"
    DELETION_UNLICENSED = "DELETION_UNLICENSED"
    ENERGY_COLLISION = "ENERGY_COLLISION"


@dataclass(frozen=True, slots=True)
class DalResidual:
    """Visible local DAL residual; not a global FailureCode."""

    kind: DalResidualKind
    trace_ref: str
    visibility: Literal["VISIBLE"] = "VISIBLE"
    blocking: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, DalResidualKind):
            raise WeightCarrierSchemaError(
                "DalResidual.kind must be a local DalResidualKind "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if self.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                "DalResidual.visibility must be VISIBLE "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                "DalResidual.blocking must be a bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalResidual.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


def _validate_dal_a1_carrier(
    *,
    identity: str,
    domain_id: str,
    scope: str,
    rank: Rank,
    trace_ref: str,
    residuals: tuple[DalResidual, ...],
    forbidden_outputs: tuple[str, ...],
) -> None:
    if not isinstance(identity, str) or not identity.strip():
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier identity must be non-empty "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )
    if domain_id != "DAL_ONLY":
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier domain_id must be DAL_ONLY "
            f"({FailureCode.DOMAIN_MISSING.value})"
        )
    if not isinstance(scope, str) or not scope.strip():
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier scope must be non-empty "
            f"({FailureCode.SCOPE_MISSING.value})"
        )
    if not isinstance(rank, Rank):
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier rank must be a Rank member "
            f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
        )
    if rank > DAL_A1_RANK_CEILING:
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier rank must not exceed CANDIDATE "
            f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )
    if not isinstance(trace_ref, str) or not trace_ref.strip():
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier trace_ref must be non-empty "
            f"({FailureCode.TRACE_MISSING.value})"
        )
    if not isinstance(residuals, tuple):
        raise WeightCarrierSchemaError(
            "DAL-A1 carrier residuals must be a tuple "
            f"({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    for residual in residuals:
        if not isinstance(residual, DalResidual):
            raise WeightCarrierSchemaError(
                "DAL-A1 carrier residual entries must be DalResidual "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
    if not isinstance(forbidden_outputs, tuple):
        raise WeightCarrierSchemaError(
            "DAL-A1 forbidden_outputs must be a tuple "
            f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
        )
    for output in forbidden_outputs:
        if not isinstance(output, str) or not output.strip():
            raise WeightCarrierSchemaError(
                "DAL-A1 forbidden output names must be non-empty "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )


@dataclass(frozen=True, slots=True)
class RawTrace:
    """DAL-A1 raw trace carrier; not an Arabic sound verdict."""

    identity: str
    raw_ref: str
    trace_kind: Literal["ACOUSTIC", "GRAPHIC", "UNICODE", "MIXED"]
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if self.trace_kind not in ("ACOUSTIC", "GRAPHIC", "UNICODE", "MIXED"):
            raise WeightCarrierSchemaError(
                "RawTrace.trace_kind must remain a pre-sound trace label "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.raw_ref, str) or not self.raw_ref.strip():
            raise WeightCarrierSchemaError(
                "RawTrace.raw_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class GraphemeCandidate:
    """DAL-A1 grapheme candidate carrier; not phonetic realization."""

    identity: str
    unicode_surface: str
    raw_trace: RawTrace
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if not isinstance(self.raw_trace, RawTrace):
            raise WeightCarrierSchemaError(
                "GraphemeCandidate.raw_trace must be RawTrace "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.unicode_surface, str) or not self.unicode_surface.strip():
            raise WeightCarrierSchemaError(
                "GraphemeCandidate.unicode_surface must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )


@dataclass(frozen=True, slots=True)
class LetterIdentity:
    """DAL-A1 letter identity carrier; not word kind, root, or meaning."""

    identity: str
    letter_label: str
    grapheme: GraphemeCandidate
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if not isinstance(self.grapheme, GraphemeCandidate):
            raise WeightCarrierSchemaError(
                "LetterIdentity.grapheme must be GraphemeCandidate "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.letter_label, str) or not self.letter_label.strip():
            raise WeightCarrierSchemaError(
                "LetterIdentity.letter_label must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )


@dataclass(frozen=True, slots=True)
class PhoneticRealization:
    """DAL-A1 phonetic realization carrier; not ArabicSound closure."""

    identity: str
    realization_ref: str
    letter_identity: LetterIdentity
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if not isinstance(self.letter_identity, LetterIdentity):
            raise WeightCarrierSchemaError(
                "PhoneticRealization.letter_identity must be LetterIdentity "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.realization_ref, str) or not self.realization_ref.strip():
            raise WeightCarrierSchemaError(
                "PhoneticRealization.realization_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class AtomicSoundUnit:
    """DAL-A1 atomic sound-unit carrier; not S1-S5 closure or word kind."""

    identity: str
    sound_ref: str
    phonetic_realization: PhoneticRealization
    makhraj_ref: str
    sifah_ref: str
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if not isinstance(self.phonetic_realization, PhoneticRealization):
            raise WeightCarrierSchemaError(
                "AtomicSoundUnit.phonetic_realization must be PhoneticRealization "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        for field_name, value in (
            ("sound_ref", self.sound_ref),
            ("makhraj_ref", self.makhraj_ref),
            ("sifah_ref", self.sifah_ref),
        ):
            if not isinstance(value, str):
                raise WeightCarrierSchemaError(
                    f"AtomicSoundUnit.{field_name} must be a string "
                    f"({FailureCode.TRACE_MISSING.value})"
                )


@dataclass(frozen=True, slots=True)
class DalAloneClosureSurface:
    """DAL-A1 surface carrier that remains before DalAloneClosed."""

    identity: str
    prior_dal_trace_ref: str
    raw_trace: RawTrace
    graphemes: tuple[GraphemeCandidate, ...]
    letters: tuple[LetterIdentity, ...]
    phonetic_realizations: tuple[PhoneticRealization, ...]
    atomic_units: tuple[AtomicSoundUnit, ...]
    domain_id: Literal["DAL_ONLY"]
    scope: str
    rank: Rank
    trace_ref: str
    residuals: tuple[DalResidual, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _validate_dal_a1_carrier(
            identity=self.identity,
            domain_id=self.domain_id,
            scope=self.scope,
            rank=self.rank,
            trace_ref=self.trace_ref,
            residuals=self.residuals,
            forbidden_outputs=self.forbidden_outputs,
        )
        if not isinstance(self.prior_dal_trace_ref, str) or not self.prior_dal_trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalAloneClosureSurface.prior_dal_trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.raw_trace, RawTrace):
            raise WeightCarrierSchemaError(
                "DalAloneClosureSurface.raw_trace must be RawTrace "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        for field_name, values, value_type in (
            ("graphemes", self.graphemes, GraphemeCandidate),
            ("letters", self.letters, LetterIdentity),
            ("phonetic_realizations", self.phonetic_realizations, PhoneticRealization),
            ("atomic_units", self.atomic_units, AtomicSoundUnit),
        ):
            if not isinstance(values, tuple):
                raise WeightCarrierSchemaError(
                    f"DalAloneClosureSurface.{field_name} must be a tuple "
                    f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
            for value in values:
                if not isinstance(value, value_type):
                    raise WeightCarrierSchemaError(
                        f"DalAloneClosureSurface.{field_name} entries have invalid type "
                        f"({FailureCode.GATE_REQUIRED.value})"
                    )


# ---------------------------------------------------------------------------
# DalBoundaryState — the two verdict states
# ---------------------------------------------------------------------------


class DalBoundaryState(StrEnum):
    """The outcome of a prove_dal() operation (docs/26 §4)."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# DalOnlyCandidate — the signifier-alone carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalOnlyCandidate:
    """The signifier-alone boundary carrier (docs/26 §2).

    Proves the signifier surface (identity, phonetic trace, graphic
    trace, prior licensing boundary verdict) stands independently
    before any signified. It does NOT carry meaning, madlul, ifadah,
    hukm, reality, binding, composition, extra-letter license,
    augmentation category, or ContractableUnitGeometry.

    Fields:
    * ``signifier_identity`` — the signifier surface identity.
    * ``phonetic_trace_ref`` — reference to phonetic trace.
    * ``graphic_trace_ref`` — reference to graphic trace (may be empty
      for oral-only forms).
    * ``prior_licensing_verdict`` — the LicensingBoundaryVerdict from PR-14.
    * ``dal_rank`` — the candidate rank, bounded to the ceiling.
    * ``residuals`` — residuals carried from prior layers.
    * ``trace_ref`` — reference, not ledger commit.
    """

    signifier_identity: str
    phonetic_trace_ref: str
    graphic_trace_ref: str
    prior_licensing_verdict: LicensingBoundaryVerdict
    dal_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.signifier_identity, str) or not self.signifier_identity.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.signifier_identity must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.phonetic_trace_ref, str) or not self.phonetic_trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.phonetic_trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.graphic_trace_ref, str):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.graphic_trace_ref must be a string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.prior_licensing_verdict, LicensingBoundaryVerdict):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.prior_licensing_verdict must be a "
                "LicensingBoundaryVerdict — signifier candidacy without a "
                f"prior licensing verdict is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.dal_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.dal_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.dal_rank > DAL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.dal_rank must not exceed "
                f"{DAL_BOUNDARY_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalOnlyCandidate.residuals entries must be Residual carriers "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# DalBoundaryVerdict — the signifier candidacy proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalBoundaryVerdict:
    """The output of :func:`prove_dal` — a signifier candidacy proof (docs/26 §4).

    Proves that a signifier surface can stand independently as a
    boundary-proven candidate. It does NOT carry meaning, madlul,
    ifadah, hukm, reality, binding, or any post-signifier content.

    Fields:
    * ``candidate`` — the DalOnlyCandidate that was proven (or None on refusal).
    * ``verdict_state`` — PROVEN or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    * ``verdict_rank`` — the verdict rank, bounded to the ceiling.
    * ``residuals`` — residuals carried through.
    * ``trace_ref`` — reference, not ledger commit.
    """

    candidate: DalOnlyCandidate | None
    verdict_state: DalBoundaryState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict_state, DalBoundaryState):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_state must be a DalBoundaryState member"
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_rank must be a Rank member"
            )
        if self.verdict_rank > DAL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_rank must not exceed "
                f"DAL_BOUNDARY_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.residuals entries must be Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.verdict_state is DalBoundaryState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a PROVEN DalBoundaryVerdict must not carry a FailureCode "
                    "(docs/26 §4)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a PROVEN DalBoundaryVerdict must carry a DalOnlyCandidate "
                    "(docs/26 §4)"
                )
            if not isinstance(self.candidate, DalOnlyCandidate):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.candidate must be a DalOnlyCandidate "
                    "(docs/26 §4)"
                )
        elif self.verdict_state is DalBoundaryState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalBoundaryVerdict must carry a named FailureCode "
                    "(docs/26 §4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.failure_code must be a FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalBoundaryVerdict must not carry a candidate "
                    "(docs/26 §4)"
                )


# ---------------------------------------------------------------------------
# prove_dal() — the signifier boundary operation
# ---------------------------------------------------------------------------


def prove_dal(
    prior_verdict: LicensingBoundaryVerdict,
    signifier_identity: str,
    phonetic_trace_ref: str,
    graphic_trace_ref: str = "",
) -> DalBoundaryVerdict:
    """Signifier boundary proof — signifier candidacy (docs/26).

    A pure function: evaluates whether the signifier surface described
    by a prior :class:`LicensingBoundaryVerdict` can stand independently
    as a DalOnlyCandidate, producing a :class:`DalBoundaryVerdict`.

    Input boundary (docs/26 §3):

    * Accepts ONLY a LicensingBoundaryVerdict as prior.
    * Refuses all other input types with a named FailureCode.

    Output:

    * On success: PROVEN with a DalOnlyCandidate.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement ---
    if not isinstance(prior_verdict, LicensingBoundaryVerdict):
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/input_boundary",
        )

    # --- Signifier identity validation ---
    if not isinstance(signifier_identity, str) or not signifier_identity.strip():
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/signifier_identity_missing",
        )

    # --- Phonetic trace validation ---
    if not isinstance(phonetic_trace_ref, str) or not phonetic_trace_ref.strip():
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/phonetic_trace_missing",
        )

    # --- Graphic trace ref validation (must be str, may be empty) ---
    if not isinstance(graphic_trace_ref, str):
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/graphic_trace_invalid",
        )

    # --- Residual governance from the prior verdict ---
    # Inherit residuals from the prior verdict's source (the WeightFitCandidate)
    inherited_residuals = prior_verdict.source.residuals

    # Check for hidden-forbidden residuals
    for r in inherited_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return DalBoundaryVerdict(
                candidate=None,
                verdict_state=DalBoundaryState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_dal/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return DalBoundaryVerdict(
                candidate=None,
                verdict_state=DalBoundaryState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_dal/refused/blocking_residual",
            )

    # --- Bound the rank ---
    dal_rank = RankLattice.meet(
        prior_verdict.eligibility_rank, DAL_BOUNDARY_RANK_CEILING
    )

    # --- Construct the DalOnlyCandidate ---
    candidate = DalOnlyCandidate(
        signifier_identity=signifier_identity,
        phonetic_trace_ref=phonetic_trace_ref,
        graphic_trace_ref=graphic_trace_ref,
        prior_licensing_verdict=prior_verdict,
        dal_rank=dal_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_dal/proven/{signifier_identity}",
    )

    return DalBoundaryVerdict(
        candidate=candidate,
        verdict_state=DalBoundaryState.PROVEN,
        failure_code=None,
        verdict_rank=dal_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_dal/proven/{signifier_identity}",
    )


class CarrierOperationProfile(StrEnum):
    """DAL-only carrier identity profile."""

    HEAVY_CARRIER = "HEAVY_CARRIER"
    LIGHT_CARRIER = "LIGHT_CARRIER"
    WEAK_OR_MADD_CARRIER = "WEAK_OR_MADD_CARRIER"
    HAMZA_OR_SEAT_CARRIER = "HAMZA_OR_SEAT_CARRIER"


class HarakaMarkType(StrEnum):
    """Haraka functions are attached to carriers, never independent tokens."""

    FATHA = "FATHA"
    DAMMA = "DAMMA"
    KASRA = "KASRA"
    SUKUN = "SUKUN"
    SHADDA = "SHADDA"
    TANWIN = "TANWIN"
    MISSING = "MISSING"


class EdgeMode(StrEnum):
    """Boundary relation mode on each edge."""

    START = "START"
    INTERNAL_WASL = "INTERNAL_WASL"
    FINAL_WAQF = "FINAL_WAQF"
    FINAL_WASL = "FINAL_WASL"
    CONTINUATION = "CONTINUATION"


class EdgeOpenness(StrEnum):
    """Opening/closure state carried by an edge."""

    OPEN_A = "OPEN_A"
    OPEN_U = "OPEN_U"
    OPEN_I = "OPEN_I"
    CLOSED = "CLOSED"
    LENGTHENED = "LENGTHENED"
    UNRESOLVED = "UNRESOLVED"


class HarakaSurfaceFunction(StrEnum):
    """DAL-only surface operation produced by a mark."""

    OPEN_EDGE_A = "OPEN_EDGE_A"
    OPEN_EDGE_U = "OPEN_EDGE_U"
    OPEN_EDGE_I = "OPEN_EDGE_I"
    CLOSE_EDGE = "CLOSE_EDGE"
    IDENTITY_COMPRESSION = "IDENTITY_COMPRESSION"
    NASAL_TAIL_POTENTIAL = "NASAL_TAIL_POTENTIAL"
    SUSPEND_MARK = "SUSPEND_MARK"


class DalAtomicCellStatus(StrEnum):
    """Cell status inside DAL-only atomic operations."""

    CELL_LICENSED = "CELL_LICENSED"
    CELL_SUSPENDED = "CELL_SUSPENDED"
    CELL_BLOCKED = "CELL_BLOCKED"
    CELL_REPAIR_REQUIRED = "CELL_REPAIR_REQUIRED"


class DalAtomicSkeletonStatus(StrEnum):
    """Surface skeleton status inside DAL-only."""

    DAL_SKELETON_LICENSED = "DAL_SKELETON_LICENSED"
    DAL_SKELETON_SUSPENDED = "DAL_SKELETON_SUSPENDED"
    DAL_SKELETON_BLOCKED = "DAL_SKELETON_BLOCKED"
    DAL_SKELETON_REPAIR_REQUIRED = "DAL_SKELETON_REPAIR_REQUIRED"


class DalAtomicOperationState(StrEnum):
    """Unified DAL-only operation outcomes."""

    LICENSED_IN_DOMAIN = "LICENSED_IN_DOMAIN"
    BRIDGE_REQUIRED = "BRIDGE_REQUIRED"
    BLOCKED_BY_GATE = "BLOCKED_BY_GATE"
    RESIDUAL_CANDIDATE = "RESIDUAL_CANDIDATE"
    PROOF_REQUIRED = "PROOF_REQUIRED"


@dataclass(frozen=True, slots=True)
class ProofObject:
    """Explicit, auditable DAL-only proof payload."""

    proof_id: str
    domain_id: Literal["DAL_ONLY"]
    checked_gates: tuple[str, ...]
    preserved_identity: tuple[str, ...]
    residuals: tuple[str, ...]
    failure_codes: tuple[FailureCode, ...]
    trace: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.proof_id, str) or not self.proof_id.strip():
            raise WeightCarrierSchemaError(
                "ProofObject.proof_id must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if self.domain_id != "DAL_ONLY":
            raise WeightCarrierSchemaError(
                "ProofObject.domain_id must be DAL_ONLY "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if not isinstance(self.checked_gates, tuple):
            raise WeightCarrierSchemaError(
                "ProofObject.checked_gates must be a tuple "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.trace, tuple) or not self.trace:
            raise WeightCarrierSchemaError(
                "ProofObject.trace must be a non-empty tuple "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.failure_codes, tuple):
            raise WeightCarrierSchemaError(
                "ProofObject.failure_codes must be a tuple "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        for code in self.failure_codes:
            if not isinstance(code, FailureCode):
                raise WeightCarrierSchemaError(
                    "ProofObject.failure_codes entries must be FailureCode members "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )


@dataclass(frozen=True, slots=True)
class DomainScopedCandidate:
    """Domain contract used by DAL-only atomic candidates."""

    candidate_id: str
    domain_id: Literal["DAL_ONLY"]
    layer_id: Literal["DAL_ATOMIC"]
    element_type: str
    local_slots: tuple[object, ...]
    forbidden_outputs: tuple[str, ...]
    proof: ProofObject
    trace_ref: str
    rank: Rank = Rank.CANDIDATE
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id.strip():
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.candidate_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.domain_id != "DAL_ONLY":
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.domain_id must be DAL_ONLY "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if self.layer_id != "DAL_ATOMIC":
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.layer_id must be DAL_ATOMIC "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.proof, ProofObject):
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.proof must be ProofObject "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.rank > Rank.CANDIDATE:
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.rank must not exceed CANDIDATE in DAL-only "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DomainScopedCandidate.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class CarrierIdentitySlot:
    """DAL-only carrier identity and operation profile."""

    carrier_id: str
    glyph: str
    position_index: int
    profile: CarrierOperationProfile
    can_bear_haraka: bool
    can_close_surface: bool
    can_link_left: bool
    can_link_right: bool
    weak_or_madd_profile: bool
    hamza_or_seat_profile: bool
    proof_object: ProofObject
    forbidden_outputs: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.carrier_id, str) or not self.carrier_id.strip():
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.carrier_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.glyph, str) or not self.glyph.strip():
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.glyph must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.position_index, int) or self.position_index < 0:
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.position_index must be a non-negative integer "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.profile, CarrierOperationProfile):
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.profile must be a CarrierOperationProfile "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.proof_object, ProofObject):
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.proof_object must be ProofObject "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "CarrierIdentitySlot.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class EdgeState:
    """Incoming/outgoing edge state of a carrier cell."""

    edge_id: str
    boundary_mode: EdgeMode
    openness: EdgeOpenness
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.edge_id, str) or not self.edge_id.strip():
            raise WeightCarrierSchemaError(
                "EdgeState.edge_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.boundary_mode, EdgeMode):
            raise WeightCarrierSchemaError(
                "EdgeState.boundary_mode must be EdgeMode "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.openness, EdgeOpenness):
            raise WeightCarrierSchemaError(
                "EdgeState.openness must be EdgeOpenness "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "EdgeState.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class HarakaFunctionSlot:
    """Carrier-attached haraka function (never independent V)."""

    haraka_id: str
    carrier_ref: str
    mark_type: HarakaMarkType
    incoming_edge_ref: str
    outgoing_edge_ref: str
    surface_function: HarakaSurfaceFunction
    possible_lafzi_potentials: tuple[str, ...]
    waqf_policy: str
    wasl_policy: str
    proof_object: ProofObject
    forbidden_outputs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.haraka_id, str) or not self.haraka_id.strip():
            raise WeightCarrierSchemaError(
                "HarakaFunctionSlot.haraka_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.carrier_ref, str) or not self.carrier_ref.strip():
            raise WeightCarrierSchemaError(
                "HarakaFunctionSlot.carrier_ref must be non-empty (no independent mark) "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.mark_type, HarakaMarkType):
            raise WeightCarrierSchemaError(
                "HarakaFunctionSlot.mark_type must be HarakaMarkType "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.proof_object, ProofObject):
            raise WeightCarrierSchemaError(
                "HarakaFunctionSlot.proof_object must be ProofObject "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


@dataclass(frozen=True, slots=True)
class ClosureCell:
    """DAL-only closure cell: left edge + carrier + haraka + right edge."""

    cell_id: str
    left_edge: EdgeState
    carrier: CarrierIdentitySlot
    haraka: HarakaFunctionSlot
    right_edge: EdgeState
    status: DalAtomicCellStatus
    proof: ProofObject
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.cell_id, str) or not self.cell_id.strip():
            raise WeightCarrierSchemaError(
                "ClosureCell.cell_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.left_edge, EdgeState) or not isinstance(self.right_edge, EdgeState):
            raise WeightCarrierSchemaError(
                "ClosureCell edges must be EdgeState carriers "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.carrier, CarrierIdentitySlot):
            raise WeightCarrierSchemaError(
                "ClosureCell.carrier must be CarrierIdentitySlot "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.haraka, HarakaFunctionSlot):
            raise WeightCarrierSchemaError(
                "ClosureCell.haraka must be HarakaFunctionSlot "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.status, DalAtomicCellStatus):
            raise WeightCarrierSchemaError(
                "ClosureCell.status must be DalAtomicCellStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.proof, ProofObject):
            raise WeightCarrierSchemaError(
                "ClosureCell.proof must be ProofObject "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "ClosureCell.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class SurfaceSkeletonCandidate:
    """DAL-only surface skeleton candidate with explicit boundary projections."""

    skeleton_id: str
    domain_candidate: DomainScopedCandidate
    cells: tuple[ClosureCell, ...]
    wasl_projection: str
    waqf_projection: str
    status: DalAtomicSkeletonStatus
    bridge_required_marker: str
    proof: ProofObject
    forbidden_outputs: tuple[str, ...]
    trace_ref: str
    rank: Rank = Rank.CANDIDATE

    def __post_init__(self) -> None:
        if not isinstance(self.skeleton_id, str) or not self.skeleton_id.strip():
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.skeleton_id must be non-empty "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.domain_candidate, DomainScopedCandidate):
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.domain_candidate must be DomainScopedCandidate "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.cells, tuple) or len(self.cells) == 0:
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.cells must be a non-empty tuple "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.wasl_projection, str) or not self.wasl_projection.strip():
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.wasl_projection must be non-empty "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.waqf_projection, str) or not self.waqf_projection.strip():
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.waqf_projection must be non-empty "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.status, DalAtomicSkeletonStatus):
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.status must be DalAtomicSkeletonStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.proof, ProofObject):
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.proof must be ProofObject "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.rank > Rank.CANDIDATE:
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.rank must not exceed CANDIDATE "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "SurfaceSkeletonCandidate.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class DalAtomicOperationResult:
    """Operation result wrapper for DAL-only atomic helpers."""

    state: DalAtomicOperationState
    failure_code: FailureCode | None
    candidate: object | None
    residuals: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, DalAtomicOperationState):
            raise WeightCarrierSchemaError(
                "DalAtomicOperationResult.state must be DalAtomicOperationState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalAtomicOperationResult.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalAtomicOperationResult.trace_ref must be non-empty "
                f"({FailureCode.TRACE_MISSING.value})"
            )


def _mark_to_edge(mark_type: HarakaMarkType) -> tuple[EdgeOpenness, HarakaSurfaceFunction]:
    mapping: dict[HarakaMarkType, tuple[EdgeOpenness, HarakaSurfaceFunction]] = {
        HarakaMarkType.FATHA: (EdgeOpenness.OPEN_A, HarakaSurfaceFunction.OPEN_EDGE_A),
        HarakaMarkType.DAMMA: (EdgeOpenness.OPEN_U, HarakaSurfaceFunction.OPEN_EDGE_U),
        HarakaMarkType.KASRA: (EdgeOpenness.OPEN_I, HarakaSurfaceFunction.OPEN_EDGE_I),
        HarakaMarkType.SUKUN: (EdgeOpenness.CLOSED, HarakaSurfaceFunction.CLOSE_EDGE),
        HarakaMarkType.SHADDA: (
            EdgeOpenness.UNRESOLVED,
            HarakaSurfaceFunction.IDENTITY_COMPRESSION,
        ),
        HarakaMarkType.TANWIN: (
            EdgeOpenness.UNRESOLVED,
            HarakaSurfaceFunction.NASAL_TAIL_POTENTIAL,
        ),
        HarakaMarkType.MISSING: (EdgeOpenness.UNRESOLVED, HarakaSurfaceFunction.SUSPEND_MARK),
    }
    return mapping[mark_type]


def identify_carrier(
    raw_letter: str,
    *,
    carrier_id: str,
    position_index: int,
    trace_ref: str,
    profile: CarrierOperationProfile = CarrierOperationProfile.LIGHT_CARRIER,
) -> DalAtomicOperationResult:
    """Build a DAL-only CarrierIdentitySlot without cross-domain claims."""
    if not isinstance(raw_letter, str) or not raw_letter.strip():
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            candidate=None,
            residuals=(),
            trace_ref="identify_carrier/refused/raw_letter_missing",
        )

    # DAL-only surface affordance: right-non-linking glyphs block right joins
    # at this orthographic layer, without opening any lexical/morphological claim.
    right_non_linking_glyphs = {"ا", "د", "ذ", "ر", "ز", "و", "ء", "ؤ"}
    can_link_left = position_index > 0
    can_link_right = raw_letter not in right_non_linking_glyphs

    proof = ProofObject(
        proof_id=f"proof://dal_only/carrier/{carrier_id}",
        domain_id="DAL_ONLY",
        checked_gates=("IDENTIFY_CARRIER",),
        preserved_identity=(carrier_id,),
        residuals=(),
        failure_codes=(),
        trace=(trace_ref,),
    )
    carrier = CarrierIdentitySlot(
        carrier_id=carrier_id,
        glyph=raw_letter,
        position_index=position_index,
        profile=profile,
        # DAL-only carrier affordance defaults (no cross-domain role claims).
        can_bear_haraka=True,
        can_close_surface=True,
        can_link_left=can_link_left,
        can_link_right=can_link_right,
        weak_or_madd_profile=profile == CarrierOperationProfile.WEAK_OR_MADD_CARRIER,
        hamza_or_seat_profile=profile == CarrierOperationProfile.HAMZA_OR_SEAT_CARRIER,
        proof_object=proof,
        forbidden_outputs=DAL_ONLY_FORBIDDEN_OUTPUTS,
        trace_ref=trace_ref,
    )
    return DalAtomicOperationResult(
        state=DalAtomicOperationState.LICENSED_IN_DOMAIN,
        failure_code=None,
        candidate=carrier,
        residuals=(),
        trace_ref=f"identify_carrier/proven/{carrier_id}",
    )


def attach_haraka(
    carrier: CarrierIdentitySlot,
    mark_type: HarakaMarkType,
    *,
    edge_mode: EdgeMode,
    trace_ref: str,
) -> DalAtomicOperationResult:
    """Attach a haraka function to a licensed carrier (no independent mark)."""
    if not isinstance(carrier, CarrierIdentitySlot):
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            residuals=("DAL_SUSPENDED_MISSING_CARRIER",),
            trace_ref="attach_haraka/refused/missing_carrier",
        )
    if not isinstance(mark_type, HarakaMarkType):
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            residuals=("DAL_BOUNDARY_RESIDUAL",),
            trace_ref="attach_haraka/refused/invalid_mark_type",
        )
    if not isinstance(edge_mode, EdgeMode):
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            residuals=("DAL_BOUNDARY_RESIDUAL",),
            trace_ref="attach_haraka/refused/invalid_edge_mode",
        )
    if edge_mode == EdgeMode.START and mark_type == HarakaMarkType.SUKUN:
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.BLOCKED_BY_GATE,
            failure_code=FailureCode.BOUNDARY_MISSING,
            candidate=None,
            residuals=("DAL_REPAIR_REQUIRED_HAMZAT_WASL",),
            trace_ref="attach_haraka/refused/initial_sukun",
        )

    mark_residuals = ("DAL_SUSPENDED_MISSING_MARK",) if mark_type == HarakaMarkType.MISSING else ()
    right_open, surface_function = _mark_to_edge(mark_type)
    proof = ProofObject(
        proof_id=f"proof://dal_only/cell/{carrier.carrier_id}/{mark_type.value.lower()}",
        domain_id="DAL_ONLY",
        checked_gates=("NO_INDEPENDENT_MARK", "ATTACH_HARAKA"),
        preserved_identity=(carrier.carrier_id,),
        residuals=mark_residuals,
        failure_codes=(),
        trace=(trace_ref,),
    )
    left_edge = EdgeState(
        edge_id=f"{carrier.carrier_id}:left",
        boundary_mode=edge_mode,
        openness=EdgeOpenness.UNRESOLVED,
        trace_ref=trace_ref,
    )
    right_edge = EdgeState(
        edge_id=f"{carrier.carrier_id}:right",
        boundary_mode=edge_mode,
        openness=right_open,
        trace_ref=trace_ref,
    )
    haraka = HarakaFunctionSlot(
        haraka_id=f"haraka://{carrier.carrier_id}",
        carrier_ref=carrier.carrier_id,
        mark_type=mark_type,
        incoming_edge_ref=left_edge.edge_id,
        outgoing_edge_ref=right_edge.edge_id,
        surface_function=surface_function,
        possible_lafzi_potentials=("PATTERN_POTENTIAL", "FINAL_EDGE_POTENTIAL"),
        waqf_policy="PROJECT_TO_WAQF",
        wasl_policy="PROJECT_TO_WASL",
        proof_object=proof,
        forbidden_outputs=DAL_ONLY_FORBIDDEN_OUTPUTS,
    )
    cell = ClosureCell(
        cell_id=f"cell://{carrier.carrier_id}",
        left_edge=left_edge,
        carrier=carrier,
        haraka=haraka,
        right_edge=right_edge,
        status=(
            DalAtomicCellStatus.CELL_SUSPENDED
            if mark_type == HarakaMarkType.MISSING
            else DalAtomicCellStatus.CELL_LICENSED
        ),
        proof=proof,
        trace_ref=trace_ref,
    )
    return DalAtomicOperationResult(
        state=(
            DalAtomicOperationState.RESIDUAL_CANDIDATE
            if mark_type == HarakaMarkType.MISSING
            else DalAtomicOperationState.LICENSED_IN_DOMAIN
        ),
        failure_code=None,
        candidate=cell,
        residuals=mark_residuals,
        trace_ref=f"attach_haraka/proven/{carrier.carrier_id}",
    )


def build_surface_skeleton(
    cells: tuple[ClosureCell, ...],
    *,
    wasl_projection: str,
    waqf_projection: str,
    trace_ref: str,
) -> DalAtomicOperationResult:
    """Build a DAL-only surface skeleton with explicit waqf/wasl projection."""
    if not isinstance(cells, tuple) or len(cells) == 0:
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            candidate=None,
            residuals=("DAL_SUSPENDED_EMPTY_SURFACE",),
            trace_ref="build_surface_skeleton/refused/empty_cells",
        )
    if any(not isinstance(cell, ClosureCell) for cell in cells):
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            residuals=("DAL_BOUNDARY_RESIDUAL",),
            trace_ref="build_surface_skeleton/refused/invalid_cell",
        )
    if not isinstance(wasl_projection, str) or not isinstance(waqf_projection, str):
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            residuals=("DAL_BOUNDARY_RESIDUAL",),
            trace_ref="build_surface_skeleton/refused/invalid_projection_type",
        )
    if not wasl_projection.strip() or not waqf_projection.strip():
        return DalAtomicOperationResult(
            state=DalAtomicOperationState.PROOF_REQUIRED,
            failure_code=FailureCode.BOUNDARY_MISSING,
            candidate=None,
            residuals=("DAL_BOUNDARY_RESIDUAL",),
            trace_ref="build_surface_skeleton/refused/missing_projection",
        )
    suspended = any(cell.status != DalAtomicCellStatus.CELL_LICENSED for cell in cells)
    proof = ProofObject(
        proof_id="proof://dal_only/surface_skeleton",
        domain_id="DAL_ONLY",
        checked_gates=("WASL_PROJECTION_GATE", "WAQF_PROJECTION_GATE"),
        preserved_identity=tuple(cell.carrier.carrier_id for cell in cells),
        residuals=("DAL_SUSPENDED_MISSING_MARK",) if suspended else (),
        failure_codes=(),
        trace=(trace_ref,),
    )
    domain_candidate = DomainScopedCandidate(
        candidate_id="dal-surface-candidate",
        domain_id="DAL_ONLY",
        layer_id="DAL_ATOMIC",
        element_type="SurfaceSkeletonCandidate",
        local_slots=cells,
        forbidden_outputs=DAL_ONLY_FORBIDDEN_OUTPUTS,
        proof=proof,
        trace_ref=trace_ref,
        rank=Rank.CANDIDATE,
        residuals=("DAL_SUSPENDED_MISSING_MARK",) if suspended else (),
    )
    skeleton = SurfaceSkeletonCandidate(
        skeleton_id="surface://dal_only",
        domain_candidate=domain_candidate,
        cells=cells,
        wasl_projection=wasl_projection,
        waqf_projection=waqf_projection,
        status=(
            DalAtomicSkeletonStatus.DAL_SKELETON_SUSPENDED
            if suspended
            else DalAtomicSkeletonStatus.DAL_SKELETON_LICENSED
        ),
        bridge_required_marker="DAL_BRIDGE_REQUIRED_TO_LAFZI",
        proof=proof,
        forbidden_outputs=DAL_ONLY_FORBIDDEN_OUTPUTS,
        trace_ref=trace_ref,
        rank=Rank.CANDIDATE,
    )
    return DalAtomicOperationResult(
        state=DalAtomicOperationState.BRIDGE_REQUIRED,
        failure_code=None,
        candidate=skeleton,
        residuals=(
            ("DAL_BRIDGE_REQUIRED_TO_LAFZI", "DAL_SUSPENDED_MISSING_MARK")
            if suspended
            else ("DAL_BRIDGE_REQUIRED_TO_LAFZI",)
        ),
        trace_ref="build_surface_skeleton/proven",
    )


__all__ = [
    "DAL_A1_FORBIDDEN_OUTPUTS",
    "DAL_A1_RANK_CEILING",
    "DAL_A1_RESIDUAL_VOCABULARY",
    "DAL_BOUNDARY_RANK_CEILING",
    "DAL_ONLY_FORBIDDEN_OUTPUTS",
    "AtomicSoundUnit",
    "CarrierIdentitySlot",
    "CarrierOperationProfile",
    "ClosureCell",
    "DalAloneClosureSurface",
    "DalAtomicCellStatus",
    "DalAtomicOperationResult",
    "DalAtomicOperationState",
    "DalAtomicSkeletonStatus",
    "DalBoundaryState",
    "DalBoundaryVerdict",
    "DalOnlyCandidate",
    "DalResidual",
    "DalResidualKind",
    "DomainScopedCandidate",
    "EdgeMode",
    "EdgeOpenness",
    "EdgeState",
    "GraphemeCandidate",
    "HarakaFunctionSlot",
    "HarakaMarkType",
    "HarakaSurfaceFunction",
    "LetterIdentity",
    "PhoneticRealization",
    "ProofObject",
    "RawTrace",
    "SurfaceSkeletonCandidate",
    "attach_haraka",
    "build_surface_skeleton",
    "identify_carrier",
    "prove_dal",
]
