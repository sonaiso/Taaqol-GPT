# 54 — GPT Answer Reasonableness Objective Law

> **Status:** Constitutional law document. Ratified in GPT-R0.
> Constitutional origin: docs/46 (Vertical Path Closure Law),
> docs/47 (Post-Vertical Roadmap), docs/53 (Project Methodology).
>
> This document declares the project's **operational objective**:
> GPT answer reasonableness verification. It does not implement
> runtime code. It names the mandatory components and establishes
> the NeedGate principle.

---

## §1 Operational Objective Declaration

```text
The operational objective of Taaqol-GPT is:

    Verification of GPT answer reasonableness
    (تدقيق معقولية جواب GPT)

This is NOT:
    - Arabic linguistic analysis for its own sake
    - Comprehensive morphological/syntactic parsing of every answer
    - An Arabic NLP toolkit
    - A GPT clone or competitor
    - An attempt to expose model internals
```

The project wraps any GPT-generated answer with an auditable
reasonableness geometry:

```text
UserQuestion
→ MaqamGPT (what the user asked, in what domain, with what constraints)
→ MantuqGPT (what GPT explicitly claimed)
→ MafhumGPT (what GPT implicitly committed to)
→ OriginBinding (which knowledge origins the claims require)
→ EvidenceSupport (what evidence supports or refutes the claims)
→ ReasonablenessVerdict (is the answer reasonable, given all of the above?)
```

---

## §2 What We Analyze and Why

```text
We do not analyze GPT's answer because it is an Arabic text.
We analyze it because it is a claim in a context (دعوى في مقام).

We do not request manṭūq for its own sake.
We request it because it is the origin of mafhūm.

We do not request mafhūm for its own sake.
We request it because it reveals implications and risks.

We do not request maqām for its own sake.
We request it because it is the origin of fitness (ملاءمة).

We do not request morphology, syntax, or semantics for their own sake.
We request them when needed because they are conditions of possibility
for judging reasonableness (شروط إمكان الحكم على المعقولية).

We do not judge reasonableness from text alone.
We bind text to knowledge origins:
entity, attribute/event, relation/operator, reference, and evidence.
```

---

## §3 Mandatory Definitions

### §3.1 MaqamGPT

```text
MaqamGPT is the preserved context of the user's question.
```

It must contain:

| Field | Description |
|-------|-------------|
| `question_type` | Factual, procedural, evaluative, creative, etc. |
| `domain` | Scientific, legal, religious, technical, everyday, etc. |
| `constraints` | What the user explicitly or implicitly requires |
| `evidence_need` | What kind of evidence the answer requires |
| `risk_level` | How dangerous a wrong answer would be |
| `time_sensitivity` | Whether the answer depends on current state |
| `forbidden_answer_forms` | What the answer must not do |

MaqamGPT is not free text. It is a structured verdict declaring
what the user needs and what risks exist.

### §3.2 MantuqGPT

```text
MantuqGPT is the set of explicit claims in GPT's answer.
```

Each claim must record:

| Field | Description |
|-------|-------------|
| `subject` | What entity the claim is about |
| `predicate` | What is being said about it |
| `qualifiers` | Conditions, restrictions, or modifiers |
| `modality` | Certainty level (assertion, possibility, etc.) |
| `domain` | Which knowledge domain the claim belongs to |
| `span_trace` | Where in the answer text this claim appears |

MantuqGPT extracts **only** what GPT explicitly stated.
It does not invent, infer, or extend.

### §3.3 MafhumGPT

```text
MafhumGPT is the set of implicit commitments and risks
derivable from MantuqGPT, not invented freely.
```

Each implication must record:

| Field | Description |
|-------|-------------|
| `source_claim` | Which MantuqGPT claim this derives from |
| `implication` | What is implicitly committed |
| `risk_level` | How dangerous this implication is |
| `type` | Necessary consequence, probable inference, or possible reading |
| `overclaim_risk` | Whether this might be stronger than intended |

MafhumGPT requires MantuqGPT. No mafhūm without manṭūq.
MafhumGPT does not produce truth — it produces risks and commitments.

### §3.4 Knowledge Origins

```text
Knowledge Origins are the Prior Classified Knowledge layer
used to verify GPT's claims. They are NOT encyclopedias.
They are the minimum structured knowledge needed to prevent
the system from judging in a vacuum.
```

