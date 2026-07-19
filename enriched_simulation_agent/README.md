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
- `AUX-ESA-F2` local bridge surface from `F experiment` into
  `EuclideanTransitionContract` vocabulary (compatibility only)
- `AUX-ESA-F3` strict bridge-field completion audit that keeps
  non-admission residuals and forbids kernel handoff/mutation calls
- `AUX-ESA-F4` local candidate-shaping surface after F3 audit
  (auxiliary-only, non-admission, non-chain-advancing)
- `AUX-ESA-F5` local contract-readiness precondition surface
  (precondition checks only; no admission and no chain advancement)
- `AUX-ESA-F6` local admission-precondition refinement for F5
  (distinguishes unsuccessful F4 shaping state from missing-shaped-candidates failure)

Triad mapping is constrained as a hypothesis only:

- `Program Entity ≈ اسم`
- `Program Transformation ≈ فعل`
- `Program Relation ≈ حرف`

## What this kernel does not prove

This kernel does not prove a simulation between Arabic and programming.
It does not prove a linguistic-to-knowledge bridge.
It does not prove real-world validity for `F`; validity here is local and falsifiable.
It does not promote `AUX-ESA-F2` into the main constitutional runtime layer.
It does not promote `AUX-ESA-F4` candidates into kernel admission.
It does not convert `AUX-ESA-F5` readiness into kernel admission or bridge completion.
It does not license WordCapability -> Relation / Ifadah / Hukm.
Triad mapping is only a structuring hypothesis.
A simulation is accepted only under a CoverageContract and preservation laws.

## Test Classification

`enriched_simulation_agent/tests/test_f_x0r_bridge.py` is a local pytest
regression suite for auxiliary precondition/readiness behavior (including F5/F5.1 hardening).
It is not a constitutional harness suite and does not constitute constitutional
admission or chain advancement.

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
