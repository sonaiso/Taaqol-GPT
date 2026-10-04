# 129 — LGE Staged Surface-to-Dalālah Bridge Licensing Law

> **Status:** Law-only constitutional bridge contract. It does not open runtime
> execution and does not displace the active `SLGE-SDLC-G0` successor position.
> **Branch:** `LGE-B0`.
> **Constitutional origin:** docs/15, docs/58–63, docs/70, docs/77, docs/79,
> docs/92 (proposal-only reference), docs/99–100, docs/110, and docs/14.

---

## §1 Governing law

```text
Linguistic layers are connected by licensed, typed, adjacent bridges.
Connection is not identity, entailment, or authority transfer.
No stage is exhausted beyond its declared domain and scope.
No next stage opens before the current stage is minimally complete.
No surface candidate alone establishes root, derivation, morphology, syntax,
dalālah, meaning, ifādah, ḥukm, truth, certainty, or reality.
```

This law provides a staged licensing contract for future bridge steps. It
integrates existing boundaries; it does not amend, replace, or merge their
runtime contracts.

## §2 Authority and current chain position

1. `docs/14_PR_CHAIN_ROADMAP.md` remains authoritative for chain order.
2. In the SLGE-SDLC lifecycle branch, `SLGE-SDLC-G0` remains the successor
   after `SLGE-SDLC-P0`; this law does not reorder, complete, or bypass it.
   It also does not displace the separately recorded `PR-F` position.
3. `docs/92_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_SLOTS_90_113.md` remains a
   proposal-only reference and grants no authority.
4. This law admits only the bridge contract and staged successor proposals
   below, including the bounded bit/letter/haraka refinement in §4A.
   Every executable bridge requires its own chain admission, law-specific tests,
   and runtime-admission evidence under docs/110.
5. Until that admission, every bridge below is a specification boundary, not an
   executable permission or verdict.

## §3 Shared bridge contract

Every bridge `Bᵢ: X → Y` MUST declare and preserve:

```text
OriginLaw
BranchAndChainPosition
InputContract
OutputContract
DomainAndScope
IdentityPropertyPreserved
EvidenceContract
TraceRef
RankCeiling
ResidualPolicy
MinimumCompleteRequirement
ForbiddenOutputsAndShortcuts
ForwardReadiness
BackwardReconstruction
```

Where the governing layer defines a scalar rank, output rank MUST NOT exceed the
meet of upstream rank, evidence rank, gate rank, and the applicable residual
ceiling. Lexical transitions MUST preserve the independent `RankVector` channels
required by docs/100; a scalar rank cannot replace them, and channel-wise
authority may not exceed its corresponding licensed inputs. Every upstream
residual MUST be inherited, resolved, transformed, or superseded with a
trace-visible disposition. Missing evidence, identity continuity, trace, or
declared scope blocks the bridge.

`MCE` means minimum-complete evidence for the declared scope, not universal
exhaustion. A stage is exhausted only when its declared finite inventory or
bounded domain has been covered, required counterexamples and inverse cases
have been tested, alternatives and unresolved cases remain visible as residuals,
and backward reconstruction and forward readiness are recorded. An open-ended
domain cannot claim exhaustion by enumeration.

## §4 Staged bridge registry

The following sequence is an admission order, not a claim that each output
logically entails the next. Each row is a separate branch boundary; any
unlisted shortcut is refused.

