from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

PROTOCOL_ID = "ARABIC-ORTHOGRAPHIC-COUNTING-PROTOCOL-1"
PROTOCOL_VERSION = "1.0.0"
DEFAULT_NORMALIZATION_POLICY = "NFC"

CARRIERS_29: tuple[str, ...] = (
    "ء",
    "ا",
    "ب",
    "ت",
    "ث",
    "ج",
    "ح",
    "خ",
    "د",
    "ذ",
    "ر",
    "ز",
    "س",
    "ش",
    "ص",
    "ض",
    "ط",
    "ظ",
    "ع",
    "غ",
    "ف",
    "ق",
    "ك",
    "ل",
    "م",
    "ن",
    "ه",
    "و",
    "ي",
)

FATHA = "\u064e"
DAMMA = "\u064f"
KASRA = "\u0650"
SUKUN = "\u0652"
SHADDA = "\u0651"
TANWIN = ("\u064b", "\u064c", "\u064d")
SHORT_HARAKAT = (FATHA, DAMMA, KASRA)

ARABIC_PRESENTATION_FORMS_RANGES = (
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
)

DIRECTIONAL_OR_LAYOUT_MARKS = {
    "\u200e",
    "\u200f",
    "\u202a",
    "\u202b",
    "\u202c",
    "\u202d",
    "\u202e",
    "\u2066",
    "\u2067",
    "\u2068",
    "\u2069",
    "\u0640",
    "\ufeff",
}


class OrthographicEligibilityState(StrEnum):
    READY = "READY"
    DEFER = "DEFER"
    REJECT = "REJECT"
    INVALID_ENCODING_OR_TYPE = "INVALID_ENCODING_OR_TYPE"
    INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class BoundaryScenario(StrEnum):
    IBTIDA = "IBTIDA"
    WASL = "WASL"
    WAQF = "WAQF"


class HarakaState(StrEnum):
    FATHA = "FATHA"
    DAMMA = "DAMMA"
    KASRA = "KASRA"
    SUKUN = "SUKUN"


@dataclass(frozen=True, slots=True)
class OrthographicRuleSpec:
    rule_id: str
    version: str
    source_ref: str
    applicability_conditions: tuple[str, ...]
    rule_input: str
    operation: str
    rule_output: str
    preserved_invariant: str
    blocker: str
    residual_when_blocked: str


@dataclass(frozen=True, slots=True)
class CountingProtocolRequest:
    source_id: str
    source_version: str
    source_bytes: bytes
    declared_encoding: str
    extraction_policy: str
    scenario: BoundaryScenario
    scope_label: str


@dataclass(frozen=True, slots=True)
class ByteNormalizationMap:
    original_text: str
    normalized_text: str
    normalization_policy: str
    unicode_version: str
    original_to_byte_offset: tuple[int, ...]
    normalized_to_original_char_index: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class OrthographicUnitCertificate:
    unit_id: str
    source_span_bytes: tuple[int, int]
    original_grapheme: str
    normalized_grapheme: str
    source_carrier: str
    projected_carrier: str | None
    role: str
    scenario: BoundaryScenario
    state: OrthographicEligibilityState
    haraka_state: HarakaState | None
    ready_for_count: bool
    atom_key: str | None
    reasons: tuple[str, ...]
    rule_ids: tuple[str, ...]
    input_output_trace: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrthographicCountingCertificate:
    protocol_id: str
    protocol_version: str
    source_id: str
    source_version: str
    source_sha256: str
    declared_encoding: str
    extraction_policy: str
    scenario: BoundaryScenario
    scope_label: str
    normalization: ByteNormalizationMap
    rules: tuple[OrthographicRuleSpec, ...]
    all_atom_keys_116: tuple[str, ...]
    atom_counts: dict[str, int]
    units: tuple[OrthographicUnitCertificate, ...]
    total_occurrences: int
    eligible_occurrences: int
    deferred_occurrences: int
    rejected_occurrences: int
    out_of_scope_occurrences: int
    count_eligible: bool
    certificate_sha256: str


@dataclass(frozen=True, slots=True)
class ProtocolRunResult:
    state: OrthographicEligibilityState
    certificate: OrthographicCountingCertificate | None
    reasons: tuple[str, ...]


