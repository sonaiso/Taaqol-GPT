"""Embargo guard tests for rejected runtime anti-patterns (PR #63).

Origin law     : docs/61_PROOF_FAILURE_POLICY_ALIGNMENT.md
Branch         : PR-63 rejected runtime anti-pattern guard
Category       : Category 3 — Regression tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_REJECTION_DOC = (_REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md").relative_to(
    _REPO_ROOT
).as_posix()
_SELF_TEST = (Path(__file__).resolve().relative_to(_REPO_ROOT)).as_posix()
_ORIGIN_LAW = "docs/61_PROOF_FAILURE_POLICY_ALIGNMENT.md"
_CONSTITUTIONAL_CHAIN = ("ProofObjectFailurePolicyAlignment", "RuntimeEmbargo")

FORBIDDEN_FILES = {
    "binding_kernel.py",
    "decision_engine.py",
    "coverage_matrix_v0.1.yaml",
}

FORBIDDEN_PATTERNS = [
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
    "domain_proved: true",
    "unit_proved: true",
    "identity_preserved: true",
    "trace_preserved: true",
    "gate_passed: true",
    "is_preserved: bool = True",
    "identity_preserved: bool = True",
    "if self.evidence:",
    "self.licensed = True",
    "def transform(self, operation: str)",
    "Bridge.translator: str",
    "Gate.condition: str",
    "ComputedVerdict",
    "computed_verdict:",
    "mrk_defaults:",
]

# Existing constitutional files that legitimately contain terms which are
# rejected only as runtime anti-patterns in this embargo branch.
# Maintenance policy: keep this list minimal and explicit; if a path is
# removed/renamed, update this allowlist in the same PR.
_ALLOWED_EXISTING_PATTERN_PATHS: dict[str, set[str]] = {
    "Rank.CERTIFICATE": {
        "src/taaqqul_slot_geometry/core/rank_lattice.py",
        "tests/test_carrier_not_verdict.py",
        "tests/test_constitutional_case_harness.py",
        "tests/test_dalalah_candidates.py",
        "tests/test_formal_shape_word_class.py",
        "tests/test_hukm_candidate.py",
        "tests/test_ifadah_candidate.py",
        "tests/test_mafhum_closure.py",
        "tests/test_mufrad_dalalah_closure.py",
        "tests/test_rank_residual_evidence.py",
        "tests/test_relation_closure.py",
        "tests/test_transition_gate.py",
        "tests/test_weight_carriers.py",
    },
    "Rank.REJECTED": set(),
    # `Rank.REJECTED` is explicitly empty-allowlisted so any new
    # appearance is blocked under this embargo guard.
}


def _tracked_text_files() -> list[Path]:
    files: list[Path] = []
    guarded_roots = {"src", "schemas", "tests", "docs"}
    for path in _REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(_REPO_ROOT)
        top_level = relative.parts[0] if relative.parts else ""
        # YAML is scanned repo-wide because forbidden artifacts can be
        # introduced outside guarded roots (e.g. at top-level tooling paths).
        if top_level in guarded_roots or path.suffix in {".yaml", ".yml"}:
            files.append(path)
    return sorted(set(files))


def test_forbidden_runtime_files_are_absent() -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN_LAW,
        branch_name="forbidden-runtime-files-absent",
        constitutional_chain=_CONSTITUTIONAL_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(),
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

    forbidden = []
    for path in _REPO_ROOT.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_FILES:
            forbidden.append(path.relative_to(_REPO_ROOT).as_posix())
    assert not forbidden, f"BLOCKED: forbidden runtime files found: {sorted(forbidden)}"


def test_forbidden_runtime_patterns_are_blocked() -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN_LAW,
        branch_name="forbidden-runtime-patterns-blocked",
        constitutional_chain=_CONSTITUTIONAL_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(),
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

    violations: list[str] = []

    for path in _tracked_text_files():
        relative = path.relative_to(_REPO_ROOT).as_posix()
        if relative in {_REJECTION_DOC, _SELF_TEST}:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for pattern in FORBIDDEN_PATTERNS:
            if pattern not in content:
                continue

            allowed_paths = _ALLOWED_EXISTING_PATTERN_PATHS.get(pattern, set())
            if relative in allowed_paths:
                continue

            violations.append(f"{relative}: {pattern}")

    assert not violations, "BLOCKED: forbidden runtime anti-patterns found:\n" + "\n".join(
        sorted(violations)
    )
