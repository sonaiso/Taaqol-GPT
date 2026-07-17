from __future__ import annotations

from sim_agent.model import (
    Blocker,
    Evidence,
    Operation,
    Residual,
    State,
    Trace,
    Transition,
    Verdict,
)


class GovernedProgrammingAgent:
    def decide_transition(
        self,
        source: State,
        operation: Operation,
        evidence: Evidence,
        target: State,
        residuals: tuple[Residual, ...] = (),
    ) -> Transition:
        blockers: list[Blocker] = []

        if source.domain != target.domain:
            blockers.append(
                Blocker(code="DOMAIN_VIOLATION", detail="transition crossed domain boundary")
            )

        if operation.preserves_identity and source.identity != target.identity:
            blockers.append(
                Blocker(
                    code="IDENTITY_NOT_PRESERVED",
                    detail="identity changed in preserved operation",
                )
            )

        if not operation.required_evidence.issubset(evidence.items):
            blockers.append(
                Blocker(code="MISSING_EVIDENCE", detail="required evidence is not fully supplied")
            )

        rank_ceiling = min(source.rank, evidence.rank)
        if target.rank > rank_ceiling:
            blockers.append(
                Blocker(code="RANK_INFLATION", detail="target rank exceeds source/evidence rank")
            )

        if any(residual.blocking for residual in residuals):
            blockers.append(
                Blocker(
                    code="BLOCKING_RESIDUAL_PRESENT",
                    detail="blocking residual must remain visible and blocks closure",
                )
            )

        if blockers:
            verdict = Verdict.BLOCK
        elif residuals:
            verdict = Verdict.DEFER
        else:
            verdict = Verdict.ACCEPT

        trace = Trace(
            source_state=source.name,
            operation=operation.name,
            evidence=tuple(sorted(evidence.items)),
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
            blockers=tuple(blockers),
            trace=trace,
        )
