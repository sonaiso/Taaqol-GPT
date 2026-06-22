"""Constitutional tests for the LAFZI-C1 Wad'i carrier surface.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C1 (carrier-only wadʿī condition surface)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import wadi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C1_FORBIDDEN_OUTPUTS,
    WADI_C1_RANK_CEILING,
    WADI_C1_RESIDUAL_VOCABULARY,
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


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/60_WADI_MADLUL_CONDITION_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("LAFZI-C0", "LAFZI-C1", "WadiMadlulContract"),
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
        produced_outputs=frozenset(),
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
    }
    values.update(overrides)
    return WadiMadlulContract(**values)  # type: ignore[arg-type]


def test_wadi_c1_declares_local_residual_vocabulary_only() -> None:
    _declare("local wadʿī residual vocabulary")

    assert tuple(kind.value for kind in WadiResidualKind) == WADI_C1_RESIDUAL_VOCABULARY
    for residual_name in WADI_C1_RESIDUAL_VOCABULARY:
        assert residual_name not in FailureCode.__members__


def test_wadi_contract_carries_docs_60_fields() -> None:
    _declare("WadiMadlulContract fields", _FORBIDDEN_WADI_OUTPUTS)

    contract = _valid_contract()
    field_names = {field.name for field in dataclasses.fields(WadiMadlulContract)}

    for field_name in (
        "lafzi_madlul_closed_ref",
        "wad_kind",
        "wad_authority",
        "usage_scope",
        "meaning_identity",
        "transfer_or_majaz_status",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert contract.domain_id == "WADI_MADLUL"
    assert contract.rank is WADI_C1_RANK_CEILING


def test_wadi_residual_refuses_hidden_visibility() -> None:
    _declare("visible residual discipline")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        WadiResidual(
            kind=WadiResidualKind.HIDDEN_WADI_RESIDUAL,
            trace_ref="trace://hidden",
            visibility="HIDDEN",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("field_name", "value", "failure_code"),
    [
        ("lafzi_madlul_closed_ref", "", FailureCode.TRACE_MISSING),
        ("trace_ref", "", FailureCode.TRACE_MISSING),
        ("scope", "", FailureCode.SCOPE_MISSING),
        ("identity", "", FailureCode.IDENTITY_BROKEN),
        ("rank", Rank.HYPOTHESIS, FailureCode.RANK_EXCEEDS_CEILING),
    ],
)
def test_wadi_contract_refuses_missing_birth_guards(
    field_name: str,
    value: object,
    failure_code: FailureCode,
) -> None:
    _declare("carrier birth guards")

    with pytest.raises(WeightCarrierSchemaError, match=failure_code.value):
        _valid_contract(**{field_name: value})


def test_wadi_contract_requires_typed_surfaces() -> None:
    _declare("typed carrier surface")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_contract(wad_kind="LUGHAWI")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        _valid_contract(residuals=("not-local-residual",))


def test_transfer_and_majaz_status_preserve_required_components() -> None:
    _declare("transfer and majaz status carriers")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        TransferOrMajazStatus(
            status_kind=TransferOrMajazKind.MANQUL,
            original_wad_ref="origin://wad",
            trace_ref="trace://manqul",
        )

    manqul = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        transfer_cause="cause://technical-transfer",
        new_usage_scope="scope://new-technical",
        preserved_trace_ref="trace://origin-preserved",
        qadih_difference="qadih://difference",
        trace_ref="trace://manqul",
    )
    majazi = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MAJAZI,
        original_haqiqah_ref="haqiqah://origin",
        relation_ref="relation://licensed",
        qarinah_ref="qarinah://visible",
        literal_preventer_ref="preventer://literal",
        trace_ref="trace://majazi",
    )

    assert manqul.status_kind is TransferOrMajazKind.MANQUL
    assert majazi.status_kind is TransferOrMajazKind.MAJAZI


def test_wadi_c1_exports_no_gate_operation_or_closed_verdict() -> None:
    _declare("carrier only no closure", _FORBIDDEN_WADI_OUTPUTS)

    exported = set(wadi_madlul.__all__)
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
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(wadi_madlul, name)
    assert WADI_C1_FORBIDDEN_OUTPUTS
