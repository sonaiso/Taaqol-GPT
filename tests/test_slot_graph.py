"""Structural invariants for ``SlotGraph`` and friends (PR-1)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry import (
    Layer,
    Rank,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotState,
)


def _slot(name: str, state: SlotState = SlotState.FILLED, required: bool = True) -> Slot:
    return Slot(name=name, required=required, state=state)


def test_slot_graph_is_frozen() -> None:
    graph = SlotGraph(center="c", slots=(_slot("a"),))
    with pytest.raises(FrozenInstanceError):
        graph.center = "other"  # type: ignore[misc]


def test_slot_is_frozen() -> None:
    slot = _slot("a")
    with pytest.raises(FrozenInstanceError):
        slot.required = False  # type: ignore[misc]


def test_slot_boundary_is_frozen() -> None:
    boundary = SlotBoundary(name="b")
    with pytest.raises(FrozenInstanceError):
        boundary.name = "other"  # type: ignore[misc]


def test_duplicate_slot_names_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate slot name"):
        SlotGraph(center="c", slots=(_slot("a"), _slot("a")))


def test_edge_referencing_unknown_slot_rejected() -> None:
    with pytest.raises(ValueError, match="unknown slot"):
        SlotGraph(
            center="c",
            slots=(_slot("a"),),
            edges=(("a", "ghost"),),
        )


def test_defaults_are_minimal() -> None:
    graph = SlotGraph(center="c", slots=(_slot("a"),))
    assert graph.edges == ()
    assert graph.constraints == ()
    assert graph.residuals == ()
    assert graph.rank == Rank.ZERO
    assert graph.declared_layer == Layer.L0_RAW
    assert graph.output_boundary is None
    assert graph.trace_ref is None
