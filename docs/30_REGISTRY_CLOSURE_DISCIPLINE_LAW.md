# 30 — Registry Closure Discipline Law

> **Status:** Constitutional law. Ratified in PR-16C.1 (Amendment-7).
> This document binds every PR that opens, consumes, or depends upon
> a semantic/wadʿi/dalālah lexicon. It extends the registry contract
> (docs/29) by requiring registry closure before any semantic lexicon
> access.

## 0. Governing principle

```text
No Meaning Before Registry Closure.
No Wadʿi / Semantic / Dalālah Lexicon before RegistryClosureVerdict.
No semantic lexicon access without a CLOSED verdict for the required scope.
RegistryClosureVerdict is not meaning.
RegistryClosureVerdict is a gate discipline, not a semantic verdict.
```

The registry contract (docs/29, PR-16C) ensures that no binding can
proceed without a lookup result for both parties. This law extends
that guarantee: even after binding succeeds, no semantic or wadʿi
lexicon may open until the pre-semantic registry is *closed* for the
relevant scope and domain. Closure means: all required entries in a
given domain and scope have been registered, and no further
admissions are pending.

## 1. Registry scope

The pre-semantic registry operates in two scopes:

```text
RegistryScope:
    MUFRAD    — single-word (individual signifier or signified)
    TARKIB    — compositional (multi-word structure)
```

Each scope is independent. Closure in MUFRAD scope does not imply
closure in TARKIB scope. TARKIB closure cannot precede composition
readiness (PR-19).

## 2. Registry closure kinds

The four closure kinds combine domain (docs/29 §1) with scope:

```text
RegistryClosureKind:
    DAL_ONLY_MUFRAD           — signifier registry, single-word
    DAL_ONLY_TARKIB           — signifier registry, compositional
    VERBAL_MADLUL_MUFRAD      — verbal signified registry, single-word
    VERBAL_MADLUL_TARKIB      — verbal signified registry, compositional
```

Each kind is independently closable. One kind being CLOSED does not
imply another is CLOSED.

## 3. Registry closure states

```text
RegistryClosureState:
    CLOSED    — the registry is sealed for this kind; no further
                admissions; semantic lexicon access is licensed
    REFUSED   — closure was attempted but a precondition failed;
                semantic access is forbidden
    DEFERRED  — closure cannot be determined now; the verdict
                is pending; semantic access is forbidden
```

Only `CLOSED` licenses downstream semantic lexicon access.
`REFUSED` and `DEFERRED` both block any semantic/wadʿi/dalālah
lexicon from opening.

## 4. Registry closure verdict

```text
RegistryClosureVerdict:
    kind            — RegistryClosureKind; which combination is judged
    state           — RegistryClosureState; the outcome
    failure_code    — FailureCode | None (present iff REFUSED)
    residuals       — tuple[Residual, ...]; visible, never hidden
    trace_ref       — str; non-empty trace reference
```

Birth guards enforce:
- `kind` is a valid `RegistryClosureKind` member.
- `state` is a valid `RegistryClosureState` member.
- `CLOSED` => failure_code is None.
- `REFUSED` => failure_code is a `FailureCode` member.
- `DEFERRED` => failure_code is None.
- `residuals` is a tuple of `Residual` carriers (no untyped entries).
- `trace_ref` is a non-empty string.

## 5. Semantic lexicon boundary

```text
SemanticLexiconBoundary cannot open unless the required
RegistryClosureVerdict is CLOSED for its scope.
```

Specifically:

```text
Mufrad semantic/dalālah access requires:
- DAL_ONLY_MUFRAD closure = CLOSED
- VERBAL_MADLUL_MUFRAD closure = CLOSED

Tarkib semantic/dalālah access requires:
- DAL_ONLY_TARKIB closure = CLOSED
- VERBAL_MADLUL_TARKIB closure = CLOSED
- Composition readiness (PR-19 must be merged)
```

This law does not close the tarkib registry now. It defines the
discipline. TARKIB closure is deferred until composition exists.

## 6. Relationship to the DEFERRED state

DEFERRED in a RegistryClosureVerdict is not a refusal. It is an
explicit acknowledgment that the verdict cannot be produced now.

```text
DEFERRED is not refusal.
DEFERRED carries no FailureCode.
DEFERRED blocks semantic lexicon access (same as REFUSED).
If a future verdict transitions from DEFERRED to REFUSED,
the transition must carry a named FailureCode.
```

This clarifies the interaction with the "every refusal is named"
principle: DEFERRED is not itself a refusal — it is a suspension.
Only REFUSED is a refusal, and only REFUSED carries a FailureCode.

## 7. Relationship to PR-16C (registry contract)

This law extends but does not replace docs/29. The registry contract
(PR-16C) defines entries, domains, lookup states, and lookup results.
This law adds:

- The concept of scope (MUFRAD / TARKIB).
- The concept of closure (the registry is sealed).
- The concept of closure verdict (the gate judgment on closure).
- The prohibition of semantic lexicon access before closure.

The registry contract remains the authority on entry shape, domain
partitioning, and lookup protocol. This law adds the closure
discipline that prevents premature semantic access.

## 8. Relationship to PR-17 (binding)

PR-17 binds signifier to verbal signified using RegistryLookupResult
(docs/29 §8). The binding does not require registry closure — only
registry lookup. However, after binding succeeds, no semantic lexicon
may open on the binding result until the relevant registry closure
verdicts are CLOSED.

```text
Binding (PR-17) requires: lookup FOUND for both parties.
Semantic access (later): requires closure CLOSED for the scope.
```

These are two distinct gates. Binding is the earlier gate; closure
is the later gate. Neither substitutes for the other.

## 9. Forbidden surface

PR-16C.1 must not produce:

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
- C_Aug
- composition
- adapter or audit changes
- new runtime dependencies
- closure of TARKIB registry (only the law, not the closure)
```

## 10. Rank ceiling

```text
REGISTRY_CLOSURE_RANK_CEILING = REGISTRY_RANK_CEILING
```

The closure verdict does not promote rank. It inherits the rank
ceiling from the registry contract (docs/29 §3).

## 11. Constitutional KPIs

```text
KPI-1  Birth-guard completeness     — 100% (every malformed verdict refused)
KPI-2  State/FailureCode coherence  — 100% (CLOSED => no FC; REFUSED => FC)
KPI-3  Rank bound compliance        — 100% (no verdict above ceiling)
KPI-4  Residual visibility          — 100% (no hidden residuals)
KPI-5  Named refusal coverage       — 100% (every REFUSED carries FailureCode)
KPI-6  Scope independence           — 100% (MUFRAD and TARKIB are independent)
KPI-7  Forbidden output absence     — 100% (no meaning, no lexicon, no content)
KPI-8  DEFERRED discipline          — 100% (DEFERRED is not refusal, no FC)
```

## 12. Golden law

```text
The registry closure discipline makes semantic access reviewable.
It does not make the registry complete.
It does not open a semantic lexicon.
It defines the gate that must be passed before any semantic lexicon opens.
Closure is a discipline, not content.
```
