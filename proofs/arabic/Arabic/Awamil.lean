import Arabic.Irab

/-!
# Arabic/Awamil.lean — مبرهنات العوامل والأدوار

كل مبرهنة هنا خاصية مبرهَنة للجدولين المعياريين `roleGovernor` و`roleCase` في `Arabic/Core.lean`.
المصدران:
- قطر الندى (`/root/NABT/src/nabt/data/source_evidence/qatr.txt`).
- ألفية ابن مالك (`/root/NABT/src/nabt/data/source_evidence/alfiyya.txt`).

قائمة الشواهد (`shawahid`) في آخر الملف تربط أسماء المبرهنات بأسطر المصدر التي عُثر عليها فعلا؛
وهي بيانات لا برهان.
-/

namespace Arabic

/-! ## لا معمول بلا عامل -/

/-- `roleGovernor` دالة تامة: لكل دور عامل واحد. -/
theorem roleGovernor_total : ∀ r : Role, ∃ g : Governor, roleGovernor r = g :=
  fun r => ⟨roleGovernor r, rfl⟩

/-- جرد الأدوار الأربعة عشر. -/
def governedRoles : List Role :=
  [ .mubtada, .khabar, .fail, .maful, .naibFail, .ismInna, .khabarInna,
    .ismKana, .khabarKana, .majrur, .mudafIlayh,
    .filMudariMarfu, .filMudariMansub, .filMudariMajzum ]

/-- الجرد تام: كل دور فيه. -/
theorem governedRoles_complete : ∀ r : Role, r ∈ governedRoles := by
  intro r; cases r <;> decide

/-- كل عامل في الجدول يعمل في دور ما (لا عامل معطّل في الجدول). -/
theorem every_governor_governs : ∀ g : Governor, ∃ r : Role, roleGovernor r = g := by
  intro g
  cases g with
  | ibtida => exact ⟨.mubtada, rfl⟩
  | mubtada => exact ⟨.khabar, rfl⟩
  | fil => exact ⟨.fail, rfl⟩
  | harfJarr => exact ⟨.majrur, rfl⟩
  | idafa => exact ⟨.mudafIlayh, rfl⟩
  | inna => exact ⟨.ismInna, rfl⟩
  | kana => exact ⟨.ismKana, rfl⟩
  | harfJazm => exact ⟨.filMudariMajzum, rfl⟩
  | harfNasb => exact ⟨.filMudariMansub, rfl⟩
  | tajarrud => exact ⟨.filMudariMarfu, rfl⟩

/-! ## الابتداء
قطر 152: «باب المبتدأ والخبر مرفوعان». ألفية 181: «ورفعوا مبتدأ بالابتدا ... كذاك رفع خبر بالمبتدا». -/

/-- كل ما عامله الابتداء أو المبتدأ مرفوع (المبتدأ بالابتداء، والخبر بالمبتدأ). -/
theorem ibtida_raf : ∀ r, roleGovernor r = .ibtida ∨ roleGovernor r = .mubtada → roleCase r = .raf := by
  intro r h
  cases r <;> first | rfl | exact absurd h (by decide)

/-- الابتداء يعمل في المبتدأ وحده، والمبتدأ يعمل في الخبر وحده (ألفية 181). -/
theorem ibtida_roles : ∀ r, (roleGovernor r = .ibtida ↔ r = .mubtada) ∧
    (roleGovernor r = .mubtada ↔ r = .khabar) := by
  intro r; cases r <;> decide

/-! ## النواسخ
قطر 171: «فيرفعن المبتدأ اسما لهن وينصبن الخبر خبرا لهن» (كان).
قطر 188–189: «فينصبن المبتدأ اسما لهن، ويرفعن الخبر خبرا لهن» (إنّ).
ألفية 210: «ترفع كان المبتدا اسما والخبر ... تنصبه»؛ ألفية 249: «لان ... كأن عكس ما لكان من عمل». -/

theorem inna_pattern : roleCase .ismInna = .nasb ∧ roleCase .khabarInna = .raf := by decide

theorem kana_pattern : roleCase .ismKana = .raf ∧ roleCase .khabarKana = .nasb := by decide

/-- إنّ وكان متعاكستان: اسم إحداهما بحالة خبر الأخرى. -/
theorem inna_kana_opposite :
    roleCase .ismInna = roleCase .khabarKana ∧
    roleCase .khabarInna = roleCase .ismKana ∧
    roleCase .ismInna ≠ roleCase .ismKana ∧
    roleCase .khabarInna ≠ roleCase .khabarKana := by decide

