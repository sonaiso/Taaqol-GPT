"""Constitutional tests for PR-16C: Pre-Semantic Registry Contract.

Origin: docs/29_PRE_SEMANTIC_REGISTRY_LAW.md, docs/14 (chain integrity).

Coverage:

1.  docs/29 origin law is present.
2.  RegistryEntry refuses empty key.
3.  RegistryEntry refuses invalid domain.
4.  RegistryEntry refuses empty non_meaning_proof.
5.  RegistryEntry refuses rank above ceiling.
6.  RegistryEntry refuses non-tuple residuals.
7.  RegistryEntry refuses empty trace_ref.
8.  RegistryLookupResult enforces FOUND/REFUSED/DEFERRED invariants.
9.  lookup_registry_entry() refuses empty candidate_key.
10. lookup_registry_entry() refuses invalid domain.
11. lookup_registry_entry() returns FOUND on matching entry.
12. lookup_registry_entry() returns REFUSED on no match.
13. Full registry round-trip with both domains.
14. PR-16C module does not import forbidden types.
15. RegistryEntry is not meaning (no meaning/ifādah/hukm/reality fields).
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.registry_contract import (
    REGISTRY_RANK_CEILING,
    RegistryDomain,
    RegistryEntry,
    RegistryLookupResult,
    RegistryLookupState,
    lookup_registry_entry,
)

_DOC_29 = "docs/29_PRE_SEMANTIC_REGISTRY_LAW.md"


# ---------------------------------------------------------------------------
# Helper: build a valid RegistryEntry
# ---------------------------------------------------------------------------


def _make_entry(
    key: str = "test-entry",
    domain: RegistryDomain = RegistryDomain.DAL_ONLY,
    non_meaning_proof: str = "This entry is a structural classification, not meaning.",
    rank: Rank = Rank.CANDIDATE,
    residuals: tuple[Residual, ...] = (),
    trace_ref: str = "registry/test-entry/trace",
) -> RegistryEntry:
    return RegistryEntry(
        key=key,
        domain=domain,
        non_meaning_proof=non_meaning_proof,
        rank=rank,
        residuals=residuals,
        trace_ref=trace_ref,
    )


# ---------------------------------------------------------------------------
# 1. Origin law present
# ---------------------------------------------------------------------------


class TestOriginLaw:
    """docs/29 origin law is present."""

    def test_docs_29_exists(self) -> None:
        doc = pathlib.Path(_DOC_29)
        assert doc.exists(), f"{_DOC_29} must exist as the origin law for PR-16C"


# ---------------------------------------------------------------------------
# 2–7. RegistryEntry birth guards
# ---------------------------------------------------------------------------


class TestRegistryEntryBirthGuards:
    """RegistryEntry refuses malformed construction (docs/29 §2)."""

    def test_refuses_empty_key(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="REQUIRED_SLOT_EMPTY"):
            _make_entry(key="")

    def test_refuses_whitespace_key(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="REQUIRED_SLOT_EMPTY"):
            _make_entry(key="   ")

    def test_refuses_invalid_domain(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="DOMAIN_MISSING"):
            RegistryEntry(
                key="x",
                domain="INVALID",  # type: ignore[arg-type]
                non_meaning_proof="not meaning",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="t",
            )

    def test_refuses_empty_non_meaning_proof(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="BOUNDARY_MISSING"):
            _make_entry(non_meaning_proof="")

    def test_refuses_rank_above_ceiling(self) -> None:
        above = Rank(REGISTRY_RANK_CEILING.value + 1)
        with pytest.raises(WeightCarrierSchemaError, match="RANK_EXCEEDS_CEILING"):
            _make_entry(rank=above)

    def test_refuses_non_rank(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="RANK_PROMOTION_WITHOUT_GATE"):
            RegistryEntry(
                key="x",
                domain=RegistryDomain.DAL_ONLY,
                non_meaning_proof="not meaning",
                rank=99,  # type: ignore[arg-type]
                residuals=(),
                trace_ref="t",
            )

    def test_refuses_non_tuple_residuals(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="HIDDEN_RESIDUAL"):
            RegistryEntry(
                key="x",
                domain=RegistryDomain.DAL_ONLY,
                non_meaning_proof="not meaning",
                rank=Rank.CANDIDATE,
                residuals=[],  # type: ignore[arg-type]
                trace_ref="t",
            )

    def test_refuses_untyped_residual_entry(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="HIDDEN_RESIDUAL"):
            RegistryEntry(
                key="x",
                domain=RegistryDomain.DAL_ONLY,
                non_meaning_proof="not meaning",
                rank=Rank.CANDIDATE,
                residuals=("not-a-residual",),  # type: ignore[arg-type]
                trace_ref="t",
            )

    def test_refuses_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="TRACE_MISSING"):
            _make_entry(trace_ref="")

    def test_valid_entry_at_ceiling(self) -> None:
        entry = _make_entry(rank=REGISTRY_RANK_CEILING)
        assert entry.rank == REGISTRY_RANK_CEILING

    def test_valid_entry_with_residuals(self) -> None:
        r = Residual(name="open-question", kind=ResidualKind.NON_BLOCKING, visible=True)
        entry = _make_entry(residuals=(r,))
        assert entry.residuals == (r,)


# ---------------------------------------------------------------------------
# 8. RegistryLookupResult invariants
# ---------------------------------------------------------------------------


class TestRegistryLookupResultInvariants:
    """RegistryLookupResult enforces state invariants (docs/29 §4)."""

    def test_found_requires_entry(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="must carry a RegistryEntry"):
            RegistryLookupResult(
                state=RegistryLookupState.FOUND,
                entry=None,
                failure_code=None,
            )

    def test_found_rejects_failure_code(self) -> None:
        entry = _make_entry()
        with pytest.raises(WeightCarrierSchemaError, match="must not carry a FailureCode"):
            RegistryLookupResult(
                state=RegistryLookupState.FOUND,
                entry=entry,
                failure_code=FailureCode.GATE_REQUIRED,
            )

    def test_refused_requires_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="must carry a named FailureCode"):
            RegistryLookupResult(
                state=RegistryLookupState.REFUSED,
                entry=None,
                failure_code=None,
            )

    def test_refused_rejects_entry(self) -> None:
        entry = _make_entry()
        with pytest.raises(WeightCarrierSchemaError, match="must not carry an entry"):
            RegistryLookupResult(
                state=RegistryLookupState.REFUSED,
                entry=entry,
                failure_code=FailureCode.GATE_REQUIRED,
            )

    def test_deferred_rejects_entry(self) -> None:
        entry = _make_entry()
        with pytest.raises(WeightCarrierSchemaError, match="must not carry an entry"):
            RegistryLookupResult(
                state=RegistryLookupState.DEFERRED,
                entry=entry,
                failure_code=None,
            )

    def test_deferred_rejects_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="must not carry a FailureCode"):
            RegistryLookupResult(
                state=RegistryLookupState.DEFERRED,
                entry=None,
                failure_code=FailureCode.GATE_REQUIRED,
            )

    def test_valid_found(self) -> None:
        entry = _make_entry()
        result = RegistryLookupResult(
            state=RegistryLookupState.FOUND,
            entry=entry,
            failure_code=None,
        )
        assert result.state is RegistryLookupState.FOUND
        assert result.entry is entry

    def test_valid_refused(self) -> None:
        result = RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_valid_deferred(self) -> None:
        result = RegistryLookupResult(
            state=RegistryLookupState.DEFERRED,
            entry=None,
            failure_code=None,
        )
        assert result.state is RegistryLookupState.DEFERRED


# ---------------------------------------------------------------------------
# 9–12. lookup_registry_entry() behavior
# ---------------------------------------------------------------------------


class TestLookupRegistryEntry:
    """lookup_registry_entry() pure function behavior (docs/29 §5)."""

    def test_refuses_empty_candidate_key(self) -> None:
        result = lookup_registry_entry("", RegistryDomain.DAL_ONLY, ())
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_whitespace_candidate_key(self) -> None:
        result = lookup_registry_entry("   ", RegistryDomain.DAL_ONLY, ())
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_invalid_domain(self) -> None:
        result = lookup_registry_entry(
            "test", "INVALID", ()  # type: ignore[arg-type]
        )
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.DOMAIN_MISSING

    def test_refuses_non_tuple_registry(self) -> None:
        result = lookup_registry_entry(
            "test", RegistryDomain.DAL_ONLY, []  # type: ignore[arg-type]
        )
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED

    def test_returns_found_on_match(self) -> None:
        entry = _make_entry(key="makhraj-ha", domain=RegistryDomain.DAL_ONLY)
        registry = (entry,)
        result = lookup_registry_entry("makhraj-ha", RegistryDomain.DAL_ONLY, registry)
        assert result.state is RegistryLookupState.FOUND
        assert result.entry is entry
        assert result.failure_code is None

    def test_returns_refused_on_no_match(self) -> None:
        entry = _make_entry(key="makhraj-ha", domain=RegistryDomain.DAL_ONLY)
        registry = (entry,)
        result = lookup_registry_entry("nonexistent", RegistryDomain.DAL_ONLY, registry)
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_domain_mismatch_returns_refused(self) -> None:
        entry = _make_entry(key="khabar", domain=RegistryDomain.VERBAL_MADLUL)
        registry = (entry,)
        result = lookup_registry_entry("khabar", RegistryDomain.DAL_ONLY, registry)
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_registry_returns_refused(self) -> None:
        result = lookup_registry_entry("test", RegistryDomain.DAL_ONLY, ())
        assert result.state is RegistryLookupState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ---------------------------------------------------------------------------
# 13. Full registry round-trip with both domains
# ---------------------------------------------------------------------------


class TestRegistryRoundTrip:
    """Full end-to-end registry lookup with both domains (docs/29 §1)."""

    def test_dal_only_roundtrip(self) -> None:
        entry = _make_entry(
            key="makhraj-ha",
            domain=RegistryDomain.DAL_ONLY,
            non_meaning_proof="Makhraj is a phonetic articulation point, not meaning.",
            trace_ref="registry/dal/makhraj-ha",
        )
        result = lookup_registry_entry("makhraj-ha", RegistryDomain.DAL_ONLY, (entry,))
        assert result.state is RegistryLookupState.FOUND
        assert result.entry is entry
        assert result.entry.domain is RegistryDomain.DAL_ONLY

    def test_verbal_madlul_roundtrip(self) -> None:
        entry = _make_entry(
            key="khabar",
            domain=RegistryDomain.VERBAL_MADLUL,
            non_meaning_proof="Khabar is a verbal structure candidate, not final meaning.",
            trace_ref="registry/madlul/khabar",
        )
        result = lookup_registry_entry("khabar", RegistryDomain.VERBAL_MADLUL, (entry,))
        assert result.state is RegistryLookupState.FOUND
        assert result.entry is entry
        assert result.entry.domain is RegistryDomain.VERBAL_MADLUL

    def test_mixed_registry_correct_domain_match(self) -> None:
        dal_entry = _make_entry(key="wazn", domain=RegistryDomain.DAL_ONLY)
        madlul_entry = _make_entry(key="isnad", domain=RegistryDomain.VERBAL_MADLUL)
        registry = (dal_entry, madlul_entry)

        r1 = lookup_registry_entry("wazn", RegistryDomain.DAL_ONLY, registry)
        assert r1.state is RegistryLookupState.FOUND
        assert r1.entry is dal_entry

        r2 = lookup_registry_entry("isnad", RegistryDomain.VERBAL_MADLUL, registry)
        assert r2.state is RegistryLookupState.FOUND
        assert r2.entry is madlul_entry

        r3 = lookup_registry_entry("wazn", RegistryDomain.VERBAL_MADLUL, registry)
        assert r3.state is RegistryLookupState.REFUSED


# ---------------------------------------------------------------------------
# 14. Module import hygiene
# ---------------------------------------------------------------------------


class TestModuleImportHygiene:
    """PR-16C module does not import forbidden types (docs/29 §7)."""

    _FORBIDDEN_NAMES = frozenset(
        {
            "DalMadlulBindingCandidate",
            "ContractableUnitGeometry",
            "RelationCandidate",
            "IfadahCandidate",
            "HukmCandidate",
            "TanzilCandidate",
            "ExtraLetterLicense",
            "Meaning",
            "ConceptualMeaning",
            "SemanticVerdict",
        }
    )

    def test_no_forbidden_imports(self) -> None:
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/registry_contract.py"
        ).read_text()
        tree = ast.parse(src)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ImportFrom, ast.Import)):
                for alias in node.names:
                    imported.add(alias.asname or alias.name)
        violations = imported & self._FORBIDDEN_NAMES
        assert not violations, f"registry_contract.py imports forbidden names: {violations}"


# ---------------------------------------------------------------------------
# 15. RegistryEntry is not meaning
# ---------------------------------------------------------------------------


class TestRegistryEntryIsNotMeaning:
    """RegistryEntry carries no meaning/ifādah/hukm/reality fields (docs/29 §6)."""

    def test_no_meaning_field(self) -> None:
        entry = _make_entry()
        field_names = {f.name for f in entry.__dataclass_fields__.values()}
        forbidden = {"meaning", "dalālah", "ifadah", "hukm", "reality", "wāqi"}
        overlap = field_names & forbidden
        assert not overlap, f"RegistryEntry has forbidden fields: {overlap}"

    def test_non_meaning_proof_is_required(self) -> None:
        entry = _make_entry()
        assert entry.non_meaning_proof, "RegistryEntry must carry non_meaning_proof"

    def test_registry_rank_ceiling_bounded(self) -> None:
        from taaqqul_slot_geometry.weight.chain_report import CHAIN_REPORT_RANK_CEILING
        assert REGISTRY_RANK_CEILING == CHAIN_REPORT_RANK_CEILING, (
            "REGISTRY_RANK_CEILING must equal CHAIN_REPORT_RANK_CEILING (docs/29 §3)"
        )
