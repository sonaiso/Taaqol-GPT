/-
Arabic/Parse.lean — محلّل حتمي للنحو المحدود G مع براهين السلامة والتمام والوحدانية.

المصدر المعياري: قطر الندى (NABT/src/nabt/data/source_evidence/qatr.txt).
لا Mathlib؛ مكتبة Lean 4.19 القياسية فقط.

## النحو G (المعلن صراحةً)

```
Jumla  ::= ISM Khabar                       -- اسمية   (qatr.txt:152)
         | FIL_TAMM ISM                      -- فعلية بلا مفعول (qatr.txt:219–220)
         | FIL_TAMM ISM ISM                  -- فعلية بمفعول به (qatr.txt:267–268)
         | INNA ISM Khabar                   -- منسوخة بإنّ (qatr.txt:187–189)
         | KANA ISM Khabar                   -- منسوخة بكان (qatr.txt:169–171)
Khabar ::= ISM                               -- خبر مفرد
         | HARF_JARR ISM                     -- شبه جملة: جار ومجرور (qatr.txt:159–160)
         | ISM ISM                           -- شبه جملة: ظرف ومضاف إليه (qatr.txt:159)
         | FIL_TAMM ISM                      -- خبر جملة فعلية (qatr.txt:157)
         | FIL_TAMM ISM ISM                  -- خبر جملة فعلية بمفعول
```

قيود G:
* الخبر الجملة مقصور على الجملة الفعلية (عمق التضمين ≤ 1). الخبر الجملة الاسمية
  («زيد أبوه قائم») والمنسوخة مستبعدان من G في هذه الطبقة لتبقى القراءة حتمية
  بدون نظر أمامي؛ يعبّر `Jumla.inG` عن ذلك صراحةً.
* الخبر دائمًا آخر مكوّن، فيُقرأ بقية المدخل كله خبرًا.
* الحالات تُفحص بـ`Jumla.wf` بعد التعرف على الشكل؛ أول دور لا يحقق حالته يُبلَّغ
  بـ`caseMismatch (الحالة المطلوبة) (العلامة الواردة)`.
-/
import Arabic.Tarkib

namespace Arabic

/-! ## النحو G كمحمول صريح -/

/-- الخبر المسموح في G: مفرد، أو شبه جملة، أو جملة فعلية فقط. -/
def Khabar.inG : Khabar → Bool
  | .mufrad _ => true
  | .shibh _ => true
  | .jumla (.filiyya _ _ _) => true
  | .jumla _ => false

/-- الجملة المسموحة في G: أحد الأشكال الأربعة وخبرها في `Khabar.inG`. -/
def Jumla.inG : Jumla → Bool
  | .ismiyya _ k => k.inG
  | .filiyya _ _ _ => true
  | .mansukhaInna _ _ k => k.inG
  | .mansukhaKana _ _ k => k.inG

/-! ## التعرّف على الشكل (بلا فحص الحالات) -/

/-- قراءة بقية المدخل كله خبرًا. -/
def shapeKhabar (sahib : Word) : List Word → Except Refusal Khabar
  | [] => .error .noIsnad
  | [w] => if w.isIsm then .ok (.mufrad w) else .error .unsupportedStructure
  | [a, b] =>
      if a.isHarfJarr && b.isIsm then .ok (.shibh (.jarrMajrur a b))
      else if a.isZarf && b.isIsm then .ok (.shibh (.zarf a b))
      else if a.isFilTamm && b.isIsm && sahib.rabitTo b then .ok (.jumla (.filiyya a b none))
      else .error .unsupportedStructure
  | [a, b, c] =>
      if a.isFilTamm && b.isIsm && c.isIsm && (sahib.rabitTo b || sahib.rabitTo c) then
        .ok (.jumla (.filiyya a b (some c)))
      else .error .unsupportedStructure
  | _ :: _ :: _ :: _ :: _ => .error .unsupportedStructure

/-- بقية الجملة الفعلية بعد الفعل التامّ: فاعل ثم مفعول اختياري. -/
def shapeFiliyya (fil : Word) : List Word → Except Refusal Jumla
  | [] => .error .noIsnad
  | [fa] => if fa.isIsm then .ok (.filiyya fil fa none) else .error .unsupportedStructure
  | [fa, mf] =>
      if fa.isIsm && mf.isIsm then .ok (.filiyya fil fa (some mf))
      else .error .unsupportedStructure
  | _ :: _ :: _ :: _ => .error .unsupportedStructure

