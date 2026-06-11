"""Constitutional tests for the PR-6 audit layer.

Coverage mirrors the PR-6 acceptance list — the propositions the
audit layer must prove:

1.  **Golden emission** (docs/17 §1, source 3): an ``APPROVED``
    :class:`TransitionVerdict` — and only it — licenses a successor
    ``SlotGraph``, carrying exactly the granted rank, the named gate
    in its trace anchor, and the verdict's target layer.
2.  **Refusal emission** (docs/08): a ``DEFERRED`` / ``REJECTED`` /
    ``BLOCKED`` / ``FORBIDDEN_LEAP`` verdict licenses *no graph at
    all* — only an audit record remains, named with the verdict's
    own :class:`FailureCode`.
3.  **Identity continuity** (docs/16 link 2): an approval whose
    trace anchor speaks about a different graph emits nothing —
    ``IDENTITY_BROKEN``.
4.  **No audit creates approval by itself** (docs/01): an
    :class:`AuditedAnswer` cannot be born holding a successor
    without an ``APPROVED`` gate verdict, and a successor-less
    audit names why with a :class:`FailureCode` at ``Rank.ZERO``.
5.  **The ledger chain** (docs/07): one :meth:`AnswerAudit.audit`
    call appends exactly the ordered ``gamma → gate → audit``
    stages, with the PR-6 trace split (``consulted_gamma_state`` /
    ``gate_transition_state``) intact on every entry.

Disciplines: the ``ModelClient`` protocol is structural only
(docs/01 — no adapter, no network surface ships in PR-6);
``emit_successor`` never touches the ``TraceLedger`` (the PR-2
purity guard pattern); birth and domain guards refuse programmer
mistakes loudly (``TypeError`` / ``SlotGraphSchemaError``), never as
constitutional verdicts.

Verdict-producing tests declare themselves through
:class:`ConstitutionalChainTestCase` (docs/12 §9) and are checked by
:func:`assert_constitutional_case`.
"""

from __future__ import annotations

import ast
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry import (
    AnswerAudit,
    AuditedAnswer,
    Center,
    ClosureState,
    EntryBoundary,
    EvidenceContract,
    EvidenceSource,
    FailureCode,
    GenerationSource,
    Layer,
    ModelClient,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    Residual,
    ResidualKind,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceLedger,
    TraceRef,
    TransitionGate,
    TransitionState,
    emit_successor,
    gamma,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — identical in shape to the gate tests; each
# audit test varies only the single axis it exercises.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="audit-test",
        refusal_codes=(FailureCode.BOUNDARY_MISSING,),
    )


def _opening() -> OpeningPolicy:
    return OpeningPolicy(allowed_potentials=frozenset({"yes", "no"}))


def _filled_slot(name: str = "answer") -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.FILLED,
        boundary=_boundary(),
        opening=_opening(),
        required=True,
        value="yes",
    )


def _trace_ref(kind: str = "DECLARED_ENTRY", anchor: str = "trace://Q1") -> TraceRef:
    return TraceRef(anchor=anchor, kind=kind)


def _center(trace_kind: str = "DECLARED_ENTRY", anchor: str = "trace://Q1") -> Center:
    return Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="audit-test",
        trace_ref=_trace_ref(trace_kind, anchor),
    )


def _output_within() -> OutputBoundary:
    return OutputBoundary(declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT)


def _entry_boundary() -> EntryBoundary:
    return EntryBoundary(
        declared_entry_kind="ARABIC_VOCALIZED_TEXT",
        representation_status="REPRESENTATIONAL_OF_PRIOR",
        ontological_status="NOT_AN_ORIGIN",
        sound_status="NOT_A_SOUND",
        meaning_status="NOT_A_MEANING",
        prior_trace_status="OUT_OF_CURRENT_EXECUTION",
        produces_only="TEXT_TRACE_CANDIDATE",
    )


def _declared_graph(*, rank: Rank = Rank.TRACE) -> SlotGraph:
    """A ``DECLARED_ENTRY`` graph — the ungated origin."""

    return SlotGraph(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=rank,
        output_boundary=_output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),
    )


