/-
Arabic/Bits.lean — طبقة البتات: من البايتات إلى نقاط الترميز (Unicode) للكتلة العربية.

هذه أدنى طبقة في البرهان: تشفير UTF-8 ثنائي البايت وفكّه، مع رفض صريح
(`Refusal.unknownByte`) لأي بايت مشوّه، و(`Refusal.notArabicBlock`) لأي نقطة خارج 0x0600..0x06FF.
لا Mathlib؛ مكتبة Lean 4.19 القياسية فقط.
-/
import Arabic.Core

namespace Arabic

/-- البايت: متّجه من ثماني بتات. -/
abbrev Byte := BitVec 8

/-- تشفير UTF-8 لنقطة ترميز ذات بايتين (0x80 ≤ cp ≤ 0x7FF):
`110xxxxx 10xxxxxx`. -/
def utf8Encode2 (cp : Nat) : List Byte :=
  [BitVec.ofNat 8 (0xC0 ||| (cp >>> 6)), BitVec.ofNat 8 (0x80 ||| (cp &&& 0x3F))]

/-- فكّ زوج بايتات `110xxxxx 10xxxxxx` إلى نقطة ترميز؛ `none` إن فشل الفحص. -/
def decodePair (b1 b2 : Byte) : Option Nat :=
  if b1.toNat &&& 0xE0 = 0xC0 ∧ b2.toNat &&& 0xC0 = 0x80 then
    some (((b1.toNat &&& 0x1F) <<< 6) ||| (b2.toNat &&& 0x3F))
  else none

/-- فكّ تسلسل UTF-8 ثنائي البايت واحد من رأس القائمة.
يتحقق من بايت القيادة `110xxxxx` وبايت المتابعة `10xxxxxx`؛ وإلا `none`. -/
def utf8Decode2 : List Byte → Option (Nat × List Byte)
  | b1 :: b2 :: rest => (decodePair b1 b2).map (·, rest)
  | _ => none

/-- هل نقطة الترميز داخل الكتلة العربية 0x0600..0x06FF؟ -/
def inArabicBlock (cp : Nat) : Bool := 0x600 ≤ cp && cp ≤ 0x6FF

/-- فكّ قائمة بايتات كاملة إلى نقاط ترميز عربية، أو رفض مسمّى.
(استدعاء ذاتي بنيوي على القائمة؛ لذا يُحسب بـ `rfl`.) -/
def decodeAll : List Byte → Except Refusal (List Nat)
  | [] => .ok []
  | b1 :: b2 :: rest =>
    match decodePair b1 b2 with
    | none => .error .unknownByte
    | some cp =>
      if inArabicBlock cp then
        match decodeAll rest with
        | .ok cps => .ok (cp :: cps)
        | .error r => .error r
      else .error .notArabicBlock
  | [_] => .error .unknownByte

/-! ## المبرهنات -/

/-- بايت قيادة صالح: لكل `h < 32`، البايت `0xC0 + h` يجتاز الفحص ويعيد `h`. -/
theorem lead_byte_bits : ∀ h, h < 32 →
    (0xC0 + h) &&& 0xE0 = 0xC0 ∧ (0xC0 + h) &&& 0x1F = h := by decide

/-- بايت متابعة صالح: لكل `l < 64`، البايت `0x80 + l` يجتاز الفحص ويعيد `l`. -/
theorem cont_byte_bits : ∀ l, l < 64 →
    (0x80 + l) &&& 0xC0 = 0x80 ∧ (0x80 + l) &&& 0x3F = l := by decide

/-- الجولة البتّية الأساسية (على مستوى الزوج): فكّ بايتَي تشفير أي نقطة ثنائية البايت يعيدها.
برهان عام على كامل المدى 0x80..0x7FF (لا تعداد منتهٍ). -/
theorem decodePair_encode2 (cp : Nat) (h1 : 0x80 ≤ cp) (h2 : cp ≤ 0x7FF) :
    decodePair (BitVec.ofNat 8 (0xC0 ||| (cp >>> 6))) (BitVec.ofNat 8 (0x80 ||| (cp &&& 0x3F)))
      = some cp := by
  have hdiv : cp >>> 6 = cp / 64 := by
    rw [Nat.shiftRight_eq_div_pow]
  have hmod : cp &&& 0x3F = cp % 64 := by
    rw [show (0x3F : Nat) = 2 ^ 6 - 1 from rfl, Nat.and_two_pow_sub_one_eq_mod]
  have hhi : cp / 64 < 2 ^ 6 := by omega
  have hlo : cp % 64 < 2 ^ 7 := by omega
  have hlo6 : cp % 64 < 2 ^ 6 := by omega
  have e1 : 0xC0 ||| (cp / 64) = 0xC0 + cp / 64 := by
    have := Nat.two_pow_add_eq_or_of_lt hhi 3
    rw [show (0xC0 : Nat) = 2 ^ 6 * 3 from rfl, this]
  have e2 : 0x80 ||| (cp % 64) = 0x80 + cp % 64 := by
    have := Nat.two_pow_add_eq_or_of_lt hlo 1
    rw [show (0x80 : Nat) = 2 ^ 7 * 1 from rfl, this]
  have e3 : ((cp / 64) <<< 6) ||| (cp % 64) = cp := by
    rw [Nat.shiftLeft_eq, Nat.mul_comm, ← Nat.two_pow_add_eq_or_of_lt hlo6]
    show 64 * (cp / 64) + cp % 64 = cp
    omega
  obtain ⟨a1, a2⟩ := lead_byte_bits (cp / 64) (by omega)
  obtain ⟨b1, b2⟩ := cont_byte_bits (cp % 64) (by omega)
  simp only [decodePair, BitVec.toNat_ofNat, hdiv, hmod, e1, e2]
  rw [Nat.mod_eq_of_lt (by omega), Nat.mod_eq_of_lt (by omega), a1, a2, b1, b2, e3]
  simp

