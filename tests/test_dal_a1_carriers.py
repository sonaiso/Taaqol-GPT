"""Constitutional tests for DAL-A1 carrier and local residual surface.

Origin law     : docs/58 (DalAlone Atomic Closure Law)
Branch         : DAL-A1 (carriers + local residual vocabulary only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import (
    DAL_A1_FORBIDDEN_OUTPUTS,
    DAL_A1_RESIDUAL_VOCABULARY,
    AtomicSoundUnit,
    DalAloneClosureSurface,
    DalResidual,
    DalResidualKind,
    GraphemeCandidate,
    LetterIdentity,
    PhoneticRealization,
    RawTrace,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_ORIGIN = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"
_CHAIN = ("DalOnlyCandidate", "DAL-A1", "DalAloneClosureSurface")
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
        forbidden_outputs=DAL_A1_FORBIDDEN_OUTPUTS,
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


def _surface_chain() -> tuple[
    RawTrace,
    GraphemeCandidate,
    LetterIdentity,
    PhoneticRealization,
    AtomicSoundUnit,
]:
    residual = DalResidual(
        kind=DalResidualKind.WAQF_UNTESTED,
        trace_ref="trace://dal-a1/residual/waqf",
    )
    raw = RawTrace(
        identity="raw-ba",
        raw_ref="unicode://dal-a1/raw/ba",
        trace_kind="UNICODE",
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/raw",
        residuals=(residual,),
    )
    grapheme = GraphemeCandidate(
        identity="grapheme-ba",
        unicode_surface="ب",
        raw_trace=raw,
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/grapheme",
    )
    letter = LetterIdentity(
        identity="letter-ba",
        letter_label="ba",
        grapheme=grapheme,
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/letter",
    )
    phonetic = PhoneticRealization(
        identity="phonetic-ba",
        realization_ref="sound://ba",
        letter_identity=letter,
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/phonetic",
    )
    sound = AtomicSoundUnit(
        identity="sound-ba",
        sound_ref="arabic-sound://ba",
        phonetic_realization=phonetic,
        makhraj_ref="makhraj://ba/candidate",
        sifah_ref="sifah://ba/candidate",
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/sound",
    )
    return raw, grapheme, letter, phonetic, sound


def test_chain_records_dal_a1_as_done_with_dal_a4_admit_current() -> None:
    _declare("chain registration for dal-a1", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A1\s+DalAlone carrier surface \+ local residual vocabulary\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A1\s+DalAlone carrier surface \+ local residual vocabulary\s+✓ done",
        claude,
    )
    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", roadmap)
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A4-ADMIT\s+post-CLOSE-6 admission decision \(DAL-A4 scope only\)\s+→ current",
        roadmap,
    )
    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", claude)
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A4-ADMIT\s+post-CLOSE-6 admission decision \(DAL-A4 scope only\)\s+→ current",
        claude,
    )


def test_dal_a1_local_residual_vocabulary_is_not_global_failure_code() -> None:
    _declare("local residual vocabulary", frozenset())

    assert set(DAL_A1_RESIDUAL_VOCABULARY) == {member.value for member in DalResidualKind}
    global_failure_names = {member.name for member in FailureCode}
    assert not set(DAL_A1_RESIDUAL_VOCABULARY).intersection(global_failure_names)


def test_dal_a1_residual_is_visible_and_frozen() -> None:
    _declare("visible local residual", frozenset())

    residual = DalResidual(
        kind=DalResidualKind.UNVOCALIZED_SURFACE,
        trace_ref="trace://dal-a1/residual/unvocalized",
    )

    assert residual.visibility == "VISIBLE"
    with pytest.raises(FrozenInstanceError):
        residual.blocking = True  # type: ignore[misc]


def test_dal_a1_carriers_preserve_rank_trace_residuals_and_forbidden_outputs() -> None:
    _declare(
        "carrier surface contract",
        frozenset({"RawTrace", "GraphemeCandidate", "LetterIdentity"}),
    )

    raw, grapheme, letter, phonetic, sound = _surface_chain()

    for carrier in (raw, grapheme, letter, phonetic, sound):
        assert carrier.domain_id == "DAL_ONLY"
        assert carrier.rank is Rank.CANDIDATE
        assert carrier.trace_ref.startswith("trace://dal-a1/")
        assert "LEXICAL_MEANING" in carrier.forbidden_outputs
        assert "LAFZI_MADLUL_GATE" in carrier.forbidden_outputs
    assert raw.residuals[0].kind is DalResidualKind.WAQF_UNTESTED


def test_dal_a1_carriers_are_frozen_pure_data() -> None:
    _declare("frozen carrier surface", frozenset({"RawTrace"}))

    raw, *_ = _surface_chain()

    with pytest.raises(FrozenInstanceError):
        raw.identity = "mutated"  # type: ignore[misc]


def test_dal_a1_carrier_refuses_rank_promotion() -> None:
    _declare("rank ceiling", frozenset())

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.RANK_EXCEEDS_CEILING.value):
        RawTrace(
            identity="raw-promoted",
            raw_ref="trace://dal-a1/raw-promoted",
            trace_kind="UNICODE",
            domain_id="DAL_ONLY",
            scope="dal-a1-carrier-test",
            rank=Rank.STRONG,
            trace_ref="trace://dal-a1/raw-promoted",
        )


def test_atomic_sound_unit_requires_visible_sound_makhraj_and_sifah_refs() -> None:
    _declare("atomic sound refs", frozenset())

    _, _, _, phonetic, _ = _surface_chain()

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        AtomicSoundUnit(
            identity="sound-missing-makhraj",
            sound_ref="arabic-sound://ba",
            phonetic_realization=phonetic,
            makhraj_ref="",
            sifah_ref="sifah://ba/candidate",
            domain_id="DAL_ONLY",
            scope="dal-a1-carrier-test",
            rank=Rank.CANDIDATE,
            trace_ref="trace://dal-a1/sound-missing-makhraj",
        )


def test_dal_alone_closure_surface_is_not_closed_verdict_or_lafzi_gate() -> None:
    _declare(
        "surface candidate not closure",
        frozenset({"DalAloneClosureSurface"}),
    )

    raw, grapheme, letter, phonetic, sound = _surface_chain()
    surface = DalAloneClosureSurface(
        identity="surface-ba",
        prior_dal_trace_ref="prove_dal/proven/ba",
        raw_trace=raw,
        graphemes=(grapheme,),
        letters=(letter,),
        phonetic_realizations=(phonetic,),
        atomic_units=(sound,),
        domain_id="DAL_ONLY",
        scope="dal-a1-carrier-test",
        rank=Rank.CANDIDATE,
        trace_ref="trace://dal-a1/surface",
        residuals=raw.residuals,
    )

    assert surface.prior_dal_trace_ref == "prove_dal/proven/ba"
    assert not hasattr(surface, "verdict_state")
    assert not hasattr(surface, "closed_state")
    assert not hasattr(surface, "lafzi_madlul")
    assert "DAL_ALONE_CLOSED" in surface.forbidden_outputs
    assert "LAFZI_MADLUL_GATE" in surface.forbidden_outputs
