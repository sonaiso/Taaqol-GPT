/-
Arabic/Pipeline.lean — المسار الكامل: بتات → خلايا → كلمات (معجم مودَع) → تركيب → منطوق → مفهوم.

ما يُبرهَن هنا:
* `pipeline_roundtrip`: لكل جملة سليمة داخل النحو G ومعجمٍ يغطي كلماتها، تشفيرها بالبتات
  ثم فكّها بالمسار الكامل يُعيد الجملة نفسها (كبنية) ومنطوقها.
* `pipeline_sound`: كل ما يقبله المسار جملة سليمة الإعراب، وتسطيرها يطابق ما قرأه المعجم.
* `pipeline_refuses_*`: الرفض المسمّى ينتقل من كل طبقة.

ما لا يُبرهَن (ويُعلَن صراحةً): صحة المعجم المودَع، واكتمال G لكل العربية.
-/
import Arabic.Cells
import Arabic.Parse
import Arabic.Mafhum

namespace Arabic

/-! ## المعجم المودَع -/

/-- المعجم: مفتاحه الصورة الخلوية الكاملة للكلمة (الجذع ثم خلية العلامة الظاهرة)،
وقيمته الكلمة بسماتها المعجمية المودَعة (القسم، الصنف، التعريف، الاستعمال).
يُودَع من المصدر ولا يُستنتج؛ السمات مدخلات لا نتائج. -/
abbrev Lexicon := List (List Cell × Word)

/-- التقطيع مودَع: المدخل قائمة كلمات كلٌّ مشفَّرة بخلاياها على حدة. -/
abbrev CellText := List (List Cell)

/-- خلية العلامة: ترميز **حاقن** لكل علامة من الإحدى عشرة إلى خلية متمايزة.
الحركات على الهمزة (ء)؛ الحروف النائبة على حرفها ساكنًا (و/ا/ي)؛ النون والتقدير وحذف حرف العلة
على النون بحركات متمايزة. `endingCell_injective` يثبت أن لا تصادم. -/
def endingCell : Ending → Cell
  | .damma => (⟨28, by decide⟩, .damma)
  | .fatha => (⟨28, by decide⟩, .fatha)
  | .kasra => (⟨28, by decide⟩, .kasra)
  | .sukun => (⟨28, by decide⟩, .sukun)
  | .waw => (⟨26, by decide⟩, .sukun)
  | .alif => (⟨0, by decide⟩, .sukun)
  | .yaa => (⟨27, by decide⟩, .sukun)
  | .thubutNun => (⟨24, by decide⟩, .damma)
  | .hadhfNun => (⟨24, by decide⟩, .sukun)
  | .hadhfHarfIlla => (⟨24, by decide⟩, .fatha)
  | .muqaddar => (⟨24, by decide⟩, .kasra)

theorem endingCell_injective : ∀ a b : Ending, endingCell a = endingCell b → a = b := by
  intro a b h; cases a <;> cases b <;> first | rfl | (simp [endingCell] at h)

/-- الصورة الخلوية للكلمة: الجذع + خلية العلامة. هذا ما يُقرأ من البتات. -/
def Word.surface (w : Word) : List Cell := w.stem ++ [endingCell w.ending]

/-- الصورة الخلوية تعيّن الجذع والعلامة معًا (السمات المعجمية وحدها تُودَع). -/
theorem surface_inj (w w' : Word) (h : w.surface = w'.surface) :
    w.stem = w'.stem ∧ w.ending = w'.ending := by
  unfold Word.surface at h
  have := List.append_inj' h rfl
  exact ⟨this.1, endingCell_injective _ _ (List.singleton_inj.mp this.2)⟩

theorem surface_ne_nil (w : Word) : w.surface ≠ [] := by
  unfold Word.surface; exact List.append_ne_nil_of_right_ne_nil _ (by simp)

/-- سلامة المعجم: كل مفتاح هو صورة قيمته. بدونه قد تُعاد كلمة لا تطابق البتات المقروءة. -/
def Lexicon.wf (lex : Lexicon) : Prop := ∀ e ∈ lex, e.1 = e.2.surface

def Lexicon.lookup (lex : Lexicon) (cells : List Cell) : Except Refusal Word :=
  match lex.find? (fun e => e.1 == cells) with
  | some e => .ok e.2
  | none => .error .notInLexicon

