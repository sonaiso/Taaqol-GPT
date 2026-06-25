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
    CoupledDalalahResidual,
    CoupledDalalahResidualKind,
    CoupledDalalahSurface,
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


def _closed_c8_result(**contract_overrides: object):
    contract = _valid_contract(**contract_overrides)
    return prove_wadi_to_coupled_dalalah(contract, _prove_c7(contract), trace_ref="trace://c8")


def _surface(**overrides: object) -> CoupledDalalahSurface:
    c8_result = _closed_c8_result()
    values: dict[str, object] = {
        "madlul_boundary_ref": "boundary://human-male",
        "included_surface": ("human", "male"),
        "excluded_surface": ("relation", "judgment"),
        "domain_ref": "domain://arabic",
        "scope_ref": "scope://general-arabic",
        "prior_knowledge_refs": ("origin://sama",),
        "trace_ref": "trace://d1",
    }
    values.update(overrides)
    return CoupledDalalahSurface.from_c8_gate_result(c8_result, **values)  # type: ignore[arg-type]


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
            madlul_boundary_ref="boundary://human-male",
            included_surface=("human",),
            excluded_surface=("judgment",),
            domain_ref="domain://arabic",
            scope_ref="scope://general-arabic",
            prior_knowledge_refs=("origin://sama",),
            trace_ref="trace://d1",
        )


@pytest.mark.parametrize(
    ("field_name", "value", "failure_code"),
    [
        ("madlul_boundary_ref", "", FailureCode.BOUNDARY_MISSING),
        ("included_surface", (), FailureCode.BOUNDARY_MISSING),
        ("domain_ref", "", FailureCode.DOMAIN_MISSING),
        ("scope_ref", "", FailureCode.SCOPE_MISSING),
        ("prior_knowledge_refs", (), FailureCode.REQUIRED_SLOT_EMPTY),
        ("trace_ref", "", FailureCode.TRACE_MISSING),
    ],
)
def test_coupled_dalalah_surface_refuses_missing_birth_guards(
    field_name: str,
    value: object,
    failure_code: FailureCode,
) -> None:
    _declare("D1 birth guards")

    with pytest.raises(WeightCarrierSchemaError, match=failure_code.value):
        _surface(**{field_name: value})


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
    surface = CoupledDalalahSurface(
        c8_gate_result_ref="coupled-dalalah://wadi-contract://rajul",
        wadi_madlul_closed_ref="wadi-contract://rajul",
        lafzi_madlul_closed_ref="trace://lafzi/closed",
        madlul_boundary_ref="boundary://human-male",
        included_surface=("human", "male"),
        excluded_surface=("relation", "judgment"),
        domain_ref="domain://arabic",
        scope_ref="scope://general-arabic",
        prior_knowledge_refs=("origin://sama",),
        c8_residuals=(c8_blocker,),
        residuals=(d1_residual,),
        rank=Rank.CANDIDATE,
        trace_ref="trace://d1",
    )

    assert c8_blocker in surface.c8_residuals
    assert d1_residual in surface.residuals
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        CoupledDalalahResidual(
            kind=CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
            trace_ref="trace://hidden",
            visibility="HIDDEN",  # type: ignore[arg-type]
        )


def test_lafzi_d1_module_exports_no_d2_or_downstream_runtime() -> None:
    _declare("carrier only no D2 runtime", forbidden_outputs=_FORBIDDEN_D1_OUTPUTS)

    exported = set(coupled_dalalah.__all__)
    forbidden_exports = {
        "MutabaqahGate",
        "TadammunGate",
        "IltizamGate",
        "DalalahMatrixVerdict",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "Reality",
        "prove_mutabaqah_gate",
        "prove_tadammun_gate",
        "prove_iltizam_gate",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(coupled_dalalah, name)
    assert LAFZI_D1_FORBIDDEN_OUTPUTS
