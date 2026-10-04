"""Constitutional tests for SLGE-SDLC-G0 PR lifecycle enforcement.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-G0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.governance import slge_sdlc_g0_enforcement as gate
from taaqqul_slot_geometry.governance.slge_sdlc_e0_runtime import (
    SLGEE0DecisionState,
    SLGEE0FailureCode,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA = _REPO_ROOT / "schemas" / "governance" / "slge_sdlc_g0_runtime.schema.json"
_CONTRACT = _REPO_ROOT / "governance" / "registry" / "slge_sdlc_g0_runtime.json"
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "ci.yml"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_name=f"SLGE-SDLC-G0 ({branch_note})",
        constitutional_chain=(
            "docs/124",
            "docs/127",
            "docs/128",
            "docs/129",
            "docs/14",
            "governance/registry/slge_sdlc_g0_runtime.json",
            "governance/registry/slge_sdlc_p0_lifecycle_events.json",
            "governance/projections/slge_sdlc_current_lifecycle_state.json",
            "src/taaqqul_slot_geometry/governance/slge_sdlc_e0_runtime.py",
            "src/taaqqul_slot_geometry/governance/slge_sdlc_g0_enforcement.py",
            ".github/workflows/ci.yml",
        ),
        chain_position="SLGE-SDLC-G0",
        origin_law_ref=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md#12-licensed-successor-chain"
        ),
        branch_of_origin=(
            "Repository and pull-request lifecycle declaration enforcement after "
            "the P0 reducer, without opening closure audit."
        ),
        forbidden_shortcut_assertions=(
            "PRDeclaration -> LifecycleApproval",
            "GreenCI -> Closure",
            "Merge -> Closure",
            "ReviewerApproval -> EpistemicTruth",
            "P0ProjectionText -> LifecycleAuthority",
            "CurrentRuntimeAdmission -> HistoricalCertification",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ClosureClaim",
            "SLGE-SDLC-C0",
            "SpellingBridge",
            "CountingRuntime",
            "MorphologyRuntime",
            "ArabicLicensing",
            "V1ClosedClaim",
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


_PR_BODY = (
    "## Constitutional Origin\n\n"
    "- Origin law: `docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
    "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md`\n"
    "- Origin law reference (file#section): "
    "`docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
    "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md#12-licensed-successor-chain`\n\n"
    "## Branch Scope\n\n"
    "- Branch: `SLGE-SDLC-G0`\n"
    "- Branch of origin (the constitutional branch, not just the local label): "
    "repository and PR lifecycle enforcement\n\n"
    "## Chain Position\n\n"
    "- Previous required PR: `SLGE-SDLC-P0`\n"
    "- Current PR (PR-N from docs/14): `SLGE-SDLC-G0`\n"
    "- Next permitted PR: `SLGE-SDLC-C0`\n\n"
    "## Allowed Scope\n\n"
    "- G0 declaration enforcement only\n\n"
    "## Forbidden Scope\n\n"
    "- Closure audit, spelling bridge, counting, morphology, or Arabic licensing\n\n"
    "## Output Boundary\n\n"
    "This PR is allowed to produce:\n"
    "- Lifecycle declaration enforcement decision\n"
    "This PR is forbidden from producing (proven absent in the diff):\n"
    "- ClosureClaim\n"
    "- SLGE-SDLC-C0 closure audit\n\n"
    "## Rank / Residual / Trace Impact\n\n"
    "- Does this PR introduce rank behavior? no\n"
    "- Does this PR introduce residual behavior? yes\n"
    "- Does this PR introduce trace behavior? yes\n\n"
    "## Constitutional Tests\n\n"
    "- `tests/test_slge_sdlc_g0_runtime.py::test_accepts_g0_pr_with_derived_p0_state`\n\n"
    "## Negative Tests\n\n"
    "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_evidence`\n"
    "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_unauthorized_stage_jump`\n"
    "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_trace`\n"
    "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_approval_prose_without_evidence`\n\n"
    "## Residuals After Merge\n\n"
    "- SLGE_C0_CLOSURE_AUDIT_PENDING remains open for SLGE-SDLC-C0.\n"
)


def _evaluate(body: str = _PR_BODY, changed_paths: tuple[str, ...] = ()) -> gate.TransitionDecision:
    _declare("PR lifecycle declaration execution")
    return gate.evaluate_pull_request(
        _REPO_ROOT,
        pull_request_body=body,
        changed_paths=changed_paths,
    )


def test_g0_contract_schema_and_registry_validate() -> None:
    _declare("runtime contract schema")
    schema = json.loads(_SCHEMA.read_text(encoding="utf-8"))
    contract = json.loads(_CONTRACT.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: list(item.path),
    )
    assert not errors, [item.message for item in errors]


def test_accepts_g0_pr_with_derived_p0_state() -> None:
    decision = _evaluate()

    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.failure_codes == ()
    assert decision.next_openings == ("SLGE-SDLC-C0",)
    assert decision.authority_ceiling == "RuntimeAuthority"
    assert decision.rank_ceiling == "E1"
    assert decision.trace_ref
    assert decision.inherited_residual_refs == ("SLGE_C0_CLOSURE_AUDIT_PENDING",)
    assert decision.rank_promotion_granted is False


def test_refuses_missing_evidence() -> None:
    body = _PR_BODY.replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_accepts_g0_pr_with_derived_p0_state`\n",
        "",
    ).replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_evidence`\n",
        "",
    ).replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_unauthorized_stage_jump`\n",
        "",
    ).replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_trace`\n",
        "",
    ).replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_approval_prose_without_evidence`\n",
        "",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.EVIDENCE_INSUFFICIENT in decision.failure_codes


def test_refuses_unauthorized_stage_jump() -> None:
    body = _PR_BODY.replace(
        "- Current PR (PR-N from docs/14): SLGE-SDLC-G0",
        "- Current PR (PR-N from docs/14): SLGE-SDLC-C0",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.TRANSITION_NOT_LICENSED in decision.failure_codes


def test_refuses_missing_trace() -> None:
    body = _PR_BODY.replace(
        "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md#12-licensed-successor-chain",
        "docs/missing_origin_law.md#missing",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.TRACE_LOSS in decision.failure_codes


def test_refuses_approval_prose_without_evidence() -> None:
    body = _PR_BODY.replace(
        "tests/test_slge_sdlc_g0_runtime.py",
        "tests/unverified_lifecycle_evidence.py",
    ).replace(
        "- `tests/unverified_lifecycle_evidence.py::test_accepts_g0_pr_with_derived_p0_state`\n",
        "- Caller gate approval: APPROVED\n",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.EVIDENCE_INSUFFICIENT in decision.failure_codes
    assert SLGEE0FailureCode.GATE_NOT_APPROVED in decision.failure_codes


def test_refuses_spelling_counting_or_morphology_scope() -> None:
    decision = _evaluate(changed_paths=("src/taaqqul_slot_geometry/weight/spelling_bridge.py",))

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.GATE_NOT_APPROVED in decision.failure_codes


def test_refuses_closure_output_in_allowed_boundary() -> None:
    body = _PR_BODY.replace(
        "- Lifecycle declaration enforcement decision\n",
        "- Lifecycle declaration enforcement decision\n- ClosureClaim\n",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.GATE_NOT_APPROVED in decision.failure_codes


def test_g0_residual_remains_open_and_closure_is_forbidden() -> None:
    _declare("G0 does not claim C0 closure")
    contract = json.loads(_CONTRACT.read_text(encoding="utf-8"))
    assert "ClosureClaim" in contract["forbidden_outputs"]
    assert contract["residual_policy"]["remains_open"] == [
        "SLGE_C0_CLOSURE_AUDIT_PENDING"
    ]
    decision = _evaluate()
    assert decision.next_openings == ("SLGE-SDLC-C0",)
    assert decision.inherited_residual_refs == ("SLGE_C0_CLOSURE_AUDIT_PENDING",)


def test_g0_workflow_runs_gate_after_tests() -> None:
    _declare("PR execution-boundary integration")
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    pytest_position = workflow.index("run: pytest")
    gate_position = workflow.index("Enforce lifecycle PR declarations")
    assert pytest_position < gate_position
    assert "if: github.event_name == 'pull_request'" in workflow
    assert "GITHUB_EVENT_PATH" in workflow
