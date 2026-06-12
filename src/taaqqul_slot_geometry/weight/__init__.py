"""``taaqqul_slot_geometry.weight`` — the PR-10 carrier surface.

PR-10 binding of ``docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md`` (the
output boundary: weight maps into PatternSpace, not Meaning) and
``docs/20_PRE_WEIGHT_LICENSING_LAW.md`` (the input boundary: nothing
enters the Mīzān before a licensed ``WeightReadinessCandidate``),
staged by ``docs/14_PR_CHAIN_ROADMAP.md``. The package holds exactly
the reserved carriers of docs/19 §9 and docs/20 §16 — frozen
dataclasses, each carrying value, type, origin, identity, domain,
scope, rank, residuals, trace — and nothing more:

* the pre-weight chain carriers (docs/20 §§4–11) —
  :class:`SyllableCandidate`, :class:`SyllableSequenceCandidate`,
  :class:`WordBoundaryCandidate`, :class:`WordCarrierCandidate`,
  the :class:`PathKind` family with :class:`PathCandidate`,
  :class:`RootStemCandidate`, :class:`LetterStanding` with
  :class:`OriginalExtraMap`, :class:`OperationTraceCandidate`,
  :class:`PreWeightSurface`, :class:`WeightReadinessCandidate`;
* the weight-image carriers (docs/19 §9) — :class:`WeightImage`,
  :class:`Mizan`, :class:`MawzunCandidate`, :class:`SlotAlignment`.

No ``weigh()``, no alignment operation, no ``μ`` operation, no path
gate, no lexicon, and no meaning / agency / hukm / reality field
lives here (docs/14 — *PR-10 Forbidden*; docs/19 §6; docs/20 §13).
The weight branch never touches the adapter or audit layers; the
static guards in ``tests/test_weight_carriers.py`` prove the import
surface in both directions.
"""

from __future__ import annotations

from taaqqul_slot_geometry.weight.carrier_core import (
    BIRTH_RANK_CEILING,
    WeightCarrierBase,
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
    PathKind,
    PreWeightSurface,
    RootStemCandidate,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)
from taaqqul_slot_geometry.weight.weight_image import (
    PATTERN_SPACE,
    MawzunCandidate,
    Mizan,
    SlotAlignment,
    WeightImage,
)

__all__ = [
    "BIRTH_RANK_CEILING",
    "PATTERN_SPACE",
    "LetterStanding",
    "MawzunCandidate",
    "Mizan",
    "OperationTraceCandidate",
    "OriginalExtraMap",
    "PathCandidate",
    "PathKind",
    "PreWeightSurface",
    "RootStemCandidate",
    "SlotAlignment",
    "SyllableCandidate",
    "SyllableSequenceCandidate",
    "WeightCarrierBase",
    "WeightCarrierSchemaError",
    "WeightImage",
    "WeightReadinessCandidate",
    "WordBoundaryCandidate",
    "WordCarrierCandidate",
]
