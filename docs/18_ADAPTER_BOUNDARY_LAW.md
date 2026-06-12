# 18 — Adapter Boundary Law

> **Status:** Constitutional law. Ratified in PR-7; chain position
> ratified by Amendment-1
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). PR-7 is
> law only: no executable adapter, no `src/` change, no `tests/`
> change ships with this document. The first concrete `ModelClient`
> adapter lands in PR-8 and is bound by this document; no later PR
> may relax it.

This document closes the most dangerous loophole that PR-8 would
otherwise open:

```text
A concrete adapter can implement ModelClient.complete,
look like a harmless transport shim, and pass a local test —
while smuggling judgment, ledger writes, rank claims, or
model-internal structure across the docs/01 boundary.
```

The remedy is to fix, **before** any adapter is written, the shape
an adapter must be born into, the guard that admits or refuses it,
the I/O it is licensed to perform, and the refusals that bind it.

The governing statement:

```text
An adapter is a transport, not a judge.

No adapter outside the ModelClient protocol.
No adapter output except one emitted answer string.
No answer reaches the caller except through AnswerAudit.
No adapter verdict. No adapter ledger write. No adapter successor.
No adapter-decided APPROVED. No adapter rank.
No model confidence as evidence.
No network or persistence beyond what this law licenses.
```

---

## 1. The licensing chain

The only constitutional path from a concrete model transport to a
system output is:

```text
ModelClient protocol → ConcreteAdapterCandidate → AdapterGuard → AuditedAnswer only
```

```text
1. ModelClient protocol
       The black-box boundary of docs/01 in protocol form
       (PR-6 — src/taaqqul_slot_geometry/audit/model_client.py):
       complete(prompt) -> str, and nothing else. A concrete
       adapter implements this protocol; it never widens it.
       No streaming surface, no sampling controls, no logits,
       no token probabilities, no hidden chain-of-thought
       crosses this boundary.

2. ConcreteAdapterCandidate
       An adapter at birth is a candidate, not a licensed
       transport. It must carry every declaration of §2 at
       construction time. A candidate with a missing or
       synthesised declaration is refused, never repaired.

3. AdapterGuard
       The structural checkpoint that admits or refuses a
       candidate before AnswerAudit may hold it. The guard's
       verdict is admission of a transport, never approval of
       an answer (§5). Every refusal is named with an existing
       FailureCode (§3).

4. AuditedAnswer only
       The assembled stack has exactly one output surface: the
       AuditedAnswer produced by AnswerAudit (docs/01). A raw
       adapter string is an internal value, never a system
       output. There is no second door.
```

Equivalently:

```text
No adapter is assembled from a bare callable, a free object
with a complete attribute bolted on at admission time, an
undeclared transport, or an unguarded candidate.
```

## 2. The mandatory declarations at birth

A `ConcreteAdapterCandidate` must require **all** of the following
declarations. A missing declaration is refused at construction
time, never deferred to the guard, and never auto-filled.

```text
AdapterIdentity     — the non-empty name of the adapter itself
                      (which transport shim is this). An unnamed
                      adapter cannot be joined to a trace story.

ModelIdentity       — the non-empty declared identity of the model
                      behind the transport. Recorded verbatim as a
                      claim about provenance; it is never evidence
                      (docs/01 — model self-description carries no
                      epistemic weight).

TransportSurface    — the declared I/O class of the adapter, one of:
                      IN_MEMORY       (no I/O at all),
                      LOCAL_PROCESS   (local runtime, no network),
                      NETWORK         (remote model endpoint).
                      An undeclared transport is a refusal: the
                      perimeter of the adapter is its boundary.

CompletionCallable  — the complete(prompt) -> str implementation
                      satisfying ModelClient structurally. The one
                      required slot of the candidate.

Configuration       — endpoints, credentials, and model parameters
                      enter at birth as constructor arguments
                      supplied by the caller. The adapter never
                      goes looking for configuration (environment,
                      filesystem, network discovery) on its own.
```

No defaults, no synthesis, no "best-effort" candidate mode. The
candidate is a frozen declaration, not a configurable service.

## 3. The AdapterGuard refusal table

The `AdapterGuard` that lands in PR-8 must implement the following
refusals using **only** `FailureCode` members that already exist
(PR-1A — `core/failure_taxonomy.py`). The table is binding: the
PR-8 implementation may not return a different code for a row in
this table, and may not add new `FailureCode` members for it.

