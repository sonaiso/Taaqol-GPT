"""``emit_successor`` — the emission half reserved by docs/08.

PR-6 binding of ``docs/17_SLOTGRAPH_GENERATION_LAW.md`` §1
(source 3 — ``TRANSITION_VERDICT``) and the emission half of
``docs/08_TRANSITION_GATE.md``: *the gate decides, the emitter
constructs* — and the emitter constructs **only** what an
``APPROVED`` verdict licenses.

``emit_successor(verdict, input_graph)`` is **pure** in the same
sense as the kernel (docs/17 §5):

* no I/O, no logging, no time reads;
* no append to a ``TraceLedger`` — this module deliberately does
  not import it; the :class:`~taaqqul_slot_geometry.audit.answer_audit.AnswerAudit`
  shell owns the ledger (docs/07);
* no mutation of ``verdict`` or ``input_graph``;
* total over its declared domain: every expected refusal returns a
  :class:`ConstructionResult` value carrying a named
  :class:`FailureCode`, never a bare exception. A wrong *type* of
  argument is a programmer mistake refused loudly with
  ``TypeError``, mirroring ``gamma``'s domain guard.

The constitutional law it binds (docs/17 §1, source 3):

* only an ``APPROVED`` :class:`TransitionVerdict` licenses a
  successor graph; every other gate verdict licenses *no graph at
  all* — only an audit record remains;
* the approving gate is *named*, and the name is preserved in the
  successor's ``trace_ref`` anchor (``…/gate/<gate_name>``) — an
  unnamed gate is a constitutional refusal, enforced at verdict
  birth by :class:`TransitionVerdict`;
* the successor's rank is exactly the verdict's ``granted_rank``
  (the §8 meet computed by the gate); emission never promotes;
* the successor is constructed *into* the verdict's
  ``target_layer`` — emitting into any other layer would be a
  silent re-decision of the move the gate already judged;
* identity is continuous (docs/16 link 2): the successor keeps the
  input graph's ``identity_claim``, slots, boundary, and declared
  residual surface. A verdict whose trace anchor does not match
  ``input_graph`` is an approval *about a different graph* and is
  refused with ``IDENTITY_BROKEN``.
"""

from __future__ import annotations

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.slot_graph import (
    Center,
    ConstructionResult,
    GenerationSource,
    OutputBoundary,
    SlotGraph,
    TraceRef,
)
from taaqqul_slot_geometry.core.transition_gate import TransitionVerdict
from taaqqul_slot_geometry.core.transition_state import TransitionState


def emit_successor(
    verdict: TransitionVerdict,
    input_graph: SlotGraph,
) -> ConstructionResult:
    """Construct the successor graph an ``APPROVED`` verdict licenses.

    Returns a :class:`ConstructionResult`:

    * a refusal value (``graph is None`` + named
      :class:`FailureCode`) for every non-``APPROVED`` verdict —
      propagating the verdict's own failure code — and for an
      approval whose trace anchor does not match ``input_graph``;
    * on approval, the result of
      :meth:`SlotGraph.construct` with
      ``generation_source=TRANSITION_VERDICT``, the verdict's
      ``granted_rank``, the verdict's ``target_layer`` as both
      declared and output layer, and a ``trace_ref`` extending the
      parent anchor with the named gate.
    """

    if not isinstance(verdict, TransitionVerdict):
        raise TypeError("emit_successor() requires a TransitionVerdict as verdict")
    if not isinstance(input_graph, SlotGraph):
        raise TypeError("emit_successor() requires a SlotGraph as input_graph")

    if verdict.state is not TransitionState.APPROVED:
        # docs/17 §1 source 3: only an APPROVED verdict generates.
        # The refusal carries the verdict's own named code — the
        # emitter never invents a second judgement about the move.
        return ConstructionResult(
            graph=None,
            failure_code=verdict.failure_code,
            message=(
                f"emit_successor: a {verdict.state.value} verdict licenses "
                "no successor graph; only an audit record remains "
                "(docs/17 §1, source 3)."
            ),
        )

    parent_anchor = input_graph.center.trace_ref.anchor
    if verdict.trace_event_candidate.parent_anchor != parent_anchor:
        # docs/16 link 2 — identity continuity: an approval whose
        # trace speaks about a different graph licenses nothing
        # here.
        return ConstructionResult(
            graph=None,
            failure_code=FailureCode.IDENTITY_BROKEN,
            message=(
                "emit_successor: the verdict's trace anchor does not match "
                "input_graph — the approval is not about this graph "
                "(docs/16 link 2)."
            ),
        )

    center = Center(
        identity_claim=input_graph.center.identity_claim,
        domain=input_graph.center.domain,
        scope=input_graph.center.scope,
        trace_ref=TraceRef(
            anchor=f"{parent_anchor}/gate/{verdict.gate_name}",
            kind="TRANSITION_VERDICT",
        ),
    )
    return SlotGraph.construct(
        center=center,
        slots=input_graph.slots,
        boundary=input_graph.boundary,
        residuals=input_graph.residuals,
        rank=verdict.granted_rank,
        output_boundary=OutputBoundary(
            declared_layer=verdict.target_layer,
            output_layer=verdict.target_layer,
        ),
        generation_source=GenerationSource.TRANSITION_VERDICT,
        entry_boundary=None,
    )


__all__ = ["emit_successor"]
