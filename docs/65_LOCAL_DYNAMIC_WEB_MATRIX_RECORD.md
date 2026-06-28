# 65 — Local Dynamic Web Matrix Record

> **Status:** Constitutional law document. Registered as `WEB-M0` in
> `docs/14_PR_CHAIN_ROADMAP.md`. Law-only: no runtime code, no API, no server,
> no static-site network call, no web dependency, no model call, no persistence,
> no telemetry, no public deployment, no adapter/audit mutation, and no new
> global `FailureCode` members.
>
> Constitutional origin: `docs/13`, `docs/14`, `docs/53`, `docs/56`, and
> `docs/64`.

---

## §1 Purpose

WEB-M0 records the matrix-side decision required before the dynamic web plan may
advance to a future boundary-law PR.

It implements only the first safe step of the plan: a law-only matrix record
that lifts permission to draft a future `WEB-L0` local dynamic web boundary law.

WEB-M0 does not create an API.
WEB-M0 does not create a server.
WEB-M0 does not alter `/website`.
WEB-M0 does not add `fetch`, `XMLHttpRequest`, `WebSocket`, or any
network-capable JavaScript to the static website.
WEB-M0 does not add runtime dependencies.
WEB-M0 does not call a model.
WEB-M0 does not license public deployment, persistence, telemetry,
authentication, or downloadable artifacts.

---

## §2 Matrix row schema

WEB-M0 uses the fixed `docs/64` row schema:

```text
condition_id      | ban_class
condition_text    | evidence_kind
evidence_locator  | owner
test_kind         | failure_code
rank_ceiling      | residual_policy
decision
```

A `LIFT_PERMITTED` row in WEB-M0 means permission to open the next law-only PR
that addresses the row's ban class. It never means permission to ship runtime
web code or public deployment.

---

## §3 Worked rows for WEB-M0

```text
W1
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The future local dynamic web boundary has a ratified
                     matrix record before any boundary law or implementation.
  evidence_kind    : RATIFIED_LAW
  evidence_locator : docs/65_LOCAL_DYNAMIC_WEB_MATRIX_RECORD.md
  owner            : chain-author
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

W2
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The lift is scoped to drafting WEB-L0 only and does not
                     ship runtime API, server, adapter, carrier, or website
                     behavior.
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/65_LOCAL_DYNAMIC_WEB_MATRIX_RECORD.md
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : OUTPUT_EXCEEDS_LAYER
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

W3
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The static `/website` surface remains local-only and
                     network-free until a later boundary explicitly changes it.
  evidence_kind    : CONSTITUTIONAL_TEST
  evidence_locator : tests/test_static_website.py
  owner            : maintainer
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : TRACE_MISSING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

W4
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : Runtime web dependencies remain unlicensed unless a later
                     dependency-expansion decision is ratified.
  evidence_kind    : DOC_SECTION
  evidence_locator : pyproject.toml
  owner            : maintainer
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

W5
  ban_class        : PUBLIC_READINESS
  condition_text   : Hosted/public deployment remains outside WEB-M0 and waits
                     for the closure audit and release steps.
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/14_PR_CHAIN_ROADMAP.md
  owner            : release-manager
  test_kind        : OPERATIONAL_AUDIT
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : DEFERRED_VISIBLE
  decision         : LIFT_DEFERRED_TO_LAW(CLOSE-5)

W6
  ban_class        : PUBLIC_READINESS
  condition_text   : Public release remains deferred until the release step;
                     WEB-M0 cannot be cited as a readiness certificate.
  evidence_kind    : PUBLISHED_RELEASE
  evidence_locator : CHANGELOG.md
  owner            : release-manager
  test_kind        : RELEASE_CHECK
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : DEFERRED_VISIBLE
  decision         : LIFT_DEFERRED_TO_LAW(CLOSE-6)
```

Rows W1-W4 lift only the constitutional permission to draft WEB-L0 as a later
law-only boundary. Rows W5-W6 keep public readiness deferred.

---

## §4 Admission conditions for WEB-L0

A future local dynamic web boundary law may be proposed only if all conditions
below remain true:

1. The boundary is local-only unless a later `PUBLIC_READINESS` matrix record
   explicitly licenses hosted/public deployment.
2. `/website` remains a static fallback unless a later boundary explicitly
   changes it and updates its tests.
3. No runtime web dependency is added unless a separate dependency-expansion
   decision passes first.
4. `core/` and `contracts/` remain pure and do not perform I/O.
5. The backend, if later implemented, is an outer shell over existing GPT
   reasonableness and AnswerAudit surfaces.
6. Inputs are limited to user question, GPT answer, visible evidence/origin
   material, and bounded risk/time/evidence hints.
7. Outputs expose input-contract status, gate report when available,
   reasonableness verdict, residuals, rank, trace refs, and named failure codes
   on refusal.
8. Missing information returns a visible refusal or deferral, never a simulated
   success.
9. The interface never claims truth certification, final authority, model
   internals, or hidden certainty.
10. Model calls require a later adapter/public-readiness decision and cannot be
    smuggled through the local web boundary.

---

## §5 Future API boundary shape

WEB-M0 licenses only the drafting of WEB-L0. If WEB-L0 is later proposed, it may
describe this local-only boundary shape:

- `GET /` serves an interface.
- `POST /api/reasonableness` receives a user question, GPT answer, visible
  evidence/origin text, and bounded hints.
- The response is JSON containing visible status, verdict, residuals, rank,
  trace refs, and refusal failure codes.

This shape remains descriptive until WEB-L0 is ratified. WEB-M0 does not create
or license runtime endpoint code.

---

## §6 Local residual vocabulary

WEB-M0 reserves these local residual names for later boundary-law discussion:

```text
LOCAL_DYNAMIC_BOUNDARY_ONLY
STATIC_FALLBACK_REQUIRED
PUBLIC_DEPLOYMENT_UNLICENSED
RUNTIME_DEPENDENCY_UNLICENSED
MODEL_CALL_UNLICENSED
PERSISTENCE_UNLICENSED
TELEMETRY_UNLICENSED
HIDDEN_RESIDUAL_RISK
CERTIFICATION_WORDING_RISK
MODEL_INTERNALS_RISK
MALFORMED_WEB_INPUT
TRACE_REQUIRED
```

These names are local to this matrix record unless a future runtime PR
explicitly binds them into executable code.

---

## §7 Forbidden outputs

WEB-M0 forbids:

- treating `GPTAnswerReasonablenessVerdict` as truth certification;
- treating `AnswerAudit.audit_with_reasonableness()` as a public deployment
  license;
- changing `ModelClient`, `AdapterGuard`, `core/`, or `contracts/`;
- adding web frameworks or transports by implication;
- adding model calls to the website;
- hiding residuals from a browser response;
- representing a local verdict as certainty, authority, or final truth.

---

## §8 Test obligations

The WEB-M0 acceptance suite must prove:

1. `docs/65` exists and declares itself law-only.
2. WEB-M0 uses the `docs/64` fixed row schema and closed decision vocabulary.
3. The lift is limited to future boundary-law permission, not runtime web I/O.
4. `/website` remains static-local and network-free.
5. Runtime dependencies, public deployment, persistence, telemetry, and model
   calls remain unlicensed.
6. Certificate wording and model-internals claims remain forbidden.
7. Future API responses must expose visible residuals and trace refs.

---

## §9 Trace

Trace path:

`docs/13` → `docs/14` → `docs/53` → `docs/56` → `docs/64` → `docs/65`
→ future `WEB-L0`.

WEB-M0 is a matrix record. It is not the dynamic web implementation.