def canonical_atom_keys_116() -> tuple[str, ...]:
    keys: list[str] = []
    for carrier in CARRIERS_29:
        for state in HarakaState:
            keys.append(f"AR116:{carrier}:{state.value}")
    return tuple(keys)


def count_atoms(request: CountingProtocolRequest) -> ProtocolRunResult:
    if not isinstance(request, CountingProtocolRequest):
        return ProtocolRunResult(
            state=OrthographicEligibilityState.INVALID_CONFIGURATION,
            certificate=None,
            reasons=("REQUEST_TYPE_INVALID",),
        )

    if not request.source_id.strip() or not request.source_version.strip() or not request.scope_label.strip():
        return ProtocolRunResult(
            state=OrthographicEligibilityState.INVALID_CONFIGURATION,
            certificate=None,
            reasons=("SOURCE_METADATA_MISSING",),
        )

    if request.declared_encoding.lower() not in {"utf-8", "utf8", "utf-8-sig"}:
        return ProtocolRunResult(
            state=OrthographicEligibilityState.OUT_OF_SCOPE,
            certificate=None,
            reasons=("ENCODING_OUT_OF_SCOPE",),
        )

    try:
        decoded = request.source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return ProtocolRunResult(
            state=OrthographicEligibilityState.INVALID_ENCODING_OR_TYPE,
            certificate=None,
            reasons=("STRICT_DECODE_FAILED",),
        )

    normalization = _build_normalization_map(decoded)
    source_sha = hashlib.sha256(request.source_bytes).hexdigest()
    rules = _rule_registry()
    atom_keys = canonical_atom_keys_116()
    counts = {key: 0 for key in atom_keys}

    units = _materialize_units(
        normalization=normalization,
        scenario=request.scenario,
        atom_keys=set(atom_keys),
    )

    for unit in units:
        if unit.ready_for_count and unit.atom_key is not None:
            counts[unit.atom_key] += 1

    total = len(units)
    eligible = sum(1 for u in units if u.ready_for_count)
    deferred = sum(1 for u in units if u.state is OrthographicEligibilityState.DEFER)
    rejected = sum(1 for u in units if u.state is OrthographicEligibilityState.REJECT)
    out_scope = sum(1 for u in units if u.state is OrthographicEligibilityState.OUT_OF_SCOPE)

    cert = OrthographicCountingCertificate(
        protocol_id=PROTOCOL_ID,
        protocol_version=PROTOCOL_VERSION,
        source_id=request.source_id,
        source_version=request.source_version,
        source_sha256=source_sha,
        declared_encoding="utf-8",
        extraction_policy=request.extraction_policy,
        scenario=request.scenario,
        scope_label=request.scope_label,
        normalization=normalization,
        rules=rules,
        all_atom_keys_116=atom_keys,
        atom_counts=counts,
        units=units,
        total_occurrences=total,
        eligible_occurrences=eligible,
        deferred_occurrences=deferred,
        rejected_occurrences=rejected,
        out_of_scope_occurrences=out_scope,
        count_eligible=eligible > 0,
        certificate_sha256="",
    )
    cert_hash = _certificate_hash(cert)
    cert = OrthographicCountingCertificate(
        protocol_id=cert.protocol_id,
        protocol_version=cert.protocol_version,
        source_id=cert.source_id,
        source_version=cert.source_version,
        source_sha256=cert.source_sha256,
        declared_encoding=cert.declared_encoding,
        extraction_policy=cert.extraction_policy,
        scenario=cert.scenario,
        scope_label=cert.scope_label,
        normalization=cert.normalization,
        rules=cert.rules,
        all_atom_keys_116=cert.all_atom_keys_116,
        atom_counts=cert.atom_counts,
        units=cert.units,
        total_occurrences=cert.total_occurrences,
        eligible_occurrences=cert.eligible_occurrences,
        deferred_occurrences=cert.deferred_occurrences,
        rejected_occurrences=cert.rejected_occurrences,
        out_of_scope_occurrences=cert.out_of_scope_occurrences,
        count_eligible=cert.count_eligible,
        certificate_sha256=cert_hash,
    )

    final_state = (
        OrthographicEligibilityState.READY
        if cert.eligible_occurrences > 0 and cert.deferred_occurrences == 0 and cert.rejected_occurrences == 0
        else OrthographicEligibilityState.DEFER
    )
    reasons = () if final_state is OrthographicEligibilityState.READY else ("PARTIAL_ELIGIBLE_COUNT_ONLY",)
    return ProtocolRunResult(state=final_state, certificate=cert, reasons=reasons)


