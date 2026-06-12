"""Weight-image carriers — PR-10 binding of docs/19 (carriers only).

The Arabic Weight Boundary Law
(``docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md``) fixes the **output**
boundary of the Mīzān: weighing is imaging — *Form → Mīzān → image in
PatternSpace* — and PatternSpace contains no meaning, agency,
patienthood, hukm, reality, real event, or knowledge (docs/19 §2).
PR-10 ships only the four reserved carriers of docs/19 §9:

* :class:`WeightImage` — the image of a form in PatternSpace;
* :class:`Mizan` — the imaging instrument, carrying **no** pattern
  table (pattern inventories are PR-14 licensing surface);
* :class:`MawzunCandidate` — the thing-to-be-weighed, which exists
  only as a licensed :class:`WeightReadinessCandidate` (docs/20 §1);
* :class:`SlotAlignment` — a *depicted* alignment of mawzūn units to
  mīzān slots, never a computed one.

``weigh()`` and ``WeightFitCandidate`` are PR-13 surface (docs/19
§5, §9) and do not exist here: nothing in this module computes a
fit, scores an alignment, or maps anywhere but PatternSpace. A
landing space other than PatternSpace is the registered straight
line *Weight → Meaning* (docs/19 §4) and is refused at birth.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.weight.carrier_core import (
    WeightCarrierBase,
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.pre_weight import WeightReadinessCandidate

#: The only space a weight image may land in (docs/19 §2). The
#: constant exists so the law is written once and compared, never
#: retyped per carrier. A landing space other than PatternSpace is
#: the registered straight line *Weight → Meaning* (docs/19 §4) and
#: is refused at birth by every carrier below. The guard is inlined
#: per carrier on purpose: the only function definitions licensed in
#: the weight package are ``__post_init__`` birth guards (docs/14 —
#: *PR-10*: no operation), and the static tests prove it.
PATTERN_SPACE: str = "PatternSpace"


@dataclass(frozen=True, slots=True)
class WeightImage(WeightCarrierBase):
    """The image of a form in PatternSpace (docs/19 §2, §9).

    The depicted image itself travels in ``value``; the only
    structural field is the landing space, which may name nothing
    but PatternSpace. An image is not a meaning, not a hukm, and not
    knowledge (docs/19 §3).
    """

    landing_space: str = PATTERN_SPACE

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.landing_space, str) or self.landing_space != PATTERN_SPACE:
            raise WeightCarrierSchemaError(
                f"WeightImage.landing_space must be {PATTERN_SPACE!r} — weight "
                f"maps into PatternSpace, not Meaning "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )


@dataclass(frozen=True, slots=True)
class Mizan(WeightCarrierBase):
    """The imaging instrument (docs/19 §2, §9).

    The Mīzān maps a licensed mawzūn into PatternSpace and nowhere
    else. It deliberately carries **no pattern table**: pattern
    inventories, lexica, samāʿ and qiyās material enter only through
    the PR-14 licensing boundary (docs/19 §6).
    """

    landing_space: str = PATTERN_SPACE

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.landing_space, str) or self.landing_space != PATTERN_SPACE:
            raise WeightCarrierSchemaError(
                f"Mizan.landing_space must be {PATTERN_SPACE!r} — the Mizan "
                f"maps into PatternSpace, not Meaning "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )


@dataclass(frozen=True, slots=True)
class MawzunCandidate(WeightCarrierBase):
    """The thing-to-be-weighed (docs/19 §9; docs/20 §1).

    Nothing enters the Mīzān before it is a licensed
    :class:`WeightReadinessCandidate`: a mawzūn built on a raw word,
    a surface, a syllable, a root, or anything else is an unlicensed
    opening of the weighing space and is refused at birth.
    """

    readiness: WeightReadinessCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.readiness, WeightReadinessCandidate):
            raise WeightCarrierSchemaError(
                "MawzunCandidate.readiness must be a WeightReadinessCandidate — "
                f"nothing enters the Mizan before weight readiness "
                f"({FailureCode.UNLICENSED_OPENING.value})"
            )


@dataclass(frozen=True, slots=True)
class SlotAlignment(WeightCarrierBase):
    """A depicted alignment of mawzūn units to mīzān slots (docs/19 §9).

    PR-10 *depicts* an alignment as declared ``(mawzūn unit, mīzān
    slot)`` pairs; it never computes one — alignment **operations**
    are forbidden PR-10 surface (docs/14) and the fit they would
    feed is PR-13 surface (docs/19 §5: fit is not approval). An
    alignment with no pairs depicts nothing; a pair that loses
    either side breaks the alignment's identity.
    """

    mawzun: MawzunCandidate
    mizan: Mizan
    pairs: tuple[tuple[str, str], ...]
    landing_space: str = PATTERN_SPACE

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.mawzun, MawzunCandidate):
            raise WeightCarrierSchemaError(
                "SlotAlignment.mawzun must be a MawzunCandidate — no alignment "
                f"before a licensed mawzun ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.mizan, Mizan):
            raise WeightCarrierSchemaError(
                "SlotAlignment.mizan must be a Mizan — no alignment without "
                f"the instrument ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.pairs, tuple) or len(self.pairs) == 0:
            raise WeightCarrierSchemaError(
                "SlotAlignment.pairs must be a non-empty tuple of "
                f"(mawzun unit, mizan slot) pairs ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for pair in self.pairs:
            if (
                not isinstance(pair, tuple)
                or len(pair) != 2
                or not isinstance(pair[0], str)
                or not pair[0].strip()
                or not isinstance(pair[1], str)
                or not pair[1].strip()
            ):
                raise WeightCarrierSchemaError(
                    "SlotAlignment.pairs entries must be non-empty "
                    "(mawzun unit, mizan slot) string pairs "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )
        if not isinstance(self.landing_space, str) or self.landing_space != PATTERN_SPACE:
            raise WeightCarrierSchemaError(
                f"SlotAlignment.landing_space must be {PATTERN_SPACE!r} — the "
                f"alignment lands in PatternSpace, not Meaning "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )


__all__ = [
    "PATTERN_SPACE",
    "Mizan",
    "MawzunCandidate",
    "SlotAlignment",
    "WeightImage",
]
