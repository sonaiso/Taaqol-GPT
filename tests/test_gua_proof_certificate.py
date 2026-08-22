"""Tests for GUA-1 shared suites and final proof-certificate outcome."""

from __future__ import annotations

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.gua import (
    CrossDomainSuite,
    DomainSpec,
    GeneralCoreExtraction,
    GUA1Status,
    LocalGeometry,
    PriorDomainMatrix,
    SharedConstitutionalSuite,
    Trace,
    TransitionContract,
    TypedSlot,
    build_default_realizations,
    freeze_general_core,
    issue_gua1_proof_certificate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

TRACE_REF = "gua-proof-trace"


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/112", "GUA-1", "GUA1ProofCertificate"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("PartialGUA1Success",),
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


def test_gua1_proof_certificate_passes_for_complete_chain() -> None:
    _declare("GUA-1 full chain pass")
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)

    shared_suite = SharedConstitutionalSuite(
        extraction_is_typed=True,
        freeze_is_deterministic=True,
        legacy_core_untouched=True,
        trace_ref=TRACE_REF,
    )
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


def test_gua1_proof_certificate_fails_for_incomplete_realizations() -> None:
    _declare("GUA-1 incomplete chain fails")
    extraction = _make_extraction()
    frozen = freeze_general_core(extraction)
    realizations = build_default_realizations(frozen, TRACE_REF)

    shared_suite = SharedConstitutionalSuite(
        extraction_is_typed=True,
        freeze_is_deterministic=True,
        legacy_core_untouched=True,
        trace_ref=TRACE_REF,
    )
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
