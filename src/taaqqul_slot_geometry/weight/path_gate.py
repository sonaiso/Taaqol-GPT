"""Pre-weight path gate — PR-11 binding of docs/20 §7 + docs/22.

PR-10 gave the carrier.  PR-10B forbade the carrier from claiming a
verdict.  PR-11 establishes the path court: the constitutional fork of
the pre-weight chain that receives a :class:`WordCarrierCandidate` and
emits a candidate path — one of the seven :class:`PathKind` members —
only after the evidence, domain, rank, and residual conditions are met,
and only through a :class:`PreWeightPathGate` with named refusals.

Structures:

* :class:`PathGateProof` — the evidence a caller presents to request a
  path kind.  A proof without evidence is refused; a proof claiming a
  kind not in :class:`PathKind` is refused.
* :class:`PathGateVerdict` — the gate's constitutional decision.
  ``APPROVED`` iff ``failure_code is None``; every refusal is named.
  Verdicts carry discovered ``residuals`` visibly.
* :class:`PreWeightPathGate` — the pure, frozen gate.
  :meth:`~PreWeightPathGate.decide` is the single decision entry point.

Laws enforced (docs/22):

* PathKind ≠ PathGateProof — a carrier declaration is never a verdict.
* Carrier declaration ≠ Gate verdict — docs/21 binding.
* Every refusal carries a named :class:`FailureCode`.
* A competing path that blocks a weaker one is a named preventer —
  never a silent override (``HIDDEN_RESIDUAL``).
* No weighing, no meaning, no extraction, no Ω judgment — those are
  PR-12+ surface.

This module adds **no new FailureCode members** and **no new runtime
dependencies**.  Every refusal maps onto the codes ratified in PR-1A.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import (
    BIRTH_RANK_CEILING,
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    PathKind,
    WordCarrierCandidate,
)


class PathGateState(StrEnum):
    """The four gate verdicts of the pre-weight path gate (docs/22 §5)."""

    APPROVED = "APPROVED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class PathGateProof:
    """The evidence a caller presents to request a path kind.

    A proof names:

    * ``claimed_kind`` — the :class:`PathKind` the caller asserts.
    * ``evidence_surface`` — a non-empty string describing the
      structural evidence for that kind.
    * ``evidence_rank`` — the rank the evidence carries into the meet.
    * ``domain`` — the declared domain of the evidence.

    A proof without evidence, or a proof claiming a kind not in
    :class:`PathKind`, is constitutionally invalid and refused at birth
    (docs/22 §4).  This is a programmer mistake (like
    :class:`WeightCarrierSchemaError`), not a gate verdict.
    """

    claimed_kind: PathKind
    evidence_surface: str
    evidence_rank: Rank
    domain: str

    def __post_init__(self) -> None:
        if not isinstance(self.claimed_kind, PathKind):
            raise WeightCarrierSchemaError(
                "PathGateProof.claimed_kind must be a PathKind member "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.evidence_surface, str) or not self.evidence_surface.strip():
            raise WeightCarrierSchemaError(
                "PathGateProof.evidence_surface must be a non-empty string "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.evidence_rank, Rank):
            raise WeightCarrierSchemaError(
                "PathGateProof.evidence_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.domain, str) or not self.domain.strip():
            raise WeightCarrierSchemaError(
                "PathGateProof.domain must be a non-empty string "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class PathGateVerdict:
    """The pure value returned by :meth:`PreWeightPathGate.decide`.

    Invariants (enforced at birth — docs/22 §5):

    * ``state`` is ``APPROVED`` **iff** ``failure_code`` is ``None``.
    * A refusal grants no path: ``approved_kind`` must be ``None`` for
      every non-``APPROVED`` state.
    * ``residuals`` are always visible (never hidden).
    * ``granted_rank`` is ``Rank.ZERO`` for refusals.
    """

    state: PathGateState
    failure_code: FailureCode | None
    approved_kind: PathKind | None
    granted_rank: Rank
    residuals: tuple[Residual, ...]
    gate_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, PathGateState):
            raise WeightCarrierSchemaError(
                "PathGateVerdict.state must be a PathGateState member"
            )
        if not isinstance(self.gate_name, str) or not self.gate_name.strip():
            raise WeightCarrierSchemaError(
                "PathGateVerdict.gate_name must be a non-empty string — "
                "an unnamed gate is a constitutional refusal (docs/22 §5)"
            )
        if not isinstance(self.granted_rank, Rank):
            raise WeightCarrierSchemaError(
                "PathGateVerdict.granted_rank must be a Rank member"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "PathGateVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "PathGateVerdict.residuals entries must be Residual carriers"
                )

        if self.state is PathGateState.APPROVED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "an APPROVED PathGateVerdict must not carry a FailureCode "
                    "(docs/22 §5 — named failure iff refusal)"
                )
            if self.approved_kind is None:
                raise WeightCarrierSchemaError(
                    "an APPROVED PathGateVerdict must carry an approved_kind"
                )
            if not isinstance(self.approved_kind, PathKind):
                raise WeightCarrierSchemaError(
                    "PathGateVerdict.approved_kind must be a PathKind member"
                )
        else:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a refusal PathGateVerdict must carry a named FailureCode "
                    "(docs/22 §5)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "PathGateVerdict.failure_code must be a FailureCode member"
                )
            if self.approved_kind is not None:
                raise WeightCarrierSchemaError(
                    "a refusal PathGateVerdict must not carry an approved_kind"
                )
            if self.granted_rank is not Rank.ZERO:
                raise WeightCarrierSchemaError(
                    "a refusal PathGateVerdict licenses nothing: "
                    "granted_rank must be Rank.ZERO"
                )


#: The maximum gate rank for a pre-weight path gate. The path gate
#: operates before weighing and before the kernel-level
#: TransitionGate, so it is capped at HYPOTHESIS — the same
#: ungated ceiling the kernel uses.
PATH_GATE_RANK_CEILING: Rank = Rank.HYPOTHESIS


@dataclass(frozen=True, slots=True)
class PreWeightPathGate:
    """The pre-weight path gate — the constitutional fork of the chain.

    A gate is born with a name and a ``gate_rank`` (capped at
    :data:`PATH_GATE_RANK_CEILING`).  Its single method
    :meth:`decide` is pure: it accepts values and returns a
    :class:`PathGateVerdict` value.  It never mutates inputs, never
    writes a ledger, and never constructs a carrier.

    Decision steps (a refusal at step *k* short-circuits):

    1. **Type guard** — ``carrier`` must be a
       :class:`WordCarrierCandidate`; ``proof`` must be a
       :class:`PathGateProof`.
    2. **Domain match** — the carrier's domain must match the proof's
       domain.
    3. **Evidence presence** — an empty evidence surface is
       ``DEFERRED`` / ``GATE_REQUIRED``.
    4. **Preventer check** — if ``preventers`` are provided, the gate
       checks whether any preventer blocks the claimed path.
    5. **Residual check** — blocking residuals on the carrier refuse
       the move.
    6. **Rank bound** — the evidence rank must not exceed the gate's
       rank ceiling (the bounded meet).
    7. **Approval** — ``APPROVED`` with the granted rank set to
       ``meet(evidence_rank, carrier_rank, gate_rank)``.
    """

    name: str
    gate_rank: Rank

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise TypeError(
                "PreWeightPathGate.name must be a non-empty string"
            )
        if not isinstance(self.gate_rank, Rank):
            raise TypeError(
                "PreWeightPathGate.gate_rank must be a Rank member"
            )
        if self.gate_rank > PATH_GATE_RANK_CEILING:
            raise TypeError(
                "PreWeightPathGate.gate_rank must not exceed "
                "PATH_GATE_RANK_CEILING (HYPOTHESIS): the path gate "
                "operates before the kernel-level TransitionGate"
            )

    def decide(
        self,
        carrier: WordCarrierCandidate,
        proof: PathGateProof,
        preventers: tuple[PathKind, ...] = (),
    ) -> PathGateVerdict:
        """Decide whether ``carrier`` may take the path claimed by ``proof``.

        Returns a :class:`PathGateVerdict` — never raises for expected
        verdicts (docs/22 §7).  Type-level mistakes (wrong argument
        types) raise ``TypeError`` as programmer errors.
        """
        if not isinstance(carrier, WordCarrierCandidate):
            raise TypeError(
                "PreWeightPathGate.decide() requires a "
                "WordCarrierCandidate as carrier"
            )
        if not isinstance(proof, PathGateProof):
            raise TypeError(
                "PreWeightPathGate.decide() requires a "
                "PathGateProof as proof"
            )

        # Step 2 — domain match
        if carrier.domain != proof.domain:
            return PathGateVerdict(
                state=PathGateState.REJECTED,
                failure_code=FailureCode.DOMAIN_MISSING,
                approved_kind=None,
                granted_rank=Rank.ZERO,
                residuals=(),
                gate_name=self.name,
            )

        # Step 3 — evidence presence (empty evidence_surface is
        # handled at proof birth; here we gate on evidence_rank)
        if proof.evidence_rank is Rank.ZERO:
            return PathGateVerdict(
                state=PathGateState.DEFERRED,
                failure_code=FailureCode.GATE_REQUIRED,
                approved_kind=None,
                granted_rank=Rank.ZERO,
                residuals=(),
                gate_name=self.name,
            )

        # Step 4 — preventer check: a stronger competing path blocks
        if preventers:
            for preventer in preventers:
                if preventer is not proof.claimed_kind:
                    # A competing path acts as a named preventer —
                    # never a silent override.
                    return PathGateVerdict(
                        state=PathGateState.BLOCKED,
                        failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                        approved_kind=None,
                        granted_rank=Rank.ZERO,
                        residuals=(
                            Residual(
                                name="competing_path_preventer",
                                kind=ResidualKind.BLOCKING,
                                visible=True,
                                note=(
                                    f"competing path {preventer.value} "
                                    f"blocks {proof.claimed_kind.value}"
                                ),
                            ),
                        ),
                        gate_name=self.name,
                    )

        # Step 5 — blocking residuals on the carrier
        for residual in carrier.residuals:
            if residual.kind is ResidualKind.BLOCKING:
                return PathGateVerdict(
                    state=PathGateState.BLOCKED,
                    failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                    approved_kind=None,
                    granted_rank=Rank.ZERO,
                    residuals=carrier.residuals,
                    gate_name=self.name,
                )

        # Step 6 — rank bound: carrier rank must not exceed ceiling
        if carrier.rank > BIRTH_RANK_CEILING:
            return PathGateVerdict(
                state=PathGateState.REJECTED,
                failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
                approved_kind=None,
                granted_rank=Rank.ZERO,
                residuals=(),
                gate_name=self.name,
            )

        # Step 7 — the bounded meet
        granted = RankLattice.meet(
            proof.evidence_rank,
            carrier.rank,
            self.gate_rank,
        )

        return PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=proof.claimed_kind,
            granted_rank=granted,
            residuals=(),
            gate_name=self.name,
        )


__all__ = [
    "PATH_GATE_RANK_CEILING",
    "PathGateProof",
    "PathGateState",
    "PathGateVerdict",
    "PreWeightPathGate",
]
