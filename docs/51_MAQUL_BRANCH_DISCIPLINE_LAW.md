# 51 — Maʿqūl Branch Discipline Law

> **Status:** Constitutional law. Ratified in PV-A4.1.
> Constitutional origin: docs/47 (Post-Vertical Roadmap), docs/48
> (Manṭūq Boundary Law), docs/50 (Mafhūm Boundary Law),
> docs/14 §1 (chain PR-15 through PR-D4).
> This document is a **clarification covenant** that names the existing
> dalālah chain as Maʿqūl al-Dalālah and establishes the discipline
> governing transitions from Manṭūq to Mafhūm to Hukm.
>
> This law does **not** introduce a new runtime layer, carrier, or
> operation. It recognises that Maʿqūl is the constitutional governing
> principle already embodied in the chain from DalOnlyCandidate through
> MufradDalālahClosure, RelationClosure, IfādahCandidate, and
> ManṭūqClosure. It is **not** a new ontological entity placed after
> Manṭūq or after Mafhūm.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change.

---

## §1 Governing principle (الجملة المركزية)

```text
المعقول ليس فرعًا بعد المنطوق، بل هو قانون انتظام الفروع
من الدال إلى الحقيقة والمجاز.

فإذا اكتمل الدال والمدلول والوضع واتحادها، تولدت الدلالة المفردة؛
ومنها المطابقة والتضمن والالتزام، ثم علاقات الكلي والجزئي
والمتواطئ والمتباين والمترادف والمشكك والمشترك والمنقول،
ثم الحقيقة اللغوية والعرفية، ثم المجاز عند تعذر الحقيقة.

وكل فرع لا يعمل إلا برخصته، وبقيد مجاله، وبقاياه، وأثره.
```

Translation:

```text
Maʿqūl is not a branch after Manṭūq; it is the law of orderly
succession of branches from the signifier to haqīqah and majāz.

When the signifier, signified, convention, and their union are complete,
singular dalālah is born; from it: muṭābaqah, taḍammun, and iltizām;
then: the relations of kullī/juzʾī, mutawāṭiʾ, mutabāyin, mutarādif,
mushakkik, mushtarak, and manqūl; then: linguistic and customary haqīqah;
then: majāz only upon licensed failure of haqīqah.

No branch operates except by its license, its domain constraint,
its residuals, and its trace.
```

---

## §2 What Maʿqūl al-Dalālah IS

Maʿqūl al-Dalālah is **not** a carrier or a runtime closure. It is
the constitutional name for the **ordering discipline** already
embodied in the existing chain:

```text
Stage 1 — Signifier alone:
    DalOnlyCandidate (PR-15)
    → preserves phonetic/graphic form, boundary, path, weight fit
    → never meaning

Stage 2 — Verbal signified alone:
    VerbalMadlulCandidate (PR-16)
    → opens licensed verbal signified candidacy
    → never final meaning, never ifādah

Stage 3 — Convention (wadʿ) and licensing:
    Lexical / Samāʿ / Qiyās License (PR-14)
    Registry Contract (PR-16C, PR-16C.1)
    → binds signifier to a declared usage domain
    → never reality, never external truth

Stage 4 — Signifier–signified union:
    Dal-Madlul Binding Candidate (PR-17)
    ContractableUnitGeometry (PR-18)
    → licensed union, not arbitrary pairing
    → never meaning as such

Stage 5 — Kullī / Juzʾī axis:
    Mufrad Semantic Slot Geometry (PR-D1)
    → determines universal/particular standing before dalālah relations
    → never dalālah itself

Stage 6 — Muṭābaqah / Taḍammun / Iltizām:
    Dalālah Relations Candidate (PR-D2)
    → correspondence, inclusion, concomitance as candidates
    → candidates only, never final meaning
    → Iltizām is شرط لا موجب (condition, not necessitator)

Stage 7 — Mufrad Dalālah Closure:
    MufradDalālahClosure (PR-D3)
    → closes singular dalālah as proven candidates

Stage 8 — Relation Closure:
    RelationClosure (PR-D4)
    → closes composition relations only after singular dalālah

Stage 9 — Ifādah (proposition closure):
    IfādahCandidate (PR-20)
    → proposition candidate; three parallel PROVEN verdicts;
      maqām is a verdict; never hukm, never meaning

Stage 10 — Maqām / Context Boundary:
    MaqāmContextBoundaryVerdict (PR-D1.2)
    → discourse domain, usage register, blocker audit
    → boundary only, never dalālah, never meaning

Stage 11 — Manṭūq Closure:
    MantuqClosureVerdict (PV-A2)
    → preserved speech-origin boundary
    → consumes IfadahVerdict + MaqamContextBoundaryVerdict
    → verifies relation_closure_ref continuity
    → deferred residuals for mafhūm / majāz / naql

Stage 12 — Mafhūm branch admission:
    MafhumClosureCandidate (PV-A4)
    → branch-opening candidate only
    → does not produce hukm, does not close understanding
    → deferred residuals for hukm / tanzīl / majāz / naql
```

