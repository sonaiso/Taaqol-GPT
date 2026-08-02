# Full-Target Native Rerun Report (Ayat al-Dayn)

## Run Metadata
- HEAD SHA: `24660601f4885226e390331d5c668a725eeee6e4`
- Registry version: `native-registry-v1`
- Registry hash: `f741286db9af74f53d2b7b919080170d61968e853e9ec469efcf427a6a230cb6`
- Corpus fixture: tokenized segment set from the requested Ayat al-Dayn spans
- Total tokens: `23`
- Total stage records: `368`

## Comparison vs Previous Reported Baseline
- Previous reported `NOT_APPLICABLE`: `0`
- Current native run `NOT_APPLICABLE`: `50` (explicitly non-zero)
- Previous reported forced blocking of built/operator/reference units: present
- Current native run routes built/operator/reference/function words to native paths with visible evidence and no forced weight-only closure

## State Distribution
- `EXECUTED`: `46`
- `BLOCKED`: `0`
- `DEFERRED`: `23`
- `NOT_OPENED`: `249`
- `NOT_APPLICABLE`: `50`

## Distribution by Path
- `ParticleOperatorPath`: `64`
- `BuiltNounPath`: `16`
- `RelativeReferencePath`: `16`
- `ConditionalOperatorPath`: `16`
- `PronounPath`: `16`
- `NegationOperatorPath`: `16`
- `JamidPath`: `16`
- `RootStemPath`: `208`

## Function/Built/Reference Units Routed Natively
- `يا`, `أيها`, `الذين`, `إذا`, `إلى`, `ولا`, `أن`, `كما`, `بينكم` all receive native path routing and stage records.
- No unit is dropped for being outside root/weight-only path.

## Failure Code and Residual Families
- FailureCode distribution: none emitted in this token-run mode (`{}`)
- Residual families (top): `RUNTIME_CONTEXT_PENDING` (`322` records)

## Deepest Reached Stage by Token
- In this token-only native run, deepest executed stage per token is `PRE_WEIGHT_CAPACITY_AUDIT`.
- Vertical-chain stop reason: required upstream context carriers for higher layers are intentionally missing, so later layers remain `DEFERRED`/`NOT_OPENED`/`NOT_APPLICABLE` instead of forced closure.

## Logic Used vs Not Yet Used
- Used now:
  - Native stage registry
  - Path-aware applicability predicates
  - State semantics split (`DEFERRED`, `NOT_OPENED`, `NOT_APPLICABLE`, `EXECUTED`)
  - Immutable traceable stage execution records
- Not yet used in this token-only run:
  - Full span/context licensed handoff into relation closure and vertical closure
  - Model-client dependent `ANSWER_AUDIT` execution

## Constitutional Claim Boundary
- This run does **not** claim full closure of the vertical chain.
- This run demonstrates runtime/report alignment and state visibility without semantic/hukm/reality overclaim.
