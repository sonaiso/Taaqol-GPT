import Arabic.Core
import Arabic.Pipeline

/-!
# تقسيم الخانات (Slot Partition) المشتقّ من البرهان

هذا الملفّ يُعرّف **تقسيم الخانات** الذي يفرضه البرهان، لا الذي تفترضه الشيفرة:
كلّ خانة في SLGE يجب أن تنفتح على مجموعة قيم مرخّصة (`allowed_potentials`)،
وهنا نُعدّد هذه المجموعات تعدادًا تامًّا ونُبرهن أنّها:

* **تامّة** (`*_complete`): كلّ قيمة يسمح بها النوع في البرهان موجودة في التعداد؛
* **بلا تكرار** (`*_nodup`): التعداد تقسيمٌ لا قائمة مرشّحين؛
* **مُقسَّمة بالعوامل**: جدول العلامات `caseEnding` يقسم الأصناف إلى اسميّة (لا جزم)
  وفعليّة (لا جرّ) بلا تداخل (`nominal_no_jazm`, `verbal_no_jarr`, `ending_partition`).

ثم تُصدَّر البيانات بياناتٍ (`manifest`) ليبني `check_slots.py` منها خانات SLGE
الفعليّة (`taaqqul_slot_geometry.core.slot_graph`) ويتحقّق أنّ كلّ توفيقٍ يرخّصه البرهان
تقبله الخانة، وكلّ ما يرفضه البرهان ترفضه الخانة.
-/

namespace Arabic.Slots

/-! ## التعدادات -/

def allMarks : List Mark := [.fatha, .damma, .kasra, .sukun]
def allCases : List Case := [.raf, .nasb, .jarr, .jazm]
def allEndings : List Ending :=
  [.damma, .fatha, .kasra, .sukun, .waw, .alif, .yaa, .thubutNun, .hadhfNun, .hadhfHarfIlla, .muqaddar]
def allClasses : List DeclensionClass :=
  [.mufrad, .jamMuannath, .mamnu, .muthanna, .jamMudhakkar, .asmaKhamsa,
   .mudariSahih, .mudariMutallAlif, .mudariMutallWawYaa, .afalKhamsa, .maqsur, .manqus]
def allRoles : List Role :=
  [.mubtada, .khabar, .fail, .maful, .naibFail, .ismInna, .khabarInna, .ismKana, .khabarKana,
   .majrur, .mudafIlayh, .filMudariMarfu, .filMudariMansub, .filMudariMajzum]
def allGovernors : List Governor :=
  [.ibtida, .mubtada, .fil, .harfJarr, .idafa, .inna, .kana, .harfJazm, .harfNasb, .tajarrud]

def allCarriers : List Carrier := List.finRange carriers.length

/-- أبجدية الخلايا: الحوامل × الحركات (A116 = 29 × 4). -/
def cellAlphabet : List Cell := allCarriers.flatMap fun c => allMarks.map fun m => (c, m)

theorem carriers_length : carriers.length = 29 := by decide
theorem cellAlphabet_length : cellAlphabet.length = 116 := by decide

theorem allMarks_complete : ∀ m : Mark, m ∈ allMarks := by intro m; cases m <;> decide
theorem allCases_complete : ∀ c : Case, c ∈ allCases := by intro c; cases c <;> decide
theorem allEndings_complete : ∀ e : Ending, e ∈ allEndings := by intro e; cases e <;> decide
theorem allClasses_complete : ∀ d : DeclensionClass, d ∈ allClasses := by intro d; cases d <;> decide
theorem allRoles_complete : ∀ r : Role, r ∈ allRoles := by intro r; cases r <;> decide
theorem allGovernors_complete : ∀ g : Governor, g ∈ allGovernors := by intro g; cases g <;> decide

