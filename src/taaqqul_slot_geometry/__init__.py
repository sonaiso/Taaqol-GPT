"""Taaqqul Slot Geometry — constitutional reasoning engine.

PR-0 shipped the constitutional scaffold. PR-1 establishes the
**Mathematical Slot Geometry Constitution** (docs) plus the minimum
carrier enums those documents reference. The executable ``SlotGraph``
and the ``gamma`` verdict function land in PR-2.

The repository law (see ``docs/02_SLOT_GEOMETRY_CONSTITUTION.md`` and
``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md``):

    SlotGeometry is a constitutional mathematical object,
    not a free data container.

    No output without a SlotGraph.
    No SlotGraph without Constitutional Geometry.
    No Slot without Boundary.
    No Boundary without Domain and Scope.
    No Closure without Gamma.
    No Gamma without Rank and Residual visibility.
    No Output without Trace.
    No transition without a Gate.
    No straight line from Evidence to Certainty.
    No straight line from Tool / Number / LCNV to Knowledge.
    No technical term moves between sciences without a licensed bridge.
"""

from taaqqul_slot_geometry.core import (
    ClosureState,
    FailureCode,
    Rank,
    Residual,
    ResidualKind,
)

__all__: list[str] = [
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
]
