/-
Arabic/Mafhum.lean — المنطوق والمفهوم.

المنطوق يُستخرج من بنية الجملة (الإسناد). المفهوم لا يُستنتج بالذكاء بل
يُرخَّص بشروط: مفهوم المخالفة يحتاج قيدًا معتبرًا وغياب المانع، ومفهوم الموافقة
يحتاج أولوية أو مساواة مودَعة. المرجع النموذجي: Mashru/Jisr/MantuqMafhum.lean
(مع الفرق أن المنطوق هنا يُشتق من `Jumla` لا يُودَع).
-/
import Arabic.Core

namespace Arabic

/-! ## المنطوق -/

/-- المحمول: الخبر مفردًا أو جملة أو شبه جملة. -/
inductive Mahmul where
  | word (w : Word)
  | jumla (j : Jumla)
  | shibh (s : ShibhJumla)

/-- الزمن/الكيف المستفاد من الناسخ أو الفعل. -/
inductive Nisba where
  | ithbat            -- إسناد مجرد (جملة اسمية)
  | hadath (t : Tense) -- حدث فعلي
  | taukid            -- إنّ
  | kawnMadi          -- كان

/-- المنطوق: مسند إليه + محمول + نسبة. -/
structure Mantuq where
  mawdu : Word
  mahmul : Mahmul
  nisba : Nisba

def Khabar.toMahmul : Khabar → Mahmul
  | .mufrad w => .word w
  | .jumla j => .jumla j
  | .shibh s => .shibh s

/-- استخراج المنطوق من الجملة: دالة كلية على كل جملة. -/
def Jumla.mantuq : Jumla → Mantuq
  | .ismiyya m k => ⟨m, k.toMahmul, .ithbat⟩
  | .filiyya f fa _ =>
      ⟨fa, .word f, .hadath (match f.kind with | .fil t _ _ => t | _ => .madi)⟩
  | .mansukhaInna _ i k => ⟨i, k.toMahmul, .taukid⟩
  | .mansukhaKana _ i k => ⟨i, k.toMahmul, .kawnMadi⟩

theorem mantuq_total (j : Jumla) : ∃ m, j.mantuq = m := ⟨_, rfl⟩

/-- المسند إليه في المنطوق هو دائمًا كلمة واحدة من الجملة. -/
theorem mantuq_mawdu_in_jumla (j : Jumla) :
    (match j with
      | .ismiyya m _ => m
      | .filiyya _ fa _ => fa
      | .mansukhaInna _ i _ => i
      | .mansukhaKana _ i _ => i) = j.mantuq.mawdu := by
  cases j <;> rfl

/-- إنّ لا تغيّر المحمول؛ تضيف التوكيد فقط. -/
theorem inna_preserves_mahmul (h i : Word) (k : Khabar) :
    (Jumla.mansukhaInna h i k).mantuq.mahmul = (Jumla.ismiyya i k).mantuq.mahmul := rfl

theorem inna_adds_taukid (h i : Word) (k : Khabar) :
    (Jumla.mansukhaInna h i k).mantuq.nisba = .taukid := rfl

/-! ## القيود والموانع -/

/-- القيود التي يُبنى عليها مفهوم المخالفة (الصفة، الشرط، الغاية، العدد) واللقب الذي لا مفهوم له. -/
inductive Qayd where
  | sifa | shart | ghaya | adad | laqab
  deriving DecidableEq, Repr

/-- الموانع المشهورة لمفهوم المخالفة. -/
inductive Mani where
  | kharajaMakhrajGhalib   -- خرج مخرج الغالب
  | jawabSual              -- ورد جوابًا لسؤال
  | jahlMukhatab           -- الجهل بحكم المسكوت
  | taghlib                -- التغليب
  deriving DecidableEq, Repr

/-- أولوية المسكوت في مفهوم الموافقة. -/
inductive Awlawiyya where
  | awla | musawi
  deriving DecidableEq, Repr

/-- السياق المودَع للجملة: ما لا يُستنتج من البنية وحدها. -/
structure Siyaq where
  qayd : Option Qayd
  mawani : List Mani
  awlawiyya : Option Awlawiyya

inductive NawMafhum where
  | muwafaqa (a : Awlawiyya)
  | mukhalafa (q : Qayd)
  deriving DecidableEq, Repr

structure Mafhum where
  asl : Mantuq
  naw : NawMafhum

/-- القيد معتبر إذا لم يكن لقبًا. -/
def Qayd.mutabar : Qayd → Bool
  | .laqab => false
  | _ => true

/-- مفهوم المخالفة المرخَّص: قيد معتبر، ولا مانع. -/
def mukhalafaOf (s : Siyaq) (m : Mantuq) : List Mafhum :=
  match s.qayd with
  | some q => if q.mutabar && s.mawani.isEmpty then [⟨m, .mukhalafa q⟩] else []
  | none => []

def muwafaqaOf (s : Siyaq) (m : Mantuq) : List Mafhum :=
  match s.awlawiyya with
  | some a => [⟨m, .muwafaqa a⟩]
  | none => []

