# CLAUDE.md — Operating instructions for AI agents

This file gives any AI agent (Claude, Copilot, GPT-class) the *minimum
constitutional rules* they must obey when contributing to this repository.

If you are an agent reading this in a future session, treat the rules
below as load-bearing. They are not style suggestions.

---

## The governing law

```text
SlotGeometry is a constitutional mathematical object,
not a free data container.

No output without a SlotGraph.
No SlotGraph without Constitutional Geometry.
No Slot without Boundary.
No Boundary without Domain and Scope.
No Closure without Gamma.
No Gamma without Rank and Residual visibility.
No Output without Trace.
No transition without a Gate.
No Gate without Evidence, Rank, and a Residual policy.
No approved output with hidden residuals.
No straight line from Evidence to Certainty.
No straight line from Tool / Number / LCNV to Knowledge.
No technical term moves between sciences without a licensed bridge.
```

The mathematical statement of these laws lives in
`docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`. Treat that document as
load-bearing: every code change in `core/`, `contracts/`, `gates/`,
or the audit wrapper must preserve its structure exactly.

The matching test-side and PR-side laws live in
`docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md` and
`docs/13_CONSTITUTIONAL_PR_GEOMETRY.md`; the binding chain of pull
requests lives in `docs/14_PR_CHAIN_ROADMAP.md`. They are
load-bearing in the same sense.

The pre-SlotGraph laws ratified in PR-1C live in
`docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md`,
`docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`, and
`docs/17_SLOTGRAPH_GENERATION_LAW.md`. They bind every later PR
that constructs, processes, or consumes a `SlotGraph` and are
load-bearing in the same sense.

The Adapter Boundary Law ratified in PR-7 lives in
`docs/18_ADAPTER_BOUNDARY_LAW.md`. It binds every PR that ships,
modifies, or assembles a concrete `ModelClient` adapter (PR-8 and
later) and is load-bearing in the same sense.

The Meta-Language Boundary Covenant ratified in PV-M0 lives in
`docs/49_META_LANGUAGE_BOUNDARY_COVENANT.md`. It binds every PR
that introduces, modifies, or consumes Arabic meta-language terms
(PV-A3 and later) and is load-bearing in the same sense.

The Mafhūm Boundary Law ratified in PV-A3 lives in
`docs/50_MAFHUM_BOUNDARY_LAW.md`. It binds every PR that
constructs, processes, or consumes a `MafhumClosureCandidate` (PV-A4 and
later) and is load-bearing in the same sense.

The Maʿqūl Branch Discipline Law ratified in PV-A4.1 lives in
`docs/51_MAQUL_BRANCH_DISCIPLINE_LAW.md`. It is a clarification covenant
that names the existing dalālah chain as Maʿqūl al-Dalālah and
governs the transition discipline from Manṭūq to Mafhūm to Hukm.
It binds every PR that opens a new dalālah branch (haqīqah, majāz,
naql, lexical relations) and is load-bearing in the same sense.

The Constitutional Test Origin Covenant ratified in PV-T0 lives in
`docs/52_CONSTITUTIONAL_TEST_ORIGIN_COVENANT.md`. It binds every PR
that introduces new tests after PV-T0 merges: every new test must
declare origin_law, branch_name, and constitutional_chain. It is
load-bearing in the same sense.

## Pre-SlotGraph laws (PR-1C ratified)

```text
SlotGraph is a constitutional mathematical object, not a container.
No SlotGraph from raw value.
No textual entry is an ontological origin.
No internal processing without the identity→truth licensing chain.
No test is constitutional if it asserts only local success.
No PR-2 implementation may merge before docs 15, 16, 17 are ratified.
```

These rules bind PR-2 in particular. Any PR that introduces a
`SlotGraph` constructor, a `Γ` implementation, a `Slot`, a `Center`,
or a `Boundary` must honour:

- the three licensed generation sources in
  `docs/17_SLOTGRAPH_GENERATION_LAW.md` §1,
- the mandatory fields at birth in `docs/17` §2,
- the constructor refusal table in `docs/17` §3,
- the ten-link Identity-to-Truth Licensing Chain in
  `docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md` §2 and its
  per-link refusal mapping in `docs/16` §3,
- the discriminating identities in
  `docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md` §2.

A PR-2 attempt that does not honor these laws is a `FORBIDDEN_LEAP`
regardless of CI status.

## Constitutional rules for tests

