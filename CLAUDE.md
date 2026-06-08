# CLAUDE.md — Operating instructions for AI agents

This file gives any AI agent (Claude, Copilot, GPT-class) the *minimum
constitutional rules* they must obey when contributing to this repository.

If you are an agent reading this in a future session, treat the rules
below as load-bearing. They are not style suggestions.

---

## The governing law

```text
No output without a SlotGraph.
No SlotGraph without a Gamma closure state.
No transition without a Gate.
No Gate without Evidence, Rank, and a Residual policy.
No approved output with hidden residuals.
No straight line from Evidence to Certainty.
No straight line from Tool / Number / LCNV to Knowledge.
No technical term moves between sciences without a licensed bridge.
```

## Scope boundaries

1. **No claims about model internals.** This repository never asserts what
   GPT or any LLM "thinks" inside its weights or hidden chain-of-thought.
   It only wraps *emitted* claims with an auditable geometry. See
   `docs/01_BLACK_BOX_BOUNDARY.md`.
2. **No Arabic linguistic code** until the core kernel (`SlotGraph`,
   `Gamma`, `RankLattice`, `ResidualPolicy`, `TransitionGate`,
   `TraceLedger`) and the forbidden-transition registry are stable. See
   `docs/09_ARABIC_APPLICATION_BOUNDARY.md`.
3. **No LLM adapters** (OpenAI, Anthropic, local models) until PR-5+ and
   only behind the `ModelClient` protocol.
4. **No persistence, no network, no filesystem I/O** in `core/` or
   `contracts/`. The kernel must remain pure.
5. **No runtime dependencies** are added in PR-0 through PR-4. Only the
   standard library.

## Architectural rules for `core/`

- All core dataclasses are frozen and hashable where reasonable.
- Core functions are pure: they accept values and return values. They do
  not append to ledgers, write files, or call out to services.
- `gamma(graph)` returns a `GammaResult` containing a
  `TraceEntryCandidate`. The ledger appends the candidate *outside* the
  pure function.
- Every refusal returns a named `FailureCode`. Never raise bare
  exceptions for expected verdicts. Never silently return `None`.
- Every cross-slot or cross-layer move passes through a
  `TransitionGate`. The gate is the only path that can promote a rank.

## PR staging (do not collapse)

```text
PR-0  Scaffold + constitutional docs              ← current
PR-1  SlotGraph + GammaClosure (Rank/Residual as carriers only)
PR-2  RankLattice + ResidualPolicy + EvidenceContract
PR-3  TransitionGate + FailureTaxonomy
PR-4  Forbidden Straight-Line Registry (+ technical-terminology cases)
PR-5  AnswerAudit wrapper (ModelClient protocol only, no adapters)
```

Do not bundle PRs. Do not add Arabic code before PR-5. Do not add LLM
adapters before a dedicated post-PR-5 milestone.

## What to do when in doubt

Stop and ask the maintainer. Do not invent a bridge between layers.
Do not promote a rank. Do not hide a residual. The repository's value is
precisely that it refuses to let answers travel without an audit trail.