This twelve-stage sequence **is** Maʿqūl al-Dalālah. Every stage
carries rank, residuals, trace, domain, and license. There is no
missing "understanding layer" — the understanding is distributed
across these stages.

---

## §3 What Maʿqūl al-Dalālah is NOT

```text
Maʿqūl is NOT:
  - A new runtime layer inserted between Manṭūq and Mafhūm.
  - A new carrier type (MaqulMantuqClosureCandidate).
  - A new closure operation (prove_maqul_mantuq_closure()).
  - An independent ontological entity with its own SlotGraph geometry.
  - A repetition of what MufradDalālahClosure + RelationClosure +
    IfādahCandidate + MantuqClosure already prove.

The prior version of this document (pre-correction) proposed
MaqulMantuqClosureCandidate and MaqulMafhumClosureCandidate as
independent runtime carriers. This is withdrawn. The existing chain
already embodies the rational ordering that "maʿqūl" names.
```

---

## §4 The discipline rules (what this law enforces)

### Rule 1 — No Mafhūm without the full dalālah sequence

```text
No MafhumClosureCandidate may be constructed unless the Manṭūq
from which it branches was itself built upon the complete dalālah
sequence (Stages 1–11 above).

The existing check in prove_mafhum_closure() — consuming
MantuqClosureVerdict which requires IfadahVerdict which requires
RelationClosure which requires MufradDalālahClosure — already
enforces this. No additional runtime carrier is needed.
```

### Rule 2 — No Hukm from Mafhūm without branch discipline

```text
No HukmCandidate may be built from a MafhumClosureVerdict unless:
  (a) The mafhūm branch proves its relation to the origin is sound.
  (b) The relevant attribute (waṣf muʾaththir) is preserved.
  (c) The disqualifying difference (fāriq qādiḥ) is proven absent.
  (d) The domain has not shifted.
  (e) Residuals are visible.

This is enforced by the admission conditions in MafhumClosure (PV-A4)
and by the existing Hukm bridge path (which requires further
licensing). No new "Maʿqūl al-Mafhūm" runtime layer is needed
beyond what the admission conditions and typed-field hardening
(future corrective PRs) will provide.
```

### Rule 3 — Iltizām is a condition, not a necessitator

```text
الالتزام شرط لا موجب.

IltizamCandidate (from PR-D2) opens a concomitance relation as a
candidate. It does NOT force a conclusion. Any operation that treats
iltizām output as proven conclusion without further gate passage is
a FORBIDDEN_LEAP.
```

### Rule 4 — Lexical-relation branches are licensed after binding

