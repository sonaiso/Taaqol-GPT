"""Constitutional tests for the PR-4 ``TransitionGate`` + FailureTaxonomy bindings.

Coverage mirrors the PR-4 acceptance list — the five propositions the
gate must prove, plus the gate-side disciplines:

1.  Evidence rank is not truth — strong evidence licenses at most the
    §8 meet, never a verdict above it, and never the ``CERTIFICATE``
    layer through this gate.
2.  Certificate evidence is not transition approval — a single
    ``CERTIFICATE`` source aggregates to ``STRONG`` (docs/11 §8), and
    even a ``CERTIFICATE``-rank pool meets ``GATE_RANK_CEILING``:
    no PR-4 verdict can grant ``CERTIFICATE``.
3.  No rank promotion outside ``TransitionGate`` — an ungated graph
    claiming a rank above ``UNGATED_RANK_CEILING`` is ``REJECTED`` /
    ``RANK_PROMOTION_WITHOUT_GATE`` (docs/16 link 9).
4.  Residual ceiling participates in meet only — a ``DEFERRABLE``
    surface caps the granted rank at ``HYPOTHESIS`` but never sets a
    rank by itself.
5.  Every rejection has ``FailureCode`` — each refusal state carries
    a named code; the verdict carrier refuses birth otherwise.

Disciplines: ``Γ`` runs before any gate (docs/11 §11); the certificate
bar precedes every retryable refusal (docs/16 §4); every verdict
proposes a ``stage="gate"`` :class:`TraceEntryCandidate` (docs/08
precondition 4); birth guards refuse malformed gates and verdicts
loudly (docs/11 §12); and the module never touches the
``TraceLedger`` (the PR-2 purity guard pattern).

Verdict-producing tests declare themselves through
:class:`ConstitutionalChainTestCase` (docs/12 §9) and are checked by
:func:`assert_constitutional_case`. Birth-guard and domain-guard
tests follow the construction-surface precedent: ``pytest.raises``
on the programmer mistake, never on a constitutional verdict.
"""

from __future__ import annotations

import ast
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry import (
    GATE_RANK_CEILING,
    UNGATED_RANK_CEILING,
    Center,
    ClosureState,
    EntryBoundary,
    EvidenceContract,
    EvidenceSource,
    FailureCode,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    RankLattice,
    Residual,
    ResidualKind,
    ResidualPolicy,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceEntryCandidate,
    TraceRef,
    TransitionGate,
    TransitionState,
    TransitionVerdict,
    gamma,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — identical in shape to the Γ kernel and PR-3
# tests; each gate test varies only the single axis it exercises.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="gate-test",
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


def _empty_slot(name: str = "answer") -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.EMPTY,
        boundary=_boundary(),
        opening=_opening(),
        required=True,
    )


def _trace_ref(kind: str = "DECLARED_ENTRY") -> TraceRef:
    return TraceRef(anchor="trace://Q1", kind=kind)


def _center(trace_kind: str = "DECLARED_ENTRY") -> Center:
    return Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="gate-test",
        trace_ref=_trace_ref(trace_kind),
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


def _build_graph(
    *,
    slots: tuple[Slot, ...] | None = None,
    residuals: tuple[Residual, ...] = (),
    rank: Rank = Rank.TRACE,
    output_boundary: OutputBoundary | None = None,
) -> SlotGraph:
    """A ``DECLARED_ENTRY`` graph — the ungated origin."""

    return SlotGraph(
        center=_center(),
        slots=slots if slots is not None else (_filled_slot(),),
        boundary=_boundary(),
        residuals=residuals,
        rank=rank,
        output_boundary=output_boundary if output_boundary is not None else _output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),
    )


