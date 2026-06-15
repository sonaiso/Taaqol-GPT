# 49 — Meta-Language Boundary Covenant

> **Status:** Constitutional law. Ratified in PV-M0.
> Constitutional origin: docs/47 (Post-Vertical Roadmap), docs/48
> (Manṭūq Boundary Law). This document is a cross-cutting covenant
> that binds every post-vertical branch using Arabic grammatical,
> morphological, phonetic, semantic, or logical meta-language terms.
>
> This document is a boundary covenant, not an encyclopedia.
> It does not close all terms.
> It only prevents domain confusion before future branches.

---

## 1. Problem statement

Arabic grammatical, morphological, phonetic, semantic, and logical
terms are often ordinary Arabic words transferred into technical use.
Without a domain tag, the same surface form may be confused across
layers:

```text
فاعل in ṣarf ≠ فاعل in naḥw ≠ real-world actor.
مفعول in ṣarf ≠ مفعول به in iʿrāb ≠ affected entity.
حرف as letter ≠ حرف as particle ≠ حرف as root material.
وزن as morphological template ≠ وزن as rank ≠ وزن as measure.
جملة as textual sentence ≠ جملة as naḥw sentence ≠ ifādah closure.
```

The project already honors a governing law that forbids straight-line
transfer between sciences (docs/04, docs/05):

```text
No technical term moves between sciences without a licensed bridge.
```

This covenant operationalizes that law for Arabic meta-language terms
specifically, before Mafhūm, Majāz, Naql, and later post-vertical
branches introduce additional terminological complexity.

---

## 2. Governing principle

```text
الميتا-لغة مرآة اللغة، لا نسيجها.
ولا يعمل اسم اصطلاحي حتى يُعرف مجاله.
```

(Meta-language mirrors language; it is not the fabric of language.
No technical term operates until its domain is identified.)

---

## 3. Central law

```text
No meta-language term may operate without an explicit domain.

No term transferred from ordinary Arabic into technical use
may cross domains without a licensed bridge.

No ṣarf term may imply a naḥw role.
No naḥw term may imply a real-world role.
No meta-language term may become a truth claim, hukm, tanzīl,
or authority by itself.
```

---

## 4. Domain levels

Every meta-language term used in this project must declare which
level it operates at:

```text
Level 0 — Object language (الكلام العربي نفسه):
    The Arabic speech itself: باء، قام، زيد، ضرب، كتاب.

Level 1 — Formal description (الصوتيات / الصرف / النحو):
    Names describing speech structure: حرف، حركة، مقطع، وزن،
    فاعل (pattern), مفعول (pattern), مبني، معرب.

Level 2 — Semantic/Logical description (الدلالة / المنطق):
    Names describing meaning relations: مطابقة، تضمن، التزام،
    دال، مدلول، إفادة، حكم.

Level 3 — Real-world reference (الإحالة / الواقع):
    Names describing reality: الفاعل الواقعي، المتأثر،
    الحدث، الزمان، المكان.
```

A term may NOT ascend levels without a licensed bridge:

```text
Level 1 → Level 2 requires a dalālah gate.
Level 2 → Level 3 requires a hukm + tanzīl gate.
Level 1 → Level 3 is FORBIDDEN (no ṣarf term produces reality).
```

---

## 5. Mandatory examples

### 5.1 فاعل (fāʿil)

```text
SARF_FAʿIL_PATTERN       — Level 1 (morphological template فاعل)
    preserves: formal agency-direction affordance
    opens:     contractability as potential agent slot
    forbids:   naḥw agency, real-world acting

NAHW_AGENT               — Level 1 (syntactic subject-agent)
    preserves: grammatical subject status under iʿrāb
    opens:     ifādah candidacy (with predicate)
    forbids:   real-world actor identity

REAL_WORLD_ACTOR         — Level 3 (referential agent)
    preserves: event participation as cause
    opens:     nothing in the formal system
    forbids:   nothing in the formal system
```

The governing rule:

```text
وزن فاعل في الصرف يفتح role potential.
ولا يثبت الفاعلية النحوية.
ولا يثبت الفاعلية الواقعية.
```

### 5.2 مفعول (mafʿūl)

```text
SARF_MAFʿUL_PATTERN      — Level 1 (morphological template مفعول)
    preserves: formal patient-direction affordance
    opens:     contractability as potential object slot
    forbids:   naḥw object status, real-world affectedness

NAHW_OBJECT              — Level 1 (syntactic object under iʿrāb)
    preserves: grammatical object status
    opens:     relation candidacy within composition
    forbids:   real-world patient identity

REAL_WORLD_PATIENT       — Level 3 (referential affected entity)
    preserves: event participation as affected
    opens:     nothing in the formal system
    forbids:   nothing in the formal system
```

### 5.3 وزن (wazn)

```text
SARF_WAZN_TEMPLATE       — Level 1 (ṣarf pattern template)
    preserves: syllable structure, root-letter positions
    opens:     weight fit candidacy (PR-13)
    forbids:   meaning, agency, rank

RANK                     — Level 2 (SlotGeometry rank)
    preserves: lattice position
    opens:     gate transition evidence
    forbids:   conflation with morphological template

MEASURE                  — Level 3 (physical/mathematical measure)
    preserves: quantity
    opens:     nothing in this project
    forbids:   conflation with either of the above
```

### 5.4 حرف (ḥarf)

