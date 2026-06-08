"""Constitutional chain tests for the PR-2 ``SlotGraph`` + ``Γ`` kernel.

Each test below declares its origin law, branch, and chain position
through :class:`ConstitutionalChainTestCase` (docs/12 §9), exercises
``gamma(graph)``, projects the result into a
:class:`ConstitutionalChainResult`, and feeds both to
:func:`assert_constitutional_case`. Green pytest is **not**
constitutional success unless that helper accepts the comparison.

Coverage mirrors the PR-2 acceptance list:

1.  OPEN — required slot empty.
2.  MINIMALLY_CLOSED — required slots filled, no residuals.
3.  PERFORATED_CLOSED — visible non-blocking residual.
4.  BLOCKED — blocking residual present.
5.  INVALID/HIDDEN_RESIDUAL — hidden residual.
6.  INVALID/CENTER_MISSING — missing center.
7.  INVALID/TRACE_MISSING — missing trace.
8.  FORBIDDEN_LEAP/OUTPUT_EXCEEDS_LAYER — output above declared layer.
9.  Purity — ``Γ`` returns a ``TraceEntryCandidate`` and never
    mutates a ``TraceLedger``; ``gamma.py`` does not import
    ``TraceLedger``.
10. SlotGraph cannot be constructed from a raw value without
    boundary — schema failure at construction time.
"""

from __future__ import annotations

import ast
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry import (
    Center,
    ClosureState,
    FailureCode,
    GenerationSource,
    Layer,
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
    TraceEntryCandidate,
    TraceLedger,
    TraceRef,
    gamma,
)
from taaqqul_slot_geometry.core.gamma import GammaResult
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — keep the graphs minimal and identical across tests
# except in the single axis each test exercises.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="slot-test",
        refusal_codes=(FailureCode.BOUNDARY_MISSING,),
    )


def _opening() -> OpeningPolicy:
    return OpeningPolicy(allowed_potentials=frozenset({"yes", "no"}))


def _filled_slot(name: str = "answer", *, required: bool = True) -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.FILLED,
        boundary=_boundary(),
        opening=_opening(),
        required=required,
        value="yes",
    )


def _empty_slot(name: str = "answer", *, required: bool = True) -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.EMPTY,
        boundary=_boundary(),
        opening=_opening(),
        required=required,
    )


def _broken_slot(name: str = "answer", *, required: bool = True) -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.BROKEN,
        boundary=_boundary(),
        opening=_opening(),
        required=required,
    )


def _center(
    *,
    identity_claim: str = "Q1",
    trace_anchor: str = "trace://Q1",
) -> Center:
    return Center(
        identity_claim=identity_claim,
        domain="reasoning",
        scope="slot-test",
        trace_ref=TraceRef(anchor=trace_anchor, kind="DECLARED_ENTRY"),
    )


def _output_within() -> OutputBoundary:
    return OutputBoundary(declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT)


_MISSING = object()


def _build_graph(
    *,
    center: Center | None | object = _MISSING,
    slots: tuple[Slot, ...] | None = None,
    residuals: tuple[Residual, ...] = (),
    output_boundary: OutputBoundary | None = None,
    rank: Rank = Rank.TRACE,
    generation_source: GenerationSource = GenerationSource.DECLARED_ENTRY,
) -> SlotGraph:
    return SlotGraph(
        center=_center() if center is _MISSING else center,  # type: ignore[arg-type]
        slots=slots if slots is not None else (_filled_slot(),),
        boundary=_boundary(),
        residuals=residuals,
        rank=rank,
        output_boundary=output_boundary
        if output_boundary is not None
        else _output_within(),
        generation_source=generation_source,
    )


def _result_from(verdict: GammaResult) -> ConstitutionalChainResult:
    """Project a :class:`GammaResult` into the harness result type."""

    return ConstitutionalChainResult(
        state=verdict.state,
        failure_code=verdict.failure_code,
        rank=verdict.rank,
        residual_visibility=verdict.residual_visibility,
        trace_present=bool(verdict.trace_event_candidate.parent_anchor),
    )


# ---------------------------------------------------------------------------
# 1. OPEN — required slot empty.
# ---------------------------------------------------------------------------


def test_open_graph_without_required_slots() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §5 Closure Law — required slots must be FILLED",
        branch_name="required-slot-empty",
        constitutional_chain=("SlotGraph", "Gamma", "Opening"),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.TRACE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.6.Opening",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#5-closure-law",
        branch_of_origin="Opening is controlled — closure refused until filled.",
        forbidden_shortcut_assertions=("Opening → Closure",),
    )
    graph = _build_graph(slots=(_empty_slot(),))

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


# ---------------------------------------------------------------------------
# 2. MINIMALLY_CLOSED — required slots filled, no residuals.
# ---------------------------------------------------------------------------


