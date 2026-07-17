from __future__ import annotations

from dataclasses import dataclass

from sim_agent.model import Rank


@dataclass(frozen=True)
class CoverageContract:
    source_domain: str
    target_domain: str
    covered_states: frozenset[str]
    covered_operations: frozenset[str]
    excluded_operations: frozenset[str]
    required_evidence: frozenset[str]
    rank_ceiling: Rank
    declared_limits: tuple[str, ...]
