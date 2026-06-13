# 29 — Pre-Semantic Registry Law

> **Status:** Constitutional law. Ratified in PR-16C (Amendment-6).
> This document binds every PR that consumes, produces, or governs
> registry entries in the pre-semantic chain (PR-17 and later).

## 0. Governing principle

```text
No binding before registry.
No Dal-Madlul Binding before the registry contract is ratified.
RegistryEntry is not meaning.
RegistryLookupResult is not a semantic verdict.
Registry lookup licenses pre-semantic admissibility only.
```

The pre-semantic registry contract exists to ensure that binding
(PR-17) cannot proceed without evidence that both the signifier
(DalOnlyCandidate) and the verbal signified (VerbalMadlulCandidate)
hold a classified entry in a pre-semantic registry. The contract
defines the *shape* of registry entries and the *protocol* for
lookup — it does not populate entries.

## 1. Registry domains

The pre-semantic registry is partitioned into two domains:

```text
RegistryDomain:
    DAL_ONLY        — entries classifying the signifier surface
    VERBAL_MADLUL   — entries classifying the verbal signified surface
```

Each domain is independent. A registry entry belongs to exactly one
domain.

## 2. Registry entry structure

A `RegistryEntry` is a frozen carrier with the following mandatory
fields:

```text
RegistryEntry:
    key             — str; unique identifier within its domain
    domain          — RegistryDomain; the domain this entry belongs to
    non_meaning_proof — str; explicit attestation that the entry
                        does not constitute meaning, ifādah, hukm,
                        or reality
    rank            — Rank; bounded by REGISTRY_RANK_CEILING
    residuals       — tuple[Residual, ...]; visible, never hidden
    trace_ref       — str; non-empty trace reference
```

Birth guards enforce:
- `key` is a non-empty string.
- `domain` is a valid `RegistryDomain` member.
- `non_meaning_proof` is a non-empty string.
- `rank` does not exceed `REGISTRY_RANK_CEILING`.
- `residuals` is a tuple of `Residual` carriers (no untyped entries).
- `trace_ref` is a non-empty string.

## 3. Registry rank ceiling

```text
REGISTRY_RANK_CEILING = CHAIN_REPORT_RANK_CEILING
```

The registry does not promote rank. No entry may be born above
`REGISTRY_RANK_CEILING`. The registry contract inherits the rank
ceiling from PR-16B (the chain report ceiling), which itself
inherits from PR-16 (the madlul boundary ceiling).

## 4. Registry lookup result

```text
RegistryLookupState:
    FOUND       — the candidate has a classified entry in the registry
    REFUSED     — the candidate has no entry; lookup refused
    DEFERRED    — the lookup cannot be completed now; deferred residual

RegistryLookupResult:
    state           — RegistryLookupState
    entry           — RegistryEntry | None (present iff FOUND)
    failure_code    — FailureCode | None (present iff REFUSED)
```

Birth guards enforce:
- `FOUND` ⇒ entry is a `RegistryEntry`, failure_code is None.
- `REFUSED` ⇒ entry is None, failure_code is a `FailureCode` member.
- `DEFERRED` ⇒ entry is None, failure_code is None.

## 5. Lookup operation

```text
lookup_registry_entry(
    candidate_key: str,
    domain: RegistryDomain,
    registry: tuple[RegistryEntry, ...],
) → RegistryLookupResult
```

A pure function. It:
1. Refuses empty `candidate_key` with `GATE_REQUIRED`.
2. Refuses invalid `domain` with `DOMAIN_MISSING`.
3. Searches `registry` for an entry matching `candidate_key` in the
   given domain.
4. Returns `FOUND` with the entry if matched.
5. Returns `REFUSED` with `REQUIRED_SLOT_EMPTY` if no match.

The function is pure: no I/O, no ledger, no network, no mutation.

## 6. Non-meaning attestation

Every `RegistryEntry` carries a `non_meaning_proof` field. This
field is a non-empty string attesting that the entry does not
constitute:

- final meaning (ma'nā / dalālah)
- ifādah (propositional content)
- hukm (judgment)
- reality (wāqi')

The attestation is structural: the field must be non-empty at birth.
The content of the attestation is not evaluated by the contract; it
exists so that no entry can travel without an explicit declaration
that it is not meaning.

## 7. Forbidden surface

PR-16C must not produce:

```text
- registry content (actual dal entries, actual verbal-madlul entries)
- lexicon
- phonetic tables
- grammatical tables
- meaning / dalālah
- ifādah
- hukm
- reality / wāqi'
- ontology
- DalMadlulBindingCandidate
- ContractableUnitGeometry
- ExtraLetterLicense
- 𝒞_Aug
- composition
- adapter or audit changes
- new runtime dependencies
```

## 8. Relationship to PR-17

PR-17 (Dal-Madlul Binding) must:
- Consume `RegistryLookupResult` as input evidence for both parties.
- Refuse binding if either party's lookup result is not `FOUND`.
- Not create or populate registry entries.
- Not produce meaning, ifādah, hukm, or reality.

## 9. Constitutional KPIs

```text
KPI-1  Birth-guard completeness     — 100% (every malformed entry refused)
KPI-2  Non-meaning proof presence   — 100% (no entry without attestation)
KPI-3  Rank bound compliance        — 100% (no entry above ceiling)
KPI-4  Residual visibility          — 100% (no hidden residuals)
KPI-5  Lookup purity                — 100% (pure function, no I/O)
KPI-6  Named refusal coverage       — 100% (every refusal carries FailureCode)
KPI-7  Forbidden output absence     — 100% (no meaning, no binding, no content)
```

## 10. Golden law

```text
The registry contract makes the registry reviewable.
It does not make the registry complete.
Completeness is a future Amendment concern.
The contract is the gate to binding.
```
