import Arabic.Core

/-!
# Arabic/Irab.lean — مبرهنات علامات الإعراب وأصناف الإعراب

كل مبرهنة هنا خاصية مبرهَنة للجدول المعياري `caseEnding` في `Arabic/Core.lean`، لا تعريفٌ جديد.
المصدران:
- قطر الندى (`/root/NABT/src/nabt/data/source_evidence/qatr.txt`) باب الإعراب، الأسطر 75–92.
- ألفية ابن مالك (`/root/NABT/src/nabt/data/source_evidence/alfiyya.txt`) الأسطر 70–100.

الأسطر المستشهد بها مذكورة في تعليق كل مبرهنة؛ القائمة التفصيلية للشواهد في `Arabic/Awamil.lean`.
لا Mathlib؛ البراهين بالتفريع على الأصناف والحالات ثم `decide`/`rfl`.
-/

namespace Arabic

/-! ## اختصاص الجر بالأسماء والجزم بالأفعال
ألفية 71: «والاسم قد خصص بالجر كما ... قد خصص الفعل بأن ينجزما».
قطر 76–77: «وجر في اسم ... وجزم نحو لم يقم». -/

/-- الجر مختص بالأسماء: كل صنف له علامة جر فهو صنف اسمي. -/
theorem jarr_only_nominal :
    ∀ cls : DeclensionClass, caseEnding cls .jarr ≠ none → cls.isNominal = true := by
  intro cls h
  cases cls <;> first | rfl | exact absurd rfl h

/-- الجزم مختص بالأفعال: كل صنف له علامة جزم فهو صنف فعلي. -/
theorem jazm_only_verbal :
    ∀ cls : DeclensionClass, caseEnding cls .jazm ≠ none → cls.isNominal = false := by
  intro cls h
  cases cls <;> first | rfl | exact absurd rfl h

/-- الصنف الاسمي لا يُجزم. -/
theorem nominal_no_jazm :
    ∀ cls : DeclensionClass, cls.isNominal = true → caseEnding cls .jazm = none := by
  intro cls h
  cases cls <;> first | rfl | exact absurd h (by decide)

/-- الصنف الفعلي لا يُجر. -/
theorem verbal_no_jarr :
    ∀ cls : DeclensionClass, cls.isNominal = false → caseEnding cls .jarr = none := by
  intro cls h
  cases cls <;> first | rfl | exact absurd h (by decide)

/-- الرفع والنصب مشتركان بين الأسماء والأفعال: لكل صنف علامة رفع وعلامة نصب.
ألفية 70: «والرفع والنصب اجعلن اعرابا ... لاسم وفعل نحو لن أهابا». -/
theorem raf_nasb_shared :
    ∀ cls : DeclensionClass, caseEnding cls .raf ≠ none ∧ caseEnding cls .nasb ≠ none := by
  intro cls
  cases cls <;> exact ⟨by decide, by decide⟩

/-! ## العلامات الأصلية
ألفية 72–73: «فارفع بضم وانصبن فتحا وجر ... كسرا ... واجزم بتسكين».
قطر 77–78: «فيرفع بضمة، وينصب بفتحة، ويجر بكسرة، ويجزم بحذف حركة». -/

/-- الاسم المفرد يأخذ العلامات الأصلية الثلاث للأسماء، ولا جزم له. -/
theorem asliyya_mufrad :
    caseEnding .mufrad .raf = some .damma ∧
    caseEnding .mufrad .nasb = some .fatha ∧
    caseEnding .mufrad .jarr = some .kasra ∧
    caseEnding .mufrad .jazm = none := by decide

/-- المضارع صحيح الآخر يأخذ الضمة والفتحة والسكون، ولا جر له. -/
theorem asliyya_mudariSahih :
    caseEnding .mudariSahih .raf = some .damma ∧
    caseEnding .mudariSahih .nasb = some .fatha ∧
    caseEnding .mudariSahih .jarr = none ∧
    caseEnding .mudariSahih .jazm = some .sukun := by decide

/-- العلامات الأصلية الأربع لا تظهر إلا في مواضعها: الضمة للرفع، الفتحة للنصب،
الكسرة للجر أو لنصب جمع المؤنث (قطر 86)، والسكون لجزم المضارع الصحيح فقط. -/
theorem damma_only_raf :
    ∀ cls c, caseEnding cls c = some .damma → c = .raf := by
  intro cls c h
  cases cls <;> cases c <;> first | rfl | exact absurd h (by decide)

