# Conformance smoke tests for the package surface.
#
# PR-0 shipped no behaviour; PR-1 lands the SlotGraph + Gamma kernel and
# re-exports its public surface from the top-level package.

import importlib

_PR1_EXPORTS = {
    "FailureCode",
    "GammaResult",
    "GammaState",
    "Layer",
    "Rank",
    "Residual",
    "ResidualKind",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotState",
    "TraceEntryCandidate",
    "TraceLedger",
    "gamma",
}


def test_package_imports() -> None:
    module = importlib.import_module("taaqqul_slot_geometry")
    assert set(module.__all__) == _PR1_EXPORTS
    for name in _PR1_EXPORTS:
        assert hasattr(module, name), f"missing export: {name}"
