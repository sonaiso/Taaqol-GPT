"""Archimedean/Euclidean transition audit + stress benchmark runner.

This surface stays in the X0R contract zone: it measures transition readiness
without opening semantic/hukm/truth runtime outputs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode

_FORBIDDEN_DIRECT_TARGETS = frozenset({"Meaning", "Hukm", "Truth", "Certainty", "Reality"})


class ArchimedeanStatus(StrEnum):
    """Audit status for O->F decomposability."""

    PASS = "PASS"
    FAIL_NON_DECOMPOSABLE = "FAIL_NON_DECOMPOSABLE"
    PARTIAL = "PARTIAL"


class EuclideanStatus(StrEnum):
    """Audit status for constructible transition units."""

    PASS = "PASS"
    FAIL_UNCONSTRUCTED_STEP = "FAIL_UNCONSTRUCTED_STEP"
    PARTIAL = "PARTIAL"


class TraceReplayStatus(StrEnum):
    """Trace replayability level."""

    PASS = "PASS"
    MISSING = "MISSING"
    SNAPSHOT_ONLY = "SNAPSHOT_ONLY"


class RankBoundStatus(StrEnum):
    """Rank bound check status."""

    PASS = "PASS"
    FAIL = "FAIL"


class StressCaseStatus(StrEnum):
    """Operational stress-case status legend (docs/80 + fixture)."""

    LICENSED = "LICENSED"
    BLOCKED = "BLOCKED"
    PENDING = "PENDING"
    EXCEPTIONAL = "EXCEPTIONAL"
    RESIDUAL = "RESIDUAL"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


@dataclass(frozen=True, slots=True)
class ArchimedeanEuclideanTransitionAuditResult:
    """Normalized audit surface for one transition request."""

    origin: str
    target: str
    domain: str
    trace_ref: str
    archimedean_status: ArchimedeanStatus
    euclidean_status: EuclideanStatus
    missing_units: tuple[str, ...]
    missing_gates: tuple[str, ...]
    missing_evidence: tuple[str, ...]
    trace_replay_status: TraceReplayStatus
    blocking_residuals: tuple[str, ...]
    rank_bound_status: RankBoundStatus
    final_status: StressCaseStatus
    forbidden_outputs_absent: tuple[str, ...]
    failure_code: FailureCode | None


@dataclass(frozen=True, slots=True)
class ConstitutionalStressCaseResult:
    """Execution result for one benchmark case."""

    case_id: str
    stress_family: str
    expected_status: StressCaseStatus
    actual_status: StressCaseStatus
    matches_expected: bool
    audit: ArchimedeanEuclideanTransitionAuditResult


def audit_transition(
    *,
    origin: str,
    target: str,
    domain: str,
    trace_ref: str,
    provided_steps: tuple[str, ...],
    required_units: tuple[str, ...],
    provided_gates: tuple[str, ...],
    required_gates: tuple[str, ...],
    provided_evidence: tuple[str, ...],
    required_evidence: tuple[str, ...],
    forbidden_outputs: tuple[str, ...],
    produced_outputs: tuple[str, ...] = (),
    blocking_residuals: tuple[str, ...] = (),
    residual_markers: tuple[str, ...] = (),
    exceptional_markers: tuple[str, ...] = (),
    requested_rank: int = 0,
    evidence_rank: int = 0,
    trace_replay_available: bool = False,
    trace_snapshot_only: bool = True,
    licensed_domains: tuple[str, ...] = (
        "text_understanding",
        "arabic_surface",
        "reasonableness_audit",
    ),
) -> ArchimedeanEuclideanTransitionAuditResult:
    """Audit one transition against decomposability, construction, and gate constraints."""

    provided_step_set = frozenset(provided_steps)
    provided_gate_set = frozenset(provided_gates)
    provided_evidence_set = frozenset(provided_evidence)

    missing_units = tuple(unit for unit in required_units if unit not in provided_step_set)
    missing_gates = tuple(gate for gate in required_gates if gate not in provided_gate_set)
    missing_evidence = tuple(
        evidence for evidence in required_evidence if evidence not in provided_evidence_set
    )

    if trace_replay_available:
        trace_replay_status = TraceReplayStatus.PASS
    elif trace_snapshot_only:
        trace_replay_status = TraceReplayStatus.SNAPSHOT_ONLY
    else:
        trace_replay_status = TraceReplayStatus.MISSING

    if requested_rank <= evidence_rank:
        rank_bound_status = RankBoundStatus.PASS
    else:
        rank_bound_status = RankBoundStatus.FAIL

    forbidden_outputs_absent = tuple(
        output for output in forbidden_outputs if output not in frozenset(produced_outputs)
    )

    direct_forbidden_target = target in _FORBIDDEN_DIRECT_TARGETS
    all_units_present = not missing_units
    all_gates_present = not missing_gates
    all_evidence_present = not missing_evidence

    if direct_forbidden_target and (not all_units_present or not all_gates_present):
        archimedean_status = ArchimedeanStatus.FAIL_NON_DECOMPOSABLE
        euclidean_status = EuclideanStatus.FAIL_UNCONSTRUCTED_STEP
        failure_code = FailureCode.FORBIDDEN_STRAIGHT_LINE
        final_status = StressCaseStatus.BLOCKED
    else:
        if all_units_present:
            archimedean_status = ArchimedeanStatus.PASS
        elif provided_steps:
            archimedean_status = ArchimedeanStatus.PARTIAL
        else:
            archimedean_status = ArchimedeanStatus.FAIL_NON_DECOMPOSABLE

        if all_gates_present:
            euclidean_status = EuclideanStatus.PASS
        elif provided_gates:
            euclidean_status = EuclideanStatus.PARTIAL
        else:
            euclidean_status = EuclideanStatus.FAIL_UNCONSTRUCTED_STEP

        if domain not in frozenset(licensed_domains):
            failure_code = FailureCode.DOMAIN_LEAP
            final_status = StressCaseStatus.OUT_OF_SCOPE
        elif blocking_residuals:
            failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT
            final_status = StressCaseStatus.BLOCKED
        elif not all_evidence_present:
            failure_code = FailureCode.GATE_REQUIRED
            final_status = StressCaseStatus.BLOCKED
        elif rank_bound_status is RankBoundStatus.FAIL:
            failure_code = FailureCode.RANK_EXCEEDS_CEILING
            final_status = StressCaseStatus.BLOCKED
        elif exceptional_markers:
            failure_code = FailureCode.GATE_REQUIRED
            final_status = StressCaseStatus.EXCEPTIONAL
        elif residual_markers or trace_replay_status is TraceReplayStatus.SNAPSHOT_ONLY:
            failure_code = None
            final_status = StressCaseStatus.RESIDUAL
        elif (
            archimedean_status is ArchimedeanStatus.PASS
            and euclidean_status is EuclideanStatus.PASS
            and all_evidence_present
        ):
            failure_code = None
            final_status = StressCaseStatus.LICENSED
        else:
            failure_code = FailureCode.GATE_REQUIRED
            final_status = StressCaseStatus.PENDING

    if final_status is StressCaseStatus.BLOCKED and failure_code is None:
        failure_code = FailureCode.GATE_REQUIRED

    return ArchimedeanEuclideanTransitionAuditResult(
        origin=origin,
        target=target,
        domain=domain,
        trace_ref=trace_ref,
        archimedean_status=archimedean_status,
        euclidean_status=euclidean_status,
        missing_units=missing_units,
        missing_gates=missing_gates,
        missing_evidence=missing_evidence,
        trace_replay_status=trace_replay_status,
        blocking_residuals=blocking_residuals,
        rank_bound_status=rank_bound_status,
        final_status=final_status,
        forbidden_outputs_absent=forbidden_outputs_absent,
        failure_code=failure_code,
    )


class ConstitutionalStressBenchmarkRunner:
    """Runtime runner for docs/80 stress fixture (measurement-only)."""

    def __init__(self, fixture_path: str | Path) -> None:
        path = Path(fixture_path)
        if not path.exists():
            raise FileNotFoundError(f"benchmark fixture not found: {path}")
        self._fixture_path = path

    def run(self) -> tuple[ConstitutionalStressCaseResult, ...]:
        payload = json.loads(self._fixture_path.read_text(encoding="utf-8"))
        results: list[ConstitutionalStressCaseResult] = []

        for case in payload["cases"]:
            result = self._run_case(case)
            results.append(result)

        return tuple(results)

    def _run_case(self, case: dict[str, object]) -> ConstitutionalStressCaseResult:
        family = str(case["stress_family"])
        expected_status = StressCaseStatus(str(case["expected_status"]))
        forbidden_outputs = tuple(str(item) for item in case["forbidden_outputs"])
        required_chain_anchor = str(case["required_chain_anchor"])

        profile = _benchmark_profile_for_family(family)
        audit = audit_transition(
            origin=required_chain_anchor,
            target=profile["target"],
            domain=profile["domain"],
            trace_ref=f"trace://ops-gov-80/{case['id']}",
            provided_steps=profile["provided_steps"],
            required_units=profile["required_units"],
            provided_gates=profile["provided_gates"],
            required_gates=profile["required_gates"],
            provided_evidence=profile["provided_evidence"],
            required_evidence=profile["required_evidence"],
            forbidden_outputs=forbidden_outputs,
            produced_outputs=(),
            blocking_residuals=profile["blocking_residuals"],
            residual_markers=profile["residual_markers"],
            exceptional_markers=profile["exceptional_markers"],
            requested_rank=profile["requested_rank"],
            evidence_rank=profile["evidence_rank"],
            trace_replay_available=profile["trace_replay_available"],
            trace_snapshot_only=profile["trace_snapshot_only"],
        )

        return ConstitutionalStressCaseResult(
            case_id=str(case["id"]),
            stress_family=family,
            expected_status=expected_status,
            actual_status=audit.final_status,
            matches_expected=audit.final_status is expected_status,
            audit=audit,
        )


def _benchmark_profile_for_family(family: str) -> dict[str, object]:
    common = {
        "required_units": (),
        "provided_steps": (),
        "required_gates": (),
        "provided_gates": (),
        "required_evidence": (),
        "provided_evidence": (),
        "blocking_residuals": (),
        "residual_markers": (),
        "exceptional_markers": (),
        "requested_rank": 2,
        "evidence_rank": 2,
        "trace_replay_available": False,
        "trace_snapshot_only": True,
    }

    profiles: dict[str, dict[str, object]] = {
        "UNVOCALIZED_TEXT": {
            **common,
            "target": "DiacritizationCandidate",
            "domain": "arabic_surface",
            "required_units": ("DIACRITIZATION_CANDIDATE",),
            "required_gates": ("DIACRITIZATION_GATE",),
            "trace_snapshot_only": False,
        },
        "MULTI_IRAB_ANALYSIS": {
            **common,
            "target": "SurfaceResolution",
            "domain": "arabic_surface",
            "required_units": ("MULTI_IRAB_CANDIDATE",),
            "provided_steps": ("MULTI_IRAB_CANDIDATE",),
            "required_gates": ("MULTI_IRAB_GATE",),
            "provided_gates": ("MULTI_IRAB_GATE",),
            "required_evidence": ("GRAMMAR_EVIDENCE",),
            "provided_evidence": ("GRAMMAR_EVIDENCE",),
            "residual_markers": ("IIRAB_COMPETITOR_VISIBLE",),
        },
        "AMBIGUOUS_PRONOUN": {
            **common,
            "target": "ReferenceBindingCandidate",
            "domain": "arabic_surface",
            "required_units": ("REFERENCE_BINDING_CANDIDATE",),
            "provided_steps": ("REFERENCE_BINDING_CANDIDATE",),
            "required_gates": ("REFERENCE_BINDING_GATE",),
            "provided_gates": ("REFERENCE_BINDING_GATE",),
            "required_evidence": ("PRONOUN_CONTEXT_EVIDENCE",),
            "provided_evidence": ("PRONOUN_CONTEXT_EVIDENCE",),
            "exceptional_markers": ("COMPETING_ANTECEDENT_ACTIVE",),
        },
        "MAJAZ_SIGNAL": {
            **common,
            "target": "MajazSemanticClosure",
            "domain": "majaz_semantics",
            "required_units": ("MAJAZ_LICENSE",),
            "required_gates": ("MAJAZ_LICENSE_GATE",),
            "required_evidence": ("MAJAZ_CONTEXT_QARINAH",),
            "trace_snapshot_only": False,
        },
        "ELLIPSIS_ESTIMATION": {
            **common,
            "target": "EllipsisCandidate",
            "domain": "arabic_surface",
            "required_units": ("ELLIPSIS_ESTIMATION_DISCIPLINE",),
            "provided_steps": ("ELLIPSIS_ESTIMATION_DISCIPLINE",),
            "required_gates": ("ELLIPSIS_ESTIMATION_GATE",),
            "provided_gates": ("ELLIPSIS_ESTIMATION_GATE",),
            "required_evidence": ("ELLIPSIS_CONTEXT_EVIDENCE",),
            "provided_evidence": ("ELLIPSIS_CONTEXT_EVIDENCE",),
            "trace_replay_available": True,
            "trace_snapshot_only": False,
        },
        "CLAIM_WITHOUT_EXTERNAL_EVIDENCE": {
            **common,
            "target": "ReasonablenessApproval",
            "domain": "reasonableness_audit",
            "required_units": ("CLAIM_GROUNDING_CANDIDATE",),
            "provided_steps": ("CLAIM_GROUNDING_CANDIDATE",),
            "required_gates": ("EXTERNAL_EVIDENCE_GATE",),
            "provided_gates": ("EXTERNAL_EVIDENCE_GATE",),
            "required_evidence": ("EXTERNAL_EVIDENCE_BUNDLE",),
            "provided_evidence": (),
            "trace_snapshot_only": False,
        },
    }

    if family not in profiles:
        raise ValueError(f"unsupported stress family: {family}")

    return profiles[family]


__all__ = [
    "ArchimedeanEuclideanTransitionAuditResult",
    "ArchimedeanStatus",
    "ConstitutionalStressBenchmarkRunner",
    "ConstitutionalStressCaseResult",
    "EuclideanStatus",
    "RankBoundStatus",
    "StressCaseStatus",
    "TraceReplayStatus",
    "audit_transition",
]
