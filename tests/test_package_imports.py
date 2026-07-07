"""Conformance smoke tests for the PR-6 public surface.

PR-1A shipped the carrier enums (``ClosureState``, ``FailureCode``,
``Rank``, ``Residual``, ``ResidualKind``). PR-2 shipped the minimum
executable kernel that the constitution binds: ``SlotGraph`` +
``Slot`` family, ``gamma`` + ``GammaResult``, ``TraceEntryCandidate``
+ ``TraceLedger``. PR-3 shipped the rank / residual / evidence
contracts: ``RankLattice`` (bounded meet/join), ``ResidualPolicy`` +
``ResidualEvaluation`` (visibility + rank ceiling), and
``EvidenceContract`` + ``EvidenceSource`` carriers. PR-4 shipped the
gate those contracts feed: ``TransitionGate`` + ``TransitionVerdict``
+ ``TransitionState`` and the two gate ceilings. PR-5 shipped the
typed Forbidden Straight-Line Registry the gate consults. PR-6 ships
the audit layer around that kernel: the ``ModelClient`` protocol
(docs/01 — protocol only, no adapters), the pure ``emit_successor``
emission half (docs/17 §1, source 3), and the ``AnswerAudit`` +
``AuditedAnswer`` impure shell that owns the ledger (docs/07). The
``CertificationGate`` (and every other ``required_bridge`` the
registry names) is still reserved for later PRs in the
``docs/14_PR_CHAIN_ROADMAP.md`` chain. PR-8 ships the first concrete
adapter behind the docs/18 Adapter Boundary Law: the
``ConcreteAdapterCandidate`` + ``AdapterGuard`` admission surface,
its named surface registries, and the in-memory
``InMemoryModelClient`` transport. PR-10 ships the weight +
pre-weight carrier surface behind the docs/19 and docs/20 laws:
the docs/20 §16 pre-weight chain carriers and the docs/19 §9
weight-image carriers — carriers only, no ``weigh()``, no ``μ``
operation, no path gate.
"""

from __future__ import annotations

import importlib

# Carriers ratified in PR-1A.
_PR1_CARRIERS = {
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
}

# Executable kernel that lands in PR-2.
_PR2_KERNEL = {
    "Center",
    "EntryBoundary",
    "GammaResult",
    "GenerationSource",
    "Layer",
    "OpeningPolicy",
    "OutputBoundary",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotGraphSchemaError",
    "SlotState",
    "TraceEntryCandidate",
    "TraceLedger",
    "TraceRef",
    "gamma",
}

# PR-2A hardening — named construction surface (docs/17 §5 totality).
_PR2A_CONSTRUCTION_SURFACE = {
    "ConstructionResult",
}

# Rank / residual / evidence contracts that land in PR-3.
_PR3_SURFACE = {
    "EvidenceContract",
    "EvidenceSource",
    "PERFORATING_KINDS",
    "RankLattice",
    "ResidualEvaluation",
    "ResidualPolicy",
    "SINGLE_SOURCE_EVIDENCE_CEILING",
}

# Transition gate surface that lands in PR-4.
_PR4_SURFACE = {
    "GATE_RANK_CEILING",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    "UNGATED_RANK_CEILING",
}

# Forbidden Straight-Line Registry surface that lands in PR-5.
_PR5_SURFACE = {
    "CANONICAL_REGISTRY",
    "FORBIDDEN_STRAIGHT_LINES",
    "ForbiddenLine",
    "ForbiddenLineRegistry",
    "TERMINOLOGY_TRANSFERS",
    "TerminologyTransfer",
    "is_forbidden_direct",
}

# Audit layer surface that lands in PR-6.
_PR6_SURFACE = {
    "AnswerAudit",
    "AuditedAnswer",
    "ModelClient",
    "emit_successor",
}

# Adapter boundary surface that lands in PR-8 (behind docs/18).
_PR8_SURFACE = {
    "AdapterAdmission",
    "AdapterGuard",
    "CONFIDENCE_SURFACE_NAMES",
    "ConcreteAdapterCandidate",
    "InMemoryModelClient",
    "LEDGER_SURFACE_NAMES",
    "RANK_SURFACE_NAMES",
    "SUCCESSOR_SURFACE_NAMES",
    "TransportSurface",
    "VERDICT_SURFACE_NAMES",
}

# Weight + pre-weight carrier surface that lands in PR-10 (behind
# docs/19 and docs/20). ``WeightCarrierBase`` and
# ``BIRTH_RANK_CEILING`` stay subpackage-level on purpose: the base
# is deliberately not a reserved name (docs/19 §9, docs/20 §16).
_PR10_SURFACE = {
    "LetterStanding",
    "MawzunCandidate",
    "Mizan",
    "OperationTraceCandidate",
    "OriginalExtraMap",
    "PATTERN_SPACE",
    "PathCandidate",
    "PathKind",
    "PreWeightSurface",
    "RootStemCandidate",
    "SlotAlignment",
    "SyllableCandidate",
    "SyllableSequenceCandidate",
    "WeightCarrierSchemaError",
    "WeightImage",
    "WeightReadinessCandidate",
    "WordBoundaryCandidate",
    "WordCarrierCandidate",
}

