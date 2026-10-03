"""Revalidate at every public consumption boundary; no caller PASS is consumed.

Gamma closes a TRACE-rank review record only. It neither licenses Arabic rules
nor promotes imported/declared priors. Trusted Python code and configured source
policies remain the trust boundary; this is not a sandbox against code execution.
"""

from __future__ import annotations

import json

from verify_fragment import verify_fragment
from verify_readout import _digest, verify_readout


def admit(question, artifact, *, policy=None, source=None, resources=None, ontology=None):
    # A deep immutable-by-convention snapshot prevents post-check caller mutation.
    candidate = json.loads(json.dumps(artifact, ensure_ascii=False))
    if candidate.get("schema") == "identity-answer-v1" and ontology is not None:
        from verify_identity import verify_identity

        ontology = json.loads(json.dumps(ontology, ensure_ascii=False))
        review = verify_identity(question, candidate, ontology)
        unresolved = candidate.get("residuals", [])
        alternatives = candidate.get("alternatives", [])
        authority = candidate.get("authority")
    elif candidate.get("schema") == "knowledge-answer-v1" and ontology is not None:
        from verify_knowledge import verify_knowledge

        ontology = json.loads(json.dumps(ontology, ensure_ascii=False))
        review = verify_knowledge(question, candidate, ontology)
        unresolved = candidate.get("residuals", [])
        alternatives = candidate.get("alternatives", [])
        authority = candidate.get("authority")
    elif candidate.get("schema") == "ontology-answer-v1" and ontology is not None:
        from verify_ontology import verify_ontology

        ontology = json.loads(json.dumps(ontology, ensure_ascii=False))
        review = verify_ontology(question, candidate, ontology)
        unresolved = candidate.get("residuals", [])
        alternatives = candidate.get("alternatives", [])
        authority = candidate.get("authority")
    elif candidate.get("schema") == "expanded-fragment-v1" and resources is not None:
        from verify_expansion import verify_expansion

        review = verify_expansion(question, candidate, resources)
        unresolved = candidate.get("residuals", [])
        alternatives = candidate.get("alternatives", [])
        authority = "derived_under_declared_family_with_attributed_lexical_priors"
    elif candidate.get("schema") == "derived-fragment-v1" and policy is not None:
        policy = json.loads(json.dumps(policy, ensure_ascii=False))
        review = verify_fragment(question, candidate, policy)
        unresolved = candidate.get("residuals", [])
        alternatives = candidate.get("alternatives", [])
        authority = "derived_under_declared_prior"
    elif candidate.get("schema") == "bounded-question-v1" and source is not None:
        review = verify_readout(question, candidate, source.data, source.expected_sha256)
        unresolved = candidate.get("residuals", [])
        alternatives = []
        authority = "imported_MASAQ_analysis"
    else:
        return {"decision": "REJECT", "answer": None, "errors": ["UNSUPPORTED_CONTRACT"]}
    binding = _digest(
        {
            "question": question,
            "artifact": candidate,
            "policy": policy,
            "source": source.expected_sha256 if source else None,
            "resources": resources.manifest() if resources else None,
            "ontology": ontology,
        }
    )
    if not review["verified"]:
        return {
            "decision": "REJECT",
            "answer": None,
            "errors": review["errors"],
            "binding": binding,
            "review": review,
        }
    from taaqqul_slot_geometry import (
        Center,
        EntryBoundary,
        FailureCode,
        GenerationSource,
        Layer,
        OpeningPolicy,
        OutputBoundary,
        Rank,
        Residual,
        ResidualKind,
        Slot,
        SlotBoundary,
        SlotGraph,
        SlotState,
        TraceRef,
        gamma,
    )

    boundary = SlotBoundary(
        domain="bounded-artifact-review",
        scope="content review under declared priors",
        refusal_codes=(FailureCode.REQUIRED_SLOT_EMPTY,),
    )
    graph = SlotGraph(
        center=Center(
            identity_claim=binding,
            domain=boundary.domain,
            scope=boundary.scope,
            trace_ref=TraceRef(binding, "DECLARED_ENTRY"),
        ),
        slots=(
            Slot(
                name="content-review",
                value_state=SlotState.FILLED,
                boundary=boundary,
                opening=OpeningPolicy(frozenset({"checked"})),
                required=True,
                value="checked",
            ),
        ),
        boundary=boundary,
        residuals=tuple(
            Residual(str(i), ResidualKind.EXPLANATORY, True, str(value))
            for i, value in enumerate(unresolved)
        ),
        rank=Rank.TRACE,
        output_boundary=OutputBoundary(Layer.TEXT_ENTRY, Layer.TEXT_ENTRY),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=EntryBoundary(
            declared_entry_kind="BOUND_REVIEW_RECORD",
            representation_status="REPRESENTATIONAL_OF_PRIOR",
            ontological_status="NOT_AN_ORIGIN",
            sound_status="NOT_A_SOUND",
            meaning_status="NOT_A_MEANING",
            prior_trace_status=binding,
            produces_only="TEXT_TRACE_CANDIDATE",
        ),
    )
    closure = gamma(graph)
    if closure.failure_code is not None:
        return {
            "decision": "REJECT",
            "answer": None,
            "errors": [closure.failure_code.name],
            "binding": binding,
        }
    answer = candidate["answer"]
    decision = "ACCEPT" if answer else "DEFER"
    if candidate.get("result_status") == "CONFLICT":
        decision = "ACCEPT_CONFLICT_REPORT"
    elif answer and len(alternatives) > 1:
        decision = "ACCEPT_WITH_ALTERNATIVES"
    elif (
        answer
        and any(x in unresolved for x in ("CASE_PREMISE_MISSING", "REPRESENTATION_PREMISE_MISSING"))
        or answer
        and (candidate.get("status") == "PARTIAL" or candidate.get("result_status") == "PARTIAL")
    ):
        decision = "PARTIAL"
    return {
        "decision": decision,
        "answer": answer,
        "binding": binding,
        "review": review,
        "authority": authority,
        "residuals": unresolved,
        "alternatives": alternatives,
        "gamma": {
            "state": closure.state.value,
            "rank": closure.rank.name,
            "scope": boundary.scope,
            "stage": closure.trace_event_candidate.stage,
        },
        "scope": candidate["scope"],
        **({"judgment_status": candidate["result_status"]} if "result_status" in candidate else {}),
    }


def render(question, artifact, **trust):
    """No overload accepting a verdict, receipt or producer status."""
    return admit(question, artifact, **trust)


def serialize_candidate(question, artifact, **trust):
    decision = admit(question, artifact, **trust)
    if decision["decision"] == "REJECT":
        raise ValueError("rejected content cannot be stored as an admitted candidate")
    return json.dumps({"question": question, "candidate": artifact}, ensure_ascii=False)


def reload_candidate(question, serialized, **trust):
    stored = json.loads(serialized)
    if set(stored) != {"question", "candidate"} or stored["question"] != question:
        return {"decision": "REJECT", "answer": None, "errors": ["RELOAD_BINDING"]}
    return admit(question, stored["candidate"], **trust)
