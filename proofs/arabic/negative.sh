#!/usr/bin/env bash
# ادعاءات نحوية خاطئة يجب أن يرفضها Lean: لو قُبل أحدها فالنموذج فارغ أو متساهل.
set -euo pipefail
cd "$(dirname "$0")"
export LEAN_PATH="$PWD/.lake/build/lib/lean"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
check_rejected() {
  local name="$1" body="$2"
  printf 'import Arabic\nopen Arabic\n%s\n' "$body" > "$tmp/$name.lean"
  if lean "$tmp/$name.lean" > "$tmp/$name.log" 2>&1; then
    echo "FAIL: false claim accepted: $name" >&2; cat "$tmp/$name.log" >&2; exit 1
  fi
  # الرفض يجب أن يكون حكمًا منطقيًا (القضية كاذبة / فشل rfl أو decide)، لا خطأ ترجمة عرضيًا.
  if ! grep -qE "is false|rfl' failed|decide' failed|unsolved goals" "$tmp/$name.log"; then
    echo "FAIL: $name rejected for an unexpected reason:" >&2; cat "$tmp/$name.log" >&2; exit 1
  fi
  echo "PASS: rejected $name"
}
# الجر للأفعال (خطأ)
check_rejected jarr_fil 'example : caseEnding .mudariSahih .jarr = some .kasra := by decide'
# إنّ ترفع اسمها (خطأ)
check_rejected inna_raf 'example : roleCase .ismInna = .raf := by decide'
# كان تنصب اسمها (خطأ)
check_rejected kana_nasb 'example : roleCase .ismKana = .nasb := by decide'
# المحلّل يقبل «إنّ زيدٌ قائمٌ» (خطأ)
check_rejected parse_inna_marfu 'example : (parse [inna, zaydun, qaimun]).toOption.isSome = true := by decide'
# مفهوم مخالفة بلا قيد (خطأ)
check_rejected mukhalafa_bila_qayd 'example (j : Jumla) : (mafahim ⟨none, [], none⟩ j).length = 1 := by simp [mafahim, muwafaqaOf, mukhalafaOf]'
# مفهوم اللقب (خطأ)
check_rejected laqab 'example : (mukhalafaOf ⟨some .laqab, [], none⟩ ⟨zaydun, .word qaimun, .ithbat⟩).length = 1 := by decide'
# فك بايت ASCII كخلية عربية (خطأ)
check_rejected ascii_cell 'example : (decodeText [0x41]).toOption.isSome = true := by decide'
# الألف الـ(Fin 0) والباء متطابقتان في الترميز (خطأ)
check_rejected carrier_collision 'example : carrierCodePoint ⟨0, by decide⟩ = carrierCodePoint ⟨1, by decide⟩ := by decide'
# خبر جملة بلا رابط يُقبل (خطأ)
check_rejected khabar_bila_rabit 'example : (parse [zaydun, qama, amrun]).toOption.isSome = true := by decide'
# اسم عادي منصوب + مجرور يُقبل ظرفًا (خطأ)
check_rejected ism_ka_zarf 'example : (parse [zaydun, qaiman, addari]).toOption.isSome = true := by decide'
# علامتان مختلفتان بخلية واحدة (خطأ)
check_rejected ending_collision 'example : endingCell .waw = endingCell .yaa := by decide'
# مضارع مجزوم الصيغة بلا جازم يُقبل فعلًا لجملة فعلية (خطأ)
check_rejected mudari_majzum_bila_jazim 'example : (parse [yaqum, zaydun]).toOption.isSome = true := by decide'
# مضارع منصوب الصيغة بلا ناصب يُقبل (خطأ)
check_rejected mudari_mansub_bila_nasib 'example : (parse [yaquma, zaydun]).toOption.isSome = true := by decide'
# مضارع موسوم بصنف اسمي يُقبل (خطأ)
check_rejected mudari_sinf_ismi 'example : (parse [yaqumuIsmi, zaydun]).toOption.isSome = true := by decide'
# الخبر الجملة يتساهل مع صيغة الفعل (خطأ)
check_rejected khabar_jumla_mudari_majzum 'example : (parse [zaydun, yaqum, hu]).toOption.isSome = true := by decide'
