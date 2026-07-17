from __future__ import annotations

from dataclasses import dataclass

from sim_agent.composition import (
    OperationHomomorphismCheck,
    OperationPath,
    ResidualMapping,
    ResidualReflectionReport,
)
from sim_agent.coverage import CoverageContract
from sim_agent.model import SimulationMap, Transition, Verdict
from sim_agent.triad import TriadMappingHypothesis


@dataclass(frozen=True)
class SimulationLawResult:
    law_name: str
    passed: bool
    violations: tuple[str, ...]


@dataclass(frozen=True)
class IdentitySimulation:
    source_transition: Transition
    target_transition: Transition
    result: SimulationLawResult


@dataclass(frozen=True)
class CompositeSimulation:
    first: IdentitySimulation
    second: IdentitySimulation
    composed_result: SimulationLawResult


@dataclass(frozen=True)
class NonTrivialityReport:
    passed: bool
    trivialities: tuple[str, ...]


def check_identity_simulation_law(
    source_transition: Transition,
    target_transition: Transition,
) -> SimulationLawResult:
    violations: list[str] = []

    if source_transition.source.domain.name != target_transition.source.domain.name:
        violations.append("DOMAIN_NOT_PRESERVED")

    if source_transition.target.identity.value != target_transition.target.identity.value:
        violations.append("IDENTITY_SHIFT")

    if source_transition.operation.name != target_transition.operation.name:
        violations.append("OPERATION_NOT_PRESERVED")

    if source_transition.evidence.items != target_transition.evidence.items:
        violations.append("MISSING_EVIDENCE")

    rank_ceiling = min(target_transition.source.rank, target_transition.evidence.rank)
    if target_transition.target.rank > rank_ceiling:
        violations.append("RANK_INFLATION")

    source_residual_codes = {r.code for r in source_transition.residuals}
    target_residual_codes = {r.code for r in target_transition.residuals}
    hidden_residuals = source_residual_codes - target_residual_codes
    if hidden_residuals:
        violations.append("HIDDEN_SOURCE_RESIDUAL")

    source_has_blocking = any(r.blocking for r in source_transition.residuals) or bool(
        source_transition.blockers
    )
    target_has_blocking = any(r.blocking for r in target_transition.residuals) or bool(
        target_transition.blockers
    )
    if source_has_blocking and not target_has_blocking:
        violations.append("BLOCKERS_NOT_PRESERVED")

    if tuple(source_transition.trace.evidence) != tuple(target_transition.trace.evidence):
        violations.append("TRACE_NOT_PRESERVED")

    if source_transition.verdict == Verdict.BLOCK and target_transition.verdict == Verdict.ACCEPT:
        violations.append("BLOCKED_SOURCE_TO_ACCEPTED_TARGET")

    if source_transition.verdict != target_transition.verdict:
        violations.append("VERDICT_NOT_PRESERVED")

    return SimulationLawResult(
        law_name="IdentitySimulationLaw",
        passed=not violations,
        violations=tuple(sorted(set(violations))),
    )


def check_composition_simulation_law(
    first_transition: Transition,
    second_transition: Transition,
    composed_transition: Transition,
    blocker_mapping: dict[str, str] | None = None,
) -> SimulationLawResult:
    violations: list[str] = []
    blocker_mapping = blocker_mapping or {}

    if first_transition.target.name != second_transition.source.name:
        violations.append("COMPOSITION_CHAIN_BROKEN")

    source_blockers = {b.code for b in first_transition.blockers}
    source_blockers.update(r.code for r in first_transition.residuals if r.blocking)

    intermediate_blockers = {b.code for b in second_transition.blockers}
    intermediate_blockers.update(r.code for r in second_transition.residuals if r.blocking)

    target_blockers = {b.code for b in composed_transition.blockers}
    target_blockers.update(r.code for r in composed_transition.residuals if r.blocking)

    if (
        (first_transition.verdict == Verdict.BLOCK or source_blockers)
        and composed_transition.verdict == Verdict.ACCEPT
    ):
        violations.append("BLOCKED_SOURCE_TO_ACCEPTED_TARGET")

    if intermediate_blockers and composed_transition.verdict == Verdict.ACCEPT:
        violations.append("INTERMEDIATE_BLOCKER_HIDDEN")

    unmapped_source = {code for code in source_blockers if code not in blocker_mapping}
    if unmapped_source:
        has_unmapped_marker = any(
            r.code == "SOURCE_BLOCKER_UNMAPPED" for r in composed_transition.residuals
        )
        if composed_transition.verdict != Verdict.DEFER:
            violations.append("SOURCE_BLOCKER_UNMAPPED")
        if not has_unmapped_marker:
            violations.append("SOURCE_BLOCKER_UNMAPPED_MARKER_MISSING")

    if source_blockers and not target_blockers and composed_transition.verdict == Verdict.ACCEPT:
        violations.append("BLOCKERS_NOT_PRESERVED")

    return SimulationLawResult(
        law_name="CompositionSimulationLaw",
        passed=not violations,
        violations=tuple(sorted(set(violations))),
    )


def check_operation_homomorphism_law(
    source_transition: Transition,
    target_transition: Transition,
    source_path: OperationPath,
    target_path: OperationPath,
) -> OperationHomomorphismCheck:
    violations: list[str] = []

    preserves_result = source_transition.verdict == target_transition.verdict
    if not preserves_result:
        violations.append("RESULT_NOT_PRESERVED")

    preserves_path = (
        source_path.source_operation == source_transition.operation.name
        and source_path.mapped_operation == target_path.source_operation
        and target_path.mapped_operation == target_transition.operation.name
    )
    if not preserves_path:
        violations.append("OPERATION_PATH_MISMATCH")

    evidence_preserved = source_transition.evidence.items == target_transition.evidence.items
    if not evidence_preserved:
        violations.append("EVIDENCE_NOT_PRESERVED")

    return OperationHomomorphismCheck(
        preserves_result=preserves_result,
        preserves_path=preserves_path,
        evidence_preserved=evidence_preserved,
        violations=tuple(sorted(set(violations))),
    )


