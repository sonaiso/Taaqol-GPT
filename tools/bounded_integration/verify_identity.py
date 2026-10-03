"""Check identity revisions and quoted propositions, then existing Gamma admission.

Trusted shared: typed source adapter, finite query grammar/reference projection,
domain rule approval, Unicode/116 replay and renderer. No producer invocation.
"""

import base64
import re

from alghanem.integration.identity_question import RESIDUALS, render, request
from alghanem.integration.knowledge_question import explanations
from alghanem.ontology.identity_network import resolve_occurrence, review_preparation
from alghanem.ontology.operational import identity
from alghanem.ontology.review import verify_closure


def check_discourse(clause, time, scope, model, closure, candidate):
    from canonical116 import verify

    if set(candidate) != {"source", "tokens", "readings", "authority"}:
        raise ValueError("DISCOURSE_FIELDS")
    if (
        candidate["source"] != clause
        or candidate["authority"] != "text_under_declared_conventions_not_116_derivation"
    ):
        raise ValueError("DISCOURSE_SOURCE_AUTHORITY")
    spans = list(re.finditer(r"\S+", clause))
    if len(spans) != len(candidate["tokens"]):
        raise ValueError("DISCOURSE_TOKEN_COVERAGE")
    for span, token in zip(spans, candidate["tokens"], strict=True):
        record = token["representation"]
        if (
            set(token) != {"text", "span", "representation"}
            or token["text"] != span[0]
            or token["span"] != list(span.span())
            or base64.b64decode(record["source_bytes_base64"]).decode(record["encoding"]) != span[0]
            or not verify(record)["reproduced"]
        ):
            raise ValueError("DISCOURSE_REPRESENTATION_BINDING")
    expected = []
    for rule in model["identity_network"]["text_rules"]:
        m = re.fullmatch(rule["pattern"], clause)
        if not m:
            continue
        if rule["rank"] != "convention" or not rule["source"]:
            raise ValueError("DISCOURSE_RULE_AUTHORITY")
        op = rule["operation"]
        if op in ("arrival", "visit") and " " in m["agent"]:
            forms = {f for v in model["identity_network"]["lexemes"].values() for f in v["forms"]}
            if m["agent"] not in forms:
                continue
        if op == "described_arrival" and not (
            m["kind"] in rule["nominals"] and m["quality"] in rule["qualities"]
        ):
            continue
        c = dict(
            predicate=rule["predicate"],
            scope="discourse_only",
            time=time,
            polarity="+",
            real_occurrence=False,
        )
        op = rule["operation"]
        if op == "mention":
            c.update(
                subject=dict(
                    kind="lexical_occurrence",
                    text=m["name"],
                    span=list(m.span("name")),
                    identity=identity([scope, time, clause, m.span("name")]),
                ),
                property="short_as_said_not_measured",
            )
        elif op in ("arrival", "visit"):
            c["agent"] = dict(
                kind="reference_occurrence",
                **resolve_occurrence(m["agent"], time, scope, model, closure),
            )
            if op == "visit":
                c["destination"] = dict(
                    kind="discourse_variable",
                    id=identity([clause, "destination"]),
                    concept="City",
                    external_identity=None,
                )
        elif op == "described_arrival":
            c["agent"] = dict(
                kind="discourse_variable",
                concept=rule["nominals"][m["kind"]],
                qualification=rule["qualities"][m["quality"]],
                external_identity=None,
            )
        elif op == "capital":
            c.update(
                holder=dict(kind="discourse_variable", concept="City", external_identity=None),
                country=dict(kind="unresolved_role", external_identity=None),
                relation="capital_of_at_time_not_a_new_species",
            )
        else:
            raise ValueError("UNSUPPORTED_DISCOURSE_OPERATION")
        expected.append(
            dict(
                rule=rule["id"],
                version=rule["version"],
                imported=rule,
                bindings={k: dict(text=m[k], span=list(m.span(k))) for k in m.groupdict()},
                content=c,
            )
        )
    if candidate["readings"] != expected:
        raise ValueError("DISCOURSE_CONTENT_OR_ALTERNATIVES")
    return candidate


def verify_identity(question, candidate, environment):
    errors = []
    try:
        review_preparation(environment, candidate["preparation"])
        records = candidate["preparation"]["records"]
        _, failures = verify_closure(environment["model"], records, candidate["closure"])
        errors.extend(failures)
        q = request(
            question,
            environment,
            candidate["closure"],
            reader=lambda *args: check_discourse(*args, candidate["request"]["analysis"]),
        )
        detail = explanations(q["goals"], candidate["closure"], records, environment["model"])
        expected = dict(
            schema="identity-answer-v1",
            question=question,
            environment_digest=identity(environment),
            preparation=candidate["preparation"],
            closure=candidate["closure"],
            request=q,
            explanations=detail,
            **render(q, detail),
            alternatives=q["reference"]["groups"] if q["reference"] else [],
            residuals=RESIDUALS,
            scope="finite_identity_naming_and_discourse",
        )
        if candidate != expected:
            errors.append("IDENTITY_ANSWER_CONTENT_BINDING")
    except (KeyError, ValueError, TypeError, IndexError, AttributeError) as error:
        errors.append("UNVERIFIED_IDENTITY:" + str(error))
    return dict(
        verified=not errors,
        errors=errors,
        binding=identity(dict(question=question, candidate=candidate, environment=environment)),
        authority="finite_identity_and_rule_review_not_world_certification",
    )
