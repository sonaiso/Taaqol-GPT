/-
Arabic/Cells.lean — طبقة الخلايا: من نقاط الترميز إلى خلايا A116 (حامل × حركة) وبالعكس.

تركّب هذه الطبقة فوق `Arabic.Bits`: نصّ = خلايا → نقاط ترميز → بايتات UTF-8، والعكس مع رفض
صريح (`Refusal.unknownCell`) لأي حرف أو حركة خارج جدول A116 (مثل الشدّة 0x651).
لا Mathlib؛ مكتبة Lean 4.19 القياسية فقط.
-/
import Arabic.Bits

namespace Arabic

/-! ## التعاريف -/

/-- عدد الحوامل: تسعة وعشرون. -/
theorem carriers_length : carriers.length = 29 := by decide

/-- نقطة ترميز الحامل: الحرف في موضعه من جدول A116. -/
def carrierCodePoint : Carrier → Nat := fun c => (carriers.get c).toNat

/-- نقطة ترميز الحركة (الفتحة، الضمة، الكسرة، السكون). -/
def markCodePoint : Mark → Nat
  | .fatha => 0x64E
  | .damma => 0x64F
  | .kasra => 0x650
  | .sukun => 0x652

/-- عكس `carrierCodePoint`: موضع الحرف في جدول A116 إن وُجد. -/
def carrierOfCodePoint (cp : Nat) : Option Carrier :=
  carriers.findFinIdx? (fun ch => ch.toNat == cp)

/-- عكس `markCodePoint`. -/
def markOfCodePoint : Nat → Option Mark
  | 0x64E => some .fatha
  | 0x64F => some .damma
  | 0x650 => some .kasra
  | 0x652 => some .sukun
  | _ => none

/-- الخلية → نقطتا ترميز: الحامل ثم الحركة. -/
def cellToCodePoints (c : Cell) : List Nat := [carrierCodePoint c.1, markCodePoint c.2]

/-- نقاط ترميز → خلايا: أزواج (حرف، حركة)؛ أي حرف أو حركة مجهولة أو زوج ناقص → `unknownCell`. -/
def codePointsToCells : List Nat → Except Refusal (List Cell)
  | [] => .ok []
  | l :: m :: rest =>
    match carrierOfCodePoint l, markOfCodePoint m with
    | some c, some mk =>
      match codePointsToCells rest with
      | .ok cells => .ok ((c, mk) :: cells)
      | .error r => .error r
    | _, _ => .error .unknownCell
  | [_] => .error .unknownCell

/-- تشفير النص: خلايا → نقاط ترميز → بايتات UTF-8. -/
def encodeText (cells : List Cell) : List Byte :=
  (cells.flatMap cellToCodePoints).flatMap utf8Encode2

/-- فكّ النص: بايتات → نقاط ترميز (مع رفض `Bits`) → خلايا (مع رفض `unknownCell`). -/
def decodeText (bs : List Byte) : Except Refusal (List Cell) :=
  match decodeAll bs with
  | .ok cps => codePointsToCells cps
  | .error r => .error r

/-! ## المبرهنات -/

/-- نقاط ترميز الحوامل متباينة (تعداد منتهٍ على 29 × 29 حالة). -/
theorem carrierCodePoint_injective :
    ∀ a b : Carrier, carrierCodePoint a = carrierCodePoint b → a = b := by
  decide

/-- كل حامل داخل الكتلة العربية 0x0600..0x06FF (تعداد منتهٍ على 29 حالة). -/
theorem carrier_in_arabic_block :
    ∀ c : Carrier, 0x600 ≤ carrierCodePoint c ∧ carrierCodePoint c ≤ 0x6FF := by
  decide

/-- كل حركة داخل الكتلة العربية. -/
theorem mark_in_arabic_block :
    ∀ m : Mark, 0x600 ≤ markCodePoint m ∧ markCodePoint m ≤ 0x6FF := by
  intro m; cases m <;> decide

/-- عكس الحامل يعيد الحامل نفسه (تعداد منتهٍ على 29 حالة). -/
theorem carrierOfCodePoint_carrierCodePoint :
    ∀ c : Carrier, carrierOfCodePoint (carrierCodePoint c) = some c := by
  decide

/-- عكس الحركة يعيد الحركة نفسها. -/
theorem markOfCodePoint_markCodePoint :
    ∀ m : Mark, markOfCodePoint (markCodePoint m) = some m := by
  intro m; cases m <;> rfl

