# Enriched Simulation Agent

A minimal governed programming kernel that enforces the transition chain:

`Candidate -> Gate -> Evidence -> Domain -> Rank -> Residuals -> Trace -> Verdict`

Verdicts are strictly one of:

`ACCEPT`, `DEFER`, `BLOCK`

## Run

```bash
cd enriched_simulation_agent
python -m pip install -e .[dev]
pytest -q
python -m sim_agent.demo
```
