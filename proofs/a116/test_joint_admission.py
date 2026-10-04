"""Synthetic gate tests, never independent review or a real admission.

Origin: docs/11, docs/13, PARALLEL-PROOF-READ-L0 proposal.
Branch: joint admission candidate. Chain: bound evidence -> conjunctive decision.
Expected outputs: JOINT_ACCEPTED only for the complete simulated contract;
BLOCKED otherwise. No rank/linguistic output. Every blocker remains visible.
"""

import copy
import unittest

from joint_admission import REVIEW_ITEMS, assess


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
        result = assess(fixture())
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
                result = assess(data)
                self.assertEqual(result["decision"], "BLOCKED")
                self.assertIn(blocker, result["blockers"])

    def test_proof_success_alone_never_licenses(self):
        data = fixture()
        data.update(reviews=[], governance_state="REFUSED")
        self.assertEqual(len(assess(data)["blockers"]), 2)

    def test_head_base_and_body_mutations_invalidate_review(self):
        for key in ("head", "base", "body_sha256"):
            data = fixture()
            data[key] = "d" * len(data[key])
            self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_old_commit_review_is_rejected(self):
        data = fixture()
        data["reviews"][0]["commit_id"] = "e" * 40
        self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_author_and_contributor_are_not_independent(self):
        for field in ("author", "contributors"):
            data = fixture()
            data[field] = "independent" if field == "author" else ["INDEPENDENT"]
            self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_unprivileged_or_bot_review_is_rejected(self):
        data = fixture()
        data["eligible_reviewers"] = []
        self.assertEqual(assess(data)["decision"], "BLOCKED")
        data = fixture()
        data["reviews"][0]["user"]["type"] = "Bot"
        self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_missing_review_obligation_is_rejected(self):
        for item in REVIEW_ITEMS:
            data = fixture()
            data["reviews"][0]["body"] = data["reviews"][0]["body"].replace(
                f"- [x] {item}", f"- [ ] {item}"
            )
            self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_dismissal_and_changes_request_supersede_approval(self):
        for state in ("DISMISSED", "CHANGES_REQUESTED"):
            data = fixture()
            later = copy.deepcopy(data["reviews"][0])
            later.update(id=2, state=state)
            data["reviews"].append(later)
            self.assertEqual(assess(data)["decision"], "BLOCKED")

    def test_changes_request_vetoes_other_approval(self):
        data = fixture()
        other = copy.deepcopy(data["reviews"][0])
        other.update(id=2, state="CHANGES_REQUESTED", user={"login": "second", "type": "User"})
        data["reviews"].append(other)
        data["eligible_reviewers"].append("second")
        self.assertIn("INDEPENDENT_CHANGES_REQUESTED", assess(data)["blockers"])

    def test_comment_does_not_retract_approval(self):
        data = fixture()
        later = copy.deepcopy(data["reviews"][0])
        later.update(id=2, state="COMMENTED")
        data["reviews"].append(later)
        self.assertEqual(assess(data)["decision"], "JOINT_ACCEPTED")


if __name__ == "__main__":
    unittest.main()
