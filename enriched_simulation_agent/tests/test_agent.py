from sim_agent.agent import GovernedProgrammingAgent
from sim_agent.model import Domain, Evidence, Identity, Operation, Rank, Residual, State, Verdict


def _base() -> tuple[State, Operation, Evidence]:
    source = State("s0", Domain("coding"), Identity("id-1"), Rank.MEDIUM)
    operation = Operation(
        "edit",
        required_evidence=frozenset({"reviewed"}),
        preserves_identity=True,
    )
    evidence = Evidence(items=frozenset({"reviewed"}), rank=Rank.MEDIUM)
    return source, operation, evidence


def test_blocks_identity_mismatch() -> None:
    source, operation, evidence = _base()
    target = State("s1", source.domain, Identity("id-2"), Rank.MEDIUM)

    transition = GovernedProgrammingAgent().decide_transition(source, operation, evidence, target)

    assert transition.verdict is Verdict.BLOCK
    assert any(blocker.code == "IDENTITY_NOT_PRESERVED" for blocker in transition.blockers)


def test_blocks_rank_inflation() -> None:
    source, operation, evidence = _base()
    target = State("s1", source.domain, source.identity, Rank.HIGH)

    transition = GovernedProgrammingAgent().decide_transition(source, operation, evidence, target)

    assert transition.verdict is Verdict.BLOCK
    assert any(blocker.code == "RANK_INFLATION" for blocker in transition.blockers)


def test_blocks_missing_evidence() -> None:
    source, operation, _ = _base()
    insufficient = Evidence(items=frozenset(), rank=Rank.MEDIUM)
    target = State("s1", source.domain, source.identity, Rank.MEDIUM)

    transition = GovernedProgrammingAgent().decide_transition(
        source,
        operation,
        insufficient,
        target,
    )

    assert transition.verdict is Verdict.BLOCK
    assert any(blocker.code == "MISSING_EVIDENCE" for blocker in transition.blockers)


def test_defers_for_non_blocking_residual() -> None:
    source, operation, evidence = _base()
    target = State("s1", source.domain, source.identity, Rank.MEDIUM)
    residuals = (Residual(code="NEEDS_REVIEW", detail="secondary review pending", blocking=False),)

    transition = GovernedProgrammingAgent().decide_transition(
        source, operation, evidence, target, residuals=residuals
    )

    assert transition.verdict is Verdict.DEFER
    assert not transition.blockers
