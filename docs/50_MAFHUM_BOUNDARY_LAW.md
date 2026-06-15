# 50 — Mafhūm Boundary Law

> **Status:** Constitutional law. Ratified in PV-A3.
> Constitutional origin: docs/47 (Post-Vertical Roadmap), docs/48
> (Manṭūq Boundary Law), docs/49 (Meta-Language Boundary Covenant).
> This document is a boundary law that defines when — and only when —
> a Mafhūm branch may be opened from a closed Manṭūq origin.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `MafhumClosureCandidate`, a `MafhumVerdict`, a `MafhumState`, or a
> `prove_mafhum_closure()` symbol before PV-A4 (the code PR) is
> merged is a `FORBIDDEN_LEAP` regardless of CI status.

---

## §1 Governing principle (الجملة المركزية)

```text
المفهوم ليس معنى جديدًا حرًا،
بل فرع مرخّص خارج حدّ منطوق مغلق،
يحفظ أصله، ويصرّح بمجاله، ويعلن علاقة الفرعية،
ولا ينتج حكمًا ولا تنزيلًا.
```

Translation:

```text
Mafhūm is not a free new meaning.
It is a licensed branch outside the boundary of a closed Manṭūq,
preserving its origin, declaring its domain, announcing the branch
relation, and producing neither hukm nor tanzīl.
```

The constitutional position preserved by this law:

```text
لا مفهوم بلا منطوق مغلق.
ولا خارج بلا داخل محدد.
ولا فرع بلا أصل محفوظ.
ولا فرع بلا علاقة فرعية معلنة.
ولا مصطلح بلا مجال.
ولا حكم من مفهوم في هذا القانون.
ولا تنزيل من مفهوم في هذا القانون.
```

Translation:

```text
No mafhūm without a closed manṭūq.
No outside without a defined inside.
No branch without a preserved origin.
No branch without a declared branch-relation.
No term without a domain.
No hukm from mafhūm in this law.
No tanzīl from mafhūm in this law.
```

---

## §2 Constitutional middle terms

The middle terms that connect Mafhūm to its predecessors and
successors:

```text
MantuqClosureCandidate   (what PV-A2 produced: the preserved explicit
                          indication with state CLOSED; the origin that
                          Mafhūm branches from)
MetaLanguageBoundaryCovenant (docs/49: domain-level disambiguation that
                          must be satisfied before any branch opens)
MafhumBoundaryLaw        (what this law defines: the admission conditions
                          under which a Mafhūm branch may open)
MafhumClosureCandidate   (what this law forbids until PV-A4: the runtime
                          carrier that represents a mafhūm closure candidate)
```

---

## §3 What this law opens

```text
PV-A4 — MafhumClosure (code).
         Carriers: MafhumClosureCandidate, MafhumVerdict, MafhumState,
                   MAFHUM_RANK_CEILING, prove_mafhum_closure().
         Nothing else.
```

PV-A4 is the **only** PR licensed by docs/50. It produces a
`MafhumClosureCandidate` carrying a verdict. This law does not
license any other runtime PR, any adapter change, any audit
expansion, any majāz/naql/haqīqah branch, any GPT proposer, or
any energy law.

---

## §4 Admission conditions (eight laws)

A Mafhūm branch may open **only if** all eight conditions hold:

### Law 1 — No Mafhūm before closed Manṭūq

```text
NO_MAFHUM_BEFORE_MANTUQ_CLOSURE

A MafhumClosureCandidate may not be constructed until a
MantuqClosureCandidate with state CLOSED exists for the same
speech origin. The Manṭūq must be fully closed — not pending,
not deferred, not partial.
```

### Law 2 — No outside branch before inside boundary is closed

```text
NO_MAFHUM_WITHOUT_OUTSIDE_BOUNDARY

Mafhūm is by definition the "outside" (ما هو خارج حدّ اللفظ).
The "inside" boundary (the Manṭūq preserved indication) must
be fully delimited before any outside branch is opened.
If the inside boundary is ambiguous, the outside is undefined.
```

### Law 3 — No Mafhūm without declared source domain

```text
NO_MAFHUM_WITHOUT_SOURCE_DOMAIN

Every term used in a MafhumClosureCandidate must have its domain
declared per docs/49 §4. A mafhūm that references terms at
undeclared domain levels is refused with META_TERM_DOMAIN_MISSING
(inherited from PV-M0).
```

### Law 4 — No Mafhūm without branch relation to preserved origin

```text
NO_MAFHUM_WITHOUT_BRANCH_RELATION

Every MafhumClosureCandidate must carry an explicit link back to the
MantuqClosureCandidate it branches from. The relation must declare:
  - the Manṭūq origin (preserved speech indication)
  - the branch type (mafhūm muwāfaqah / mafhūm mukhālafah)
  - the constraint that licenses the branch (the qayd that
    separates inside from outside)
A mafhūm without this link is a free meaning — forbidden.
```

### Law 5 — No unlicensed cross-domain transfer

