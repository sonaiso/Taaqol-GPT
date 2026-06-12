# 19 — Arabic Weight Boundary Law

> **Status:** Constitutional law. Ratified in PR-9; chain position
> ratified by Amendment-2 and re-staged by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). PR-9 is
> law only: no Arabic code, no carrier, no `src/` change, no
> `tests/` change ships with this document. The weight carriers
> land in PR-10 and the `weigh()` operation in PR-13, both bound by
> this document; no later PR may relax it.

This document closes, **before** any Arabic code exists, the
loophole the weight branch would otherwise open:

```text
An Arabic weight module can align a vocalized form with a
pattern (wazn), look like harmless morphology, and pass a
local test — while smuggling meaning, agency, hukm, or
reality claims across the alignment, as if the scale had
judged the world instead of imaging a form.
```

The remedy is to fix, before the first carrier is written, the one
space weight is licensed to land in, the identities it may never
collapse, and the refusals that bind every later weight-branch PR.

The governing statement:

```text
Weight does not mean — weight images.

Weight → PatternSpace, not Meaning.
WeightFit ≠ Knowledge.
Root ≠ Reality.
MorphologicalAgent ≠ RealAgent.
No lexicon, no semantics, no ontology, no hukm.
No Arabic weight code inside the adapter or audit layers.
```

---

## 1. The docs/09 door

[`09_ARABIC_APPLICATION_BOUNDARY.md`](09_ARABIC_APPLICATION_BOUNDARY.md)
holds that a first Arabic application may enter only through a
separate proposal that declares its gates, its un-shortcut
transitions, and its evidence sources. This law is that proposal,
and its declarations are:

```text
Gates implemented            : none. PR-9 is law only. The
                               pre-weight gates open in PR-11
                               and the chain operations in
                               PR-12, all under docs/20 and
                               behind TransitionGates.

Transitions not shortcut     : Root → LexicalMeaning,
                               Weight → Agency,
                               Pattern → SyntaxRole,
                               WordForm → Meaning,
                               LexiconEntry → Candidate,
                               Candidate → Certificate,
                               Evidence → Certainty,
                               Tool/Number/LCNV → Knowledge
                               (the §4 table maps every
                               weight-branch leap onto these
                               registered rows).

Evidence sources consulted   : none. The weight branch consults
                               no lexicon, no samāʿ corpus, and
                               no qiyās rule before the PR-14
                               licensing boundary; model
                               confidence is never evidence
                               (docs/01).
```

## 2. The imaging boundary

A weight (*wazn*) is a morphological scale. Constitutionally it
does exactly one thing:

```text
Form → Mīzān → image in PatternSpace
```

PatternSpace is the space of morphological patterns — the mawāzīn —
and it is an **image space, not a meaning space**:

```text
PatternSpace ∌ Meaning, Agency, Patienthood, Hukm, Reality,
               RealEvent, Knowledge.
```

Alignment yields a `WeightFitCandidate` (PR-13) — a depicted fit
between a form and a pattern — and never yields Meaning, Agency,
Hukm, or Reality. The fit is a picture of structure, not a claim
about the world.

The **input** side of the Mīzān — what may be weighed, and the
licensing chain that produces a weighable candidate — is owned by
the Pre-Weight Licensing Law (docs/20, PR-9A) and is deliberately
not stated here. This law fixes the **output** side: wherever
weighing lands, it lands in PatternSpace and nowhere else.

## 3. The discriminating identities

In the same sense as docs/15 §2, each carrier of the weight branch
is what it is, and is not its neighbour up the ladder:

```text
wazn       — a pattern image. Not a meaning, not a role,
             not a judgment.

WeightFit  — a depicted alignment between a form and a
             pattern. Not knowledge; not a certificate;
             not an approval.

root       — a derivational locus (docs/04: Root →
             LexicalMeaning). Not a reality, not a referent,
             not a truth claim about the world.

fāʿil      — a morphological agent pattern. Not a real agent,
             not Agency (docs/04: Weight → Agency).

mafʿūl     — a morphological patient pattern. Not Patienthood
             (docs/04: Pattern → SyntaxRole).

maṣdar     — a verbal-noun pattern. Not a RealEvent (docs/04:
             WordForm → Meaning).
```

