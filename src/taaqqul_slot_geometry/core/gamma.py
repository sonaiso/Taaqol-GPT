from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .slot_graph import Rank, Residual, ResidualKind, SlotGraph, TraceRef


class GammaClosureState(str, Enum):
    OPEN = "OPEN"
    MINIMALLY_CLOSED = "MINIMALLY_CLOSED"
    PERFORATED_CLOSED = "PERFORATED_CLOSED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


@dataclass(frozen=True)
class GammaResult:
    state: GammaClosureState
    graph: SlotGraph
    trace: TraceRef
    rank: Rank
    output_layer: int
    residuals: tuple[Residual, ...] = ()
    missing_required_slots: tuple[str, ...] = ()
    limited_candidate: bool = False


PERFORATING_RESIDUALS = {
    ResidualKind.DEFERRABLE,
    ResidualKind.NON_BLOCKING,
    ResidualKind.EXPLANATORY,
}
BLOCKING_RESIDUALS = {
    ResidualKind.BLOCKING,
    ResidualKind.HIDDEN_FORBIDDEN,
}


def close_slot_graph(graph: SlotGraph, requested_output_layer: int | None = None) -> GammaResult:
    output_layer = graph.layer if requested_output_layer is None else requested_output_layer

    if not graph.trace.trace_id or not graph.center.strip() or not graph.identity_ok:
        return GammaResult(
            state=GammaClosureState.INVALID,
            graph=graph,
            trace=graph.trace,
            rank=Rank.ZERO,
            output_layer=output_layer,
            residuals=graph.residuals,
        )

    if not graph.allows_output_layer(output_layer):
        return GammaResult(
            state=GammaClosureState.FORBIDDEN_LEAP,
            graph=graph,
            trace=graph.trace,
            rank=Rank.ZERO,
            output_layer=output_layer,
            residuals=graph.residuals,
        )

    blocking_residuals = tuple(
        residual for residual in graph.residuals if residual.kind in BLOCKING_RESIDUALS
    )
    if blocking_residuals:
        return GammaResult(
            state=GammaClosureState.BLOCKED,
            graph=graph,
            trace=graph.trace,
            rank=Rank.ZERO,
            output_layer=output_layer,
            residuals=blocking_residuals,
        )

    missing_required_slots = graph.missing_required_slots()
    if missing_required_slots:
        return GammaResult(
            state=GammaClosureState.OPEN,
            graph=graph,
            trace=graph.trace,
            rank=Rank.TRACE,
            output_layer=output_layer,
            residuals=graph.residuals,
            missing_required_slots=missing_required_slots,
        )

    perforating_residuals = tuple(
        residual for residual in graph.residuals if residual.kind in PERFORATING_RESIDUALS
    )
    if perforating_residuals:
        return GammaResult(
            state=GammaClosureState.PERFORATED_CLOSED,
            graph=graph,
            trace=graph.trace,
            rank=Rank.CANDIDATE,
            output_layer=output_layer,
            residuals=perforating_residuals,
            limited_candidate=True,
        )

    return GammaResult(
        state=GammaClosureState.MINIMALLY_CLOSED,
        graph=graph,
        trace=graph.trace,
        rank=Rank.LICENSED,
        output_layer=output_layer,
        residuals=graph.residuals,
    )