theorem sukun_only_mudariSahih_jazm :
    ∀ cls c, caseEnding cls c = some .sukun → cls = .mudariSahih ∧ c = .jazm := by
  intro cls c h
  cases cls <;> cases c <;> first | exact ⟨rfl, rfl⟩ | exact absurd h (by decide)

/-! ## العلامات النائبة (الفرعية)
ألفية 73: «وغير ما ذكر ينوب». قطر 78–91. -/

/-- الواو نائبة عن الضمة في جمع المذكر السالم والأسماء الخمسة فقط.
ألفية 75: «وارفع بواو وانصبن بالألف ... واجرر بياء ما من الأسماء أصف»؛ ألفية 83. -/
theorem waw_only_jamMudhakkar_or_asmaKhamsa :
    ∀ cls c, caseEnding cls c = some .waw → cls = .jamMudhakkar ∨ cls = .asmaKhamsa := by
  intro cls c h
  cases cls <;> cases c <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

/-- الواو لا تكون إلا علامة رفع. -/
theorem waw_only_raf : ∀ cls c, caseEnding cls c = some .waw → c = .raf := by
  intro cls c h
  cases cls <;> cases c <;> first | rfl | exact absurd h (by decide)

/-- الألف نائبة في المثنى (رفعا) والأسماء الخمسة (نصبا) فقط.
ألفية 80: «بالألف ارفع المثنى»؛ قطر 82. -/
theorem alif_only_muthanna_or_asmaKhamsa :
    ∀ cls c, caseEnding cls c = some .alif → cls = .muthanna ∨ cls = .asmaKhamsa := by
  intro cls c h
  cases cls <;> cases c <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

/-- الياء نائبة في المثنى وجمع المذكر السالم والأسماء الخمسة فقط، ولا تكون علامة رفع.
ألفية 82: «وتخلف اليا في جميعها الألف ... جرا ونصبا»؛ قطر 83: «ويجران وينصبان بالياء». -/
theorem yaa_only_farii :
    ∀ cls c, caseEnding cls c = some .yaa →
      (cls = .muthanna ∨ cls = .jamMudhakkar ∨ cls = .asmaKhamsa) ∧ c ≠ .raf := by
  intro cls c h
  cases cls <;> cases c <;>
    first
    | exact ⟨Or.inl rfl, by decide⟩
    | exact ⟨Or.inr (Or.inl rfl), by decide⟩
    | exact ⟨Or.inr (Or.inr rfl), by decide⟩
    | exact absurd h (by decide)

/-- ثبوت النون وحذفها خاصان بالأفعال الخمسة.
ألفية 93–94: «واجعل لنحو يفعلان النونا رفعا ... وحذفها للجزم والنصب سمه»؛ قطر 88–89. -/
theorem nun_only_afalKhamsa :
    ∀ cls c e, caseEnding cls c = some e → (e = .thubutNun ∨ e = .hadhfNun) →
      cls = .afalKhamsa := by
  intro cls c e h he
  cases cls <;> cases c <;> cases e <;>
    first
    | rfl
    | exact absurd h (by decide)
    | exact absurd he (by decide)

/-- حذف حرف العلة خاص بجزم المضارع المعتل الآخر.
قطر 90–91: «والفعل المضارع المعتل الآخر فيجزم بحذف آخره»؛ ألفية 100. -/
theorem hadhfHarfIlla_only_mudariMutall_jazm :
    ∀ cls c, caseEnding cls c = some .hadhfHarfIlla →
      (cls = .mudariMutallAlif ∨ cls = .mudariMutallWawYaa) ∧ c = .jazm := by
  intro cls c h
  cases cls <;> cases c <;>
    first | exact ⟨Or.inl rfl, rfl⟩ | exact ⟨Or.inr rfl, rfl⟩ | exact absurd h (by decide)

