"""Constitutional tests for SLGE-SDLC-G0 PR lifecycle enforcement.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-G0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
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
    "- C0 closure-audit output\n\n"
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
        "- Current PR (PR-N from docs/14): `SLGE-SDLC-G0`",
        "- Current PR (PR-N from docs/14): `SLGE-SDLC-C0`",
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


def test_refuses_inaccurate_impact_declarations() -> None:
    declarations = (
        ("rank behavior", "no", "yes"),
        ("residual behavior", "yes", "no"),
        ("trace behavior", "yes", "no"),
    )
    for impact, expected, actual in declarations:
        body = _PR_BODY.replace(
            f"- Does this PR introduce {impact}? {expected}",
            f"- Does this PR introduce {impact}? {actual}",
        )
        decision = _evaluate(body)

        assert decision.state is SLGEE0DecisionState.REFUSED
        assert SLGEE0FailureCode.GATE_NOT_APPROVED in decision.failure_codes


def test_refuses_tests_in_wrong_sections() -> None:
    negative_test = (
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_evidence`\n"
    )
    body = _PR_BODY.replace(negative_test, "").replace(
        "## Negative Tests",
        f"{negative_test}\n## Negative Tests",
    )
    decision = _evaluate(body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.EVIDENCE_INSUFFICIENT in decision.failure_codes


def test_refuses_changes_outside_g0_allowed_paths() -> None:
    decision = _evaluate(changed_paths=("src/unrelated/runtime.py",))

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.GATE_NOT_APPROVED in decision.failure_codes


def test_accepts_changes_inside_g0_allowed_paths() -> None:
    decision = _evaluate(changed_paths=gate.G0_ALLOWED_CHANGED_PATHS)

    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.failure_codes == ()


def test_refuses_mismatched_recorded_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    event, recorded_decision, current = gate._g0_transition(_REPO_ROOT)
    monkeypatch.setattr(
        gate,
        "_g0_transition",
        lambda _root: (event, {**recorded_decision, "attempt_id": "ATTEMPT-UNRELATED"}, current),
    )

    decision = _evaluate()

    assert decision.state is SLGEE0DecisionState.REFUSED
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


def test_accepts_explicit_c0_closure_audit_prohibition() -> None:
    decision = _evaluate()

    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.failure_codes == ()


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
    assert "types: [opened, synchronize, reopened, edited]" in workflow


# --- Amendment-108: PROOF-EVIDENCE-L1 lane inside G0 ---------------------------

_LANE_PROOF_FILES = (
    "proofs/arabic/rules.json",
    "proofs/arabic/check.sh",
    "proofs/arabic/README_AR.md",
    "proofs/arabic/Arabic/Core.lean",
)
_LANE_CHANGED_PATHS = (*_LANE_PROOF_FILES, ".github/workflows/arabic-proof.yml")
_LANE_REPO_FILES = (
    "governance/registry/slge_sdlc_g0_runtime.json",
    "governance/registry/slge_sdlc_p0_lifecycle_events.json",
    "governance/projections/slge_sdlc_current_lifecycle_state.json",
    "schemas/governance/slge_sdlc_p0_lifecycle_events.schema.json",
    "schemas/governance/slge_sdlc_current_lifecycle_state.schema.json",
    "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md",
    "docs/127_SLGE_SDLC_E0_LIFECYCLE_EXECUTION_ENGINE.md",
    "docs/128_SLGE_SDLC_P0_DETERMINISTIC_LIFECYCLE_PROJECTION.md",
    "docs/14_PR_CHAIN_ROADMAP.md",
    gate.G0_RUNTIME_PATH,
    gate.G0_TEST_PATH,
)

_LANE_PR_BODY = (
    _PR_BODY.replace(
        "- Branch: `SLGE-SDLC-G0`\n",
        "- Branch: `SLGE-SDLC-G0`\n- Lane: `PROOF-EVIDENCE-L1`\n",
    )
    .replace(
        "- Next permitted PR: `SLGE-SDLC-C0`\n",
        "- Next permitted PR: `SLGE-SDLC-C0`\n"
        "- ProofPackageCheck: `bash proofs/arabic/check.sh`\n",
    )
    .replace(
        "- G0 declaration enforcement only\n",
        "- PROOF-EVIDENCE-L1 evidence lane inside G0: `proofs/arabic/**` and its workflow only\n",
    )
    .replace(
        "- Closure audit, spelling bridge, counting, morphology, or Arabic licensing\n",
        "- Closure audit, spelling bridge, counting, morphology, Arabic licensing, "
        "or any runtime bridge from proofs/arabic\n",
    )
    .replace(
        "- Lifecycle declaration enforcement decision\n",
        "- Formal-proof evidence package (Lean 4) with pinned source hashes\n",
    )
    .replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_accepts_g0_pr_with_derived_p0_state`\n",
        "- `tests/test_slge_sdlc_g0_runtime.py::test_lane_accepts_proof_evidence_paths`\n",
    )
    .replace(
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_evidence`\n"
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_unauthorized_stage_jump`\n"
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_missing_trace`\n"
        "- `tests/test_slge_sdlc_g0_runtime.py::test_refuses_approval_prose_without_evidence`\n",
        "- `tests/test_slge_sdlc_g0_runtime.py::test_lane_refuses_g0_only_paths`\n"
        "- `tests/test_slge_sdlc_g0_runtime.py::test_lane_refuses_missing_proof_package_check`\n"
        "- `tests/test_slge_sdlc_g0_runtime.py::test_lane_refuses_closure_claim`\n",
    )
    .replace(
        "- SLGE_C0_CLOSURE_AUDIT_PENDING remains open for SLGE-SDLC-C0.\n",
        "- SLGE_C0_CLOSURE_AUDIT_PENDING remains open for SLGE-SDLC-C0.\n"
        "- ARABIC_PROOF_RUNTIME_BRIDGE_PENDING is added and remains open.\n",
    )
)


@pytest.fixture
def lane_repo(tmp_path: Path) -> Path:
    """Minimal repository root with the G0 inputs plus a dummy proofs/arabic package."""

    root = tmp_path / "repo"
    for rel_path in _LANE_REPO_FILES:
        target = root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_REPO_ROOT / rel_path, target)
    for rel_path in _LANE_CHANGED_PATHS:
        target = root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("placeholder\n", encoding="utf-8")
    return root


def _evaluate_lane(
    root: Path,
    body: str = _LANE_PR_BODY,
    changed_paths: tuple[str, ...] = _LANE_CHANGED_PATHS,
) -> gate.LaneDecision:
    _declare("PROOF-EVIDENCE-L1 lane evaluation")
    decision = gate.evaluate_pull_request(
        root,
        pull_request_body=body,
        changed_paths=changed_paths,
    )
    assert isinstance(decision, gate.LaneDecision)
    return decision


def test_lane_accepts_proof_evidence_paths(lane_repo: Path) -> None:
    decision = _evaluate_lane(lane_repo)

    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.failure_codes == ()
    assert decision.lane == "PROOF-EVIDENCE-L1"
    assert decision.trace_ref == "proofs/arabic/rules.json"
    assert set(decision.evidence_refs) >= {
        "proofs/arabic/rules.json",
        "proofs/arabic/check.sh",
        "proofs/arabic/README_AR.md",
    }


def test_lane_refuses_g0_only_paths(lane_repo: Path) -> None:
    for intruder in (
        "src/taaqqul_slot_geometry/weight/x.py",
        "tests/test_new.py",
        "governance/registry/slge_sdlc_g0_runtime.json",
        "governance/projections/current_state.json",
        ".github/workflows/ci.yml",
        "schemas/governance/slge_sdlc_g0_runtime.schema.json",
        "proofs/arabic/../../src/evil.py",
        "proofs/other/thing.lean",
    ):
        decision = _evaluate_lane(lane_repo, changed_paths=(*_LANE_CHANGED_PATHS, intruder))

        assert decision.state is SLGEE0DecisionState.REFUSED, intruder
        assert gate.G0LaneFailureCode.LANE_SCOPE_VIOLATION in decision.failure_codes, intruder


def test_lane_refuses_missing_proof_package_check(lane_repo: Path) -> None:
    body = _LANE_PR_BODY.replace("- ProofPackageCheck: `bash proofs/arabic/check.sh`\n", "")
    decision = _evaluate_lane(lane_repo, body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert gate.G0LaneFailureCode.LANE_DECLARATION_MISSING in decision.failure_codes


def test_lane_refuses_closure_claim(lane_repo: Path) -> None:
    body = _LANE_PR_BODY.replace(
        "- Formal-proof evidence package (Lean 4) with pinned source hashes\n",
        "- Formal-proof evidence package (Lean 4) with pinned source hashes\n- ClosureClaim\n",
    )
    decision = _evaluate_lane(lane_repo, body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert gate.G0LaneFailureCode.LANE_OUTPUT_BOUNDARY_VIOLATION in decision.failure_codes

    body = _LANE_PR_BODY.replace(
        "- SLGE_C0_CLOSURE_AUDIT_PENDING remains open for SLGE-SDLC-C0.\n",
        "- SLGE_C0_CLOSURE_AUDIT_PENDING resolved by the proof package.\n",
    )
    decision = _evaluate_lane(lane_repo, body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert gate.G0LaneFailureCode.LANE_RESIDUAL_POLICY_VIOLATION in decision.failure_codes


def test_lane_refuses_missing_evidence_files(lane_repo: Path) -> None:
    (lane_repo / "proofs/arabic/rules.json").unlink()
    decision = _evaluate_lane(lane_repo)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert gate.G0LaneFailureCode.LANE_EVIDENCE_INSUFFICIENT in decision.failure_codes
    assert gate.G0LaneFailureCode.LANE_TRACE_LOSS in decision.failure_codes


def test_lane_refuses_unregistered_lane(lane_repo: Path) -> None:
    body = _LANE_PR_BODY.replace("- Lane: `PROOF-EVIDENCE-L1`", "- Lane: `RUNTIME-BRIDGE-L9`")
    decision = _evaluate_lane(lane_repo, body)

    assert decision.state is SLGEE0DecisionState.REFUSED
    assert decision.failure_codes == (gate.G0LaneFailureCode.LANE_NOT_REGISTERED,)


def test_lane_decision_opens_no_successor_and_keeps_c0_residual_open(lane_repo: Path) -> None:
    projection = lane_repo / "governance/projections/slge_sdlc_current_lifecycle_state.json"
    before = projection.read_bytes()
    decision = _evaluate_lane(lane_repo)
    after = projection.read_bytes()

    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.opens_successor is False
    assert decision.next_openings == ()
    assert decision.rank_change == "none"
    assert decision.authority_change == "none"
    assert decision.lifecycle_projection_changed is False
    assert decision.rank_promotion_granted is False
    assert decision.consumed_residual_refs == ()
    assert decision.inherited_residual_refs == ("SLGE_C0_CLOSURE_AUDIT_PENDING",)
    assert decision.added_residual_refs == ("ARABIC_PROOF_RUNTIME_BRIDGE_PENDING",)
    assert before == after

    contract = json.loads(_CONTRACT.read_text(encoding="utf-8"))
    lane = contract["lanes"]["PROOF-EVIDENCE-L1"]
    assert lane["decision_effects"]["opens_successor"] is False
    assert lane["decision_effects"]["resolves_residuals"] == []
    assert "ClosureClaim" in lane["forbidden_outputs"]
    assert "ArabicLicensing" in lane["forbidden_outputs"]
    assert contract["residual_policy"]["remains_open"] == ["SLGE_C0_CLOSURE_AUDIT_PENDING"]
    assert contract["allowed_changed_paths"] == list(gate.G0_ALLOWED_CHANGED_PATHS)
    with pytest.raises(gate.G0EnforcementError):
        gate.LaneDecision(
            lane="PROOF-EVIDENCE-L1",
            attempt_id="x",
            state=SLGEE0DecisionState.APPROVED,
            failure_codes=(),
            authority_ceiling="RuntimeAuthority",
            rank_ceiling="E1",
            inherited_residual_refs=(),
            added_residual_refs=(),
            evidence_refs=(),
            trace_ref="proofs/arabic/rules.json",
            next_openings=("SLGE-SDLC-C0",),
        )


def test_non_lane_body_is_unaffected_by_lane_contract() -> None:
    decision = _evaluate(changed_paths=gate.G0_ALLOWED_CHANGED_PATHS)

    assert not isinstance(decision, gate.LaneDecision)
    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.next_openings == ("SLGE-SDLC-C0",)
    refused = _evaluate(changed_paths=("proofs/arabic/rules.json",))
    assert refused.state is SLGEE0DecisionState.REFUSED
    assert SLGEE0FailureCode.GATE_NOT_APPROVED in refused.failure_codes


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def test_changed_paths_do_not_hide_renames_into_lane_scope(tmp_path: Path) -> None:
    _declare("rename-hiding regression")
    repo = tmp_path / "scratch"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    governed = repo / "governance/registry/slge_sdlc_g0_runtime.json"
    governed.parent.mkdir(parents=True)
    governed.write_text('{"version": "1.0.0"}\n', encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "base")
    base = _git(repo, "rev-parse", "HEAD").strip()
    _git(repo, "checkout", "-q", "-b", "lane")
    (repo / "proofs/arabic").mkdir(parents=True)
    _git(repo, "mv", "governance/registry/slge_sdlc_g0_runtime.json", "proofs/arabic/moved.json")
    _git(repo, "commit", "-q", "-m", "move")
    head = _git(repo, "rev-parse", "HEAD").strip()

    changed = gate._changed_paths(base, head, repo)

    assert "governance/registry/slge_sdlc_g0_runtime.json" in changed
    assert "proofs/arabic/moved.json" in changed
    assert gate._lane_scope_violations(
        {
            "allowed_path_globs": ["proofs/arabic/**"],
            "forbidden_path_prefixes": ["governance/registry/slge_sdlc_g0_runtime.json"],
        },
        changed,
    ) == ("governance/registry/slge_sdlc_g0_runtime.json",)


def test_changed_paths_reject_parent_segments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _declare("path traversal rejection")

    class _Result:
        stdout = "proofs/arabic/../../src/x.py\n"

    monkeypatch.setattr(gate.subprocess, "run", lambda *args, **kwargs: _Result())
    with pytest.raises(gate.G0EnforcementError) as excinfo:
        gate._changed_paths("a", "b", tmp_path)
    assert excinfo.value.code == "PR_PATH_UNSAFE"
