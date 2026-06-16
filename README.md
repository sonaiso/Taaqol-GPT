# Taaqol-GPT

> **Taaqqul Slot Geometry Engine** — a constitutional, model-agnostic layer
> for traceable, rank-bounded, residual-visible reasoning outputs.

---

## What this repository is

`Taaqol-GPT` hosts the Python package **`taaqqul_slot_geometry`**: a
*constitutional reasoning engine* that wraps any claim — whether it comes
from a human author, a rule system, or a language model — and forces it
through a fixed seven-stage pipeline:

```text
Trace → SlotGraph → Gamma → Candidate → Rank → Residuals → TransitionGate → Output
```

The engine enforces that no output passes without an auditable trace, a
closed SlotGraph, a Gamma verdict, a bounded rank, visible residuals, an
evidence contract, and a licensed gate transition.

The repository is **not** an Arabic NLP toolkit, a GPT clone, or an attempt
to reverse-engineer any language model's internal weights or hidden
chain-of-thought. See [`docs/01_BLACK_BOX_BOUNDARY.md`](docs/01_BLACK_BOX_BOUNDARY.md).

## What this repository is *not*

This repository does **not** claim to expose the hidden internal reasoning
of GPT or any other language model. Instead, it builds a constitutional
slot-geometry layer *around* generated answers. Every input, claim,
transition, and output must pass through `SlotGraph` construction,
`Gamma` minimal closure, `RankLattice`, `ResidualPolicy`,
`EvidenceContract`, `TransitionGate`, and `TraceLedger`. The goal is to
prevent false straight-line transitions
such as `Signifier → Meaning`, `Weight → Agency`, `Evidence → Certainty`,
`Candidate → Certificate`, or `Tool/Number/LCNV → Knowledge`.

## بالعربية

لا يدّعي هذا المستودع كشف التفكير الداخلي المخفي للنموذج، بل يبني طبقةً
دستوريةً خارجيةً تجعل كل جواب قابلًا للتتبع والتقييم. فلا يمر أثرٌ إلى معنًى،
ولا معنًى إلى حكم، ولا دليلٌ إلى يقين، ولا أداةٌ إلى معرفة، إلا عبر خاناتٍ
مرخّصة، وإغلاق Gamma، ورتبة، وبقايا، ودليل، وأثرٍ محفوظ.

## Governing law

```text
No output without a SlotGraph.
No SlotGraph without a Gamma closure state.
No transition without a Gate.
No Gate without Evidence, Rank, and a Residual policy.
No approved output with hidden residuals.
No straight line from Evidence to Certainty.
No straight line from Tool / Number / LCNV to Knowledge.
No technical term moves between sciences without a licensed bridge.
```

## Project status — v0.1.0

The constitutional engine is **closed** as a functional vertical path.
The following layers are implemented, tested, and ratified:

### Core kernel (PR-0 through PR-6.1)

- `SlotGraph` + `construct()` — constitutional graph construction with
  mandatory center/boundary/rank/residuals/trace
- `gamma()` — pure ordered Gamma closure function (6 verdict states)
- `RankLattice` — bounded meet/join on ranks
- `ResidualPolicy` — residual visibility enforcement
- `EvidenceContract` — evidence source separation from model confidence
- `TransitionGate` — the sole transition authority (evidence + rank + residual)
- `TraceLedger` — immutable trace recording
- `ForbiddenLines` — straight-line registry preventing unlicensed transitions
- `AnswerAudit` — audit wrapper (gamma → gate → audit pipeline)

### Adapter layer (PR-7 through PR-8.1)

- `ModelClient` protocol — black-box boundary for LLM integration
- `AdapterGuard` — static judging purity enforcement
- `InMemoryAdapter` — first concrete adapter (behind Adapter Boundary Law)

### Arabic weight chain (PR-9 through PR-22-AUDIT)

The full vertical Arabic path is closed:

```text
PreWeightCandidate → WeightFit → LicensingBoundary
→ DalOnlyCandidate → VerbalMadlulCandidate → DalMadlulBinding
→ ContractableUnitGeometry → RelationCandidate
→ FormalShape (ISM/FI'L/HARF, Built/Reference, Weight patterns,
              Inflection, ContractSlot, CompositionPattern)
→ FormalStyleCandidate
→ MufradSemanticSlotGeometry → MaqamContextBoundary
→ Mutabaqah/Tadammun/Iltizam Candidates
→ MufradDalalahClosure → RelationClosure
→ IfadahCandidate → HukmCandidate → ManatCandidate → TanzilCandidate
→ AuditedTanzilBridge
```

### Post-vertical phase (PV0 through PV-A4.1)

- Mantuq Boundary Law + MantuqClosure (preserved spoken/textual origin)
- Mafhum Boundary Law + MafhumClosure (inferential branch from closed Mantuq)
- Meta-Language Boundary Covenant (prevents terminological domain confusion)
- Constitutional Test Origin Covenant (every new test must declare origin/branch/chain)
- Maqul Branch Discipline Law (names the existing chain as Maqul al-Dalalah)

### What is NOT shipped

The following remain **deferred** (explicitly declared, not forgotten):

- PV-M1: Mabni Stability Boundary Law
- Real Arabic parser from raw text
- External network adapters (OpenAI, Anthropic API)
- Government service engine
- GPT proposer layer
- Conditions DAG
- Haqiqah/Majaz/Naql branches
- Full orphan test audit (PV-T0.2)

## Architecture