def _gated_graph(
    *,
    residuals: tuple[Residual, ...] = (),
    rank: Rank = Rank.HYPOTHESIS,
    anchor: str = "trace://Q1",
) -> SlotGraph:
    """A graph that *is* the product of a prior transition verdict."""

    return SlotGraph(
        center=_center("TRANSITION_VERDICT", anchor),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=residuals,
        rank=rank,
        output_boundary=_output_within(),
        generation_source=GenerationSource.TRANSITION_VERDICT,
    )


def _gate(rank: Rank = Rank.LICENSED) -> TransitionGate:
    return TransitionGate(name="slot-to-candidate", gate_rank=rank)


def _evidence(name: str, rank: Rank) -> EvidenceSource:
    return EvidenceSource(
        name=name,
        kind="declared-observation",
        rank=rank,
        trace_ref=_trace_ref(),
    )


def _strong_evidence() -> EvidenceContract:
    return EvidenceContract(sources=(_evidence("e1", Rank.STRONG),))


def _blocking_residual() -> Residual:
    return Residual(
        name="unresolved-objection",
        kind=ResidualKind.BLOCKING,
        visible=True,
        note="a blocking residual prevents the move",
    )


class _EchoClient:
    """Minimal docs/01 black box: a prompt in, an emitted answer out."""

    def complete(self, prompt: str) -> str:
        return f"emitted:{prompt}"


class _NonStringClient:
    """A broken client whose completion violates the docs/01 surface."""

    def complete(self, prompt: str) -> str:
        return 42  # type: ignore[return-value]


# The audit dual of the gate tests' mapping: the harness vocabulary
# is ClosureState, so a refused *move* is reported through the same
# table while an APPROVED move reports Γ's own closure verdict.
_TRANSITION_TO_CLOSURE: dict[TransitionState, ClosureState] = {
    TransitionState.DEFERRED: ClosureState.OPEN,
    TransitionState.BLOCKED: ClosureState.BLOCKED,
    TransitionState.REJECTED: ClosureState.INVALID,
    TransitionState.FORBIDDEN_LEAP: ClosureState.FORBIDDEN_LEAP,
}


def _result_from(audited: AuditedAnswer) -> ConstitutionalChainResult:
    state = (
        audited.gamma_state
        if audited.gate_state is TransitionState.APPROVED
        else _TRANSITION_TO_CLOSURE[audited.gate_state]
    )
    produced: set[str] = set()
    if audited.successor is not None:
        produced.add("SUCCESSOR_SLOTGRAPH")
        produced.add(f"RANK_{audited.successor.rank.name}")
    return ConstitutionalChainResult(
        state=state,
        failure_code=audited.failure_code,
        rank=audited.rank,
        residual_visibility=audited.residual_visibility,
        trace_present=bool(audited.trace_anchor),
        produced_outputs=frozenset(produced),
    )


# ---------------------------------------------------------------------------
# 1. The ModelClient protocol — structural boundary, never an adapter.
# ---------------------------------------------------------------------------


def test_model_client_is_a_structural_protocol_not_an_adapter() -> None:
    """docs/01 — the audit layer may only see ``complete(prompt)``.

    ``runtime_checkable`` makes the check structural: anything with a
    ``complete`` method passes, nothing else does, and the protocol
    itself cannot be instantiated — PR-6 ships no concrete adapter.
    """

    assert isinstance(_EchoClient(), ModelClient)
    assert not isinstance(object(), ModelClient)
    with pytest.raises(TypeError):
        ModelClient()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. Golden emission — APPROVED licenses exactly one successor.
# ---------------------------------------------------------------------------


