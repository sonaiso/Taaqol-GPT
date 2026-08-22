"""GUA-1 proof suites and final proof-certificate carrier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError
from taaqqul_slot_geometry.gua.core.geometry import (
    CoreFreeze,
    GeneralCoreExtraction,
    compute_general_core_extraction_hash,
)
from taaqqul_slot_geometry.gua.core.realization import RealizationContract
from taaqqul_slot_geometry.gua.core.residual import Residual, ResidualKind, ResidualSet

_REQUIRED_REALIZATION_DOMAINS = frozenset(
    {"language", "mathematics", "physics", "programming"}
)
_LEGACY_CORE_INTEGRITY_WITNESS = (
    "additive-surface-only:src/taaqqul_slot_geometry/core remains outside gua/"
)
_GUA1_ISSUANCE_CAPABILITY = object()


class GUA1Status(StrEnum):
    """Single final outcome for GUA-1."""

    PASS = "PASS"
    FAIL = "FAIL"


class GUA1Stage(StrEnum):
    """Non-partial stage chain inside GUA-1."""

    GENERAL_CORE_EXTRACTION = "GeneralCoreExtraction"
    CORE_FREEZE = "CoreFreeze"
    REALIZATIONS = "4Realizations"
    SHARED_CONSTITUTIONAL_SUITE = "SharedConstitutionalSuite"
    CROSS_DOMAIN_SUITE = "CrossDomainSuite"
    GUA1_PROOF_CERTIFICATE = "GUA1ProofCertificate"


@dataclass(frozen=True, slots=True)
class StageCheck:
    """Single stage result inside the final certificate."""

    stage: GUA1Stage
    passed: bool
    detail: str

    def __post_init__(self) -> None:
        if not isinstance(self.stage, GUA1Stage):
            raise GuaCoreSchemaError("StageCheck.stage must be GUA1Stage")
        if not isinstance(self.passed, bool):
            raise GuaCoreSchemaError("StageCheck.passed must be bool")
        if not isinstance(self.detail, str) or not self.detail.strip():
            raise GuaCoreSchemaError("StageCheck.detail must be a non-empty string")


@dataclass(frozen=True, slots=True)
class SharedConstitutionalSuite:
    """Shared suite that validates common constitutional invariants."""

    extraction_type_witness: str
    freeze_hash_witness: str
    recomputed_hash_witness: str
    legacy_core_integrity_witness: str
    trace_ref: str

    def __post_init__(self) -> None:
        _require_str(
            self.__class__.__name__,
            "extraction_type_witness",
            self.extraction_type_witness,
        )
        _require_str(self.__class__.__name__, "freeze_hash_witness", self.freeze_hash_witness)
        _require_str(
            self.__class__.__name__,
            "recomputed_hash_witness",
            self.recomputed_hash_witness,
        )
        _require_str(
            self.__class__.__name__,
            "legacy_core_integrity_witness",
            self.legacy_core_integrity_witness,
        )
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)

    @property
    def passed(self) -> bool:
        return (
            self.extraction_type_witness == GeneralCoreExtraction.__name__
            and self.freeze_hash_witness == self.recomputed_hash_witness
            and self.legacy_core_integrity_witness == _LEGACY_CORE_INTEGRITY_WITNESS
        )


def build_shared_constitutional_suite(
    extraction: GeneralCoreExtraction, core_freeze: CoreFreeze
) -> SharedConstitutionalSuite:
    """Build a shared-suite witness from concrete extraction/freeze artifacts."""

    if not isinstance(extraction, GeneralCoreExtraction):
        raise GuaCoreSchemaError("build_shared_constitutional_suite expects GeneralCoreExtraction")
    if not isinstance(core_freeze, CoreFreeze):
        raise GuaCoreSchemaError("build_shared_constitutional_suite expects CoreFreeze")
    return SharedConstitutionalSuite(
        extraction_type_witness=type(extraction).__name__,
        freeze_hash_witness=core_freeze.extraction_hash,
        recomputed_hash_witness=compute_general_core_extraction_hash(extraction),
        legacy_core_integrity_witness=_LEGACY_CORE_INTEGRITY_WITNESS,
        trace_ref=core_freeze.trace_ref,
    )


@dataclass(frozen=True, slots=True)
class CrossDomainSuite:
    """Cross-domain suite validating the four realization contracts."""

    contracts: tuple[RealizationContract, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.contracts, tuple) or not self.contracts:
            raise GuaCoreSchemaError("CrossDomainSuite.contracts must be a non-empty tuple")
        for contract in self.contracts:
            if not isinstance(contract, RealizationContract):
                raise GuaCoreSchemaError(
                    "CrossDomainSuite.contracts entries must be RealizationContract"
                )
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)

    @property
    def passed(self) -> bool:
        domains = {contract.domain for contract in self.contracts}
        if domains != _REQUIRED_REALIZATION_DOMAINS:
            return False
        frozen_hashes = {contract.frozen_core_hash for contract in self.contracts}
        if len(frozen_hashes) != 1:
            return False
        return all(_contract_trace_matches(contract, self.trace_ref) for contract in self.contracts)


@dataclass(frozen=True, slots=True)
class GUA1ProofEvidence:
    """Artifact chain required to derive a GUA-1 certificate verdict."""

    extraction: GeneralCoreExtraction
    core_freeze: CoreFreeze
    realizations: tuple[RealizationContract, ...]
    shared_suite: SharedConstitutionalSuite
    cross_domain_suite: CrossDomainSuite
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.extraction, GeneralCoreExtraction):
            raise GuaCoreSchemaError("GUA1ProofEvidence.extraction must be GeneralCoreExtraction")
        if not isinstance(self.core_freeze, CoreFreeze):
            raise GuaCoreSchemaError("GUA1ProofEvidence.core_freeze must be CoreFreeze")
        if not isinstance(self.realizations, tuple) or not self.realizations:
            raise GuaCoreSchemaError(
                "GUA1ProofEvidence.realizations must be a non-empty tuple"
            )
        for realization in self.realizations:
            if not isinstance(realization, RealizationContract):
                raise GuaCoreSchemaError(
                    "GUA1ProofEvidence.realizations entries must be RealizationContract"
                )
        if not isinstance(self.shared_suite, SharedConstitutionalSuite):
            raise GuaCoreSchemaError(
                "GUA1ProofEvidence.shared_suite must be SharedConstitutionalSuite"
            )
        if not isinstance(self.cross_domain_suite, CrossDomainSuite):
            raise GuaCoreSchemaError(
                "GUA1ProofEvidence.cross_domain_suite must be CrossDomainSuite"
            )
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True, init=False)
class GUA1ProofCertificate:
    """Final non-partial proof artifact for GUA-1."""

    status: GUA1Status
    checks: tuple[StageCheck, ...]
    residuals: ResidualSet
    evidence: GUA1ProofEvidence
    trace_ref: str

    def __init__(
        self,
        *,
        status: GUA1Status,
        checks: tuple[StageCheck, ...],
        residuals: ResidualSet,
        evidence: GUA1ProofEvidence,
        trace_ref: str,
        issuance_capability: object,
    ) -> None:
        if issuance_capability is not _GUA1_ISSUANCE_CAPABILITY:
            raise GuaCoreSchemaError(
                "GUA1ProofCertificate must be issued via issue_gua1_proof_certificate"
            )
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "checks", checks)
        object.__setattr__(self, "residuals", residuals)
        object.__setattr__(self, "evidence", evidence)
        object.__setattr__(self, "trace_ref", trace_ref)
        self.__post_init__()

    def __post_init__(self) -> None:
        if not isinstance(self.status, GUA1Status):
            raise GuaCoreSchemaError("GUA1ProofCertificate.status must be GUA1Status")
        if not isinstance(self.checks, tuple) or not self.checks:
            raise GuaCoreSchemaError("GUA1ProofCertificate.checks must be a non-empty tuple")
        for check in self.checks:
            if not isinstance(check, StageCheck):
                raise GuaCoreSchemaError("GUA1ProofCertificate.checks entries must be StageCheck")
        if type(self.residuals) is not ResidualSet:
            raise GuaCoreSchemaError("GUA1ProofCertificate.residuals must be concrete ResidualSet")
        if not isinstance(self.evidence, GUA1ProofEvidence):
            raise GuaCoreSchemaError("GUA1ProofCertificate.evidence must be GUA1ProofEvidence")
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)
        _require_exact_stage_coverage(self.checks)
        if self.trace_ref != self.evidence.trace_ref:
            raise GuaCoreSchemaError("GUA1ProofCertificate.trace_ref must match evidence trace_ref")
        expected_status, expected_checks = _derive_certificate_from_evidence(
            self.evidence, self.residuals
        )
        if self.status != expected_status or self.checks != expected_checks:
            raise GuaCoreSchemaError(
                "GUA1ProofCertificate status/checks must be derived from GUA1ProofEvidence"
            )
        if self.status is GUA1Status.PASS:
            has_hidden, has_blocking = _compute_validated_residual_flags(self.residuals)
            if has_hidden or has_blocking:
                raise GuaCoreSchemaError(
                    "GUA1ProofCertificate PASS is forbidden with hidden/blocking residuals"
                )
            if any(not check.passed for check in self.checks):
                raise GuaCoreSchemaError(
                    "GUA1ProofCertificate PASS requires all stage checks to pass"
                )

def issue_gua1_proof_certificate(
    extraction: GeneralCoreExtraction,
    core_freeze: CoreFreeze,
    realizations: tuple[RealizationContract, ...],
    shared_suite: SharedConstitutionalSuite,
    cross_domain_suite: CrossDomainSuite,
    trace_ref: str,
    residuals: ResidualSet | None = None,
) -> GUA1ProofCertificate:
    """Evaluate all GUA-1 stages and produce the single PASS/FAIL certificate."""

    evidence = GUA1ProofEvidence(
        extraction=extraction,
        core_freeze=core_freeze,
        realizations=realizations,
        shared_suite=shared_suite,
        cross_domain_suite=cross_domain_suite,
        trace_ref=trace_ref,
    )
    evaluated_residuals = residuals if residuals is not None else ResidualSet()
    status, all_checks = _derive_certificate_from_evidence(evidence, evaluated_residuals)
    return GUA1ProofCertificate(
        status=status,
        checks=all_checks,
        residuals=evaluated_residuals,
        evidence=evidence,
        trace_ref=trace_ref,
        issuance_capability=_GUA1_ISSUANCE_CAPABILITY,
    )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_bool(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be bool")


def _contract_trace_matches(contract: RealizationContract, trace_ref: str) -> bool:
    if contract.trace_ref != trace_ref:
        return False
    return all(transition.trace_ref == trace_ref for transition in contract.transitions)


def _extraction_is_trace_continuous(extraction: GeneralCoreExtraction, trace_ref: str) -> bool:
    if extraction.geometry.trace.trace_ref != trace_ref:
        return False
    if extraction.prior_matrix.trace_ref != trace_ref:
        return False
    return all(transition.trace_ref == trace_ref for transition in extraction.transitions)


def _derive_certificate_from_evidence(
    evidence: GUA1ProofEvidence, residuals: ResidualSet
) -> tuple[GUA1Status, tuple[StageCheck, ...]]:
    has_hidden, has_blocking = _compute_validated_residual_flags(residuals)
    expected_extraction_hash = compute_general_core_extraction_hash(evidence.extraction)
    expected_shared_suite = build_shared_constitutional_suite(
        evidence.extraction, evidence.core_freeze
    )
    stage_checks = (
        StageCheck(
            stage=GUA1Stage.GENERAL_CORE_EXTRACTION,
            passed=_extraction_is_trace_continuous(evidence.extraction, evidence.trace_ref),
            detail="general core extraction is structurally complete",
        ),
        StageCheck(
            stage=GUA1Stage.CORE_FREEZE,
            passed=(
                evidence.core_freeze.trace_ref == evidence.trace_ref
                and evidence.core_freeze.extraction_hash == expected_extraction_hash
            ),
            detail="core freeze is present and trace-bound",
        ),
        StageCheck(
            stage=GUA1Stage.REALIZATIONS,
            passed=(
                len(evidence.realizations) == 4
                and all(
                    realization.frozen_core_hash == evidence.core_freeze.extraction_hash
                    and _contract_trace_matches(realization, evidence.trace_ref)
                    for realization in evidence.realizations
                )
                and {realization.domain for realization in evidence.realizations}
                == _REQUIRED_REALIZATION_DOMAINS
            ),
            detail="four realization contracts are present",
        ),
        StageCheck(
            stage=GUA1Stage.SHARED_CONSTITUTIONAL_SUITE,
            passed=(
                evidence.shared_suite == expected_shared_suite
                and evidence.shared_suite.passed
                and evidence.shared_suite.trace_ref == evidence.trace_ref
            ),
            detail="shared constitutional suite passed",
        ),
        StageCheck(
            stage=GUA1Stage.CROSS_DOMAIN_SUITE,
            passed=(
                evidence.cross_domain_suite.passed
                and evidence.cross_domain_suite.trace_ref == evidence.trace_ref
                and evidence.cross_domain_suite.contracts == evidence.realizations
            ),
            detail="cross-domain suite passed",
        ),
    )
    residuals_safe = not has_hidden and not has_blocking
    passed = all(check.passed for check in stage_checks) and residuals_safe
    final_check = StageCheck(
        stage=GUA1Stage.GUA1_PROOF_CERTIFICATE,
        passed=passed,
        detail=(
            "final GUA-1 certificate status is derived from all prior stages "
            "plus residual visibility and blocking safety"
        ),
    )
    all_checks = (*stage_checks, final_check)
    _require_exact_stage_coverage(all_checks)
    return (GUA1Status.PASS if passed else GUA1Status.FAIL, all_checks)


def _require_exact_stage_coverage(checks: tuple[StageCheck, ...]) -> None:
    expected_stages = frozenset(GUA1Stage)
    actual_stages = [check.stage for check in checks]
    if len(actual_stages) != len(expected_stages) or frozenset(actual_stages) != expected_stages:
        raise GuaCoreSchemaError(
            "GUA1ProofCertificate.checks must cover each GUA1Stage exactly once"
        )


def _compute_validated_residual_flags(residuals: ResidualSet) -> tuple[bool, bool]:
    if type(residuals) is not ResidualSet:
        raise GuaCoreSchemaError("residuals must be concrete ResidualSet")
    has_hidden = False
    has_blocking = False
    for item in residuals.items:
        if type(item) is not Residual:
            raise GuaCoreSchemaError("residuals.items entries must be concrete Residual")
        if not isinstance(item.visible, bool):
            raise GuaCoreSchemaError("residuals.items.visible must be bool")
        has_hidden = has_hidden or not item.visible
        has_blocking = has_blocking or item.kind is ResidualKind.BLOCKING
    return has_hidden, has_blocking
