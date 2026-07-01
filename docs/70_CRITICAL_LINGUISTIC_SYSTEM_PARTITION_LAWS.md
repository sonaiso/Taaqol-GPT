# 70 — Critical Linguistic System Partition Laws

> **Status:** law-only foundational boundary for critical linguistic partition
> licensing. This step defines partition and identity/tier obligations before any
> runtime implementation.
>
> Constitutional origin: `docs/11`, `docs/14`, `docs/63`, `docs/68`, and
> `docs/69`.
>
> This document introduces no runtime code, no parser, no morphology/syntax
> engine, no semantic/hukm surface, no new global `FailureCode` enum member, and
> no adapter/audit mutation.

---

## §1 Scope

This law opens only the definition boundary for:

- phonetic partition,
- structural partition,
- system partition,
- identity-property conservation across partition transitions,
- triadic identity continuity (`previous → current → next`),
- necessity-tier discipline (`daruri / haji / tahsini`),
- named failure mapping and residual visibility.

No runtime gate, carrier, parser, morphology, syntax, semantics, ifādah, hukm,
truth, certainty, or reality output is licensed here.

---

## §2 Partition boundary definitions

The critical partition surface is fixed as:

- **PhoneticPartition**: boundary separating sound-level evidence and claims.
- **StructuralPartition**: boundary separating form/arrangement evidence and claims.
- **SystemicPartition**: boundary separating rule-system evidence and claims.
- **PartitionBridge**: declared transition statement between exactly two adjacent partitions.

Rules:

1. A partition may not absorb another partition by name.
2. A bridge may not skip an intermediate partition.
3. A bridge must expose domain, scope, trace reference, and residual visibility.
4. A partition verdict is never a semantic verdict.

---

## §3 Identity conservation law

Identity obligations across partition movement are:

- **IdentityPropertyConservation**: preserved identifying property is explicitly named.
- **LicensedIdentityTransition**: any identity move must be gate-licensed and trace-visible.
- **PreviousIdentityLink**: current layer links to its declared upstream identity.
- **NextIdentityLink**: current layer links to its licensed downstream identity opening.
- **PreviousNextIdentityBridge**: the upstream/downstream link pair is coherent and non-contradictory.

A transition that breaks any identity obligation is refused.

---

## §4 Necessity-tier discipline

Tier vocabulary is fixed as:

- **DARURI** (ضروري),
- **HAJI** (حاجي),
- **TAHSINI** (تحسيني).

Tier rules:

1. Tier labels do not produce closure by themselves.
2. Tier promotion requires explicit evidence and a licensed transition.
3. Cross-tier movement without declared cause is refused.
4. Hidden residuals invalidate any claimed tier readiness.

---

## §5 Failure mapping and residual policy

This law binds the following named failure surface for future runtime contracts:

- `PARTITION_UNDECLARED`
- `PARTITION_BRIDGE_MISSING`
- `PARTITION_BRIDGE_FORBIDDEN`
- `IDENTITY_PROPERTY_BROKEN`
- `IDENTITY_TRANSITION_UNLICENSED`
- `TRIADIC_IDENTITY_GAP`
- `NECESSITY_TIER_UNDECLARED`
- `NECESSITY_TIER_PROMOTION_UNLICENSED`
- `HIDDEN_RESIDUAL`
- `FORBIDDEN_STRAIGHT_LINE`

Until a later runtime PR opens dedicated carriers/gates, these names are
law-level obligations only and remain mapped through existing refusal surfaces.

Residual policy remains strict-visible: no approved output with hidden residuals.

---

## §6 Golden fixtures and staged opening

This step requires future runtime PRs to ship fixture-backed coverage for:

- partition declarations and bridge refusals,
- identity conservation and triadic continuity refusals,
- tier declaration and promotion refusals,
- explicit failed-stage and failure-code surfacing.

This document itself does not add runtime fixtures; it licenses their required
shape for the later runtime step.

---

## §7 Forbidden surface

Forbidden in this step:

- implementing parser, morphology, syntax, or semantic runtime;
- introducing new runtime carriers or transition gates for these partitions;
- producing ifādah, mafhūm, hukm, truth, certainty, or reality outputs;
- bypassing identity continuity via naming-only or probability-only transitions;
- treating this law as closure audit or release authorization.

---

## §8 Evidence anchors

- Coverage matrix alignment: `docs/69_FOUNDATIONAL_EUCLIDEAN_COVERAGE_MATRIX.md`
- Chain registration: `docs/14_PR_CHAIN_ROADMAP.md`
- Staging mirror: `CLAUDE.md`
- Acceptance tests: `tests/test_critical_linguistic_system_partition_law.py`
