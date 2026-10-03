"""Content checker for a declared formal fragment, not general linguistic authority.

Trusted: bridge implementation, declared lexical inventory/grammar, GEN-0 carrier
contract. Independently checks the producer's rule instances, complete alternatives,
question projection and generation. Does not call the analysis/generation producer.
"""

from __future__ import annotations

import itertools

from verify_readout import _digest, _verify_transitions


def verify_fragment(question, artifact, policy):
    from canonical116 import verify

    errors = []

    def need(condition, reason):
        if not condition:
            errors.append(reason)

    try:
        need(
            set(artifact)
            == {
                "schema",
                "question",
                "policy",
                "authority",
                "scope",
                "request",
                "representations",
                "applications",
                "alternatives",
                "claims",
                "generation",
                "answer",
                "residuals",
            },
            "ARTIFACT_FIELDS",
        )
        need(artifact["question"] == question, "QUESTION_BINDING")
        need(artifact["policy"] == policy, "TRUST_POLICY_BINDING")
        need(policy["id"] == "explicit-case-fragment-v1", "POLICY_VERSION")
        need(policy["authority"] == "declared_controlled_grammar_convention", "PRIOR_RANK")
        need(
            policy["rules"]
            == [
                "FULL_QUESTION_V1",
                "BRIDGE_SUPPORT_TANWIN_V1",
                "LEXICAL_MEMBERSHIP_V1",
                "ACTIVE_CASE_ASSIGNMENT_V1",
                "REQUEST_PROJECTION_V1",
            ],
            "RULE_VERSION",
        )
        need(artifact["authority"] == "derived_under_declared_prior", "AUTHORITY")
        need(
            artifact["scope"]
            == policy["scope"]
            == "quoted_syntactic_function_under_declared_prior_not_external_event",
            "SCOPE",
        )
        need(artifact["schema"] == "derived-fragment-v1", "SCHEMA")
        residuals = list(policy["residuals"])
        claims, alternatives, applications = [], [], []
        request, words, records, forms = None, [], [], []
        valid_question = False
        for target in ("الفعل", "الفاعل", "المفعول به", "الأطراف"):
            prefix = "ما " + target + " في «"
            if question.startswith(prefix) and question.endswith("»؟"):
                clause = question[len(prefix) : -2]
                if clause and "«" not in clause and "»" not in clause and "\n" not in clause:
                    request = {"target": target, "clause": clause}
                    words = clause.split(" ")
                    valid_question = True
        if not valid_question:
            residuals.append("QUESTION_OUTSIDE_FRAGMENT")
        elif len(words) != 3 or not all(words):
            residuals.append("THREE_WORD_CLAUSE_REQUIRED")
        else:
            records = artifact["representations"]
            need(len(records) == 3, "REPRESENTATION_COUNT")
            for word, record in zip(words, records, strict=True):
                need(record["source_text"] == word, "TEXT_IDENTITY")
                need(
                    record["options"]
                    == {
                        "encoding": "utf-8",
                        "profile": "modern-support-tanwin-v1",
                        "contexts": None,
                        "annotations": None,
                    },
                    "SIDE_INPUT",
                )
                need(verify(record)["reproduced"], "REPRESENTATION_REPLAY")
            if records[0]["status"] != "READY" or records[0]["boundaries"]:
                residuals.append("REPRESENTATION_PREMISE_MISSING")
            else:
                forms = [
                    r["words"][0]["orthographic_projection"]["text"] if r["words"] else None
                    for r in records
                ]
                if forms[0] not in policy["verbs"]:
                    residuals.append("VERB_PRIOR_MISSING")
                else:
                    claims.append({"role": "الفعل", "occurrence": 0, "surface": words[0]})
                    applications.append(
                        {
                            "rule": "LEXICAL_MEMBERSHIP_V1",
                            "inputs": records[0]["canonical_atoms"],
                            "premise": ["verbs", forms[0]],
                            "output": {"verb": 0, "past": True, "active": True},
                            "origin": "atom shape plus declared verb paradigm",
                        }
                    )
                    possible = {"nominative": set(), "accusative": set()}
                    for i in (1, 2):
                        if (
                            forms[i] not in policy["nouns"]
                            or records[i]["status"] != "READY"
                            or records[i]["boundaries"]
                        ):
                            continue
                        if forms[i] in policy["indeclinables"]:
                            for indices in possible.values():
                                indices.add(i)
                        else:
                            sequence = records[i]["canonical_atoms"] or []
                            for case, mark in (("nominative", "ُ"), ("accusative", "َ")):
                                if (
                                    len(sequence) > 1
                                    and sequence[-1] == "نْ"
                                    and sequence[-2].endswith(mark)
                                ):
                                    possible[case].add(i)
                    for subject, obj in itertools.permutations((1, 2)):
                        if (
                            subject not in possible["nominative"]
                            or obj not in possible["accusative"]
                        ):
                            continue
                        alt = {"verb": 0, "subject": subject, "object": obj}
                        alternatives.append(alt)
                        applications.append(
                            {
                                "rule": "ACTIVE_CASE_ASSIGNMENT_V1",
                                "inputs": [
                                    records[i]["canonical_atoms"][-2:] for i in (subject, obj)
                                ],
                                "premises": [["nouns", forms[subject]], ["nouns", forms[obj]]],
                                "conditions": [
                                    "nominative subject",
                                    "accusative object",
                                    "active past",
                                ],
                                "output": alt,
                                "origin": (
                                    "representation plus lexical cases " "plus controlled grammar"
                                ),
                            }
                        )
                    if len(alternatives) == 1:
                        for role, key in (("الفاعل", "subject"), ("المفعول به", "object")):
                            i = alternatives[0][key]
                            claims.append({"role": role, "occurrence": i, "surface": words[i]})
                    else:
                        residuals.append(
                            "CASE_ASSIGNMENT_AMBIGUOUS" if alternatives else "CASE_PREMISE_MISSING"
                        )
        need(artifact["request"] == request, "REQUEST")
        need(artifact["representations"] == records, "UNEXPECTED_REPRESENTATIONS")
        need(artifact["claims"] == claims, "CLAIM_CONTENT")
        need(artifact["alternatives"] == alternatives, "ALTERNATIVES")
        need(artifact["applications"] == applications, "RULE_APPLICATION")
        need(artifact["residuals"] == residuals, "RESIDUALS")
        selected = [c for c in claims if request and request["target"] in ("الأطراف", c["role"])]
        expected_answer = (
            "؛ ".join(c["role"] + " في العبارة: " + c["surface"] for c in selected) or None
        )
        need(artifact["answer"] == expected_answer, "ANSWER_BINDING")
        if len(alternatives) != 1:
            need(artifact["generation"] == [], "UNLICENSED_GENERATION")
        else:
            need(len(artifact["generation"]) == 1, "GENERATION_COUNT")
            g = artifact["generation"][0]
            need(
                g["specification"]["requested_tense"] == "past"
                and g["specification"]["requested_voice"] == "active"
                and g["specification"]["requested_sentence_form"] == "verbal_vso"
                and g["specification"]["realization_constraints"] == [],
                "GENERATION_CONSTRAINTS",
            )
            indices = [0, alternatives[0]["subject"], alternatives[0]["object"]]
            ids = list(map(str, indices))
            targets = ["predicate_position", "faa_il_position", "maf_ul_bih_position"]
            need(g["surface"] == " ".join(words[i] for i in indices), "GENERATED_DIRECTION")
            need(g["derived_from_116"] is False, "GENERATION_AUTHORITY")
            need(
                g["syntactic_binding_scope"] == "derived case assignment under declared prior",
                "GENERATION_ORIGIN",
            )
            need(g["specification_digest"] == _digest(g["specification"]), "SPEC_DIGEST")
            for j, i in enumerate(indices):
                token = g["tokens"][j]
                need(
                    token["surface"] == words[i]
                    and token["source_element_id"] == str(i)
                    and token["syntactic_target"] == targets[j],
                    "TOKEN_CONTENT",
                )
                choice = g["specification"]["lexical_choice_refs"][j]
                need(
                    choice["entry_content_id"] == _digest(records[i])
                    and choice["lexical_source_digest"] == _digest(policy)
                    and choice["element_id"] == str(i),
                    "LEXICAL_PREMISE",
                )
                need(
                    g["specification"]["realization_targets"][j]["element_id"] == str(i),
                    "SPEC_DIRECTION",
                )
            need(len(g["stages"]) == 12, "STAGES")
            for stage in g["stages"]:
                need(stage["output_digest"] == _digest(stage["output"]), "STAGE_DIGEST")
            for start in (0, 3, 6, 9):
                need(g["stages"][start]["input"] == g["specification_digest"], "STAGE_ORIGIN")
                for j in (start + 1, start + 2):
                    need(
                        g["stages"][j]["input"] == g["stages"][j - 1]["output_digest"],
                        "STAGE_CHAIN",
                    )
            _verify_transitions(
                g,
                ids,
                targets,
                need,
                "fragment.case.binding.v1",
                "derived case assignment under declared prior",
            )
            need(g["stages"][-1]["output"]["tokens"] == g["tokens"], "TOKEN_TRACE")
    except (KeyError, TypeError, ValueError, IndexError, AttributeError):
        errors.append("MALFORMED_ARTIFACT")
    return {
        "verified": not errors,
        "errors": sorted(set(errors)),
        "authority": "formal_fragment_under_trusted_policy",
        "binding": _digest({"question": question, "artifact": artifact, "policy": policy}),
    }
