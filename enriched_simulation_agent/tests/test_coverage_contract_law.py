from sim_agent.coverage import CoverageContract
from sim_agent.laws import check_coverage_contract_law
from sim_agent.model import (
    Domain,
    Evidence,
    Identity,
    Operation,
    Rank,
    State,
    Trace,
    Transition,
    Verdict,
)


def _transition(source: State, target: State, operation_name: str, verdict: Verdict) -> Transition:
    operation = Operation(operation_name, required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)
    trace = Trace(source.name, operation_name, ("tests_pass",), target.name, verdict)
    return Transition(source, operation, evidence, target, verdict, (), (), trace)


def test_coverage_contract_law_accepts_inside_contract() -> None:
    domain = Domain("coding")
    source = State("s0", domain, Identity("id"), Rank.MEDIUM)
    target = State("s1", domain, Identity("id"), Rank.MEDIUM)
    transition = _transition(source, target, "refactor", Verdict.ACCEPT)

    contract = CoverageContract(
        source_domain="coding",
        target_domain="coding",
        covered_states=frozenset({"s0", "s1"}),
        covered_operations=frozenset({"refactor"}),
        excluded_operations=frozenset(),
        required_evidence=frozenset({"tests_pass"}),
        rank_ceiling=Rank.MEDIUM,
        declared_limits=("no_relation_layer",),
    )

    result = check_coverage_contract_law(transition, contract)

    assert result.passed


def test_coverage_contract_law_rejects_coverage_escape() -> None:
    domain = Domain("coding")
    source = State("s0", domain, Identity("id"), Rank.MEDIUM)
    target = State("outside", domain, Identity("id"), Rank.MEDIUM)
    transition = _transition(source, target, "unsafe_operation", Verdict.ACCEPT)

    contract = CoverageContract(
        source_domain="coding",
        target_domain="coding",
        covered_states=frozenset({"s0", "s1"}),
        covered_operations=frozenset({"refactor"}),
        excluded_operations=frozenset({"unsafe_operation"}),
        required_evidence=frozenset({"tests_pass", "reviewed"}),
        rank_ceiling=Rank.LOW,
        declared_limits=("strict",),
    )

    result = check_coverage_contract_law(transition, contract)

    assert not result.passed
    assert "COVERAGE_ESCAPE" in result.violations
