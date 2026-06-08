# 11 — Mathematical Slot Geometry Laws

> **Status:** Constitutional law. Ratified in PR-1. Every later PR
> binds these laws in code; no later PR may relax them.

This document is the mathematical core of the repository. It
specifies the structure that every `SlotGraph`, every `Γ` verdict,
every `Gate`, every `Rank` promotion, every `Residual` declaration,
and every `Trace` entry **must** preserve.

The shorter governing statements live in
[`02_SLOT_GEOMETRY_CONSTITUTION.md`](02_SLOT_GEOMETRY_CONSTITUTION.md);
this document gives the formal versions and the obligations they
impose on any implementation.

## 1. SlotGraph as Constitutional Mathematical Object

A `SlotGraph` is the nine-tuple

```text
G = ⟨C, S, E, B, Ω, R, Δ, T, Γ⟩
```

where

```text
C  = Center          — identity-preserving anchor
S  = Slots           — finite set of constitutional slots
E  = Edges           — directed structural relations over S
B  = Boundaries      — perimeter declarations
                       (domain, scope, output_boundary)
Ω  = Operations      — finite set of licensed operations on G
R  = Rank            — carrier rank in the bounded order
Δ  = Residuals       — finite set of declared residuals
T  = Trace           — opaque reference to the trace anchor
Γ  = Closure         — the pure verdict function Γ: G ↦ ClosureState
```

A construct that omits any component of `G` is not a `SlotGraph`. The
implementation must refuse it at construction time, not at closure
time. ``Γ`` is named in the tuple because closure is part of the
graph's identity, not an afterthought.

## 2. Center Law

The `Center` is the identity-preserving anchor:

```text
C = ⟨identity_claim, domain, scope, trace_ref⟩
```

Law:

```text
∀ G. Γ(G) ∈ {MINIMALLY_CLOSED, PERFORATED_CLOSED}
      ⇒ C is present ∧ identity_claim is present ∧ trace_ref is present.
```

Consequence: a missing center forces `INVALID / CENTER_MISSING` at
step 1 of `Γ`. The center is never inferred; it is declared by the
constructor of the graph.

## 3. Boundary Law

A `Boundary` declares the licensed perimeter:

```text
B = ⟨domain, scope, licensed_operations, refusal_codes⟩
```

Laws:

```text
∀ slot s ∈ S. s carries a Boundary.
∀ Boundary b. b.domain ≠ ∅ ∧ b.scope ≠ ∅.
∀ operation ω applied to G. ω ∈ Ω ∧ ω respects every traversed Boundary.
```

A boundary is *named by its refusals*: it lists the `FailureCode`s a
crossing would emit. Boundaries are prescriptive, not descriptive.

## 4. Opening Law

An `Opening` is licensed unresolved potential:

```text
opening(slot s) =
  { admissible filling positions p
    such that p ∈ s.boundary.licensed_domain }
```

Laws:

```text
∀ slot s. opening(s) ⊆ s.boundary.licensed_domain.
A filling outside s.boundary is an UNLICENSED_OPENING and is refused
before Γ is consulted.
```

Opening is *not* generic absence. A slot may be `EMPTY` but its
opening — the set of positions it may legally accept — is bounded
upfront.

## 5. Closure Law

Closure is boundary satisfaction under constraints, **not** truth:

```text
closure(G) holds iff
    (∀ required slot s ∈ S. s.value_state = FILLED)
  ∧ (∀ slot s ∈ S. s.value_state ≠ BROKEN)
  ∧ (∀ residual δ ∈ Δ. δ.kind ≠ HIDDEN_FORBIDDEN ∧ δ.visible)
  ∧ (G.output_boundary ⪯ G.declared_layer)
  ∧ C is present ∧ T is present.
```

Axiom (constitutional, non-negotiable):

```text
ClosureState ≠ TruthState.
```

`MINIMALLY_CLOSED` does not assert truth. It asserts that the
required positions for *this* boundary are filled with identity
intact and trace preserved. Any code path that treats a closure
verdict as a truth verdict violates this law.

## 6. Perforated Closure Law

```text
PERFORATED_CLOSED(G) ⇔
    closure(G)
  ∧ (∀ residual δ ∈ Δ. δ.kind ≠ BLOCKING)
  ∧ (∃ residual δ ∈ Δ. δ.kind ∈ {NON_BLOCKING, DEFERRABLE, EXPLANATORY}
                       ∧ δ.visible).
```

Output law for perforated closure:

```text
Γ(G) = PERFORATED_CLOSED
  ⇒ G may license at most a Candidate,
    bounded by the rank ceiling of §8.
  ⇒ G never licenses a Certificate.
```

## 7. Gamma Closure Function

`Γ : SlotGraph → ClosureState` is pure and ordered. The order is:

