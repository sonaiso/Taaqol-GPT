"""PR-5 kernel surface.

PR-1A shipped the carrier enums and the constitutional documents.
PR-1B/PR-1C ratified the test-side and pre-SlotGraph laws (docs 12,
13, 14, 15, 16, 17). PR-2/PR-2A shipped and hardened the minimum
executable kernel:

* :class:`SlotGraph` — the constitutional mathematical object
  (docs/11 §1, §11).
* :func:`gamma` — the pure ordered verdict function (docs/03 +
  docs/11 §7).
* :class:`GammaResult` + :class:`TraceEntryCandidate` — the
  immutable value pair every closure verdict produces.
* :class:`TraceLedger` — the minimum in-memory ledger the caller
  uses to record what ``Γ`` proposes (docs/07).

**PR-3** bound the rank / residual / evidence laws those documents
reserve:

* :class:`RankLattice` — bounded ``meet`` / ``join`` over
  :class:`Rank` (docs/05 + docs/11 §8); no promotion lives here.
* :class:`ResidualPolicy` + :class:`ResidualEvaluation` — the
  visibility engine and the residual rank ceiling consumed by ``Γ``
  step 9 (docs/06 + docs/11 §9).
* :class:`EvidenceContract` + :class:`EvidenceSource` — the evidence
  carriers whose ``evidence_rank`` the transition gate enters into
  the §8 meet (docs/08).

**PR-4** bound the gate those three components feed:

* :class:`TransitionGate` — the only legal cross-layer move
  (docs/08 + docs/11 §8, §10, §11). Its ordered ``decide`` consults
  ``Γ`` first, grants ranks only through the bounded lattice
  ``meet``, and names every refusal with a :class:`FailureCode` —
  binding the reserved ``FORBIDDEN_STRAIGHT_LINE``,
  ``RANK_PROMOTION_WITHOUT_GATE``, and ``GATE_REQUIRED`` codes.
* :class:`TransitionVerdict` + :class:`TransitionState` — the
  immutable verdict value and its five-state vocabulary (docs/08).

**PR-5** binds the registry the gate consults:

* :class:`ForbiddenLineRegistry` + :data:`CANONICAL_REGISTRY` — the
  typed Forbidden Straight-Line Registry (docs/04 + docs/16 §4):
  every canonical row, every pre-text declared-entry row, and the
  six chain lines, each with its named ``required_bridge`` and
  :class:`FailureCode`, queried through the docs/04 contract
  :func:`is_forbidden_direct`. ``TransitionGate.decide`` step 2 now
  consults this registry, so every registered line is fatal before
  any retryable refusal.
* :class:`ForbiddenLine` + :class:`TerminologyTransfer` — the two
  deliberately distinct row carriers; the latter holds the docs/10
  technical-terminology non-confusion cases (``cause`` / ``sabab``
  / ``ʿillah``, ``qiyās``) behind their own query surface so the
  two laws never collapse into one mechanism.

Nothing else moves in PR-5: the ``CertificationGate`` and every
other ``required_bridge`` the rows name, ``AnswerAudit``, lexicons,
Arabic linguistic code, and LLM adapters are all reserved for later
PRs as the ``docs/14_PR_CHAIN_ROADMAP.md`` chain prescribes. PR-5
names forbidden lines but opens no bridge: ``CERTIFICATE`` remains
structurally ungrantable through the generic gate.
"""

from taaqqul_slot_geometry.core import (
    ClosureState,
    FailureCode,
    Rank,
    Residual,
    ResidualKind,
)
from taaqqul_slot_geometry.core.evidence_contract import (
    SINGLE_SOURCE_EVIDENCE_CEILING,
    EvidenceContract,
    EvidenceSource,
)
from taaqqul_slot_geometry.core.forbidden_lines import (
    CANONICAL_REGISTRY,
    FORBIDDEN_STRAIGHT_LINES,
    TERMINOLOGY_TRANSFERS,
    ForbiddenLine,
    ForbiddenLineRegistry,
    TerminologyTransfer,
    is_forbidden_direct,
)
from taaqqul_slot_geometry.core.gamma import GammaResult, gamma
from taaqqul_slot_geometry.core.rank_lattice import RankLattice
from taaqqul_slot_geometry.core.residual_policy import (
    PERFORATING_KINDS,
    ResidualEvaluation,
    ResidualPolicy,
)
from taaqqul_slot_geometry.core.slot_graph import (
    Center,
    ConstructionResult,
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
from taaqqul_slot_geometry.core.transition_gate import (
    GATE_RANK_CEILING,
    UNGATED_RANK_CEILING,
    TransitionGate,
    TransitionState,
    TransitionVerdict,
)

__all__: list[str] = [
    # PR-1A carriers
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
    # PR-2 SlotGraph carriers
    "Center",
    "ConstructionResult",
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
    # PR-3 rank lattice
    "RankLattice",
    # PR-3 residual policy engine
    "PERFORATING_KINDS",
    "ResidualEvaluation",
    "ResidualPolicy",
    # PR-3 evidence carriers
    "SINGLE_SOURCE_EVIDENCE_CEILING",
    "EvidenceContract",
    "EvidenceSource",
    # PR-4 transition gate
    "GATE_RANK_CEILING",
    "UNGATED_RANK_CEILING",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    # PR-5 forbidden straight-line registry
    "CANONICAL_REGISTRY",
    "FORBIDDEN_STRAIGHT_LINES",
    "TERMINOLOGY_TRANSFERS",
    "ForbiddenLine",
    "ForbiddenLineRegistry",
    "TerminologyTransfer",
    "is_forbidden_direct",
]
