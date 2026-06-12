# 14 — PR Chain Roadmap

> **Status:** Constitutional law. Ratified in PR-1B. Amended by
> Amendment-1 (§2 — Amendment record), which appends PR-7 and PR-8.
> Amended by Amendment-2 (§2), which appends the Arabic Weight
> Boundary branch (PR-9 through PR-13). Amended by Amendment-3
> (§2), which inserts PR-9A (Pre-Weight Licensing Law) and
> re-stages the branch as PR-9 through PR-14.
> This file is the authoritative chain of pull requests. The
> [Constitutional PR Geometry](13_CONSTITUTIONAL_PR_GEOMETRY.md) binds
> every PR to declare its position in this chain. A PR that
> implements work belonging to a later position is a
> `FORBIDDEN_LEAP`, regardless of CI status.

The chain is intentionally narrow. Each step exists to make the next
step reviewable, not to deliver standalone value.

```text
PR-0    Scaffold + Constitution                            ✓ done
PR-1A   Mathematical Slot Geometry Constitution            ✓ done
        + minimum carrier enums
PR-1B   Constitutional Test Geometry                       ✓ done
        + Constitutional PR Geometry
        + PR template + roadmap
PR-1C   Pre-SlotGraph constitutional closure               ✓ done
        + docs 15 (Textual Communication Entry Law)
        + docs 16 (Identity-to-Truth Licensing Chain)
        + docs 17 (SlotGraph Generation Law)
        + ConstitutionalChainTestCase (schema only)
PR-2    SlotGraph + GammaClosure minimal implementation    ✓ done
        (Rank / Residual carriers wired into the kernel)
PR-2A   Harden SlotGraph construction against              ✓ done
        constitutional gaps (corrective PR;
        Copilot review on PR-2 — no new layer)
PR-3    RankLattice + ResidualPolicy + EvidenceContract    ✓ done
PR-4    TransitionGate + FailureTaxonomy bindings          ✓ done
PR-5    Forbidden Straight-Line Registry                   ✓ done
        (+ technical-terminology non-confusion cases)
PR-6    AnswerAudit wrapper                                ✓ done
        (ModelClient protocol only — no adapters)
PR-6.1  Harden AnswerAudit trace coherence                 ✓ done
        + source hygiene fallback (corrective PR;
        post-merge judgment on PR-6 — no new layer)
PR-7    Adapter Boundary Law                               ✓ done
        (docs/18 — law only; licenses concrete
        ModelClient adapters; no code, no adapter)
PR-8    First concrete ModelClient adapter                 ✓ done
        (first adapter behind the docs/18 boundary;
        FORBIDDEN_LEAP before docs/18 is ratified)
PR-8.1  Harden AdapterGuard static judging purity          ✓ done
        (corrective PR; post-merge Copilot review
        on PR-8 — no new layer)
PR-9    Arabic Weight Boundary Law                         ✓ done
        (docs/19 — law only; Weight → PatternSpace,
        not Meaning; no Arabic code, no lexicon)
PR-9A   Pre-Weight Licensing Law                           planned
        (docs/20 — law only; the syllable →
        weight-readiness licensing chain; weigh()
        operates only on its output; no code)
PR-10   Weight + pre-weight carrier surface                planned
        (carriers only: WeightImage, Mizan,
        MawzunCandidate, SlotAlignment, plus the
        docs/20 carriers SyllableCandidate through
        WeightReadinessCandidate)
PR-11   Pre-weight path gates                              planned
        (μ_path_gate before any weighing — Root /
        Jamid / Mabni / Operator / ProperName /
        Borrowed / Residual candidate paths only —
        no final lexicon)
PR-12   Pre-weight licensing chain operations              planned
        (μ_seq → μ_boundary → μ_word_carrier →
        μ_root_stem → μ_original_extra → μ_ops →
        μ_weight_readiness — gated, named refusals)
PR-13   Minimal WeightFit operation                        planned
        (weigh(WeightReadinessCandidate, ...) →
        WeightFitCandidate or a named Refusal — fit
        only, never meaning)
PR-14   Lexical / Samāʿ / Qiyās License Boundary           planned
        (lexical, samāʿ, and qiyās licensing before
        any semantics)
```

## 1. Per-step boundary summary

