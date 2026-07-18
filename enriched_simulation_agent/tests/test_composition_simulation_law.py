from sim_agent.laws import check_composition_simulation_law
from sim_agent.model import (
    Blocker,
    Domain,
    Evidence,
    Identity,
    Operation,
    Rank,
    Residual,
    State,
    Trace,
    Transition,
    Verdict,
)


def _transition(
    *,
    source: State,
    target: State,
    verdict: Verdict,
    blockers: tuple[Blocker, ...] = (),
    residuals: tuple[Residual, ...] = (),
) -> Transition:
    operation = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)
    trace = Trace(
        source_state=source.name,
        operation=operation.name,
        evidence=("tests_pass",),
        target_state=target.name,
        verdict=verdict,
    )
    return Transition(
        source=source,
        operation=operation,
        evidence=evidence,
        target=target,
        verdict=verdict,
        residuals=residuals,
        blockers=blockers,
        trace=trace,
    )


def test_composition_simulation_law_accepts_valid_composition() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(source=a, target=b, verdict=Verdict.ACCEPT)
    second = _transition(source=b, target=c, verdict=Verdict.ACCEPT)
    composed = _transition(source=a, target=c, verdict=Verdict.ACCEPT)

    result = check_composition_simulation_law(first, second, composed)

    assert result.passed
    assert not result.violations


def test_composition_simulation_law_rejects_blocked_source_to_accepted_target() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(
        source=a,
        target=b,
        verdict=Verdict.BLOCK,
        blockers=(Blocker(code="SOURCE_BLOCK", detail="cannot pass"),),
    )
    second = _transition(source=b, target=c, verdict=Verdict.ACCEPT)
    composed = _transition(source=a, target=c, verdict=Verdict.ACCEPT)

    result = check_composition_simulation_law(first, second, composed)

    assert not result.passed
    assert "BLOCKED_SOURCE_TO_ACCEPTED_TARGET" in result.violations
    assert "SOURCE_BLOCKER_UNMAPPED_ACCEPT_FORBIDDEN" in result.violations


def test_composition_simulation_law_requires_unmapped_blocker_to_defer() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(
        source=a,
        target=b,
        verdict=Verdict.BLOCK,
        residuals=(Residual(code="SOURCE_BLOCK", detail="still blocked", blocking=True),),
    )
    second = _transition(source=b, target=c, verdict=Verdict.DEFER)
    composed = _transition(
        source=a,
        target=c,
        verdict=Verdict.DEFER,
        residuals=(
            Residual(code="SOURCE_BLOCKER_UNMAPPED", detail="not translated", blocking=False),
        ),
    )

    result = check_composition_simulation_law(first, second, composed)

    assert result.passed


def test_composition_simulation_law_rejects_unmapped_blocker_missing_marker() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(
        source=a,
        target=b,
        verdict=Verdict.BLOCK,
        residuals=(Residual(code="SOURCE_BLOCK", detail="still blocked", blocking=True),),
    )
    second = _transition(source=b, target=c, verdict=Verdict.DEFER)
    composed = _transition(source=a, target=c, verdict=Verdict.DEFER)

    result = check_composition_simulation_law(first, second, composed)

    assert not result.passed
    assert "SOURCE_BLOCKER_UNMAPPED_MARKER_MISSING" in result.violations


def test_composition_simulation_law_rejects_nonblocking_unmapped_residual_as_accept() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(
        source=a,
        target=b,
        verdict=Verdict.ACCEPT,
        residuals=(Residual(code="SOURCE_NONBLOCKING", detail="review later", blocking=False),),
    )
    second = _transition(source=b, target=c, verdict=Verdict.ACCEPT)
    composed = _transition(source=a, target=c, verdict=Verdict.ACCEPT)

    result = check_composition_simulation_law(first, second, composed)

    assert not result.passed
    assert "SOURCE_RESIDUAL_UNMAPPED_ACCEPT_FORBIDDEN" in result.violations


def test_composition_simulation_law_accepts_mapped_blocker_translation() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(
        source=a,
        target=b,
        verdict=Verdict.BLOCK,
        blockers=(Blocker(code="SOURCE_BLOCK", detail="still blocked"),),
    )
    second = _transition(source=b, target=c, verdict=Verdict.BLOCK)
    composed = _transition(
        source=a,
        target=c,
        verdict=Verdict.BLOCK,
        blockers=(Blocker(code="TARGET_BLOCK", detail="translated blocker"),),
    )

    result = check_composition_simulation_law(
        first,
        second,
        composed,
        blocker_mapping={"SOURCE_BLOCK": "TARGET_BLOCK"},
    )

    assert result.passed
    assert not result.violations


def test_composition_simulation_law_blocks_unexplained_target_blocker() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(source=a, target=b, verdict=Verdict.ACCEPT)
    second = _transition(source=b, target=c, verdict=Verdict.BLOCK)
    composed = _transition(
        source=a,
        target=c,
        verdict=Verdict.DEFER,
        blockers=(Blocker(code="TARGET_ONLY_BLOCKER", detail="no source evidence"),),
    )

    result = check_composition_simulation_law(first, second, composed)

    assert not result.passed
    assert "TARGET_UNEXPLAINED_BLOCKER_NOT_BLOCKED" in result.violations


def test_composition_simulation_law_allows_clean_accept_without_blockers() -> None:
    domain = Domain("coding")
    a = State("a", domain, Identity("id"), Rank.MEDIUM)
    b = State("b", domain, Identity("id"), Rank.MEDIUM)
    c = State("c", domain, Identity("id"), Rank.MEDIUM)

    first = _transition(source=a, target=b, verdict=Verdict.ACCEPT)
    second = _transition(source=b, target=c, verdict=Verdict.ACCEPT)
    composed = _transition(source=a, target=c, verdict=Verdict.ACCEPT)

    result = check_composition_simulation_law(first, second, composed, blocker_mapping={})

    assert result.passed