theorem allMarks_nodup : allMarks.Nodup := by decide
theorem allCases_nodup : allCases.Nodup := by decide
theorem allEndings_nodup : allEndings.Nodup := by decide
theorem allClasses_nodup : allClasses.Nodup := by decide
theorem allRoles_nodup : allRoles.Nodup := by decide
theorem allGovernors_nodup : allGovernors.Nodup := by decide
theorem cellAlphabet_nodup : cellAlphabet.Nodup := by decide

theorem cellAlphabet_complete : ∀ c : Cell, c ∈ cellAlphabet := by
  intro ⟨i, m⟩; cases m <;> (revert i; decide)

/-- خلايا العلامات الإعرابيّة جزءٌ من أبجدية الخلايا. -/
theorem endingCell_mem_alphabet : ∀ e : Ending, endingCell e ∈ cellAlphabet := by
  intro e; exact cellAlphabet_complete _

/-! ## تقسيم جدول العلامات بالعوامل -/

/-- الأصناف الاسميّة لا تُجزم. -/
theorem nominal_classes_no_jazm : ∀ d : DeclensionClass, d.isNominal = true → caseEnding d .jazm = none := by
  intro d h; cases d <;> first | rfl | simp [DeclensionClass.isNominal] at h

/-- الأصناف الفعليّة لا تُجرّ. -/
theorem verbal_classes_no_jarr : ∀ d : DeclensionClass, d.isNominal = false → caseEnding d .jarr = none := by
  intro d h; cases d <;> first | rfl | simp [DeclensionClass.isNominal] at h

/-- الرفع والنصب مشتركان بين القبيلين: لكلّ صنف علامةٌ فيهما. -/
theorem raf_nasb_total : ∀ d : DeclensionClass, (caseEnding d .raf).isSome ∧ (caseEnding d .nasb).isSome := by
  intro d; cases d <;> decide

/-- التقسيم: الحالة مرخَّصة لصنفٍ إذا وفقط إذا وافقت قبيلته (الجرّ للأسماء، الجزم للأفعال). -/
theorem ending_partition : ∀ d : DeclensionClass, ∀ c : Case,
    (caseEnding d c).isSome = true ↔
      (c = .raf ∨ c = .nasb ∨ (c = .jarr ∧ d.isNominal = true) ∨ (c = .jazm ∧ d.isNominal = false)) := by
  intro d c; cases d <;> cases c <;> decide

/-- دور الاسم يقتضي حالة اسميّة، ودور الفعل حالةً فعليّة. -/
theorem role_case_partition : ∀ r : Role,
    (r.isNominal = true → roleCase r ≠ .jazm) ∧ (r.isNominal = false → roleCase r ≠ .jarr) := by
  intro r; cases r <;> decide

/-- كلّ دور له عامل، وكلّ عامل في التعداد. -/
theorem roleGovernor_mem : ∀ r : Role, roleGovernor r ∈ allGovernors := by
  intro r; exact allGovernors_complete _

/-! ## التصدير -/

def _root_.Arabic.Mark.tag : Mark → String
  | .fatha => "fatha" | .damma => "damma" | .kasra => "kasra" | .sukun => "sukun"
def _root_.Arabic.Case.tag : Case → String
  | .raf => "raf" | .nasb => "nasb" | .jarr => "jarr" | .jazm => "jazm"
def _root_.Arabic.Ending.tag : Ending → String
  | .damma => "damma" | .fatha => "fatha" | .kasra => "kasra" | .sukun => "sukun"
  | .waw => "waw" | .alif => "alif" | .yaa => "yaa" | .thubutNun => "thubutNun"
  | .hadhfNun => "hadhfNun" | .hadhfHarfIlla => "hadhfHarfIlla" | .muqaddar => "muqaddar"
def _root_.Arabic.DeclensionClass.tag : DeclensionClass → String
  | .mufrad => "mufrad" | .jamMuannath => "jamMuannath" | .mamnu => "mamnu"
  | .muthanna => "muthanna" | .jamMudhakkar => "jamMudhakkar" | .asmaKhamsa => "asmaKhamsa"
  | .mudariSahih => "mudariSahih" | .mudariMutallAlif => "mudariMutallAlif"
  | .mudariMutallWawYaa => "mudariMutallWawYaa" | .afalKhamsa => "afalKhamsa"
  | .maqsur => "maqsur" | .manqus => "manqus"
