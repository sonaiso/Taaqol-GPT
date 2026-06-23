# 61 — ProofObject Failure-Policy Alignment (Audit Only)

> **Status:** Audit-only policy document.
> This document constrains static coverage expectations only.
> It ships no runtime code, no evaluator, no kernel, and no computed verdict logic.

---

## §1 Scope

This policy links ProofObject kinds to:

- canonical failure family
- allowed `expected_verdict` labels in coverage cases
- residual policy label
- required metadata for static coverage authoring

This document is **non-runtime** and **non-executable**. It does not evaluate proofs.

---

## §2 Runtime Embargo

The following remain forbidden in this step:

- `binding_kernel.py`
- `decision_engine.py`
- `coverage_matrix_v0.1.yaml`
- computed verdict execution
- boolean-as-proof shortcuts (`domain_proved`, `identity_preserved`, `gate_passed`)
- certificate-style outputs

---

## §3 Alignment Table

| ProofObject | Failure family | Allowed expected verdict | Residual policy | Required metadata |
| --- | --- | --- | --- | --- |
| `MRKProof` | `MRK` | `EXPECTED_PROOF_REQUIRED` | `no_runtime` | `expected_failure_family` |
| `DomainProof` | `DOMAIN` | `EXPECTED_PROOF_REQUIRED` | `no_runtime` | `expected_failure_family` |
| `IdentityProof` | `IDENTITY` | `EXPECTED_BLOCKED`, `EXPECTED_PROOF_REQUIRED` | `identity_loss_residual` | `expected_failure_family` |
| `GateProof` | `GATE` | `EXPECTED_BLOCKED`, `EXPECTED_PROOF_REQUIRED` | `gate_residual` | `expected_failure_family` |
| `BridgeProof` | `BRIDGE` | `EXPECTED_BRIDGE_REQUIRED` | `bridge_required` | `required_bridges` |
| `EvidenceProof` | `EVIDENCE` | `EXPECTED_PROOF_REQUIRED` | `evidence_residual` | `expected_failure_family` |
| `CoverageProof` | `COVERAGE` | `EXPECTED_PROOF_REQUIRED`, `EXPECTED_RESIDUAL` | `coverage_residual` | `expected_failure_family`, `expected_residual_policy` |

All rows are audit-only policy rows. None is executable.

---

## §4 Canonical Policy Invariants

1. Every known ProofObject kind has exactly one policy row.
2. Every `failure_family` must be canonical.
3. Every `allowed_expected_verdict` must be schema-accepted.
4. `BridgeProof` failure maps to `EXPECTED_BRIDGE_REQUIRED` and family `BRIDGE`.
5. `IdentityProof` failure is not residual-only.
6. `EvidenceProof` failure cannot promote rank.
7. `CoverageProof` failure cannot emit computed verdict.
8. Every row is marked `AUDIT_ONLY`.

---

## §5 Audit-Only Declaration

```text
ProofObject failure policy is audit-only.
It does not evaluate proofs.
It does not emit computed verdict.
It does not open runtime.
It only constrains future coverage cases.
```