/-- بقية الجملة المنسوخة بعد الناسخ: اسم ثم خبر؛ `mk` هو البانية (إنّ أو كان). -/
def shapeNasikh (mk : Word → Word → Khabar → Jumla) (nasikh : Word) :
    List Word → Except Refusal Jumla
  | [] => .error .noIsnad
  | i :: rest =>
      if i.isIsm then
        match shapeKhabar i rest with
        | .ok k => .ok (mk nasikh i k)
        | .error e => .error e
      else .error .unsupportedStructure

/-- التعرف على شكل الجملة: الكلمة الأولى تحدد الشكل حتميًا. -/
def shape : List Word → Except Refusal Jumla
  | [] => .error .noIsnad
  | w :: rest =>
      if w.isIsm then
        match shapeKhabar w rest with
        | .ok k => .ok (.ismiyya w k)
        | .error e => .error e
      else if w.isFilTamm then shapeFiliyya w rest
      else if w.isNasikhInna then shapeNasikh .mansukhaInna w rest
      else if w.isKana then shapeNasikh .mansukhaKana w rest
      else .error .unsupportedStructure

/-- تشخيص جملة صحيحة الشكل فاسدة الإعراب: أول دور لا يحقق حالته. -/
def diagnose (j : Jumla) : Refusal :=
  match j.roles.find? (fun p => !p.1.realizes (roleCase p.2)) with
  | some (w, r) => .caseMismatch (roleCase r) w.ending
  | none => .unsupportedStructure

/-- المحلّل: يتعرف على الشكل ثم يفحص السلامة الإعرابية؛ يستهلك المدخل كله. -/
def parse (ws : List Word) : Except Refusal Jumla :=
  match shape ws with
  | .error e => .error e
  | .ok j => if j.wf then .ok j else .error (diagnose j)

/-! ## السلامة: ما يقبله المحلّل سليم وتسطيره هو المدخل -/

theorem shapeKhabar_linearize (sahib : Word) (ws : List Word) (k : Khabar) (h : shapeKhabar sahib ws = .ok k) :
    k.linearize = ws ∧ k.inG = true := by
  match ws with
  | [] => simp [shapeKhabar] at h
  | [w] =>
    simp [shapeKhabar] at h
    split at h
    · cases h; simp [Khabar.linearize, Khabar.inG]
    · simp at h
  | [a, b] =>
    simp [shapeKhabar] at h
    split at h
    · cases h; simp [Khabar.linearize, ShibhJumla.linearize, Khabar.inG]
    · split at h
      · cases h; simp [Khabar.linearize, ShibhJumla.linearize, Khabar.inG]
      · split at h
        · cases h; simp [Khabar.linearize, Jumla.linearize, Khabar.inG, Option.toList]
        · simp at h
  | [a, b, c] =>
    simp [shapeKhabar] at h
    split at h
    · cases h; simp [Khabar.linearize, Jumla.linearize, Khabar.inG, Option.toList]
    · simp at h
  | _ :: _ :: _ :: _ :: _ => simp [shapeKhabar] at h

theorem shapeFiliyya_linearize (fil : Word) (ws : List Word) (j : Jumla)
    (h : shapeFiliyya fil ws = .ok j) : j.linearize = fil :: ws ∧ j.inG = true := by
  match ws with
  | [] => simp [shapeFiliyya] at h
  | [fa] =>
    simp [shapeFiliyya] at h
    split at h
    · cases h; simp [Jumla.linearize, Jumla.inG, Option.toList]
    · simp at h
  | [fa, mf] =>
    simp [shapeFiliyya] at h
    split at h
    · cases h; simp [Jumla.linearize, Jumla.inG, Option.toList]
    · simp at h
  | _ :: _ :: _ :: _ => simp [shapeFiliyya] at h

theorem shapeNasikh_linearize (mk : Word → Word → Khabar → Jumla) (nasikh : Word)
    (hmk : ∀ n i k, (mk n i k).linearize = n :: i :: k.linearize ∧ (mk n i k).inG = k.inG)
    (ws : List Word) (j : Jumla) (h : shapeNasikh mk nasikh ws = .ok j) :
    j.linearize = nasikh :: ws ∧ j.inG = true := by
  match ws with
  | [] => simp [shapeNasikh] at h
  | i :: rest =>
    simp only [shapeNasikh] at h
    split at h
    · split at h
      · rename_i k hk
        have hl := shapeKhabar_linearize _ rest k hk
        cases h
        rw [(hmk nasikh i k).1, (hmk nasikh i k).2, hl.1]
        exact ⟨rfl, hl.2⟩
      · simp at h
    · simp at h

