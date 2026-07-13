# 91 — Execution Gap Matrix (46 Items)

> Status: operational classification matrix.
> Scope: explicit mapping of 46 requested execution gaps into one of four states:
> `runtime-closed`, `law-only`, `proposal-only`, `not-started`.
> Snapshot date: 2026-07-13.

## 1) Status Vocabulary

```text
runtime-closed = implemented as bounded runtime surface in current repository state
law-only       = declared as ratified law boundary without runtime opening
proposal-only  = design/proposal surface; non-ratified or non-executable
not-started    = no dedicated ratified law/runtime surface for the requested item
```

## 2) Classification Method

```text
STATE_TRUTH_SOURCE_ORDER = docs/14 -> runtime(src/) + tests/ -> docs/80
NO_OVERCLAIM_RULE = runtime-closed here means bounded constitutional runtime,
                    not unrestricted linguistic totality
```

## 3) Matrix (46 Items)

| # | Gap Item | Status |
| --- | --- | --- |
| 1 | تعريف الوحدة الأولية التنفيذي النهائي | runtime-closed |
| 2 | جبر الصوت والمقطع والحدود (الصوتي الأساسي) | runtime-closed |
| 3 | إثبات "الحركة جسر" جبريًا | runtime-closed |
| 4 | إغلاق هندسة المقاطع | runtime-closed |
| 5 | الاستنفاد المحلي الرياضي (Relevant/termination/pruning) | not-started |
| 6 | قانون الحدود الكامل متعدد المستويات | not-started |
| 7 | الفصل الصارم Root/Stem/Base/Lemma | not-started |
| 8 | نظام الجذور المعتلة تفصيليًا | not-started |
| 9 | أبواب الفعل بناءً كاملًا | law-only |
| 10 | فصل الزمن/الصيغة/الجهة/الحدث | law-only |
| 11 | نظام المصدر | not-started |
| 12 | نظام الجامد بناءً مستقلًا | runtime-closed |
| 13 | إغلاق المشتقات | runtime-closed |
| 14 | إغلاق العدد | law-only |
| 15 | إغلاق التذكير والتأنيث | law-only |
| 16 | إغلاق المعرفة والنكرة | law-only |
| 17 | إغلاق اللواصق والضمائر والإحالة | law-only |
| 18 | مسار الحروف والمبنيات بالتفصيل | law-only |
| 19 | الممنوع من الصرف | not-started |
| 20 | الدخيل والمعرب | not-started |
| 21 | بناء المعجم الدستوري | law-only |
| 22 | إغلاق الوضع والاستعمال | law-only |
| 23 | التحكيم بين القراءات (CANDIDATE-ARBITRATION-K0) | proposal-only |
| 24 | إغلاق المراسي الأنطولوجية | runtime-closed |
| 25 | صلاحية الحمل Bearable(p,x) | not-started |
| 26 | جبر العلاقات الكامل | not-started |
| 27 | جبر الإحالة | law-only |
| 28 | بناء النسبة تنفيذيًا | runtime-closed |
| 29 | بناء الجملة الاسمية/الفعلية/شبه الجملة | runtime-closed |
| 30 | إغلاق الإعراب | runtime-closed |
| 31 | اقتران الدال والمدلول تنفيذيًا | runtime-closed |
| 32 | إغلاق المقام | runtime-closed |
| 33 | بناء الإفادة | runtime-closed |
| 34 | المنطوق/المفهوم/الاقتضاء/الإشارة (منظومة موحدة إضافية) | not-started |
| 35 | إغلاق الخبر والإنشاء | runtime-closed |
| 36 | بناء القضية والحكم | runtime-closed |
| 37 | إغلاق نظام الدليل | runtime-closed |
| 38 | بناء الرتبة حسابيًا | runtime-closed |
| 39 | التحقق الخارجي | law-only |
| 40 | عبور المجالات تنفيذيًا | not-started |
| 41 | إغلاق الاقتصاد الأرخميدي | runtime-closed |
| 42 | بروتوكول التعلم من الفشل | runtime-closed |
| 43 | إغلاق الإصلاح (Repair/Supersession/Rollback) | proposal-only |
| 44 | النسخ والتوافق بين الإصدارات | not-started |
| 45 | قابلية الإنهاء وكشف الدوران | proposal-only |
| 46 | مصفوفة التغطية (طبقات/مدخلات/مخرجات/فشل/بقايا) | runtime-closed |

## 4) Integrity Notes

```text
- This matrix is a state-truth snapshot, not a chain-amendment PR step by itself.
- Any future status flip must follow constitutional chain discipline and synchronized evidence.
```
