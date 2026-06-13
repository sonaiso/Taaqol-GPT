"""Registry Closure Discipline — PR-16C.1.

PR-16C.1 binding of ``docs/30_REGISTRY_CLOSURE_DISCIPLINE_LAW.md``.
This module introduces:

* :class:`RegistryScope` — MUFRAD / TARKIB.
* :class:`RegistryClosureKind` — the four closure kinds.
* :class:`RegistryClosureState` — CLOSED / REFUSED / DEFERRED.
* :class:`RegistryClosureVerdict` — the closure verdict carrier.

Constitutional invariants (docs/30):

* No Meaning Before Registry Closure.
* No semantic/wadʿi/dalālah lexicon before RegistryClosureVerdict.CLOSED.
* RegistryClosureVerdict ≠ Meaning.
* RegistryClosureVerdict ≠ SemanticVerdict.
* DEFERRED is not refusal; it carries no FailureCode.
* Only REFUSED carries a FailureCode.
* No registry content (no actual entries, no lexicon).
* No meaning, ifādah, hukm, reality, ontology.
* No DalMadlulBindingCandidate, ContractableUnitGeometry.
* No new FailureCode members; no new runtime dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.registry_contract import REGISTRY_RANK_CEILING

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for registry closure verdicts — same as REGISTRY_RANK_CEILING.
#: The closure discipline does not promote rank (docs/30 §10).
REGISTRY_CLOSURE_RANK_CEILING: Rank = REGISTRY_RANK_CEILING


# ---------------------------------------------------------------------------
# RegistryScope — the two pre-semantic registry scopes
# ---------------------------------------------------------------------------


class RegistryScope(StrEnum):
    """The two pre-semantic registry scopes (docs/30 §1)."""

    MUFRAD = "MUFRAD"
    TARKIB = "TARKIB"


# ---------------------------------------------------------------------------
# RegistryClosureKind — the four closure kinds
# ---------------------------------------------------------------------------


class RegistryClosureKind(StrEnum):
    """The four registry closure kinds combining domain and scope (docs/30 §2)."""

    DAL_ONLY_MUFRAD = "DAL_ONLY_MUFRAD"
    DAL_ONLY_TARKIB = "DAL_ONLY_TARKIB"
    VERBAL_MADLUL_MUFRAD = "VERBAL_MADLUL_MUFRAD"
    VERBAL_MADLUL_TARKIB = "VERBAL_MADLUL_TARKIB"


# ---------------------------------------------------------------------------
# RegistryClosureState — the three closure outcomes
# ---------------------------------------------------------------------------


class RegistryClosureState(StrEnum):
    """The outcome of a registry closure judgment (docs/30 §3)."""

    CLOSED = "CLOSED"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


# ---------------------------------------------------------------------------
# RegistryClosureVerdict — the frozen closure verdict carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RegistryClosureVerdict:
    """A registry closure verdict (docs/30 §4).

    A frozen carrier representing the judgment on whether a particular
    registry closure kind is sealed. Only a CLOSED verdict licenses
    downstream semantic lexicon access.

    This carrier is NOT meaning. It is a gate discipline that governs
    the transition from pre-semantic registry to semantic lexicon.
    """

    kind: RegistryClosureKind
    state: RegistryClosureState
    failure_code: FailureCode | None
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, RegistryClosureKind):
            raise WeightCarrierSchemaError(
                "RegistryClosureVerdict.kind must be a RegistryClosureKind member "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if not isinstance(self.state, RegistryClosureState):
            raise WeightCarrierSchemaError(
                "RegistryClosureVerdict.state must be a RegistryClosureState member "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if self.state is RegistryClosureState.CLOSED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a CLOSED RegistryClosureVerdict must not carry a FailureCode "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
        elif self.state is RegistryClosureState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED RegistryClosureVerdict must carry a named FailureCode "
                    f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "RegistryClosureVerdict.failure_code must be a FailureCode member "
                    f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
        elif self.state is RegistryClosureState.DEFERRED:  # noqa: SIM102
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED RegistryClosureVerdict must not carry a FailureCode — "
                    "DEFERRED is not refusal (docs/30 §6) "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "RegistryClosureVerdict.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "RegistryClosureVerdict.residuals entries must be Residual carriers "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            # docs/30 §4: "residuals — visible, never hidden"
            if r.kind is ResidualKind.HIDDEN_FORBIDDEN or not r.visible:
                raise WeightCarrierSchemaError(
                    "RegistryClosureVerdict.residuals must be visible — "
                    "HIDDEN_FORBIDDEN or invisible residuals are forbidden at birth "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "RegistryClosureVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )


__all__ = [
    "REGISTRY_CLOSURE_RANK_CEILING",
    "RegistryClosureKind",
    "RegistryClosureState",
    "RegistryClosureVerdict",
    "RegistryScope",
]