These identities are non-confusion cases in exactly the sense of
[`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md):
*fāʿil* as a ṣarf term never travels into ontology or law as
"agent" without a licensed bridge.

## 4. The registered straight lines this law binds

Every leap the weight branch could be tempted to take is already a
registered forbidden straight line
([`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md),
bound as data in PR-5):

```text
| Weight-branch leap                  | Registered line (docs/04)    |
| wazn → meaning of the weighed form  | WordForm → Meaning           |
| root → lexical meaning / reality    | Root → LexicalMeaning        |
| fāʿil pattern → agency              | Weight → Agency              |
| mafʿūl pattern → patienthood        | Pattern → SyntaxRole         |
| maṣdar pattern → real event         | WordForm → Meaning           |
| weight fit → knowledge              | Tool/Number/LCNV → Knowledge |
| lexicon entry → candidate           | LexiconEntry → Candidate     |
| fit candidate → certificate         | Candidate → Certificate      |
| fit evidence → certainty            | Evidence → Certainty         |
```

This law adds **no new registry rows and no new FailureCode
members**. A weight-branch implementation that takes any of these
leaps directly is refused with the registered
`FORBIDDEN_STRAIGHT_LINE`; an implementation shipped out of chain
position is a `FORBIDDEN_LEAP`. Both codes exist since PR-1A.

## 5. Fit is not approval

The Mīzān introduces **no second authority**:

```text
weigh() aligns a form. It never approves an answer,
asserts a meaning, or judges the world.
```

A `WeightFitCandidate` grants no rank, closes no graph, licenses
no output, writes no trace, and carries no meaning field. After
fit, every move toward lexicon, samāʿ, or qiyās passes the PR-14
licensing boundary; semantics stays beyond the current chain
entirely; and the pipeline disciplines stay intact: only the gate
grants rank (docs/08), only `AnswerAudit` appends the ledger
(docs/07), and only an `APPROVED` verdict licenses a successor
graph (docs/17 §1).

## 6. Forbidden weight-branch forms

The following are constitutional refusals at the boundary level.
None of them may be added by any PR, including future PRs, without
an Amendment PR that opens them under a named gate.

```text
forbidden: any weight surface emits Meaning, Agency,
           Patienthood, RealEvent, Hukm, Reality, or
           Knowledge — from alignment or from fit.
forbidden: a meaning, agency, hukm, or reality field on any
           weight or pre-weight carrier (binds PR-10).
forbidden: weigh()/alignment shipped before PR-13, or weight
           carriers shipped before PR-10.
forbidden: docs/20 content shipped under this law — the
           pre-weight licensing chain belongs to PR-9A.
forbidden: lexicons, root tables, pattern tables, or any
           samāʿ/qiyās material before the PR-14 license.
forbidden: Arabic weight code inside the adapter or audit
           layers, or any kernel, gate, or schema change made
           for the weight branch.
forbidden: a weight verdict — fit is a candidate, never an
           APPROVED, never a ClosureState.
forbidden: rank promotion from fit — rank moves only via the
           gate's bounded meet (docs/08).
forbidden: new runtime dependencies for the weight branch.
```

## 7. Purity and totality

Future weight operations are bound by the same discipline as `Γ`
and the construction surface (docs/11 §7, docs/17 §5):

```text
purity:        weight operations are pure functions — no I/O,
               no ledger writes, no time reads, no network.
totality:      every weighing either fits or refuses with a
               named FailureCode. No bare exception for an
               expected verdict; no silent None.
no synthesis:  no operation fabricates a missing carrier,
               boundary, center, or trace. Missing means
               refuse.
no promotion:  fit carries no rank and raises none.
```

## 8. Anti-collapse rules