/-- العلامة المقدّرة لا تظهر إلا في: المقصور (كلها)، المنقوص (رفعًا وجرًّا)، المضارع المعتل
بالألف (رفعًا ونصبًا)، المضارع المعتل بالواو/الياء (رفعًا فقط).
قطر 92–94: «تقدر جميع الحركات في نحو غلامي والفتى ... والضمة في نحو يدعو ويقضي. وتظهر الفتحة
في نحو إن القاضي لن يقضي ولن يدعو». -/
theorem muqaddar_only_mutall :
    ∀ cls c, caseEnding cls c = some .muqaddar →
      cls = .maqsur ∨ (cls = .manqus ∧ c ≠ .nasb) ∨
      (cls = .mudariMutallAlif ∧ c ≠ .jazm) ∨ (cls = .mudariMutallWawYaa ∧ c = .raf) := by
  intro cls c h
  cases cls <;> cases c <;> simp_all [caseEnding]

/-- المنقوص: الفتحة ظاهرة في النصب (قطر 94: «وتظهر الفتحة في نحو إن القاضي»). -/
theorem manqus_nasb_visible : caseEnding .manqus .nasb = some .fatha := rfl

/-- المقصور: كل الحركات مقدّرة (ألفية 96). -/
theorem maqsur_all_muqaddar : ∀ c, c ≠ .jazm → caseEnding .maqsur c = some .muqaddar := by
  intro c h; cases c <;> first | rfl | exact absurd rfl h

/-- المعتل بالواو/الياء: النصب ظاهر بالفتحة (قطر 94: «لن يقضي ولن يدعو»). -/
theorem mutall_waw_yaa_nasb_visible : caseEnding .mudariMutallWawYaa .nasb = some .fatha := rfl

/-! ## التباس العلامة: متى لا تكفي العلامة الظاهرة لتعيين الحالة؟
هذا هو التصريح الأمين بأن العلامة وحدها لا تعيّن الحالة دائما؛ العامل هو الذي يعيّنها
(`Arabic/Awamil.lean`). -/

/-- حالتان مختلفتان لصنف واحد تتفقان في علامة ظاهرة (غير ممتنعة). -/
def Ambiguous (cls : DeclensionClass) (c₁ c₂ : Case) : Prop :=
  c₁ ≠ c₂ ∧ caseEnding cls c₁ = caseEnding cls c₂ ∧ caseEnding cls c₁ ≠ none

instance (cls : DeclensionClass) (c₁ c₂ : Case) : Decidable (Ambiguous cls c₁ c₂) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

/-- فهرس الالتباسات الكامل (بالترتيبين):
- جمع المؤنث السالم: نصب = جر بالكسرة (قطر 86؛ ألفية 89).
- الممنوع من الصرف: نصب = جر بالفتحة (قطر 87؛ ألفية 92).
- المثنى وجمع المذكر السالم: نصب = جر بالياء (قطر 83؛ ألفية 82–83).
- الأفعال الخمسة: نصب = جزم بحذف النون (قطر 88–89؛ ألفية 94).
- المقصور: الحالات الثلاث كلها مقدّرة (قطر 92؛ ألفية 96).
- المنقوص: الرفع = الجر مقدّرًا؛ النصب ظاهر فلا يلتبس (قطر 94).
- المضارع المعتل بالألف: الرفع = النصب مقدّرًا.
- المضارع المعتل بالواو/الياء: لا التباس (الرفع مقدّر، النصب فتحة، الجزم حذف). -/
def ambiguousTriples : List (DeclensionClass × Case × Case) :=
  [ (.jamMuannath, .nasb, .jarr), (.jamMuannath, .jarr, .nasb),
    (.mamnu, .nasb, .jarr), (.mamnu, .jarr, .nasb),
    (.muthanna, .nasb, .jarr), (.muthanna, .jarr, .nasb),
    (.jamMudhakkar, .nasb, .jarr), (.jamMudhakkar, .jarr, .nasb),
    (.afalKhamsa, .nasb, .jazm), (.afalKhamsa, .jazm, .nasb),
    (.maqsur, .raf, .nasb), (.maqsur, .nasb, .raf),
    (.maqsur, .raf, .jarr), (.maqsur, .jarr, .raf),
    (.maqsur, .nasb, .jarr), (.maqsur, .jarr, .nasb),
    (.manqus, .raf, .jarr), (.manqus, .jarr, .raf),
    (.mudariMutallAlif, .raf, .nasb), (.mudariMutallAlif, .nasb, .raf) ]

/-- الفهرس تام وصحيح: الالتباس يقع إذا وفقط إذا كانت الثلاثية في `ambiguousTriples`. -/
theorem ambiguity_catalog :
    ∀ cls c₁ c₂, Ambiguous cls c₁ c₂ ↔ (cls, c₁, c₂) ∈ ambiguousTriples := by
  intro cls c₁ c₂
  cases cls <;> cases c₁ <;> cases c₂ <;> decide