def _gated_graph(
    *,
    residuals: tuple[Residual, ...] = (),
    rank: Rank = Rank.HYPOTHESIS,
) -> SlotGraph:
    """A graph that *is* the product of a prior transition verdict.

    ``generation_source=TRANSITION_VERDICT`` is the only origin
    licensed to carry a gate-granted rank into a further gate
    (docs/16 link 9; docs/17 §1 source 3).
    """

    return SlotGraph(
        center=_center("TRANSITION_VERDICT"),
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


def _gate_candidate(rank: Rank = Rank.ZERO) -> TraceEntryCandidate:
    return TraceEntryCandidate(
        parent_anchor="trace://Q1",
        stage="gate",
        snapshot_state=ClosureState.MINIMALLY_CLOSED,
        snapshot_failure=None,
        snapshot_rank=rank,
    )


# A gate verdict speaks about a *move*; the harness speaks
# ``ClosureState``. An APPROVED move reports the consulted Γ closure
# state (the gate approves a move on a closed graph); every refusal
# reports the ``ClosureState`` dual of its ``TransitionState``
# (docs/08 verdict table beside docs/03's six verdicts).
_TRANSITION_TO_CLOSURE: dict[TransitionState, ClosureState] = {
    TransitionState.DEFERRED: ClosureState.OPEN,
    TransitionState.BLOCKED: ClosureState.BLOCKED,
    TransitionState.REJECTED: ClosureState.INVALID,
    TransitionState.FORBIDDEN_LEAP: ClosureState.FORBIDDEN_LEAP,
}


def _result_from(verdict: TransitionVerdict) -> ConstitutionalChainResult:
    state = (
        verdict.gamma_state
        if verdict.state is TransitionState.APPROVED
        else _TRANSITION_TO_CLOSURE[verdict.state]
    )
    return ConstitutionalChainResult(
        state=state,
        failure_code=verdict.failure_code,
        rank=verdict.granted_rank,
        residual_visibility=verdict.residual_visibility,
        trace_present=bool(verdict.trace_event_candidate.parent_anchor),
    )


# ---------------------------------------------------------------------------
# 1. Birth guards — a malformed gate or verdict is a programmer
#    mistake refused loudly, never a constitutional verdict
#    (docs/11 §12; the Residual precedent of PR-3-FIX).
# ---------------------------------------------------------------------------


def test_transition_gate_cannot_be_born_malformed() -> None:
    """docs/11 §12 — missing means refuse: a malformed gate can never
    decide anything because it can never be born."""

    with pytest.raises(TypeError):
        TransitionGate(name="", gate_rank=Rank.LICENSED)
    with pytest.raises(TypeError):
        TransitionGate(name="   ", gate_rank=Rank.LICENSED)
    with pytest.raises(TypeError):
        TransitionGate(name=3, gate_rank=Rank.LICENSED)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        TransitionGate(name="slot-to-candidate", gate_rank="STRONG")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        TransitionGate(name="slot-to-candidate", gate_rank=5)  # type: ignore[arg-type]


def test_certificate_granting_gate_cannot_be_born() -> None:
    """docs/04 — ``Candidate → Certificate`` requires a
    ``CertificationGate`` (PR-5). The PR-4 birth cap makes a
    ``CERTIFICATE``-granting gate structurally impossible."""

    assert GATE_RANK_CEILING is Rank.STRONG
    with pytest.raises(TypeError) as excinfo:
        TransitionGate(name="certifier", gate_rank=Rank.CERTIFICATE)
    assert "CertificationGate" in str(excinfo.value)
    # The cap binds strictly above STRONG: a STRONG gate is licit.
    strong_gate = TransitionGate(name="strong-gate", gate_rank=Rank.STRONG)
    assert strong_gate.gate_rank is Rank.STRONG


def test_transition_verdict_cannot_be_born_malformed() -> None:
    """docs/08 precondition 5 — every refusal is named; an approval
    carries no failure; a refusal licenses nothing. The carrier
    refuses birth otherwise (docs/11 §12), so no code path can ever
    hand a caller an unnamed refusal or a granting rejection."""

    with pytest.raises(SlotGraphSchemaError):
        TransitionVerdict(
            state=TransitionState.APPROVED,
            failure_code=FailureCode.GATE_REQUIRED,
            granted_rank=Rank.ZERO,
            gamma_state=ClosureState.MINIMALLY_CLOSED,
            residual_visibility=True,
            trace_event_candidate=_gate_candidate(),
        )
    with pytest.raises(SlotGraphSchemaError):
        TransitionVerdict(
            state=TransitionState.REJECTED,
            failure_code=None,
            granted_rank=Rank.ZERO,
            gamma_state=ClosureState.INVALID,
            residual_visibility=True,
            trace_event_candidate=_gate_candidate(),
        )
    with pytest.raises(SlotGraphSchemaError):
        TransitionVerdict(
            state=TransitionState.REJECTED,
            failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            granted_rank=Rank.LICENSED,  # a refusal licenses nothing
            gamma_state=ClosureState.INVALID,
            residual_visibility=True,
            trace_event_candidate=_gate_candidate(),
        )
    with pytest.raises(SlotGraphSchemaError):
        TransitionVerdict(
            state="APPROVED",  # type: ignore[arg-type]
            failure_code=None,
            granted_rank=Rank.ZERO,
            gamma_state=ClosureState.MINIMALLY_CLOSED,
            residual_visibility=True,
            trace_event_candidate=_gate_candidate(),
        )


def test_decide_refuses_ill_typed_arguments_loudly() -> None:
    """Mirrors ``gamma``'s domain guard: a wrong *type* of argument
    is a programmer mistake (``TypeError``), never a verdict."""

    gate = _gate()
    with pytest.raises(TypeError):
        gate.decide("not-a-graph", Layer.CANDIDATE, _strong_evidence())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        gate.decide(_gated_graph(), 3, _strong_evidence())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        gate.decide(_gated_graph(), Layer.CANDIDATE, ())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 2. Γ runs before any Gate (docs/11 §11) — a Γ refusal maps to the
#    docs/08 verdict table carrying Γ's own named code unchanged.
# ---------------------------------------------------------------------------


def test_open_graph_is_deferred_with_gamma_failure_named() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §11 — Γ runs before any Gate",
        branch_name="gate-consults-gamma-open-graph",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate"),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.6.Opening",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#11-no-data-container-law",
        branch_of_origin="An open graph defers the move; the gate never fills a slot.",
        forbidden_shortcut_assertions=("Opening → Closure",),
    )
    graph = _build_graph(slots=(_empty_slot(),))

    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.DEFERRED
    assert verdict.granted_rank is Rank.ZERO, "a deferred move licenses nothing"


