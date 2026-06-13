# 14 — PR Chain Roadmap

> **Status:** Constitutional law. Ratified in PR-1B. Amended by
> Amendment-1 (§2 — Amendment record), which appends PR-7 and PR-8.
> Amended by Amendment-2 (§2), which appends the Arabic Weight
> Boundary branch (PR-9 through PR-13). Amended by Amendment-3
> (§2), which inserts PR-9A (Pre-Weight Licensing Law) and
> re-stages the branch as PR-9 through PR-14. Amended by
> Amendment-4 (§2), which appends the pre-semantic
> signifier/signified chain (PR-15 through PR-22). Amended by
> Amendment-5 (§2), which inserts PR-16B (Unified Pre-Semantic
> Chain Report) between PR-16 and PR-17. Amended by Amendment-6
> (§2), which inserts PR-16C (Pre-Semantic Registry Contract)
> between PR-16B and PR-17. Amended by Amendment-7 (§2), which
> inserts PR-16C.1 (Registry Closure Discipline) between PR-16C
> and PR-17. Amended by Amendment-8 (§2), which inserts PR-F1
> through PR-F7 (Formal Shape Registry branch) between PR-19
> and PR-20.
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
PR-9A   Pre-Weight Licensing Law                           ✓ done
        (docs/20 — law only; the syllable →
        weight-readiness licensing chain; weigh()
        operates only on its output; no code)
PR-10   Weight + pre-weight carrier surface                ✓ done
        (carriers only: WeightImage, Mizan,
        MawzunCandidate, SlotAlignment, plus the
        docs/20 carriers SyllableCandidate through
        WeightReadinessCandidate)
PR-10B  Clarify carrier declarations are not               ✓ done
        gate verdicts (corrective PR; docs/21
        + negative tests — no new layer)
PR-11   Pre-weight path gates                              ✓ done
        (PathGateProof / PathGateVerdict /
        PreWeightPathGate + docs/22 law —
        no weighing, no Ω, no μ chain ops)
PR-11B  Clarify hidden-residual wording in docs/22          ✓ done
        (corrective PR; visible carry ≠ Ω clearance
        — no new layer, no code behavior change)
PR-12   Pre-weight licensing chain operations              ✓ done
        (μ_seq → μ_boundary → μ_word_carrier →
        μ_root_stem → μ_original_extra → μ_ops →
        μ_weight_readiness — gated, named refusals)
PR-13   Minimal WeightFit operation                        ✓ done
        (weigh(WeightReadinessCandidate, ...) →
        WeightFitCandidate or a named Refusal — fit
        only, never meaning)
PR-14   Lexical / Samāʿ / Qiyās License Boundary           ✓ done
        (lexical, samāʿ, and qiyās licensing before
        any semantics)
PR-15   DalOnlyCandidate Boundary                        ✓ done
        (signifier alone — surface identity, phonetic/
        graphic trace, boundary, path, weight fit,
        licensing verdict; never meaning)
PR-16   VerbalMadlulCandidate Boundary                   ✓ done
        (verbal signified alone — wadʿ usage license,
        boundary verdicts, conceptual correspondence
        candidate; never final meaning)
PR-16B  Unified Pre-Semantic Chain Report                ✓ done
        (integration-only — aggregates PR-10 through
        PR-16 into a single PreSemanticChainReport;
        no new linguistic layer; corrective PR)
PR-16C  Pre-Semantic Registry Contract                  ✓ done
        (registry contract only — RegistryDomain,
        RegistryEntry, RegistryLookupResult,
        lookup_registry_entry(); no registry content,
        no lexicon, no meaning)
PR-16C.1 Registry Closure Discipline                   ✓ done
        (corrective PR — RegistryScope,
        RegistryClosureKind, RegistryClosureState,
        RegistryClosureVerdict; no semantic lexicon
        before registry closure; docs/30)
PR-17   Dal-Madlul Binding Candidate                    ✓ done
        (binding of signifier and verbal signified as
        a candidate under rank/residual/trace; never
        meaning, never ifādah; docs/31)
