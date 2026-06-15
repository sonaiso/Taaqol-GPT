# 51 — Maʿqūl Interlock Law

> **Status:** Constitutional law. Ratified in PV-A4.1.
> Constitutional origin: docs/47 (Post-Vertical Roadmap), docs/48
> (Manṭūq Boundary Law), docs/50 (Mafhūm Boundary Law).
> This document is a boundary law that defines the two reasoning
> closure layers required between Manṭūq and Hukm:
> Maʿqūl al-Manṭūq and Maʿqūl al-Mafhūm.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `MaqulMantuqClosureCandidate`, a `MaqulMafhumClosureCandidate`,
> or any `prove_maqul_*()` symbol before the corresponding code PR
> is merged is a `FORBIDDEN_LEAP` regardless of CI status.

---

## §1 Governing principle (الجملة المركزية)

```text
المنطوق يُغلق حدّ القول.
معقول المنطوق يُغلق فهم الداخل.
المفهوم يفتح فرع الخارج.
معقول المفهوم يُغلق فهم الفرع.
الحكم لا يدخل إلا بعد ذلك بجسر مستقل.
```

Translation:

```text
Manṭūq closes the boundary of speech.
Maʿqūl al-Manṭūq closes internal understanding of that boundary.
Mafhūm opens the branch outside the boundary.
Maʿqūl al-Mafhūm closes understanding of that branch.
Hukm enters only after that, through an independent bridge.
```

The constitutional position preserved by this law:

```text
لا مفهوم قبل معقول المنطوق.
ولا حكم من مفهوم قبل معقول المفهوم.
ولا معقول بلا أصل مغلق.
ولا معقول بلا مجال.
ولا معقول بلا رتبة محصورة.
ولا معقول بلا بقايا مرئية.
ولا خط مستقيم من منطوق إلى حكم.
ولا خط مستقيم من مفهوم إلى حكم.
```

Translation:

```text
No mafhūm before Maʿqūl al-Manṭūq.
No hukm from mafhūm before Maʿqūl al-Mafhūm.
No reasoning closure without a closed origin.
No reasoning closure without a domain.
No reasoning closure with rank above its ceiling.
No reasoning closure with hidden residuals.
No straight line from manṭūq to hukm.
No straight line from mafhūm to hukm.
```

---

## §2 Definitions

### Maʿqūl al-Manṭūq (معقول المنطوق)

```text
Maʿqūl al-Manṭūq is the closure of what is rationally understood
from the Manṭūq within its own boundary — before any exit to
Mafhūm.

It answers:
  - What is the internal relation within the speech indication?
  - What is the constraint (qayd)?
  - What is the cause (sabab)?
  - What is the condition (shart)?
  - What is the impediment (māniʿ)?
  - What is the general (ʿāmm)?
  - What is the specific (khāṣṣ)?
  - What is the absolute (muṭlaq)?
  - What is the restricted (muqayyad)?
  - Does the expression admit more than one construal?
  - Are there residuals that block understanding?
  - Are all terms within their declared domain?
```

Maʿqūl al-Manṭūq is **not** Manṭūq itself. Manṭūq closes the
boundary; Maʿqūl al-Manṭūq closes the rational understanding of
what falls within that boundary.

### Maʿqūl al-Mafhūm (معقول المفهوم)

```text
Maʿqūl al-Mafhūm is the closure of what is rationally understood
from the Mafhūm branch — after establishing that the branch is
licensed from a reasoned Manṭūq.

It answers:
  - Is the branch rationally sound?
  - Is the relation to the origin correct?
  - Is it muwāfaqah (agreement) or mukhālafah (divergence)?
  - Is the relevant attribute (waṣf muʾaththir) preserved?
  - Is the disqualifying difference (fāriq qādiḥ) absent?
  - Has the domain remained constant?
  - Are there blocking residuals?
  - Does the rank not exceed the evidence?
```

Maʿqūl al-Mafhūm is **not** Mafhūm itself. Mafhūm opens the
branch outside the boundary; Maʿqūl al-Mafhūm closes rational
understanding of that branch.