```text
PR-0
    Origin   : "A repository must declare its laws before its code."
    Output   : repository scaffold, top-level constitutional docs.
    Forbidden: any executable kernel.

PR-1A
    Origin   : "SlotGeometry is a constitutional mathematical object."
    Output   : docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md
               + minimum carrier enums (ClosureState, FailureCode,
               Rank, Residual, ResidualKind).
    Forbidden: SlotGraph, gamma, TraceLedger, TransitionGate.

PR-1B
    Origin   : "No PR without origin/branch/chain;
                no test without origin/branch/chain."
    Output   : docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md,
               docs/13_CONSTITUTIONAL_PR_GEOMETRY.md,
               docs/14_PR_CHAIN_ROADMAP.md,
               tests/support/constitutional_case.py,
               minimal harness tests proving schema rules,
               .github/pull_request_template.md,
               CLAUDE.md updates.
    Forbidden: any new runtime behavior; SlotGraph; gamma;
               TransitionGate; LLM adapters; Arabic code.

PR-1C (this PR)
    Origin   : "No SlotGraph from a raw value;
                no text without a communicative entry boundary;
                no internal processing without the
                identity-to-truth licensing chain;
                no partial test pass is a constitutional pass."
    Output   : docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md,
               docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md,
               docs/17_SLOTGRAPH_GENERATION_LAW.md,
               docs/12 § 9 (ChainTestCase),
               tests/support/constitutional_case.py
                   (ConstitutionalChainTestCase, schema only),
               CLAUDE.md and PR template updates that bind PR-2
               to these laws.
    Forbidden: any executable kernel; SlotGraph; Slot; gamma;
               TransitionGate; EvidenceContract; TraceLedger;
               any new src/ module beyond what already exists;
               new src/taaqqul_slot_geometry/ logic;
               LLM adapters; lexicons; Arabic linguistic code;
               new runtime dependencies.
    Binding  : Any PR-2 attempt opened before this PR is merged,
               or that does not honor docs 15, 16, 17, is a
               FORBIDDEN_LEAP regardless of CI status.

PR-2
    Origin   : Mathematical Slot Geometry Laws sections 1–4.
    Output   : SlotGraph, Slot, Center, Boundary, gamma()
               returning a GammaResult with a TraceEntryCandidate.
    Forbidden: TransitionGate emission; rank promotion;
               forbidden-line registry; LLM adapters; Arabic code.

PR-2A
    Origin   : "Construction refusals must be named and complete"
               — docs/17 §§2–3 + §5 totality, docs/15 §5, docs/12.
    Output   : SlotBoundary refuses empty refusal_codes;
               OpeningPolicy refuses empty allowed_potentials;
               TraceRef refuses empty anchor;
               Center requires non-empty identity_claim + real
               TraceRef; EntryBoundary carries the full docs/15 §5
               surface (representation/ontological/sound/meaning
               status + prior_trace_status + produces_only);
               SlotGraph.center mandatory; entry_boundary required
               when generation_source is DECLARED_ENTRY; named
               construction surface SlotGraph.construct(...) →
               ConstructionResult with FailureCode for every
               presence-level row of docs/17 §3.
    Forbidden: RankLattice policy; ResidualPolicy engine;
               EvidenceContract; TransitionGate; Forbidden
               Straight-Line Registry; AnswerAudit; Arabic code;
               lexicons; LLM adapters; new FailureCode members;
               changes to gamma's verdict semantics; gamma side
               effects; TraceLedger imports from gamma; TypeError
               as a constitutional refusal.

PR-3
    Origin   : Mathematical Slot Geometry Laws sections 5–7
               (Rank, Residual, Evidence).
    Output   : RankLattice with bounded meet/join;
               ResidualPolicy enforcing visibility;
               EvidenceContract carriers.
    Forbidden: TransitionGate emission; forbidden-line registry;
               LLM adapters; Arabic code.

PR-4
    Origin   : Mathematical Slot Geometry Laws section 8 + docs/08.
    Output   : TransitionGate; FailureTaxonomy bindings;
               named refusals everywhere previously promised.
    Forbidden: forbidden-line registry; LLM adapters; Arabic code.

PR-5
    Origin   : docs/04 + docs/10.
    Output   : Forbidden Straight-Line Registry; technical
               terminology non-confusion cases.
    Forbidden: LLM adapters; Arabic code beyond the constitutional
               cases listed in docs/09.

PR-6
    Origin   : docs/01 (black-box boundary).
    Output   : AnswerAudit wrapper that consumes the kernel
               via a ModelClient protocol.
    Forbidden: any concrete adapter (OpenAI, Anthropic, local).
               Concrete adapters require a separate post-PR-6
               milestone.

PR-6.1
    Origin   : "No verdict is licensed with a trace candidate that
               contradicts it in rank, failure, or gamma/gate
               state" — docs/07 (PR-6 trace split) + docs/12;
               post-merge judgment on PR-6 (corrective PR;
               no new layer).
    Output   : TransitionVerdict birth guard mirrors every
               verdict-owned snapshot field (consulted_gamma_state,
               snapshot_failure, snapshot_rank — beyond the PR-6
               stage / gate_transition_state checks);
               deterministic git-free fallback for the source
               hygiene guard's tracked-file enumeration;
               ratified PR-6 Trace-Coherence Law (docs/07 —
               PR-6.1 binding: a gate trace record is evidence
               of the verdict, not a second authority).
    Forbidden: concrete adapters; network; persistence; Arabic
               application layer; ModelClient protocol changes;
               new runtime dependencies; any functional expansion
               of gate, emitter, or audit semantics.

PR-7
    Origin   : docs/01 (black-box boundary) + the PR-6 forbidden
               surface above ("Concrete adapters require a separate
               post-PR-6 milestone"); chain position ratified by
               Amendment-1 (§2).
    Output   : docs/18_ADAPTER_BOUNDARY_LAW.md — the Adapter
               Boundary Law that licenses concrete ModelClient
               adapters under the shape
               ModelClient protocol → ConcreteAdapterCandidate →
               AdapterGuard → AuditedAnswer only.
               Law only: no executable adapter ships here.
    Forbidden: any concrete adapter (OpenAI, Anthropic, local);
               any src/ or tests/ behavior change; network;
               persistence; schema expansion (TraceEntryCandidate
               stays as ratified in docs/07); the deferred
               Hypergraph / Residual-History branch (§2); Arabic
               code; new runtime dependencies.
    Binding  : No docs/18 content may ship before Amendment-1 is
               merged, and no adapter code before docs/18 is
               ratified. Violations are FORBIDDEN_LEAP regardless
               of CI status.

PR-8
    Origin   : docs/18 (once ratified by PR-7) + docs/01.
    Output   : the first concrete ModelClient adapter, behind the
               docs/18 boundary; the adapter yields raw answers to
               AnswerAudit, and AuditedAnswer remains the only
               output surface.
    Forbidden: adapter emitting verdicts; adapter bypassing
               AnswerAudit; adapter writing the TraceLedger;
               adapter emitting successor graphs; adapter deciding
               APPROVED; rank promotion outside a TransitionGate;
               network or persistence beyond what docs/18
               explicitly licenses; a second adapter; Arabic
               application layer; schema expansion; runtime
               dependencies beyond what docs/18 explicitly
               licenses.
    Binding  : Any PR-8 attempt opened before docs/18 is ratified
               is a FORBIDDEN_LEAP regardless of CI status.

PR-8.1
    Origin   : docs/18 §7 ("admission is structural — the guard
               never executes adapter code while judging") +
               post-merge Copilot review on PR-8 (corrective PR;
               no new layer).
    Output   : AdapterGuard resolves every judged name statically
               (inspect.getattr_static over the instance and MRO
               __dict__ mappings) — adapter-authored
               __getattribute__ / __getattr__ / descriptor __get__
               never run while the guard is judging; tripwire
               constitutional tests (a detonating metaclass,
               detonating descriptors, and a __dict__-hiding hook
               all stay cold); ratified docs/18 §7 PR-8.1 binding
               (a computed transport is not a declaration; a name
               synthesised only by dynamic lookup is not a
               structural surface).
    Forbidden: any change to the docs/18 §3 refusal rows, their
               FailureCodes, or their order; ModelClient protocol
               changes; kernel, gate, or audit semantics changes;
               a second adapter; new transports; network;
               persistence; Arabic application layer; new runtime
               dependencies.

PR-9
    Origin   : docs/04 (forbidden lines Root → LexicalMeaning,
               Weight → Agency) + docs/09 ("a separate proposal
               may open the door to a first Arabic application");
               chain position ratified by Amendment-2 (§2).
    Output   : docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md — the Arabic
               Weight Boundary Law. Law only: no code ships here.
               Center: weight does not mean — weight images. A
               weight maps into PatternSpace, not into Meaning;
               alignment yields a WeightFitCandidate, never
               Meaning, Agency, Hukm, or Reality; root does not
               yield Reality; fāʿil does not yield Agency; mafʿūl
               does not yield Patienthood; maṣdar does not yield
               RealEvent.
    Forbidden: any Arabic linguistic code; lexicons, root tables,
               pattern tables; weight carriers (WeightImage,
               Mizan, MawzunCandidate, SlotAlignment); any
               weigh()/alignment operation; semantics; ontology;
               hukm; adapter or audit layer changes; kernel,
               gate, or schema changes; new runtime dependencies.
    Binding  : No docs/19 content may ship before Amendment-2 is
               merged, and no Arabic weight code before docs/19
               is ratified. Arabic weight code never enters the
               adapter or audit layers. Violations are
               FORBIDDEN_LEAP regardless of CI status.

PR-9A
    Origin   : docs/04 (Pronunciation → Syllable and Syllable →
               Word are forbidden straight lines with declared
               bridges) + docs/09 + docs/19 (once ratified by
               PR-9); chain position ratified by Amendment-3
               (§2).
    Output   : docs/20_PRE_WEIGHT_LICENSING_LAW.md — the
               Pre-Weight Licensing Law. Law only: no code ships
               here. Center: nothing enters the Mīzān without a
               completed pre-weight licensing chain — Syllable →
               SyllableSequence → WordBoundary → WordCarrier →
               PathGate → RootStem / non-root path →
               OriginalExtra → OperationTrace → WeightReadiness.
               Every stage is a licensed branch-of-origin
               (condition, cause, no preventer, jāmiʿ ʿilla,
               effective attribute, no defeating difference)
               with preserved trace, visible residuals, bounded
               rank, and a named FailureCode on refusal; weigh()
               is licensed to operate only on a
               WeightReadinessCandidate.
    Forbidden: any Arabic linguistic code; weight or pre-weight
               carriers; μ operations; path gates; lexicons,
               root tables, pattern tables; new FailureCode
               members; new forbidden-line registry rows;
               semantics; ontology; hukm; adapter or audit layer
               changes; kernel, gate, or schema changes; new
               runtime dependencies.
    Binding  : No docs/20 content may ship before Amendment-3 is
               merged, and no pre-weight code before docs/20 is
               ratified. Once docs/20 is ratified, weighing any
               input other than a WeightReadinessCandidate is a
               forbidden leap. Violations are FORBIDDEN_LEAP
               regardless of CI status.

PR-10
    Origin   : docs/19 + docs/20 (once ratified by PR-9 and
               PR-9A) + docs/11 (carrier discipline — no
               reserved name bound to a free container).
    Output   : the weight + pre-weight carrier surface —
               carriers only: WeightImage, Mizan,
               MawzunCandidate, SlotAlignment (docs/19), plus
               the docs/20 pre-weight carriers:
               SyllableCandidate, SyllableSequenceCandidate,
               WordBoundaryCandidate, WordCarrierCandidate, the
               PathCandidate family, RootStemCandidate,
               OriginalExtraMap, OperationTraceCandidate,
               WeightReadinessCandidate — each carrying value,
               type, origin, identity, domain, scope, rank,
               residuals, trace. Frozen carriers that depict
               structure; no operation, no fit computation, no
               meaning field.
    Forbidden: weigh()/alignment operations; μ operations; path
               gates; lexicons; meaning, agency, hukm, or
               reality fields on any carrier; binding reserved
               names to free containers; adapter or audit
               changes; kernel semantics changes; new runtime
               dependencies.

PR-11
    Origin   : docs/20 §7 (the path gate precedes the root) +
               docs/19 + docs/08 (gates own transitions);
               re-staged before weighing by Amendment-3 (§2).
    Output   : the pre-weight path gates — μ_path_gate emitting
               candidate paths only: Root (mushtaqq), Jamid,
               Mabni, Operator, ProperName, Borrowed, Residual.
               Each path sits behind a TransitionGate with named
               refusals; no path is a verdict, no path is a
               meaning, and a stronger competing path is a named
               preventer, never a silent override.
    Forbidden: a final lexicon; semantic assignment; hukm;
               ontology; root/stem extraction; original/extra
               split; weighing; any path that bypasses a
               TransitionGate; adapter or audit changes; new
               runtime dependencies.

PR-12
    Origin   : docs/20 §§4–11 (the eight-stage pre-weight
               licensing chain) + docs/04 (Pronunciation →
               Syllable and Syllable → Word open here as
               licensed bridges, never as shortcuts).
    Output   : the pre-weight licensing chain operations —
               μ_seq, μ_boundary, μ_word_carrier, μ_root_stem,
               μ_original_extra, μ_ops, μ_weight_readiness.
               Pure functions; every transition behind a
               TransitionGate; every refusal a named
               FailureCode; deferral and blockage are named
               verdicts, never silent None; pass-with-residual
               is closure with visible residuals, never a new
               verdict kind; samāʿ-grounded preventers stay
               DEFERRED residuals until PR-14.
    Forbidden: weighing; meaning; semantics; hukm; ontology;
               synthesising a missing boundary, carrier, center,
               or trace; erasing an underlying form (operations
               preserve the path of transformation); lexicons;
               adapter or audit changes; new runtime
               dependencies.

PR-13
    Origin   : docs/19 + docs/20 (weigh() operates only on the
               output of the pre-weight algebra) + docs/04
               (Weight → Agency stays gated).
    Output   : the minimal WeightFit operation —
               weigh(WeightReadinessCandidate, ...) →
               WeightFitCandidate or a named Refusal
               (FailureCode). Pure function; fit only: the
               candidate carries pattern-space fit, never
               meaning, agency, patienthood, real events, or
               hukm. The only licensed input is a
               WeightReadinessCandidate.
    Forbidden: weighing a raw word, surface, syllable, or any
               carrier other than a WeightReadinessCandidate;
               meaning/agency/hukm/reality output; silent None;
               bare exceptions for expected verdicts; rank
               promotion outside a TransitionGate; lexicons;
               path gates; adapter or audit changes; new runtime
               dependencies.

PR-14
    Origin   : docs/19 + docs/20 + docs/04 and docs/09
               (LexiconEntry → Candidate is a forbidden straight
               line).
    Output   : the Lexical / Samāʿ / Qiyās License Boundary —
               lexical, samāʿ (attested usage), and qiyās
               (analogy) licenses placed before any semantics;
               an unlicensed entry is refused with a named
               FailureCode; the samāʿ-grounded preventers left
               DEFERRED by PR-11 and PR-12 close here.
    Forbidden: semantics / dalālah output; ontology; hukm;
               treating a lexicon entry as a candidate without a
               license; adapter or audit changes; new runtime
               dependencies.
```

