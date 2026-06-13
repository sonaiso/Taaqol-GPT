# 34 — Formal Shape Registry Law

> **Status:** Constitutional law. Ratified in PR-F1.
> This document binds every PR that constructs, consumes, or depends upon
> a `FormalShapeDefinition`, a `FormalShapeFamily`, a `FormalShapeDomain`,
> or a `FormalShapeClosure`. It establishes the formal shape boundary:
> no semantic lexicon entry is constructible without formal shape closure.

## 0. Governing principle

```text
No semantic lexicon entry without formal shape.
No formal shape without proven definition.
No proven definition without constitutional evidence.
No ContractabilityProfile string has grammatical standing
    until a FormalShapeDefinition proves it.
No open string is a formal category.
No transition from signifier to meaning without the formal middle term.
The Formal Shape Registry is structure, not meaning.
```

The supreme law of this branch:

> لا مدلول وضعي للمعاني قبل تعريف شكلي
> (No semantic-wadʿi signified for meanings before a formal definition.)

A `FormalShapeDefinition` is the constitutional middle term between:
- the **signifier surface** (dal, phonetic trace, weight fit) — proved
  by the pre-semantic chain (PR-10 through PR-19), and
- the **semantic lexicon** (meaning, ifādah, hukm) — not yet licensed.

Without a Formal Shape Registry, the only path from signifier to
meaning would be a forbidden straight line:
`ContractabilityProfile.open_string → SemanticLexicon`. This law closes
that gap by requiring a proven formal shape as the licensed bridge.

## 1. FormalShapeDomain — the top-level classification

```text
FormalShapeDomain:
    WORD_CLASS           — ism / fiʿl / ḥarf (docs/34 §5)
    BUILT_REFERENCE      — built forms and reference forms (docs/34 §6)
    WEIGHT_PATTERN       — weight-pattern definitions (docs/34 §7)
    INFLECTION           — iʿrāb / bināʾ / triptote / diptote (docs/34 §8)
    CONTRACT_SLOT        — formal agent / object / subject / predicate (docs/34 §9)
    COMPOSITION_PATTERN  — nominal / verbal / iḍāfa / etc. (docs/34 §10)
```

Each domain is a bounded classification space. Domains do not overlap:
a formal shape belongs to exactly one domain.

## 2. FormalShapeFamily — the sub-classification within a domain

```text
FormalShapeFamily:
    domain      : FormalShapeDomain
    family_id   : str   — unique identifier within the domain
    description : str   — non-empty human-readable description
```

Families group related formal shapes within a domain. For example,
within WORD_CLASS: `ism`, `fiʿl`, `ḥarf` are families. Within
INFLECTION: `iʿrāb`, `bināʾ`, `mamduud`, `maqsuur`, `manquus` are
families.

## 3. FormalShapeDefinition — the proven type

```text
FormalShapeDefinition:
    shape_id                : str   — unique identifier (globally unique)
    domain                  : FormalShapeDomain
    family                  : FormalShapeFamily
    canonical_name          : str   — the Arabic grammatical term
    definition_text         : str   — formal textual definition
    distinguishing_evidence : str   — what proves this shape vs. others
    boundary_conditions     : tuple[str, ...]  — when this shape applies
    exclusion_conditions    : tuple[str, ...]  — when this shape does NOT apply
    weight_constraint       : str | None  — weight pattern requirement (if any)
    path_constraint         : str | None  — PathKind constraint (if any)
    rank                    : Rank
    residuals               : tuple[Residual, ...]
    trace_ref               : str
```

### 3.1 Constitutional requirements for a FormalShapeDefinition

Every FormalShapeDefinition must satisfy:

1. **shape_id** — globally unique, non-empty string.
2. **domain** — must be a valid FormalShapeDomain member.
3. **family** — must be a FormalShapeFamily whose domain matches.
4. **canonical_name** — non-empty Arabic grammatical term.
5. **definition_text** — non-empty formal textual definition.
6. **distinguishing_evidence** — non-empty string proving distinction.
7. **boundary_conditions** — non-empty tuple of applicability conditions.
8. **exclusion_conditions** — tuple (may be empty) of non-applicability.
9. **weight_constraint** — if present, must name a valid weight pattern.
10. **path_constraint** — if present, must name a valid PathKind member.
11. **rank** — must not exceed the domain's rank ceiling.
12. **residuals** — no HIDDEN_FORBIDDEN or BLOCKING residuals.
13. **trace_ref** — non-empty string.

