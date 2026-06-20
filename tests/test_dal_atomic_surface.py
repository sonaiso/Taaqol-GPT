"""Constitutional tests for DAL-only atomic surface operations.

Origin law: docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md
Branch: DAL-only atomic operations boundary hardening
Constitutional chain: DAL_ONLY -> DAL_ATOMIC -> SurfaceSkeletonCandidate
Category: Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dal_only import (
    DAL_ONLY_FORBIDDEN_OUTPUTS,
    CarrierIdentitySlot,
    DalAtomicCellStatus,
    DalAtomicOperationState,
    EdgeMode,
    HarakaFunctionSlot,
    HarakaMarkType,
    HarakaSurfaceFunction,
    ProofObject,
    SurfaceSkeletonCandidate,
    attach_haraka,
    build_surface_skeleton,
    identify_carrier,
)


def test_identify_carrier_emits_dal_only_carrier_identity() -> None:
    result = identify_carrier(
        "ض",
        carrier_id="carrier-1",
        position_index=0,
        trace_ref="trace://dal/carrier-1",
    )

    assert result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    assert result.failure_code is None
    assert isinstance(result.candidate, CarrierIdentitySlot)
    assert result.candidate.glyph == "ض"
    assert "ROOT_FORM" in result.candidate.forbidden_outputs
    assert "LEXICAL_MEANING" in result.candidate.forbidden_outputs


def test_haraka_slot_refuses_empty_carrier_ref() -> None:
    proof = ProofObject(
        proof_id="proof://dal/haraka",
        domain_id="DAL_ONLY",
        checked_gates=("NO_INDEPENDENT_MARK",),
        preserved_identity=("carrier-1",),
        residuals=(),
        failure_codes=(),
        trace=("trace://dal/haraka",),
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        HarakaFunctionSlot(
            haraka_id="haraka://carrier-1",
            carrier_ref="",
            mark_type=HarakaMarkType.FATHA,
            incoming_edge_ref="edge://left",
            outgoing_edge_ref="edge://right",
            surface_function=HarakaSurfaceFunction.OPEN_EDGE_A,
            possible_lafzi_potentials=("PATTERN_POTENTIAL",),
            waqf_policy="PROJECT_TO_WAQF",
            wasl_policy="PROJECT_TO_WASL",
            proof_object=proof,
            forbidden_outputs=DAL_ONLY_FORBIDDEN_OUTPUTS,
        )


def test_attach_haraka_blocks_initial_sukun_without_repair() -> None:
    carrier_result = identify_carrier(
        "ب",
        carrier_id="carrier-2",
        position_index=0,
        trace_ref="trace://dal/carrier-2",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)

    result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.SUKUN,
        edge_mode=EdgeMode.START,
        trace_ref="trace://dal/cell-2",
    )

    assert result.state is DalAtomicOperationState.BLOCKED_BY_GATE
    assert result.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_REPAIR_REQUIRED_HAMZAT_WASL" in result.residuals


def test_attach_haraka_builds_cell_for_attached_mark() -> None:
    carrier_result = identify_carrier(
        "ب",
        carrier_id="carrier-3",
        position_index=1,
        trace_ref="trace://dal/carrier-3",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)

    result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.FATHA,
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-3",
    )

    assert result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    cell = result.candidate
    assert cell is not None
    assert cell.status is DalAtomicCellStatus.CELL_LICENSED
    assert cell.haraka.surface_function is HarakaSurfaceFunction.OPEN_EDGE_A


def test_attach_haraka_refuses_non_enum_mark_type() -> None:
    carrier_result = identify_carrier(
        "ب",
        carrier_id="carrier-invalid-mark",
        position_index=1,
        trace_ref="trace://dal/carrier-invalid-mark",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)

    result = attach_haraka(
        carrier_result.candidate,
        "FATHA",  # type: ignore[arg-type]
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-invalid-mark",
    )

    assert result.state is DalAtomicOperationState.PROOF_REQUIRED
    assert result.failure_code is FailureCode.GATE_REQUIRED
    assert result.candidate is None


def test_attach_haraka_missing_mark_surfaces_residual_in_proof() -> None:
    carrier_result = identify_carrier(
        "ب",
        carrier_id="carrier-missing-mark",
        position_index=1,
        trace_ref="trace://dal/carrier-missing-mark",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)

    result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.MISSING,
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-missing-mark",
    )

    assert result.state is DalAtomicOperationState.RESIDUAL_CANDIDATE
    assert result.candidate is not None
    assert "DAL_SUSPENDED_MISSING_MARK" in result.residuals
    assert "DAL_SUSPENDED_MISSING_MARK" in result.candidate.proof.residuals


def test_surface_skeleton_requires_waqf_and_wasl_projections() -> None:
    carrier_result = identify_carrier(
        "ض",
        carrier_id="carrier-4",
        position_index=0,
        trace_ref="trace://dal/carrier-4",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)
    cell_result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.FATHA,
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-4",
    )
    cell = cell_result.candidate
    assert cell is not None

    result = build_surface_skeleton(
        (cell,),
        wasl_projection="",
        waqf_projection="WAQF_STOP",
        trace_ref="trace://dal/skeleton-4",
    )

    assert result.state is DalAtomicOperationState.PROOF_REQUIRED
    assert result.failure_code is FailureCode.BOUNDARY_MISSING


def test_surface_skeleton_refuses_invalid_cells_and_projection_types() -> None:
    result_with_invalid_cells = build_surface_skeleton(
        ("not-a-cell",),  # type: ignore[arg-type]
        wasl_projection="WASL_CONTINUE",
        waqf_projection="WAQF_STOP",
        trace_ref="trace://dal/skeleton-invalid-cells",
    )
    assert result_with_invalid_cells.state is DalAtomicOperationState.PROOF_REQUIRED
    assert result_with_invalid_cells.failure_code is FailureCode.GATE_REQUIRED

    carrier_result = identify_carrier(
        "ض",
        carrier_id="carrier-invalid-projection-type",
        position_index=0,
        trace_ref="trace://dal/carrier-invalid-projection-type",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)
    cell_result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.FATHA,
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-invalid-projection-type",
    )
    cell = cell_result.candidate
    assert cell is not None

    result_with_invalid_projection_type = build_surface_skeleton(
        (cell,),
        wasl_projection=1,  # type: ignore[arg-type]
        waqf_projection="WAQF_STOP",
        trace_ref="trace://dal/skeleton-invalid-projection-type",
    )
    assert result_with_invalid_projection_type.state is DalAtomicOperationState.PROOF_REQUIRED
    assert result_with_invalid_projection_type.failure_code is FailureCode.GATE_REQUIRED


def test_surface_skeleton_is_bridge_required_candidate_only() -> None:
    carrier_result = identify_carrier(
        "ض",
        carrier_id="carrier-5",
        position_index=0,
        trace_ref="trace://dal/carrier-5",
    )
    assert isinstance(carrier_result.candidate, CarrierIdentitySlot)
    cell_result = attach_haraka(
        carrier_result.candidate,
        HarakaMarkType.DAMMA,
        edge_mode=EdgeMode.INTERNAL_WASL,
        trace_ref="trace://dal/cell-5",
    )
    cell = cell_result.candidate
    assert cell is not None

    result = build_surface_skeleton(
        (cell,),
        wasl_projection="WASL_CONTINUE",
        waqf_projection="WAQF_STOP",
        trace_ref="trace://dal/skeleton-5",
    )

    assert result.state is DalAtomicOperationState.BRIDGE_REQUIRED
    assert result.failure_code is None
    assert isinstance(result.candidate, SurfaceSkeletonCandidate)
    assert result.candidate.rank is Rank.CANDIDATE
    assert result.candidate.domain_candidate.domain_id == "DAL_ONLY"
    assert result.candidate.domain_candidate.layer_id == "DAL_ATOMIC"
    assert "IFADAH" in result.candidate.forbidden_outputs
