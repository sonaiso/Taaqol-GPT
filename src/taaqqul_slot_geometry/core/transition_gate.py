"""Transition gate — PR-4 binding of docs/08 + docs/11 §8, §10, §11.

PR-3 shipped the three meet components the constitution names
(``RankLattice``, ``ResidualPolicy``, ``EvidenceContract``). PR-4
binds the gate that consumes them. The law the gate closes is:

    TransitionAllowed(x → y) ⇔
        EvidenceContract valid ∧ Identity valid ∧ Gate valid
        ∧ ResidualPolicy valid
        ∧ rank_out ≤ meet(evidence_rank, identity_rank,
                          gate_rank, residual_ceiling)
        ∧ failure is named when blocked

following the verdict table and preconditions of
``docs/08_TRANSITION_GATE.md`` and the Rank Ceiling Law of
``docs/11`` §8.

The gate is pure: :meth:`TransitionGate.decide` accepts values and
returns a :class:`TransitionVerdict` value. It never appends to a
:class:`TraceLedger` (this module deliberately does not import
``TraceLedger`` — the PR-2 purity guard pattern), never mutates the
input graph, and never *constructs* the successor graph: emitting a
new ``SlotGraph`` whose ``generation_source`` is
``TRANSITION_VERDICT`` (docs/17 §1, source 3) is the caller's act,
licensed — and rank-bounded — by the verdict value returned here.

PR-4 binds the three :class:`FailureCode` members that every earlier
PR reserved without emitting:

* ``FORBIDDEN_STRAIGHT_LINE`` — a transition targeting the
  ``CERTIFICATE`` layer through this generic gate. ``Candidate →
  Certificate`` requires a ``CertificationGate`` (docs/04), and each
  forbidden line stays ``FORBIDDEN_STRAIGHT_LINE`` "until the row's
  required bridge is opened by a future PR" (docs/16 §4). The typed
  registry itself is PR-5; PR-4 hard-codes only this one bar.
* ``RANK_PROMOTION_WITHOUT_GATE`` — an input graph that *claims* a
  gate-licensed rank (above :data:`UNGATED_RANK_CEILING`) without
  being the product of a transition verdict (docs/16 link 9: the
  forbidden line ``Candidate → Truth``).
* ``GATE_REQUIRED`` — a transition attempted on an empty evidence
  surface (docs/08 precondition 1; docs/16 link 10: a gate passage
  without evidence is not a gate passage). The verdict is
  ``DEFERRED``: retry is permitted once evidence arrives.

Declared residuals of PR-4 (visible, deferrable):

* the typed Forbidden Straight-Line Registry (PR-5) — only the
  certificate-layer bar is bound here;
* the ``CertificationGate`` that could license ``CERTIFICATE``
  (PR-5) — every PR-4 gate is capped at :data:`GATE_RANK_CEILING`;
* successor-graph emission and the audit wrapper (PR-6).

See ``docs/08_TRANSITION_GATE.md`` — *PR-4 binding*.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.evidence_contract import EvidenceContract
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.gamma import GammaResult, gamma
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import ResidualPolicy
from taaqqul_slot_geometry.core.slot_graph import (
    GenerationSource,
    Layer,
    SlotGraph,
    SlotGraphSchemaError,
)
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate


class TransitionState(StrEnum):
    """The five gate verdicts of docs/08.

    ``TransitionState`` is deliberately distinct from
    :class:`ClosureState`: a gate verdict speaks about a *move*, a
    closure verdict speaks about a *graph*. The two never coerce
    into each other silently — :class:`TransitionVerdict` carries
    the consulted ``gamma_state`` alongside the gate ``state`` so
    both judgements stay visible.
    """

    APPROVED = "APPROVED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


# The highest rank a graph may *carry into* a gate without being the
# product of a prior transition verdict. ``LICENSED`` is, by name and
# by docs/11 §8 corollary, a *gate-licensed* rank: claiming it (or
# anything above it) from a ``DECLARED_ENTRY`` / ``CANDIDATE``
# generation source is the forbidden line ``Candidate → Truth``
# (docs/16 link 9) and is refused with
# ``RANK_PROMOTION_WITHOUT_GATE``.
UNGATED_RANK_CEILING: Rank = Rank.HYPOTHESIS

# The highest rank a PR-4 gate itself may carry into the §8 meet. A
# gate born with ``gate_rank = CERTIFICATE`` would be a
# ``CertificationGate`` — the bridge docs/04 reserves for the
# ``Candidate → Certificate`` line, which lands with the Forbidden
# Straight-Line Registry in PR-5. Because ``granted_rank`` is a meet
# that includes ``gate_rank``, this birth cap makes it *structurally*
# impossible for any PR-4 verdict to grant ``CERTIFICATE``.
GATE_RANK_CEILING: Rank = Rank.STRONG


# Γ refusal → gate verdict (docs/11 §11 — the Gate consults Γ; §9 —
# a refused graph may not be approved by any gate):
#
# * ``INVALID`` — the graph itself is constitutionally refused; the
#   move is unlicensed for *every* gate → ``REJECTED``.
# * ``FORBIDDEN_LEAP`` — the graph already exceeds its declared
#   layer; the gate names the same fatality → ``FORBIDDEN_LEAP``.
# * ``BLOCKED`` — a blocking residual prevents the move (docs/08)
#   → ``BLOCKED``.
# * ``OPEN`` — preconditions not yet met; retry permitted once the
#   required slots fill (docs/08) → ``DEFERRED``.
_GAMMA_REFUSAL_TO_TRANSITION: dict[ClosureState, TransitionState] = {
    ClosureState.INVALID: TransitionState.REJECTED,
    ClosureState.FORBIDDEN_LEAP: TransitionState.FORBIDDEN_LEAP,
    ClosureState.BLOCKED: TransitionState.BLOCKED,
    ClosureState.OPEN: TransitionState.DEFERRED,
}


@dataclass(frozen=True, slots=True)
class TransitionVerdict:
    """Pure value returned by :meth:`TransitionGate.decide`.

    Invariants (enforced at birth — docs/11 §12, *missing means
    refuse*; a malformed verdict can never reach a caller):

    * ``state`` is ``APPROVED`` **iff** ``failure_code`` is ``None``
      — every refusal is named, never silent (docs/08 precondition
      5).
    * A refusal grants nothing: ``granted_rank`` must be
      ``Rank.ZERO`` for every non-``APPROVED`` state (mirroring the
      empty :class:`EvidenceContract` → lattice bottom rule).
    * ``gamma_state`` / ``residual_visibility`` — the Γ consultation
      the gate is bound to perform (docs/11 §11) stays visible on
      the verdict; the gate never hides what ``Γ`` said.
    * ``trace_event_candidate`` — every verdict, approval or
      refusal, proposes a ``stage="gate"`` trace entry for the
      caller to append (docs/08 precondition 4). The gate itself
      never appends.
    """

    state: TransitionState
    failure_code: FailureCode | None
    granted_rank: Rank
    gamma_state: ClosureState
    residual_visibility: bool
    trace_event_candidate: TraceEntryCandidate

    def __post_init__(self) -> None:
        if not isinstance(self.state, TransitionState):
            raise SlotGraphSchemaError(
                "TransitionVerdict.state must be a TransitionState member"
            )
        if self.failure_code is not None and not isinstance(
            self.failure_code, FailureCode
        ):
            raise SlotGraphSchemaError(
                "TransitionVerdict.failure_code must be a FailureCode or None"
            )
        if not isinstance(self.granted_rank, Rank):
            raise SlotGraphSchemaError(
                "TransitionVerdict.granted_rank must be a Rank member"
            )
        if not isinstance(self.gamma_state, ClosureState):
            raise SlotGraphSchemaError(
                "TransitionVerdict.gamma_state must be a ClosureState member"
            )
        if not isinstance(self.residual_visibility, bool):
            raise SlotGraphSchemaError(
                "TransitionVerdict.residual_visibility must be a bool"
            )
        if not isinstance(self.trace_event_candidate, TraceEntryCandidate):
            raise SlotGraphSchemaError(
                "TransitionVerdict.trace_event_candidate must be a "
                "TraceEntryCandidate"
            )

        if self.state is TransitionState.APPROVED:
            if self.failure_code is not None:
                raise SlotGraphSchemaError(
                    "an APPROVED TransitionVerdict must not carry a "
                    "FailureCode (docs/08 — named failure iff refusal)"
                )
        else:
            if self.failure_code is None:
                raise SlotGraphSchemaError(
                    "a refusal TransitionVerdict must carry a named "
                    "FailureCode (docs/08 precondition 5)"
                )
            if self.granted_rank is not Rank.ZERO:
                raise SlotGraphSchemaError(
                    "a refusal TransitionVerdict licenses nothing: "
                    "granted_rank must be Rank.ZERO"
                )


def _verdict(
    gamma_result: GammaResult,
    state: TransitionState,
    failure: FailureCode | None,
    granted: Rank = Rank.ZERO,
) -> TransitionVerdict:
    """Package a verdict with its ``stage="gate"`` trace candidate.

    The candidate snapshots the *consulted* Γ state next to the
    gate's own named failure: the trace records both that ``Γ`` ran
    first (docs/11 §11) and what the gate decided about the move.
    The parent anchor is the one ``Γ`` already extracted — the gate
    never re-inspects the opaque trace content (docs/11 §12).
    """

    return TransitionVerdict(
        state=state,
        failure_code=failure,
        granted_rank=granted,
        gamma_state=gamma_result.state,
        residual_visibility=gamma_result.residual_visibility,
        trace_event_candidate=TraceEntryCandidate(
            parent_anchor=gamma_result.trace_event_candidate.parent_anchor,
            stage="gate",
            snapshot_state=gamma_result.state,
            snapshot_failure=failure,
            snapshot_rank=granted,
        ),
    )


@dataclass(frozen=True, slots=True)
class TransitionGate:
    """The only legal cross-layer or cross-slot move (docs/08).

    A gate is born with an identity and a declared ``gate_rank`` —
    the rank *this* gate is licensed to enter into the §8 meet. The
    birth guards mirror the :class:`Residual` carrier (PR-3-FIX): a
    malformed gate is a programmer mistake refused loudly with
    ``TypeError``, never a constitutional verdict, and therefore can
    never decide anything.

    ``gate_rank`` may never exceed :data:`GATE_RANK_CEILING`
    (``STRONG``): a ``CERTIFICATE``-granting gate is the
    ``CertificationGate`` reserved for PR-5 (docs/04 — the
    ``Candidate → Certificate`` bridge).
    """

    name: str
    gate_rank: Rank

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise TypeError("TransitionGate.name must be a non-empty string")
        if not isinstance(self.gate_rank, Rank):
            raise TypeError("TransitionGate.gate_rank must be a Rank")
        if self.gate_rank > GATE_RANK_CEILING:
            raise TypeError(
                "TransitionGate.gate_rank must not exceed GATE_RANK_CEILING "
                "(STRONG): a CERTIFICATE-granting gate is the "
                "CertificationGate reserved for PR-5 (docs/04)"
            )

    def decide(
        self,
        input_graph: SlotGraph,
        target_layer: Layer,
        evidence: EvidenceContract,
    ) -> TransitionVerdict:
        """Decide ``input_graph → target_layer`` under ``evidence``.

        The ordered steps (a refusal at step *k* short-circuits the
        rest, mirroring ``Γ``'s ordered closure law):

        1. **Γ consultation** (docs/11 §11 — ``Γ`` runs before any
           Gate). A Γ refusal maps to the gate verdict table in
           :data:`_GAMMA_REFUSAL_TO_TRANSITION`, carrying Γ's own
           named :class:`FailureCode` through unchanged.
        2. **Certificate-layer bar** (docs/04, docs/16 §4): a
           ``CERTIFICATE`` target through this generic gate is
           ``FORBIDDEN_LEAP`` / ``FORBIDDEN_STRAIGHT_LINE`` — even
           with certificate-rank evidence. Fatal; no retry.
        3. **Ungated rank claim** (docs/16 link 9): a graph whose
           ``generation_source`` is not ``TRANSITION_VERDICT``
           claiming a rank above :data:`UNGATED_RANK_CEILING` is
           ``REJECTED`` / ``RANK_PROMOTION_WITHOUT_GATE``.
        4. **Evidence presence** (docs/08 precondition 1): an empty
           evidence surface is ``DEFERRED`` / ``GATE_REQUIRED`` —
           retry permitted once evidence arrives.
        5. **The §8 meet** (docs/08 preconditions 2–3):
           ``granted = meet(evidence_rank, identity_rank,
           gate_rank, residual_ceiling)`` where ``identity_rank`` is
           the rank the input graph carries (docs/05) and the
           residual ceiling comes from
           :meth:`ResidualPolicy.ceiling` via ``evaluate``. The meet
           can only keep or lower — this is the single place a rank
           may be *granted*, and it is bounded.
        6. **Approval**: ``APPROVED`` with ``granted_rank`` set to
           the meet, ``failure_code`` ``None``.

        Every path returns a :class:`TransitionVerdict` carrying a
        ``stage="gate"`` :class:`TraceEntryCandidate` (docs/08
        precondition 4); expected refusals are named values, never
        exceptions (precondition 5). A wrong *type* of argument is a
        programmer mistake refused loudly with ``TypeError``,
        mirroring ``gamma``'s domain guard.
        """

        if not isinstance(input_graph, SlotGraph):
            raise TypeError(
                "TransitionGate.decide() requires a SlotGraph as input_graph"
            )
        if not isinstance(target_layer, Layer):
            raise TypeError(
                "TransitionGate.decide() requires a Layer member as target_layer"
            )
        if not isinstance(evidence, EvidenceContract):
            raise TypeError(
                "TransitionGate.decide() requires an EvidenceContract as evidence"
            )

        # Step 1 — Γ runs before any Gate (docs/11 §11). A refused
        # graph may not be approved by any gate (docs/11 §9).
        gamma_result = gamma(input_graph)
        if gamma_result.failure_code is not None:
            return _verdict(
                gamma_result,
                _GAMMA_REFUSAL_TO_TRANSITION[gamma_result.state],
                gamma_result.failure_code,
            )

        # Step 2 — the certificate-layer bar. ``Evidence →
        # Certainty`` / ``Candidate → Certificate`` stay forbidden
        # straight lines until the CertificationGate bridge opens in
        # PR-5 (docs/04; docs/16 §4).
        if target_layer is Layer.CERTIFICATE:
            return _verdict(
                gamma_result,
                TransitionState.FORBIDDEN_LEAP,
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
            )

        # Step 3 — no rank promotion outside a gate (docs/16 link 9).
        # Only a graph that *is* the product of a transition verdict
        # may carry a gate-licensed rank into a gate.
        if (
            input_graph.generation_source is not GenerationSource.TRANSITION_VERDICT
            and input_graph.rank > UNGATED_RANK_CEILING
        ):
            return _verdict(
                gamma_result,
                TransitionState.REJECTED,
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )

        # Step 4 — evidence must be present (docs/08 precondition 1;
        # docs/16 link 10). Absent evidence defers: the move is not
        # forbidden, it is simply not yet licensed.
        if not evidence.sources:
            return _verdict(
                gamma_result,
                TransitionState.DEFERRED,
                FailureCode.GATE_REQUIRED,
            )

        # Step 5 — the §8 meet (docs/08 preconditions 2–3). The
        # residual ceiling participates in the meet only; it never
        # sets a rank by itself.
        ceiling = ResidualPolicy.evaluate(input_graph.residuals).ceiling
        granted = RankLattice.meet(
            evidence.evidence_rank,
            input_graph.rank,
            self.gate_rank,
            ceiling,
        )

        # Step 6 — approval, bounded by the meet.
        return _verdict(gamma_result, TransitionState.APPROVED, None, granted)


__all__ = [
    "GATE_RANK_CEILING",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    "UNGATED_RANK_CEILING",
]
