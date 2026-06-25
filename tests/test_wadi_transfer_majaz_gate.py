"""Constitutional tests for LAFZI-C6 TransferMajazGate.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C6 (W5 TransferMajazGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import wadi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C6_ALLOWED_OUTPUT,
    WADI_C6_RANK_CEILING,
    MeaningIdentity,
    MeaningIdentityGateResult,
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
    WadiResidualKind,
    WadKind,
    prove_meaning_identity_gate,
    prove_transfer_majaz_gate,
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
    "WadiResidualAudit",
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
            "TransferMajazGate",
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


def _prove_c5(contract: WadiMadlulContract) -> MeaningIdentityGateResult:
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
    return prove_meaning_identity_gate(contract, usage_scope_result, trace_ref="trace://w4")


def test_transfer_majaz_gate_proves_direct_path() -> None:
    _declare(
        "LAFZI-C6 direct transfer status",
        produced_outputs=frozenset({WADI_C6_ALLOWED_OUTPUT}),
    )
    contract = _valid_contract()
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-direct")

    assert result.state is TransferMajazGateState.PROVEN
    assert result.status_kind is TransferOrMajazKind.DIRECT
    assert result.residuals == ()
    assert result.rank is WADI_C6_RANK_CEILING
    assert result.output == WADI_C6_ALLOWED_OUTPUT


def test_transfer_majaz_gate_proves_manqul_with_required_fields() -> None:
    _declare("LAFZI-C6 manqul transfer status")
    status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        transfer_cause="cause://technical-transfer",
        new_usage_scope="scope://new-technical",
        preserved_trace_ref="trace://origin-preserved",
        qadih_difference="qadih://difference",
        trace_ref="trace://manqul",
    )
    contract = _valid_contract(transfer_or_majaz_status=status)
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-manqul")

    assert result.state is TransferMajazGateState.PROVEN
    assert result.status_kind is TransferOrMajazKind.MANQUL
    assert result.original_wad_ref == "origin://wad"
    assert result.transfer_cause == "cause://technical-transfer"
    assert result.new_usage_scope == "scope://new-technical"
    assert result.preserved_trace_ref == "trace://origin-preserved"
    assert result.qadih_difference == "qadih://difference"
    assert result.residuals == ()


def test_transfer_majaz_gate_proves_majazi_with_required_fields() -> None:
    _declare("LAFZI-C6 majazi transfer status")
    status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MAJAZI,
        original_haqiqah_ref="haqiqah://origin",
        relation_ref="relation://licensed",
        qarinah_ref="qarinah://visible",
        literal_preventer_ref="preventer://literal",
        trace_ref="trace://majazi",
    )
    contract = _valid_contract(transfer_or_majaz_status=status)
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-majazi")

    assert result.state is TransferMajazGateState.PROVEN
    assert result.status_kind is TransferOrMajazKind.MAJAZI
    assert result.original_haqiqah_ref == "haqiqah://origin"
    assert result.relation_ref == "relation://licensed"
    assert result.qarinah_ref == "qarinah://visible"
    assert result.literal_preventer_ref == "preventer://literal"
    assert result.residuals == ()


def test_transfer_majaz_gate_preserves_deferred_prior_c5() -> None:
    _declare("LAFZI-C6 preserves deferred C5")
    contract = _valid_contract(
        meaning_identity=MeaningIdentity(
            identity_kind=MeaningIdentityKind.DEFERRED,
            boundary="boundary://deferred",
            included_surface=("deferred",),
            excluded_surface=("closure",),
            residuals=(),
            trace_ref="trace://meaning-deferred",
        )
    )
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-after-c5")

    assert result.state is TransferMajazGateState.DEFERRED
    assert result.residuals == c5_result.residuals


def test_transfer_majaz_gate_preserves_blocking_prior_residual() -> None:
    _declare("LAFZI-C6 preserves blocking residual")
    residual = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_WADI_CLOSURE_JUMP,
        trace_ref="trace://blocked",
        blocking=True,
    )
    contract = _valid_contract(residuals=(residual,))
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-blocked")

    assert result.state is TransferMajazGateState.BLOCKED
    assert result.residuals == (residual,)


def test_transfer_majaz_gate_missing_manqul_components_add_visible_residuals() -> None:
    _declare("LAFZI-C6 missing manqul fields")
    status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        trace_ref="trace://manqul-incomplete",
    )
    contract = _valid_contract(transfer_or_majaz_status=status)
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-manqul")

    assert result.state is TransferMajazGateState.DEFERRED
    assert {residual.kind for residual in result.residuals} == {
        WadiResidualKind.TRANSFER_ORIGIN_REQUIRED,
        WadiResidualKind.TRANSFER_CAUSE_REQUIRED,
    }
    assert all(residual.visibility == "VISIBLE" for residual in result.residuals)


def test_transfer_majaz_gate_missing_majazi_components_add_visible_residuals() -> None:
    _declare("LAFZI-C6 missing majazi fields")
    status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MAJAZI,
        original_haqiqah_ref="haqiqah://origin",
        trace_ref="trace://majazi-incomplete",
    )
    contract = _valid_contract(transfer_or_majaz_status=status)
    c5_result = _prove_c5(contract)

    result = prove_transfer_majaz_gate(contract, c5_result, trace_ref="trace://w5-majazi")

    assert result.state is TransferMajazGateState.DEFERRED
    assert {residual.kind for residual in result.residuals} == {
        WadiResidualKind.MAJAZ_RELATION_REQUIRED,
        WadiResidualKind.MAJAZ_QARINAH_REQUIRED,
        WadiResidualKind.MAJAZ_LITERAL_PREVENTER_REQUIRED,
    }
    assert all(residual.visibility == "VISIBLE" for residual in result.residuals)


def test_transfer_majaz_gate_refuses_broken_prior_identity() -> None:
    _declare("LAFZI-C6 prior identity continuity")
    contract = _valid_contract()
    other_contract = _valid_contract(identity="wadi-contract://other")
    other_c5_result = _prove_c5(other_contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        prove_transfer_majaz_gate(contract, other_c5_result, trace_ref="trace://w5")


def test_transfer_majaz_gate_refuses_missing_trace_or_wrong_prior_gate() -> None:
    _declare("LAFZI-C6 birth guards")
    contract = _valid_contract()
    c5_result = _prove_c5(contract)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_transfer_majaz_gate(contract, c5_result, trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_transfer_majaz_gate(
            contract,
            "not-c5-result",  # type: ignore[arg-type]
            trace_ref="trace://w5",
        )


def test_transfer_majaz_gate_exports_no_downstream_runtime() -> None:
    _declare("LAFZI-C6 no downstream jump", forbidden_outputs=_FORBIDDEN_WADI_OUTPUTS)

    exported = set(wadi_madlul.__all__)
    assert {
        "TransferMajazGateResult",
        "TransferMajazGateState",
        "prove_transfer_majaz_gate",
    } <= exported

    forbidden_exports = {
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
        "CoupledDalalahGateResult",
        "MutabaqahGateResult",
        "TadammunGateResult",
        "IltizamGateResult",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(wadi_madlul, name)


def test_transfer_majaz_gate_local_residuals_remain_outside_failure_code() -> None:
    _declare("LAFZI-C6 local residual vocabulary only")

    assert WadiResidualKind.TRANSFER_ORIGIN_REQUIRED.value not in FailureCode.__members__
    assert WadiResidualKind.MAJAZ_QARINAH_REQUIRED.value not in FailureCode.__members__