theorem shape_linearize (ws : List Word) (j : Jumla) (h : shape ws = .ok j) :
    j.linearize = ws ∧ j.inG = true := by
  match ws with
  | [] => simp [shape] at h
  | w :: rest =>
    simp only [shape] at h
    split at h
    · split at h
      · rename_i k hk
        have hl := shapeKhabar_linearize _ rest k hk
        cases h
        simp [Jumla.linearize, Jumla.inG, hl.1, hl.2]
      · simp at h
    · split at h
      · exact shapeFiliyya_linearize w rest j h
      · split at h
        · exact shapeNasikh_linearize .mansukhaInna w
            (fun _ _ _ => ⟨rfl, rfl⟩) rest j h
        · split at h
          · exact shapeNasikh_linearize .mansukhaKana w
              (fun _ _ _ => ⟨rfl, rfl⟩) rest j h
          · simp at h

/-- سلامة المحلّل: كل جملة يقبلها سليمة الإعراب وتسطيرها هو المدخل نفسه. -/
theorem parse_sound (ws : List Word) (j : Jumla) (h : parse ws = .ok j) :
    j.wf = true ∧ j.linearize = ws := by
  unfold parse at h
  split at h
  · simp at h
  · rename_i j' hj'
    have hl := shape_linearize ws j' hj'
    split at h
    · cases h
      exact ⟨by assumption, hl.1⟩
    · simp at h

/-- ما يقبله المحلّل داخل G. -/
theorem parse_inG (ws : List Word) (j : Jumla) (h : parse ws = .ok j) : j.inG = true := by
  unfold parse at h
  split at h
  · simp at h
  · rename_i j' hj'
    have hl := shape_linearize ws j' hj'
    split at h
    · cases h
      exact hl.2
    · simp at h

/-! ## التمام نسبةً إلى G: كل جملة سليمة في G يستعيدها المحلّل من تسطيرها -/

theorem shapeKhabar_complete (k : Khabar) (c : Case) (sahib : Word) (hw : k.wfWith c sahib = true)
    (hg : k.inG = true) : shapeKhabar sahib k.linearize = .ok k := by
  cases k with
  | mufrad w =>
    simp [Khabar.wfWith] at hw
    simp [Khabar.linearize, shapeKhabar, hw.1]
  | shibh s =>
    cases s with
    | jarrMajrur harf majrur =>
      simp [Khabar.wfWith, ShibhJumla.wf] at hw
      obtain ⟨⟨h1, h2⟩, _⟩ := hw
      simp [Khabar.linearize, ShibhJumla.linearize, shapeKhabar, h1, h2]
    | zarf z mi =>
      simp [Khabar.wfWith, ShibhJumla.wf] at hw
      obtain ⟨⟨⟨h1, _⟩, h3⟩, _⟩ := hw
      have hz := Word.isIsm_of_isZarf z h1
      simp [Khabar.linearize, ShibhJumla.linearize, shapeKhabar, h1, h3, hz,
        Word.isHarfJarr_eq_false_of_isIsm z hz]
  | jumla j =>
    cases j with
    | filiyya fil fail maful =>
      simp [Khabar.wfWith, Jumla.wf, Jumla.hasRabitTo] at hw
      obtain ⟨⟨⟨⟨h1, h2⟩, _⟩, h4⟩, hr⟩ := hw
      have hi := Word.isIsm_eq_false_of_isFilTamm fil h1
      have hj := Word.isHarfJarr_eq_false_of_isFilTamm fil h1
      have hz := Word.isZarf_eq_false_of_not_isIsm fil hi
      cases maful with
      | none =>
        simp [Option.any] at hr
        simp [Khabar.linearize, Jumla.linearize, Option.toList, shapeKhabar, h1, h2, hi, hj, hz, hr]
      | some m =>
        simp [wfMaful] at h4
        simp [Option.any] at hr
        simp [Khabar.linearize, Jumla.linearize, Option.toList, shapeKhabar, h1, h2, h4.1, hr]
    | ismiyya _ _ => simp [Khabar.inG] at hg
    | mansukhaInna _ _ _ => simp [Khabar.inG] at hg
    | mansukhaKana _ _ _ => simp [Khabar.inG] at hg