```text
NO_MAFHUM_CROSS_DOMAIN_LEAP

No transfer from ṣarf to naḥw, naḥw to dalālah, or dalālah to
reality without a licensed bridge. The PV-M0 failure codes apply
as admission preconditions:
  - SARF_TO_NAHW_ROLE_LEAP
  - NAHW_TO_REALITY_ROLE_LEAP
  - META_TERM_DOMAIN_LEAP
  - META_TERM_UNLICENSED_TRANSFER

A MafhumClosureCandidate that uses a morphological term to imply a
syntactic role, or a syntactic term to imply reality, is refused
regardless of the correctness of the mafhūm itself.
```

### Law 6 — No Mafhūm with blocking Manṭūq constraint

```text
MANTUQ_BLOCKS_MAFHUM

If the Manṭūq carries a constraint that explicitly blocks the
proposed outside branch — e.g. a limitation (تقييد), an exception
(استثناء), or a condition (شرط) that covers the case the mafhūm
would assert — the mafhūm is refused.

The Manṭūq constraint takes precedence over the mafhūm branch.
```

### Law 7 — No Mafhūm with hidden residuals

```text
MAFHUM_HIDDEN_RESIDUAL

A MafhumClosureCandidate may not be approved if it carries residuals
that are not visible. All residuals must be declared:
  - deferred mafhūm types (e.g. mafhūm al-muwāfaqah defers
    mafhūm al-mukhālafah)
  - unresolved constraints from the Manṭūq
  - domain-level ambiguities (even if the term is declared,
    additional domain senses may remain)
Hidden residuals are a constitutional violation.
```

### Law 8 — No Hukm or Tanzīl from Mafhūm in this law

```text
MAFHUM_HUKM_LEAP
MAFHUM_TANZIL_LEAP

This law does not produce a hukm. A MafhumClosureCandidate remains a
candidate forever (like every other candidate in this system).
It does not generate reality, does not constitute authority,
does not license application (tanzīl), and does not assert
what is true in the world.

Any attempt to derive hukm or tanzīl directly from a
MafhumClosureCandidate without passing through the proper vertical
gates (HukmCandidate → ManāṭCandidate → TanzilCandidate)
is a FORBIDDEN_LEAP.
```

---

## §5 PV-M0 failure codes as admission preconditions

The following failure codes from docs/49 (Meta-Language Boundary
Covenant) apply as admission preconditions for any Mafhūm branch:

```text
META_TERM_DOMAIN_MISSING         — a meta-language term was used
                                   without declaring its domain level.
                                   Blocks mafhūm admission.

META_TERM_DOMAIN_LEAP            — a term was treated at a domain
                                   level higher than its declaration.
                                   Blocks mafhūm admission.

META_TERM_UNLICENSED_TRANSFER    — a term was transferred from one
                                   science to another without a licensed
                                   bridge. Blocks mafhūm admission.

SARF_TO_NAHW_ROLE_LEAP           — a morphological pattern was used
                                   to imply a syntactic role without
                                   a composition/contract gate.
                                   Blocks mafhūm admission.

NAHW_TO_REALITY_ROLE_LEAP        — a syntactic role was used to imply
                                   a real-world participant without
                                   hukm + tanzīl.
                                   Blocks mafhūm admission.
```

---

## §6 Reserved failure codes (documentation only)

The following failure codes are reserved for runtime implementation
when Mafhūm enforcement becomes operational (PV-A4):

```text
NO_MAFHUM_BEFORE_MANTUQ_CLOSURE  — MantuqClosureCandidate not CLOSED.

NO_MAFHUM_WITHOUT_OUTSIDE_BOUNDARY — inside boundary not delimited.

NO_MAFHUM_WITHOUT_SOURCE_DOMAIN  — term domain undeclared (refs docs/49).

NO_MAFHUM_WITHOUT_BRANCH_RELATION — no explicit link to origin manṭūq.

NO_MAFHUM_CROSS_DOMAIN_LEAP     — unlicensed domain transfer detected.

MANTUQ_BLOCKS_MAFHUM             — manṭūq constraint blocks the branch.

MAFHUM_HIDDEN_RESIDUAL           — undeclared residuals present.

MAFHUM_HUKM_LEAP                 — attempt to derive hukm from mafhūm
                                   without proper vertical gates.

MAFHUM_TANZIL_LEAP               — attempt to derive tanzīl from mafhūm
                                   without proper vertical gates.
```

These codes do not exist in the runtime today. They are reserved
names that PV-A4 (if/when Mafhūm enforcement becomes operational)
must use. No PR may introduce a different name for the same refusal.

---

## §7 What this law forbids (forbidden surface)

```text
This law does NOT:
- create MafhumClosureCandidate, MafhumVerdict, MafhumState, or any runtime carrier
- implement prove_mafhum_closure() or any runtime operation
- add FailureCode enum values to src/
- license Majāz, Naql, Haqīqah, GPT proposer, or energy law
- produce hukm, tanzīl, or reality
- license any adapter or audit change
- modify src/ or tests/
- add any runtime dependency
```

