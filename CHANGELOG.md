# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses a constitutional chain (see `docs/14_PR_CHAIN_ROADMAP.md`)
rather than semantic versioning milestones — each entry corresponds to a
chain step, not a release.

## [Unreleased]

### Added
- LAFZI-C4: UsageScopeGate — bounded W3 gate result over
  WadiMadlulContract plus prior WadAuthorityGateResult. Preserves domain,
  scope boundary, rank, residual visibility, trace, and forbids closure or
  CoupledDalalah / mutabaqah / tadammun / iltizam outputs. Marks LAFZI-C5 as
  next.
- State-truth cleanup: README, roadmap, and agent staging now record the
  project as constitutional/research alpha, docs/62 as ratified law-only
  LAFZI-D0, and runtime LAFZI-D1 through LAFZI-D6 as deferred until LAFZI-C8.
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
