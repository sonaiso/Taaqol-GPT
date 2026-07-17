from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum


@dataclass(frozen=True)
class Domain:
    name: str


@dataclass(frozen=True)
class Identity:
    value: str


class Rank(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True)
class State:
    name: str
    domain: Domain
    identity: Identity
    rank: Rank


@dataclass(frozen=True)
class Evidence:
    items: frozenset[str]
    rank: Rank


@dataclass(frozen=True)
class Operation:
    name: str
    required_evidence: frozenset[str]
    preserves_identity: bool = True


@dataclass(frozen=True)
class Residual:
    code: str
    detail: str
    blocking: bool


@dataclass(frozen=True)
class Blocker:
    code: str
    detail: str


class Verdict(StrEnum):
    ACCEPT = "ACCEPT"
    DEFER = "DEFER"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Trace:
    source_state: str
    operation: str
    evidence: tuple[str, ...]
    target_state: str
    verdict: Verdict


@dataclass(frozen=True)
class Transition:
    source: State
    operation: Operation
    evidence: Evidence
    target: State
    verdict: Verdict
    residuals: tuple[Residual, ...]
    blockers: tuple[Blocker, ...]
    trace: Trace


@dataclass(frozen=True)
class LicensedSystem:
    name: str
    states: dict[str, State]
    operations: dict[str, Operation]


@dataclass(frozen=True)
class SimulationMap:
    state_map: dict[str, str]
    operation_map: dict[str, str]
