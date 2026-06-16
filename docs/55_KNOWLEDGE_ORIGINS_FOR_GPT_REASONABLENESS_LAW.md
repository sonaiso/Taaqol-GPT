# 55 — Knowledge Origins Boundary Law for GPT Reasonableness

> **Status:** Constitutional law document. Ratified in GPT-K0.
> Constitutional origin: docs/54 (GPT Answer Reasonableness Objective Law),
> docs/46 (Vertical Path Closure Law), docs/47 (Post-Vertical Roadmap).
>
> This document defines the **Knowledge Origins Boundary** — the
> structural frame for the five Knowledge Origins that GPT answer
> reasonableness verification requires. It does not implement runtime
> code. It defines boundaries, interaction rules, and forbidden outputs.

---

## §1 The Transparent Reasonableness Barrier

```text
Taaqol-GPT is a Transparent Reasonableness Barrier:
a boundary architecture around black-box LLMs that transforms
their external answers into traceable, evidence-bound,
rank-limited, residual-visible reasonableness proof objects.

It proves not that the answer is absolutely true,
but that the verdict about its reasonableness is procedurally justified
under declared origins, evidence, gates, rank, residuals, and trace.
```

In Arabic:

```text
تعقّل-GPT حاجز معقولية شفاف حول مخرجات الصندوق الأسود.
لا يفتح النموذج، ولا يصدق جوابه مباشرة،
بل يحوّل الجواب الخارجي إلى كائن تحقق معقولية
ذي أثر محفوظ، ودليل مصرح، ورتبة محدودة، وبقايا ظاهرة، وبوابات انتقال.
وهو لا يثبت حقيقة الجواب المطلقة،
بل يثبت أن الحكم على معقوليته مبرر إجرائيًا
وفق الأصول والدليل والرتبة والبقايا والأثر.
```

### §1.1 What the Barrier Does

```text
The barrier does NOT:
  - Open the black box
  - Claim knowledge of model internals
  - Produce truth certificates
  - Issue execution orders
  - Generate Euclidean proofs of external reality

The barrier DOES:
  - Transform GPT output into an auditable object
  - Bind claims to knowledge origins
  - Expose residuals (unverified portions)
  - Enforce rank limits (no overclaiming)
  - Maintain trace continuity
  - Produce a bounded reasonableness verdict
```

### §1.2 Procedural Validity vs. Absolute Truth

```text
The barrier proves:
  Given this question (MaqamGPT),
  given this answer (MantuqGPT),
  given these implications (MafhumGPT),
  given these origins (OriginBinding),
  given this evidence (EvidenceSupport),
  given these gates,
  given these residuals,

  the verdict REASONABLE / UNREASONABLE / MU'ALLAQ
  is procedurally valid.

The barrier does NOT prove:
  The world is as GPT said.
```

This distinction is constitutionally binding. No future implementation
may claim or imply that a REASONABLE verdict certifies absolute truth.

---

## §2 Knowledge Origins: Definition and Role

```text
Knowledge Origins are Prior Classified Knowledge:
the minimum structured knowledge required to prevent
the reasonableness barrier from judging in a vacuum.

They are NOT:
  - Encyclopedias
  - Exhaustive lexicons
  - Complete world models
  - Unquestionable authorities

They ARE:
  - Structured reference points for claim verification
  - Typed and bounded
  - Ranked (some origins are more stable than others)
  - Residual-visible (what they do NOT cover is declared)
  - Updatable (origins can be corrected when evidence warrants)
```

### §2.1 The Five Knowledge Origins

| # | Identifier | Question It Answers | Domain |
|---|-----------|-------------------|--------|
| 1 | `EntityGenusOrigin` | What is this entity? What can it bear? What is its genus? | Ontological standing |
| 2 | `AttributeEventOrigin` | What does this predicate require? What conditions must hold? | Predicate requirements |
| 3 | `RelationOperatorOrigin` | What does this relation/operator mean? How does it bind? | Relation semantics |
| 4 | `ReferenceOrigin` | What does this pronoun/reference point to? | Referential resolution |
| 5 | `EvidenceOrigin` | What supports or refutes this claim? From what source? | Evidential support |

### §2.2 Origin Roles

```text
Origins 1–4 answer: Is this claim structurally and epistemically possible?
  - Can this entity bear this predicate?
  - Does the predicate require conditions not met?
  - Does the relation bind as claimed?
  - Does the reference resolve correctly?

Origin 5 answers: Is this claim actually supported or refuted now?
  - What evidence exists?
  - From what source?
  - What rank does this evidence carry?
  - What contradicts it?
```