def verify_certificate_integrity(certificate: OrthographicCountingCertificate) -> bool:
    if not isinstance(certificate, OrthographicCountingCertificate):
        return False
    return _certificate_hash(certificate) == certificate.certificate_sha256


def _build_normalization_map(text: str) -> ByteNormalizationMap:
    normalized_parts: list[str] = []
    normalized_to_original: list[int] = []
    for idx, ch in enumerate(text):
        n = unicodedata.normalize(DEFAULT_NORMALIZATION_POLICY, ch)
        normalized_parts.append(n)
        normalized_to_original.extend([idx] * len(n))
    normalized_text = "".join(normalized_parts)

    offsets = [0]
    total = 0
    for ch in text:
        total += len(ch.encode("utf-8"))
        offsets.append(total)

    return ByteNormalizationMap(
        original_text=text,
        normalized_text=normalized_text,
        normalization_policy=DEFAULT_NORMALIZATION_POLICY,
        unicode_version=unicodedata.unidata_version,
        original_to_byte_offset=tuple(offsets),
        normalized_to_original_char_index=tuple(normalized_to_original),
    )


def _segment_graphemes(text: str) -> list[tuple[int, str]]:
    chunks: list[tuple[int, str]] = []
    current = ""
    start = 0
    for idx, ch in enumerate(text):
        if not current:
            current = ch
            start = idx
            continue
        if unicodedata.combining(ch):
            current += ch
            continue
        chunks.append((start, current))
        current = ch
        start = idx
    if current:
        chunks.append((start, current))
    return chunks


