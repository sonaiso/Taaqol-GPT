"""Core carrier surface.

PR-1A shipped **names, not behaviour**: the constitutional documents
that govern ``SlotGraph``/``Γ``/``Gate`` plus the minimum carrier enums
those documents and their tests reference. This ``__init__``
intentionally re-exports only that PR-1A carrier surface
(``ClosureState``, ``FailureCode``, ``Rank``, ``Residual``,
``ResidualKind``); it does not re-export the executable kernel.
The kernel — ``SlotGraph`` and ``gamma`` (PR-2, hardened by PR-2A),
``RankLattice`` / ``ResidualPolicy`` / ``EvidenceContract`` (PR-3),
``TransitionGate`` (PR-4), the Forbidden Straight-Line Registry
(PR-5) — lives in the sibling ``core.*`` submodules, and its
canonical public import surface is the package top level,
``taaqqul_slot_geometry``.

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