/-- النواسخ تحفظ حالات المبتدأ والخبر معكوسةً أو مطابقةً: كان تبقي رفع الاسم وتنصب الخبر،
وإنّ تنصب الاسم وتبقي رفع الخبر. -/
theorem nawasikh_vs_ibtida :
    roleCase .ismKana = roleCase .mubtada ∧ roleCase .khabarKana ≠ roleCase .khabar ∧
    roleCase .ismInna ≠ roleCase .mubtada ∧ roleCase .khabarInna = roleCase .khabar := by decide

/-! ## الجر والجزم -/

/-- المجرور بالحرف والمضاف إليه هما المجروران لا غير.
ألفية 482: «هاك حروف الجر»؛ ألفية 508: «والثاني اجرر». -/
theorem jarr_roles : ∀ r, roleCase r = .jarr ↔ r = .majrur ∨ r = .mudafIlayh := by
  intro r; cases r <;> decide

/-- المضارع المجزوم هو المجزوم الوحيد.
ألفية 905: «بلا ولام طالبا ضع جزما ... في الفعل هكذا بلم ولما»؛ قطر 112. -/
theorem jazm_roles : ∀ r, roleCase r = .jazm ↔ r = .filMudariMajzum := by
  intro r; cases r <;> decide

/-- الدور الاسمي لا يُجزم. -/
theorem nominal_role_not_jazm : ∀ r : Role, r.isNominal = true → roleCase r ≠ .jazm := by
  intro r h
  cases r <;> first | decide | exact absurd h (by decide)

/-- الدور الفعلي لا يُجر. -/
theorem verbal_role_not_jarr : ∀ r : Role, r.isNominal = false → roleCase r ≠ .jarr := by
  intro r h
  cases r <;> first | decide | exact absurd h (by decide)

/-- اتساق جدول الأدوار مع جدول الأصناف: الدور الاسمي تقبله الأصناف الاسمية فقط
والفعلي الأصناف الفعلية فقط، بمعنى أن حالته غير ممتنعة لصنف من نوعه. -/
theorem role_case_realizable :
    ∀ (r : Role) (cls : DeclensionClass), r.isNominal = cls.isNominal →
      caseEnding cls (roleCase r) ≠ none := by
  intro r cls h
  cases r <;> cases cls <;> first | decide | exact absurd h (by decide)

/-! ## الفعل
قطر 219: «باب الفاعل مرفوع»؛ قطر 267: «باب المفعول منصوب»؛ قطر 241 (النائب عن الفاعل).
ألفية 311؛ ألفية 331: «ينوب مفعول به عن فاعل». -/

/-- الفعل عامل واحد يرفع الفاعل ونائبه وينصب المفعول. -/
theorem fil_governs_raf_and_nasb :
    roleGovernor .fail = .fil ∧ roleCase .fail = .raf ∧
    roleGovernor .naibFail = .fil ∧ roleCase .naibFail = .raf ∧
    roleGovernor .maful = .fil ∧ roleCase .maful = .nasb := by decide

/-- معمولات الفعل ثلاثة لا غير. -/
theorem fil_roles : ∀ r, roleGovernor r = .fil ↔ r = .fail ∨ r = .maful ∨ r = .naibFail := by
  intro r; cases r <;> decide

/-- النائب عن الفاعل يأخذ حكم الفاعل في الرفع (قطر 241: «ينوب عنه في أحكامه كلها»). -/
theorem naibFail_like_fail :
    roleCase .naibFail = roleCase .fail ∧ roleGovernor .naibFail = roleGovernor .fail := by decide

/-! ## المضارع
قطر 94: «يرفع المضارع خاليا من ناصب وجازم»؛ ألفية 883–884. -/

theorem mudari_pattern :
    roleGovernor .filMudariMarfu = .tajarrud ∧ roleCase .filMudariMarfu = .raf ∧
    roleGovernor .filMudariMansub = .harfNasb ∧ roleCase .filMudariMansub = .nasb ∧
    roleGovernor .filMudariMajzum = .harfJazm ∧ roleCase .filMudariMajzum = .jazm := by decide

/-! ## الجدول الصريح -/