---

## §3 Constitutional middle terms

The chain with Maʿqūl layers inserted:

```text
MantuqClosureVerdict        (PV-A2: preserved speech-origin closure)
    ↓
MaqulMantuqClosureCandidate (PV-A4.2: internal rational understanding
                             of the manṭūq before any outside branch)
    ↓
MafhumClosureCandidate      (PV-A4: admission/branch-opening candidate)
    ↓
MaqulMafhumClosureCandidate (PV-A6: rational understanding of the
                             branch before any hukm bridge)
    ↓
HukmCandidate               (future: only after Maʿqūl al-Mafhūm or
                             directly after Maʿqūl al-Manṭūq when no
                             mafhūm branch is opened)
```

Two paths to Hukm are licensed:

```text
Path A (direct from reasoned Manṭūq):
  MantuqClosureVerdict → MaqulMantuqClosure → Hukm Bridge

Path B (through Mafhūm):
  MantuqClosureVerdict → MaqulMantuqClosure → MafhumClosure
  → MaqulMafhumClosure → Hukm Bridge
```

No third path exists. No direct route from Mafhūm to Hukm without
Maʿqūl al-Mafhūm. No direct route from Manṭūq to Hukm without
Maʿqūl al-Manṭūq.

---

## §4 Effect on PV-A4 (MafhumClosure)

PV-A4 is **not invalidated** by this law. Its constitutional reading
is narrowed:

```text
PV-A4 MafhumClosureCandidate = Mafhūm admission closure.
It proves that a mafhūm branch was opened legally.
It does NOT prove that the branch is rationally understood.
It does NOT prove readiness for hukm.
```

The function `prove_mafhum_closure()` currently consumes
`MantuqClosureVerdict` directly. After PV-A4.2 (Maʿqūl al-Manṭūq
runtime), PV-A4.3 will harden `prove_mafhum_closure()` so it
consumes `MaqulMantuqClosureVerdict` instead of raw
`MantuqClosureVerdict`.

Until PV-A4.3 merges, the existing consumption of
`MantuqClosureVerdict` is a **tolerated residual** — not a
violation:

```text
Residual: MAFHUM_CONSUMES_RAW_MANTUQ_BEFORE_MAQUL
Status:   non-blocking until PV-A4.3
Fix:      PV-A4.3 changes the input type
```

---

## §5 What this law opens

```text
PV-A4.2 — Maʿqūl al-Manṭūq Closure (code).
           Carriers: MaqulMantuqClosureCandidate, MaqulMantuqClosureVerdict,
                     MaqulMantuqClosureState, prove_maqul_mantuq_closure().
           Nothing else.

PV-A4.3 — Harden MafhumClosure (corrective).
           Changes prove_mafhum_closure() to consume
           MaqulMantuqClosureVerdict instead of MantuqClosureVerdict.
           No new layer.

PV-A5  — Maʿqūl al-Mafhūm Boundary Law (law only).
           Defines admission conditions for Maʿqūl al-Mafhūm.

PV-A6  — Maʿqūl al-Mafhūm Closure (code).
           Carriers: MaqulMafhumClosureCandidate, MaqulMafhumClosureVerdict,
                     MaqulMafhumClosureState, prove_maqul_mafhum_closure().
           Nothing else.

Future — Mafhūm → Hukm Bridge Law (law only).
           Not licensed until PV-A6 is done.
```

---

## §6 Admission conditions for Maʿqūl al-Manṭūq

A Maʿqūl al-Manṭūq closure may be attempted **only if** all five
conditions hold:

### Condition 1 — Closed Manṭūq required

```text
MAQUL_MANTUQ_REQUIRES_CLOSED_MANTUQ

No MaqulMantuqClosureCandidate may be constructed without a PROVEN
MantuqClosureVerdict. The manṭūq boundary must be fully closed.
```

### Condition 2 — Domain declared