A FormalShapeDefinition that fails any requirement is refused with a
named `FailureCode`.

### 3.2 What a FormalShapeDefinition is NOT

```text
FormalShapeDefinition ≠ Meaning.
FormalShapeDefinition ≠ SemanticEntry.
FormalShapeDefinition ≠ WadʿiSignified.
FormalShapeDefinition ≠ ConceptualMeaning.
FormalShapeDefinition ≠ Reference.
FormalShapeDefinition ≠ Dalālah (mutabaqah / tadammun / iltizām).
FormalShapeDefinition ≠ SyntaxRole (it is formal category, not assignment).
```

A FormalShapeDefinition describes the **structural form** of a
grammatical category — its shape, conditions, and evidence — never
its semantic content. It is the "what-shape" (mā shakluhu), never the
"what-it-means" (mā maʿnāhu).

## 4. FormalShapeRegistry — the classified collection

```text
FormalShapeRegistry:
    domain         : FormalShapeDomain
    families       : tuple[FormalShapeFamily, ...]
    definitions    : tuple[FormalShapeDefinition, ...]
    rank_ceiling   : Rank
    closure_state  : FormalShapeClosureState
```

The registry holds all definitions for a single domain. A registry
with no definitions is EMPTY. A registry with definitions but
incomplete families is PARTIAL. A registry with all required families
proven is CLOSED.

### 4.1 FormalShapeClosureState

```text
FormalShapeClosureState:
    CLOSED   — all required families have at least one proven definition
    PARTIAL  — some families defined, some missing
    EMPTY    — no definitions registered
    REFUSED  — closure check failed with a named FailureCode
```

## 5. Domain: WORD_CLASS — ism / fiʿl / ḥarf

The WORD_CLASS domain classifies every Arabic word into exactly one of
three families:

```text
Family: ISM (noun/name)
    Evidence: accepts al- (definite article), tanwīn, or jarr (genitive)
    Boundary: not a verb; not a particle

Family: FI'L (verb)
    Evidence: accepts tāʾ al-fāʿil (subject-tāʾ), qad, sawfa, or sīn
    Boundary: not a noun; not a particle

Family: HARF (particle)
    Evidence: does not accept noun-markers or verb-markers
    Boundary: neither noun nor verb; carries meaning only in
              combination, not independently
```

Each family requires at least one FormalShapeDefinition proving the
distinguishing evidence.

## 6. Domain: BUILT_REFERENCE — built forms and reference forms

The BUILT_REFERENCE domain classifies forms that are morphologically
"built" (mabnī) on fixed patterns and reference forms:

```text
Family: PERSONAL_PRONOUN — (ḍamīr)
    Subcategories: munfaṣil (separate), muttaṣil (attached),
                   mustatir (hidden)

Family: DEMONSTRATIVE — (ism ishārah)
    Near/far, singular/dual/plural, masculine/feminine

Family: RELATIVE_PRONOUN — (ism mawṣūl)
    Specific (alladhī, allatī, ...) and generic (man, mā)

Family: INTERROGATIVE — (ism istifhām)
    man, mā, ayyu, matā, ayna, kayfa, kam, ...

Family: CONDITIONAL — (adawāt al-sharṭ)
    in, idhā, man, mā, matā, ayna, ...
```

## 7. Domain: WEIGHT_PATTERN — weight-pattern definitions

The WEIGHT_PATTERN domain classifies morphological weight patterns
(awzān):

```text
Family: VERBAL_PATTERNS — verb weight forms
    faʿala, faʿʿala, fāʿala, afʿala, tafaʿʿala, tafāʿala,
    infaʿala, iftaʿala, ifʿalla, istafʿala, ...

Family: NOMINAL_PATTERNS — noun weight forms
    fāʿil, mafʿūl, mifʿāl, faʿīl, fuʿūl, afʿāl,
    mafāʿil, mafāʿīl, ...

Family: MAṢDAR_PATTERNS — verbal noun weight forms
    faʿl, fuʿūl, fiʿālah, tafʿīl, mufāʿalah, ifʿāl, ...
```

