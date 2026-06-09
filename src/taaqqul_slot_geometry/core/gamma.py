"""``Γ`` — pure verdict function. PR-2 binding of docs/03 + docs/11 §7.

``gamma(graph)`` is a **pure** function:

* no I/O, no logging, no time reads;
* no mutation of ``graph`` or of any external store;
* no append to a :class:`TraceLedger` (this module deliberately does
  not import ``TraceLedger`` — see ``docs/07_TRACE_LEDGER.md``
  *PR-2 binding*);
* no rank promotion (only a :class:`TransitionGate` may, and only
  bounded by the lattice meet — PR-4);
* no residual classification beyond the visibility and kind checks
  named in ``docs/11`` §9 (the full :class:`ResidualPolicy` engine
  lands in PR-3);
* no synthesis of a missing field — missing means refuse.

``Γ`` returns a :class:`GammaResult` carrying:

* the verdict ``state`` (a :class:`ClosureState` member);
* the ``failure_code`` (a :class:`FailureCode` member when the
  verdict is a refusal; ``None`` for a closure verdict);
* the passthrough ``rank`` (carrier only in PR-2 — the rank-ceiling
  computation lands in PR-3);
* the projection of ``residuals`` and their aggregate
  ``residual_visibility``;
* a :class:`TraceEntryCandidate` snapshotting the verdict.

The order of checks is load-bearing. A refusal at step *k*
short-circuits steps *k+1 … 10* (docs/03 — *The ordered closure
law*).
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import SlotGraph, SlotState
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate

# Residual kinds that, when visible, license a perforated closure
# (docs/11 §6). HIDDEN_FORBIDDEN is *never* in this set; BLOCKING
# is handled at step 7 before this check is consulted.
_PERFORATING_KINDS: frozenset[ResidualKind] = frozenset(
    {
        ResidualKind.NON_BLOCKING,
        ResidualKind.DEFERRABLE,
        ResidualKind.EXPLANATORY,
    }
)


@dataclass(frozen=True, slots=True)
class GammaResult:
    """The pure verdict returned by :func:`gamma`.

    Properties:

    * ``state`` — exactly one of the six :class:`ClosureState`
      verdicts (docs/03 — *The six verdicts*).
    * ``failure_code`` — ``None`` iff ``state`` is a closure verdict
      (``MINIMALLY_CLOSED`` or ``PERFORATED_CLOSED``); a named
      :class:`FailureCode` member otherwise.
    * ``rank`` — passthrough carrier in PR-2; never promoted.
    * ``residuals`` / ``residual_visibility`` — projection of the
      input graph's residual surface. ``residual_visibility`` is the
      conjunction *(every residual is visible and not
      ``HIDDEN_FORBIDDEN``)*; the empty-residual case is vacuously
      visible (no hidden surface to expose).
    * ``trace_event_candidate`` — the immutable
      :class:`TraceEntryCandidate` a caller may then append to a
      :class:`TraceLedger`. ``Γ`` itself never appends.
    """

    state: ClosureState
    failure_code: FailureCode | None
    rank: Rank
    residuals: tuple[Residual, ...]
    residual_visibility: bool
    trace_event_candidate: TraceEntryCandidate


def _trace_anchor(graph: SlotGraph) -> str:
    """Return the opaque trace anchor without inspecting its content.

    Returns an empty string when no trace is present; the caller
    decides what to do with that information.
    """

    center = graph.center
    if center is None or center.trace_ref is None:
        return ""
    return center.trace_ref.anchor


def _candidate(
    graph: SlotGraph,
    state: ClosureState,
    failure: FailureCode | None,
) -> TraceEntryCandidate:
    return TraceEntryCandidate(
        parent_anchor=_trace_anchor(graph),
        stage="gamma",
        snapshot_state=state,
        snapshot_failure=failure,
        snapshot_rank=graph.rank,
    )


def _visibility(residuals: tuple[Residual, ...]) -> bool:
    """``Γ`` step 6's projection, used for the returned summary."""

    return all(
        r.visible and r.kind is not ResidualKind.HIDDEN_FORBIDDEN for r in residuals
    )


def _refuse(
    graph: SlotGraph,
    state: ClosureState,
    failure: FailureCode,
) -> GammaResult:
    return GammaResult(
        state=state,
        failure_code=failure,
        rank=graph.rank,
        residuals=graph.residuals,
        residual_visibility=_visibility(graph.residuals),
        trace_event_candidate=_candidate(graph, state, failure),
    )