def Lexicon.lookupAll (lex : Lexicon) : CellText → Except Refusal (List Word)
  | [] => .ok []
  | c :: cs => do
      let w ← lex.lookup c
      let ws ← lex.lookupAll cs
      pure (w :: ws)

theorem lookup_wf {lex : Lexicon} (hl : lex.wf) {cells : List Cell} {w : Word}
    (h : lex.lookup cells = .ok w) : w.surface = cells := by
  unfold Lexicon.lookup at h
  split at h
  · rename_i e he
    simp only [Except.ok.injEq] at h; subst h
    have hmem := List.mem_of_find?_eq_some he
    have heq := List.find?_some he
    rw [← hl e hmem]; exact beq_iff_eq.mp heq
  · cases h

theorem lookupAll_wf {lex : Lexicon} (hl : lex.wf) :
    ∀ {cells : CellText} {ws : List Word}, lex.lookupAll cells = .ok ws → ws.map Word.surface = cells
  | [], ws, h => by simp [Lexicon.lookupAll] at h; subst h; rfl
  | c :: cs, ws, h => by
      simp only [Lexicon.lookupAll, bind, Except.bind] at h
      split at h
      · cases h
      · rename_i w hw
        split at h
        · cases h
        · rename_i ws' hws
          simp only [pure, Except.pure, Except.ok.injEq] at h; subst h
          simp [List.map, lookup_wf hl hw, lookupAll_wf hl hws]

/-! ## التشفير والفك على مستوى النص -/

/-- تشفير كل كلمة إلى بايتاتها (الكلمات مفصولة بنيويًا). -/
def encodeWords (ws : List (List Cell)) : List (List Byte) := ws.map encodeText

def decodeWords : List (List Byte) → Except Refusal CellText
  | [] => .ok []
  | b :: bs => do
      let c ← decodeText b
      let cs ← decodeWords bs
      pure (c :: cs)

theorem decodeWords_encodeWords (ws : CellText) : decodeWords (encodeWords ws) = .ok ws := by
  induction ws with
  | nil => rfl
  | cons c cs ih =>
    simp only [encodeWords, List.map, decodeWords, decodeText_encodeText]
    simp only [encodeWords] at ih
    rw [ih]; rfl

/-! ## المسار -/

structure Qiraa where
  jumla : Jumla
  mantuq : Mantuq
  mafahim : List Mafhum

/-- المسار الكامل. -/
def pipeline (lex : Lexicon) (s : Siyaq) (bytes : List (List Byte)) : Except Refusal Qiraa := do
  let cells ← decodeWords bytes
  let words ← lex.lookupAll cells
  let j ← parse words
  pure ⟨j, j.mantuq, mafahim s j⟩

/-- المعجم يغطي الكلمة: صورتها الخلوية تعيد الكلمة ذاتها (أول مطابقة). -/
def Lexicon.covers (lex : Lexicon) (w : Word) : Prop := lex.lookup w.surface = .ok w

theorem lookupAll_of_covers (lex : Lexicon) (ws : List Word)
    (h : ∀ w ∈ ws, lex.covers w) : lex.lookupAll (ws.map Word.surface) = .ok ws := by
  induction ws with
  | nil => rfl
  | cons w ws ih =>
    have hw : lex.lookup w.surface = .ok w := h w (List.mem_cons_self ..)
    have hrest := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    simp only [List.map, Lexicon.lookupAll, hw, hrest]
    rfl

/-- **الجولة الكاملة**: جملة سليمة داخل G، معجم يغطي كلماتها ⇒ بتاتها تُقرأ إلى الجملة نفسها ومنطوقها ومفاهيمها. -/
theorem pipeline_roundtrip (lex : Lexicon) (s : Siyaq) (j : Jumla)
    (hw : j.wf = true) (hg : j.inG = true)
    (hcov : ∀ w ∈ j.linearize, lex.covers w) :
    pipeline lex s (encodeWords (j.linearize.map Word.surface)) =
      .ok ⟨j, j.mantuq, mafahim s j⟩ := by
  unfold pipeline
  rw [decodeWords_encodeWords]
  simp only [bind, Except.bind]
  rw [lookupAll_of_covers lex _ hcov]
  simp only [parse_complete j hw hg]
  rfl

