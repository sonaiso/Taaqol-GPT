"""Language realization over the frozen GUA general core."""

from __future__ import annotations

from taaqqul_slot_geometry.gua.core.geometry import CoreFreeze
from taaqqul_slot_geometry.gua.core.realization import RealizationContract
from taaqqul_slot_geometry.gua.core.slot import TypedSlot
from taaqqul_slot_geometry.gua.core.transition import TransitionContract


def build_language_realization(core_freeze: CoreFreeze, trace_ref: str) -> RealizationContract:
    """Build the language realization contract from a frozen general core."""

    slot = TypedSlot(
        slot_type="unit",
        domain_id="language",
        coordinates=("token", "order"),
        boundary=("domain", "scope"),
        invariants=("identity_continuity",),
        prior_requirements=("declared_origin",),
        admissible_states=("candidate",),
        residual_region=("visible_residual",),
    )
    transition = TransitionContract(
        transition_id="language_unit_to_relation",
        source_state="candidate",
        target_state="relation",
        required_evidence=("traceable_observation",),
        rank_ceiling="CANDIDATE",
        trace_ref=trace_ref,
    )
    return RealizationContract(
        domain="language",
        frozen_core_hash=core_freeze.extraction_hash,
        slots=(slot,),
        transitions=(transition,),
        trace_ref=trace_ref,
    )
