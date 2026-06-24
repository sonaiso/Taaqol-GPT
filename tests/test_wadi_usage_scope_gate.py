"""Constitutional tests for LAFZI-C4 UsageScopeGate.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C4 (W3 UsageScopeGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import wadi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C4_ALLOWED_OUTPUT,
    WADI_C4_RANK_CEILING,
    MeaningIdentity,
    MeaningIdentityKind,
    TransferOrMajazKind,
    TransferOrMajazStatus,
    UsageScope,
    UsageScopeGateState,
    UsageScopeKind,
    WadAuthority,
    WadAuthorityFamily,
    WadiMadlulContract,
    WadiResidual,
    WadiResidualKind,
    WadKind,
    prove_usage_scope_gate,
    prove_wad_authority_gate,
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
        constitutional_chain=(
            "LAFZI-C0",
            "LAFZI-C1",
            "LAFZI-C2",
            "LAFZI-C3",
            "LAFZI-C4",
            "UsageScopeGate",
        ),
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


def _prove_authority(contract: WadiMadlulContract):
    wad_kind_result = prove_wad_kind_gate(contract, trace_ref="trace://w1")
    return prove_wad_authority_gate(contract, wad_kind_result, trace_ref="trace://w2")


def test_usage_scope_gate_proves_visible_scope_without_closure() -> None:
    _declare(
        "LAFZI-C4 UsageScopeGate proven output",
        produced_outputs=frozenset({WADI_C4_ALLOWED_OUTPUT}),
    )
    contract = _valid_contract()
    wad_authority_result = _prove_authority(contract)

    result = prove_usage_scope_gate(
        contract,
        wad_authority_result,
        trace_ref="trace://w3",
    )

    assert result.state is UsageScopeGateState.PROVEN
    assert result.scope_kind is UsageScopeKind.LANGUAGE
    assert result.domain_ref == "domain://arabic"
    assert result.boundary_ref == "scope://general-arabic"
    assert result.rank is WADI_C4_RANK_CEILING
    assert result.output == WADI_C4_ALLOWED_OUTPUT
    assert not result.residuals


def test_usage_scope_gate_defers_missing_scope_with_visible_residual() -> None:
    _declare("LAFZI-C4 deferred usage scope")
    contract = _valid_contract(
        usage_scope=UsageScope(
            scope_kind=UsageScopeKind.DEFERRED,
            domain_ref="domain://deferred",
            boundary_ref="scope://deferred",
            trace_ref="trace://scope-deferred",
        )
    )
    wad_authority_result = _prove_authority(contract)

    result = prove_usage_scope_gate(
        contract,
        wad_authority_result,
        trace_ref="trace://w3-deferred",
    )

    assert result.state is UsageScopeGateState.DEFERRED
    assert result.residuals == (
        WadiResidual(
            kind=WadiResidualKind.USAGE_SCOPE_REQUIRED,
            trace_ref="trace://w3-deferred",
        ),
    )
    assert all(residual.visibility == "VISIBLE" for residual in result.residuals)


def test_usage_scope_gate_preserves_prior_deferred_authority() -> None:
    _declare("LAFZI-C4 preserves deferred WadAuthority")
    contract = _valid_contract(
        wad_authority=WadAuthority(
            family=WadAuthorityFamily.DEFERRED,
            authority_ref="authority://deferred",
            evidence_ref="evidence://deferred",
            trace_ref="trace://authority-deferred",
        )
    )
    wad_authority_result = _prove_authority(contract)

    result = prove_usage_scope_gate(
        contract,
        wad_authority_result,
        trace_ref="trace://w3-after-deferred-w2",
    )

    assert result.state is UsageScopeGateState.DEFERRED
    assert result.residuals == wad_authority_result.residuals


def test_usage_scope_gate_blocks_on_visible_blocking_residual() -> None:
    _declare("LAFZI-C4 blocking residual")
    residual = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_WADI_CLOSURE_JUMP,
        trace_ref="trace://blocked",
        blocking=True,
    )
    contract = _valid_contract(residuals=(residual,))
    wad_authority_result = _prove_authority(contract)

    result = prove_usage_scope_gate(
        contract,
        wad_authority_result,
        trace_ref="trace://w3-blocked",
    )

    assert result.state is UsageScopeGateState.BLOCKED
    assert result.residuals == (residual,)
    assert result.rank is Rank.CANDIDATE


def test_usage_scope_gate_refuses_missing_trace_or_prior_gate() -> None:
    _declare("LAFZI-C4 birth guards")
    contract = _valid_contract()
    wad_authority_result = _prove_authority(contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_usage_scope_gate(contract, wad_authority_result, trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_usage_scope_gate(
            contract,
            "not-wad-authority-result",  # type: ignore[arg-type]
            trace_ref="trace://w3",
        )


def test_usage_scope_gate_refuses_broken_prior_gate_identity() -> None:
    _declare("LAFZI-C4 prior gate identity continuity")
    contract = _valid_contract()
    other_contract = _valid_contract(identity="wadi-contract://other")
    other_wad_authority_result = _prove_authority(other_contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        prove_usage_scope_gate(
            contract,
            other_wad_authority_result,
            trace_ref="trace://w3",
        )


def test_usage_scope_gate_exports_no_downstream_gate_or_closed_verdict() -> None:
    _declare("LAFZI-C4 no downstream jump", forbidden_outputs=_FORBIDDEN_WADI_OUTPUTS)

    exported = set(wadi_madlul.__all__)
    assert {"UsageScopeGateResult", "UsageScopeGateState", "prove_usage_scope_gate"} <= exported

    forbidden_exports = {
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


def test_usage_scope_gate_adds_no_global_failure_codes() -> None:
    _declare("LAFZI-C4 local residual vocabulary only")

    assert WadiResidualKind.USAGE_SCOPE_REQUIRED.value not in FailureCode.__members__
