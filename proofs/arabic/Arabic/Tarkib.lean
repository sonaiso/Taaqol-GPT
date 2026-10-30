/-
Arabic/Tarkib.lean — سلامة التراكيب، الإسناد، التسطير، والأدوار.

تعتمد على الأنواع المعلنة في `Arabic/Core.lean` ولا تعدّلها.
المصدر المعياري: قطر الندى (NABT/src/nabt/data/source_evidence/qatr.txt)؛
أرقام الأسطر المذكورة في التعليقات تشير إلى ذلك الملف.
لا Mathlib؛ مكتبة Lean 4.19 القياسية فقط.
-/
import Arabic.Core

namespace Arabic

/-! ## أصناف الكلمة (قرارات بوليانية على السمة المودَعة) -/

/-- هل الكلمة اسم؟ يشترط اتساق الصنف: الاسم من صنف اسمي (`DeclensionClass.isNominal`)،
فلا يُعدّ «اسمٌ» بصنف فعلي اسمًا سليمًا. -/
def Word.isIsm : Word → Bool
  | ⟨_, .ism cls _ _, _⟩ => cls.isNominal
  | _ => false

/-- هل الكلمة ظرف (سمة معجمية مودَعة)؟ -/
def Word.isZarf : Word → Bool
  | ⟨_, .ism cls _ .zarf, _⟩ => cls.isNominal
  | _ => false

theorem Word.isIsm_of_isZarf (w : Word) (h : w.isZarf = true) : w.isIsm = true := by
  unfold Word.isZarf at h; unfold Word.isIsm
  split at h <;> simp_all

theorem Word.isZarf_eq_false_of_not_isIsm (w : Word) (h : w.isIsm = false) : w.isZarf = false := by
  cases hz : w.isZarf
  · rfl
  · rw [Word.isIsm_of_isZarf w hz] at h; cases h

/-- هل الكلمة ضمير؟ (اسم مبني؛ رابط الخبر الجملة) -/
def Word.isDamir : Word → Bool
  | ⟨_, .ism cls _ (.damir _), _⟩ => cls.isNominal
  | _ => false

/-- الضمير رابطٌ إلى صاحبه إذا كان مرجعه جذعَ الصاحب (العود على المبتدأ بعينه). -/
def Word.rabitTo (sahib w : Word) : Bool :=
  match w with
  | ⟨_, .ism cls _ (.damir m), _⟩ => cls.isNominal && m == sahib.stem
  | _ => false

theorem Word.isDamir_of_rabitTo (sahib w : Word) (h : sahib.rabitTo w = true) : w.isDamir = true := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | ism cls d u => cases u <;> simp_all [Word.rabitTo, Word.isDamir]
  | _ => simp_all [Word.rabitTo]

theorem Word.isIsm_of_isDamir (w : Word) (h : w.isDamir = true) : w.isIsm = true := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | ism cls d u => cases u <;> simp_all [Word.isDamir, Word.isIsm]
  | _ => simp_all [Word.isDamir]

/-- الرابط: الخبر الجملة لا بدّ له من رابط يعود على المبتدأ بعينه (qatr.txt:157 «والخبر جملة لها رابط»).
نمثّله بضمير مرجعُه الصاحب في موقع الفاعل أو المفعول في الجملة الفعلية. -/
def Jumla.hasRabitTo (sahib : Word) : Jumla → Bool
  | .filiyya _ fail maful => sahib.rabitTo fail || maful.any (sahib.rabitTo ·)
  | _ => false

/-- هل الكلمة حرف جر؟ -/
def Word.isHarfJarr : Word → Bool
  | ⟨_, .harf .jarr, _⟩ => true
  | _ => false

/-- هل الكلمة فعل مضارع؟ -/
def Word.isMudari : Word → Bool
  | ⟨_, .fil .mudari cls _, _⟩ => !cls.isNominal
  | _ => false

/-- هل الكلمة من «إنّ وأخواتها»؟ (qatr.txt:187–189) -/
def Word.isNasikhInna : Word → Bool
  | ⟨_, .harf .nasikhInna, _⟩ => true
  | _ => false