Origins 1–4 establish **structural possibility**.
Origin 5 establishes **evidential status**.

A claim may be structurally possible yet unsupported (no evidence).
A claim may be structurally impossible regardless of evidence.

---

## §3 EntityGenusOrigin — Structural Definition

```text
EntityGenusOrigin declares what an entity IS:
its genus, its essential properties, and what it can bear.
```

### §3.1 Required Fields

| Field | Description |
|-------|-------------|
| `entity_id` | Canonical identifier for the entity |
| `genus` | What kind of thing this is |
| `essential_properties` | What the entity necessarily has |
| `bearing_capacity` | What predicates this entity can accept |
| `bearing_refusal` | What predicates this entity cannot accept |
| `domain` | Scientific, legal, everyday, etc. |
| `stability` | How stable this classification is (permanent, period-bound, contested) |
| `source_ref` | Where this origin is derived from |
| `rank` | Epistemic rank of this origin |
| `residuals` | What this origin does NOT cover |

### §3.2 Example

```text
EntityGenusOrigin:
  entity_id: moon
  genus: celestial body / natural satellite
  essential_properties: reflects light, orbits Earth
  bearing_capacity: illumination (reflected), orbital motion, tidal effects
  bearing_refusal: self-luminosity, atmosphere, magnetic field (significant)
  domain: physical astronomy
  stability: permanent (stable physical fact)
  source_ref: established astronomy
  rank: high (scientific consensus)
  residuals: exact albedo values, transient phenomena
```

### §3.3 What EntityGenusOrigin Is NOT

```text
EntityGenusOrigin is NOT:
  - A full scientific description (not all properties)
  - An encyclopedia article
  - Exhaustive (residuals are always declared)
  - Infallible (can be corrected with evidence and Amendment)
  - Self-sufficient for verdict (needs other origins + evidence)
```

---

## §4 AttributeEventOrigin — Structural Definition

```text
AttributeEventOrigin declares what a predicate REQUIRES:
what conditions must hold for a predicate to be truthfully
attributed to an entity.
```

### §4.1 Required Fields

| Field | Description |
|-------|-------------|
| `attribute_id` | Canonical identifier for the predicate/attribute |
| `required_conditions` | What must be true for this predicate to apply |
| `contradicting_conditions` | What makes this predicate impossible |
| `typical_bearers` | What kinds of entities typically bear this predicate |
| `impossible_bearers` | What kinds of entities cannot bear this predicate |
| `domain` | Scientific, legal, everyday, etc. |
| `stability` | How stable these requirements are |
| `source_ref` | Where this origin is derived from |
| `rank` | Epistemic rank |
| `residuals` | Uncovered cases |

### §4.2 Example

```text
AttributeEventOrigin:
  attribute_id: self_luminous
  required_conditions: internal energy source (fusion, chemical, etc.)
  contradicting_conditions: receives all light from external source
  typical_bearers: stars, bioluminescent organisms, heated objects
  impossible_bearers: natural satellites (reflected light only)
  domain: physical optics
  stability: permanent
  source_ref: established physics
  rank: high
  residuals: edge cases (e.g., tidally heated bodies)
```

---

## §5 RelationOperatorOrigin — Structural Definition

```text
RelationOperatorOrigin declares what a relation or operator MEANS:
how it binds its arguments, what it presupposes, and what it produces.
```

### §5.1 Required Fields

| Field | Description |
|-------|-------------|
| `relation_id` | Canonical identifier for the relation/operator |
| `argument_structure` | What the relation takes and produces |
| `presuppositions` | What must be true for this relation to apply |
| `binding_semantics` | How the relation connects its arguments |
| `domain` | Scientific, logical, linguistic, everyday, etc. |
| `stability` | How stable this definition is |
| `source_ref` | Where this origin is derived from |
| `rank` | Epistemic rank |
| `residuals` | Ambiguous or contested cases |

### §5.2 Example

```text
RelationOperatorOrigin:
  relation_id: causal_bi (بـ as causal/source)
  argument_structure: entity (source) — event (caused)
  presuppositions: source has causal power for the event
  binding_semantics: X is the source/cause of Y
  domain: causal relations
  stability: stable (linguistic convention)
  source_ref: Arabic grammar + causal logic
  rank: high
  residuals: figurative uses, weakened causality
```

---

## §6 ReferenceOrigin — Structural Definition

