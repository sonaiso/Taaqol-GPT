from sim_agent.laws import check_identity_simulation_law
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
    evidence_items: frozenset[str] = frozenset({"tests_pass"}),
    residuals: tuple[Residual, ...] = (),
    blockers: tuple[Blocker, ...] = (),
) -> Transition:
    operation = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=evidence_items, rank=Rank.MEDIUM)
    trace = Trace(
        source_state=source.name,
        operation=operation.name,
        evidence=tuple(sorted(evidence_items)),
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


def test_identity_simulation_law_accepts_preserved_chain() -> None:
    domain = Domain("coding")
    source = State("l0_a", domain, Identity("id-1"), Rank.MEDIUM)
    target = State("l0_b", domain, Identity("id-1"), Rank.MEDIUM)

    src_t = _transition(source=source, target=target, verdict=Verdict.DEFER)
    tgt_t = _transition(
        source=State("k0_a", domain, Identity("id-1"), Rank.MEDIUM),
        target=State("k0_b", domain, Identity("id-1"), Rank.MEDIUM),
        verdict=Verdict.DEFER,
    )

    result = check_identity_simulation_law(src_t, tgt_t)

    assert result.passed
    assert not result.violations


def test_identity_simulation_law_rejects_identity_shift_rank_inflation_and_hidden_residual(
) -> None:
    domain = Domain("coding")
    source = State("l0_a", domain, Identity("id-1"), Rank.MEDIUM)
    mid = State("l0_b", domain, Identity("id-1"), Rank.MEDIUM)

    src_t = _transition(
        source=source,
        target=mid,
        verdict=Verdict.BLOCK,
        residuals=(Residual(code="NEEDS_REVIEW", detail="review", blocking=True),),
        blockers=(Blocker(code="SOURCE_BLOCK", detail="source blocked"),),
    )

    tgt_t = _transition(
        source=State("k0_a", domain, Identity("id-1"), Rank.MEDIUM),
        target=State("k0_b", domain, Identity("id-2"), Rank.HIGH),
        verdict=Verdict.ACCEPT,
        evidence_items=frozenset(),
    )

    result = check_identity_simulation_law(src_t, tgt_t)

    assert not result.passed
    assert "IDENTITY_SHIFT" in result.violations
    assert "RANK_INFLATION" in result.violations
    assert "MISSING_EVIDENCE" in result.violations
    assert "HIDDEN_SOURCE_RESIDUAL" in result.violations
    assert "BLOCKED_SOURCE_TO_ACCEPTED_TARGET" in result.violations
