"""Source-content review plus independent closure and linguistic certificate review."""

from alghanem.integration.knowledge_question import explanations, plan, presentation
from alghanem.ontology.acquisition import bit_learning, review_acquisition
from alghanem.ontology.operational import evidence_atoms, identity
from alghanem.ontology.review import saturate, verify_closure
from verify_ontology import verify_ontology


def verify_knowledge(question, candidate, environment):
    errors = []
    try:
        if candidate["question"] != question or candidate["environment_digest"] != identity(
            environment
        ):
            raise ValueError("ENVIRONMENT_BINDING")
        review_acquisition(environment, candidate["acquisition"])
        records = candidate["acquisition"]["records"]
        model, context = environment["model"], environment["context"]
        facts, issues = verify_closure(model, records, candidate["closure"])
        errors.extend(issues)
        q = plan(question, model, context, [list(x) for x in sorted(facts)])
        inner = candidate["inner"]
        if q["operation"] == "legacy":
            checked = verify_ontology(
                question, inner, dict(model=model, evidence=records, context=context)
            )
            errors.extend(checked["errors"])
            q["goals"] = inner["request"]["goals"]
        elif inner is not None:
            errors.append("UNEXPECTED_LEGACY_ANSWER")
        if q != candidate["request"]:
            errors.append("QUESTION_REQUEST_BINDING")
        detail = explanations(q["goals"], candidate["closure"], records, model)
        if detail != candidate["explanations"]:
            errors.append("EXPLANATION_PROOF_BINDING")
        rendered = (
            {k: inner[k] for k in ("answer", "result_status", "authority")}
            if inner
            else presentation(q, detail, model)
        )
        if inner and rendered["answer"] and detail:
            evidence = sorted(
                {e["id"] for row in detail for p in row["proofs"] for e in p["evidence"]}
            )
            rendered["answer"] += " الدليل: " + ", ".join(evidence)
        for key, value in rendered.items():
            if candidate[key] != value:
                errors.append("ANSWER:" + key)
        leaves, _ = evidence_atoms(model, environment["evidence"])
        baseline = {"index": [{"atom": list(x)} for x in saturate(model, set(leaves.values()))]}
        after = {"index": [{"atom": list(x)} for x in facts]}
        if candidate["learning"] != bit_learning(baseline, after):
            errors.append("BIT_LEARNING_BINDING")
        residuals = (inner["residuals"] if inner else []) + [
            "simulated sources in demonstration",
            "no persistence or ownership from location",
            "Gamma TRACE",
            "question grammar and renderer remain shared trusted components",
        ]
        if candidate["residuals"] != residuals or candidate["alternatives"] != []:
            errors.append("RESIDUALS")
        if candidate["scope"] != "finite_knowledge_acquisition_under_declared_source_policy":
            errors.append("SCOPE")
        if (
            set(candidate)
            != {
                "schema",
                "question",
                "environment_digest",
                "acquisition",
                "closure",
                "request",
                "inner",
                "explanations",
                "learning",
                "answer",
                "result_status",
                "authority",
                "scope",
                "alternatives",
                "residuals",
            }
            or candidate["schema"] != "knowledge-answer-v1"
        ):
            errors.append("FIELDS_OR_SCHEMA")
    except (KeyError, ValueError, TypeError, IndexError, AttributeError) as error:
        errors.append("UNVERIFIED:" + str(error))
    return dict(
        verified=not errors,
        errors=sorted(set(errors)),
        binding=identity(
            {"question": question, "candidate": candidate, "environment": environment}
        ),
        authority="bounded_acquisition_and_rule_review",
    )
