# 58 — DalAlone Atomic Closure Law

> **Status:** Constitutional law document. Ratified in DAL-A0.
> Constitutional origin: docs/26 (DalOnlyCandidate Boundary Law),
> docs/47 (Post-Vertical Roadmap), docs/51 (Maʿqūl Branch Discipline Law),
> and docs/14 (PR Chain Roadmap Amendment-35).
>
> This document defines the **DalAlone Atomic Closure** boundary. It is
> law-only: it introduces no runtime code, no carriers, no enums, no
> operations, no adapter change, no audit change, and no global
> `FailureCode` expansion.
>
> Numbering note: docs/56 and docs/57 are already reserved in the roadmap
> for GPT reasonableness boundary documents, so this DAL law uses docs/58.

---

## §1 Governing principle

```text
No LafziMadlulGate before DalAloneClosed.
No DalAloneClosed without atomic sound / graphic / boundary closure.
No atomic closure with hidden residuals.
No signifier-alone closure may emit meaning, word kind, root, pattern,
ifādah, hukm, tanzīl, or reality.
```

`DalOnlyCandidate` proves that a signifier surface can stand as a
pre-semantic candidate. It does **not** by itself prove the atomic closure
needed before the verbal-signified gate.

This law inserts an explicit closure boundary:

```text
DalOnlyCandidate
  -> DalAloneAtomicClosure
  -> DalAloneClosed
  -> LafziMadlulGate
```

The boundary remains pre-semantic. It proves only that the signifier-alone
surface is atomically closed as a licensed sound / graphic sequence with
visible residuals.

---

## §2 Domain and non-domain

### §2.1 Domain

`DalAloneAtomicClosure` may inspect only the pre-semantic signifier surface:

```text
RawAcousticTrace
UnicodeTrace
GraphemeCandidate
LetterIdentity
PhoneticRealization
ArabicSoundCandidate
AtomicSoundUnit
SoundTransition
SyllableLicense
WaqfLicense
WaslLicense
UsageTrace
ResidualAudit
```

### §2.2 Non-domain

`DalAloneAtomicClosure` must not emit or infer:

```text
WordKind
Root
Pattern
LicensedWeight
LexicalMeaning
VerbalMadlulCandidate
DalMadlulBindingCandidate
RelationCandidate
IfadahCandidate
HukmCandidate
TanzilCandidate
Reality
Ontology
```

A successful closure opens only `LafziMadlulGate`; it does not cross it.

---

## §3 Required atomic gates

`DalAloneClosed` may be declared only after the following gates are passed
or leave visible non-blocking / deferred residuals:

```text
RawAcousticTraceGate
UnicodeNormalizationGate
SoundLetterGraphemeSeparationGate
ArabicSoundInventoryGate
MakhrajSifahMatrixGate
QadihSoundDifferenceGate
HarakaCarrierGate
MaddExtensionGate
HamzaResolutionGate
ShaddaIdghamGate
TanwinTraceGate
SukunCollisionGate
SyllableLicenseGate
InitialSukunGate
HamzatWaslGate
SoundTransitionMatrixGate
AdjacencyToSequenceGate
AtomicSoundCountingGate
S1_S5LicenseGate
WaqfLicenseGate
WaslLicenseGate
UsageBeforeMeaningGate
LoanArabizedGate
DeletionTraceGate
DalResidualAuditGate
```

These names are law names. A later runtime PR may implement them as helper
functions, transition contracts, dataclasses, or verdict wrappers, but it
must preserve their boundary meaning.

---

## §4 Raw trace before sound

```text
AcousticTrace != ArabicSound.
UnicodeTrace != ArabicSound.
Breath != Letter.
Noise != Letter.
```

`RawAcousticTraceGate` must distinguish at least:

```text
SILENCE
BREATH_ONLY
RAW_NOISE
LINGUISTIC_SOUND_CANDIDATE
ARABIC_SOUND_CANDIDATE
```

A sound may enter the Arabic branch only after `Makhraj`, `Sifah`,
`Repeatability`, `QadihDifference`, `EnergyProfile`, and `Trace` are
visible.

---

## §5 Graphic / letter / sound separation

The following chain is mandatory:

```text
UnicodeTrace
  -> GraphemeCandidate
  -> LetterIdentity
  -> PhoneticRealization
```

Forbidden shortcuts:

```text
UnicodeTrace -> ArabicSound
GraphemeCandidate -> PhoneticRealization
LetterIdentity -> Meaning
```

Examples that must remain unresolved until licensed:

```text
ا  may be alif madd, hamza seat, hamzat wasl, or graphic trace.
ى  may be graphic alif maqsurah, not a yāʾ sound.
ة  may project differently in waqf and wasl.
```

---

## §6 ArabicSoundInventory requirements

A later `ArabicSoundInventory` implementation must provide, for each
licensed sound:

```text
sound_id
makhraj
sifah tuple
qadih_difference tuple
energy_profile
trace_ref / license_ref
```

The initial inventory may be minimal and fixture-sized, but it must include
at least enough entries to distinguish:

```text
ب / م / ن / ء / ه
ا as madd or non-sound-bearing graphic support
و as consonant or madd
ي as consonant or madd
ة as wasl/waqf-sensitive graphic-letter identity
```

The inventory is not a lexicon and carries no meanings.

---

## §7 Hamza, shadda, tanwin, sukun, and madd

### §7.1 Hamza

`HamzaResolutionGate` must distinguish:

```text
HamzatQat
HamzatWasl
AlifMadd
SeatOfHamza
```