def _materialize_units(
    *,
    normalization: ByteNormalizationMap,
    scenario: BoundaryScenario,
    atom_keys: set[str],
) -> tuple[OrthographicUnitCertificate, ...]:
    units: list[OrthographicUnitCertificate] = []
    graphemes = _segment_graphemes(normalization.normalized_text)
    unit_seq = 0

    for start_idx, grapheme in graphemes:
        base = grapheme[0]
        marks = grapheme[1:]
        byte_span = _grapheme_byte_span(normalization, start_idx, len(grapheme))

        if base.isspace() or unicodedata.category(base).startswith("P"):
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    None,
                    "NON_LETTER_BOUNDARY",
                    scenario,
                    OrthographicEligibilityState.OUT_OF_SCOPE,
                    None,
                    False,
                    None,
                    ("NON_ARABIC_LETTER_OR_PUNCTUATION",),
                    (),
                    ("source->ignored",),
                )
            )
            unit_seq += 1
            continue

        if base in DIRECTIONAL_OR_LAYOUT_MARKS:
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    None,
                    "LAYOUT_OR_DIRECTION_MARK",
                    scenario,
                    OrthographicEligibilityState.OUT_OF_SCOPE,
                    None,
                    False,
                    None,
                    ("LAYOUT_MARK_EXCLUDED",),
                    ("R-DIRECTION",),
                    ("source->excluded",),
                )
            )
            unit_seq += 1
            continue

        if _is_presentation_form(base):
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    None,
                    "PRESENTATION_FORM_FORBIDDEN",
                    scenario,
                    OrthographicEligibilityState.REJECT,
                    None,
                    False,
                    None,
                    ("PRESENTATION_FORM_REJECTED",),
                    ("R-PRESENTATION",),
                    ("source->rejected",),
                )
            )
            unit_seq += 1
            continue

        if base == "ٱ" and scenario is BoundaryScenario.WASL:
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    None,
                    "HAMZAT_WASL_DROPPED",
                    scenario,
                    OrthographicEligibilityState.OUT_OF_SCOPE,
                    None,
                    False,
                    None,
                    ("HAMZAT_WASL_DROPPED_IN_WASL",),
                    ("R-HAMZAT-WASL",),
                    ("source->zero-output",),
                )
            )
            unit_seq += 1
            continue

        projected_carrier, role, role_rule_ids = _project_carrier(base, scenario)
        if projected_carrier is None:
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    None,
                    role,
                    scenario,
                    OrthographicEligibilityState.REJECT,
                    None,
                    False,
                    None,
                    ("UNSUPPORTED_CARRIER",),
                    role_rule_ids,
                    ("source->rejected",),
                )
            )
            unit_seq += 1
            continue

        shadda_present = SHADDA in marks
        tanwin_present = any(mark in TANWIN for mark in marks)
        sukun_present = SUKUN in marks
        short_marks = tuple(mark for mark in marks if mark in SHORT_HARAKAT)

        if tanwin_present:
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    projected_carrier,
                    role,
                    scenario,
                    OrthographicEligibilityState.DEFER,
                    None,
                    False,
                    None,
                    ("TANWIN_FUNCTIONAL_ROLE_UNRESOLVED",),
                    role_rule_ids + ("R-TANWIN",),
                    ("source->deferred",),
                )
            )
            unit_seq += 1
            continue

        if len(short_marks) > 1 or (sukun_present and short_marks):
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    projected_carrier,
                    role,
                    scenario,
                    OrthographicEligibilityState.REJECT,
                    None,
                    False,
                    None,
                    ("CONFLICTING_DIACRITIC_MARKS",),
                    role_rule_ids + ("R-DIACRITIC-CONFLICT",),
                    ("source->rejected",),
                )
            )
            unit_seq += 1
            continue

        if shadda_present:
            first_state = HarakaState.SUKUN
            first_atom = f"AR116:{projected_carrier}:{first_state.value}"
            units.append(
                _unit(
                    unit_seq,
                    byte_span,
                    grapheme,
                    grapheme,
                    base,
                    projected_carrier,
                    f"{role}:SHADDA_PART_1",
                    scenario,
                    OrthographicEligibilityState.READY,
                    first_state,
                    first_atom in atom_keys,
                    first_atom if first_atom in atom_keys else None,
                    (),
                    role_rule_ids + ("R-SHADDA-BRIDGE",),
                    ("source->unit[0]",),
                )
            )
            unit_seq += 1

            second = _ready_or_deferred_for_mark(
                unit_id=unit_seq,
                byte_span=byte_span,
                grapheme=grapheme,
                base=base,
                projected_carrier=projected_carrier,
                role=f"{role}:SHADDA_PART_2",
                scenario=scenario,
                mark=short_marks[0] if short_marks else "",
                extra_rule_ids=role_rule_ids + ("R-SHADDA-BRIDGE",),
                atom_keys=atom_keys,
            )
            units.append(second)
            unit_seq += 1
            continue

        mark = ""
        if sukun_present:
            mark = SUKUN
        elif short_marks:
            mark = short_marks[0]

        units.append(
            _ready_or_deferred_for_mark(
                unit_id=unit_seq,
                byte_span=byte_span,
                grapheme=grapheme,
                base=base,
                projected_carrier=projected_carrier,
                role=role,
                scenario=scenario,
                mark=mark,
                extra_rule_ids=role_rule_ids,
                atom_keys=atom_keys,
            )
        )
        unit_seq += 1

    return tuple(units)


def _ready_or_deferred_for_mark(
    *,
    unit_id: int,
    byte_span: tuple[int, int],
    grapheme: str,
    base: str,
    projected_carrier: str,
    role: str,
    scenario: BoundaryScenario,
    mark: str,
    extra_rule_ids: tuple[str, ...],
    atom_keys: set[str],
) -> OrthographicUnitCertificate:
    if not mark:
        return _unit(
            unit_id,
            byte_span,
            grapheme,
            grapheme,
            base,
            projected_carrier,
            role,
            scenario,
            OrthographicEligibilityState.DEFER,
            None,
            False,
            None,
            ("HARAKA_MISSING_NOT_EQUIVALENT_TO_SUKUN",),
            extra_rule_ids,
            ("source->deferred",),
        )

    if projected_carrier == "ا" and mark in SHORT_HARAKAT:
        return _unit(
            unit_id,
            byte_span,
            grapheme,
            grapheme,
            base,
            projected_carrier,
            role,
            scenario,
            OrthographicEligibilityState.DEFER,
            None,
            False,
            None,
            ("ALIF_WITH_SHORT_HARAKA_NOT_AUTO_MADD",),
            extra_rule_ids + ("R-ALIF-HARAKA",),
            ("source->deferred",),
        )

    state = _state_from_mark(mark)
    if state is None:
        return _unit(
            unit_id,
            byte_span,
            grapheme,
            grapheme,
            base,
            projected_carrier,
            role,
            scenario,
            OrthographicEligibilityState.REJECT,
            None,
            False,
            None,
            ("UNSUPPORTED_MARK",),
            extra_rule_ids,
            ("source->rejected",),
        )

    atom_key = f"AR116:{projected_carrier}:{state.value}"
    ready = atom_key in atom_keys
    return _unit(
        unit_id,
        byte_span,
        grapheme,
        grapheme,
        base,
        projected_carrier,
        role,
        scenario,
        OrthographicEligibilityState.READY if ready else OrthographicEligibilityState.REJECT,
        state,
        ready,
        atom_key if ready else None,
        () if ready else ("ATOM_KEY_NOT_REGISTERED",),
        extra_rule_ids,
        ("source->unit",),
    )