def test_blocking_residual_blocks_the_move() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/08 Verdicts — a blocking residual prevents the move",
        branch_name="gate-consults-gamma-blocking-residual",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualPolicy", "TransitionGate"),
        expected_state=ClosureState.BLOCKED,
        expected_failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/08_TRANSITION_GATE.md#verdicts",
        branch_of_origin="A blocking residual blocks the move; the gate names Γ's code.",
        forbidden_shortcut_assertions=("Closure → Certificate",),
    )
    blocking = Residual(name="hard-stop", kind=ResidualKind.BLOCKING, visible=True)
    graph = _build_graph(residuals=(blocking,))

    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.BLOCKED


def test_hidden_residual_rejects_the_move_with_visibility_exposed() -> None:
    """docs/11 §9 — no approved output with hidden residuals. The
    verdict reports ``residual_visibility=False``: the gate never
    hides what ``Γ`` saw."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual visibility law — hidden residual",
        branch_name="gate-consults-gamma-hidden-residual",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualPolicy", "TransitionGate"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.HIDDEN_RESIDUAL,
        forbidden_outputs=("APPROVED", "CERTIFICATE", "MINIMALLY_CLOSED"),
        max_rank=Rank.ZERO,
        required_trace=True,
        # The hidden surface IS the branch under test: visibility is
        # expected to be reported false, never required true.
        required_residual_visibility=False,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="A hidden residual is named and rejected; visibility reports false.",
        forbidden_shortcut_assertions=("Closure → Certificate",),
    )
    hidden = Residual(name="quiet-gap", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False)
    graph = _build_graph(residuals=(hidden,))

    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.REJECTED
    assert verdict.residual_visibility is False, "the gate must expose, never hide"


def test_output_exceeding_layer_is_a_forbidden_leap_at_the_gate() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §7 Gamma closure — output exceeds declared layer",
        branch_name="gate-consults-gamma-output-exceeds-layer",
        constitutional_chain=("SlotGraph", "Gamma", "OutputBoundary", "TransitionGate"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.OUTPUT_EXCEEDS_LAYER,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#7-gamma-closure-function",
        branch_of_origin="A graph above its declared layer cannot move anywhere.",
        forbidden_shortcut_assertions=("Closure → Certificate",),
    )
    exceeding = OutputBoundary(declared_layer=Layer.SLOT, output_layer=Layer.CANDIDATE)
    graph = _build_graph(output_boundary=exceeding)

    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.FORBIDDEN_LEAP


# ---------------------------------------------------------------------------
# 3. The canonical forbidden straight line (docs/11 §10; docs/16
#    link 10): Evidence → Certainty has no direct path.
# ---------------------------------------------------------------------------


def test_evidence_to_certainty_direct_is_forbidden_even_with_strong_evidence() -> None:
    """The canonical negative test docs/12 names. A ``CERTIFICATE``
    target through the generic gate is ``FORBIDDEN_STRAIGHT_LINE``
    even under a certificate-rank evidence pool."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §10 Forbidden straight-line law — Evidence → Certainty",
        branch_name="certificate-target-with-certificate-pool",
        constitutional_chain=("SlotGraph", "Gamma", "EvidenceContract", "TransitionGate"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#10-forbidden-straight-line-law",
        branch_of_origin="Evidence → Certainty stays forbidden until the CertificationGate (PR-5).",
        forbidden_shortcut_assertions=(
            "Evidence → Certainty",
            "Candidate → Certificate",
            "Closure → Certificate",
        ),
    )
    pool = EvidenceContract(
        sources=(_evidence("e1", Rank.CERTIFICATE), _evidence("e2", Rank.CERTIFICATE))
    )
    assert pool.evidence_rank is Rank.CERTIFICATE  # the pool really is that strong

    verdict = _gate(Rank.STRONG).decide(_gated_graph(), Layer.CERTIFICATE, pool)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.FORBIDDEN_LEAP
    assert verdict.granted_rank is Rank.ZERO, "the forbidden line licenses nothing"


