# 77 — G₀ Bare Jamid Stem / Identity Anchor Law (Zero-Layer, Law Only)

> **Status:** Constitutional law. Ratified by Amendment-57 to
> `docs/14_PR_CHAIN_ROADMAP.md`. Law only — no `src/` runtime, no
> carriers, no gates, no new global `FailureCode`, no opening of any
> horizontal branch by this PR.
> **Chain position:** `G0-L0` — zero-layer covenant. Precedes every
> derivation, plural/dual, nisbah, majāz, isnād, reference, and ḥukm
> operation in the linguistic algebra.
> **Admission:** Phase-2 X0R-E1 admission (docs/76) — law-only step.
> **Scope:** the Bare Jamid Stem as Identity Anchor. Nothing else.

---

## §1 Constitutional definition

> **G₀ هي الطبقة الصفرية للجبر اللغوي. تُصنِّف الألفاظ بوصفها
> "مراسي هوية" (Identity Anchors) لا تحمل حكماً، ولا معنى مركباً،
> ولا اشتقاقاً. تعمل بوضع لغوي حقيقي، وتصنيف أنطولوجي، ورتبة
> إبستمولوجية، وجنس نحوي، بلا مجاز ولا نقل ولا سياق.**

G₀ is the *zero layer* of the linguistic algebra. It classifies
words as **Identity Anchors** (مراسي هوية) that carry:

- no ḥukm (judgment),
- no composite meaning,
- no derivation,
- no context resolution,
- no majāz / naql (metaphor / transferred usage).

G₀ operates on the **real linguistic assignment** (الوضع اللغوي
الحقيقي) alone, with an ontological classification, an epistemic
rank, and a stem-property gender.

## §2 What enters and what leaves

| Admitted into G₀ (مرخَّص) | Forbidden / deferred (ممنوع/معلَّق) |
| :--- | :--- |
| Triliteral or quadriliteral jamid stem | Verb, present, imperative |
| Singular-form word (mufrad al-ṣūrah) | Maṣdar (event, marra, hayʾa, ṣināʿī) |
| Assigned on the real (mawḍūʿ ʿalā al-ḥaqīqah) | Ism fāʿil, ism mafʿūl |
| Identity anchor: body, matter, plant, animal, human, group, tool, place, phenomenon, real abstract | Ism makān, ism zamān, ism ālah |
| Attested by a real lexical witness | Dual, sound plural, broken plural |
| Carries masculine/feminine as a stem property | Nisbah (فَعَلِيّ / نِسْبَة) |
| Admits individual, species, genus, group, mass (ontological entity rank, not morphological) | Ṣināʿī maṣdar (يَّة) |
| | Al-taʿrīf (as a referential operation) |
| | Pronoun, demonstrative, relative |
| | Majāz, naql, terminological extension |
| | Discursive context for polysemy resolution |

## §3 Minimum ontological matrix

| Code | Ontological origin | Examples |
| :--- | :--- | :--- |
| O₁ | Solid body / inanimate object | jabal, ḥajar, qamar, arḍ |
| O₂ | Matter / mass | māʾ, turāb, zayt, laban |
| O₃ | Plant | nakhl, ʿinab, qamḥ, ward |
| O₄ | Non-rational animal | faras, asad, ḥimār, ghurāb, ʿaqrab |
| O₅ | Human / rational | bashar, rajul, imraʾah, insān |
| O₆ | Group (as singular form) | qawm, qabīlah, ʿashīrah, rahṭ |
| O₇ | Tool / manufactured | sayf, bayt, jardal, qirṭās |
| O₈ | Place / locus | balad, dār, sūq (as jamid stem) |
| O₉ | Phenomenon / effect | dukhān, ẓill, nār (in classical conception) |
| O₁₀ | Abstract / real conventional entity | ḥaqq, ʿahd, milk, jins (as self-standing conventional entities, not attributes) |

**Note:** O₉ and O₁₀ open only if the word is assigned on the
real as an *identity anchor*, not as an attribute or an event.
"Nār" is a self-standing genus in the classical conception; "ḥaqq"
is a self-standing conventional entity (not an attribute of
something else).

## §4 Epistemic classification (evidence strength)

