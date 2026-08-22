"""Tests for GUA-1 shared suites and final proof-certificate outcome."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.gua import (
    CrossDomainSuite,
    DomainSpec,
    GeneralCoreExtraction,
    GUA1ProofCertificate,
    GUA1ProofEvidence,
    GUA1Stage,
    GUA1Status,
    GuaCoreSchemaError,
    LocalGeometry,
    PriorDomainMatrix,
    Residual,
    ResidualKind,
    ResidualSet,
    SharedConstitutionalSuite,
    StageCheck,
    Trace,
    TransitionContract,
    TypedSlot,
    build_default_realizations,
    build_shared_constitutional_suite,
    compute_general_core_extraction_hash,
    freeze_general_core,
    issue_gua1_proof_certificate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

TRACE_REF = "gua-proof-trace"


def _assert_chain_case(
    *,
    branch_name: str,
    certificate: GUA1ProofCertificate,
    expected_state: ClosureState,
    expected_failure_code: FailureCode | None,
    origin_law_ref: str,
    required_residual_visibility: bool = True,
) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/118", "GUA-1R", "GUA1ProofCertificate"),
        chain_position="GUA-1 proof integrity certificate closure",
        origin_law_ref=origin_law_ref,
        branch_of_origin="GUA proof-certificate integrity chain",
        forbidden_shortcut_assertions=(
            "Extraction -> PASS",
            "Freeze -> PASS without hash binding",
            "Realizations -> PASS without cross-domain coherence",
        ),
        expected_state=expected_state,
        expected_failure_code=expected_failure_code,
        forbidden_outputs=("PartialGUA1Success",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=required_residual_visibility,
    )
    residual_visibility = not certificate.residuals.has_hidden
    if certificate.status is GUA1Status.PASS:
        observed_failure_code = None
    elif certificate.residuals.has_hidden:
        observed_failure_code = FailureCode.HIDDEN_RESIDUAL
    elif certificate.residuals.has_blocking:
        observed_failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT
    else:
        observed_failure_code = FailureCode.FORBIDDEN_STRAIGHT_LINE
    result = ConstitutionalChainResult(
        state=(
            ClosureState.MINIMALLY_CLOSED
            if certificate.status is GUA1Status.PASS
            else ClosureState.FORBIDDEN_LEAP
        ),
        failure_code=observed_failure_code,
        rank=Rank.ZERO,
        residual_visibility=residual_visibility,
        trace_present=bool(certificate.trace_ref.strip()),
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _assert_refusal_chain_case(
    *,
    branch_name: str,
    origin_law_ref: str,
    observed_refusal: ObservedRefusal,
    expected_failure_code: FailureCode | None = None,
) -> None:
    observed_result = _derive_refusal_chain_result(observed_refusal)
    if expected_failure_code is not None:
        assert observed_result.failure_code is expected_failure_code
    case = ConstitutionalChainTestCase(
        origin_law="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/118", "GUA-1R.2", "GUA1ProofCertificate"),
        chain_position="GUA-1 proof integrity certificate closure",
        origin_law_ref=origin_law_ref,
        branch_of_origin="GUA proof-certificate integrity chain",
        forbidden_shortcut_assertions=(
            "Direct construction -> PASS",
            "Replay of valid certificate fields -> PASS",
            "Residual virtual override -> PASS",
        ),
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=observed_result.failure_code,
        forbidden_outputs=("ParallelIssuancePath",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    assert_constitutional_case(case, observed_result)


@dataclass(frozen=True, slots=True)
class ObservedRefusal:
    exception: GuaCoreSchemaError
    residuals: ResidualSet | None
    trace_ref: str | None


def _observe_refusal(
    action: Callable[[], object],
    *,
    residuals: ResidualSet | None = None,
    trace_ref: str | None = TRACE_REF,
) -> ObservedRefusal:
    with pytest.raises(GuaCoreSchemaError) as exc_info:
        action()
    return ObservedRefusal(
        exception=exc_info.value,
        residuals=residuals,
        trace_ref=trace_ref,
    )


def _derive_refusal_chain_result(observed: ObservedRefusal) -> ConstitutionalChainResult:
    has_hidden, has_blocking = _concrete_residual_flags(observed.residuals)
    if has_hidden:
        failure_code = FailureCode.HIDDEN_RESIDUAL
    elif has_blocking:
        failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT
    else:
        failure_code = FailureCode.FORBIDDEN_STRAIGHT_LINE
    trace_present = bool((observed.trace_ref or "").strip())
    return ConstitutionalChainResult(
        state=ClosureState.FORBIDDEN_LEAP,
        failure_code=failure_code,
        rank=Rank.ZERO,
        residual_visibility=not has_hidden,
        trace_present=trace_present,
        produced_outputs=frozenset(),
    )


def _concrete_residual_flags(residuals: ResidualSet | None) -> tuple[bool, bool]:
    if residuals is None:
        return (False, False)
    has_hidden = False
    has_blocking = False
    for residual in residuals.items:
        if not residual.visible:
            has_hidden = True
        if residual.kind is ResidualKind.BLOCKING:
            has_blocking = True
    return (has_hidden, has_blocking)


def _make_extraction() -> GeneralCoreExtraction:
    return GeneralCoreExtraction(
        domain=DomainSpec(
            domain_id="generic-domain",
            scope="bounded-scope",
            boundaries=("domain", "scope"),
            invariants=("identity_continuity",),
        ),
        prior_matrix=PriorDomainMatrix(
            domain_id="generic-domain",
            required_priors=("declared_origin",),
            trace_ref=TRACE_REF,
        ),
        geometry=LocalGeometry(
            slots=(
                TypedSlot(
                    slot_type="unit",
                    domain_id="generic-domain",
                    coordinates=("axis_a", "axis_b"),
                    boundary=("domain", "scope"),
                    invariants=("identity_continuity",),
                    prior_requirements=("declared_origin",),
                    admissible_states=("candidate",),
                    residual_region=("visible_residual",),
                ),
            ),
            trace=Trace(trace_ref=TRACE_REF, stage="extraction"),
        ),
        transitions=(
            TransitionContract(
                transition_id="unit_to_relation",
                source_state="candidate",
                target_state="relation",
                required_evidence=("traceable_observation",),
                rank_ceiling="CANDIDATE",
                trace_ref=TRACE_REF,
            ),
        ),
    )


def _make_valid_evidence() -> GUA1ProofEvidence:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)
    return GUA1ProofEvidence(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )


def test_gua1_proof_certificate_passes_for_complete_chain() -> None:
    branch_name = "GUA-1 full chain pass"
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.PASS
    assert all(check.passed for check in certificate.checks)
    _assert_chain_case(
        branch_name=branch_name,
        certificate=certificate,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#4-pass-predicate",
    )


def test_gua1_proof_certificate_fails_for_incomplete_realizations() -> None:
    branch_name = "GUA-1 incomplete chain fails"
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations[:3], trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations[:3],
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    assert any(not check.passed for check in certificate.checks)
    _assert_chain_case(
        branch_name=branch_name,
        certificate=certificate,
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
    )


def test_gua1_proof_certificate_fails_for_forged_freeze_hash() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    forged = replace(frozen, extraction_hash="forged-hash")
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=forged,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    freeze_stage = next(check for check in certificate.checks if check.stage.name == "CORE_FREEZE")
    assert freeze_stage.passed is False


def test_gua1_proof_certificate_fails_for_realization_hash_mismatch() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    wrong_hash = compute_general_core_extraction_hash(_make_extraction())
    forged_realization = replace(realizations[0], frozen_core_hash=f"{wrong_hash}-mismatch")
    forged_realizations = (forged_realization, *realizations[1:])
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=forged_realizations, trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=forged_realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    realization_stage = next(
        check for check in certificate.checks if check.stage.name == "REALIZATIONS"
    )
    assert realization_stage.passed is False


def test_gua1_proof_certificate_fails_for_cross_suite_tuple_mismatch() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    mismatched = (realizations[1], realizations[0], realizations[2], realizations[3])
    cross_suite = CrossDomainSuite(contracts=mismatched, trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    cross_stage = next(
        check for check in certificate.checks if check.stage.name == "CROSS_DOMAIN_SUITE"
    )
    assert cross_stage.passed is False


def test_gua1_proof_certificate_fails_with_hidden_residual() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)
    hidden_residuals = ResidualSet(
        items=(
            Residual(
                kind=ResidualKind.INFORMATIONAL,
                detail="hidden informational residual must fail certificate",
                visible=False,
            ),
        )
    )

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
        residuals=hidden_residuals,
    )

    assert certificate.status is GUA1Status.FAIL
    assert certificate.residuals.has_hidden is True
    _assert_chain_case(
        branch_name="GUA-1 hidden residual refusal",
        certificate=certificate,
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.HIDDEN_RESIDUAL,
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
        required_residual_visibility=False,
    )


def test_gua1_proof_certificate_fails_with_blocking_residual() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)
    blocking_residuals = ResidualSet(
        items=(
            Residual(
                kind=ResidualKind.BLOCKING,
                detail="blocking residual must fail certificate",
                visible=True,
            ),
        )
    )

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
        residuals=blocking_residuals,
    )

    assert certificate.status is GUA1Status.FAIL
    assert certificate.residuals.has_blocking is True
    _assert_chain_case(
        branch_name="GUA-1 blocking residual refusal",
        certificate=certificate,
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
    )


def test_shared_suite_rejects_manual_witness_substitution() -> None:
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)
    forged_shared_suite = SharedConstitutionalSuite(
        extraction_type_witness="GeneralCoreExtraction",
        freeze_hash_witness=frozen.extraction_hash,
        recomputed_hash_witness=frozen.extraction_hash,
        legacy_core_integrity_witness="forged-witness",
        trace_ref=TRACE_REF,
    )

    certificate = issue_gua1_proof_certificate(
        extraction=extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=forged_shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    shared_stage = next(
        check for check in certificate.checks if check.stage.name == "SHARED_CONSTITUTIONAL_SUITE"
    )
    assert shared_stage.passed is False


def test_gua1_proof_certificate_fails_for_trace_substitution() -> None:
    extraction = _make_extraction()
    forged_extraction = replace(
        extraction,
        prior_matrix=replace(extraction.prior_matrix, trace_ref="forged-gua-proof-trace"),
    )
    frozen = freeze_general_core(forged_extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)
    shared_suite = build_shared_constitutional_suite(forged_extraction, frozen)
    cross_suite = CrossDomainSuite(contracts=realizations, trace_ref=TRACE_REF)

    certificate = issue_gua1_proof_certificate(
        extraction=forged_extraction,
        core_freeze=frozen,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_suite,
        trace_ref=TRACE_REF,
    )

    assert certificate.status is GUA1Status.FAIL
    extraction_stage = next(
        check for check in certificate.checks if check.stage.name == "GENERAL_CORE_EXTRACTION"
    )
    assert extraction_stage.passed is False
    _assert_chain_case(
        branch_name="GUA-1 trace substitution refusal",
        certificate=certificate,
        expected_state=ClosureState.FORBIDDEN_LEAP,
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#6-test-discipline",
    )


def test_gua1_certificate_cannot_be_directly_forged_even_if_fields_look_valid() -> None:
    evidence = _make_valid_evidence()
    non_blocking_residuals = ResidualSet()
    checks = (
        StageCheck(
            stage=GUA1Stage.GENERAL_CORE_EXTRACTION,
            passed=True,
            detail="forged extraction stage",
        ),
        StageCheck(stage=GUA1Stage.CORE_FREEZE, passed=True, detail="forged freeze stage"),
        StageCheck(stage=GUA1Stage.REALIZATIONS, passed=True, detail="forged realization stage"),
        StageCheck(
            stage=GUA1Stage.SHARED_CONSTITUTIONAL_SUITE,
            passed=True,
            detail="forged shared suite stage",
        ),
        StageCheck(
            stage=GUA1Stage.CROSS_DOMAIN_SUITE,
            passed=True,
            detail="forged cross-domain stage",
        ),
        StageCheck(
            stage=GUA1Stage.GUA1_PROOF_CERTIFICATE,
            passed=True,
            detail="forged final stage",
        ),
    )

    def _forge_direct_certificate() -> None:
        GUA1ProofCertificate(
            status=GUA1Status.PASS,
            checks=checks,
            residuals=non_blocking_residuals,
            evidence=evidence,
            trace_ref=TRACE_REF,
            issuance_capability=object(),
        )

    observed_refusal = _observe_refusal(_forge_direct_certificate, residuals=non_blocking_residuals)
    assert "must be issued via issue_gua1_proof_certificate" in str(observed_refusal.exception)
    _assert_refusal_chain_case(
        branch_name="GUA-1 direct construction forgery refusal",
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
        observed_refusal=observed_refusal,
    )


def test_gua1_certificate_replay_of_valid_pass_fields_is_refused() -> None:
    evidence = _make_valid_evidence()
    valid_certificate = issue_gua1_proof_certificate(
        extraction=evidence.extraction,
        core_freeze=evidence.core_freeze,
        realizations=evidence.realizations,
        shared_suite=evidence.shared_suite,
        cross_domain_suite=evidence.cross_domain_suite,
        trace_ref=evidence.trace_ref,
    )

    def _replay_valid_certificate_fields() -> None:
        GUA1ProofCertificate(
            status=valid_certificate.status,
            checks=valid_certificate.checks,
            residuals=valid_certificate.residuals,
            evidence=valid_certificate.evidence,
            trace_ref=valid_certificate.trace_ref,
            issuance_capability=object(),
        )

    observed_refusal = _observe_refusal(
        _replay_valid_certificate_fields,
        residuals=valid_certificate.residuals,
        trace_ref=valid_certificate.trace_ref,
    )
    assert "must be issued via issue_gua1_proof_certificate" in str(observed_refusal.exception)
    _assert_refusal_chain_case(
        branch_name="GUA-1 valid-certificate replay forgery refusal",
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
        observed_refusal=observed_refusal,
    )


def test_gua1_certificate_rejects_residual_set_subclass_forgery() -> None:
    class ForgedResidualSet(ResidualSet):
        @property
        def has_blocking(self) -> bool:
            return False

        @property
        def has_hidden(self) -> bool:
            return False

    evidence = _make_valid_evidence()
    forged_residuals = ForgedResidualSet(
        items=(
            Residual(
                kind=ResidualKind.BLOCKING,
                detail="blocking residual hidden by virtual override",
                visible=True,
            ),
        )
    )

    def _issue_with_forged_residual_subclass() -> None:
        issue_gua1_proof_certificate(
            extraction=evidence.extraction,
            core_freeze=evidence.core_freeze,
            realizations=evidence.realizations,
            shared_suite=evidence.shared_suite,
            cross_domain_suite=evidence.cross_domain_suite,
            trace_ref=evidence.trace_ref,
            residuals=forged_residuals,
        )

    observed_refusal = _observe_refusal(
        _issue_with_forged_residual_subclass,
        residuals=forged_residuals,
        trace_ref=evidence.trace_ref,
    )
    assert "concrete ResidualSet" in str(observed_refusal.exception)
    _assert_refusal_chain_case(
        branch_name="GUA-1 residual subclass forgery refusal",
        origin_law_ref="docs/118_GUA_1_PROOF_INTEGRITY_BOUNDARY_LAW.md#5-forbidden-surface",
        observed_refusal=observed_refusal,
        expected_failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
    )


def test_gua1_certificate_has_no_class_level_issuance_token_surface() -> None:
    assert hasattr(GUA1ProofCertificate, "_ISSUANCE_TOKEN") is False
