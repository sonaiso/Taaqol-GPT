"""Coverage of the six gamma verdicts (PR-1 decision table).

Test names match the directive exactly.
"""

from __future__ import annotations

from taaqqul_slot_geometry import (
    FailureCode,
    GammaState,
    Layer,
    Residual,
    ResidualKind,
    Slot,
    SlotGraph,
    SlotState,
    TraceEntryCandidate,
    TraceLedger,
    gamma,
)


def _required(name: str, state: SlotState) -> Slot:
    return Slot(name=name, required=True, state=state)


def test_open_graph_without_required_slots() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.EMPTY),),
    )
    result = gamma(graph)
    assert result.state == GammaState.OPEN
    assert result.failure_code == FailureCode.REQUIRED_SLOT_EMPTY


def test_minimally_closed_graph_with_required_slots() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED), _required("b", SlotState.FILLED)),
    )
    result = gamma(graph)
    assert result.state == GammaState.MINIMALLY_CLOSED
    assert result.failure_code is None


def test_perforated_closed_graph_with_non_blocking_residuals() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
        residuals=(
            Residual(name="r1", kind=ResidualKind.NON_BLOCKING, visible=True),
        ),
    )
    result = gamma(graph)
    assert result.state == GammaState.PERFORATED_CLOSED
    assert result.failure_code is None


def test_blocked_graph_with_blocking_residual() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
        residuals=(
            Residual(name="r1", kind=ResidualKind.BLOCKING, visible=True),
        ),
    )
    result = gamma(graph)
    assert result.state == GammaState.BLOCKED
    assert result.failure_code == FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_invalid_graph_with_identity_break() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(
            _required("a", SlotState.FILLED),
            _required("b", SlotState.BROKEN),
        ),
    )
    result = gamma(graph)
    assert result.state == GammaState.INVALID
    assert result.failure_code == FailureCode.IDENTITY_BROKEN


def test_forbidden_leap_when_output_exceeds_layer() -> None:
    # Generic layer ordering used here; no Forbidden Straight-Line Registry.
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
        declared_layer=Layer.L1_FORM,
        output_boundary=Layer.L3_JUDGMENT,
    )
    result = gamma(graph)
    assert result.state == GammaState.FORBIDDEN_LEAP
    assert result.failure_code == FailureCode.OUTPUT_EXCEEDS_LAYER


def test_hidden_residual_is_invalid_not_approved() -> None:
    # Case A: kind == HIDDEN_FORBIDDEN.
    graph_a = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
        residuals=(
            Residual(name="r1", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=True),
        ),
    )
    result_a = gamma(graph_a)
    assert result_a.state == GammaState.INVALID
    assert result_a.failure_code == FailureCode.HIDDEN_RESIDUAL

    # Case B: visible=False on an otherwise non-blocking residual.
    graph_b = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
        residuals=(
            Residual(name="r2", kind=ResidualKind.NON_BLOCKING, visible=False),
        ),
    )
    result_b = gamma(graph_b)
    assert result_b.state == GammaState.INVALID
    assert result_b.failure_code == FailureCode.HIDDEN_RESIDUAL
    assert result_b.state not in {GammaState.MINIMALLY_CLOSED, GammaState.PERFORATED_CLOSED}


def test_gamma_returns_trace_entry_candidate_without_mutating_ledger() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(_required("a", SlotState.FILLED),),
    )
    ledger = TraceLedger()
    result = gamma(graph)
    # gamma must return a TraceEntryCandidate inside its result.
    assert isinstance(result.trace_event_candidate, TraceEntryCandidate)
    assert result.trace_event_candidate.stage == "gamma"
    assert result.trace_event_candidate.verdict == result.state.value
    # gamma must not have touched the ledger.
    assert len(ledger) == 0
    assert ledger.entries == ()
    # The caller — and only the caller — appends.
    ledger.append(result.trace_event_candidate)
    assert len(ledger) == 1