/-- جدول (عامل، دور، حالة) الكامل. -/
def governor_case_table : List (Governor × Role × Case) :=
  [ (.ibtida, .mubtada, .raf), (.mubtada, .khabar, .raf),
    (.fil, .fail, .raf), (.fil, .maful, .nasb), (.fil, .naibFail, .raf),
    (.inna, .ismInna, .nasb), (.inna, .khabarInna, .raf),
    (.kana, .ismKana, .raf), (.kana, .khabarKana, .nasb),
    (.harfJarr, .majrur, .jarr), (.idafa, .mudafIlayh, .jarr),
    (.tajarrud, .filMudariMarfu, .raf),
    (.harfNasb, .filMudariMansub, .nasb),
    (.harfJazm, .filMudariMajzum, .jazm) ]

/-- الجدول الصريح مطابق تماما لدالّتي `roleGovernor` و`roleCase`. -/
theorem governor_case_table_exact :
    ∀ g r c, (g, r, c) ∈ governor_case_table ↔ roleGovernor r = g ∧ roleCase r = c := by
  intro g r c
  cases g <;> cases r <;> cases c <;> decide

/-! ## ملاءمة الكلمة للدور -/

/-- الكلمة تلائم الدور إذا حققت علامتُها حالةَ الدور. -/
def fits (w : Word) (r : Role) : Bool := w.realizes (roleCase r)

theorem fits_iff : ∀ w r, fits w r = true ↔ w.realizes (roleCase r) = true :=
  fun _ _ => Iff.rfl

/-- للاسم المعرب: الملاءمة هي مطابقة العلامة لعلامة الصنف في حالة الدور. -/
theorem fits_ism_iff :
    ∀ stem cls d e r, fits (Word.mk stem (.ism cls d .aam) e) r = true ↔
      caseEnding cls (roleCase r) = some e :=
  fun stem cls d e _ =>
    ⟨caseEnding_of_realizes stem cls d _ e, realizes_of_caseEnding stem cls d _ e⟩

/-- المبني يلائم كل دور من جهة العلامة وحدها (ولذا لا تكفي العلامة؛ انظر `kindAllowsRole`). -/
theorem mabni_fits_all : ∀ w : Word, w.declClass = none → ∀ r, fits w r = true :=
  fun w h r => mabni_realizes_all w h (roleCase r)

/-- لا اسم من صنف اسمي يلائم الدور المجزوم `filMudariMajzum` (قيد الصنف لازم لأن النوع `Kind.ism`
يقبل أي صنف؛ اتساق القسم مع الصنف شأن المعجم لا الجدول). -/
theorem ism_never_fits_majzum :
    ∀ stem cls d e, cls.isNominal = true →
      fits (Word.mk stem (.ism cls d .aam) e) .filMudariMajzum = false := by
  intro stem cls d e h
  cases cls <;> first
    | exact absurd h (by decide)
    | simp [fits, Word.realizes, Word.declClass, roleCase, caseEnding]

/-- ولا مضارع من صنف فعلي يلائم دورا مجرورا. -/
theorem mudari_never_fits_jarr :
    ∀ stem cls n e r, cls.isNominal = false → roleCase r = .jarr →
      fits (Word.mk stem (.fil .mudari cls n) e) r = false := by
  intro stem cls n e r h hr
  cases cls <;> first
    | exact absurd h (by decide)
    | simp [fits, Word.realizes, Word.declClass, hr, caseEnding]

/-! ## قسم الكلمة والدور -/

/-- هل يسمح قسم الكلمة بهذا الدور؟ الأدوار الاسمية للاسم، وأدوار المضارع للمضارع،
والحرف لا يشغل دورا معمولا (الحروف عوامل لا معمولات). -/
def kindAllowsRole : Kind → Role → Bool
  | .ism _ _ _, r => r.isNominal
  | .fil .mudari _ _, r => !r.isNominal
  | .fil .madi _ _, _ => false
  | .fil .amr _ _, _ => false
  | .harf _, _ => false

theorem kindAllowsRole_ism : ∀ cls d u r, kindAllowsRole (.ism cls d u) r = r.isNominal :=
  fun _ _ _ _ => rfl

theorem kindAllowsRole_mudari : ∀ cls n r, kindAllowsRole (.fil .mudari cls n) r = !r.isNominal :=
  fun _ _ _ => rfl

/-- الحرف لا يشغل دورا. -/
theorem harf_never_role : ∀ k r, kindAllowsRole (.harf k) r = false := fun _ _ => rfl

