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

## 3A. Meta-Term Construction Law

A meta-language term is not licensed by surface similarity between
ordinary Arabic and technical Arabic. It is licensed by a complete
qiyās-based construction chain:

```text
الميتا-مصطلح لا يولد من تشابه اللفظ.
بل يولد من أصل محفوظ،
وفرع محتاج،
وباعث معتبر،
ووصف مؤثر جامع،
وانتفاء فرق قادح،
وسبب مشغّل،
وشروط ضابطة،
وموانع منتفية.
```

The full licensing chain:

```text
MetaTerm(t) is licensed iff:

1. أصل محفوظ      — preserved origin in ordinary Arabic usage
2. فرع مطلوب      — declared technical branch requiring the transfer
3. باعث معتبر     — valid reason the branch was needed
4. وصف مؤثر جامع  — effective attribute linking origin to branch
5. انتفاء فرق قادح — absence of disqualifying difference
6. سبب مشغّل      — triggering cause that activates the term
7. شروط عمل       — conditions for the term to operate
8. انتفاء موانع    — absence of blockers
9. مجال مصرح      — declared domain (ṣarf / naḥw / ṣawt / dalālah / manṭiq / wāqiʿ / ḥukm)
10. دليل           — evidence of the transfer or usage
11. رتبة           — bounded rank (never exceeds candidate)
12. بقايا          — visible residuals
13. trace_ref      — trace to original_origin, transferred_branch, baʿith,
                     wasf_muʾaththir, and farq_qadih decision
```

Note: `MetaTermContract` (§3B) also requires `effect` and
`forbidden_overclaim` as mandatory disclosures. These are not
licensing preconditions (a term can be licensed without them being
evaluated first) but they must be declared before a licensed term
may be consumed by a downstream PR.

### 3A.1 Definitions

**Baʿith (الباعث):** The motivating reason for creating the
technical branch. It answers: *why did we need to transfer this
term?* The baʿith alone does not license the transfer.

**Wasf muʾaththir (الوصف المؤثر):** The effective attribute that
links the origin meaning to the branch meaning. It is the *jāmiʿ*
(unifier) that makes the transfer rational, not merely lexical.
Without it, the transfer is surface similarity only.

**Farq qādiḥ (الفرق القادح):** A disqualifying difference between
origin and branch that, if present, *prevents* the transfer or
prevents its generalization. It is the constitutional veto on
false analogy.

**Sabab (السبب):** The triggering event that activates the term
within a specific instance.

**Sharṭ (الشرط):** The conditions that must hold for the sabab to
operate.

**Māniʿ (المانع):** A blocker that prevents the term from operating
even when the sabab is present.

### 3A.2 Governing chain

```text
لا فرع بلا باعث.
ولا باعث بلا وصف مؤثر.
ولا وصف مؤثر مع فرق قادح.
ولا سبب بلا شرط.
ولا شرط يعمل مع مانع.
```

Translation:

```text
No branch without baʿith.
No baʿith without effective attribute.
No effective attribute with disqualifying difference.
No sabab without sharṭ.
No sharṭ operates with māniʿ.
```

### 3A.3 Why this matters before Mafhūm

`Mafhūm` is itself a transferred term:

```text
مفهوم in ordinary Arabic = what is understood.
مفهوم in Uṣūl = a non-spoken semantic branch derived from
                  a preserved manṭūq under specific conditions.
```

Without the effective-attribute / disqualifying-difference framework,
any "understanding" could become a `MafhumCandidate`. The construction
law prevents this:

```text
لا مفهوم بلا منطوق.
ولا منطوق بلا قيد.
ولا قيد بلا وصف مؤثر.
ولا مفهوم مع فرق قادح.
```

### 3A.4 Forbidden false-analogy transfers

The following equations are constitutionally forbidden because in
each case a disqualifying difference is present:

```text
CV syllable = word                              (farq: syllable ≠ lexeme)
two-letter lexical word = biliteral root        (farq: surface ≠ derivation)
surface length = root cardinality               (farq: letter count ≠ radical count)
morphological pattern = syntactic role          (farq: form ≠ relation)
syntactic role = real-world role                (farq: grammar ≠ reality)
hukm candidate = execution                     (farq: candidate ≠ certificate)
iftiqār (demand) = transition license           (farq: need ≠ evidence)
```

The governing principle:

```text
تشابه اللفظ يفتح احتمالًا فقط.
والوصف المؤثر يرخص الفرع.
والفرق القادح يمنع النقل.
```

---