Unresolved hamza blocks `DalAloneClosed`.

### §7.2 Shadda

```text
Shadda = implicit closure + following realization.
```

A shadda must expand into a licensed doubled / idghām trace or remain a
visible residual. An unexpanded shadda blocks full closure.

### §7.3 Tanwin

Tanwīn is a waqf/wasl sound/graphic trace at this layer. It is not
indefiniteness, semantic use, or lexical meaning.

### §7.4 Sukun

Sukūn is a closure state, not mere absence. Internal sukūn, waqf sukūn,
original sukūn, and unlicensed collision must be separated.

### §7.5 Madd

Madd requires extension evidence. No madd may be inferred from fatha alone
without a licensed extension relation.

---

## §8 Syllable, transition, adjacency, and S1-S5 discipline

```text
CellSequence != DalAloneClosed.
WrittenAdjacency != PhoneticSequence.
S1/S2/S3/S4/S5 != Weight.
S1/S2/S3/S4/S5 != WordKind.
```

A later runtime PR must define `AtomicSoundUnit` before counting S1 through
S5. Counting must account for at least:

```text
carrier + haraka cell
madd extension
shadda expansion
tanwin wasl trace
hamzat wasl start/drop behavior
missing-vowel candidate sets
```

Every transition from one sound unit to the next must preserve trace,
qādih difference, and energy policy.

---

## §9 Waqf and wasl are structured gates

`WaqfLicense` is not a boolean. It must distinguish at least:

```text
final sukun projection
ta marbutah waqf projection
tanwin waqf projection
madd under waqf
ha al-sakt trace
hamza waqf treatment
```

`WaslLicense` is not a boolean. It must distinguish at least:

```text
sukun collision repair
hamzat wasl drop
idgham
izhar
wasl movement
deletion / lightening with visible residual
```

Missing waqf or wasl evidence prevents full closure.

---

## §10 Usage before meaning

`UsageBeforeMeaningGate` may determine only whether a phonetic/graphic
surface is used, unused, loan/arabized, symbolic, or unresolved.

It must not emit a lexical definition. It must not classify word kind. It
must not produce meaning.

```text
PhoneticLicense != LexicalUse.
LexicalUse != LexicalMeaning.
LoanArabizedPath != RootPath.
```

Unused or loan/arabized status may leave visible residuals and may block the
next gate, but it never licenses a semantic shortcut.

---

## §11 Local DAL residual vocabulary

DAL atomic residuals are local to this boundary unless a later law promotes
one into the global `FailureCode` taxonomy.

The required local vocabulary is:

```text
RAW_TRACE_NOT_SPEECH
MAKHRAJ_MISSING
SIFAH_MISSING
QADIH_SOUND_DIFF_MISSING
HARAKA_WITHOUT_CARRIER
MADD_WITHOUT_EXTENSION
SHADDA_UNEXPANDED
HAMZA_UNRESOLVED
WASL_HAMZA_UNRESOLVED
SUKUN_COLLISION
SYLLABLE_UNLICENSED
WAQF_UNTESTED
WASL_UNTESTED
UNVOCALIZED_SURFACE
PHONETIC_SEQUENCE_AMBIGUOUS
UNUSED_LAFZ
LOAN_PATH_REQUIRED
DELETION_UNLICENSED
ENERGY_COLLISION
```

Hard refusals map to existing global refusal names, including:

```text
GATE_REQUIRED
BOUNDARY_MISSING
TRACE_MISSING
IDENTITY_BROKEN
FORBIDDEN_STRAIGHT_LINE
```

No residual may be hidden to produce closure.

---

## §12 Closure contract

`DalAloneClosed` is licit only if:

1. raw trace / graphic trace / sound trace are separated;
2. every Arabic sound has visible makhraj and sifah evidence;
3. qādih difference is visible where confusion is possible;
4. every haraka has a carrier;
5. every madd has extension evidence;
6. shadda is expanded or blocks closure;
7. hamza is resolved or blocks closure;
8. sukūn collision is licensed or blocks closure;
9. syllable shape is licensed;
10. written adjacency has become a phonetic sequence;
11. S1-S5 counting has declared origin, branch, cause, condition,
    preventer, preserved trace, and new contribution;
12. waqf and wasl are both tested;
13. unvocalized surfaces remain candidate sets unless resolved by evidence;
14. usage / unused / loan status is visible before LafziMadlulGate;
15. deletion or estimation has trace and license;
16. every residual is visible;
17. no output crosses into word kind, meaning, composition, ifādah, hukm,
    or reality.

---

## §13 Runtime staging opened by this law

This law opens a later implementation sequence only after DAL-A0 is ratified:

```text
DAL-A1  carriers + local residual vocabulary
DAL-A2  raw trace / grapheme / letter / sound separation gates
DAL-A3  ArabicSoundInventory + makhraj/sifah/qādih matrix
DAL-A4  hamza / shadda / tanwin / sukun / madd gates
DAL-A5  syllable / transition / adjacency / S1-S5 gates
DAL-A6  detailed waqf / wasl closure
DAL-A7  usage / loan / unvocalized / deletion residual gates
DAL-A8  final DalAloneClosed -> LafziMadlulGate integration
```

Each later step must be separately staged in docs/14 before code ships.
DAL-A0 itself ships no runtime code.

---

## §14 Golden law

```text
DalOnlyCandidate is not enough for LafziMadlulGate.
DalAloneClosed is atomic closure, not meaning.
DalAloneClosed opens the verbal-signified gate only; it does not cross it.
No approved output with hidden DAL residuals.
```