/-- هل الكلمة «كان» الماضية الناقصة؟ (qatr.txt:169–171). نقتصر على الماضي لأن النسبة
المشتقّة `kawnMadi` ماضية؛ مضارع كان خارج G. -/
def Word.isKana : Word → Bool
  | ⟨_, .fil .madi _ true, _⟩ => true
  | _ => false

/-- هل الكلمة فعل تامّ؟ (غير ناقص) — فحص شكلي لتمييز القسم فقط. -/
def Word.isFilTamm : Word → Bool
  | ⟨_, .fil _ _ false, _⟩ => true
  | _ => false

/-- سلامة صيغة الفعل التامّ الواقع عاملًا في جملة فعلية لا ناصب فيها ولا جازم:
* الماضي والأمر مبنيان فيُقبلان كما هما (علامتهما علامة بناء).
* المضارع لا بدّ أن يكون صنفه فعليًا (`DeclensionClass.isNominal = false`) وأن يكون
  مرفوعًا بالتجرّد (qatr.txt:96 «يرفع المضارع خاليا من ناصب وجازم نحو "يقوم زيد"»)؛
  فالمضارع المجزوم أو المنصوب بلا عامل، والمضارع بصنف اسمي، صيغ فاسدة. -/
def Word.wfFilTamm (w : Word) : Bool :=
  match w with
  | ⟨_, .fil .mudari cls false, _⟩ => !cls.isNominal && w.realizes .raf
  | ⟨_, .fil _ _ false, _⟩ => true
  | _ => false

theorem Word.isFilTamm_of_wfFilTamm (w : Word) (h : w.wfFilTamm = true) : w.isFilTamm = true := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil t _ n => cases t <;> cases n <;> simp_all [Word.wfFilTamm, Word.isFilTamm]
  | _ => simp_all [Word.wfFilTamm]

/-- المضارع التامّ سليم الصيغة إذا وفقط إذا كان صنفه فعليًا ومرفوعًا. -/
theorem Word.wfFilTamm_mudari (stem : List Cell) (cls : DeclensionClass) (e : Ending) :
    (Word.mk stem (.fil .mudari cls false) e).wfFilTamm = true ↔
      cls.isNominal = false ∧ (Word.mk stem (.fil .mudari cls false) e).realizes .raf = true := by
  simp [Word.wfFilTamm]

/-! ### تنافر الأصناف: الكلمة الواحدة لا تكون اسمًا وحرفًا وفعلًا معًا -/

theorem Word.isHarfJarr_eq_false_of_isIsm (w : Word) (h : w.isIsm = true) :
    w.isHarfJarr = false := by
  obtain ⟨_, k, _⟩ := w
  cases k <;> simp_all [Word.isIsm, Word.isHarfJarr]

theorem Word.isIsm_eq_false_of_isHarfJarr (w : Word) (h : w.isHarfJarr = true) :
    w.isIsm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | harf hk => cases hk <;> simp_all [Word.isIsm, Word.isHarfJarr]
  | _ => simp_all [Word.isIsm, Word.isHarfJarr]

theorem Word.isIsm_eq_false_of_isFilTamm (w : Word) (h : w.isFilTamm = true) :
    w.isIsm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil _ _ n => cases n <;> simp_all [Word.isIsm, Word.isFilTamm]
  | _ => simp_all [Word.isIsm, Word.isFilTamm]

theorem Word.isHarfJarr_eq_false_of_isFilTamm (w : Word) (h : w.isFilTamm = true) :
    w.isHarfJarr = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil _ _ n => cases n <;> simp_all [Word.isHarfJarr, Word.isFilTamm]
  | _ => simp_all [Word.isHarfJarr, Word.isFilTamm]

theorem Word.isIsm_eq_false_of_isNasikhInna (w : Word) (h : w.isNasikhInna = true) :
    w.isIsm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | harf hk => cases hk <;> simp_all [Word.isIsm, Word.isNasikhInna]
  | _ => simp_all [Word.isIsm, Word.isNasikhInna]

theorem Word.isFilTamm_eq_false_of_isNasikhInna (w : Word) (h : w.isNasikhInna = true) :
    w.isFilTamm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | harf hk => cases hk <;> simp_all [Word.isFilTamm, Word.isNasikhInna]
  | _ => simp_all [Word.isFilTamm, Word.isNasikhInna]

