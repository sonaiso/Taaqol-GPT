from sim_agent.laws import check_nontriviality_strengthening_law
from sim_agent.model import Domain, Evidence, Identity, Operation, Rank, Residual, SimulationMap, State, Trace, Transition, Verdict


def _transition(source: State, target: State, verdict: Verdict, residual_code: str) -> Transition:
    operation = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)
    trace = Trace(source.name, operation.name, ("tests_pass",), target.name, verdict)
    residuals = (Residual(code=residual_code, detail="detail", blocking=False),)
    return Transition(source, operation, evidence, target, verdict, residuals, (), trace)


def test_nontriviality_strengthening_law_accepts_diverse_mapping() -> None:
    domain = Domain("coding")
    s0 = State("s0", domain, Identity("id-a"), Rank.MEDIUM)
    s1 = State("s1", domain, Identity("id-b"), Rank.MEDIUM)
    t0 = State("t0", domain, Identity("id-a"), Rank.MEDIUM)
    t1 = State("t1", domain, Identity("id-b"), Rank.MEDIUM)

    mapping = SimulationMap(
        state_map={"s0": "t0", "s1": "t1"},
        operation_map={"refactor": "refactor", "review": "review"},
    )

    src = (_transition(s0, s1, Verdict.ACCEPT, "SRC_R1"),)
    tgt = (_transition(t0, t1, Verdict.ACCEPT, "TGT_R1"),)

    report = check_nontriviality_strengthening_law(mapping, src, tgt)

    assert report.passed
    assert not report.trivialities


def test_nontriviality_strengthening_law_detects_state_and_operation_collapse() -> None:
    domain = Domain("coding")
    s0 = State("s0", domain, Identity("id-shared"), Rank.MEDIUM)
    s1 = State("s1", domain, Identity("id-shared"), Rank.MEDIUM)
    t0 = State("t0", domain, Identity("id-shared"), Rank.MEDIUM)
    t1 = State("t1", domain, Identity("id-shared"), Rank.MEDIUM)

    mapping = SimulationMap(
        state_map={"s0": "t0", "s1": "t0"},
        operation_map={"refactor": "op", "review": "op"},
    )

    src = (
        _transition(s0, s1, Verdict.DEFER, "GENERIC_RESIDUAL"),
        _transition(s1, s0, Verdict.DEFER, "GENERIC_RESIDUAL"),
    )
    tgt = (
        _transition(t0, t1, Verdict.DEFER, "GENERIC_RESIDUAL"),
        _transition(t1, t0, Verdict.DEFER, "GENERIC_RESIDUAL"),
    )

    report = check_nontriviality_strengthening_law(mapping, src, tgt)

    assert not report.passed
    assert "TRIVIAL_STATE_COLLAPSE" in report.trivialities
    assert "TRIVIAL_OPERATION_COLLAPSE" in report.trivialities
    assert "TRIVIAL_EVIDENCE_COLLAPSE" in report.trivialities
    assert "TRIVIAL_RESIDUAL_COLLAPSE" in report.trivialities
    assert "TRIVIAL_VERDICT_COLLAPSE" in report.trivialities
    assert "TRIVIAL_IDENTITY_COLLAPSE" in report.trivialities
