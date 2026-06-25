"""Constitutional tests for LAFZI-C8 Wad'iMadlulClosed integration.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C8 (W7 WadiStopGate -> CoupledDalalahGate integration)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.wadi_c8_integration import (
    WADI_C8_ALLOWED_OUTPUT,
    WADI_C8_RANK_CEILING,
    CoupledDalalahGateResult,
    WadiMadlulState,
    prove_coupled_dalalah_gate,
    prove_wadi_madlul,
    prove_wadi_stop_gate,
    prove_wadi_to_coupled_dalalah,
)
from taaqqul_slot_geometry.weight.wadi_madlul import (
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
    prove_meaning_identity_gate,
    prove_transfer_majaz_gate,
    prove_usage_scope_gate,
    prove_wad_authority_gate,
    prove_wad_kind_gate,
    prove_wadi_residual_audit,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_FORBIDDEN_WADI_OUTPUTS = (
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
            "LAFZI-C5",
            "LAFZI-C6",
            "LAFZI-C7",
            "LAFZI-C8",
            "CoupledDalalahGate",
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


def _prove_c7(contract: WadiMadlulContract):
    w1 = prove_wad_kind_gate(contract, trace_ref="trace://w1")
    w2 = prove_wad_authority_gate(contract, w1, trace_ref="trace://w2")
    w3 = prove_usage_scope_gate(contract, w2, trace_ref="trace://w3")
    w4 = prove_meaning_identity_gate(contract, w3, trace_ref="trace://w4")
    w5 = prove_transfer_majaz_gate(contract, w4, trace_ref="trace://w5")
    return prove_wadi_residual_audit(contract, w5, trace_ref="trace://w6")


def test_wadi_c8_emits_coupled_dalalah_after_closed_wadi_surface() -> None:
    _declare(
        "LAFZI-C8 closed integration",
        produced_outputs=frozenset({WADI_C8_ALLOWED_OUTPUT}),
    )
    contract = _valid_contract()
    c7_result = _prove_c7(contract)

    verdict = prove_wadi_madlul(contract, c7_result, trace_ref="trace://w7")
    assert verdict.state is WadiMadlulState.CLOSED
    assert verdict.closed is not None

    stop_result = prove_wadi_stop_gate(verdict, trace_ref="trace://w7-stop")
    result = prove_coupled_dalalah_gate(contract, stop_result, trace_ref="trace://c8")

    assert isinstance(result, CoupledDalalahGateResult)
    assert result.state is WadiMadlulState.CLOSED
    assert result.rank is WADI_C8_RANK_CEILING
    assert result.output == WADI_C8_ALLOWED_OUTPUT
    assert result.wadi_madlul_closed_ref == contract.identity
    assert result.lafzi_madlul_closed_ref == contract.lafzi_madlul_closed_ref
    assert result.coupled_dalalah_ref


def test_wadi_c8_keeps_deferred_path_without_coupling_ref() -> None:
    _declare("LAFZI-C8 deferred path")
    deferred_status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        trace_ref="trace://manqul-incomplete",
    )
    contract = _valid_contract(transfer_or_majaz_status=deferred_status)
    c7_result = _prove_c7(contract)

    result = prove_wadi_to_coupled_dalalah(contract, c7_result, trace_ref="trace://c8-deferred")

    assert result.state is WadiMadlulState.DEFERRED
    assert result.wadi_madlul_closed_ref == ""
    assert result.coupled_dalalah_ref == ""


def test_wadi_c8_blocks_on_blocking_residual() -> None:
    _declare("LAFZI-C8 blocked path")
    blocking = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_WADI_CLOSURE_JUMP,
        trace_ref="trace://blocking",
        blocking=True,
    )
    contract = _valid_contract(residuals=(blocking,))
    c7_result = _prove_c7(contract)

    result = prove_wadi_to_coupled_dalalah(contract, c7_result, trace_ref="trace://c8-blocked")

    assert result.state is WadiMadlulState.BLOCKED
    assert blocking in result.residuals
    assert result.wadi_madlul_closed_ref == ""
    assert result.coupled_dalalah_ref == ""


def test_wadi_c8_refuses_broken_prior_identity_and_missing_trace() -> None:
    _declare("LAFZI-C8 birth guards")
    contract = _valid_contract()
    other_contract = _valid_contract(identity="wadi-contract://other")
    c7_other = _prove_c7(other_contract)
    c7 = _prove_c7(contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        prove_wadi_madlul(contract, c7_other, trace_ref="trace://w7")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_wadi_to_coupled_dalalah(contract, c7, trace_ref="")