/-- الجولة على مستوى نقاط الترميز: `codePointsToCells (cells.flatMap cellToCodePoints) = .ok cells`
(استقراء عام على أي قائمة خلايا). -/
theorem codePointsToCells_cellToCodePoints :
    ∀ cells : List Cell, codePointsToCells (cells.flatMap cellToCodePoints) = .ok cells := by
  intro cells
  induction cells with
  | nil => rfl
  | cons cell cells ih =>
    rw [List.flatMap_cons]
    simp only [cellToCodePoints, List.cons_append, List.nil_append, codePointsToCells,
      carrierOfCodePoint_carrierCodePoint, markOfCodePoint_markCodePoint, ih]

/-- كل نقطة ناتجة عن خلية داخل الكتلة العربية. -/
theorem cellCodePoints_in_arabic_block (cells : List Cell) :
    ∀ cp ∈ cells.flatMap cellToCodePoints, 0x600 ≤ cp ∧ cp ≤ 0x6FF := by
  intro cp hcp
  rw [List.mem_flatMap] at hcp
  obtain ⟨cell, _, hmem⟩ := hcp
  simp only [cellToCodePoints, List.mem_cons, List.not_mem_nil, or_false] at hmem
  rcases hmem with rfl | rfl
  · exact carrier_in_arabic_block cell.1
  · exact mark_in_arabic_block cell.2

/-- لا فراغ (0x20) في تشفير أي نصّ خلوي. -/
theorem encodeText_no_space (cells : List Cell) : ∀ b ∈ encodeText cells, b ≠ (0x20 : Byte) := by
  intro b hb
  unfold encodeText at hb
  rw [List.mem_flatMap] at hb
  obtain ⟨cp, hcp, hb⟩ := hb
  exact utf8Encode2_no_space cp (by have := (cellCodePoints_in_arabic_block cells cp hcp).2; omega) b hb

/-- تشفير نصّ غير فارغ غير فارغ. -/
theorem encodeText_ne_nil (cells : List Cell) (h : cells ≠ []) : encodeText cells ≠ [] := by
  cases cells with
  | nil => exact absurd rfl h
  | cons c cs => simp [encodeText, cellToCodePoints, utf8Encode2]

/-- الجولة الكاملة من البتات إلى الخلايا: `decodeText (encodeText cells) = .ok cells`
(برهان عام يركّب `decodeAll_encode` مع `codePointsToCells_cellToCodePoints`). -/
theorem decodeText_encodeText :
    ∀ cells : List Cell, decodeText (encodeText cells) = .ok cells := by
  intro cells
  unfold decodeText encodeText
  rw [decodeAll_encode _ (cellCodePoints_in_arabic_block cells)]
  exact codePointsToCells_cellToCodePoints cells

/-- رفض: نصّ يحوي الشدّة (0x651) — داخل الكتلة العربية لكنها ليست حركة A116 — يُرفض بـ `unknownCell`.
النص: باء (0x628) + شدّة. -/
theorem decodeText_refuses_shadda :
    decodeText ([0x628, 0x651].flatMap utf8Encode2) = .error .unknownCell := rfl

/-- رفض: حرف منفرد بلا حركة (باء 0x628 ثم نهاية) → `unknownCell`. -/
theorem decodeText_refuses_bare_letter :
    decodeText (utf8Encode2 0x628) = .error .unknownCell := rfl

/-- رفض ينتقل من طبقة البتات: بايت ASCII ليس نصًا عربيًا مشفّرًا → `unknownByte`. -/
theorem decodeText_refuses_ascii :
    decodeText [0x41] = .error .unknownByte := rfl

/-- رفض ينتقل من طبقة البتات: ألفا اليونانية (0x3B1) ثم فتحة → `notArabicBlock`. -/
theorem decodeText_refuses_non_arabic :
    decodeText ([0x3B1, 0x64E].flatMap utf8Encode2) = .error .notArabicBlock := rfl

/-- الرفض ليس تشفيرًا لأي خلايا: ما يُرفض لا يساوي `encodeText` لأي قائمة خلايا. -/
theorem refused_not_encodeText (bs : List Byte) (r : Refusal) (h : decodeText bs = .error r) :
    ∀ cells : List Cell, encodeText cells ≠ bs := by
  intro cells heq
  rw [← heq, decodeText_encodeText] at h
  exact Except.noConfusion h

end Arabic