```text
| Guard refusal                                   | Failure code                |
| Adapter identity missing or empty               | IDENTITY_BROKEN             |
| Model identity missing or empty                 | IDENTITY_BROKEN             |
| Transport surface undeclared                    | BOUNDARY_MISSING            |
| Completion callable missing / not ModelClient   | REQUIRED_SLOT_EMPTY         |
| I/O beyond the declared, licensed surface (§4)  | UNLICENSED_OPENING          |
| Adapter exposes a verdict surface               | FORBIDDEN_STRAIGHT_LINE     |
| Adapter exposes confidence / internals as       | FORBIDDEN_STRAIGHT_LINE     |
|   evidence (Tool/Number/LCNV → Knowledge)       |                             |
| Adapter exposes a TraceLedger write surface     | OUTPUT_EXCEEDS_LAYER        |
| Adapter exposes a successor-graph surface       | GATE_REQUIRED               |
| Adapter exposes a rank claim                    | RANK_PROMOTION_WITHOUT_GATE |
```

A wrong *type* handed to the guard (not a candidate at all) is a
programmer mistake refused loudly with `TypeError`, consistent
with the PR-6 audit surface; everything in the table above is an
expected, named constitutional refusal — a value, never a bare
exception.

## 4. The licensed I/O surface

PR-8's forbidden surface in
[`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) bans "network
or persistence beyond what docs/18 explicitly licenses". This
section is that explicit license. Anything not listed is refused.

```text
1. Call-scoped I/O only. All transport I/O happens inside
   complete() and nowhere else. Import-time and construction-time
   I/O are forbidden (construction consumes declarations; it
   contacts nothing).

2. One prompt in, one emitted string out. The adapter sends
   exactly one prompt and returns exactly one answer string per
   call. A streaming transport must be joined into a single
   string before the boundary is crossed; no partial state leaks.

3. No persistence. The adapter stores nothing across calls beyond
   its birth declarations: no caches, no logs, no files, no
   queues. A caching or logging adapter requires its own future
   law.

4. No model internals. Logits, token probabilities, sampling
   metadata, hidden chain-of-thought, and self-reported
   confidence must not cross the return boundary even when the
   transport exposes them (docs/01).

5. Only the declared surface. An IN_MEMORY adapter performs no
   I/O; a LOCAL_PROCESS adapter touches no network; a NETWORK
   adapter contacts only the endpoint declared at birth.

6. Dependencies stay optional. The base package remains free of
   runtime dependencies. A concrete adapter's transport
   dependency may be licensed only as an optional extra
   (pyproject [project.optional-dependencies]) scoped to that
   adapter, imported only inside the adapter's own module. The
   kernel and the audit layer import nothing new.
```

## 5. Admission is not approval

The `AdapterGuard` introduces **no second authority**:

```text
AdapterGuard admits a transport. It never approves an answer.
```

Admission grants no rank, closes no graph, licenses no output, and
writes no trace. The straight line `GuardAdmitted → ApprovedAnswer`
is forbidden in exactly the sense of
[`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md):
after admission, every emitted answer still walks the full
`Γ → TransitionGate → AnswerAudit` pipeline, and only the gate can
grant a rank (docs/08), only `AnswerAudit` can append to the
ledger (docs/07), and only `emit_successor` licensed by an
`APPROVED` verdict can produce a successor graph (docs/17 §1,
source 3).

## 6. Forbidden adapter forms

The following are constitutional refusals at the boundary level.
None of them may be added by any PR, including future PRs, without
an Amendment PR that opens them under a named gate.

```text
forbidden: adapter emits a verdict (ClosureState or
           TransitionState from transport code).
forbidden: adapter bypasses AnswerAudit — any code path that
           surfaces the raw answer string as a system output.
forbidden: adapter writes the TraceLedger (docs/07 — only the
           AnswerAudit shell owns ledger writes).
forbidden: adapter emits a successor SlotGraph (docs/17 §1 —
           only an APPROVED TransitionVerdict licenses one).
forbidden: adapter decides APPROVED, or carries any field that
           implies an approval state.
forbidden: adapter attaches a rank to its answer (docs/08 — rank
           moves only through the gate's bounded meet).
forbidden: adapter reports model confidence, logits, or internal
           state as evidence (docs/01 rule 4; the registered line
           Tool/Number/LCNV → Knowledge).
forbidden: adapter constructs a SlotGraph from the answer text
           (docs/17 §4 — no graph from raw value).
forbidden: adapter widens the ModelClient protocol (streaming,
           sampling controls, tool calls) — protocol changes are
           their own chain step.
forbidden: a second concrete adapter inside PR-8 — each further
           adapter is its own chain step behind this law.
```

## 7. Guard purity and totality

The guard is bound by the same discipline as `Γ` and the
construction surface (docs/11 §7, docs/17 §5):

```text
purity:        admission is structural. The guard never calls
               complete(), never probes the transport, performs
               no I/O, no logging, no time reads. A guard that
               "test-fires" the adapter has crossed the boundary
               it exists to hold.
totality:      every candidate either is admitted or refused with
               a named FailureCode from §3. No bare exception for
               an expected refusal; no silent None.
no synthesis:  the guard never fabricates a missing declaration.
no promotion:  admission carries no rank and raises none.
```

