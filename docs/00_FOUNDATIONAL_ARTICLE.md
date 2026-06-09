# 00 — Foundational article

## Why this repository exists

Large language models emit answers as opaque strings. There is no native
way for a reader to ask: *what is the layer of this claim? what is its
rank? what evidence supports it? what residuals remain? did it cross a
forbidden boundary on its way to my screen?*

`Taaqol-GPT` answers those questions for any claim that passes through
it. It is a **constitutional reasoning engine**: not a model, not a
parser, not a classifier. A *governance layer* that refuses to let an
output exist without an audit trail.

## The seven-stage pipeline

Every claim that enters the engine traverses the same fixed pipeline:

```text
Trace
  → SlotGraph
    → Gamma (minimal closure)
      → Candidate
        → Rank (lattice meet)
          → Residuals (policy evaluation)
            → TransitionContract (gate verdict)
              → ApprovedLimitedOutput
```

No stage may be skipped. No stage may be inverted. Each stage produces a
typed verdict; failure at any stage halts the pipeline with a named
`FailureCode` rather than a silent fallback.

## What the engine refuses

The engine refuses every *false straight line*. A false straight line is
any direct transition from a lower layer to a higher layer without an
intervening gate. Canonical examples (the full registry lands in PR-4):

```text
Binary       → Text
Unicode      → ArabicLetter
HarakaMark   → CaseFunction
Weight       → Agency
LexiconEntry → Candidate
Evidence     → Certainty
Candidate    → Certificate
ResidualHidden → ApprovedOutput
Tool/Number/LCNV → Knowledge
```

These transitions are not impossible. They are forbidden *as direct
moves*. They become legal only when mediated by a `TransitionGate` that
carries `Evidence`, satisfies the `RankLattice`, and clears the
`ResidualPolicy`.

## What the engine does *not* claim

It does not unpack the internal weights, activations, or hidden
chain-of-thought of any language model. See
[`01_BLACK_BOX_BOUNDARY.md`](01_BLACK_BOX_BOUNDARY.md).

## Six cores

The engine is organised around six cores, in deliberately small number:

```text
1. SlotGraph         — the geometric carrier of every entity
2. GammaClosure      — the minimal-closure verdict function
3. TransitionGate    — the only legal cross-layer move
4. RankLattice       — the bounded order over evidential strength
5. ResidualPolicy    — the law that surfaces and bounds leftovers
6. TraceLedger       — the append-only record that makes audit possible
```

Anything that is not one of these six cores is downstream of them.

## Staged roadmap

| PR    | Scope                                                                 |
| ----- | --------------------------------------------------------------------- |
| PR-0  | Scaffold + constitutional documents (this PR)                         |
| PR-1  | `SlotGraph` + `GammaClosure`; `Rank` and `Residual` as carriers only  |
| PR-2  | `RankLattice` + `ResidualPolicy` + `EvidenceContract` (lightweight)   |
| PR-3  | `TransitionGate` + `FailureTaxonomy`                                  |
| PR-4  | Forbidden Straight-Line Registry (+ technical-terminology cases)      |
| PR-5  | `AnswerAudit` wrapper — `ModelClient` protocol only, no LLM adapters  |

PRs are not bundled. The order is constitutional, not cosmetic: each
later PR depends on the typed verdicts produced by the earlier ones.

## The single sentence that captures it all

> Every claim that enters this engine leaves it as a *rank-bounded,
> residual-visible, trace-linked, gate-approved limited output* — or it
> does not leave at all.