def test_minimally_closed_graph_with_required_slots() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §5 Closure Law — minimal closure",
        branch_name="all-required-filled-no-residuals",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "ResidualVisibility",
            "Trace",
            "OutputBoundary",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "CERTIFICATE",
            "CANDIDATE_WITH_HIDDEN_RESIDUAL",
        ),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#5-closure-law",
        branch_of_origin="Closure is established (minimal, no residuals).",
        forbidden_shortcut_assertions=(
            "Closure → Certificate",
            "Closure → Truth",
        ),
    )
    graph = _build_graph()

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    # Additional structural assertions binding the verdict to docs/03.
    assert verdict.failure_code is None
    assert verdict.trace_event_candidate.snapshot_state is (
        ClosureState.MINIMALLY_CLOSED
    )


# ---------------------------------------------------------------------------
# 3. PERFORATED_CLOSED — visible non-blocking residual preserved.
# ---------------------------------------------------------------------------


def test_perforated_closed_graph_with_visible_non_blocking_residual() -> None:
    residual = Residual(
        name="explanation-pending",
        kind=ResidualKind.NON_BLOCKING,
        visible=True,
        note="follow-up note visible in output",
    )
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §6 Perforated Closure Law",
        branch_name="visible-non-blocking-residual-preserved",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "ResidualVisibility",
            "Trace",
        ),
        expected_state=ClosureState.PERFORATED_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#6-perforated-closure-law",
        branch_of_origin="Closure with declared non-blocking residual.",
        forbidden_shortcut_assertions=(
            "PerforatedClosure → Certificate",
            "Candidate → Truth",
        ),
    )
    graph = _build_graph(residuals=(residual,))

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    # The residual is preserved in the verdict (not silently dropped).
    assert verdict.residuals == (residual,)
    assert verdict.residual_visibility is True


# ---------------------------------------------------------------------------
# 4. BLOCKED — blocking residual present.
# ---------------------------------------------------------------------------


def test_blocked_graph_with_blocking_residual() -> None:
    residual = Residual(
        name="missing-precondition",
        kind=ResidualKind.BLOCKING,
        visible=True,
    )
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual Visibility / Blocking residual law",
        branch_name="blocking-residual-present",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualPolicy"),
        expected_state=ClosureState.BLOCKED,
        expected_failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.TRACE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="A blocking residual blocks closure.",
        forbidden_shortcut_assertions=("Closure → Approval (with BLOCKING)",),
    )
    graph = _build_graph(residuals=(residual,))

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


# ---------------------------------------------------------------------------
# 5. INVALID — hidden residual.
# ---------------------------------------------------------------------------


def test_hidden_residual_is_invalid_not_approved() -> None:
    hidden = Residual(
        name="hidden-cost",
        kind=ResidualKind.HIDDEN_FORBIDDEN,
        visible=False,
    )
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual Visibility Law — fatality clause",
        branch_name="hidden-residual-refused",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualVisibility"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.HIDDEN_RESIDUAL,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.TRACE,
        required_trace=True,
        # The residual visibility check is the very thing being tested;
        # declaring it as a required axis would tautologically pass.
        required_residual_visibility=False,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="A hidden residual is INVALID, never approved.",
        forbidden_shortcut_assertions=("HiddenResidual → ApprovedOutput",),
    )
    graph = _build_graph(residuals=(hidden,))

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.residual_visibility is False


# ---------------------------------------------------------------------------
# 6. INVALID — missing center.
# ---------------------------------------------------------------------------


def test_missing_center_is_invalid() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §2 Center Law",
        branch_name="missing-center",
        constitutional_chain=("SlotGraph", "Gamma", "Center"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.CENTER_MISSING,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.TRACE,
        required_trace=False,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.1.Identity",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#2-center-law",
        branch_of_origin="A SlotGraph with no Center is INVALID.",
        forbidden_shortcut_assertions=("Identity → Truth",),
    )
    graph = _build_graph(center=None)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


# ---------------------------------------------------------------------------
# 7. INVALID — missing trace.
# ---------------------------------------------------------------------------


def test_missing_trace_is_invalid() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §2 Center Law — trace_ref clause",
        branch_name="missing-trace",
        constitutional_chain=("SlotGraph", "Gamma", "Trace"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.TRACE_MISSING,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.TRACE,
        required_trace=False,  # tested axis is the absence itself
        required_residual_visibility=True,
        chain_position="IdentityChain.link.1.Identity",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#2-center-law",
        branch_of_origin="A Center without a Trace is INVALID.",
        forbidden_shortcut_assertions=("Identity → Truth (without trace)",),
    )
    no_trace_center = Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="slot-test",
        trace_ref=None,
    )
    graph = _build_graph(center=no_trace_center)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


# ---------------------------------------------------------------------------
# 8. FORBIDDEN_LEAP — output exceeds declared layer.
# ---------------------------------------------------------------------------


def test_forbidden_leap_when_output_exceeds_boundary() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §5 Closure Law — output_boundary ⪯ declared_layer",
        branch_name="output-exceeds-declared-layer",
        constitutional_chain=("SlotGraph", "Gamma", "OutputBoundary"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.OUTPUT_EXCEEDS_LAYER,
        forbidden_outputs=("APPROVED_OUTPUT", "CANDIDATE", "CERTIFICATE"),
        max_rank=Rank.TRACE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#5-closure-law",
        branch_of_origin="Output above declared layer is a forbidden leap.",
        forbidden_shortcut_assertions=(
            "Slot → Certificate (no Gate)",
            "Evidence → Certainty",
        ),
    )
    over_layer = OutputBoundary(
        declared_layer=Layer.SLOT, output_layer=Layer.CERTIFICATE
    )
    graph = _build_graph(output_boundary=over_layer)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