```text
MANTUQ_REASON_DOMAIN_MISSING

Every term used in the reasoning must have its domain declared per
docs/49. A Maʿqūl al-Manṭūq that uses undeclared-domain terms is
refused.
```

### Condition 3 — Internal relation closed

```text
MANTUQ_REASON_RELATION_UNCLOSED

The internal logical relations (constraint, cause, condition,
impediment, general/specific, absolute/restricted) must be declared.
An undeclared internal relation is a residual, not a gap.
```

### Condition 4 — No hidden residuals

```text
MAQUL_MANTUQ_HIDDEN_RESIDUAL

All residuals must be visible. Hidden residuals in the reasoning
of manṭūq are a constitutional violation.
```

### Condition 5 — Rank ceiling

```text
MAQUL_MANTUQ_RANK_EXCEEDS_CEILING

MAQUL_MANTUQ_RANK_CEILING = Rank.CANDIDATE

No MaqulMantuqClosureCandidate may exceed CANDIDATE rank.
```

---

## §7 Admission conditions for Maʿqūl al-Mafhūm

A Maʿqūl al-Mafhūm closure may be attempted **only if** all six
conditions hold:

### Condition 1 — Proven MafhumClosureCandidate required

```text
MAQUL_MAFHUM_REQUIRES_PROVEN_MAFHUM

No MaqulMafhumClosureCandidate may be constructed without a PROVEN
MafhumClosureVerdict. The mafhūm branch must be legally opened.
```

### Condition 2 — Maʿqūl al-Manṭūq required

```text
MAQUL_MAFHUM_REQUIRES_MAQUL_MANTUQ

The reasoning layer for the origin manṭūq must already be closed.
No Maʿqūl al-Mafhūm before Maʿqūl al-Manṭūq.
```

### Condition 3 — Origin preserved

```text
MAFHUM_ORIGIN_NOT_PRESERVED

The branch must still trace to the same preserved origin that the
MantuqClosureCandidate established. Detachment from origin is a
constitutional violation.
```

### Condition 4 — Branch reasoning sound

```text
MAFHUM_BRANCH_REASON_LEAP

The branch must be shown to be rationally sound:
  - relevant attribute preserved (waṣf muʾaththir)
  - disqualifying difference absent (fāriq qādiḥ)
  - domain unchanged
A branch that leaps over any of these is refused.
```

### Condition 5 — No hidden residuals

```text
MAQUL_MAFHUM_HIDDEN_RESIDUAL

All residuals must be visible. Hidden residuals in the reasoning
of the mafhūm branch are a constitutional violation.
```

### Condition 6 — Rank ceiling

```text
MAQUL_MAFHUM_RANK_EXCEEDS_CEILING

MAQUL_MAFHUM_RANK_CEILING = Rank.CANDIDATE

No MaqulMafhumClosureCandidate may exceed CANDIDATE rank.
```

---

## §8 Forbidden outputs

This law does **not** produce:

```text
HukmCandidate
TanzilCandidate
Certificate
RealityClaim
MajazVerdict
NaqlVerdict
MaqulMantuqClosureCandidate  (runtime — deferred to PV-A4.2)
MaqulMafhumClosureCandidate  (runtime — deferred to PV-A6)
```

---

## §9 Reserved failure codes (documentation only)

The following failure codes are reserved for runtime implementation
when the Maʿqūl layers become operational:

