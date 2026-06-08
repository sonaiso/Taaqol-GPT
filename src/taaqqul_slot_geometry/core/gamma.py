"""Gamma closure — the pure verdict function for ``SlotGraph``.

``gamma(graph)`` returns one of six verdicts defined in
``docs/03_GAMMA_CLOSURE_CONTRACT.md``. It is pure: it never raises for
expected verdicts, never performs I/O, and never appends to a ledger.
Every refusal carries a named ``FailureCode``.

Note on imports: this module intentionally does **not** import
``TraceLedger``. A static guard in ``tests/test_gamma_purity.py``
enforces this.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.residual_policy import ResidualKind
from taaqqul_slot_geometry.core.slot_graph import SlotGraph, SlotState
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate


class GammaState(StrEnum):
    """The six gamma verdicts."""

    OPEN = "OPEN"
    MINIMALLY_CLOSED = "MINIMALLY_CLOSED"
    PERFORATED_CLOSED = "PERFORATED_CLOSED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


@dataclass(frozen=True, slots=True)
class GammaResult:
    """Immutable verdict returned by ``gamma``."""

    state: GammaState
    failure_code: FailureCode | None
    trace_event_candidate: TraceEntryCandidate
    reasons: tuple[str, ...] = ()


_STAGE = "gamma"


def _input_ref(graph: SlotGraph) -> str:
    """Deterministic short id for the input graph.

    Uses ``repr`` of the frozen dataclass tree; ``hashlib`` is
    standard library, so no new dependency is introduced and no I/O
    is performed.
    """

    return hashlib.sha256(repr(graph).encode("utf-8")).hexdigest()[:16]


def _residual_names(graph: SlotGraph) -> tuple[str, ...]:
    return tuple(r.name for r in graph.residuals)


def _build(
    graph: SlotGraph,
    state: GammaState,
    failure_code: FailureCode | None,
    reasons: tuple[str, ...],
) -> GammaResult:
    candidate = TraceEntryCandidate(
        stage=_STAGE,
        input_ref=_input_ref(graph),
        verdict=state.value,
        failure_code=failure_code,
        residuals_seen=_residual_names(graph),
        notes=reasons,
    )
    return GammaResult(
        state=state,
        failure_code=failure_code,
        trace_event_candidate=candidate,
        reasons=reasons,
    )


def gamma(graph: SlotGraph) -> GammaResult:
    """Pure verdict function for ``SlotGraph``.

    Evaluates the PR-1 decision table in fixed precedence order; see
    ``docs/03_GAMMA_CLOSURE_CONTRACT.md`` for the binding table.
    """

    # 1. Identity broken — any BROKEN slot drives the graph to INVALID.
    broken = [s.name for s in graph.slots if s.state == SlotState.BROKEN]
    if broken:
        reasons = tuple(f"slot {name!r} is BROKEN" for name in broken)
        return _build(graph, GammaState.INVALID, FailureCode.IDENTITY_BROKEN, reasons)

    # 2. Hidden residual — HIDDEN_FORBIDDEN kind or visible=False.
    hidden = [
        r.name
        for r in graph.residuals
        if r.kind == ResidualKind.HIDDEN_FORBIDDEN or not r.visible
    ]
    if hidden:
        reasons = tuple(f"residual {name!r} is hidden" for name in hidden)
        return _build(graph, GammaState.INVALID, FailureCode.HIDDEN_RESIDUAL, reasons)

    # 3. Forbidden leap — output_boundary strictly above declared_layer.
    if graph.output_boundary is not None and graph.output_boundary > graph.declared_layer:
        reasons = (
            f"output_boundary {graph.output_boundary.name} exceeds "
            f"declared_layer {graph.declared_layer.name}",
        )
        return _build(
            graph, GammaState.FORBIDDEN_LEAP, FailureCode.OUTPUT_EXCEEDS_LAYER, reasons
        )

    # 4. Blocking residual present.
    blocking = [r.name for r in graph.residuals if r.kind == ResidualKind.BLOCKING]
    if blocking:
        reasons = tuple(f"residual {name!r} is BLOCKING" for name in blocking)
        return _build(
            graph, GammaState.BLOCKED, FailureCode.BLOCKING_RESIDUAL_PRESENT, reasons
        )

    # 5. Open — any required slot is EMPTY.
    empty_required = [
        s.name for s in graph.slots if s.required and s.state == SlotState.EMPTY
    ]
    if empty_required:
        reasons = tuple(f"required slot {name!r} is EMPTY" for name in empty_required)
        return _build(graph, GammaState.OPEN, FailureCode.REQUIRED_SLOT_EMPTY, reasons)

    # 6 / 7. Closed: perforated if any residual remains, else minimally closed.
    if graph.residuals:
        reasons = tuple(
            f"declared residual {r.name!r} ({r.kind.value})" for r in graph.residuals
        )
        return _build(graph, GammaState.PERFORATED_CLOSED, None, reasons)

    return _build(graph, GammaState.MINIMALLY_CLOSED, None, ())


__all__ = ["GammaResult", "GammaState", "gamma"]