```text
Γ(G):
  1.  if C absent or identity_claim absent      → INVALID/CENTER_MISSING
  2.  if T absent                               → INVALID/TRACE_MISSING
  3.  if any of (domain, scope, boundary) absent
                                                → INVALID/{DOMAIN,SCOPE,BOUNDARY}_MISSING
  4.  if ∃ s ∈ S. s.value_state = BROKEN        → INVALID/IDENTITY_BROKEN
  5.  if G.output_boundary ≻ G.declared_layer   → FORBIDDEN_LEAP/OUTPUT_EXCEEDS_LAYER
  6.  if ∃ δ ∈ Δ. δ.kind = HIDDEN_FORBIDDEN
        or ¬δ.visible                           → INVALID/HIDDEN_RESIDUAL
  7.  if ∃ δ ∈ Δ. δ.kind = BLOCKING             → BLOCKED/BLOCKING_RESIDUAL_PRESENT
  8.  if ∃ required s ∈ S. s.value_state = EMPTY → OPEN/REQUIRED_SLOT_EMPTY
  9.  compute ceiling = meet(EvidenceRank, IdentityRank,
                             ResidualCeiling, GateRank)
        and verify no path exceeds ceiling      → INVALID/RANK_EXCEEDS_CEILING
  10. if ∃ visible non-blocking residual        → PERFORATED_CLOSED
      else                                      → MINIMALLY_CLOSED
```

Properties `Γ` must satisfy in any binding implementation:

```text
purity:       Γ has no side effects. It does not mutate G, append to
              the ledger, perform I/O, or call out to services.
totality:     ∀ G. Γ(G) is defined and is exactly one ClosureState.
ordering:     The first failing check determines the verdict.
named refusal: every non-closure verdict carries a FailureCode.
no synthesis: Γ never fabricates a missing center, boundary, domain,
              scope, or trace; it refuses.
```

## 8. Rank Ceiling Law

The rank lattice is the bounded total order

```text
ZERO < TRACE < CANDIDATE < HYPOTHESIS < LICENSED < STRONG < CERTIFICATE
```

with monotone `meet`. The non-promotion law:

```text
OutputRank(G) ≤ meet(EvidenceRank,
                     IdentityRank,
                     GateRank,
                     ResidualCeiling).
```

Corollaries:

```text
* No code path may produce a rank greater than the meet of its inputs.
* Only a TransitionGate may raise a Rank, and only to a value ≤ the meet.
* A single evidence source may never license CERTIFICATE.
* Evidence → Certainty is a forbidden straight line (see §10).
```

PR-1 ships `Rank` as a carrier enum. The `meet`, the ceiling
computation, and the gate-bound promotion land in PR-3.

## 9. Residual Visibility Law

Residual kinds:

```text
ResidualKind ∈ {
  BLOCKING,
  DEFERRABLE,
  NON_BLOCKING,
  EXPLANATORY,
  HIDDEN_FORBIDDEN,
}
```

Laws:

```text
visibility:    ∀ approved output O of G. every residual δ ∈ Δ that
               applies to O appears in O, except residuals of kind
               EXPLANATORY that the policy explicitly suppresses.
fatality:      ∃ δ ∈ Δ. δ.kind = HIDDEN_FORBIDDEN ∨ ¬δ.visible
                  ⇒ Γ(G) = INVALID ∧ no Gate may approve G.
ceiling:       ResidualCeiling(G) = meet over δ ∈ Δ of rank-cap(δ.kind),
               and feeds the rank ceiling of §8.
```

`ResidualHidden → ApprovedOutput` is forbidden. This is not advisory.

## 10. Forbidden Straight-Line Law

A *forbidden straight line* is a direct transition from a lower layer
to a higher layer **without** an intervening `TransitionGate` that
carries `Evidence`, satisfies the `RankLattice`, and clears the
`ResidualPolicy`.

```text
∀ transition s → t.
   layer(t) > layer(s)
   ∧ no Gate g with g(Evidence, Rank, Residuals) = APPROVED
   ⇒ Γ-or-Gate emits FORBIDDEN_STRAIGHT_LINE.
```

The typed registry of canonical forbidden transitions and their
required bridges lands in PR-5. PR-1 names the failure code; doc 04
records the table.

## 11. No-Data-Container Law

```text
SlotGeometry is not a data structure first.
It is a constitutional mathematical object first.
```

Refusals enforced by review and by tests:

```text
forbidden: class Slot(name, value).
forbidden: class SlotGraph(slots).
forbidden: a Slot without (boundary, domain, scope, rank, residuals, trace_ref).
forbidden: a SlotGraph without (center, boundaries, rank, residuals, trace).
forbidden: a Γ implementation whose order differs from §7.
forbidden: a Gamma return that depends on the verdict of a Gate or a
           rank promotion (Γ runs before any Gate; the Gate consults Γ).
forbidden: any approved output produced without a SlotGraph + Γ + Gate.
```

A pull request that introduces a free container under any of the
reserved names is rejected at review.

## 12. Implementation Obligations

Every PR that binds part of this constitution must satisfy the
following, in addition to the laws above:

1. **Frozen dataclasses.** Every constitutional object is
   `frozen=True, slots=True`. A transition constructs a new graph.
2. **Pure core.** Modules under `core/` perform no I/O, no logging,
   no network, no filesystem access, no time reads. They depend only
   on the Python standard library through PR-4.
3. **Named refusals.** Every refusal returns a `FailureCode` member.
   No bare exceptions for expected verdicts; no silent `None`.
