# 17 — SlotGraph Generation Law

> **Status:** Constitutional law. Ratified in PR-1C. The executable
> `SlotGraph` constructor that lands in PR-2 is bound by this
> document; no later PR may relax it.

This document closes the most dangerous loophole that PR-2 would
otherwise open:

```text
A SlotGraph can be constructed from a raw value,
look well-formed, and pass a local test —
while violating the constitution at the door.
```

The remedy is to fix, **before** the constructor is written, the
sources from which a `SlotGraph` may be born, the fields it must
carry at birth, and the refusals that bind its constructor.

The governing statement:

```text
SlotGraph is not a container.
SlotGraph is a constitutional mathematical object.

No SlotGraph from raw value.
No Slot without Boundary.
No Center without Trace.
No Opening without allowed potentials.
No Closure without Gamma.
No Output beyond declared boundary.
```

---

## 1. The three licensed generation sources

A `SlotGraph` may be generated **only** from one of three licensed
sources. Any other source is a constitutional refusal at construction
time, before `Γ` is consulted.

```text
1. DeclaredEntry
       A textual entry that satisfies the
       Textual Communication Entry Law (docs/15) and the
       Declared Entry Boundary Law (docs/11 §13).
       The entry produces a TextTraceCandidate, and the
       constructor lifts that candidate into a SlotGraph
       whose center carries the entry's identity claim.

2. Candidate
       A prior SlotGraph whose Γ verdict is
       MINIMALLY_CLOSED or PERFORATED_CLOSED, and whose
       rank is bounded at CANDIDATE under the rank lattice
       (docs/11 §8). The constructor copies the prior
       trace into the new graph's trace_ref and re-enters
       the Identity-to-Truth Licensing Chain (docs/16)
       from link 3 (Matching).

3. TransitionVerdict
       A prior SlotGraph whose Γ verdict went through a
       TransitionGate (PR-4) that returned APPROVED, with
       a named gate identifier preserved in the new
       graph's trace_ref. The constructor must record
       the gate identifier; an unnamed gate is a
       constitutional refusal.
```

Equivalently:

```text
No SlotGraph is generated from a raw string,
a raw bytes value, a raw dict, a free dataclass,
a partially constructed prior graph, or an unnamed
upstream verdict.
```

## 2. The mandatory fields at birth

A `SlotGraph` constructor must require **all** of the following
fields. A missing field is refused at construction time, never
deferred to `Γ`.

```text
Center               — the identity-preserving anchor
                       (docs/11 §2). Must carry an explicit
                       identity_claim and a trace_ref.

Domain               — the named domain the graph belongs to
                       (docs/11 §3). Empty domain is refused.

Scope                — the named scope inside the domain
                       (docs/11 §3). Empty scope is refused.

Boundary             — the perimeter declaration that names
                       its refusal codes (docs/11 §3). Boundary
                       without refusal codes is refused.

RequiredSlots        — the finite, non-empty set of slots whose
                       value_state must be FILLED for closure
                       (docs/11 §5).

OpeningPolicy        — the per-slot opening control that bounds
                       admissible fillings (docs/11 §4).

ClosurePolicy        — the named closure policy the graph claims
                       (e.g. minimally-closed branch, perforated
                       branch). The policy is declared at birth;
                       Γ verifies it.

RankCarrier          — a Rank value from the carrier enum
                       (docs/11 §8). Birth rank is bounded at
                       TRACE; CANDIDATE and above require a
                       prior Candidate source or a Gate verdict.

ResidualCarrier      — the finite set of declared Residual values
                       attached to the graph at birth. May be
                       empty; may not be unspecified.

TraceReference       — an opaque trace anchor inherited from the
                       generation source. Never None, never
                       synthesised inside the constructor.

OutputBoundary       — the declared layer the graph is allowed
                       to produce outputs into (docs/11 §5,
                       last clause). Outputs beyond this layer
                       are refused before they leave the graph.
```

Each field above maps onto an existing `FailureCode` in
`core/failure_taxonomy.py` (PR-1A). The constructor must use the
already-named carriers and must not invent new failure names in
PR-1C.

## 3. The constructor refusal table

The `SlotGraph` constructor that lands in PR-2 must implement the
following refusals using **only** `FailureCode` members that already
exist in PR-1A. The table is binding: the PR-2 implementation may
not return a different code for a row in this table.

```text
| Constructor refusal                          | Failure code            |
| Center missing                               | CENTER_MISSING          |
| Identity-claim missing                       | IDENTITY_BROKEN         |
| Domain missing or empty                      | DOMAIN_MISSING          |
| Scope missing or empty                       | SCOPE_MISSING           |
| Boundary missing or empty                    | BOUNDARY_MISSING        |
| Trace reference missing                      | TRACE_MISSING           |
| Required slot declared empty at birth        | REQUIRED_SLOT_EMPTY     |
| Opening outside slot boundary                | UNLICENSED_OPENING      |
| Output boundary beyond declared layer        | OUTPUT_EXCEEDS_LAYER    |
| Hidden / invisible residual at birth         | HIDDEN_RESIDUAL         |
| Blocking residual at birth                   | BLOCKING_RESIDUAL_PRESENT |
| Birth rank above the inferred ceiling        | RANK_EXCEEDS_CEILING    |
| Rank above TRACE without licensed source     | RANK_PROMOTION_WITHOUT_GATE |
| Source not in §1                             | FORBIDDEN_STRAIGHT_LINE |
| Crossing a layer with no Gate                | GATE_REQUIRED           |
```