| Rank | Meaning | Verdict in G₀ |
| :--- | :--- | :--- |
| E₀ | Weight only nominates a genus (pre-lexical) | No verdict (nomination only) |
| E₁ | One real lexical witness | Candidate for real assignment |
| E₂ | Multiple lexical witnesses (Lisān al-ʿArab, samāʿ, Qurʾanic usage) | Licensed on the real |
| E₃ | Real polysemy (e.g. *ʿayn*) | Recorded as real multiplicity, undecided |
| E₄ | Insufficient witness (does not prove the assignment) | Suspended |
| E₅ | Requires context, terminological transfer, or metaphor | Forbidden in G₀ |

## §5 Bare Jamid Stem Card (the sole output of G₀)

```text
BareJamidStemCard:
  stem: "جَبَل"
  vocalized: "جَبَل"
  size: 3
  pattern: "فَعَل"
  has_productive_addition: false
  jamid: true
  ontological_class: O₁ (jamād / natural body)
  entity_rank: individual / species / genus / group / mass (by assignment, not context)
  gender: masculine / feminine
  gender_evidence: lexical assignment / frozen stem marker / samāʿ
  epistemic_rank: E₂ (multiple witnesses)
  lexical_truth_status: attested (fixed in the lexicon)
  hard_blockers_passed: []
  d_form: 0.00
  d_wad: 0.00
  d_onto: 0.00
  decision: "licensed as a jamid identity anchor"
```

The card is the **only** output G₀ may issue. It is neither a ḥukm
nor a meaning; it is an **anchor certificate** on which later
layers may build.

## §6 Bounded epistemic distance law

Distance is computed **only after** the hard blockers of §7 have
been passed. Distance is the measure of match between the stem and
its ontological + epistemic origin.

```text
d_G0 = sqrt(
  ( α(1-S)² + β(1-J)² + γ(1-W)² + δ(1-A)² +
    ε(1-O)² + ζ(1-G)² + η(1-E)² )
  / (α + β + γ + δ + ε + ζ + η)
)
```

| Dimension | Meaning | Suggested weight |
| :--- | :--- | :--- |
| S | Stem purity (free of productive addition) | 2.0 |
| J | Jāmidiyyah (no event, no time) | 2.0 |
| W | Real-assignment attestation | 3.0 |
| A | Anchor-of-genus attestation | 2.0 |
| O | Ontological classification match | 2.0 |
| G | Gender as stem property | 1.0 |
| E | Epistemic-evidence strength | 2.0 |

| Range | Verdict |
| :--- | :--- |
| `0.00 – 0.10` | Full real origin (licensed without residuals) |
| `0.10 – 0.25` | Licensed on the real (silent residuals) |
| `0.25 – 0.40` | Licensed conditional on stronger witness (visible residuals) |
| `0.40 – 0.60` | Suspended (no verdict until assignment is proven) |
| `> 0.60` | Insufficient (forbidden or deferred) |
| Any hard blocker present | Forbidden regardless of `d` |

## §7 Hard blockers (applied before the distance)

| Blocker | Verdict |
| :--- | :--- |
| Presence of a dual | Forbidden |
| Presence of a sound or broken plural | Forbidden |
| Presence of a nisbah (shadda-yāʾ) | Forbidden |
| Presence of a ṣināʿī maṣdar (يَّة) | Forbidden |
| Presence of verbal form or tense | Forbidden |
| Presence of event-maṣdar | Forbidden |
| Presence of standard fāʿil / mafʿūl / ālah derivation | Forbidden |
| Requires majāz | Forbidden |
| Requires terminological naql | Forbidden |
| Requires context for polysemy resolution | Suspended (deferred to upper layers) |

## §8 Constitutional golden rule

> **G₀ does not issue a judgment; it issues an identity anchor.**
>
> **No derivation before G₀.**
> **No plural before G₀.**
> **No nisbah before G₀.**
> **No majāz before G₀.**
> **No context before G₀.**
> **No morphological or syntactic judgment before G₀.**
> **No composite meaning before G₀.**
>
> Every word passing G₀ is classified as a **jamid identity anchor**
> under:
>
> 1. Stem purity (freedom from productive addition).
> 2. Real-assignment attestation (lexical witness).
> 3. Ontological classification (O₁ … O₁₀).
> 4. Epistemic rank (E₀ … E₅).
> 5. Masculine or feminine (as stem property).
> 6. Entity rank (individual, species, genus, group, mass).
> 7. Bounded Euclidean distance that measures the strength of the match.
>
> Whatever fails G₀ is forbidden from derivation, composition, and
> predication, or is deferred to later layers with visible residuals
> (context, majāz, terminological naql).

