"""Pre-weight chain operations + Ω residual governance — PR-12.

PR-12 binding of ``docs/20_PRE_WEIGHT_LICENSING_LAW.md`` §§4–11 and
``docs/23_PRE_WEIGHT_CHAIN_OPERATIONS_LAW.md``. This module introduces:

* :class:`OmegaGovernanceState` — the four Ω verdict states.
* :class:`ResidualGovernanceVerdict` — the pure value returned by Ω.
* :func:`omega_governance` — the Ω pure function: classifies residuals
  on a pre-weight surface and decides transition authority.
* The seven μ operations: :func:`mu_seq`, :func:`mu_boundary`,
  :func:`mu_word_carrier`, :func:`mu_root_stem`,
  :func:`mu_original_extra`, :func:`mu_ops`, :func:`mu_weight_readiness`.
* :class:`MuStepResult` — the bounded candidate or named refusal
  returned by every μ step.

Constitutional invariants (docs/23):

* PR-11 sees and carries; PR-12 judges and governs.
* VisibleResidual is audit visibility; ΩResidualGovernance is transition
  authority.
* Every μ step accepts only the previous licensed output.
* Every refusal is a named FailureCode — never silent None.
* No μ step promotes rank beyond the ceiling.
* No weigh(), no WeightFitCandidate, no meaning, no lexicon.
* Ω and μ are pure: no I/O, no ledger, no network.

This module adds **no new FailureCode members** and **no new runtime
dependencies**. Every refusal maps onto the codes ratified in PR-1A.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import (
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.path_gate import (
    PATH_GATE_RANK_CEILING,
    PathGateState,
    PathGateVerdict,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
    PathKind,
    PreWeightSurface,
    RootStemCandidate,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)

# ---------------------------------------------------------------------------
# Ω Residual Governance
# ---------------------------------------------------------------------------

#: The μ chain rank ceiling — the same as PATH_GATE_RANK_CEILING.
#: No μ step may emit a rank above this value.
MU_CHAIN_RANK_CEILING: Rank = PATH_GATE_RANK_CEILING


class OmegaGovernanceState(StrEnum):
    """The four governance verdicts of the Ω residual judgment (docs/23 §2.2)."""

    GRANTED = "GRANTED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class ResidualGovernanceVerdict:
    """The pure value returned by :func:`omega_governance`.

    Invariants (enforced at birth — docs/23 §2.3):

    * ``state`` is ``GRANTED`` **iff** ``failure_code`` is ``None``.
    * ``REJECTED``/``BLOCKED`` always carry a named FailureCode.
    * ``DEFERRED`` carries a named FailureCode.
    * ``residuals`` are the full residual surface evaluated — always visible.
    * ``granted_rank`` is Rank.ZERO for non-GRANTED states.
    """

    state: OmegaGovernanceState
    failure_code: FailureCode | None
    residuals: tuple[Residual, ...]
    granted_rank: Rank

    def __post_init__(self) -> None:
        if not isinstance(self.state, OmegaGovernanceState):
            raise WeightCarrierSchemaError(
                "ResidualGovernanceVerdict.state must be an OmegaGovernanceState member"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ResidualGovernanceVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "ResidualGovernanceVerdict.residuals entries must be Residual carriers"
                )
        if not isinstance(self.granted_rank, Rank):
            raise WeightCarrierSchemaError(
                "ResidualGovernanceVerdict.granted_rank must be a Rank member"
            )

        if self.state is OmegaGovernanceState.GRANTED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a GRANTED ResidualGovernanceVerdict must not carry a FailureCode "
                    "(docs/23 §2.2 — no failure on granted transition)"
                )
        else:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a non-GRANTED ResidualGovernanceVerdict must carry a named "
                    "FailureCode (docs/23 §2.2)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "ResidualGovernanceVerdict.failure_code must be a FailureCode member"
                )
            if self.granted_rank is not Rank.ZERO:
                raise WeightCarrierSchemaError(
                    "a non-GRANTED ResidualGovernanceVerdict licenses nothing: "
                    "granted_rank must be Rank.ZERO"
                )


def omega_governance(
    residuals: tuple[Residual, ...],
    surface_rank: Rank,
) -> ResidualGovernanceVerdict:
    """Ω residual governance — the pre-weight transition authority.

    A pure function: classifies the residuals on a pre-weight surface
    and returns a :class:`ResidualGovernanceVerdict`.

    Decision order (mirrors docs/06 / Γ ordering):

    1. HIDDEN_FORBIDDEN → REJECTED (cannot pass silently).
    2. BLOCKING → BLOCKED (prevents transition).
    3. DEFERRABLE → DEFERRED (constrains but does not block).
    4. Otherwise → GRANTED (NON_BLOCKING and EXPLANATORY pass visibly).

    Rank is bounded: the granted rank is the meet of `surface_rank`
    and `MU_CHAIN_RANK_CEILING`, never a promotion.
    """
    if not isinstance(residuals, tuple):
        raise TypeError("omega_governance() requires a tuple of Residual carriers")
    if not isinstance(surface_rank, Rank):
        raise TypeError("omega_governance() requires a Rank for surface_rank")

    # Step 1 — HIDDEN_FORBIDDEN: any hidden or invisible residual rejects
    for r in residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN or not r.visible:
            return ResidualGovernanceVerdict(
                state=OmegaGovernanceState.REJECTED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                residuals=residuals,
                granted_rank=Rank.ZERO,
            )

    # Step 2 — BLOCKING: any blocking residual blocks
    for r in residuals:
        if r.kind is ResidualKind.BLOCKING:
            return ResidualGovernanceVerdict(
                state=OmegaGovernanceState.BLOCKED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                residuals=residuals,
                granted_rank=Rank.ZERO,
            )

    # Step 3 — DEFERRABLE: any deferrable residual defers
    for r in residuals:
        if r.kind is ResidualKind.DEFERRABLE:
            return ResidualGovernanceVerdict(
                state=OmegaGovernanceState.DEFERRED,
                failure_code=FailureCode.GATE_REQUIRED,
                residuals=residuals,
                granted_rank=Rank.ZERO,
            )

    # Step 4 — GRANTED: only NON_BLOCKING and EXPLANATORY remain
    granted_rank = RankLattice.meet(surface_rank, MU_CHAIN_RANK_CEILING)
    return ResidualGovernanceVerdict(
        state=OmegaGovernanceState.GRANTED,
        failure_code=None,
        residuals=residuals,
        granted_rank=granted_rank,
    )


# ---------------------------------------------------------------------------
# μ Chain Operations — the MuStepResult carrier
# ---------------------------------------------------------------------------


class MuStepState(StrEnum):
    """The outcome of a μ step (docs/23 §3.1)."""

    LICENSED = "LICENSED"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True, slots=True)
class MuStepResult:
    """The bounded candidate or named refusal returned by every μ step.

    Invariants:

    * ``state`` is ``LICENSED`` **iff** ``failure_code`` is ``None`` and
      ``output`` is not ``None``.
    * A refusal carries a named FailureCode and no output.
    * A deferred result carries a named FailureCode and may carry output.
    * ``step_name`` identifies which μ step produced this result.
    * ``residuals`` are always visible.
    * ``rank`` never exceeds MU_CHAIN_RANK_CEILING.
    """

    state: MuStepState
    step_name: str
    failure_code: FailureCode | None
    output: object | None
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, MuStepState):
            raise WeightCarrierSchemaError(
                "MuStepResult.state must be a MuStepState member"
            )
        if not isinstance(self.step_name, str) or not self.step_name.strip():
            raise WeightCarrierSchemaError(
                "MuStepResult.step_name must be a non-empty string"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "MuStepResult.rank must be a Rank member"
            )
        if self.rank > MU_CHAIN_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "MuStepResult.rank must not exceed MU_CHAIN_RANK_CEILING "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "MuStepResult.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "MuStepResult.residuals entries must be Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "MuStepResult.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        if self.state is MuStepState.LICENSED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a LICENSED MuStepResult must not carry a FailureCode"
                )
            if self.output is None:
                raise WeightCarrierSchemaError(
                    "a LICENSED MuStepResult must carry an output"
                )
        elif self.state is MuStepState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED MuStepResult must carry a named FailureCode"
                )
            if self.output is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED MuStepResult must not carry an output"
                )
        else:  # DEFERRED
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED MuStepResult must carry a named FailureCode"
                )


# ---------------------------------------------------------------------------
# μ Chain Operations — the seven steps
# ---------------------------------------------------------------------------


def mu_seq(
    syllables: tuple[SyllableCandidate, ...],
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_seq: licensed syllables → SyllableSequenceCandidate (docs/20 §4).

    Accepts only licensed SyllableCandidate carriers. Applies Ω governance
    before transition. Returns a bounded candidate or named refusal.
    """
    if not isinstance(syllables, tuple) or len(syllables) == 0:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_seq",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_seq/refused/empty_input",
        )

    for s in syllables:
        if not isinstance(s, SyllableCandidate):
            return MuStepResult(
                state=MuStepState.REFUSED,
                step_name="mu_seq",
                failure_code=FailureCode.GATE_REQUIRED,
                output=None,
                rank=Rank.ZERO,
                residuals=(),
                trace_ref="mu_seq/refused/unlicensed_input",
            )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_seq",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_seq/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_seq",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_seq/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_seq",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_seq/deferred/omega_deferred",
        )

    # GRANTED — produce the sequence
    first = syllables[0]
    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_seq",
        failure_code=None,
        output=SyllableSequenceCandidate(
            value=first.value,
            type="syllable_sequence",
            origin=first.origin,
            identity=f"seq-{first.identity}",
            domain=first.domain,
            scope=first.scope,
            rank=RankLattice.meet(first.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=first.trace,
            syllables=syllables,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_seq/licensed",
    )


def mu_boundary(
    sequence: SyllableSequenceCandidate,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_boundary: SyllableSequenceCandidate → WordBoundaryCandidate (docs/20 §5).

    Accepts only a licensed SyllableSequenceCandidate.
    """
    if not isinstance(sequence, SyllableSequenceCandidate):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_boundary",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_boundary/refused/unlicensed_input",
        )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_boundary",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_boundary/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_boundary",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_boundary/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_boundary",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_boundary/deferred/omega_deferred",
        )

    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_boundary",
        failure_code=None,
        output=WordBoundaryCandidate(
            value=sequence.value,
            type="word_boundary",
            origin=sequence.origin,
            identity=f"wb-{sequence.identity}",
            domain=sequence.domain,
            scope=sequence.scope,
            rank=RankLattice.meet(sequence.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=sequence.trace,
            sequence=sequence,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_boundary/licensed",
    )


def mu_word_carrier(
    boundary: WordBoundaryCandidate,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_word_carrier: WordBoundaryCandidate → WordCarrierCandidate (docs/20 §6).

    Accepts only a licensed WordBoundaryCandidate.
    """
    if not isinstance(boundary, WordBoundaryCandidate):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_word_carrier",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_word_carrier/refused/unlicensed_input",
        )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_word_carrier",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_word_carrier/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_word_carrier",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_word_carrier/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_word_carrier",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_word_carrier/deferred/omega_deferred",
        )

    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_word_carrier",
        failure_code=None,
        output=WordCarrierCandidate(
            value=boundary.value,
            type="word_carrier",
            origin=boundary.origin,
            identity=f"wc-{boundary.identity}",
            domain=boundary.domain,
            scope=boundary.scope,
            rank=RankLattice.meet(boundary.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=boundary.trace,
            bounded_surface=boundary,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_word_carrier/licensed",
    )


def mu_root_stem(
    path_candidate: PathCandidate,
    path_verdict: PathGateVerdict,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_root_stem: PathCandidate + PathGateVerdict → RootStemCandidate (docs/20 §8).

    Requires a PathGateVerdict — extraction only on the ROOT path.
    Non-root paths continue without extraction (returned as-is in output).
    """
    if not isinstance(path_candidate, PathCandidate):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_root_stem",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_root_stem/refused/unlicensed_input",
        )

    if not isinstance(path_verdict, PathGateVerdict):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_root_stem",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_root_stem/refused/no_verdict",
        )

    # Path gate must have approved
    if path_verdict.state is not PathGateState.APPROVED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_root_stem",
            failure_code=path_verdict.failure_code or FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=path_verdict.residuals,
            trace_ref="mu_root_stem/refused/path_not_approved",
        )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_root_stem",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_root_stem/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_root_stem",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_root_stem/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_root_stem",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_root_stem/deferred/omega_deferred",
        )

    # Non-root paths continue without root/stem extraction
    if path_candidate.kind is not PathKind.ROOT:
        return MuStepResult(
            state=MuStepState.LICENSED,
            step_name="mu_root_stem",
            failure_code=None,
            output=path_candidate,
            rank=governance.granted_rank,
            residuals=governance.residuals,
            trace_ref="mu_root_stem/licensed/non_root_continuation",
        )

    # ROOT path — produce RootStemCandidate
    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_root_stem",
        failure_code=None,
        output=RootStemCandidate(
            value=path_candidate.value,
            type="root_stem",
            origin=path_candidate.origin,
            identity=f"root-{path_candidate.identity}",
            domain=path_candidate.domain,
            scope=path_candidate.scope,
            rank=RankLattice.meet(path_candidate.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=path_candidate.trace,
            path=path_candidate,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_root_stem/licensed/root_extracted",
    )


def mu_original_extra(
    form: str,
    assignments: tuple[tuple[str, str], ...],
    source_carrier: PathCandidate | RootStemCandidate,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_original_extra: path/root output → OriginalExtraMap (docs/20 §9).

    Accepts the §8 output (PathCandidate for non-root, RootStemCandidate for
    root path). The split is structural, never semantic.
    """
    from taaqqul_slot_geometry.weight.pre_weight import LetterStanding

    if not isinstance(source_carrier, (PathCandidate, RootStemCandidate)):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_original_extra",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_original_extra/refused/unlicensed_input",
        )

    if not isinstance(form, str) or not form.strip():
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_original_extra",
            failure_code=FailureCode.TRACE_MISSING,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_original_extra/refused/empty_form",
        )

    if not isinstance(assignments, tuple) or len(assignments) == 0:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_original_extra",
            failure_code=FailureCode.IDENTITY_BROKEN,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_original_extra/refused/no_assignments",
        )

    # Validate assignment entries
    for assignment in assignments:
        if (
            not isinstance(assignment, tuple)
            or len(assignment) != 2
            or not isinstance(assignment[0], str)
            or not assignment[0].strip()
            or not isinstance(assignment[1], str)
            or assignment[1] not in (ls.value for ls in LetterStanding)
        ):
            return MuStepResult(
                state=MuStepState.REFUSED,
                step_name="mu_original_extra",
                failure_code=FailureCode.IDENTITY_BROKEN,
                output=None,
                rank=Rank.ZERO,
                residuals=(),
                trace_ref="mu_original_extra/refused/invalid_assignment",
            )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_original_extra",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_original_extra/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_original_extra",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_original_extra/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_original_extra",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_original_extra/deferred/omega_deferred",
        )

    # Convert string standings to LetterStanding enum for the carrier
    typed_assignments = tuple(
        (letter, LetterStanding(standing)) for letter, standing in assignments
    )

    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_original_extra",
        failure_code=None,
        output=OriginalExtraMap(
            value=source_carrier.value,
            type="original_extra_map",
            origin=source_carrier.origin,
            identity=f"oem-{source_carrier.identity}",
            domain=source_carrier.domain,
            scope=source_carrier.scope,
            rank=RankLattice.meet(source_carrier.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=source_carrier.trace,
            underlying_form=form,
            assignments=typed_assignments,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_original_extra/licensed",
    )


def mu_ops(
    steps: tuple[str, ...],
    source_carrier: OriginalExtraMap,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_ops: OriginalExtraMap → OperationTraceCandidate (docs/20 §10).

    Every transformation applied to the form is recorded. An operation
    that cannot show its step is not an operation but an erasure.
    """
    if not isinstance(source_carrier, OriginalExtraMap):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_ops",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_ops/refused/unlicensed_input",
        )

    if not isinstance(steps, tuple) or len(steps) == 0:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_ops",
            failure_code=FailureCode.TRACE_MISSING,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_ops/refused/no_steps",
        )

    for step in steps:
        if not isinstance(step, str) or not step.strip():
            return MuStepResult(
                state=MuStepState.REFUSED,
                step_name="mu_ops",
                failure_code=FailureCode.TRACE_MISSING,
                output=None,
                rank=Rank.ZERO,
                residuals=(),
                trace_ref="mu_ops/refused/erased_step",
            )

    # Apply Ω governance
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_ops",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_ops/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_ops",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_ops/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_ops",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_ops/deferred/omega_deferred",
        )

    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_ops",
        failure_code=None,
        output=OperationTraceCandidate(
            value=source_carrier.value,
            type="operation_trace",
            origin=source_carrier.origin,
            identity=f"ops-{source_carrier.identity}",
            domain=source_carrier.domain,
            scope=source_carrier.scope,
            rank=RankLattice.meet(source_carrier.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=source_carrier.trace,
            steps=steps,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_ops/licensed",
    )


def mu_weight_readiness(
    surface: PreWeightSurface,
    governance: ResidualGovernanceVerdict,
) -> MuStepResult:
    """μ_weight_readiness: PreWeightSurface → WeightReadinessCandidate (docs/20 §11).

    The final μ step. Produces a WeightReadinessCandidate ONLY if Ω
    governance is GRANTED. This is pre-weighing readiness — NOT weight
    fit, NOT licensed weight, NOT weight discovery.

    WeightReadinessCandidate is the lawful object that later weight
    discovery (PR-13) may inspect. PR-12 does not discover weight.
    """
    if not isinstance(surface, PreWeightSurface):
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_weight_readiness",
            failure_code=FailureCode.GATE_REQUIRED,
            output=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="mu_weight_readiness/refused/unlicensed_input",
        )

    # Apply Ω governance — this is the final authority check
    if governance.state is OmegaGovernanceState.REJECTED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_weight_readiness",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_weight_readiness/refused/omega_rejected",
        )
    if governance.state is OmegaGovernanceState.BLOCKED:
        return MuStepResult(
            state=MuStepState.REFUSED,
            step_name="mu_weight_readiness",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_weight_readiness/refused/omega_blocked",
        )
    if governance.state is OmegaGovernanceState.DEFERRED:
        return MuStepResult(
            state=MuStepState.DEFERRED,
            step_name="mu_weight_readiness",
            failure_code=governance.failure_code,
            output=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="mu_weight_readiness/deferred/omega_deferred",
        )

    # GRANTED — produce WeightReadinessCandidate
    return MuStepResult(
        state=MuStepState.LICENSED,
        step_name="mu_weight_readiness",
        failure_code=None,
        output=WeightReadinessCandidate(
            value=surface.value,
            type="weight_readiness",
            origin=surface.origin,
            identity=f"wr-{surface.identity}",
            domain=surface.domain,
            scope=surface.scope,
            rank=RankLattice.meet(surface.rank, MU_CHAIN_RANK_CEILING),
            residuals=governance.residuals,
            trace=surface.trace,
            surface=surface,
        ),
        rank=governance.granted_rank,
        residuals=governance.residuals,
        trace_ref="mu_weight_readiness/licensed",
    )


__all__ = [
    "MU_CHAIN_RANK_CEILING",
    "MuStepResult",
    "MuStepState",
    "OmegaGovernanceState",
    "ResidualGovernanceVerdict",
    "mu_boundary",
    "mu_ops",
    "mu_original_extra",
    "mu_root_stem",
    "mu_seq",
    "mu_weight_readiness",
    "mu_word_carrier",
    "omega_governance",
]