| Step | Bridge and licensed input | Required evidence / MCE | Permitted effect | Boundary and downstream condition |
| --- | --- | --- | --- | --- |
| `LGE-B1` | Encoded representation → Unicode/text-trace candidate | Encoding declaration, decoder/version and byte-to-code-point trace; malformed and ambiguous sequences tested | Reconstructible textual representation candidate | Text is not Arabic letter, sound, or meaning; require `LGE-B2` |
| `LGE-B2` | Unicode/text-trace → orthographic/grapheme candidate | Normalization policy, code-point/grapheme mapping, source-preserved spelling, and confusable/normalization countercases | Bounded grapheme and spelling-form candidates | Grapheme is not phoneme, root, or lexical identity; require `LGE-B3` for sound claims |
| `LGE-B3` | Orthographic candidate ↔ phonetic realization candidate | Independently sourced acoustic trace and sound/letter separation evidence; missing or conflicting signal remains visible | Paired, trace-linked orthographic and phonetic candidates | Text alone cannot prove sound and sound alone cannot prove spelling; require `LGE-B4` for atomic sequence closure |
| `LGE-B4` | Licensed letter/haraka and sound candidates → atomic signifier sequence | Applicable DAL gates for grapheme, letter, sound, haraka, syllable, adjacency, waqf/wasl, usage, and residual audit; test all declared in-scope forms and boundary cases | Bounded atomic signifier closure candidate | No word kind, root, pattern, or meaning; the current 29×4 inventory is bounded to 116 forms, and extensions require their own admitted evidence and scope |
| `LGE-B5` | Closed atomic signifier + independently licensed stem evidence → stem/root candidate | G₀ anchor conditions for bare jamid; root-specific source and identity evidence for root claims; competing segmentations and weak/ambiguous cases retained | Bare-stem identity candidate or separately bounded root candidate | A G₀ jamid anchor is not a general root certificate; no root from surface resemblance or syllable alone |
| `LGE-B6` | Licensed stem/root candidate → derivational candidate | Declared base identity, derivational operation, formal evidence, inverse/reconstruction case, and bounded competing analyses | Candidate derivational form/path | No derived-form semantics, agent/patient actuality, or productivity claim beyond scope |
| `LGE-B7` | Stem/derivation candidate → morphological candidate | Dedicated morphology law, declared paradigm and feature scope, form/inflection evidence, counterexamples, and residual audit | Bounded morphological candidate | This law supplies no morphology classifier; no syntactic role, meaning, or hukm |
| `LGE-B8` | Closed token/morphology candidates → formal composition/syntax candidate | Licensed constituent identities, adjacency/order and relation evidence, composition MCE, and preservation of all source traces/residuals | Formal sentence/relation candidate under existing LGE-C2…C5 and applicable formal-shape laws | Surface composition only; no proposition, entailment, or semantic closure |
| `LGE-B9` | Closed signifier and licensed lexical inputs → Dal-alone / lafẓī / wadʿī / coupled dalālah stages | Apply docs/58–62 in their exact order, with their required gates, evidence, domain/scope, and residual audits | Only the candidate/closure surface authorized by the specific governing law at that stage | No direct surface-to-dalālah jump; no ifādah, mafhūm, ḥukm, truth, certainty, or reality beyond the separately governed chain |

The relation between singleton and composition is a bounded graph: each
constituent first retains its own identity and scope, then composition receives
only the licensed constituent candidates it declares. Composition does not
retroactively prove a constituent, erase its residuals, or collapse its identity
with neighboring constituents.

## §4A Per-bit values and the 29 × 4 surface grid

### §4A.1 Bit valuation contract

Every observed bit is assigned its representational value, not a linguistic
meaning:

```text
BitObservation = <
  source_ref,
  encoding_id,
  encoding_version,
  byte_offset,
  bit_index,
  bit_order,
  value ∈ {0, 1},
  trace_ref,
  residuals
>
```

The bit index is interpreted only under the declared encoding's bit-order
convention. No bit value, byte value, bit pattern, or binary resemblance alone
licenses Unicode, a grapheme, an Arabic letter, a haraka, a sound, or meaning.
Byte/code-unit decoding is a separate, encoding-specific bridge and must retain
reconstructible source offsets.

For a declared finite input, bit-stage MCE requires every source bit position to
be accounted for exactly once, values to be only `0` or `1`, the encoding and
bit order to be explicit, and the full source span to be reconstructible. This
exhausts only that declared input span under that encoding; it does not exhaust
the encoding standard or all possible bitstreams. Missing positions, duplicate
positions, unknown encoding, or ambiguous bit order block or defer the bridge
with visible residuals.

### §4A.2 Licensed adjacency for representation, writing, and sound

The bounded representational order is:

```text
ObservedBit(0|1)
  -> DeclaredByteOrCodeUnit
  -> UnicodeCodePointCandidate
  -> OrthographicGraphemeCandidate
  -> ArabicLetterCandidate / HarakaCandidate
  -> IndependentlyEvidencedSoundCandidate
```

Each arrow is a distinct evidence-bearing handoff under §3 and the applicable
stage in §4. In particular:

- bits combine into bytes/code units only under their declared encoding;
- code units decode to code-point candidates only under that encoding;
- normalization/grapheme segmentation preserve both normalized and source
  identities and their mapping trace;
- sound claims require sound evidence independent of the textual bitstream;
- no adjacent handoff treats textual evidence as acoustic evidence or vice versa.

These are licensed contract shapes, not runtime admission. This sequence neither
changes the current 116 forms nor opens the stages in code.

### §4A.3 Separate 29-letter and four-haraka inventories

The currently declared LGE-C1 inventory consists of exactly 29 letter candidates,
with hamza and alif maintained as distinct entries, and four separately
identified mark candidates:

```text
Letters = (L₁, …, L₂₉)
Harakat = (H₁, H₂, H₃, H₄)
H = {fatḥah, ḍammah, kasrah, sukūn}
```

