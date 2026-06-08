"""PR-2 kernel surface.

PR-1A shipped the carrier enums and the constitutional documents.
PR-1B/PR-1C ratified the test-side and pre-SlotGraph laws (docs 12,
13, 14, 15, 16, 17). **PR-2** ships the minimum executable kernel
that those documents bind:

* :class:`SlotGraph` — the constitutional mathematical object
  (docs/11 §1, §11).
* :func:`gamma` — the pure ordered verdict function (docs/03 +
  docs/11 §7).
* :class:`GammaResult` + :class:`TraceEntryCandidate` — the
  immutable value pair every closure verdict produces.
* :class:`TraceLedger` — the minimum in-memory ledger the caller
  uses to record what ``Γ`` proposes (docs/07).

Nothing else moves in PR-2: ``RankLattice``, ``ResidualPolicy``
engine, ``TransitionGate``, the Forbidden Straight-Line Registry,
``AnswerAudit``, lexicons, Arabic linguistic code, and LLM adapters
are all reserved for later PRs as the
``docs/14_PR_CHAIN_ROADMAP.md`` chain prescribes.
"""

from taaqqul_slot_geometry.core import (
    ClosureState,
    FailureCode,
    Rank,
    Residual,
    ResidualKind,
)
from taaqqul_slot_geometry.core.gamma import GammaResult, gamma
from taaqqul_slot_geometry.core.slot_graph import (
    Center,
    EntryBoundary,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceRef,
)
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate, TraceLedger

__all__: list[str] = [
    # PR-1A carriers
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
    # PR-2 SlotGraph carriers
    "Center",
    "EntryBoundary",
    "GenerationSource",
    "Layer",
    "OpeningPolicy",
    "OutputBoundary",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotGraphSchemaError",
    "SlotState",
    "TraceRef",
    # PR-2 trace ledger carriers
    "TraceEntryCandidate",
    "TraceLedger",
    # PR-2 verdict function
    "GammaResult",
    "gamma",
]