Each definition carries the weight pattern as its weight_constraint
and proves distinction from other patterns in the same family.

## 8. Domain: INFLECTION — iʿrāb / bināʾ / triptote / diptote

The INFLECTION domain classifies case/mood marking systems:

```text
Family: I'RAB — syntactic case marking (muʿrab words)
    rafʿ (nominative), naṣb (accusative), jarr (genitive),
    jazm (jussive)

Family: BINA' — fixed ending (mabnī words)
    mabnī ʿalā al-fatḥ, mabnī ʿalā al-ḍamm,
    mabnī ʿalā al-kasr, mabnī ʿalā al-sukūn

Family: TRIPTOTE — fully declinable (munṣarif)
    Takes tanwīn and all case markers

Family: DIPTOTE — restricted declension (mamnūʿ min al-ṣarf)
    Does not take tanwīn; takes fatḥah instead of kasrah in jarr
```

## 9. Domain: CONTRACT_SLOT — formal agent / object / subject / predicate

The CONTRACT_SLOT domain classifies the **formal** grammatical positions
(not their semantic content):

```text
Family: FORMAL_SUBJECT — (mubtadaʾ / fāʿil / nāʾib al-fāʿil)
    The formal subject position in a clause — proved by
    iʿrāb (nominative case), not by agency

Family: FORMAL_PREDICATE — (khabar / fiʿl)
    The formal predicate position — proved by
    relationship to subject, not by action

Family: FORMAL_OBJECT — (mafʿūl bih / other mafʿūlāt)
    The formal object position — proved by
    naṣb (accusative case), not by patienthood

Family: FORMAL_COMPLEMENT — (tamyīz / ḥāl / muḍāf ilayh)
    Formal complement positions — proved by structural
    relationship, not by semantic role
```

**Constitutional invariant**: CONTRACT_SLOT ≠ SyntaxRole. The formal
position is a structural category proven by inflection and governance
evidence, not a semantic assignment of agency, patienthood, or action.

## 10. Domain: COMPOSITION_PATTERN — sentence and phrase patterns

The COMPOSITION_PATTERN domain classifies structural composition forms:

```text
Family: NOMINAL_SENTENCE — (jumlah ismiyyah)
    mubtadaʾ + khabar pattern; subject-predicate structure

Family: VERBAL_SENTENCE — (jumlah fiʿliyyah)
    fiʿl + fāʿil pattern; verb-subject structure

Family: IDAFA — (iḍāfah)
    muḍāf + muḍāf ilayh; annexation structure

Family: SIFA_MAWSUF — (ṣifah + mawṣūf)
    adjective-noun attribution structure

Family: ATIF — (ʿaṭf)
    coordination pattern with conjunction

Family: BADAL — (badal)
    apposition/substitution pattern
```

## 11. FormalShapeClosure — the gate to semantic eligibility

```text
FormalShapeClosure:
    required_domains       : tuple[FormalShapeDomain, ...]
    domain_states          : dict[FormalShapeDomain, FormalShapeClosureState]
    closure_verdict        : FormalShapeClosureVerdict
    failure_code           : FailureCode | None
    rank                   : Rank
    residuals              : tuple[Residual, ...]
    trace_ref              : str
```

### 11.1 FormalShapeClosureVerdict

```text
FormalShapeClosureVerdict:
    CLOSED        — all required domains are CLOSED
    PARTIAL       — some domains closed, some not
    REFUSED       — closure check failed
    NOT_APPLICABLE — domain not required for this candidate
```

### 11.2 Closure requirements

A `FormalShapeClosure` is CLOSED only when ALL of the following hold:

1. Every required `FormalShapeDomain` has `closure_state == CLOSED`.
2. Every CLOSED domain has at least one FormalShapeDefinition per
   required family.
3. No domain has HIDDEN_FORBIDDEN or BLOCKING residuals.
4. Rank does not exceed the formal shape rank ceiling.

### 11.3 The semantic eligibility gate