## §9 Minimal G₀-only matrix (illustrative, not exhaustive)

| Stem | Size | Pattern | Ontological origin | Entity rank | Gender | Epistemic rank | d | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| jabal (جَبَل) | 3 | فَعَل | O₁ | individual / genus | m | E₂ | 0.00 | licensed |
| ḥajar (حَجَر) | 3 | فَعَل | O₁ | individual | m | E₂ | 0.00 | licensed |
| qamar (قَمَر) | 3 | فَعَل | O₁ (celestial) | individual | m | E₂ | 0.00 | licensed |
| arḍ (أَرْض) | 3 | فَعْل | O₁ | individual / mass | f | E₂ | 0.00 | licensed |
| māʾ (مَاء) | 3 | فَعْل | O₂ | mass | m | E₂ | 0.00 | licensed |
| baḥr (بَحْر) | 3 | فَعْل | O₂ | individual / mass | m | E₂ | 0.00 | licensed |
| nakhl (نَخْل) | 3 | فَعْل | O₃ | genus / collective | f (verbal) | E₂ | 0.00 | licensed |
| ʿinab (عِنَب) | 3 | فِعَل | O₃ | genus | m | E₂ | 0.00 | licensed |
| faras (فَرَس) | 3 | فَعَل | O₄ | individual / species | f (real) | E₂ | 0.00 | licensed |
| asad (أَسَد) | 3 | فَعَل | O₄ | individual / species | m | E₂ | 0.00 | licensed |
| ḥimār (حِمَار) | 3 | فِعَال | O₄ | individual / species | m | E₂ | 0.00 | licensed |
| ghurāb (غُرَاب) | 3 | فُعَال | O₄ | individual / species | m | E₂ | 0.00 | licensed |
| rajul (رَجُل) | 3 | فَعُل | O₅ | individual | m | E₂ | 0.00 | licensed |
| imraʾah (اِمْرَأَة) | 3 | فَعْلَة | O₅ | individual | f | E₂ | 0.00 | licensed |
| insān (إِنْسَان) | 3 | فِعْلَان | O₅ | genus | m/f | E₂ | 0.00 | licensed |
| qawm (قَوْم) | 3 | فَعْل | O₆ | collective | m | E₂ | 0.00 | licensed |
| qabīlah (قَبِيلَة) | 3 | فَعِيلَة | O₆ | collective | f | E₂ | 0.00 | licensed |
| sayf (سَيْف) | 3 | فَعْل | O₇ | individual | m | E₂ | 0.00 | licensed |
| bayt (بَيْت) | 3 | فَعْل | O₇ | individual | m | E₂ | 0.00 | licensed |
| jurdul (جُرْدُل) | 4 | فُعْلُل | O₇ | individual | m | E₂ | 0.00 | licensed |
| qirṭās (قِرْطَاس) | 4 | فِعْلَال | O₇ | individual | m | E₂ | 0.00 | licensed |
| ʿaqrab (عَقْرَب) | 4 | فَعْلَل | O₄ | individual / species | f (samāʿ) | E₂ | 0.00 | licensed |
| dukhān (دُخَان) | 3 | فُعَال | O₉ | phenomenon | m | E₁ | 0.10 | licensed (with residuals) |
| ẓill (ظِلّ) | 3 | فِعْل | O₉ | phenomenon | m | E₁ | 0.10 | licensed (with residuals) |
| ḥaqq (حَقّ) | 3 | فَعْل | O₁₀ | abstract conventional | m | E₂ | 0.00 | licensed |
| ʿahd (عَهْد) | 3 | فَعْل | O₁₀ | abstract conventional | m | E₂ | 0.00 | licensed |
| milk (مِلْك) | 3 | فِعْل | O₁₀ | abstract conventional | m | E₂ | 0.00 | licensed |
| ʿayn (عَيْن) | 3 | فَعْل | shared (O₁/O₂/O₅) | — | f | E₃ | 0.15 | suspended (resolved by context in an upper layer) |

## §10 Binding between G₀ and later layers

G₀ does not produce a ḥukm; it produces an **anchor certificate**.
That certificate is the foundation on which every later layer is
built:

| Later layer | Operation on the anchor |
| :--- | :--- |
| Derivation (maṣādir, verbs, attributes) | Apply morphological patterns to the anchor to yield events and attributes |
| Plural / dual | Apply number operations to the anchor (individual → group) |
| Nisbah / ṣināʿī maṣdar | Apply abstraction / affiliation relations to the anchor |
| Syntactic predication | Bind the anchor to another anchor via a relation (fāʿil, mafʿūl, iḍāfah) |
| Reference and maqām | Resolve the anchor in the discourse context (pronoun, demonstrative, definiteness) |
| Ḥukm and truth | Judge whether the predication matches the reality (real vs. metaphor) |

**Golden rule:**

> **No later layer may open without an identity anchor issued by G₀.**

## §11 Constitutional closing

> **G₀ is the zero gate of the linguistic algebra. It is what
> prevents confusion between stem and derivation, between jamid and
> mushtaqq, between real and metaphor, between existence and
> convention, between individual and group.**
>
> **By it we guarantee that every later linguistic construction is
> built on a real identity anchor, not on a lexical illusion or a
> semantic leap.**
>
> **By it we protect the language from the "hallucination" of
> abstract meanings in the matrix of genera, and defer everything
> that is conceptual, mental, conventional, contextual, or
> metaphorical to its own gate in a later stage of the algebra.**

## §12 Chain position and admission

```text
FAMILY               = G0
STEP                 = G0-L0
STEP_KIND            = LAW_ONLY
ADMISSION_GATE       = docs/76 Phase-2 X0R-E1 admission (law-only clause)
CHAIN_POSITION       = zero-layer covenant; precedes every derivation,
                       plural/dual, nisbah, majāz, isnād, reference,
                       and ḥukm operation.
ORIGIN_LAW           = docs/14_PR_CHAIN_ROADMAP.md
BOUNDARY             = law only — declares the Bare Jamid Stem as
                       Identity Anchor and the ten hard blockers.
SCOPE                = docs/77 alone; no `src/`, no tests beyond the
                       structural acceptance test for docs/77 itself.
FORBIDDEN_SURFACE    = any runtime code, any carrier, any gate, any
                       verdict, any new global FailureCode, any
                       ResidualKind expansion, any opening of any
                       horizontal branch, any adapter/audit mutation,
                       any lexicon, any semantic output, any ḥukm.
RESIDUALS            = deferred to future admitted steps
                       G0-C1 … G0-C6 (see §13).
NON_INTERFERENCE     = DAL-A* (atomic phonetic closure) — orthogonal.
                       LAFZI-B/C/D (madlūl correspondence) — not
                       replaced; G₀ issues an anchor, not a madlūl.
                       MufradDalālahClosure (PR-D3) — G₀'s anchor is
                       a precondition for admitting mufrad identity;
                       it does not replace dalālah semantics.
                       LAW-E0 / LAW-E1R — compatible; G₀ adds a
                       zero-layer identity slice, not a new partition.
```

## §13 Reserved successor steps (not shipped by this PR)

The following carriers/gates are **explicitly out of scope** for
`G0-L0` and are reserved for future admitted PRs, each requiring
its own admission, per-step boundary block, and constitutional
tests:

```text
G0-C1  Bare-stem carrier surface
       (BareJamidStemCandidate, AnchorCertificate)
G0-C2  Hard-blocker gates (§7)
G0-C3  Bounded epistemic distance computation (§6)
G0-C4  Ontological classifier (O₁ … O₁₀)
G0-C5  Epistemic ranker (E₀ … E₅)
G0-C6  Anchor-certificate issuance and downstream consumption gate
```

None of these ship in `G0-L0`. Any attempt to bundle them with the
law step is a `FORBIDDEN_LEAP` regardless of CI status.

## §14 What this law does *not* claim

- G₀ does **not** decide meaning, madlūl, or ḥukm.
- G₀ does **not** decide syntactic role.
- G₀ does **not** resolve polysemy (E₃ is recorded as multiplicity,
  not decided).
- G₀ does **not** produce a certificate of truth, correctness, or
  release readiness.
- G₀ does **not** license any horizontal branch in `docs/14`.
- G₀ does **not** modify `AnswerAudit`, `ModelClient`, or any
  adapter.
- G₀ does **not** expand the global `FailureCode` or `ResidualKind`
  enums.

## §15 Trace

```text
docs/12 → docs/13 → docs/14 → docs/52 → docs/76 → docs/77
       → tests/test_g0_bare_jamid_stem_identity_anchor_law.py
       → CLAUDE.md (PR staging).
```
