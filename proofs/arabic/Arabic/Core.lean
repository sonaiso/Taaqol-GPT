/-
Arabic/Core.lean — الأنواع المشتركة لبرهان المسار العربي.

هذه الطبقة تعلن الأنواع فقط. كل طبقة لاحقة تبرهن على هذه الأنواع.
لا Mathlib؛ مكتبة Lean 4.19 القياسية فقط.
-/

namespace Arabic

/-! ## الخلايا (A116): حامل × حركة -/

/-- الحوامل التسعة والعشرون بترتيب A116 نفسه (مطابق لـ proofs/a116/A116.lean). -/
def carriers : List Char := "ابتثجحخدذرزسشصضطظعغفقكلمنهويء".toList

abbrev Carrier := Fin carriers.length

inductive Mark where
  | fatha | damma | kasra | sukun
  deriving DecidableEq, Repr, Inhabited

abbrev Cell := Carrier × Mark

/-! ## الإعراب -/

/-- حالات الإعراب الأربع (قطر الندى: الرفع والنصب مشتركان، الجر للأسماء، الجزم للأفعال). -/
inductive Case where
  | raf | nasb | jarr | jazm
  deriving DecidableEq, Repr, Inhabited

/-- علامة الإعراب الظاهرة في آخر الكلمة. -/
inductive Ending where
  | damma | fatha | kasra | sukun        -- العلامات الأصلية
  | waw | alif | yaa                     -- الحروف النائبة
  | thubutNun | hadhfNun                 -- الأفعال الخمسة
  | hadhfHarfIlla                        -- المعتل الآخر المجزوم
  | muqaddar                             -- مقدّرة (المقصور/المنقوص/المضاف إلى ياء المتكلم)
  deriving DecidableEq, Repr, Inhabited

/-- أصناف الإعراب في قطر الندى. -/
inductive DeclensionClass where
  | mufrad                 -- الاسم المفرد والجمع التكسير
  | jamMuannath            -- جمع المؤنث السالم
  | mamnu                  -- الممنوع من الصرف
  | muthanna               -- المثنى
  | jamMudhakkar           -- جمع المذكر السالم
  | asmaKhamsa             -- الأسماء الخمسة
  | mudariSahih            -- المضارع صحيح الآخر
  | mudariMutallAlif       -- المضارع معتل الآخر بالألف (يخشى): الرفع والنصب مقدّران
  | mudariMutallWawYaa     -- المضارع معتل الآخر بالواو/الياء (يدعو/يقضي): الرفع مقدّر والنصب ظاهر
  | afalKhamsa             -- الأفعال الخمسة
  | maqsur                 -- المقصور: الحركات الثلاث مقدّرة
  | manqus                 -- المنقوص: الضمة والكسرة مقدّرتان، الفتحة ظاهرة
  deriving DecidableEq, Repr, Inhabited

/-! ## أقسام الكلمة -/

inductive Tense where
  | madi | mudari | amr
  deriving DecidableEq, Repr, Inhabited

inductive Definiteness where
  | marifa | nakira
  deriving DecidableEq, Repr, Inhabited

/-- استعمال الاسم المودَع معجميًا: عادي، أو ظرف (زمان/مكان) يصلح لشبه الجملة. -/
inductive NounUse where
  | aam    -- اسم عامّ معرب
  | zarf   -- ظرف (يقع خبرًا شبه جملة)
  | damir (marji : List Cell)  -- ضمير: اسم مبني يحمل مرجعه (جذع ما يعود عليه)؛ الرابط في الخبر الجملة (qatr.txt:157)
  deriving DecidableEq, Repr, Inhabited

inductive HarfKind where
  | jarr          -- حرف جر
  | nasikhInna    -- إنّ وأخواتها
  | jazm          -- أدوات الجزم
  | nasbFil       -- أدوات نصب المضارع
  | atf           -- حرف عطف
  | nafy          -- حرف نفي غير عامل
  deriving DecidableEq, Repr, Inhabited

