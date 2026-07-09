# 82 — Wad'i to Naql/Majaz Boundary Law (LEX-BOUNDARY-L0)

> Status: constitutional law document (law-only).
> Scope: transition boundary discipline for lexical-evidence staged outputs.
> Snapshot date: 2026-07-09.

## §1 Governing negative-neighbor rule

```text
Wad'iMadlulLicensed NOT_EQUAL NaqliMadlulLicensed
Wad'iMadlulLicensed NOT_EQUAL MajaziMadlulLicensed
Wad'iMadlulLicensed DOES_NOT_IMPLY NaqliMadlulLicensed
Wad'iMadlulLicensed DOES_NOT_IMPLY MajaziMadlulLicensed
```

Licensing a wad'i candidate is a bounded proof about placed lexical usability.
It is not a license for transferred meaning (naql), metaphorical meaning (majaz),
contextual meaning, final meaning, hukm, truth, certainty, or reality.

## §2 Lexical attestation role

```text
LEXICAL_ATTESTATION_ROLE = WITNESS_ONLY
LEXICAL_ATTESTATION_OUTPUT = Wad'iCandidateOnly
```

A lexical attestation may support only candidate-level wad'i readiness.
It must not certify naqli or majazi licensing by itself.

## §3 Independent gate requirement

Transitions beyond wad'i are licensed only through independent gates:

```text
NaqlGate  = required for any Wad'i -> Naqli transition
MajazGate = required for any Wad'i -> Majazi transition
```

No automatic transition is constitutional.

### §3.1 NaqlGate minimum evidence surface

```text
original_wad_trace
transferred_usage_attestation
domain_of_transfer
historical_or_usage_evidence
preserved_identity_or_declared_shift
differentiating_feature
visible_residuals
```

### §3.2 MajazGate minimum evidence surface

```text
original_wad_trace
literal_path_status
qarina_sarifa
relation_type
maqam_context_evidence
literal_preventer
visible_residuals
```

## §4 Allowed and forbidden outputs

```text
ALLOWED_OUTPUTS = {
  Wad'iMadlulCandidate,
  Wad'iCompatibilityCandidate,
  LexicalEvidenceFitnessVerdict,
  NaqliMadlulCandidate,
  MajaziMadlulCandidate
}
```

`NaqliMadlulCandidate` and `MajaziMadlulCandidate` are allowed only after their
independent gate proofs in §3.

```text
FORBIDDEN_OUTPUTS = {
  NaqliMadlulLicensed_without_NaqlGate,
  MajaziMadlulLicensed_without_MajazGate,
  ContextualMeaning,
  FinalMeaning,
  Hukm,
  Truth,
  Certainty,
  Reality
}
```

## §5 Residual and rank discipline

```text
RESIDUAL_VISIBILITY = REQUIRED
DEFAULT_RESIDUAL_ON_MISSING_GATE = DEFERRABLE
RANK_CEILING_WITHOUT_INDEPENDENT_GATE = HYPOTHESIS
```

If `NaqlGate` or `MajazGate` evidence is missing, output remains blocked or
deferred with visible residuals. No hidden residual may accompany an approved
transition.

## §6 Runtime embargo in this step

```text
RUNTIME_NOT_OPENED = {
  lexical_evidence_gate,
  naql_gate_runtime,
  majaz_gate_runtime,
  lexical_meaning_runtime,
  truth_engine,
  hukm_engine
}
```

LEX-BOUNDARY-L0 is law-only and introduces no runtime code, no carriers,
no gate implementation, and no semantic/hukm/truth/reality execution surface.