```text
No test without an origin.
No test without a branch.
No test without a constitutional chain.
No partial pass counts as constitutional success.
Every rejection must be named with a FailureCode.
Green pytest is not constitutional success.
```

A test is accepted as **constitutional** only if it declares all of:

- origin law (a named law from `docs/02..14`)
- branch case (the single branch under examination)
- constitutional chain (the ordered layers the test walks)
- expected verdict (a `ClosureState`)
- forbidden outputs (proven absent)
- rank ceiling (`max_rank` not exceeded)
- residual visibility expectation
- trace expectation
- named `FailureCode` when the verdict is a refusal

The executable schema lives in
`tests/support/constitutional_case.py` (see
`ConstitutionalTestCase` and `assert_constitutional_case`). Tests
that ship a bare `assert gamma(graph).state == ...` without
walking the rest of the chain are partial passes and are rejected
at review.

## Constitutional rules for pull requests

```text
No PR without an Origin.
No PR without a Branch.
No PR without a Chain position.
No PR without a declared Boundary.
No PR without Constitutional Tests.
No green CI as Constitutional Success.
Every PR is itself a SlotGraph subject to a Gamma-like review.
No PR may exceed its declared layer.
```

The chain of pull requests is authoritative in
`docs/14_PR_CHAIN_ROADMAP.md`. A PR that implements work belonging
to a later step is a `FORBIDDEN_LEAP`, regardless of CI status. The
only licit way to change the chain is an Amendment PR whose entire
branch is the chain change.

The PR template at `.github/pull_request_template.md` is binding;
it operationalises `docs/13_CONSTITUTIONAL_PR_GEOMETRY.md` at
submission time.

## Scope boundaries

1. **No claims about model internals.** This repository never asserts what
   GPT or any LLM "thinks" inside its weights or hidden chain-of-thought.
   It only wraps *emitted* claims with an auditable geometry. See
   `docs/01_BLACK_BOX_BOUNDARY.md`.
2. **No Arabic linguistic code** until the core kernel (`SlotGraph`,
   `Gamma`, `RankLattice`, `ResidualPolicy`, `TransitionGate`,
   `TraceLedger`) and the forbidden-transition registry are stable. See
   `docs/09_ARABIC_APPLICATION_BOUNDARY.md`. The first Arabic branch
   (ratified by Amendment-2 and re-staged as PR-9 through PR-14 by
   Amendment-3 in `docs/14` §2) enters only through the Arabic
   Weight Boundary Law (`docs/19`) and the Pre-Weight Licensing Law
   (`docs/20`), law first — weight maps into PatternSpace, not
   Meaning, and weigh() operates only on a licensed
   WeightReadinessCandidate — and never touches the adapter or audit
   layers.
3. **No LLM adapters** (OpenAI, Anthropic, local models) before PR-8,
   and then only behind the `ModelClient` protocol under the Adapter
   Boundary Law (`docs/18_ADAPTER_BOUNDARY_LAW.md`).
4. **No persistence, no network, no filesystem I/O** in `core/` or
   `contracts/`. The kernel must remain pure.
5. **No runtime dependencies** are added in PR-0 through PR-4. Only the
   standard library.

## Architectural rules for `core/`

- `SlotGeometry` is a constitutional mathematical object first, a
  data structure second. Every implementation of `Slot`, `SlotGraph`,
  `Center`, `Boundary`, `Rank`, `Residual`, `Trace`, `Γ`, or `Gate`
  must preserve the structure specified in
  `docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`.
- Reserved names — `Slot`, `SlotGraph`, `Gamma`, `Gate`, `Rank`,
  `Residual`, `Trace`, `Center`, `Boundary` — may not be bound to
  free containers. A `Slot(name, value)` or a `SlotGraph` without
  center / boundary / rank / residuals / trace is constitutionally
  invalid and must be refused at review.
- All core dataclasses are frozen and hashable where reasonable.
- Core functions are pure: they accept values and return values. They
  do not append to ledgers, write files, or call out to services.
- `gamma(graph)` returns a `GammaResult` containing a
  `TraceEntryCandidate`. The ledger appends the candidate *outside*
  the pure function.
- Every refusal returns a named `FailureCode`. Never raise bare
  exceptions for expected verdicts. Never silently return `None`.
- No implementation may synthesise a missing center, boundary,
  domain, scope, or trace. Missing means refuse.