def test_emit_successor_constructs_licensed_graph_from_approved_verdict() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/17 §1 source 3 — only an APPROVED verdict generates",
        branch_name="approved-verdict-licenses-successor",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RANK_CERTIFICATE", "CERTIFICATE_LAYER_OUTPUT"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.9.Candidate",
        origin_law_ref=(
            "docs/17_SLOTGRAPH_GENERATION_LAW.md#1-the-three-licensed-generation-sources"
        ),
        branch_of_origin="Successor graphs exist only through licensed source 3.",
        forbidden_shortcut_assertions=(
            "Evidence → Certainty",
            "Audit → Approval",
        ),
    )
    graph = _gated_graph()
    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())
    assert verdict.state is TransitionState.APPROVED

    emission = emit_successor(verdict, graph)

    assert not emission.is_refusal
    successor = emission.graph
    assert successor is not None
    # The successor carries exactly what the verdict granted — the
    # emitter never promotes and never re-decides the move.
    assert successor.rank is verdict.granted_rank
    assert successor.rank is Rank.HYPOTHESIS
    assert successor.generation_source is GenerationSource.TRANSITION_VERDICT
    assert successor.output_boundary.declared_layer is Layer.CANDIDATE
    assert successor.output_boundary.output_layer is Layer.CANDIDATE
    # Identity continuity + the named gate preserved in the anchor.
    assert successor.center.identity_claim == graph.center.identity_claim
    assert successor.center.trace_ref.anchor == "trace://Q1/gate/slot-to-candidate"
    assert successor.center.trace_ref.kind == "TRANSITION_VERDICT"
    # The licensed successor itself closes under Γ.
    closure = gamma(successor)
    assert_constitutional_case(
        case,
        ConstitutionalChainResult(
            state=closure.state,
            failure_code=closure.failure_code,
            rank=successor.rank,
            residual_visibility=closure.residual_visibility,
            trace_present=bool(successor.center.trace_ref.anchor),
            produced_outputs=frozenset(
                {"SUCCESSOR_SLOTGRAPH", f"RANK_{successor.rank.name}"}
            ),
        ),
    )


# ---------------------------------------------------------------------------
# 3. Refusal emission — every non-APPROVED verdict licenses nothing.
# ---------------------------------------------------------------------------


def _assert_refusal_emits_nothing(
    case: ConstitutionalChainTestCase,
    graph: SlotGraph,
    target_layer: Layer,
    evidence: EvidenceContract,
    expected_gate_state: TransitionState,
) -> None:
    verdict = _gate().decide(graph, target_layer, evidence)
    assert verdict.state is expected_gate_state

    emission = emit_successor(verdict, graph)

    assert emission.is_refusal
    assert emission.graph is None
    # The emitter propagates the verdict's own named code — it never
    # invents a second judgement about the move.
    assert emission.failure_code is verdict.failure_code
    assert "audit record" in emission.message
    assert_constitutional_case(
        case,
        ConstitutionalChainResult(
            state=_TRANSITION_TO_CLOSURE[verdict.state],
            failure_code=verdict.failure_code,
            rank=verdict.granted_rank,
            residual_visibility=verdict.residual_visibility,
            trace_present=bool(verdict.trace_event_candidate.parent_anchor),
            produced_outputs=frozenset(),
        ),
    )


def test_deferred_verdict_emits_no_successor() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/08 Required preconditions — evidence is non-empty",
        branch_name="deferred-verdict-emits-nothing",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.GATE_REQUIRED,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/08_TRANSITION_GATE.md#required-preconditions",
        branch_of_origin="Absent evidence defers the move; nothing is emitted.",
        forbidden_shortcut_assertions=("Deferral → Successor",),
    )
    _assert_refusal_emits_nothing(
        case,
        _gated_graph(),
        Layer.CANDIDATE,
        EvidenceContract(),
        TransitionState.DEFERRED,
    )


def test_rejected_verdict_emits_no_successor() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/16 link 9 — no rank promotion outside TransitionGate",
        branch_name="rejected-verdict-emits-nothing",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.9.Candidate",
        origin_law_ref="docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md#3-per-link-refusal-mapping",
        branch_of_origin="An ungated rank claim is rejected; nothing is emitted.",
        forbidden_shortcut_assertions=("Rejection → Successor",),
    )
    _assert_refusal_emits_nothing(
        case,
        _declared_graph(rank=Rank.LICENSED),
        Layer.CANDIDATE,
        _strong_evidence(),
        TransitionState.REJECTED,
    )