def test_certificate_bar_precedes_every_retryable_refusal() -> None:
    """The ordered decide law: the certificate bar (step 2) precedes
    the evidence check (step 4) — an empty contract on a
    ``CERTIFICATE`` target is the fatal ``FORBIDDEN_STRAIGHT_LINE``,
    never the retryable ``GATE_REQUIRED``."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/16 §4 — forbidden lines bind before retryable deferrals",
        branch_name="certificate-target-with-empty-evidence",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        forbidden_outputs=("APPROVED", "CERTIFICATE", "DEFERRED"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref=(
            "docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md"
            "#4-the-six-new-forbidden-straight-lines"
        ),
        branch_of_origin="A fatal forbidden line is never downgraded into a retryable deferral.",
        forbidden_shortcut_assertions=("Evidence → Certainty",),
    )
    verdict = _gate().decide(_gated_graph(), Layer.CERTIFICATE, EvidenceContract())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.failure_code is not FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 4. No rank promotion outside TransitionGate (docs/16 link 9).
# ---------------------------------------------------------------------------


def test_ungated_licensed_rank_is_rejected_as_promotion() -> None:
    """docs/16 link 9 — ``Candidate → Truth``: a ``DECLARED_ENTRY``
    graph claiming a gate-licensed rank is rejected even though
    ``Γ`` closes it — the closure is licit; the *claim* into a gate
    is not. Step 3 precedes step 4: the refusal binds even on an
    empty evidence surface."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/16 link 9 — no rank promotion outside TransitionGate",
        branch_name="ungated-graph-claims-licensed-rank",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "RankLattice"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.9.Candidate",
        origin_law_ref="docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md#3-per-link-refusal-mapping",
        branch_of_origin="Candidate → Truth is refused: only a gate's verdict licenses a rank.",
        forbidden_shortcut_assertions=("Candidate → Truth",),
    )
    assert UNGATED_RANK_CEILING is Rank.HYPOTHESIS
    graph = _build_graph(rank=Rank.LICENSED)  # ungated DECLARED_ENTRY origin
    assert gamma(graph).failure_code is None, "Γ closes the graph; the gate refuses the claim"

    verdict = _gate().decide(graph, Layer.CANDIDATE, EvidenceContract())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.REJECTED
    assert verdict.failure_code is not FailureCode.GATE_REQUIRED, (
        "the promotion refusal precedes the evidence check"
    )