```text
no-meaning:      weight never yields meaning; PatternSpace is
                 the only landing space.
no-agency:       fāʿil never yields a real agent.
no-patienthood:  mafʿūl never yields patienthood.
no-real-event:   maṣdar never yields a real event.
no-reality:      a root never yields reality.
no-knowledge:    a fit is never knowledge.
no-hukm:         no juridical or evaluative judgment from
                 weight.
no-ontology:     no being-claims from morphology.
no-lexicon:      no lexicon before the PR-14 license.
no-verdict:      fit is a candidate, never an approval.
no-promotion:    no rank from fit; only the gate promotes.
no-entry:        weight code never enters the adapter or audit
                 layers.
law-first:       no weight code before this law; no pre-weight
                 code before docs/20.
named-refusal:   every refusal returns a named FailureCode.
```

## 9. Reserved names

`WeightImage`, `Mizan`, `MawzunCandidate`, and `SlotAlignment` are
reserved names under the reserved-name rule in `CLAUDE.md`. They
land in PR-10 **only**, as frozen carriers that depict structure.
`weigh()` and `WeightFitCandidate` land in PR-13 **only**. The
docs/20 pre-weight names are reserved by PR-9A once ratified.
Binding any of these names to a free container, or shipping any of
them before its chain position, is a `FORBIDDEN_LEAP` regardless of
CI status.

## 10. Short constitutional summary

```text
الوزن لا يعني — الوزن يصوِّر.
الوزن إلى فضاء الأوزان، لا إلى المعنى.
مطابقة الوزن ليست معرفة.
الجذر ليس الواقع.
الفاعل الصرفي ليس الفاعل الحقيقي.
لا معجم، ولا دلالة، ولا أنطولوجيا، ولا حكم.
```

In English:

```text
Weight does not mean — weight images.
Weight maps into PatternSpace, not into Meaning.
A weight fit is not knowledge.
The root is not reality.
The morphological agent is not the real agent.
No lexicon, no semantics, no ontology, no hukm.
```

---

## Cross-references

- The door this law opens, and the declarations it owes:
  [`09_ARABIC_APPLICATION_BOUNDARY.md`](09_ARABIC_APPLICATION_BOUNDARY.md).
- The registered straight-line surface every §4 row maps onto:
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md)
  and the PR-5 registry in
  [`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py).
- The terminology non-confusion law the §3 identities instantiate:
  [`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md).
- The only rank authority, which fit never bypasses:
  [`08_TRANSITION_GATE.md`](08_TRANSITION_GATE.md).
- The carrier discipline that binds the PR-10 surface:
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md).
- The generation law binding any future SlotGraph that carries
  weight content:
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md).
- The black-box boundary (model confidence is never evidence):
  [`01_BLACK_BOX_BOUNDARY.md`](01_BLACK_BOX_BOUNDARY.md).
- The chain position of this document and of the code it licenses:
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) — PR-9,
  PR-9A through PR-14, and the §2 Amendment-2/Amendment-3 records.

---

## PR-10 through PR-14 binding

PR-9 writes no code. This document binds what the later
weight-branch PRs must do:

```text
1. PR-9A ships docs/20 — the Pre-Weight Licensing Law — before
   any pre-weight or weight code. The input side of the Mīzān
   (what may be weighed, and the licensing chain that produces
   a weighable candidate) lives there, not here.
2. PR-10 ships the carriers only — WeightImage, Mizan,
   MawzunCandidate, SlotAlignment, plus the docs/20 pre-weight
   carriers — frozen, with no operation, no fit computation,
   and no meaning field; and adds the docs/19 and docs/20
   presence guards beside its constitutional tests, in the
   shape of the existing docs-presence guards.
3. PR-11 and PR-12 open the pre-weight path gates and chain
   operations under docs/20 — every transition behind a
   TransitionGate, every refusal a named FailureCode.
4. PR-13 ships weigh(WeightReadinessCandidate, ...) →
   WeightFitCandidate or a named Refusal — fit only, never
   meaning; the only licensed input is a
   WeightReadinessCandidate (docs/20).
5. PR-14 places the lexical / samāʿ / qiyās licenses before
   any semantics; until it lands, lexicon material stays out
   of the repository entirely.
```

A weight-branch PR that does not honor this law is a
`FORBIDDEN_LEAP` regardless of CI status.
