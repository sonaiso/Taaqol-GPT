"""``AnswerAudit`` — the designated impure shell around the pure kernel.

PR-6 binding of ``docs/01_BLACK_BOX_BOUNDARY.md`` (the wrapper that
audits *emitted* answers) and ``docs/07_TRACE_LEDGER.md`` (the
ledger lives **outside** the pure functions; this module is the
place that owns it).

The division of labour is constitutional, not stylistic:

* ``gamma`` and ``TransitionGate.decide`` are pure — they *return*
  trace candidates and never append them;
* :func:`~taaqqul_slot_geometry.audit.successor.emit_successor` is
  pure — it constructs a licensed successor and never appends;
* :class:`AnswerAudit` is the impure shell: it calls the model
  through the :class:`ModelClient` protocol, runs the kernel, and
  appends the resulting candidates to its :class:`TraceLedger` in
  constitutional order — ``gamma`` → ``gate`` → ``audit``.

**No audit creates approval by itself.** The audit layer carries
verdicts; it never makes them. An :class:`AuditedAnswer` cannot be
born holding a successor graph unless the gate said ``APPROVED``,
and a successor-less audit must name *why* with a
:class:`FailureCode`. The model's own confidence never participates:
the only inputs to the verdict are the claim's :class:`SlotGraph`,
the :class:`EvidenceContract`, and the gate (docs/01).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from taaqqul_slot_geometry.audit.model_client import ModelClient
from taaqqul_slot_geometry.audit.reasonableness_integration import (
    AuditReasonablenessStatus,
    derive_reasonableness_residual_kind,
)
from taaqqul_slot_geometry.audit.successor import emit_successor
from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.evidence_contract import EvidenceContract
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.gamma import gamma
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual
from taaqqul_slot_geometry.core.slot_graph import (
    Layer,
    SlotGraph,
    SlotGraphSchemaError,
)
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate, TraceLedger
from taaqqul_slot_geometry.core.transition_gate import TransitionGate
from taaqqul_slot_geometry.core.transition_state import TransitionState

if TYPE_CHECKING:  # pragma: no cover — type-checker only
    from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
        GPTAnswerReasonablenessVerdict,
    )


@dataclass(frozen=True, slots=True)
class AuditedAnswer:
    """An emitted answer wrapped with its full constitutional verdict.

    Every claim carries its own ``gamma_state``, ``gate_state``,
    ``rank``, ``evidence_refs``, and ``residuals`` (docs/01 — the
    audit wrapper exposes the geometry, it never hides it).

    Birth invariants (enforced; ``SlotGraphSchemaError``):

    * ``successor`` present ⇒ ``gate_state is APPROVED`` and
      ``failure_code is None`` — **no audit creates approval by
      itself**: the only way to hold a successor is to have been
      handed one licensed by an ``APPROVED``
      :class:`~taaqqul_slot_geometry.core.transition_gate.TransitionVerdict`;
    * ``successor`` present ⇒ ``rank is successor.rank`` — the
      audit record never re-ranks what the gate granted;
    * ``successor`` absent ⇒ ``failure_code`` is a named
      :class:`FailureCode` and ``rank is Rank.ZERO`` — a
      successor-less audit names why and licenses nothing.

    ``prompt`` and ``answer`` are recorded verbatim and may be
    empty: the audit judges the *claim graph*, not the surface
    text. ``trace_anchor`` is the audited claim graph's own anchor
    so the record can be joined back to the ledger chain.
    """

    prompt: str
    answer: str
    gamma_state: ClosureState
    gate_state: TransitionState
    failure_code: FailureCode | None
    rank: Rank
    evidence_refs: tuple[str, ...]
    residuals: tuple[Residual, ...]
    residual_visibility: bool
    successor: SlotGraph | None
    trace_anchor: str
    # GPT-R8 (docs/56 §4.1) — Shape A additive field. The verdict is
    # never *constructed* by the audit shell: it is either passed in
    # by the caller (status=CARRIED) or absent and *named*-absent by
    # the integration status (NOT_RUN / DEFERRED / R7_NOT_CONSUMED).
    # Both fields default to a "no reasonableness consulted" state so
    # every pre-GPT-R8 call site keeps working unmodified
    # (docs/56 §2 B3 — birth invariants preserved).
    reasonableness_verdict: GPTAnswerReasonablenessVerdict | None = None
    reasonableness_status: AuditReasonablenessStatus = field(
        default=AuditReasonablenessStatus.NOT_RUN
    )

    def __post_init__(self) -> None:
        if not isinstance(self.prompt, str):
            raise SlotGraphSchemaError("AuditedAnswer.prompt must be a string")
        if not isinstance(self.answer, str):
            raise SlotGraphSchemaError("AuditedAnswer.answer must be a string")
        if not isinstance(self.gamma_state, ClosureState):
            raise SlotGraphSchemaError(
                "AuditedAnswer.gamma_state must be a ClosureState member"
            )
        if not isinstance(self.gate_state, TransitionState):
            raise SlotGraphSchemaError(
                "AuditedAnswer.gate_state must be a TransitionState member"
            )
        if self.failure_code is not None and not isinstance(
            self.failure_code, FailureCode
        ):
            raise SlotGraphSchemaError(
                "AuditedAnswer.failure_code must be a FailureCode or None"
            )
        if not isinstance(self.rank, Rank):
            raise SlotGraphSchemaError("AuditedAnswer.rank must be a Rank member")
        if not isinstance(self.evidence_refs, tuple):
            raise SlotGraphSchemaError(
                "AuditedAnswer.evidence_refs must be a tuple of strings"
            )
        for ref in self.evidence_refs:
            if not isinstance(ref, str):
                raise SlotGraphSchemaError(
                    "every AuditedAnswer.evidence_refs entry must be a string"
                )
        if not isinstance(self.residuals, tuple):
            raise SlotGraphSchemaError(
                "AuditedAnswer.residuals must be a tuple of Residual"
            )
        for residual in self.residuals:
            if not isinstance(residual, Residual):
                raise SlotGraphSchemaError(
                    "every AuditedAnswer.residuals entry must be a Residual"
                )
        if not isinstance(self.residual_visibility, bool):
            raise SlotGraphSchemaError(
                "AuditedAnswer.residual_visibility must be a bool"
            )
        if self.successor is not None and not isinstance(self.successor, SlotGraph):
            raise SlotGraphSchemaError(
                "AuditedAnswer.successor must be a SlotGraph or None"
            )
        if not isinstance(self.trace_anchor, str) or not self.trace_anchor.strip():
            raise SlotGraphSchemaError(
                "AuditedAnswer.trace_anchor must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        if self.successor is not None:
            if self.gate_state is not TransitionState.APPROVED:
                raise SlotGraphSchemaError(
                    "an AuditedAnswer cannot hold a successor without an "
                    "APPROVED gate verdict — no audit creates approval by "
                    "itself (docs/01; docs/17 §1, source 3)"
                )
            if self.failure_code is not None:
                raise SlotGraphSchemaError(
                    "an AuditedAnswer holding a successor must not carry a "
                    "FailureCode (named failure iff refusal)"
                )
            if self.rank is not self.successor.rank:
                raise SlotGraphSchemaError(
                    "AuditedAnswer.rank must equal the successor's rank — "
                    "the audit record never re-ranks the gate's grant"
                )
        else:
            if self.failure_code is None:
                raise SlotGraphSchemaError(
                    "a successor-less AuditedAnswer must name why with a "
                    "FailureCode (docs/08 precondition 5)"
                )
            if self.rank is not Rank.ZERO:
                raise SlotGraphSchemaError(
                    "a successor-less AuditedAnswer licenses nothing: rank "
                    "must be Rank.ZERO"
                )

        # ----- GPT-R8 (docs/56 §4.1) reasonableness-integration block -----
        # The block is appended *after* the existing B3 invariants (docs/56
        # §2 B3): nothing above this point is edited; the additive field
        # is checked in its own contiguous section so a verdict-less audit
        # remains byte-identical in behaviour to PR-6.
        if not isinstance(self.reasonableness_status, AuditReasonablenessStatus):
            raise SlotGraphSchemaError(
                "AuditedAnswer.reasonableness_status must be an "
                "AuditReasonablenessStatus member (docs/56 §4.1)"
            )
        # Avoid importing GPTAnswerReasonablenessVerdict at module load
        # time (audit/ does not depend on gpt/ at runtime); the type
        # check is performed by class-name probe via attribute presence,
        # then by isinstance only if available.
        verdict = self.reasonableness_verdict
        if verdict is not None:
            from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
                GPTAnswerReasonablenessVerdict,
            )

            if not isinstance(verdict, GPTAnswerReasonablenessVerdict):
                raise SlotGraphSchemaError(
                    "AuditedAnswer.reasonableness_verdict must be a "
                    "GPTAnswerReasonablenessVerdict or None (docs/56 §4.1)"
                )
            # docs/56 §2 B4 — no certificate, no authority, no truth. The
            # R7 carrier already enforces this at birth; the audit shell
            # re-asserts it independently so a forged carrier (one whose
            # attribute was mutated post-construction) cannot smuggle a
            # certificate through the audit boundary.
            if verdict.certificate_allowed is not False:
                raise SlotGraphSchemaError(
                    "AuditedAnswer.reasonableness_verdict.certificate_allowed "
                    "must be False — no certificate, no authority, no truth "
                    "(docs/56 §2 B4)"
                )
            # docs/56 §4.1 — verdict.rank must not exceed AuditedAnswer.rank.
            if verdict.rank > self.rank:
                raise SlotGraphSchemaError(
                    "AuditedAnswer.reasonableness_verdict.rank must not "
                    "exceed AuditedAnswer.rank (docs/56 §4.1)"
                )
            # docs/56 §4.1 — verdict.trace_ref must be present. R7 already
            # enforces a 'trace://'-prefixed non-empty string at birth; the
            # audit shell re-asserts presence at the integration boundary
            # so the invariant is visible in the audit's own schema
            # (docs/56 §2 B6 — trace continuity is mandatory).
            if not isinstance(verdict.trace_ref, str) or not verdict.trace_ref.strip():
                raise SlotGraphSchemaError(
                    "AuditedAnswer.reasonableness_verdict.trace_ref must be "
                    "a non-empty string (docs/56 §2 B6)"
                )
            # docs/56 §2.1.7 — CARRIED ⇔ verdict is not None.
            if self.reasonableness_status is not AuditReasonablenessStatus.CARRIED:
                raise SlotGraphSchemaError(
                    "AuditedAnswer with a reasonableness_verdict must carry "
                    "reasonableness_status=CARRIED (docs/56 §4.1)"
                )
        else:
            # docs/56 §2.1.7 — NOT_RUN / DEFERRED / R7_NOT_CONSUMED ⇔ verdict is None.
            if self.reasonableness_status is AuditReasonablenessStatus.CARRIED:
                raise SlotGraphSchemaError(
                    "AuditedAnswer.reasonableness_status=CARRIED requires a "
                    "non-None reasonableness_verdict (docs/56 §4.1)"
                )

    # ----- GPT-R8 (docs/56 §2 B5) read-through accessors --------------
    # Both methods are pure read-through enumerators; neither mutates state
    # and neither *constructs* a verdict (docs/56 §6 — no straight line from
    # AuditedAnswer to a verdict). Their purpose is to make residual
    # visibility and the integration-status residual kind explicit, so a
    # silent drop is structurally impossible.

    def enumerate_reasonableness_residuals(self) -> tuple:
        """Return the verdict's origin residuals verbatim, or ``()``.

        docs/56 §2 B5: every residual on a carried verdict must be
        enumerable on the audit record. Returns the empty tuple when
        no verdict is carried (not ``None`` — absence is named, not
        silent).
        """

        if self.reasonableness_verdict is None:
            return ()
        return self.reasonableness_verdict.residuals

    def reasonableness_residual_kind(self) -> str | None:
        """Return the docs/56 §7 local residual name for the current status.

        ``None`` for ``NOT_RUN`` / ``CARRIED`` (no residual is implied);
        the named string for ``DEFERRED`` / ``R7_NOT_CONSUMED``.
        """

        return derive_reasonableness_residual_kind(self.reasonableness_status)


class AnswerAudit:
    """The audit wrapper of docs/01 — call a model, judge the claim.

    ``AnswerAudit`` owns the only :class:`TraceLedger` writes in the
    package (docs/07): the pure kernel returns candidates, this
    shell appends them. One :meth:`audit` call appends exactly three
    entries, in constitutional order:

    1. the ``stage="gamma"`` candidate (``Γ`` ran first — docs/11
       §11);
    2. the ``stage="gate"`` candidate carried by the
       :class:`~taaqqul_slot_geometry.core.transition_gate.TransitionVerdict`;
    3. a ``stage="audit"`` candidate snapshotting the final audit
       record.

    The wrapper never constructs a ``SlotGraph`` itself (docs/17
    §4 — no graph from raw text): the claim graph arrives already
    constructed through a licensed source, and the only successor
    it can hand out is the one
    :func:`~taaqqul_slot_geometry.audit.successor.emit_successor`
    licenses from an ``APPROVED`` verdict.
    """

    __slots__ = ("_client", "_ledger")

    def __init__(self, client: ModelClient, ledger: TraceLedger) -> None:
        if not isinstance(client, ModelClient):
            raise TypeError(
                "AnswerAudit requires a ModelClient (an object with a "
                "complete(prompt) method — docs/01)"
            )
        if not isinstance(ledger, TraceLedger):
            raise TypeError("AnswerAudit requires a TraceLedger (docs/07)")
        self._client = client
        self._ledger = ledger

    def audit(
        self,
        prompt: str,
        claim_graph: SlotGraph,
        gate: TransitionGate,
        target_layer: Layer,
        evidence: EvidenceContract,
    ) -> AuditedAnswer:
        """Audit one emitted answer against its claim graph.

        Flow: complete the prompt through the black-box boundary →
        run ``Γ`` and ledger the ``gamma`` candidate → run the gate
        and ledger the ``gate`` candidate → if (and only if) the
        gate ``APPROVED``, request the licensed successor from
        :func:`emit_successor` → build the :class:`AuditedAnswer`
        and ledger the ``audit`` candidate.

        ``Γ`` runs twice by design (standalone and inside
        ``decide``): it is pure and deterministic, and the ledger
        must show the full ``gamma → gate → audit`` chain rather
        than a gate entry with no ``Γ`` record before it.

        Expected refusals surface as values on the returned
        :class:`AuditedAnswer` (named ``failure_code``, ``successor
        is None``, ``rank is Rank.ZERO``); a wrong *type* of
        argument is a programmer mistake refused loudly with
        ``TypeError``.
        """

        if not isinstance(prompt, str):
            raise TypeError("AnswerAudit.audit() requires a string prompt")
        if not isinstance(claim_graph, SlotGraph):
            raise TypeError(
                "AnswerAudit.audit() requires a SlotGraph as claim_graph"
            )
        if not isinstance(gate, TransitionGate):
            raise TypeError(
                "AnswerAudit.audit() requires a TransitionGate as gate"
            )
        if not isinstance(target_layer, Layer):
            raise TypeError(
                "AnswerAudit.audit() requires a Layer member as target_layer"
            )
        if not isinstance(evidence, EvidenceContract):
            raise TypeError(
                "AnswerAudit.audit() requires an EvidenceContract as evidence"
            )

        answer = self._client.complete(prompt)
        if not isinstance(answer, str):
            raise TypeError(
                "ModelClient.complete() must return a string answer (docs/01)"
            )

        gamma_result = gamma(claim_graph)
        self._ledger.append(gamma_result.trace_event_candidate)

        verdict = gate.decide(claim_graph, target_layer, evidence)
        self._ledger.append(verdict.trace_event_candidate)

        successor: SlotGraph | None = None
        failure_code = verdict.failure_code
        rank = Rank.ZERO
        if verdict.state is TransitionState.APPROVED:
            emission = emit_successor(verdict, claim_graph)
            if emission.is_refusal:
                # Theoretically unreachable through this flow (the
                # verdict was just produced for this very graph),
                # but emit_successor is total and the audit stays
                # total with it: the refusal is carried, named.
                failure_code = emission.failure_code
            else:
                successor = emission.graph
                rank = verdict.granted_rank

        audited = AuditedAnswer(
            prompt=prompt,
            answer=answer,
            gamma_state=verdict.gamma_state,
            gate_state=verdict.state,
            failure_code=failure_code,
            rank=rank,
            evidence_refs=tuple(
                source.trace_ref.anchor for source in evidence.sources
            ),
            residuals=gamma_result.residuals,
            residual_visibility=verdict.residual_visibility,
            successor=successor,
            trace_anchor=claim_graph.center.trace_ref.anchor,
        )
        self._ledger.append(
            TraceEntryCandidate(
                parent_anchor=audited.trace_anchor,
                stage="audit",
                consulted_gamma_state=verdict.gamma_state,
                gate_transition_state=verdict.state,
                snapshot_failure=failure_code,
                snapshot_rank=rank,
            )
        )
        return audited

    def audit_with_reasonableness(
        self,
        prompt: str,
        claim_graph: SlotGraph,
        gate: TransitionGate,
        target_layer: Layer,
        evidence: EvidenceContract,
        *,
        reasonableness_verdict: GPTAnswerReasonablenessVerdict | None,
        reasonableness_status: AuditReasonablenessStatus,
    ) -> AuditedAnswer:
        """Audit one answer and carry a GPT-R7 reasonableness verdict surface.

        Shape A integration (docs/56 §4.1): the existing
        :meth:`audit` is called unchanged to produce the gamma → gate
        → audit ledger entries; an :class:`AuditedAnswer` is then
        re-constructed with the optional reasonableness fields, and a
        single additional ``stage="audit.reasonableness"`` entry is
        appended to the ledger when the integration status warrants
        it (docs/56 §2 B6 — constitutional order ``gamma → gate →
        audit → audit.reasonableness``).

        ``reasonableness_status=NOT_RUN`` (with verdict ``None``) is
        the legacy / default path: no fourth ledger entry is appended,
        but the returned :class:`AuditedAnswer` still names the
        absence via :attr:`AuditedAnswer.reasonableness_status` (no
        silent drop — docs/56 §2 B5). Statuses ``CARRIED`` /
        ``DEFERRED`` / ``R7_NOT_CONSUMED`` each force a fourth ledger
        entry naming the integration state explicitly.

        Pre-validation (before any ledger write) refuses a malformed
        carrier at the seam:

        * ``reasonableness_status`` must be an
          :class:`AuditReasonablenessStatus` member;
        * if ``reasonableness_verdict`` is not ``None`` it must be a
          :class:`GPTAnswerReasonablenessVerdict` whose
          ``certificate_allowed`` is exactly ``False`` (docs/56 §2
          B4 — re-asserted at the integration boundary even though
          GPT-R7 already enforces it at birth);
        * the ``status`` ⇔ ``verdict-presence`` invariant from
          docs/56 §4.1 must hold.
        """

        if not isinstance(reasonableness_status, AuditReasonablenessStatus):
            raise TypeError(
                "AnswerAudit.audit_with_reasonableness() requires an "
                "AuditReasonablenessStatus as reasonableness_status (docs/56 §4.1)"
            )
        if reasonableness_verdict is not None:
            # Local import keeps the audit/ → gpt/ dependency runtime-free
            # at module load. The carrier is inspected by type only here.
            from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
                GPTAnswerReasonablenessVerdict,
            )

            if not isinstance(reasonableness_verdict, GPTAnswerReasonablenessVerdict):
                raise TypeError(
                    "AnswerAudit.audit_with_reasonableness() requires a "
                    "GPTAnswerReasonablenessVerdict or None as "
                    "reasonableness_verdict (docs/56 §4.1)"
                )
            if reasonableness_verdict.certificate_allowed is not False:
                raise SlotGraphSchemaError(
                    "AnswerAudit.audit_with_reasonableness() refuses a "
                    "verdict whose certificate_allowed is not False — no "
                    "certificate, no authority, no truth (docs/56 §2 B4)"
                )
            if reasonableness_status is not AuditReasonablenessStatus.CARRIED:
                raise SlotGraphSchemaError(
                    "a non-None reasonableness_verdict requires "
                    "reasonableness_status=CARRIED (docs/56 §4.1)"
                )
        else:
            if reasonableness_status is AuditReasonablenessStatus.CARRIED:
                raise SlotGraphSchemaError(
                    "reasonableness_status=CARRIED requires a non-None "
                    "reasonableness_verdict (docs/56 §4.1)"
                )

        base = self.audit(prompt, claim_graph, gate, target_layer, evidence)

        if reasonableness_verdict is None and (
            reasonableness_status is AuditReasonablenessStatus.NOT_RUN
        ):
            # Legacy/default — the base audit() result is already complete;
            # no fourth entry is appended (absence is named on the carrier
            # by status=NOT_RUN; docs/56 §2 B5).
            return base

        audited = AuditedAnswer(
            prompt=base.prompt,
            answer=base.answer,
            gamma_state=base.gamma_state,
            gate_state=base.gate_state,
            failure_code=base.failure_code,
            rank=base.rank,
            evidence_refs=base.evidence_refs,
            residuals=base.residuals,
            residual_visibility=base.residual_visibility,
            successor=base.successor,
            trace_anchor=base.trace_anchor,
            reasonableness_verdict=reasonableness_verdict,
            reasonableness_status=reasonableness_status,
        )
        self._ledger.append(
            TraceEntryCandidate(
                parent_anchor=audited.trace_anchor,
                stage="audit.reasonableness",
                consulted_gamma_state=audited.gamma_state,
                gate_transition_state=audited.gate_state,
                snapshot_failure=audited.failure_code,
                snapshot_rank=audited.rank,
            )
        )
        return audited


__all__ = ["AnswerAudit", "AuditedAnswer"]