```text
LETTER_NAME              — Level 0/1 (the letter as alphabetic unit)
    preserves: identity in the writing system
    opens:     spelling, root identification
    forbids:   meaning attribution

LETTER_SOUND             — Level 1 (phonetic realization)
    preserves: articulation point (makhraj), manner (ṣifa)
    opens:     syllable candidacy
    forbids:   meaning attribution

PARTICLE_OF_MEANING      — Level 1 (naḥw particle: حرف جر، حرف عطف)
    preserves: relational function in syntax
    opens:     governance (ʿamal) candidacy
    forbids:   independent meaning, referential content

ROOT_MATERIAL            — Level 1 (radical letter in root)
    preserves: position in triconsonantal/quadriconsonantal root
    opens:     derivation candidacy
    forbids:   meaning by itself
```

### 5.5 جملة (jumla)

```text
TEXTUAL_SENTENCE         — Level 0 (any stretch of text)
    preserves: surface segmentation
    opens:     parsing candidacy
    forbids:   ifādah, naḥw sentence status

NAHW_SENTENCE            — Level 1 (isnād: musnad + musnad ilayh)
    preserves: predication structure
    opens:     ifādah candidacy
    forbids:   automatic truth, real-world correspondence

IFADAH_CLOSURE           — Level 2 (closed proposition candidate)
    preserves: dalālah closure + relation closure + maqām verdict
    opens:     hukm candidacy
    forbids:   automatic truth, reality, tanzīl without gate
```

---

## 6. Failure codes (reserved for future runtime)

The following failure codes are reserved for runtime implementation
when meta-language enforcement becomes operational:

```text
META_TERM_DOMAIN_MISSING         — a meta-language term was used
                                   without declaring its domain level.

META_TERM_DOMAIN_LEAP            — a term was treated at a domain
                                   level higher than its declaration.

META_TERM_UNLICENSED_TRANSFER    — a term was transferred from one
                                   science (ṣarf/naḥw/dalālah/wāqiʿ)
                                   to another without a licensed bridge.

SARF_TO_NAHW_ROLE_LEAP           — a morphological pattern was used
                                   to imply a syntactic role without
                                   a composition/contract gate.

NAHW_TO_REALITY_ROLE_LEAP        — a syntactic role was used to imply
                                   a real-world participant without
                                   hukm + tanzīl.
```

These codes do not exist in the runtime today. They are reserved
names that future PRs (if/when meta-language enforcement becomes
operational) must use. No PR may introduce a different name for
the same refusal.

---

## 7. Binding rules for all future PRs

Any PR that introduces, modifies, or consumes Arabic meta-language
terms must satisfy:

```text
Rule 1: Every meta-language term in a carrier, enum value, or
         docstring must carry or reference its domain level.

Rule 2: No carrier may conflate terms from different domain levels
         in a single field without a bridge declaration.

Rule 3: Code review must flag any term that appears at multiple
         domain levels without explicit disambiguation.

Rule 4: A term's domain level is fixed at the point of introduction
         into the project's vocabulary. Changing the level requires
         an Amendment PR.

Rule 5: The mandatory examples in §5 are governing — they are not
         illustrative but constitutional. A PR that contradicts
         them is a FORBIDDEN_LEAP.
```

---

## 8. Relationship to existing laws

This covenant extends, not replaces, the following:

| Existing law | Relationship |
|---|---|
| docs/04 (Forbidden Straight Lines) | This covenant operationalizes the "no term crosses sciences without a bridge" rule for Arabic meta-language specifically. |
| docs/05 (Transition Discipline) | Domain-level transitions are a special case of gate transitions. |
| docs/19 (Arabic Weight Boundary) | Weight (وزن) as morphological template is Level 1 only; this covenant prevents conflation with Rank. |
| docs/34 (Formal Shape Registry) | Formal definitions (PR-F2 through PR-F7) live at Level 1; this covenant prevents their promotion to Level 2 or Level 3 without a gate. |
| docs/48 (Manṭūq Boundary Law) | Manṭūq operates at Level 1→Level 2 boundary; terms like "منطوق" and "مفهوم" are Level 2 meta-language. |

---

## 9. What this covenant does NOT do

```text
This covenant does NOT:
- close any individual term (closure requires law + boundary + tests)
- create a runtime carrier or enum
- license any future branch (PV-A3, PV-B*, PV-C* still require
  their own laws)
- constitute an encyclopedia of Arabic terminology
- replace the admission rule in docs/47 §4
```

---

## 10. Candidate term families (inventoried, not closed)

The following families are inventoried but not closed by this
covenant. Each future family requires its own law or runtime branch
if it becomes operational:

```text
Family: Phonetics (الصوتيات)
    Terms: مخرج، صفة، حركة، مد، مقطع، اقتصاد صوتي
    Level: 1

Family: Morphology (الصرف)
    Terms: وزن، جذر، مادة، بناء، اشتقاق، تصريف، جامد، مشتق، منقول
    Level: 1

Family: Syntax (النحو)
    Terms: فاعل، مفعول، مبتدأ، خبر، عامل، معمول، إعراب، بناء، جملة
    Level: 1

Family: Semantics (الدلالة)
    Terms: مطابقة، تضمن، التزام، دال، مدلول، وضع، استعمال، حمل
    Level: 2

Family: Logic / Uṣūl (المنطق / الأصول)
    Terms: منطوق، مفهوم، قيد، شرط، علة، موافقة، مخالفة، تخريج، تنقيح، تحقيق
    Level: 2

Family: Reference (الإحالة)
    Terms: ضمير، إشارة، موصول، عائد، مرجع
    Level: 1 → 2 → 3 (must traverse intermediate gates;
           direct 1→3 is FORBIDDEN per §4)
```

---

## 11. Governing sentence

```text
من قال "فاعل" ولم يحدد مجاله، لم يقل شيئًا صالحًا للبناء عليه.
```

(Whoever says "fāʿil" without specifying its domain has said nothing
fit to build upon.)
