# SLGE-SDLC-G0 Repository and PR Lifecycle Enforcement

## Origin and position

- Origin law: `docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md`
- Predecessor: `SLGE-SDLC-P0`
- Current step: `SLGE-SDLC-G0`
- Next and only permitted successor: `SLGE-SDLC-C0`

G0 enforces lifecycle declarations at the pull-request execution boundary. It
uses the P0 reducer for current state and E0's shared transition evaluator;
declaration text, green CI, and approval prose are not transition decisions.
G0 does not audit implementation closure.

## Contract

- Required inputs: reducer-derived `LifecycleProjection` and typed
  `EnforcementContracts`.
- Permitted operation: `EnforceLifecycleDeclarations`.
- PR declarations are checked against the G0 origin, predecessor, current
  stage, permitted successor, and the binding PR template.
- Cited evidence paths and traces must resolve to repository files or the
  lifecycle event's explicit trace URI; test paths must exist and include the
  G0 constitutional governance test.
- The declared rank/residual/trace impact answers, required test sections, and
  changed paths must exactly satisfy the executable G0 contract. PR-body edits
  rerun the gate before a prior successful check can remain authoritative.
- The runtime derives transition predicates from the current P0 projection,
  event registry, contract records, PR declaration, and actual file presence.
  Caller-provided approval, evidence-sufficiency, and proof-validity assertions
  are not inputs.
- Refusal is delegated to the existing E0 transition evaluator, with named
  transition failure codes, visible residuals, bounded rank/authority, and a
  trace-bearing decision.
- The pull-request workflow runs the gate after lint and tests. Its success is
  execution evidence only, never lifecycle closure.

## Boundaries

- `ClosureClaim` remains forbidden; `SLGE-SDLC-C0` remains unopened.
- The G0 pending residual is resolved only by this enforcement runtime; the C0
  closure-audit residual remains visible and open.
- No spelling/orthographic bridge, counting, morphology, Arabic licensing,
  semantic, truth, or empirical-validation surface is opened.
- No claim of `V1_CLOSED`, general algebra validation, observatory closure, or
  knowledge-transfer closure is licensed.

## Requirement-to-evidence map

| Contract commitment | Execution surface | Constitutional evidence |
| --- | --- | --- |
| Use the P0-derived lifecycle state; reject drift or a non-G0 state | `slge_sdlc_g0_enforcement.py::_g0_transition` recomputes and checks P0 | `test_accepts_g0_pr_with_derived_p0_state`; `test_refuses_approval_prose_without_evidence` |
| Check G0 declaration against P0 → G0 → C0 and the R0 slot contract | `evaluate_pull_request`; `slge_sdlc_g0_runtime.json`; shared E0 evaluator | `test_refuses_unauthorized_stage_jump` |
| Require evidence and reconstructible traces rather than caller assertions | PR field/path checks and derived E0 `TransitionAttempt` | `test_refuses_missing_evidence`; `test_refuses_missing_trace`; `test_refuses_approval_prose_without_evidence` |
| Enforce the PR boundary after tests execute | `.github/workflows/ci.yml` G0 gate step | `test_g0_workflow_runs_gate_after_tests` |
| Keep residuals visible and closure authority absent | G0 result inherits C0 residual and names C0 as the only next opening | `test_g0_residual_remains_open_and_closure_is_forbidden` |
| Do not expand into spelling, counting, or morphology | G0 gate refuses PR diffs that enter those paths | `test_refuses_spelling_counting_or_morphology_scope` |
| Reject paths outside the contract-backed G0 change surface | Contract allowlist is checked against every PR changed path | `test_refuses_changes_outside_g0_allowed_paths` |
| Require accurate impact declarations and test-section placement | Impact values and constitutional/negative test declarations are independently validated | `test_refuses_inaccurate_impact_declarations`; `test_refuses_tests_in_wrong_sections` |
| Refuse a mismatched transition-attempt identity | Recorded attempt ID is bound to the applied event before E0 approval | `test_refuses_mismatched_recorded_attempt` |
| Recheck edited PR declarations | Workflow runs the gate on PR `edited` activity | `test_g0_workflow_rechecks_edited_pull_requests` |
| Admit `proofs/arabic/**` evidence only through the declared lane (Amendment-108) | `Lane: PROOF-EVIDENCE-L1` routes to `_evaluate_lane_pull_request`; globs and forbidden prefixes come from `slge_sdlc_g0_runtime.json#lanes` | `test_lane_accepts_proof_evidence_paths`; `test_lane_refuses_unregistered_lane` |
| Refuse any lane PR that touches a G0-only or runtime path | `LANE_SCOPE_VIOLATION` on `src/`, `tests/`, `schemas/`, the G0 contract, projections, `ci.yml`, this document, `weight/`, `runtime/`, `lge/`, `x0r/`, or any `..` segment | `test_lane_refuses_g0_only_paths` |
| Require the eleven lane declarations and a real `ProofPackageCheck` | `LANE_DECLARATION_MISSING`; `ProofPackageCheck` must name `proofs/arabic/check.sh` | `test_lane_refuses_missing_proof_package_check` |
| Keep closure, C0, and runtime-bridge outputs forbidden inside the lane | `LANE_OUTPUT_BOUNDARY_VIOLATION`; `LANE_RESIDUAL_POLICY_VIOLATION` | `test_lane_refuses_closure_claim` |
| Lane evidence must be real files with a hash-pinned index | `LANE_EVIDENCE_INSUFFICIENT`; `LANE_TRACE_LOSS` when `proofs/arabic/rules.json` is absent | `test_lane_refuses_missing_evidence_files` |
| Lane decisions open no successor and leave the lifecycle untouched | `LaneDecision` pins `opens_successor=false`, `next_openings=()`, `rank_change=none`, `authority_change=none`; C0 residual inherited open | `test_lane_decision_opens_no_successor_and_keeps_c0_residual_open` |
| Plain G0 PRs are unaffected by the lane | Bodies without `Lane:` take the pre-amendment path bit-for-bit | `test_non_lane_body_is_unaffected_by_lane_contract` |
| Renames cannot smuggle governance files into lane scope | `_changed_paths` uses `git diff --name-only --no-renames` and refuses `..` segments (`PR_PATH_UNSAFE`) | `test_changed_paths_do_not_hide_renames_into_lane_scope`; `test_changed_paths_reject_parent_segments` |