PR-18   ContractableUnitGeometry                         ✓ done
        (objecthood of the bound dal-madlul unit;
        only after binding readiness; docs/32)
PR-19   Composition / RelationCandidate                   ✓ done
        (composition of contractable units; relation
        affordance as candidate, not as meaning; docs/33)
PR-F1   Formal Shape Registry Law                         ✓ done
        (docs/34 — law only; formal shape as the
        middle term between signifier and meaning;
        no code, no definitions)
PR-F2   Word-Class Formal Definitions
        (ISM / FI'L / HARF carriers; domain CLOSED)
PR-F3   Built and Reference Formal Definitions
        (pronouns, demonstratives, relatives, etc.)
PR-F4   Weight Formal Definitions
        (verbal / nominal / maṣdar patterns)
PR-F5   Inflection Formal Definitions
        (iʿrāb / bināʾ / triptote / diptote)
PR-F6   Contract Slot Formal Definitions
        (formal agent / object / subject / predicate)
PR-F7   Composition Pattern Formal Definitions
        (nominal / verbal / iḍāfa / etc.)
PR-20   IfādahCandidate
        (proposition candidate — only after composition;
        never hukm, never reality)
PR-21   HukmCandidate
        (judgment candidate — only after ifādah;
        never reality, never tanzil)
PR-22   TanzilCandidate
        (application candidate — only after hukm)
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

PR-10B
    Origin   : docs/19 + docs/20 + docs/14 (corrective PR
               shape — no new layer; clarifies the reading
               of PR-10 carriers).
    Output   : docs/21_CARRIER_DECLARATION_IS_NOT_VERDICT_LAW.md —
               the Carrier Declaration Is Not Verdict Law.
               Negative constitutional tests proving that:
               PathKind ≠ PathGateProof; OriginalExtraMap ≠
               ExtraLetterLicense; WeightReadinessCandidate ≠
               WeightFitCandidate; Mizan ≠ weighing authority;
               typed residuals ≠ residual clearance; TraceRef ≠
               ledger commit; Candidate rank ≠ gate rank.
    Forbidden: any new carrier; any operation; any new code in the
               weight package; adapter, audit, or kernel changes;
               new runtime dependencies; anything that constitutes
               a new layer.

PR-11
    Origin   : docs/20 §7 (the path gate precedes the root) +
               docs/19 + docs/22 (the Pre-Weight Path Gate Law);
               re-staged before weighing by Amendment-3 (§2).
    Output   : docs/22_PRE_WEIGHT_PATH_GATE_LAW.md — the law.
               PathGateProof, PathGateVerdict, PathGateState,
               PreWeightPathGate (the pure gate with a decide()
               method). PATH_GATE_RANK_CEILING. All seven
               PathKind members decidable. Constitutional tests
               proving carrier ≠ verdict, PathKind ≠ proof,
               verdict ≠ meaning, verdict ≠ weight.
               Updates to test_weight_carriers.py static guards.
    Forbidden: weighing; Ω judgment; μ chain operations;
               root/stem extraction; original/extra split;
               meaning; semantics; hukm; ontology; lexicon;
               samāʿ; qiyās; adapter or audit changes; new
               FailureCode members; new runtime dependencies.

PR-11B
    Origin   : docs/22 §5 + docs/14 (corrective PR shape —
               no new layer; clarifies the reading of PR-11
               hidden-residual wording).
    Output   : docs/22 §5 clarification paragraph: visible
               carry is not Ω clearance; PathGateVerdict
               docstring note; test docstring note.
    Forbidden: any code behavior change; any new gate state;
               any new FailureCode; Ω judgment; residual
               clearance; weighing; WeightFitCandidate;
               lexical/samāʿ/qiyās; extra-letter licensing;
               adapter or audit changes; new runtime
               dependencies; anything that constitutes a new
               layer.

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

PR-15
    Origin   : docs/25 (licensing boundary verdicts license
               eligibility, not meaning) + docs/04 (Sign → Meaning
               is a forbidden straight line).
    Output   : DalOnlyCandidate — the signifier-alone boundary.
               Proves the signifier surface (identity, phonetic
               trace, graphic trace, boundary, path gate verdict,
               weight fit candidate, licensing boundary verdict)
               stands independently before any signified.
               Law document (docs/26).
    Forbidden: VerbalMadlulCandidate; DalMadlulBindingCandidate;
               meaning; ifādah; hukm; reality; ontology;
               conceptual correspondence output; LicensedWeight;
               ExtraLetterLicense; 𝒞_Aug; generation from qiyās;
               samāʿ generalization; adapter or audit changes;
               new runtime dependencies.
    Law      : DalOnlyCandidate ≠ LexicalMadlul.
               DalOnlyCandidate ≠ Meaning.
               DalOnlyCandidate ≠ Ifādah.
               DalOnlyCandidate ≠ Hukm.

PR-16
    Origin   : docs/25 + docs/04 (Root → LexicalMeaning is a
               forbidden straight line) + docs/26 (once ratified
               by PR-15).
    Output   : VerbalMadlulCandidate — the verbal signified
               alone boundary. A signified candidate carrying wadʿ
               usage license, boundary verdicts, conceptual
               correspondence candidate, inclusion candidate,
               iltizām condition candidate, existence/event/
               relation affordance candidates — each as a
               candidate at rank, not as a final meaning.
               Law document (docs/27).
    Forbidden: DalMadlulBindingCandidate; final conceptual meaning;
               reference; ifādah; hukm; ontology; reality;
               LicensedWeight; ExtraLetterLicense; 𝒞_Aug;
               generation from qiyās; samāʿ generalization;
               adapter or audit changes; new runtime dependencies.
    Law      : VerbalMadlulCandidate ≠ ConceptualMeaning.
               VerbalMadlulCandidate ≠ Reference.
               VerbalMadlulCandidate ≠ Relation.
               VerbalMadlulCandidate ≠ Ifādah.
               VerbalMadlulCandidate ≠ Hukm.

PR-16B
    Origin   : PR-10 through PR-16 (all prior weight-branch PRs).
    Output   : PreSemanticChainReport — a read-only integration
               of the full pre-semantic chain (weight readiness,
               weight fit, licensing, dal boundary, madlul
               boundary) into a single frozen report.
               Proves rank monotonicity, residual continuity,
               and trace coverage across the entire chain.
               Law document (docs/28).
    Forbidden: New linguistic layer; new carrier ontology;
               meaning; ifādah; hukm; reality;
               DalMadlulBindingCandidate;
               adapter or audit changes; new runtime dependencies.
    Law      : PreSemanticChainReport is integration, not layer.
               No new rank promotion path.
               No residual suppression.
               Chain traversal is read-only.

PR-16C
    Origin   : docs/28 (once ratified by PR-16B) + docs/14
               (strategic integration doctrine — "no binding
               before registry") + docs/04 (Sign → Meaning
               is a forbidden straight line).
    Output   : the Pre-Semantic Registry Contract — contract
               only: RegistryDomain (DAL_ONLY / VERBAL_MADLUL),
               RegistryEntry (frozen carrier with key, domain,
               non_meaning_proof, rank, residuals, trace_ref),
               RegistryLookupResult (FOUND / REFUSED / DEFERRED
               with entry or named FailureCode),
               lookup_registry_entry() (pure function accepting
               candidate + domain + registry → bounded result).
               Law document (docs/29).
    Forbidden: registry content (no actual dal entries, no actual
               verbal-madlul entries, no lexicon, no phonetic
               tables, no grammatical tables); meaning; ifādah;
               hukm; reality; ontology; DalMadlulBindingCandidate;
               ContractableUnitGeometry; ExtraLetterLicense;
               𝒞_Aug; composition; adapter or audit changes;
               new runtime dependencies.
    Law      : RegistryEntry ≠ Meaning.
               RegistryLookupResult ≠ SemanticVerdict.
               RegistryLookupResult ≠ Binding.
               lookup_registry_entry() licenses pre-semantic
               admissibility only.
    Binding  : No DalMadlulBindingCandidate (PR-17) before the
               registry contract (PR-16C) is ratified. PR-17
               must consume RegistryLookupResult as input and
               must not create or populate registry entries.
               Violations are FORBIDDEN_LEAP regardless of CI
               status.

PR-16C.1
    Origin   : docs/29 (once ratified by PR-16C) + docs/14
               (strategic integration doctrine — "no meaning
               before registry closure") + docs/04 (Sign →
               Meaning is a forbidden straight line).
    Output   : the Registry Closure Discipline — corrective PR:
               RegistryScope (MUFRAD / TARKIB),
               RegistryClosureKind (DAL_ONLY_MUFRAD /
               DAL_ONLY_TARKIB / VERBAL_MADLUL_MUFRAD /
               VERBAL_MADLUL_TARKIB),
               RegistryClosureState (CLOSED / REFUSED /
               DEFERRED),
               RegistryClosureVerdict (frozen carrier with kind,
               state, failure_code, residuals, trace_ref).
               Law document (docs/30).
    Forbidden: registry content; lexicon; meaning; ifādah; hukm;
               reality; ontology; DalMadlulBindingCandidate;
               ContractableUnitGeometry; ExtraLetterLicense;
               𝒞_Aug; composition; adapter or audit changes;
               new runtime dependencies; closure of TARKIB
               registry (only the law, not the closure).
    Law      : No Meaning Before Registry Closure.
               RegistryClosureVerdict ≠ Meaning.
               RegistryClosureVerdict ≠ SemanticVerdict.
               DEFERRED is not refusal.
               Only CLOSED licenses semantic lexicon access.
    Binding  : No semantic/wadʿi/dalālah lexicon access before
               RegistryClosureVerdict.CLOSED for the required
               scope. Violations are FORBIDDEN_LEAP regardless
               of CI status.

PR-17
    Origin   : docs/26 + docs/27 (once ratified by PR-15 and
               PR-16) + docs/29 (once ratified by PR-16C).
    Output   : DalMadlulBindingCandidate — the binding of
               signifier and verbal signified under
               rank/residual/trace governance. Proves a
               DalOnlyCandidate can be bound to a
               VerbalMadlulCandidate with a binding license,
               residual governance, and rank bound — producing a
               DalMadlulBindingCandidate, never meaning.
               Consumes RegistryLookupResult as input evidence.
               Law document (docs/30).
    Forbidden: meaning; ifādah; hukm; reality; ontology;
               ContractableUnitGeometry; LicensedWeight;
               ExtraLetterLicense; 𝒞_Aug; generation from qiyās;
               samāʿ generalization; adapter or audit changes;
               new runtime dependencies.
    Law      : DalMadlulBindingCandidate ≠ Meaning.
               DalMadlulBindingCandidate ≠ Ifādah.
               DalMadlulBindingCandidate ≠ Hukm.
               DalMadlulBindingCandidate ≠ Reality.

PR-18
    Origin   : docs/31 (once ratified by PR-17) + docs/11
               (SlotGeometry is a constitutional mathematical
               object).
    Output   : ContractableUnitGeometry — the objecthood of a
               bound dal-madlul unit. Only a
               DalMadlulBindingCandidate can enter; the geometry
               establishes contractability, never meaning.
               ContractabilityProfile (affordance, not SyntaxRole).
               prove_contractable_unit() pure function.
               Law document (docs/32).
    Forbidden: composition; relation; ifādah; hukm; reality;
               ExtraLetterLicense; 𝒞_Aug; meaning;
               generation from qiyās; samāʿ generalization;
               adapter or audit changes; new runtime dependencies.
    Binding  : No ContractableUnitGeometry before binding
               readiness (PR-17 merged). Violations are
               FORBIDDEN_LEAP regardless of CI status.
    Law      : ContractableUnitGeometry ≠ Meaning.
               ContractableUnitGeometry ≠ RelationCandidate.
               ContractabilityProfile ≠ SyntaxRole.
               ContractableUnitGeometry proves objecthood,
               not meaning.

PR-19
    Origin   : docs/32 (ratified by PR-18) + docs/04
               (Composition → Reality is a forbidden straight
               line).
    Output   : Composition / RelationCandidate — composition of
               contractable units and relation affordance as
               candidate. Multiple ContractableUnitGeometry
               instances may compose, producing a
               RelationCandidate — never meaning, never reality.
               Law document (docs/33).
    Forbidden: ifādah; hukm; reality; meaning; ontology;
               ExtraLetterLicense; 𝒞_Aug; adapter or audit
               changes; new runtime dependencies.
    Law      : RelationCandidate ≠ Meaning.
               RelationCandidate ≠ Reality.
               RelationCandidate ≠ Ifādah.
               RelationCandidate ≠ Hukm.
               ContractabilityProfile ≠ SyntaxRole.
               RelationCandidate must re-gate admissible_roles.

PR-F1
    Origin   : docs/33 §8 (open residuals — Arabic formal vocabulary
               not licensed) + docs/04 (Sign → Meaning is a forbidden
               straight line) + docs/14 Amendment-8.
    Output   : docs/34_FORMAL_SHAPE_REGISTRY_LAW.md — the Formal Shape
               Registry Law. Law only: no code ships here.
               Center: no semantic-wadʿi signified for meanings before a
               formal definition. The formal shape is the constitutional
               middle term between signifier surface and semantic lexicon.
               Defines FormalShapeDomain, FormalShapeFamily,
               FormalShapeDefinition, FormalShapeRegistry,
               FormalShapeClosure, FormalShapeClosureVerdict.
    Forbidden: formal shape carriers; FormalShapeDefinition instances;
               registry content; meaning; ifādah; hukm; reality;
               ontology; semantic lexicon; wadʿi dalālah; adapter or
               audit changes; new runtime dependencies.
    Binding  : No FormalShapeDefinition content before docs/34 is
               ratified. No semantic lexicon before
               FormalShapeClosure.CLOSED. Violations are FORBIDDEN_LEAP
               regardless of CI status.
    Law      : FormalShapeDefinition ≠ Meaning.
               FormalShapeDefinition ≠ SemanticEntry.
               FormalShapeRegistry ≠ SemanticLexicon.
               CONTRACT_SLOT ≠ SyntaxRole.
               No meaning before form.

PR-F2
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §5 (WORD_CLASS).
    Output   : FormalShapeDefinition instances for ISM, FI'L, HARF.
               WORD_CLASS domain FormalShapeRegistry with closure_state
               CLOSED. Constitutional tests proving each definition.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; wadʿi dalālah; adapter or audit changes; new
               runtime dependencies; definitions from other domains.
    Law      : Word-class is formal category, not meaning.

PR-F3
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §6
               (BUILT_REFERENCE).
    Output   : FormalShapeDefinition instances for personal pronouns,
               demonstratives, relative pronouns, interrogatives,
               conditionals. BUILT_REFERENCE domain registry CLOSED.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; adapter or audit changes; new runtime
               dependencies; definitions from other domains.
    Law      : Built/reference form is formal shape, not meaning.

PR-F4
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §7
               (WEIGHT_PATTERN).
    Output   : FormalShapeDefinition instances for verbal, nominal,
               and maṣdar weight patterns. WEIGHT_PATTERN domain
               registry CLOSED.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; adapter or audit changes; new runtime
               dependencies; definitions from other domains.
    Law      : Weight pattern is formal shape, not meaning.
               faʿala ≠ action. mafʿūl ≠ patienthood.

PR-F5
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §8 (INFLECTION).
    Output   : FormalShapeDefinition instances for iʿrāb, bināʾ,
               triptote, diptote. INFLECTION domain registry CLOSED.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; adapter or audit changes; new runtime
               dependencies; definitions from other domains.
    Law      : Inflection is formal marking, not meaning.
               rafʿ ≠ agency. naṣb ≠ patienthood.

PR-F6
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §9
               (CONTRACT_SLOT).
    Output   : FormalShapeDefinition instances for formal subject,
               predicate, object, complement. CONTRACT_SLOT domain
               registry CLOSED.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; SyntaxRole assignment; adapter or audit
               changes; new runtime dependencies; definitions from
               other domains.
    Law      : CONTRACT_SLOT ≠ SyntaxRole.
               Formal position is proved by inflection, not by
               semantic agency.

PR-F7
    Origin   : docs/34 (ratified by PR-F1) + docs/34 §10
               (COMPOSITION_PATTERN).
    Output   : FormalShapeDefinition instances for nominal sentence,
               verbal sentence, iḍāfa, ṣifa-mawṣūf, ʿaṭf, badal.
               COMPOSITION_PATTERN domain registry CLOSED.
               FormalShapeClosure gate operational.
    Forbidden: meaning; ifādah; hukm; reality; ontology; semantic
               lexicon; adapter or audit changes; new runtime
               dependencies; definitions from other domains.
    Binding  : No IfādahCandidate (PR-20) before PR-F7 closes the
               composition pattern domain. Violations are
               FORBIDDEN_LEAP regardless of CI status.
    Law      : Composition pattern is formal structure, not meaning.
               jumlah ismiyyah ≠ proposition.
               jumlah fiʿliyyah ≠ event.

PR-20
    Origin   : docs/34 (once ratified by PR-F7) + docs/33
               (once ratified by PR-19) + FormalShapeClosure.CLOSED
               prerequisite.
    Output   : IfādahCandidate — the proposition candidate. Only
               after composition and formal shape closure; proves a
               complete composed structure can be assessed for
               propositional
               candidacy — never hukm, never reality, never
               truth-value.
               Law document (docs/32).
    Forbidden: hukm; reality; truth-value; tanzil; ontology;
               adapter or audit changes; new runtime dependencies.
    Law      : IfādahCandidate ≠ Hukm.
               IfādahCandidate ≠ Reality.
               IfādahCandidate ≠ TruthValue.

PR-21
    Origin   : docs/32 (once ratified by PR-20).
    Output   : HukmCandidate — the judgment candidate. Only after
               ifādah; proves a proposition candidate can be
               assessed for judgment candidacy — never reality,
               never tanzil.
               Law document (docs/33).
    Forbidden: reality; tanzil; application; ontology;
               adapter or audit changes; new runtime dependencies.
    Law      : HukmCandidate ≠ Reality.
               HukmCandidate ≠ Tanzil.

PR-22
    Origin   : docs/33 (once ratified by PR-21).
    Output   : TanzilCandidate — the application candidate. Only
               after hukm; proves a judgment candidate can be
               assessed for application candidacy.
               Law document (docs/34).
    Forbidden: reality-assertion; independent existence claims;
               adapter or audit changes; new runtime dependencies.
    Law      : TanzilCandidate ≠ RealityAssertion.
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

Amendment-4 (post-PR-14 — chain change only)
    Branch   : append PR-15 through PR-22 to the chain — the
               pre-semantic signifier/signified chain.
    Chosen   : Pre-semantic dal-madlul path —
               PR-15  DalOnlyCandidate Boundary
                      (signifier alone; never meaning),
               PR-16  VerbalMadlulCandidate Boundary
                      (verbal signified alone; never final
                      meaning),
               PR-17  Dal-Madlul Binding Candidate
                      (binding as candidate; never meaning,
                      never ifādah),
               PR-18  ContractableUnitGeometry
                      (objecthood; only after binding readiness),
               PR-19  Composition / RelationCandidate
                      (relation affordance as candidate),
               PR-20  IfādahCandidate
                      (proposition candidate; never hukm),
               PR-21  HukmCandidate
                      (judgment candidate; never reality),
               PR-22  TanzilCandidate
                      (application candidate; end of chain).
    Rationale: PR-14 closed boundary eligibility — the last step
               in the pre-semantic licensing chain. The next layer
               must test the signifier and the verbal signified
               independently before binding them, preventing the
               forbidden leap Sign → Meaning. The chain ensures:
               (1) the signifier stands alone as a proven surface
               before any signified is considered;
               (2) the verbal signified is a candidate at rank,
               not a conceptual meaning;
               (3) binding is a licensed operation, not an
               identity;
               (4) ContractableUnitGeometry enters only after
               binding readiness, not before;
               (5) composition, ifādah, hukm, and tanzil each
               require the previous layer's readiness.
               The governing principle: pre-semantic success is
               the prevention of meaning claims, not their
               production.
    Deferred : Typed Hypergraph + Immutable Residual History Law
               path — still deferred (Amendment-1), not retired.
               ExtraLetterLicense and 𝒞_Aug stay outside the
               chain until after ContractableUnitGeometry (PR-18)
               is ratified. LicensedWeight requires a separate
               staging step between PR-14 and PR-15 only if
               future review determines that licensing-boundary
               eligibility is insufficient input to the
               signifier boundary; otherwise PR-15 consumes
               LicensingBoundaryVerdict directly. Each deferred
               item may enter only through a future Amendment PR.
    Forbidden: this amendment ships no code, no law documents
               (docs/26–33), no carriers, no binding operation,
               no ContractableUnitGeometry, no composition, no
               ifādah, no hukm, no tanzil, no meaning, no
               semantic output, no ExtraLetterLicense, no 𝒞_Aug,
               no LicensedWeight, no adapter or audit change, no
               new runtime dependencies, and no schema expansion.

Amendment-5 (post-PR-16 — chain change only)
    Branch   : insert PR-16B (Unified Pre-Semantic Chain Report)
               between PR-16 and PR-17, and renumber PR-17's law
               document from docs/28 to docs/29.
    Chosen   : Integration report path —
               PR-16B  Unified Pre-Semantic Chain Report
                       (integration-only — aggregates PR-10
                       through PR-16; no new linguistic layer;
                       docs/28).
    Rationale: by PR-16 the pre-semantic chain is six layers deep
               (weight readiness, weight fit, licensing, dal
               boundary, madlul boundary) but no single point
               proves that rank monotonicity, residual continuity,
               and trace coverage hold across the entire chain
               together. PR-16B is not a new boundary; it is a
               vertical integration proving the chain is one
               auditable system, not a collection of independent
               islands.
    Deferred : all items deferred by Amendment-1 through
               Amendment-4 remain deferred.
    Forbidden: this amendment ships no new linguistic layer, no
               new carrier ontology, no meaning, no ifādah, no
               hukm, no reality, no binding candidate, no adapter
               or audit change, no new runtime dependencies. The
               only new code is the integration report (a
               read-only traversal over existing carriers).

Amendment-6 (post-PR-16B — chain change only)
    Branch   : insert PR-16C (Pre-Semantic Registry Contract)
               between PR-16B and PR-17, and renumber PR-17's
               law document from docs/29 to docs/30 (cascading
               PR-18 through PR-22 one position forward).
    Chosen   : Registry contract path —
               PR-16C  Pre-Semantic Registry Contract
                       (contract only — RegistryDomain,
                       RegistryEntry, RegistryLookupResult,
                       lookup_registry_entry(); docs/29).
    Rationale: PR-16B proved the chain is one auditable system.
               But proving chain unity does not prove that the
               chain possesses a classified pre-semantic registry.
               Without a registry contract, PR-17 (binding) would
               bind signifier to verbal signified without evidence
               that each party holds a classified entry in a
               pre-semantic registry — making the binding
               structurally unanchored. The governing principle:
               no binding before registry. PR-16C is not a
               registry content PR; it is a registry contract that
               defines RegistryEntry, RegistryDomain,
               RegistryLookupResult, and lookup_registry_entry()
               — the minimum surface PR-17 must consume to prove
               that both parties are admissible.
    Deferred : all items deferred by Amendment-1 through
               Amendment-5 remain deferred. Registry content
               slices (actual dal entries, actual verbal-madlul
               entries) are deferred to a future Amendment; they
               are not part of this chain change.
    Forbidden: this amendment ships no registry content, no actual
               dal entries, no actual verbal-madlul entries, no
               lexicon, no phonetic tables, no grammatical tables,
               no meaning, no ifādah, no hukm, no reality, no
               ontology, no DalMadlulBindingCandidate, no
               ContractableUnitGeometry, no ExtraLetterLicense,
               no 𝒞_Aug, no composition, no adapter or audit
               change, no new runtime dependencies, and no schema
               expansion beyond the registry contract surface.

Amendment-7 (post-PR-16C — chain change only)
    Branch   : insert PR-16C.1 (Registry Closure Discipline)
               between PR-16C and PR-17.
    Chosen   : Registry closure discipline path —
               PR-16C.1  Registry Closure Discipline
                         (corrective PR — RegistryScope,
                         RegistryClosureKind,
                         RegistryClosureState,
                         RegistryClosureVerdict; docs/30).
    Rationale: PR-16C proved the chain possesses a classified
               pre-semantic registry contract. But proving the
               contract exists does not prove that the registry
               is sealed before semantic access. Without a
               closure discipline, PR-17 (binding) may succeed,
               and downstream layers may open a semantic/wadʿi/
               dalālah lexicon without evidence that the
               registry is closed for the relevant domain and
               scope — leaving a premature-meaning gap. The
               governing principle: no meaning before registry
               closure. PR-16C.1 defines the closure verdict
               carriers and the law that forbids semantic lexicon
               access before CLOSED; it does not close any
               registry.
    Deferred : all items deferred by Amendment-1 through
               Amendment-6 remain deferred. TARKIB registry
               closure is deferred until composition readiness
               (PR-19). Actual registry content is still deferred
               to a future Amendment.
    Forbidden: this amendment ships no registry content, no actual
               dal entries, no actual verbal-madlul entries, no
               lexicon, no meaning, no ifādah, no hukm, no
               reality, no ontology, no DalMadlulBindingCandidate,
               no ContractableUnitGeometry, no ExtraLetterLicense,
               no 𝒞_Aug, no composition, no adapter or audit
               change, no new runtime dependencies, and no schema
               expansion beyond the registry closure discipline
               surface.

Amendment-8 (post-PR-19 — chain change only)
    Branch   : insert PR-F1 through PR-F7 (Formal Shape Registry
               branch) between PR-19 and PR-20.
    Chosen   : Formal Shape Registry path —
               PR-F1  Formal Shape Registry Law
                      (docs/34, law only),
               PR-F2  Word-Class Formal Definitions
                      (ISM / FI'L / HARF — domain carriers),
               PR-F3  Built and Reference Formal Definitions
                      (pronouns, demonstratives, relatives, etc.),
               PR-F4  Weight Formal Definitions
                      (verbal / nominal / maṣdar patterns),
               PR-F5  Inflection Formal Definitions
                      (iʿrāb / bināʾ / triptote / diptote),
               PR-F6  Contract Slot Formal Definitions
                      (formal agent / object / subject / predicate),
               PR-F7  Composition Pattern Formal Definitions
                      (nominal / verbal / iḍāfa / etc.).
    Rationale: PR-19 proved that two contractable units can stand in
               a governed relation — but the ContractabilityProfile
               strings (admissible_roles, blocked_roles,
               word_class_affordance, inflection_affordance,
               derivational_affordance) are open strings, not proven
               Arabic grammatical types. Without a Formal Shape
               Registry, the path from RelationCandidate to
               IfādahCandidate (PR-20) would require an unlicensed
               leap: open string → semantic lexicon. The Formal Shape
               Registry is the constitutional middle term — it proves
               that the strings used in ContractabilityProfile and
               RelationCandidate correspond to formally defined,
               constitutionally evidenced Arabic grammatical categories
               before any semantic content can be constructed.
               The supreme law: لا مدلول وضعي للمعاني قبل تعريف شكلي
               (no semantic-wadʿi signified for meanings before a
               formal definition).
    Deferred : all items deferred by Amendment-1 through Amendment-7
               remain deferred. Semantic lexicon content, wadʿi
               dalālah operations, ExtraLetterLicense, and 𝒞_Aug
               remain outside the chain until after PR-F7
               (Composition Pattern closure).
    Forbidden: this amendment ships no code, no formal shape
               carriers, no FormalShapeDefinition instances, no
               registry content, no meaning, no ifādah, no hukm,
               no reality, no ontology, no semantic lexicon, no
               adapter or audit change, no new runtime dependencies,
               and no schema expansion. Only the law document
               (docs/34) and chain table updates are allowed in
               PR-F1.
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
