from sim_agent.composition import OperationPath
from sim_agent.laws import check_operation_homomorphism_law
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


def _transition(source: State, target: State, operation_name: str) -> Transition:
    operation = Operation(operation_name, required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)
    trace = Trace(
        source_state=source.name,
        operation=operation_name,
        evidence=("tests_pass",),
        target_state=target.name,
        verdict=Verdict.ACCEPT,
    )
    return Transition(
        source=source,
        operation=operation,
        evidence=evidence,
        target=target,
        verdict=Verdict.ACCEPT,
        residuals=(),
        blockers=(),
        trace=trace,
    )


def test_operation_homomorphism_law_accepts_when_result_and_path_are_preserved() -> None:
    domain = Domain("coding")
    src = _transition(
        State("l0_a", domain, Identity("id-1"), Rank.MEDIUM),
        State("l0_b", domain, Identity("id-1"), Rank.MEDIUM),
        operation_name="refactor",
    )
    tgt = _transition(
        State("k0_a", domain, Identity("id-1"), Rank.MEDIUM),
        State("k0_b", domain, Identity("id-1"), Rank.MEDIUM),
        operation_name="transform_refactor",
    )

    result = check_operation_homomorphism_law(
        src,
        tgt,
        source_path=OperationPath(
            source_operation="refactor",
            mapped_operation="transform_refactor",
        ),
        target_path=OperationPath(
            source_operation="transform_refactor", mapped_operation="transform_refactor"
        ),
    )

    assert not result.violations


def test_operation_homomorphism_law_rejects_path_mismatch_even_if_result_matches() -> None:
    domain = Domain("coding")
    src = _transition(
        State("l0_a", domain, Identity("id-1"), Rank.MEDIUM),
        State("l0_b", domain, Identity("id-1"), Rank.MEDIUM),
        operation_name="refactor",
    )
    tgt = _transition(
        State("k0_a", domain, Identity("id-1"), Rank.MEDIUM),
        State("k0_b", domain, Identity("id-1"), Rank.MEDIUM),
        operation_name="different_path",
    )

    result = check_operation_homomorphism_law(
        src,
        tgt,
        source_path=OperationPath(
            source_operation="refactor",
            mapped_operation="transform_refactor",
        ),
        target_path=OperationPath(source_operation="another", mapped_operation="different_path"),
    )

    assert "OPERATION_PATH_MISMATCH" in result.violations
