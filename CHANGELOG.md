# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses a constitutional chain (see `docs/14_PR_CHAIN_ROADMAP.md`)
rather than semantic versioning milestones — each entry corresponds to a
chain step, not a release.

## [Unreleased]

### Changed
- phase-closure anchoring: added `docs/75_PHASE_1_CLOSURE_DECLARATION.md` as a
  bounded three-phase declaration (`Phase 1` closed with boundaries,
  `Phase 2` readiness/carrier contracts, `Phase 3` MGCM staged runtime),
  fixing terminal Phase-1 output at `WORD_CAPABILITY`, preserving forbidden
  downstream openings (relation/sentence/ifādah/hukm/truth/reality), and
  declaring `NEXT_PERMITTED_ACTION = X0R_E1_CARRIER_ONLY_ADMISSION` under
  admission discipline.
- state-truth synchronization + LAFZI trace audit: aligned `README.md` with
  `docs/14_PR_CHAIN_ROADMAP.md` and `CLAUDE.md` (removing stale `DAL-A5 current`
  and `LAFZI-B* unopened` wording), recorded `LAW-E0` as planned law-only
  status truth, and added `docs/74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md` with
  explicit B1..B7 trace map, C/D closure evidence, and no-jump proof from
  `WordCapability` to relation/sentence/ifādah/hukm/truth.
- DAL-A5 runtime gates: added
  `src/taaqqul_slot_geometry/weight/dal_a5_runtime_gates.py` with bounded
  DAL-A5-only runtime carriers/verdict (`DalA5SyllableInput`,
  `DalA5SyllableCandidate`, `DalA5TransitionCandidate`,
  `DalA5AdjacencyVerdict`, `DalA5RuntimeVerdict`) and
  `prove_dal_a5_runtime_gates()` over DAL-A4 trace-preserving inputs only.
- DAL-A5 chain synchronization: updated `docs/14_PR_CHAIN_ROADMAP.md`,
  `CLAUDE.md`, `README.md`, and chain tests so `DAL-A5-ADMIT` is marked done
  and `DAL-A5` runtime is the current chain step, while DAL-A6..A8/LAFZI-B0..B7/
  LAW-E0 runtime and parser/morphology/syntax/semantic/hukm/reality outputs
  remain unopened.
- DAL-A4 runtime gates: implemented bounded DAL-only runtime surface in `src/taaqqul_slot_geometry/weight/dal_a4_runtime_gates.py` for `HamzaResolutionGate`, `ShaddaIdghamGate`, `TanwinTraceGate`, `SukunCollisionGate`, and `MaddExtensionGate`; synchronized chain state so `DAL-A4-ADMIT` is done and `DAL-A4` is current while DAL-A5..A8, LAFZI-B0..B7, LAW-E0 runtime, parser/morphology/syntax runtime, and semantic/hukm outputs remain deferred.
- DAL-A4-ADMIT admission-only chain step: marked `CLOSE-6.1` as done and
  added `DAL_A4_ADMISSION_MATRIX` + `DAL_A4_ADMISSION_VERDICT` in
  `docs/14_PR_CHAIN_ROADMAP.md` to decide DAL-A4 admissibility without
  opening any `src/` runtime surface; DAL-A5..A8, LAFZI-B0..B7, and LAW-E0
  metric/runtime remain deferred.
- CLOSE-6.1 post-merge release-boundary verification: normalized
  chain/status wording after PR #173 by synchronizing
  `docs/14_PR_CHAIN_ROADMAP.md`, `CLAUDE.md`, `README.md`, and this
  changelog; added `CLOSE_6_1_VERDICT` and a bounded gap/admission matrix
  confirming no runtime opening and keeping DAL-A4..A8, LAFZI-B0..B7, and
  LAW-E0 metric/runtime completion deferred.
- CLOSE-6 release-boundary declaration is now recorded as merged
  declaration-only scope; runtime DAL/LAFZI/parser/semantic openings remain
  forbidden and not present.
