# 109 — V0.229 Meta-Core Reconstruction & Derived-Law Recovery Law

> Status: constitutional reconstruction boundary + bounded test-template document.
> Scope: prove that the reduced V0.228 candidate can reconstruct pre-228 distinctions without hidden reintroduction.
> Snapshot date: 2026-08-10.

## §1 Constitutional transition after V0.228

After V0.228, reduction-by-search is closed. The governing condition is:

```text
Reduction is licensed iff Reconstruction survives.
```

So deletion count is never a success metric by itself.

## §2 Reduction stop law

For capability `C` and reduced core `M_C`:

```text
ReductionStop_C(M_C)
  <=> Reconstructive_C(M_C)
   and RegressionStable_C(M_C)
   and NoHiddenReintroduction_C(M_C)
```

Governance freeze is downstream of proof:

```text
ReductionStop_C(M_C) => FrozenMetaCore_C(M_C)
```

## §3 Frozen-core mutation guard

```text
FrozenMetaCore_C and not RegressionCertificate => not ChangeMetaCore
```

A failing test alone is insufficient. Any reopening request must carry a named
certificate object:

```text
RC = <Claim, OldVerdict, NewVerdict, Witness, TraceDifference, LostDistinction>
```

## §4 V0.229 objective and forbidden shortcut

`V0.229` is a reconstruction step, not a primitive-expansion step.

Required objective:

```text
Decode_X(M_C) ~=_C X_pre228
```

for each decoded constitutional concept `X`.

Forbidden shortcut:

```text
No new primitive may be introduced and counted as reconstruction success.
```

## §5 DerivedLawProof object (test-side constitutional template)

Every decoded concept must ship one explicit proof object:

```text
DLP_X = <Definition, Dependencies, PositiveWitness, Countermodel, Trace, EquivalenceProof>
```

This object is mandatory test input, not optional narrative.

## §6 Minimal decoded concept set for V0.229

The following decoded concepts must be represented through `DLP_X` objects:

- Witness (typed provider profile)
- Requirement (typed demand profile)
- Scope (licensing index)
- Domain (typing index)
- Authority (licensed satisfaction/operation jurisdiction)
- Closure (partial-operation closure property)
- Boundary (failure/non-definition frontier)
- Bridge (licensed reindexing/transport)
- Rank (trace/evidence-supported observational order)
- NoJump (absence of unlicensed typed transport)

## §7 Acceptance criteria (execution gate)

1. `AC-1 Law registration`
- `docs/109...` is present and indexed in `docs/README.md`.

2. `AC-2 DLP template completeness`
- A unified test template validates all six `DLP_X` fields as explicit,
  non-empty constitutional declarations.

3. `AC-3 Reconstruction equivalence discipline`
- Tests assert decode-equivalence by capability (`~=_C`) and refuse
  boolean-only shortcut claims.

4. `AC-4 Regression triad coverage`
- Regression checks include positive-path preservation, negative-path
  preservation, and residual-path preservation.

5. `AC-5 Local reopening discipline`
- On lost distinction, reopening is local:
  `Reopen(228, LostDistinction_X)` and not global reduction restart.

6. `AC-6 No hidden reintroduction`
- Any reconstruction that silently reintroduces removed primitives is refused.

## §8 Constitutional closure statement for this step

`V0.229` closes only when reconstruction proof objects are executable at test
level and decode-equivalence checks pass for the declared capability boundary.
This step does not authorize new runtime primitives.