```text
Mutawāṭiʾ (univocal), Mutabāyin (equivocal), Mutarādif (synonymous),
Mushakkik (graduated), Mushtarak (homonymous), and Manqūl
(transferred) — these are licensed lexical-relation branches.

Each operates only after:
  - Dal-Madlul Binding (Stage 4) is proven.
  - Kullī/Juzʾī axis (Stage 5) is declared.

Each requires:
  - carrier, domain, evidence, difference test, residuals, rank, trace.
```

### Rule 5 — Haqīqah before Majāz

```text
لا مجاز قبل محاولة الحقيقة.
ولا حقيقة عرفية بلا عرف مثبت.
ولا حقيقة اصطلاحية بلا مجال اصطلاحي.
ولا نقل بلا ناقل ومجال وأثر.

No majāz opens without:
  1. Attempting linguistic haqīqah.
  2. Attempting customary/technical haqīqah if its domain exists.
  3. Licensed failure or impossibility (taʿadhdhur) of haqīqah
     in the given maqām.
  4. A declared ṣārifah (diverting indicator).
  5. A licensed majāz relation type.
  6. Visible residuals.
```

### Rule 6 — No straight line from any stage to Hukm

```text
No single stage output constitutes material for Hukm.
The minimum path to Hukm requires completion of the full chain
(Stages 1–12) plus the Hukm bridge (which remains its own
licensed step).

This restates the existing constitutional principle:
  No straight line from Evidence to Certainty.
  No straight line from Tool / Number / LCNV to Knowledge.
```

---

## §5 Effect on the existing codebase

### ManṭūqClosure is NOT raw

The current `MantuqClosure` code consumes:
- `IfadahVerdict` (which requires `RelationClosure` → `MufradDalālahClosure`)
- `MaqamContextBoundaryVerdict`
- Checks `relation_closure_ref` continuity (PV-A2.2)

This is **not** a "raw" manṭūq that lacks rational grounding. It is
a manṭūq built on the full dalālah sequence. The characterisation of
MantuqClosureVerdict as "raw" in the pre-correction version of this
document is withdrawn.

### MafhumClosure consuming MantuqClosureVerdict is constitutionally valid

`prove_mafhum_closure()` consuming `MantuqClosureVerdict` directly
is correct — because that verdict already proves the full dalālah
chain underneath. No intermediate `MaqulMantuqClosureVerdict` is
needed.

The residual `MAFHUM_CONSUMES_RAW_MANTUQ_BEFORE_MAQUL` declared in
the pre-correction version of this document is **discharged** — it
was based on a false premise.

### PV-A4 (MafhumClosure) is not invalidated

PV-A4 stands as correct admission/branch-opening. Its fields
(`source_domain`, `cross_domain_transfer`, `outside_boundary`, `qayd`,
`mantuq_blocks`) are accepted as boundary checks at the admission
level. They are not full typed enforcement — but that is a future
hardening matter, not a constitutional gap.

---

## §6 Deferred residuals (future hardening, not new layers)

The following are residuals requiring **typed-field hardening** in
future corrective PRs — not new runtime closure layers:

### Residual 1 — `source_domain: str`

Currently a bare string. Future hardening will introduce typed
domain carriers (`MetaTermDomain`, `DomainLevel`) when the
Haqīqah/Majāz branch opens. This is governed by docs/49.

### Residual 2 — `cross_domain_transfer: str`

Currently any non-empty string triggers refusal. Future hardening
will introduce `LicensedDomainBridge` to distinguish licensed
transfers (naql) from unlicensed leaps. Not all cross-domain
movement is forbidden — some is licensed naql.

### Residual 3 — `outside_boundary: str` and `qayd: str`

Currently untyped. Future hardening will type the constraint
taxonomy:

```text
ṣifah (attribute)
sharṭ (condition)
ghāyah (terminus)
ʿadad (number)
istithnāʾ (exception)
laqab (proper name)
waṣf muʾaththir (relevant attribute)
fāriq qādiḥ (disqualifying difference)
```

### Residual 4 — Lexical-relation branches