- WEB-M0 law-only matrix record: added `docs/65_LOCAL_DYNAMIC_WEB_MATRIX_RECORD.md` to lift only permission to draft a future local dynamic web boundary law while keeping runtime API, `/website` changes, dependencies, public deployment, persistence, telemetry, and model calls unlicensed.
- LAFZI-D6 runtime implementation: added `DalalahMatrixClosed` ->
  `WordCapability` integration bounded to a PROVEN, residual-free D5 audit,
  preserving D1-D5 boundary/domain/scope identity, rank ceiling, and trace
  continuity.
- LAFZI-D1 hardening: CoupledDalalahSurface now requires an explicit
  D1C8HandoffCard derived from a CLOSED C8 result and matching wadʿī contract;
  D1 boundary/domain/scope fields are no longer free inputs, forbidden outputs
  cannot be weakened, and included/excluded boundary surfaces must be disjoint.
- State-truth correction: synchronized `docs/14_PR_CHAIN_ROADMAP.md`,
  `CLAUDE.md`, `README.md`, and `CHANGELOG.md` on the same forward chain:
  `LAFZI-D6` done, `GPT-R6` done, then `GPT-R7` done → `GPT-R8`, then
  `CLOSE-3` → `CLOSE-4` → `CLOSE-5` → `CLOSE-6`.

### Added
- LAW-E1: `docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md` adds a
  law-only boundary for phonetic/structural/system partition definitions,
  identity-property conservation + triadic continuity, and
  daruri/haji/tahsini tier discipline with named failure-mapping
  obligations. Runtime carriers/gates and semantic outputs remain deferred.
- LAW-E0: `docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md` registers a
  law-only Arabic Euclidean layer-contract discipline: every future Arabic
  layer must answer condition of possibility, minimum complete limit,
  opening, demand, identity preservation, closure, visible residual, and
  licensed transition. Runtime carriers, parsers, DAL closure, ifādah, hukm,
  truth, and certainty remain deferred; `GPT-R8` remains the current next
  step.
- PR-X0L: Euclidean learning-loop runtime over X0R contract surfaces only.
  Added `learn_success`, `learn_failure`, `refine_contract`, and
  `promote_rank_if_evidence_sufficient` with visible evidence references,
  residual policy, and rank-promotion refusal guards.
- LAFZI-D6: DalalahMatrixClosed and WordCapabilityBoundary — bounded
  post-audit matrix closure over a proven D5 residual audit, preserving D1-D5
  ancestry, rank, residuals, trace, domain, and scope. Ifādah, mafhūm, hukm,
  tanzīl, reality, truth, ontology, and final meaning remain forbidden.
- GPT-R6: Reasonableness gates runtime surface — added
  `GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT`,
  `ReasonablenessGateDecision`, `ReasonablenessGateReport`, and
  `run_reasonableness_gates` with six bounded gates (maqam fit,
  origin binding completeness, evidence support, contradiction check,
  forbidden leap check, and rank/residual policy). GPT-R7 is now next.
- GPT-R7: GPTAnswerReasonablenessVerdict runtime surface — added
  `GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT`,
  `GPTAnswerReasonablenessVerdict`, `ReasonablenessVerdictState`, and
  `prove_gpt_answer_reasonableness_verdict` consuming GPT-R6 gate reports
  only. GPT-R8 audit integration is now next; certificate/authority semantics
  remain forbidden.
- LAFZI-D1: CoupledDalalah carrier surface — carrier-only handoff from the
  CLOSED C8 CoupledDalalahGateResult preserving wadʿī/lafẓī refs, boundary,
  domain/scope, prior knowledge refs, visible residuals, rank, and trace.
  MutabaqahGate, TadammunGate, IltizamGate, ifādah, hukm, tanzīl, truth,
  and reality remain forbidden at this step.
- LAFZI-C4: UsageScopeGate — bounded W3 gate result over
  WadiMadlulContract plus prior WadAuthorityGateResult. Preserves domain,
  scope boundary, rank, residual visibility, trace, and forbids closure or
  CoupledDalalah / mutabaqah / tadammun / iltizam outputs.
- State-truth cleanup: README, roadmap, and agent staging now record the
  project as constitutional/research alpha, docs/62 as ratified law-only
  LAFZI-D0, and runtime LAFZI-D1 through LAFZI-D6 as staged after LAFZI-C8.
- LAFZI-C3: WadAuthorityGate — bounded W2 gate result preserving visible
  authority family/ref, evidence ref, residuals, rank, and trace.
