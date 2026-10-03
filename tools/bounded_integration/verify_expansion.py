"""Bounded composition review, not promotion to independent linguistic truth.

Trusted: declared question grammar/renderer and resource adapters, pinned source
bytes, bridge. Rechecks actual inner rule applications with verify_fragment;
never invokes the producer. Reconstructs lexical premises from external resources.
"""

from contracts import definition_claims, lexical_policy, parse_request, quoted_records
from pipeline import EXAMPLE, presentation
from verify_fragment import verify_fragment
from verify_readout import _digest


def verify_expansion(question, artifact, stock):
    errors = []

    def need(condition, reason):
        if not condition:
            errors.append(reason)

    try:
        stock.validate()
        need(artifact["schema"] == "expanded-fragment-v1", "SCHEMA")
        need(artifact["question"] == question, "QUESTION_BINDING")
        need(artifact["resources"] == stock.manifest(), "RESOURCE_BINDING")
        request = parse_request(question, "questions" in stock.features)
        records = quoted_records(question)
        need(artifact["request"] == request, "REQUEST_BINDING")
        need(artifact["representations"] == records, "SOURCE_REPRESENTATIONS")
        inner, evidence, definitions = artifact["inner"], [], []
        canonical_question = None
        if request and request["operation"] in ("syntax", "semantic_actor"):
            policy, evidence = lexical_policy(records, stock)
            target = request["target"] if request["operation"] == "syntax" else "الفاعل"
            canonical_question = f'ما {target} في «{request["clause"]}»؟'
        elif (
            request
            and request["operation"] == "compare_definitions"
            and "explanation" in stock.features
        ):
            definitions = definition_claims(stock, request["target"])
            policy, evidence = lexical_policy(quoted_records(f"«{EXAMPLE}»"), stock)
            canonical_question = f"ما الأطراف في «{EXAMPLE}»؟"
        if canonical_question:
            review = verify_fragment(canonical_question, inner, policy)
            errors += ["INNER:" + e for e in review["errors"]]
        else:
            need(inner is None, "UNLICENSED_INNER")
        need(artifact["evidence"] == evidence, "LEXICAL_WITNESSES")
        need(artifact["definitions"] == definitions, "DEFINITION_WITNESSES")
        expected = presentation(request, inner, definitions, evidence)
        for key, value in expected.items():
            need(artifact.get(key) == value, "PRESENTATION:" + key)
        need(
            set(artifact)
            == set(expected)
            | {
                "schema",
                "question",
                "resources",
                "request",
                "representations",
                "evidence",
                "definitions",
                "inner",
            },
            "FIELDS",
        )
    except (KeyError, ValueError, TypeError, IndexError, AttributeError):
        errors.append("MALFORMED_OR_UNTRUSTED_SOURCE")
    return {
        "verified": not errors,
        "errors": sorted(set(errors)),
        "authority": "review_under_declared_family_and_imported_lexical_stock",
        "binding": _digest(
            {"question": question, "artifact": artifact, "resources": stock.manifest()}
        ),
    }