## 2. Amendment discipline

```text
The only licit way to change this chain is an Amendment PR
whose entire branch is the chain change itself.
```

An Amendment PR is bound by
[`13_CONSTITUTIONAL_PR_GEOMETRY.md`](13_CONSTITUTIONAL_PR_GEOMETRY.md)
exactly like any other PR. Its `origin_law` is "this roadmap" and
its `branch_name` is the specific step being added, split, merged,
or retired.

### Amendment record

```text
Amendment-1 (post-PR-6.1 — chain change only)
    Branch   : append PR-7 and PR-8 to the chain.
    Chosen   : Adapter Boundary path —
               PR-7  Adapter Boundary Law (docs/18, law only),
               PR-8  first concrete ModelClient adapter behind it.
    Rationale: the near-term goal is practical operation of the
               audit layer over a real model; this path makes the
               repository exercisable end-to-end without touching
               kernel semantics.
    Deferred : Typed Hypergraph + Immutable Residual History Law
               path — deferred, not retired. It may enter the
               chain only through a future Amendment PR; nothing
               in PR-7 or PR-8 may pre-implement it.
    Forbidden: this amendment ships no code, no docs/18 content,
               no adapter, no hypergraph, no Arabic code, no new
               runtime dependencies, and no schema expansion.

Amendment-2 (post-PR-8.1 — chain change only)
    Branch   : append PR-9 through PR-13 to the chain — the
               Arabic Weight Boundary branch.
    Chosen   : Arabic Weight Boundary path —
               PR-9   Arabic Weight Boundary Law
                      (docs/19, law only),
               PR-10  Weight / Mīzān carrier surface
                      (carriers only),
               PR-11  minimal WeightFit operation
                      (weigh → fit candidate, never meaning),
               PR-12  Jamid/Mushtaq/Masdar/Mabni/Operator path
                      gates (candidate paths only),
               PR-13  Lexical/Samāʿ/Qiyās License Boundary
                      (licensing before semantics).
    Rationale: PR-8.1 closed the adapter layer's last residual,
               so the external input gate is complete. The first
               Arabic branch can now open — but only as a
               boundary law first, honoring docs/09 (the first
               Arabic application must declare its gates and the
               straight lines it does not shortcut) and docs/04
               (Root → LexicalMeaning and Weight → Agency stay
               gated). Its center: weight does not mean — weight
               images; alignment yields a WeightFitCandidate,
               never Meaning, Agency, Hukm, or Reality. Weight
               mathematics never enters the adapter or audit
               layers.
    Deferred : Typed Hypergraph + Immutable Residual History Law
               path — still deferred (Amendment-1), not retired.
               A second (network) adapter also stays outside the
               chain. Either may enter only through a future
               Amendment PR.
    Forbidden: this amendment ships no code, no docs/19 content,
               no carriers, no weigh operation, no path gates, no
               lexicon, no Arabic linguistic code, no adapter or
               audit change, no new runtime dependencies, and no
               schema expansion.

Amendment-3 (pre-PR-9 — chain change only)
    Branch   : insert PR-9A (Pre-Weight Licensing Law — docs/20,
               law only) after PR-9, and re-stage the Arabic
               Weight Boundary branch as PR-10 through PR-14.
    Chosen   : Pre-weight licensing path —
               PR-9   Arabic Weight Boundary Law
                      (docs/19, law only — unchanged),
               PR-9A  Pre-Weight Licensing Law
                      (docs/20, law only),
               PR-10  weight + pre-weight carrier surface
                      (carriers only; absorbs the docs/20
                      pre-weight carriers into the old PR-10
                      step),
               PR-11  pre-weight path gates
                      (the old PR-12 subject, moved before
                      weighing and widened by docs/20 §7 with
                      ProperName / Borrowed / Residual paths),
               PR-12  pre-weight licensing chain operations
                      (μ_seq through μ_weight_readiness — new
                      step),
               PR-13  minimal WeightFit operation
                      (the old PR-11 subject, moved after
                      readiness; weigh() consumes only a
                      WeightReadinessCandidate),
               PR-14  Lexical / Samāʿ / Qiyās License Boundary
                      (the old PR-13 subject, renumbered only).
    Rationale: the Pre-Weight Licensing Theorem holds that
               syllable → weight is a forbidden leap: the Mīzān
               may operate only over a completed licensing chain
               (syllable sequence, word boundary, word carrier,
               path gate, root/stem or non-root path,
               original/extra split, operation trace, weight
               readiness). The Amendment-2 staging placed
               weigh() (old PR-11) before the path gates (old
               PR-12), contradicting that dependency, and no
               step carried the pre-weight carriers or the μ
               operations. This amendment re-stages the branch
               so law precedes carriers, carriers precede gates,
               gates precede the chain operations, and weigh()
               operates only on the output of the pre-weight
               algebra. docs/04 already names Pronunciation →
               Syllable and Syllable → Word as forbidden
               straight lines with declared bridges; the
               pre-weight chain is the licensed opening of those
               bridges, never a shortcut.
    Deferred : Typed Hypergraph + Immutable Residual History Law
               path — still deferred (Amendment-1), not retired.
               A second (network) adapter also stays outside the
               chain. The syllable origin itself stays bound to
               the declared text entry (ArabicVocalizedText —
               docs/04 pre-text table): the voice/audio pre-text
               chain stays out of execution. Each may enter only
               through a future Amendment PR.
    Forbidden: this amendment ships no code, no docs/19 or
               docs/20 content, no carriers, no μ operation, no
               path gate, no weigh operation, no lexicon, no
               forbidden-line registry rows, no new FailureCode
               members, no Arabic linguistic code, no adapter or
               audit change, no new runtime dependencies, and no
               schema expansion.
```

## 3. Reading order for reviewers

```text
1. CLAUDE.md
2. docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md
3. docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md
4. docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
5. docs/14_PR_CHAIN_ROADMAP.md
6. docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md
7. docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md
8. docs/17_SLOTGRAPH_GENERATION_LAW.md
9. The PR description, checked against (4), (5), (6), (7), (8).
```

A reviewer who skips (4), (5), (6), (7), or (8) cannot tell whether
the PR is a constitutional branch or a leap. CI cannot tell either.
