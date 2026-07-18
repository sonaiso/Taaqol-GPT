from __future__ import annotations

from dataclasses import dataclass

from sim_agent.model import Verdict


@dataclass(frozen=True)
class SourceBlockerTranslation:
    source_code: str
    target_code: str


@dataclass(frozen=True)
class SourceBlockerTranslationPolicy:
    unmapped_residual_code: str = "SOURCE_BLOCKER_UNMAPPED"


@dataclass(frozen=True)
class SourceBlockerTranslationResult:
    unmapped_residual_code: str
    mapped_source_preserved: bool
    unmapped_source: tuple[str, ...]
    unexplained_target: tuple[str, ...]
    allowed: bool
    violations: tuple[str, ...]


def evaluate_source_blocker_translation(
    *,
    source_blockers: set[str],
    target_blockers: set[str],
    blocker_mapping: dict[str, str],
    composed_verdict: Verdict,
    policy: SourceBlockerTranslationPolicy | None = None,
) -> SourceBlockerTranslationResult:
    policy = policy or SourceBlockerTranslationPolicy()
    violations: list[str] = []

    mapped_source = {code for code in source_blockers if code in blocker_mapping}
    mapped_source_preserved = all(
        (code in target_blockers) or (blocker_mapping[code] in target_blockers)
        for code in mapped_source
    )
    if not mapped_source_preserved:
        violations.append("MAPPED_SOURCE_BLOCKER_NOT_PRESERVED")

    unmapped_source = tuple(sorted(code for code in source_blockers if code not in blocker_mapping))
    if unmapped_source and composed_verdict == Verdict.ACCEPT:
        violations.append("SOURCE_BLOCKER_UNMAPPED_ACCEPT_FORBIDDEN")
    if unmapped_source and composed_verdict not in {Verdict.DEFER, Verdict.BLOCK}:
        violations.append("SOURCE_BLOCKER_UNMAPPED_OUTCOME_INVALID")

    mapped_target_codes = set(blocker_mapping.values())
    unexplained_target = tuple(
        sorted(
            code
            for code in target_blockers
            if code not in source_blockers and code not in mapped_target_codes
        )
    )
    if unexplained_target and composed_verdict != Verdict.BLOCK:
        violations.append("TARGET_UNEXPLAINED_BLOCKER_NOT_BLOCKED")

    return SourceBlockerTranslationResult(
        unmapped_residual_code=policy.unmapped_residual_code,
        mapped_source_preserved=mapped_source_preserved,
        unmapped_source=unmapped_source,
        unexplained_target=unexplained_target,
        allowed=not violations,
        violations=tuple(sorted(set(violations))),
    )
