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


def _systems() -> tuple[
    LicensedSystem,
    LicensedSystem,
    SimulationMap,
    State,
    State,
    Operation,
    Evidence,
]:
    domain = Domain("coding")

    l0_a = State("l0_a", domain, Identity("id-a"), Rank.MEDIUM)
    l0_b = State("l0_b", domain, Identity("id-a"), Rank.MEDIUM)
    k0_a = State("k0_a", domain, Identity("id-a"), Rank.MEDIUM)
    k0_b = State("k0_b", domain, Identity("id-a"), Rank.MEDIUM)

    op = Operation("refactor", required_evidence=frozenset({"tests_pass"}))
    ev = Evidence(items=frozenset({"tests_pass"}), rank=Rank.MEDIUM)

    source_system = LicensedSystem(
        name="L0",
        states={l0_a.name: l0_a, l0_b.name: l0_b},
        operations={op.name: op},
    )
    target_system = LicensedSystem(
        name="K0",
        states={k0_a.name: k0_a, k0_b.name: k0_b},
        operations={op.name: op},
    )
    mapping = SimulationMap(
        state_map={l0_a.name: k0_a.name, l0_b.name: k0_b.name},
        operation_map={op.name: op.name},
    )
    return source_system, target_system, mapping, l0_a, l0_b, op, ev


def test_detects_verdict_not_preserved() -> None:
    source_system, target_system, mapping, l0_a, l0_b, op, ev = _systems()
    agent = GovernedProgrammingAgent()

    src_block = agent.decide_transition(
        source=l0_a,
        operation=op,
        evidence=ev,
        target=State("l0_b_bad", l0_b.domain, Identity("id-other"), Rank.MEDIUM),
    )
    tgt_accept = agent.decide_transition(
        source=target_system.states[mapping.state_map[l0_a.name]],
        operation=op,
        evidence=ev,
        target=target_system.states[mapping.state_map[l0_b.name]],
    )

    result = SimulationValidator().validate(
        source_system=source_system,
        target_system=target_system,
        mapping=mapping,
        source_transitions=(src_block,),
        target_transitions=(tgt_accept,),
    )

    assert not result.ok
    assert "VERDICT_NOT_PRESERVED" in result.violations


def test_rejects_trivial_simulation() -> None:
    source_system, target_system, _, l0_a, l0_b, op, ev = _systems()
    agent = GovernedProgrammingAgent()

    src_t = agent.decide_transition(l0_a, op, ev, l0_b)
    tgt_t = agent.decide_transition(
        target_system.states["k0_a"],
        op,
        ev,
        target_system.states["k0_b"],
    )

    trivial_map = SimulationMap(
        state_map={"l0_a": "k0_a", "l0_b": "k0_a"},
        operation_map={"refactor": "refactor"},
    )

    result = SimulationValidator().validate(
        source_system=source_system,
        target_system=target_system,
        mapping=trivial_map,
        source_transitions=(src_t,),
        target_transitions=(tgt_t,),
    )

    assert not result.ok
    assert "TRIVIAL_SIMULATION_STATE_COLLAPSE" in result.violations


def test_accepts_consistent_simulation() -> None:
    source_system, target_system, mapping, l0_a, l0_b, op, ev = _systems()
    agent = GovernedProgrammingAgent()

    src_t = agent.decide_transition(l0_a, op, ev, l0_b)
    tgt_t = agent.decide_transition(
        target_system.states["k0_a"],
        op,
        ev,
        target_system.states["k0_b"],
    )

    result = SimulationValidator().validate(
        source_system=source_system,
        target_system=target_system,
        mapping=mapping,
        source_transitions=(src_t,),
        target_transitions=(tgt_t,),
        require_target_coverage=True,
    )

    assert result.ok
    assert not result.violations
