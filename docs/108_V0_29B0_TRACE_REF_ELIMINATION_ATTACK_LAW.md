# 108 — V0.29b.0 TraceRef Elimination Attack Law

> Status: constitutional closure boundary + bounded runtime/specification document.
> Scope: close the constitutional status of `trace_ref` before opening any `pi_psi` projection work.
> Snapshot date: 2026-08-09.

## §1 Origin and objective

`V0.29a` closed structural independence but left one explicit residual:

```text
TraceRefConstitutivity = OPEN
```

`V0.29b.0` closes this residual with an elimination attack that must end in exactly one explicit decision:

```text
TRACE_REF_CONSTITUTIVE
or
TRACE_REF_NON_CONSTITUTIVE_REALIZATION_ONLY
```

## §2 Elimination attack form

Let `T_K_S0` be the structural theory from docs/107. Build a trace-elided theory:

```text
T_K_S0^- := T_K_S0 \ {trace_ref-linked constitutive constraints}
```

Then execute the attack question:

```text
exists M:
  M satisfies T_K_S0^-
  and M violates T_K_S0 only through trace_ref-linked axioms
```

If such witness exists and no independent structural collapse is proven,
`trace_ref` is not constitutive for class membership.

## §3 No-Renaming-Smuggling boundary

The attack is invalid if trace functionality is reintroduced by alias names.

```text
No-Renaming-Smuggling:
  origin_ref, lineage_ref, audit_ref, proof_ref, source_ref
  must not be used as hidden replacements for trace_ref constitutivity.
```

## §4 Acceptance criteria (execution gate)

1. `AC-1 Decision Completeness`
- Runtime emits one and only one explicit constitutivity decision.

2. `AC-2 Structural-only elimination witness`
- At least one admitted model under `T_K_S0^-` is excluded by `T_K_S0` only through trace-linked witnesses.

3. `AC-3 Anti-smuggling preserved`
- Anti-smuggling holds for both `T_K_S0` and `T_K_S0^-`.

4. `AC-4 No-Renaming-Smuggling`
- Alias-based reinjection is detected and refused.

5. `AC-5 Scope discipline`
- `V0.29b.0` does not open `pi_psi`, equivalence classes, FRP, finite quotient, or cutoff proofs.

## §5 Test matrix (minimal constitutional set)

- `B0-T01` docs scope + index registration.
- `B0-T02` runtime decision completeness.
- `B0-T03` trace-only counterexample witness discipline.
- `B0-T04` trace-elided theory anti-smuggling hygiene.
- `B0-T05` No-Renaming-Smuggling alias reinjection detection.

## §6 Transition contract to V0.29b.1

`V0.29b.1` may open only after `V0.29b.0` emits a closed decision.

`V0.29b.1` scope starts at structural projection independence (`pi_psi`) and claim blindness.

`V0.29b.2` scope starts at Non-Trivial Compression.

```text
Claim blindness:
M1|Sigma_pi = M2|Sigma_pi => pi_psi(M1) = pi_psi(M2)

Non-Trivial Compression:
exists M != N : pi_psi(M) = pi_psi(N)
```

These are downstream gates and are not proven in this document.

## §7 Closure statement for this step

The executable closure of this step is the explicit constitutivity verdict produced
by the `V0.29b.0` elimination attack runtime, with anti-smuggling and
No-Renaming-Smuggling audits passing.
