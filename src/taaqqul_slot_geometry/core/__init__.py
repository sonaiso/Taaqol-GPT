"""PR-1 carrier surface.

PR-1 ships **names, not behaviour**: the constitutional documents that
govern ``SlotGraph``/``Γ``/``Gate`` plus the minimum carrier enums that
those documents and their tests need to reference. The executable
``SlotGraph`` and ``gamma`` land in PR-2.

See ``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md``.
"""

from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind

__all__ = [
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
]