4. **No synthesis.** No implementation may fabricate a missing
   center, boundary, domain, scope, or trace. Missing = refuse.
5. **No promotion outside a gate.** Only a `TransitionGate` may raise
   a `Rank`, and only to a value bounded by the lattice `meet`.
6. **Trace is opaque to core.** Core carries `trace_ref` as an opaque
   identifier. The `TraceLedger` lives outside the pure verdict
   functions and is appended by the caller.
7. **PR staging is not negotiable.** The carriers in PR-1, the
   executable `SlotGraph` + `Γ` in PR-2, `RankLattice` +
   `ResidualPolicy` + `Evidence` in PR-3, `TransitionGate` in PR-4,
   the forbidden-transition registry in PR-5, the `AnswerAudit`
   wrapper in PR-6.

Any change to this document is a constitutional amendment. Treat it
as load-bearing: a single relaxation here can unlock an
audit-violating output downstream.

## 13. Declared Entry Boundary Law

The engine is permitted to declare an *operational entry point* —
the layer at which the current milestone begins to execute. The
current declared operational entry is:

```text
DeclaredOperationalEntry = ArabicVocalizedText
                         = نص عربي مشكول منضبط
```

This declaration is a *scope of execution*, not a *claim of origin*.
The pre-text chain — human voice, binary audio, binary text, Unicode
encoding, code points, graphemes — remains constitutionally
acknowledged as prior trace, but is **out of current execution**
unless a future PR explicitly opens its gate.

Governing identity:

```text
DeclaredEntry ≠ OntologicalOrigin.
```

Or, equivalently:

```text
ما قبل النص ليس خارج الوجود.
بل خارج التنفيذ الحالي ما لم يُصرّح به.
```

### 13.1 Three layers of beginning

```text
OntologicalTrace      — HumanVoice, HumanWriting, SourceEvent
EncodingTrace         — BinaryAudio, BinaryText, Unicode,
                        CodePoint, Grapheme
DeclaredOperational   — ArabicVocalizedText  (current entry)
```

Only the third layer is executed by the current pipeline. The
first two layers are *named and preserved* as prior trace; they
are never erased and never silently collapsed into the third.

### 13.2 Boundary obligations on every SlotGraph

Every `SlotGraph` that enters at the declared operational entry
must carry an `entry_boundary` declaration of the form:

```text
entry_boundary:
  declared_entry_kind: ARABIC_VOCALIZED_TEXT
  prior_trace_status:  OUT_OF_CURRENT_EXECUTION
  prior_trace_kinds:
    - HUMAN_VOICE
    - BINARY_AUDIO
    - BINARY_TEXT
    - UNICODE_ENCODING
    - CODE_POINT
    - GRAPHEME
  claim: "not evaluated in this pipeline"
```

The carrier for this declaration lands with the executable
`SlotGraph` in PR-2. PR-1A ratifies the law; later PRs bind it in
code. No `SlotGraph` may omit `entry_boundary`; missing = refuse.

### 13.3 Forbidden pre-text collapses

The Declared Entry Boundary Law forbids any direct collapse from
a pre-text layer to a text, letter, sound, or meaning layer. The
following identities are constitutional refusals:

```text
BinaryAudio    ≠ Text.
BinaryText     ≠ Unicode.
Unicode        ≠ ArabicLetter.
CodePoint      ≠ Phoneme.
Grapheme       ≠ FunctionalLetter.
ArabicText     ≠ Meaning.
VocalizedText  ≠ ValidAnalysis.
DeclaredEntry  ≠ OntologicalOrigin.
```

In particular, the system may never reason:

```text
لدينا نص → إذن لدينا حرف عربي وظيفي.
لدينا Unicode → إذن لدينا دال.
لدينا حركة → إذن لدينا وظيفة.
لدينا نص مضبوط → إذن لدينا معنى.
```

A vocalized text yields only a `TextTraceCandidate`. It does not
yield `LetterIdentity`, `Phoneme`, `Meaning`, or `Judgment`.

### 13.4 No-erasure of prior trace

```text
Operational entry may omit prior layers from execution,
but may not erase them from constitutional trace.
```

Equivalently:

```text
يجوز للبداية التشغيلية أن تستثني ما قبلها من التنفيذ،
لكن لا يجوز لها أن تمحو ما قبلها من الأثر الدستوري.
```

### 13.5 Scope of this PR

PR-1A ratifies the Declared Entry Boundary Law as constitutional
text only. It **does not** introduce:

```text
ASR
audio decoders
binary-text decoders
Unicode normalisation
phoneme extractors
encoding pipelines
```

The forbidden pre-text transitions are recorded in doc 04
(§ Pre-text declared-entry transitions). Their required bridge
gates are *declared but not implemented*; each gate is opened only
by an explicit future PR that satisfies the
`Forbidden Straight-Line Law` (§10).

The short constitutional summary:

```text
النص ليس الصوت.
Unicode ليس حرفًا.
BinaryText ليس Unicode.
BinaryAudio ليس نصًا.
والبداية التشغيلية لا تمحو أثر ما قبلها.
```