## 3B. MetaTermContract template

Every meta-language term introduced in this project must, in principle,
satisfy the following contract. This template is not runtime code; it is
a constitutional schema that future PRs must honor:

```text
MetaTermContract:

1.  surface_name          — اللفظ الظاهر للمصطلح
2.  original_origin       — الأصل اللغوي أو الاستعمال الأول
3.  transferred_branch    — الفرع الاصطلاحي المنقول إليه
4.  baʿith                — الباعث: لماذا احتجنا هذا الفرع؟
5.  wasf_muʾaththir       — الوصف المؤثر: ما الجامع المرخص؟
6.  farq_qadih            — الفرق القادح: ما الفرق المانع للنقل أو التعميم؟
7.  sabab                 — السبب: ما الواقعة المشغلة؟
8.  shart                 — الشرط: ما الذي يلزم ليعمل المصطلح؟
9.  maniʿ                 — المانع: ما الذي يمنع عمل المصطلح؟
10. domain                — المجال: صرف / نحو / صوت / دلالة / منطق / واقع / حكم
11. effect                — الأثر: ما الذي يفتحه المصطلح عند الترخيص؟
12. forbidden_overclaim   — ما الذي لا يحق للمصطلح ادعاؤه؟
13. evidence              — دليل النقل أو الاستعمال
14. rank                  — سقف الادعاء
15. residuals             — ما بقي غير محسوم
16. trace_ref             — أثر المصطلح إلى أصله وفرعه وباعثه ووصفه المؤثر وقرار فرقه القادح
```

The governing sentence:

```text
الميتا-مصطلح قياس مرخص، لا تسمية عائمة.
```

(A meta-term is a licensed analogy, not a floating label.)

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
    original_origin:     من نُسب إليه فعل في الاستعمال العام
    baʿith:              الحاجة إلى تسمية صيغة صرفية تدل على جهة القيام
    wasf_muʾaththir:     نسبة بين أصل حدثي وصورة لفظية تدل على جهة القيام
    farq_qadih:          الصورة الصرفية لا تساوي علاقة إسنادية في تركيب
    preserves:           formal agency-direction affordance
    opens:               contractability as potential agent slot
    forbids:             naḥw agency, real-world acting

NAHW_AGENT               — Level 1 (syntactic subject-agent)
    original_origin:     من نُسب إليه فعل في الاستعمال العام
    baʿith:              الحاجة إلى تسمية الطرف المسند إليه الفعل في التركيب
    wasf_muʾaththir:     نسبة الفعل إلى طرف داخل علاقة إسنادية
    farq_qadih:          الفاعل النحوي ليس بالضرورة فاعلًا واقعيًا
    preserves:           grammatical subject status under iʿrāb
    opens:               ifādah candidacy (with predicate)
    forbids:             real-world actor identity

REAL_WORLD_ACTOR         — Level 3 (referential agent)
    preserves:           event participation as cause
    opens:               nothing in the formal system
    forbids:             nothing in the formal system
```

The governing rule:

```text
وزن فاعل في الصرف يفتح role potential.
ولا يثبت الفاعلية النحوية.
ولا يثبت الفاعلية الواقعية.

فاعل الصرف فرع من معنى الفاعلية اللغوية،
لكن وصفه المؤثر صرفي،
وفرقه القادح عن النحو أنه صورة لا علاقة إسناد.
```

### 5.2 مفعول (mafʿūl)

```text
SARF_MAFʿUL_PATTERN      — Level 1 (morphological template مفعول)
    original_origin:     من وقع عليه الفعل في الاستعمال العام
    baʿith:              الحاجة إلى تسمية صيغة تدل على جهة وقوع الحدث
    wasf_muʾaththir:     وجود جهة انفعال أو تلقي للفعل في الصورة الصرفية
    farq_qadih:          الصيغة الصرفية لا تثبت أنه مفعول به في الجملة
    preserves:           formal patient-direction affordance
    opens:               contractability as potential object slot
    forbids:             naḥw object status, real-world affectedness

NAHW_OBJECT              — Level 1 (syntactic object under iʿrāb)
    original_origin:     من وقع عليه الفعل في الاستعمال العام
    baʿith:              الحاجة إلى تسمية الطرف الذي وقع عليه الفعل في التركيب
    wasf_muʾaththir:     تعلق الفعل المتعدي بطرف منصوب أو في محل نصب
    farq_qadih:          المفعول به النحوي ليس بالضرورة اسم مفعول صرفيًا
    preserves:           grammatical object status
    opens:               relation candidacy within composition
    forbids:             real-world patient identity

