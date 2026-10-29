"""Synthetic gate tests, never independent review or a real admission.

Origin: docs/11, docs/13, PARALLEL-PROOF-READ-L0 proposal.
Branch: joint admission candidate. Chain: bound evidence -> conjunctive decision.
Expected outputs: JOINT_ACCEPTED only for the complete simulated contract;
BLOCKED otherwise. No rank/linguistic output. Every blocker remains visible.
"""

import copy
import unittest

from joint_admission import REVIEW_ITEMS, assess
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank


def assert_admission_case(
    branch_name: str, data: dict, expected_state: ClosureState
) -> dict:
    result = assess(data)
    state = (
        ClosureState.MINIMALLY_CLOSED
        if result["decision"] == "JOINT_ACCEPTED"
        else ClosureState.BLOCKED
    )
    failure_code = (
        None if state is ClosureState.MINIMALLY_CLOSED else FailureCode.UNLICENSED_OPENING
    )
    case = ConstitutionalTestCase(
        origin_law="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        branch_name=f"A116 joint admission: {branch_name}",
        constitutional_chain=(
            "proof and review evidence",
            "governance approval",
            "joint admission",
        ),
        expected_state=expected_state,
        expected_failure_code=(
            None
            if expected_state is ClosureState.MINIMALLY_CLOSED
            else FailureCode.UNLICENSED_OPENING
        ),
        forbidden_outputs=("linguistic_license", "runtime_rank_promotion"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    chain_result = ConstitutionalChainResult(
        state=state,
        failure_code=failure_code,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(
            output
            for output in ("linguistic_license", "runtime_rank_promotion")
            if result.get(output)
        ),
    )
    assert_constitutional_case(case, chain_result)
    return result


def fixture():
    head, base, body = "a" * 40, "b" * 40, "c" * 64
    review = {
        "id": 1,
        "user": {"login": "independent", "type": "User"},
        "state": "APPROVED",
        "commit_id": head,
        "body": "\n".join(
            [
                f"Proof-Head: {head}",
                f"Proof-Base: {base}",
                f"PR-Body-SHA256: {body}",
                *(f"- [x] {item}" for item in REVIEW_ITEMS),
            ]
        ),
    }
    return {
        "head": head,
        "base": base,
        "body_sha256": body,
        "proof_run_id": 1,
        "proof_passed": True,
        "fresh": True,
        "contributors_complete": True,
        "contributors": ["writer"],
        "author": "owner",
        "eligible_reviewers": ["independent"],
        "reviews": [review],
        "governance_state": "APPROVED",
        "governance_detail": "synthetic test only",
    }


class JointAdmissionTests(unittest.TestCase):
    def test_complete_simulated_contract(self):
        result = assert_admission_case(
            "complete simulated contract", fixture(), ClosureState.MINIMALLY_CLOSED
        )
        self.assertEqual(result["decision"], "JOINT_ACCEPTED")
        self.assertFalse(result["linguistic_license"])
        self.assertFalse(result["runtime_rank_promotion"])

    def test_each_required_leg_is_necessary(self):
        for key, value, blocker in [
            ("proof_passed", False, "PROOF_NOT_VERIFIED_AT_HEAD"),
            ("governance_state", "REFUSED", "GOVERNANCE_NOT_APPROVED"),
            ("reviews", [], "INDEPENDENT_REVIEW_MISSING_OR_STALE"),
            ("fresh", False, "SNAPSHOT_CHANGED"),
            ("contributors_complete", False, "CONTRIBUTOR_IDENTITY_UNRESOLVED"),
        ]:
            with self.subTest(key=key):
                data = fixture()
                data[key] = value
                result = assert_admission_case(
                    f"required leg {key} missing", data, ClosureState.BLOCKED
                )
                self.assertEqual(result["decision"], "BLOCKED")
                self.assertIn(blocker, result["blockers"])

    def test_proof_success_alone_never_licenses(self):
        data = fixture()
        data.update(reviews=[], governance_state="REFUSED")
        result = assert_admission_case(
            "proof success without review or governance",
            data,
            ClosureState.BLOCKED,
        )
        self.assertEqual(len(result["blockers"]), 2)

    def test_head_base_and_body_mutations_invalidate_review(self):
        for key in ("head", "base", "body_sha256"):
            data = fixture()
            data[key] = "d" * len(data[key])
            result = assert_admission_case(
                f"review invalidated by {key} mutation", data, ClosureState.BLOCKED
            )
            self.assertEqual(result["decision"], "BLOCKED")

    def test_old_commit_review_is_rejected(self):
        data = fixture()
        data["reviews"][0]["commit_id"] = "e" * 40
        result = assert_admission_case(
            "old-commit review rejected", data, ClosureState.BLOCKED
        )
        self.assertEqual(result["decision"], "BLOCKED")

    def test_author_and_contributor_are_not_independent(self):
        for field in ("author", "contributors"):
            data = fixture()
            data[field] = "independent" if field == "author" else ["INDEPENDENT"]
            result = assert_admission_case(
                f"{field} cannot be independent reviewer", data, ClosureState.BLOCKED
            )
            self.assertEqual(result["decision"], "BLOCKED")

    def test_unprivileged_or_bot_review_is_rejected(self):
        data = fixture()
        data["eligible_reviewers"] = []
        result = assert_admission_case(
            "unprivileged reviewer rejected", data, ClosureState.BLOCKED
        )
        self.assertEqual(result["decision"], "BLOCKED")
        data = fixture()
        data["reviews"][0]["user"]["type"] = "Bot"
        result = assert_admission_case(
            "bot review rejected", data, ClosureState.BLOCKED
        )
        self.assertEqual(result["decision"], "BLOCKED")

    def test_missing_review_obligation_is_rejected(self):
        for item in REVIEW_ITEMS:
            data = fixture()
            data["reviews"][0]["body"] = data["reviews"][0]["body"].replace(
                f"- [x] {item}", f"- [ ] {item}"
            )
            result = assert_admission_case(
                f"missing review obligation {item}", data, ClosureState.BLOCKED
            )
            self.assertEqual(result["decision"], "BLOCKED")

    def test_dismissal_and_changes_request_supersede_approval(self):
        for state in ("DISMISSED", "CHANGES_REQUESTED"):
            data = fixture()
            later = copy.deepcopy(data["reviews"][0])
            later.update(id=2, state=state)
            data["reviews"].append(later)
            result = assert_admission_case(
                f"{state.lower()} supersedes approval", data, ClosureState.BLOCKED
            )
            self.assertEqual(result["decision"], "BLOCKED")

    def test_changes_request_vetoes_other_approval(self):
        data = fixture()
        other = copy.deepcopy(data["reviews"][0])
        other.update(id=2, state="CHANGES_REQUESTED", user={"login": "second", "type": "User"})
        data["reviews"].append(other)
        data["eligible_reviewers"].append("second")
        result = assert_admission_case(
            "changes request vetoes other approval", data, ClosureState.BLOCKED
        )
        self.assertIn("INDEPENDENT_CHANGES_REQUESTED", result["blockers"])

    def test_comment_does_not_retract_approval(self):
        data = fixture()
        later = copy.deepcopy(data["reviews"][0])
        later.update(id=2, state="COMMENTED")
        data["reviews"].append(later)
        result = assert_admission_case(
            "comment does not retract approval", data, ClosureState.MINIMALLY_CLOSED
        )
        self.assertEqual(result["decision"], "JOINT_ACCEPTED")


if __name__ == "__main__":
    unittest.main()