The five Knowledge Origins:

| # | Name | Question It Answers |
|---|------|-------------------|
| 1 | `EntityGenusOrigin` | What is this entity? What can it bear? |
| 2 | `AttributeEventOrigin` | What does this predicate require? |
| 3 | `RelationOperatorOrigin` | What does this relation/operator do? |
| 4 | `ReferenceOrigin` | What does this pronoun/reference point to? |
| 5 | `EvidenceOrigin` | What supports or refutes this claim? |

Origins 1–4 answer: **Is this claim structurally and epistemically possible?**
Origin 5 answers: **Is this claim actually supported or refuted now?**

### §3.5 ReasonablenessVerdict

```text
GPTAnswerReasonablenessVerdict is the final output.
It is NEVER a certificate, truth declaration, or execution order.
It is a bounded verdict with trace, rank, and visible residuals.
```

The verdict is PROVEN (reasonable) if and only if:

1. MaqamGPT is preserved (answer fits what was asked).
2. MantuqGPT claims are extracted with trace.
3. MafhumGPT implications derive from MantuqGPT, not invented freely.
4. Each claim binds to the required knowledge origins.
5. Each factual claim has suitable evidence.
6. No contradiction with a stable origin or supplied evidence.
7. No forbidden leap.
8. No hidden residual.
9. Rank does not exceed evidence.

The verdict states (non-exhaustive):

```text
REASONABLE
PARTIALLY_REASONABLE
UNREASONABLE
OFF_MAQAM
UNSUPPORTED
CONTRADICTORY
OVERCLAIMED
ORIGIN_CONTRADICTION
FORBIDDEN_LEAP
RESIDUAL_BLOCKED
NEEDS_CLARIFICATION
```

### §3.6 NeedGate

```text
NeedGate is the principle that Arabic linguistic analysis
is conditional on verification need.
```

The rules:

```text
No morphological analysis unless needed to verify a claim.
No syntactic analysis unless needed to verify a relation.
No haqīqah/majāz unless there is a transfer suspicion.
No reference resolution unless a pronoun/reference affects the verdict.
No full semantic analysis unless the claim requires it.
```

NeedGate prevents the project from degenerating into Arabic analysis
for its own sake. The constitutional chain (PR-0 through PV-A4.1)
remains valid infrastructure — but it is **consumed on demand**,
not **executed unconditionally** for every answer.

---

## §4 Relationship to Existing Infrastructure

The existing constitutional infrastructure is not discarded.
It is reframed as the **engine** that GPT reasonableness
verification **consumes**:

| Existing Component | Role in GPT Reasonableness |
|-------------------|---------------------------|
| `IfadahCandidate` | MantuqGPT claims are ifādah candidates in maqām |
| `MantuqClosure` | Preserves explicit claims before mafhūm extraction |
| `MafhumClosure` | Extracts implications as licensed branches of manṭūq |
| `SpeechForce/FormalStyle Bridge` | Prevents form-only judgments |
| `AnswerAudit` | Final audit wrapper for reasonableness verdicts |
| `SlotGraph / Gamma / Rank / Residuals / Trace` | Core geometry that every verdict carries |
| `TransitionGate` | Prevents forbidden leaps in the verification pipeline |
| `ForbiddenLines` | Registry of prohibited straight-line transitions |

The new GPT-R layer does not replace these. It **targets** them
toward GPT answer verification.

---

## §5 Forbidden Outputs

This law forbids:

```text
1. Treating GPT reasonableness as Arabic analysis for its own sake.
2. Running full morphological/syntactic/semantic chain unconditionally.
3. Producing a ReasonablenessVerdict without MaqamGPT.
4. Producing MafhumGPT without MantuqGPT.
5. Producing a verdict without trace, rank, and residuals.
6. Treating the verdict as a certificate, truth, or authority.
7. Judging from text alone without knowledge origin binding.
8. Accepting a factual claim without evidence policy.
9. Accepting a claim that contradicts a stable knowledge origin.
10. Hiding residuals to force a REASONABLE verdict.
```

---

## §6 GPT-R Branch Family Roadmap

The following steps implement GPT answer reasonableness verification.
Each follows the law-first discipline (docs/47 §4 admission rule):