A construction attempt that violates any row is `INVALID` (for the
structural rows) or `FORBIDDEN_LEAP` (for the source / layer rows),
per the verdict ordering of `Γ` in
[`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md) §7.

## 4. Forbidden generation forms

The following are constitutional refusals at the source level. None
of them may be added by any PR, including future PRs, without an
Amendment PR that opens them under a named gate.

```text
forbidden: SlotGraph(slots={...})                  — free container.
forbidden: SlotGraph.from_dict(payload)            — raw value.
forbidden: SlotGraph.from_text(s)                  — bypasses DeclaredEntry.
forbidden: SlotGraph(...)  without a Center        — missing identity.
forbidden: SlotGraph(...)  without a Boundary      — missing perimeter.
forbidden: SlotGraph(...)  without a TraceReference — missing trace.
forbidden: SlotGraph(...)  with rank ≥ CANDIDATE
           and no Candidate / Gate source           — unlicensed promotion.
forbidden: SlotGraph(...)  with synthesised center,
           boundary, domain, scope, or trace        — synthesis = refusal.
```

The list mirrors `docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md` §11
(No-Data-Container Law) and binds it specifically to the
constructor.

## 5. Constructor purity and totality

The constructor is bound by the same purity discipline as `Γ`
(`docs/11` §7):

```text
purity:        the constructor performs no I/O, no logging, no
               network, no filesystem access, no time reads.
totality:      every input either yields a valid SlotGraph or a
               named refusal. A constructor that raises a bare
               exception for an expected refusal is invalid.
no synthesis:  the constructor never fabricates a missing field.
no promotion:  the constructor never raises a rank above the
               value it receives from its generation source.
```

PR-1C does not write the constructor. PR-2 writes it; this document
binds what PR-2 must do.

## 6. Relationship to `Γ`

The constructor's refusals are a **strict subset** of `Γ`'s
ordering (`docs/11` §7). The same refusal must be emitted with the
same `FailureCode` whether it surfaces at construction time or at
closure time:

```text
construction refusal  ⇒  Γ would refuse with the same code.
Γ refusal             ⇏  the constructor would also refuse
                          (some Γ refusals depend on later
                          residual or rank information).
```

This subset relationship is mandatory. PR-2 may not return a
different code at construction time for a row in §3.

## 7. Relationship to PR-1A carriers

This law names obligations only with the carriers already shipped
in PR-1A:

```text
ClosureState, FailureCode, Rank, Residual, ResidualKind.
```

PR-1C deliberately does **not** add any new carrier, helper, or
function under `src/taaqqul_slot_geometry/`. The `SlotGraph` itself,
the `Slot`, the `Center`, the `Boundary`, the `Operation`, and the
constructor land in PR-2. This document is the law that PR-2 binds.

## 8. Anti-collapse rules

```text
no-bare-value:   No `SlotGraph` is generated from a raw value
                 (string, bytes, dict, list, free dataclass).
no-implicit:    No field listed in §2 may be defaulted, inferred,
                or auto-filled by the constructor.
no-fallback:    No "permissive" or "best-effort" constructor mode
                may be added in any PR.
no-shortcut:    No alternative entry point may bypass the three
                sources in §1.
no-merge:       The constructor and `Γ` may not be merged into one
                function; their orderings are distinct (see §6).
named-refusal:  Every refusal returns a named FailureCode and never
                a bare exception or a silent `None`.
```

## 9. Short constitutional summary

```text
لا SlotGraph من قيمة خام.
لا Slot بلا حدّ.
لا Center بلا أثر.
لا فتح بلا كمون مرخّص.
لا إغلاق بلا Γ.
لا مُخرَج خارج الحدّ المُعلَن.
```

In English:

```text
No SlotGraph from a raw value.
No Slot without a Boundary.
No Center without a Trace.
No Opening without licensed potential.
No Closure without Γ.
No Output beyond the declared boundary.
```

---

## Cross-references

- The mathematical foundation:
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
  §1–§11.
- The textual entry source:
  [`15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md`](15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md).
- The internal processing chain that runs inside a generated
  `SlotGraph`:
  [`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md).
- The Γ contract that consumes a generated `SlotGraph`:
  [`03_GAMMA_CLOSURE_CONTRACT.md`](03_GAMMA_CLOSURE_CONTRACT.md).
- The forbidden straight-line surface:
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md).
- The test-side schema that proves PR-2's constructor refusals:
  [`12_CONSTITUTIONAL_TEST_GEOMETRY.md`](12_CONSTITUTIONAL_TEST_GEOMETRY.md) §9.
- The PR-chain position of this document:
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) — PR-1C.

---

## PR-6 binding

Source 3 of §1 is now executable: `emit_successor(verdict,
input_graph)` in
[`src/taaqqul_slot_geometry/audit/successor.py`](../src/taaqqul_slot_geometry/audit/successor.py)
constructs a successor `SlotGraph` only from an `APPROVED`
`TransitionVerdict`, through the named construction surface
`SlotGraph.construct` with `GenerationSource.TRANSITION_VERDICT`.
The named gate is preserved in the successor's trace anchor
(`{parent_anchor}/gate/{gate_name}`), and the rank at birth is
exactly the gate's granted rank — emission never promotes. Every
other verdict state (`DEFERRED`, `BLOCKED`, `REJECTED`,
`FORBIDDEN_LEAP`) is a constructor refusal carrying the verdict's
own `FailureCode`: only an audit record remains. An approval whose
verdict does not trace back to the input graph's anchor is refused
as `IDENTITY_BROKEN` (docs/16 link 2). No `SlotGraph` from a raw
verdict either: the function checks its domain loudly
(`TypeError`) before any constitutional verdict.