/-- الجولة البتّية الأساسية: فكّ تشفير أي نقطة ثنائية البايت يعيدها مع البقية.
برهان عام على كامل المدى 0x80..0x7FF. -/
theorem utf8Decode2_encode2 (cp : Nat) (h1 : 0x80 ≤ cp) (h2 : cp ≤ 0x7FF) (rest : List Byte) :
    utf8Decode2 (utf8Encode2 cp ++ rest) = some (cp, rest) := by
  simp only [utf8Encode2, List.cons_append, List.nil_append, utf8Decode2,
    decodePair_encode2 cp h1 h2, Option.map_some']

/-- كل بايت في تشفير نقطة ثنائية البايت له البت الأعلى مرفوعًا، فليس هو الفراغ 0x20.
هذا ما يسمح بالتقطيع على الفراغ دون التباس مع محتوى الكلمة. -/
theorem utf8Encode2_no_space (cp : Nat) (h2 : cp ≤ 0x7FF) :
    ∀ b ∈ utf8Encode2 cp, b ≠ (0x20 : Byte) := by
  have hdiv : cp >>> 6 = cp / 64 := by rw [Nat.shiftRight_eq_div_pow]
  have hmod : cp &&& 0x3F = cp % 64 := by
    rw [show (0x3F : Nat) = 2 ^ 6 - 1 from rfl, Nat.and_two_pow_sub_one_eq_mod]
  have hhi : cp / 64 < 2 ^ 6 := by omega
  have hlo : cp % 64 < 2 ^ 7 := by omega
  have e1 : 0xC0 ||| (cp / 64) = 0xC0 + cp / 64 := by
    have := Nat.two_pow_add_eq_or_of_lt hhi 3
    rw [show (0xC0 : Nat) = 2 ^ 6 * 3 from rfl, this]
  have e2 : 0x80 ||| (cp % 64) = 0x80 + cp % 64 := by
    have := Nat.two_pow_add_eq_or_of_lt hlo 1
    rw [show (0x80 : Nat) = 2 ^ 7 * 1 from rfl, this]
  have k1 : ∀ h, h < 64 → BitVec.ofNat 8 (0xC0 + h) ≠ (0x20 : Byte) := by decide
  have k2 : ∀ l, l < 64 → BitVec.ofNat 8 (0x80 + l) ≠ (0x20 : Byte) := by decide
  intro b hb
  simp only [utf8Encode2, List.mem_cons, List.not_mem_nil, or_false, hdiv, hmod, e1, e2] at hb
  rcases hb with rfl | rfl
  · exact k1 _ (by omega)
  · exact k2 _ (by omega)

/-- حجم التشفير ثابت: بايتان. -/
theorem utf8Encode2_length (cp : Nat) : (utf8Encode2 cp).length = 2 := rfl

/-- فكّ الكل بعد تشفير الكل: لأي قائمة نقاط داخل الكتلة العربية،
`decodeAll (cps.flatMap utf8Encode2) = .ok cps`. -/
theorem decodeAll_encode : ∀ cps : List Nat,
    (∀ cp ∈ cps, 0x600 ≤ cp ∧ cp ≤ 0x6FF) →
    decodeAll (cps.flatMap utf8Encode2) = .ok cps := by
  intro cps
  induction cps with
  | nil => intro _; rfl
  | cons cp cps ih =>
    intro hall
    have hcp := hall cp (List.mem_cons_self ..)
    have hrest : ∀ c ∈ cps, 0x600 ≤ c ∧ c ≤ 0x6FF :=
      fun c hc => hall c (List.mem_cons_of_mem _ hc)
    have hblk : inArabicBlock cp = true := by
      simp only [inArabicBlock, Bool.and_eq_true, decide_eq_true_eq]; omega
    rw [List.flatMap_cons]
    simp only [utf8Encode2, List.cons_append, List.nil_append, decodeAll,
      decodePair_encode2 cp (by omega) (by omega), hblk, ih hrest]
    simp

/-- رفض: بايت ASCII (`0x41` = `A`) ليس بايت قيادة ثنائي البايت. -/
theorem decodeAll_refuses_ascii_lead : decodeAll [0x41] = .error .unknownByte := rfl

/-- رفض: ألفا اليونانية (0x3B1) تُفكّ بنجاح لكنها خارج الكتلة العربية. -/
theorem decodeAll_refuses_non_arabic : decodeAll (utf8Encode2 0x3B1) = .error .notArabicBlock := rfl

/-- رفض: بايت متابعة وحيد بلا قيادة. -/
theorem decodeAll_refuses_lone_continuation : decodeAll [0xBF, 0x80] = .error .unknownByte := rfl

/-- رفض: بايت قيادة مقطوع (بلا متابعة). -/
theorem decodeAll_refuses_truncated : decodeAll [0xD8] = .error .unknownByte := rfl

end Arabic
