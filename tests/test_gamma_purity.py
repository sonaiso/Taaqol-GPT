"""Purity guards for ``gamma`` (PR-1)."""

from __future__ import annotations

import importlib
from pathlib import Path

from taaqqul_slot_geometry import (
    Slot,
    SlotGraph,
    SlotState,
    gamma,
)

gamma_module = importlib.import_module("taaqqul_slot_geometry.core.gamma")


def test_gamma_module_does_not_import_or_use_trace_ledger() -> None:
    source = Path(gamma_module.__file__).read_text(encoding="utf-8")
    # Strip docstrings/comments by inspecting only non-comment, non-string code
    # lines for the two patterns that would prove impurity.
    code_lines = [
        line
        for line in source.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    code_only = "\n".join(code_lines)
    # gamma must never import the TraceLedger container.
    assert "import TraceLedger" not in code_only
    assert "from taaqqul_slot_geometry.core.trace_ledger import" not in code_only or (
        "TraceLedger" not in code_only.split(
            "from taaqqul_slot_geometry.core.trace_ledger import", 1
        )[1].splitlines()[0]
    ), "gamma.py must not import TraceLedger; the caller appends, not gamma."
    # And gamma must never call .append on anything.
    assert ".append(" not in code_only, (
        "gamma.py must not call .append(); it is a pure verdict function."
    )


def test_gamma_is_deterministic_for_the_same_input() -> None:
    graph = SlotGraph(
        center="entity",
        slots=(Slot(name="a", required=True, state=SlotState.FILLED),),
    )
    assert gamma(graph) == gamma(graph)