```text
MAQUL_MANTUQ_REQUIRED_BEFORE_MAFHUM    — Maʿqūl al-Manṭūq not closed
                                          before MafhumClosure attempted.

MANTUQ_NOT_REASONED                    — MantuqClosureVerdict exists but
                                          Maʿqūl al-Manṭūq was not proven.

MANTUQ_REASON_DOMAIN_MISSING           — term domain undeclared in
                                          Maʿqūl al-Manṭūq reasoning.

MANTUQ_REASON_RELATION_UNCLOSED        — internal logical relation not
                                          declared in Maʿqūl al-Manṭūq.

MAFHUM_MAQUL_REQUIRED_BEFORE_HUKM     — attempt to bridge Mafhūm to
                                          Hukm without Maʿqūl al-Mafhūm.

MAFHUM_REASON_NOT_CLOSED               — MafhumClosureVerdict exists but
                                          Maʿqūl al-Mafhūm was not proven.

MAFHUM_ORIGIN_NOT_PRESERVED            — branch detached from origin
                                          during Maʿqūl al-Mafhūm.

MAFHUM_BRANCH_REASON_LEAP              — branch reasoning skipped a
                                          required step.

MAFHUM_TO_HUKM_BEFORE_MAQUL           — direct Mafhūm → Hukm attempted
                                          without Maʿqūl al-Mafhūm.

MAQUL_DOMAIN_LEAP                      — domain changed between reasoning
                                          layers without a licensed bridge.
```

These codes do not exist in the runtime today. They are reserved
names that PV-A4.2 and PV-A6 must use. No PR may introduce a
different name for the same refusal.

---

## §10 Relation to existing laws

### docs/48 (Manṭūq Boundary Law)

docs/48 defines ManṭūqClosure as the preserved speech-origin
boundary. This law adds that ManṭūqClosure alone is insufficient
for mafhūm; Maʿqūl al-Manṭūq must close the rational understanding
of that boundary first.

### docs/50 (Mafhūm Boundary Law)

docs/50 defines MafhumClosure as a branch-opening from closed
Manṭūq. This law adds that:
- Mafhūm admission requires Maʿqūl al-Manṭūq (not raw Manṭūq alone)
- Mafhūm → Hukm requires Maʿqūl al-Mafhūm (not raw Mafhūm alone)

### docs/49 (Meta-Language Boundary Covenant)

All domain-declaration requirements from docs/49 apply within both
Maʿqūl layers. Domain violations in reasoning are admission failures.

### docs/11 (Mathematical Slot Geometry Laws)

Both Maʿqūl layers are constitutional mathematical objects with:
- a center (the reasoning proposition)
- a boundary (the origin closure it reasons about)
- a rank (bounded at CANDIDATE)
- residuals (visible, never hidden)
- a trace (auditable)

---

## §11 Illustrative example (non-normative)

For the speech: "لا تقل لهما أفّ" (Do not say 'uff' to them)

```text
Manṭūq:
  The prohibition of saying 'uff' within the speech boundary.
  → MantuqClosureVerdict (PROVEN)

Maʿqūl al-Manṭūq:
  'Uff' is the lowest verbal form of annoyance/displeasure in the
  context (maqām) of parents. The prohibition covers this minimum.
  Internal relations: cause (ṣighat nahiy), scope (parents),
  degree (minimum verbal harm).
  → MaqulMantuqClosureCandidate (PROVEN)

Mafhūm (muwāfaqah — a fortiori):
  Branch outside: what is stronger than 'uff' (e.g. striking).
  Licensed because: branch-relation declared, origin preserved,
  constraint identified, domain constant.
  → MafhumClosureCandidate (PROVEN as admission)

Maʿqūl al-Mafhūm:
  The branch is rationally sound:
  - relevant attribute (verbal harm) is preserved and exceeded
  - disqualifying difference absent
  - domain unchanged (filial obligation context)
  → MaqulMafhumClosureCandidate (PROVEN)

Only then:
  Material licensed for a Hukm bridge (separate operation).
```

This example is non-normative. It illustrates the ordering but does
not constitute runtime enforcement.

---

## §12 Chain position after this law

```text
PV-A4.1  Maʿqūl Interlock Law (this document — law only)        ← current
PV-A4.2  Maʿqūl al-Manṭūq Closure runtime
PV-A4.3  Harden MafhumClosure (consumes MaqulMantuqClosureVerdict)
PV-A5    Maʿqūl al-Mafhūm Boundary Law (law only)
PV-A6    Maʿqūl al-Mafhūm Closure runtime
Future   Mafhūm → Hukm Bridge Law (law only)
```

No step may be skipped. No step may be bundled with another.