/-- **السلامة**: كل قراءة يقبلها المسار جملتها سليمة الإعراب ومنطوقها مشتق منها ومفاهيمها مرخّصة. -/
theorem pipeline_sound (lex : Lexicon) (s : Siyaq) (bytes : List (List Byte)) (q : Qiraa)
    (h : pipeline lex s bytes = .ok q) :
    q.jumla.wf = true ∧ q.mantuq = q.jumla.mantuq ∧
      (∀ f ∈ q.mafahim, f.asl = q.mantuq) := by
  unfold pipeline at h
  simp only [bind, Except.bind] at h
  split at h
  · cases h
  · split at h
    · cases h
    · split at h
      · cases h
      · rename_i _ _ _ _ j hj
        simp only [pure, Except.pure, Except.ok.injEq] at h
        subst h
        refine ⟨(parse_sound _ _ hj).1, rfl, ?_⟩
        intro f hf; exact mafhum_min_mantuq hf

/-- **ترخيص المفاهيم**: كل مفهوم يقبله المسار إمّا موافقة بأولوية مودَعة في السياق،
وإمّا مخالفة بقيد معتبر مودَع مع انتفاء الموانع. لا مفهوم من غير ذلك. -/
theorem pipeline_mafahim_licensed (lex : Lexicon) (s : Siyaq) (bytes : List (List Byte)) (q : Qiraa)
    (h : pipeline lex s bytes = .ok q) :
    ∀ f ∈ q.mafahim,
      (∃ a, s.awlawiyya = some a ∧ f = ⟨q.mantuq, .muwafaqa a⟩) ∨
      (∃ qd, s.qayd = some qd ∧ qd.mutabar = true ∧ s.mawani = [] ∧ f = ⟨q.mantuq, .mukhalafa qd⟩) := by
  unfold pipeline at h
  simp only [bind, Except.bind] at h
  split at h
  · cases h
  · split at h
    · cases h
    · split at h
      · cases h
      · simp only [pure, Except.pure, Except.ok.injEq] at h
        subst h
        intro f hf
        simp only [mafahim] at hf
        rcases List.mem_append.mp hf with hf | hf
        · exact Or.inl (mem_muwafaqaOf hf)
        · exact Or.inr (mem_mukhalafaOf hf)

/-- **الأمانة للبتات**: مع معجم سليم، الكلمات المعادة هي بالضبط ما فُكّ من البتات
(صورة الجملة المعادة تساوي الخلايا المقروءة)، فلا تُعاد «زيدٌ» لبتات «زيدًا». -/
theorem pipeline_faithful (lex : Lexicon) (hl : lex.wf) (s : Siyaq) (bytes : List (List Byte)) (q : Qiraa)
    (h : pipeline lex s bytes = .ok q) :
    decodeWords bytes = .ok (q.jumla.linearize.map Word.surface) := by
  unfold pipeline at h
  simp only [bind, Except.bind] at h
  split at h
  · cases h
  · rename_i cells hc
    split at h
    · cases h
    · rename_i ws hws
      split at h
      · cases h
      · rename_i j hj
        simp only [pure, Except.pure, Except.ok.injEq] at h
        subst h
        rw [hc, (parse_sound _ _ hj).2, lookupAll_wf hl hws]

/-! ## مجرى بايتات واحد: التقطيع على الفراغ -/

/-- الفاصل: الفراغ ASCII. لا يظهر داخل أي كلمة مشفَّرة (`encodeText_no_space`). -/
def space : Byte := 0x20

/-- ضمّ الكلمات في مجرى واحد بفاصل واحد بينها. -/
def joinWords : List (List Byte) → List Byte
  | [] => []
  | [w] => w
  | w :: ws => w ++ space :: joinWords ws

def splitAux : List Byte → List Byte → List (List Byte)
  | [], acc => [acc.reverse]
  | b :: bs, acc => if b = space then acc.reverse :: splitAux bs [] else splitAux bs (b :: acc)

/-- التقطيع على الفراغ. -/
def splitWords (bs : List Byte) : List (List Byte) := splitAux bs []