def test_blocked_verdict_emits_no_successor() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/08 Verdicts — a blocking residual prevents the move",
        branch_name="blocked-verdict-emits-nothing",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.BLOCKED,
        expected_failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/08_TRANSITION_GATE.md#verdicts",
        branch_of_origin="A blocking residual blocks the move; nothing is emitted.",
        forbidden_shortcut_assertions=("Blocked → Successor",),
    )
    _assert_refusal_emits_nothing(
        case,
        _gated_graph(residuals=(_blocking_residual(),)),
        Layer.CANDIDATE,
        _strong_evidence(),
        TransitionState.BLOCKED,
    )


def test_forbidden_leap_verdict_emits_no_successor() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §10 Forbidden straight-line law — Evidence → Certainty",
        branch_name="forbidden-leap-verdict-emits-nothing",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#10-forbidden-straight-line-law",
        branch_of_origin="A forbidden line is fatal; nothing is emitted.",
        forbidden_shortcut_assertions=("Evidence → Certainty",),
    )
    _assert_refusal_emits_nothing(
        case,
        _gated_graph(),
        Layer.CERTIFICATE,
        _strong_evidence(),
        TransitionState.FORBIDDEN_LEAP,
    )


# ---------------------------------------------------------------------------
# 4. Identity continuity — an approval about a different graph.
# ---------------------------------------------------------------------------


def test_emit_successor_refuses_an_approval_about_a_different_graph() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/16 link 2 — identity is stable under licensed ops",
        branch_name="approval-about-a-different-graph",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "Successor"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.IDENTITY_BROKEN,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.2.Stability",
        origin_law_ref="docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md#2-the-ten-licensing-links",
        branch_of_origin="An approval licenses only the graph it judged.",
        forbidden_shortcut_assertions=("ForeignApproval → Successor",),
    )
    approved_graph = _gated_graph()
    verdict = _gate().decide(approved_graph, Layer.CANDIDATE, _strong_evidence())
    assert verdict.state is TransitionState.APPROVED
    other_graph = _gated_graph(anchor="trace://Q2")

    emission = emit_successor(verdict, other_graph)

    assert emission.is_refusal
    assert emission.graph is None
    assert emission.failure_code is FailureCode.IDENTITY_BROKEN
    assert_constitutional_case(
        case,
        ConstitutionalChainResult(
            state=ClosureState.INVALID,
            failure_code=emission.failure_code,
            rank=Rank.ZERO,
            residual_visibility=True,
            trace_present=bool(other_graph.center.trace_ref.anchor),
            produced_outputs=frozenset(),
        ),
    )


# ---------------------------------------------------------------------------
# 5. The audit wrapper — golden flow with the full ledger chain.
# ---------------------------------------------------------------------------


def test_answer_audit_wraps_approved_claim_with_successor_and_ledger_chain() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/01 — the engine wraps emitted claims, never internals",
        branch_name="audit-approved-claim",
        constitutional_chain=(
            "ModelClient",
            "SlotGraph",
            "Gamma",
            "TransitionGate",
            "Successor",
            "AuditedAnswer",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RANK_CERTIFICATE",),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/01_BLACK_BOX_BOUNDARY.md#what-the-engine-does-do",
        branch_of_origin="The audit carries the gate's approval; it never makes one.",
        forbidden_shortcut_assertions=(
            "Audit → Approval",
            "Confidence → Evidence",
        ),
    )
    ledger = TraceLedger()
    audit = AnswerAudit(_EchoClient(), ledger)
    graph = _gated_graph()
    evidence = _strong_evidence()

    audited = audit.audit("What is Q1?", graph, _gate(), Layer.CANDIDATE, evidence)

    assert audited.answer == "emitted:What is Q1?"
    assert audited.gate_state is TransitionState.APPROVED
    assert audited.gamma_state is ClosureState.MINIMALLY_CLOSED
    assert audited.failure_code is None
    assert audited.successor is not None
    assert audited.rank is audited.successor.rank
    assert audited.rank is Rank.HYPOTHESIS
    assert audited.evidence_refs == ("trace://Q1",)
    assert audited.trace_anchor == "trace://Q1"
    # The ledger shows the full constitutional chain, in order, with
    # the PR-6 trace split intact on every entry (docs/07).
    assert len(ledger) == 3
    gamma_entry, gate_entry, audit_entry = ledger.entries
    assert gamma_entry.stage == "gamma"
    assert gamma_entry.consulted_gamma_state is ClosureState.MINIMALLY_CLOSED
    assert gamma_entry.gate_transition_state is None
    assert gate_entry.stage == "gate"
    assert gate_entry.consulted_gamma_state is ClosureState.MINIMALLY_CLOSED
    assert gate_entry.gate_transition_state is TransitionState.APPROVED
    assert audit_entry.stage == "audit"
    assert audit_entry.consulted_gamma_state is ClosureState.MINIMALLY_CLOSED
    assert audit_entry.gate_transition_state is TransitionState.APPROVED
    assert audit_entry.snapshot_failure is None
    assert audit_entry.snapshot_rank is Rank.HYPOTHESIS
    assert audit_entry.parent_anchor == "trace://Q1"
    assert_constitutional_case(case, _result_from(audited))


