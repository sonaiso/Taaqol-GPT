from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationPath:
    source_operation: str
    mapped_operation: str


@dataclass(frozen=True)
class OperationHomomorphismCheck:
    preserves_result: bool
    preserves_path: bool
    evidence_preserved: bool
    violations: tuple[str, ...]


@dataclass(frozen=True)
class ResidualMapping:
    source_code: str
    target_code: str
    reason: str


@dataclass(frozen=True)
class ResidualReflectionReport:
    source_preserved: bool
    target_explained: bool
    unmapped_source: tuple[str, ...]
    unexplained_target: tuple[str, ...]
    mappings_used: tuple[ResidualMapping, ...]
