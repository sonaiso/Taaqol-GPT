"""G0-C1 carrier surface: BareJamidStemCandidate + AnchorCertificate.

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §5, §13.
Chain position: G0-C1 (carrier surface only).
Forbidden: gates, verdicts, rank promotion, hukm/truth/certainty outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class G0C1CarrierSchemaError(TypeError):
    """Raised when a G0-C1 carrier is malformed at birth."""


class OntologicalClass(StrEnum):
    """Ontological class codes from docs/77 §3."""

    O1 = "O1"
    O2 = "O2"
    O3 = "O3"
    O4 = "O4"
    O5 = "O5"
    O6 = "O6"
    O7 = "O7"
    O8 = "O8"
    O9 = "O9"
    O10 = "O10"


class EpistemicRank(StrEnum):
    """Epistemic rank codes from docs/77 §4."""

    E0 = "E0"
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"
    E4 = "E4"
    E5 = "E5"


class EntityRank(StrEnum):
    """Entity-rank surface named in docs/77 §5."""

    INDIVIDUAL = "INDIVIDUAL"
    SPECIES = "SPECIES"
    GENUS = "GENUS"
    GROUP = "GROUP"
    MASS = "MASS"


class StemGender(StrEnum):
    """Stem-property gender surface (docs/77 §1, §5)."""

    MASCULINE = "MASCULINE"
    FEMININE = "FEMININE"
    COMMON = "COMMON"


class LexicalTruthStatus(StrEnum):
    """Lexical assignment status for the bare stem surface."""

    ATTESTED = "ATTESTED"
    CANDIDATE = "CANDIDATE"
    SUSPENDED = "SUSPENDED"



def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C1CarrierSchemaError(f"{cls_name}.{field} must be a non-empty string")



def _require_tuple_of_strings(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise G0C1CarrierSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise G0C1CarrierSchemaError(
                f"{cls_name}.{field} must contain non-empty strings"
            )



def _require_probability(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, float) or value < 0.0 or value > 1.0:
        raise G0C1CarrierSchemaError(f"{cls_name}.{field} must be a float in [0.0, 1.0]")



def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise G0C1CarrierSchemaError(
            f"{cls_name}.{field} must start with 'trace://'"
        )


@dataclass(frozen=True, slots=True)
class BareJamidStemCandidate:
    """Carrier-only representation of the docs/77 §5 Bare Jamid Stem card."""

    stem: str
    vocalized: str
    size: int
    pattern: str
    has_productive_addition: bool
    jamid: bool
    ontological_class: OntologicalClass
    entity_rank: EntityRank
    gender: StemGender
    gender_evidence: str
    epistemic_rank: EpistemicRank
    lexical_truth_status: LexicalTruthStatus
    hard_blockers_passed: tuple[str, ...]
    d_form: float
    d_wad: float
    d_onto: float
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "stem", self.stem)
        _require_nonempty_str(cls, "vocalized", self.vocalized)
        if not isinstance(self.size, int) or self.size < 1:
            raise G0C1CarrierSchemaError(f"{cls}.size must be a positive integer")
        _require_nonempty_str(cls, "pattern", self.pattern)
        if not isinstance(self.has_productive_addition, bool):
            raise G0C1CarrierSchemaError(
                f"{cls}.has_productive_addition must be bool"
            )
        if not isinstance(self.jamid, bool):
            raise G0C1CarrierSchemaError(f"{cls}.jamid must be bool")
        if not isinstance(self.ontological_class, OntologicalClass):
            raise G0C1CarrierSchemaError(
                f"{cls}.ontological_class must be OntologicalClass"
            )
        if not isinstance(self.entity_rank, EntityRank):
            raise G0C1CarrierSchemaError(f"{cls}.entity_rank must be EntityRank")
        if not isinstance(self.gender, StemGender):
            raise G0C1CarrierSchemaError(f"{cls}.gender must be StemGender")
        _require_nonempty_str(cls, "gender_evidence", self.gender_evidence)
        if not isinstance(self.epistemic_rank, EpistemicRank):
            raise G0C1CarrierSchemaError(
                f"{cls}.epistemic_rank must be EpistemicRank"
            )
        if not isinstance(self.lexical_truth_status, LexicalTruthStatus):
            raise G0C1CarrierSchemaError(
                f"{cls}.lexical_truth_status must be LexicalTruthStatus"
            )
        _require_tuple_of_strings(cls, "hard_blockers_passed", self.hard_blockers_passed)
        _require_probability(cls, "d_form", self.d_form)
        _require_probability(cls, "d_wad", self.d_wad)
        _require_probability(cls, "d_onto", self.d_onto)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class AnchorCertificate:
    """Carrier-only anchor certificate shell reserved for downstream steps."""

    certificate_id: str
    stem_key: str
    ontological_class: OntologicalClass
    epistemic_rank: EpistemicRank
    entity_rank: EntityRank
    source_trace_ref: str
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "certificate_id", self.certificate_id)
        _require_nonempty_str(cls, "stem_key", self.stem_key)
        if not isinstance(self.ontological_class, OntologicalClass):
            raise G0C1CarrierSchemaError(
                f"{cls}.ontological_class must be OntologicalClass"
            )
        if not isinstance(self.epistemic_rank, EpistemicRank):
            raise G0C1CarrierSchemaError(
                f"{cls}.epistemic_rank must be EpistemicRank"
            )
        if not isinstance(self.entity_rank, EntityRank):
            raise G0C1CarrierSchemaError(f"{cls}.entity_rank must be EntityRank")
        _require_trace_ref(cls, "source_trace_ref", self.source_trace_ref)
        _require_tuple_of_strings(cls, "residuals", self.residuals)


__all__ = [
    "AnchorCertificate",
    "BareJamidStemCandidate",
    "EntityRank",
    "EpistemicRank",
    "G0C1CarrierSchemaError",
    "LexicalTruthStatus",
    "OntologicalClass",
    "StemGender",
]
