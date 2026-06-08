"""Taaqqul Slot Geometry — constitutional reasoning engine.

PR-1 lands the kernel: ``SlotGraph`` + the pure ``gamma`` verdict
function. ``Rank`` and ``Residual`` are exposed as carriers only; the
lattice meet, the residual engine, the transition gate, and the
forbidden-transition registry land in later PRs.

The repository law (see ``docs/02_SLOT_GEOMETRY_CONSTITUTION.md``):

    No output without a SlotGraph.
    No SlotGraph without a Gamma closure state.
    No transition without a Gate.
    No Gate without Evidence, Rank, and a Residual policy.
    No approved output with hidden residuals.
    No straight line from Evidence to Certainty.
    No straight line from Tool / Number / LCNV to Knowledge.
    No technical term moves between sciences without a licensed bridge.
"""

from taaqqul_slot_geometry.core import (
    FailureCode,
    GammaResult,
    GammaState,
    Layer,
    Rank,
    Residual,
    ResidualKind,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotState,
    TraceEntryCandidate,
    TraceLedger,
    gamma,
)

__all__: list[str] = [
    "FailureCode",
    "GammaResult",
    "GammaState",
    "Layer",
    "Rank",
    "Residual",
    "ResidualKind",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotState",
    "TraceEntryCandidate",
    "TraceLedger",
    "gamma",
]
