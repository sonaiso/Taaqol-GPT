"""Conformance smoke tests for the PR-1 carrier surface.

PR-1 ships the Mathematical Slot Geometry Constitution (docs) plus a
minimum set of carrier enums those docs reference. The executable
``SlotGraph`` and ``gamma`` land in PR-2; they are deliberately
absent from the public surface here.
"""

from __future__ import annotations

import importlib

_PR1_CARRIERS = {
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
}


def test_package_exposes_only_pr1_carriers() -> None:
    module = importlib.import_module("taaqqul_slot_geometry")
    assert set(module.__all__) == _PR1_CARRIERS
    for name in _PR1_CARRIERS:
        assert hasattr(module, name), f"missing carrier export: {name}"


def test_executable_kernel_not_yet_shipped() -> None:
    """PR-1 must not ship SlotGraph, gamma, TraceLedger or a transition gate.

    These names are reserved for PR-2 and later. If a future change
    ships them prematurely, this guard fails and forces the
    constitution to be updated first.
    """

    module = importlib.import_module("taaqqul_slot_geometry")
    for forbidden in ("SlotGraph", "Slot", "gamma", "TraceLedger", "TransitionGate"):
        assert not hasattr(module, forbidden), (
            f"{forbidden!r} is reserved for PR-2+; do not ship from PR-1"
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