theorem Word.isIsm_eq_false_of_isKana (w : Word) (h : w.isKana = true) :
    w.isIsm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil _ _ n => cases n <;> simp_all [Word.isIsm, Word.isKana]
  | _ => simp_all [Word.isIsm, Word.isKana]

theorem Word.isFilTamm_eq_false_of_isKana (w : Word) (h : w.isKana = true) :
    w.isFilTamm = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil _ _ n => cases n <;> simp_all [Word.isFilTamm, Word.isKana]
  | _ => simp_all [Word.isFilTamm, Word.isKana]

theorem Word.isNasikhInna_eq_false_of_isKana (w : Word) (h : w.isKana = true) :
    w.isNasikhInna = false := by
  obtain ⟨_, k, _⟩ := w
  cases k with
  | fil _ _ n => cases n <;> simp_all [Word.isNasikhInna, Word.isKana]
  | _ => simp_all [Word.isNasikhInna, Word.isKana]

/-! ## سلامة شبه الجملة -/

/-- سلامة شبه الجملة: جار ومجرور (المجرور اسم مجرور)، أو ظرف منصوب ومضاف إليه مجرور.
qatr.txt:159–160 «وظرفا منصوبا … وجارا ومجرورا». -/
def ShibhJumla.wf : ShibhJumla → Bool
  | .jarrMajrur harf majrur => harf.isHarfJarr && majrur.isIsm && majrur.realizes .jarr
  | .zarf z mudafIlayh =>
      z.isZarf && z.realizes .nasb && mudafIlayh.isIsm && mudafIlayh.realizes .jarr

/-- سلامة المفعول به الاختياري: إن وُجد فهو اسم منصوب (qatr.txt:267–268). -/
def wfMaful : Option Word → Bool
  | none => true
  | some m => m.isIsm && m.realizes .nasb

/-! ## سلامة الخبر والجملة (استقراء متبادل بنيوي) -/

mutual
  /-- سلامة الخبر بحالةٍ `c` يقتضيها العامل في الخبر المفرد:
  `.raf` للمبتدأ وإنّ، `.nasb` لكان. الخبر الجملة وشبه الجملة لا تتأثر بالحالة
  (qatr.txt:157–161: الخبر جملة أو ظرف أو جار ومجرور)؛ والخبر الجملة يشترط رابطًا. -/
  def Khabar.wfWith (c : Case) (sahib : Word) : Khabar → Bool
    | .mufrad w => w.isIsm && w.realizes c
    | .jumla j => j.wf && j.hasRabitTo sahib
    | .shibh s => s.wf

  /-- سلامة الجملة:
  * اسمية: مبتدأ اسم مرفوع وخبر مرفوع (qatr.txt:152 «باب المبتدأ والخبر مرفوعان»).
  * فعلية: فعل تامّ سليم الصيغة (`Word.wfFilTamm`: ماضٍ/أمر مبني، أو مضارع فعليّ الصنف مرفوع
    بالتجرّد؛ qatr.txt:96) يليه فاعل اسم مرفوع (qatr.txt:219–220 «باب الفاعل مرفوع ك"قام زيد"»)
    ومفعول به اختياري منصوب (qatr.txt:267–268).
  * منسوخة بإنّ: حرف ناسخ، اسم منصوب، خبر مرفوع (qatr.txt:187–189).
  * منسوخة بكان: فعل ناقص، اسم مرفوع، خبر منصوب (qatr.txt:169–171). -/
  def Jumla.wf : Jumla → Bool
    | .ismiyya mubtada khabar =>
        mubtada.isIsm && mubtada.realizes .raf && khabar.wfWith .raf mubtada
    | .filiyya fil fail maful =>
        fil.wfFilTamm && fail.isIsm && fail.realizes .raf && wfMaful maful
    | .mansukhaInna harf ism khabar =>
        harf.isNasikhInna && ism.isIsm && ism.realizes .nasb && khabar.wfWith .raf ism
    | .mansukhaKana kana ism khabar =>
        kana.isKana && ism.isIsm && ism.realizes .raf && khabar.wfWith .nasb ism
end

/-- سلامة خبر المبتدأ وخبر إنّ: الخبر المفرد مرفوع. -/
abbrev Khabar.wf (sahib : Word) : Khabar → Bool := Khabar.wfWith .raf sahib

