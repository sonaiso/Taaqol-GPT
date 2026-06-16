# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-06-16

### Project Closure: Constitutional Engine v0.1

This release closes the constitutional engine as a functional vertical
path. The engine enforces: Trace → SlotGraph → Gamma → Candidate →
Rank → Residuals → TransitionGate → Output on every claim.

### Added

- **Core kernel** (PR-0 through PR-6.1): SlotGraph, Gamma closure,
  RankLattice, ResidualPolicy, EvidenceContract, TransitionGate,
  TraceLedger, ForbiddenLines registry, AnswerAudit wrapper.
- **Adapter layer** (PR-7 through PR-8.1): ModelClient protocol,
  AdapterGuard (static judging purity), InMemoryAdapter.
- **Arabic vertical chain** (PR-9 through PR-22-AUDIT):
  PreWeight → WeightFit → LicensingBoundary → DalOnly → VerbalMadlul
  → DalMadlulBinding → ContractableUnit → Relation → FormalShape
  (6 sub-registries) → FormalStyle → MufradSemanticSlot → Maqam
  → Dalalah relations → MufradDalalahClosure → RelationClosure
  → Ifadah → Hukm → Manat → Tanzil → AuditedTanzilBridge.
- **Post-vertical branches** (PV0 through PV-A4.1): MantuqClosure,
  MafhumClosure, Meta-Language Boundary Covenant, Constitutional
  Test Origin Covenant, Maqul Branch Discipline Law.
- **53 constitutional law documents** (docs/00 through docs/52).
- **1739+ constitutional tests** covering kernel, gate, audit, adapter,
  vertical Arabic chain, post-vertical branches, trace continuity,
  rank monotonicity, and forbidden straight-line prevention.
- **LICENSE** file (Apache-2.0).

### Deferred (explicitly declared residuals)

- PV-M1: Mabni Stability Boundary Law
- PV-T0.1: Test origin scanner/enforcement
- PV-T0.2: Full orphan test audit
- External network adapters (OpenAI, Anthropic)
- Real Arabic parser from raw text
- Government service engine
- GPT proposer layer
- Conditions DAG
- Haqiqah/Majaz/Naql branches

### Constitutional invariants proven

- No output without SlotGraph
- No transition without Gate
- No Gate without Evidence + Rank + Residual policy
- No approved output with hidden residuals
- No straight line (Evidence→Certainty, Candidate→Certificate, etc.)
- No model confidence as evidence (black-box boundary)
- No rank promotion without gate
- No Ifadah before RelationClosure + MufradDalalahClosure
- No Hukm before Ifadah
- No Tanzil before Hukm + Manat
- No execution (Tanzil = presentation/application candidate only)
- No new orphan tests (test origin covenant)
