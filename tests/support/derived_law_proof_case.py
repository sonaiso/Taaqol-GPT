"""Derived-law reconstruction proof schema for V0.229 tests.

This module provides a test-side constitutional template for
``docs/109_V0_229_META_CORE_RECONSTRUCTION_DERIVED_LAW_RECOVERY_LAW.md``.
The schema is intentionally strict: a derived-law proof object is not
accepted if any required field is missing or empty.
"""

from __future__ import annotations

from dataclasses import dataclass


class DerivedLawProofSchemaError(AssertionError):
    """Raised when a derived-law proof case/result violates schema."""


@dataclass(frozen=True)
class DerivedLawProofCase:
    """Declarative test-side representation of `DLP_X`."""

    concept_name: str
    definition: str
    dependencies: tuple[str, ...]
    positive_witness: str
    countermodel: str
    trace: str
    equivalence_proof: str
    capability: str

    def __post_init__(self) -> None:
        if not isinstance(self.concept_name, str) or not self.concept_name.strip():
            raise DerivedLawProofSchemaError("concept_name must be a non-empty string")
        if not isinstance(self.definition, str) or not self.definition.strip():
            raise DerivedLawProofSchemaError("definition must be a non-empty string")
        if not isinstance(self.dependencies, tuple):
            raise DerivedLawProofSchemaError("dependencies must be a tuple of strings")
        for dep in self.dependencies:
            if not isinstance(dep, str) or not dep.strip():
                raise DerivedLawProofSchemaError(
                    "each dependency must be a non-empty string"
                )
        if not isinstance(self.positive_witness, str) or not self.positive_witness.strip():
            raise DerivedLawProofSchemaError(
                "positive_witness must be a non-empty string"
            )
        if not isinstance(self.countermodel, str) or not self.countermodel.strip():
            raise DerivedLawProofSchemaError("countermodel must be a non-empty string")
        if not isinstance(self.trace, str) or not self.trace.strip():
            raise DerivedLawProofSchemaError("trace must be a non-empty string")
        if not isinstance(self.equivalence_proof, str) or not self.equivalence_proof.strip():
            raise DerivedLawProofSchemaError(
                "equivalence_proof must be a non-empty string"
            )
        if not isinstance(self.capability, str) or not self.capability.strip():
            raise DerivedLawProofSchemaError("capability must be a non-empty string")


@dataclass(frozen=True)
class DerivedLawProofResult:
    """Observed result of decoding one concept from the reduced core."""

    concept_name: str
    decoded_equivalent: bool
    trace_present: bool
    lost_distinction: tuple[str, ...]
    regression_positive_preserved: bool
    regression_negative_preserved: bool
    regression_residual_preserved: bool
    hidden_reintroduction_detected: bool

    def __post_init__(self) -> None:
        if not isinstance(self.concept_name, str) or not self.concept_name.strip():
            raise DerivedLawProofSchemaError("concept_name must be a non-empty string")
        if not isinstance(self.decoded_equivalent, bool):
            raise DerivedLawProofSchemaError("decoded_equivalent must be a bool")
        if not isinstance(self.trace_present, bool):
            raise DerivedLawProofSchemaError("trace_present must be a bool")
        if not isinstance(self.lost_distinction, tuple):
            raise DerivedLawProofSchemaError(
                "lost_distinction must be a tuple of strings"
            )
        for item in self.lost_distinction:
            if not isinstance(item, str) or not item.strip():
                raise DerivedLawProofSchemaError(
                    "lost_distinction items must be non-empty strings"
                )
        if not isinstance(self.regression_positive_preserved, bool):
            raise DerivedLawProofSchemaError(
                "regression_positive_preserved must be a bool"
            )
        if not isinstance(self.regression_negative_preserved, bool):
            raise DerivedLawProofSchemaError(
                "regression_negative_preserved must be a bool"
            )
        if not isinstance(self.regression_residual_preserved, bool):
            raise DerivedLawProofSchemaError(
                "regression_residual_preserved must be a bool"
            )
        if not isinstance(self.hidden_reintroduction_detected, bool):
            raise DerivedLawProofSchemaError(
                "hidden_reintroduction_detected must be a bool"
            )


def assert_derived_law_proof_case(
    case: DerivedLawProofCase, result: DerivedLawProofResult
) -> None:
    """Assert V0.229 derived-law recovery conditions for one concept."""

    if not isinstance(case, DerivedLawProofCase):
        raise DerivedLawProofSchemaError(
            "assert_derived_law_proof_case requires a DerivedLawProofCase"
        )
    if not isinstance(result, DerivedLawProofResult):
        raise DerivedLawProofSchemaError(
            "assert_derived_law_proof_case requires a DerivedLawProofResult"
        )
    if result.concept_name != case.concept_name:
        raise AssertionError(
            f"concept mismatch: case={case.concept_name} result={result.concept_name}"
        )
    if not result.decoded_equivalent:
        raise AssertionError(
            f"[{case.concept_name}] decode-equivalence (~=_C) was not preserved"
        )
    if not result.trace_present:
        raise AssertionError(f"[{case.concept_name}] trace evidence is required")
    if result.hidden_reintroduction_detected:
        raise AssertionError(
            f"[{case.concept_name}] hidden primitive reintroduction is forbidden"
        )
    if result.lost_distinction:
        raise AssertionError(
            f"[{case.concept_name}] lost distinction requires local reopening: "
            f"{result.lost_distinction}"
        )
    if not result.regression_positive_preserved:
        raise AssertionError(f"[{case.concept_name}] positive regression not preserved")
    if not result.regression_negative_preserved:
        raise AssertionError(f"[{case.concept_name}] negative regression not preserved")
    if not result.regression_residual_preserved:
        raise AssertionError(f"[{case.concept_name}] residual regression not preserved")


__all__ = [
    "DerivedLawProofCase",
    "DerivedLawProofResult",
    "DerivedLawProofSchemaError",
    "assert_derived_law_proof_case",
]