def test_answer_audit_refusal_leaves_only_an_audit_record() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/08 Required preconditions — evidence is non-empty",
        branch_name="audit-deferred-claim",
        constitutional_chain=(
            "ModelClient",
            "SlotGraph",
            "Gamma",
            "TransitionGate",
            "AuditedAnswer",
        ),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.GATE_REQUIRED,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/08_TRANSITION_GATE.md#required-preconditions",
        branch_of_origin="A refused move leaves an audit record and nothing else.",
        forbidden_shortcut_assertions=("Audit → Approval",),
    )
    ledger = TraceLedger()
    audit = AnswerAudit(_EchoClient(), ledger)

    audited = audit.audit(
        "What is Q1?", _gated_graph(), _gate(), Layer.CANDIDATE, EvidenceContract()
    )

    assert audited.successor is None
    assert audited.gate_state is TransitionState.DEFERRED
    # The split keeps both judgements visible: Γ closed the graph,
    # the gate deferred the move — neither masks the other.
    assert audited.gamma_state is ClosureState.MINIMALLY_CLOSED
    assert audited.failure_code is FailureCode.GATE_REQUIRED
    assert audited.rank is Rank.ZERO
    assert len(ledger) == 3
    gamma_entry, gate_entry, audit_entry = ledger.entries
    assert (gamma_entry.stage, gate_entry.stage, audit_entry.stage) == (
        "gamma",
        "gate",
        "audit",
    )
    assert gate_entry.gate_transition_state is TransitionState.DEFERRED
    assert audit_entry.gate_transition_state is TransitionState.DEFERRED
    assert audit_entry.snapshot_failure is FailureCode.GATE_REQUIRED
    assert audit_entry.snapshot_rank is Rank.ZERO
    assert_constitutional_case(case, _result_from(audited))


# ---------------------------------------------------------------------------
# 6. No audit creates approval by itself — birth guards.
# ---------------------------------------------------------------------------


def test_audited_answer_cannot_be_born_claiming_unlicensed_approval() -> None:
    """docs/01 — the audit layer carries verdicts; it never makes them.

    Birth-guard discipline (the construction-surface precedent): a
    record claiming what no gate granted is a programmer mistake
    refused loudly with ``SlotGraphSchemaError``, never a verdict.
    """

    graph = _gated_graph()
    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())
    successor = emit_successor(verdict, graph).graph
    assert successor is not None
    common = {
        "prompt": "What is Q1?",
        "answer": "emitted",
        "gamma_state": ClosureState.MINIMALLY_CLOSED,
        "evidence_refs": (),
        "residuals": (),
        "residual_visibility": True,
        "trace_anchor": "trace://Q1",
    }

    # A successor without an APPROVED gate verdict.
    with pytest.raises(SlotGraphSchemaError):
        AuditedAnswer(
            gate_state=TransitionState.REJECTED,
            failure_code=None,
            rank=successor.rank,
            successor=successor,
            **common,
        )
    # A successor travelling with a named failure.
    with pytest.raises(SlotGraphSchemaError):
        AuditedAnswer(
            gate_state=TransitionState.APPROVED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=successor.rank,
            successor=successor,
            **common,
        )
    # A successor re-ranked away from the gate's grant.
    with pytest.raises(SlotGraphSchemaError):
        AuditedAnswer(
            gate_state=TransitionState.APPROVED,
            failure_code=None,
            rank=Rank.ZERO,
            successor=successor,
            **common,
        )
    # A successor-less record that names no failure.
    with pytest.raises(SlotGraphSchemaError):
        AuditedAnswer(
            gate_state=TransitionState.DEFERRED,
            failure_code=None,
            rank=Rank.ZERO,
            successor=None,
            **common,
        )
    # A successor-less record licensing a rank anyway.
    with pytest.raises(SlotGraphSchemaError):
        AuditedAnswer(
            gate_state=TransitionState.DEFERRED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=Rank.HYPOTHESIS,
            successor=None,
            **common,
        )