theorem shape_complete (j : Jumla) (hw : j.wf = true) (hg : j.inG = true) :
    shape j.linearize = .ok j := by
  cases j with
  | ismiyya mubtada khabar =>
    simp [Jumla.wf] at hw
    obtain ⟨⟨h1, _⟩, h3⟩ := hw
    simp [Jumla.inG] at hg
    simp [Jumla.linearize, shape, h1, shapeKhabar_complete khabar .raf mubtada h3 hg]
  | filiyya fil fail maful =>
    simp [Jumla.wf] at hw
    obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := hw
    have hi := Word.isIsm_eq_false_of_isFilTamm fil h1
    cases maful with
    | none => simp [Jumla.linearize, Option.toList, shape, shapeFiliyya, h1, h2, hi]
    | some m =>
      simp [wfMaful] at h4
      simp [Jumla.linearize, Option.toList, shape, shapeFiliyya, h1, h2, h4.1, hi]
  | mansukhaInna harf ism khabar =>
    simp [Jumla.wf] at hw
    obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := hw
    simp [Jumla.inG] at hg
    simp [Jumla.linearize, shape, shapeNasikh, h1, h2, Word.isIsm_eq_false_of_isNasikhInna harf h1,
      Word.isFilTamm_eq_false_of_isNasikhInna harf h1, shapeKhabar_complete khabar .raf ism h4 hg]
  | mansukhaKana kana ism khabar =>
    simp [Jumla.wf] at hw
    obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := hw
    simp [Jumla.inG] at hg
    simp [Jumla.linearize, shape, shapeNasikh, h1, h2, Word.isIsm_eq_false_of_isKana kana h1,
      Word.isFilTamm_eq_false_of_isKana kana h1, Word.isNasikhInna_eq_false_of_isKana kana h1,
      shapeKhabar_complete khabar .nasb ism h4 hg]

/-- التمام نسبةً إلى G: كل جملة سليمة في G يعيد المحلّل بناءها من تسطيرها. -/
theorem parse_complete (j : Jumla) (hw : j.wf = true) (hg : j.inG = true) :
    parse j.linearize = .ok j := by
  simp [parse, shape_complete j hw hg, hw]

/-! ## الوحدانية -/

/-- المحلّل دالة؛ فالناتج وحيد. -/
theorem parse_unique (ws : List Word) (j₁ j₂ : Jumla)
    (h₁ : parse ws = .ok j₁) (h₂ : parse ws = .ok j₂) : j₁ = j₂ :=
  Except.ok.inj (h₁.symm.trans h₂)

/-- التسطير متباين على الجمل السليمة في G: لا جملتان سليمتان مختلفتان لهما الكلمات نفسها. -/
theorem linearize_injective_on_wf (j₁ j₂ : Jumla)
    (hw₁ : j₁.wf = true) (hw₂ : j₂.wf = true) (hg₁ : j₁.inG = true) (hg₂ : j₂.inG = true)
    (h : j₁.linearize = j₂.linearize) : j₁ = j₂ := by
  have p₁ := parse_complete j₁ hw₁ hg₁
  have p₂ := parse_complete j₂ hw₂ hg₂
  rw [h] at p₁
  exact parse_unique _ _ _ p₁ p₂

/-- المدخل الفارغ لا إسناد فيه. -/
theorem parse_refuses_empty : parse [] = .error .noIsnad := rfl

/-! ## شواهد عينية (كلمات مصغّرة: الجذع خلية واحدة أو لا شيء) -/

/-- زيدٌ -/
def zaydun : Word := ⟨[(⟨10, by decide⟩, .fatha)], .ism .mufrad .marifa .aam, .damma⟩
/-- زيدًا -/
def zaydan : Word := ⟨[(⟨10, by decide⟩, .fatha)], .ism .mufrad .marifa .aam, .fatha⟩
/-- قائمٌ -/
def qaimun : Word := ⟨[(⟨20, by decide⟩, .fatha), (⟨0, by decide⟩, .kasra)], .ism .mufrad .nakira .aam, .damma⟩
/-- قائمًا -/
def qaiman : Word := ⟨[(⟨20, by decide⟩, .fatha), (⟨0, by decide⟩, .kasra)], .ism .mufrad .nakira .aam, .fatha⟩
/-- قامَ (ماضٍ مبني؛ علامته فتحة بناء) -/
def qama : Word := ⟨[(⟨20, by decide⟩, .fatha), (⟨23, by decide⟩, .fatha)], .fil .madi .mufrad false, .fatha⟩
/-- إنّ -/
def inna : Word := ⟨[], .harf .nasikhInna, .fatha⟩
/-- كانَ -/
def kana : Word := ⟨[(⟨21, by decide⟩, .fatha)], .fil .madi .mufrad true, .fatha⟩
/-- في -/
def fi : Word := ⟨[(⟨18, by decide⟩, .kasra)], .harf .jarr, .sukun⟩
/-- فوقَ (ظرف مكان منصوب؛ السمة `NounUse.zarf` مودَعة) -/
def fawqa : Word := ⟨[(⟨19, by decide⟩, .fatha)], .ism .mufrad .nakira .zarf, .fatha⟩
/-- ضربَ -/
def daraba : Word := ⟨[(⟨14, by decide⟩, .fatha), (⟨9, by decide⟩, .fatha)], .fil .madi .mufrad false, .fatha⟩
/-- عمرٌو -/
def amrun : Word := ⟨[(⟨17, by decide⟩, .fatha), (⟨23, by decide⟩, .sukun)], .ism .mufrad .marifa .aam, .damma⟩
/-- ـهُ (ضمير مبني، رابط) -/
def hu : Word := ⟨[(⟨25, by decide⟩, .damma)], .ism .mufrad .marifa (.damir zaydun.stem), .damma⟩
/-- ـهُ عائد على عمرو (لا على زيد) -/
def huAmr : Word := ⟨[(⟨25, by decide⟩, .damma)], .ism .mufrad .marifa (.damir amrun.stem), .damma⟩
/-- الدارِ -/
def addari : Word := ⟨[(⟨7, by decide⟩, .fatha)], .ism .mufrad .marifa .aam, .kasra⟩

