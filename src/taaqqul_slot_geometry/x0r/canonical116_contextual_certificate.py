"""Reproducible contextual certification from canonical116 readiness to word-in-context.

This module implements a bounded, replayable evidence chain that keeps
source-provenance identity separate from lexical/syntactic licensing.

Key constitutional discipline in this surface:
- canonical116 readiness is a separate layer and never implies word licensing.
- source fingerprint is provenance evidence and never implies morphology/syntax truth.
- claim C (dataset-origin linkage) is never inferred from claim A/B.
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256
from pathlib import Path


class CertificationSchemaError(ValueError):
    """Raised when fixture or runtime inputs violate this bounded surface."""


class ClaimState(StrEnum):
    PROVEN = "PROVEN"
    REFUSED = "REFUSED"
    SUSPENDED = "SUSPENDED"


class LayerState(StrEnum):
    LICENSED = "LICENSED"
    REFUSED = "REFUSED"
    SUSPENDED = "SUSPENDED"


@dataclass(frozen=True, slots=True)
class ClaimVerdict:
    claim_id: str
    state: ClaimState
    reason: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LayerVerdict:
    layer_id: str
    state: LayerState
    reason: str
    evidence_refs: tuple[str, ...]
    dependencies: tuple[str, ...]
    residuals: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TransitionRecord:
    step_id: str
    input_ref: str
    operation: str
    condition: str
    blocker: str | None
    evidence_ref: str
    rank: str
    output_ref: str
    dependencies: tuple[str, ...]
    residuals: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SourceOccurrence:
    source_id: str
    sentence: str
    byte_start: int
    byte_end: int
    char_start: int
    char_end: int
    context_before: str
    context_after: str


@dataclass(frozen=True, slots=True)
class ContextualCertificate:
    fixture_id: str
    case_id: str
    dataset_excerpt_id: str
    domain_scope: str
    excluded_scope: tuple[str, ...]
    previous_audit_zip_found: tuple[str, ...]
    source_identities: tuple[dict[str, str], ...]
    claims: tuple[ClaimVerdict, ...]
    occurrences: tuple[SourceOccurrence, ...]
    layers: tuple[LayerVerdict, ...]
    overall_state: LayerState
    overall_reason: str
    transitions: tuple[TransitionRecord, ...]


def _strict_normalize(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise CertificationSchemaError("text must be a non-empty string")
    if "\uFFFD" in text:
        raise CertificationSchemaError("replacement character found; lossy decode is forbidden")
    for char in text:
        code = ord(char)
        if code < 32 and char not in {"\n", "\r", "\t"}:
            raise CertificationSchemaError(
                "control characters are forbidden in strict normalization"
            )
    return unicodedata.normalize("NFC", text)


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _list_previous_audit_zip(search_roots: tuple[Path, ...]) -> tuple[str, ...]:
    matches: list[str] = []
    wanted = {"Arabic_Letter_Exhaustive_Audit.zip"}
    prefixes = ("Arabic_Letter_Exhaustive_Audit",)
    for root in search_roots:
        if not root.exists() or not root.is_dir():
            continue
        for path in root.rglob("*.zip"):
            name = path.name
            if name in wanted or name.startswith(prefixes):
                matches.append(str(path))
    return tuple(sorted(set(matches)))


def _find_occurrences(source_id: str, text: str, sentence: str) -> tuple[SourceOccurrence, ...]:
    occurrences: list[SourceOccurrence] = []
    start = 0
    while True:
        idx = text.find(sentence, start)
        if idx < 0:
            break
        end = idx + len(sentence)
        before = text[max(0, idx - 40) : idx]
        after = text[end : end + 40]
        byte_start = len(text[:idx].encode("utf-8"))
        byte_end = len(text[:end].encode("utf-8"))
        occurrences.append(
            SourceOccurrence(
                source_id=source_id,
                sentence=sentence,
                byte_start=byte_start,
                byte_end=byte_end,
                char_start=idx,
                char_end=end,
                context_before=before,
                context_after=after,
            )
        )
        start = end
    return tuple(occurrences)


def _find_anchor_locked_occurrence(
    *,
    source_id: str,
    source_text: str,
    left_anchor: str,
    snippet: str,
    right_anchor: str,
) -> SourceOccurrence | None:
    needle = f"{left_anchor}{snippet}{right_anchor}"
    idx = source_text.find(needle)
    if idx < 0:
        return None
    second = source_text.find(needle, idx + len(needle))
    if second >= 0:
        return None
    sentence_start = idx + len(left_anchor)
    sentence_end = sentence_start + len(snippet)
    return SourceOccurrence(
        source_id=source_id,
        sentence=snippet,
        byte_start=len(source_text[:sentence_start].encode("utf-8")),
        byte_end=len(source_text[:sentence_end].encode("utf-8")),
        char_start=sentence_start,
        char_end=sentence_end,
        context_before=source_text[max(0, sentence_start - 40) : sentence_start],
        context_after=source_text[sentence_end : sentence_end + 40],
    )


def _claims_for_case(
    *,
    case: dict[str, object],
    sources: dict[str, dict[str, str]],
    search_occurrences: tuple[SourceOccurrence, ...],
) -> tuple[ClaimVerdict, ClaimVerdict, ClaimVerdict]:
    claim_a = ClaimVerdict(
        claim_id="A_PHRASE_EXISTS_IN_SOURCE",
        state=ClaimState.PROVEN if search_occurrences else ClaimState.REFUSED,
        reason=(
            "found at least one literal occurrence in configured source search set"
            if search_occurrences
            else "no literal occurrence in configured source search set"
        ),
        evidence_refs=tuple(
            f"occ:{occ.source_id}:{occ.byte_start}-{occ.byte_end}" for occ in search_occurrences
        ),
    )

    claim_b = ClaimVerdict(
        claim_id="B_UNIQUE_LOCATION_IN_SEARCH_SET",
        state=(ClaimState.PROVEN if len(search_occurrences) == 1 else ClaimState.REFUSED),
        reason=(
            "exactly one location in configured search set"
            if len(search_occurrences) == 1
            else f"expected one location but found {len(search_occurrences)}"
        ),
        evidence_refs=tuple(
            f"occ:{occ.source_id}:{occ.byte_start}-{occ.byte_end}" for occ in search_occurrences
        ),
    )

    origin_link = case.get("origin_link")
    if origin_link is None:
        claim_c = ClaimVerdict(
            claim_id="C_DATASET_ORIGIN_LINK",
            state=ClaimState.SUSPENDED,
            reason="dataset excerpt has no explicit source-origin map",
            evidence_refs=("origin-link:missing",),
        )
        return claim_a, claim_b, claim_c

    if not isinstance(origin_link, dict):
        raise CertificationSchemaError("origin_link must be object or null")

    source_id = str(origin_link.get("source_id", "")).strip()
    if source_id not in sources:
        claim_c = ClaimVerdict(
            claim_id="C_DATASET_ORIGIN_LINK",
            state=ClaimState.REFUSED,
            reason="origin link points to unknown source",
            evidence_refs=(f"origin-link:bad-source:{source_id}",),
        )
        return claim_a, claim_b, claim_c

    left_anchor = str(origin_link.get("left_anchor", ""))
    snippet = str(origin_link.get("snippet", ""))
    right_anchor = str(origin_link.get("right_anchor", ""))

    occ = _find_anchor_locked_occurrence(
        source_id=source_id,
        source_text=sources[source_id]["normalized_text"],
        left_anchor=left_anchor,
        snippet=snippet,
        right_anchor=right_anchor,
    )

    if occ is None:
        claim_c = ClaimVerdict(
            claim_id="C_DATASET_ORIGIN_LINK",
            state=ClaimState.REFUSED,
            reason="anchor-locked origin map is missing or non-unique",
            evidence_refs=(
                f"origin-link:{source_id}",
                f"left:{left_anchor}",
                f"right:{right_anchor}",
            ),
        )
    else:
        claim_c = ClaimVerdict(
            claim_id="C_DATASET_ORIGIN_LINK",
            state=ClaimState.PROVEN,
            reason="anchor-locked map resolved to one source position",
            evidence_refs=(
                f"occ:{occ.source_id}:{occ.byte_start}-{occ.byte_end}",
                f"source-sha256:{sources[source_id]['source_sha256']}",
            ),
        )

    return claim_a, claim_b, claim_c


def _derive_layers(
    *,
    case: dict[str, object],
    claims: tuple[ClaimVerdict, ClaimVerdict, ClaimVerdict],
) -> tuple[LayerVerdict, ...]:
    claim_map = {claim.claim_id: claim for claim in claims}
    layers: list[LayerVerdict] = []

    layers.append(
        LayerVerdict(
            layer_id="encoding_normalization",
            state=LayerState.LICENSED,
            reason="strict NFC normalization completed without lossy decode",
            evidence_refs=("normalization:STRICT_NFC_NO_LOSS",),
            dependencies=(),
            residuals=(),
        )
    )

    canonical = case.get("canonical116")
    if not isinstance(canonical, dict):
        raise CertificationSchemaError("case.canonical116 must be object")
    ready = bool(canonical.get("ready", False))
    unit_count = int(canonical.get("unit_count", 0))
    if ready and unit_count == 116:
        canonical_state = LayerState.LICENSED
        canonical_reason = "canonical116 representation accepted at unit-count boundary"
    else:
        canonical_state = LayerState.REFUSED
        canonical_reason = "canonical116 representation invalid (ready flag/unit_count mismatch)"

    layers.append(
        LayerVerdict(
            layer_id="canonical116_acceptance",
            state=canonical_state,
            reason=canonical_reason,
            evidence_refs=(f"canonical116:ready={ready}", f"canonical116:unit_count={unit_count}"),
            dependencies=("encoding_normalization",),
            residuals=("CANONICAL116_READY_NOT_WORD_LICENSE",),
        )
    )

    boundaries = case.get("boundaries")
    if not isinstance(boundaries, dict):
        raise CertificationSchemaError("case.boundaries must be object")
    wasl = str(boundaries.get("wasl", ""))
    waqf_claim = str(boundaries.get("waqf_performance_claim", ""))
    if wasl == "FORCED_TO_SYNTHETIC_TOKEN":
        seg_state = LayerState.REFUSED
        seg_reason = "wasl boundary requires synthetic token (forbidden)"
    elif waqf_claim != "NO_PERFORMANCE_CLAIM" and wasl == "STOP_AT_PERIOD":
        seg_state = LayerState.SUSPENDED
        seg_reason = "punctuation alone cannot prove claimed waqf performance"
    else:
        seg_state = LayerState.LICENSED
        seg_reason = "boundaries declared without synthetic continuation"

    layers.append(
        LayerVerdict(
            layer_id="segment_boundary_license",
            state=seg_state,
            reason=seg_reason,
            evidence_refs=(f"boundary:wasl={wasl}", f"boundary:waqf_claim={waqf_claim}"),
            dependencies=("encoding_normalization",),
            residuals=(),
        )
    )

    morphology = case.get("morphology")
    if not isinstance(morphology, dict):
        raise CertificationSchemaError("case.morphology must be object")
    target_word = str(case.get("target_word", "")).strip()
    root = str(morphology.get("root", "")).strip()
    stem = str(morphology.get("stem", "")).strip()
    weight = str(morphology.get("weight", "")).strip()
    i3rab = str(morphology.get("i3rab", "")).strip()
    tanween_role = str(morphology.get("tanween_role", "")).strip()
    evidence_refs = tuple(morphology.get("evidence_refs", ()))

    if not all([root, stem, weight, i3rab, tanween_role]) or not evidence_refs:
        morph_state = LayerState.SUSPENDED
        morph_reason = "morphological premise incomplete"
    elif any(mark in root for mark in ("ً", "ٌ", "ٍ")):
        morph_state = LayerState.REFUSED
        morph_reason = "root must not include tanween marks"
    elif "ٌ" in target_word and tanween_role in {"NONE", "UNKNOWN"}:
        morph_state = LayerState.REFUSED
        morph_reason = "tanween present in target but tanween role is unresolved"
    else:
        morph_state = LayerState.LICENSED
        morph_reason = "morphology accepted as evidence-backed candidate analysis"

    layers.append(
        LayerVerdict(
            layer_id="morphology_weight_analysis",
            state=morph_state,
            reason=morph_reason,
            evidence_refs=evidence_refs,
            dependencies=("canonical116_acceptance",),
            residuals=("SOURCE_HASH_NOT_MORPHOLOGY_PROOF",),
        )
    )

    syntax = case.get("syntax")
    if not isinstance(syntax, dict):
        raise CertificationSchemaError("case.syntax must be object")
    syntax_refs = tuple(syntax.get("evidence_refs", ()))
    if not syntax_refs:
        syntax_state = LayerState.SUSPENDED
        syntax_reason = "syntax evidence is missing"
    else:
        syntax_state = LayerState.LICENSED
        syntax_reason = "syntactic relation candidate is evidence-backed"

    layers.append(
        LayerVerdict(
            layer_id="syntax_relation_analysis",
            state=syntax_state,
            reason=syntax_reason,
            evidence_refs=syntax_refs,
            dependencies=("segment_boundary_license", "morphology_weight_analysis"),
            residuals=(),
        )
    )

    reference = case.get("reference")
    if not isinstance(reference, dict):
        raise CertificationSchemaError("case.reference must be object")
    reference_mode = str(reference.get("mode", "")).strip()
    reference_refs = tuple(reference.get("evidence_refs", ()))

    if claim_map["C_DATASET_ORIGIN_LINK"].state is not ClaimState.PROVEN:
        ref_state = LayerState.SUSPENDED
        ref_reason = "origin linkage unresolved; context transfer is blocked"
        ref_residuals = ("CONTEXT_TRANSFER_BLOCKED_BY_ORIGIN_GAP",)
    elif reference_mode == "UNPROVEN_DATASET_ADJACENCY":
        ref_state = LayerState.REFUSED
        ref_reason = "adjacent dataset lines are not accepted as source context proof"
        ref_residuals = ("UNTRUSTED_DATASET_ADJACENCY",)
    elif not reference_refs:
        ref_state = LayerState.SUSPENDED
        ref_reason = "reference evidence missing"
        ref_residuals = ("REFERENCE_EVIDENCE_MISSING",)
    else:
        ref_state = LayerState.LICENSED
        ref_reason = "textual reference resolved from proven source context"
        ref_residuals = ()

    layers.append(
        LayerVerdict(
            layer_id="textual_reference_resolution",
            state=ref_state,
            reason=ref_reason,
            evidence_refs=reference_refs,
            dependencies=("syntax_relation_analysis", "C_DATASET_ORIGIN_LINK"),
            residuals=ref_residuals,
        )
    )

    return tuple(layers)


def _derive_overall(layers: tuple[LayerVerdict, ...]) -> tuple[LayerState, str]:
    if any(layer.state is LayerState.REFUSED for layer in layers):
        return LayerState.REFUSED, "at least one mandatory layer is refused"
    if any(layer.state is LayerState.SUSPENDED for layer in layers):
        return LayerState.SUSPENDED, "at least one mandatory layer is suspended"
    return LayerState.LICENSED, "all mandatory layers are licensed"


def _build_transitions(
    *,
    case_id: str,
    claims: tuple[ClaimVerdict, ...],
    layers: tuple[LayerVerdict, ...],
    overall_state: LayerState,
) -> tuple[TransitionRecord, ...]:
    claim_map = {claim.claim_id: claim for claim in claims}
    layer_map = {layer.layer_id: layer for layer in layers}
    return (
        TransitionRecord(
            step_id=f"{case_id}:T1",
            input_ref="source_bytes",
            operation="strict_normalize",
            condition="NFC + no lossy decode",
            blocker=None,
            evidence_ref="normalization:STRICT_NFC_NO_LOSS",
            rank="ZERO",
            output_ref="normalized_text",
            dependencies=(),
            residuals=(),
        ),
        TransitionRecord(
            step_id=f"{case_id}:T2",
            input_ref="normalized_text",
            operation="locate_sentence_occurrences",
            condition="literal match in configured source set",
            blocker=(
                None
                if claim_map["A_PHRASE_EXISTS_IN_SOURCE"].state is ClaimState.PROVEN
                else "phrase-not-found"
            ),
            evidence_ref=claim_map["A_PHRASE_EXISTS_IN_SOURCE"].evidence_refs[0]
            if claim_map["A_PHRASE_EXISTS_IN_SOURCE"].evidence_refs
            else "occ:none",
            rank="ZERO",
            output_ref="occurrence_list",
            dependencies=("T1",),
            residuals=(),
        ),
        TransitionRecord(
            step_id=f"{case_id}:T3",
            input_ref="occurrence_list",
            operation="evaluate_claims_A_B_C",
            condition="C requires explicit origin map",
            blocker=(
                None
                if claim_map["C_DATASET_ORIGIN_LINK"].state is ClaimState.PROVEN
                else claim_map["C_DATASET_ORIGIN_LINK"].reason
            ),
            evidence_ref="claims:A_B_C",
            rank="ZERO",
            output_ref="claim_verdicts",
            dependencies=("T2",),
            residuals=("NO_C_FROM_A_OR_B",),
        ),
        TransitionRecord(
            step_id=f"{case_id}:T4",
            input_ref="canonical116_representation",
            operation="validate_unit_count",
            condition="ready=true and unit_count=116",
            blocker=(
                None
                if layer_map["canonical116_acceptance"].state is LayerState.LICENSED
                else layer_map["canonical116_acceptance"].reason
            ),
            evidence_ref="canonical116:boundary",
            rank="ZERO",
            output_ref="canonical116_layer",
            dependencies=("T1",),
            residuals=("CANONICAL116_READY_NOT_WORD_LICENSE",),
        ),
        TransitionRecord(
            step_id=f"{case_id}:T5",
            input_ref="token_boundaries",
            operation="boundary_license_check",
            condition="ibtida/wasl/waqf constraints",
            blocker=(
                None
                if layer_map["segment_boundary_license"].state is LayerState.LICENSED
                else layer_map["segment_boundary_license"].reason
            ),
            evidence_ref="boundary:declared",
            rank="ZERO",
            output_ref="boundary_layer",
            dependencies=("T1",),
            residuals=layer_map["segment_boundary_license"].residuals,
        ),
        TransitionRecord(
            step_id=f"{case_id}:T6",
            input_ref="morphology_claims",
            operation="evidence_backed_morphology_check",
            condition="root/stem/weight/i3rab/tanween role all explicit",
            blocker=(
                None
                if layer_map["morphology_weight_analysis"].state is LayerState.LICENSED
                else layer_map["morphology_weight_analysis"].reason
            ),
            evidence_ref="morphology:evidence-refs",
            rank="CANDIDATE",
            output_ref="morphology_layer",
            dependencies=("T4",),
            residuals=layer_map["morphology_weight_analysis"].residuals,
        ),
        TransitionRecord(
            step_id=f"{case_id}:T7",
            input_ref="syntax_claims",
            operation="relation_check",
            condition="jar/majrur + khabar + mubtada mapping",
            blocker=(
                None
                if layer_map["syntax_relation_analysis"].state is LayerState.LICENSED
                else layer_map["syntax_relation_analysis"].reason
            ),
            evidence_ref="syntax:evidence-refs",
            rank="CANDIDATE",
            output_ref="syntax_layer",
            dependencies=("T5", "T6"),
            residuals=(),
        ),
        TransitionRecord(
            step_id=f"{case_id}:T8",
            input_ref="reference_claims",
            operation="textual_reference_resolution",
            condition="requires proven origin link + source-context evidence",
            blocker=(
                None
                if layer_map["textual_reference_resolution"].state is LayerState.LICENSED
                else layer_map["textual_reference_resolution"].reason
            ),
            evidence_ref="reference:evidence-refs",
            rank="CANDIDATE",
            output_ref="word_in_context_verdict",
            dependencies=("T3", "T7"),
            residuals=layer_map["textual_reference_resolution"].residuals,
        ),
        TransitionRecord(
            step_id=f"{case_id}:T9",
            input_ref="layer_verdicts",
            operation="derive_overall_state",
            condition="all mandatory layers licensed",
            blocker=(
                None
                if overall_state is LayerState.LICENSED
                else "mandatory-layer-not-fully-licensed"
            ),
            evidence_ref=f"overall:{overall_state.value}",
            rank="CANDIDATE",
            output_ref="overall_contextual_license",
            dependencies=("T4", "T5", "T6", "T7", "T8"),
            residuals=(),
        ),
    )


def certify_case(
    case: dict[str, object],
    *,
    fixture_id: str,
    sources: dict[str, dict[str, str]],
    previous_audit_zip_found: tuple[str, ...],
) -> ContextualCertificate:
    sentence = _strict_normalize(str(case.get("sentence", "")))
    target_word = _strict_normalize(str(case.get("target_word", "")))
    if target_word not in sentence:
        raise CertificationSchemaError("target_word must be part of sentence")

    search_source_ids = case.get("search_sources")
    if not isinstance(search_source_ids, list) or not search_source_ids:
        raise CertificationSchemaError("case.search_sources must be non-empty list")

    search_occurrences: list[SourceOccurrence] = []
    for source_id in search_source_ids:
        key = str(source_id)
        if key not in sources:
            raise CertificationSchemaError(f"unknown source in search_sources: {key}")
        search_occurrences.extend(
            _find_occurrences(key, sources[key]["normalized_text"], sentence)
        )

    claims = _claims_for_case(
        case=case,
        sources=sources,
        search_occurrences=tuple(search_occurrences),
    )
    layers = _derive_layers(case=case, claims=claims)
    overall_state, overall_reason = _derive_overall(layers)
    transitions = _build_transitions(
        case_id=str(case.get("case_id", "")),
        claims=claims,
        layers=layers,
        overall_state=overall_state,
    )

    source_identities = tuple(
        {
            "source_id": source_id,
            "source_version": source["source_version"],
            "source_license": source["source_license"],
            "source_sha256": source["source_sha256"],
            "extraction_policy": source["extraction_policy"],
            "normalization_policy": source["normalization_policy"],
        }
        for source_id, source in sorted(sources.items())
    )

    return ContextualCertificate(
        fixture_id=fixture_id,
        case_id=str(case.get("case_id", "")),
        dataset_excerpt_id=str(case.get("dataset_excerpt_id", "")),
        domain_scope=str(case.get("domain_scope", "")),
        excluded_scope=tuple(str(item) for item in case.get("excluded_scope", ())),
        previous_audit_zip_found=previous_audit_zip_found,
        source_identities=source_identities,
        claims=claims,
        occurrences=tuple(search_occurrences),
        layers=layers,
        overall_state=overall_state,
        overall_reason=overall_reason,
        transitions=transitions,
    )


def load_fixture(path: Path) -> tuple[str, dict[str, dict[str, str]], list[dict[str, object]]]:
    body = json.loads(path.read_text(encoding="utf-8"))
    fixture_id = str(body.get("fixture_id", "")).strip()
    if not fixture_id:
        raise CertificationSchemaError("fixture_id is required")

    normalization_policy = str(body.get("normalization_policy", "")).strip()
    if not normalization_policy:
        raise CertificationSchemaError("normalization_policy is required")

    sources_raw = body.get("sources")
    if not isinstance(sources_raw, list) or not sources_raw:
        raise CertificationSchemaError("sources must be a non-empty list")

    sources: dict[str, dict[str, str]] = {}
    for item in sources_raw:
        if not isinstance(item, dict):
            raise CertificationSchemaError("source entries must be objects")
        source_id = str(item.get("source_id", "")).strip()
        source_version = str(item.get("source_version", "")).strip()
        source_license = str(item.get("source_license", "")).strip()
        extraction_policy = str(item.get("extraction_policy", "")).strip()
        text = _strict_normalize(str(item.get("text", "")))
        if not all((source_id, source_version, source_license, extraction_policy)):
            raise CertificationSchemaError("source metadata fields are required")
        sources[source_id] = {
            "source_id": source_id,
            "source_version": source_version,
            "source_license": source_license,
            "extraction_policy": extraction_policy,
            "normalization_policy": normalization_policy,
            "normalized_text": text,
            "source_sha256": _sha256_text(text),
            "position_map_sha256": _sha256_text(f"{source_id}:{text}"),
        }

    cases_raw = body.get("cases")
    if not isinstance(cases_raw, list) or not cases_raw:
        raise CertificationSchemaError("cases must be a non-empty list")
    cases: list[dict[str, object]] = []
    for case in cases_raw:
        if not isinstance(case, dict):
            raise CertificationSchemaError("case entries must be objects")
        cases.append(case)

    return fixture_id, sources, cases


def run_fixture(path: Path) -> tuple[ContextualCertificate, ...]:
    fixture_id, sources, cases = load_fixture(path)
    repo_root = path.resolve().parents[2]
    previous_audit_zip_found = _list_previous_audit_zip((repo_root, repo_root.parent))
    return tuple(
        certify_case(
            case,
            fixture_id=fixture_id,
            sources=sources,
            previous_audit_zip_found=previous_audit_zip_found,
        )
        for case in cases
    )


def certificate_to_dict(certificate: ContextualCertificate) -> dict[str, object]:
    return asdict(certificate)


def render_arabic_report(certificates: tuple[ContextualCertificate, ...]) -> str:
    lines: list[str] = []
    for cert in certificates:
        lines.append(f"الحالة: {cert.case_id} ({cert.dataset_excerpt_id})")
        lines.append(f"الحكم الإجمالي: {cert.overall_state.value} — {cert.overall_reason}")
        if cert.previous_audit_zip_found:
            lines.append(f"أرشيف التدقيق السابق: موجود ({len(cert.previous_audit_zip_found)})")
        else:
            lines.append("أرشيف التدقيق السابق: غير موجود في المسارات المفحوصة")
        lines.append("دعاوى الإثبات:")
        for claim in cert.claims:
            lines.append(f"- {claim.claim_id}: {claim.state.value} ({claim.reason})")
        lines.append("طبقات الحكم:")
        for layer in cert.layers:
            lines.append(f"- {layer.layer_id}: {layer.state.value} ({layer.reason})")
        lines.append("")
    return "\n".join(lines).strip()


def main() -> int:
    default_fixture = (
        Path(__file__).resolve().parents[3]
        / "data"
        / "contextual_evidence"
        / "canonical116_contextual_cases.json"
    )
    certs = run_fixture(default_fixture)
    payload = [certificate_to_dict(item) for item in certs]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\n=== Arabic Report ===")
    print(render_arabic_report(certs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
