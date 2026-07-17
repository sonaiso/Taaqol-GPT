# Enriched Simulation Agent

A minimal governed programming kernel that enforces the transition chain:

`Candidate -> Gate -> Evidence -> Domain -> Rank -> Residuals -> Trace -> Verdict`

Verdicts are strictly one of:

`ACCEPT`, `DEFER`, `BLOCK`

## AUX-ESA Law Coverage

This kernel now includes auxiliary law coverage for:

- `IdentitySimulationLaw`
- `CompositionSimulationLaw`
- `OperationHomomorphismLaw`
- `ResidualReflectionLaw`
- `CoverageContractLaw`
- `NonTrivialityStrengtheningLaw`

Triad mapping is constrained as a hypothesis only:

- `Program Entity ≈ اسم`
- `Program Transformation ≈ فعل`
- `Program Relation ≈ حرف`

## What this kernel does not prove

This kernel does not prove a simulation between Arabic and programming.
It does not prove a linguistic-to-knowledge bridge.
It does not license WordCapability -> Relation / Ifadah / Hukm.
Triad mapping is only a structuring hypothesis.
A simulation is accepted only under a CoverageContract and preservation laws.

## ما الذي لا تثبته هذه النواة

هذه النواة لا تثبت وجود المحاكاة بين العربية والبرمجة.
ولا تفتح أي جسر من WordCapability إلى Relation أو Ifadah أو Hukm.
ولا تجعل الثالوث برهانًا، بل تجعله فرضية تنظيم تخضع للفحص.

## Run

```bash
cd enriched_simulation_agent
python -m pip install -e .[dev]
pytest -q
python -m sim_agent.demo
```