- LAFZI-D0: Coupled Dalalah Matrix Law (docs/62) — law-only staging for
  CoupledDalalah, MutabaqahGate, TadammunGate, IltizamGate, residual audit,
  and WordCapability integration after Wad'iMadlulClosed.
- LAFZI-C1/C2: Wad'i carrier surface and WadKindGate for the wadʿī condition
  chain opened by docs/60.
- DAL-A1: DalAlone carrier surface + local residual vocabulary.
- GPT-R1 through GPT-R5: GPT answer input, MaqamGPT, MantuqGPT extraction,
  MafhumGPT extraction, and Origin Binding Gate. The final reasonableness
  gates/verdict/audit integration remain planned as GPT-R6 through GPT-R8.
- GPT-K2: Minimal Golden Origins Dataset for auditable origin-binding tests.
- GPT-K1: Origin Schema Carriers — frozen dataclasses for the five Knowledge
  Origins (EntityGenusOrigin, AttributeEventOrigin, RelationOperatorOrigin,
  ReferenceOrigin, EvidenceOrigin) plus OriginBinding and OriginResidual
  carriers. New module: src/taaqqul_slot_geometry/gpt/. Enums: OriginRank,
  OriginStability, OriginResidualKind, BindingVerdict, EvidenceDirection,
  ResolutionType. 57 acceptance tests. No verdicts, no gates, no pipeline.
  Flips GPT-K0 marker to done.
- GPT-K0: docs/55 (Knowledge Origins Boundary Law) + acceptance tests
  defining the structural frame for the five Knowledge Origins, OriginBinding,
  OriginResidual, NeedGate integration, and the Transparent Reasonableness
  Barrier framing. Flips CLOSE-1 and GPT-R0 markers to done.
- CLOSE-1: LICENSE (Apache-2.0), CHANGELOG, updated README and pyproject.toml
  reflecting post-vertical constitutional state.
- GPT-R0: docs/54 (GPT Answer Reasonableness Objective Law) + 33 acceptance
  tests declaring that the project's operational objective is GPT answer
  reasonableness verification.

## Chain History (PR-0 through CLOSE-1)

The following is a summary of the constitutional chain. The authoritative
record lives in `docs/14_PR_CHAIN_ROADMAP.md`.

### Core Kernel (PR-0 through PR-6.1)

- **PR-0**: Scaffold + constitutional documents (docs/00–10)
- **PR-1A**: Mathematical Slot Geometry Constitution + minimal carriers
- **PR-1B**: Constitutional Test Geometry + PR Geometry + template + roadmap
- **PR-1C**: Pre-SlotGraph constitutional closure (docs/15–17)
- **PR-2**: SlotGraph + GammaClosure implementation
- **PR-2A**: Harden SlotGraph construction (corrective)
- **PR-3**: RankLattice + ResidualPolicy + EvidenceContract
- **PR-4**: TransitionGate + FailureTaxonomy bindings
- **PR-5**: Forbidden Straight-Line Registry
- **PR-6**: AnswerAudit wrapper (ModelClient protocol, no adapters)
- **PR-6.1**: Harden AnswerAudit trace coherence (corrective)

### Adapter Layer (PR-7 through PR-8.1)

- **PR-7**: Adapter Boundary Law (docs/18 — law only)
- **PR-8**: First concrete ModelClient adapter
- **PR-8.1**: Harden AdapterGuard static judging purity (corrective)

### Arabic Weight Branch (PR-9 through PR-14)

- **PR-9**: Arabic Weight Boundary Law (docs/19 — law only)
- **PR-9A**: Pre-Weight Licensing Law (docs/20 — law only)
- **PR-10**: Weight + pre-weight carrier surface
- **PR-10B**: Clarify carrier declarations are not gate verdicts (corrective)
- **PR-11**: Pre-weight path gates
- **PR-11B**: Clarify hidden-residual wording (corrective)
- **PR-12**: Pre-weight chain operations (mu_seq through mu_weight_readiness)
- **PR-13**: Minimal WeightFit operation
- **PR-14**: Lexical / Sama / Qiyas License Boundary

### Pre-Semantic Path (PR-15 through PR-19)

