# 53 — Project Methodology, Objectives, and KPI Plan

> **Status:** Constitutional planning document. Ratified in CLOSE-2.
> Merged via PR #93 (combined merge with PV-T0-C1, commit 290587c).
> Binding for all branches after CLOSE-2 per Amendment-26.
> Constitutional origin: docs/46 (Vertical Path Closure Law),
> docs/47 (Post-Vertical Roadmap).
>
> This document declares the project's governing origin, licensed
> inputs/outputs, forbidden outputs, strategic objectives, measurable
> indicators, and the branch admission contract. It does not implement
> runtime code.

---

## §1 Governing Origin

The project's governing origin:

```text
No output without Trace.
No Trace without a licensed layer.
No transition without a Gate.
No Gate without Evidence.
No Evidence without Rank and visible Residuals.
No candidate becomes a certificate, execution, or authority.
```

Taaqol-GPT is a **constitutional reasoning engine**: a model-agnostic,
evidence-bounded, trace-preserving, residual-visible governance system
for claims, Arabic linguistic candidates, and audited outputs.

The project has closed the minimum vertical path from
`MufradDalalahClosure` to `AuditedTanzilBridge` per docs/46. The
closure proves: trace continuity, rank monotonicity, residual
visibility, envelope preservation, named refusals, and no execution
leakage.

---

## §2 Project Definition

### §2.1 What the project is

```text
Taaqol-GPT is a constitutional reasoning engine:
a model-agnostic, evidence-bounded, trace-preserving, residual-visible
governance system for claims, Arabic linguistic candidates, and audited outputs.
```

### §2.2 What the project is NOT

```text
- GPT clone
- Arabic parser from raw text
- fatwa / qada / execution engine
- hidden chain-of-thought extractor
- unbounded / totalizing truth-engine claim
- government decision automation engine
- model confidence evaluator
```

### §2.3 Truth Engine first-experiment posture

```text
Taaqol-GPT is the project's first executable Truth Engine experiment:
it produces licensed linguistic knowledge under constitutional gates,
with preserved trace and explicit rollback/supersession boundaries.
```

This posture is bounded, not totalizing. It does not grant unrestricted
knowledge production outside licensed layers, and it does not erase the
open execution-gap ledger tracked in docs/91.

Truth Engine guard clauses (binding textual contract):

```text
first bounded execution experiment
not a universal truth engine
licensed knowledge production does not imply truth
truth requires correspondence and evidence
certificate rank does not imply external truth
```

Any wording that upgrades this bounded posture into totalized truth,
automatic reality-correspondence, or universal truth certification is
constitutionally forbidden.

### §2.4 Four pillars

```text
1. Constitution
   Governing laws for transition, testing, rank, residuals, and evidence.

2. Execution Kernel
   SlotGraph, Gamma, RankLattice, ResidualPolicy, EvidenceContract,
   TransitionGate, TraceLedger, AnswerAudit.

3. Arabic Semantic Column
   From signifier and signified to singular dalalah, relation, ifadah,
   hukm, manat, tanzil, then the audit surface.

4. Post-Closure Branches
   Mantuq, mafhum, meta-language, mabni/muʿrab, haqiqah/majaz, naql,
   reference, conditions, AI proposer, and industrial applications.
```

---

## §3 Licensed Inputs

The project accepts only:

```text
1. Declared claim + evidence + trace + rank + residuals + gate
2. Arabic linguistic candidate produced by a licensed upstream layer
3. Model output wrapped behind ModelClient protocol (black-box boundary)
4. Constitutional test declaration with all nine mandatory fields
```

The project does NOT accept:

```text
- Raw text as ontological origin
- Model confidence as evidence
- Model answer as truth
- Candidate as certificate
- Hukm as execution
- Tanzil as authority
```

---

## §4 Licensed Outputs

The project may produce:

```text
1. Candidate (bounded, never final)
2. Verdict (PROVEN / REFUSED with named FailureCode)
3. Audit surface (AuditedAnswer via AnswerAudit pipeline)
4. Refusal (named FailureCode, never silent None)
5. Trace entry (TraceEntryCandidate appended to TraceLedger)
6. Residual declaration (visible, never hidden)
```