Each member requires its own stable identity, source/evidence reference,
trace, rank ceiling, and visible residuals. An ordinal is an index, not
linguistic evidence. This law assigns no sound value to a letter or mark by
index alone. Introducing a new letter or mark is outside this closed inventory
and requires its own separately admitted scope, evidence, and tests before it
can participate in a licensed product.

### §4A.4 Product bridge and exhaustion

Only after the letter inventory (29/29) and mark inventory (4/4) independently
meet their declared MCE may the bounded product bridge be proposed:

```text
LetterHarakaGrid = Letters × Harakat
|LetterHarakaGrid| = 29 × 4 = 116
GridEntry(i, j) = <letter_ref=Lᵢ, haraka_ref=Hⱼ, pair_ref, trace_ref, residuals>
```

Grid MCE requires all and only 116 ordered pairs, each pair appearing exactly
once; stable references back to both independently licensed members; traceable
generation order; and visible residuals. Tests must prove 29 distinct letters,
four distinct marks, 116 unique pairs, no omissions, no duplicates, and refusal
of any unlicensed member. This is finite-inventory exhaustion for this declared
grid only; it proves neither pronunciation, syllabification, wordhood, nor any
downstream linguistic property. The arithmetic formula `N × M` licenses a
size check only after `N` and `M` are independently admitted; it cannot authorize
expanding either set.

## §5 Waqf, waṣl, and stage closure

Waqf and waṣl are explicit boundary conditions of the applicable sound/sequence
stage, not punctuation-based permission to skip closure:

1. Waqf closes only the declared utterance boundary supported by its evidence.
2. Waṣl preserves a traceable adjacency relation and does not fuse distinct
   letter, word, or identity carriers.
3. A missing, conflicting, or out-of-scope boundary is blocked or deferred with
   visible residuals.
4. Neither condition promotes a candidate into a word, root, syntactic role, or
   meaning.

## §6 Admission and exhaustion gate

A successor stage may be proposed only after its immediate predecessor has:

1. passed its declared MCE tests for the bounded domain and scope;
2. preserved input identity and a backward-reconstructible trace;
3. dispositioned every inherited residual visibly;
4. passed positive, negative, counterexample, inverse, and forbidden-shortcut
   tests;
5. declared output rank ceiling and forward readiness for exactly the next
   admitted stage; and
6. received its own chain position and runtime admission, where runtime is
   proposed, under docs/14 and docs/110.

Passing these conditions does not authorize skipping a stage. Refusal is named
with the applicable existing `FailureCode`; this law adds no global failure or
residual vocabulary.

## §7 Forbidden transitions

At minimum, the following remain refused unless a distinct law and admitted
runtime explicitly establish the exact bridge:

```text
Bytes -> ArabicLetter
Text / Unicode -> Sound
Grapheme -> Phoneme
LetterHaraka -> Word
Syllable -> Root
SurfaceResemblance -> Root
JamidAnchor -> DerivedMeaning
Derivation -> MorphologyClosure
Morphology -> SyntacticRole
FormalComposition -> Dalalah
SurfaceToken / SentenceSlot -> Meaning
DalAloneClosed -> Wad'iMadlulClosed
DalalahCandidate -> Ifadah / Hukm / Truth / Certainty / Reality
```

No bridge may bypass its immediate predecessor, infer a missing layer, turn
formal classification into semantic proof, or treat finite in-scope exhaustion
as universal linguistic completeness.

## §8 Scope exclusions

This law is law-only. It introduces no runtime code, carriers, enums, parser,
root detector, derivational or morphological analyzer, syntax engine, semantic
engine, DAL/LAFZI gate, adapter/audit change, or new global failure/residual
kind. It does not activate any `LGE-B1…LGE-B9` runtime stage, modify the 116
surface inventory, change the order of docs/58–62, or claim branch/runtime
closure.

## §9 Constitutional tests and trace

Tests for this law must establish:

- the stage registry covers encoding, orthography, sound, atomic signifier,
  stem/root, derivation, morphology, formal composition, and staged dalālah;
- each observed bit has a trace-bound value in `{0,1}` under an explicit
  encoding and bit-order declaration, without a direct bit-to-language jump;
- the 29-letter and four-haraka inventories are separately identified before
  their exact, duplicate-free 116-pair product is licensed;
- each stage declares input, evidence, effect, residual/rank/MCE boundary;
- current chain position and law-only/runtime-admission separation are explicit;
- waqf/waṣl, singleton/composition, inherited residuals, rank ceilings, and
  forbidden shortcuts are preserved; and
- docs/14, docs index, and `CLAUDE.md` record this law without claiming any
  runtime opening.

```text
docs/15 + docs/58–63 + docs/70 + docs/77 + docs/79 + docs/99–100
→ docs/129
→ tests/test_lge_staged_bridge_licensing_law.py
→ docs/14 → docs/README.md → CLAUDE.md
```
