"""Check ontology answers against independently supplied context and evidence.

Shared trusted linguistic frontend; independent proof-rule review and saturation.
No call to question.answer or operational.infer, no promotion of demo evidence.
"""

from alghanem.integration.language_review import check_analysis
from alghanem.integration.ontology_question import render, request
from alghanem.ontology.operational import evidence_atoms, identity
from alghanem.ontology.review import saturate, verify_closure


def verify_ontology(question, candidate, environment):
    errors = []
    try:
        model, records, context = (environment[k] for k in ("model", "evidence", "context"))
        q = request(
            question,
            model,
            context,
            analysis_reader=lambda clause, prior: check_analysis(
                clause, prior, candidate["request"]["analysis"]
            ),
        )
        for key, value in {
            "schema": "ontology-answer-v1",
            "question": question,
            "request": q,
            "model_digest": identity(model),
            "evidence_digest": identity(records),
            "context": context,
        }.items():
            if candidate.get(key) != value:
                errors.append("BINDING:" + key)
        facts, issues = verify_closure(model, records, candidate["closure"])
        errors.extend(issues)
        expected = []
        deletions = []
        leaves, _ = evidence_atoms(model, records)
        index = {tuple(r["atom"]): r["proofs"] for r in candidate["closure"]["index"]}
        for goal in q["goals"]:
            positive = tuple(goal)
            negative = (*positive[:3], "-" if positive[3] == "+" else "+", *positive[4:])
            mask = int(positive in facts) | (int(negative in facts) << 1)
            expected.append(
                dict(
                    target=goal,
                    support_bits=mask,
                    status=("UNDETERMINED", "SUPPORTED", "NEGATED", "CONFLICT")[mask],
                    supporting=index.get(positive, []),
                    opposing=index.get(negative, []),
                    knowledge_state=("unknown", "known", "known", "disputed")[mask],
                    minimality=(
                        "inclusion-minimal evidence supports in this "
                        "proof system; not global cardinality minimum"
                    ),
                )
            )
            checked = []
            if index.get(positive):
                selected = candidate["closure"]["nodes"][index[positive][0]]["leaves"]
                for rid in selected:
                    remaining = {leaves[x] for x in selected if x != rid}
                    checked.append(
                        dict(
                            deleted=rid,
                            selected_proof_still_supported=positive in saturate(model, remaining),
                        )
                    )
            deletions.append(checked)
        if candidate["decisions"] != expected:
            errors.append("JUDGMENT_CONTENT")
        if candidate["selected_proof_deletion_checks"] != deletions:
            errors.append("MINIMALITY_CHECK")
        for key, value in render(q, expected).items():
            if candidate.get(key) != value:
                errors.append("ANSWER:" + key)
        residuals = (
            q["residuals"]
            + (q["analysis"]["residuals"] if q["analysis"] else [])
            + [
                "not universal Arabic semantics",
                "actual-world evidence unavailable in this demonstration",
                "no persistence beyond evidence timestamp",
                "Gamma review rank TRACE",
            ]
        )
        if (
            candidate["residuals"] != residuals
            or candidate["scope"] != "finite_declared_ontology_and_simulated_world"
            or candidate["alternatives"] != []
        ):
            errors.append("SCOPE_OR_RESIDUALS")
        if set(candidate) != {
            "schema",
            "question",
            "request",
            "model_digest",
            "evidence_digest",
            "context",
            "closure",
            "decisions",
            "selected_proof_deletion_checks",
            "scope",
            "alternatives",
            "residuals",
            "answer",
            "result_status",
            "authority",
        }:
            errors.append("UNAUTHORIZED_FIELDS")
    except (KeyError, TypeError, ValueError, IndexError, AttributeError) as error:
        errors.append("MALFORMED_OR_UNVERIFIED:" + str(error))
    return dict(
        verified=not errors,
        errors=sorted(set(errors)),
        binding=identity(
            {"question": question, "candidate": candidate, "environment": environment}
        ),
        authority="bounded_content_review_not_actual_world_certification",
    )
