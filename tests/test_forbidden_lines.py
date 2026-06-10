"""Constitutional tests for the PR-5 Forbidden Straight-Line Registry.

Coverage mirrors the PR-5 acceptance list — the registry the
constitution names, plus the binding that makes the generic gate
consult it:

1.  Birth guards — a malformed row or registry is a programmer
    mistake refused loudly with ``TypeError`` (docs/11 §12), never a
    constitutional verdict.
2.  Query domain guards — ill-typed query arguments are refused
    loudly, mirroring the gate's domain guard.
3.  The docs/04 query contract — ``is_forbidden_direct`` answers the
    canonical table, matching is strip + casefold, and every row
    names its ``required_bridge``.
4.  The docs/16 §4 merger — all six chain lines are rows of the
    canonical registry ("must be merged into the registry that lands
    in PR-5").
5.  The pre-text declared-entry table (docs/04; docs/11 §13) is
    registered, including the row whose bridge is constitutionally
    ``none``.
6.  The governing law's compound row — ``Tool / Number / LCNV →
    Knowledge`` — answers the query contract for each name.
7.  Row completeness — every row of both surfaces names its bridge,
    its origin, and emits ``FORBIDDEN_STRAIGHT_LINE``; the canonical
    instance holds exactly the module tuples.
8.  Terminology transfers are a separate mechanism (docs/10): the
    domain-leap surface never answers the layer-leap query, and vice
    versa.
9.  **The golden binding** — the generic ``TransitionGate`` consults
    the registry before the retryable evidence check: a fatal
    forbidden line never degrades into ``GATE_REQUIRED``.
10. Licit moves stay approved — the registry consultation adds no
    refusal to an unregistered pair (the PR-4 regression guard).
11. The purity guard — ``forbidden_lines.py`` never touches the
    ``TraceLedger`` (docs/07).
12. The consultation is structural — the gate module really imports
    and references ``CANONICAL_REGISTRY`` (docs/08 step 2, PR-5
    binding).

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
    CANONICAL_REGISTRY,
    FORBIDDEN_STRAIGHT_LINES,
    TERMINOLOGY_TRANSFERS,
    Center,
    ClosureState,
    EvidenceContract,
    EvidenceSource,
    FailureCode,
    ForbiddenLine,
    ForbiddenLineRegistry,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotState,
    TerminologyTransfer,
    TraceRef,
    TransitionGate,
    TransitionState,
    TransitionVerdict,
    is_forbidden_direct,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — identical in shape to the gate tests; each
# registry test varies only the single axis it exercises.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="registry-test",
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


def _trace_ref(kind: str = "DECLARED_ENTRY") -> TraceRef:
    return TraceRef(anchor="trace://Q1", kind=kind)


def _center(trace_kind: str = "DECLARED_ENTRY") -> Center:
    return Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="registry-test",
        trace_ref=_trace_ref(trace_kind),
    )


def _output_within() -> OutputBoundary:
    return OutputBoundary(declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT)


def _gated_graph(rank: Rank = Rank.HYPOTHESIS) -> SlotGraph:
    """A graph that *is* the product of a prior transition verdict
    (docs/17 §1 source 3) — the only origin licensed to carry a
    gate-granted rank into a further gate."""

    return SlotGraph(
        center=_center("TRANSITION_VERDICT"),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
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


# A gate verdict speaks about a *move*; the harness speaks
# ``ClosureState`` (docs/08 verdict table beside docs/03's six
# verdicts) — the same adapter the gate tests use.
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
# 1. Birth guards — a malformed row or registry is a programmer
#    mistake refused loudly, never a constitutional verdict
#    (docs/11 §12; the TransitionGate carrier precedent).
# ---------------------------------------------------------------------------


def test_forbidden_line_cannot_be_born_malformed() -> None:
    """docs/11 §12 — missing means refuse: a row that names no
    source, no bridge, or no FailureCode can never enter a registry
    because it can never be born."""

    with pytest.raises(TypeError):
        ForbiddenLine(
            source="",
            target="Certainty",
            reason="r",
            required_bridge="b",
            origin_law="docs/04",
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    with pytest.raises(TypeError):
        ForbiddenLine(
            source="Evidence",
            target="Certainty",
            reason="r",
            required_bridge="   ",
            origin_law="docs/04",
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    with pytest.raises(TypeError):
        ForbiddenLine(
            source="Evidence",
            target="Certainty",
            reason=3,  # type: ignore[arg-type]
            required_bridge="b",
            origin_law="docs/04",
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    with pytest.raises(TypeError):
        ForbiddenLine(
            source="Evidence",
            target="Certainty",
            reason="r",
            required_bridge="b",
            origin_law="docs/04",
            failure_code="FORBIDDEN_STRAIGHT_LINE",  # type: ignore[arg-type]
        )


def test_terminology_transfer_cannot_be_born_malformed() -> None:
    """docs/10 row schema — every field of ``(term, source_domain,
    target_domain, required_bridge)`` is mandatory at birth."""

    with pytest.raises(TypeError):
        TerminologyTransfer(
            term="",
            source_domain="logic",
            target_domain="mathematics",
            required_bridge="TerminologyBridgeGate",
            origin_law="docs/10",
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    with pytest.raises(TypeError):
        TerminologyTransfer(
            term="qiyās",
            source_domain="logic",
            target_domain=None,  # type: ignore[arg-type]
            required_bridge="TerminologyBridgeGate",
            origin_law="docs/10",
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    with pytest.raises(TypeError):
        TerminologyTransfer(
            term="qiyās",
            source_domain="logic",
            target_domain="mathematics",
            required_bridge="TerminologyBridgeGate",
            origin_law="docs/10",
            failure_code=None,  # type: ignore[arg-type]
        )


def test_registry_cannot_be_born_malformed() -> None:
    """The registry is a constitutional value, not a free container:
    its surfaces are tuples of the two named row carriers only."""

    row = FORBIDDEN_STRAIGHT_LINES[0]
    with pytest.raises(TypeError):
        ForbiddenLineRegistry(lines=[row])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ForbiddenLineRegistry(lines=(row, "Evidence -> Certainty"))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ForbiddenLineRegistry(lines=(row,), term_transfers=[TERMINOLOGY_TRANSFERS[0]])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ForbiddenLineRegistry(lines=(row,), term_transfers=(row,))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 2. Query domain guards — a wrong *type* of argument is a
#    programmer mistake refused loudly, mirroring the gate's
#    domain guard; it is never a silent ``False``.
# ---------------------------------------------------------------------------


def test_queries_refuse_ill_typed_arguments_loudly() -> None:
    with pytest.raises(TypeError):
        CANONICAL_REGISTRY.find(3, "Certainty")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        CANONICAL_REGISTRY.find("Evidence", None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        CANONICAL_REGISTRY.is_forbidden_direct(Layer.CANDIDATE, Layer.CERTIFICATE)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        CANONICAL_REGISTRY.find_term_transfer(3, "logic", "mathematics")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        CANONICAL_REGISTRY.is_forbidden_term_transfer("qiyās", None, "mathematics")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 3. The docs/04 query contract over the canonical table.
# ---------------------------------------------------------------------------


def test_registry_answers_the_docs04_query_contract() -> None:
    """docs/04 — the registry is "queried by ``is_forbidden_direct
    (src, tgt)``". Matching is strip + casefold so the ``Layer``
    enum names meet the constitutional row names; an unregistered
    pair is not forbidden; every hit names its bridge."""

    assert CANONICAL_REGISTRY.is_forbidden_direct("Evidence", "Certainty")
    assert is_forbidden_direct("Evidence", "Certainty"), (
        "the module-level contract answers over the canonical instance"
    )
    assert CANONICAL_REGISTRY.is_forbidden_direct("CANDIDATE", "CERTIFICATE"), (
        "matching is case-insensitive so Layer names meet the rows"
    )
    assert CANONICAL_REGISTRY.is_forbidden_direct("  Evidence  ", "Certainty"), (
        "matching strips whitespace"
    )
    assert not CANONICAL_REGISTRY.is_forbidden_direct("Slot", "Candidate"), (
        "an unregistered pair is not a forbidden straight line"
    )

    line = CANONICAL_REGISTRY.find("Candidate", "Certificate")
    assert line is not None
    assert line.required_bridge == "CertificationGate"
    assert line.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE

    evidence_line = CANONICAL_REGISTRY.find("Evidence", "Certainty")
    assert evidence_line is not None
    assert evidence_line.required_bridge == "RankLattice (no auto-promote)"


def test_every_docs16_chain_line_is_merged_into_the_registry() -> None:
    """docs/16 §4 — the six new forbidden straight lines "must be
    merged into the registry that lands in PR-5". This is that
    merger, proven row by row."""

    chain_pairs = (
        ("Identity", "Truth"),
        ("Matching", "Meaning"),
        ("Potentiality", "Actuality"),
        ("Opening", "Closure"),
        ("Closure", "Certificate"),
        ("Candidate", "Truth"),
    )
    for source, target in chain_pairs:
        row = CANONICAL_REGISTRY.find(source, target)
        assert row is not None, f"docs/16 §4 line {source} → {target} is not registered"
        assert row.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
        assert row.origin_law.startswith("docs/16"), (
            f"{source} → {target} must carry its docs/16 §4 origin"
        )


def test_pre_text_declared_entry_rows_are_registered() -> None:
    """docs/04 pre-text table (docs/11 §13) — the declared-entry
    moves are rows of the same registry, including the one whose
    bridge is constitutionally ``none``: a declared entry never
    becomes an ontological origin."""

    assert CANONICAL_REGISTRY.is_forbidden_direct("HumanVoice", "ArabicText")
    assert CANONICAL_REGISTRY.is_forbidden_direct("BinaryAudio", "Meaning")

    no_bridge = CANONICAL_REGISTRY.find("DeclaredEntry", "OntologicalOrigin")
    assert no_bridge is not None
    assert no_bridge.required_bridge.startswith("none"), (
        "docs/04: no bridge will ever open this line — the refusal is constitutional"
    )


def test_tool_number_lcnv_each_answer_the_governing_law() -> None:
    """The governing law: ``No straight line from Tool / Number /
    LCNV to Knowledge``. The compound docs/04 row answers the query
    contract for each of its three names."""

    for source in ("Tool", "Number", "LCNV"):
        row = CANONICAL_REGISTRY.find(source, "Knowledge")
        assert row is not None, f"{source} → Knowledge is not registered"
        assert row.required_bridge == "ToolBoundaryGate"
        assert row.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_every_row_names_its_bridge_and_failure_code() -> None:
    """docs/04 + docs/16 §4 — every row emits the named
    ``FORBIDDEN_STRAIGHT_LINE`` until its bridge opens; no row is
    anonymous about its bridge or its origin. The canonical instance
    holds exactly the module tuples — no hidden rows, no dropped
    rows."""

    assert len(FORBIDDEN_STRAIGHT_LINES) > 0
    for row in FORBIDDEN_STRAIGHT_LINES:
        assert row.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
        assert row.required_bridge.strip()
        assert row.origin_law.strip()

    assert len(TERMINOLOGY_TRANSFERS) > 0
    for transfer in TERMINOLOGY_TRANSFERS:
        assert transfer.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
        assert transfer.required_bridge.strip()
        assert transfer.origin_law.strip()

    assert CANONICAL_REGISTRY.lines == FORBIDDEN_STRAIGHT_LINES
    assert CANONICAL_REGISTRY.term_transfers == TERMINOLOGY_TRANSFERS


# ---------------------------------------------------------------------------
# 4. docs/10 — terminology transfers are a separate mechanism from
#    layer leaps; the two surfaces never collapse into one.
# ---------------------------------------------------------------------------


def test_terminology_transfers_are_a_separate_mechanism() -> None:
    """docs/10 keeps the terminology law separate from docs/04 "so
    that future contributors do not collapse them into one
    mechanism": a domain leap answers only the term-transfer query,
    never the layer-leap query, and vice versa."""

    assert CANONICAL_REGISTRY.is_forbidden_term_transfer("qiyās", "logic", "uṣūl al-fiqh")
    assert not CANONICAL_REGISTRY.is_forbidden_direct("logic", "uṣūl al-fiqh"), (
        "a domain pair is not a layer leap — the surfaces stay distinct"
    )
    assert CANONICAL_REGISTRY.find_term_transfer("Evidence", "Certainty", "anywhere") is None, (
        "a layer leap is not a terminology transfer — the surfaces stay distinct"
    )

    transfer = CANONICAL_REGISTRY.find_term_transfer("qiyās", "logic", "uṣūl al-fiqh")
    assert transfer is not None
    assert transfer.required_bridge == "TerminologyBridgeGate"
    assert transfer.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE

    # The starting docs/10 cases hold in their stated directions only:
    # ``cause`` is fixed in physics; ``sabab`` is fixed in fiqh.
    assert CANONICAL_REGISTRY.is_forbidden_term_transfer("cause", "physics", "fiqh")
    assert not CANONICAL_REGISTRY.is_forbidden_term_transfer("cause", "fiqh", "physics"), (
        "the registry holds the declared rows only; it synthesises no reverse row"
    )


# ---------------------------------------------------------------------------
# 5. The golden binding — the generic gate consults the registry
#    before the retryable evidence check (docs/08 step 2, PR-5).
# ---------------------------------------------------------------------------


def test_generic_gate_consults_forbidden_line_registry_before_evidence_retry() -> None:
    """The PR-5 golden test: a registered forbidden line is *fatal* —
    it must never degrade into the retryable ``GATE_REQUIRED``. The
    move ``CANDIDATE → CERTIFICATE`` with an *empty* evidence surface
    would defer at step 4; the registry row binds at step 2 first,
    so the verdict is ``FORBIDDEN_LEAP`` / ``FORBIDDEN_STRAIGHT_LINE``
    and no retry is ever invited."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/04 — registered forbidden lines bind before retryable deferrals",
        branch_name="registered-line-with-empty-evidence",
        constitutional_chain=("SlotGraph", "Gamma", "ForbiddenLineRegistry", "TransitionGate"),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        forbidden_outputs=("APPROVED", "CERTIFICATE", "DEFERRED", "GATE_REQUIRED"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.10.EvidenceBoundTruth",
        origin_law_ref="docs/04_FORBIDDEN_STRAIGHT_LINES.md#canonical-forbidden-transitions",
        branch_of_origin="A fatal forbidden line never becomes a retryable GATE_REQUIRED.",
        forbidden_shortcut_assertions=("Candidate → Certificate", "Evidence → Certainty"),
    )

    # The line the gate must consult really is registered.
    line = CANONICAL_REGISTRY.find(Layer.CANDIDATE.name, Layer.CERTIFICATE.name)
    assert line is not None
    assert line.required_bridge == "CertificationGate"

    verdict = _gate().decide(_gated_graph(), Layer.CERTIFICATE, EvidenceContract())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.FORBIDDEN_LEAP
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.failure_code is not FailureCode.GATE_REQUIRED, (
        "a fatal forbidden line must not become GATE_REQUIRED"
    )
    assert verdict.granted_rank is Rank.ZERO, "a registered line licenses nothing"