```text
src/taaqqul_slot_geometry/
├── __init__.py                     # public API surface
├── core/                           # pure kernel — no I/O, no mutation
│   ├── closure_state.py            # ClosureState — the six Γ verdicts
│   ├── failure_taxonomy.py         # FailureCode — every named refusal
│   ├── slot_graph.py               # SlotGraph + carriers + construct()
│   ├── gamma.py                    # Γ — the pure ordered verdict function
│   ├── rank_lattice.py             # Rank + RankLattice (bounded meet/join)
│   ├── residual_policy.py          # Residual + ResidualPolicy
│   ├── evidence_contract.py        # EvidenceSource + EvidenceContract
│   ├── forbidden_lines.py          # Forbidden Straight-Line Registry
│   ├── transition_state.py         # TransitionState (leaf module)
│   ├── transition_gate.py          # TransitionGate + TransitionVerdict
│   └── trace_ledger.py             # TraceEntryCandidate + TraceLedger
├── audit/                          # designated impure shell
│   ├── model_client.py             # ModelClient protocol — black-box boundary
│   ├── successor.py                # emit_successor — pure emission half
│   ├── answer_audit.py             # AnswerAudit + AuditedAnswer
│   └── tanzil_bridge.py            # Vertical chain audit bridge
├── adapters/                       # concrete ModelClient implementations
│   ├── adapter_boundary.py         # AdapterGuard — static judging purity
│   └── in_memory.py                # InMemoryAdapter (test/dev adapter)
└── weight/                         # Arabic linguistic chain (candidates only)
    ├── carrier_core.py             # shared carrier declarations
    ├── pre_weight.py               # PreWeightCandidate + licensing
    ├── path_gate.py                # pre-weight path gates
    ├── mu_chain.py                 # μ chain operations
    ├── weight_fit.py               # WeightFit operation
    ├── weight_image.py             # weight image carrier
    ├── licensing_boundary.py       # lexical/samaʿ/qiyas licensing
    ├── dal_only.py                 # DalOnlyCandidate (signifier alone)
    ├── verbal_madlul.py            # VerbalMadlulCandidate (verbal signified)
    ├── dal_madlul_binding.py       # Dal-Madlul binding
    ├── contractable_unit_geometry.py # ContractableUnitGeometry
    ├── relation_candidate.py       # RelationCandidate (composition)
    ├── formal_shape.py             # FormalShape registry (ISM/FI'L/HARF)
    ├── formal_shape_built_reference.py  # pronouns, demonstratives
    ├── formal_shape_weight_pattern.py   # verbal/nominal/masdar patterns
    ├── formal_shape_inflection.py  # iʿrab/binaʾ/triptote/diptote
    ├── formal_shape_contract_slot.py    # formal agent/object/subject
    ├── formal_shape_composition.py # nominal/verbal/idafa patterns
    ├── formal_style_candidate.py   # khabar/inshaʾ formal style
    ├── mufrad_semantic_slot_geometry.py # semantic slot frame
    ├── maqam_context_boundary.py   # maqam/context readiness
    ├── dalalah_candidates.py       # mutabaqah/tadammun/iltizam
    ├── mufrad_dalalah_closure.py   # MufradDalalahClosure
    ├── relation_closure.py         # RelationClosure
    ├── ifadah_candidate.py         # IfadahCandidate (proposition)
    ├── hukm_candidate.py           # HukmCandidate (judgment)
    ├── manat_candidate.py          # ManatCandidate (ratio legis)
    ├── tanzil_candidate.py         # TanzilCandidate (application)
    ├── mantuq_closure.py           # MantuqClosure (preserved textual origin)
    ├── mafhum_closure.py           # MafhumClosure (inferential branch)
    ├── registry_contract.py        # pre-semantic registry contract
    ├── registry_closure.py         # registry closure discipline
    └── chain_report.py             # unified chain report
```

## Constitutional documents

53 constitutional law documents govern the engine (`docs/00` through `docs/52`).
The authoritative chain and per-step scope lives in
[`docs/14_PR_CHAIN_ROADMAP.md`](docs/14_PR_CHAIN_ROADMAP.md).

Key documents:

| Doc | Name | Scope |
|-----|------|-------|
| 01 | Black Box Boundary | No model-internal claims |
| 11 | Mathematical Slot Geometry Laws | Core mathematical structure |
| 12 | Constitutional Test Geometry | Test framework requirements |
| 14 | PR Chain Roadmap | Authoritative build chain |
| 18 | Adapter Boundary Law | ModelClient protocol boundary |
| 46 | Vertical Path Closure Law | Minimum vertical path closed |
| 47 | Post-Vertical Roadmap | Branch governance after closure |
| 52 | Constitutional Test Origin Covenant | Test origin discipline |

## Development

Requires Python 3.11+. The package has **no runtime dependencies** —
the kernel is standard-library only. Development tooling is `pytest`
and `ruff` (installed via the `dev` extra).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

ruff check .
pytest
```

## Test suite

The test suite contains 1739+ constitutional tests covering:

- Core kernel closure (SlotGraph, Gamma, RankLattice, ResidualPolicy)
- TransitionGate evidence/rank/residual enforcement
- Forbidden straight-line prevention
- AnswerAudit pipeline (gamma → gate → audit)
- Adapter boundary enforcement
- Full vertical Arabic chain (MufradDalalah → Tanzil → Audit)
- Post-vertical branches (Mantuq, Mafhum)
- Trace continuity and rank monotonicity

## License

Apache-2.0. See [`LICENSE`](LICENSE).
