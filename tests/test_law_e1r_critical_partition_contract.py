"""Runtime contract tests for LAW-E1R critical partition surface.

Origin law          : docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md
Branch name         : LAW-E1R Critical Partition Runtime Contract Surface
Constitutional chain: docs/70 -> LAW-E1R -> X0R runtime contract surface
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    CriticalPartitionRuntimeContract,
    CriticalPartitionStage,
    IdentityPropertyConservationProof,
    NecessityTier,
    NecessityTierProof,
    PartitionBridgeProof,
    PartitionDeclaration,
    PartitionKind,
    PartitionReadinessState,
    TriadicIdentityContinuityProof,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md",
        branch_name=branch_name,
        constitutional_chain=("docs/70", "LAW-E1R", "X0RRuntimeContractSurface"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("ParserRuntime", "SemanticClosureClaim"),
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


def _contract() -> CriticalPartitionRuntimeContract:
    return CriticalPartitionRuntimeContract(
        declared_partitions=frozenset(
            {
                (PartitionKind.PHONETIC, "text_understanding", "critical_partition"),
                (PartitionKind.STRUCTURAL, "text_understanding", "critical_partition"),
                (PartitionKind.SYSTEMIC, "text_understanding", "critical_partition"),
            }
        ),
        declared_bridges=frozenset(
            {
                (
                    PartitionKind.PHONETIC,
                    PartitionKind.STRUCTURAL,
                    "text_understanding",
                    "critical_partition",
                    "PHONETIC_TO_STRUCTURAL",
                ),
                (
                    PartitionKind.STRUCTURAL,
                    PartitionKind.SYSTEMIC,
                    "text_understanding",
                    "critical_partition",
                    "STRUCTURAL_TO_SYSTEMIC",
                ),
            }
        ),
    )


def _declaration(kind: PartitionKind = PartitionKind.PHONETIC) -> PartitionDeclaration:
    return PartitionDeclaration(
        partition_kind=kind,
        domain="text_understanding",
        scope="critical_partition",
        trace_ref="trace://e1r/test",
        residual_visible=True,
    )


def _bridge(
    source: PartitionKind = PartitionKind.PHONETIC,
    target: PartitionKind = PartitionKind.STRUCTURAL,
    bridge_name: str = "PHONETIC_TO_STRUCTURAL",
) -> PartitionBridgeProof:
    return PartitionBridgeProof(
        source_partition=source,
        target_partition=target,
        domain="text_understanding",
        scope="critical_partition",
        trace_ref="trace://e1r/test",
        residual_visible=True,
        bridge_name=bridge_name,
    )


def _identity(**overrides: object) -> IdentityPropertyConservationProof:
    payload = {
        "identity_anchor": "id://anchor/test",
        "preserved_properties": ("phoneme_profile",),
        "licensed_variants": (),
        "broken_properties": (),
        "trace_ref": "trace://e1r/test",
    }
    payload.update(overrides)
    return IdentityPropertyConservationProof(**payload)


def _triadic(**overrides: object) -> TriadicIdentityContinuityProof:
    payload = {
        "previous_identity_ref": "id://prev/test",
        "current_identity_ref": "id://curr/test",
        "next_identity_ref": "id://next/test",
        "previous_current_link": "prev->current",
        "current_next_link": "current->next",
        "bridge_coherent": True,
        "residual_visible": True,
    }
    payload.update(overrides)
    return TriadicIdentityContinuityProof(**payload)


def _tier(
    tier: NecessityTier = NecessityTier.DARURI,
    *,
    declared_cause: str = "core-need",
    evidence_ref: str = "evidence://test",
    transition_ref: str = "transition://test",
    residual_visible: bool = True,
) -> NecessityTierProof:
    return NecessityTierProof(
        tier=tier,
        declared_cause=declared_cause,
        evidence_ref=evidence_ref,
        transition_ref=transition_ref,
        residual_visible=residual_visible,
    )


def test_law_e1r_declares_runtime_surface_identity() -> None:
    _declare("LAW-E1R runtime surface identity")


def test_missing_partition_declaration_is_refused() -> None:
    _declare("missing partition declaration")
    verdict = _contract().evaluate(
        declaration=PartitionDeclaration(
            partition_kind=PartitionKind.PHONETIC,
            domain="text_understanding",
            scope="non_critical_scope",
            trace_ref="trace://e1r/test",
            residual_visible=True,
        ),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://systemic/structural",
    )
    assert verdict.partition_allowed is False
    assert verdict.failed_stage is CriticalPartitionStage.PARTITION_DECLARATION
    assert verdict.local_failure_name == "PARTITION_UNDECLARED"
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_missing_bridge_is_deferred_gate_required() -> None:
    _declare("missing bridge")
    verdict = _contract().evaluate(
        declaration=_declaration(),
        bridge_proof=_bridge(
            PartitionKind.PHONETIC,
            PartitionKind.SYSTEMIC,
            "PHONETIC_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://phonetic/systemic",
    )
    assert verdict.partition_allowed is False
    assert verdict.readiness_state is PartitionReadinessState.DEFERRED
    assert verdict.local_failure_name == "PARTITION_BRIDGE_MISSING"
    assert verdict.failure_code is FailureCode.GATE_REQUIRED


def test_identity_and_triadic_gaps_are_refused() -> None:
    _declare("identity and triadic gaps")
    contract = _contract()

    broken_identity = contract.evaluate(
        declaration=_declaration(),
        bridge_proof=_bridge(),
        identity_proof=_identity(preserved_properties=(), broken_properties=("phoneme_profile",)),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://phonetic/structural",
    )
    triadic_gap = contract.evaluate(
        declaration=_declaration(),
        bridge_proof=_bridge(),
        identity_proof=_identity(),
        triadic_proof=_triadic(next_identity_ref="", current_next_link=""),
        tier_proof=_tier(),
        handoff="handoff://phonetic/structural",
    )

    assert broken_identity.local_failure_name == "IDENTITY_PROPERTY_BROKEN"
    assert broken_identity.failure_code is FailureCode.IDENTITY_BROKEN
    assert triadic_gap.local_failure_name == "TRIADIC_IDENTITY_GAP"
    assert triadic_gap.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_broken_identity_is_refused_even_with_licensed_variants() -> None:
    _declare("broken identity refused even with licensed variants")
    verdict = _contract().evaluate(
        declaration=_declaration(),
        bridge_proof=_bridge(),
        identity_proof=_identity(
            preserved_properties=("phoneme_profile",),
            licensed_variants=("variant_a",),
            broken_properties=("phoneme_profile",),
        ),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://phonetic/structural",
    )
    assert verdict.partition_allowed is False
    assert verdict.local_failure_name == "IDENTITY_PROPERTY_BROKEN"
    assert verdict.failure_code is FailureCode.IDENTITY_BROKEN


def test_necessity_tier_rules_refuse_unlicensed_promotion_or_closure_claim() -> None:
    _declare("necessity tier refusals")
    contract = _contract()

    no_evidence = contract.evaluate(
        declaration=_declaration(PartitionKind.STRUCTURAL),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(evidence_ref="", transition_ref=""),
        handoff="handoff://structural/systemic",
    )
    tahsini_closure = contract.evaluate(
        declaration=_declaration(PartitionKind.STRUCTURAL),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(
            tier=NecessityTier.TAHSINI,
            declared_cause="semantic closure claim",
            evidence_ref="closure://asserted",
        ),
        handoff="handoff://structural/systemic",
    )

    assert no_evidence.local_failure_name == "NECESSITY_TIER_PROMOTION_UNLICENSED"
    assert no_evidence.failure_code is FailureCode.GATE_REQUIRED
    assert tahsini_closure.local_failure_name == "TIER_LABEL_AS_CLOSURE_FORBIDDEN"
    assert tahsini_closure.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_hidden_residual_is_refused() -> None:
    _declare("hidden residual")
    verdict = _contract().evaluate(
        declaration=_declaration(),
        bridge_proof=_bridge(),
        identity_proof=_identity(),
        triadic_proof=_triadic(residual_visible=False),
        tier_proof=_tier(),
        handoff="handoff://phonetic/structural",
        residuals=("triadic residual hidden",),
    )
    assert verdict.partition_allowed is False
    assert verdict.failed_stage is CriticalPartitionStage.RESIDUALS
    assert verdict.local_failure_name == "HIDDEN_RESIDUAL"
    assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL


def test_forbidden_neighbor_leaps_are_refused() -> None:
    _declare("forbidden neighbor leaps")
    contract = _contract()

    phonetic_to_meaning = contract.evaluate(
        declaration=_declaration(PartitionKind.PHONETIC),
        bridge_proof=_bridge(),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://meaning/claim",
    )
    structural_to_hukm = contract.evaluate(
        declaration=_declaration(PartitionKind.STRUCTURAL),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://hukm/claim",
    )
    systemic_to_truth = contract.evaluate(
        declaration=_declaration(PartitionKind.SYSTEMIC),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(),
        triadic_proof=_triadic(),
        tier_proof=_tier(),
        handoff="handoff://truth/claim",
    )

    assert phonetic_to_meaning.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
    assert structural_to_hukm.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
    assert systemic_to_truth.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"


def test_phonetic_handoff_to_semantic_ifadah_or_mafhum_is_refused() -> None:
    _declare("phonetic handoff to semantic ifadah mafhum refused")
    contract = _contract()
    for handoff in (
        "handoff://semantic/claim",
        "handoff://ifadah/claim",
        "handoff://mafhum/claim",
    ):
        verdict = contract.evaluate(
            declaration=_declaration(PartitionKind.PHONETIC),
            bridge_proof=_bridge(),
            identity_proof=_identity(),
            triadic_proof=_triadic(),
            tier_proof=_tier(),
            handoff=handoff,
        )
        assert verdict.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
        assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_structural_handoff_to_meaning_or_ifadah_is_refused() -> None:
    _declare("structural handoff to meaning ifadah refused")
    contract = _contract()
    for handoff in ("handoff://meaning/claim", "handoff://ifadah/claim"):
        verdict = contract.evaluate(
            declaration=_declaration(PartitionKind.STRUCTURAL),
            bridge_proof=_bridge(
                PartitionKind.STRUCTURAL,
                PartitionKind.SYSTEMIC,
                "STRUCTURAL_TO_SYSTEMIC",
            ),
            identity_proof=_identity(),
            triadic_proof=_triadic(),
            tier_proof=_tier(),
            handoff=handoff,
        )
        assert verdict.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
        assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_systemic_handoff_to_certainty_or_reality_is_refused() -> None:
    _declare("systemic handoff to certainty reality refused")
    contract = _contract()
    for handoff in ("handoff://certainty/claim", "handoff://reality/claim"):
        verdict = contract.evaluate(
            declaration=_declaration(PartitionKind.SYSTEMIC),
            bridge_proof=_bridge(
                PartitionKind.STRUCTURAL,
                PartitionKind.SYSTEMIC,
                "STRUCTURAL_TO_SYSTEMIC",
            ),
            identity_proof=_identity(),
            triadic_proof=_triadic(),
            tier_proof=_tier(),
            handoff=handoff,
        )
        assert verdict.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
        assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_forbidden_handoff_tokens_are_case_and_separator_stable() -> None:
    _declare("forbidden handoff token stability")
    contract = _contract()
    for handoff in ("handoff://Semantic_Claim", "handoff://IFADAH-CLAIM", "handoff://mafhūm.claim"):
        verdict = contract.evaluate(
            declaration=_declaration(PartitionKind.PHONETIC),
            bridge_proof=_bridge(),
            identity_proof=_identity(),
            triadic_proof=_triadic(),
            tier_proof=_tier(),
            handoff=handoff,
        )
        assert verdict.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"


def test_arabic_forbidden_handoff_tokens_are_refused() -> None:
    _declare("arabic forbidden handoff tokens refused")
    contract = _contract()
    for partition, handoff in (
        (PartitionKind.STRUCTURAL, "handoff://حكم"),
        (PartitionKind.STRUCTURAL, "handoff://حكم،"),
        (PartitionKind.STRUCTURAL, "handoff://إفادة"),
        (PartitionKind.STRUCTURAL, "handoff://إفادة-claim"),
        (PartitionKind.SYSTEMIC, "handoff://واقع"),
    ):
        verdict = contract.evaluate(
            declaration=_declaration(partition),
            bridge_proof=_bridge(
                PartitionKind.STRUCTURAL,
                PartitionKind.SYSTEMIC,
                "STRUCTURAL_TO_SYSTEMIC",
            ),
            identity_proof=_identity(),
            triadic_proof=_triadic(),
            tier_proof=_tier(),
            handoff=handoff,
        )
        assert verdict.local_failure_name == "FORBIDDEN_NEIGHBOR_LEAP"
        assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_valid_path_returns_link_ready_decision() -> None:
    _declare("valid path link ready")
    verdict = _contract().evaluate(
        declaration=_declaration(PartitionKind.STRUCTURAL),
        bridge_proof=_bridge(
            PartitionKind.STRUCTURAL,
            PartitionKind.SYSTEMIC,
            "STRUCTURAL_TO_SYSTEMIC",
        ),
        identity_proof=_identity(
            preserved_properties=("root_form",),
            trace_ref="trace://e1r/test",
        ),
        triadic_proof=_triadic(),
        tier_proof=_tier(
            tier=NecessityTier.HAJI,
            declared_cause="contextual-need",
            evidence_ref="evidence://ok",
            transition_ref="transition://ok",
        ),
        handoff="handoff://structural/systemic",
    )
    assert verdict.partition_allowed is True
    assert verdict.readiness_state is PartitionReadinessState.LINK_READY
    assert verdict.failed_stage is None
    assert verdict.failure_code is None
