# Terminology Control Map

This file provides a quick canonical naming map to prevent term drift across
docs, code, tests, and PR discussions.

It is subordinate to:

- `docs/10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`
- `docs/49_META_LANGUAGE_BOUNDARY_COVENANT.md`

When this file conflicts with a constitutional law document, the law document
wins.

## 1) Kernel canonical terms

- `SlotGraph`: constitutional mathematical object; never a free container.
- `Gamma` / `gamma(...)`: closure function over a licensed `SlotGraph`.
- `Rank` / `RankLattice`: bounded rank discipline for transitions.
- `Residual` / `ResidualPolicy`: visible residual governance; no hidden residuals.
- `TransitionGate`: only licensed transition path.
- `Trace` / `TraceLedger`: trace candidate and external append discipline.
- `FailureCode`: named refusal code for every non-approved verdict.

## 2) Vertical chain canonical candidate names

- `DalOnlyCandidate`
- `VerbalMadlulCandidate`
- `DalMadlulBindingCandidate`
- `ContractableUnitGeometry`
- `RelationCandidate`
- `MufradDalalahClosure`
- `RelationClosure`
- `IfadahCandidate`
- `HukmCandidate`
- `ManatCandidate`
- `TanzilCandidate`

Use these names as-is in docs/tests/reviews. Do not invent synonym labels for
the same runtime surface.

## 3) Post-vertical branch names

- `MantuqClosure`
- `MafhumClosure`
- `Maqul al-Dalalah` (discipline name from docs/51, not a new runtime layer)

## 4) GPT reasonableness branch names

- `MaqamGPT`
- `MantuqGPT`
- `MafhumGPT`
- `OriginBinding`
- `ReasonablenessVerdict`

## 5) Non-interchangeable terms (must not be collapsed)

- `Evidence` is not `Certainty`.
- `Candidate` is not `Certificate`.
- `Tool/Number/LCNV` is not `Knowledge`.
- `Signifier` is not `Meaning`.
- `Carrier declaration` is not `gate verdict`.

## 6) Writing rule for contributors

Before introducing a new term in docs or code comments:

1. Check if a canonical name already exists in this file or in docs/10 and docs/49.
2. Reuse the existing canonical name exactly when it matches the same concept.
3. If you must add a truly new term, define its boundary and non-equivalence
   explicitly in the governing law document first.