theorem splitAux_append (w : List Byte) (hw : ∀ b ∈ w, b ≠ space) :
    ∀ (rest acc : List Byte), splitAux (w ++ rest) acc = splitAux rest (w.reverse ++ acc) := by
  induction w with
  | nil => intros; rfl
  | cons b w ih =>
    intro rest acc
    have hb : b ≠ space := hw b (List.mem_cons_self ..)
    simp only [List.cons_append, splitAux, if_neg hb, List.reverse_cons, List.append_assoc,
      List.singleton_append]
    exact ih (fun x hx => hw x (List.mem_cons_of_mem _ hx)) rest (b :: acc)

/-- **جولة التقطيع**: ضمّ كلمات خالية من الفراغ ثم تقطيعها يعيدها. -/
theorem splitWords_joinWords : ∀ (ws : List (List Byte)), ws ≠ [] →
    (∀ w ∈ ws, ∀ b ∈ w, b ≠ space) → splitWords (joinWords ws) = ws
  | [], h, _ => absurd rfl h
  | [w], _, hw => by
      simp only [splitWords, joinWords]
      rw [← List.append_nil w, splitAux_append w (hw w (List.mem_singleton_self w))]
      simp [splitAux]
  | w :: w' :: ws, _, hw => by
      simp only [splitWords, joinWords]
      rw [splitAux_append w (hw w (List.mem_cons_self ..))]
      simp only [splitAux, if_true, List.append_nil, List.reverse_reverse, List.cons.injEq, true_and]
      exact splitWords_joinWords (w' :: ws) (by simp) (fun x hx => hw x (List.mem_cons_of_mem _ hx))

/-- المسار من مجرى بايتات واحد. -/
def pipelineText (lex : Lexicon) (s : Siyaq) (bs : List Byte) : Except Refusal Qiraa :=
  pipeline lex s (splitWords bs)

/-- بايتات الجملة: كلماتها مشفَّرة ومضمومة بفراغ. -/
def Jumla.bytes (j : Jumla) : List Byte := joinWords (encodeWords (j.linearize.map Word.surface))

/-- **الجولة الكاملة من مجرى بايتات واحد**: جملة سليمة في G، معجم يغطيها ⇒ مجرى بايتاتها
(بفواصل الفراغ) يُقطَّع ويُفكّ ويُحلَّل إلى الجملة نفسها ومنطوقها ومفاهيمها. -/
theorem pipelineText_roundtrip (lex : Lexicon) (s : Siyaq) (j : Jumla)
    (hw : j.wf = true) (hg : j.inG = true)
    (hcov : ∀ w ∈ j.linearize, lex.covers w) :
    pipelineText lex s j.bytes = .ok ⟨j, j.mantuq, mafahim s j⟩ := by
  unfold pipelineText Jumla.bytes
  rw [splitWords_joinWords]
  · exact pipeline_roundtrip lex s j hw hg hcov
  · have := linearize_length_pos j
    simp only [encodeWords, ne_eq, List.map_eq_nil_iff]
    intro h; rw [h] at this; exact absurd this (by simp)
  · intro w hw b hb
    simp only [encodeWords, List.mem_map] at hw
    obtain ⟨cells, _, rfl⟩ := hw
    exact encodeText_no_space cells b hb

theorem pipelineText_sound (lex : Lexicon) (s : Siyaq) (bs : List Byte) (q : Qiraa)
    (h : pipelineText lex s bs = .ok q) :
    q.jumla.wf = true ∧ q.mantuq = q.jumla.mantuq ∧ (∀ f ∈ q.mafahim, f.asl = q.mantuq) :=
  pipeline_sound lex s _ q h

/-- الرفض ينتقل من طبقة البتات. -/
theorem pipeline_refuses_bad_bytes (lex : Lexicon) (s : Siyaq) :
    pipeline lex s [[0x41]] = .error .unknownByte := rfl

/-- الرفض ينتقل من طبقة الخلايا (شدّة غير مدعومة). -/
theorem pipeline_refuses_shadda (lex : Lexicon) (s : Siyaq) :
    pipeline lex s [[0x628, 0x651].flatMap utf8Encode2] = .error .unknownCell := by
  unfold pipeline decodeWords
  rw [decodeText_refuses_shadda]; rfl

/-- الرفض ينتقل من المعجم: معجم فارغ لا يقرأ شيئًا. -/
theorem pipeline_refuses_empty_lexicon (s : Siyaq) (c : List Cell) :
    pipeline [] s [encodeText c] = .error .notInLexicon := by
  unfold pipeline decodeWords
  rw [decodeText_encodeText]; rfl

/-- لا قراءة بلا إسناد: مدخل فارغ. -/
theorem pipeline_refuses_empty (lex : Lexicon) (s : Siyaq) :
    pipeline lex s [] = .error .noIsnad := rfl

/-! ## شواهد تنفيذية كاملة من البتات -/

/-- معجم الشواهد: مفتاحه الصورة الخلوية (جذع + علامة) فيميّز زيدٌ من زيدًا. -/
def lexShahid : Lexicon :=
  [zaydun, zaydan, qaimun, qaiman, qama, inna, kana, fi, addari, fawqa].map (fun w => (w.surface, w))

/-- كل كلمات الشواهد مغطّاة بمفاتيح متمايزة. -/
theorem lexShahid_surfaces_distinct :
    ([zaydun, zaydan, qaimun, qaiman, qama, inna, kana, fi, addari, fawqa].map Word.surface).Nodup := by
  decide

/-- مجرى بايتات واحد للكلمات (بفواصل الفراغ): هذا هو المدخل الحقيقي. -/
def bytesOf (ws : List Word) : List Byte := joinWords (encodeWords (ws.map Word.surface))

/-- «زيدٌ قائمٌ» من البتات حتى المنطوق؛ بلا سياق فلا مفهوم. -/
theorem zaydun_qaimun_from_bytes :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [zaydun, qaimun]) =
      .ok ⟨.ismiyya zaydun (.mufrad qaimun), ⟨zaydun, .word qaimun, .ithbat⟩, []⟩ := by
  rfl