---

## §5 Forbidden Outputs

The project must NEVER produce:

```text
FO-1:  raw_text → meaning
FO-2:  model_answer → truth
FO-3:  candidate → certificate
FO-4:  hukm → execution
FO-5:  tanzil → authority
FO-6:  model_confidence → evidence
FO-7:  hidden residual → approved output
FO-8:  rank promotion without gate
FO-9:  transition without evidence
FO-10: output without trace
FO-11: candidate → final_meaning
FO-12: mabni_form → syntactic_role (without licensing)
FO-13: harf → hukm (without full chain)
FO-14: pronoun → final_reference (without maqam)
FO-15: majaz_before_haqiqah_attempt
```

---

## §6 Strategic Objectives

### SO-1: Close the project as Constitutional Engine v0.1

```text
Transform the project from open research/foundation to a releasable
Constitutional Engine v0.1 with defined I/O, measurement tests, and
closure report.
```

Success indicator:
- docs/53 ratified (this document)
- docs/54 objective law ratified (GPT-R0)
- docs/54 includes a short normative capsule:
  Definitions + Axioms + Theorem + Claim-Boundary
- roadmap registers next GPT sequence (GPT-K2 → GPT-R8)
- README, pyproject, CHANGELOG, LICENSE consistent
- No open PR violating its declared constitutional scope

### SO-2: Stabilize I/O contract

```text
Prevent any ambiguity about what enters and exits the project.
```

Success indicator:
- §3 (Licensed Inputs) fully declared
- §4 (Licensed Outputs) fully declared
- §5 (Forbidden Outputs) with ≥ 15 named symbols

### SO-3: Tests as constitutional proofs, not merely CI

```text
Transform tests into licensed transition proofs. Green pytest alone
is not sufficient evidence — each test must prove its origin, branch,
and constitutional chain.
```

Success indicator:
- 0 new orphan tests after PV-T0
- 100% of new tests declare origin_law, branch_name, constitutional_chain

### SO-4: Protect the closed vertical column from future branches

```text
Every new branch (mabni, haqiqah/majaz, naql, reference, conditions,
GPT proposer, government engine) must prove connection to the column
and must not produce meaning, hukm, or execution from itself alone.
```

Success indicator:
- 0 forbidden output leakage from any future branch
- 100% of future branches have BranchContract (§8)

### SO-5: Governed expansion platform

```text
Open future branches only under law:
law-first, tests-second, runtime-third.
```

Success indicator:
- 100% of future branches follow law → contract → test → runtime → audit

---

## §7 Long-Term Objectives

### LTO-1: Complete Arabic reasoning algebra

```text
Transform Arabic into a system of licensed transitions from carrier
to dalalah to hukm without layer-jumping.
```

Measurement:
- 100% of new Arabic branches have: origin law + BranchContract +
  refusal taxonomy + trace tests + rank tests

### LTO-2: Model-agnostic audit engine

```text
Any language model or tool may produce a claim, but only this engine
governs whether the claim passes as an audited candidate or is refused.
```

Measurement:
- 0 cases: model confidence used as evidence
- 0 cases: model output used as verdict
- 0 cases: model suggestion writes trace

### LTO-3: Safe application layer

```text
Consumption of AuditedTanzilBridge in educational/governmental/research
applications without the output becoming execution or authority.
```

Measurement:
- 100% of future applications start from AuditedTanzilBridge
- 0 applications start from HukmCandidate or ManatCandidate alone

### LTO-4: Complete constitutional measurement system

```text
Transform tests into a real KPI system that measures objective
achievement, not merely code success.
```

Measurement:
- Every Objective has a TestCase
- Every TestCase has origin/branch/chain
- Every failure has a FailureCode
- Every residual is visible or blocking

---

## §8 BranchContract Template

Every future branch must be written according to this contract:

```text
BranchContract:
    original_origin            the origin this branch derives from
    branch_name                name of the branch
    sabab                      the triggering cause
    shart                      conditions that must be met
    mani                       the blocker that stops the branch
    input_contract             licensed inputs
    output_contract            licensed outputs
    forbidden_outputs          what must not be produced
    evidence_contract          type of evidence required
    rank_ceiling               maximum rank
    residual_policy            residual visibility policy
    trace_contract             trace preservation to origin
    upstream_dependency        required upstream layer
    downstream_effect          what the branch opens and what it does not
```

