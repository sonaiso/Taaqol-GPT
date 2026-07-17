from sim_agent.composition import ResidualMapping
from sim_agent.laws import check_residual_reflection_law
from sim_agent.model import (
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


def _transition(residuals: tuple[Residual, ...]) -> Transition:
    domain = Domain("coding")
    source = State("a", domain, Identity("id"), Rank.MEDIUM)
    target = State("b", domain, Identity("id"), Rank.MEDIUM)
    operation = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)
    trace = Trace("a", "refactor", ("tests_pass",), "b", Verdict.DEFER)
    return Transition(source, operation, evidence, target, Verdict.DEFER, residuals, (), trace)


def test_residual_reflection_law_accepts_mapped_target_residuals() -> None:
    source_t = _transition((Residual(code="SRC_R1", detail="src", blocking=False),))
    target_t = _transition((Residual(code="TGT_R1", detail="mapped", blocking=False),))

    report = check_residual_reflection_law(
        source_t,
        target_t,
        mapping=(ResidualMapping(source_code="SRC_R1", target_code="TGT_R1", reason="licensed"),),
    )

    assert report.source_preserved
    assert report.target_explained


def test_residual_reflection_law_rejects_unexplained_target_residual() -> None:
    source_t = _transition((Residual(code="SRC_R1", detail="src", blocking=False),))
    target_t = _transition((Residual(code="UNEXPLAINED", detail="unknown", blocking=False),))

    report = check_residual_reflection_law(source_t, target_t)

    assert not report.source_preserved
    assert not report.target_explained
    assert "UNEXPLAINED" in report.unexplained_target