/-- خارج الفهرس، العلامة تعيّن الحالة داخل الصنف:
إن اتفقت حالتان في علامة ظاهرة وليستا في الفهرس فهما حالة واحدة. -/
theorem ending_determines_case_within_class :
    ∀ cls c₁ c₂ e, caseEnding cls c₁ = some e → caseEnding cls c₂ = some e →
      (cls, c₁, c₂) ∉ ambiguousTriples → c₁ = c₂ := by
  intro cls c₁ c₂ e h₁ h₂ hn
  refine Decidable.byContradiction fun hne => ?_
  exact hn ((ambiguity_catalog cls c₁ c₂).mp ⟨hne, h₁.trans h₂.symm, by rw [h₁]; exact nofun⟩)

/-- في المفرد والمضارع الصحيح والأسماء الخمسة لا التباس البتة. -/
theorem no_ambiguity_asliyya_and_asmaKhamsa :
    ∀ c₁ c₂, ¬ Ambiguous .mufrad c₁ c₂ ∧ ¬ Ambiguous .mudariSahih c₁ c₂ ∧
      ¬ Ambiguous .asmaKhamsa c₁ c₂ := by
  intro c₁ c₂
  cases c₁ <;> cases c₂ <;> decide

/-! ## من الجدول إلى الكلمة: `Word.realizes` -/

/-- إن كانت علامة الصنف في الحالة `c` هي `e`، فالاسم من هذا الصنف المختوم بـ`e` يحقق `c`. -/
theorem realizes_of_caseEnding :
    ∀ (stem : List Cell) (cls : DeclensionClass) (d : Definiteness) (c : Case) (e : Ending),
      caseEnding cls c = some e → (Word.mk stem (.ism cls d .aam) e).realizes c = true := by
  intro stem cls d c e h
  simp [Word.realizes, Word.declClass, h]

/-- العكس: إن حقق الاسم الحالة `c` فعلامته هي علامة صنفه في `c`. -/
theorem caseEnding_of_realizes :
    ∀ (stem : List Cell) (cls : DeclensionClass) (d : Definiteness) (c : Case) (e : Ending),
      (Word.mk stem (.ism cls d .aam) e).realizes c = true → caseEnding cls c = some e := by
  intro stem cls d c e h
  simpa [Word.realizes, Word.declClass] using h

/-- المثل للمضارع (المعرب): `Word.declClass` يعيد صنفه، فيسري عليه الجدول. -/
theorem realizes_mudari_iff :
    ∀ (stem : List Cell) (cls : DeclensionClass) (n : Bool) (c : Case) (e : Ending),
      (Word.mk stem (.fil .mudari cls n) e).realizes c = true ↔ caseEnding cls c = some e := by
  intro stem cls n c e
  simp [Word.realizes, Word.declClass]

/-- المبني لا تتغير صورته: كل كلمة بلا صنف إعرابي تحقق كل حالة.
قطر 72: «وجميع الحروف مبنية»؛ ألفية 66: «وفعل أمر ومضي بنيا». -/
theorem mabni_realizes_all :
    ∀ w : Word, w.declClass = none → ∀ c : Case, w.realizes c = true := by
  intro w h c
  simp [Word.realizes, h]

/-- الحروف والماضي والأمر مبنية بالتعريف. -/
theorem harf_mabni : ∀ stem k e, (Word.mk stem (.harf k) e).declClass = none := by
  intro stem k e; rfl

theorem madi_amr_mabni :
    ∀ stem t cls n e, t ≠ Tense.mudari → (Word.mk stem (.fil t cls n) e).declClass = none := by
  intro stem t cls n e h
  cases t <;> first | rfl | exact absurd rfl h

/-- المعرب (اسم أو مضارع) يحقق حالة واحدة على الأقل لا تتجاوز علامته صنفه:
إن حقق حالة `c` فعلامته ليست ممتنعة لصنفه في `c`. -/
theorem realizes_implies_ending_allowed :
    ∀ (w : Word) (cls : DeclensionClass) (c : Case),
      w.declClass = some cls → w.realizes c = true → caseEnding cls c = some w.ending := by
  intro w cls c hd hr
  simpa [Word.realizes, hd] using hr

end Arabic
