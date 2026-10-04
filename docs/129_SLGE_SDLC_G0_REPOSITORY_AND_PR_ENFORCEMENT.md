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

## Verification is not closure

The runtime and its evidence establish only that G0's declaration-enforcement
boundary executes under its declared inputs. CI, review, merge, and this
evidence do not satisfy the independent C0 closure audit.
