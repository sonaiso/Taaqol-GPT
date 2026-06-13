# 22 — Pre-Weight Path Gate Law

> **Status:** Constitutional law. Ratified in PR-11; chain position
> ratified by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law the pre-weight path gate implements.
>
> PR-10 gave the carrier.
> PR-10B forbade the carrier from claiming a verdict.
> PR-11 establishes the path court.

## 1. The governing principle

```text
A carrier declaration is not a gate verdict.
A path gate verdict is not a meaning.
A path gate verdict is not a weight.
```

The path gate is the constitutional fork of the pre-weight chain
(docs/20 §7). It receives a `WordCarrierCandidate` and emits a
candidate path — one of the seven `PathKind` members — only after
the evidence, domain, rank, and residual conditions are met, and
only through a `TransitionGate` with named refusals.

```text
SurfaceCarrier + PathGateEvidence + Domain + NoPreventer
  + ResidualCheck + RankBound
  → PathGateVerdict
```

If the evidence is insufficient, the verdict is blocked or deferred
with a named `FailureCode`, never a licensed path.

## 2. The discriminating identities

In the same sense as docs/21, each element has a fixed identity:

```text
PathKind            — a declared candidate kind (carrier surface).
                      NOT a PathGateProof.

PathGateProof       — the evidence structure a gate evaluates.
                      NOT a carrier field. NOT a PathKind value.

PathGateVerdict     — the gate's constitutional decision.
                      NOT a carrier declaration. NOT a meaning.
                      NOT a weight.

PathCandidate       — the depicted carrier of a path (PR-10).
                      NOT a gate verdict. NOT a gate proof.
```

## 3. The required constitutional law

The following identities are binding on PR-11 and every later PR:

```text
PathKind ≠ PathGateProof.
Carrier declaration ≠ Gate verdict.
OriginalExtraMap ≠ ExtraLetterLicense.
Mizan ≠ weighing authority.
TraceRef ≠ audit ledger commit.
CandidateRank ≠ GateRank.
```

These identities inherit from docs/21 and remain binding.

## 4. The path gate input

The path gate accepts:

```text
carrier   : WordCarrierCandidate — the bounded surface with its
            syllable sequence and word boundary. No raw word, no
            unbounded string, no bare syllable.

evidence  : PathGateProof — the structural evidence for the
            candidate path. The proof structure names the kind
            of path claimed and the evidence surface that supports
            it. A proof without evidence is refused.

domain    : the declared domain of the carrier (must match).
```

## 5. The path gate output

The path gate emits a `PathGateVerdict`:

```text
APPROVED  — the evidence supports the claimed path kind.
            The verdict carries the approved PathKind, the
            evidence rank bounded by the gate's meet, and no
            failure code.

DEFERRED  — the evidence is insufficient but may arrive later.
            The verdict carries a named FailureCode.

BLOCKED   — a named preventer blocks the path.
            The verdict carries a named FailureCode.

REJECTED  — the evidence contradicts the claimed path, or a
            constitutional violation is present.
            The verdict carries a named FailureCode.
```

Every path verdict carries a `residuals` tuple: discovered residuals
are visible, never hidden. A stronger competing path that blocks a
weaker one is a named preventer — never a silent override.

## 6. The seven candidate paths

```text
ROOT        — the derivational root path (mushtaqq).
JAMID       — the non-derived (rigid) path.
MABNI       — the invariably-built path.
OPERATOR    — the functional operator path.
PROPER_NAME — the proper-name path.
BORROWED    — the borrowed-word path.
RESIDUAL    — the unresolved/residual path.
```

Each path sits behind a gate. No path is a verdict, no path is a
meaning. The `RESIDUAL` path is not a clearance — it is a named,
visible remainder.

## 7. Forbidden forms

```text
forbidden: PathKind treated as PathGateProof.
forbidden: PathGateVerdict without named FailureCode on refusal.
forbidden: a silent override of a competing path.
forbidden: a path that bypasses the gate.
forbidden: weighing from a PathGateVerdict (PR-13 surface).
forbidden: meaning, agency, hukm from a path verdict.
forbidden: root/stem extraction (PR-12 surface).
forbidden: original/extra split (PR-12 surface).
forbidden: Ω judgment (PR-12 surface).
forbidden: lexicon, samāʿ, qiyās (PR-14 surface).
forbidden: new FailureCode members.
forbidden: new runtime dependencies.
```

## 8. What enters only through later PRs

```text
PR-12:  μ chain operations, root/stem extraction,
        original/extra split, Ω judgment
PR-13:  weigh(), WeightFitCandidate
PR-14:  lexicon, samāʿ, qiyās licensing
```

## 9. Constitutional summary

```text
PR-10 أعطى الحامل.
PR-10B منع الحامل من ادعاء الحكم.
PR-11 أنشأ محكمة المسار.

المسار المصرّح ليس حكمًا.
حكم البوابة ليس معنى.
حكم البوابة ليس وزنًا.
الحامل لا يدّعي الحكم.
والحكم لا يدّعي المعنى.
```
