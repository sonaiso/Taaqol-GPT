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