- Every cross-slot or cross-layer move passes through a
  `TransitionGate`. The gate is the only path that can promote a
  rank, and only bounded by the lattice `meet`.

## PR staging (do not collapse)

```text
PR-0   Scaffold + constitutional docs                                  ✓ done
PR-1A  Mathematical Slot Geometry Constitution + minimal carriers      ✓ done
PR-1B  Constitutional Test Geometry + Constitutional PR Geometry       ✓ done
       (test harness, PR template, PR chain roadmap)
PR-1C  Pre-SlotGraph constitutional closure                            ✓ done
       (docs 15/16/17, ConstitutionalChainTestCase, schema only)
PR-2   SlotGraph + GammaClosure implementation (Rank/Residual carriers) ✓ done
PR-2A  Harden SlotGraph construction (corrective PR, no new layer)     ✓ done
PR-3   RankLattice + ResidualPolicy + EvidenceContract                 ✓ done
PR-4   TransitionGate + FailureTaxonomy bindings                       ✓ done
PR-5   Forbidden Straight-Line Registry (+ technical-terminology cases) ✓ done
PR-6   AnswerAudit wrapper (ModelClient protocol only, no adapters)     ✓ done
PR-6.1 Harden AnswerAudit trace coherence + hygiene fallback            ✓ done
       (corrective PR, no new layer)
PR-7   Adapter Boundary Law (docs/18, law only — licenses adapters)     ✓ done
PR-8   First concrete ModelClient adapter (behind docs/18)              ✓ done
PR-8.1 Harden AdapterGuard static judging purity                        ✓ done
       (corrective PR, no new layer)
PR-9   Arabic Weight Boundary Law (docs/19, law only — no code)         ✓ done
PR-9A  Pre-Weight Licensing Law (docs/20, law only — no code)           ✓ done
PR-10  Weight + pre-weight carrier surface (carriers only)              ✓ done
PR-10B Clarify carrier declarations are not gate verdicts               ✓ done
       (corrective PR, no new layer)
PR-11  Pre-weight path gates (paths only, before any weighing)          ✓ done
PR-11B Clarify hidden-residual wording (corrective PR, no new layer)    ✓ done
PR-12  Pre-weight chain operations (μ_seq → … → μ_weight_readiness)     ✓ done
PR-13  Minimal WeightFit operation (weigh(WeightReadiness…) → fit)      ✓ done
PR-14  Lexical/Samāʿ/Qiyās License Boundary (license before semantics)  ✓ done
PR-15  DalOnlyCandidate Boundary (signifier alone, never meaning)        ✓ done
PR-16  VerbalMadlulCandidate Boundary (verbal signified alone)            ✓ done
PR-16B Unified Pre-Semantic Chain Report (integration, no new layer)      ✓ done
PR-16C Pre-Semantic Registry Contract (contract only, no content)          ✓ done
PR-16C.1 Registry Closure Discipline (corrective PR, no new layer)          ✓ done
PR-17  Dal-Madlul Binding Candidate (binding, never meaning/ifādah)        ✓ done
PR-18  ContractableUnitGeometry (only after binding readiness)              ✓ done
PR-19  Composition / RelationCandidate (relation affordance as candidate)   ✓ done
PR-F1  Formal Shape Registry Law (docs/34, law only — no code)              ✓ done
PR-F2  Word-Class Formal Definitions (ISM / FI'L / HARF)                ✓ done
PR-F2.1 Word-Class MCE Hardening (corrective PR, no new layer)          ✓ done
PR-F3  Built and Reference Formal Definitions (pronouns, demonstratives)     ✓ done
PR-F4  Weight Formal Definitions (verbal / nominal / maṣdar patterns)        ✓ done
PR-F5  Inflection Formal Definitions (iʿrāb / bināʾ / triptote / diptote)    ✓ done
PR-F6  Contract Slot Formal Definitions (formal agent / object / subject)     ✓ done
PR-F7  Composition Pattern Formal Definitions (nominal / verbal / iḍāfa)      ✓ done
PR-F7.1 Chain Correction: No Ifādah before Mufrad Dalālah Closure            ✓ done
       (corrective PR — residual rename, roadmap correction; no new layer)
PR-F8  Formal Style Candidate (khabar/inshāʾ formal only — no meaning)         ✓ done
PR-D1  Mufrad Semantic Slot Geometry (semantic slot frame, identity     ✓ done
       continuity, wadʿ evidence, per-unit formal profile, kulli/juzʾi
       axis, branch-link geometry — never dalālah itself)
PR-D1.2 Maqām / Context Boundary Readiness (discourse domain, usage      ✓ done
       register, technical domain, qarīnah readiness, blocker audit,
       literal domain constraint, wadʿ scope constraint — boundary
       only, never dalālah, never meaning; docs/37)
PR-D2  Mutābaqah / Taḍammun / Iltizām Candidate (dalālah relations        ✓ done
       built on PR-D1 geometry; candidates only, never meaning)
PR-D3  Mufrad Dalālah Closure (closes singular dalālah as candidates)       ✓ done
PR-D4  Relation Closure (relation closes only after MufradDalālahClosure)        ✓ done
PR-D5  Ifādah Boundary Law (docs/41, law only — licenses PR-20)                  ✓ done
PR-D5.1 Stabilize Ifādah Boundary Law identifiers                                ✓ done
       (corrective PR — identifier stabilization; no new layer)
PR-D5.2 Finalize Ifādah Boundary verdict identifier surface                       ✓ done
       (corrective PR — no new layer)
PR-D6  SpeechForce / FormalStyle Bridge Law (docs/42, law only)         ✓ done
PR-20  IfādahCandidate (proposition candidate; 3 parallel PROVEN verdicts;  ✓ done
       maqām is a verdict; never hukm, never meaning)
PR-D7  Hukm Domain Boundary Law (docs/43, law only — NORMATIVE_CANDIDATE,
       AUTHORITY_LEAK forbidden)                                                 ✓ done
PR-21  HukmCandidate (judgment candidate; AST alias-drop guard; never reality)  ✓ done
PR-D8  Manāṭ Boundary Law (docs/44, law only — TAKHRIJ / TANQIH /
       TAHQIQ_READINESS_ONLY)                                                    ✓ done
PR-D8.1 Stabilize Manāṭ Boundary Law references and residual naming             ✓ done
       (corrective PR — no new layer)
PR-D8.2 Clarify Manāṭ Law source roles for Forbidden Lines and Rank Lattice     ✓ done
       (corrective PR — no new layer)
PR-21M ManāṭCandidate (manāṭ candidate; never TAHQIQ verdict)                  ✓ done
PR-D9  Tanzīl Presentation Boundary Law (docs/45, law only — layered envelope)  ✓ done
PR-22  TanzilCandidate (application candidate; carries presentation envelope)  ✓ done
PR-22-AUDIT  Vertical Chain AnswerAudit Bridge (verdict stays inside      ✓ done
             AnswerAudit; ModelClient/AdapterGuard unchanged)
PR-D10 Vertical Path Closure Law (docs/46) + ConstitutionalVerticalChainTestCase
       + Amendment-13 (horizontal-branch ban until PR-D10 merges)         ✓ done
─── Post-Vertical Phase ───────────────────────────────────────────
PV0    Post-Vertical Roadmap Amendment (docs/47, planning only —          ✓ done
       declares vertical closure, branch families, admission rule,
       WIP rule; no runtime code)
PV-A1  Manṭūq Boundary Law (docs/48, law only — defines Manṭūq as       ✓ done
       preserved spoken/textual origin; opens PV-A2 only; no src/,
       no tests, no runtime code)
PV-A1.1 Clarify Manṭūq Boundary Lexical-Origin Requirement              ✓ done
       (docs/48 §10.1 — law-only corrective; ManṭūqClosure
       consumes MufradDalālahClosure through IfadahVerdict,
       not a new LexicalMeaningClosure; no new layer)
PV-A2  ManṭūqClosure code (MantuqClosureState / Candidate / Verdict;    ✓ done
       prove_mantuq_closure(); consumes IfadahVerdict + MaqamContext;
       deferred residuals for mafhūm / majāz / naql)
PV-A2.2 Enforce Upstream Mufrad-Dalālah Continuity                      ✓ done
       (corrective PR — no new layer; UPSTREAM_MUFRAD_DALALAH_MISSING
       FailureCode; prove_mantuq_closure() refuses if
       IfadahCandidate.relation_closure_ref is missing)
PV-A2.3 Harden Manṭūq Upstream Continuity Tests                         ✓ done
       (corrective test-only PR — no runtime change;
       dataclass_fields-based helper; exact trace_ref assertion)
PV-M0  Meta-Language Boundary Covenant                                    ✓ done
       (docs/49 — law only; cross-cutting covenant preventing
       meta-language domain confusion; no src/, no tests,
       no runtime code; prerequisite for PV-A3)
PV-M0.2 Clarify MetaTermContract schema-level trace obligation       ✓ done
       (corrective PR — docs/49 §9A; explicit statement that
       trace_ref is a schema-level obligation, not runtime;
       no new layer, no src/, no tests, no runtime code)
PV-M0.3 Stabilize MetaTermContract trace schema and chain markers    ✓ done
       (corrective PR — align §9A field labels with §3B template;
       add farq_qadih to §3A/§3B trace_ref; add TRACE_SCHEMA_VIOLATION
       to §6 reserved inventory; fix dual-current-PR markers;
       no new layer, no src/, no tests, no runtime code)
PV-T0  Constitutional Test Origin Covenant                              ✓ done
       (docs/52 — law only; extends docs/12 with mandatory
       origin-and-branch declaration for every test; defines
       test categories and transition discipline; no src/,
       no tests/, no scanner, no runtime code;
       prerequisite for PV-M1)
PV-T0-C1 Stabilize Constitutional Test Origin Covenant Surface          ✓ done
       (corrective PR — no new layer; aligns docs/52 §2 field
       names with docs/12 + constitutional_case.py; clarifies
       ConstitutionalChainTestCase requirement; resolves §4
       Category 2 omission inconsistency; fixes CLAUDE.md wording;
       no src/, no tests/, no scanner, no runtime code)
CLOSE-2 Project Methodology, Objectives, and KPI Plan                   ✓ done
       (docs/53 + acceptance tests; declares project origin,
       licensed I/O, forbidden outputs, objectives, KPI matrix,
       BranchContract template, future branch admission rule;
       no runtime code)
CLOSE-2.1 Stabilize post-merge methodology/KPI chain state             ✓ done
       (corrective PR — no new layer; records that PR #93 merged
       both PV-T0-C1 and CLOSE-2; flips their markers to done;
       declares docs/53 binding for all post-CLOSE-2 branches;
       no src/, no tests/, no scanner, no runtime code)
CLOSE-1 Project State Truth                                             ✓ done
       (README, pyproject.toml, LICENSE, CHANGELOG — reflect
       current constitutional state; no runtime code, no new
       carriers, no new enums, no new operations)
GPT-R0 GPT Answer Reasonableness Objective Law                           ✓ done
       (docs/54 — law only; declares that the project's
       operational objective is GPT answer reasonableness
       verification; defines MaqamGPT, MantuqGPT, MafhumGPT,
       NeedGate, Knowledge Origins, ReasonablenessVerdict;
       no src/ runtime code, acceptance tests only)
GPT-K0 Knowledge Origins Boundary Law                                    ✓ done
       (docs/55 — law only; defines the structural frame for
       the five Knowledge Origins; establishes OriginBinding
       requirements, OriginResidual, NeedGate integration,
       and the Transparent Reasonableness Barrier framing;
       no src/ runtime code, acceptance tests only)
GPT-K1 Origin Schema Carriers                                             ✓ done
       (src/taaqqul_slot_geometry/gpt/ — frozen dataclasses for
       EntityGenusOrigin, AttributeEventOrigin, RelationOperatorOrigin,
       ReferenceOrigin, EvidenceOrigin, OriginBinding, OriginResidual;
       no verdicts, no gates, no full pipeline)
PR-X0  Jump-Test Matrix Law + Minimal Residual Vocabulary                 ✓ done
       (law-only constitutional amendment in docs/14; defines
       universal transition jump-test matrix, minimal residual
       vocabulary, default FORBIDDEN_STRAIGHT_LINE fallback,
       and path-matrix discipline after CellSequence; no src/
       runtime code, no parser, no syntax/semantic runtime)
PR-X0R Runtime Contract Hooks                                            ✓ done
       (runtime contract hooks only: JumpTestInput / JumpTestResult /
       ResidualKind / TransitionContract + default
       FORBIDDEN_STRAIGHT_LINE fallback; no parser, no syntax/semantic
       runtime inference)
PR-X0R-AUDIT Post-merge verification + closure note                     ✓ done
       (documentation-only: records that PR #114 merged with one check
       pending at merge time, then passed `ruff check .`, targeted PR-X0R
       tests, and full `pytest` on main; structural verification on main,
       not constitutional closure)
PR-X0L  Euclidean Learning Loop over X0R Contract                       → next
       (learning over X0R only: learn_success / learn_failure /
       refine_contract / evidence-based rank-promotion decisions; no DAL
       learning merge)
PV-A3  Mafhūm Boundary Law                                               ✓ done
       (docs/50 — law only; defines when a Mafhūm branch
       may open from a closed Manṭūq; eight admission
       conditions; no src/, no tests, no runtime code;
       prerequisite for PV-A4)
PV-A4  MafhumClosure code                                                   ✓ done
       (MafhumClosureState / Candidate / Verdict;
       prove_mafhum_closure(); consumes MantuqClosureVerdict;
       eight admission conditions; deferred residuals for
       hukm / tanzil / majāz / naql)
PV-A4.1 Maʿqūl Branch Discipline Law (docs/51, law only — no code)   ✓ done
       (clarification covenant: Maʿqūl is the governing discipline
       of the existing dalālah chain, not a new runtime layer;
       names the 12-stage sequence as Maʿqūl al-Dalālah;
       withdraws MaqulMantuqClosure/MaqulMafhumClosure proposals;
       no src/, no tests, no runtime code)
GPT-K2  Minimal Golden Origins Dataset                                     ✓ done
       (minimal auditable prior-knowledge dataset for origin
       verification; no verdicts, no gates, no full pipeline)
GPT-R1  GPT Answer Input Contract                                          ✓ done
GPT-R2 MaqamGPT Boundary                                                  ✓ done
GPT-R3 MantuqGPT Claim Extraction                                         ✓ done
GPT-R4 MafhumGPT Implication Extraction                                   ✓ done
GPT-R5 Origin Binding Gate                                                ✓ done
DAL-A0  DalAlone Atomic Closure Law (docs/58, law only — corrective        ✓ done
        PR-15.x / DAL-hardening; defines DalAloneClosed before
        LafziMadlulGate; no runtime code)
DAL-A1  DalAlone carrier surface + local residual vocabulary             planned
        (carriers only; local DAL residual vocabulary; no gate execution,
        no DalAloneClosed verdict, no LafziMadlulGate)
DAL-A2  Raw trace / grapheme / letter / sound separation gates            planned
DAL-A3  ArabicSoundInventory + makhraj/sifah/qadih matrix                 planned
DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      planned
DAL-A5  Syllable / transition / adjacency / S1-S5 gates                   planned
DAL-A6  Detailed waqf / wasl closure                                      planned
DAL-A7  Usage / loan / unvocalized / deletion residual gates              planned
DAL-A8  DalAloneClosed -> LafziMadlulGate integration                     planned
LAFZI-B0 Lafzi Madlul Correspondence Law (docs/59, law only —             planned
         DalAloneClosed opens LafziMadlulCandidateSet; no runtime code)
LAFZI-B1 Lafzi carrier surface + local residual vocabulary                planned
LAFZI-B2 WordKindCandidateGate                                            planned
LAFZI-B3 SourceIdentityGate                                               planned
LAFZI-B4 FormStateGate                                                    planned
LAFZI-B5 InternalWordPathGate                                             planned
LAFZI-B6 LafziResidualAudit                                               planned
LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 planned
LAFZI-C0 Wad'iMadlulConditionLaw (docs/60, law only —                     ✓ done
         LafziMadlulClosed opens Wad'iMadlulGate; no runtime code)
LAFZI-C1 Wad'i carrier surface + local residual vocabulary                ✓ done
LAFZI-C2 WadKindGate                                                      ✓ done
LAFZI-C3 WadAuthorityGate                                                 ✓ done
LAFZI-C4 UsageScopeGate                                                   → next
LAFZI-C5 MeaningIdentityGate                                              planned
LAFZI-C6 TransferMajazGate                                                planned
LAFZI-C7 Wad'iResidualAudit                                               planned
LAFZI-C8 Wad'iMadlulClosed -> CoupledDalalahGate integration              planned
LAFZI-D0 Coupled Dalalah Matrix Law (docs/62, law only —                  planned
         places mutabaqah/tadammun/iltizam after Wad'iMadlulClosed +
         CoupledDalalah and before word capability / relation / sentence /
         ifādah / mafhūm / hukm; no runtime code)
LAFZI-D1 CoupledDalalah carrier surface                                   planned
LAFZI-D2 MutabaqahGate                                                    planned
LAFZI-D3 TadammunGate                                                     planned
LAFZI-D4 IltizamGate                                                      planned
LAFZI-D5 DalalahMatrixResidualAudit                                       planned
LAFZI-D6 DalalahMatrixClosed -> WordCapability                            planned
GPT-R6 Reasonableness Gates                                               planned
GPT-R7 GPTAnswerReasonablenessVerdict                                     planned
GPT-R8 Audit Integration                                                  planned
```