This contract prevents future branches from becoming independent
projects. Every branch must prove it is a branch of the current
origin, not a leap over it.

A branch that cannot answer all 14 fields is:

```text
BRANCH_NOT_ADMITTED
```

Not:

```text
work in progress
```

---

## §9 Medium-Term Objectives

### MTO-1: Complete v0.1 closure

Scope: CLOSE-1 through CLOSE-6.

Outputs:
- docs/53 (this document)
- chain synchronization in docs/14 + CLAUDE (next GPT sequence registered)
- test-origin scanner (PV-T0.1)
- minimal golden origins dataset (GPT-K2)
- golden closure fixtures
- v0.1.0 tag

Measurement:
- pytest = pass
- ruff = pass
- new orphan tests = 0
- hidden residual leakage = 0
- rank promotion leakage = 0
- forbidden output leakage = 0

### MTO-2: Test origin enforcement

Scope: PV-T0.1.

Output: test origin scanner.

Measurement:
- Every new test after PV-T0 declares: origin_law, branch_name,
  constitutional_chain, expected_state, forbidden_outputs,
  expected_failure_code, max_rank, required_residual_visibility,
  required_trace

### MTO-2.1: GPT reasonableness staged execution

Scope: GPT-K2 then GPT-R1 through GPT-R8.

Output:
- GPT-K2 minimal golden dataset
- GPT-R1 input contract
- GPT-R2 MaqamGPT boundary
- GPT-R3 MantuqGPT extraction
- GPT-R4 MafhumGPT extraction
- GPT-R5 origin binding gate
- GPT-R6 reasonableness gates
- GPT-R7 reasonableness verdict
- GPT-R8 AnswerAudit integration

Measurement:
- chain order is preserved (no FORBIDDEN_LEAP)
- no hidden residual reaches final verdict
- no rank promotion without gate
- no output without trace

### MTO-3: Open PV-M1 correctly

Scope: Mabni Stability Boundary Law.

Goal: govern mabni, muʿrab, harf, pronoun, demonstrative as
dangerous terms that do not produce meaning, syntactic role, or
final reference from form alone.

Measurement:
- No Mabni → Meaning
- No Mabni → SyntaxRole
- No Harf → Hukm
- No Pronoun → FinalReference without Maqam

### MTO-4: Open haqiqah/majaz and naql

Scope: Haqiqah/Majaz, Naql, Lexical relation branches.

Measurement:
- No Majaz before HaqiqahAttempt
- No Naql without original_origin + transferred_branch + wasf_muaththir
- No lexical relation without Dal-Madlul binding

---

## §10 Short-Term Objectives

### STO-1: PR scope consistency

Every PR touches only files declared in its scope.

Measurement: diff matches declaration, 100%.

### STO-2: This document (docs/53)

Output: docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md

Required sections:
- Project origin
- Strategic objectives
- Licensed inputs/outputs
- Forbidden outputs
- BranchContract
- KPI matrix

### STO-3: Acceptance tests for docs/53

Output: tests/test_project_methodology_objectives_kpi_plan.py

Tests:
- test_docs_53_exists
- test_docs_53_declares_project_origin
- test_docs_53_declares_licensed_inputs
- test_docs_53_declares_licensed_outputs
- test_docs_53_declares_forbidden_outputs
- test_docs_53_declares_branch_contract
- test_docs_53_declares_kpi_matrix
- test_docs_53_declares_future_branch_origin_rule

### STO-4: Closure audit (docs/54)

Output: docs/54_PROJECT_CLOSURE_AUDIT.md

Contents:
- Achieved
- Deferred
- Forbidden
- Residuals
- Release Gate

---

## §11 KPI Matrix

