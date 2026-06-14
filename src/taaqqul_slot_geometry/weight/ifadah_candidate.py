"""IfādahCandidate — PR-20.

PR-20 binding of ``docs/41_IFADAH_BOUNDARY_LAW.md`` and
``docs/42_SPEECH_FORCE_FORMAL_STYLE_BRIDGE_LAW.md``.

This module proves that a closed relation between two mufrad-dalalah-closed
units, under a proven formal style, a licensed speech-force kind, and a single
shared maqam verdict, carries a **speech-level closure candidate** (ifadah
candidate). It does not determine truth, hukm, application, or meaning.

PR-20 consumes:
1. A PROVEN RelationClosureVerdict.
2. A PROVEN FormalStyleVerdict.
3. A PROVEN MaqamContextBoundaryVerdict (single shared maqam).
4. A SpeechForceKind (KHABAR or INSHA — supplied, not derived).
5. ifadah_evidence (non-empty).
6. closure_scope (non-empty).

Constitutional invariants (docs/41 §8):

* IfadahCandidate ≠ Meaning.
* IfadahCandidate ≠ FinalMeaning.
* IfadahCandidate ≠ Hukm.
* IfadahCandidate ≠ Manat.
* IfadahCandidate ≠ Tanzil.
* IfadahCandidate ≠ PropositionTruthValue.
* IfadahCandidate ≠ SpeakerIntentVerdict.
* IfadahCandidate ≠ MafhumCandidate / MantuqClosure.
* IfadahCandidate ≠ MajazVerdict / HaqiqahAttemptVerdict.
* IfadahCandidate ≠ OntologicalClaim.
* IfadahCandidate ≠ FreeReasoning.
* No ifadah closure without three PROVEN input verdicts.
* No ifadah closure without a licensed SpeechForceKind.
* No ifadah closure without a single shared maqam verdict.
* No ifadah closure with hidden or blocking residuals.
* No rank promotion beyond IFADAH_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network, no clock.

Deferred residuals (docs/41 §10, docs/42 §9):

* IFADAH_NOT_PROPOSITION — ifadah is candidate-shape, not truth-valued.
* HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW — awaits docs/43.
* MANAT_DEFERRED_UNTIL_MANAT_LAW — awaits docs/44.
* TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW — awaits docs/45.
* MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL — awaits docs/46.
* MAJAZ_HAQIQAH_DEFERRED_POST_VERTICAL — awaits docs/46.
* EXTRA_SPEECH_FORCE_DEFERRED — AMR/NAHY/etc. never enum members.
* SPEAKER_INTENT_DEFERRED — speaker intent is not ifadah.
* AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT — AnswerAudit ships later.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FormalStyleCandidate,
    FormalStyleFamily,
    FormalStyleState,
    FormalStyleVerdict,
)
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    MaqamContextBoundaryVerdict,
    MaqamContextState,
)
from taaqqul_slot_geometry.weight.relation_closure import (
    RELATION_CLOSURE_RANK_CEILING,
    RelationClosureCandidate,
    RelationClosureState,
    RelationClosureVerdict,
)

__all__ = [
    "IFADAH_RANK_CEILING",
    "IfadahCandidate",
    "IfadahState",
    "IfadahVerdict",
    "SpeechForceKind",
    "prove_ifadah_candidate",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from relation closure layer
# ---------------------------------------------------------------------------

IFADAH_RANK_CEILING: Rank = RELATION_CLOSURE_RANK_CEILING

# ---------------------------------------------------------------------------
# SpeechForceKind — minimal set (docs/41 §2, docs/42 §3)
# ---------------------------------------------------------------------------


class SpeechForceKind(StrEnum):
    """Minimal speech-force kind set for PR-20.

    Only KHABAR and INSHA are licensed members. All other speech-force
    categories (AMR, NAHY, ISTIFHAM, NIDA, DUA, TAMANNI, TARAJJI,
    TAHDID, TAAJJUB, QASAM) are deferred residuals only — never enum
    members in PR-20.

    SpeechForceKind is supplied by the caller and validated by the bridge.
    It is never derived from form alone, maqam alone, or relation alone.
    """

    KHABAR = "KHABAR"
    INSHA = "INSHA"


# ---------------------------------------------------------------------------
# IfadahState — verdict outcome
# ---------------------------------------------------------------------------


class IfadahState(StrEnum):
    """The outcome of a prove_ifadah_candidate() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# IfadahCandidate — the speech-level closure carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IfadahCandidate:
    """Speech-level closure candidate (docs/41 §1, docs/42 §8).

    Proves that a closed relation between two mufrad-dalalah-closed units
    carries a speech-level closure inside a single bounded maqam, with a
    compatible formal style and speech force.

    IfadahCandidate ≠ Meaning.
    IfadahCandidate ≠ Hukm.
    IfadahCandidate ≠ PropositionTruthValue.
    """

    relation_closure_ref: str
    formal_style_ref: str
    maqam_verdict_ref: str
    speech_force: SpeechForceKind
    first_dal_identity_ref: str
    second_dal_identity_ref: str
    ifadah_evidence: str
    closure_scope: str
    bridge_compatible: bool
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.relation_closure_ref, str)
            or not self.relation_closure_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "relation_closure_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.formal_style_ref, str)
            or not self.formal_style_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "formal_style_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.maqam_verdict_ref, str)
            or not self.maqam_verdict_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "maqam_verdict_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.speech_force, SpeechForceKind):
            raise WeightCarrierSchemaError(
                f"speech_force must be a SpeechForceKind member, "
                f"got {type(self.speech_force).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.first_dal_identity_ref, str)
            or not self.first_dal_identity_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "first_dal_identity_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.second_dal_identity_ref, str)
            or not self.second_dal_identity_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "second_dal_identity_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.ifadah_evidence, str)
            or not self.ifadah_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "ifadah_evidence must be a non-empty string",
                FailureCode.NO_IFADAH_EVIDENCE,
            )
        if (
            not isinstance(self.closure_scope, str)
            or not self.closure_scope.strip()
        ):
            raise WeightCarrierSchemaError(
                "closure_scope must be a non-empty string",
                FailureCode.NO_IFADAH_SCOPE,
            )
        if not isinstance(self.bridge_compatible, bool):
            raise WeightCarrierSchemaError(
                "bridge_compatible must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if self.bridge_compatible is not True:
            raise WeightCarrierSchemaError(
                "bridge_compatible must be True on a constructed candidate",
                FailureCode.FORMAL_STYLE_CONFLICT,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > IFADAH_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{IFADAH_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"each residual must be a Residual instance, "
                    f"got {type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# IfadahVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IfadahVerdict:
    """Verdict from prove_ifadah_candidate() (docs/41 §6).

    PROVEN carries an IfadahCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: IfadahCandidate | None
    verdict_state: IfadahState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder (docs/41 §10, docs/42 §9)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 9 required deferred residuals for IfadahCandidate."""
    names_and_notes = (
        (
            "IFADAH_NOT_PROPOSITION",
            "Ifadah is candidate-shape, not truth-valued. "
            "It does not determine truth, hukm, or application.",
        ),
        (
            "HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW",
            "Hukm (judgment) awaits docs/43 (PR-D7). "
            "No judgment before its domain boundary.",
        ),
        (
            "MANAT_DEFERRED_UNTIL_MANAT_LAW",
            "Manat (effective cause identification) awaits docs/44 (PR-D8). "
            "No manat before its boundary law.",
        ),
        (
            "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
            "Tanzil (application/presentation) awaits docs/45 (PR-D9). "
            "No application before its presentation boundary.",
        ),
        (
            "MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL",
            "Mafhum/mantuq operations await docs/46 (PR-D10) "
            "horizontal-branch licence. Forbidden before vertical closure.",
        ),
        (
            "MAJAZ_HAQIQAH_DEFERRED_POST_VERTICAL",
            "Majaz/haqiqah determination awaits docs/46 (PR-D10) "
            "horizontal-branch licence. Forbidden before vertical closure.",
        ),
        (
            "EXTRA_SPEECH_FORCE_DEFERRED",
            "AMR, NAHY, ISTIFHAM, NIDA, DUA, TAMANNI, TARAJJI, "
            "TAHDID, TAAJJUB, QASAM are deferred. "
            "Never enum members in PR-20.",
        ),
        (
            "SPEAKER_INTENT_DEFERRED",
            "Speaker intent is not ifadah. Intent determination "
            "requires a separate chain step beyond PR-20.",
        ),
        (
            "AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT",
            "AnswerAudit bridge ships in PR-22-AUDIT. "
            "IfadahCandidate does not directly enter AnswerAudit yet.",
        ),
    )
    return tuple(
        Residual(
            name=name,
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=note,
        )
        for name, note in names_and_notes
    )


# ---------------------------------------------------------------------------
# Bridge compatibility check (docs/42 §6 — explicit, never silent)
# ---------------------------------------------------------------------------

#: Formal style families compatible with KHABAR (docs/42 §6).
_KHABAR_COMPATIBLE_FAMILIES: frozenset[FormalStyleFamily] = frozenset({
    FormalStyleFamily.DECLARATIVE_STYLE_FORM,
})

#: Formal style families compatible with INSHA (docs/42 §6).
_INSHA_COMPATIBLE_FAMILIES: frozenset[FormalStyleFamily] = frozenset({
    FormalStyleFamily.COMMAND_STYLE_FORM,
    FormalStyleFamily.PROHIBITION_STYLE_FORM,
    FormalStyleFamily.INTERROGATIVE_STYLE_FORM,
    FormalStyleFamily.VOCATIVE_STYLE_FORM,
    FormalStyleFamily.WISH_STYLE_FORM,
    FormalStyleFamily.HOPE_STYLE_FORM,
    FormalStyleFamily.OATH_STYLE_FORM,
    FormalStyleFamily.CONDITION_STYLE_FORM,
    FormalStyleFamily.EXCLAMATION_STYLE_FORM,
})


def _check_bridge_compatibility(
    style_family: FormalStyleFamily,
    speech_force: SpeechForceKind,
) -> bool:
    """Check FormalStyle ↔ SpeechForce compatibility (docs/42 §6).

    Returns True if the pair is compatible, False otherwise.
    This is an explicit named-branch check, never a silent dispatch table.
    """
    if speech_force is SpeechForceKind.KHABAR:
        return style_family in _KHABAR_COMPATIBLE_FAMILIES
    if speech_force is SpeechForceKind.INSHA:
        return style_family in _INSHA_COMPATIBLE_FAMILIES
    # Unreachable if SpeechForceKind is validated; defensive refusal.
    return False


# ---------------------------------------------------------------------------
# prove_ifadah_candidate — the pure operation
# ---------------------------------------------------------------------------


def prove_ifadah_candidate(
    relation_closure_verdict: RelationClosureVerdict,
    formal_style_verdict: FormalStyleVerdict,
    ifadah_maqam_verdict: MaqamContextBoundaryVerdict,
    speech_force: SpeechForceKind,
    ifadah_evidence: str,
    closure_scope: str,
) -> IfadahVerdict:
    """Prove ifadah (speech-level closure) candidate.

    Parameters
    ----------
    relation_closure_verdict
        PROVEN RelationClosureVerdict (PR-D4).
    formal_style_verdict
        PROVEN FormalStyleVerdict (PR-F8).
    ifadah_maqam_verdict
        PROVEN MaqamContextBoundaryVerdict (PR-D1.2). Must be the
        single shared maqam verdict across all input layers.
    speech_force
        SpeechForceKind (KHABAR or INSHA). Supplied by caller,
        never derived from form, maqam, or relation alone.
    ifadah_evidence
        Non-empty evidence string supporting the ifadah closure.
    closure_scope
        Non-empty scope bounding the closure.

    Returns
    -------
    IfadahVerdict
        PROVEN with an IfadahCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_ifadah_candidate"

    # --- Input boundary: relation_closure_verdict type ---
    if not isinstance(relation_closure_verdict, RelationClosureVerdict):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_RELATION_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_closure_invalid_type",
        )

    # --- Input boundary: relation closure must be PROVEN ---
    if relation_closure_verdict.verdict_state is not RelationClosureState.PROVEN:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_RELATION_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_closure_not_proven",
        )

    # --- Input boundary: relation closure candidate present ---
    if not isinstance(
        relation_closure_verdict.candidate, RelationClosureCandidate
    ):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_RELATION_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_closure_candidate_invalid",
        )

    # --- Input boundary: formal_style_verdict type ---
    if not isinstance(formal_style_verdict, FormalStyleVerdict):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_FORMAL_STYLE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/formal_style_invalid_type",
        )

    # --- Input boundary: formal style must be PROVEN ---
    if formal_style_verdict.verdict_state is not FormalStyleState.PROVEN:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_FORMAL_STYLE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/formal_style_not_proven",
        )

    # --- Input boundary: formal style candidate present ---
    if not isinstance(formal_style_verdict.candidate, FormalStyleCandidate):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_FORMAL_STYLE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/formal_style_candidate_invalid",
        )

    # --- Input boundary: speech_force type ---
    if not isinstance(speech_force, SpeechForceKind):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_SPEECH_FORCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/speech_force_invalid_type",
        )

    # --- Input boundary: ifadah_maqam_verdict type ---
    if not isinstance(ifadah_maqam_verdict, MaqamContextBoundaryVerdict):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_MAQAM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_maqam_invalid_type",
        )

    # --- Input boundary: maqam must be PROVEN ---
    if ifadah_maqam_verdict.verdict_state is not MaqamContextState.PROVEN:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_MAQAM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_maqam_not_proven",
        )

    # --- Input boundary: ifadah_evidence ---
    if not isinstance(ifadah_evidence, str) or not ifadah_evidence.strip():
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_EVIDENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_evidence_empty",
        )

    # --- Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_SCOPE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- Maqam divergence check (docs/41 §6): single shared maqam ---
    # The relation closure was produced under a maqam (relation_maqam).
    # The ifadah_maqam_verdict must share the same trace origin.
    rc_candidate: RelationClosureCandidate = relation_closure_verdict.candidate
    if rc_candidate.relation_maqam != ifadah_maqam_verdict.trace_ref:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.MAQAM_DIVERGENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_divergence",
        )

    # --- Bridge compatibility check (docs/42 §6) ---
    style_family: FormalStyleFamily = (
        formal_style_verdict.candidate.style_family
    )
    bridge_ok = _check_bridge_compatibility(style_family, speech_force)
    if not bridge_ok:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.FORMAL_STYLE_CONFLICT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/formal_style_conflict",
        )

    # --- Identity continuity: two distinct dal identities ---
    # RelationClosure already enforces this, but re-check defensively here
    # to guard against malformed RelationClosureCandidate instances.
    if (
        rc_candidate.first_dal_identity_ref
        == rc_candidate.second_dal_identity_ref
    ):
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/identity_broken_same_unit",
        )

    # --- Compute rank (meet of all input ranks with ceiling) ---
    verdict_rank = RankLattice.meet(
        relation_closure_verdict.verdict_rank,
        formal_style_verdict.verdict_rank,
        ifadah_maqam_verdict.verdict_rank,
        IFADAH_RANK_CEILING,
    )

    # --- Check rank ceiling ---
    if verdict_rank > IFADAH_RANK_CEILING:
        return IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- Check residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return IfadahVerdict(
                candidate=None,
                verdict_state=IfadahState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return IfadahVerdict(
                candidate=None,
                verdict_state=IfadahState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Check input verdict residuals for hidden/blocking ---
    for input_residuals in (
        relation_closure_verdict.residuals,
        formal_style_verdict.residuals,
        ifadah_maqam_verdict.residuals,
    ):
        for r in input_residuals:
            if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
                return IfadahVerdict(
                    candidate=None,
                    verdict_state=IfadahState.REFUSED,
                    failure_code=FailureCode.HIDDEN_RESIDUAL,
                    verdict_rank=Rank.ZERO,
                    residuals=deferred_residuals,
                    trace_ref=(
                        f"{_trace_base}/refused/input_hidden_residual"
                    ),
                )
            if r.kind is ResidualKind.BLOCKING:
                return IfadahVerdict(
                    candidate=None,
                    verdict_state=IfadahState.REFUSED,
                    failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                    verdict_rank=Rank.ZERO,
                    residuals=deferred_residuals,
                    trace_ref=(
                        f"{_trace_base}/refused/input_blocking_residual"
                    ),
                )

    # --- Construct IfadahCandidate ---
    candidate = IfadahCandidate(
        relation_closure_ref=rc_candidate.trace_ref,
        formal_style_ref=formal_style_verdict.trace_ref,
        maqam_verdict_ref=ifadah_maqam_verdict.trace_ref,
        speech_force=speech_force,
        first_dal_identity_ref=rc_candidate.first_dal_identity_ref,
        second_dal_identity_ref=rc_candidate.second_dal_identity_ref,
        ifadah_evidence=ifadah_evidence,
        closure_scope=closure_scope,
        bridge_compatible=True,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return IfadahVerdict(
        candidate=candidate,
        verdict_state=IfadahState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
