# 40 — Relation Closure Law

> **Status:** Constitutional law. Ratified by PR-D4.
> This document binds PR-D4 and every later PR that depends on
> RelationClosure (PR-20 onward). It is load-bearing.

## §1 Governing principle

```text
No RelationClosure without two MufradDalalahClosure-proven units.
No RelationClosure without a RelationType.
No RelationType without a maqam bounding the relation.
No maqam is valid unless it bounds the relation itself.
No Ifadah inside PR-D4.
No Hukm inside PR-D4.
No meaning inside PR-D4.
```

RelationClosure proves that a relation between two singular
dalalah-closed units is formally closed as a **candidate**. It does
not determine meaning, ifadah, hukm, reality, or mafhum.

## §2 Minimal RelationType

PR-D4 introduces the minimal set of relation types. This set is
intentionally small — extensions are gated by later PRs.

| RelationType  | Description                                    |
|---------------|------------------------------------------------|
| PREDICATIVE   | Subject–predicate (mubtadaʾ–khabar / fiʿl–fāʿil) |
| RESTRICTIVE   | Qualifier–qualified (ṣifa–mawṣūf / iḍāfa)     |
| INCLUSION     | Part within whole (at relational level)        |
| REFERENCE     | Pronominal/demonstrative back-reference        |
| OPERATOR      | Governance by a particle or ʿāmil             |

## §3 Input requirements

```text
first_verdict  : MufradDalalahClosureVerdict (state = PROVEN)
second_verdict : MufradDalalahClosureVerdict (state = PROVEN)
relation_type  : RelationType (one of the minimal set)
relation_maqam : str (non-empty — contextual boundary)
relation_evidence : str (non-empty — evidence basis)
closure_scope  : str (non-empty — scope boundary)
```

Both verdicts must carry a `MufradDalalahClosureCandidate`. The two
candidates must have **distinct** `dal_identity_ref` values — a unit
cannot close a relation with itself.

## §4 RelationClosureCandidate — the carrier

```text
first_closure_ref       : trace_ref of first MufradDalalahClosureCandidate
second_closure_ref      : trace_ref of second MufradDalalahClosureCandidate
first_dal_identity_ref  : dal_identity_ref from first candidate
second_dal_identity_ref : dal_identity_ref from second candidate
relation_type           : RelationType
relation_maqam          : str (non-empty)
relation_evidence       : str (non-empty)
closure_scope           : str (non-empty)
rank                    : Rank (bounded by RELATION_CLOSURE_RANK_CEILING)
residuals               : tuple[Residual, ...]
trace_ref               : str (non-empty)
```

## §5 RelationClosureVerdict — the operation result

```text
candidate     : RelationClosureCandidate | None
verdict_state : RelationClosureState (PROVEN | REFUSED)
failure_code  : FailureCode | None
verdict_rank  : Rank
residuals     : tuple[Residual, ...]
trace_ref     : str
```

## §6 Constitutional invariants

* RelationClosureCandidate ≠ Meaning.
* RelationClosureCandidate ≠ FinalMeaning.
* RelationClosureCandidate ≠ Ifadah.
* RelationClosureCandidate ≠ Hukm.
* RelationClosureCandidate ≠ Tanzil.
* RelationClosureCandidate ≠ MafhumCandidate.
* RelationClosureCandidate ≠ MantuqClosure.
* RelationClosureCandidate ≠ MajazVerdict.
* RelationClosureCandidate ≠ HaqiqahAttemptVerdict.
* RelationClosureCandidate ≠ OntologicalClaim.
* RelationClosureCandidate ≠ FreeReasoning.
* No relation closure without two PROVEN MufradDalalahClosureVerdicts.
* No relation closure without RelationType.
* No relation closure without relation_maqam.
* No relation closure without distinct dal_identity_ref values.
* No relation closure with hidden or blocking residuals.
* No rank promotion beyond RELATION_CLOSURE_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network.

## §7 Deferred residuals

| Name                                    | Note                                    |
|-----------------------------------------|-----------------------------------------|
| RELATION_CLOSURE_NOT_MEANING            | Closure, not meaning.                   |
| IFADAH_DEFERRED_UNTIL_SPEECH_FORCE      | Ifadah needs speech force boundary.     |
| HUKM_DEFERRED_UNTIL_IFADAH             | Hukm needs ifadah first.               |
| MAFHUM_DEFERRED_UNTIL_MANTUQ           | Mafhum needs mantuq first.             |
| HAQIQAH_MAJAZ_DEFERRED_TO_POST_RELATION | Haqiqah/majaz is post-relation.        |

All deferred residuals are EXPLANATORY and visible.

## §8 Rank ceiling

```text
RELATION_CLOSURE_RANK_CEILING = MUFRAD_DALALAH_CLOSURE_RANK_CEILING
```

The relation closure rank is bounded by the meet of both input
candidate ranks and the ceiling.

## §9 Forbidden surface

PR-D4 does NOT export, instantiate, or reference:

* IfadahCandidate
* HukmCandidate
* TanzilCandidate
* MafhumCandidate
* MantuqClosure
* MajazVerdict / MajazLicense
* ManqulVerdict / ManqulLicense
* HaqiqahAttemptVerdict
* SpeakerIntentVerdict
* OntologicalClaim
* FreeReasoning
* QiyasResult
* FinalMeaning / Meaning