```text
ReferenceOrigin declares what a pronoun, demonstrative,
or reference expression POINTS TO in context.
```

### §6.1 Required Fields

| Field | Description |
|-------|-------------|
| `reference_id` | The referring expression |
| `referent` | What it points to in this context |
| `resolution_type` | Anaphoric, cataphoric, deictic, etc. |
| `confidence` | How certain the resolution is |
| `domain` | Context domain |
| `maqam_dependency` | Whether resolution depends on discourse context |
| `residuals` | Ambiguous or contested resolutions |

### §6.2 Example

```text
ReferenceOrigin:
  reference_id: dhātihi (ذاته) in "مضيء بذاته"
  referent: the moon (القمر)
  resolution_type: anaphoric (refers back to subject)
  confidence: high (unambiguous in this context)
  domain: textual reference
  maqam_dependency: low
  residuals: none in this case
```

### §6.3 NeedGate Integration

```text
ReferenceOrigin is only invoked when:
  - A pronoun or reference in MantuqGPT affects the verdict.
  - Ambiguous reference could change the claim's meaning.
  - Reference resolution is needed for origin binding.

ReferenceOrigin is NOT invoked:
  - For every pronoun in the text.
  - When the reference is trivially clear and does not affect the verdict.
```

This implements docs/54 §3.6 NeedGate for reference resolution.

---

## §7 EvidenceOrigin — Structural Definition

```text
EvidenceOrigin declares what SUPPORTS or REFUTES a claim
from external sources, not from the text itself.
```

### §7.1 Required Fields

| Field | Description |
|-------|-------------|
| `claim_ref` | Which claim this evidence relates to |
| `evidence_type` | Scientific consensus, authoritative source, observation, etc. |
| `evidence_direction` | Supports, refutes, partially supports, neutral |
| `evidence_content` | The substance of the evidence |
| `source` | Where this evidence comes from |
| `source_rank` | Reliability of the source |
| `recency` | How current the evidence is |
| `domain` | Scientific, legal, statistical, etc. |
| `stability` | How stable this evidence is |
| `residuals` | What the evidence does NOT cover |
| `contradiction_with` | Which other origins or evidence this conflicts with |

### §7.2 Example

```text
EvidenceOrigin:
  claim_ref: "القمر مضيء بذاته"
  evidence_type: scientific consensus
  evidence_direction: refutes
  evidence_content: the moon reflects sunlight; has no internal light source
  source: established astronomy (NASA, IAU, physics textbooks)
  source_rank: high
  recency: permanent (stable physical fact)
  domain: physical astronomy
  stability: permanent
  residuals: exact reflectance percentages
  contradiction_with: the claim itself
```

### §7.3 Evidence Freshness Rule

```text
EvidenceOrigin must declare its recency:
  - Permanent: stable physical/mathematical fact
  - Period-bound: true within a time window (law, price, status)
  - Contested: multiple credible sources disagree
  - Unknown: no evidence found
```

A REASONABLE verdict on a period-bound claim requires evidence
that is current relative to the claim's time sensitivity
(as declared in MaqamGPT.time_sensitivity).

---

## §8 OriginBinding — The Verification Link

```text
OriginBinding is the act of connecting a MantuqGPT claim
to the required Knowledge Origins.
```

### §8.1 Binding Rules

```text
1. Every MantuqGPT claim must bind to at least one origin.
2. The binding type depends on the claim structure:
   - Entity claims bind to EntityGenusOrigin.
   - Predicate claims bind to AttributeEventOrigin.
   - Relation claims bind to RelationOperatorOrigin.
   - Reference-dependent claims bind to ReferenceOrigin.
   - Factual claims bind to EvidenceOrigin.
3. A claim may require multiple origin bindings.
4. Each binding produces a verdict:
   - COMPATIBLE: claim is consistent with origin.
   - CONTRADICTED: claim conflicts with origin.
   - UNSUPPORTED: no relevant origin found.
   - PARTIALLY_COMPATIBLE: some aspects match, others unclear.
5. An UNSUPPORTED or CONTRADICTED binding generates a residual.
6. A CONTRADICTED binding from a stable, high-rank origin is a
   strong signal for UNREASONABLE verdict.
```

### §8.2 Binding Completeness

```text
OriginBinding is complete when:
  - Every MantuqGPT claim has been assessed against required origins.
  - All binding verdicts are recorded.
  - All residuals from incomplete bindings are visible.
  - The trace records which origins were consulted.

OriginBinding is NOT complete when:
  - A claim has no binding at all (BINDING_MISSING).
  - A binding was attempted but the origin is missing (ORIGIN_ABSENT).
  - A binding contradicts the origin but no residual is declared.
```

