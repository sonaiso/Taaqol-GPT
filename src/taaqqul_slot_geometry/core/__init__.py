"""PR-1 kernel: SlotGraph + GammaClosure (Rank/Residual as carriers only).

See ``docs/02_SLOT_GEOMETRY_CONSTITUTION.md`` and
``docs/03_GAMMA_CLOSURE_CONTRACT.md`` for the binding contract.
"""

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.gamma import GammaResult, GammaState, gamma
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import (
    Layer,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotState,
)
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate, TraceLedger

__all__ = [
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