`Mutawāṭiʾ`, `Mutabāyin`, `Mutarādif`, `Mushakkik`, `Mushtarak`,
`Manqūl` — these are not yet implemented as typed carriers. They
are branches of Maʿqūl al-Dalālah that will open in future PRs
with their own laws (per the post-vertical roadmap, docs/47).

### Residual 5 — Haqīqah / Majāz path

The haqīqah lugawiyyah → haqīqah ʿurfiyyah → taʿadhdhur → majāz
path is not yet implemented. It is a future post-vertical branch
(Family A continuation or new family) per docs/47.

---

## §7 Withdrawn elements

The following elements from the pre-correction version of this
document are **withdrawn**:

```text
WITHDRAWN:
  - MaqulMantuqClosureCandidate as a new runtime carrier.
  - MaqulMafhumClosureCandidate as a new runtime carrier.
  - prove_maqul_mantuq_closure() as a new operation.
  - prove_maqul_mafhum_closure() as a new operation.
  - MaqulMantuqClosureState / MaqulMafhumClosureState as new enums.
  - PV-A4.2 (Maʿqūl al-Manṭūq Closure runtime) as a chain step.
  - PV-A4.3 (Harden MafhumClosure to consume MaqulMantuqClosureVerdict).
  - PV-A5 (Maʿqūl al-Mafhūm Boundary Law).
  - PV-A6 (Maʿqūl al-Mafhūm Closure runtime).
  - The residual MAFHUM_CONSUMES_RAW_MANTUQ_BEFORE_MAQUL.
  - All ten reserved failure codes from the pre-correction §9.

REASON:
  These were based on the misconception that Maʿqūl is a new
  runtime layer after Manṭūq. It is not. The existing chain
  already embodies the rational ordering. Adding carriers that
  duplicate MufradDalālahClosure + RelationClosure + Ifādah +
  MantuqClosure is architectural hallucination.
```

---

## §8 What this law opens (revised chain)

The chain after PV-A4.1 is now:

```text
PV-A4.1   Maʿqūl Branch Discipline Law (this document)           ← current
              Clarification covenant only. No new runtime.

FUTURE (post-vertical branches, per docs/47 admission rule):
  PV-B1    Haqīqah / Majāz Boundary Law (law only)
              Defines when haqīqah closes and when majāz opens.
              Requires its own admission rule per docs/47.

  PV-C1    Naql Boundary Law (law only)
              Defines licensed transfer (naql) conditions.

  PV-D1    Lexical Relation Branch Law (law only)
              Defines mutawāṭiʾ/mutabāyin/mutarādif/mushakkik/
              mushtarak formal carriers.

  (Exact numbering to be established by future amendments to docs/14)
```

No step requires a new "Maʿqūl al-Manṭūq runtime" or "Maʿqūl
al-Mafhūm runtime." The branches above extend the dalālah chain
directly, each governed by its own law per docs/47.

---

## §9 Preserved prohibitions

This law preserves the following constitutional prohibitions:

```text
1. No mafhūm without the full dalālah sequence closed in the manṭūq.
   (Enforced by: MantuqClosure consuming IfadahVerdict which
   requires RelationClosure which requires MufradDalālahClosure.)

2. No hukm from mafhūm without branch-discipline proof.
   (Enforced by: MafhumClosure admission conditions +
   future Hukm bridge law.)

3. No straight line from manṭūq to hukm.
   (Enforced by: the vertical chain PR-D5 through PR-D10.)

4. No straight line from mafhūm to hukm.
   (Enforced by: the admission conditions preventing
   MafhumClosureCandidate from producing HukmCandidate directly.)

5. No majāz before licensed failure of haqīqah.
   (To be enforced by: future PV-B1 Haqīqah/Majāz Boundary Law.)

6. No naql without a licensed bridge.
   (To be enforced by: future PV-C1 Naql Boundary Law.)

7. No iltizām output treated as proven conclusion.
   (Enforced by: IltizamCandidate remaining at Rank.CANDIDATE.)
```