/-- زيدٌ قائمٌ -/
theorem witness_ismiyya :
    parse [zaydun, qaimun] = .ok (.ismiyya zaydun (.mufrad qaimun)) := rfl

/-- قامَ زيدٌ -/
theorem witness_filiyya :
    parse [qama, zaydun] = .ok (.filiyya qama zaydun none) := rfl

/-- إنّ زيدًا قائمٌ -/
theorem witness_inna :
    parse [inna, zaydan, qaimun] = .ok (.mansukhaInna inna zaydan (.mufrad qaimun)) := rfl

/-- كانَ زيدٌ قائمًا -/
theorem witness_kana :
    parse [kana, zaydun, qaiman] = .ok (.mansukhaKana kana zaydun (.mufrad qaiman)) := rfl

/-- زيدٌ في الدارِ -/
theorem witness_shibh :
    parse [zaydun, fi, addari] = .ok (.ismiyya zaydun (.shibh (.jarrMajrur fi addari))) := rfl

/-- زيدٌ فوقَ الدارِ — خبر شبه جملة ظرفية. -/
theorem witness_zarf :
    parse [zaydun, fawqa, addari] = .ok (.ismiyya zaydun (.shibh (.zarf fawqa addari))) := rfl

/-- زيدٌ قائمٌ الدارِ — اسمٌ عادي (غير ظرف) متبوع باسم لا يكوّن شبه جملة: مرفوض. -/
theorem witness_non_zarf_refused :
    parse [zaydun, qaiman, addari] = .error .unsupportedStructure := rfl

/-- زيدٌ ضربَ عمرٌو ـهُ — خبر جملة فعلية رابطها ضمير المفعول. -/
theorem witness_khabar_jumla :
    parse [zaydun, daraba, amrun, hu] =
      .ok (.ismiyya zaydun (.jumla (.filiyya daraba amrun (some hu)))) := rfl

/-- زيدٌ ضربَ عمرٌو ـهُ(عائد على عمرو) — ضمير موجود لكنه لا يعود على المبتدأ: مرفوض. -/
theorem witness_khabar_jumla_wrong_marji :
    parse [zaydun, daraba, amrun, huAmr] = .error .unsupportedStructure := rfl

/-- زيدٌ قامَ عمرٌو — خبر جملة بلا رابط: مرفوض (qatr.txt:157). -/
theorem witness_khabar_jumla_no_rabit :
    parse [zaydun, qama, amrun] = .error .unsupportedStructure := rfl

/-- إنّ زيدٌ قائمٌ — اسم إنّ مرفوع: مرفوض بمخالفة النصب. -/
theorem witness_inna_mismatch :
    parse [inna, zaydun, qaimun] = .error (.caseMismatch .nasb .damma) := rfl

/-- كانَ زيدٌ قائمٌ — خبر كان مرفوع: مرفوض بمخالفة النصب. -/
theorem witness_kana_mismatch :
    parse [kana, zaydun, qaimun] = .error (.caseMismatch .nasb .damma) := rfl

/-- زيدٌ وحده: مبتدأ بلا خبر، لا إسناد. -/
theorem witness_no_khabar : parse [zaydun] = .error .noIsnad := rfl

end Arabic
