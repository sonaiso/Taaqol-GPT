"""GUA-1 proof suites and final proof-certificate carrier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError
from taaqqul_slot_geometry.gua.core.geometry import CoreFreeze, GeneralCoreExtraction
from taaqqul_slot_geometry.gua.core.realization import RealizationContract
from taaqqul_slot_geometry.gua.core.residual import ResidualSet

_REQUIRED_REALIZATION_DOMAINS = frozenset(
    {"language", "mathematics", "physics", "programming"}
)


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

    extraction_is_typed: bool
    freeze_is_deterministic: bool
    legacy_core_untouched: bool
    trace_ref: str

    def __post_init__(self) -> None:
        _require_bool(self.__class__.__name__, "extraction_is_typed", self.extraction_is_typed)
        _require_bool(
            self.__class__.__name__,
            "freeze_is_deterministic",
            self.freeze_is_deterministic,
        )
        _require_bool(self.__class__.__name__, "legacy_core_untouched", self.legacy_core_untouched)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)

    @property
    def passed(self) -> bool:
        return (
            self.extraction_is_typed
            and self.freeze_is_deterministic
            and self.legacy_core_untouched
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
        return all(contract.trace_ref == self.trace_ref for contract in self.contracts)


@dataclass(frozen=True, slots=True)
class GUA1ProofCertificate:
    """Final non-partial proof artifact for GUA-1."""

    status: GUA1Status
    checks: tuple[StageCheck, ...]
    residuals: ResidualSet
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.status, GUA1Status):
            raise GuaCoreSchemaError("GUA1ProofCertificate.status must be GUA1Status")
        if not isinstance(self.checks, tuple) or not self.checks:
            raise GuaCoreSchemaError("GUA1ProofCertificate.checks must be a non-empty tuple")
        for check in self.checks:
            if not isinstance(check, StageCheck):
                raise GuaCoreSchemaError("GUA1ProofCertificate.checks entries must be StageCheck")
        if not isinstance(self.residuals, ResidualSet):
            raise GuaCoreSchemaError("GUA1ProofCertificate.residuals must be ResidualSet")
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


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

    if not isinstance(extraction, GeneralCoreExtraction):
        raise GuaCoreSchemaError("issue_gua1_proof_certificate expects GeneralCoreExtraction")
    if not isinstance(core_freeze, CoreFreeze):
        raise GuaCoreSchemaError("issue_gua1_proof_certificate expects CoreFreeze")
    if not isinstance(realizations, tuple) or not realizations:
        raise GuaCoreSchemaError(
            "issue_gua1_proof_certificate expects non-empty realizations tuple"
        )
    if not isinstance(shared_suite, SharedConstitutionalSuite):
        raise GuaCoreSchemaError("issue_gua1_proof_certificate expects SharedConstitutionalSuite")
    if not isinstance(cross_domain_suite, CrossDomainSuite):
        raise GuaCoreSchemaError("issue_gua1_proof_certificate expects CrossDomainSuite")
    _require_str("issue_gua1_proof_certificate", "trace_ref", trace_ref)

    stage_checks = (
        StageCheck(
            stage=GUA1Stage.GENERAL_CORE_EXTRACTION,
            passed=bool(extraction.geometry.slots and extraction.transitions),
            detail="general core extraction is structurally complete",
        ),
        StageCheck(
            stage=GUA1Stage.CORE_FREEZE,
            passed=core_freeze.trace_ref == trace_ref and bool(core_freeze.extraction_hash),
            detail="core freeze is present and trace-bound",
        ),
        StageCheck(
            stage=GUA1Stage.REALIZATIONS,
            passed=len(realizations) == 4,
            detail="four realization contracts are present",
        ),
        StageCheck(
            stage=GUA1Stage.SHARED_CONSTITUTIONAL_SUITE,
            passed=shared_suite.passed and shared_suite.trace_ref == trace_ref,
            detail="shared constitutional suite passed",
        ),
        StageCheck(
            stage=GUA1Stage.CROSS_DOMAIN_SUITE,
            passed=cross_domain_suite.passed and cross_domain_suite.trace_ref == trace_ref,
            detail="cross-domain suite passed",
        ),
    )
    passed = all(check.passed for check in stage_checks)
    final_check = StageCheck(
        stage=GUA1Stage.GUA1_PROOF_CERTIFICATE,
        passed=passed,
        detail="final GUA-1 certificate status is derived from all prior stages",
    )
    all_checks = (*stage_checks, final_check)
    return GUA1ProofCertificate(
        status=GUA1Status.PASS if passed else GUA1Status.FAIL,
        checks=all_checks,
        residuals=residuals if residuals is not None else ResidualSet(),
        trace_ref=trace_ref,
    )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_bool(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be bool")