---

## §10 Relation to existing laws

### docs/48 (Manṭūq Boundary Law)

ManṭūqClosure is the preserved speech-origin boundary built upon
the full dalālah sequence. This law confirms that ManṭūqClosure
is constitutionally complete as currently implemented — it is not
"raw" or "un-reasoned."

### docs/50 (Mafhūm Boundary Law)

MafhumClosure is a branch-opening from closed Manṭūq. Its
consumption of MantuqClosureVerdict (which embodies the full
dalālah chain) is constitutionally valid. No intermediate
"Maʿqūl al-Manṭūq" carrier is needed between them.

### docs/49 (Meta-Language Boundary Covenant)

All domain-declaration requirements from docs/49 continue to
apply at every stage of Maʿqūl al-Dalālah. This is not new — it
was already binding from PV-M0 onward.

### docs/11 (Mathematical Slot Geometry Laws)

Every stage in the Maʿqūl al-Dalālah sequence is already a
constitutional mathematical object with center, boundary, rank,
residuals, and trace. This law adds no new geometry.

### docs/14 (PR Chain Roadmap)

This law corrects the chain: PV-A4.2, PV-A4.3, PV-A5, PV-A6
are withdrawn. Future branches (Haqīqah/Majāz, Naql, Lexical
Relations) will follow docs/47 admission rules with their own
numbering.

---

## §11 Illustrative chain reading (non-normative)

For the speech: "لا تقل لهما أفّ" (Do not say 'uff' to them)

```text
The existing Maʿqūl al-Dalālah chain proves:

1. DalOnly: "أفّ" as signifier (sound-form, graphic trace).
2. VerbalMadlul: opens verbal signified candidacy for "أفّ."
3. License: wadʿ/usage license for "أفّ" in this registry.
4. Binding: signifier–signified union for "أفّ" → displeasure-sound.
5. Kulli/Juzʾi: "أفّ" is juzʾī (particular instance of displeasure).
6. Dalālah: muṭābaqah (what "أفّ" fully corresponds to).
7. MufradDalālah: closes singular dalālah of "أفّ."
8. Relation: "أفّ" in composition with "لا تقل" and "لهما."
9. Ifādah: "لا تقل لهما أفّ" = prohibition proposition.
10. Maqām: filial-obligation context established.
11. Manṭūq: preserved speech-origin = "prohibition of saying أفّ
    to parents" — built on all 10 preceding stages.

Then:
12. Mafhūm (muwāfaqah — a fortiori):
    Branch: "what is stronger than أفّ (e.g. striking)."
    Admission: branch-relation declared, origin preserved,
    constraint identified, domain constant.
    → MafhumClosureCandidate (PROVEN as admission).

The mafhūm does not need a separate "Maʿqūl al-Manṭūq" runtime
to license it — the MantuqClosureVerdict it consumes already
proves Stages 1–11.
```

This example is non-normative. It illustrates the ordering but does
not constitute runtime enforcement.

---

## §12 The corrective record

This document replaces the pre-correction "Maʿqūl Interlock Law"
which proposed Maʿqūl al-Manṭūq and Maʿqūl al-Mafhūm as
independent runtime closure layers. The correction recognises:

```text
1. Maʿqūl = the constitutional ordering discipline of dalālah branches.
2. The existing chain (PR-15 → PV-A4) already embodies this ordering.
3. No new carrier duplicating MufradDalālahClosure through
   MantuqClosure is needed.
4. MafhumClosure consuming MantuqClosureVerdict is constitutionally
   valid — not a tolerated residual.
5. Future branches (haqīqah, majāz, naql, lexical relations)
   extend the dalālah chain directly under docs/47 governance.
```

The governing correction:

> لا تعالج التفكك بمزيد من التفكيك.
> (Do not treat fragmentation with more fragmentation.)

---