REAL_WORLD_PATIENT       — Level 3 (referential affected entity)
    preserves:           event participation as affected
    opens:               nothing in the formal system
    forbids:             nothing in the formal system
```

### 5.3 وزن (wazn)

```text
SARF_WAZN_TEMPLATE       — Level 1 (ṣarf pattern template)
    original_origin:     القياس أو المقدار في الاستعمال العام
    baʿith:              الحاجة إلى تسمية قالب يضبط توزيع الحروف والحركات
    wasf_muʾaththir:     المشابهة في معنى القياس: قياس المادة اللفظية على قالب
    farq_qadih:          الوزن الصرفي ليس رتبة معرفية وليس مقدارًا ماديًا
    preserves:           syllable structure, root-letter positions
    opens:               weight fit candidacy (PR-13)
    forbids:             meaning, agency, rank

RANK                     — Level 2 (SlotGeometry rank)
    preserves:           lattice position
    opens:               gate transition evidence
    forbids:             conflation with morphological template

MEASURE                  — Level 3 (physical/mathematical measure)
    preserves:           quantity
    opens:               nothing in this project
    forbids:             conflation with either of the above
```

### 5.4 حرف (ḥarf)

```text
LETTER_NAME              — Level 0/1 (the letter as alphabetic unit)
    original_origin:     طرف الشيء أو حده في الاستعمال العام
    baʿith:              الحاجة إلى تسمية وحدات الكتابة
    wasf_muʾaththir:     كونها وحدة حدية صغيرة تدخل في بناء أكبر
    farq_qadih:          اسم الحرف ليس الصوت، وليس حرف المعنى
    preserves:           identity in the writing system
    opens:               spelling, root identification
    forbids:             meaning attribution

LETTER_SOUND             — Level 1 (phonetic realization)
    original_origin:     طرف الشيء أو حده في الاستعمال العام
    baʿith:              الحاجة إلى تسمية الصوت المنطوق
    wasf_muʾaththir:     كونه وحدة صوتية حدية في نظام النطق
    farq_qadih:          الصوت ليس حرف المعنى وليس حرف الجذر
    preserves:           articulation point (makhraj), manner (ṣifa)
    opens:               syllable candidacy
    forbids:             meaning attribution

PARTICLE_OF_MEANING      — Level 1 (naḥw particle: حرف جر، حرف عطف)
    original_origin:     طرف الشيء أو حده في الاستعمال العام
    baʿith:              الحاجة إلى تسمية أدوات الربط النحوي
    wasf_muʾaththir:     كونه وحدة وظيفية لا تستقل بمعنى بل تربط
    farq_qadih:          حرف المعنى ليس حرف هجاء وليس حرفًا جذريًا
    preserves:           relational function in syntax
    opens:               governance (ʿamal) candidacy
    forbids:             independent meaning, referential content

ROOT_MATERIAL            — Level 1 (radical letter in root)
    original_origin:     طرف الشيء أو حده في الاستعمال العام
    baʿith:              الحاجة إلى تسمية مكونات الجذر
    wasf_muʾaththir:     كونه وحدة أصلية في البنية الجذرية
    farq_qadih:          حرف الجذر ليس حرف هجاء وليس حرف معنى
    preserves:           position in triconsonantal/quadriconsonantal root
    opens:               derivation candidacy
    forbids:             meaning by itself
```

### 5.5 جملة (jumla)

```text
TEXTUAL_SENTENCE         — Level 0 (any stretch of text)
    original_origin:     ما تم وأفاد في الاستعمال العام
    baʿith:              الحاجة إلى تسمية قطعة نصية ظاهرة
    wasf_muʾaththir:     كونها وحدة نصية قابلة للتقطيع
    farq_qadih:          القطعة النصية ليست بالضرورة جملة نحوية
    preserves:           surface segmentation
    opens:               parsing candidacy
    forbids:             ifādah, naḥw sentence status

NAHW_SENTENCE            — Level 1 (isnād: musnad + musnad ilayh)
    original_origin:     ما تم وأفاد في الاستعمال العام
    baʿith:              الحاجة إلى تسمية بنية الإسناد في التركيب
    wasf_muʾaththir:     وجود علاقة إسنادية بين مسند ومسند إليه
    farq_qadih:          الجملة النحوية ليست بالضرورة مفيدة (إفادة)
    preserves:           predication structure
    opens:               ifādah candidacy
    forbids:             automatic truth, real-world correspondence