/-- السمات المعجمية المودَعة للكلمة؛ تُعطى من المصدر ولا تُستنتج. -/
inductive Kind where
  | ism (cls : DeclensionClass) (def_ : Definiteness) (use : NounUse)
  | fil (tense : Tense) (cls : DeclensionClass) (naqis : Bool)  -- naqis: كان وأخواتها
  | harf (k : HarfKind)
  deriving DecidableEq, Repr, Inhabited

/-- الكلمة: جذع من الخلايا + سمة معجمية + علامة إعراب ظاهرة. -/
structure Word where
  stem : List Cell
  kind : Kind
  ending : Ending
  deriving DecidableEq, Repr, Inhabited

/-! ## العوامل والأدوار -/

inductive Role where
  | mubtada | khabar
  | fail | maful | naibFail
  | ismInna | khabarInna
  | ismKana | khabarKana
  | majrur | mudafIlayh
  | filMudariMarfu | filMudariMansub | filMudariMajzum
  deriving DecidableEq, Repr, Inhabited

inductive Governor where
  | ibtida          -- الابتداء (عامل معنوي يرفع المبتدأ)
  | mubtada         -- المبتدأ يرفع الخبر (الألفية 181)
  | fil             -- الفعل
  | harfJarr
  | idafa
  | inna
  | kana
  | harfJazm
  | harfNasb
  | tajarrud        -- التجرد من الناصب والجازم (رفع المضارع)
  deriving DecidableEq, Repr, Inhabited


/-! ## الجداول المعيارية (قطر الندى / الألفية) — تُستعمل من كل الطبقات -/

/-- عامل كل دور (لا معمول بلا عامل). -/
def roleGovernor : Role → Governor
  | .mubtada => .ibtida
  | .khabar => .mubtada
  | .fail | .maful | .naibFail => .fil
  | .ismInna | .khabarInna => .inna
  | .ismKana | .khabarKana => .kana
  | .majrur => .harfJarr
  | .mudafIlayh => .idafa
  | .filMudariMarfu => .tajarrud
  | .filMudariMansub => .harfNasb
  | .filMudariMajzum => .harfJazm

/-- الحالة التي يقتضيها الدور. -/
def roleCase : Role → Case
  | .mubtada | .khabar | .fail | .naibFail | .khabarInna | .ismKana | .filMudariMarfu => .raf
  | .maful | .ismInna | .khabarKana | .filMudariMansub => .nasb
  | .majrur | .mudafIlayh => .jarr
  | .filMudariMajzum => .jazm

/-- هل الدور اسمي؟ (الجر مختص بالأسماء، الجزم مختص بالأفعال) -/
def Role.isNominal : Role → Bool
  | .filMudariMarfu | .filMudariMansub | .filMudariMajzum => false
  | _ => true

/-- علامة الإعراب لكل صنف وحالة (قطر الندى، باب الإعراب). `none` = الحالة ممتنعة لهذا الصنف. -/
def caseEnding : DeclensionClass → Case → Option Ending
  | .mufrad, .raf => some .damma
  | .mufrad, .nasb => some .fatha
  | .mufrad, .jarr => some .kasra
  | .mufrad, .jazm => none
  | .jamMuannath, .raf => some .damma
  | .jamMuannath, .nasb => some .kasra
  | .jamMuannath, .jarr => some .kasra
  | .jamMuannath, .jazm => none
  | .mamnu, .raf => some .damma
  | .mamnu, .nasb => some .fatha
  | .mamnu, .jarr => some .fatha
  | .mamnu, .jazm => none
  | .muthanna, .raf => some .alif
  | .muthanna, .nasb => some .yaa
  | .muthanna, .jarr => some .yaa
  | .muthanna, .jazm => none
  | .jamMudhakkar, .raf => some .waw
  | .jamMudhakkar, .nasb => some .yaa
  | .jamMudhakkar, .jarr => some .yaa
  | .jamMudhakkar, .jazm => none
  | .asmaKhamsa, .raf => some .waw
  | .asmaKhamsa, .nasb => some .alif
  | .asmaKhamsa, .jarr => some .yaa
  | .asmaKhamsa, .jazm => none
  | .maqsur, .raf => some .muqaddar
  | .maqsur, .nasb => some .muqaddar
  | .maqsur, .jarr => some .muqaddar
  | .maqsur, .jazm => none
  | .manqus, .raf => some .muqaddar
  | .manqus, .nasb => some .fatha
  | .manqus, .jarr => some .muqaddar
  | .manqus, .jazm => none
  | .mudariSahih, .raf => some .damma
  | .mudariSahih, .nasb => some .fatha
  | .mudariSahih, .jarr => none
  | .mudariSahih, .jazm => some .sukun
  | .mudariMutallAlif, .raf => some .muqaddar
  | .mudariMutallAlif, .nasb => some .muqaddar
  | .mudariMutallAlif, .jarr => none
  | .mudariMutallAlif, .jazm => some .hadhfHarfIlla
  | .mudariMutallWawYaa, .raf => some .muqaddar
  | .mudariMutallWawYaa, .nasb => some .fatha
  | .mudariMutallWawYaa, .jarr => none
  | .mudariMutallWawYaa, .jazm => some .hadhfHarfIlla
  | .afalKhamsa, .raf => some .thubutNun
  | .afalKhamsa, .nasb => some .hadhfNun
  | .afalKhamsa, .jarr => none
  | .afalKhamsa, .jazm => some .hadhfNun

