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
Trace → SlotGraph → Gamma → Candidate → Rank → Residuals → TransitionContract → Output
```

The repository is **not** an Arabic NLP toolkit, a GPT clone, or an attempt
to reverse-engineer any language model's internal weights or hidden
chain-of-thought. See [`docs/01_BLACK_BOX_BOUNDARY.md`](docs/01_BLACK_BOX_BOUNDARY.md).

## What this repository is *not*

This repository does **not** claim to expose the hidden internal reasoning
of GPT or any other language model. Instead, it builds a constitutional
slot-geometry layer *around* generated answers. Every input, claim,
transition, and output must pass through `SlotGraph` construction,
`Gamma` minimal closure, `RankLattice`, `ResidualPolicy`, `EvidenceGate`,
and `TraceLedger`. The goal is to prevent false straight-line transitions
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

PR-0 (this commit) ships only the scaffold and the constitutional
documents. The core kernel (`SlotGraph` + `GammaClosure`) lands in PR-1.
See [`docs/00_FOUNDATIONAL_ARTICLE.md`](docs/00_FOUNDATIONAL_ARTICLE.md)
for the staged roadmap.

## Layout

```text
Taaqol-GPT/
├── pyproject.toml
├── README.md
├── CLAUDE.md
├── docs/
│   ├── 00_FOUNDATIONAL_ARTICLE.md
│   ├── 01_BLACK_BOX_BOUNDARY.md
│   ├── 02_SLOT_GEOMETRY_CONSTITUTION.md
│   ├── 03_GAMMA_CLOSURE_CONTRACT.md
│   ├── 04_FORBIDDEN_STRAIGHT_LINES.md
│   ├── 05_RANK_LATTICE.md
│   ├── 06_RESIDUAL_POLICY.md
│   ├── 07_TRACE_LEDGER.md
│   ├── 08_TRANSITION_GATE.md
│   ├── 09_ARABIC_APPLICATION_BOUNDARY.md
│   └── 10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md
├── src/taaqqul_slot_geometry/
│   └── __init__.py
└── tests/
    └── test_package_imports.py
```

## Development

Requires Python 3.11+. There are no runtime dependencies in PR-0 through
PR-4.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

ruff check .
pytest
```

## License

Apache-2.0. See `LICENSE` (to be added in a follow-up PR).