IFADAH_CLOSURE           — Level 2 (closed proposition candidate)
    preserves:           dalālah closure + relation closure + maqām verdict
    opens:               hukm candidacy
    forbids:             automatic truth, reality, tanzīl without gate
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

META_TERM_ORIGIN_MISSING         — a meta-term was introduced without
                                   declaring its preserved origin.

META_TERM_BRANCH_MISSING         — a meta-term was used without
                                   declaring its transferred branch.

META_TERM_BAITH_MISSING          — a meta-term branch was opened
                                   without a valid baʿith.

META_TERM_EFFECTIVE_ATTRIBUTE_MISSING
                                 — a meta-term transfer was attempted
                                   without a wasf muʾaththir linking
                                   origin to branch.

META_TERM_DISQUALIFYING_DIFFERENCE_PRESENT
                                 — a farq qādiḥ was identified between
                                   origin and branch that prevents the
                                   transfer or its generalization.

META_TERM_SABAB_MISSING          — a meta-term was activated without
                                   a triggering cause.

META_TERM_SHART_MISSING          — a meta-term's sabab was triggered
                                   without satisfying its conditions.

META_TERM_MANI_PRESENT           — a blocker prevents the meta-term
                                   from operating despite sabab + sharṭ.

MCE_DOMAIN_LEAP                  — a minimum completeness envelope was
                                   assumed at a domain level where it
                                   does not apply.

IFTIQAR_AS_LICENSE_OVERCLAIM     — iftiqār (demand signal) was treated
                                   as a transition license.

SURFACE_LENGTH_AS_ROOT_CARDINALITY
                                 — surface letter count was confused
                                   with root consonant count.

LEXICAL_WORD_AS_DERIVATIONAL_ROOT
                                 — a two-letter lexical word was treated
                                   as a productive biliteral root.

TRACE_SCHEMA_VIOLATION           — a future runtime implementation of
                                   MetaTermContract failed to preserve
                                   the schema-level trace_ref obligations
                                   declared in §9A.
                                   (Reserved only — no runtime FailureCode
                                   is added by this covenant.)

```

Note: `MORPHOLOGICAL_PATTERN_AS_SYNTACTIC_ROLE` was withdrawn — it
duplicates `SARF_TO_NAHW_ROLE_LEAP` (same refusal: using a ṣarf
pattern to assert a naḥw role without a gate). Per §6 rule: "No PR
may introduce a different name for the same refusal."

These codes do not exist in the runtime today. They are reserved
names that future PRs (if/when meta-language enforcement becomes
operational) must use. No PR may introduce a different name for
the same refusal.

The governing rule for reserved codes:

```text
Future runtime branches may add these FailureCodes
or map them to existing codes with exact trace_ref labels.
Silent fallback is forbidden.
```

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

## 9A. Schema-level trace obligation

This covenant introduces **no runtime trace behavior**. It does not
add a `TraceEntryCandidate`, does not append to any ledger, and does
not alter the trace surface defined by PR-6/PR-6.1.

It **does** introduce a schema-level trace obligation: every
`MetaTermContract` instance (§3B field 16, `trace_ref`) must preserve
a trace reference to:

```text
1. original_origin    — the preserved origin in ordinary Arabic usage
2. transferred_branch — the declared technical branch
3. baʿith            — the motivating reason for the transfer
4. wasf_muʾaththir   — the effective attribute licensing the transfer
5. farq_qadih        — the disqualifying-difference decision
                       (either "absent — transfer may continue"
                       or "present — transfer refused")
```

Future runtime implementations that instantiate `MetaTermContract`
as a carrier or pass a meta-language term through a gate must honor
this trace obligation. A runtime PR that consumes a
`MetaTermContract` without preserving `trace_ref` is a
`TRACE_SCHEMA_VIOLATION`.

The governing sentence:

```text
لا مصطلح بلا أثر إلى أصله.
ولا أثر بلا فرع وباعث ووصف مؤثر وقرار الفرق القادح.
```

(No term without a trace to its origin. And no trace without branch,
baʿith, effective attribute, and the farq qādiḥ decision.)

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

And the extended form (ratified by this amendment):

```text
كل مصطلح لا يثبت أصله وفرعه وباعثه ووصفه المؤثر
وينفي فرقه القادح
ليس مصطلحًا دستوريًا،
بل لفظًا متشابهًا خطرًا.
```

(Any term that does not establish its origin, branch, baʿith, and
effective attribute — and negate its disqualifying difference — is not
a constitutional term, but a dangerous surface similarity.)
