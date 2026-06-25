"""Constitutional tests for LAFZI-D1 CoupledDalalah carrier surface.

Origin law     : docs/62 (Coupled Dalālah Matrix Law)
Branch         : LAFZI-D1 (CoupledDalalah carrier surface only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import coupled_dalalah
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.coupled_dalalah import (
    LAFZI_D1_ALLOWED_OUTPUT,
    LAFZI_D1_FORBIDDEN_OUTPUTS,
    LAFZI_D1_RANK_CEILING,
    LAFZI_D1_RESIDUAL_VOCABULARY,
    LAFZI_D2_ALLOWED_OUTPUT,
    LAFZI_D2_FORBIDDEN_OUTPUTS,
    LAFZI_D2_RANK_CEILING,
    CoupledDalalahResidual,
    CoupledDalalahResidualKind,
    CoupledDalalahSurface,
    D1C8HandoffCard,
    MutabaqahGateResult,
    MutabaqahGateState,
    prove_mutabaqah_gate,
)
from taaqqul_slot_geometry.weight.wadi_c8_integration import (
    WadiMadlulState,
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
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_FORBIDDEN_D1_OUTPUTS = (
    "Mutabaqah",
    "Tadammun",
    "Iltizam",
    "DalalahMatrix",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
)

_FORBIDDEN_D2_OUTPUTS = (
    "Tadammun",
    "Iltizam",
    "DalalahMatrix",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_D1_OUTPUTS,
) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/62_COUPLED_DALALAH_MATRIX_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("LAFZI-C8", "LAFZI-D0", "LAFZI-D1", "CoupledDalalahSurface"),
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


def _declare_d2(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    failure_code: FailureCode | None = None,
) -> None:
    expected_state = ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    case = ConstitutionalTestCase(
        origin_law="docs/62_COUPLED_DALALAH_MATRIX_LAW.md",
        branch_name=branch_name,
        constitutional_chain=(
            "LAFZI-C8",
            "LAFZI-D0",
            "LAFZI-D1",
            "CoupledDalalahSurface",
            "LAFZI-D2",
            "MutabaqahGateResult",
        ),
        expected_state=expected_state,
        expected_failure_code=failure_code,
        forbidden_outputs=_FORBIDDEN_D2_OUTPUTS,
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=expected_state,
        failure_code=failure_code,
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


def _closed_c8_pair(**contract_overrides: object):
    contract = _valid_contract(**contract_overrides)
    c8_result = prove_wadi_to_coupled_dalalah(contract, _prove_c7(contract), trace_ref="trace://c8")
    return contract, c8_result


def _handoff_card(
    *,
    contract_overrides: dict[str, object] | None = None,
    **overrides: object,
) -> D1C8HandoffCard:
    contract, c8_result = _closed_c8_pair(**(contract_overrides or {}))
    values: dict[str, object] = {
        "prior_knowledge_refs": ("origin://sama",),
        "trace_ref": "trace://d1",
    }
    values.update(overrides)
    return D1C8HandoffCard.from_c8_gate_result(c8_result, contract, **values)  # type: ignore[arg-type]


def _surface(
    *,
    contract_overrides: dict[str, object] | None = None,
    **overrides: object,
) -> CoupledDalalahSurface:
    contract, c8_result = _closed_c8_pair(**(contract_overrides or {}))
    values: dict[str, object] = {
        "prior_knowledge_refs": ("origin://sama",),
        "trace_ref": "trace://d1",
    }
    values.update(overrides)
    return CoupledDalalahSurface.from_c8_gate_result(c8_result, contract, **values)  # type: ignore[arg-type]


def test_lafzi_d1_declares_local_residual_vocabulary_only() -> None:
    _declare("local coupled dalālah residual vocabulary")

    assert tuple(kind.value for kind in CoupledDalalahResidualKind) == LAFZI_D1_RESIDUAL_VOCABULARY
    for residual_name in LAFZI_D1_RESIDUAL_VOCABULARY:
        assert residual_name not in FailureCode.__members__


def test_coupled_dalalah_surface_preserves_c8_refs_and_boundary_fields() -> None:
    _declare("D1 carrier surface fields", produced_outputs=frozenset({LAFZI_D1_ALLOWED_OUTPUT}))

    surface = _surface()
    field_names = {field.name for field in dataclasses.fields(CoupledDalalahSurface)}

    for field_name in (
        "c8_gate_result_ref",
        "birth_card",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "domain_ref",
        "scope_ref",
        "prior_knowledge_refs",
        "c8_residuals",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert surface.output == LAFZI_D1_ALLOWED_OUTPUT
    assert surface.rank is LAFZI_D1_RANK_CEILING
    assert surface.wadi_madlul_closed_ref == "wadi-contract://rajul"
    assert surface.lafzi_madlul_closed_ref == "trace://lafzi/closed"
    assert surface.madlul_boundary_ref == "boundary://human-male"
    assert surface.included_surface == ("human", "male")
    assert surface.excluded_surface == ("relation", "judgment")
    assert surface.domain_ref == "domain://arabic"
    assert surface.scope_ref == "scope://general-arabic"
    assert isinstance(surface.birth_card, D1C8HandoffCard)
    assert surface.birth_card.contract_ref == "wadi-contract://rajul"
    assert surface.birth_card.c8_trace_ref == "trace://c8"


def test_coupled_dalalah_surface_requires_closed_c8_handoff() -> None:
    _declare("closed C8 handoff required")
    deferred_status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        trace_ref="trace://deferred-transfer",
    )
    contract = _valid_contract(transfer_or_majaz_status=deferred_status)
    c8_result = prove_wadi_to_coupled_dalalah(contract, _prove_c7(contract), trace_ref="trace://c8")

    assert c8_result.state is WadiMadlulState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        CoupledDalalahSurface.from_c8_gate_result(
            c8_result,
            contract,
            prior_knowledge_refs=("origin://sama",),
            trace_ref="trace://d1",
        )


@pytest.mark.parametrize(
    ("field_name", "value", "failure_code"),
    [
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING),
        ("included_surface", (), FailureCode.BOUNDARY_MISSING),
        ("excluded_surface", (), FailureCode.BOUNDARY_MISSING),
        ("domain_ref", "", FailureCode.DOMAIN_MISSING),
        ("scope_ref", "", FailureCode.SCOPE_MISSING),
        ("prior_knowledge_refs", (), FailureCode.REQUIRED_SLOT_EMPTY),
        ("trace_ref", "", FailureCode.TRACE_MISSING),
    ],
)
def test_d1c8_handoff_card_refuses_missing_birth_guards(
    field_name: str,
    value: object,
    failure_code: FailureCode,
) -> None:
    _declare("D1 birth guards")

    card = _handoff_card()
    with pytest.raises(WeightCarrierSchemaError, match=failure_code.value):
        dataclasses.replace(card, **{field_name: value})


def test_coupled_dalalah_surface_preserves_visible_residuals() -> None:
    _declare("visible residual discipline")
    c8_blocker = WadiResidual(
        kind=WadiResidualKind.FORBIDDEN_IFADAH_JUMP,
        trace_ref="trace://visible-c8-residual",
    )
    d1_residual = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
        trace_ref="trace://visible-d1-residual",
    )
    surface = _surface(
        contract_overrides={"residuals": (c8_blocker,)},
        residuals=(d1_residual,),
    )

    assert c8_blocker in surface.c8_residuals
    assert d1_residual in surface.residuals
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        CoupledDalalahResidual(
            kind=CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
            trace_ref="trace://hidden",
            visibility="HIDDEN",  # type: ignore[arg-type]
        )


def test_d1_refuses_non_closed_c8_handoff_card() -> None:
    _declare("D1 birth card requires closed C8")
    deferred_status = TransferOrMajazStatus(
        status_kind=TransferOrMajazKind.MANQUL,
        original_wad_ref="origin://wad",
        trace_ref="trace://deferred-transfer",
    )
    contract = _valid_contract(transfer_or_majaz_status=deferred_status)
    c8_result = prove_wadi_to_coupled_dalalah(contract, _prove_c7(contract), trace_ref="trace://c8")

    assert c8_result.state is WadiMadlulState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        D1C8HandoffCard.from_c8_gate_result(
            c8_result,
            contract,
            prior_knowledge_refs=("origin://sama",),
            trace_ref="trace://d1",
        )


def test_d1_refuses_c8_contract_identity_mismatch() -> None:
    _declare("D1 birth card preserves C8 contract identity")
    _, c8_result = _closed_c8_pair()
    unrelated_contract = _valid_contract(identity="wadi-contract://unrelated")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        D1C8HandoffCard.from_c8_gate_result(
            c8_result,
            unrelated_contract,
            prior_knowledge_refs=("origin://sama",),
            trace_ref="trace://d1",
        )


def test_d1_refuses_boundary_not_derived_from_wadi_contract() -> None:
    _declare("D1 boundary is derived from C8 wadʿī contract")
    surface = _surface()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.IDENTITY_BROKEN.value):
        dataclasses.replace(surface, madlul_boundary_ref="boundary://unrelated")


def test_coupled_dalalah_surface_refuses_weakened_forbidden_outputs() -> None:
    _declare("D1 forbidden downstream surface is not weakenable")
    surface = _surface()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.OUTPUT_EXCEEDS_LAYER.value):
        dataclasses.replace(surface, forbidden_outputs=("MUTABAQAH",))


def test_d1_refuses_included_excluded_overlap() -> None:
    _declare("D1 boundary included and excluded surfaces are disjoint")
    overlapping_identity = MeaningIdentity(
        identity_kind=MeaningIdentityKind.ENTITY,
        boundary="boundary://overlap",
        included_surface=("human", "male"),
        excluded_surface=("male", "judgment"),
        residuals=(),
        trace_ref="trace://meaning-identity-overlap",
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _surface(contract_overrides={"meaning_identity": overlapping_identity})


def test_d1_surface_requires_birth_card() -> None:
    _declare("D1 surface requires explicit birth card")
    surface = _surface()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(surface, birth_card=None)


def test_lafzi_d1_module_exports_d2_only_no_downstream_runtime() -> None:
    _declare("D1 carrier plus opened D2 gate only", forbidden_outputs=_FORBIDDEN_D2_OUTPUTS)

    exported = set(coupled_dalalah.__all__)
    forbidden_exports = {
        "TadammunGate",
        "IltizamGate",
        "DalalahMatrixVerdict",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "Reality",
        "prove_tadammun_gate",
        "prove_iltizam_gate",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(coupled_dalalah, name)
    assert LAFZI_D1_FORBIDDEN_OUTPUTS
    assert "D1C8HandoffCard" in exported
    assert "MutabaqahGateResult" in exported
    assert "prove_mutabaqah_gate" in exported


def test_mutabaqah_gate_accepts_minimal_coupled_dalalah_surface() -> None:
    _declare_d2("minimal MutabaqahGate", produced_outputs=frozenset({LAFZI_D2_ALLOWED_OUTPUT}))

    surface = _surface()
    result = prove_mutabaqah_gate(surface, trace_ref="trace://d2")
    field_names = {field.name for field in dataclasses.fields(MutabaqahGateResult)}

    for field_name in (
        "source_surface",
        "coupled_dalalah_surface_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is MutabaqahGateState.PROVEN
    assert result.output == LAFZI_D2_ALLOWED_OUTPUT
    assert result.rank is LAFZI_D2_RANK_CEILING
    assert result.rank is surface.rank
    assert result.coupled_dalalah_surface_ref == surface.trace_ref
    assert result.madlul_boundary_ref == surface.madlul_boundary_ref
    assert result.included_surface == surface.included_surface
    assert result.forbidden_outputs == LAFZI_D2_FORBIDDEN_OUTPUTS


def test_mutabaqah_gate_refuses_missing_coupled_dalalah_surface() -> None:
    _declare_d2("MutabaqahGate requires D1 surface", failure_code=FailureCode.GATE_REQUIRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_mutabaqah_gate(None, trace_ref="trace://d2")  # type: ignore[arg-type]


def test_mutabaqah_result_refuses_missing_madlul_boundary() -> None:
    _declare_d2("MutabaqahGate requires madlul boundary", failure_code=FailureCode.BOUNDARY_MISSING)
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        dataclasses.replace(result, madlul_boundary_ref="")


def test_mutabaqah_gate_refuses_hidden_residual() -> None:
    _declare_d2("MutabaqahGate residual visibility", failure_code=FailureCode.HIDDEN_RESIDUAL)
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(result, residuals=(object(),))  # type: ignore[arg-type]


def test_mutabaqah_gate_refuses_rank_promotion() -> None:
    _declare_d2(
        "MutabaqahGate rank ceiling",
        failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
    )
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    with pytest.raises(
        WeightCarrierSchemaError,
        match=FailureCode.RANK_PROMOTION_WITHOUT_GATE.value,
    ):
        dataclasses.replace(result, rank=Rank.TRACE)


@pytest.mark.parametrize(
    ("field_name", "value", "match"),
    [
        ("included_surface", ("unrelated",), FailureCode.IDENTITY_BROKEN.value),
        ("domain_ref", "domain://other", "DOMAIN_MISMATCH"),
    ],
)
def test_mutabaqah_gate_refuses_boundary_or_identity_drift(
    field_name: str,
    value: object,
    match: str,
) -> None:
    _declare_d2("MutabaqahGate preserves D1 boundary and identity")
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    with pytest.raises(WeightCarrierSchemaError, match=match):
        dataclasses.replace(result, **{field_name: value})


def test_mutabaqah_gate_does_not_open_tadammun_or_iltizam() -> None:
    _declare_d2("D2 does not open D3 or D4", produced_outputs=frozenset({LAFZI_D2_ALLOWED_OUTPUT}))
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")
    exported = set(coupled_dalalah.__all__)

    assert result.output == LAFZI_D2_ALLOWED_OUTPUT
    assert "TADAMMUN" in result.forbidden_outputs
    assert "ILTIZAM" in result.forbidden_outputs
    assert "TadammunGateResult" not in exported
    assert "IltizamGateResult" not in exported
    assert "prove_tadammun_gate" not in exported
    assert "prove_iltizam_gate" not in exported
