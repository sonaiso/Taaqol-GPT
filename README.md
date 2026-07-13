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

وبذلك يعمل المشروع كتجربةٍ تنفيذيةٍ أولى لمحرك حقيقة منضبط (Truth Engine):
إنتاج معرفةٍ لغويةٍ مرخّصة مع حفظ الأثر وإمكان الرجوع، مع بقاء فجوات التنفيذ
المتبقية مُدارةً صراحةً عبر مصفوفة الحالة في `docs/91`.

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

Current status is **constitutional / research alpha**, not final public
readiness. Chain records in `docs/14_PR_CHAIN_ROADMAP.md` and `CLAUDE.md`
are synchronized through completed DAL and LAFZI runtime families
(`DAL-A8.1`, `LAFZI-B7`, `LAFZI-C8`, `LAFZI-D6`), completed GPT
reasonableness integration (`GPT-R8`), and completed closure/release-boundary
steps (`CLOSE-6.1`, `DAL-A4-ADMIT`, `LAW-E1R-A`).

`GPT-R8L` (law-only in `docs/56`) and `GPT-R8` (Shape A audit integration)
are both implemented as done chain steps.

`LAW-E0` is **✓ done (law-only)** in chain records. It does not open
runtime parser/morphology/syntax paths, and it does not license
semantic/ifādah/mafhūm/hukm/truth/certainty/reality outputs.
Its law surface is defined in `docs/63`.

`X0R-E1` carrier surface is **✓ done** as a generic runtime
carrier-only step (`LayerQuestionSet`, `EuclideanLayerContract`,
`LayerResidual`, `LayerClosureSurface`, `LayerTransitionReadiness`)
with no gate/closure execution and no parser/semantic opening.

`X0R-E2` origin-branch licensing carrier surface is **✓ done** as a
generic runtime carrier-only step (`OriginBranchLinkSurface`,
`OriginBranchLicensingContract`, `OriginBranchResidual`,
`OriginBranchReadinessState`) with no transition evaluation, no
certificate semantics, and no parser/semantic opening.

The authoritative per-step chain status (including what is done, planned, and
forbidden) lives in
[`docs/14_PR_CHAIN_ROADMAP.md`](docs/14_PR_CHAIN_ROADMAP.md).
For state-truth interpretation discipline, use
[`docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md`](docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md):
`docs/14`/`CLAUDE.md`/runtime+tests are live reference truth, while
`docs/71`..`docs/76` are historical snapshot records.
`docs/54` also contains a concise standard capsule
(Definitions/Axioms/Theorem/Claim-Boundary) for the GPT reasonableness
objective statement.
`docs/64` registers `CLOSE-3.1 Lift-the-Ban Matrix Law` as a
law-only closure-class protocol for future lift events; it does
not open any horizontal branch. `docs/67` registers `CLOSE-4
Golden Closure Fixtures Law` as a chain-truth snapshot, not a
certificate; it does not declare public readiness.
The authoritative chain — per-step scope, forbidden surface,
and current status — lives in
[`docs/14_PR_CHAIN_ROADMAP.md`](docs/14_PR_CHAIN_ROADMAP.md).

## Documentation navigation

To keep repository terminology and structure consistent:

- Use [`docs/README.md`](docs/README.md) as the entry index for document families.
- Use [`docs/TERMINOLOGY.md`](docs/TERMINOLOGY.md) for canonical term names and non-interchangeable terms.

## Layout

```text
Taaqol-GPT/
├── pyproject.toml
├── README.md
├── CLAUDE.md                            # AI agent operating instructions
├── LICENSE                              # Apache-2.0
├── CHANGELOG.md                         # chain history
├── docs/                                # constitutional law/audit documents
│   ├── 00_FOUNDATIONAL_ARTICLE.md
│   ├── ...
│   ├── 62_COUPLED_DALALAH_MATRIX_LAW.md
│   ├── 63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md
│   └── 74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md
├── website/                             # static local testing/readiness surface
│   ├── index.html
│   ├── styles.css
│   └── app.js
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
    └── test_*.py                        # 69 test modules (2064 tests)
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

To open the dependency-free local testing website:

```bash
python -m webbrowser website/index.html
```

## License

Apache-2.0. See [`LICENSE`](LICENSE).