| Code  | Objective                     | Type       | KPI                             | Target |
|-------|-------------------------------|------------|---------------------------------|-------:|
| SO-1  | Close v0.1                    | Strategic  | release gate pass               |   100% |
| SO-2  | I/O clarity                   | Strategic  | docs/53 sections                |   100% |
| SO-3  | Tests as proofs               | Strategic  | no new orphan tests             |      0 |
| SO-4  | Column protection             | Strategic  | forbidden leak tests            |      0 |
| SO-5  | Governed expansion            | Strategic  | future BranchContract coverage  |   100% |
| LTO-1 | Arabic algebra                | Long-term  | branch law coverage             |   100% |
| LTO-2 | Model-agnostic engine         | Long-term  | model confidence as evidence    |      0 |
| LTO-3 | Safe applications             | Long-term  | execution leakage               |      0 |
| LTO-4 | Measurement system            | Long-term  | objective-test coverage         |   100% |
| MTO-1 | v0.1 closure                  | Medium     | docs/53 + docs/54 + tests       |   pass |
| MTO-2 | Scanner                       | Medium     | orphan new tests                |      0 |
| MTO-3 | PV-M1                         | Medium     | unsafe mabni transitions        |      0 |
| MTO-4 | Haqiqah/Majaz/Naql            | Medium     | pre-attempt violations          |      0 |
| STO-1 | PR scope                      | Short-term | diff matches declaration        |   100% |
| STO-2 | docs/53                       | Short-term | document contract tests         |   pass |
| STO-3 | Acceptance tests              | Short-term | 8 test functions                |   pass |
| STO-4 | Closure audit                 | Short-term | residual report exists          |   pass |

---

## §12 Test Enforcement Plan

### §12.1 Test layers

```text
Layer 1 — Document existence tests
    Verify that required constitutional documents exist.

Layer 2 — Contract surface tests
    Verify that documents contain required fields/sections.

Layer 3 — Public API tests
    Verify the public surface does not export forbidden symbols.

Layer 4 — Golden path tests
    Prove the correct path from origin to audited output.

Layer 5 — Negative/refusal tests
    Prove that blockers work (named FailureCode on every refusal).

Layer 6 — Residual tests
    Prove that residuals are never hidden.

Layer 7 — Rank tests
    Prove that rank is never promoted without a gate.

Layer 8 — Trace tests
    Prove that trace is never broken.

Layer 9 — Branch admission tests
    Prove that future branches connect to their origin.
```

### §12.2 Objective-KPI test schema (future)

```python
@dataclass(frozen=True)
class ObjectiveKpiTestCase:
    objective_id: str
    origin_law: str
    branch_name: str
    strategic_goal: str
    invariant_under_test: str
    input_contract: str
    expected_output: str
    forbidden_output: str
    measurable_indicator: str
    expected_state: str
    failure_code_expectation: str
    rank_expectation: str
    residual_expectation: str
    trace_expectation: str
```

This schema binds each test not only to a behaviour but to an
**objective**. It is reserved for future implementation after the
test-origin scanner (PV-T0.1) is in place.

---

## §13 Future Branch Admission Rule

No future branch opens unless it answers all of the following:

```text
1. What origin does it derive from?
2. What cause triggers it?
3. What condition must be met?
4. What blocker stops it?
5. What is the licensed input?
6. What is the licensed output?
7. What must it NOT produce?
8. What is the evidence?
9. What is the rank?
10. What are the residuals?
11. Where is the trace?
12. What test proves all of the above?
```

A branch that fails to answer any one of these is:

```text
BRANCH_NOT_ADMITTED
```

---

## §14 Execution Methodology

```text
The project is governed by:
Law → Contract → Test → Runtime → Audit → Closure.

Every law declares an origin and a branch.
Every branch declares a cause, condition, and blocker.
Every input has a contract.
Every output has a ceiling.
Every refusal has a FailureCode.
Every residual is visible.
Every rank is bounded.
Every trace is connected.
Every objective has a KPI.
Every KPI has a test.
```

---

## §15 Closing Statement

```text
Closing the project does not mean stopping it.
It means that every expansion after closure is born not from the
desire to add, but from a preserved origin, a needed branch, a
considered cause, a met condition, a removed blocker, apparent
evidence, a bounded rank, visible residuals, and an unbroken trace.

The objective is not accepted until it becomes a test.
The test is not accepted until it declares its origin and branch.
The branch is not accepted until it proves its service to the origin.
```
