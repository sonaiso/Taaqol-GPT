# 02 — Slot Geometry Constitution

> **Status:** Constitutional law. PR-1 ratifies the mathematical
> surface below; the executable ``SlotGraph`` and ``Γ`` land in PR-2.

`SlotGeometry` is **a constitutional mathematical object, not a free
data container.** Every implementation in this repository — every
present one and every future one — must preserve the structure named
here. A class whose name is ``SlotGraph`` but whose shape omits a
center, a boundary, a domain, a scope, a rank, a residual surface, or
a trace is not a ``SlotGraph``; it is a free container, and the
constitution refuses it.

## The first law

```text
No SlotGraph without Constitutional Geometry.
No Slot without Boundary.
No Boundary without Domain and Scope.
No Closure without Gamma.
No Gamma without Rank and Residual visibility.
No Output without Trace.
```

For the full mathematical statement of these laws, see
[`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md).

## The six cores

1. **`SlotGraph`** — the geometric carrier of every entity that enters
   the engine. A nine-tuple `⟨C, S, E, B, Ω, R, Δ, T, Γ⟩` (center,
   slots, edges, boundaries, licensed operations, rank, residuals,
   trace, closure). See doc 11 §1.
2. **`GammaClosure`** — the pure verdict function
   `Γ : SlotGraph → ClosureState`. Returns one of `OPEN`,
   `MINIMALLY_CLOSED`, `PERFORATED_CLOSED`, `BLOCKED`, `INVALID`,
   `FORBIDDEN_LEAP`. See doc 03 and doc 11 §7.
3. **`TransitionGate`** — the only legal cross-layer or cross-slot
   move. Requires `Evidence`, `Rank`, and a `ResidualPolicy` result.
   Returns one of `APPROVED`, `DEFERRED`, `BLOCKED`, `REJECTED`,
   `FORBIDDEN_LEAP`. See doc 08.
4. **`RankLattice`** — the bounded total order
   `ZERO < TRACE < CANDIDATE < HYPOTHESIS < LICENSED < STRONG < CERTIFICATE`
   with a monotone `meet` operation. No rank promotion without a
   gate. See doc 05 and doc 11 §8.
5. **`ResidualPolicy`** — the law that classifies residuals as
   `BLOCKING`, `DEFERRABLE`, `NON_BLOCKING`, `EXPLANATORY`, or
   `HIDDEN_FORBIDDEN`, and computes a ceiling rank for the output.
   See doc 06 and doc 11 §9.
6. **`TraceLedger`** — the append-only record of every verdict the
   engine has produced. Required for audit; *not* called from inside
   pure core functions. See doc 07.

## The constitutional shape of a Slot

A `Slot` is a constitutional contract, never a `(name, value)` pair.
Every implementation must carry, at minimum, this tuple:

```text
Slot = ⟨id, kind, domain, scope, required, value_state,
        boundary, evidence_ref, rank, residuals, trace_ref⟩
```

- `id` — stable identity within the graph.
- `kind` — what *kind* of position this is (e.g., role, anchor,
  modifier). Kinds are declared, not inferred.
- `domain` — the science / register the slot belongs to.
- `scope` — the bounded layer within that domain.
- `required` — whether the slot must be filled for any closure verdict
  other than `OPEN`.
- `value_state` — one of `EMPTY`, `FILLED`, `BROKEN` (a single
  `BROKEN` slot drives the graph to `INVALID`).
- `boundary` — the licensed perimeter of acceptable fillings.
- `evidence_ref` — opaque reference to the supporting evidence
  record. The slot does not *contain* the evidence; it points to it.
- `rank` — the local rank carrier (capped by `RankLattice`).
- `residuals` — the residual surface this slot exposes upward.
- `trace_ref` — opaque reference to the trace entry that produced
  this slot's current state.

A `(name, value)` pair carrying anything less is not a slot. It is a
record. Refuse it.

## The constitutional shape of the Center

The `Center` is the identity-preserving anchor of a graph. It is not
a label. Its sole job is to prevent the subject from silently
mutating during closure:

```text
A drawn glyph is not a sound.
A sound is not a functional letter.
A signifier is not a meaning.
A lexicon entry is not a candidate.
Evidence is not certainty.
```

```text
Center = ⟨identity_claim, domain, scope, trace_ref⟩
```

Law of the Center:

```text
No Γ without Center.
No Center without IdentityClaim.
No IdentityClaim without Trace.
```

## The constitutional shape of a Boundary

A `Boundary` declares the licensed perimeter for a slot, an edge, an
operation, or the graph's output:

```text
Boundary = ⟨domain, scope, licensed_operations, refusal_codes⟩
```

A boundary is *prescriptive*, not descriptive. Crossing it without a
licensed operation is a `FORBIDDEN_LEAP`. Producing an output above
the graph's `output_boundary` is a `FORBIDDEN_LEAP`. The boundary
*is* the law of what is permitted, named by its refusals.

## The constitutional shape of Opening

An `Opening` is a **licensed unresolved potential** — not generic
absence. A slot may open *only* onto positions admissible inside its
domain and scope. The set of admissible openings for a slot is part
of the slot's boundary. An opening that escapes its boundary is an
`UNLICENSED_OPENING` and is refused before closure is attempted.

## The constitutional shape of Closure

`Closure` is not "truth". `Closure` is:

```text
Closure = boundary satisfaction
          under rank and residual constraints,
          identity preserved.
```

Hence the load-bearing distinction the implementation must preserve:

```text
ClosureState ≠ TruthState
```

A `MINIMALLY_CLOSED` graph is *not* a certificate. It is a graph that
has filled every required slot inside its declared boundary, with no
hidden residual and no broken identity. The output it licenses is
bounded by the rank ceiling computed from evidence and residuals.

## The constitutional shape of Perforated Closure

`PERFORATED_CLOSED` is a mathematical state, not a metaphor:

```text
PERFORATED_CLOSED(G) ⇔
    (every required slot in B is filled)
  ∧ (no residual ∈ Δ has kind = BLOCKING)
  ∧ (no residual ∈ Δ has kind = HIDDEN_FORBIDDEN
       and no residual ∈ Δ has visible = false)
  ∧ (no slot ∈ S has state = BROKEN)
  ∧ (output_boundary ⪯ declared_layer)
  ∧ (∃ residual ∈ Δ with kind ∈ {NON_BLOCKING, DEFERRABLE, EXPLANATORY})
```

The output a perforated closure licenses is a `Candidate` bounded by
the rank ceiling, never a `Certificate`. See doc 11 §6.

## Immutability law

All core dataclasses are frozen and hashable where reasonable. A
transition does not mutate a `SlotGraph`; it constructs a new one.
This is a constitutional requirement, not a style preference: a
mutable `SlotGraph` cannot carry a stable trace, and an engine
without a stable trace cannot honour the audit law.

## Purity law

Core functions are pure. They accept values and return values. They
do not append to ledgers, write files, or call out to services. In
particular, `Γ(G)` returns a `ClosureState` (and, in the PR-2
binding, a `TraceEntryCandidate`); appending to the `TraceLedger` is
the caller's job. See doc 07.

## No-Data-Container law

```text
SlotGeometry is not a data structure first.
It is a constitutional mathematical object first.
```

A pull request that adds a class named `SlotGraph`, `Slot`, `Gamma`,
`Gate`, `Rank`, `Residual`, or `Trace` without preserving the
constitutional structure above is rejected. The names are reserved
*by the constitution*; the executable shapes that may bind them are
specified in doc 11 §12 and ratified by their numbered docs.

## What PR-1 ratifies vs. what PR-2 implements

PR-1 ratifies this constitution and ships **names only** as carrier
enums (`Rank`, `ResidualKind`, `ClosureState`, `FailureCode`) so the
docs and tests can reference exact identifiers. The executable
`SlotGraph`, the validators, and the pure `Γ` land in PR-2 and must
match this constitution exactly.

The detailed contracts for each core live in the matching numbered
documents (`03`–`08`, `11`).
