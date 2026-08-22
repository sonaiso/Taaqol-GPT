"""Tests for GUA-1 shared suites and final proof-certificate outcome."""

from __future__ import annotations

from dataclasses import replace

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

    try:
        GUA1ProofCertificate(
            status=GUA1Status.PASS,
            checks=checks,
            residuals=non_blocking_residuals,
            evidence=evidence,
            trace_ref=TRACE_REF,
            issuance_token=object(),
        )
    except GuaCoreSchemaError as exc:
        assert "must be issued via issue_gua1_proof_certificate" in str(exc)
    else:
        raise AssertionError("direct GUA1ProofCertificate construction unexpectedly succeeded")


def test_gua1_certificate_cannot_be_forged_via_issue_classmethod() -> None:
    evidence = _make_valid_evidence()
    forged_checks = (
        StageCheck(
            stage=GUA1Stage.GUA1_PROOF_CERTIFICATE,
            passed=True,
            detail="forged single-stage pass",
        ),
    )

    try:
        GUA1ProofCertificate._issue(
            status=GUA1Status.PASS,
            checks=forged_checks,
            residuals=ResidualSet(),
            evidence=evidence,
            trace_ref=TRACE_REF,
        )
    except GuaCoreSchemaError as exc:
        assert "must cover each GUA1Stage exactly once" in str(exc)
    else:
        raise AssertionError("GUA1ProofCertificate._issue unexpectedly accepted forged PASS")


def test_gua1_certificate_cannot_be_forged_with_real_issuance_token() -> None:
    evidence = _make_valid_evidence()
    forged_checks = (
        StageCheck(
            stage=GUA1Stage.GENERAL_CORE_EXTRACTION,
            passed=True,
            detail="forged extraction pass",
        ),
        StageCheck(
            stage=GUA1Stage.CORE_FREEZE,
            passed=True,
            detail="forged freeze pass",
        ),
        StageCheck(
            stage=GUA1Stage.REALIZATIONS,
            passed=True,
            detail="forged realizations pass",
        ),
        StageCheck(
            stage=GUA1Stage.SHARED_CONSTITUTIONAL_SUITE,
            passed=True,
            detail="forged shared suite pass",
        ),
        StageCheck(
            stage=GUA1Stage.CROSS_DOMAIN_SUITE,
            passed=True,
            detail="forged cross-domain pass",
        ),
        StageCheck(
            stage=GUA1Stage.GUA1_PROOF_CERTIFICATE,
            passed=True,
            detail="forged final pass",
        ),
    )

    try:
        GUA1ProofCertificate(
            status=GUA1Status.PASS,
            checks=forged_checks,
            residuals=ResidualSet(),
            evidence=evidence,
            trace_ref=TRACE_REF,
            issuance_token=GUA1ProofCertificate._ISSUANCE_TOKEN,
        )
    except GuaCoreSchemaError as exc:
        assert "must be derived from GUA1ProofEvidence" in str(exc)
    else:
        raise AssertionError(
            "GUA1ProofCertificate unexpectedly accepted forged PASS with real issuance token"
        )