/-- جسر المنطوق إلى المفهوم. -/
def mafahim (s : Siyaq) (j : Jumla) : List Mafhum :=
  muwafaqaOf s j.mantuq ++ mukhalafaOf s j.mantuq

/-! ## المبرهنات -/

theorem mem_mukhalafaOf {s : Siyaq} {m : Mantuq} {f : Mafhum} (h : f ∈ mukhalafaOf s m) :
    ∃ q, s.qayd = some q ∧ q.mutabar = true ∧ s.mawani = [] ∧ f = ⟨m, .mukhalafa q⟩ := by
  unfold mukhalafaOf at h
  split at h
  · rename_i q hq
    split at h
    · rename_i hc
      simp at h
      have hc' := hc
      simp [Bool.and_eq_true, List.isEmpty_iff] at hc'
      exact ⟨q, hq, hc'.1, hc'.2, h⟩
    · simp at h
  · simp at h

theorem mem_muwafaqaOf {s : Siyaq} {m : Mantuq} {f : Mafhum} (h : f ∈ muwafaqaOf s m) :
    ∃ a, s.awlawiyya = some a ∧ f = ⟨m, .muwafaqa a⟩ := by
  unfold muwafaqaOf at h
  split at h
  · rename_i a ha; simp at h; exact ⟨a, ha, h⟩
  · simp at h

/-- كل مفهوم أصله منطوق الجملة نفسها: لا مفهوم بلا منطوق. -/
theorem mafhum_min_mantuq {s : Siyaq} {j : Jumla} {f : Mafhum} (h : f ∈ mafahim s j) :
    f.asl = j.mantuq := by
  unfold mafahim at h
  rcases List.mem_append.mp h with h | h
  · obtain ⟨_, _, rfl⟩ := mem_muwafaqaOf h; rfl
  · obtain ⟨_, _, _, _, rfl⟩ := mem_mukhalafaOf h; rfl

/-- مفهوم المخالفة يقتضي قيدًا معتبرًا. -/
theorem mukhalafa_min_qayd {s : Siyaq} {j : Jumla} {q : Qayd}
    (h : (⟨j.mantuq, .mukhalafa q⟩ : Mafhum) ∈ mafahim s j) :
    s.qayd = some q ∧ q.mutabar = true := by
  unfold mafahim at h
  rcases List.mem_append.mp h with h | h
  · obtain ⟨_, _, hf⟩ := mem_muwafaqaOf h; cases hf
  · obtain ⟨q', hq, hm, _, hf⟩ := mem_mukhalafaOf h
    cases hf; exact ⟨hq, hm⟩

/-- المانع يمنع مفهوم المخالفة. -/
theorem mani_yamna_mukhalafa (s : Siyaq) (m : Mantuq) (h : s.mawani ≠ []) :
    mukhalafaOf s m = [] := by
  unfold mukhalafaOf
  split
  · have : s.mawani.isEmpty = false := by
      cases hm : s.mawani with
      | nil => exact absurd hm h
      | cons _ _ => rfl
    simp [this]
  · rfl

/-- مفهوم اللقب لا يُعتبر. -/
theorem laqab_la_mukhalafa (s : Siyaq) (m : Mantuq) (h : s.qayd = some .laqab) :
    mukhalafaOf s m = [] := by
  unfold mukhalafaOf; rw [h]; rfl

/-- لا مفهوم موافقة بلا أولوية مودَعة. -/
theorem muwafaqa_min_awlawiyya {s : Siyaq} {j : Jumla} {a : Awlawiyya}
    (h : (⟨j.mantuq, .muwafaqa a⟩ : Mafhum) ∈ mafahim s j) : s.awlawiyya = some a := by
  unfold mafahim at h
  rcases List.mem_append.mp h with h | h
  · obtain ⟨a', ha, hf⟩ := mem_muwafaqaOf h; cases hf; exact ha
  · obtain ⟨_, _, _, _, hf⟩ := mem_mukhalafaOf h; cases hf

/-- لكل جملة مفهوم مخالفة واحد على الأكثر. -/
theorem mukhalafa_wahida (s : Siyaq) (m : Mantuq) : (mukhalafaOf s m).length ≤ 1 := by
  unfold mukhalafaOf; split <;> (try split) <;> simp

/-- عدد المفاهيم محدود باثنين. -/
theorem adad_mafahim (s : Siyaq) (j : Jumla) : (mafahim s j).length ≤ 2 := by
  unfold mafahim muwafaqaOf
  have := mukhalafa_wahida s j.mantuq
  split <;> simp <;> omega

/-- سياق خالٍ: لا مفهوم أصلًا، والمنطوق وحده يبقى. -/
theorem siyaq_farigh_la_mafhum (j : Jumla) : mafahim ⟨none, [], none⟩ j = [] := rfl

/-! ## الاستدلال المشروط (شهادة صريحة) -/

/-- قضية ذرّية: إسناد محمول إلى موضوع (مُرمَّزان بأرقام من المعجم). -/
structure Qadiyya where
  mawdu : Nat
  mahmul : Nat
  deriving DecidableEq, Repr

/-- قاعدة هورن: مقدمات ← نتيجة. -/
structure Qaida where
  muqaddimat : List Qadiyya
  natija : Qadiyya

