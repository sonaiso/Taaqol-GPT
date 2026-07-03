"""DAL-A3 Arabic sound inventory + makhraj/sifah/qadih proof surface.

This module opens only the DAL-A3 boundary licensed by docs/58 and docs/14.
It remains a bounded inventory/proof surface and does not open DAL-A4/DAL-A5.
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
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

DAL_A3_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A3_ALLOWED_OUTPUT: str = "ArabicSoundInventoryGate"
DAL_A3_GATE_ORDER: tuple[str, ...] = (
    "InventoryDeclarationStage",
    "SoundEntryStage",
    "MakhrajProofStage",
    "SifahProofStage",
    "QadihSoundDifferenceStage",
    "ResidualVisibilityStage",
    "ForbiddenOutputStage",
    "HandoffStage",
)

DAL_A3_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "SyllableLicenseGate",
    "RootIdentityGate",
    "WeightPathSelectionGate",
    "MeaningGate",
    "IfadahGate",
    "MafhumGate",
    "HukmGate",
    "Truth",
    "Reality",
)

DAL_A3_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MAKHRAJ_MISSING",
    "SIFAH_MISSING",
    "QADIH_SOUND_DIFF_MISSING",
    "SOUND_SIMILARITY_INDICATOR_ONLY",
    # DAL-A3 can register marker/diacritic entries but must defer closure.
    "DEFERRED_TO_DAL_A4",
    "FORBIDDEN_DAL_A3_HANDOFF",
)


class ArabicSoundInventoryKind(StrEnum):
    """DAL-A3 sound inventory kind labels."""

    ARABIC_CONSONANT = "ARABIC_CONSONANT"
    ARABIC_LONG_VOWEL = "ARABIC_LONG_VOWEL"
    DIACRITIC_OR_MARKER = "DIACRITIC_OR_MARKER"


class QadihSoundDifferenceStatus(StrEnum):
    """Qadih sound-difference status labels."""

    CLEAR = "CLEAR"
    BLOCKING = "BLOCKING"
    RESIDUAL = "RESIDUAL"
    UNCHECKED = "UNCHECKED"


class ArabicSoundInventoryReadinessState(StrEnum):
    """DAL-A3 readiness surface."""

    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REFUSED = "REFUSED"


class ArabicSoundInventoryFailedStage(StrEnum):
    """DAL-A3 failure/defer stage labels."""

    INVENTORY = "INVENTORY"
    MAKHRAJ = "MAKHRAJ"
    SIFAH = "SIFAH"
    QADIH = "QADIH"
    RESIDUALS = "RESIDUALS"
    HANDOFF = "HANDOFF"


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A3_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _merge_residuals(*groups: tuple[str, ...]) -> tuple[str, ...]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for residual in group:
            if residual not in seen:
                seen.add(residual)
                merged.append(residual)
    return tuple(merged)


def _remove_residual(residuals: tuple[str, ...], name: str) -> tuple[str, ...]:
    return tuple(residual for residual in residuals if residual != name)


@dataclass(frozen=True, slots=True)
class MakhrajProof:
    """DAL-A3 makhraj evidence carrier."""

    sound_ref: str
    makhraj_ref: str
    makhraj_path: tuple[str, ...]
    source_policy: str
    inventory_version: str
    trace_ref: str
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(self.sound_ref, "MakhrajProof.sound_ref", FailureCode.IDENTITY_BROKEN)
        _require_non_empty(self.makhraj_ref, "MakhrajProof.makhraj_ref", FailureCode.TRACE_MISSING)
        _require_non_empty(
            self.source_policy,
            "MakhrajProof.source_policy",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.inventory_version,
            "MakhrajProof.inventory_version",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(self.trace_ref, "MakhrajProof.trace_ref", FailureCode.TRACE_MISSING)
        if not isinstance(self.makhraj_path, tuple) or not self.makhraj_path:
            raise WeightCarrierSchemaError(
                "MakhrajProof.makhraj_path must be a non-empty tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for node in self.makhraj_path:
            _require_non_empty(
                node,
                "MakhrajProof.makhraj_path entry",
                FailureCode.BOUNDARY_MISSING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "MakhrajProof.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class SifahProof:
    """DAL-A3 sifah evidence carrier."""

    sound_ref: str
    sifah_refs: tuple[str, ...]
    source_policy: str
    inventory_version: str
    trace_ref: str
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(self.sound_ref, "SifahProof.sound_ref", FailureCode.IDENTITY_BROKEN)
        _require_non_empty(
            self.source_policy,
            "SifahProof.source_policy",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.inventory_version,
            "SifahProof.inventory_version",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(self.trace_ref, "SifahProof.trace_ref", FailureCode.TRACE_MISSING)
        if not isinstance(self.sifah_refs, tuple) or not self.sifah_refs:
            raise WeightCarrierSchemaError(
                "SifahProof.sifah_refs must be a non-empty tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for ref in self.sifah_refs:
            _require_non_empty(ref, "SifahProof.sifah_refs entry", FailureCode.BOUNDARY_MISSING)
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "SifahProof.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class QadihSoundDifferenceProof:
    """DAL-A3 qādih sound-difference matrix evidence carrier.

    ``shared_sifah_refs`` records overlapping properties used for similarity
    indication only, while ``differentiating_sifah_refs`` records explicit
    distinguishing properties required to avoid collapsing the two sounds.
    """

    origin_sound_ref: str
    branch_sound_ref: str
    shared_sifah_refs: tuple[str, ...]
    differentiating_sifah_refs: tuple[str, ...]
    blocking_difference: bool
    qadih_status: QadihSoundDifferenceStatus
    source_policy: str
    inventory_version: str
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(
            self.origin_sound_ref,
            "QadihSoundDifferenceProof.origin_sound_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.branch_sound_ref,
            "QadihSoundDifferenceProof.branch_sound_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.source_policy,
            "QadihSoundDifferenceProof.source_policy",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.inventory_version,
            "QadihSoundDifferenceProof.inventory_version",
            FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.shared_sifah_refs, tuple):
            raise WeightCarrierSchemaError(
                "QadihSoundDifferenceProof.shared_sifah_refs must be a tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.differentiating_sifah_refs, tuple):
            raise WeightCarrierSchemaError(
                "QadihSoundDifferenceProof.differentiating_sifah_refs must be a tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for ref in self.shared_sifah_refs + self.differentiating_sifah_refs:
            _require_non_empty(
                ref,
                "QadihSoundDifferenceProof.sifah reference",
                FailureCode.BOUNDARY_MISSING,
            )
        if not isinstance(self.blocking_difference, bool):
            raise WeightCarrierSchemaError(
                "QadihSoundDifferenceProof.blocking_difference must be bool "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.qadih_status, QadihSoundDifferenceStatus):
            raise WeightCarrierSchemaError(
                "QadihSoundDifferenceProof.qadih_status must be QadihSoundDifferenceStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "QadihSoundDifferenceProof.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class ArabicSoundInventoryEntry:
    """DAL-A3 inventory entry carrier."""

    sound_ref: str
    grapheme: str
    phonetic_label: str
    sound_kind: ArabicSoundInventoryKind
    makhraj_ref: str
    sifah_refs: tuple[str, ...]
    source_policy: str
    inventory_version: str
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(
            self.sound_ref,
            "ArabicSoundInventoryEntry.sound_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.grapheme,
            "ArabicSoundInventoryEntry.grapheme",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.phonetic_label,
            "ArabicSoundInventoryEntry.phonetic_label",
            FailureCode.IDENTITY_BROKEN,
        )
        if not isinstance(self.sound_kind, ArabicSoundInventoryKind):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryEntry.sound_kind must be ArabicSoundInventoryKind "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.source_policy,
            "ArabicSoundInventoryEntry.source_policy",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.inventory_version,
            "ArabicSoundInventoryEntry.inventory_version",
            FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.sifah_refs, tuple):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryEntry.sifah_refs must be a tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for ref in self.sifah_refs:
            _require_non_empty(
                ref,
                "ArabicSoundInventoryEntry.sifah_refs entry",
                FailureCode.BOUNDARY_MISSING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryEntry.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _require_non_empty(
            self.makhraj_ref,
            "ArabicSoundInventoryEntry.makhraj_ref",
            FailureCode.BOUNDARY_MISSING,
        )


@dataclass(frozen=True, slots=True)
class ArabicSoundInventoryDecision:
    """DAL-A3 decision surface."""

    sound_inventory_ready: bool
    readiness_state: ArabicSoundInventoryReadinessState
    failed_stage: ArabicSoundInventoryFailedStage | None
    local_failure_name: str | None
    residuals: tuple[str, ...]
    handoff: str
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.sound_inventory_ready, bool):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryDecision.sound_inventory_ready must be bool "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.readiness_state, ArabicSoundInventoryReadinessState):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryDecision.readiness_state must be "
                "ArabicSoundInventoryReadinessState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.failed_stage is not None and not isinstance(
            self.failed_stage, ArabicSoundInventoryFailedStage
        ):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryDecision.failed_stage must be ArabicSoundInventoryFailedStage "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.local_failure_name is not None:
            _require_non_empty(
                self.local_failure_name,
                "ArabicSoundInventoryDecision.local_failure_name",
                FailureCode.BOUNDARY_MISSING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryDecision.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _require_non_empty(
            self.handoff,
            "ArabicSoundInventoryDecision.handoff",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.trace_ref, "ArabicSoundInventoryDecision.trace_ref", FailureCode.TRACE_MISSING
        )


@dataclass(frozen=True, slots=True)
class SoundSimilarityIndicator:
    """Performance indicator only; never qiyās or hukm."""

    origin_sound_ref: str
    branch_sound_ref: str
    shared_sifah_refs: tuple[str, ...]
    indicator_only: Literal[True] = True
    residual_name: str = "SOUND_SIMILARITY_INDICATOR_ONLY"

    def __post_init__(self) -> None:
        _require_non_empty(
            self.origin_sound_ref,
            "SoundSimilarityIndicator.origin_sound_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.branch_sound_ref,
            "SoundSimilarityIndicator.branch_sound_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        if not isinstance(self.shared_sifah_refs, tuple):
            raise WeightCarrierSchemaError(
                "SoundSimilarityIndicator.shared_sifah_refs must be a tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for ref in self.shared_sifah_refs:
            _require_non_empty(
                ref,
                "SoundSimilarityIndicator.shared_sifah_refs entry",
                FailureCode.BOUNDARY_MISSING,
            )


@dataclass(frozen=True, slots=True)
class ArabicSoundInventoryCandidate:
    """DAL-A3 candidate output; inventory/proof only."""

    entry: ArabicSoundInventoryEntry
    makhraj_proof: MakhrajProof
    sifah_proof: SifahProof
    qadih_sound_difference_proof: QadihSoundDifferenceProof
    similarity_indicator: SoundSimilarityIndicator | None
    rank: Rank
    trace_ref: str
    residuals: tuple[str, ...] = ()
    forbidden_outputs: tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.entry, ArabicSoundInventoryEntry):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryCandidate.entry must be ArabicSoundInventoryEntry "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.makhraj_proof, MakhrajProof):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryCandidate.makhraj_proof must be MakhrajProof "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.sifah_proof, SifahProof):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryCandidate.sifah_proof must be SifahProof "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.qadih_sound_difference_proof, QadihSoundDifferenceProof):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryCandidate.qadih_sound_difference_proof must be "
                f"QadihSoundDifferenceProof ({FailureCode.GATE_REQUIRED.value})"
            )
        _validate_rank(self.rank, "ArabicSoundInventoryCandidate")
        _require_non_empty(
            self.trace_ref, "ArabicSoundInventoryCandidate.trace_ref", FailureCode.TRACE_MISSING
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryCandidate.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "ArabicSoundInventoryCandidate")


@dataclass(frozen=True, slots=True)
class ArabicSoundInventoryGateResult:
    """DAL-A3 gate result wrapper."""

    decision: ArabicSoundInventoryDecision
    candidate: ArabicSoundInventoryCandidate | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.decision, ArabicSoundInventoryDecision):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryGateResult.decision must be ArabicSoundInventoryDecision "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "ArabicSoundInventoryGateResult.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


_FORBIDDEN_HANDOFF_ALIASES: dict[str, str] = {
    "SYLLABLE_CANDIDATE": "SyllableLicenseGate",
    "مقطع": "SyllableLicenseGate",
    "ROOT": "RootIdentityGate",
    "جذر": "RootIdentityGate",
    "WEIGHT": "WeightPathSelectionGate",
    "وزن": "WeightPathSelectionGate",
    "MEANING": "MeaningGate",
    "SEMANTIC": "MeaningGate",
    "معنى": "MeaningGate",
    "IFADAH": "IfadahGate",
    "إفادة": "IfadahGate",
    "MAFHUM": "MafhumGate",
    "مفهوم": "MafhumGate",
    "HUKM": "HukmGate",
    "حكم": "HukmGate",
    "TRUTH": "Truth",
    "حقيقة": "Truth",
    "REALITY": "Reality",
    "واقع": "Reality",
}


def _canonical_handoff(handoff: str) -> str:
    stripped = handoff.strip()
    return _FORBIDDEN_HANDOFF_ALIASES.get(stripped, stripped)


def evaluate_arabic_sound_inventory_gate(
    *,
    entry: ArabicSoundInventoryEntry,
    makhraj_proof: MakhrajProof | None,
    sifah_proof: SifahProof | None,
    qadih_sound_difference_proof: QadihSoundDifferenceProof | None,
    comparison_requested: bool,
    handoff: str,
    trace_ref: str,
) -> ArabicSoundInventoryGateResult:
    """Evaluate DAL-A3 readiness from inventory + explicit makhraj/sifah/qadih proofs."""

    if not isinstance(entry, ArabicSoundInventoryEntry):
        raise WeightCarrierSchemaError(
            "evaluate_arabic_sound_inventory_gate.entry must be ArabicSoundInventoryEntry "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "evaluate_arabic_sound_inventory_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        handoff,
        "evaluate_arabic_sound_inventory_gate.handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(comparison_requested, bool):
        raise WeightCarrierSchemaError(
            "evaluate_arabic_sound_inventory_gate.comparison_requested must be bool "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    residuals = _merge_residuals(entry.residuals)

    if entry.sound_kind is ArabicSoundInventoryKind.DIACRITIC_OR_MARKER:
        residuals = _merge_residuals(residuals, ("DEFERRED_TO_DAL_A4",))
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.DEFERRED,
            failed_stage=ArabicSoundInventoryFailedStage.INVENTORY,
            local_failure_name="DEFERRED_TO_DAL_A4",
            residuals=residuals,
            handoff=_canonical_handoff(handoff),
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=None,
        )

    if makhraj_proof is None:
        residuals = _merge_residuals(residuals, ("MAKHRAJ_MISSING",))
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.DEFERRED,
            failed_stage=ArabicSoundInventoryFailedStage.MAKHRAJ,
            local_failure_name="MAKHRAJ_MISSING",
            residuals=residuals,
            handoff=_canonical_handoff(handoff),
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=None,
        )
    if makhraj_proof.sound_ref != entry.sound_ref:
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.BLOCKED,
            failed_stage=ArabicSoundInventoryFailedStage.MAKHRAJ,
            local_failure_name="MAKHRAJ_PROOF_SOUND_REF_MISMATCH",
            residuals=_merge_residuals(residuals, ("MAKHRAJ_MISSING",)),
            handoff=_canonical_handoff(handoff),
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=FailureCode.IDENTITY_BROKEN,
        )
    residuals = _remove_residual(residuals, "MAKHRAJ_MISSING")

    if sifah_proof is None:
        residuals = _merge_residuals(residuals, ("SIFAH_MISSING",))
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.DEFERRED,
            failed_stage=ArabicSoundInventoryFailedStage.SIFAH,
            local_failure_name="SIFAH_MISSING",
            residuals=residuals,
            handoff=_canonical_handoff(handoff),
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=None,
        )
    if sifah_proof.sound_ref != entry.sound_ref:
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.BLOCKED,
            failed_stage=ArabicSoundInventoryFailedStage.SIFAH,
            local_failure_name="SIFAH_PROOF_SOUND_REF_MISMATCH",
            residuals=_merge_residuals(residuals, ("SIFAH_MISSING",)),
            handoff=_canonical_handoff(handoff),
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=FailureCode.IDENTITY_BROKEN,
        )
    residuals = _remove_residual(residuals, "SIFAH_MISSING")

    similarity_indicator: SoundSimilarityIndicator | None = None
    if qadih_sound_difference_proof is not None:
        if qadih_sound_difference_proof.origin_sound_ref != entry.sound_ref:
            decision = ArabicSoundInventoryDecision(
                sound_inventory_ready=False,
                readiness_state=ArabicSoundInventoryReadinessState.BLOCKED,
                failed_stage=ArabicSoundInventoryFailedStage.QADIH,
                local_failure_name="QADIH_PROOF_SOUND_REF_MISMATCH",
                residuals=_merge_residuals(residuals, ("QADIH_SOUND_DIFF_MISSING",)),
                handoff=_canonical_handoff(handoff),
                trace_ref=trace_ref,
            )
            return ArabicSoundInventoryGateResult(
                decision=decision,
                candidate=None,
                failure_code=FailureCode.IDENTITY_BROKEN,
            )
        if qadih_sound_difference_proof.qadih_status is QadihSoundDifferenceStatus.BLOCKING:
            decision = ArabicSoundInventoryDecision(
                sound_inventory_ready=False,
                readiness_state=ArabicSoundInventoryReadinessState.BLOCKED,
                failed_stage=ArabicSoundInventoryFailedStage.QADIH,
                local_failure_name="QADIH_BLOCKING_DIFFERENCE",
                residuals=_merge_residuals(residuals, ("QADIH_SOUND_DIFF_MISSING",)),
                handoff=_canonical_handoff(handoff),
                trace_ref=trace_ref,
            )
            return ArabicSoundInventoryGateResult(
                decision=decision,
                candidate=None,
                failure_code=FailureCode.BOUNDARY_MISSING,
            )
        if qadih_sound_difference_proof.qadih_status in (
            QadihSoundDifferenceStatus.RESIDUAL,
            QadihSoundDifferenceStatus.UNCHECKED,
        ):
            residuals = _merge_residuals(residuals, ("QADIH_SOUND_DIFF_MISSING",))
            decision = ArabicSoundInventoryDecision(
                sound_inventory_ready=False,
                readiness_state=ArabicSoundInventoryReadinessState.DEFERRED,
                failed_stage=ArabicSoundInventoryFailedStage.QADIH,
                local_failure_name="QADIH_SOUND_DIFF_MISSING",
                residuals=residuals,
                handoff=_canonical_handoff(handoff),
                trace_ref=trace_ref,
            )
            return ArabicSoundInventoryGateResult(
                decision=decision,
                candidate=None,
                failure_code=None,
            )

        residuals = _remove_residual(residuals, "QADIH_SOUND_DIFF_MISSING")
        if qadih_sound_difference_proof.shared_sifah_refs:
            residuals = _merge_residuals(residuals, ("SOUND_SIMILARITY_INDICATOR_ONLY",))
            similarity_indicator = SoundSimilarityIndicator(
                origin_sound_ref=qadih_sound_difference_proof.origin_sound_ref,
                branch_sound_ref=qadih_sound_difference_proof.branch_sound_ref,
                shared_sifah_refs=qadih_sound_difference_proof.shared_sifah_refs,
            )

    canonical_handoff = _canonical_handoff(handoff)
    if canonical_handoff in DAL_A3_FORBIDDEN_OUTPUTS:
        residuals = _merge_residuals(residuals, ("FORBIDDEN_DAL_A3_HANDOFF",))
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.REFUSED,
            failed_stage=ArabicSoundInventoryFailedStage.HANDOFF,
            local_failure_name=f"FORBIDDEN_DAL_A3_HANDOFF:{canonical_handoff}",
            residuals=residuals,
            handoff=canonical_handoff,
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    # Definitive DAL-A3 guard: candidate emission is forbidden without explicit
    # qādih proof, even when handoff is otherwise safe.
    if qadih_sound_difference_proof is None:
        residuals = _merge_residuals(residuals, ("QADIH_SOUND_DIFF_MISSING",))
        decision = ArabicSoundInventoryDecision(
            sound_inventory_ready=False,
            readiness_state=ArabicSoundInventoryReadinessState.DEFERRED,
            failed_stage=ArabicSoundInventoryFailedStage.QADIH,
            local_failure_name="QADIH_SOUND_DIFF_MISSING",
            residuals=residuals,
            handoff=canonical_handoff,
            trace_ref=trace_ref,
        )
        return ArabicSoundInventoryGateResult(
            decision=decision,
            candidate=None,
            failure_code=None,
        )

    candidate = ArabicSoundInventoryCandidate(
        entry=entry,
        makhraj_proof=makhraj_proof,
        sifah_proof=sifah_proof,
        qadih_sound_difference_proof=qadih_sound_difference_proof,
        similarity_indicator=similarity_indicator,
        rank=Rank.CANDIDATE,
        trace_ref=f"{trace_ref}/candidate",
        residuals=residuals,
    )
    decision = ArabicSoundInventoryDecision(
        sound_inventory_ready=True,
        readiness_state=ArabicSoundInventoryReadinessState.LINK_READY,
        failed_stage=None,
        local_failure_name=None,
        residuals=residuals,
        handoff=canonical_handoff,
        trace_ref=trace_ref,
    )
    return ArabicSoundInventoryGateResult(decision=decision, candidate=candidate, failure_code=None)


__all__ = [
    "DAL_A3_ALLOWED_OUTPUT",
    "DAL_A3_FORBIDDEN_OUTPUTS",
    "DAL_A3_GATE_ORDER",
    "DAL_A3_RANK_CEILING",
    "DAL_A3_RESIDUAL_VOCABULARY",
    "ArabicSoundInventoryCandidate",
    "ArabicSoundInventoryDecision",
    "ArabicSoundInventoryEntry",
    "ArabicSoundInventoryFailedStage",
    "ArabicSoundInventoryGateResult",
    "ArabicSoundInventoryKind",
    "ArabicSoundInventoryReadinessState",
    "MakhrajProof",
    "QadihSoundDifferenceProof",
    "QadihSoundDifferenceStatus",
    "SifahProof",
    "SoundSimilarityIndicator",
    "evaluate_arabic_sound_inventory_gate",
]