/-- الصنف اسمي أم فعلي. -/
def DeclensionClass.isNominal : DeclensionClass → Bool
  | .mudariSahih | .mudariMutallAlif | .mudariMutallWawYaa | .afalKhamsa => false
  | _ => true

/-- حالة الكلمة في دور معيّن مقبولة إذا طابقت علامتها علامة صنفها. -/
def Word.declClass : Word → Option DeclensionClass
  | ⟨_, .ism _ _ (.damir _), _⟩ => none  -- الضمائر مبنية
  | ⟨_, .ism cls _ _, _⟩ => some cls
  | ⟨_, .fil .mudari cls _, _⟩ => some cls
  | ⟨_, .fil _ _ _, _⟩ => none      -- الماضي والأمر مبنيان
  | ⟨_, .harf _, _⟩ => none          -- الحروف مبنية

/-- هل علامة الكلمة تحقق الحالة المطلوبة؟ المبني يُقبل كما هو (لا محل للإعراب الظاهر). -/
def Word.realizes (w : Word) (c : Case) : Bool :=
  match w.declClass with
  | some cls => caseEnding cls c == some w.ending
  | none => true

/-! ## التراكيب -/

/-- شبه الجملة: جار ومجرور أو ظرف ومضاف إليه. -/
inductive ShibhJumla where
  | jarrMajrur (harf : Word) (majrur : Word)
  | zarf (zarf : Word) (mudafIlayh : Word)
  deriving DecidableEq, Repr, Inhabited

mutual
  /-- الخبر: مفرد، أو جملة، أو شبه جملة (قطر الندى). -/
  inductive Khabar where
    | mufrad (w : Word)
    | jumla (j : Jumla)
    | shibh (s : ShibhJumla)

  /-- الجملة: اسمية أو فعلية أو منسوخة. -/
  inductive Jumla where
    | ismiyya (mubtada : Word) (khabar : Khabar)
    | filiyya (fil : Word) (fail : Word) (maful : Option Word)
    | mansukhaInna (harf : Word) (ism : Word) (khabar : Khabar)
    | mansukhaKana (kana : Word) (ism : Word) (khabar : Khabar)
end

/-! ## الإسناد -/

/-- طرفا الإسناد: المسند والمسند إليه (كلمة أو جملة). -/
inductive Tarf where
  | word (w : Word)
  | jumla (j : Jumla)
  | shibh (s : ShibhJumla)

structure Isnad where
  musnad : Tarf
  musnadIlayh : Tarf

/-! ## أخطاء مسمّاة -/

inductive Refusal where
  | unknownByte
  | notArabicBlock
  | unknownCell
  | notInLexicon
  | caseMismatch (expected : Case) (got : Ending)
  | noIsnad
  | unsupportedStructure
  deriving DecidableEq, Repr

end Arabic