# ---------------------------------------------------------------------------
# 9. Purity — ``Γ`` returns a candidate and never mutates a ledger.
# ---------------------------------------------------------------------------


def test_gamma_returns_trace_entry_candidate_without_mutating_ledger() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §7 / docs/03 — Γ is pure (no ledger append)",
        branch_name="gamma-is-pure",
        constitutional_chain=("SlotGraph", "Gamma", "TraceLedgerPurity"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/03_GAMMA_CLOSURE_CONTRACT.md#purity-law",
        branch_of_origin="Γ produces a candidate; the caller appends.",
        forbidden_shortcut_assertions=("Γ → LedgerAppend (without caller)",),
    )
    graph = _build_graph()
    ledger = TraceLedger()
    snapshot_len = len(ledger)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    # The candidate is a value, not a side effect.
    assert isinstance(verdict.trace_event_candidate, TraceEntryCandidate)
    # No ledger mutation occurred.
    assert len(ledger) == snapshot_len
    assert ledger.entries == ()
    # The caller is the only path that can write the candidate.
    ledger.append(verdict.trace_event_candidate)
    assert ledger.entries == (verdict.trace_event_candidate,)


def test_gamma_module_does_not_import_traceledger_class() -> None:
    """Static guard from docs/07 *PR-2 binding*:

        gamma.py must not import TraceLedger; the constitutional
        purity rule will be enforced by a static guard in the PR-2
        test suite.

    Importing :class:`TraceEntryCandidate` is allowed and required.
    Importing :class:`TraceLedger` would let a careless future
    refactor turn ``Γ`` into a function with side effects, breaking
    the purity law.
    """

    spec = importlib.util.find_spec("taaqqul_slot_geometry.core.gamma")
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_names.add(alias.name)
    assert "TraceLedger" not in imported_names, (
        "gamma.py must not import TraceLedger (docs/07 purity guard)"
    )
    # Belt and braces: no attribute reference to TraceLedger either.
    referenced = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    } | {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    assert "TraceLedger" not in referenced, (
        "gamma.py must not reference the TraceLedger symbol "
        "(docs/07 purity guard)"
    )


# ---------------------------------------------------------------------------
# 10. Cannot construct a SlotGraph from a raw value without boundary.
# ---------------------------------------------------------------------------


def test_slotgraph_cannot_be_constructed_from_raw_value_without_boundary() -> None:
    """docs/17 §4 — *forbidden: SlotGraph(slots={...}) — free container*.

    The PR-2 ``SlotGraph`` constructor refuses any attempt to be
    born from a raw value: ``boundary`` is a required field with no
    default, and every nested carrier is type-checked at
    construction time. Passing a raw string where the constructor
    expects rich carriers raises :class:`SlotGraphSchemaError`
    (which is a :class:`TypeError`).
    """

    # Form A — bare positional ``SlotGraph("raw")`` is rejected by
    # Python: the constructor requires multiple keyword fields and
    # has no ``from_raw_value`` / ``from_text`` shortcut.
    with pytest.raises(TypeError):
        SlotGraph("raw")  # type: ignore[call-arg]

    # Form B — omitting ``boundary`` is rejected too: the docs/17 §2
    # mandatory-fields list has no default for the perimeter
    # declaration. Constructing the graph without the boundary
    # keyword raises a ``TypeError`` from Python's dataclass
    # machinery.
    with pytest.raises(TypeError):
        SlotGraph(  # type: ignore[call-arg]
            center=_center(),
            slots=(_filled_slot(),),
            # boundary intentionally omitted.
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.DECLARED_ENTRY,
        )

    # Form C — passing a raw dict where a ``SlotBoundary`` is
    # required is refused at the schema layer with the named
    # exception subtype.
    with pytest.raises(SlotGraphSchemaError):
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary={"domain": "x", "scope": "y"},  # type: ignore[arg-type]
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.DECLARED_ENTRY,
        )


# ---------------------------------------------------------------------------
# Bonus: step-order short-circuit — a BROKEN slot is INVALID/IDENTITY_BROKEN.
# Not in the §6 enumeration but required to keep the docs/03 ordered table
# bound to executable behaviour.
# ---------------------------------------------------------------------------


def test_broken_slot_is_invalid_identity_broken() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/03 step 4 — no slot with BROKEN value_state",
        branch_name="broken-slot",
        constitutional_chain=("SlotGraph", "Gamma", "Identity"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.IDENTITY_BROKEN,
        forbidden_outputs=("APPROVED_OUTPUT",),
        max_rank=Rank.TRACE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.1.Identity",
        origin_law_ref="docs/03_GAMMA_CLOSURE_CONTRACT.md#the-ordered-closure-law",
        branch_of_origin="A BROKEN slot breaks identity.",
        forbidden_shortcut_assertions=("Identity → Truth",),
    )
    graph = _build_graph(slots=(_broken_slot(),))

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
