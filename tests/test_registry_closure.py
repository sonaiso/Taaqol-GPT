"""Constitutional tests for the Registry Closure Discipline — PR-16C.1.

Proves that docs/30_REGISTRY_CLOSURE_DISCIPLINE_LAW.md is implemented
correctly:

* RegistryScope, RegistryClosureKind, RegistryClosureState enums exist.
* RegistryClosureVerdict birth guards enforce all invariants.
* CLOSED => no FailureCode.
* REFUSED => has FailureCode.
* DEFERRED => no FailureCode (DEFERRED is not refusal).
* Residual visibility: no untyped residuals.
* Trace presence: non-empty trace_ref required.
* Scope independence: MUFRAD and TARKIB are independent.
* Forbidden output absence: no meaning, no lexicon, no content.
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.registry_closure import (
    REGISTRY_CLOSURE_RANK_CEILING,
    RegistryClosureKind,
    RegistryClosureState,
    RegistryClosureVerdict,
    RegistryScope,
)

# ---------------------------------------------------------------------------
# §0. Origin law existence
# ---------------------------------------------------------------------------


class TestOriginLaw:
    """Proves docs/30 exists — the constitutional origin of PR-16C.1."""

    def test_docs_30_exists(self) -> None:
        docs = pathlib.Path(__file__).resolve().parents[1] / "docs"
        assert (docs / "30_REGISTRY_CLOSURE_DISCIPLINE_LAW.md").is_file()


# ---------------------------------------------------------------------------
# §1. Enum completeness
# ---------------------------------------------------------------------------


class TestRegistryScopeEnum:
    """Proves RegistryScope has exactly two members (docs/30 §1)."""

    def test_mufrad_exists(self) -> None:
        assert RegistryScope.MUFRAD == "MUFRAD"

    def test_tarkib_exists(self) -> None:
        assert RegistryScope.TARKIB == "TARKIB"

    def test_exactly_two_members(self) -> None:
        assert len(RegistryScope) == 2


class TestRegistryClosureKindEnum:
    """Proves RegistryClosureKind has exactly four members (docs/30 §2)."""

    def test_dal_only_mufrad(self) -> None:
        assert RegistryClosureKind.DAL_ONLY_MUFRAD == "DAL_ONLY_MUFRAD"

    def test_dal_only_tarkib(self) -> None:
        assert RegistryClosureKind.DAL_ONLY_TARKIB == "DAL_ONLY_TARKIB"

    def test_verbal_madlul_mufrad(self) -> None:
        assert RegistryClosureKind.VERBAL_MADLUL_MUFRAD == "VERBAL_MADLUL_MUFRAD"

    def test_verbal_madlul_tarkib(self) -> None:
        assert RegistryClosureKind.VERBAL_MADLUL_TARKIB == "VERBAL_MADLUL_TARKIB"

    def test_exactly_four_members(self) -> None:
        assert len(RegistryClosureKind) == 4


class TestRegistryClosureStateEnum:
    """Proves RegistryClosureState has exactly three members (docs/30 §3)."""

    def test_closed(self) -> None:
        assert RegistryClosureState.CLOSED == "CLOSED"

    def test_refused(self) -> None:
        assert RegistryClosureState.REFUSED == "REFUSED"

    def test_deferred(self) -> None:
        assert RegistryClosureState.DEFERRED == "DEFERRED"

    def test_exactly_three_members(self) -> None:
        assert len(RegistryClosureState) == 3


# ---------------------------------------------------------------------------
# §2. Rank ceiling
# ---------------------------------------------------------------------------


class TestRankCeiling:
    """Proves REGISTRY_CLOSURE_RANK_CEILING inherits from REGISTRY_RANK_CEILING."""

    def test_ceiling_is_rank(self) -> None:
        assert isinstance(REGISTRY_CLOSURE_RANK_CEILING, Rank)

    def test_ceiling_matches_registry(self) -> None:
        from taaqqul_slot_geometry.weight.registry_contract import REGISTRY_RANK_CEILING

        assert REGISTRY_CLOSURE_RANK_CEILING is REGISTRY_RANK_CEILING


# ---------------------------------------------------------------------------
# §3. RegistryClosureVerdict birth guards
# ---------------------------------------------------------------------------


def _make_verdict(
    *,
    kind: RegistryClosureKind = RegistryClosureKind.DAL_ONLY_MUFRAD,
    state: RegistryClosureState = RegistryClosureState.CLOSED,
    failure_code: FailureCode | None = None,
    residuals: tuple[Residual, ...] = (),
    trace_ref: str = "trace-closure-test",
) -> RegistryClosureVerdict:
    return RegistryClosureVerdict(
        kind=kind,
        state=state,
        failure_code=failure_code,
        residuals=residuals,
        trace_ref=trace_ref,
    )


class TestVerdictBirthGuards:
    """Proves every malformed RegistryClosureVerdict is refused (docs/30 §4)."""

    # --- Valid verdicts ---

    def test_closed_verdict_valid(self) -> None:
        v = _make_verdict(state=RegistryClosureState.CLOSED, failure_code=None)
        assert v.state is RegistryClosureState.CLOSED
        assert v.failure_code is None

    def test_refused_verdict_valid(self) -> None:
        v = _make_verdict(
            state=RegistryClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )
        assert v.state is RegistryClosureState.REFUSED
        assert v.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_deferred_verdict_valid(self) -> None:
        v = _make_verdict(state=RegistryClosureState.DEFERRED, failure_code=None)
        assert v.state is RegistryClosureState.DEFERRED
        assert v.failure_code is None

    # --- Invalid kind ---

    def test_invalid_kind_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="RegistryClosureKind"):
            RegistryClosureVerdict(
                kind="NOT_A_KIND",  # type: ignore[arg-type]
                state=RegistryClosureState.CLOSED,
                failure_code=None,
                residuals=(),
                trace_ref="t",
            )

    # --- Invalid state ---

    def test_invalid_state_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="RegistryClosureState"):
            RegistryClosureVerdict(
                kind=RegistryClosureKind.DAL_ONLY_MUFRAD,
                state="NOT_A_STATE",  # type: ignore[arg-type]
                failure_code=None,
                residuals=(),
                trace_ref="t",
            )

    # --- CLOSED with FailureCode ---

    def test_closed_with_failure_code_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="CLOSED.*must not carry"):
            _make_verdict(
                state=RegistryClosureState.CLOSED,
                failure_code=FailureCode.GATE_REQUIRED,
            )

    # --- REFUSED without FailureCode ---

    def test_refused_without_failure_code_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="REFUSED.*must carry"):
            _make_verdict(state=RegistryClosureState.REFUSED, failure_code=None)

    # --- REFUSED with non-FailureCode ---

    def test_refused_with_invalid_failure_code_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="FailureCode member"):
            RegistryClosureVerdict(
                kind=RegistryClosureKind.DAL_ONLY_MUFRAD,
                state=RegistryClosureState.REFUSED,
                failure_code="not_a_code",  # type: ignore[arg-type]
                residuals=(),
                trace_ref="t",
            )

    # --- DEFERRED with FailureCode (docs/30 §6: DEFERRED is not refusal) ---

    def test_deferred_with_failure_code_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="DEFERRED.*must not carry"):
            _make_verdict(
                state=RegistryClosureState.DEFERRED,
                failure_code=FailureCode.GATE_REQUIRED,
            )

    # --- Invalid residuals ---

    def test_non_tuple_residuals_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="residuals.*tuple"):
            RegistryClosureVerdict(
                kind=RegistryClosureKind.DAL_ONLY_MUFRAD,
                state=RegistryClosureState.CLOSED,
                failure_code=None,
                residuals=[],  # type: ignore[arg-type]
                trace_ref="t",
            )

    def test_untyped_residual_entry_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="Residual carriers"):
            RegistryClosureVerdict(
                kind=RegistryClosureKind.DAL_ONLY_MUFRAD,
                state=RegistryClosureState.CLOSED,
                failure_code=None,
                residuals=("not_a_residual",),  # type: ignore[arg-type]
                trace_ref="t",
            )

    # --- Empty trace_ref ---

    def test_empty_trace_ref_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="trace_ref.*non-empty"):
            _make_verdict(trace_ref="")

    def test_whitespace_trace_ref_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="trace_ref.*non-empty"):
            _make_verdict(trace_ref="   ")

    # --- Valid with residuals ---

    def test_verdict_with_typed_residuals(self) -> None:
        r = Residual(name="test-residual", kind=ResidualKind.NON_BLOCKING, visible=True)
        v = _make_verdict(residuals=(r,))
        assert v.residuals == (r,)


# ---------------------------------------------------------------------------
# §4. All four closure kinds are independently judgeable
# ---------------------------------------------------------------------------


class TestClosureKindIndependence:
    """Proves each of the four closure kinds can be judged independently."""

    @pytest.mark.parametrize(
        "kind",
        list(RegistryClosureKind),
        ids=[k.value for k in RegistryClosureKind],
    )
    def test_each_kind_produces_valid_closed_verdict(
        self, kind: RegistryClosureKind
    ) -> None:
        v = _make_verdict(kind=kind, state=RegistryClosureState.CLOSED)
        assert v.kind is kind
        assert v.state is RegistryClosureState.CLOSED

    @pytest.mark.parametrize(
        "kind",
        list(RegistryClosureKind),
        ids=[k.value for k in RegistryClosureKind],
    )
    def test_each_kind_produces_valid_refused_verdict(
        self, kind: RegistryClosureKind
    ) -> None:
        v = _make_verdict(
            kind=kind,
            state=RegistryClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
        )
        assert v.kind is kind
        assert v.state is RegistryClosureState.REFUSED

    @pytest.mark.parametrize(
        "kind",
        list(RegistryClosureKind),
        ids=[k.value for k in RegistryClosureKind],
    )
    def test_each_kind_produces_valid_deferred_verdict(
        self, kind: RegistryClosureKind
    ) -> None:
        v = _make_verdict(kind=kind, state=RegistryClosureState.DEFERRED)
        assert v.kind is kind
        assert v.state is RegistryClosureState.DEFERRED


# ---------------------------------------------------------------------------
# §5. Frozen carrier discipline
# ---------------------------------------------------------------------------


class TestFrozenCarrier:
    """Proves RegistryClosureVerdict is frozen (immutable)."""

    def test_verdict_is_frozen(self) -> None:
        v = _make_verdict()
        with pytest.raises(AttributeError):
            v.state = RegistryClosureState.REFUSED  # type: ignore[misc]

    def test_verdict_is_frozen_kind(self) -> None:
        v = _make_verdict()
        with pytest.raises(AttributeError):
            v.kind = RegistryClosureKind.DAL_ONLY_TARKIB  # type: ignore[misc]


# ---------------------------------------------------------------------------
# §6. Module import hygiene — no forbidden names
# ---------------------------------------------------------------------------


class TestModuleImportHygiene:
    """Proves registry_closure.py does not import forbidden names."""

    def test_no_dal_madlul_binding(self) -> None:
        import taaqqul_slot_geometry.weight.registry_closure as mod

        assert not hasattr(mod, "DalMadlulBindingCandidate")

    def test_no_contractable_unit_geometry(self) -> None:
        import taaqqul_slot_geometry.weight.registry_closure as mod

        assert not hasattr(mod, "ContractableUnitGeometry")

    def test_no_meaning_field(self) -> None:
        import taaqqul_slot_geometry.weight.registry_closure as mod

        exported = dir(mod)
        for forbidden in ("Meaning", "Dalaalah", "Ifaadah", "Hukm", "Reality"):
            assert forbidden not in exported


# ---------------------------------------------------------------------------
# §7. RegistryClosureVerdict is not meaning
# ---------------------------------------------------------------------------


class TestVerdictIsNotMeaning:
    """Proves RegistryClosureVerdict carries no meaning/semantic fields."""

    def test_no_meaning_field(self) -> None:
        v = _make_verdict()
        assert not hasattr(v, "meaning")

    def test_no_dalaalah_field(self) -> None:
        v = _make_verdict()
        assert not hasattr(v, "dalaalah")

    def test_no_ifaadah_field(self) -> None:
        v = _make_verdict()
        assert not hasattr(v, "ifaadah")

    def test_no_hukm_field(self) -> None:
        v = _make_verdict()
        assert not hasattr(v, "hukm")

    def test_no_reality_field(self) -> None:
        v = _make_verdict()
        assert not hasattr(v, "reality")
