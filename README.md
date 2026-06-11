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

The constitutional kernel and the audit layer are shipped through
PR-6.1: `SlotGraph` + `gamma` (PR-2/PR-2A), `RankLattice` +
`ResidualPolicy` + `EvidenceContract` (PR-3), `TransitionGate` (PR-4),
the Forbidden Straight-Line Registry (PR-5), and the `AnswerAudit`
wrapper behind the `ModelClient` protocol (PR-6, hardened by PR-6.1).
Concrete LLM adapters, claim ingestion, persistence, and the Arabic
application layer are **not** shipped; they remain reserved for later
chain steps.

The authoritative chain — per-step scope, forbidden surface, and
current status — lives in
[`docs/14_PR_CHAIN_ROADMAP.md`](docs/14_PR_CHAIN_ROADMAP.md).

## Layout

```text
Taaqol-GPT/
├── pyproject.toml
├── README.md
├── CLAUDE.md
├── docs/                            # constitutional documents 00–17
│   ├── 00_FOUNDATIONAL_ARTICLE.md
│   ├── ...
│   └── 17_SLOTGRAPH_GENERATION_LAW.md
├── src/taaqqul_slot_geometry/
│   ├── __init__.py                  # public API surface
│   ├── core/                        # pure kernel — no I/O, no ledger writes
│   │   ├── closure_state.py         # ClosureState — the six Γ verdicts
│   │   ├── failure_taxonomy.py      # FailureCode — every named refusal
│   │   ├── slot_graph.py            # SlotGraph + carriers + construct()
│   │   ├── gamma.py                 # Γ — the pure ordered verdict function
│   │   ├── rank_lattice.py          # Rank + RankLattice (bounded meet/join)
│   │   ├── residual_policy.py       # Residual + ResidualPolicy
│   │   ├── evidence_contract.py     # EvidenceSource + EvidenceContract
│   │   ├── forbidden_lines.py       # Forbidden Straight-Line Registry
│   │   ├── transition_state.py      # TransitionState (leaf module)
│   │   ├── transition_gate.py       # TransitionGate + TransitionVerdict
│   │   └── trace_ledger.py          # TraceEntryCandidate + TraceLedger
│   └── audit/                       # designated impure shell (docs/01, 07)
│       ├── model_client.py          # ModelClient protocol — black-box boundary
│       ├── successor.py             # emit_successor — pure emission half
│       └── answer_audit.py          # AnswerAudit + AuditedAnswer
└── tests/                           # constitutional test suite (docs/12)
    ├── support/constitutional_case.py
    └── test_*.py
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

Apache-2.0. See `LICENSE` (to be added in a follow-up PR).
