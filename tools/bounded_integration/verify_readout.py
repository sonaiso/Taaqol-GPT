"""Independent experimental artifact verifier; no Alghanem imports or producer calls.

This is a pre-SlotGraph review tool. VERIFIED here means the quoted row readout
preserves the controlled request and imported annotations. It issues no
Gamma closure, knowledge rank, final audit, or universal linguistic license.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json


def _digest(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8", "surrogatepass"
        )
    ).hexdigest()


def verify_readout(question, artifact, data, expected_sha256):
    errors = []

    def require(condition, code):
        if not condition:
            errors.append(code)

    require(hashlib.sha256(data).hexdigest() == expected_sha256, "SOURCE_INTEGRITY")
    if errors:
        return {"verified": False, "errors": errors, "authority": "pre_admission_only"}
    try:
        require(
            set(artifact)
            == {
                "schema",
                "question",
                "status",
                "scope",
                "claims",
                "residuals",
                "trace",
                "generation",
                "answer",
                "derived_from_116",
                "llm_contribution",
                "request",
                "evidence",
                "content_digest",
            },
            "UNDECLARED_ARTIFACT_FIELD",
        )
        require(artifact["schema"] == "bounded-question-v1", "ARTIFACT_SCHEMA")
        require(artifact["question"] == question, "QUESTION_BINDING")
        require(artifact["scope"] == "quoted_text_analysis_not_event_assertion", "SCOPE_ESCALATION")
        require(artifact["derived_from_116"] is False, "UNLICENSED_ALGEBRA_CLAIM")
        # A separate grammar implementation, sharing only the written contract.
        prefix, address = question.strip().removesuffix("؟").split(" في المقطع ")
        target = prefix.removeprefix("ما ")
        require(
            prefix == "ما " + target and target in ("الفعل", "الفاعل", "المفعول به", "الأطراف"),
            "REQUEST_GRAMMAR",
        )
        coordinates = address.split(":")
        require(
            len(coordinates) == 3 and all(c.isascii() and c.isdecimal() for c in coordinates),
            "REQUEST_ADDRESS",
        )
        sura, ayah, word = map(int, coordinates)
        require(
            artifact["request"]
            == {
                "target": target,
                "locus": [sura, ayah, word],
                "constraints": {"mode": "quote", "family": "past_active_vso"},
            },
            "REQUEST_CHANGED",
        )
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
        rows = list(reader)
        expected_roles = ("فعل ماضٍ", "فاعل", "مفعول به")
        expected_case = ("مبني", "مرفوع", "منصوب")
        expected_targets = ("predicate_position", "faa_il_position", "maf_ul_bih_position")
        require(
            len(artifact["claims"]) == 3 and len(artifact["evidence"]) == 3, "CLAIM_CARDINALITY"
        )
        derived = []
        for offset in range(3):
            loc = [sura, ayah, word + offset]
            selected = [
                (i, r)
                for i, r in enumerate(rows)
                if [r["Sura_No"], r["Verse_No"], r["Column5"]] == list(map(str, loc))
            ]
            rs = [r for _, r in selected]
            evidence = artifact["evidence"][offset]
            require(evidence["source_sha256"] == expected_sha256, "EVIDENCE_SOURCE")
            require(evidence["locus"] == loc, "EVIDENCE_LOCUS")
            require(
                evidence["rows"]
                == [{"row_index": i, "row_digest": _digest(r), "content": r} for i, r in selected],
                "EVIDENCE_ROWS",
            )
            stems = [r for r in rs if r["Morph_type"] == "Stem"]
            valid = (
                bool(rs)
                and len(stems) == 1
                and len({r["ID"] for r in rs}) == 1
                and len({(r["Word"], r["Without_Diacritics"]) for r in rs}) == 1
                and [r["Word_No"] for r in rs] == [str(i + 1) for i in range(len(rs))]
                and not any(
                    r["ID"] == rs[0]["ID"]
                    and [r["Sura_No"], r["Verse_No"], r["Column5"]] != list(map(str, loc))
                    for r in rows
                )
            )
            if valid:
                stem = stems[0]
                valid = (
                    stem["Syntactic_Role"] == expected_roles[offset]
                    and stem["Case_Mood"] == expected_case[offset]
                    and (
                        stem["Morph_tag"] == "PV"
                        if offset == 0
                        else stem["Morph_tag"].startswith("NOUN_") or stem["Morph_tag"] == "GERUND"
                    )
                )
                for r in rs:
                    if r is stem:
                        continue
                    valid = valid and (
                        r["Morph_tag"] == "DET"
                        and r["Morph_type"] == "Prefix"
                        or r["Segmented_Word"] == "(null)"
                        and r["Morph_tag"] == "PVSUFF_SUBJ:3MS"
                        or r["Morph_tag"].startswith("CASE_")
                        and r["Segmented_Word"] in ("ا", "(null)")
                    )
            c = artifact["claims"][offset]
            require(
                set(c)
                == {"role", "locus", "status", "value", "premises", "residuals", "authority"},
                "UNDECLARED_CLAIM_FIELD",
            )
            require(c["locus"] == loc and c["role"] == expected_roles[offset], "CLAIM_DIRECTION")
            require(c["status"] == ("PASS" if valid else "DEFER"), "CLAIM_VERDICT")
            require(c["value"] == (rs[0]["Word"] if valid else None), "CLAIM_VALUE")
            require(c["premises"] == [_digest(r) for r in rs], "CLAIM_DEPENDENCIES")
            require(c["authority"] == "MASAQ_annotation_at_occurrence", "CLAIM_AUTHORITY")
            require(not valid or not c["residuals"], "HIDDEN_CONTRADICTION")
            require(valid or bool(c["residuals"]), "UNNAMED_SUSPENSION")
            derived.append((bool(valid), rs[0]["Word"] if valid else None))
        wanted = {"الفعل": (0,), "الفاعل": (1,), "المفعول به": (2,), "الأطراف": (0, 1, 2)}[target]
        supported = [i for i in wanted if derived[i][0]]
        expected_answer = (
            "؛ ".join(expected_roles[i] + ": " + derived[i][1] for i in supported) or None
        )
        if all(v for v, _ in derived) and expected_answer is not None:
            expected_answer = (
                "في المقطع «" + " ".join(t for _, t in derived) + "»: " + expected_answer
            )
        require(artifact["answer"] == expected_answer, "ANSWER_DOES_NOT_MATCH_REQUEST")
        expected_status = (
            "PASS" if len(supported) == len(wanted) else "PARTIAL" if supported else "DEFER"
        )
        require(artifact["status"] == expected_status, "ANSWER_VERDICT")
        require(
            artifact["content_digest"]
            == _digest({k: v for k, v in artifact.items() if k != "content_digest"}),
            "ARTIFACT_DIGEST",
        )
        generation = artifact["generation"]
        if all(v for v, _ in derived):
            require(generation is not None, "MISSING_GENERATION")
            ids = [":".join(map(str, (sura, ayah, word + i))) for i in range(3)]
            require(generation["surface"] == " ".join(t for _, t in derived), "SURFACE_CHANGED")
            require(generation["derived_from_116"] is False, "GENERATION_AUTHORITY")
            spec = generation["specification"]
            require(
                spec["requested_tense"] == "past"
                and spec["requested_voice"] == "active"
                and spec["requested_sentence_form"] == "verbal_vso",
                "TENSE_VOICE_FORM",
            )
            require(spec["realization_constraints"] == [], "UNSUPPORTED_CONSTRAINT")
            require(generation["specification_digest"] == _digest(spec), "SPEC_DIGEST")
            require(len(generation["tokens"]) == 3, "TOKEN_CARDINALITY")
            for i, token in enumerate(generation["tokens"]):
                require(
                    token["surface"] == derived[i][1] and token["source_element_id"] == ids[i],
                    "TOKEN_SOURCE_DIRECTION",
                )
                require(token["syntactic_target"] == expected_targets[i], "TOKEN_ROLE")
                require(
                    spec["realization_targets"][i]["element_id"] == ids[i]
                    and spec["realization_targets"][i]["target"] == expected_targets[i],
                    "SPEC_ROLE_DIRECTION",
                )
                choice = spec["lexical_choice_refs"][i]
                require(
                    choice["entry_id"] == ids[i]
                    and choice["element_id"] == ids[i]
                    and choice["lexical_source_digest"] == expected_sha256
                    and choice["entry_content_id"] == _digest(artifact["evidence"][i]["rows"]),
                    "LEXICAL_READOUT",
                )
                require(token["lexical_choice_id"] == choice["choice_id"], "TOKEN_CHOICE")
            declaration = generation["execution_document"]["nisbah"]
            require(
                declaration["predicate"]["predicate_id"] == ids[0]
                and [a["anchor_id"] for a in declaration["anchors"]] == ids[1:],
                "EXECUTION_SOURCE_BINDING",
            )
            require(
                spec["source_ref"]["execution_digest"] == generation["execution_digest"],
                "EXECUTION_REFERENCE",
            )
            stages = generation["stages"]
            require(len(stages) == 12, "STAGE_CARDINALITY")
            for stage in stages:
                require(stage["output_digest"] == _digest(stage["output"]), "STAGE_DIGEST")
            for start in (0, 3, 6, 9):
                require(
                    stages[start]["input"] == generation["specification_digest"], "STAGE_ORIGIN"
                )
                for j in (start + 1, start + 2):
                    require(
                        stages[j]["input"] == stages[j - 1]["output_digest"], "STAGE_CONTINUITY"
                    )
            _verify_transitions(generation, ids, expected_targets, require)
            require(stages[-1]["output"]["tokens"] == generation["tokens"], "ORTHOGRAPHIC_PAYLOAD")
        else:
            require(generation is None, "GENERATED_WITH_MISSING_PREMISE")
        trace = artifact["trace"]
        expected_origins = {
            "question": "caller_selection; parser is a declared convention",
            "claims": "imported source; no semantic discovery from atoms",
            "generation": "declared family + imported forms and roles",
            "answer": "derived from verified row readouts",
        }
        require(
            all(t["origin"] == expected_origins[t["name"]] for t in trace),
            "UNLICENSED_PREMISE_ORIGIN",
        )
        expected_rules = {
            "question": "bounded-question-v1",
            "claims": "MASAQ-exact-header-adapter-v1",
            "generation": "generation/PAST_ACTIVE_TRANSITIVE_VSO",
            "answer": "bounded-answer-v1",
        }
        require(
            all(t["rule_source"] == expected_rules[t["name"]] for t in trace),
            "UNKNOWN_TRANSITION_RULE",
        )
        require(artifact["llm_contribution"] is None, "UNDECLARED_MODEL_CONTRIBUTION")
        require(
            [t["name"] for t in trace]
            == (
                ["question", "claims", "generation", "answer"]
                if generation is not None
                else ["question", "claims", "answer"]
            ),
            "TRACE_COVERAGE",
        )
        require(
            trace[0]["inputs"] == question and trace[0]["output"] == artifact["request"],
            "TRACE_REQUEST",
        )
        require(
            trace[1]["inputs"] == artifact["evidence"] and trace[1]["output"] == artifact["claims"],
            "TRACE_CLAIMS",
        )
        require(
            trace[-1]["output"] == artifact["answer"]
            and trace[-1]["inputs"] == [artifact["claims"][i] for i in wanted],
            "TRACE_ANSWER",
        )
        if generation is not None:
            require(
                trace[2]["inputs"] == artifact["claims"] and trace[2]["output"] == generation,
                "TRACE_GENERATION",
            )
        require(
            all(
                t["rule_source"] and t["conditions"] and t["origin"] and t["preserved"]
                for t in trace
            ),
            "UNDECLARED_PREMISE_OR_RULE",
        )
    except (KeyError, ValueError, TypeError, IndexError, AttributeError):
        errors.append("MALFORMED_OR_UNSUPPORTED_ARTIFACT")
    return {
        "verified": not errors,
        "errors": sorted(set(errors)),
        "authority": "pre_admission_only",
        "checked": "question, occurrence, imported roles, form, direction, trace",
        "not_proved": [
            "external truth",
            "116 semantic derivation",
            "Gamma closure",
            "independent proof of execution kernel laws",
        ],
    }


def _verify_transitions(
    generation,
    ids,
    targets,
    require,
    binding_rule="masaq.role.binding.v1",
    origin="imported form/role + declared family operation",
):
    stages = generation["stages"]
    spec = generation["specification"]
    tokens = generation["tokens"]
    names = ["lexical_selection", "word_form", "relation_slot_assignment"]
    rules = ["occurrence.read.form.v1", "attested.form.no.inflection.v1", binding_rule]
    effects = ["no_effect_in_this_family", "raf", "nasb"]
    nisbah = generation["execution_document"]["nisbah"]["nisbah_id"]
    for i in range(3):
        block = stages[i * 3 : i * 3 + 3]
        selection, form, slot = (x["output"] for x in block)
        require([x["stage"] for x in block] == names, "STAGE_KIND")
        require([x["operation"] for x in block] == rules, "STAGE_OPERATION")
        require(
            selection["choice"] == spec["lexical_choice_refs"][i]
            and selection["element_id"] == ids[i]
            and selection["target"] == targets[i]
            and selection["specification_content_id"] == generation["specification_digest"],
            "SELECTION_PREMISES",
        )
        require(
            form["selection_content_id"] == block[0]["output_digest"]
            and form["element_id"] == ids[i]
            and form["target"] == targets[i]
            and form["lexical_form_ref"] == ids[i]
            and form["morphological_operation_trace"] == ["lexically_attested_form_selection"],
            "WORD_FORM_PREMISES",
        )
        require(
            slot["word_form_content_id"] == block[1]["output_digest"]
            and slot["element_id"] == ids[i]
            and slot["target"] == targets[i]
            and slot["source_nisbah_id"] == nisbah
            and slot["source_execution_digest"] == generation["execution_digest"],
            "SLOT_PREMISES",
        )
        require(
            tokens[i]["case_effect"] == effects[i]
            and tokens[i]["morphological_operation_trace"] == ["lexically_attested_form_selection"],
            "TOKEN_MORPHOLOGY",
        )
        expected_steps = [
            {
                "stage": names[j],
                "rule_id": rules[j],
                "input_content_id": block[j]["input"],
                "output_content_id": block[j]["output_digest"],
                "residuals": [],
            }
            for j in range(3)
        ]
        require(tokens[i]["generation_trace"]["steps"] == expected_steps, "TOKEN_TRANSITION_RULE")
    for stage in stages:
        require(
            stage["rule_source"] == "GEN-0/PAST_ACTIVE_TRANSITIVE_VSO"
            and stage["origin"] == origin
            and stage["conditions"]
            == ["occurrence identity checked", "family constraints retained"]
            and stage["preserved"]
            == ["source element identity", "syntactic target", "attested form"]
            and stage["residuals"] == ["not a derivation of semantics from 116"],
            "STAGE_AUTHORITY_OR_CONDITIONS",
        )
    require(
        [x["operation"] for x in stages[9:]]
        == ["family.vso.v1", "imported.case.alignment.v1", "attested.surface.join.v1"],
        "FINAL_STAGE_OPERATION",
    )
    composition, case, orthography = (x["output"] for x in stages[9:])
    require(
        [x["stage"] for x in stages[9:]]
        == ["composition", "case_effect", "orthographic_projection"],
        "FINAL_STAGE_KIND",
    )
    require(
        composition["assignments"] == [stages[i]["output"] for i in (2, 5, 8)]
        and composition["surface_order"] == list(targets)
        and composition["source_nisbah_id"] == nisbah,
        "COMPOSITION_PREMISES",
    )
    require(
        case["composition_content_id"] == stages[9]["output_digest"]
        and case["effects"] == dict(zip(targets, effects, strict=False)),
        "CASE_PREMISES",
    )
    require(
        orthography["case_effect_content_id"] == stages[10]["output_digest"]
        and orthography["orthographic_source"] == "lexically_attested_form_selection",
        "ORTHOGRAPHIC_PREMISES",
    )