# ---------------------------------------------------------------------------
# 7. Domain guards — programmer mistakes are loud, never verdicts.
# ---------------------------------------------------------------------------


def test_audit_layer_refuses_malformed_construction_and_arguments() -> None:
    ledger = TraceLedger()
    graph = _gated_graph()
    gate = _gate()
    evidence = _strong_evidence()

    # AnswerAudit birth guards.
    with pytest.raises(TypeError):
        AnswerAudit(object(), ledger)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        AnswerAudit(_EchoClient(), object())  # type: ignore[arg-type]

    # audit() argument guards.
    audit = AnswerAudit(_EchoClient(), ledger)
    with pytest.raises(TypeError):
        audit.audit(42, graph, gate, Layer.CANDIDATE, evidence)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        audit.audit("p", "not-a-graph", gate, Layer.CANDIDATE, evidence)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        audit.audit("p", graph, "not-a-gate", Layer.CANDIDATE, evidence)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        audit.audit("p", graph, gate, 3, evidence)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        audit.audit("p", graph, gate, Layer.CANDIDATE, "not-evidence")  # type: ignore[arg-type]

    # A completion that is not a string violates docs/01.
    broken = AnswerAudit(_NonStringClient(), TraceLedger())
    with pytest.raises(TypeError):
        broken.audit("p", graph, gate, Layer.CANDIDATE, evidence)

    # emit_successor domain guards.
    verdict = gate.decide(graph, Layer.CANDIDATE, evidence)
    with pytest.raises(TypeError):
        emit_successor("not-a-verdict", graph)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        emit_successor(verdict, "not-a-graph")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 8. Static guards — no adapter surface, and emission stays pure.
# ---------------------------------------------------------------------------

_AUDIT_MODULES = (
    "taaqqul_slot_geometry.audit",
    "taaqqul_slot_geometry.audit.answer_audit",
    "taaqqul_slot_geometry.audit.model_client",
    "taaqqul_slot_geometry.audit.successor",
)

_FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "anthropic",
    "http",
    "httpx",
    "openai",
    "requests",
    "socket",
    "urllib",
}


def _module_tree(module_name: str) -> ast.Module:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    return ast.parse(source)


def test_audit_layer_ships_no_adapter_and_no_network_surface() -> None:
    """docs/14 — concrete adapters are a post-PR-6 milestone.

    The audit layer must not import any model SDK or network module:
    the only model surface in PR-6 is the ``ModelClient`` protocol.
    """

    for module_name in _AUDIT_MODULES:
        imported: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        leaked = imported & _FORBIDDEN_IMPORT_ROOTS
        assert not leaked, (
            f"{module_name} imports forbidden adapter/network modules: "
            f"{sorted(leaked)} (docs/14 — post-PR-6 milestone)"
        )


def test_emission_module_never_touches_the_trace_ledger() -> None:
    """docs/07 — only the ``AnswerAudit`` shell owns ledger writes.

    The PR-2 purity-guard pattern, applied to the emission half:
    ``successor.py`` must neither import nor reference
    ``TraceLedger``; its result is a value the shell may then record.
    """

    imported: set[str] = set()
    referenced: set[str] = set()
    for node in ast.walk(_module_tree("taaqqul_slot_geometry.audit.successor")):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module)
            for alias in node.names:
                referenced.add(alias.name)
        elif isinstance(node, ast.Name):
            referenced.add(node.id)
        elif isinstance(node, ast.Attribute):
            referenced.add(node.attr)
    assert "TraceLedger" not in referenced
    assert not any("trace_ledger" in module for module in imported)
