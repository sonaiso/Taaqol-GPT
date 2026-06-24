"""Constitutional tests for LAFZI-C2 WadKindGate.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C2 (W1 WadKindGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import wadi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C2_ALLOWED_OUTPUT,
    WADI_C2_RANK_CEILING,
    MeaningIdentity,
    MeaningIdentityKind,
    TransferOrMajazKind,
    TransferOrMajazStatus,
    UsageScope,
    UsageScopeKind,
    WadAuthority,
    WadAuthorityFamily,
    WadiMadlulContract,
    WadiResidual,
    WadiResidualKind,
    WadKind,
    WadKindGateState,
    prove_wad_kind_gate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_FORBIDDEN_WADI_OUTPUTS = (
    "Wad'iMadlulClosed",
    "CoupledDalalah",
    "Mutabaqah",
    "Tadammun",
    "Iltizam",
    "Ifadah",
    "Hukm",
    "Tanzil",
    "Reality",
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_WADI_OUTPUTS,
) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/60_WADI_MADLUL_CONDITION_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("LAFZI-C0", "LAFZI-C1", "LAFZI-C2", "WadKindGate"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=forbidden_outputs,
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=produced_outputs,
    )
    assert_constitutional_case(case, result)


def _valid_contract(**overrides: object) -> WadiMadlulContract:
    values: dict[str, object] = {
        "lafzi_madlul_closed_ref": "trace://lafzi/closed",
        "wad_kind": WadKind.LUGHAWI,
        "wad_authority": WadAuthority(
            family=WadAuthorityFamily.LUGHAWI,
            authority_ref="authority://arabic-usage",
            evidence_ref="evidence://sama",
            trace_ref="trace://authority",
        ),
        "usage_scope": UsageScope(
            scope_kind=UsageScopeKind.LANGUAGE,
            domain_ref="domain://arabic",
            boundary_ref="scope://general-arabic",
            trace_ref="trace://scope",
        ),
        "meaning_identity": MeaningIdentity(
            identity_kind=MeaningIdentityKind.ENTITY,
            boundary="boundary://human-male",
            included_surface=("human", "male"),
            excluded_surface=("relation", "judgment"),
            residuals=(),
            trace_ref="trace://meaning-identity",
        ),
        "transfer_or_majaz_status": TransferOrMajazStatus(
            status_kind=TransferOrMajazKind.DIRECT,
            trace_ref="trace://transfer-status",
        ),
        "residuals": (),
        "rank": Rank.CANDIDATE,
        "trace_ref": "trace://wadi-contract",
        "identity": "wadi-contract://rajul",
        "scope": "WADI_CONDITION",
    }
    values.update(overrides)
    return WadiMadlulContract(**values)  # type: ignore[arg-type]


def test_wad_kind_gate_proves_bounded_kind_without_closure() -> None:
    _declare(
        "LAFZI-C2 WadKindGate proven output",
        produced_outputs=frozenset({WADI_C2_ALLOWED_OUTPUT}),
    )

    result = prove_wad_kind_gate(_valid_contract(), trace_ref="trace://w1")

    assert result.state is WadKindGateState.PROVEN
    assert result.wad_kind is WadKind.LUGHAWI
    assert result.rank is WADI_C2_RANK_CEILING
    assert result.output == WADI_C2_ALLOWED_OUTPUT
    assert not result.residuals


def test_wad_kind_gate_defers_unknown_kind_with_visible_residual() -> None:
    _declare("LAFZI-C2 deferred WadKind")

    result = prove_wad_kind_gate(
        _valid_contract(wad_kind=WadKind.DEFERRED),
        trace_ref="trace://w1-deferred",
    )

    assert result.state is WadKindGateState.DEFERRED
    assert result.residuals == (
        WadiResidual(
            kind=WadiResidualKind.WAD_KIND_REQUIRED,
            trace_ref="trace://w1-deferred",
        ),
    )
    assert all(residual.visibility == "VISIBLE" for residual in result.residuals)


def test_wad_kind_gate_blocks_on_visible_blocking_residual() -> None:
    _declare("LAFZI-C2 blocking residual")
    residual = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_WADI_CLOSURE_JUMP,
        trace_ref="trace://blocked",
        blocking=True,
    )

    result = prove_wad_kind_gate(
        _valid_contract(residuals=(residual,)),
        trace_ref="trace://w1-blocked",
    )

    assert result.state is WadKindGateState.BLOCKED
    assert result.residuals == (residual,)
    assert result.rank is Rank.CANDIDATE


def test_wad_kind_gate_refuses_missing_trace_or_contract() -> None:
    _declare("LAFZI-C2 birth guards")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_wad_kind_gate(_valid_contract(), trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_wad_kind_gate("not-contract", trace_ref="trace://w1")  # type: ignore[arg-type]


def test_wad_kind_gate_exports_no_downstream_gate_or_closed_verdict() -> None:
    _declare("LAFZI-C2 no downstream jump", forbidden_outputs=_FORBIDDEN_WADI_OUTPUTS)

    exported = set(wadi_madlul.__all__)
    assert {"WadKindGateResult", "WadKindGateState", "prove_wad_kind_gate"} <= exported

    forbidden_exports = {
        "WadAuthorityGate",
        "UsageScopeGate",
        "MeaningIdentityGate",
        "TransferMajazGate",
        "WadiResidualAudit",
        "WadiStopGate",
        "WadiMadlulState",
        "WadiMadlulVerdict",
        "WadiMadlulClosed",
        "CoupledDalalah",
        "Mutabaqah",
        "Tadammun",
        "Iltizam",
        "Ifadah",
        "Hukm",
        "Tanzil",
        "Reality",
        "prove_wadi_madlul",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(wadi_madlul, name)
