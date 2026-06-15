"""Constitutional Vertical Chain Test Case schema and assertion helper.

This module is the executable form of
``docs/46_VERTICAL_PATH_CLOSURE_LAW.md``. It defines:

* :class:`ConstitutionalVerticalChainTestCase` — the frozen schema
  for vertical-chain closure tests. Every test that exercises the
  minimum vertical path (MufradDalalahClosure → ... →
  AuditedTanzilBridge) must declare itself through this class.

* :func:`assert_vertical_chain_case` — the helper that compares a
  vertical-chain result against a declared case and refuses partial
  passes.

The vertical chain is:

    MufradDalalahClosure
    → RelationClosure
    → IfadahCandidate
    → HukmCandidate
    → ManatCandidate
    → TanzilCandidate
    → AuditedTanzilBridge

Every step must prove: PROVEN verdict, bounded rank, EXPLANATORY
residual visibility, present trace_ref, named FailureCode on every
refusal, and absence of forbidden horizontal-branch symbols.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainTestCase,
    ConstitutionalSchemaError,
)

# The ordered layers in the minimum vertical path.
VERTICAL_CHAIN_LAYERS: tuple[str, ...] = (
    "MufradDalalahClosure",
    "RelationClosure",
    "IfadahCandidate",
    "HukmCandidate",
    "ManatCandidate",
    "TanzilCandidate",
    "AuditedTanzilBridge",
)

# Closure states accepted as vertical closure.
_CLOSURE_STATES: frozenset[ClosureState] = frozenset(
    {ClosureState.MINIMALLY_CLOSED, ClosureState.PERFORATED_CLOSED}
)

# Forbidden horizontal-branch symbols that must never appear.
FORBIDDEN_HORIZONTAL_SYMBOLS: tuple[str, ...] = (
    "Majaz",
    "MajazVerdict",
    "MajazLicense",
    "Mantuq",
    "MantuqClosure",
    "Mafhum",
    "MafhumCandidate",
    "Naql",
    "ManqulVerdict",
    "ManqulLicense",
    "ReferenceExpansion",
    "ArabicConditionsDAG",
    "GPTProposer",
    "T5Proposer",
    "GovernmentServiceEngine",
)

# Forbidden certificate/execution symbols.
FORBIDDEN_CERTIFICATE_SYMBOLS: tuple[str, ...] = (
    "Certificate",
    "FinalCertificate",
    "Execution",
    "ExternalAction",
    "Enforcement",
    "Fatwa",
    "Qada",
    "FinalAuthority",
    "DivineAuthorityClaim",
    "RealityApplication",
    "RealityVerification",
    "FinalMeaning",
    "Meaning",
    "OntologicalClaim",
    "PropositionTruthValue",
    "FreeReasoning",
    "AuthorityClaim",
    "NormativeJudgment",
)


@dataclass(frozen=True)
class VerticalChainStepResult:
    """Observed result at one step of the vertical chain.

    Each step in the vertical walk produces one of these.
    """

    layer: str
    verdict_proven: bool
    rank: Rank
    residuals_visible: bool
    trace_ref_present: bool
    failure_code: FailureCode | None
    produced_outputs: frozenset[str]

    def __post_init__(self) -> None:
        if not isinstance(self.layer, str) or not self.layer.strip():
            raise ConstitutionalSchemaError(
                "VerticalChainStepResult.layer must be a non-empty string"
            )
        if not isinstance(self.rank, Rank):
            raise ConstitutionalSchemaError(
                "VerticalChainStepResult.rank must be a Rank member"
            )
        if not isinstance(self.residuals_visible, bool):
            raise ConstitutionalSchemaError(
                "VerticalChainStepResult.residuals_visible must be a bool"
            )
        if not isinstance(self.trace_ref_present, bool):
            raise ConstitutionalSchemaError(
                "VerticalChainStepResult.trace_ref_present must be a bool"
            )
        if not isinstance(self.produced_outputs, frozenset):
            raise ConstitutionalSchemaError(
                "VerticalChainStepResult.produced_outputs must be a frozenset"
            )


@dataclass(frozen=True)
class VerticalChainResult:
    """Observed result of walking the full vertical chain.

    Contains one VerticalChainStepResult per layer, plus aggregate
    properties for the full walk.
    """

    steps: tuple[VerticalChainStepResult, ...]
    trace_continuous: bool
    rank_monotone: bool
    envelope_preserved: bool
    all_produced_outputs: frozenset[str]

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple):
            raise ConstitutionalSchemaError(
                "VerticalChainResult.steps must be a tuple"
            )
        if len(self.steps) == 0:
            raise ConstitutionalSchemaError(
                "VerticalChainResult.steps must contain at least one step"
            )
        if not isinstance(self.trace_continuous, bool):
            raise ConstitutionalSchemaError(
                "VerticalChainResult.trace_continuous must be a bool"
            )
        if not isinstance(self.rank_monotone, bool):
            raise ConstitutionalSchemaError(
                "VerticalChainResult.rank_monotone must be a bool"
            )
        if not isinstance(self.envelope_preserved, bool):
            raise ConstitutionalSchemaError(
                "VerticalChainResult.envelope_preserved must be a bool"
            )
        if not isinstance(self.all_produced_outputs, frozenset):
            raise ConstitutionalSchemaError(
                "VerticalChainResult.all_produced_outputs must be a frozenset"
            )


@dataclass(frozen=True)
class ConstitutionalVerticalChainTestCase(ConstitutionalChainTestCase):
    """Vertical-chain closure test case.

    Extends :class:`ConstitutionalChainTestCase` with vertical-path
    specific requirements:

    * ``vertical_layers``: the ordered layers this test walks (must
      be a subset of VERTICAL_CHAIN_LAYERS).
    * ``requires_trace_continuity``: True if the test asserts trace
      continuity across all layers.
    * ``requires_rank_monotonicity``: True if the test asserts rank
      never promotes.
    * ``requires_envelope_preservation``: True if the test asserts
      the presentation envelope survives through audit.
    * ``forbidden_horizontal_branches``: tuple of horizontal-branch
      symbols that must be absent.
    * ``forbidden_certificate_symbols``: tuple of certificate/execution
      symbols that must be absent.
    """

    vertical_layers: tuple[str, ...] = ()
    requires_trace_continuity: bool = True
    requires_rank_monotonicity: bool = True
    requires_envelope_preservation: bool = True
    forbidden_horizontal_branches: tuple[str, ...] = FORBIDDEN_HORIZONTAL_SYMBOLS
    forbidden_certificate_symbols: tuple[str, ...] = FORBIDDEN_CERTIFICATE_SYMBOLS

    def __post_init__(self) -> None:
        super().__post_init__()

        if not isinstance(self.vertical_layers, tuple):
            raise ConstitutionalSchemaError(
                "vertical_layers must be a tuple of layer names"
            )
        if len(self.vertical_layers) == 0:
            raise ConstitutionalSchemaError(
                "vertical_layers must contain at least one layer"
            )
        for layer in self.vertical_layers:
            if not isinstance(layer, str) or not layer.strip():
                raise ConstitutionalSchemaError(
                    "every vertical_layers entry must be a non-empty string"
                )
            if layer not in VERTICAL_CHAIN_LAYERS:
                raise ConstitutionalSchemaError(
                    f"vertical_layers entry '{layer}' is not in "
                    f"VERTICAL_CHAIN_LAYERS"
                )

        if not isinstance(self.requires_trace_continuity, bool):
            raise ConstitutionalSchemaError(
                "requires_trace_continuity must be a bool"
            )
        if not isinstance(self.requires_rank_monotonicity, bool):
            raise ConstitutionalSchemaError(
                "requires_rank_monotonicity must be a bool"
            )
        if not isinstance(self.requires_envelope_preservation, bool):
            raise ConstitutionalSchemaError(
                "requires_envelope_preservation must be a bool"
            )

        if not isinstance(self.forbidden_horizontal_branches, tuple):
            raise ConstitutionalSchemaError(
                "forbidden_horizontal_branches must be a tuple"
            )
        if not isinstance(self.forbidden_certificate_symbols, tuple):
            raise ConstitutionalSchemaError(
                "forbidden_certificate_symbols must be a tuple"
            )


def assert_vertical_chain_case(
    case: ConstitutionalVerticalChainTestCase,
    result: VerticalChainResult,
) -> None:
    """Compare a vertical chain result against a declared case.

    Walks the assertion chain required by docs/46 §6 in order.
    The first violated step raises AssertionError with a message
    naming the law, the branch, and the violated step.
    """
    if not isinstance(case, ConstitutionalVerticalChainTestCase):
        raise ConstitutionalSchemaError(
            "assert_vertical_chain_case requires a "
            "ConstitutionalVerticalChainTestCase"
        )
    if not isinstance(result, VerticalChainResult):
        raise ConstitutionalSchemaError(
            "assert_vertical_chain_case requires a VerticalChainResult"
        )

    prefix = f"[{case.origin_law} / {case.branch_name}]"

    # --- 1. Trace continuity ---
    if case.requires_trace_continuity and not result.trace_continuous:
        raise AssertionError(
            f"{prefix} trace continuity was required but not observed"
        )

    # --- 2. Rank monotonicity ---
    if case.requires_rank_monotonicity and not result.rank_monotone:
        raise AssertionError(
            f"{prefix} rank monotonicity was required but violated"
        )

    # --- 3. Envelope preservation ---
    if case.requires_envelope_preservation and not result.envelope_preserved:
        raise AssertionError(
            f"{prefix} presentation envelope preservation was required "
            "but violated"
        )

    # --- 4. Per-step checks ---
    for step in result.steps:
        step_prefix = f"{prefix} [{step.layer}]"

        # If the case expects closure, every step must be proven
        if case.expected_state in _CLOSURE_STATES:
            if not step.verdict_proven:
                raise AssertionError(
                    f"{step_prefix} expected PROVEN verdict but step was not"
                )
            if not step.residuals_visible:
                raise AssertionError(
                    f"{step_prefix} residual visibility required but not "
                    "observed"
                )
            if not step.trace_ref_present:
                raise AssertionError(
                    f"{step_prefix} trace_ref required but not present"
                )

    # --- 5. Rank ceiling ---
    for step in result.steps:
        if step.rank.value > case.max_rank.value:
            raise AssertionError(
                f"{prefix} [{step.layer}] rank {step.rank.name} exceeds "
                f"ceiling {case.max_rank.name}"
            )

    # --- 6. Forbidden horizontal branches ---
    horizontal_present = sorted(
        set(case.forbidden_horizontal_branches)
        & set(result.all_produced_outputs)
    )
    if horizontal_present:
        raise AssertionError(
            f"{prefix} forbidden horizontal branch symbols present: "
            f"{horizontal_present}"
        )

    # --- 7. Forbidden certificate symbols ---
    certificate_present = sorted(
        set(case.forbidden_certificate_symbols)
        & set(result.all_produced_outputs)
    )
    if certificate_present:
        raise AssertionError(
            f"{prefix} forbidden certificate/execution symbols present: "
            f"{certificate_present}"
        )


__all__: list[str] = [
    "VERTICAL_CHAIN_LAYERS",
    "FORBIDDEN_HORIZONTAL_SYMBOLS",
    "FORBIDDEN_CERTIFICATE_SYMBOLS",
    "VerticalChainStepResult",
    "VerticalChainResult",
    "ConstitutionalVerticalChainTestCase",
    "assert_vertical_chain_case",
]
