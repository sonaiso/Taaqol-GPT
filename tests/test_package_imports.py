"""Conformance smoke tests for the PR-4 public surface.

PR-1A shipped the carrier enums (``ClosureState``, ``FailureCode``,
``Rank``, ``Residual``, ``ResidualKind``). PR-2 shipped the minimum
executable kernel that the constitution binds: ``SlotGraph`` +
``Slot`` family, ``gamma`` + ``GammaResult``, ``TraceEntryCandidate``
+ ``TraceLedger``. PR-3 shipped the rank / residual / evidence
contracts: ``RankLattice`` (bounded meet/join), ``ResidualPolicy`` +
``ResidualEvaluation`` (visibility + rank ceiling), and
``EvidenceContract`` + ``EvidenceSource`` carriers. PR-4 ships the
gate those contracts feed: ``TransitionGate`` + ``TransitionVerdict``
+ ``TransitionState`` and the two gate ceilings. The typed Forbidden
Straight-Line Registry, the ``CertificationGate``, and ``AnswerAudit``
are all still reserved for later PRs in the
``docs/14_PR_CHAIN_ROADMAP.md`` chain.
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


def test_package_exposes_pr1_through_pr4_surface() -> None:
    module = importlib.import_module("taaqqul_slot_geometry")
    expected = (
        _PR1_CARRIERS
        | _PR2_KERNEL
        | _PR2A_CONSTRUCTION_SURFACE
        | _PR3_SURFACE
        | _PR4_SURFACE
    )
    assert set(module.__all__) == expected
    for name in expected:
        assert hasattr(module, name), f"missing export: {name}"


def test_post_pr4_symbols_still_reserved() -> None:
    """The registry, ``CertificationGate``, and ``AnswerAudit`` stay reserved.

    They belong to PR-5 / PR-6; shipping them from PR-4 would be a
    ``FORBIDDEN_LEAP`` under ``docs/14_PR_CHAIN_ROADMAP.md``
    regardless of CI status.
    """

    module = importlib.import_module("taaqqul_slot_geometry")
    for forbidden in ("ForbiddenLineRegistry", "CertificationGate", "AnswerAudit"):
        assert not hasattr(module, forbidden), (
            f"{forbidden!r} is reserved for PR-5+; do not ship from PR-4"
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
