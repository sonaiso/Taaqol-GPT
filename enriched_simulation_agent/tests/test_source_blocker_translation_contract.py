from sim_agent.blocker_translation import evaluate_source_blocker_translation
from sim_agent.model import Verdict


def test_mapped_source_blocker_is_preserved_or_translated() -> None:
    result = evaluate_source_blocker_translation(
        source_blockers={"SOURCE_BLOCK"},
        target_blockers={"TARGET_BLOCK"},
        blocker_mapping={"SOURCE_BLOCK": "TARGET_BLOCK"},
        composed_verdict=Verdict.BLOCK,
    )
    assert result.allowed


def test_unmapped_source_blocker_cannot_accept() -> None:
    result = evaluate_source_blocker_translation(
        source_blockers={"SOURCE_BLOCK"},
        target_blockers=set(),
        blocker_mapping={},
        composed_verdict=Verdict.ACCEPT,
    )
    assert not result.allowed
    assert "SOURCE_BLOCKER_UNMAPPED_ACCEPT_FORBIDDEN" in result.violations


def test_unexplained_target_blocker_must_block() -> None:
    result = evaluate_source_blocker_translation(
        source_blockers=set(),
        target_blockers={"TARGET_ONLY_BLOCKER"},
        blocker_mapping={},
        composed_verdict=Verdict.DEFER,
    )
    assert not result.allowed
    assert "TARGET_UNEXPLAINED_BLOCKER_NOT_BLOCKED" in result.violations


def test_valid_empty_surface_allows_accept() -> None:
    result = evaluate_source_blocker_translation(
        source_blockers=set(),
        target_blockers=set(),
        blocker_mapping={},
        composed_verdict=Verdict.ACCEPT,
    )
    assert result.allowed


def test_mapped_source_blocker_missing_target_is_refused() -> None:
    result = evaluate_source_blocker_translation(
        source_blockers={"SOURCE_BLOCK"},
        target_blockers=set(),
        blocker_mapping={"SOURCE_BLOCK": "TARGET_BLOCK"},
        composed_verdict=Verdict.BLOCK,
    )
    assert not result.allowed
    assert "MAPPED_SOURCE_BLOCKER_NOT_PRESERVED" in result.violations
