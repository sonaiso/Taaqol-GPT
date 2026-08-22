# 118 — GUA-1 Proof Integrity Boundary Law (GUA-1R)

> Status: constitutional hardening boundary document (runtime-hardening only).
> Scope: ratify and harden the already-merged GUA scaffold under `src/taaqqul_slot_geometry/gua/`.
> Snapshot date: 2026-08-22.

## §1 Constitutional role

`GUA-1R` does not open a new branch family.

It hardens the merged GUA scaffold so `GUA1ProofCertificate` can no longer report `PASS` under residual concealment, hash substitution, suite substitution, or trace substitution.

## §2 Governing law

```text
No GUA pass with hidden residuals.
No GUA pass with blocking residuals.
No freeze acceptance without extraction-hash equality.
No realization acceptance without frozen-core hash equality.
No cross-domain pass unless suite contracts equal the certified tuple.
No chain pass without trace continuity from extraction to certificate.
```

## §3 Licensed artifact chain

`GUA-1R` binds one auditable chain:

```text
GeneralCoreExtraction
-> CoreFreeze
-> 4 Realizations
-> SharedConstitutionalSuite
-> CrossDomainSuite
-> GUA1ProofCertificate
```

## §4 PASS predicate

`GUA1_PASS` is licensed iff all of the following hold in one chain instance:

1. extraction trace continuity is preserved.
2. `compute_general_core_extraction_hash(extraction) == core_freeze.extraction_hash`.
3. all four realization domains are present exactly once.
4. every realization uses the same `frozen_core_hash` as the certified freeze.
5. `SharedConstitutionalSuite` witnesses are artifact-derived (not caller booleans).
6. `CrossDomainSuite.contracts == realizations`.
7. all stage traces are continuous.
8. residual safety holds: no hidden residual and no blocking residual.

## §5 Forbidden surface

The following are forbidden:

- `PASS` with hidden residual.
- `PASS` with blocking residual.
- freeze/realization hash mismatch accepted as pass.
- cross-domain suite tuple substitution accepted as pass.
- trace substitution across extraction/freeze/realization/suite/certificate.
- self-attested boolean suite claims accepted without witness binding.
- direct `GUA1ProofCertificate` construction accepted as a parallel
  issuance path.

## §6 Test discipline

Constitutional tests for GUA chain closure must use `ConstitutionalChainTestCase` (docs/12 §9), and include negative tests for:

- forged freeze hash,
- realization hash mismatch,
- suite tuple mismatch,
- hidden residual,
- blocking residual,
- trace substitution,
- direct certificate-constructor forging,
- domain incompleteness/coherence failures.

## §7 Boundary of this step

`GUA-1R` does not:

- mutate `src/taaqqul_slot_geometry/core`,
- open semantic/hukm/truth/reality paths,
- grant certificate rank promotion,
- alter adapter/audit boundary contracts.

## §8 Constitutional effect

`GUA-1` is ratified only as a hardened bounded runtime surface under this law.

Without §4 and §5 conditions, any reported GUA pass is constitutionally invalid.