## Lane PROOF-EVIDENCE-L1 (Amendment-108)

G0 may carry bounded *evidence lanes*. A lane is not a lifecycle slot: it is a
declared sub-scope inside the current G0 state whose decisions can never open a
successor, change rank or authority, or move the P0 projection. Amendment-108
registers one lane in `governance/registry/slge_sdlc_g0_runtime.json#lanes`:

- Lane id: `PROOF-EVIDENCE-L1`. A PR enters it by declaring
  `- Lane: PROOF-EVIDENCE-L1` in the binding PR body; a body without `Lane:`
  is evaluated as a plain G0 PR exactly as before.
- Scope: every changed path must match `proofs/arabic/**`,
  `.github/workflows/arabic-proof.yml`, `governance/registry/evidence_map.json`,
  `governance/registry/residuals.json`, `governance/history/amendments.jsonl`,
  or `docs/14_PR_CHAIN_ROADMAP.md`, and none may start with `src/`, `tests/`,
  `schemas/`, `governance/registry/slge_sdlc_g0_runtime.json`,
  `governance/projections/`, `.github/workflows/ci.yml`, this document,
  `weight/`, `runtime/`, `lge/`, or `x0r/`. Any violation is refused with
  `LANE_SCOPE_VIOLATION`. Changed paths are derived with `--no-renames`, so a
  `git mv` out of governance shows the source as a deleted, out-of-scope path.
- Declarations: the nine G0 declarations plus `Lane` and `ProofPackageCheck`
  (`bash proofs/arabic/check.sh`). Chain-position fields still read
  P0 → G0 → C0; `Allowed Scope` must name the lane; `Forbidden Scope` must
  still name closure, spelling, counting, morphology, and Arabic licensing;
  `Output Boundary` must still forbid `ClosureClaim` and C0 output.
- Evidence: `proofs/arabic/rules.json` (rule → theorem index with pinned
  source hashes), `proofs/arabic/check.sh`, and `proofs/arabic/README_AR.md`
  must exist in the repository; the lane constitutional and negative tests
  must resolve in `tests/test_slge_sdlc_g0_runtime.py`.
- Decision effects: `opens_successor=false`, `rank_change=none`,
  `authority_change=none`, `resolves_residuals=[]`,
  `adds_residuals=[ARABIC_PROOF_RUNTIME_BRIDGE_PENDING]`;
  `SLGE_C0_CLOSURE_AUDIT_PENDING` is inherited open.
- Forbidden outputs: identical to G0 (`ClosureClaim`, `SLGE-SDLC-C0`,
  `SpellingBridge`, `CountingRuntime`, `MorphologyRuntime`, `ArabicLicensing`,
  `V1ClosedClaim`).

Non-effects: the lane admits a Lean proof package as *evidence only*. It does
not bridge the proofs into `runtime/`, `weight/`, `lge/`, or `x0r/`; it does
not license Arabic semantics, spelling, counting, or morphology; it does not
claim closure, does not open `SLGE-SDLC-C0`, and does not alter
`allowed_changed_paths` for plain G0 PRs. Changing the lane itself is a
G0-scoped amendment made only through G0's own allowed paths.

## Verification is not closure

The runtime and its evidence establish only that G0's declaration-enforcement
boundary executes under its declared inputs. CI, review, merge, and this
evidence do not satisfy the independent C0 closure audit.