/-- «إنّ زيدًا قائمٌ» من البتات: إنّ تنصب الاسم وتضيف التوكيد. -/
theorem inna_zaydan_qaimun_from_bytes :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [inna, zaydan, qaimun]) =
      .ok ⟨.mansukhaInna inna zaydan (.mufrad qaimun), ⟨zaydan, .word qaimun, .taukid⟩, []⟩ := by
  rfl

/-- «كانَ زيدٌ قائمًا» من البتات. -/
theorem kana_zaydun_qaiman_from_bytes :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [kana, zaydun, qaiman]) =
      .ok ⟨.mansukhaKana kana zaydun (.mufrad qaiman), ⟨zaydun, .word qaiman, .kawnMadi⟩, []⟩ := by
  rfl

/-- «قامَ زيدٌ» من البتات: الفعل مسند والفاعل مسند إليه. -/
theorem qama_zaydun_from_bytes :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [qama, zaydun]) =
      .ok ⟨.filiyya qama zaydun none, ⟨zaydun, .word qama, .hadath .madi⟩, []⟩ := by
  rfl

/-- «زيدٌ فوقَ الدارِ»: خبر شبه جملة ظرفية (الظرف سمة معجمية مودَعة). -/
theorem zaydun_fawqa_addari_from_bytes :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [zaydun, fawqa, addari]) =
      .ok ⟨.ismiyya zaydun (.shibh (.zarf fawqa addari)),
           ⟨zaydun, .shibh (.zarf fawqa addari), .ithbat⟩, []⟩ := by
  rfl

/-- «إنّ زيدٌ قائمٌ» بالبتات يُرفض برفع اسم إنّ: الرفض مسمّى بالحالة المطلوبة والعلامة الواردة. -/
theorem inna_zaydun_from_bytes_refused :
    pipelineText lexShahid ⟨none, [], none⟩ (bytesOf [inna, zaydun, qaimun]) =
      .error (.caseMismatch .nasb .damma) := by
  rfl

/-- مع قيد صفة ولا مانع: ينشأ مفهوم مخالفة واحد أصله المنطوق. -/
theorem zaydun_qaimun_with_sifa :
    (pipelineText lexShahid ⟨some .sifa, [], none⟩ (bytesOf [zaydun, qaimun])).map
      (fun q => q.mafahim.map (·.naw)) = .ok [.mukhalafa .sifa] := by
  rfl

/-- مع مانع: لا مفهوم مخالفة. -/
theorem zaydun_qaimun_with_mani :
    (pipelineText lexShahid ⟨some .sifa, [.jawabSual], none⟩ (bytesOf [zaydun, qaimun])).map
      (fun q => q.mafahim.length) = .ok 0 := by
  rfl

end Arabic