def check_residual_reflection_law(
    source_transition: Transition,
    target_transition: Transition,
    mapping: tuple[ResidualMapping, ...] = (),
) -> ResidualReflectionReport:
    source_codes = {r.code for r in source_transition.residuals}
    target_codes = {r.code for r in target_transition.residuals}

    mapping_sources = {m.source_code for m in mapping}
    mapping_targets = {m.target_code for m in mapping}

    mapped_source_codes = {
        m.source_code for m in mapping if m.source_code in source_codes and m.target_code in target_codes
    }
    unmapped_source = tuple(
        sorted(code for code in source_codes if code not in target_codes and code not in mapped_source_codes)
    )
    source_preserved = not unmapped_source

    unexplained_target = tuple(
        sorted(
            code
            for code in target_codes
            if code not in source_codes
            and code not in mapping_targets
        )
    )

    invalid_mappings = tuple(sorted(code for code in mapping_sources if code not in source_codes))
    if invalid_mappings:
        unexplained_target = tuple(sorted(set(unexplained_target + invalid_mappings)))

    target_explained = not unexplained_target

    return ResidualReflectionReport(
        source_preserved=source_preserved,
        target_explained=target_explained,
        unmapped_source=unmapped_source,
        unexplained_target=unexplained_target,
        mappings_used=mapping,
    )


def check_coverage_contract_law(
    transition: Transition,
    contract: CoverageContract,
) -> SimulationLawResult:
    violations: list[str] = []

    if transition.source.domain.name != contract.source_domain:
        violations.append("SOURCE_DOMAIN_OUTSIDE_CONTRACT")

    if transition.target.domain.name != contract.target_domain:
        violations.append("TARGET_DOMAIN_OUTSIDE_CONTRACT")

    if transition.source.name not in contract.covered_states:
        violations.append("SOURCE_STATE_OUTSIDE_COVERAGE")

    if transition.target.name not in contract.covered_states:
        violations.append("TARGET_STATE_OUTSIDE_COVERAGE")

    if transition.operation.name not in contract.covered_operations:
        violations.append("OPERATION_OUTSIDE_COVERAGE")

    if transition.operation.name in contract.excluded_operations:
        violations.append("OPERATION_EXCLUDED_BY_CONTRACT")

    if not contract.required_evidence.issubset(transition.evidence.items):
        violations.append("MISSING_EVIDENCE")

    if transition.target.rank > contract.rank_ceiling:
        violations.append("RANK_CEILING_EXCEEDED")

    if violations and transition.verdict == Verdict.ACCEPT:
        violations.append("COVERAGE_ESCAPE")

    return SimulationLawResult(
        law_name="CoverageContractLaw",
        passed=not violations,
        violations=tuple(sorted(set(violations))),
    )


def check_nontriviality_strengthening_law(
    mapping: SimulationMap,
    source_transitions: tuple[Transition, ...],
    target_transitions: tuple[Transition, ...],
) -> NonTrivialityReport:
    trivialities: list[str] = []

    if len(mapping.state_map) > 1 and len(set(mapping.state_map.values())) == 1:
        trivialities.append("TRIVIAL_STATE_COLLAPSE")

    if len(mapping.operation_map) > 1 and len(set(mapping.operation_map.values())) == 1:
        trivialities.append("TRIVIAL_OPERATION_COLLAPSE")

    if len(target_transitions) > 1 and len({t.evidence.items for t in target_transitions}) == 1:
        trivialities.append("TRIVIAL_EVIDENCE_COLLAPSE")

    residual_sets = [{r.code for r in t.residuals} for t in target_transitions]
    if residual_sets and all(rs in ({"GENERIC_RESIDUAL"}, set()) for rs in residual_sets):
        trivialities.append("TRIVIAL_RESIDUAL_COLLAPSE")

    if target_transitions and all(t.verdict == Verdict.DEFER for t in target_transitions):
        trivialities.append("TRIVIAL_VERDICT_COLLAPSE")

    identities = set()
    for transition in source_transitions + target_transitions:
        identities.add(transition.source.identity.value)
        identities.add(transition.target.identity.value)
    if len(identities) == 1 and len(source_transitions + target_transitions) > 1:
        trivialities.append("TRIVIAL_IDENTITY_COLLAPSE")

    return NonTrivialityReport(
        passed=not trivialities,
        trivialities=tuple(sorted(set(trivialities))),
    )


def check_triad_mapping_hypothesis(
    hypothesis: TriadMappingHypothesis,
    treat_as_acceptance_proof: bool,
) -> SimulationLawResult:
    violations: list[str] = []

    if not hypothesis.is_structuring_hypothesis:
        violations.append("TRIAD_STRUCTURING_FLAG_MISSING")

    if hypothesis.acceptance_proof or treat_as_acceptance_proof:
        violations.append("TRIAD_MAPPING_TREATED_AS_PROOF")

    if "=" in hypothesis.entity_mapping or "=" in hypothesis.transformation_mapping:
        violations.append("TRIAD_DIRECT_EQUALITY_NOT_ALLOWED")

    return SimulationLawResult(
        law_name="TriadMappingHypothesisBoundary",
        passed=not violations,
        violations=tuple(sorted(set(violations))),
    )
