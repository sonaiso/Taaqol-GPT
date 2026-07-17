from __future__ import annotations

from sim_agent.agent import GovernedProgrammingAgent
from sim_agent.model import (
    Domain,
    Evidence,
    Identity,
    LicensedSystem,
    Operation,
    Rank,
    SimulationMap,
    State,
)
from sim_agent.validator import SimulationValidator


def main() -> None:
    domain = Domain("coding")
    source_state = State("src_A", domain, Identity("id_1"), Rank.MEDIUM)
    target_state = State("src_B", domain, Identity("id_1"), Rank.MEDIUM)

    operation = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    evidence = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)

    agent = GovernedProgrammingAgent()
    transition = agent.decide_transition(source_state, operation, evidence, target_state)

    source_system = LicensedSystem(
        name="L0",
        states={source_state.name: source_state, target_state.name: target_state},
        operations={operation.name: operation},
    )
    target_system = LicensedSystem(
        name="K0",
        states={source_state.name: source_state, target_state.name: target_state},
        operations={operation.name: operation},
    )
    mapping = SimulationMap(
        state_map={source_state.name: source_state.name, target_state.name: target_state.name},
        operation_map={operation.name: operation.name},
    )

    validator = SimulationValidator()
    result = validator.validate(
        source_system=source_system,
        target_system=target_system,
        mapping=mapping,
        source_transitions=(transition,),
        target_transitions=(transition,),
        require_target_coverage=True,
    )

    print(f"Transition verdict: {transition.verdict.value}")
    print(f"Simulation valid: {result.ok}")
    if result.violations:
        print(f"Violations: {', '.join(result.violations)}")


if __name__ == "__main__":
    main()
