"""Constitutional surface tests for docs/90 governor/proof contract hardening.

Origin law          : docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
Branch name         : DOC90-HARDENING-R4
Constitutional chain: docs/12 -> docs/13 -> docs/90
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import re
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOC_90 = _REPO_ROOT / "docs" / "90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        branch_name=f"DOC90-HARDENING-R4 ({branch_note})",
        constitutional_chain=("docs/12", "docs/13", "docs/90"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "RatificationClaim",
            "ChainMutationClaim",
            "ScopeCollapseClaim",
        ),
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


def _body() -> str:
    return _DOC_90.read_text(encoding="utf-8")


def _section(body: str, section_number: int) -> str:
    pattern = re.compile(
        rf"^## {section_number}\).*?(?=^## \d+\)|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    assert match is not None, f"docs/90 missing section {section_number}"
    return match.group(0)


def test_preflight_result_variants_carry_typed_payloads() -> None:
    _declare("typed preflight result payloads")
    body = _body()
    section_1 = _section(body, 1)
    assert "PreflightResult =" in section_1
    assert "PermitGranted(permit: TransitionPermit)" in section_1
    assert "PreflightRejected(failure: PreflightFailure)" in section_1
    assert "PreflightSuspended(suspension: SuspensionRecord)" in section_1
    assert "Permit(p)" not in section_1


def test_top_level_cycle_uses_stage_execute() -> None:
    _declare("top-level cycle uses stage execute")
    body = _body()
    section_1 = _section(body, 1)
    assert "Proposal\n-> PreflightResult" in section_1
    assert "PermitGranted\n-> StageExecute\n-> ExecutionCandidate\n-> PostflightResult" in section_1
    assert "PostflightApproved\n-> AtomicCommit\n-> CommittedArtifact" in section_1
    assert "EngineExecution" not in section_1
    assert "LayerProposal" not in section_1


def test_revoke_is_not_a_postflight_result() -> None:
    _declare("revoke/reopen are lifecycle transitions")
    body = _body()
    section_1 = _section(body, 1)
    postflight_block = section_1.split("PostflightResult =", maxsplit=1)[1]
    assert "PostflightApproved(approved: ApprovedPostflight)" in postflight_block
    assert "PostflightRejected(failure: PostflightFailure)" in postflight_block
    assert "PostflightSuspended(suspension: SuspensionRecord)" in postflight_block
    assert "Revoke" not in postflight_block
    assert "Reopen" not in postflight_block


def test_committed_state_requires_permitted_and_approved() -> None:
    _declare("legal state-combination invariants")
    body = _body()
    section_5 = _section(body, 5)
    assert "Committed(x)" in section_5
    assert "=> Preflight(x) = PERMITTED and Postflight(x) = APPROVED" in section_5
    assert "Preflight(x) in {REJECTED, SUSPENDED}" in section_5
    assert "=> Commit(x) = UNCOMMITTED" in section_5
    assert "Lifecycle(x) in {ACTIVE, REOPENED, REVOKED, SUPERSEDED, ARCHIVED}" in section_5
    assert "=> Commit(x) = COMMITTED" in section_5


def test_claim_validity_uses_computed_rank_not_ceiling() -> None:
    _declare("claim rank must be computed not ceiling-only")
    body = _body()
    section_8 = _section(body, 8)
    assert "ComputedRank(H) >= RequiredRank(c)" in section_8
    assert "ComputedRank(H) <= DeclaredRankCeiling(H)" in section_8
    assert "ComputedRank(H) = meet(" in section_8
    assert "RankCeiling(H) >= RequiredRank(c)" not in section_8


def test_word_precomp_path_splits_weight_formal_from_bridge() -> None:
    _declare("word->precomp path includes formal weight + ontology bridge split")
    body = _body()
    section_9 = _section(body, 9)
    assert "-> WEIGHT-FORMAL-L0 -> WEIGHT-ONTOLOGY-BRIDGE-L0" in section_9
    assert "-> WEIGHT-L0R" not in section_9


def test_weight_bridge_is_typed_compatibility_not_semantic_generation() -> None:
    _declare("weight/ontology bridge is typed compatibility only")
    body = _body()
    section_10 = _section(body, 10)
    assert "Ontology != Weight" in section_10
    assert "Weight != Meaning" in section_10
    assert "TypedCompatibility (not SemanticGeneration)" in section_10
    assert "`WEIGHT-FORMAL-L0` emits readiness directions" in section_10
    assert (
        "`WEIGHT-ONTOLOGY-BRIDGE-L0` only licenses admissible typed anchor candidates."
        in section_10
    )
    assert "WeightedEntityAnchorCandidate" in section_10
    assert "WeightedReferenceInterfaceCandidate" in section_10
    assert "ActualThing" in section_10
    assert "ExternalTruth" in section_10


def test_weight_bridge_declares_k0_hardening_constraints() -> None:
    _declare("weight/ontology bridge k0 hardening constraints")
    body = _body()
    section_10 = _section(body, 10)
    for marker in (
        "NoWeightedAnchor without ActiveOntologySchema.",
        "No bridge output from weight image alone.",
        "FormalFit DOES_NOT_IMPLY LexicalizedReading.",
        "Compat:",
        "FormalWeightCandidate",
        "OntologySchemaCandidate",
        "-> BridgeAssessment",
        "BridgeAssessment =",
        "<Decision, Rank, Conflict, Residuals, AllowedAnchors>",
        "DeclaredWeightKind",
        "TypedCompatibilityRule",
        "LexicalEvidence",
        "Missing(ActiveOntologySchema) -> REFUSED",
        "Missing(DeclaredWeightKind) -> REFUSED",
        "Missing(TypedCompatibilityRule) -> REFUSED",
        "JAMID_STEM",
        "SOURCE",
        "DERIVATIONAL_NOUN",
        "VERB_FORM",
        "TRANSFORMATION_PATTERN",
        "PLURAL",
        "DIMINUTIVE",
        "NISBA",
        "StructuralCompatibility is not LexicalAttestation.",
        "LexicalAttestation is not UsageCompatibility.",
        "CompatibleAlternatives + Underdetermined + Suspended",
        "HARF-PATH and MABNI-PATH do not open WEIGHT-ONTOLOGY-BRIDGE-L0 by default.",
        "dependent weighted anchors are revoked",
        "bridge status reopens to pending",
    ):
        assert marker in section_10


def test_proof_claim_requires_derivation_hypergraph() -> None:
    _declare("provenance path and claim proof graph are separated")
    body = _body()
    section_8 = _section(body, 8)
    assert "ProvenanceReachable(x) requires a ProvenancePath P" in section_8
    assert (
        "ValidClaim(c) only if there exists a WellFoundedProofDerivationHypergraph H"
        in section_8
    )
    assert "ProofDerivationSubgraph H" not in section_8
    assert "Rank(path) = meet(" not in section_8


def test_residual_disposition_does_not_encode_conflict() -> None:
    _declare("conflict stays separate from residual disposition")
    body = _body()
    section_5 = _section(body, 5)
    assert "ResidualDisposition:" in section_5
    assert "CONTRADICTORY" not in section_5
    assert "class ConflictState(str, Enum):" in section_5
    assert 'CONTRADICTION = "contradiction"' in section_5
    assert "Conflict != Residual" in section_5


def test_commit_consumes_permit_atomically() -> None:
    _declare("atomic consume-and-commit law")
    body = _body()
    section_6 = _section(body, 6)
    section_13 = _section(body, 13)
    assert "consumption_limit: Literal[1]" in section_6
    assert "AtomicCommit(permit, candidate) =" in section_13
    assert "ConsumePermitNonce" in section_13
    assert "ALL_OR_NOTHING" in section_13
    assert "CommitConflict" in section_13
    assert "-> ReopenFromFreshSnapshot" in section_13
    assert "single_use: bool" not in section_6


def test_output_origin_distinguishes_provenance_from_evidence() -> None:
    _declare("origin/evidence wording is unified")
    body = _body()
    section_7 = _section(body, 7)
    section_14 = _section(body, 14)
    assert "Every output has provenance/execution origin." in section_7
    assert "Every committed epistemic claim has evidentiary support." in section_7
    assert "Every output has provenance/execution origin." in section_14
    assert "Every committed epistemic claim has evidentiary support." in section_14
    assert "Every output has evidentiary/execution origin." not in body


def test_pure_derivation_is_not_confused_with_effectful_execution() -> None:
    _declare("pure derivation remains allowed without permit")
    body = _body()
    section_1 = _section(body, 1)
    section_14 = _section(body, 14)
    assert "NoPermit => NoEffectfulExecution" in section_1
    assert "NoPermit => NoCanonicalMutation" in section_1
    assert "No governed effectful execution without a matching permit." in section_14
    assert "No canonical mutation before approved postflight and atomic commit." in section_14
    assert "No execution without preflight." not in body