### §8.3 OriginBinding Residuals

```text
Every incomplete or contested binding produces an OriginResidual:

OriginResidual types:
  ORIGIN_ABSENT         — required origin does not exist in the system
  ORIGIN_OUTDATED       — origin exists but may be stale
  ORIGIN_CONTESTED      — multiple origins disagree
  BINDING_AMBIGUOUS     — claim could bind to multiple origins differently
  EVIDENCE_MISSING      — no evidence origin found for factual claim
  EVIDENCE_INSUFFICIENT — evidence exists but is weak or partial
  EVIDENCE_CONTRADICTED — evidence refutes the claim
  REFERENCE_AMBIGUOUS   — reference resolution is uncertain
  DOMAIN_MISMATCH       — claim domain does not match origin domain
```

These residuals are ALWAYS visible. No verdict may hide them.

---

## §9 NeedGate Integration with Origins

```text
Knowledge Origins are consumed on demand, not exhaustively.
```

### §9.1 NeedGate Rules for Origins

```text
1. EntityGenusOrigin is consulted when:
   - A claim attributes a property to an entity.
   - The property may exceed the entity's bearing capacity.

2. AttributeEventOrigin is consulted when:
   - A predicate has non-trivial requirements.
   - The claim asserts something that requires specific conditions.

3. RelationOperatorOrigin is consulted when:
   - A relation or operator in the claim is ambiguous.
   - The binding semantics affect the verdict.

4. ReferenceOrigin is consulted when:
   - A reference is ambiguous and affects the claim.
   - (NeedGate: skip if reference is trivially clear.)

5. EvidenceOrigin is consulted when:
   - The claim is factual and the maqam requires evidence.
   - The claim contradicts common knowledge.
   - The claim carries risk if wrong.
   - (NeedGate: skip for low-risk, self-evident claims.)
```

### §9.2 Unconditional vs. Conditional Origins

```text
UNCONDITIONAL (always required for any claim):
  - At least one origin binding per MantuqGPT claim.
  - Residual declaration for any missing binding.
  - Trace of which origins were consulted.

CONDITIONAL (NeedGate controlled):
  - Full morphological analysis for reference resolution.
  - Full semantic analysis for relation disambiguation.
  - Multiple evidence sources for low-risk claims.
  - Deep genus analysis for familiar entities.
```

---

## §10 Forbidden Outputs

This law forbids:

```text
1. Producing a ReasonablenessVerdict without origin binding.
2. Judging from text alone without consulting required origins.
3. Treating origins as infallible authorities (they carry rank and residuals).
4. Hiding origin residuals to force a REASONABLE verdict.
5. Treating the barrier as a truth-certification engine.
6. Using the term "Certificate" or "Euclidean proof" to describe
   the verdict or any output of the barrier.
7. Claiming that the barrier "reveals model internals."
8. Claiming that the barrier proves absolute truth of GPT's answer.
9. Running full origin analysis unconditionally (violates NeedGate).
10. Accepting a factual claim without evidence policy declaration.
11. Building encyclopedic origins before need is demonstrated.
12. Treating Knowledge Origins as a replacement for user judgment.
```

---

## §11 Origin Rank and Stability

```text
Every Knowledge Origin carries a rank:
  - HIGH: stable scientific consensus, settled law, proven mathematics
  - MEDIUM: reliable but domain-dependent (medical guidelines, current policy)
  - LOW: plausible but contested, outdated, or limited scope
  - UNKNOWN: origin exists but its reliability is undetermined

Every Knowledge Origin carries a stability:
  - PERMANENT: will not change (mathematical truth, stable physical fact)
  - PERIOD_BOUND: true within a time window (law, market price, status)
  - CONTESTED: credible disagreement exists
  - PROVISIONAL: best current knowledge, may be revised
```

### §11.1 Rank-Evidence Interaction

```text
The reasonableness verdict must respect:
  - A claim contradicting a HIGH/PERMANENT origin requires extraordinary
    evidence to avoid UNREASONABLE.
  - A claim consistent with a CONTESTED origin produces a
    PARTIALLY_REASONABLE with explicit residual.
  - A claim whose only supporting origin is PROVISIONAL carries
    a visible residual regardless of verdict.
  - No verdict may exceed the rank of its supporting evidence.
```

---

## §12 Relationship to Existing Infrastructure

