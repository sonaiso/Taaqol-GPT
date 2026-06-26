"""Constitutional tests for LAFZI-D1 through D5 CoupledDalalah surfaces.

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
    LAFZI_D3_ALLOWED_OUTPUT,
    LAFZI_D3_FORBIDDEN_OUTPUTS,
    LAFZI_D3_RANK_CEILING,
    LAFZI_D4_ALLOWED_OUTPUT,
    LAFZI_D4_FORBIDDEN_OUTPUTS,
    LAFZI_D4_RANK_CEILING,
    LAFZI_D5_ALLOWED_OUTPUT,
    LAFZI_D5_FORBIDDEN_OUTPUTS,
    LAFZI_D5_RANK_CEILING,
    LAFZI_D6_FORBIDDEN_OUTPUTS,
    LAFZI_D6_MATRIX_CLOSED_ALLOWED_OUTPUT,
    LAFZI_D6_RANK_CEILING,
    LAFZI_D6_WORD_CAPABILITY_ALLOWED_OUTPUT,
    CoupledDalalahResidual,
    CoupledDalalahResidualKind,
    CoupledDalalahSurface,
    D1C8HandoffCard,
    DalalahMatrixClosed,
    DalalahMatrixClosedState,
    DalalahMatrixResidualAuditResult,
    DalalahMatrixResidualAuditState,
    IltizamGateResult,
    IltizamGateState,
    MutabaqahGateResult,
    MutabaqahGateState,
    TadammunGateResult,
    TadammunGateState,
    WordCapabilityBoundary,
    WordCapabilityBoundaryState,
    prove_dalalah_matrix_closed,
    prove_dalalah_matrix_residual_audit,
    prove_iltizam_gate,
    prove_mutabaqah_gate,
    prove_tadammun_gate,
    prove_word_capability_boundary,
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

_FORBIDDEN_D3_OUTPUTS = (
    "Iltizam",
    "DalalahMatrix",
    "WordCapabilityVerdict",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
)

_FORBIDDEN_D4_OUTPUTS = (
    "DalalahMatrix",
    "WordCapabilityVerdict",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
    "Ontology",
)

_FORBIDDEN_D5_OUTPUTS = (
    "DalalahMatrixVerdict",
    "WordCapabilityVerdict",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
    "Ontology",
)

_FORBIDDEN_D6_OUTPUTS = (
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Tanzil",
    "Reality",
    "TruthValue",
    "Ontology",
    "FinalMeaning",
)

_OUTSIDE_MADLUL_PART_REF = "judgment"


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
    expected_state = (
        ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    )
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


def _declare_d3(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    failure_code: FailureCode | None = None,
) -> None:
    expected_state = (
        ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    )
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
            "LAFZI-D3",
            "TadammunGateResult",
        ),
        expected_state=expected_state,
        expected_failure_code=failure_code,
        forbidden_outputs=_FORBIDDEN_D3_OUTPUTS,
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


def _declare_d4(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    failure_code: FailureCode | None = None,
) -> None:
    expected_state = (
        ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    )
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
            "LAFZI-D3",
            "TadammunGateResult",
            "LAFZI-D4",
            "IltizamGateResult",
        ),
        expected_state=expected_state,
        expected_failure_code=failure_code,
        forbidden_outputs=_FORBIDDEN_D4_OUTPUTS,
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


def _declare_d5(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    failure_code: FailureCode | None = None,
) -> None:
    expected_state = (
        ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    )
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
            "LAFZI-D3",
            "TadammunGateResult",
            "LAFZI-D4",
            "IltizamGateResult",
            "LAFZI-D5",
            "DalalahMatrixResidualAuditResult",
        ),
        expected_state=expected_state,
        expected_failure_code=failure_code,
        forbidden_outputs=_FORBIDDEN_D5_OUTPUTS,
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


def _declare_d6(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    failure_code: FailureCode | None = None,
) -> None:
    expected_state = (
        ClosureState.BLOCKED if failure_code is not None else ClosureState.MINIMALLY_CLOSED
    )
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
            "LAFZI-D3",
            "TadammunGateResult",
            "LAFZI-D4",
            "IltizamGateResult",
            "LAFZI-D5",
            "DalalahMatrixResidualAuditResult",
            "LAFZI-D6",
            "DalalahMatrixClosed",
            "WordCapabilityBoundary",
        ),
        expected_state=expected_state,
        expected_failure_code=failure_code,
        forbidden_outputs=_FORBIDDEN_D6_OUTPUTS,
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


def _tadammun_result(
    *,
    claimed_internal_part_ref: str = "human",
    residuals: tuple[CoupledDalalahResidual, ...] = (),
) -> TadammunGateResult:
    mutabaqah = prove_mutabaqah_gate(_surface(residuals=residuals), trace_ref="trace://d2")
    return prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref=claimed_internal_part_ref,
        trace_ref="trace://d3",
    )


def _iltizam_result(
    *,
    tadammun: TadammunGateResult | None = None,
    claimed_external_lazim_ref: str = "lazim://laughing-capacity",
    luzum_evidence_ref: str = "evidence://luzum-human-laughing-capacity",
) -> IltizamGateResult:
    return prove_iltizam_gate(
        tadammun or _tadammun_result(),
        claimed_external_lazim_ref=claimed_external_lazim_ref,
        luzum_evidence_ref=luzum_evidence_ref,
        trace_ref="trace://d4",
    )


def _dalalah_matrix_audit_result(
    *,
    iltizam: IltizamGateResult | None = None,
) -> DalalahMatrixResidualAuditResult:
    return prove_dalalah_matrix_residual_audit(
        iltizam or _iltizam_result(),
        trace_ref="trace://d5",
    )


def _dalalah_matrix_closed(
    *,
    audit: DalalahMatrixResidualAuditResult | None = None,
) -> DalalahMatrixClosed:
    return prove_dalalah_matrix_closed(
        audit or _dalalah_matrix_audit_result(),
        trace_ref="trace://d6-matrix",
    )


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
        "DalalahMatrixVerdict",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "Reality",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(coupled_dalalah, name)
    assert LAFZI_D1_FORBIDDEN_OUTPUTS
    assert "D1C8HandoffCard" in exported
    assert "MutabaqahGateResult" in exported
    assert "prove_mutabaqah_gate" in exported
    assert "TadammunGateResult" in exported
    assert "prove_tadammun_gate" in exported


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


def test_mutabaqah_gate_result_does_not_emit_tadammun_or_iltizam() -> None:
    _declare_d2("D2 does not open D3 or D4", produced_outputs=frozenset({LAFZI_D2_ALLOWED_OUTPUT}))
    result = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    assert result.output == LAFZI_D2_ALLOWED_OUTPUT
    assert "TADAMMUN" in result.forbidden_outputs
    assert "ILTIZAM" in result.forbidden_outputs
    assert not hasattr(result, "claimed_internal_part_ref")


def test_tadammun_gate_accepts_minimal_mutabaqah_result() -> None:
    _declare_d3("minimal TadammunGate", produced_outputs=frozenset({LAFZI_D3_ALLOWED_OUTPUT}))
    mutabaqah = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )
    field_names = {field.name for field in dataclasses.fields(TadammunGateResult)}

    for field_name in (
        "source_result",
        "mutabaqah_gate_result_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "claimed_internal_part_ref",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is TadammunGateState.PROVEN
    assert result.output == LAFZI_D3_ALLOWED_OUTPUT
    assert result.rank is LAFZI_D3_RANK_CEILING
    assert result.rank is mutabaqah.rank
    assert result.mutabaqah_gate_result_ref == mutabaqah.trace_ref
    assert result.madlul_boundary_ref == mutabaqah.madlul_boundary_ref
    assert result.included_surface == mutabaqah.included_surface
    assert result.claimed_internal_part_ref == "human"
    assert result.forbidden_outputs == LAFZI_D3_FORBIDDEN_OUTPUTS


def test_tadammun_gate_refuses_missing_mutabaqah_predecessor() -> None:
    _declare_d3("TadammunGate requires D2 result", failure_code=FailureCode.GATE_REQUIRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_tadammun_gate(
            _surface(),  # type: ignore[arg-type]
            claimed_internal_part_ref="human",
            trace_ref="trace://d3",
        )


def test_tadammun_gate_refuses_missing_trace() -> None:
    _declare_d3("TadammunGate requires trace", failure_code=FailureCode.TRACE_MISSING)
    mutabaqah = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_tadammun_gate(mutabaqah, claimed_internal_part_ref="human", trace_ref="")


def test_tadammun_gate_preserves_identity_trace_boundary_domain_and_scope() -> None:
    _declare_d3("TadammunGate preserves D2 identity and boundary")
    mutabaqah = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="male",
        trace_ref="trace://d3",
    )

    assert result.source_result is mutabaqah
    assert result.mutabaqah_gate_result_ref == "trace://d2"
    assert result.trace_ref == "trace://d3"
    assert result.wadi_madlul_closed_ref == mutabaqah.wadi_madlul_closed_ref
    assert result.lafzi_madlul_closed_ref == mutabaqah.lafzi_madlul_closed_ref
    assert result.madlul_boundary_ref == mutabaqah.madlul_boundary_ref
    assert result.domain_ref == mutabaqah.domain_ref
    assert result.scope_ref == mutabaqah.scope_ref


def test_tadammun_gate_preserves_visible_residuals_without_erasing_d2_residuals() -> None:
    _declare_d3("TadammunGate residual visibility")
    residual = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
        trace_ref="trace://visible-d2-residual",
    )
    mutabaqah = prove_mutabaqah_gate(_surface(residuals=(residual,)), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )

    assert result.state is TadammunGateState.DEFERRED
    assert result.residuals[: len(mutabaqah.residuals)] == mutabaqah.residuals
    assert residual in result.residuals


def test_tadammun_gate_refuses_hidden_residual() -> None:
    _declare_d3("TadammunGate refuses hidden residual", failure_code=FailureCode.HIDDEN_RESIDUAL)
    result = prove_tadammun_gate(
        prove_mutabaqah_gate(_surface(), trace_ref="trace://d2"),
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(result, residuals=(object(),))  # type: ignore[arg-type]


def test_tadammun_gate_refuses_rank_promotion() -> None:
    _declare_d3(
        "TadammunGate rank ceiling",
        failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
    )
    result = prove_tadammun_gate(
        prove_mutabaqah_gate(_surface(), trace_ref="trace://d2"),
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )

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
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING.value),
    ],
)
def test_tadammun_gate_refuses_boundary_or_domain_drift(
    field_name: str,
    value: object,
    match: str,
) -> None:
    _declare_d3("TadammunGate refuses boundary or domain drift")
    result = prove_tadammun_gate(
        prove_mutabaqah_gate(_surface(), trace_ref="trace://d2"),
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )

    with pytest.raises(WeightCarrierSchemaError, match=match):
        dataclasses.replace(result, **{field_name: value})


def test_tadammun_gate_residualizes_missing_internal_part() -> None:
    _declare_d3("TadammunGate requires internal part")
    mutabaqah = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="",
        trace_ref="trace://d3",
    )

    assert result.state is TadammunGateState.DEFERRED
    assert any(
        residual.kind is CoupledDalalahResidualKind.INTERNAL_PART_REQUIRED
        for residual in result.residuals
    )


def test_tadammun_gate_blocks_part_outside_madlul_boundary() -> None:
    _declare_d3("TadammunGate blocks part outside boundary")
    mutabaqah = prove_mutabaqah_gate(_surface(), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="judgment",
        trace_ref="trace://d3",
    )

    assert result.state is TadammunGateState.BLOCKED
    assert any(
        residual.kind is CoupledDalalahResidualKind.PART_OUTSIDE_MADLUL
        and residual.blocking
        for residual in result.residuals
    )


def test_tadammun_gate_preserves_blocking_policy_from_d2() -> None:
    _declare_d3("TadammunGate preserves blocking residual policy")
    blocker = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
        trace_ref="trace://blocking-d2-residual",
        blocking=True,
    )
    mutabaqah = prove_mutabaqah_gate(_surface(residuals=(blocker,)), trace_ref="trace://d2")
    result = prove_tadammun_gate(
        mutabaqah,
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )

    assert mutabaqah.state is MutabaqahGateState.BLOCKED
    assert result.state is TadammunGateState.BLOCKED
    assert result.residuals[: len(mutabaqah.residuals)] == mutabaqah.residuals


def test_tadammun_gate_does_not_open_forbidden_downstream_outputs() -> None:
    _declare_d3("D3 does not open D4 D5 D6 or semantic outputs")
    result = prove_tadammun_gate(
        prove_mutabaqah_gate(_surface(), trace_ref="trace://d2"),
        claimed_internal_part_ref="human",
        trace_ref="trace://d3",
    )
    exported = set(coupled_dalalah.__all__)

    assert result.output == LAFZI_D3_ALLOWED_OUTPUT
    assert "TADAMMUN" not in result.forbidden_outputs
    assert "ILTIZAM" in result.forbidden_outputs
    assert "DALALAH_MATRIX" in result.forbidden_outputs
    assert "IltizamGateResult" in exported
    assert "DalalahMatrixClosed" in exported
    assert "WordCapabilityBoundary" in exported
    assert "prove_iltizam_gate" in exported
    for forbidden in ("Ifadah", "Mafhum", "Hukm", "Tanzil", "Reality"):
        assert (
            forbidden.upper() in result.forbidden_outputs
            or forbidden in result.forbidden_outputs
        )
        assert not hasattr(result, forbidden.lower())


def test_iltizam_gate_accepts_minimal_tadammun_result() -> None:
    _declare_d4("minimal IltizamGate", produced_outputs=frozenset({LAFZI_D4_ALLOWED_OUTPUT}))
    tadammun = _tadammun_result()
    result = _iltizam_result(tadammun=tadammun)
    field_names = {field.name for field in dataclasses.fields(IltizamGateResult)}

    for field_name in (
        "source_result",
        "tadammun_gate_result_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "claimed_external_lazim_ref",
        "luzum_evidence_ref",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is IltizamGateState.PROVEN
    assert result.output == LAFZI_D4_ALLOWED_OUTPUT
    assert result.rank is LAFZI_D4_RANK_CEILING
    assert result.rank is tadammun.rank
    assert result.tadammun_gate_result_ref == tadammun.trace_ref
    assert result.madlul_boundary_ref == tadammun.madlul_boundary_ref
    assert result.included_surface == tadammun.included_surface
    assert result.claimed_external_lazim_ref == "lazim://laughing-capacity"
    assert result.luzum_evidence_ref == "evidence://luzum-human-laughing-capacity"
    assert result.forbidden_outputs == LAFZI_D4_FORBIDDEN_OUTPUTS


def test_iltizam_gate_export_surface_exposes_only_licensed_d4_symbols() -> None:
    _declare_d4("D4 export surface", produced_outputs=frozenset({LAFZI_D4_ALLOWED_OUTPUT}))

    exported = set(coupled_dalalah.__all__)
    assert "IltizamGateResult" in exported
    assert "IltizamGateState" in exported
    assert "prove_iltizam_gate" in exported
    assert LAFZI_D4_ALLOWED_OUTPUT == "ILTIZAM_GATE_RESULT"
    assert "ILTIZAM" not in LAFZI_D4_FORBIDDEN_OUTPUTS
    for forbidden in (
        "DALALAH_MATRIX",
        "WORD_CAPABILITY",
        "IFADAH",
        "MAFHUM",
        "HUKM",
        "TANZIL",
        "REALITY",
        "TRUTH_VALUE",
        "ONTOLOGY",
    ):
        assert forbidden in LAFZI_D4_FORBIDDEN_OUTPUTS
    for forbidden_export in (
        "DalalahMatrixVerdict",
        "WordCapabilityVerdict",
        "Reality",
        "Truth",
        "Ontology",
    ):
        assert forbidden_export not in exported
        assert not hasattr(coupled_dalalah, forbidden_export)


def test_iltizam_gate_refuses_missing_or_wrong_tadammun_predecessor() -> None:
    _declare_d4("IltizamGate requires D3 result", failure_code=FailureCode.GATE_REQUIRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_iltizam_gate(
            prove_mutabaqah_gate(_surface(), trace_ref="trace://d2"),  # type: ignore[arg-type]
            claimed_external_lazim_ref="lazim://laughing-capacity",
            luzum_evidence_ref="evidence://luzum",
            trace_ref="trace://d4",
        )


def test_iltizam_gate_refuses_missing_trace() -> None:
    _declare_d4("IltizamGate requires trace", failure_code=FailureCode.TRACE_MISSING)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_iltizam_gate(
            _tadammun_result(),
            claimed_external_lazim_ref="lazim://laughing-capacity",
            luzum_evidence_ref="evidence://luzum",
            trace_ref="",
        )


def test_iltizam_gate_preserves_identity_trace_boundary_domain_and_scope() -> None:
    _declare_d4("IltizamGate preserves D3 identity and boundary")
    tadammun = _tadammun_result()
    result = _iltizam_result(tadammun=tadammun)

    assert result.source_result is tadammun
    assert result.tadammun_gate_result_ref == "trace://d3"
    assert result.trace_ref == "trace://d4"
    assert result.wadi_madlul_closed_ref == tadammun.wadi_madlul_closed_ref
    assert result.lafzi_madlul_closed_ref == tadammun.lafzi_madlul_closed_ref
    assert result.madlul_boundary_ref == tadammun.madlul_boundary_ref
    assert result.domain_ref == tadammun.domain_ref
    assert result.scope_ref == tadammun.scope_ref


def test_iltizam_gate_preserves_visible_residuals_without_erasing_d3_residuals() -> None:
    _declare_d4("IltizamGate residual ancestry")
    residual = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
        trace_ref="trace://visible-d2-residual",
    )
    tadammun = _tadammun_result(residuals=(residual,))
    result = _iltizam_result(tadammun=tadammun)

    assert result.state is IltizamGateState.DEFERRED
    assert result.residuals[: len(tadammun.residuals)] == tadammun.residuals
    assert residual in result.residuals


def test_iltizam_gate_refuses_hidden_residual() -> None:
    _declare_d4("IltizamGate refuses hidden residual", failure_code=FailureCode.HIDDEN_RESIDUAL)
    result = _iltizam_result()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(result, residuals=(object(),))  # type: ignore[arg-type]


def test_iltizam_gate_refuses_rank_promotion() -> None:
    _declare_d4("IltizamGate rank ceiling", failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE)
    result = _iltizam_result()

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
        ("scope_ref", "scope://other", FailureCode.IDENTITY_BROKEN.value),
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING.value),
    ],
)
def test_iltizam_gate_refuses_boundary_domain_or_scope_drift(
    field_name: str,
    value: object,
    match: str,
) -> None:
    _declare_d4("IltizamGate refuses boundary domain or scope drift")
    result = _iltizam_result()

    with pytest.raises(WeightCarrierSchemaError, match=match):
        dataclasses.replace(result, **{field_name: value})


def test_iltizam_gate_residualizes_missing_external_lazim() -> None:
    _declare_d4("IltizamGate requires external lazim")
    result = _iltizam_result(claimed_external_lazim_ref="")

    assert result.state is IltizamGateState.DEFERRED
    assert result.claimed_external_lazim_ref == "UNPROVEN_EXTERNAL_LAZIM"
    assert any(
        residual.kind is CoupledDalalahResidualKind.LAZIM_OUTSIDE_REQUIRED
        for residual in result.residuals
    )


def test_iltizam_gate_blocks_lazim_inside_madlul_boundary() -> None:
    _declare_d4("IltizamGate requires lazim outside madlul")
    result = _iltizam_result(claimed_external_lazim_ref="human")

    assert result.state is IltizamGateState.BLOCKED
    assert any(
        residual.kind is CoupledDalalahResidualKind.LAZIM_OUTSIDE_REQUIRED
        and residual.blocking
        for residual in result.residuals
    )


def test_iltizam_gate_residualizes_missing_luzum_evidence() -> None:
    _declare_d4("IltizamGate requires luzum evidence")
    result = _iltizam_result(luzum_evidence_ref="")

    assert result.state is IltizamGateState.DEFERRED
    assert result.luzum_evidence_ref == "UNPROVEN_LUZUM_EVIDENCE"
    assert any(
        residual.kind is CoupledDalalahResidualKind.LUZUM_EVIDENCE_REQUIRED
        for residual in result.residuals
    )


def test_iltizam_gate_blocks_mere_association_not_luzum() -> None:
    _declare_d4("IltizamGate refuses mere association")
    result = _iltizam_result(luzum_evidence_ref="association://habit")

    assert result.state is IltizamGateState.BLOCKED
    assert any(
        residual.kind is CoupledDalalahResidualKind.MERE_ASSOCIATION_NOT_LUZUM
        and residual.blocking
        for residual in result.residuals
    )


def test_iltizam_gate_preserves_blocking_and_deferred_policy_from_d3() -> None:
    _declare_d4("IltizamGate preserves D3 blocking and deferred policy")
    blocked_d3 = _tadammun_result(claimed_internal_part_ref="judgment")
    blocked_d4 = _iltizam_result(tadammun=blocked_d3)
    deferred_d3 = _tadammun_result(claimed_internal_part_ref="")
    deferred_d4 = _iltizam_result(tadammun=deferred_d3)

    assert blocked_d3.state is TadammunGateState.BLOCKED
    assert blocked_d4.state is IltizamGateState.BLOCKED
    assert blocked_d4.residuals[: len(blocked_d3.residuals)] == blocked_d3.residuals
    assert deferred_d3.state is TadammunGateState.DEFERRED
    assert deferred_d4.state is IltizamGateState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(deferred_d4, state=IltizamGateState.PROVEN)


def test_iltizam_gate_does_not_open_matrix_closure_or_downstream_outputs() -> None:
    _declare_d4("D4 does not open D5 D6 or semantic outputs")
    result = _iltizam_result()
    exported = set(coupled_dalalah.__all__)

    assert result.output == LAFZI_D4_ALLOWED_OUTPUT
    assert "ILTIZAM" not in result.forbidden_outputs
    assert "DALALAH_MATRIX" in result.forbidden_outputs
    assert "WORD_CAPABILITY" in result.forbidden_outputs
    assert "DalalahMatrixClosed" in exported
    assert "WordCapabilityBoundary" in exported
    for forbidden in ("Ifadah", "Mafhum", "Hukm", "Tanzil", "Reality", "Truth", "Ontology"):
        assert (
            forbidden.upper() in result.forbidden_outputs
            or f"{forbidden.upper()}_VALUE" in result.forbidden_outputs
            or forbidden in result.forbidden_outputs
        )
        assert not hasattr(result, forbidden.lower())


def test_dalalah_matrix_residual_audit_accepts_minimal_d4_chain() -> None:
    _declare_d5(
        "minimal DalalahMatrixResidualAudit",
        produced_outputs=frozenset({LAFZI_D5_ALLOWED_OUTPUT}),
    )
    iltizam = _iltizam_result()
    result = _dalalah_matrix_audit_result(iltizam=iltizam)
    field_names = {field.name for field in dataclasses.fields(DalalahMatrixResidualAuditResult)}

    for field_name in (
        "source_result",
        "iltizam_gate_result_ref",
        "tadammun_gate_result_ref",
        "mutabaqah_gate_result_ref",
        "coupled_dalalah_surface_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "claimed_internal_part_ref",
        "claimed_external_lazim_ref",
        "luzum_evidence_ref",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is DalalahMatrixResidualAuditState.PROVEN
    assert result.output == LAFZI_D5_ALLOWED_OUTPUT
    assert result.output != "DALALAH_MATRIX_CLOSED"
    assert result.rank is LAFZI_D5_RANK_CEILING
    assert result.rank is iltizam.rank
    assert result.iltizam_gate_result_ref == iltizam.trace_ref
    assert result.tadammun_gate_result_ref == iltizam.source_result.trace_ref
    assert result.mutabaqah_gate_result_ref == iltizam.source_result.source_result.trace_ref
    assert (
        result.coupled_dalalah_surface_ref
        == iltizam.source_result.source_result.source_surface.trace_ref
    )
    assert result.forbidden_outputs == LAFZI_D5_FORBIDDEN_OUTPUTS


def test_dalalah_matrix_residual_audit_export_surface_exposes_only_d5_symbols() -> None:
    _declare_d5("D5 export surface", produced_outputs=frozenset({LAFZI_D5_ALLOWED_OUTPUT}))

    exported = set(coupled_dalalah.__all__)
    assert "DalalahMatrixResidualAuditResult" in exported
    assert "DalalahMatrixResidualAuditState" in exported
    assert "prove_dalalah_matrix_residual_audit" in exported
    assert LAFZI_D5_ALLOWED_OUTPUT == "DALALAH_MATRIX_RESIDUAL_AUDIT_RESULT"
    for forbidden in (
        "DALALAH_MATRIX_CLOSED",
        "WORD_CAPABILITY",
        "IFADAH",
        "MAFHUM",
        "HUKM",
        "TANZIL",
        "REALITY",
        "TRUTH_VALUE",
        "ONTOLOGY",
        "FINAL_MEANING",
    ):
        assert forbidden in LAFZI_D5_FORBIDDEN_OUTPUTS
    for forbidden_export in (
        "DalalahMatrixVerdict",
        "WordCapabilityVerdict",
        "Ifadah",
        "Mafhum",
        "Hukm",
        "Tanzil",
        "Reality",
        "Truth",
        "Ontology",
    ):
        assert forbidden_export not in exported
        assert not hasattr(coupled_dalalah, forbidden_export)


def test_dalalah_matrix_residual_audit_preserves_identity_trace_boundary_domain_scope() -> None:
    _declare_d5("D5 preserves D1-D4 identity and boundary")
    iltizam = _iltizam_result()
    result = _dalalah_matrix_audit_result(iltizam=iltizam)

    assert result.source_result is iltizam
    assert result.trace_ref == "trace://d5"
    assert result.wadi_madlul_closed_ref == iltizam.wadi_madlul_closed_ref
    assert result.lafzi_madlul_closed_ref == iltizam.lafzi_madlul_closed_ref
    assert result.madlul_boundary_ref == iltizam.madlul_boundary_ref
    assert result.included_surface == iltizam.included_surface
    assert result.excluded_surface == iltizam.excluded_surface
    assert result.domain_ref == iltizam.domain_ref
    assert result.scope_ref == iltizam.scope_ref
    assert result.claimed_internal_part_ref == iltizam.source_result.claimed_internal_part_ref
    assert result.claimed_external_lazim_ref == iltizam.claimed_external_lazim_ref
    assert result.luzum_evidence_ref == iltizam.luzum_evidence_ref


def test_dalalah_matrix_residual_audit_preserves_d1_d2_d3_d4_residual_ancestry() -> None:
    _declare_d5("D5 residual ancestry")
    residual = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
        trace_ref="trace://visible-d2-residual",
    )
    iltizam = _iltizam_result(tadammun=_tadammun_result(residuals=(residual,)))
    result = _dalalah_matrix_audit_result(iltizam=iltizam)

    assert iltizam.state is IltizamGateState.DEFERRED
    assert result.state is DalalahMatrixResidualAuditState.DEFERRED
    assert result.residuals == iltizam.residuals
    assert residual in result.residuals
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(result, residuals=())


def test_dalalah_matrix_residual_audit_refuses_missing_or_wrong_d4_predecessor() -> None:
    _declare_d5("D5 requires IltizamGateResult", failure_code=FailureCode.GATE_REQUIRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_dalalah_matrix_residual_audit(
            _tadammun_result(),  # type: ignore[arg-type]
            trace_ref="trace://d5",
        )


def test_dalalah_matrix_residual_audit_refuses_missing_trace() -> None:
    _declare_d5("D5 requires trace", failure_code=FailureCode.TRACE_MISSING)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_dalalah_matrix_residual_audit(_iltizam_result(), trace_ref="")


@pytest.mark.parametrize(
    ("field_name", "value", "match"),
    [
        ("included_surface", ("unrelated",), FailureCode.IDENTITY_BROKEN.value),
        ("domain_ref", "domain://other", "DOMAIN_MISMATCH"),
        ("scope_ref", "scope://other", FailureCode.IDENTITY_BROKEN.value),
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING.value),
        ("iltizam_gate_result_ref", "trace://other-d4", FailureCode.IDENTITY_BROKEN.value),
    ],
)
def test_dalalah_matrix_residual_audit_refuses_identity_boundary_domain_or_scope_drift(
    field_name: str,
    value: object,
    match: str,
) -> None:
    _declare_d5("D5 refuses identity boundary domain or scope drift")
    result = _dalalah_matrix_audit_result()

    with pytest.raises(WeightCarrierSchemaError, match=match):
        dataclasses.replace(result, **{field_name: value})


def test_dalalah_matrix_residual_audit_refuses_rank_promotion() -> None:
    _declare_d5("D5 rank ceiling", failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE)
    result = _dalalah_matrix_audit_result()

    with pytest.raises(
        WeightCarrierSchemaError,
        match=FailureCode.RANK_PROMOTION_WITHOUT_GATE.value,
    ):
        dataclasses.replace(result, rank=Rank.TRACE)


def test_dalalah_matrix_residual_audit_refuses_hidden_residuals() -> None:
    _declare_d5("D5 refuses hidden residual", failure_code=FailureCode.HIDDEN_RESIDUAL)
    result = _dalalah_matrix_audit_result()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(result, residuals=(object(),))  # type: ignore[arg-type]


def test_dalalah_matrix_residual_audit_preserves_blocking_and_deferred_policy_from_d4() -> None:
    _declare_d5("D5 preserves D4 blocking and deferred policy")
    blocked_d4 = _iltizam_result(tadammun=_tadammun_result(claimed_internal_part_ref="judgment"))
    blocked_d5 = _dalalah_matrix_audit_result(iltizam=blocked_d4)
    deferred_d4 = _iltizam_result(luzum_evidence_ref="")
    deferred_d5 = _dalalah_matrix_audit_result(iltizam=deferred_d4)

    assert blocked_d4.state is IltizamGateState.BLOCKED
    assert blocked_d5.state is DalalahMatrixResidualAuditState.BLOCKED
    assert deferred_d4.state is IltizamGateState.DEFERRED
    assert deferred_d5.state is DalalahMatrixResidualAuditState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(blocked_d5, state=DalalahMatrixResidualAuditState.DEFERRED)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(deferred_d5, state=DalalahMatrixResidualAuditState.PROVEN)


def test_dalalah_matrix_residual_audit_visible_residuals_prevent_proven_clearance() -> None:
    _declare_d5("D5 visible residuals prevent proven clearance")
    residual = CoupledDalalahResidual(
        kind=CoupledDalalahResidualKind.LUZUM_EVIDENCE_REQUIRED,
        trace_ref="trace://visible-d4-residual",
    )
    iltizam = _iltizam_result(tadammun=_tadammun_result(residuals=(residual,)))
    result = _dalalah_matrix_audit_result(iltizam=iltizam)

    assert result.state is DalalahMatrixResidualAuditState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(result, state=DalalahMatrixResidualAuditState.PROVEN)


def test_dalalah_matrix_residual_audit_does_not_emit_matrix_closed_or_downstream_outputs() -> None:
    _declare_d5("D5 does not open D6 or semantic outputs")
    result = _dalalah_matrix_audit_result()
    exported = set(coupled_dalalah.__all__)

    assert result.output == LAFZI_D5_ALLOWED_OUTPUT
    assert "DALALAH_MATRIX_CLOSED" in result.forbidden_outputs
    assert "WORD_CAPABILITY" in result.forbidden_outputs
    assert "DalalahMatrixClosed" in exported
    assert "WordCapabilityBoundary" in exported
    for forbidden in ("Ifadah", "Mafhum", "Hukm", "Tanzil", "Reality", "Truth", "Ontology"):
        assert (
            forbidden.upper() in result.forbidden_outputs
            or f"{forbidden.upper()}_VALUE" in result.forbidden_outputs
            or forbidden in result.forbidden_outputs
        )
        assert not hasattr(result, forbidden.lower())


def test_dalalah_matrix_closed_accepts_minimal_d5_audit() -> None:
    _declare_d6(
        "minimal DalalahMatrixClosed",
        produced_outputs=frozenset({LAFZI_D6_MATRIX_CLOSED_ALLOWED_OUTPUT}),
    )
    audit = _dalalah_matrix_audit_result()
    result = _dalalah_matrix_closed(audit=audit)
    field_names = {field.name for field in dataclasses.fields(DalalahMatrixClosed)}

    for field_name in (
        "source_result",
        "residual_audit_result_ref",
        "iltizam_gate_result_ref",
        "tadammun_gate_result_ref",
        "mutabaqah_gate_result_ref",
        "coupled_dalalah_surface_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "claimed_internal_part_ref",
        "claimed_external_lazim_ref",
        "luzum_evidence_ref",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is DalalahMatrixClosedState.PROVEN
    assert result.output == LAFZI_D6_MATRIX_CLOSED_ALLOWED_OUTPUT
    assert result.rank is LAFZI_D6_RANK_CEILING
    assert result.rank is audit.rank
    assert result.residual_audit_result_ref == audit.trace_ref
    assert result.iltizam_gate_result_ref == audit.iltizam_gate_result_ref
    assert result.mutabaqah_gate_result_ref == audit.mutabaqah_gate_result_ref
    assert result.coupled_dalalah_surface_ref == audit.coupled_dalalah_surface_ref
    assert result.forbidden_outputs == LAFZI_D6_FORBIDDEN_OUTPUTS


def test_word_capability_boundary_accepts_minimal_matrix_closure() -> None:
    _declare_d6(
        "minimal WordCapability boundary",
        produced_outputs=frozenset({LAFZI_D6_WORD_CAPABILITY_ALLOWED_OUTPUT}),
    )
    matrix = _dalalah_matrix_closed()
    result = prove_word_capability_boundary(matrix, trace_ref="trace://d6-word")
    field_names = {field.name for field in dataclasses.fields(WordCapabilityBoundary)}

    for field_name in (
        "source_matrix",
        "matrix_closed_ref",
        "residual_audit_result_ref",
        "iltizam_gate_result_ref",
        "tadammun_gate_result_ref",
        "mutabaqah_gate_result_ref",
        "coupled_dalalah_surface_ref",
        "wadi_madlul_closed_ref",
        "lafzi_madlul_closed_ref",
        "madlul_boundary_ref",
        "included_surface",
        "excluded_surface",
        "claimed_internal_part_ref",
        "claimed_external_lazim_ref",
        "luzum_evidence_ref",
        "domain_ref",
        "scope_ref",
        "residuals",
        "rank",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in field_names
    assert result.state is WordCapabilityBoundaryState.PROVEN
    assert result.output == LAFZI_D6_WORD_CAPABILITY_ALLOWED_OUTPUT
    assert result.matrix_closed_ref == matrix.trace_ref
    assert result.rank is matrix.rank
    assert result.residuals == matrix.residuals
    assert result.forbidden_outputs == LAFZI_D6_FORBIDDEN_OUTPUTS


def test_lafzi_d6_export_surface_exposes_only_licensed_d6_symbols() -> None:
    _declare_d6("D6 export surface")
    exported = set(coupled_dalalah.__all__)

    for symbol in (
        "DalalahMatrixClosed",
        "DalalahMatrixClosedState",
        "WordCapabilityBoundary",
        "WordCapabilityBoundaryState",
        "prove_dalalah_matrix_closed",
        "prove_word_capability_boundary",
    ):
        assert symbol in exported
    for forbidden in (
        "IFADAH",
        "MAFHUM",
        "HUKM",
        "TANZIL",
        "REALITY",
        "TRUTH_VALUE",
        "ONTOLOGY",
        "FINAL_MEANING",
    ):
        assert forbidden in LAFZI_D6_FORBIDDEN_OUTPUTS
    for forbidden_export in (
        "IfadahVerdict",
        "MafhumVerdict",
        "HukmAuthority",
        "TanzilReality",
        "TruthValue",
        "Ontology",
        "FinalMeaning",
    ):
        assert forbidden_export not in exported
        assert not hasattr(coupled_dalalah, forbidden_export)


def test_d6_preserves_identity_boundary_domain_scope_trace_rank_and_residuals() -> None:
    _declare_d6("D6 preserves matrix ancestry")
    audit = _dalalah_matrix_audit_result()
    matrix = _dalalah_matrix_closed(audit=audit)
    word_boundary = prove_word_capability_boundary(matrix, trace_ref="trace://d6-word")

    assert matrix.source_result is audit
    assert matrix.trace_ref == "trace://d6-matrix"
    assert matrix.wadi_madlul_closed_ref == audit.wadi_madlul_closed_ref
    assert matrix.lafzi_madlul_closed_ref == audit.lafzi_madlul_closed_ref
    assert matrix.madlul_boundary_ref == audit.madlul_boundary_ref
    assert matrix.included_surface == audit.included_surface
    assert matrix.excluded_surface == audit.excluded_surface
    assert matrix.domain_ref == audit.domain_ref
    assert matrix.scope_ref == audit.scope_ref
    assert word_boundary.source_matrix is matrix
    assert word_boundary.trace_ref == "trace://d6-word"
    assert word_boundary.domain_ref == matrix.domain_ref
    assert word_boundary.scope_ref == matrix.scope_ref


def test_d6_refuses_missing_or_wrong_predecessors() -> None:
    _declare_d6("D6 predecessors are gates", failure_code=FailureCode.GATE_REQUIRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_dalalah_matrix_closed(_iltizam_result(), trace_ref="trace://d6")  # type: ignore[arg-type]
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_word_capability_boundary(
            _dalalah_matrix_audit_result(),  # type: ignore[arg-type]
            trace_ref="trace://d6-word",
        )


def test_d6_refuses_missing_trace() -> None:
    _declare_d6("D6 trace required", failure_code=FailureCode.TRACE_MISSING)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_dalalah_matrix_closed(_dalalah_matrix_audit_result(), trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_word_capability_boundary(_dalalah_matrix_closed(), trace_ref="")


def test_d6_refuses_hidden_residual_erasure_and_rank_promotion() -> None:
    _declare_d6("D6 residual and rank discipline", failure_code=FailureCode.HIDDEN_RESIDUAL)
    matrix = _dalalah_matrix_closed()
    word_boundary = prove_word_capability_boundary(matrix, trace_ref="trace://d6-word")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(matrix, residuals=(object(),))  # type: ignore[arg-type]
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        dataclasses.replace(word_boundary, residuals=(object(),))  # type: ignore[arg-type]
    with pytest.raises(
        WeightCarrierSchemaError,
        match=FailureCode.RANK_PROMOTION_WITHOUT_GATE.value,
    ):
        dataclasses.replace(matrix, rank=Rank.TRACE)


@pytest.mark.parametrize(
    ("field_name", "value", "match"),
    [
        ("wadi_madlul_closed_ref", "wadi-contract://other", FailureCode.IDENTITY_BROKEN.value),
        ("included_surface", ("unrelated",), FailureCode.IDENTITY_BROKEN.value),
        ("domain_ref", "domain://other", "DOMAIN_MISMATCH"),
        ("scope_ref", "scope://other", FailureCode.IDENTITY_BROKEN.value),
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING.value),
    ],
)
def test_d6_refuses_identity_boundary_domain_or_scope_drift(
    field_name: str,
    value: object,
    match: str,
) -> None:
    _declare_d6(f"D6 refuses {field_name} drift")
    matrix = _dalalah_matrix_closed()

    with pytest.raises(WeightCarrierSchemaError, match=match):
        dataclasses.replace(matrix, **{field_name: value})


def test_d6_blocked_or_deferred_d5_prevents_matrix_closure_and_word_capability() -> None:
    _declare_d6("D6 preserves blocked and deferred D5 policy")
    blocked_d5 = _dalalah_matrix_audit_result(
        iltizam=_iltizam_result(
            tadammun=_tadammun_result(claimed_internal_part_ref=_OUTSIDE_MADLUL_PART_REF)
        )
    )
    deferred_d5 = _dalalah_matrix_audit_result(iltizam=_iltizam_result(luzum_evidence_ref=""))
    blocked_matrix = _dalalah_matrix_closed(audit=blocked_d5)
    deferred_matrix = _dalalah_matrix_closed(audit=deferred_d5)

    assert blocked_d5.state is DalalahMatrixResidualAuditState.BLOCKED
    assert blocked_matrix.state is DalalahMatrixClosedState.BLOCKED
    assert deferred_d5.state is DalalahMatrixResidualAuditState.DEFERRED
    assert deferred_matrix.state is DalalahMatrixClosedState.DEFERRED
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(blocked_matrix, state=DalalahMatrixClosedState.PROVEN)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        dataclasses.replace(deferred_matrix, state=DalalahMatrixClosedState.PROVEN)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_word_capability_boundary(deferred_matrix, trace_ref="trace://d6-word")


def test_d6_does_not_emit_semantic_or_reality_outputs() -> None:
    _declare_d6("D6 forbids semantic and reality outputs")
    matrix = _dalalah_matrix_closed()
    word_boundary = prove_word_capability_boundary(matrix, trace_ref="trace://d6-word")

    assert matrix.output == LAFZI_D6_MATRIX_CLOSED_ALLOWED_OUTPUT
    assert word_boundary.output == LAFZI_D6_WORD_CAPABILITY_ALLOWED_OUTPUT
    for result in (matrix, word_boundary):
        for forbidden in ("Ifadah", "Mafhum", "Hukm", "Tanzil", "Reality", "Truth", "Ontology"):
            assert (
                forbidden.upper() in result.forbidden_outputs
                or f"{forbidden.upper()}_VALUE" in result.forbidden_outputs
                or forbidden in result.forbidden_outputs
            )
            assert not hasattr(result, forbidden.lower())