def _project_carrier(base: str, scenario: BoundaryScenario) -> tuple[str | None, str, tuple[str, ...]]:
    if base in CARRIERS_29:
        return base, "DIRECT_CARRIER", ("R-DIRECT",)
    if base in {"أ", "إ", "آ", "ٱ"}:
        return "ا", "HAMZA_ON_ALIF", ("R-HAMZA-SEAT",)
    if base == "ؤ":
        return "و", "HAMZA_ON_WAW", ("R-HAMZA-SEAT",)
    if base == "ئ":
        return "ي", "HAMZA_ON_YA", ("R-HAMZA-SEAT",)
    if base == "ة":
        if scenario is BoundaryScenario.WAQF:
            return "ه", "TA_MARBUTA_WAQF_HA", ("R-TA-MARBUTA",)
        return "ت", "TA_MARBUTA_LINKED_TA", ("R-TA-MARBUTA",)
    if base == "ى":
        return "ا", "ALIF_MAQSURA", ("R-ALIF-MAQSURA",)
    return None, "UNMAPPED_CARRIER", ()


def _state_from_mark(mark: str) -> HarakaState | None:
    if mark == FATHA:
        return HarakaState.FATHA
    if mark == DAMMA:
        return HarakaState.DAMMA
    if mark == KASRA:
        return HarakaState.KASRA
    if mark == SUKUN:
        return HarakaState.SUKUN
    return None


def _grapheme_byte_span(
    normalization: ByteNormalizationMap,
    start_idx: int,
    length: int,
) -> tuple[int, int]:
    original_indices = normalization.normalized_to_original_char_index[start_idx : start_idx + length]
    if not original_indices:
        return (0, 0)
    first = min(original_indices)
    last = max(original_indices) + 1
    return (
        normalization.original_to_byte_offset[first],
        normalization.original_to_byte_offset[last],
    )


def _is_presentation_form(ch: str) -> bool:
    cp = ord(ch)
    return any(start <= cp <= end for start, end in ARABIC_PRESENTATION_FORMS_RANGES)


def _unit(
    unit_id: int,
    byte_span: tuple[int, int],
    original_grapheme: str,
    normalized_grapheme: str,
    source_carrier: str,
    projected_carrier: str | None,
    role: str,
    scenario: BoundaryScenario,
    state: OrthographicEligibilityState,
    haraka_state: HarakaState | None,
    ready: bool,
    atom_key: str | None,
    reasons: tuple[str, ...],
    rule_ids: tuple[str, ...],
    trace: tuple[str, ...],
) -> OrthographicUnitCertificate:
    return OrthographicUnitCertificate(
        unit_id=f"unit://{unit_id}",
        source_span_bytes=byte_span,
        original_grapheme=original_grapheme,
        normalized_grapheme=normalized_grapheme,
        source_carrier=source_carrier,
        projected_carrier=projected_carrier,
        role=role,
        scenario=scenario,
        state=state,
        haraka_state=haraka_state,
        ready_for_count=ready,
        atom_key=atom_key,
        reasons=reasons,
        rule_ids=rule_ids,
        input_output_trace=trace,
    )