The Knowledge Origins layer does not replace the existing constitutional
infrastructure. It **consumes** it:

| Existing Component | Role in Knowledge Origins |
|-------------------|--------------------------|
| `SlotGraph / Rank / Residuals / Trace` | Every origin binding carries these |
| `TransitionGate` | Origin consultation passes through gates |
| `ForbiddenLines` | Prevents straight-line from origin to certainty |
| `MantuqClosure` | MantuqGPT claims ARE the input to origin binding |
| `MafhumClosure` | MafhumGPT implications also require origin verification |
| `AnswerAudit` | Final audit wraps origin-bound verdicts |
| `NeedGate (docs/54)` | Controls when origins are consulted |

---

## §13 What This Law Opens

```text
After GPT-K0 merges, the following becomes licensed:

GPT-K1: Origin Schema Carriers
  - Python dataclasses for EntityGenusOrigin, AttributeEventOrigin,
    RelationOperatorOrigin, ReferenceOrigin, EvidenceOrigin
  - OriginBinding carrier
  - OriginResidual carrier
  - No verdicts, no gates, no full pipeline

GPT-K2: Minimal Golden Origins Dataset
  - 50 entities with EntityGenusOrigin
  - 50 attributes with AttributeEventOrigin
  - 30 relations with RelationOperatorOrigin
  - 20 reference patterns with ReferenceOrigin
  - 50 evidence entries with EvidenceOrigin
  - For testing and calibration only
```

What this law does NOT open:

```text
- docs/56 (Reasonableness Proof Object Boundary Law) — deferred
- docs/57 (Transparent Barrier Architecture Law) — deferred
- docs/70 or any number beyond docs/55 — forbidden jump
- Certificate/Truth terminology as central architecture concept
- Runtime GPT-R pipeline code
- Adapter or audit changes
```

---

## §14 The Barrier Proves Procedure, Not Reality

This section is constitutionally binding and must be preserved verbatim
in any future document that references the barrier:

```text
The Transparent Reasonableness Barrier:

1. Does NOT open the black box.
2. Does NOT claim knowledge of model internals.
3. Does NOT produce truth certificates.
4. Does NOT issue execution orders.
5. Does NOT prove that GPT's answer matches reality.

The barrier PROVES:

1. That the reasonableness verdict followed a declared procedure.
2. That the claims were extracted with trace (MantuqGPT).
3. That implications were derived with trace (MafhumGPT).
4. That claims were bound to knowledge origins (OriginBinding).
5. That evidence was consulted where required (EvidenceOrigin).
6. That residuals are visible (OriginResidual + all upstream residuals).
7. That rank does not exceed evidence (RankGate).
8. That no forbidden leaps occurred (TransitionGate + ForbiddenLines).
9. That the verdict carries full trace from MaqamGPT to final output.
```

---

## §15 Binding Declarations

```text
1. This document is binding for all GPT-K and GPT-R family branches.
2. No GPT-K1 implementation PR may merge before this document is ratified.
3. The five Knowledge Origins are structurally defined here and may not
   be restructured without an Amendment PR.
4. OriginBinding rules are constitutionally declared and binding.
5. OriginResidual types are constitutionally declared and may not be
   reduced without an Amendment PR (they may be extended).
6. The Transparent Reasonableness Barrier framing (§1, §14) is
   binding for any future architectural description of the project.
7. The prohibition on Certificate/Truth/Euclidean terminology (§10.6)
   is binding for all future documents and code.
8. docs/54 remains binding — this document extends it with the
   knowledge origins structural frame, it does not replace it.
9. NeedGate (docs/54 §3.6) is binding for origin consultation —
   this document does not override or weaken NeedGate.
```

---

## §16 Deferred Work

```text
The following are explicitly deferred and may not be implemented
before their chain position:

1. Origin Schema Carriers (GPT-K1) — requires this law to be ratified.
2. Golden Origins Dataset (GPT-K2) — requires GPT-K1 carriers.
3. Reasonableness Proof Object (docs/56) — requires GPT-K0 + GPT-K1.
4. Transparent Barrier Architecture (docs/57) — requires docs/56.
5. Proof Object Algebra (docs/58) — requires docs/56; must be partial,
   typed, non-commutative, and conservative (no ⊤, no absolute acceptance).
6. ResidualSeverityScore — deferred until calibration data exists.
   Residuals remain typed and ordered, not numeric.
7. Certificate Algebra — forbidden in its absolute form.
   Only partial composition with refusal on contradiction is permitted.
```