/-- سلامة خبر كان: الخبر المفرد منصوب (qatr.txt:171 «وينصبن الخبر خبرا لهن»). -/
abbrev Khabar.wfKana (sahib : Word) : Khabar → Bool := Khabar.wfWith .nasb sahib

/-! ## الإسناد -/

/-- الخبر طرفًا في الإسناد. -/
def Khabar.tarf : Khabar → Tarf
  | .mufrad w => .word w
  | .jumla j => .jumla j
  | .shibh s => .shibh s

/-- طرفا الإسناد في كل جملة: المسند إليه هو المبتدأ/الفاعل/اسم الناسخ،
والمسند هو الخبر/الفعل. -/
def Jumla.isnad : Jumla → Isnad
  | .ismiyya mubtada khabar => ⟨khabar.tarf, .word mubtada⟩
  | .filiyya fil fail _ => ⟨.word fil, .word fail⟩
  | .mansukhaInna _ ism khabar => ⟨khabar.tarf, .word ism⟩
  | .mansukhaKana _ ism khabar => ⟨khabar.tarf, .word ism⟩

/-- شبه الجملة لا إسناد فيها بذاتها؛ هي متعلقة بمحذوف
(qatr.txt:160–161 «وتعلقهما بمستقر أو استقر محذوفتين»؛ qatr.txt:143). -/
def ShibhJumla.hasIsnad : ShibhJumla → Bool := fun _ => false

theorem shibh_jumla_no_isnad (s : ShibhJumla) : s.hasIsnad = false := rfl

theorem isnad_total (j : Jumla) : ∃ i, j.isnad = i := ⟨_, rfl⟩

/-- المسند إليه اسم (كلمة) دائمًا في هذه الشبكة. -/
theorem isnad_ilayh_is_word (j : Jumla) : ∃ w, j.isnad.musnadIlayh = .word w := by
  cases j <;> exact ⟨_, rfl⟩

/-! ## التسطير (ترتيب الكلمات) -/

/-- كلمات شبه الجملة بالترتيب. -/
def ShibhJumla.linearize : ShibhJumla → List Word
  | .jarrMajrur harf majrur => [harf, majrur]
  | .zarf z mudafIlayh => [z, mudafIlayh]

mutual
  def Khabar.linearize : Khabar → List Word
    | .mufrad w => [w]
    | .jumla j => j.linearize
    | .shibh s => s.linearize

  /-- الترتيب المعتمد: المبتدأ فالخبر؛ الفعل فالفاعل فالمفعول (qatr.txt:220 «ولا يتأخر عامله عنه»)؛
  الناسخ فاسمه فخبره. -/
  def Jumla.linearize : Jumla → List Word
    | .ismiyya mubtada khabar => mubtada :: khabar.linearize
    | .filiyya fil fail maful => fil :: fail :: maful.toList
    | .mansukhaInna harf ism khabar => harf :: ism :: khabar.linearize
    | .mansukhaKana kana ism khabar => kana :: ism :: khabar.linearize
end

theorem linearize_length_pos (j : Jumla) : 0 < j.linearize.length := by
  cases j <;> simp [Jumla.linearize]

/-! ## الأدوار -/

/-- أدوار شبه الجملة. الظرف منصوب على الظرفية (مفعول فيه) وناصبه الفعل المحذوف «استقر»
(qatr.txt:159–161)؛ لعدم وجود دور `mafulFih` في `Role` نسجّله بـ`.maful` (نصب، عامله فعل). -/
def ShibhJumla.roles : ShibhJumla → List (Word × Role)
  | .jarrMajrur _ majrur => [(majrur, .majrur)]
  | .zarf z mudafIlayh => [(z, .maful), (mudafIlayh, .mudafIlayh)]