def _rule_registry() -> tuple[OrthographicRuleSpec, ...]:
    return (
        OrthographicRuleSpec(
            rule_id="R-HAMZA-SEAT",
            version="1.0.0",
            source_ref="docs/20_PRE_WEIGHT_LICENSING_LAW.md",
            applicability_conditions=("hamza-seat-observed",),
            rule_input="hamza_graphic",
            operation="project_to_carrier_with_identity_preservation",
            rule_output="carrier_projection_with_hamza_role",
            preserved_invariant="source_hamza_identity_preserved",
            blocker="seat_not_mapped",
            residual_when_blocked="HAMZA_SEAT_UNMAPPED",
        ),
        OrthographicRuleSpec(
            rule_id="R-TA-MARBUTA",
            version="1.0.0",
            source_ref="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
            applicability_conditions=("ta_marbuta_observed", "boundary_scenario_declared"),
            rule_input="ta_marbuta_graphic",
            operation="scenario_projection",
            rule_output="linked_ta_or_waqf_ha",
            preserved_invariant="source_ta_marbuta_identity_preserved",
            blocker="boundary_scenario_missing",
            residual_when_blocked="TA_MARBUTA_SCENARIO_UNRESOLVED",
        ),
        OrthographicRuleSpec(
            rule_id="R-HAMZAT-WASL",
            version="1.0.0",
            source_ref="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
            applicability_conditions=("hamzat_wasl_observed", "scenario_declared"),
            rule_input="hamzat_wasl_graphic",
            operation="ibtida_wasl_projection",
            rule_output="emit_or_drop_with_trace",
            preserved_invariant="source_span_traced",
            blocker="scenario_missing",
            residual_when_blocked="HAMZAT_WASL_SCENARIO_UNRESOLVED",
        ),
        OrthographicRuleSpec(
            rule_id="R-SHADDA-BRIDGE",
            version="1.0.0",
            source_ref="docs/20_PRE_WEIGHT_LICENSING_LAW.md",
            applicability_conditions=("shadda_mark_present",),
            rule_input="single_grapheme_with_shadda",
            operation="bridge_to_two_units",
            rule_output="geminated_pair",
            preserved_invariant="byte_span_preserved",
            blocker="diacritic_conflict",
            residual_when_blocked="SHADDA_CONFLICT",
        ),
        OrthographicRuleSpec(
            rule_id="R-TANWIN",
            version="1.0.0",
            source_ref="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
            applicability_conditions=("tanwin_mark_present",),
            rule_input="tanwin_mark",
            operation="separate_graphic_from_functional_role",
            rule_output="deferred_until_boundary_role_resolution",
            preserved_invariant="source_mark_preserved",
            blocker="functional_role_unresolved",
            residual_when_blocked="TANWIN_FUNCTIONAL_ROLE_UNRESOLVED",
        ),
        OrthographicRuleSpec(
            rule_id="R-ALIF-HARAKA",
            version="1.0.0",
            source_ref="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
            applicability_conditions=("alif_with_short_haraka",),
            rule_input="alif_plus_short_haraka",
            operation="block_auto_madd_license",
            rule_output="deferred_symbolic_carrier",
            preserved_invariant="unicode_validity_kept_distinct_from_role_license",
            blocker="role_not_proven",
            residual_when_blocked="ALIF_WITH_SHORT_HARAKA_NOT_AUTO_MADD",
        ),
        OrthographicRuleSpec(
            rule_id="R-PRESENTATION",
            version="1.0.0",
            source_ref="docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md",
            applicability_conditions=("presentation_form_detected",),
            rule_input="arabic_presentation_form",
            operation="reject_display_form_in_counting_protocol",
            rule_output="rejected_unit",
            preserved_invariant="original_bytes_preserved",
            blocker="none",
            residual_when_blocked="PRESENTATION_FORM_REJECTED",
        ),
        OrthographicRuleSpec(
            rule_id="R-DIACRITIC-CONFLICT",
            version="1.0.0",
            source_ref="docs/20_PRE_WEIGHT_LICENSING_LAW.md",
            applicability_conditions=("multiple_conflicting_marks",),
            rule_input="conflicting_haraka_marks",
            operation="reject_conflicting_mark_sequence",
            rule_output="rejected_unit",
            preserved_invariant="trace_visible",
            blocker="conflict_present",
            residual_when_blocked="CONFLICTING_DIACRITIC_MARKS",
        ),
        OrthographicRuleSpec(
            rule_id="R-DIRECTION",
            version="1.0.0",
            source_ref="docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md",
            applicability_conditions=("layout_or_direction_mark_detected",),
            rule_input="layout_mark",
            operation="exclude_from_orthographic_atoms",
            rule_output="out_of_scope_unit",
            preserved_invariant="source_bytes_and_offsets_preserved",
            blocker="none",
            residual_when_blocked="LAYOUT_MARK_EXCLUDED",
        ),
        OrthographicRuleSpec(
            rule_id="R-ALIF-MAQSURA",
            version="1.0.0",
            source_ref="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
            applicability_conditions=("alif_maqsura_observed",),
            rule_input="alif_maqsura_graphic",
            operation="project_symbolic_carrier",
            rule_output="carrier_projection",
            preserved_invariant="source_identity_preserved",
            blocker="role_unresolved",
            residual_when_blocked="ALIF_MAQSURA_ROLE_UNRESOLVED",
        ),
        OrthographicRuleSpec(
            rule_id="R-DIRECT",
            version="1.0.0",
            source_ref="docs/20_PRE_WEIGHT_LICENSING_LAW.md",
            applicability_conditions=("direct_carrier_member",),
            rule_input="carrier_grapheme",
            operation="direct_carrier_projection",
            rule_output="projected_carrier",
            preserved_invariant="source_span_preserved",
            blocker="none",
            residual_when_blocked="UNSUPPORTED_CARRIER",
        ),
    )


