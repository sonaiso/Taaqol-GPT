"""Constitutional/runtime tests for DAL-A4 bounded surface gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law) + docs/14 DAL-A4 position
Branch         : DAL-A4 runtime (hamza/shadda/tanwin/sukun/madd only)
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import fields

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.dal_a4_runtime_gates import (
    DAL_A4_FORBIDDEN_OUTPUTS,
    DAL_A4_GATE_ORDER,
    DalA4GateCertificate,
    DalA4GateName,
    DalA4GateResult,
    DalA4GateStatus,
    HamzaSurfaceForm,
    MaddTraceForm,
    ShaddaTraceForm,
    SukunTraceForm,
    TanwinTraceForm,
    evaluate_hamza_resolution_gate,
    evaluate_madd_extension_gate,
    evaluate_shadda_idgham_gate,
    evaluate_sukun_collision_gate,
    evaluate_tanwin_trace_gate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_ORIGIN = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"
_CHAIN = (
    "DalOnlyCandidate",
    "DAL-A1",
    "DAL-A2",
    "DAL-A3",
    "DAL-A4",
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_MODULE = _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "dal_a4_runtime_gates.py"


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A4_FORBIDDEN_OUTPUTS,
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


def test_chain_records_dal_a4_runtime_done_and_dal_a5_admit_current() -> None:
    _declare("chain registration for dal-a4 runtime completion", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(r"DAL-A4\s+Hamza / shadda / tanwin / sukun / madd gates\s+✓ done", roadmap)
    assert re.search(
        r"DAL-A4-ADMIT\s+post-CLOSE-6 admission decision \(DAL-A4 scope only\)\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A5\s+Syllable / transition / adjacency / S1-S5 gates\s+→ current",
        roadmap,
    )
    assert re.search(r"DAL-A4\s+Hamza / shadda / tanwin / sukun / madd gates\s+✓ done", claude)
    assert re.search(
        r"DAL-A4-ADMIT\s+post-CLOSE-6 admission decision \(DAL-A4 scope only\)\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done",
        claude,
    )


def test_dal_a4_gate_surface_exists() -> None:
    _declare(
        "gate classes/functions exist",
        frozenset({"HamzaResolutionGate", "MaddExtensionGate"}),
    )
    assert DAL_A4_GATE_ORDER == (
        "HamzaResolutionGate",
        "ShaddaIdghamGate",
        "TanwinTraceGate",
        "SukunCollisionGate",
        "MaddExtensionGate",
    )


@pytest.mark.parametrize(
    ("gate_name", "result"),
    (
        (
            DalA4GateName.HAMZA_RESOLUTION,
            lambda: evaluate_hamza_resolution_gate(
                input_ref="dal-a4://hamza/input",
                identity="hamza-id",
                hamza_form=HamzaSurfaceForm.HAMZAT_QAT,
                trace_ref="trace://dal-a4/hamza",
            ),
        ),
        (
            DalA4GateName.SHADDA_IDGHAM,
            lambda: evaluate_shadda_idgham_gate(
                input_ref="dal-a4://shadda/input",
                lead_identity="shadda-lead",
                tail_identity="shadda-tail",
                shadda_form=ShaddaTraceForm.IDGHAM_TRACE,
                trace_ref="trace://dal-a4/shadda",
            ),
        ),
        (
            DalA4GateName.TANWIN_TRACE,
            lambda: evaluate_tanwin_trace_gate(
                input_ref="dal-a4://tanwin/input",
                identity="tanwin-id",
                tanwin_form=TanwinTraceForm.NOMINAL_TRACE,
                trace_ref="trace://dal-a4/tanwin",
            ),
        ),
        (
            DalA4GateName.SUKUN_COLLISION,
            lambda: evaluate_sukun_collision_gate(
                input_ref="dal-a4://sukun/input",
                identity="sukun-id",
                sukun_form=SukunTraceForm.INTERNAL_SUKUN,
                has_collision=False,
                trace_ref="trace://dal-a4/sukun",
            ),
        ),
        (
            DalA4GateName.MADD_EXTENSION,
            lambda: evaluate_madd_extension_gate(
                input_ref="dal-a4://madd/input",
                identity="madd-id",
                madd_form=MaddTraceForm.EXTENSION_TRACE,
                extension_evidence=True,
                trace_ref="trace://dal-a4/madd",
            ),
        ),
    ),
)
def test_each_gate_returns_bounded_dal_a4_certificate(
    gate_name: DalA4GateName,
    result: callable,
) -> None:
    _declare("bounded dal-a4 certificates", frozenset({"DAL-A4"}))
    gate_result = result()
    assert isinstance(gate_result, DalA4GateResult)
    assert isinstance(gate_result.certificate, DalA4GateCertificate)
    assert gate_result.certificate.gate_name is gate_name
    assert gate_result.certificate.status in (
        DalA4GateStatus.PASSED,
        DalA4GateStatus.DEFERRED,
        DalA4GateStatus.REFUSED,
    )
    assert gate_result.certificate.trace_ref.startswith("trace://dal-a4/")


def test_hamza_gate_preserves_identity_without_root_weight_or_meaning_output() -> None:
    _declare("hamza bounded identity", frozenset({"HamzaResolutionGate"}))
    result = evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/input",
        identity="hamza-identity",
        hamza_form=HamzaSurfaceForm.SEAT_OF_HAMZA,
        trace_ref="trace://dal-a4/hamza/passed",
    )

    assert result.failure_code is None
    assert result.certificate.preserved_identity == ("hamza-identity",)
    assert "RootIdentityGate" in result.certificate.forbidden_outputs
    assert "WeightPathSelectionGate" in result.certificate.forbidden_outputs
    assert "MeaningGate" in result.certificate.forbidden_outputs


def test_shadda_gate_refuses_silent_identity_collapse() -> None:
    _declare("shadda identity collapse refusal", frozenset({"ShaddaIdghamGate"}))
    result = evaluate_shadda_idgham_gate(
        input_ref="dal-a4://shadda/input",
        lead_identity="same",
        tail_identity="same",
        shadda_form=ShaddaTraceForm.IDGHAM_TRACE,
        trace_ref="trace://dal-a4/shadda/collapse",
    )

    assert result.certificate.status is DalA4GateStatus.REFUSED
    assert result.failure_code is FailureCode.IDENTITY_BROKEN
    assert "SHADDA_IDENTITY_COLLAPSE_BLOCKED" in result.certificate.residuals


def test_tanwin_gate_records_trace_without_i3rab_or_definiteness_engine() -> None:
    _declare("tanwin trace only", frozenset({"TanwinTraceGate"}))
    result = evaluate_tanwin_trace_gate(
        input_ref="dal-a4://tanwin/input",
        identity="tanwin-id",
        tanwin_form=TanwinTraceForm.TERMINAL_NASAL_TRACE,
        trace_ref="trace://dal-a4/tanwin/passed",
    )

    assert result.certificate.status is DalA4GateStatus.PASSED
    assert result.failure_code is None
    assert not hasattr(result.certificate, "i3rab_state")
    assert not hasattr(result.certificate, "definiteness_state")


def test_sukun_gate_records_collision_without_opening_dal_a5_adjacency() -> None:
    _declare("sukun bounded collision", frozenset({"SukunCollisionGate"}))
    collision = evaluate_sukun_collision_gate(
        input_ref="dal-a4://sukun/input",
        identity="sukun-id",
        sukun_form=SukunTraceForm.INTERNAL_SUKUN,
        has_collision=True,
        trace_ref="trace://dal-a4/sukun/collision",
    )
    dal_a5_handoff = evaluate_sukun_collision_gate(
        input_ref="dal-a4://sukun/input",
        identity="sukun-id",
        sukun_form=SukunTraceForm.ORIGINAL_SUKUN,
        has_collision=False,
        trace_ref="trace://dal-a4/sukun/handoff",
        requested_handoff="DAL-A5",
    )

    assert collision.certificate.status is DalA4GateStatus.REFUSED
    assert collision.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert "SUKUN_COLLISION_RECORDED" in collision.certificate.residuals
    assert dal_a5_handoff.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "BLOCKED_DAL_A5_HANDOFF" in dal_a5_handoff.certificate.residuals


def test_madd_gate_records_extension_without_tajwid_or_syllable_runtime() -> None:
    _declare("madd extension trace only", frozenset({"MaddExtensionGate"}))
    result = evaluate_madd_extension_gate(
        input_ref="dal-a4://madd/input",
        identity="madd-id",
        madd_form=MaddTraceForm.NO_EXTENSION,
        extension_evidence=False,
        trace_ref="trace://dal-a4/madd/deferred",
    )

    assert result.certificate.status is DalA4GateStatus.DEFERRED
    assert result.failure_code is FailureCode.BOUNDARY_MISSING
    assert "MADD_EXTENSION_MISSING" in result.certificate.residuals
    assert "SyllableLicenseGate" in result.certificate.forbidden_outputs
    assert "MeaningGate" in result.certificate.forbidden_outputs


@pytest.mark.parametrize("handoff", ("IfadahGate", "MafhumGate", "HukmGate", "Reality"))
def test_dal_a4_refuses_semantic_neighbor_handoffs(handoff: str) -> None:
    _declare("forbidden semantic handoff", frozenset())
    result = evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/input",
        identity="hamza-id",
        hamza_form=HamzaSurfaceForm.HAMZAT_WASL,
        trace_ref="trace://dal-a4/hamza/forbidden",
        requested_handoff=handoff,
    )

    assert result.certificate.status is DalA4GateStatus.REFUSED
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "BLOCKED_SEMANTIC_OUTPUT" in result.certificate.residuals


def test_negative_green_ci_is_not_runtime_opening() -> None:
    _declare("negative green ci shortcut", frozenset())
    claude = _CLAUDE.read_text(encoding="utf-8")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Green pytest is not constitutional success." in claude
    assert (
        "DAL-A6-ADMIT admission boundary after DAL-A5 runtime                      → current"
        in roadmap
    )


def test_no_forbidden_output_terms_in_runtime_fields_status_or_next_operation() -> None:
    _declare("forbidden terms not in runtime field surface", frozenset())
    forbidden_terms = {"root", "meaning", "ifadah", "mafhum", "hukm", "reality", "syntax"}

    field_names = {field.name.lower() for field in fields(DalA4GateCertificate)}
    status_values = {status.value.lower() for status in DalA4GateStatus}
    sample_next_ops = {
        evaluate_hamza_resolution_gate(
            input_ref="dal-a4://hamza/input",
            identity="hamza-id",
            hamza_form=HamzaSurfaceForm.ALIF_MADD,
            trace_ref="trace://dal-a4/hamza/safe-next",
        ).certificate.next_allowed_operation.lower(),
        evaluate_madd_extension_gate(
            input_ref="dal-a4://madd/input",
            identity="madd-id",
            madd_form=MaddTraceForm.EXTENSION_TRACE,
            extension_evidence=True,
            trace_ref="trace://dal-a4/madd/safe-next",
        ).certificate.next_allowed_operation.lower(),
    }

    assert not any(any(term in name for term in forbidden_terms) for name in field_names)
    assert not any(any(term in value for term in forbidden_terms) for value in status_values)
    assert not any(any(term in op for term in forbidden_terms) for op in sample_next_ops)

    module_text = _MODULE.read_text(encoding="utf-8").lower()
    assert "class dala4gatecertificate" in module_text
    assert "class dala4gateresult" in module_text