- **PR-15**: DalOnlyCandidate Boundary (signifier alone)
- **PR-16**: VerbalMadlulCandidate Boundary (verbal signified alone)
- **PR-16B**: Unified Pre-Semantic Chain Report (integration)
- **PR-16C**: Pre-Semantic Registry Contract
- **PR-16C.1**: Registry Closure Discipline (corrective)
- **PR-17**: Dal-Madlul Binding Candidate
- **PR-18**: ContractableUnitGeometry
- **PR-19**: Composition / RelationCandidate

### Formal Shape Registry (PR-F1 through PR-F8)

- **PR-F1**: Formal Shape Registry Law (docs/34 — law only)
- **PR-F2**: Word-Class Formal Definitions (ISM / FI'L / HARF)
- **PR-F2.1**: Word-Class MCE Hardening (corrective)
- **PR-F3**: Built and Reference Formal Definitions
- **PR-F4**: Weight Formal Definitions
- **PR-F5**: Inflection Formal Definitions
- **PR-F6**: Contract Slot Formal Definitions
- **PR-F7**: Composition Pattern Formal Definitions
- **PR-F7.1**: Chain Correction: No Ifadah before Mufrad Dalalah Closure
- **PR-F8**: Formal Style Candidate

### Mufrad Dalalah Closure (PR-D1 through PR-D4)

- **PR-D1**: Mufrad Semantic Slot Geometry
- **PR-D1.2**: Maqam / Context Boundary Readiness
- **PR-D2**: Mutabaqah / Tadammun / Iltizam Candidate
- **PR-D3**: Mufrad Dalalah Closure
- **PR-D4**: Relation Closure

### Vertical Closure (PR-D5 through PR-D10)

- **PR-D5**: Ifadah Boundary Law (docs/41 — law only)
- **PR-D5.1**: Stabilize Ifadah Boundary Law identifiers (corrective)
- **PR-D5.2**: Finalize Ifadah Boundary verdict identifier surface (corrective)
- **PR-D6**: SpeechForce / FormalStyle Bridge Law (docs/42 — law only)
- **PR-20**: IfadahCandidate (proposition candidate)
- **PR-D7**: Hukm Domain Boundary Law (docs/43 — law only)
- **PR-21**: HukmCandidate (judgment candidate)
- **PR-D8**: Manat Boundary Law (docs/44 — law only)
- **PR-D8.1**: Stabilize Manat Boundary Law references (corrective)
- **PR-D8.2**: Clarify Manat Law source roles (corrective)
- **PR-21M**: ManatCandidate
- **PR-D9**: Tanzil Presentation Boundary Law (docs/45 — law only)
- **PR-22**: TanzilCandidate
- **PR-22-AUDIT**: Vertical Chain AnswerAudit Bridge
- **PR-D10**: Vertical Path Closure Law (docs/46)

### Post-Vertical Phase (PV0 through PV-A4.1)

- **PV0**: Post-Vertical Roadmap Amendment (docs/47)
- **PV-A1**: Mantuq Boundary Law (docs/48 — law only)
- **PV-A1.1**: Clarify Mantuq Boundary Lexical-Origin Requirement (corrective)
- **PV-A2**: MantuqClosure code
- **PV-A2.2**: Enforce Upstream Mufrad-Dalalah Continuity (corrective)
- **PV-A2.3**: Harden Mantuq Upstream Continuity Tests (corrective)
- **PV-M0**: Meta-Language Boundary Covenant (docs/49 — law only)
- **PV-M0.2**: Clarify MetaTermContract schema-level trace obligation (corrective)
- **PV-M0.3**: Stabilize MetaTermContract trace schema and chain markers (corrective)
- **PV-T0**: Constitutional Test Origin Covenant (docs/52 — law only)
- **PV-T0-C1**: Stabilize Constitutional Test Origin Covenant Surface (corrective)
- **PV-A3**: Mafhum Boundary Law (docs/50 — law only)
- **PV-A4**: MafhumClosure code
- **PV-A4.1**: Maqul Branch Discipline Law (docs/51 — law only)

### Project Closure (CLOSE family)

- **CLOSE-2**: Project Methodology, Objectives, and KPI Plan (docs/53)
- **CLOSE-2.1**: Stabilize post-merge methodology/KPI chain state (corrective)
- **CLOSE-1**: Project State Truth (this entry)
