from __future__ import annotations

from dataclasses import dataclass

from sim_agent.model import LicensedSystem, SimulationMap, Transition, Verdict


@dataclass(frozen=True)
class SimulationValidationResult:
    ok: bool
    violations: tuple[str, ...]


class SimulationValidator:
    def validate(
        self,
        source_system: LicensedSystem,
        target_system: LicensedSystem,
        mapping: SimulationMap,
        source_transitions: tuple[Transition, ...],
        target_transitions: tuple[Transition, ...],
        require_target_coverage: bool = False,
    ) -> SimulationValidationResult:
        violations: list[str] = []

        if len(mapping.state_map) > 1 and len(set(mapping.state_map.values())) == 1:
            violations.append("TRIVIAL_SIMULATION_STATE_COLLAPSE")

        if len(mapping.operation_map) > 1 and len(set(mapping.operation_map.values())) == 1:
            violations.append("TRIVIAL_SIMULATION_OPERATION_COLLAPSE")

        target_index = {(t.source.name, t.operation.name): t for t in target_transitions}

        for src_t in source_transitions:
            mapped_source = mapping.state_map.get(src_t.source.name)
            mapped_operation = mapping.operation_map.get(src_t.operation.name)
            if mapped_source is None or mapped_operation is None:
                violations.append("MAPPING_MISSING")
                continue

            tgt_t = target_index.get((mapped_source, mapped_operation))
            if tgt_t is None:
                violations.append("TARGET_TRANSITION_MISSING")
                continue

            if src_t.source.domain.name != tgt_t.source.domain.name:
                violations.append("DOMAIN_NOT_PRESERVED")

            if src_t.target.identity.value != tgt_t.target.identity.value:
                violations.append("IDENTITY_NOT_PRESERVED")

            if src_t.target.name not in mapping.state_map:
                violations.append("TARGET_NOT_PRESERVED")

            if src_t.verdict != tgt_t.verdict:
                violations.append("VERDICT_NOT_PRESERVED")

            if src_t.verdict == Verdict.BLOCK and tgt_t.verdict == Verdict.ACCEPT:
                violations.append("VERDICT_NOT_PRESERVED")

            if tgt_t.target.rank > min(tgt_t.source.rank, tgt_t.evidence.rank):
                violations.append("RANK_INFLATION")

            if src_t.evidence.items != tgt_t.evidence.items:
                violations.append("EVIDENCE_NOT_PRESERVED")

            if tuple(src_t.trace.evidence) != tuple(tgt_t.trace.evidence):
                violations.append("TRACE_NOT_PRESERVED")

            src_residual_codes = {r.code for r in src_t.residuals}
            tgt_residual_codes = {r.code for r in tgt_t.residuals}
            if not src_residual_codes.issubset(tgt_residual_codes):
                violations.append("RESIDUALS_NOT_PRESERVED")

            src_has_blocking = any(r.blocking for r in src_t.residuals) or bool(src_t.blockers)
            tgt_has_blocking = any(r.blocking for r in tgt_t.residuals) or bool(tgt_t.blockers)
            if src_has_blocking and not tgt_has_blocking:
                violations.append("BLOCKERS_NOT_PRESERVED")

        if require_target_coverage:
            covered_states = set(mapping.state_map.values())
            uncovered_states = set(target_system.states.keys()) - covered_states
            if uncovered_states:
                violations.append("TARGET_COVERAGE_INCOMPLETE")

        return SimulationValidationResult(
            ok=not violations,
            violations=tuple(sorted(set(violations))),
        )