def test_gated_graph_may_carry_its_licensed_rank_onward() -> None:
    """docs/17 §1 source 3 — the discrimination is on the generation
    source: a ``TRANSITION_VERDICT`` graph carrying ``LICENSED`` is
    not a promotion claim, and the meet keeps it."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/16 link 9 — gated rank is carried, not promoted",
        branch_name="gated-graph-carries-licensed-rank",
        constitutional_chain=("SlotGraph", "Gamma", "TransitionGate", "RankLattice"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.LICENSED,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.9.Candidate",
        origin_law_ref=(
            "docs/17_SLOTGRAPH_GENERATION_LAW.md#1-the-three-licensed-generation-sources"
        ),
        branch_of_origin="A transition-verdict origin may carry its granted rank into a gate.",
        forbidden_shortcut_assertions=("Candidate → Truth",),
    )
    graph = _gated_graph(rank=Rank.LICENSED)

    verdict = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.APPROVED
    # meet(STRONG evidence, LICENSED identity, LICENSED gate, TOP ceiling)
    assert verdict.granted_rank is Rank.LICENSED


# ---------------------------------------------------------------------------
# 5. Evidence presence — GATE_REQUIRED defers; retry is permitted
#    (docs/08 precondition 1 + verdict table; docs/16 link 10).
# ---------------------------------------------------------------------------


def test_empty_evidence_defers_with_gate_required_then_licenses_on_retry() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/08 Required preconditions — evidence is non-empty",
        branch_name="empty-evidence-surface-defers",
        constitutional_chain=("SlotGraph", "Gamma", "EvidenceContract", "TransitionGate"),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.GATE_REQUIRED,
        forbidden_outputs=("APPROVED", "CERTIFICATE"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/08_TRANSITION_GATE.md#required-preconditions",
        branch_of_origin="Absent evidence defers the move; it does not forbid it.",
        forbidden_shortcut_assertions=("Evidence → Certainty",),
    )
    graph = _gated_graph()

    deferred = _gate().decide(graph, Layer.CANDIDATE, EvidenceContract())

    assert_constitutional_case(case, _result_from(deferred))
    assert deferred.state is TransitionState.DEFERRED

    retried = _gate().decide(graph, Layer.CANDIDATE, _strong_evidence())
    assert retried.state is TransitionState.APPROVED, "retry is permitted once evidence arrives"
    assert retried.failure_code is None


# ---------------------------------------------------------------------------
# 6. The §8 meet — approval grants exactly the bounded meet; the
#    residual ceiling participates in the meet only; certificate
#    evidence never grants CERTIFICATE.
# ---------------------------------------------------------------------------


def test_approval_grants_exactly_the_section8_meet() -> None:
    """docs/11 §8 — ``rank_out ≤ meet(evidence, identity, gate,
    residual ceiling)``: the gate grants exactly the meet, the single
    bounded place a rank is ever granted."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §8 Rank ceiling law — the bounded meet",
        branch_name="approval-grants-the-meet",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "EvidenceContract",
            "RankLattice",
            "TransitionGate",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#8-rank-ceiling-law",
        branch_of_origin="The granted rank is the meet of its licensing components.",
        forbidden_shortcut_assertions=("Evidence → Certainty", "Candidate → Certificate"),
    )
    graph = _gated_graph(rank=Rank.HYPOTHESIS)
    gate = _gate(Rank.LICENSED)
    evidence = _strong_evidence()

    verdict = gate.decide(graph, Layer.CANDIDATE, evidence)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.APPROVED
    expected = RankLattice.meet(
        evidence.evidence_rank,
        graph.rank,
        gate.gate_rank,
        ResidualPolicy.ceiling(graph.residuals),
    )
    assert verdict.granted_rank is expected
    assert verdict.granted_rank is Rank.HYPOTHESIS
    assert verdict.granted_rank <= evidence.evidence_rank, "evidence rank is not truth"


