"""Candidate joint admission check; never grants a linguistic or runtime rank.

Origin: docs/11 + docs/13 + proposed PARALLEL-PROOF-READ-L0 (#350).
Branch: A116 proof/review/governance binding, pending constitutional admission.
Authority comes from GitHub evidence and the BASE revision's G0 evaluator.
No producer-supplied approval flags or reviews are accepted by the CLI.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REVIEW_ITEMS = (
    "MODEL_SOURCE_MAPPING",
    "THEOREM_STATEMENT",
    "AXIOM_DEPENDENCIES",
    "NEGATIVE_WITNESSES",
    "LINGUISTIC_LIMITS",
)


def body_digest(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def assess(snapshot: dict) -> dict:
    """Pure decision over an adapter-derived snapshot; fixtures are not authority."""
    blockers = []
    head, base = snapshot["head"], snapshot["base"]
    if not snapshot["fresh"]:
        blockers.append("SNAPSHOT_CHANGED")
    if not snapshot["proof_passed"]:
        blockers.append("PROOF_NOT_VERIFIED_AT_HEAD")
    if not snapshot["contributors_complete"]:
        blockers.append("CONTRIBUTOR_IDENTITY_UNRESOLVED")
    if snapshot["governance_state"] != "APPROVED":
        blockers.append("GOVERNANCE_NOT_APPROVED")
    latest = {}
    for review in sorted(snapshot["reviews"], key=lambda r: r["id"]):
        # A later COMMENTED review is not a retraction of an approval.
        if review["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}:
            latest[review["user"]["login"].casefold()] = review
    eligible = set(snapshot["eligible_reviewers"])
    excluded = {x.casefold() for x in snapshot["contributors"]}
    excluded.add(snapshot["author"].casefold())
    approvals = []
    markers = (
        f"Proof-Head: {head}",
        f"Proof-Base: {base}",
        f"PR-Body-SHA256: {snapshot['body_sha256']}",
        *(f"- [x] {item}" for item in REVIEW_ITEMS),
    )
    for login, review in latest.items():
        if login not in eligible or login in excluded or review["user"]["type"] != "User":
            continue
        if review["state"] == "CHANGES_REQUESTED":
            blockers.append("INDEPENDENT_CHANGES_REQUESTED")
            continue
        if review["state"] != "APPROVED" or review.get("commit_id") != head:
            continue
        lines = set((review.get("body") or "").splitlines())
        if all(marker in lines for marker in markers):
            approvals.append({"review_id": review["id"], "reviewer": login})
    if not approvals:
        blockers.append("INDEPENDENT_REVIEW_MISSING_OR_STALE")
    return {
        "decision": "JOINT_ACCEPTED" if not blockers else "BLOCKED",
        "head": head,
        "base": base,
        "body_sha256": snapshot["body_sha256"],
        "proof_run_id": snapshot["proof_run_id"],
        "independent_reviews": approvals,
        "governance_state": snapshot["governance_state"],
        "governance_detail": snapshot["governance_detail"],
        "blockers": sorted(set(blockers)),
        "linguistic_license": False,
        "runtime_rank_promotion": False,
    }


def api(path: str):
    request = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pages(path: str, key: str | None = None) -> list:
    result = []
    for page in range(1, 101):
        payload = api(f"{path}?per_page=100&page={page}")
        rows = payload[key] if key else payload
        result.extend(rows)
        if len(rows) < 100:
            return result
    raise ValueError("PAGINATION_NOT_EXHAUSTED")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def governance(base: str, head: str, body: str) -> tuple[str, str]:
    """Evaluate unchanged BASE governance, not a gate supplied by the PR."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "base"
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(root), base],
            check=True,
            capture_output=True,
            text=True,
        )
        try:
            sys.path.insert(0, str(root / "src"))
            module = importlib.import_module(
                "taaqqul_slot_geometry.governance.slge_sdlc_g0_enforcement"
            )
            changes = tuple(git("diff", "--name-only", f"{base}...{head}").splitlines())
            result = module.evaluate_pull_request(
                root, pull_request_body=body, changed_paths=changes
            )
            return result.state.value, ",".join(code.value for code in result.failure_codes)
        except Exception as error:
            return "ERROR", type(error).__name__ + ": " + str(error)
        finally:
            sys.path.pop(0)
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )


def collect() -> dict:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    number = event["pull_request"]["number"]
    repo = os.environ["GITHUB_REPOSITORY"]
    prefix = f"/repos/{repo}"
    pr = api(f"{prefix}/pulls/{number}")
    head, base = pr["head"]["sha"], pr["base"]["sha"]
    body = pr.get("body") or ""
    run_id = int(os.environ["GITHUB_RUN_ID"])
    run = api(f"{prefix}/actions/runs/{run_id}")
    jobs = pages(f"{prefix}/actions/runs/{run_id}/jobs", "jobs")
    proof_passed = (
        run["head_sha"] == head
        and run["event"] in {"pull_request", "pull_request_review"}
        and any(job["name"] == "proof" and job["conclusion"] == "success" for job in jobs)
    )
    reviews = pages(f"{prefix}/pulls/{number}/reviews")
    commits = pages(f"{prefix}/pulls/{number}/commits")
    contributors = set()
    complete = bool(commits) and len(commits) == pr["commits"]
    for commit in commits:
        # An unmapped author is not silently treated as an independent person.
        author = commit.get("author")
        if not author or not author.get("login"):
            complete = False
        else:
            contributors.add(author["login"])
    eligible = []
    for login in sorted({review["user"]["login"] for review in reviews}):
        permission = api(f"{prefix}/collaborators/{login}/permission")
        if permission["permission"] in {"write", "maintain", "admin"}:
            eligible.append(login.casefold())
    state, detail = governance(base, head, body)
    after = api(f"{prefix}/pulls/{number}")
    fresh = (
        git("rev-parse", "HEAD") == head
        and event["pull_request"]["head"]["sha"] == head
        and after["head"]["sha"] == head
        and after["base"]["sha"] == base
        and (after.get("body") or "") == body
        and pages(f"{prefix}/pulls/{number}/reviews") == reviews
        and after["state"] == "open"
    )
    return {
        "head": head,
        "base": base,
        "body_sha256": body_digest(body),
        "proof_run_id": run_id,
        "proof_passed": proof_passed,
        "fresh": fresh,
        "contributors": sorted(contributors),
        "contributors_complete": complete,
        "author": pr["user"]["login"],
        "eligible_reviewers": eligible,
        "reviews": reviews,
        "governance_state": state,
        "governance_detail": detail,
    }


def main() -> int:
    try:
        result = assess(collect())
    except Exception as error:
        result = {
            "decision": "BLOCKED",
            "blockers": ["EVIDENCE_COLLECTION_FAILED"],
            "error_type": type(error).__name__,
            "linguistic_license": False,
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a") as stream:
            stream.write("## Joint proof admission\n\n```json\n" + payload + "\n```\n")
    return 0 if result["decision"] == "JOINT_ACCEPTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
