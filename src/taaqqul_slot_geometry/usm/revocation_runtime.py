"""USM-C3.2 bounded revocation runtime for dependency-sensitive authority recomputation.

This module implements Phase-1 MVP for R39 only:
Evidence -> DerivedKnowledge -> EvidenceRevocation -> CascadingInvalidation -> ExplicitReDerivation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.usm.evidence_contract import ScienceEvidenceContract
from taaqqul_slot_geometry.usm.identifiers import (
    EvidenceTypeId,
    TraceRef,
    USMSchemaError,
    require_non_empty_text,
    require_tuple_of_type,
)
from taaqqul_slot_geometry.usm.validator import USMFailureCode

_REQUIRED_TCB_COMPONENTS: tuple[str, ...] = (
    "TypeChecker",
    "CertificateVerifier",
    "InvariantChecker",
    "HashTraceVerifier",
)


class TrustAssumptionLayer(StrEnum):
    OMEGA_0 = "OMEGA_0"


class EvidenceLifecycleState(StrEnum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"


class KnowledgeAuthorityState(StrEnum):
    VALID = "VALID"
    STALE = "STALE"
    INVALID = "INVALID"


class RevocationPolicy(StrEnum):
    MARK_STALE = "MARK_STALE"
    MARK_INVALID = "MARK_INVALID"


class ProvenanceEventKind(StrEnum):
    EVIDENCE_REVOKED = "EVIDENCE_REVOKED"
    OBJECT_INVALIDATED = "OBJECT_INVALIDATED"
    OBJECT_REDERIVED = "OBJECT_REDERIVED"


class InvalidationDecision(StrEnum):
    KEEP_VALID = "KEEP_VALID"
    MARK_STALE = "MARK_STALE"
    MARK_INVALID = "MARK_INVALID"
    FAIL_CLOSED = "FAIL_CLOSED"


@dataclass(frozen=True, slots=True)
class TrustKernelBoundary:
    assumption_layer: TrustAssumptionLayer
    assumption_statement: str
    components: tuple[str, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if self.assumption_layer is not TrustAssumptionLayer.OMEGA_0:
            raise USMSchemaError(
                "TrustKernelBoundary.assumption_layer must be OMEGA_0 for TCB foundationalism"
            )
        require_non_empty_text(
            "TrustKernelBoundary",
            "assumption_statement",
            self.assumption_statement,
        )
        if not isinstance(self.components, tuple) or not all(
            isinstance(component, str) and component for component in self.components
        ):
            raise USMSchemaError("TrustKernelBoundary.components must be tuple[str]")
        if tuple(self.components) != _REQUIRED_TCB_COMPONENTS:
            raise USMSchemaError(
                "TrustKernelBoundary.components must equal "
                "('TypeChecker','CertificateVerifier','InvariantChecker','HashTraceVerifier')"
            )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TrustKernelBoundary.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_ref: str
    evidence_type_id: EvidenceTypeId
    contract_ref: ScienceEvidenceContract
    state: EvidenceLifecycleState
    revocation_event_refs: tuple[str, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        require_non_empty_text("EvidenceRecord", "evidence_ref", self.evidence_ref)
        if not isinstance(self.evidence_type_id, EvidenceTypeId):
            raise USMSchemaError("EvidenceRecord.evidence_type_id must be EvidenceTypeId")
        if not isinstance(self.contract_ref, ScienceEvidenceContract):
            raise USMSchemaError("EvidenceRecord.contract_ref must be ScienceEvidenceContract")
        if not isinstance(self.state, EvidenceLifecycleState):
            raise USMSchemaError("EvidenceRecord.state must be EvidenceLifecycleState")
        if not isinstance(self.revocation_event_refs, tuple) or not all(
            isinstance(ref, str) and ref for ref in self.revocation_event_refs
        ):
            raise USMSchemaError("EvidenceRecord.revocation_event_refs must be tuple[str]")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("EvidenceRecord.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class DerivationPath:
    derivation_ref: str
    certificate_ref: str
    dependency_evidence_refs: tuple[str, ...]
    dependency_object_refs: tuple[str, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        require_non_empty_text("DerivationPath", "derivation_ref", self.derivation_ref)
        require_non_empty_text("DerivationPath", "certificate_ref", self.certificate_ref)
        if not isinstance(self.dependency_evidence_refs, tuple) or not all(
            isinstance(ref, str) and ref for ref in self.dependency_evidence_refs
        ):
            raise USMSchemaError("DerivationPath.dependency_evidence_refs must be tuple[str]")
        if len(self.dependency_evidence_refs) == 0:
            raise USMSchemaError("DerivationPath.dependency_evidence_refs must not be empty")
        if not isinstance(self.dependency_object_refs, tuple) or not all(
            isinstance(ref, str) and ref for ref in self.dependency_object_refs
        ):
            raise USMSchemaError("DerivationPath.dependency_object_refs must be tuple[str]")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("DerivationPath.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class KnowledgeObjectRecord:
    object_ref: str
    claim_ref: str
    derivation_paths: tuple[DerivationPath, ...]
    policy: RevocationPolicy
    authority_state: KnowledgeAuthorityState
    invalidated_by_event_ref: str | None
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        require_non_empty_text("KnowledgeObjectRecord", "object_ref", self.object_ref)
        require_non_empty_text("KnowledgeObjectRecord", "claim_ref", self.claim_ref)
        require_tuple_of_type(
            "KnowledgeObjectRecord", "derivation_paths", self.derivation_paths, DerivationPath
        )
        if len(self.derivation_paths) == 0:
            raise USMSchemaError("KnowledgeObjectRecord.derivation_paths must not be empty")
        if not isinstance(self.policy, RevocationPolicy):
            raise USMSchemaError("KnowledgeObjectRecord.policy must be RevocationPolicy")
        if not isinstance(self.authority_state, KnowledgeAuthorityState):
            raise USMSchemaError(
                "KnowledgeObjectRecord.authority_state must be KnowledgeAuthorityState"
            )
        if self.invalidated_by_event_ref is not None:
            require_non_empty_text(
                "KnowledgeObjectRecord", "invalidated_by_event_ref", self.invalidated_by_event_ref
            )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("KnowledgeObjectRecord.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class ProvenanceEvent:
    event_ref: str
    kind: ProvenanceEventKind
    target_ref: str
    caused_by_ref: str | None
    dependency_path: tuple[str, ...]
    decision: InvalidationDecision | None
    failure_code: USMFailureCode | None
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        require_non_empty_text("ProvenanceEvent", "event_ref", self.event_ref)
        if not isinstance(self.kind, ProvenanceEventKind):
            raise USMSchemaError("ProvenanceEvent.kind must be ProvenanceEventKind")
        require_non_empty_text("ProvenanceEvent", "target_ref", self.target_ref)
        if self.caused_by_ref is not None:
            require_non_empty_text("ProvenanceEvent", "caused_by_ref", self.caused_by_ref)
        if not isinstance(self.dependency_path, tuple) or not all(
            isinstance(entry, str) and entry for entry in self.dependency_path
        ):
            raise USMSchemaError("ProvenanceEvent.dependency_path must be tuple[str]")
        if self.decision is not None and not isinstance(self.decision, InvalidationDecision):
            raise USMSchemaError("ProvenanceEvent.decision must be InvalidationDecision | None")
        if self.failure_code is not None and not isinstance(self.failure_code, USMFailureCode):
            raise USMSchemaError("ProvenanceEvent.failure_code must be USMFailureCode | None")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("ProvenanceEvent.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class RevocationRuntime:
    tcb_boundary: TrustKernelBoundary
    evidence_records: tuple[EvidenceRecord, ...]
    knowledge_objects: tuple[KnowledgeObjectRecord, ...]
    events: tuple[ProvenanceEvent, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.tcb_boundary, TrustKernelBoundary):
            raise USMSchemaError("RevocationRuntime.tcb_boundary must be TrustKernelBoundary")
        require_tuple_of_type(
            "RevocationRuntime", "evidence_records", self.evidence_records, EvidenceRecord
        )
        require_tuple_of_type(
            "RevocationRuntime",
            "knowledge_objects",
            self.knowledge_objects,
            KnowledgeObjectRecord,
        )
        require_tuple_of_type("RevocationRuntime", "events", self.events, ProvenanceEvent)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("RevocationRuntime.trace_ref must be TraceRef")
        if len({record.evidence_ref for record in self.evidence_records}) != len(
            self.evidence_records
        ):
            raise USMSchemaError("RevocationRuntime.evidence_records must have unique evidence_ref")
        if len({record.object_ref for record in self.knowledge_objects}) != len(
            self.knowledge_objects
        ):
            raise USMSchemaError("RevocationRuntime.knowledge_objects must have unique object_ref")
        if len({event.event_ref for event in self.events}) != len(self.events):
            raise USMSchemaError("RevocationRuntime.events must have unique event_ref")


@dataclass(frozen=True, slots=True)
class AffectedObject:
    object_ref: str
    authority_state: KnowledgeAuthorityState
    decision: InvalidationDecision
    dependency_path: tuple[str, ...]
    failure_code: USMFailureCode

    def __post_init__(self) -> None:
        require_non_empty_text("AffectedObject", "object_ref", self.object_ref)
        if not isinstance(self.authority_state, KnowledgeAuthorityState):
            raise USMSchemaError("AffectedObject.authority_state must be KnowledgeAuthorityState")
        if not isinstance(self.decision, InvalidationDecision):
            raise USMSchemaError("AffectedObject.decision must be InvalidationDecision")
        if self.decision is InvalidationDecision.KEEP_VALID:
            raise USMSchemaError("AffectedObject.decision cannot be KEEP_VALID")
        if not isinstance(self.dependency_path, tuple) or not all(
            isinstance(entry, str) and entry for entry in self.dependency_path
        ):
            raise USMSchemaError("AffectedObject.dependency_path must be tuple[str]")
        if not isinstance(self.failure_code, USMFailureCode):
            raise USMSchemaError("AffectedObject.failure_code must be USMFailureCode")


@dataclass(frozen=True, slots=True)
class RevocationResult:
    runtime: RevocationRuntime
    revocation_event: ProvenanceEvent
    affected_objects: tuple[AffectedObject, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.runtime, RevocationRuntime):
            raise USMSchemaError("RevocationResult.runtime must be RevocationRuntime")
        if not isinstance(self.revocation_event, ProvenanceEvent):
            raise USMSchemaError("RevocationResult.revocation_event must be ProvenanceEvent")
        require_tuple_of_type(
            "RevocationResult", "affected_objects", self.affected_objects, AffectedObject
        )


@dataclass(frozen=True, slots=True)
class ReDerivationResult:
    runtime: RevocationRuntime
    new_object: KnowledgeObjectRecord
    event: ProvenanceEvent

    def __post_init__(self) -> None:
        if not isinstance(self.runtime, RevocationRuntime):
            raise USMSchemaError("ReDerivationResult.runtime must be RevocationRuntime")
        if not isinstance(self.new_object, KnowledgeObjectRecord):
            raise USMSchemaError("ReDerivationResult.new_object must be KnowledgeObjectRecord")
        if not isinstance(self.event, ProvenanceEvent):
            raise USMSchemaError("ReDerivationResult.event must be ProvenanceEvent")


@dataclass(frozen=True, slots=True)
class _PathStatus:
    licensed: bool
    failure_code: USMFailureCode | None
    dependency_path: tuple[str, ...]


def revoke_evidence(
    runtime: RevocationRuntime,
    *,
    evidence_ref: str,
    revocation_event_ref: str,
    trace_ref: TraceRef,
) -> RevocationResult:
    """Apply append-only evidence revocation and recompute affected authority deterministically."""
    if not isinstance(runtime, RevocationRuntime):
        raise USMSchemaError("revoke_evidence requires RevocationRuntime")
    require_non_empty_text("revoke_evidence", "evidence_ref", evidence_ref)
    require_non_empty_text("revoke_evidence", "revocation_event_ref", revocation_event_ref)
    if not isinstance(trace_ref, TraceRef):
        raise USMSchemaError("revoke_evidence.trace_ref must be TraceRef")

    evidence_map = {record.evidence_ref: record for record in runtime.evidence_records}
    if evidence_ref not in evidence_map:
        raise USMSchemaError(
            "revoke_evidence.evidence_ref must resolve to existing EvidenceRecord "
            f"({USMFailureCode.REVOKED_EVIDENCE_UNRESOLVED.value})"
        )

    updated_evidence = []
    already_revoked = False
    for record in runtime.evidence_records:
        if record.evidence_ref != evidence_ref:
            updated_evidence.append(record)
            continue
        if record.state is EvidenceLifecycleState.REVOKED:
            already_revoked = True
            updated_evidence.append(record)
        else:
            updated_evidence.append(
                EvidenceRecord(
                    evidence_ref=record.evidence_ref,
                    evidence_type_id=record.evidence_type_id,
                    contract_ref=record.contract_ref,
                    state=EvidenceLifecycleState.REVOKED,
                    revocation_event_refs=record.revocation_event_refs + (revocation_event_ref,),
                    trace_ref=record.trace_ref,
                )
            )

    revocation_event = ProvenanceEvent(
        event_ref=revocation_event_ref,
        kind=ProvenanceEventKind.EVIDENCE_REVOKED,
        target_ref=evidence_ref,
        caused_by_ref=None,
        dependency_path=(evidence_ref,),
        decision=None,
        failure_code=None,
        trace_ref=trace_ref,
    )

    base_runtime = RevocationRuntime(
        tcb_boundary=runtime.tcb_boundary,
        evidence_records=tuple(updated_evidence),
        knowledge_objects=runtime.knowledge_objects,
        events=runtime.events,
        trace_ref=runtime.trace_ref,
    )

    if already_revoked:
        final_runtime = RevocationRuntime(
            tcb_boundary=base_runtime.tcb_boundary,
            evidence_records=base_runtime.evidence_records,
            knowledge_objects=base_runtime.knowledge_objects,
            events=base_runtime.events + (revocation_event,),
            trace_ref=base_runtime.trace_ref,
        )
        return RevocationResult(
            runtime=final_runtime,
            revocation_event=revocation_event,
            affected_objects=(),
        )

    affected, state_map = _recompute_authority(base_runtime, evidence_ref=evidence_ref)
    new_objects = tuple(
        KnowledgeObjectRecord(
            object_ref=record.object_ref,
            claim_ref=record.claim_ref,
            derivation_paths=record.derivation_paths,
            policy=record.policy,
            authority_state=state_map[record.object_ref],
            invalidated_by_event_ref=(
                revocation_event_ref
                if record.object_ref in {item.object_ref for item in affected}
                else record.invalidated_by_event_ref
            ),
            trace_ref=record.trace_ref,
        )
        for record in base_runtime.knowledge_objects
    )
    invalidation_events = tuple(
        ProvenanceEvent(
            event_ref=f"{revocation_event_ref}::invalidate::{index}",
            kind=ProvenanceEventKind.OBJECT_INVALIDATED,
            target_ref=item.object_ref,
            caused_by_ref=revocation_event_ref,
            dependency_path=item.dependency_path,
            decision=item.decision,
            failure_code=item.failure_code,
            trace_ref=TraceRef(f"{trace_ref.value}/affected/{index}"),
        )
        for index, item in enumerate(affected, start=1)
    )

    final_runtime = RevocationRuntime(
        tcb_boundary=base_runtime.tcb_boundary,
        evidence_records=base_runtime.evidence_records,
        knowledge_objects=new_objects,
        events=base_runtime.events + (revocation_event,) + invalidation_events,
        trace_ref=base_runtime.trace_ref,
    )

    return RevocationResult(
        runtime=final_runtime,
        revocation_event=revocation_event,
        affected_objects=affected,
    )


def explicit_rederive(
    runtime: RevocationRuntime,
    *,
    prior_object_ref: str,
    new_object: KnowledgeObjectRecord,
    rederivation_event_ref: str,
    trace_ref: TraceRef,
) -> ReDerivationResult:
    """Require explicit re-derivation to restore authority after invalidation."""
    if not isinstance(runtime, RevocationRuntime):
        raise USMSchemaError("explicit_rederive requires RevocationRuntime")
    require_non_empty_text("explicit_rederive", "prior_object_ref", prior_object_ref)
    require_non_empty_text("explicit_rederive", "rederivation_event_ref", rederivation_event_ref)
    if not isinstance(new_object, KnowledgeObjectRecord):
        raise USMSchemaError("explicit_rederive.new_object must be KnowledgeObjectRecord")
    if not isinstance(trace_ref, TraceRef):
        raise USMSchemaError("explicit_rederive.trace_ref must be TraceRef")

    object_map = {record.object_ref: record for record in runtime.knowledge_objects}
    if prior_object_ref not in object_map:
        raise USMSchemaError("explicit_rederive.prior_object_ref must resolve to existing object")
    prior = object_map[prior_object_ref]
    if new_object.object_ref in object_map:
        raise USMSchemaError("explicit_rederive.new_object.object_ref must be new identity")
    if new_object.claim_ref != prior.claim_ref:
        raise USMSchemaError("explicit_rederive requires claim continuity with prior object")

    evidence_map = {record.evidence_ref: record for record in runtime.evidence_records}
    object_state_map = {
        record.object_ref: record.authority_state for record in runtime.knowledge_objects
    }
    licensed = False
    for path in new_object.derivation_paths:
        status = _path_status(
            path,
            evidence_map=evidence_map,
            object_state_map=object_state_map,
            dependency_reason_paths={},
        )
        if status.licensed:
            licensed = True
            break
    if not licensed:
        raise USMSchemaError(
            "explicit_rederive.new_object must include at least one licensed derivation path"
        )

    event = ProvenanceEvent(
        event_ref=rederivation_event_ref,
        kind=ProvenanceEventKind.OBJECT_REDERIVED,
        target_ref=new_object.object_ref,
        caused_by_ref=prior_object_ref,
        dependency_path=(prior_object_ref, new_object.object_ref),
        decision=InvalidationDecision.KEEP_VALID,
        failure_code=None,
        trace_ref=trace_ref,
    )

    next_runtime = RevocationRuntime(
        tcb_boundary=runtime.tcb_boundary,
        evidence_records=runtime.evidence_records,
        knowledge_objects=runtime.knowledge_objects + (new_object,),
        events=runtime.events + (event,),
        trace_ref=runtime.trace_ref,
    )
    return ReDerivationResult(runtime=next_runtime, new_object=new_object, event=event)


def replay_affected_set(
    runtime: RevocationRuntime,
    *,
    evidence_ref: str,
    revocation_event_ref: str,
    trace_ref: TraceRef,
) -> tuple[str, ...]:
    """Return deterministic affected object set for replay assertions."""
    result = revoke_evidence(
        runtime,
        evidence_ref=evidence_ref,
        revocation_event_ref=revocation_event_ref,
        trace_ref=trace_ref,
    )
    return tuple(sorted(item.object_ref for item in result.affected_objects))


def query_provenance(runtime: RevocationRuntime, *, object_ref: str) -> tuple[ProvenanceEvent, ...]:
    """Return append-only provenance history for one object."""
    require_non_empty_text("query_provenance", "object_ref", object_ref)
    return tuple(
        event
        for event in runtime.events
        if event.target_ref == object_ref or event.caused_by_ref == object_ref
    )


def _recompute_authority(
    runtime: RevocationRuntime,
    *,
    evidence_ref: str,
) -> tuple[tuple[AffectedObject, ...], dict[str, KnowledgeAuthorityState]]:
    evidence_map = {record.evidence_ref: record for record in runtime.evidence_records}
    state_map = {record.object_ref: record.authority_state for record in runtime.knowledge_objects}
    dependency_reason_paths: dict[str, tuple[str, ...]] = {}
    affected: dict[str, AffectedObject] = {}

    changed = True
    while changed:
        changed = False
        for record in sorted(runtime.knowledge_objects, key=lambda entry: entry.object_ref):
            if state_map[record.object_ref] is not KnowledgeAuthorityState.VALID:
                continue

            any_licensed = False
            path_statuses: list[_PathStatus] = []
            for path in record.derivation_paths:
                status = _path_status(
                    path,
                    evidence_map=evidence_map,
                    object_state_map=state_map,
                    dependency_reason_paths=dependency_reason_paths,
                )
                path_statuses.append(status)
                if status.licensed:
                    any_licensed = True
                    break

            if any_licensed:
                continue

            fail_closed = next(
                (
                    status
                    for status in path_statuses
                    if status.failure_code
                    is USMFailureCode.REVOCATION_DEPENDENCY_REFERENCE_UNRESOLVED
                ),
                None,
            )
            if fail_closed is not None:
                decision = InvalidationDecision.FAIL_CLOSED
                next_state = KnowledgeAuthorityState.INVALID
                failure_code = USMFailureCode.REVOCATION_DEPENDENCY_REFERENCE_UNRESOLVED
                dependency_path = fail_closed.dependency_path
            else:
                decision = (
                    InvalidationDecision.MARK_INVALID
                    if record.policy is RevocationPolicy.MARK_INVALID
                    else InvalidationDecision.MARK_STALE
                )
                next_state = (
                    KnowledgeAuthorityState.INVALID
                    if decision is InvalidationDecision.MARK_INVALID
                    else KnowledgeAuthorityState.STALE
                )
                failure_code = USMFailureCode.REVOCATION_NO_REMAINING_LICENSED_DERIVATION
                dependency_path = _best_dependency_path(path_statuses, fallback=evidence_ref)

            changed = True
            state_map[record.object_ref] = next_state
            dependency_reason_paths[record.object_ref] = dependency_path
            affected[record.object_ref] = AffectedObject(
                object_ref=record.object_ref,
                authority_state=next_state,
                decision=decision,
                dependency_path=dependency_path,
                failure_code=failure_code,
            )

    return tuple(affected[key] for key in sorted(affected.keys())), state_map


def _path_status(
    path: DerivationPath,
    *,
    evidence_map: dict[str, EvidenceRecord],
    object_state_map: dict[str, KnowledgeAuthorityState],
    dependency_reason_paths: dict[str, tuple[str, ...]],
) -> _PathStatus:
    for evidence_ref in path.dependency_evidence_refs:
        evidence = evidence_map.get(evidence_ref)
        if evidence is None:
            return _PathStatus(
                licensed=False,
                failure_code=USMFailureCode.REVOCATION_DEPENDENCY_REFERENCE_UNRESOLVED,
                dependency_path=(evidence_ref, "missing-evidence-ref"),
            )
        if evidence.state is EvidenceLifecycleState.REVOKED:
            return _PathStatus(
                licensed=False,
                failure_code=USMFailureCode.REVOCATION_NO_REMAINING_LICENSED_DERIVATION,
                dependency_path=(evidence_ref,),
            )

    for object_ref in path.dependency_object_refs:
        state = object_state_map.get(object_ref)
        if state is None:
            return _PathStatus(
                licensed=False,
                failure_code=USMFailureCode.REVOCATION_DEPENDENCY_REFERENCE_UNRESOLVED,
                dependency_path=(object_ref, "missing-object-ref"),
            )
        if state is not KnowledgeAuthorityState.VALID:
            path_prefix = dependency_reason_paths.get(object_ref, (object_ref,))
            return _PathStatus(
                licensed=False,
                failure_code=USMFailureCode.REVOCATION_NO_REMAINING_LICENSED_DERIVATION,
                dependency_path=path_prefix + (object_ref,),
            )

    return _PathStatus(licensed=True, failure_code=None, dependency_path=())


def _best_dependency_path(path_statuses: list[_PathStatus], *, fallback: str) -> tuple[str, ...]:
    candidate = next(
        (status.dependency_path for status in path_statuses if status.dependency_path),
        (),
    )
    return candidate if candidate else (fallback,)


__all__ = [
    "AffectedObject",
    "DerivationPath",
    "EvidenceLifecycleState",
    "EvidenceRecord",
    "InvalidationDecision",
    "KnowledgeAuthorityState",
    "KnowledgeObjectRecord",
    "ProvenanceEvent",
    "ProvenanceEventKind",
    "ReDerivationResult",
    "RevocationPolicy",
    "RevocationResult",
    "RevocationRuntime",
    "TrustAssumptionLayer",
    "TrustKernelBoundary",
    "explicit_rederive",
    "query_provenance",
    "replay_affected_set",
    "revoke_evidence",
]
