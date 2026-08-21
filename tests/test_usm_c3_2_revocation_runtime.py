"""USM-C3.2 R39 revocation runtime tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    ClaimTypeId,
    DerivationPath,
    DomainId,
    EvidenceLifecycleState,
    EvidenceRecord,
    EvidenceTypeId,
    InvalidationDecision,
    KnowledgeAuthorityState,
    KnowledgeObjectRecord,
    RevocationPolicy,
    RevocationRuntime,
    RuleId,
    ScienceEvidenceContract,
    ScienceId,
    TraceRef,
    TrustAssumptionLayer,
    TrustKernelBoundary,
    USMFailureCode,
    USMSchemaError,
    explicit_rederive,
    query_provenance,
    replay_affected_set,
    revoke_evidence,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"USM-C3.2 ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2.1", "USM-C3", "USM-C3.1", "USM-C3.2"),
        chain_position="USM-C3.2 revocation propagation runtime for R39",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM capability authority hardening branch",
        forbidden_shortcut_assertions=(
            "EvidenceRevoked -> DeleteHistory",
            "EvidenceRevoked -> RetroactiveSilentRescue",
            "DependencyLinkOnly -> InvalidateWithoutAuthorityCheck",
            "TrustKernel -> SelfProof",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "HistoryRewrite",
            "SilentObjectRevalidation",
            "TCBSelfProofCertificate",
            "ExternalTruthCertificate",
        ),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _evidence_contract(tag: str) -> ScienceEvidenceContract:
    return ScienceEvidenceContract(
        evidence_type_id=EvidenceTypeId(f"EVIDENCE_TYPE::{tag}"),
        science_id=ScienceId("SCI::R39"),
        supported_claim_types=(ClaimTypeId("CLAIM-TYPE::R39"),),
        domain_scope=DomainId("DOMAIN::R39"),
        relevance_rule=RuleId("RULE::REL"),
        coverage_rule=RuleId("RULE::COV"),
        independence_rule=RuleId("RULE::IND"),
        counterevidence_rule=RuleId("RULE::CTR"),
        global_rank_ceiling=Rank.CANDIDATE,
        trace_ref=TraceRef(f"trace://r39/contracts/{tag}"),
    )


def _evidence(ref: str, *, revoked: bool = False) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_ref=ref,
        evidence_type_id=EvidenceTypeId(f"EVIDENCE_TYPE::{ref}"),
        contract_ref=_evidence_contract(ref),
        state=EvidenceLifecycleState.REVOKED if revoked else EvidenceLifecycleState.ACTIVE,
        revocation_event_refs=("rev-event::previous",) if revoked else (),
        trace_ref=TraceRef(f"trace://r39/evidence/{ref}"),
    )


def _path(ref: str, evidences: tuple[str, ...], deps: tuple[str, ...] = ()) -> DerivationPath:
    return DerivationPath(
        derivation_ref=f"derivation::{ref}",
        certificate_ref=f"certificate::{ref}",
        dependency_evidence_refs=evidences,
        dependency_object_refs=deps,
        trace_ref=TraceRef(f"trace://r39/derivations/{ref}"),
    )


def _object(
    ref: str,
    claim: str,
    *,
    paths: tuple[DerivationPath, ...],
    policy: RevocationPolicy = RevocationPolicy.MARK_INVALID,
    state: KnowledgeAuthorityState = KnowledgeAuthorityState.VALID,
) -> KnowledgeObjectRecord:
    return KnowledgeObjectRecord(
        object_ref=ref,
        claim_ref=claim,
        derivation_paths=paths,
        policy=policy,
        authority_state=state,
        invalidated_by_event_ref=None,
        trace_ref=TraceRef(f"trace://r39/objects/{ref}"),
    )


def _runtime(*, include_forged: bool = False) -> RevocationRuntime:
    objects = (
        _object("obj::direct", "claim::A", paths=(_path("direct", ("evi::1",)),)),
        _object("obj::parent", "claim::P", paths=(_path("parent", ("evi::1",)),)),
        _object(
            "obj::child",
            "claim::C",
            paths=(_path("child", ("evi::2",), deps=("obj::parent",)),),
            policy=RevocationPolicy.MARK_STALE,
        ),
        _object(
            "obj::shared",
            "claim::S",
            paths=(_path("shared", ("evi::1", "evi::2")),),
        ),
        _object(
            "obj::independent",
            "claim::I",
            paths=(
                _path("indep-a", ("evi::1",)),
                _path("indep-b", ("evi::2",)),
            ),
        ),
        _object("obj::unrelated", "claim::U", paths=(_path("unrelated", ("evi::3",)),)),
        _object(
            "obj::already-stale",
            "claim::R",
            paths=(_path("already-stale", ("evi::rev",)),),
            state=KnowledgeAuthorityState.STALE,
            policy=RevocationPolicy.MARK_STALE,
        ),
    )
    if include_forged:
        objects = objects + (
            _object("obj::forged", "claim::F", paths=(_path("forged", ("evi::missing",)),)),
        )

    return RevocationRuntime(
        tcb_boundary=TrustKernelBoundary(
            assumption_layer=TrustAssumptionLayer.OMEGA_0,
            assumption_statement="TCB soundness is an explicit foundational assumption.",
            components=(
                "TypeChecker",
                "CertificateVerifier",
                "InvariantChecker",
                "HashTraceVerifier",
            ),
            trace_ref=TraceRef("trace://r39/tcb/omega0"),
        ),
        evidence_records=(
            _evidence("evi::1"),
            _evidence("evi::2"),
            _evidence("evi::3"),
            _evidence("evi::rev", revoked=True),
        ),
        knowledge_objects=objects,
        events=(),
        trace_ref=TraceRef("trace://r39/runtime/base"),
    )


def _object_state(runtime: RevocationRuntime, ref: str) -> KnowledgeAuthorityState:
    return next(
        item.authority_state for item in runtime.knowledge_objects if item.object_ref == ref
    )


def test_direct_dependency_invalidation() -> None:
    _declare("direct dependency invalidation")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::1",
        trace_ref=TraceRef("trace://r39/events/rev-1"),
    )
    assert _object_state(result.runtime, "obj::direct") is KnowledgeAuthorityState.INVALID


def test_multi_hop_cascading_invalidation() -> None:
    _declare("multi-hop cascading invalidation")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::2",
        trace_ref=TraceRef("trace://r39/events/rev-2"),
    )
    assert _object_state(result.runtime, "obj::parent") is KnowledgeAuthorityState.INVALID
    assert _object_state(result.runtime, "obj::child") is KnowledgeAuthorityState.STALE


def test_unrelated_object_remains_valid() -> None:
    _declare("unrelated object remains valid")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::3",
        trace_ref=TraceRef("trace://r39/events/rev-3"),
    )
    assert _object_state(result.runtime, "obj::unrelated") is KnowledgeAuthorityState.VALID


def test_shared_derivation_with_one_revoked_dependency_invalidates() -> None:
    _declare("shared derivation one revoked dependency")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::4",
        trace_ref=TraceRef("trace://r39/events/rev-4"),
    )
    assert _object_state(result.runtime, "obj::shared") is KnowledgeAuthorityState.INVALID


def test_alternate_independent_derivation_stays_valid_when_sufficient() -> None:
    _declare("alternate independent derivation remains valid")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::5",
        trace_ref=TraceRef("trace://r39/events/rev-5"),
    )
    assert _object_state(result.runtime, "obj::independent") is KnowledgeAuthorityState.VALID


def test_revocation_of_already_revoked_evidence_is_idempotent() -> None:
    _declare("idempotent revocation for already-revoked evidence")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::rev",
        revocation_event_ref="rev-event::6",
        trace_ref=TraceRef("trace://r39/events/rev-6"),
    )
    assert result.affected_objects == ()


def test_no_retroactive_rescue_requires_explicit_rederivation() -> None:
    _declare("no retroactive rescue")
    revoked = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::7",
        trace_ref=TraceRef("trace://r39/events/rev-7"),
    ).runtime

    evidence_plus = revoked.evidence_records + (_evidence("evi::4"),)
    with_added_evidence = replace(revoked, evidence_records=evidence_plus)

    assert _object_state(with_added_evidence, "obj::direct") is KnowledgeAuthorityState.INVALID


def test_explicit_rederivation_creates_new_object_version() -> None:
    _declare("explicit re-derivation creates new object/version")
    revoked_runtime = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::8",
        trace_ref=TraceRef("trace://r39/events/rev-8"),
    ).runtime
    runtime_plus = replace(
        revoked_runtime,
        evidence_records=revoked_runtime.evidence_records + (_evidence("evi::4"),),
    )

    rederived = explicit_rederive(
        runtime_plus,
        prior_object_ref="obj::direct",
        new_object=_object(
            "obj::direct::v2",
            "claim::A",
            paths=(_path("direct-v2", ("evi::4",)),),
        ),
        rederivation_event_ref="rederive-event::1",
        trace_ref=TraceRef("trace://r39/events/rederive-1"),
    )

    assert _object_state(rederived.runtime, "obj::direct") is KnowledgeAuthorityState.INVALID
    assert _object_state(rederived.runtime, "obj::direct::v2") is KnowledgeAuthorityState.VALID


def test_provenance_history_remains_queryable_after_invalidation() -> None:
    _declare("append-only provenance remains queryable")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::9",
        trace_ref=TraceRef("trace://r39/events/rev-9"),
    )
    history = query_provenance(result.runtime, object_ref="obj::direct")
    assert history
    assert any(event.target_ref == "obj::direct" for event in history)


def test_forged_or_missing_dependency_reference_fails_closed() -> None:
    _declare("forged/missing dependency reference fails closed")
    result = revoke_evidence(
        _runtime(include_forged=True),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::10",
        trace_ref=TraceRef("trace://r39/events/rev-10"),
    )
    forged = next(item for item in result.affected_objects if item.object_ref == "obj::forged")
    assert forged.authority_state is KnowledgeAuthorityState.INVALID
    assert forged.decision is InvalidationDecision.FAIL_CLOSED
    assert forged.failure_code is USMFailureCode.REVOCATION_DEPENDENCY_REFERENCE_UNRESOLVED


def test_deterministic_replay_produces_same_affected_set() -> None:
    _declare("deterministic replay")
    runtime = _runtime()
    first = replay_affected_set(
        runtime,
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::11a",
        trace_ref=TraceRef("trace://r39/events/rev-11a"),
    )
    second = replay_affected_set(
        runtime,
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::11b",
        trace_ref=TraceRef("trace://r39/events/rev-11b"),
    )
    assert first == second


def test_auditability_exposes_revoked_evidence_to_decision_path() -> None:
    _declare("auditability path is explicit")
    result = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::12",
        trace_ref=TraceRef("trace://r39/events/rev-12"),
    )
    direct = next(item for item in result.affected_objects if item.object_ref == "obj::direct")
    assert direct.dependency_path
    assert direct.dependency_path[0] == "evi::1"


def test_tcb_boundary_is_explicit_omega0_assumption() -> None:
    _declare("R38 explicit TCB boundary")
    runtime = _runtime()
    assert runtime.tcb_boundary.assumption_layer is TrustAssumptionLayer.OMEGA_0
    assert runtime.tcb_boundary.components == (
        "TypeChecker",
        "CertificateVerifier",
        "InvariantChecker",
        "HashTraceVerifier",
    )


def test_rederive_without_new_licensed_path_is_rejected() -> None:
    _declare("invalid re-derivation rejected")
    revoked_runtime = revoke_evidence(
        _runtime(),
        evidence_ref="evi::1",
        revocation_event_ref="rev-event::13",
        trace_ref=TraceRef("trace://r39/events/rev-13"),
    ).runtime
    with pytest.raises(USMSchemaError):
        explicit_rederive(
            revoked_runtime,
            prior_object_ref="obj::direct",
            new_object=_object(
                "obj::direct::bad",
                "claim::A",
                paths=(_path("direct-bad", ("evi::1",)),),
            ),
            rederivation_event_ref="rederive-event::bad",
            trace_ref=TraceRef("trace://r39/events/rederive-bad"),
        )