```text
No semantic lexicon entry without FormalShapeClosure.CLOSED.
No IfādahCandidate without FormalShapeClosure.CLOSED for
    the relevant composition pattern domain.
No wadʿi/dalālah access without FormalShapeClosure.CLOSED
    for the relevant word-class and inflection domains.
```

This gate operates between PR-19 (RelationCandidate) and PR-20
(IfādahCandidate). Without formal shape closure, the path from
composition affordance to propositional candidacy is a forbidden leap:

```text
RelationCandidate.open_string → SemanticLexicon = FORBIDDEN_LEAP
RelationCandidate → FormalShapeClosure.CLOSED → SemanticLexicon = licensed
```

## 12. FailureCodes consumed by this law

The Formal Shape Registry reuses existing FailureCodes:

- `FailureCode.REQUIRED_SLOT_EMPTY` — missing required field.
- `FailureCode.GATE_REQUIRED` — attempting to bypass the formal shape gate.
- `FailureCode.HIDDEN_RESIDUAL` — HIDDEN_FORBIDDEN residual present.
- `FailureCode.BLOCKING_RESIDUAL_PRESENT` — BLOCKING residual present.
- `FailureCode.RANK_EXCEEDS_CEILING` — rank above ceiling.
- `FailureCode.TRACE_MISSING` — trace reference absent.

No new FailureCode members are introduced by PR-F1.

## 13. PR-F1 through PR-F7 staging

```text
PR-F1   Formal Shape Registry Law (this document — law only, no code)
PR-F2   Word-Class Formal Definitions (ISM / FI'L / HARF carriers)
PR-F3   Built and Reference Formal Definitions (pronouns, demonstratives, etc.)
PR-F4   Weight Formal Definitions (verbal / nominal / maṣdar patterns)
PR-F5   Inflection Formal Definitions (iʿrāb / bināʾ / triptote / diptote)
PR-F6   Contract Slot Formal Definitions (formal agent / object / subject / predicate)
PR-F7   Composition Pattern Formal Definitions (nominal / verbal / iḍāfa / etc.)
```

Each PR-F2 through PR-F7 produces:
- FormalShapeDefinition instances for its domain
- Constitutional tests proving each definition
- Registry closure proof for the domain

## 14. Forbidden outputs (proven absent in this law)

- meaning, reference, denotation, concept
- ifādah, hukm, reality, ontology, truth-value
- semantic lexicon content
- wadʿi/dalālah/iltizām
- ExtraLetterLicense, 𝒞_Aug
- adapter or audit changes
- new FailureCode members
- new runtime dependencies
- SyntaxRole assignment (formal shape is category, not assignment)

## 15. Constitutional invariants

1. `FormalShapeDefinition ≠ Meaning` — formal shape is structure,
   never semantic content.
2. `FormalShapeDefinition ≠ SemanticEntry` — the definition does not
   produce or contain a semantic lexicon entry.
3. `FormalShapeDefinition ≠ Dalālah` — no mutabaqah, tadammun, or
   iltizām.
4. `FormalShapeRegistry ≠ SemanticLexicon` — the registry is a
   structural catalogue, not a meaning dictionary.
5. `CONTRACT_SLOT ≠ SyntaxRole` — the formal position is proved by
   inflection and governance, not assigned by semantic agency.
6. The Formal Shape Registry is the constitutional middle term between
   signifier and meaning — without it, the path is a forbidden leap.
7. Every refusal carries a named `FailureCode`.
8. No rank promotion beyond the domain's rank ceiling.
9. No hidden or blocking residuals pass.
10. All operations are pure: no I/O, no ledger, no network.
11. No semantic lexicon entry without `FormalShapeClosure.CLOSED`.
12. Formal shapes are proven by constitutional evidence (weight
    constraints, path constraints, inflection patterns), not by
    definition-by-fiat.

## 16. Euclidean principle

```text
No meaning before form.
No form before signifier.
No signifier before trace.
```

The chain that this law governs:

```text
Signifier (PR-15) → Form (PR-F1..F7) → Meaning (PR-20+)
```

Each link requires proof of the previous. The Formal Shape Registry is
the proof of form — the constitutional middle term that licenses the
transition from proven signifier surface to semantic eligibility.