/-- شهادة استدلال: سلسلة خطوات كل منها قاعدة وُجدت مقدماتها في المعلوم. -/
def istidlal (maluum : List Qadiyya) : List Qaida → Option (List Qadiyya)
  | [] => some maluum
  | r :: rs =>
      if r.muqaddimat.all (fun p => maluum.contains p) then istidlal (r.natija :: maluum) rs
      else none

/-- سلامة الاستدلال: كل نتيجة إمّا من المعلوم أو نتيجة قاعدة وُجدت مقدماتها. -/
theorem istidlal_sound (maluum : List Qadiyya) (rs : List Qaida) (out : List Qadiyya)
    (h : istidlal maluum rs = some out) :
    ∀ q ∈ out, q ∈ maluum ∨ ∃ r ∈ rs, r.natija = q := by
  induction rs generalizing maluum with
  | nil =>
    simp [istidlal] at h; subst h
    intro q hq; exact Or.inl hq
  | cons r rs ih =>
    simp only [istidlal] at h
    split at h
    · intro q hq
      rcases ih _ h q hq with hm | ⟨r', hr', hn⟩
      · rcases List.mem_cons.mp hm with rfl | hm
        · exact Or.inr ⟨r, List.mem_cons_self .., rfl⟩
        · exact Or.inl hm
      · exact Or.inr ⟨r', List.mem_cons_of_mem _ hr', hn⟩
    · cases h

/-- الاشتقاق الاستقرائي: القضية مشتقّة إن كانت معلومة، أو نتيجةَ قاعدةٍ من المجموعة
كلُّ مقدماتها مشتقّة. هذا هو المعيار الذي تُقاس عليه الشهادة الحسابية. -/
inductive Derivable (maluum : List Qadiyya) (rs : List Qaida) : Qadiyya → Prop
  | base {q} : q ∈ maluum → Derivable maluum rs q
  | step {r} : r ∈ rs → (∀ p ∈ r.muqaddimat, Derivable maluum rs p) → Derivable maluum rs r.natija

theorem Derivable.mono_rules {maluum : List Qadiyya} {rs rs' : List Qaida}
    (hsub : ∀ r ∈ rs, r ∈ rs') {q : Qadiyya} (h : Derivable maluum rs q) : Derivable maluum rs' q := by
  induction h with
  | base hq => exact .base hq
  | step hr _ ih => exact .step (hsub _ hr) ih

/-- نقل الاشتقاق: ما اشتُقّ من معلومٍ موسَّع بقواعد أقل، مشتقّ من المعلوم الأصلي بالقواعد الأكثر،
متى كان كل عنصر في المعلوم الموسَّع مشتقًّا بالقواعد الأكثر. -/
theorem Derivable.transfer {m m' : List Qadiyya} {rs rs' : List Qaida}
    (hb : ∀ p ∈ m', Derivable m rs' p) (hsub : ∀ r ∈ rs, r ∈ rs')
    {q : Qadiyya} (h : Derivable m' rs q) : Derivable m rs' q := by
  induction h with
  | base hq => exact hb _ hq
  | step hr _ ih => exact .step (hsub _ hr) ih

/-- السلامة القوية: كل قضية في مخرج الشهادة مشتقّةٌ فعلًا من المعلوم بالقواعد المعطاة،
بمقدماتٍ مشتقّة هي الأخرى (لا يكفي أن تكون نتيجةَ قاعدةٍ ما). -/
theorem istidlal_derivable (maluum : List Qadiyya) (rs : List Qaida) (out : List Qadiyya)
    (h : istidlal maluum rs = some out) :
    ∀ q ∈ out, Derivable maluum rs q := by
  induction rs generalizing maluum with
  | nil =>
    simp [istidlal] at h; subst h
    intro q hq; exact .base hq
  | cons r rs ih =>
    simp only [istidlal] at h
    split at h
    · rename_i hall
      intro q hq
      have hbase : ∀ p ∈ r.natija :: maluum, Derivable maluum (r :: rs) p := by
        intro p hp
        rcases List.mem_cons.mp hp with rfl | hp
        · refine .step (List.mem_cons_self ..) ?_
          intro m hm
          have := List.all_eq_true.mp hall m hm
          exact .base (by simpa [List.contains_iff_mem] using this)
        · exact .base hp
      exact Derivable.transfer hbase (fun _ hr => List.mem_cons_of_mem _ hr) (ih _ h q hq)
    · cases h

/-- لا استدلال بمقدمة مفقودة. -/
theorem la_natija_bila_muqaddima (maluum : List Qadiyya) (r : Qaida) (rs : List Qaida)
    (p : Qadiyya) (hp : p ∈ r.muqaddimat) (hm : ¬ p ∈ maluum) :
    istidlal maluum (r :: rs) = none := by
  have : r.muqaddimat.all (fun p => maluum.contains p) = false := by
    rw [List.all_eq_false]
    exact ⟨p, hp, by simpa [List.contains_iff_mem] using hm⟩
  simp only [istidlal]
  rw [this]
  rfl

end Arabic
