"""Tests for GUA-1 neutral core extraction and freeze discipline."""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.gua import (
    DomainSpec,
    GeneralCoreExtraction,
    LocalGeometry,
    PriorDomainMatrix,
    Trace,
    TransitionContract,
    TypedSlot,
    freeze_general_core,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/112", "GUA-1", "GeneralCoreExtraction"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("LegacyCoreMutation",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _make_extraction(trace_ref: str = "gua-trace-1") -> GeneralCoreExtraction:
    domain = DomainSpec(
        domain_id="generic-domain",
        scope="bounded-scope",
        boundaries=("domain", "scope"),
        invariants=("identity_continuity",),
    )
    prior = PriorDomainMatrix(
        domain_id="generic-domain",
        required_priors=("declared_origin",),
        trace_ref=trace_ref,
    )
    slot = TypedSlot(
        slot_type="unit",
        domain_id="generic-domain",
        coordinates=("axis_a", "axis_b"),
        boundary=("domain", "scope"),
        invariants=("identity_continuity",),
        prior_requirements=("declared_origin",),
        admissible_states=("candidate",),
        residual_region=("visible_residual",),
    )
    transition = TransitionContract(
        transition_id="unit_to_relation",
        source_state="candidate",
        target_state="relation",
        required_evidence=("traceable_observation",),
        rank_ceiling="CANDIDATE",
        trace_ref=trace_ref,
    )
    return GeneralCoreExtraction(
        domain=domain,
        prior_matrix=prior,
        geometry=LocalGeometry(slots=(slot,), trace=Trace(trace_ref=trace_ref, stage="extraction")),
        transitions=(transition,),
    )


def test_gua_core_freeze_is_deterministic() -> None:
    _declare("GUA-1 freeze determinism")
    extraction = _make_extraction()

    first = freeze_general_core(extraction)
    second = freeze_general_core(extraction)

    assert first.extraction_hash == second.extraction_hash
    assert first.frozen_fields == ("domain", "prior_matrix", "geometry", "transitions")


def test_gua_core_avoids_domain_specific_vocabulary() -> None:
    _declare("GUA-1 neutral core vocabulary")
    base = Path(__file__).resolve().parents[1] / "src" / "taaqqul_slot_geometry" / "gua" / "core"
    banned_terms = {
        "arabic",
        "ifadah",
        "hukm",
        "mantuq",
        "mafhum",
        "physics",
        "vector",
        "function",
        "python",
        "word",
        "phoneme",
    }

    for path in base.glob("*.py"):
        content = path.read_text(encoding="utf-8").lower()
        for term in banned_terms:
            assert term not in content, f"{path.name} contains banned core term: {term}"
