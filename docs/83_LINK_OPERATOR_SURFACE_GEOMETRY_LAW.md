# 83 — Licensed Link Operators Surface Geometry Law (LGE-LINK-L0)

> Status: constitutional law document (law-only).
> Scope: link-operator surface geometry as relation-demand openers only.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
A link operator opens a conditioned relation-demand slot.
It does not produce relation closure.

LinkTool DOES_NOT_IMPLY RelationClosure
LinkTool DOES_IMPLY RelationDemand
```

Constitutional rule:

```text
No link tool without demand.
No demand without operand side(s).
No closed relation without satisfying both required sides.
```

## §2 Branch identity and scope

```text
FAMILY               = LGE-LINK
STEP                 = LGE-LINK-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = LINK_OPERATOR_SURFACE_GEOMETRY
OBJECTIVE            = RelationDemandSurface only
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
and no parser/semantic/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  LinkOperatorCandidate,
  RelationDemandSurface,
  LinkAttachmentReadiness
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUTS = {
  LinkTool -> Ifadah,
  LinkTool -> Truth,
  Particle -> Meaning,
  Harf -> FinalRelation,
  RelationDemand -> Hukm,
  CausalMarker -> CausalTruth,
  ConditionTool -> Hukm,
  ExceptionTool -> FinalJudgment
}
```

```text
FORBIDDEN_OUTPUTS = {
  FinalRelation,
  FinalMeaning,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality
}
```

## §5 Minimal requirement kernel (MRK)

`MRK(LinkTool)` is not satisfied by symbol presence alone. Minimum declared surface:

1. `ToolIdentity`
2. `LinkFamily`
3. `DemandType`
4. `LeftAttachmentRequired`
5. `RightAttachmentRequired`
6. `AttachmentStatus` (candidate / partially_closed / blocked)
7. `VisibleResidual`
8. `TraceRef`

## §6 Link families as surface operation only

Licensed families are operational surfaces, not semantic closure:

1. Locative/circumstantial: `في`, `على`, `عند`, `بين`, `تحت`, `فوق`, `أمام`, `خلف`, `قبل`, `بعد`
2. Source/goal/boundary: `من`, `إلى`, `حتى`
3. Cause/purpose/explanatory: `لـ`, `كي`, `لكي`, `لأن`, `بسبب`, `إذ`, `حيث`
4. Condition tools: `إن`, `إذا`, `لو`, `لولا`, `لمّا`, `كلما`, `من`, `ما`, `مهما`
5. Negation/blocking: `لا`, `ما`, `لم`, `لن`, `ليس`, `غير`, `دون`
6. Exception/correction/contrast: `إلا`, `غير`, `سوى`, `لكن`, `بل`
7. Coordination/sequence/alternative: `و`, `ف`, `ثم`, `أو`, `أم`

Constitutional note:

```text
Cause markers open causal-claim demand only; they do not prove real causality.
The particle "fa" does not prove causality by itself.
```

## §7 Residual vocabulary (local)

```text
LINK_TOOL_UNKNOWN
LINK_FAMILY_AMBIGUOUS
RIGHT_COMPLEMENT_MISSING
LEFT_ANCHOR_MISSING
CONDITION_ANSWER_MISSING
EXCEPTION_BASE_MISSING
CAUSAL_PROOF_PENDING
ATTACHMENT_AMBIGUOUS
DOMAIN_TRANSFER_PENDING
MAQAM_CONTEXT_REQUIRED
```

Classification discipline:

- `RIGHT_COMPLEMENT_MISSING` is blocking.
- `CAUSAL_PROOF_PENDING` is non-blocking for linguistic surface, blocking for reality-level claims.
- `LINK_FAMILY_AMBIGUOUS` is deferred or blocking by declared domain policy.
- `MAQAM_CONTEXT_REQUIRED` is deferred.

## §8 Safe staging and anti-jump rule

This step opens only a law boundary and no runtime implementation:

```text
LGE-LINK-L0   law only
LGE-LINK-C1   LinkOperatorCandidate carriers
LGE-LINK-G1   LinkOperatorGate
LGE-LINK-T1   benchmark fixtures
LGE-LINK-R1   surface runtime
```

Ordering constraint with currently open infrastructure priorities:

```text
1. LGE-LINK-L0 law-only
2. EvidenceFitnessCarrier
3. TraceReplayVerifier
4. RankVector/DomainPolicy
5. LGE-LINK-C1 carriers
6. LGE-LINK-G1 gate
```

`LGE-LINK-L0` must not bypass evidence/trace/rank discipline.

## §9 Runtime embargo in this step

```text
RUNTIME_NOT_OPENED = {
  src_runtime_implementation,
  parser_changes,
  semantic_engine,
  ifadah_engine,
  hukm_engine,
  truth_engine,
  certainty_engine,
  reality_engine
}
```

## §10 Constitutional examples (surface-only)

Example A:

```text
Input: ذهبتُ إلى
Output: LinkOperatorCandidate LICENSED + RIGHT_COMPLEMENT_MISSING
RelationClosure: BLOCKED
```

Example B:

```text
Input: جئتُ من البيت
Output: LinkAttachmentReadiness LICENSED (surface candidate)
Forbidden: FinalMeaning / Ifadah / Hukm / Truth
```

Example C:

```text
Input: انكسر الزجاج لأن الحجر أصابه
Output: CausalClaimSurface LICENSED
ExternalCausality: PENDING
Forbidden: Truth / Certainty / Reality
```