def test_residual_ceiling_participates_in_meet_only() -> None:
    """docs/06 + docs/11 §9 — the ``DEFERRABLE`` cap enters the meet
    and bounds the grant from above; with weaker evidence the meet
    lands *below* the ceiling — the ceiling never sets a rank."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual visibility law — ceiling in the meet",
        branch_name="deferrable-cap-binds-inside-the-meet",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "ResidualPolicy",
            "RankLattice",
            "TransitionGate",
        ),
        expected_state=ClosureState.PERFORATED_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE", "MINIMALLY_CLOSED"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.8.Implication",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="The ceiling caps the grant; the residual stays visible in the verdict.",
        forbidden_shortcut_assertions=("Implication → Truth",),
    )
    deferrable = Residual(name="open-question", kind=ResidualKind.DEFERRABLE, visible=True)
    graph = _gated_graph(residuals=(deferrable,), rank=Rank.HYPOTHESIS)
    gate = _gate(Rank.STRONG)

    capped = gate.decide(graph, Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(capped))
    # meet(STRONG evidence, HYPOTHESIS identity, STRONG gate,
    # HYPOTHESIS ceiling) — the cap holds the grant at the ceiling.
    assert capped.granted_rank is Rank.HYPOTHESIS

    weak = gate.decide(
        graph, Layer.CANDIDATE, EvidenceContract(sources=(_evidence("w1", Rank.TRACE),))
    )
    assert weak.state is TransitionState.APPROVED
    assert weak.granted_rank is Rank.TRACE, (
        "the ceiling participates in the meet only — it never sets a rank"
    )


def test_single_certificate_source_never_grants_certificate() -> None:
    """docs/11 §8 corollary — a single ``CERTIFICATE`` source
    aggregates to ``STRONG``; and even a ``CERTIFICATE``-rank *pool*
    meets ``GATE_RANK_CEILING``: certificate evidence is not
    transition approval, and no PR-4 verdict grants CERTIFICATE."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §8 Rank ceiling law — single source never licenses CERTIFICATE",
        branch_name="certificate-evidence-grants-at-most-strong",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "EvidenceContract",
            "RankLattice",
            "TransitionGate",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.STRONG,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#8-rank-ceiling-law",
        branch_of_origin="Certificate-rank evidence licenses a move, never a certificate.",
        forbidden_shortcut_assertions=("Evidence → Certainty", "Candidate → Certificate"),
    )
    graph = _gated_graph(rank=Rank.STRONG)
    gate = _gate(Rank.STRONG)

    single = EvidenceContract(sources=(_evidence("e1", Rank.CERTIFICATE),))
    verdict = gate.decide(graph, Layer.CANDIDATE, single)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.granted_rank is Rank.STRONG
    assert verdict.granted_rank < Rank.CERTIFICATE

    pool = EvidenceContract(
        sources=(_evidence("e1", Rank.CERTIFICATE), _evidence("e2", Rank.CERTIFICATE))
    )
    pooled = gate.decide(graph, Layer.CANDIDATE, pool)
    assert pooled.granted_rank is Rank.STRONG, (
        "even a certificate-rank pool meets GATE_RANK_CEILING: "
        "CERTIFICATE is structurally ungrantable in PR-4"
    )


# ---------------------------------------------------------------------------
# 7. Trace discipline and purity (docs/08 precondition 4; docs/07).
# ---------------------------------------------------------------------------


def test_every_verdict_proposes_a_gate_stage_trace_candidate() -> None:
    """docs/08 precondition 4 — every verdict, approval or refusal,
    proposes a ``stage="gate"`` candidate snapshotting both the Γ
    consultation and the gate's decision. The candidate is a value;
    the gate itself never appends (docs/07)."""

    approved = _gate().decide(_gated_graph(), Layer.CANDIDATE, _strong_evidence())
    refused = _gate().decide(_gated_graph(), Layer.CERTIFICATE, _strong_evidence())
    assert approved.state is TransitionState.APPROVED
    assert refused.state is TransitionState.FORBIDDEN_LEAP

    for verdict in (approved, refused):
        candidate = verdict.trace_event_candidate
        assert candidate.stage == "gate"
        assert candidate.parent_anchor == "trace://Q1"
        assert candidate.snapshot_state is verdict.gamma_state
        assert candidate.snapshot_failure is verdict.failure_code
        assert candidate.snapshot_rank is verdict.granted_rank


def test_transition_gate_module_never_touches_the_ledger() -> None:
    """The PR-2 purity guard, extended to the gate (docs/07 — the
    ledger lives outside the pure core): ``transition_gate.py``
    neither imports nor references ``TraceLedger``."""

    spec = importlib.util.find_spec("taaqqul_slot_geometry.core.transition_gate")
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_names.add(alias.name)
    assert "TraceLedger" not in imported_names, (
        "transition_gate.py must not import TraceLedger (docs/07 purity guard)"
    )
    referenced = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    } | {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    assert "TraceLedger" not in referenced, (
        "transition_gate.py must not reference the TraceLedger symbol "
        "(docs/07 purity guard)"
    )
