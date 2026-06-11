# 10 — Technical Terminology Non-Confusion Law

> **Status:** Constitutional declaration in PR-0. The starting cases
> entered the forbidden-transition registry in PR-5 as
> `TerminologyTransfer` rows. No lexicons, no glossaries, no
> terminological code in this repository at this stage.

## The law

```text
No technical term without a domain.
No domain without a scope.
No transfer of a technical term from one science to another without a
licensed bridge.
```

A *technical term* (اصطلاح) is a sign whose meaning has been *fixed by
the conventions of a specific science*. The same surface form may exist
in several sciences with mutually incompatible meanings. Reading the
form across sciences as if it were a single concept is a forbidden
straight line of the kind the engine refuses by construction.

## Canonical confusable terms (examples only — no code in PR-0)

The following are illustrations of the kind of confusion the law
forbids. They are *not* an enumeration; PR-5 added the typed registry.

```text
cause ≠ sabab (سبب) ≠ ʿillah (علة)
    across physics, fiqh, and philosophy.

qiyās (قياس) in logic ≠ qiyās in uṣūl al-fiqh ≠ qiyās in mathematics
    (analogy / juristic analogy / measurement).

root (جذر) in Arabic morphology ≠ root in mathematics ≠ root in botany
    (triliteral derivational locus / zero of a function / underground organ).

set in mathematics ≠ set in linguistics ≠ set in social science
    (collection / paradigmatic class / fixed group of people).

field in physics ≠ field in mathematics ≠ field in databases
    (region of force / algebraic structure / record column).
```

In every such case, the move from one science's usage to another is a
forbidden straight line until a `TerminologyBridgeGate` is supplied
that carries:

1. The *source domain* and its scope.
2. The *target domain* and its scope.
3. The *evidence* that the two usages share a stable mapping in this
   context.
4. The *residuals* that the mapping leaves unresolved.

## Why this law is separate from `04_FORBIDDEN_STRAIGHT_LINES.md`

The forbidden-transitions registry concerns *layer leaps* (e.g.,
`Evidence → Certainty`, `Tool → Knowledge`). The terminology
non-confusion law concerns *domain leaps within the same surface form*.
Both produce false outputs; both are forbidden as direct moves. They
are documented separately so that future contributors do not collapse
them into one mechanism.

## What entered PR-5

PR-5 added, *as data*, the starting entries of the form:

```text
(term, source_domain, target_domain, required_bridge_gate_name)
```

covering the `cause / sabab / ʿillah` and `qiyās` cases above — every
directed pair between the listed sciences, each naming
`TerminologyBridgeGate` as its required bridge. The rows live as
`TerminologyTransfer` carriers in
[`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py)
behind their own query surface
(`is_forbidden_term_transfer(term, source_domain, target_domain)`),
deliberately distinct from the layer-leap surface so the two laws
stay separate mechanisms. No lexicon files, no glossaries, and no
Arabic morphological code were added; no `TerminologyBridgeGate` is
implemented.