```text
GPT-R0  This document (objective correction law)
GPT-K0  Knowledge Origins Boundary Law (docs/55, law only)
GPT-K1  Origin Schema Carriers (carriers only, no verdicts)
GPT-K2  Minimal Golden Origins Dataset (50 entities, 50 attributes, etc.)
GPT-R1  GPT Answer Input Contract (GPTAnswerInput carrier)
GPT-R2  MaqamGPT Boundary (MaqamGPTVerdict)
GPT-R3  MantuqGPT Claim Extraction (MantuqGPTVerdict)
GPT-R4  MafhumGPT Implication Extraction (MafhumGPTVerdict)
GPT-R5  Origin Binding Gate (OriginBindingVerdict)
GPT-R6  Reasonableness Gates (6 specific gates)
GPT-R7  GPTAnswerReasonablenessVerdict (final verdict)
GPT-R8  Audit Integration (AnswerAudit bridge)
```

Each step requires its own Amendment in docs/14, its own chain position,
constitutional tests, and adherence to the admission rule.

---

## §7 KPI Summary for GPT Reasonableness MVP

The MVP is complete when these pass:

| KPI | Target |
|-----|--------|
| MaqamGPT extraction | 100% of golden set questions classified |
| MantuqGPT extraction | ≥ 95% of explicit claims extracted with span |
| MafhumGPT extraction | ≥ 90% of golden implications extracted |
| Origin binding | ≥ 95% of claims bound to correct origin |
| Origin contradiction detection | 0 false accepts |
| Evidence support | 0 acceptance of high-risk factual claims without evidence |
| NeedGate compliance | 0 unconditional Arabic analysis |
| Hidden residuals | 0 verdicts with hidden residuals |
| Forbidden leaps | 0 accepted leaps |
| Trace continuity | 100% of verdicts carry full trace |

---

## §8 Binding Declarations

```text
1. This document is binding for all GPT-R family branches.
2. No GPT-K or GPT-R implementation PR may merge before this
   document is ratified.
3. NeedGate is binding for the entire project after GPT-R0 merges.
4. The five Knowledge Origins are constitutionally named and may not
   be renamed without an Amendment PR.
5. The ReasonablenessVerdict states are constitutionally declared
   and may not be reduced without an Amendment PR.
6. docs/53 methodology remains binding — this document extends it
   with the operational objective, it does not replace it.
```

---

## §9 Example: "القمر مضيء بذاته"

This section demonstrates the full pipeline on a single example.

### §9.1 MaqamGPT

```text
question_type: scientific / phenomenon explanation
domain: physical astronomy
constraints: user expects physical explanation
evidence_need: factual/scientific
risk_level: medium (factual misinformation)
time_sensitivity: none (stable physical fact)
```

### §9.2 MantuqGPT

```text
Claim-1:
  subject: القمر (the moon)
  predicate: مضيء (luminous)
  qualifier: بذاته (by itself / self-sourced)
  modality: assertion (جزم)
  domain: physical
  span_trace: "القمر مضيء بذاته"
```

### §9.3 MafhumGPT

```text
Implication-1: The moon is a self-luminous body.
Implication-2: The moon does not need the sun for its light.
Risk: misleading about a basic physical fact.
```

### §9.4 Origin Binding

```text
EntityGenusOrigin:
  moon = celestial body, reflects light, NOT self-luminous

AttributeEventOrigin:
  "luminous by itself" requires a self-source of light

RelationOperatorOrigin:
  "bi-" (بـ) in "bi-dhātihi" = self-source/causal relation

ReferenceOrigin:
  "dhātihi" = refers back to the moon itself
```

### §9.5 Verification

```text
ORIGIN_CONTRADICTION:
  claim.self_luminous = true
  origin.moon.self_luminous = false

FORBIDDEN_LEAP:
  appears bright → self-luminous

EVIDENCE:
  no supporting evidence; stable origin says opposite

RESIDUAL:
  possible figurative reading not declared by GPT
```

### §9.6 Verdict

```text
GPTAnswerReasonablenessVerdict:
  state: UNREASONABLE
  failure_codes:
    - ORIGIN_CONTRADICTION
    - UNSUPPORTED_FACTUAL_CLAIM
    - FORBIDDEN_LEAP_APPEARANCE_TO_SELF_SOURCE
  visible_residuals:
    - possible figurative reading not declared
  trace:
    MaqamGPT → MantuqGPT → MafhumGPT → OriginBinding → Verdict
  rank: 0 (no evidence supports the claim)
```
