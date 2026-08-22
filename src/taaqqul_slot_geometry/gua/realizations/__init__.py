"""GUA realization builders over the frozen general core."""

from taaqqul_slot_geometry.gua.core.geometry import CoreFreeze
from taaqqul_slot_geometry.gua.core.realization import RealizationContract
from taaqqul_slot_geometry.gua.realizations.language import build_language_realization
from taaqqul_slot_geometry.gua.realizations.mathematics import build_mathematics_realization
from taaqqul_slot_geometry.gua.realizations.physics import build_physics_realization
from taaqqul_slot_geometry.gua.realizations.programming import build_programming_realization


def build_default_realizations(
    core_freeze: CoreFreeze, trace_ref: str
) -> tuple[RealizationContract, ...]:
    """Build the four licensed GUA-1 realization contracts."""

    return (
        build_language_realization(core_freeze, trace_ref),
        build_mathematics_realization(core_freeze, trace_ref),
        build_physics_realization(core_freeze, trace_ref),
        build_programming_realization(core_freeze, trace_ref),
    )


__all__ = [
    "build_default_realizations",
    "build_language_realization",
    "build_mathematics_realization",
    "build_physics_realization",
    "build_programming_realization",
]