> **PR-8.1 binding (structural reading).** "Structural" includes
> the *lookup itself*: while judging, every judged name — the five
> §3 surface registries and the declared `transport_surface` — is
> resolved **statically** (`inspect.getattr_static` over the
> instance and MRO `__dict__` mappings). The guard never executes
> adapter-authored `__getattribute__`, `__getattr__`, or a
> descriptor's `__get__`; machinery that would run, lie, or
> detonate during judging stays cold. Two corollaries: a transport
> *computed* on access is not a declaration (§2) and counts as
> undeclared; and a name synthesised only by dynamic lookup hooks
> is not a structural surface. A descriptor *object* sitting in a
> `__dict__` under a judged name is still seen — and still refused
> by its §3 row — without being invoked.

## 8. Anti-collapse rules

```text
no-judge:          an adapter never produces, carries, or implies
                   a verdict.
no-bypass:         no code path returns adapter text to a caller
                   except through AnswerAudit.
no-ledger:         only AnswerAudit appends to a TraceLedger.
no-successor:      only emit_successor licensed by APPROVED
                   produces successor graphs.
no-promotion:      no adapter rank; rank moves only via the
                   gate's bounded meet.
no-confidence:     model confidence never enters evidence or
                   rank.
no-second-door:    AuditedAnswer is the only output surface of
                   the assembled stack.
no-extension:      the ModelClient protocol is not widened.
no-second-adapter: PR-8 ships exactly one adapter.
named-refusal:     every guard refusal returns a named
                   FailureCode and never a bare exception or a
                   silent None.
```

## 9. Reserved names

`ConcreteAdapterCandidate` and `AdapterGuard` are reserved names
under the reserved-name rule in `CLAUDE.md`. They land in PR-8
**only**, with the full §2 declaration surface and the full §3
refusal table. Binding either name to a free container, or
shipping either name before PR-8, is a `FORBIDDEN_LEAP` regardless
of CI status.

## 10. Short constitutional summary

```text
المحوِّل ناقلٌ لا حاكم.
لا محوِّل خارج بروتوكول ModelClient.
لا جواب يصل إلا عبر AnswerAudit.
لا حكم من المحوِّل، ولا كتابة أثر، ولا خَلَف، ولا رتبة.
لا ثقة النموذج دليلًا.
لا شبكة ولا حفظ خارج ما يرخّصه هذا القانون.
```

In English:

```text
The adapter is a carrier, not a judge.
No adapter outside the ModelClient protocol.
No answer arrives except through AnswerAudit.
No verdict, no ledger write, no successor, no rank from the adapter.
No model confidence as evidence.
No network or persistence beyond what this law licenses.
```

---

## Cross-references

- The black-box boundary the adapter must not cross:
  [`01_BLACK_BOX_BOUNDARY.md`](01_BLACK_BOX_BOUNDARY.md).
- The forbidden straight-line surface (`Tool/Number/LCNV →
  Knowledge`, `Evidence → Certainty`, `Candidate → Certificate`):
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md).
- The ledger-ownership law the adapter must not violate:
  [`07_TRACE_LEDGER.md`](07_TRACE_LEDGER.md) — only the
  `AnswerAudit` shell appends; the trace schema stays as ratified
  (PR-6.1 binding — this law expands no trace surface).
- The only rank authority:
  [`08_TRANSITION_GATE.md`](08_TRANSITION_GATE.md).
- The identity link an unnamed adapter breaks:
  [`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md)
  §2, link 2 (Identity).
- The generation law that forbids a graph from raw answer text:
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md)
  §1, §4.
- The chain position of this document and of the adapter it
  licenses: [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) —
  PR-7, PR-8, and the §2 Amendment record.

---

## PR-8 binding

PR-7 does not write the adapter. PR-8 writes it; this document
binds what PR-8 must do:

```text
1. Ship ConcreteAdapterCandidate and AdapterGuard with the full
   §2 declaration surface and the full §3 refusal table, using
   only existing FailureCode members.
2. Ship exactly one concrete adapter, behind the guard, with one
   declared TransportSurface and only the §4 licensed I/O.
3. Hand answers to AnswerAudit untouched; AuditedAnswer remains
   the only output surface.
4. Prove every §3 refusal branch with constitutional tests under
   docs/12 (named FailureCode per refusal), and prove the §6
   forbidden neighbours absent (no-bypass, no-ledger, no-verdict,
   no-successor, no-rank) with negative guards in the shape the
   suite already uses for the audit layer.
5. Add the docs/18 presence guard beside its constitutional
   tests, in the shape of the existing docs-presence guards.
```

A PR-8 attempt that does not honor this law is a `FORBIDDEN_LEAP`
regardless of CI status.
