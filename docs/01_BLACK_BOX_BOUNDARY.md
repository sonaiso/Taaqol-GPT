# 01 — The black-box boundary

This document fixes, in precise language, what this repository **does
not** claim. The boundary is constitutional. Any future contribution
that crosses it is out of scope and must be rejected, even if it is
otherwise correct.

## The exact wording

> We cannot expose the internal weights or hidden chain-of-thought of
> any language model. We can, however, build an external governing layer
> that makes every emitted answer traceable, evaluable, rank-bounded,
> residual-visible, evidence-linked, and boundary-aware.

## What this means in practice

The engine never:

1. Asserts what a model "thought" between input and output.
2. Reports activations, attention patterns, logits, or any internal
   tensor as if it were a reason.
3. Treats a model's self-reported chain-of-thought as a privileged
   source of truth. Self-reports are themselves claims that must pass
   through the same `SlotGraph → Gamma → Gate` pipeline as any other
   claim.
4. Tags any output as `CERTIFICATE` rank merely because a model
   expressed high confidence. Model confidence is not evidence.

## What the engine *does* do

The engine wraps the *observable surface* of a model — the prompt it
received and the answer it emitted — and forces the answer through the
seven-stage pipeline described in
[`00_FOUNDATIONAL_ARTICLE.md`](00_FOUNDATIONAL_ARTICLE.md). The result
is an `AuditedAnswer`: a structured object in which every claim carries
its own `gamma_state`, `rank`, `evidence_refs`, and `residuals`.

The engine therefore converts:

```text
Black-box answer
```

into:

```text
Auditable answer
```

That is the entire promise. Nothing more, nothing less.

## Why the boundary is load-bearing

If the engine claimed to expose model internals, it would itself be
guilty of the forbidden straight line `Tool/Number/LCNV → Knowledge` —
treating a measurement of the model (an activation, a probability) as
knowledge about the world. The whole point of the engine is to refuse
that move. It must refuse it about *itself* first.

## PR-6 binding

PR-6 binds this boundary in code. The observable surface is typed as
the `ModelClient` protocol in
[`src/taaqqul_slot_geometry/audit/model_client.py`](../src/taaqqul_slot_geometry/audit/model_client.py):
a single `complete(prompt) -> str` — the engine sees the prompt it
sent and the text that came back, nothing else. The protocol is
structural and deliberately empty of transport: concrete adapters
(OpenAI, Anthropic, local models) remain forbidden until the
dedicated post-PR-6 milestone.

`AnswerAudit.audit` wraps each emitted answer as the promised
`AuditedAnswer`: the claim's `gamma_state`, gate verdict, granted
`rank`, `evidence_refs`, and full residual surface travel with the
text. Model confidence never enters the rank meet (rule 4 above) —
only the `EvidenceContract`, the input graph's rank, the gate's own
rank, and the residual ceiling do. No audit creates approval by
itself: an `AuditedAnswer` without an `APPROVED` gate verdict
carries `Rank.ZERO`, a named `FailureCode`, and no successor graph.