The authoritative chain (with per-step scope and forbidden surface)
lives in `docs/14_PR_CHAIN_ROADMAP.md`. Do not bundle PRs. Do not
add LLM adapters except behind the docs/18 Adapter Boundary Law. Do
not add Arabic weight code before docs/19 and docs/20 are ratified
(PR-9, PR-9A), and never inside the adapter or audit layers. No
Arabic lexicon, semantics, ontology, or hukm inside the weight
branch — lexical, samāʿ, and qiyās material enters only through the
PR-14 licensing boundary, and semantics stays beyond the current
chain. The post-PR-14 chain (PR-15 through PR-22) stages the
pre-semantic signifier/signified path: each step produces a bounded
candidate, never meaning. No semantic output (ifādah, hukm, reality)
before its declared chain position. ExtraLetterLicense and 𝒞_Aug
stay outside the chain until after PR-18 (ContractableUnitGeometry).
The post-PR-19 chain (PR-F1 through PR-F7) stages the Formal Shape
Registry: each step produces proven formal Arabic grammatical
definitions (not meaning). No semantic lexicon entry (IfādahCandidate,
PR-20) before FormalShapeClosure.CLOSED (PR-F7). The formal shape is
the constitutional middle term between signifier and meaning.
The post-PR-F7 chain (PR-F8 through PR-D4) stages the Mufrad Dalālah
Closure path: FormalShapeClosure.CLOSED is permission to open mufrad
dalālah, not ifādah. PR-D1 establishes the semantic slot geometry
(identity continuity, wadʿ evidence, per-unit formal profile,
kulli/juzʾi axis, branch-link geometry) before any dalālah relation.
PR-D1.2 establishes maqām/context boundary readiness (discourse domain,
usage register, blocker audit, wadʿ scope constraint) — without which
dalālah operations degenerate into unbounded correspondence.
No IfādahCandidate (PR-20) before
MufradDalālahClosure (PR-D3) + RelationClosure (PR-D4).
The post-PR-D4 chain (PR-D5 through PR-D10) stages the
Ifādah → Hukm → Manāṭ → Tanzīl vertical closure: each code step
is preceded by a law-only step (docs/41 → docs/45), the column
reaches the AnswerAudit surface via PR-22-AUDIT, and the column
itself is closed by docs/46 + ConstitutionalVerticalChainTestCase
(PR-D10). The minimum vertical path is now constitutionally closed.
Post-vertical branches (majāz, mantūq, mafhūm, naql, reference
expansion, conditions DAG, GPT-proposer layer) are governed by
docs/47 (Post-Vertical Roadmap): each requires its own law, chain
position, scope, forbidden surface, constitutional tests, and
residual policy. Only one post-vertical branch may be open at a
time (WIP rule). No post-vertical runtime branch may start before
PV0 is merged. The first post-vertical branch is PV-A1 (Manṭūq
Boundary Law, docs/48) — law only, opening PV-A2 (ManṭūqClosure
code). No Mafhūm before ManṭūqClosure.

## Strategic integration doctrine

Every PR in the weight branch (PR-10 onward) must do **one** of the
following three things:

1. **Extend the chain** — add a new boundary candidate that receives
   the previous layer's output and proves one new constitutional
   property (e.g. PR-15 proves signifier standing, PR-16 proves
   verbal signified standing).
2. **Harden the chain** — ship a corrective PR (e.g. PR-10B, PR-11B)
   that tightens an existing boundary without adding a new layer.
3. **Integrate the chain** — ship a vertical-integration PR (e.g.
   PR-16B) that proves the full chain is one auditable system, not
   independent islands.

No PR may ship isolated code that neither extends, hardens, nor
integrates. The governing principle:

> Do not treat fragmentation with more fragmentation.
> (لا تعالج التفكك بمزيد من التفكيك)

## What to do when in doubt

Stop and ask the maintainer. Do not invent a bridge between layers.
Do not promote a rank. Do not hide a residual. The repository's value is
precisely that it refuses to let answers travel without an audit trail.