mutual
  /-- أدوار الخبر؛ `r` هو دور الخبر المفرد بحسب العامل (خبر/خبر إنّ/خبر كان). -/
  def Khabar.roles (r : Role) : Khabar → List (Word × Role)
    | .mufrad w => [(w, r)]
    | .jumla j => j.roles
    | .shibh s => s.roles

  /-- أدوار الجملة. الأفعال التامة والحروف الناسخة وكان لا تحمل دورًا إعرابيًا اسميًا. -/
  def Jumla.roles : Jumla → List (Word × Role)
    | .ismiyya mubtada khabar => (mubtada, .mubtada) :: khabar.roles .khabar
    | .filiyya _ fail maful => (fail, .fail) :: (maful.map (fun m => (m, .maful))).toList
    | .mansukhaInna _ ism khabar => (ism, .ismInna) :: khabar.roles .khabarInna
    | .mansukhaKana _ ism khabar => (ism, .ismKana) :: khabar.roles .khabarKana
end

/-! ## المبرهنات: السلامة تضمن مطابقة كل دور لحالته -/

theorem ShibhJumla.wf_roles_realize (s : ShibhJumla) (h : s.wf = true) :
    ∀ p ∈ s.roles, p.1.realizes (roleCase p.2) = true := by
  cases s with
  | jarrMajrur harf majrur =>
    simp [ShibhJumla.wf] at h
    simp [ShibhJumla.roles, roleCase, h]
  | zarf z mudafIlayh =>
    simp [ShibhJumla.wf] at h
    simp [ShibhJumla.roles, roleCase, h]

mutual
  theorem Khabar.wfWith_roles_realize (k : Khabar) :
      ∀ (c : Case) (sahib : Word) (r : Role), roleCase r = c → k.wfWith c sahib = true →
        ∀ p ∈ k.roles r, p.1.realizes (roleCase p.2) = true := by
    intro c sahib r hr h p hp
    cases k with
    | mufrad w =>
      simp [Khabar.roles] at hp
      subst hp
      simp [Khabar.wfWith] at h
      simpa [hr] using h.2
    | jumla j =>
      exact Jumla.wf_roles_realize j (by simp [Khabar.wfWith] at h; exact h.1) p
        (by simpa [Khabar.roles] using hp)
    | shibh s =>
      exact ShibhJumla.wf_roles_realize s (by simpa [Khabar.wfWith] using h) p
        (by simpa [Khabar.roles] using hp)

  /-- كل كلمة ذات دور في جملة سليمة تحقق حالة دورها. -/
  theorem Jumla.wf_roles_realize (j : Jumla) :
      j.wf = true → ∀ p ∈ j.roles, p.1.realizes (roleCase p.2) = true := by
    intro h p hp
    cases j with
    | ismiyya mubtada khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨_, h2⟩, h3⟩ := h
      simp [Jumla.roles] at hp
      rcases hp with rfl | hp
      · simpa [roleCase] using h2
      · exact Khabar.wfWith_roles_realize khabar .raf mubtada .khabar rfl h3 p hp
    | filiyya fil fail maful =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨_, _⟩, h3⟩, h4⟩ := h
      simp [Jumla.roles] at hp
      rcases hp with rfl | hp
      · simpa [roleCase] using h3
      · cases maful with
        | none => simp [Option.map, Option.toList] at hp
        | some m =>
          simp [Option.map, Option.toList] at hp
          subst hp
          simp [wfMaful] at h4
          simpa [roleCase] using h4.2
    | mansukhaInna harf ism khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨_, _⟩, h3⟩, h4⟩ := h
      simp [Jumla.roles] at hp
      rcases hp with rfl | hp
      · simpa [roleCase] using h3
      · exact Khabar.wfWith_roles_realize khabar .raf ism .khabarInna rfl h4 p hp
    | mansukhaKana kana ism khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨_, _⟩, h3⟩, h4⟩ := h
      simp [Jumla.roles] at hp
      rcases hp with rfl | hp
      · simpa [roleCase] using h3
      · exact Khabar.wfWith_roles_realize khabar .nasb ism .khabarKana rfl h4 p hp
end

theorem wf_roles_realize (j : Jumla) (h : j.wf = true) :
    ∀ p ∈ j.roles, p.1.realizes (roleCase p.2) = true :=
  Jumla.wf_roles_realize j h

/-! ## المبرهنات: محاذاة الأدوار مع التسطير -/

