# Native Corpus Execution Gap Analysis

## Scope
- Repository: `sonaiso/Taaqol-GPT`
- Baseline SHA (reported): `05c6668dfb95d9238cff5df1d8bc73d0664bccb3`
- Analysis SHA (current HEAD): resolved at runtime by native runner
- Objective: reconcile constitutional truth, runtime truth, and corpus report truth without semantic overreach.

## Baseline Verification (Executed)
- `python -m pip install -e ".[dev]"`
- `pytest` -> `3013 passed`
- `ruff check .` -> `All checks passed`

## Governing Law Snapshot
- Core governing source: `docs/14_PR_CHAIN_ROADMAP.md`, `CLAUDE.md`, `README.md`, `docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md`.
- Forbidden shortcuts remain enforced:
  - `Signifier -> Meaning`
  - `Weight -> Meaning`
  - `Weight -> Agency`
  - `Candidate -> Certificate`
  - `Evidence -> Certainty`
  - `Hukm -> Tanzil without Manat`
  - `Tool/Number/LCNV -> Knowledge`

## Effective Public API (Extracted)
- Top-level public surface (`src/taaqqul_slot_geometry/__init__.py`): `134` exports.
- Weight-branch public surface (`src/taaqqul_slot_geometry/weight/__init__.py`): `433` exports.
- Runtime callable surfaces used by the native registry:
  - `prove_dal`, `prove_verbal_madlul`, `bind_dal_madlul`, `prove_contractable_unit`, `prove_relation_candidate`
  - `build_word_class_registry`, `prove_mufrad_dalalah_closure`, `prove_relation_closure`
  - `prove_ifadah_candidate`, `prove_hukm_candidate`, `prove_manat_candidate`, `prove_tanzil_candidate`
  - `assemble_chain_report`

## Runtime Registries / Carriers / Gates Found
- Forbidden-line registry: `core/forbidden_lines.py` (`CANONICAL_REGISTRY`).
- Pre-semantic registry contract: `weight/registry_contract.py`.
- Registry closure discipline: `weight/registry_closure.py`.
- Vertical runtime carriers and gates: `weight/*.py` for DalOnly -> Tanzil.
- Missing before this PR: native corpus-level stage registry derived from executable runtime.

## Gap Matrix (Law -> Runtime -> Corpus)
| Law / Stage | Runtime File | Public API | Used by Corpus Runner | Gap Type | Why Gap Existed | Minimum PR |
| --- | --- | --- | --- | --- | --- | --- |
| PR-15 DalOnly | `weight/dal_only.py` | yes (`weight.__all__`) | now yes | wiring | no native corpus orchestrator | PR-B |
| PR-16 VerbalMadlul | `weight/verbal_madlul.py` | yes | now yes | wiring | no stage registry | PR-B |
| PR-17 Binding | `weight/dal_madlul_binding.py` | yes | now yes | context | runner lacked registry proofs per-token | PR-D |
| PR-18 ContractableUnit | `weight/contractable_unit_geometry.py` | yes | now yes | context | token-only execution lacked span context | PR-F |
| PR-19 Relation | `weight/relation_candidate.py` | yes | now guarded | applicability | non-content tokens were pushed into content path | PR-C |
| PR-F2..F7 FormalShape | `weight/formal_shape*.py` | yes | now yes | wiring | no route for built/operator/reference tokens | PR-E |
| PR-D3 MufradDalalah | `weight/mufrad_dalalah_closure.py` | yes | guarded | context | missing multi-token closure context | PR-F |
| PR-20 Ifadah | `weight/ifadah_candidate.py` | yes | guarded | context | no explicit span readiness boundary | PR-F |
| PR-21 Hukm | `weight/hukm_candidate.py` | yes | guarded | report | corpus reports lacked stage-local refusal semantics | PR-D |
| PR-21M Manat | `weight/manat_candidate.py` | yes | guarded | report | no explicit deferred/not-opened distinction | PR-C |
| PR-22 Tanzil | `weight/tanzil_candidate.py` | yes | guarded | no-jump | hukm->tanzil chain stop was not made explicit in corpus report | PR-D |
| AnswerAudit bridge | `audit/answer_audit.py` | top-level API | not enabled in token runner | applicability | model-client dependent; not valid for isolated token run | PR-I |

## Token-Level Hard Gap Observation
- Function and built/reference units (`يا`, `أيها`, `الذين`, `إذا`, `إلى`, `أن`, `كما`, `ولا`) were previously over-blocked by root/weight-dominant routing.
- Native path-aware routing now maps these units to primary path families with visible evidence and without forced weight closure.

## Gap Classification Summary
- `wiring`: executable stage existed but was never called by corpus execution.
- `carrier`: stage expected carriers not represented in corpus records.
- `registry`: no single runtime-native stage registry with predecessor/successor discipline.
- `context`: token-level runs attempted higher layers without span/context readiness.
- `applicability`: path mismatch treated as blocked instead of not-applicable/deferred.
- `report`: states were not separated with traceable, auditable semantics.

## Closure Discipline for This Step
- No rank promotion introduced.
- No residual hiding introduced.
- No meaning/hukm/reality claim is synthesized from token/formal morphology.
- No forbidden straight-line transition is licensed.