---

## §8 Relationship to existing laws

| Existing law | Relationship |
|---|---|
| docs/04 (Forbidden Straight Lines) | Mafhūm may not produce a straight line from evidence to certainty. The branch is a candidate, never a certificate. |
| docs/05 (Transition Discipline) | Opening a mafhūm branch is a transition that requires a gate. |
| docs/11 (Mathematical Slot Geometry Laws) | Mafhūm obeys: no output without trace, no closure without gamma, no hidden residuals. |
| docs/46 (Vertical Path Closure) | Mafhūm is a horizontal branch off the closed vertical path. It does not re-open the vertical. |
| docs/47 (Post-Vertical Roadmap) | PV-A3 is the law step for the Manṭūq → Mafhūm branch family (Family A). |
| docs/48 (Manṭūq Boundary Law) | Mafhūm consumes MantuqClosureCandidate.CLOSED. No mafhūm before manṭūq closure. |
| docs/49 (Meta-Language Boundary Covenant) | All terms used in Mafhūm must have declared domains. PV-M0 failure codes are admission preconditions. |

---

## §9 Mafhūm types (inventoried, not implemented)

The following mafhūm types are inventoried for future reference but
are NOT implemented, closed, or licensed by this law:

```text
مفهوم الموافقة (mafhūm al-muwāfaqah):
    The implied meaning that agrees with the manṭūq in its ruling
    direction. Also called "فحوى الخطاب" (fahwā al-khiṭāb) or
    "لحن الخطاب" (laḥn al-khiṭāb).
    Example: "لا تقل لهما أفّ" implies prohibition of greater harm.

مفهوم المخالفة (mafhūm al-mukhālafah):
    The implied meaning that opposes the manṭūq when its constraining
    attribute is absent. Subtypes:
      - مفهوم الصفة (mafhūm al-ṣifah) — qualifier absence
      - مفهوم الشرط (mafhūm al-sharṭ) — condition absence
      - مفهوم الغاية (mafhūm al-ghāyah) — endpoint crossed
      - مفهوم العدد (mafhūm al-ʿadad) — number exceeded
      - مفهوم اللقب (mafhūm al-laqab) — title replacement
```

Each of these types requires its own admission test under §4
when PV-A4 runtime is built. This law does not determine which
types are valid — only that all must satisfy the eight admission
conditions.

---

## §10 Rank ceiling

```text
MAFHUM_RANK_CEILING = CANDIDATE

A MafhumClosureCandidate can never exceed rank CANDIDATE.
It never reaches PROVEN, CLOSED, or CERTIFIED by itself.
It remains a candidate that may be consumed by a future
HukmCandidate only through the vertical gates
(Hukm → Manāṭ → Tanzīl).
```

---

## §11 Deferred residuals

The following are explicitly deferred by this law:

```text
DEFERRED: MafhumClosureCandidate runtime implementation (PV-A4)
DEFERRED: Mafhūm al-Muwāfaqah specific admission tests
DEFERRED: Mafhūm al-Mukhālafah specific admission tests
DEFERRED: Mafhūm → Hukm bridge (requires its own law)
DEFERRED: Mafhūm → Majāz interaction (requires PV-B branch)
DEFERRED: Mafhūm → Naql interaction (requires PV-C branch)
DEFERRED: General Energy Conservation Law (PV-E0)
DEFERRED: Conditions DAG (interacts with mafhūm al-sharṭ)
```

---

## §12 Constitutional chain verification

For PV-A3 to be constitutionally valid, the following must hold:

```text
✓ PV-A2   ManṭūqClosure code merged (provides MantuqClosureCandidate)
✓ PV-A2.2 Upstream Mufrad-Dalālah continuity enforced
✓ PV-A2.3 Upstream continuity tests hardened
✓ PV-M0   Meta-Language Boundary Covenant ratified (docs/49)
⬤ PV-A3   This law (docs/50)
  PV-A4   MafhumClosure code (next — only after this law)
```

---

## §13 Binding rules for PV-A4 implementors

When PV-A4 is eventually implemented, it must satisfy:

```text
Rule 1: MafhumClosureCandidate must carry a reference to its source
         MantuqClosureCandidate (never constructed without one).

Rule 2: MafhumClosureCandidate must declare the branch type
         (muwāfaqah or mukhālafah) and the specific subtype
         if mukhālafah.

Rule 3: MafhumClosureCandidate must declare the qayd (constraint) that
         licenses the branch — the property whose presence/absence
         separates inside from outside.

Rule 4: prove_mafhum_closure() must check all eight admission
         conditions from §4 before producing a verdict.

Rule 5: prove_mafhum_closure() must refuse with a named FailureCode
         (from §6) for every violation. Never silently return None.

Rule 6: MafhumClosureCandidate.rank may never exceed MAFHUM_RANK_CEILING.

Rule 7: All residuals must be visible in the verdict.

Rule 8: No hukm, no tanzīl, no reality claim in the output.
```
