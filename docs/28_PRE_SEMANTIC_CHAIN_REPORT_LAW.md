# docs/28 — Pre-Semantic Chain Report Law

Ratified by: PR-16B.
Origin: docs/14 §§1–2 (chain integrity); docs/11 (SlotGeometry is a
constitutional mathematical object); docs/27 (PR-16 closes verbal
signified candidacy).

---

## 0. Purpose

This law governs the **PreSemanticChainReport** — a read-only
integration carrier that proves the pre-semantic chain (PR-10 through
PR-16) produces a single vertical slice from syllable to verbal
signified candidacy, with unbroken rank monotonicity, residual
continuity, trace coverage, and named refusal coverage.

The report adds **no new linguistic claim**. It aggregates existing
outputs without promoting rank, hiding residuals, or asserting
meaning.

---

## 1. Governing principle

```text
The project is not a set of independent linguistic modules.
It is a single licensed chain.

Every branch must either:
1. add one licensed transition,
2. add one boundary/verdict,
3. or integrate prior outputs without adding new claims.

A branch that adds a new local object without showing its place
in the vertical chain risks becoming an island.

PR-16B is category (3): integration without new claims.
```

---

## 2. PreSemanticChainReport — required fields

```text
PreSemanticChainReport {
  # --- Source identity ---
  source_surface_identity: str       non-empty

  # --- Weight readiness layer (PR-10/12) ---
  weight_readiness_ref: str          non-empty trace reference

  # --- Weight fit layer (PR-13) ---
  weight_fit_ref: str                non-empty trace reference
  weight_fit_rank: Rank              bounded

  # --- Licensing boundary layer (PR-14) ---
  licensing_boundary_ref: str        non-empty trace reference
  licensing_boundary_kind: str       boundary kind label
  licensing_eligibility_rank: Rank   bounded

  # --- Signifier layer (PR-15) ---
  dal_ref: str                       non-empty trace reference
  signifier_identity: str            non-empty
  dal_rank: Rank                     bounded

  # --- Verbal signified layer (PR-16) ---
  verbal_madlul_ref: str             non-empty trace reference
  wad_usage_boundary: str            non-empty
  correspondence_candidate: str
  inclusion_candidate: str
  iltizam_condition: str
  madlul_rank: Rank                  bounded

  # --- Governance summary ---
  chain_rank_ceiling: Rank           the tightest ceiling in the chain
  residuals: tuple[Residual, ...]    all residuals (visible, governed)
  named_refusals: tuple[str, ...]    any refusals encountered (empty on success)
  trace_refs: tuple[str, ...]        ordered trace references

  # --- Forbidden output attestation ---
  forbidden_outputs_absent: bool     must be True
}
```

---

## 3. Construction rule

```text
assemble_chain_report() accepts ONLY a VerbalMadlulCandidate.
It refuses all other input types with FailureCode.GATE_REQUIRED.
```

The function traverses the candidate's embedded chain:
```text
VerbalMadlulCandidate
  .dal_only: DalOnlyCandidate
    .prior_licensing_verdict: LicensingBoundaryVerdict
      .source: WeightFitCandidate
        .source: WeightReadinessCandidate
```

This traversal is **read-only**: no field is mutated, no rank is
promoted, no residual is added or hidden.

---

## 4. Rank monotonicity invariant

```text
For every adjacent pair (layer_i, layer_j) in the chain:
  rank(layer_j) <= rank(layer_i)
```

The report must verify this property. If violated, the report
refuses with FailureCode.RANK_EXCEEDS_CEILING.

---

## 5. Residual continuity invariant

```text
No residual present at layer_i may be absent at layer_j (j > i)
unless explicitly consumed by a gate between them.
```

Since PR-10 through PR-16 have no residual-consuming gates (only
residual-carrying gates), all residuals must be present throughout.
The report carries the full residual tuple from the terminal layer.

---

## 6. Forbidden output attestation

The report must attest that NONE of the following are present
anywhere in the chain:

```text
meaning
reference_certainty
ifadah
hukm
reality
ontological_claim
binding (DalMadlulBindingCandidate)
relation (RelationCandidate)
contractable_unit (ContractableUnitGeometry)
extra_letter_license (ExtraLetterLicense)
augmentation_category (C_Aug)
```

If any forbidden output is detected, the report refuses with
FailureCode.FORBIDDEN_LEAP.

---

## 7. Report rank ceiling

```text
CHAIN_REPORT_RANK_CEILING = MADLUL_BOUNDARY_RANK_CEILING
```

The report does not promote rank. Its chain_rank_ceiling field
reports the tightest ceiling encountered in the chain — which equals
MADLUL_BOUNDARY_RANK_CEILING since all ceilings in PR-10 through
PR-16 are equal.

---

## 8. FailureCode discipline

The report uses only existing FailureCode members:
- `GATE_REQUIRED` — input is not a VerbalMadlulCandidate.
- `RANK_EXCEEDS_CEILING` — rank monotonicity violated.
- `HIDDEN_RESIDUAL` — hidden-forbidden residual found.
- `FORBIDDEN_STRAIGHT_LINE` — forbidden output detected in chain.
- `TRACE_MISSING` — trace reference missing at any layer.

No new FailureCode members are introduced.

---

## 9. Forbidden surface (PR-16B)

```text
No DalMadlulBindingCandidate.
No meaning.
No reference certainty.
No ifadah, hukm, reality.
No ContractableUnitGeometry.
No RelationCandidate.
No ExtraLetterLicense.
No C_Aug.
No LicensedWeight.
No new linguistic layer.
No adapter or audit changes.
No new runtime dependencies.
No new FailureCode members.
No rank promotion.
No residual hiding.
```

---

## 10. Constitutional KPIs

```text
KPI-1: Vertical trace coverage — 100%.
        Every layer has a non-empty trace_ref.

KPI-2: Residual continuity — 100%.
        No residual disappears between layers.

KPI-3: Rank monotonicity — 100%.
        No rank increases between layers.

KPI-4: Named refusal coverage — 100%.
        Every refusal has a FailureCode.

KPI-5: Forbidden output absence — 100%.
        No meaning, relation, ifadah, hukm, reality.

KPI-6: Chain demonstrability — at least one canonical end-to-end
        test fixture that builds the full chain without mocks.
```

---

## 11. Golden law

```text
PR-16B proves the chain is one chain, not many islands.

The report reads the existing structure.
It adds no claim.
It promotes no rank.
It hides no residual.
It asserts no meaning.

It is the first vertical slice:
the moment the project sees itself as a single licensed chain.
```