def _certificate_hash(certificate: OrthographicCountingCertificate) -> str:
    payload = {
        "protocol_id": certificate.protocol_id,
        "protocol_version": certificate.protocol_version,
        "source_id": certificate.source_id,
        "source_version": certificate.source_version,
        "source_sha256": certificate.source_sha256,
        "declared_encoding": certificate.declared_encoding,
        "extraction_policy": certificate.extraction_policy,
        "scenario": certificate.scenario.value,
        "scope_label": certificate.scope_label,
        "normalization": {
            "original_text": certificate.normalization.original_text,
            "normalized_text": certificate.normalization.normalized_text,
            "normalization_policy": certificate.normalization.normalization_policy,
            "unicode_version": certificate.normalization.unicode_version,
            "original_to_byte_offset": certificate.normalization.original_to_byte_offset,
            "normalized_to_original_char_index": (
                certificate.normalization.normalized_to_original_char_index
            ),
        },
        "rules": [rule.__dict__ for rule in certificate.rules],
        "all_atom_keys_116": certificate.all_atom_keys_116,
        "atom_counts": certificate.atom_counts,
        "units": [
            {
                "unit_id": unit.unit_id,
                "source_span_bytes": unit.source_span_bytes,
                "original_grapheme": unit.original_grapheme,
                "normalized_grapheme": unit.normalized_grapheme,
                "source_carrier": unit.source_carrier,
                "projected_carrier": unit.projected_carrier,
                "role": unit.role,
                "scenario": unit.scenario.value,
                "state": unit.state.value,
                "haraka_state": unit.haraka_state.value if unit.haraka_state is not None else None,
                "ready_for_count": unit.ready_for_count,
                "atom_key": unit.atom_key,
                "reasons": unit.reasons,
                "rule_ids": unit.rule_ids,
                "input_output_trace": unit.input_output_trace,
            }
            for unit in certificate.units
        ],
        "total_occurrences": certificate.total_occurrences,
        "eligible_occurrences": certificate.eligible_occurrences,
        "deferred_occurrences": certificate.deferred_occurrences,
        "rejected_occurrences": certificate.rejected_occurrences,
        "out_of_scope_occurrences": certificate.out_of_scope_occurrences,
        "count_eligible": certificate.count_eligible,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


__all__ = [
    "PROTOCOL_ID",
    "PROTOCOL_VERSION",
    "CARRIERS_29",
    "BoundaryScenario",
    "ByteNormalizationMap",
    "CountingProtocolRequest",
    "HarakaState",
    "OrthographicCountingCertificate",
    "OrthographicEligibilityState",
    "OrthographicRuleSpec",
    "OrthographicUnitCertificate",
    "ProtocolRunResult",
    "canonical_atom_keys_116",
    "count_atoms",
    "verify_certificate_integrity",
]
