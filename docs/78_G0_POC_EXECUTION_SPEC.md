# 78 — G₀ PoC Execution Spec (Short Industrial Track)

> **Status:** PoC implementation spec for a bounded industrial prototype.
> This document defines measurable PoC outputs and does not claim
> semantic closure, hukm, truth certification, or authority.

---

## 1) Scope Contract (Allowed / Forbidden)

### Allowed

- Build a bounded **G₀ classifier** with traceable explanation cards.
- Route non-G₀ items to `M0 / D0 / K0 / X0` without forcing G₀ verdicts.
- Use a fixed law registry, lexical evidence store, and ontology store.
- Emit one of four decisions only:
  - `مرخّص`
  - `مرفوض`
  - `معلّق`
  - `محوّل`

### Forbidden

- Any output that claims final meaning, hukm, truth, or authority.
- Any hidden residual in approved output.
- Any decision without trace.
- Any direct transition from token to certainty without law/evidence.
- Opening `T / R / H` layers in this PoC.

---

## 2) Unified Analysis Card I/O

### Input

- `token` (string)
- `trace_ref` (must start with `trace://`)

### Output (single unified card)

- `axis` (`𝔇 / 𝔐 / 𝔚`)
- `path` (`G0 / M0 / D0 / K0 / X0`)
- `decision` (`مرخّص / مرفوض / معلّق / محوّل`)
- `law_ids` (one or more law identifiers)
- `preventer` (named blocker or `NONE`)
- `residuals` (visible residual list)
- `trace` (selected laws + reason + path)

---

## 2.1 Meta-language framing for decision labels

This PoC uses Arabic decision labels as UI-facing terms only, with explicit
boundary markers:

- `origin_law`: docs/53 §3–§5, docs/54 §1, this spec (§1/§2)
- `branch_name`: G0-POC short industrial track
- `farq_qadih`: decision labels are presentation labels; they are not hukm,
  truth, certificate, or authority outputs
- `trace obligation`: every label must remain bound to a trace payload

---

## 3) PoC Data Stores

The PoC ships four measurable artifacts:

1. `data/g0_poc_law_registry.json`
   - initial fixed law set (30 rows)
   - fields: origin, condition, preventer, decisive difference, evidence rank
2. `data/g0_poc_lexical_evidence.json`
   - initial lexical witness set (sample corpus)
3. `data/g0_poc_ontology_store.json`
   - operational ontology rows used in explanation context
   - each row declares `boundary_status`:
     - `G0_ADMISSIBLE`
     - `ROUTE_ONLY`
     - `DEFERRED_ONLY`
     - `TEST_SENTINEL`
   - `G0` licensing is allowed only when `boundary_status = G0_ADMISSIBLE`
4. `data/g0_poc_coverage_matrix.json`
   - explicit runtime coverage and forbidden layers

---

## 4) Rule/Trace Requirements

- Every analysis card must include a non-empty trace payload.
- Rule conflict at the top priority must produce `مرفوض` with visible residual.
- Rule composition at equal top priority and same decision is allowed with
  `LAW_COMPOSITION` residual.
- Unknown token or missing law binding produces `معلّق`.

---

## 5) Measurable Evaluation Outputs

PoC evaluation report must include:

- `accuracy`
- `correct_refusal_rate`
- `deferred_rate`
- `trace_completeness_rate`
- `coverage`
- `gap_tokens`

Go/No-Go helper thresholds:

- `accuracy >= 0.80`
- `trace_completeness_rate == 1.00`
- `deferred_rate <= 0.25`

If any threshold fails, verdict is `NO_GO` with explicit reasons.

---

## 6) Final PoC Deliverable

**G₀ Classifier + Law-Certified Explanation Engine**

The engine accepts a token and returns one bounded, traceable, law-linked card
with explicit decision, blocker, residuals, and trace.