/-- الماضي والأمر لا يشغلان دور المضارع المعرب ولا دورا اسميا. -/
theorem madi_amr_never_role :
    ∀ t cls n r, t ≠ Tense.mudari → kindAllowsRole (.fil t cls n) r = false := by
  intro t cls n r h
  cases t <;> first | rfl | exact absurd rfl h

/-- المواصفة الكاملة: القسم يسمح بالدور إذا وفقط إذا كان اسما ودورا اسميا، أو مضارعا ودورا فعليا. -/
theorem kindAllowsRole_spec :
    ∀ k r, kindAllowsRole k r = true ↔
      ((∃ cls d u, k = .ism cls d u) ∧ r.isNominal = true) ∨
      ((∃ cls n, k = .fil .mudari cls n) ∧ r.isNominal = false) := by
  intro k r
  cases k with
  | ism cls d u =>
    simp only [kindAllowsRole]
    constructor
    · intro h; exact Or.inl ⟨⟨cls, d, u, rfl⟩, h⟩
    · rintro (⟨_, h⟩ | ⟨⟨_, _, h⟩, _⟩)
      · exact h
      · cases h
  | fil t cls n =>
    cases t with
    | mudari =>
      simp only [kindAllowsRole, Bool.not_eq_true']
      constructor
      · intro h; exact Or.inr ⟨⟨cls, n, rfl⟩, h⟩
      · rintro (⟨⟨_, _, _, h⟩, _⟩ | ⟨_, h⟩)
        · cases h
        · exact h
    | madi =>
      simp only [kindAllowsRole, Bool.false_eq_true, false_iff]
      rintro (⟨⟨_, _, _, h⟩, _⟩ | ⟨⟨_, _, h⟩, _⟩) <;> cases h
    | amr =>
      simp only [kindAllowsRole, Bool.false_eq_true, false_iff]
      rintro (⟨⟨_, _, _, h⟩, _⟩ | ⟨⟨_, _, h⟩, _⟩) <;> cases h
  | harf hk =>
    simp only [kindAllowsRole, Bool.false_eq_true, false_iff]
    rintro (⟨⟨_, _, _, h⟩, _⟩ | ⟨⟨_, _, h⟩, _⟩) <;> cases h

/-- اتساق القسم مع الصنف: الاسم من صنف اسمي، والمضارع من صنف فعلي. النوع `Kind` لا يفرض ذلك،
فهو قيد معجمي يُشترط صراحةً. -/
def kindConsistent : Kind → Bool
  | .ism cls _ _ => cls.isNominal
  | .fil .mudari cls _ => !cls.isNominal
  | .fil .madi _ _ | .fil .amr _ _ | .harf _ => true

/-- القسم المتسق مع صنفه والمسموح له بالدور يضمن أن حالة الدور غير ممتنعة للصنف:
لا يقع الاسم في دور يقتضي جزما ولا المضارع في دور يقتضي جرا. -/
theorem kindAllowsRole_case_realizable :
    ∀ (stem : List Cell) (k : Kind) (e : Ending) (cls : DeclensionClass) (r : Role),
      kindConsistent k = true → kindAllowsRole k r = true →
      (Word.mk stem k e).declClass = some cls → caseEnding cls (roleCase r) ≠ none := by
  intro stem k e cls r hkc hk hd
  cases k with
  | ism cls' d u =>
    cases u with
    | damir _ => simp [Word.declClass] at hd
    | aam =>
      have hc : cls = cls' := (Option.some.inj (by simpa [Word.declClass] using hd)).symm
      subst hc
      exact role_case_realizable r cls (hk.trans hkc.symm)
    | zarf =>
      have hc : cls = cls' := (Option.some.inj (by simpa [Word.declClass] using hd)).symm
      subst hc
      exact role_case_realizable r cls (hk.trans hkc.symm)
  | fil t cls' n =>
    cases t with
    | mudari =>
      have hc : cls = cls' := (Option.some.inj hd).symm
      subst hc
      refine role_case_realizable r cls ?_
      cases n <;> cases r <;> cases cls <;>
        first | rfl | exact absurd hk (by decide) | exact absurd hkc (by decide)
    | madi => cases hd
    | amr => cases hd
  | harf hk' => cases hd

/-! ## الشواهد (بيانات لا برهان)
كل مدخل: اسم المبرهنة ↦ (ملف المصدر، رقم السطر، الاقتباس). أرقام الأسطر تحقَّق منها بـ`sed -n`
على نسخة المصادر المثبتة في NABT. هذه القائمة توثيق لمرجعية الجداول؛ البراهين أعلاه لا تعتمد عليها. -/

structure Shahid where
  source : String
  line : Nat
  quote : String
  deriving Repr, DecidableEq

def qatrPath : String := "/root/NABT/src/nabt/data/source_evidence/qatr.txt"
def alfiyyaPath : String := "/root/NABT/src/nabt/data/source_evidence/alfiyya.txt"

def shawahid : List (String × Shahid) :=
  [ ("raf_nasb_shared",
      ⟨alfiyyaPath, 70, "والرفع والنصب اجعلن اعرابا ... لاسم وفعل نحو لن أهابا"⟩),
    ("jarr_only_nominal",
      ⟨alfiyyaPath, 71, "والاسم قد خصص بالجر كما ... قد خصص الفعل بأن ينجزما"⟩),
    ("jazm_only_verbal",
      ⟨alfiyyaPath, 71, "قد خصص الفعل بأن ينجزما"⟩),
    ("asliyya_mufrad",
      ⟨alfiyyaPath, 72, "فارفع بضم وانصبن فتحا وجر ... كسرا"⟩),
    ("asliyya_mufrad",
      ⟨qatrPath, 77, "فيرفع بضمة، وينصب بفتحة،"⟩),
    ("asliyya_mudariSahih",
      ⟨alfiyyaPath, 73, "واجزم بتسكين وغير ما ذكر ... ينوب"⟩),
    ("asliyya_mudariSahih",
      ⟨qatrPath, 78, "ويجر بكسرة، ويجزم بحذف حركة،"⟩),
    ("waw_only_jamMudhakkar_or_asmaKhamsa",
      ⟨alfiyyaPath, 75, "وارفع بواو وانصبن بالألف ... واجرر بياء ما من الأسماء أصف"⟩),
    ("waw_only_jamMudhakkar_or_asmaKhamsa",
      ⟨qatrPath, 79, "فترفع بالواو وتنصب بالألف وتجر بالياء"⟩),
    ("waw_only_jamMudhakkar_or_asmaKhamsa",
      ⟨alfiyyaPath, 83, "وارفع بواو وبيا واجرر وانصب ... سالم جمع عامر ومذنب"⟩),
    ("alif_only_muthanna_or_asmaKhamsa",
      ⟨alfiyyaPath, 80, "بالألف ارفع المثنى"⟩),
    ("yaa_only_farii",
      ⟨alfiyyaPath, 82, "وتخلف اليا في جميعها الألف ... جرا ونصبا"⟩),
    ("yaa_only_farii",
      ⟨qatrPath, 83, "ويجران وينصبان بالياء"⟩),
    ("ambiguity_catalog",
      ⟨alfiyyaPath, 89, "ومابتا وألف قد جمعا ... يكسر في الجر وفي النصب معا"⟩),
    ("ambiguity_catalog",
      ⟨qatrPath, 86, "فينصب بالكسرة"⟩),
    ("ambiguity_catalog",
      ⟨alfiyyaPath, 92, "وجر بالفتحة ما لا ينصرف"⟩),
    ("ambiguity_catalog",
      ⟨qatrPath, 87, "وما لا ينصرف فيجر بالفتحة"⟩),
    ("ambiguity_catalog",
      ⟨alfiyyaPath, 94, "وحذفها للجزم والنصب سمه"⟩),
    ("nun_only_afalKhamsa",
      ⟨alfiyyaPath, 93, "واجعل لنحو يفعلان النونا ... رفعا وتدعين وتسألونا"⟩),
    ("nun_only_afalKhamsa",
      ⟨qatrPath, 89, "فترفع بثبوت النون، وتجزم"⟩),
    ("hadhfHarfIlla_only_mudariMutall_jazm",
      ⟨qatrPath, 91, "فيجزم بحذف آخره"⟩),
    ("muqaddar_only_mutall",
      ⟨qatrPath, 92, "فصل: تقدر جميع الحركات في نحو"⟩),
    ("muqaddar_only_mutall",
      ⟨alfiyyaPath, 96, "فالأول الإعراب فيه قدرا ... جميعه وهو الذي قد قصرا"⟩),
    ("mabni_realizes_all",
      ⟨qatrPath, 72, "مبنية."⟩),
    ("mabni_realizes_all",
      ⟨alfiyyaPath, 66, "وفعل أمر ومضي بنيا ... وأعربوا مضارعا إن عريا"⟩),
    ("ibtida_raf",
      ⟨qatrPath, 152, "باب المبتدأ والخبر مرفوعان"⟩),
    ("ibtida_raf",
      ⟨alfiyyaPath, 181, "ورفعوا مبتدأ بالابتدا ... كذاك رفع خبر بالمبتدا"⟩),
    ("kana_pattern",
      ⟨qatrPath, 171, "فيرفعن المبتدأ اسما لهن وينصبن الخبر خبرا لهن"⟩),
    ("kana_pattern",
      ⟨alfiyyaPath, 210, "ترفع كان المبتدا اسما والخبر ... تنصبه ككان سيدا عمر"⟩),
    ("inna_pattern",
      ⟨qatrPath, 188, "فينصبن المبتدأ اسما لهن،"⟩),
    ("inna_pattern",
      ⟨qatrPath, 189, "ويرفعن الخبر خبرا لهن"⟩),
    ("inna_kana_opposite",
      ⟨alfiyyaPath, 249, "لان أن ليت لكن لعل ... كأن عكس ما لكان من عمل"⟩),
    ("fil_governs_raf_and_nasb",
      ⟨qatrPath, 219, "باب الفاعل مرفوع"⟩),
    ("fil_governs_raf_and_nasb",
      ⟨qatrPath, 267, "باب المفعول منصوب وهو خمسة"⟩),
    ("fil_governs_raf_and_nasb",
      ⟨alfiyyaPath, 311, "الفاعل الذي كمرفوعي أتى"⟩),
    ("naibFail_like_fail",
      ⟨qatrPath, 241, "يحذف الفاعل فينوب عنه في أحكامه كلها مفعول به"⟩),
    ("naibFail_like_fail",
      ⟨alfiyyaPath, 331, "ينوب مفعول به عن فاعل ... فيما له كنيل خير نائل"⟩),
    ("jarr_roles",
      ⟨alfiyyaPath, 482, "هاك حروف الجر وهي من إلى"⟩),
    ("jarr_roles",
      ⟨alfiyyaPath, 508, "والثاني اجرر وانو من أو في إذا"⟩),
    ("jazm_roles",
      ⟨alfiyyaPath, 905, "بلا ولام طالبا ضع جزما ... في الفعل هكذا بلم ولما"⟩),
    ("jazm_roles",
      ⟨qatrPath, 112, "ويجزم أيضا بلم نحو"⟩),
    ("mudari_pattern",
      ⟨qatrPath, 96, "فصل: يرفع المضارع خاليا من ناصب وجازم نحو"⟩),
    ("mudari_pattern",
      ⟨alfiyyaPath, 883, "رفع مضارعا إذا يجرد ... من ناصب وجازم كتسعد"⟩),
    ("mudari_pattern",
      ⟨alfiyyaPath, 884, "وبلن انصبه وكي كذا بأن"⟩) ]

/-- كل اسم مبرهنة في الشواهد يشير إلى مبرهنة معرّفة أعلاه (فحص اسمي بسيط عبر `decide`). -/
def shawahidTheoremNames : List String :=
  [ "raf_nasb_shared", "jarr_only_nominal", "jazm_only_verbal", "asliyya_mufrad",
    "asliyya_mudariSahih", "waw_only_jamMudhakkar_or_asmaKhamsa",
    "alif_only_muthanna_or_asmaKhamsa", "yaa_only_farii", "ambiguity_catalog",
    "nun_only_afalKhamsa", "hadhfHarfIlla_only_mudariMutall_jazm", "muqaddar_only_mutall",
    "mabni_realizes_all", "ibtida_raf", "kana_pattern", "inna_pattern", "inna_kana_opposite",
    "fil_governs_raf_and_nasb", "naibFail_like_fail", "jarr_roles", "jazm_roles",
    "mudari_pattern" ]

theorem shawahid_names_known :
    shawahid.all (fun p => shawahidTheoremNames.contains p.1) = true := by decide

/-- كل شاهد يشير إلى أحد الملفين المصدريين. -/
theorem shawahid_sources :
    shawahid.all (fun p => p.2.source == qatrPath || p.2.source == alfiyyaPath) = true := by
  decide

end Arabic
