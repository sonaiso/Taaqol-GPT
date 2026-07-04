"""Constitutional tests for DAL-A2 separation gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law)
Branch         : DAL-A2 (raw/grapheme/letter/sound separation gates)
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.dal_only import (
    DalAtomicOperationState,
    DalResidualKind,
    GraphemeCandidate,
    RawAcousticTraceCandidate,
    RawAcousticTraceClass,
    RawTrace,
    SoundLetterGraphemeSeparationCandidate,
    grapheme_to_phonetic_shortcut_gate,
    raw_acoustic_trace_gate,
    sound_letter_grapheme_separation_gate,
    unicode_normalization_gate,
    unicode_to_arabic_sound_shortcut_gate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_ORIGIN = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"
_CHAIN = ("DalOnlyCandidate", "DAL-A1", "DAL-A2", "SoundLetterGraphemeSeparationCandidate")
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ArabicSoundInventoryGate",
            "MakhrajSifahMatrixGate",
            "QadihSoundDifferenceGate",
            "SyllableLicenseGate",
            "WordKindGate",
            "RootIdentityGate",
            "WeightPathSelectionGate",
            "MeaningGate",
            "IfadahGate",
            "HukmGate",
            "LafziMadlulGate",
            "DalAloneClosed",
        ),
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


def _raw(trace_kind: str = "MIXED") -> RawTrace:
    return RawTrace(
        identity=f"raw-{trace_kind.lower()}",
        raw_ref=f"trace://dal-a2/raw/{trace_kind.lower()}",
        trace_kind=trace_kind,
        domain_id="DAL_ONLY",
        scope="dal-a2-test",
        rank=Rank.CANDIDATE,
        trace_ref=f"trace://dal-a2/raw/{trace_kind.lower()}",
    )


def test_chain_records_dal_a2_as_done_with_close_6_1_current() -> None:
    _declare("chain registration for dal-a2", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A2\s+Raw trace / grapheme / letter / sound separation gates\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A2\s+Raw trace / grapheme / letter / sound separation gates\s+✓ done",
        claude,
    )
    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", roadmap)
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+→ current",
        roadmap,
    )
    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", claude)
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+→ current",
        claude,
    )


def test_raw_acoustic_trace_gate_blocks_non_speech() -> None:
    _declare("raw acoustic speech filtering", frozenset())
    result = raw_acoustic_trace_gate(
        _raw("ACOUSTIC"),
        acoustic_class=RawAcousticTraceClass.SILENCE,
        trace_ref="trace://dal-a2/raw-acoustic/silence",
    )

    assert result.state is DalAtomicOperationState.BLOCKED_BY_GATE
    assert result.failure_code is FailureCode.BOUNDARY_MISSING
    assert DalResidualKind.RAW_TRACE_NOT_SPEECH.value in result.residuals
    assert result.candidate is None


def test_raw_acoustic_trace_gate_licenses_linguistic_sound_candidate() -> None:
    _declare("raw acoustic linguistic candidate", frozenset({"RawAcousticTraceGate"}))
    result = raw_acoustic_trace_gate(
        _raw("ACOUSTIC"),
        acoustic_class=RawAcousticTraceClass.LINGUISTIC_SOUND_CANDIDATE,
        trace_ref="trace://dal-a2/raw-acoustic/linguistic",
    )

    assert result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    assert result.failure_code is None
    assert isinstance(result.candidate, RawAcousticTraceCandidate)
    assert result.residuals == ()


def test_raw_acoustic_trace_gate_marks_arabic_sound_as_unverified_before_dal_a3() -> None:
    _declare("raw acoustic arabic candidate is unverified", frozenset({"RawAcousticTraceGate"}))
    result = raw_acoustic_trace_gate(
        _raw("ACOUSTIC"),
        acoustic_class=RawAcousticTraceClass.ARABIC_SOUND_CANDIDATE,
        trace_ref="trace://dal-a2/raw-acoustic/arabic-candidate",
    )

    assert result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    assert isinstance(result.candidate, RawAcousticTraceCandidate)
    assert DalResidualKind.MAKHRAJ_MISSING.value in result.residuals
    assert DalResidualKind.SIFAH_MISSING.value in result.residuals
    assert DalResidualKind.QADIH_SOUND_DIFF_MISSING.value in result.residuals


def test_unicode_normalization_gate_emits_grapheme_candidate() -> None:
    _declare("unicode normalization to grapheme", frozenset({"GraphemeCandidate"}))
    result = unicode_normalization_gate(
        _raw("UNICODE"),
        identity="grapheme-alif-hamza",
        unicode_surface="أ",
        scope="dal-a2-test",
        trace_ref="trace://dal-a2/grapheme/alif-hamza",
    )

    assert result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    assert isinstance(result.candidate, GraphemeCandidate)
    assert result.candidate.unicode_surface == "أ"


def test_sound_letter_grapheme_separation_gate_enforces_ordered_chain() -> None:
    _declare(
        "grapheme to letter to phonetic chain",
        frozenset({"LetterIdentity", "PhoneticRealization"}),
    )
    grapheme_result = unicode_normalization_gate(
        _raw("UNICODE"),
        identity="grapheme-ba",
        unicode_surface="ب",
        scope="dal-a2-test",
        trace_ref="trace://dal-a2/grapheme/ba",
    )
    assert isinstance(grapheme_result.candidate, GraphemeCandidate)

    separation_result = sound_letter_grapheme_separation_gate(
        grapheme_result.candidate,
        letter_identity_id="letter-ba",
        letter_label="ba",
        phonetic_identity_id="phonetic-ba",
        realization_ref="sound://ba/candidate",
        scope="dal-a2-test",
        trace_ref="trace://dal-a2/separation/ba",
    )

    assert separation_result.state is DalAtomicOperationState.LICENSED_IN_DOMAIN
    assert isinstance(
        separation_result.candidate,
        SoundLetterGraphemeSeparationCandidate,
    )
    assert separation_result.candidate.grapheme.raw_trace.identity == "raw-unicode"
    assert (
        separation_result.candidate.letter_identity.grapheme.identity
        == separation_result.candidate.grapheme.identity
    )
    assert (
        separation_result.candidate.phonetic_realization.letter_identity.identity
        == separation_result.candidate.letter_identity.identity
    )
    assert separation_result.candidate.letter_identity.letter_label == "ba"
    assert separation_result.candidate.phonetic_realization.realization_ref == "sound://ba/candidate"
    phonetic_residual_kinds = {
        residual.kind for residual in separation_result.candidate.phonetic_realization.residuals
    }
    assert DalResidualKind.MAKHRAJ_MISSING in phonetic_residual_kinds
    assert DalResidualKind.SIFAH_MISSING in phonetic_residual_kinds
    assert DalResidualKind.QADIH_SOUND_DIFF_MISSING in phonetic_residual_kinds
    assert DalResidualKind.MAKHRAJ_MISSING.value in separation_result.residuals
    assert DalResidualKind.SIFAH_MISSING.value in separation_result.residuals
    assert DalResidualKind.QADIH_SOUND_DIFF_MISSING.value in separation_result.residuals


def test_forbidden_shortcuts_are_refused_by_straight_line_rule() -> None:
    _declare("forbidden shortcuts", frozenset())
    raw = _raw("UNICODE")
    grapheme_result = unicode_normalization_gate(
        raw,
        identity="grapheme-meem",
        unicode_surface="م",
        scope="dal-a2-test",
        trace_ref="trace://dal-a2/grapheme/meem",
    )
    assert isinstance(grapheme_result.candidate, GraphemeCandidate)

    direct_unicode = unicode_to_arabic_sound_shortcut_gate(
        raw,
        trace_ref="trace://dal-a2/shortcut/unicode-to-sound",
    )
    direct_grapheme = grapheme_to_phonetic_shortcut_gate(
        grapheme_result.candidate,
        trace_ref="trace://dal-a2/shortcut/grapheme-to-phonetic",
    )

    assert direct_unicode.state is DalAtomicOperationState.BLOCKED_BY_GATE
    assert direct_unicode.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert direct_grapheme.state is DalAtomicOperationState.BLOCKED_BY_GATE
    assert direct_grapheme.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
