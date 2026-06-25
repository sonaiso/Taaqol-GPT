"""Constitutional tests for LAFZI-C7 WadiResidualAudit.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C7 (W6 WadiResidualAudit only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import wadi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C7_ALLOWED_OUTPUT,
    WADI_C7_RANK_CEILING,
    MeaningIdentity,
    MeaningIdentityKind,
    TransferMajazGateState,
    TransferOrMajazKind,
    TransferOrMajazStatus,
    UsageScope,
    UsageScopeKind,
    WadAuthority,
    WadAuthorityFamily,
    WadiMadlulContract,
    WadiResidual,
    WadiResidualAuditState,
    WadiResidualKind,
    WadKind,
    prove_meaning_identity_gate,
    prove_transfer_majaz_gate,
    prove_usage_scope_gate,
    prove_wad_authority_gate,
    prove_wad_kind_gate,
    prove_wadi_residual_audit,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_FORBIDDEN_WADI_OUTPUTS = (
    "Wad'iMadlulClosed",
    "WadiStopGate",
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
            "LAFZI-C5",
            "LAFZI-C6",
            "LAFZI-C7",
            "WadiResidualAudit",
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


def _prove_c6(contract: WadiMadlulContract):
    wad_kind_result = prove_wad_kind_gate(contract, trace_ref="trace://w1")
    wad_authority_result = prove_wad_authority_gate(
        contract,
        wad_kind_result,
        trace_ref="trace://w2",
    )
    usage_scope_result = prove_usage_scope_gate(
        contract,
        wad_authority_result,
        trace_ref="trace://w3",
    )
    meaning_identity_result = prove_meaning_identity_gate(
        contract,
        usage_scope_result,
        trace_ref="trace://w4",
    )
    return prove_transfer_majaz_gate(
        contract,
        meaning_identity_result,
        trace_ref="trace://w5",
    )


def test_wadi_residual_audit_proves_visible_residual_surface() -> None:
    _declare(
        "LAFZI-C7 visible residual audit",
        produced_outputs=frozenset({WADI_C7_ALLOWED_OUTPUT}),
    )
    contract = _valid_contract()
    c6_result = _prove_c6(contract)

    result = prove_wadi_residual_audit(contract, c6_result, trace_ref="trace://w6")

    assert result.state is WadiResidualAuditState.PROVEN
    assert result.residuals == ()
    assert result.rank is WADI_C7_RANK_CEILING
    assert result.output == WADI_C7_ALLOWED_OUTPUT


def test_wadi_residual_audit_preserves_deferred_prior_gate() -> None:
    _declare("LAFZI-C7 preserves deferred C6")
    status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        trace_ref="trace://manqul-incomplete",
    )
    contract = _valid_contract(transfer_or_majaz_status=status)
    c6_result = _prove_c6(contract)
    assert c6_result.state is TransferMajazGateState.DEFERRED

    result = prove_wadi_residual_audit(contract, c6_result, trace_ref="trace://w6-deferred")

    assert result.state is WadiResidualAuditState.DEFERRED
    assert result.residuals == c6_result.residuals
    assert all(residual.visibility == "VISIBLE" for residual in result.residuals)


def test_wadi_residual_audit_blocks_on_visible_blocking_residual() -> None:
    _declare("LAFZI-C7 blocks on visible blocker")
    residual = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_WADI_CLOSURE_JUMP,
        trace_ref="trace://blocking",
        blocking=True,
    )
    contract = _valid_contract(residuals=(residual,))
    c6_result = _prove_c6(contract)

    result = prove_wadi_residual_audit(contract, c6_result, trace_ref="trace://w6-blocked")

    assert result.state is WadiResidualAuditState.BLOCKED
    assert result.residuals == (residual,)


def test_wadi_residual_audit_refuses_missing_trace_or_wrong_prior_gate() -> None:
    _declare("LAFZI-C7 birth guards")
    contract = _valid_contract()
    c6_result = _prove_c6(contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_wadi_residual_audit(contract, c6_result, trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_wadi_residual_audit(
            contract,
            "not-c6-result",  # type: ignore[arg-type]
            trace_ref="trace://w6",
        )


def test_wadi_residual_audit_refuses_broken_prior_identity() -> None:
    _declare("LAFZI-C7 prior identity continuity")
    contract = _valid_contract()
    other_contract = _valid_contract(identity="wadi-contract://other")
    other_c6_result = _prove_c6(other_contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        prove_wadi_residual_audit(contract, other_c6_result, trace_ref="trace://w6")


def test_wadi_residual_audit_exports_no_c8_or_downstream_runtime() -> None:
    _declare("LAFZI-C7 no downstream jump", forbidden_outputs=_FORBIDDEN_WADI_OUTPUTS)

    exported = set(wadi_madlul.__all__)
    assert {
        "WadiResidualAuditResult",
        "WadiResidualAuditState",
        "prove_wadi_residual_audit",
    } <= exported

    forbidden_exports = {
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
        "CoupledDalalahGateResult",
        "MutabaqahGateResult",
        "TadammunGateResult",
        "IltizamGateResult",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(wadi_madlul, name)


def test_wadi_residual_audit_adds_no_global_failure_codes() -> None:
    _declare("LAFZI-C7 local residual vocabulary only")

    assert WadiResidualKind.HIDDEN_WADI_RESIDUAL.value not in FailureCode.__members__