def gamma(graph: SlotGraph) -> GammaResult:
    """Compute the constitutional closure verdict for ``graph``.

    See :mod:`taaqqul_slot_geometry.core.gamma` module docstring and
    ``docs/03_GAMMA_CLOSURE_CONTRACT.md`` for the ordered law. The
    function is pure: it returns a :class:`GammaResult` value and
    never raises for an expected refusal.
    """

    if not isinstance(graph, SlotGraph):
        # Programmer mistake (wrong type), not a constitutional
        # verdict. Refuse loudly: ``Γ`` is total only over its
        # declared domain ``SlotGraph``.
        raise TypeError("gamma(graph) requires a SlotGraph instance")

    center = graph.center

    # Step 1 — Center / identity_claim present.
    # PR-2A makes ``Center`` mandatory at SlotGraph construction time
    # (docs/17 §3); a graph reaching ``Γ`` with ``center is None`` is
    # therefore constructively unreachable through the named
    # construction surface :meth:`SlotGraph.construct`. The check
    # stays as a defence-in-depth invariant so ``Γ`` remains total
    # over its declared domain (docs/03 — ``Γ`` is total).
    if center is None or not center.identity_claim.strip():
        return _refuse(graph, ClosureState.INVALID, FailureCode.CENTER_MISSING)

    # Step 2 — Trace reference present.
    if center.trace_ref is None or not center.trace_ref.anchor.strip():
        return _refuse(graph, ClosureState.INVALID, FailureCode.TRACE_MISSING)

    # Step 3 — Domain / Scope / Boundary present.
    # ``boundary`` itself is a type-required field; the content
    # checks below mirror docs/11 §3 (``b.domain ≠ ∅ ∧ b.scope ≠ ∅``).
    if not graph.boundary.domain.strip():
        return _refuse(graph, ClosureState.INVALID, FailureCode.DOMAIN_MISSING)
    if not graph.boundary.scope.strip():
        return _refuse(graph, ClosureState.INVALID, FailureCode.SCOPE_MISSING)

    # Step 4 — No slot is BROKEN.
    for slot in graph.slots:
        if slot.value_state is SlotState.BROKEN:
            return _refuse(
                graph, ClosureState.INVALID, FailureCode.IDENTITY_BROKEN
            )

    # Step 5 — Output boundary stays within the declared layer.
    if graph.output_boundary.output_layer > graph.output_boundary.declared_layer:
        return _refuse(
            graph,
            ClosureState.FORBIDDEN_LEAP,
            FailureCode.OUTPUT_EXCEEDS_LAYER,
        )

    # Step 6 — No hidden / invisible residual.
    for residual in graph.residuals:
        if (
            residual.kind is ResidualKind.HIDDEN_FORBIDDEN
            or not residual.visible
        ):
            return _refuse(
                graph, ClosureState.INVALID, FailureCode.HIDDEN_RESIDUAL
            )

    # Step 7 — No blocking residual.
    for residual in graph.residuals:
        if residual.kind is ResidualKind.BLOCKING:
            return _refuse(
                graph,
                ClosureState.BLOCKED,
                FailureCode.BLOCKING_RESIDUAL_PRESENT,
            )

    # Step 8 — Every required slot is FILLED.
    for slot in graph.slots:
        if slot.required and slot.value_state is not SlotState.FILLED:
            return _refuse(
                graph, ClosureState.OPEN, FailureCode.REQUIRED_SLOT_EMPTY
            )

    # Step 9 — Rank ceiling. PR-2 carries the rank as a passthrough
    # (docs/03 — *Step 9's rank computation is fully implemented in
    # PR-3*). ``Γ`` must not *promote*; it does not here. The
    # ``RANK_EXCEEDS_CEILING`` failure code is reserved and emitted
    # by PR-3's ``RankLattice``.

    # Step 10 — Closure verdict.
    has_visible_nonblocking = any(
        r.visible and r.kind in _PERFORATING_KINDS for r in graph.residuals
    )
    state = (
        ClosureState.PERFORATED_CLOSED
        if has_visible_nonblocking
        else ClosureState.MINIMALLY_CLOSED
    )
    return GammaResult(
        state=state,
        failure_code=None,
        rank=graph.rank,
        residuals=graph.residuals,
        residual_visibility=_visibility(graph.residuals),
        trace_event_candidate=_candidate(graph, state, None),
    )


__all__ = ["GammaResult", "gamma"]