def _root_.Arabic.Role.tag : Role → String
  | .mubtada => "mubtada" | .khabar => "khabar" | .fail => "fail" | .maful => "maful"
  | .naibFail => "naibFail" | .ismInna => "ismInna" | .khabarInna => "khabarInna"
  | .ismKana => "ismKana" | .khabarKana => "khabarKana" | .majrur => "majrur"
  | .mudafIlayh => "mudafIlayh" | .filMudariMarfu => "filMudariMarfu"
  | .filMudariMansub => "filMudariMansub" | .filMudariMajzum => "filMudariMajzum"
def _root_.Arabic.Governor.tag : Governor → String
  | .ibtida => "ibtida" | .mubtada => "mubtada" | .fil => "fil" | .harfJarr => "harfJarr"
  | .idafa => "idafa" | .inna => "inna" | .kana => "kana" | .harfJazm => "harfJazm"
  | .harfNasb => "harfNasb" | .tajarrud => "tajarrud"

/-- الوسوم حاقنة: وسمان متساويان ⇒ قيمتان متساويتان (فلا تلتبس خانتان). -/
theorem _root_.Arabic.Ending.tag_injective : ∀ a b : Ending, Ending.tag a = Ending.tag b → a = b := by
  intro a b h; cases a <;> cases b <;> first | rfl | (simp [Ending.tag] at h)
theorem _root_.Arabic.DeclensionClass.tag_injective : ∀ a b : DeclensionClass,
    DeclensionClass.tag a = DeclensionClass.tag b → a = b := by
  intro a b h; cases a <;> cases b <;> first | rfl | (simp [DeclensionClass.tag] at h)
theorem _root_.Arabic.Role.tag_injective : ∀ a b : Role, Role.tag a = Role.tag b → a = b := by
  intro a b h; cases a <;> cases b <;> first | rfl | (simp [Role.tag] at h)

private def q (s : String) : String := "\"" ++ s ++ "\""
private def arr (xs : List String) : String := "[" ++ ", ".intercalate xs ++ "]"
private def obj (kvs : List (String × String)) : String :=
  "{" ++ ", ".intercalate (kvs.map fun (k, v) => q k ++ ": " ++ v) ++ "}"

def cellJson (c : Cell) : String := obj [("carrier", toString c.1.val), ("mark", q c.2.tag)]

/-- بيان الخانات: كلّ ما تحتاجه SLGE لبناء خاناتها من البرهان لا من افتراض. -/
def manifest : String :=
  obj [
    ("carriers", arr (carriers.map fun ch => toString ch.toNat)),
    ("marks", arr (allMarks.map (q ·.tag))),
    ("cells", arr (cellAlphabet.map cellJson)),
    ("cases", arr (allCases.map (q ·.tag))),
    ("endings", arr (allEndings.map fun e => obj [("ending", q e.tag), ("cell", cellJson (endingCell e))])),
    ("classes", arr (allClasses.map fun d => obj [
        ("class", q d.tag), ("nominal", toString d.isNominal),
        ("endings", obj (allCases.map fun c =>
          (c.tag, match caseEnding d c with | some e => q e.tag | none => "null")))])),
    ("roles", arr (allRoles.map fun r => obj [
        ("role", q r.tag), ("case", q (roleCase r).tag),
        ("governor", q (roleGovernor r).tag), ("nominal", toString r.isNominal)])),
    ("governors", arr (allGovernors.map (q ·.tag))),
    ("jumla_shapes", arr (["ismiyya", "filiyya", "mansukhaInna", "mansukhaKana"].map q)),
    ("khabar_shapes", arr (["mufrad", "jumla", "shibh"].map q)),
    ("shibh_shapes", arr (["jarrMajrur", "zarf"].map q))
  ]

end Arabic.Slots
