"""Pre-Semantic Registry Contract — PR-16C.

PR-16C binding of ``docs/29_PRE_SEMANTIC_REGISTRY_LAW.md``.
This module introduces:

* :class:`RegistryDomain` — DAL_ONLY / VERBAL_MADLUL.
* :class:`RegistryEntry` — the frozen registry entry carrier.
* :class:`RegistryLookupState` — FOUND / REFUSED / DEFERRED.
* :class:`RegistryLookupResult` — the lookup result carrier.
* :func:`lookup_registry_entry` — the pure lookup operation.

Constitutional invariants (docs/29):

* RegistryEntry ≠ Meaning.
* RegistryLookupResult ≠ SemanticVerdict.
* RegistryLookupResult ≠ Binding.
* lookup_registry_entry() licenses pre-semantic admissibility only.
* No registry content (no actual dal/verbal-madlul entries).
* No meaning, ifādah, hukm, reality, ontology.
* No DalMadlulBindingCandidate, ContractableUnitGeometry.
* No new FailureCode members; no new runtime dependencies.
* lookup_registry_entry() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.chain_report import CHAIN_REPORT_RANK_CEILING

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for registry entries — same as CHAIN_REPORT_RANK_CEILING.
#: The registry does not promote rank (docs/29 §3).
REGISTRY_RANK_CEILING: Rank = CHAIN_REPORT_RANK_CEILING


# ---------------------------------------------------------------------------
# RegistryDomain — the two pre-semantic registry domains
# ---------------------------------------------------------------------------


class RegistryDomain(StrEnum):
    """The two pre-semantic registry domains (docs/29 §1)."""

    DAL_ONLY = "DAL_ONLY"
    VERBAL_MADLUL = "VERBAL_MADLUL"


# ---------------------------------------------------------------------------
# RegistryEntry — the frozen registry entry carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RegistryEntry:
    """A pre-semantic registry entry (docs/29 §2).

    A frozen carrier classifying a candidate within a pre-semantic
    registry domain. Every entry carries an explicit non-meaning
    attestation (docs/29 §6) and is bounded by REGISTRY_RANK_CEILING.

    This carrier is NOT meaning. It is a pre-semantic classification
    that licenses admissibility for binding (PR-17).
    """

    key: str
    domain: RegistryDomain
    non_meaning_proof: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.key, str) or not self.key.strip():
            raise WeightCarrierSchemaError(
                "RegistryEntry.key must be a non-empty string "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.domain, RegistryDomain):
            raise WeightCarrierSchemaError(
                "RegistryEntry.domain must be a RegistryDomain member "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if not isinstance(self.non_meaning_proof, str) or not self.non_meaning_proof.strip():
            raise WeightCarrierSchemaError(
                "RegistryEntry.non_meaning_proof must be a non-empty string — "
                "no entry may travel without a non-meaning attestation "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "RegistryEntry.rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.rank > REGISTRY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"RegistryEntry.rank must not exceed {REGISTRY_RANK_CEILING.name} "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "RegistryEntry.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "RegistryEntry.residuals entries must be Residual carriers "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "RegistryEntry.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# RegistryLookupState — the three lookup outcomes
# ---------------------------------------------------------------------------


class RegistryLookupState(StrEnum):
    """The outcome of a registry lookup operation (docs/29 §4)."""

    FOUND = "FOUND"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


# ---------------------------------------------------------------------------
# RegistryLookupResult — the lookup result carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RegistryLookupResult:
    """The result of :func:`lookup_registry_entry` (docs/29 §4).

    Fields:
    * ``state`` — FOUND, REFUSED, or DEFERRED.
    * ``entry`` — the RegistryEntry (present iff FOUND).
    * ``failure_code`` — named FailureCode (present iff REFUSED).
    """

    state: RegistryLookupState
    entry: RegistryEntry | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.state, RegistryLookupState):
            raise WeightCarrierSchemaError(
                "RegistryLookupResult.state must be a RegistryLookupState member"
            )
        if self.state is RegistryLookupState.FOUND:
            if self.entry is None:
                raise WeightCarrierSchemaError(
                    "a FOUND RegistryLookupResult must carry a RegistryEntry"
                )
            if not isinstance(self.entry, RegistryEntry):
                raise WeightCarrierSchemaError(
                    "RegistryLookupResult.entry must be a RegistryEntry"
                )
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a FOUND RegistryLookupResult must not carry a FailureCode"
                )
        elif self.state is RegistryLookupState.REFUSED:
            if self.entry is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED RegistryLookupResult must not carry an entry"
                )
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED RegistryLookupResult must carry a named FailureCode"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "RegistryLookupResult.failure_code must be a FailureCode member"
                )
        elif self.state is RegistryLookupState.DEFERRED:
            if self.entry is not None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED RegistryLookupResult must not carry an entry"
                )
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED RegistryLookupResult must not carry a FailureCode"
                )


# ---------------------------------------------------------------------------
# lookup_registry_entry() — the pure lookup operation
# ---------------------------------------------------------------------------


def lookup_registry_entry(
    candidate_key: str,
    domain: RegistryDomain,
    registry: tuple[RegistryEntry, ...],
) -> RegistryLookupResult:
    """Look up a candidate in the pre-semantic registry (docs/29 §5).

    A pure function: no I/O, no ledger writes, no network.

    Input boundary:
    * Refuses empty candidate_key with GATE_REQUIRED.
    * Refuses invalid domain with DOMAIN_MISSING.
    * Searches registry for a matching entry.

    Output:
    * FOUND with entry if matched.
    * REFUSED with REQUIRED_SLOT_EMPTY if no match.
    """
    # --- Input boundary enforcement ---
    if not isinstance(candidate_key, str) or not candidate_key.strip():
        return RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.GATE_REQUIRED,
        )

    if not isinstance(domain, RegistryDomain):
        return RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.DOMAIN_MISSING,
        )

    if not isinstance(registry, tuple):
        return RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.GATE_REQUIRED,
        )

    # --- Search for matching entry ---
    for entry in registry:
        if (
            isinstance(entry, RegistryEntry)
            and entry.key == candidate_key.strip()
            and entry.domain is domain
        ):
            return RegistryLookupResult(
                state=RegistryLookupState.FOUND,
                entry=entry,
                failure_code=None,
            )

    # --- No match found ---
    return RegistryLookupResult(
        state=RegistryLookupState.REFUSED,
        entry=None,
        failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
    )


__all__ = [
    "REGISTRY_RANK_CEILING",
    "RegistryDomain",
    "RegistryEntry",
    "RegistryLookupResult",
    "RegistryLookupState",
    "lookup_registry_entry",
]