# PR-22-AUDIT: Vertical Chain AnswerAudit Bridge surface.
_PR22_AUDIT_SURFACE = {
    "AuditBridgeState",
    "AuditedTanzilBridge",
    "AuditedTanzilBridgeVerdict",
    "bridge_tanzil_to_audit",
}

# G0-C1 bare-stem carrier surface.
_G0_C1_SURFACE = {
    "AnchorCertificate",
    "BareJamidStemCandidate",
    "EntityRank",
    "EpistemicRank",
    "G0C1CarrierSchemaError",
    "LexicalTruthStatus",
    "OntologicalClass",
    "StemGender",
}

# G0-C2 hard-blocker gate surface.
_G0_C2_SURFACE = {
    "G0C2GateSchemaError",
    "G0HardBlocker",
    "G0HardBlockerGateResult",
    "G0HardBlockerGateState",
    "G0HardBlockerResidual",
    "G0HardBlockerResidualKind",
    "G0_C2_ALLOWED_OUTPUT",
    "G0_C2_FORBIDDEN_OUTPUTS",
    "G0_C2_RANK_CEILING",
    "prove_g0_hard_blocker_gates",
}

# G0-C3 bounded epistemic distance surface.
_G0_C3_SURFACE = {
    "G0BoundedDistanceResult",
    "G0C3DistanceSchemaError",
    "G0DistanceBand",
    "G0DistanceResidual",
    "G0DistanceResidualKind",
    "G0_C3_ALLOWED_OUTPUT",
    "G0_C3_FORBIDDEN_OUTPUTS",
    "G0_C3_RANK_CEILING",
    "compute_g0_bounded_epistemic_distance",
}


def test_package_exposes_pr1_through_pr10_surface() -> None:
    module = importlib.import_module("taaqqul_slot_geometry")
    expected = (
        _PR1_CARRIERS
        | _PR2_KERNEL
        | _PR2A_CONSTRUCTION_SURFACE
        | _PR3_SURFACE
        | _PR4_SURFACE
        | _PR5_SURFACE
        | _PR6_SURFACE
        | _PR8_SURFACE
        | _PR10_SURFACE
        | _PR22_AUDIT_SURFACE
        | _G0_C1_SURFACE
        | _G0_C2_SURFACE
        | _G0_C3_SURFACE
    )
    assert set(module.__all__) == expected
    for name in expected:
        assert hasattr(module, name), f"missing export: {name}"


def test_post_pr10_symbols_still_reserved() -> None:
    """``CertificationGate``, ``weigh`` and friends stay reserved.

    PR-10 ships carriers only. ``weigh()`` and
    ``WeightFitCandidate`` belong to PR-13, the path gates to PR-11,
    the ``μ`` chain operations to PR-12, and the pattern tables /
    lexica to PR-14; the ``CertificationGate`` belongs to a
    dedicated future PR. Shipping any of them now would be a
    ``FORBIDDEN_LEAP`` under ``docs/14_PR_CHAIN_ROADMAP.md``
    regardless of CI status.
    """

    module = importlib.import_module("taaqqul_slot_geometry")
    for forbidden in ("CertificationGate", "weigh", "WeightFitCandidate"):
        assert not hasattr(module, forbidden), (
            f"{forbidden!r} is reserved for a later PR; do not ship from PR-10"
        )


def test_closure_state_has_the_six_constitutional_verdicts() -> None:
    from taaqqul_slot_geometry import ClosureState

    assert {s.value for s in ClosureState} == {
        "OPEN",
        "MINIMALLY_CLOSED",
        "PERFORATED_CLOSED",
        "BLOCKED",
        "INVALID",
        "FORBIDDEN_LEAP",
    }


def test_rank_is_totally_ordered_from_zero_to_certificate() -> None:
    from taaqqul_slot_geometry import Rank

    expected = [
        "ZERO",
        "TRACE",
        "CANDIDATE",
        "HYPOTHESIS",
        "LICENSED",
        "STRONG",
        "CERTIFICATE",
    ]
    assert [r.name for r in sorted(Rank)] == expected


def test_residual_kinds_match_the_constitution() -> None:
    from taaqqul_slot_geometry import ResidualKind

    assert {k.value for k in ResidualKind} == {
        "BLOCKING",
        "DEFERRABLE",
        "NON_BLOCKING",
        "EXPLANATORY",
        "HIDDEN_FORBIDDEN",
    }


def test_failure_codes_cover_every_constitutional_refusal_name() -> None:
    from taaqqul_slot_geometry import FailureCode

    # The constitution (docs 02, 03, 04, 05, 06, 08, 11) names these
    # refusals; PR-1 reserves the names even though their emit sites
    # land in PR-2 and later.
    required = {
        "IDENTITY_BROKEN",
        "CENTER_MISSING",
        "BOUNDARY_MISSING",
        "DOMAIN_MISSING",
        "SCOPE_MISSING",
        "TRACE_MISSING",
        "REQUIRED_SLOT_EMPTY",
        "UNLICENSED_OPENING",
        "OUTPUT_EXCEEDS_LAYER",
        "HIDDEN_RESIDUAL",
        "BLOCKING_RESIDUAL_PRESENT",
        "RANK_PROMOTION_WITHOUT_GATE",
        "RANK_EXCEEDS_CEILING",
        "FORBIDDEN_STRAIGHT_LINE",
        "GATE_REQUIRED",
    }
    assert required.issubset({f.value for f in FailureCode})
