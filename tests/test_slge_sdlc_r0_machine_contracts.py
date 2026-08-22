"""Constitutional tests for SLGE-SDLC-R0 machine-contract staging.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-R0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.governance import repo_org_projection as projector
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_GOVERNANCE = _REPO_ROOT / "governance"
_REGISTRY = _GOVERNANCE / "registry"
_SCHEMAS = _REPO_ROOT / "schemas" / "governance"
_DOCS = _REPO_ROOT / "docs"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_name=f"SLGE-SDLC-R0 ({branch_note})",
        constitutional_chain=(
            "docs/124",
            "schemas/governance/slge_sdlc_r0_contracts.schema.json",
            "governance/registry/slge_sdlc_r0_contracts.json",
            "src/taaqqul_slot_geometry/governance/repo_org_projection.py",
            "governance/projections/current_state.json",
        ),
        chain_position="SLGE-SDLC-R0",
        origin_law_ref=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_of_origin=(
            "Machine-readable lifecycle contracts and referential integrity checks "
            "without lifecycle transition execution runtime."
        ),
        forbidden_shortcut_assertions=(
            "LawDocument -> RuntimeAdmission",
            "RatifiedLaw -> EmpiricalTruth",
            "SchemaValidity -> TransitionApproval",
            "RegistryExistence -> Closure",
            "ArtifactRegistration -> EpistemicValidation",
            "EvidenceRequirementDefinition -> EvidenceSatisfaction",
            "GateReference -> GateApproval",
            "LifecycleSlotDefinition -> RuntimeState",
            "MCLTContractDefinition -> SuccessfulMCLT",
            "READMEText -> Authority",
            "HistoricalOrder -> DependencyOrder",
            "Merge -> Closure",
            "GreenCI -> Closure",
            "ReviewerApproval -> EpistemicTruth",
            "LocalSuccess -> GeneralInvariant",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "LifecycleRuntimeExecution",
            "TransitionApproval",
            "ClosureClaim",
            "RuntimeAdmissionClaim",
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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_slge_r0_contract_registry_validates_against_schema() -> None:
    _declare("schema surface validation")
    schema = _load_json(_SCHEMAS / "slge_sdlc_r0_contracts.schema.json")
    payload = _load_json(_REGISTRY / "slge_sdlc_r0_contracts.json")
    validator = Draft202012Validator(schema)

    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    assert not errors, [e.message for e in errors]


def test_slge_r0_semantic_contract_integrity_passes() -> None:
    _declare("semantic contract integrity")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    projector._validate_semantics(_REPO_ROOT, inputs)


def test_lifecycle_axes_are_independent_and_non_overloaded() -> None:
    _declare("maturity-axis independence")
    payload = _load_json(_REGISTRY / "slge_sdlc_r0_contracts.json")
    dimensions = {
        item["dimension_id"]: set(item["allowed_values"])
        for item in payload["maturity_dimensions"]
    }
    artifact = next(
        item for item in payload["project_artifacts"] if item["artifact_id"] == "DOC-124"
    )

    assert artifact["current_lifecycle_slot_ref"] in dimensions["LifecycleSlot"]
    assert artifact["constitutional_maturity_ref"] in dimensions["ConstitutionalMaturity"]
    assert artifact["runtime_maturity_ref"] in dimensions["RuntimeMaturity"]
    assert artifact["release_maturity_ref"] in dimensions["ReleaseMaturity"]
    assert artifact["generality_scope_ref"] in dimensions["GeneralityScope"]


def test_constitutional_and_empirical_evidence_are_distinct() -> None:
    _declare("constitutional-vs-empirical evidence split")
    payload = _load_json(_REGISTRY / "slge_sdlc_r0_contracts.json")
    requirements = payload["evidence_requirements"]

    constitutional = next(
        item
        for item in requirements
        if item["evidence_requirement_id"] == "EVR-SLGE-L0-RATIFICATION"
    )
    empirical = next(
        item
        for item in requirements
        if item["evidence_requirement_id"] == "EVR-SLGE-L0-EMPIRICAL"
    )

    assert constitutional["evidence_kind"] == "ConstitutionalRatificationEvidence"
    assert constitutional["verdict"] == "PROVEN"
    assert empirical["evidence_kind"] == "EpistemicClaimEvidence"
    assert empirical["verdict"] == "DEFERRED"


def test_projection_law_authority_is_not_projection_runtime_authority() -> None:
    _declare("authority separation")
    artifacts = _load_json(_REGISTRY / "slge_sdlc_r0_contracts.json")["project_artifacts"]
    doc_124 = next(item for item in artifacts if item["artifact_id"] == "DOC-124")
    repo_org_p0 = next(item for item in artifacts if item["artifact_id"] == "REPO-ORG-P0")

    assert "LawAuthority" in doc_124["authority_roles"]
    assert "ProjectionRuntimeAuthority" not in doc_124["authority_roles"]
    assert "ProjectionRuntimeAuthority" in repo_org_p0["authority_roles"]


def test_r0_transition_contract_does_not_open_runtime() -> None:
    _declare("contract-only runtime boundary")
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]
    branch_statuses = _load_json(_REGISTRY / "branches.json")["branch_statuses"]

    r0_runtime = next(item for item in runtime_map if item["branch_id"] == "SLGE-SDLC-R0")
    m0_branch = next(item for item in branch_statuses if item["branch_id"] == "SLGE-SDLC-M0")

    assert r0_runtime["runtime_status"] == "ABSENT"
    assert m0_branch["constitutional_status"] == "PROPOSED"


def test_semantic_validation_refuses_unknown_transition_slot() -> None:
    _declare("unknown lifecycle slot refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_r0_contracts"]["lifecycle_transition_contracts"][0][
        "to_slot_ref"
    ] = "SLGE-SDLC-Z9"

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected UNKNOWN_LIFECYCLE_SLOT"
    except projector.ProjectionError as exc:
        assert exc.code == "UNKNOWN_LIFECYCLE_SLOT"


def test_semantic_validation_refuses_duplicate_lifecycle_ids() -> None:
    _declare("duplicate lifecycle identifier refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_r0_contracts"]["lifecycle_slots"].append(
        copy.deepcopy(tampered["slge_r0_contracts"]["lifecycle_slots"][0])
    )

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected DUPLICATE_LIFECYCLE_ID"
    except projector.ProjectionError as exc:
        assert exc.code == "DUPLICATE_LIFECYCLE_ID"


def test_chain_and_docs_announce_r0_current_and_m0_next() -> None:
    _declare("chain successor discipline")
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")

    assert "Amendment-103 (SLGE-SDLC-R0 — Lifecycle Registry and Machine Contracts)" in chain
    assert "Immediate successor after `SLGE-SDLC-R0` is" in chain
    assert "`SLGE-SDLC-M0` only." in chain
