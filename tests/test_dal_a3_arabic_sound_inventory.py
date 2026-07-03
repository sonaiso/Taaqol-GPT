"""Constitutional tests for DAL-A3 Arabic sound inventory boundary.

Origin law     : docs/58 (DalAlone Atomic Closure Law)
Branch         : DAL-A3 (ArabicSoundInventory + makhraj/sifah/qadih matrix)
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
import pathlib
import re

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.arabic_sound_inventory import (
    DAL_A3_ALLOWED_OUTPUT,
    DAL_A3_FORBIDDEN_OUTPUTS,
    ArabicSoundInventoryEntry,
    ArabicSoundInventoryFailedStage,
    ArabicSoundInventoryKind,
    ArabicSoundInventoryReadinessState,
    MakhrajProof,
    QadihSoundDifferenceProof,
    QadihSoundDifferenceStatus,
    SifahProof,
    evaluate_arabic_sound_inventory_gate,
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
    "ArabicSoundInventoryGate",
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_FIXTURES = _REPO_ROOT / "data" / "dal_a3_arabic_sound_inventory_fixtures.json"


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A3_FORBIDDEN_OUTPUTS,
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


def _fixture_map() -> dict[str, dict[str, object]]:
    fixtures = json.loads(_FIXTURES.read_text(encoding="utf-8"))
    return {str(entry["fixture_id"]): entry for entry in fixtures}


def _entry(payload: dict[str, object]) -> ArabicSoundInventoryEntry:
    return ArabicSoundInventoryEntry(
        sound_ref=str(payload["sound_ref"]),
        grapheme=str(payload["grapheme"]),
        phonetic_label=str(payload["phonetic_label"]),
        sound_kind=ArabicSoundInventoryKind[str(payload["sound_kind"])],
        makhraj_ref=str(payload["makhraj_ref"]),
        sifah_refs=tuple(str(ref) for ref in payload["sifah_refs"]),
        source_policy=str(payload["source_policy"]),
        inventory_version=str(payload["inventory_version"]),
        residuals=tuple(str(residual) for residual in payload["residuals"]),
    )


def _makhraj(sound_ref: str, trace: str) -> MakhrajProof:
    return MakhrajProof(
        sound_ref=sound_ref,
        makhraj_ref=f"makhraj://{sound_ref.rsplit('//', maxsplit=1)[-1]}",
        makhraj_path=("mouth", "tongue", "edge"),
        source_policy="docs/58",
        inventory_version="dal-a3-v1",
        trace_ref=f"{trace}/makhraj",
    )


def _sifah(sound_ref: str, trace: str) -> SifahProof:
    return SifahProof(
        sound_ref=sound_ref,
        sifah_refs=("JAHR", "RIKHWA"),
        source_policy="docs/58",
        inventory_version="dal-a3-v1",
        trace_ref=f"{trace}/sifah",
    )


def _qadih(sound_ref: str, trace: str, *, shared: tuple[str, ...]) -> QadihSoundDifferenceProof:
    return QadihSoundDifferenceProof(
        origin_sound_ref=sound_ref,
        branch_sound_ref="sound://comparison-target",
        shared_sifah_refs=shared,
        differentiating_sifah_refs=("DIFF_TRACE",),
        blocking_difference=False,
        qadih_status=QadihSoundDifferenceStatus.CLEAR,
        source_policy="docs/58",
        inventory_version="dal-a3-v1",
    )


def test_chain_records_dal_a3_as_done_without_displacing_close_5() -> None:
    _declare("chain registration for dal-a3", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A3\s+ArabicSoundInventory \+ makhraj/sifah/qadih matrix\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A3\s+ArabicSoundInventory \+ makhraj/sifah/qadih matrix\s+✓ done",
        claude,
    )
    assert re.search(r"CLOSE-5\s+Final closure audit\s+→ current", roadmap)
    assert re.search(r"CLOSE-5\s+Final closure audit\s+→ current", claude)


def test_fixture_pack_contains_required_dal_a3_cases() -> None:
    _declare("fixture pack coverage", frozenset())
    fixtures = _fixture_map()
    expected_ids = {
        "arabic_sound_without_makhraj_deferred",
        "arabic_sound_without_sifah_deferred",
        "sound_difference_without_qadih_deferred",
        "dad_with_makhraj_sifah_link_ready",
        "forbidden_handoff_to_syllable_refused",
        "forbidden_handoff_to_hukm_refused",
        "similarity_indicator_only_not_qiyas",
    }
    assert expected_ids.issubset(set(fixtures))


def test_dal_a3_sound_candidate_requires_makhraj() -> None:
    _declare("sound candidate requires makhraj", frozenset())
    fixture = _fixture_map()["arabic_sound_without_makhraj_deferred"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=None,
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/no-makhraj"),
        qadih_sound_difference_proof=None,
        comparison_requested=False,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/no-makhraj",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.DEFERRED
    assert result.decision.failed_stage is ArabicSoundInventoryFailedStage.MAKHRAJ
    assert result.decision.local_failure_name == "MAKHRAJ_MISSING"
    assert "MAKHRAJ_MISSING" in result.decision.residuals


def test_dal_a3_sound_candidate_requires_sifah() -> None:
    _declare("sound candidate requires sifah", frozenset())
    fixture = _fixture_map()["arabic_sound_without_sifah_deferred"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/no-sifah"),
        sifah_proof=None,
        qadih_sound_difference_proof=None,
        comparison_requested=False,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/no-sifah",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.DEFERRED
    assert result.decision.failed_stage is ArabicSoundInventoryFailedStage.SIFAH
    assert result.decision.local_failure_name == "SIFAH_MISSING"
    assert "SIFAH_MISSING" in result.decision.residuals


def test_dal_a3_qadih_matrix_required_for_sound_comparison() -> None:
    _declare("qadih matrix required", frozenset())
    fixture = _fixture_map()["sound_difference_without_qadih_deferred"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/no-qadih"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/no-qadih"),
        qadih_sound_difference_proof=None,
        comparison_requested=True,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/no-qadih",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.DEFERRED
    assert result.decision.failed_stage is ArabicSoundInventoryFailedStage.QADIH
    assert result.decision.local_failure_name == "QADIH_SOUND_DIFF_MISSING"
    assert "QADIH_SOUND_DIFF_MISSING" in result.decision.residuals


def test_dal_a3_complete_sound_inventory_entry_is_link_ready() -> None:
    _declare("complete inventory entry link ready", frozenset({DAL_A3_ALLOWED_OUTPUT}))
    fixture = _fixture_map()["dad_with_makhraj_sifah_link_ready"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/link-ready"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/link-ready"),
        qadih_sound_difference_proof=_qadih(
            entry.sound_ref,
            "trace://dal-a3/link-ready",
            shared=("ITBAQ",),
        ),
        comparison_requested=True,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/link-ready",
    )

    assert result.failure_code is None
    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.LINK_READY
    assert result.decision.sound_inventory_ready is True
    assert result.candidate is not None
    assert "MAKHRAJ_MISSING" not in result.decision.residuals
    assert "SIFAH_MISSING" not in result.decision.residuals
    assert "QADIH_SOUND_DIFF_MISSING" not in result.decision.residuals
    assert result.decision.handoff == "HarakaCarrierGate"


@pytest.mark.parametrize(
    "handoff",
    ("SyllableLicenseGate", "RootIdentityGate", "WeightPathSelectionGate"),
)
def test_dal_a3_forbids_syllable_root_weight_outputs(handoff: str) -> None:
    _declare("forbid syllable/root/weight handoff", frozenset())
    fixture = _fixture_map()["forbidden_handoff_to_syllable_refused"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/forbidden-structural"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/forbidden-structural"),
        qadih_sound_difference_proof=_qadih(
            entry.sound_ref,
            "trace://dal-a3/forbidden-structural",
            shared=(),
        ),
        comparison_requested=True,
        handoff=handoff,
        trace_ref="trace://dal-a3/forbidden-structural",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.REFUSED
    assert result.decision.failed_stage is ArabicSoundInventoryFailedStage.HANDOFF
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "FORBIDDEN_DAL_A3_HANDOFF" in result.decision.residuals
    assert handoff in result.decision.local_failure_name


@pytest.mark.parametrize(
    "handoff",
    ("MeaningGate", "IfadahGate", "MafhumGate", "HukmGate", "Truth", "Reality"),
)
def test_dal_a3_forbids_semantic_hukm_outputs(handoff: str) -> None:
    _declare("forbid semantic/hukm handoff", frozenset())
    fixture = _fixture_map()["forbidden_handoff_to_hukm_refused"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/forbidden-semantic"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/forbidden-semantic"),
        qadih_sound_difference_proof=_qadih(
            entry.sound_ref,
            "trace://dal-a3/forbidden-semantic",
            shared=(),
        ),
        comparison_requested=True,
        handoff=handoff,
        trace_ref="trace://dal-a3/forbidden-semantic",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.REFUSED
    assert result.decision.failed_stage is ArabicSoundInventoryFailedStage.HANDOFF
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "FORBIDDEN_DAL_A3_HANDOFF" in result.decision.residuals
    assert handoff in result.decision.local_failure_name


def test_sound_similarity_is_indicator_not_qiyas() -> None:
    _declare("similarity indicator only", frozenset({DAL_A3_ALLOWED_OUTPUT}))
    fixture = _fixture_map()["similarity_indicator_only_not_qiyas"]
    entry = _entry(fixture["entry"])
    result = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/similarity"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/similarity"),
        qadih_sound_difference_proof=_qadih(
            entry.sound_ref,
            "trace://dal-a3/similarity",
            shared=("GHUNNAH",),
        ),
        comparison_requested=True,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/similarity",
    )

    assert result.decision.readiness_state is ArabicSoundInventoryReadinessState.LINK_READY
    assert "SOUND_SIMILARITY_INDICATOR_ONLY" in result.decision.residuals
    assert result.candidate is not None
    assert result.candidate.similarity_indicator is not None
    assert result.candidate.similarity_indicator.indicator_only is True
    assert not hasattr(result.candidate, "qiyas_verdict")
    assert not hasattr(result.candidate, "hukm")


def test_dal_a2_residuals_are_closed_only_by_dal_a3_surface() -> None:
    _declare("residual closure requires explicit proof", frozenset({DAL_A3_ALLOWED_OUTPUT}))
    fixture = _fixture_map()["dad_with_makhraj_sifah_link_ready"]
    entry = _entry(fixture["entry"])

    deferred = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=None,
        sifah_proof=None,
        qadih_sound_difference_proof=None,
        comparison_requested=True,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/residuals/deferred",
    )
    assert deferred.decision.readiness_state is ArabicSoundInventoryReadinessState.DEFERRED
    assert "MAKHRAJ_MISSING" in deferred.decision.residuals
    assert "SIFAH_MISSING" in deferred.decision.residuals
    assert "QADIH_SOUND_DIFF_MISSING" in deferred.decision.residuals

    linked = evaluate_arabic_sound_inventory_gate(
        entry=entry,
        makhraj_proof=_makhraj(entry.sound_ref, "trace://dal-a3/residuals/linked"),
        sifah_proof=_sifah(entry.sound_ref, "trace://dal-a3/residuals/linked"),
        qadih_sound_difference_proof=_qadih(
            entry.sound_ref,
            "trace://dal-a3/residuals/linked",
            shared=("ITBAQ",),
        ),
        comparison_requested=True,
        handoff=str(fixture["handoff"]),
        trace_ref="trace://dal-a3/residuals/linked",
    )
    assert linked.decision.readiness_state is ArabicSoundInventoryReadinessState.LINK_READY
    assert "MAKHRAJ_MISSING" not in linked.decision.residuals
    assert "SIFAH_MISSING" not in linked.decision.residuals
    assert "QADIH_SOUND_DIFF_MISSING" not in linked.decision.residuals