def test_registry_consultation_leaves_licit_moves_approved() -> None:
    """The PR-4 regression guard: consulting the registry adds no
    refusal to an unregistered pair — a gated graph moving within
    its declared layer under strong evidence is still approved."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/08 — the registry consultation refuses only registered lines",
        branch_name="unregistered-pair-stays-approved",
        constitutional_chain=("SlotGraph", "Gamma", "ForbiddenLineRegistry", "TransitionGate"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.LICENSED,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.9.Candidate",
        origin_law_ref="docs/08_TRANSITION_GATE.md#pr-5-binding",
        branch_of_origin="An unregistered pair passes step 2 untouched and meets normally.",
        forbidden_shortcut_assertions=("Candidate → Certificate",),
    )

    assert CANONICAL_REGISTRY.find(Layer.CANDIDATE.name, Layer.CANDIDATE.name) is None, (
        "the exercised pair really is unregistered"
    )

    verdict = _gate().decide(_gated_graph(), Layer.CANDIDATE, _strong_evidence())

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.state is TransitionState.APPROVED
    assert verdict.failure_code is None


# ---------------------------------------------------------------------------
# 6. Purity + structural-binding guards.
# ---------------------------------------------------------------------------


def _module_ast(module_name: str) -> ast.AST:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    return ast.parse(source)


def test_forbidden_lines_module_never_touches_the_ledger() -> None:
    """The PR-2 purity guard, extended to the registry (docs/07 —
    the ledger lives outside the pure core): ``forbidden_lines.py``
    neither imports nor references ``TraceLedger``."""

    tree = _module_ast("taaqqul_slot_geometry.core.forbidden_lines")
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_names.add(alias.name)
    assert "TraceLedger" not in imported_names, (
        "forbidden_lines.py must not import TraceLedger (docs/07 purity guard)"
    )
    referenced = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    } | {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "TraceLedger" not in referenced, (
        "forbidden_lines.py must not reference the TraceLedger symbol "
        "(docs/07 purity guard)"
    )


def test_gate_consults_the_canonical_registry() -> None:
    """docs/08 step 2 (PR-5 binding) is structural, not incidental:
    ``transition_gate.py`` imports ``CANONICAL_REGISTRY`` from the
    registry module and references it in its decision path."""

    tree = _module_ast("taaqqul_slot_geometry.core.transition_gate")
    imports_registry = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "taaqqul_slot_geometry.core.forbidden_lines"
        and any(alias.name == "CANONICAL_REGISTRY" for alias in node.names)
        for node in ast.walk(tree)
    )
    assert imports_registry, (
        "transition_gate.py must import CANONICAL_REGISTRY from "
        "taaqqul_slot_geometry.core.forbidden_lines (docs/08 step 2)"
    )
    referenced = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "CANONICAL_REGISTRY" in referenced, (
        "transition_gate.py must consult CANONICAL_REGISTRY in its decision path"
    )
