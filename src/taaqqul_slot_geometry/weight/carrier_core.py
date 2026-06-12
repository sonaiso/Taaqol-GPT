"""Shared constitutional base of the PR-10 weight-branch carriers.

PR-10 binding of ``docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md`` and
``docs/20_PRE_WEIGHT_LICENSING_LAW.md`` under the docs/14 chain row
*PR-10 — Weight + pre-weight carrier surface*. That row licenses
**carriers only**: frozen dataclasses "each carrying value, type,
origin, identity, domain, scope, rank, residuals, trace" that depict
structure — no operation, no fit computation, no meaning field.

Two shared pieces live here so the nine-field law is stated once:

* :class:`WeightCarrierSchemaError` — raised when a carrier is
  malformed at birth. A schema error is a programmer mistake, not a
  constitutional verdict (mirroring ``SlotGraphSchemaError``), but
  every message still names the :class:`FailureCode` of the violated
  axis (docs/12 §4 — every rejection must be named).
* :class:`WeightCarrierBase` — the nine mandatory fields of the
  docs/14 PR-10 row with their birth guards, so no weight carrier
  can ever be a free data container (docs/11 carrier discipline;
  docs/19 §8 and docs/20 §15 anti-collapse rules).

``WeightCarrierBase`` is deliberately *not* a reserved name
(docs/19 §9, docs/20 §16) and is not exported at the package top
level; it exists so the nine-field law is written exactly once.

Rank discipline: no gate exists anywhere in the weight branch before
PR-11, and the gate is the only path that can promote a rank
(docs/11 §8), so no weight carrier may be *born* above
``Rank.CANDIDATE`` — a higher rank at birth would be a rank
promotion without a gate (docs/20 §11).
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual
from taaqqul_slot_geometry.core.slot_graph import TraceRef


class WeightCarrierSchemaError(TypeError):
    """A weight carrier was constructed with a malformed field.

    Raised at carrier birth (``__post_init__``), before any carrier
    can travel. The message always names the :class:`FailureCode` of
    the violated constitutional axis, so the refusal is never
    anonymous (docs/12 §4) — but it remains a Python schema error,
    not a constitutional verdict: no ``Γ`` or ``Ω`` judgment runs in
    PR-10 (the Ω judgment is reserved to PR-12 by docs/20 §11).
    """


#: The maximum rank any weight-branch carrier may hold at birth.
#: There is no gate in the weight branch before PR-11, and the gate
#: is the only path that can promote a rank (docs/11 §8), so every
#: PR-10 carrier is at most a candidate. The constant only *enters*
#: a comparison; it is never an output rank by itself.
BIRTH_RANK_CEILING: Rank = Rank.CANDIDATE


@dataclass(frozen=True, slots=True)
class WeightCarrierBase:
    """The nine mandatory fields of every PR-10 weight carrier.

    docs/14 — *PR-10*: "each carrying value, type, origin, identity,
    domain, scope, rank, residuals, trace". Every concrete carrier in
    :mod:`taaqqul_slot_geometry.weight` inherits these fields and
    this birth guard, then adds the structural fields its own law
    section names. Residual *visibility* is declared at birth and
    judged later (the Ω judgment of docs/20 §11 is PR-12 surface),
    mirroring how ``SlotGraph`` defers hidden-residual verdicts to
    ``Γ`` — birth only refuses an untyped residual surface.

    Subclasses invoke this guard as
    ``WeightCarrierBase.__post_init__(self)`` rather than through
    zero-argument ``super()``: ``@dataclass(slots=True)`` returns a
    *new* class object, so the implicit ``__class__`` cell of a
    subclass method still points at the pre-decoration class and
    zero-argument ``super()`` raises ``TypeError`` at runtime. The
    explicit call resolves the rebound name correctly.
    """

    value: str
    type: str
    origin: str
    identity: str
    domain: str
    scope: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace: TraceRef

    def __post_init__(self) -> None:
        cls_name = self.__class__.__name__
        if not isinstance(self.value, str) or not self.value.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.value must be a non-empty string "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.type, str) or not self.type.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.type must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.origin, str) or not self.origin.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.origin must be a non-empty string naming the "
                f"licensed generation source ({FailureCode.UNLICENSED_OPENING.value})"
            )
        if not isinstance(self.identity, str) or not self.identity.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.identity must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.domain, str) or not self.domain.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.domain must be a non-empty string "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if not isinstance(self.scope, str) or not self.scope.strip():
            raise WeightCarrierSchemaError(
                f"{cls_name}.scope must be a non-empty string "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"{cls_name}.rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.rank.value > BIRTH_RANK_CEILING.value:
            raise WeightCarrierSchemaError(
                f"{cls_name}.rank must not exceed {BIRTH_RANK_CEILING.name} at "
                f"birth — no weight-branch gate exists before PR-11 "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                f"{cls_name}.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, Residual):
                raise WeightCarrierSchemaError(
                    f"{cls_name}.residuals entries must be Residual carriers — "
                    f"an untyped entry hides its kind and visibility "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace, TraceRef):
            raise WeightCarrierSchemaError(
                f"{cls_name}.trace must be a TraceRef "
                f"({FailureCode.TRACE_MISSING.value})"
            )


__all__ = [
    "BIRTH_RANK_CEILING",
    "WeightCarrierBase",
    "WeightCarrierSchemaError",
]