theorem ShibhJumla.roles_align (s : ShibhJumla) (h : s.wf = true) :
    s.roles.map Prod.fst = s.linearize.filter Word.isIsm := by
  cases s with
  | jarrMajrur harf majrur =>
    simp [ShibhJumla.wf] at h
    obtain ⟨⟨h1, h2⟩, _⟩ := h
    simp [ShibhJumla.roles, ShibhJumla.linearize, List.filter_cons, h2,
      Word.isIsm_eq_false_of_isHarfJarr harf h1]
  | zarf z mudafIlayh =>
    simp [ShibhJumla.wf] at h
    obtain ⟨⟨⟨h1, _⟩, h3⟩, _⟩ := h
    simp [ShibhJumla.roles, ShibhJumla.linearize, List.filter_cons, Word.isIsm_of_isZarf z h1, h3]

mutual
  theorem Khabar.roles_align (k : Khabar) :
      ∀ (c : Case) (sahib : Word) (r : Role), k.wfWith c sahib = true →
        (k.roles r).map Prod.fst = k.linearize.filter Word.isIsm := by
    intro c sahib r h
    cases k with
    | mufrad w =>
      simp [Khabar.wfWith] at h
      simp [Khabar.roles, Khabar.linearize, List.filter_cons, h.1]
    | jumla j =>
      simp only [Khabar.roles, Khabar.linearize]
      exact Jumla.roles_align j (by simp [Khabar.wfWith] at h; exact h.1)
    | shibh s =>
      simp only [Khabar.roles, Khabar.linearize]
      exact ShibhJumla.roles_align s (by simpa [Khabar.wfWith] using h)

  /-- في الجملة السليمة، الكلمات الحاملة للأدوار هي الأسماء كلها دون سواها، بترتيب التسطير نفسه.
  (الأفعال التامة والنواسخ وحروف الجر عوامل لا معمولات.) -/
  theorem Jumla.roles_align (j : Jumla) :
      j.wf = true → j.roles.map Prod.fst = j.linearize.filter Word.isIsm := by
    intro h
    cases j with
    | ismiyya mubtada khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨h1, _⟩, h3⟩ := h
      simp only [Jumla.roles, Jumla.linearize, List.map_cons, List.filter_cons, h1,
        ↓reduceIte]
      rw [Khabar.roles_align khabar .raf mubtada .khabar h3]
    | filiyya fil fail maful =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := h
      have hf := Word.isIsm_eq_false_of_isFilTamm fil (Word.isFilTamm_of_wfFilTamm fil h1)
      cases maful with
      | none =>
        simp [Jumla.roles, Jumla.linearize, List.filter_cons, Option.map, Option.toList,
          h2, hf]
      | some m =>
        simp [wfMaful] at h4
        simp [Jumla.roles, Jumla.linearize, List.filter_cons, Option.map, Option.toList,
          h2, h4.1, hf]
    | mansukhaInna harf ism khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := h
      have hf := Word.isIsm_eq_false_of_isNasikhInna harf h1
      simp only [Jumla.roles, Jumla.linearize, List.map_cons, List.filter_cons, h2, hf,
        ↓reduceIte, Bool.false_eq_true]
      rw [Khabar.roles_align khabar .raf ism .khabarInna h4]
    | mansukhaKana kana ism khabar =>
      simp [Jumla.wf] at h
      obtain ⟨⟨⟨h1, h2⟩, _⟩, h4⟩ := h
      have hf := Word.isIsm_eq_false_of_isKana kana h1
      simp only [Jumla.roles, Jumla.linearize, List.map_cons, List.filter_cons, h2, hf,
        ↓reduceIte, Bool.false_eq_true]
      rw [Khabar.roles_align khabar .nasb ism .khabarKana h4]
end

theorem linearize_roles_align (j : Jumla) (h : j.wf = true) :
    j.roles.map Prod.fst = j.linearize.filter Word.isIsm :=
  Jumla.roles_align j h

/-- كل كلمة ذات دور في جملة سليمة واردة في تسطيرها. -/
theorem roles_subset_linearize (j : Jumla) (h : j.wf = true) :
    ∀ p ∈ j.roles, p.1 ∈ j.linearize := by
  intro p hp
  have hm : p.1 ∈ j.roles.map Prod.fst := List.mem_map_of_mem hp
  rw [linearize_roles_align j h] at hm
  exact (List.mem_filter.mp hm).1

end Arabic
