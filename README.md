# Taaqol-GPT

> **Taaqqul Slot Geometry Engine** — a constitutional, model-agnostic layer
> for traceable, rank-bounded, residual-visible reasoning outputs.

---

## What this repository is

`Taaqol-GPT` hosts the Python package **`taaqqul_slot_geometry`**: a
*constitutional reasoning engine* that wraps any claim — whether it comes
from a human author, a rule system, or a language model — and forces it
through a fixed auditable pipeline:

```text
Trace → SlotGraph → Gamma → Candidate → Rank → Residuals → TransitionGate → Output
```

The engine implements a complete vertical closure path:

```text
DalOnly → VerbalMadlul → Binding → ContractableUnit → Relation →
FormalShape → MufradDalalah → RelationClosure → Ifadah → Hukm →
Manat → Tanzil → AnswerAudit
```

And a post-vertical branch (Mantuq → Mafhum) governed by the
Maqul al-Dalalah discipline.

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

## Repository status

The constitutional kernel, audit layer, adapter boundary, Arabic weight
branch, pre-semantic path, formal shape registry, mufrad dalalah closure,
vertical closure (Ifadah → Hukm → Manat → Tanzil → AnswerAudit), and
post-vertical branches (Mantuq → Mafhum) are shipped and constitutionally
closed. The project methodology and KPI plan (docs/53) is ratified.

**94 pull requests** have been merged through the constitutional chain.
The authoritative chain — per-step scope, forbidden surface, and
current status — lives in
[`docs/14_PR_CHAIN_ROADMAP.md`](docs/14_PR_CHAIN_ROADMAP.md).

## Layout

```text
Taaqol-GPT/
├── pyproject.toml
├── README.md
├── CLAUDE.md                            # AI agent operating instructions
├── LICENSE                              # Apache-2.0
├── CHANGELOG.md                         # chain history
├── docs/                                # 55 constitutional documents (00–54)
│   ├── 00_FOUNDATIONAL_ARTICLE.md
│   ├── ...
│   └── 54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md
├── src/taaqqul_slot_geometry/
│   ├── __init__.py                      # public API surface
│   ├── core/                            # pure kernel — no I/O, no ledger writes
│   │   ├── closure_state.py             # ClosureState — the six Γ verdicts
│   │   ├── failure_taxonomy.py          # FailureCode — every named refusal
│   │   ├── slot_graph.py               # SlotGraph + carriers + construct()
│   │   ├── gamma.py                     # Γ — the pure ordered verdict function
│   │   ├── rank_lattice.py             # Rank + RankLattice (bounded meet/join)
│   │   ├── residual_policy.py          # Residual + ResidualPolicy
│   │   ├── evidence_contract.py        # EvidenceSource + EvidenceContract
│   │   ├── forbidden_lines.py          # Forbidden Straight-Line Registry
│   │   ├── transition_state.py         # TransitionState (leaf module)
│   │   ├── transition_gate.py          # TransitionGate + TransitionVerdict
│   │   └── trace_ledger.py             # TraceEntryCandidate + TraceLedger
│   ├── audit/                           # designated impure shell (docs/01, 07)
│   │   ├── model_client.py             # ModelClient protocol — black-box boundary
│   │   ├── successor.py                # emit_successor — pure emission half
│   │   └── answer_audit.py             # AnswerAudit + AuditedAnswer
│   ├── adapters/                        # concrete ModelClient adapters (docs/18)
│   │   ├── adapter_boundary.py         # AdapterGuard
│   │   └── in_memory.py                # InMemoryModelClient (reference adapter)
│   └── weight/                          # Arabic weight branch (docs/19, 20)
│       ├── carrier_core.py             # weight carriers
│       ├── pre_weight.py               # pre-weight licensing chain
│       ├── path_gate.py                # pre-weight path gates
│       ├── mu_chain.py                 # μ chain operations
│       ├── weight_fit.py               # weigh() → WeightFitCandidate
│       ├── weight_image.py             # WeightImage, Mizan
│       ├── licensing_boundary.py       # lexical/sama/qiyas licensing
│       ├── dal_only.py                 # DalOnlyCandidate
│       ├── verbal_madlul.py            # VerbalMadlulCandidate
│       ├── dal_madlul_binding.py       # DalMadlulBindingCandidate
│       ├── contractable_unit_geometry.py # ContractableUnitGeometry
│       ├── relation_candidate.py       # RelationCandidate
│       ├── formal_shape.py             # FormalShape registry (ISM/FIL/HARF)
│       ├── formal_shape_*.py           # built/reference, weight, inflection, etc.
│       ├── formal_style_candidate.py   # khabar/insha formal style
│       ├── mufrad_semantic_slot_geometry.py  # semantic slot frame
│       ├── maqam_context_boundary.py   # maqam/context boundary
│       ├── dalalah_candidates.py       # mutabaqah/tadammun/iltizam
│       ├── mufrad_dalalah_closure.py   # MufradDalalahClosure
│       ├── relation_closure.py         # RelationClosure
│       ├── ifadah_candidate.py         # IfadahCandidate
│       ├── hukm_candidate.py           # HukmCandidate
│       ├── manat_candidate.py          # ManatCandidate
│       ├── tanzil_candidate.py         # TanzilCandidate
│       ├── mantuq_closure.py           # MantuqClosure (post-vertical)
│       ├── mafhum_closure.py           # MafhumClosure (post-vertical)
│       ├── registry_contract.py        # pre-semantic registry
│       ├── registry_closure.py         # registry closure discipline
│       └── chain_report.py             # PreSemanticChainReport
└── tests/                               # constitutional test suite (docs/12)
    ├── support/constitutional_case.py   # ConstitutionalTestCase harness
    └── test_*.py                        # 45 test modules (1758 tests)
```

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

## License

Apache-2.0. See [`LICENSE`](LICENSE).
