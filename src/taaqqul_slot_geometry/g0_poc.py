"""Short PoC runtime for a law-certified G₀ classifier and explanation card.

This module is an industrial prototype surface that keeps all decisions traceable,
residual-visible, and law-bound. It does not issue hukm, truth, or authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


class G0PoCSchemaError(TypeError):
    """Raised when PoC inputs or stores are malformed."""


class AnalysisAxis(StrEnum):
    """Tri-axis router labels for signifier, signified, and coupled routes."""

    DAL = "𝔇"
    MADLUL = "𝔐"
    COUPLED = "𝔚"


class AnalysisPath(StrEnum):
    """Licensed short PoC route labels."""

    G0 = "G0"
    M0 = "M0"
    D0 = "D0"
    K0 = "K0"
    X0 = "X0"


class DecisionState(StrEnum):
    """Unified analysis-card decisions (presentation labels, never hukm/truth/authority)."""

    LICENSED = "مرخّص"
    REFUSED = "مرفوض"
    DEFERRED = "معلّق"
    ROUTED = "محوّل"


class BoundaryStatus(StrEnum):
    """Ontology boundary status used by the short PoC admissibility guard."""

    G0_ADMISSIBLE = "G0_ADMISSIBLE"
    ROUTE_ONLY = "ROUTE_ONLY"
    DEFERRED_ONLY = "DEFERRED_ONLY"
    TEST_SENTINEL = "TEST_SENTINEL"


NO_PREVENTER = "NONE"
LAW_UNRESOLVED = "LAW-UNRESOLVED"
LAW_UNBOUND = "LAW-UNBOUND"
LAW_ROUTE_FALLBACK = "LAW-ROUTE"
ONTOLOGY_KEY_UNRESOLVED = "ONTOLOGY_KEY_UNRESOLVED"
G0_ONTOLOGY_NOT_ADMISSIBLE = "G0_ONTOLOGY_NOT_ADMISSIBLE"
_SYNTHETIC_PREVENTERS: frozenset[str] = frozenset(
    {
        NO_PREVENTER,
        "NO_WITNESS",
        "G0_SCOPE_ONLY",
        "LAW_REGISTRY_GAP",
        "CONFLICTING_TOP_LAWS",
        ONTOLOGY_KEY_UNRESOLVED,
        G0_ONTOLOGY_NOT_ADMISSIBLE,
    }
)


def _validate_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str):
        raise G0PoCSchemaError(f"{cls_name}.{field} must be a string")
    if not value.strip():
        raise G0PoCSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _validate_int_range(cls_name: str, field: str, value: object, *, low: int, high: int) -> None:
    if not isinstance(value, int) or value < low or value > high:
        raise G0PoCSchemaError(f"{cls_name}.{field} must be an int in [{low}, {high}]")


def _validate_tuple_of_nonempty_strings(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise G0PoCSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise G0PoCSchemaError(f"{cls_name}.{field} must contain non-empty strings")


@dataclass(frozen=True, slots=True)
class LawRecord:
    """Single law-row in the PoC registry."""

    law_id: str
    origin: str
    axis: AnalysisAxis
    path: AnalysisPath
    decision_hint: DecisionState
    condition: str
    preventer: str
    decisive_difference: str
    evidence_rank: int
    priority: int
    required_tags: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "law_id", self.law_id)
        _validate_nonempty_str(cls, "origin", self.origin)
        if not isinstance(self.axis, AnalysisAxis):
            raise G0PoCSchemaError(f"{cls}.axis must be AnalysisAxis")
        if not isinstance(self.path, AnalysisPath):
            raise G0PoCSchemaError(f"{cls}.path must be AnalysisPath")
        if not isinstance(self.decision_hint, DecisionState):
            raise G0PoCSchemaError(f"{cls}.decision_hint must be DecisionState")
        _validate_nonempty_str(cls, "condition", self.condition)
        _validate_nonempty_str(cls, "preventer", self.preventer)
        _validate_nonempty_str(cls, "decisive_difference", self.decisive_difference)
        _validate_int_range(cls, "evidence_rank", self.evidence_rank, low=1, high=5)
        _validate_int_range(cls, "priority", self.priority, low=1, high=10)
        _validate_tuple_of_nonempty_strings(cls, "required_tags", self.required_tags)


@dataclass(frozen=True, slots=True)
class LexicalEvidence:
    """Lexical evidence row used by router + rule engine."""

    token: str
    witness: str
    axis: AnalysisAxis
    path: AnalysisPath
    evidence_rank: int
    tags: tuple[str, ...]
    ontology_key: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "token", self.token)
        _validate_nonempty_str(cls, "witness", self.witness)
        if not isinstance(self.axis, AnalysisAxis):
            raise G0PoCSchemaError(f"{cls}.axis must be AnalysisAxis")
        if not isinstance(self.path, AnalysisPath):
            raise G0PoCSchemaError(f"{cls}.path must be AnalysisPath")
        _validate_int_range(cls, "evidence_rank", self.evidence_rank, low=1, high=5)
        _validate_tuple_of_nonempty_strings(cls, "tags", self.tags)
        _validate_nonempty_str(cls, "ontology_key", self.ontology_key)


@dataclass(frozen=True, slots=True)
class OntologyNode:
    """Operational ontology row for PoC explanation."""

    key: str
    path: AnalysisPath
    genus: str
    boundary_status: BoundaryStatus
    allowed_predicates: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "key", self.key)
        if not isinstance(self.path, AnalysisPath):
            raise G0PoCSchemaError(f"{cls}.path must be AnalysisPath")
        _validate_nonempty_str(cls, "genus", self.genus)
        if not isinstance(self.boundary_status, BoundaryStatus):
            raise G0PoCSchemaError(f"{cls}.boundary_status must be BoundaryStatus")
        _validate_tuple_of_nonempty_strings(cls, "allowed_predicates", self.allowed_predicates)


@dataclass(frozen=True, slots=True)
class AnalysisTrace:
    """Trace payload attached to every analysis card."""

    trace_ref: str
    routed_axis: AnalysisAxis
    routed_path: AnalysisPath
    selected_laws: tuple[str, ...]
    reason: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "trace_ref", self.trace_ref)
        if not self.trace_ref.startswith("trace://"):
            raise G0PoCSchemaError(f"{cls}.trace_ref must start with 'trace://'")
        if not isinstance(self.routed_axis, AnalysisAxis):
            raise G0PoCSchemaError(f"{cls}.routed_axis must be AnalysisAxis")
        if not isinstance(self.routed_path, AnalysisPath):
            raise G0PoCSchemaError(f"{cls}.routed_path must be AnalysisPath")
        _validate_tuple_of_nonempty_strings(cls, "selected_laws", self.selected_laws)
        _validate_nonempty_str(cls, "reason", self.reason)


@dataclass(frozen=True, slots=True)
class AnalysisCard:
    """Unified output card for the PoC analyzer."""

    token: str
    axis: AnalysisAxis
    path: AnalysisPath
    decision: DecisionState
    law_ids: tuple[str, ...]
    preventer: str
    residuals: tuple[str, ...]
    trace: AnalysisTrace
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "token", self.token)
        if not isinstance(self.axis, AnalysisAxis):
            raise G0PoCSchemaError(f"{cls}.axis must be AnalysisAxis")
        if not isinstance(self.path, AnalysisPath):
            raise G0PoCSchemaError(f"{cls}.path must be AnalysisPath")
        if not isinstance(self.decision, DecisionState):
            raise G0PoCSchemaError(f"{cls}.decision must be DecisionState")
        _validate_tuple_of_nonempty_strings(cls, "law_ids", self.law_ids)
        _validate_nonempty_str(cls, "preventer", self.preventer)
        _validate_tuple_of_nonempty_strings(cls, "residuals", self.residuals)
        if not isinstance(self.trace, AnalysisTrace):
            raise G0PoCSchemaError(f"{cls}.trace must be AnalysisTrace")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0PoCSchemaError(f"{cls}.failure_code must be FailureCode or None")


@dataclass(frozen=True, slots=True)
class G0PoCStores:
    """Loaded law/lexicon/ontology stores for the short PoC."""

    laws: tuple[LawRecord, ...]
    lexical: tuple[LexicalEvidence, ...]
    ontology: tuple[OntologyNode, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.laws, tuple) or not self.laws:
            raise G0PoCSchemaError(f"{cls}.laws must be a non-empty tuple")
        if not isinstance(self.lexical, tuple) or not self.lexical:
            raise G0PoCSchemaError(f"{cls}.lexical must be a non-empty tuple")
        if not isinstance(self.ontology, tuple) or not self.ontology:
            raise G0PoCSchemaError(f"{cls}.ontology must be a non-empty tuple")


@dataclass(frozen=True, slots=True)
class EvaluationSample:
    """Expected outcome row for measurable PoC evaluation."""

    token: str
    expected_decision: DecisionState

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _validate_nonempty_str(cls, "token", self.token)
        if not isinstance(self.expected_decision, DecisionState):
            raise G0PoCSchemaError(f"{cls}.expected_decision must be DecisionState")


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    """Compact measurable report for phase-4 verification."""

    total: int
    accuracy: float
    correct_refusal_rate: float
    deferred_rate: float
    trace_completeness_rate: float
    coverage: tuple[tuple[str, int], ...]
    gap_tokens: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GoNoGoDecision:
    """Final transition decision after evaluation."""

    verdict: str
    reasons: tuple[str, ...]


def _json_rows(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise G0PoCSchemaError(f"{path} must contain a top-level JSON list")
    rows: list[dict[str, object]] = []
    for row in payload:
        if not isinstance(row, dict):
            raise G0PoCSchemaError(f"{path} rows must be JSON objects")
        rows.append(row)
    return rows


def _store_dir(base_path: str | Path | None) -> Path:
    if base_path is None:
        return Path(__file__).resolve().parents[2] / "data"
    return Path(base_path)


def load_g0_poc_stores(base_path: str | Path | None = None) -> G0PoCStores:
    """Load PoC stores from JSON files in ``data/`` (or a custom directory)."""

    store_dir = _store_dir(base_path)
    laws = tuple(
        LawRecord(
            law_id=str(row["law_id"]),
            origin=str(row["origin"]),
            axis=AnalysisAxis(str(row["axis"])),
            path=AnalysisPath(str(row["path"])),
            decision_hint=DecisionState(str(row["decision_hint"])),
            condition=str(row["condition"]),
            preventer=str(row["preventer"]),
            decisive_difference=str(row["decisive_difference"]),
            evidence_rank=int(row["evidence_rank"]),
            priority=int(row["priority"]),
            required_tags=tuple(str(v) for v in row["required_tags"]),
        )
        for row in _json_rows(store_dir / "g0_poc_law_registry.json")
    )
    lexical = tuple(
        LexicalEvidence(
            token=str(row["token"]),
            witness=str(row["witness"]),
            axis=AnalysisAxis(str(row["axis"])),
            path=AnalysisPath(str(row["path"])),
            evidence_rank=int(row["evidence_rank"]),
            tags=tuple(str(v) for v in row["tags"]),
            ontology_key=str(row["ontology_key"]),
        )
        for row in _json_rows(store_dir / "g0_poc_lexical_evidence.json")
    )
    ontology = tuple(
        OntologyNode(
            key=str(row["key"]),
            path=AnalysisPath(str(row["path"])),
            genus=str(row["genus"]),
            boundary_status=BoundaryStatus(str(row["boundary_status"])),
            allowed_predicates=tuple(str(v) for v in row["allowed_predicates"]),
        )
        for row in _json_rows(store_dir / "g0_poc_ontology_store.json")
    )
    known_ontology_keys = {node.key for node in ontology}
    unresolved_ontology_keys = sorted(
        {row.ontology_key for row in lexical if row.ontology_key not in known_ontology_keys}
    )
    if unresolved_ontology_keys:
        raise G0PoCSchemaError(
            "unresolved ontology_key entries in lexical evidence: "
            + ", ".join(unresolved_ontology_keys)
        )
    return G0PoCStores(laws=laws, lexical=lexical, ontology=ontology)


def declared_preventer_enum(stores: G0PoCStores) -> frozenset[str]:
    """Return the declared analysis-card preventer vocabulary."""

    return frozenset(law.preventer for law in stores.laws) | _SYNTHETIC_PREVENTERS


def _normalize_token(token: str) -> str:
    return " ".join(token.strip().split())


def _token_rows(token: str, stores: G0PoCStores) -> tuple[LexicalEvidence, ...]:
    norm = _normalize_token(token)
    return tuple(row for row in stores.lexical if row.token == norm)


def _matching_laws(row: LexicalEvidence, stores: G0PoCStores) -> tuple[LawRecord, ...]:
    tags = set(row.tags)
    return tuple(
        law
        for law in stores.laws
        if law.axis is row.axis and law.path is row.path and set(law.required_tags).issubset(tags)
    )


def _pick_token_row(rows: tuple[LexicalEvidence, ...]) -> LexicalEvidence:
    """Select lexical evidence with the highest declared evidence rank."""
    return sorted(rows, key=lambda item: item.evidence_rank, reverse=True)[0]


def analyze_token(token: str, stores: G0PoCStores, trace_ref: str) -> AnalysisCard:
    """Analyze one token and produce a complete explanation card."""

    norm = _normalize_token(token)
    if not norm:
        raise G0PoCSchemaError("token must be non-empty")

    rows = _token_rows(norm, stores)
    if not rows:
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=AnalysisAxis.DAL,
            routed_path=AnalysisPath.G0,
            selected_laws=(LAW_UNRESOLVED,),
            reason="NO_LEXICAL_EVIDENCE",
        )
        return AnalysisCard(
            token=norm,
            axis=AnalysisAxis.DAL,
            path=AnalysisPath.G0,
            decision=DecisionState.DEFERRED,
            law_ids=(LAW_UNRESOLVED,),
            preventer="NO_WITNESS",
            residuals=("LEXICAL_EVIDENCE_MISSING",),
            trace=trace,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )

    token_row = _pick_token_row(rows)
    ontology_by_key = {node.key: node for node in stores.ontology}
    ontology_node = ontology_by_key.get(token_row.ontology_key)
    if ontology_node is None:
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=token_row.axis,
            routed_path=token_row.path,
            selected_laws=(LAW_UNBOUND,),
            reason="ONTOLOGY_KEY_UNRESOLVED",
        )
        return AnalysisCard(
            token=norm,
            axis=token_row.axis,
            path=token_row.path,
            decision=DecisionState.DEFERRED,
            law_ids=(LAW_UNBOUND,),
            preventer=ONTOLOGY_KEY_UNRESOLVED,
            residuals=("ONTOLOGY_KEY_UNRESOLVED",),
            trace=trace,
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    if (
        token_row.path is AnalysisPath.G0
        and ontology_node.boundary_status is not BoundaryStatus.G0_ADMISSIBLE
    ):
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=token_row.axis,
            routed_path=token_row.path,
            selected_laws=(LAW_UNBOUND,),
            reason="ONTOLOGY_G0_NOT_ADMISSIBLE",
        )
        return AnalysisCard(
            token=norm,
            axis=token_row.axis,
            path=token_row.path,
            decision=DecisionState.DEFERRED,
            law_ids=(LAW_UNBOUND,),
            preventer=G0_ONTOLOGY_NOT_ADMISSIBLE,
            residuals=("G0_ONTOLOGY_ADMISSIBILITY_REQUIRED",),
            trace=trace,
            failure_code=FailureCode.BOUNDARY_MISSING,
        )
    laws = _matching_laws(token_row, stores)

    if token_row.path is not AnalysisPath.G0:
        route_law_ids = tuple(sorted(law.law_id for law in laws)) or (LAW_ROUTE_FALLBACK,)
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=token_row.axis,
            routed_path=token_row.path,
            selected_laws=route_law_ids,
            reason="ROUTED_NON_G0_PATH",
        )
        return AnalysisCard(
            token=norm,
            axis=token_row.axis,
            path=token_row.path,
            decision=DecisionState.ROUTED,
            law_ids=route_law_ids,
            preventer="G0_SCOPE_ONLY",
            residuals=("ROUTED_TO_NON_G0_PATH",),
            trace=trace,
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    if not laws:
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=token_row.axis,
            routed_path=token_row.path,
            selected_laws=(LAW_UNBOUND,),
            reason="NO_MATCHING_LAW",
        )
        return AnalysisCard(
            token=norm,
            axis=token_row.axis,
            path=token_row.path,
            decision=DecisionState.DEFERRED,
            law_ids=(LAW_UNBOUND,),
            preventer="LAW_REGISTRY_GAP",
            residuals=("LAW_MISSING",),
            trace=trace,
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    top_priority = max(law.priority for law in laws)
    top_laws = tuple(law for law in laws if law.priority == top_priority)
    top_decisions = {law.decision_hint for law in top_laws}

    # Same-priority laws with different decision hints are a hard conflict.
    if len(top_decisions) > 1:
        trace = AnalysisTrace(
            trace_ref=trace_ref,
            routed_axis=token_row.axis,
            routed_path=token_row.path,
            selected_laws=tuple(sorted(law.law_id for law in top_laws)),
            reason="LAW_CONFLICT",
        )
        return AnalysisCard(
            token=norm,
            axis=token_row.axis,
            path=token_row.path,
            decision=DecisionState.REFUSED,
            law_ids=trace.selected_laws,
            preventer="CONFLICTING_TOP_LAWS",
            residuals=("LAW_CONFLICT",),
            trace=trace,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    chosen_decision = top_laws[0].decision_hint
    selected_laws = tuple(sorted(law.law_id for law in top_laws))
    composed = len(selected_laws) > 1
    reason = "COMPOSED_LAWS" if composed else "SINGLE_TOP_LAW"

    failure_code = None
    preventer = NO_PREVENTER
    residuals: tuple[str, ...] = ("LAW_COMPOSITION",) if composed else ()

    if chosen_decision is DecisionState.REFUSED:
        preventer = top_laws[0].preventer
        failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT
        residuals = residuals + ("PREVENTER_TRIGGERED",)
    elif chosen_decision is DecisionState.DEFERRED:
        preventer = top_laws[0].preventer
        failure_code = FailureCode.GATE_REQUIRED
        residuals = residuals + ("ADDITIONAL_EVIDENCE_REQUIRED",)

    trace = AnalysisTrace(
        trace_ref=trace_ref,
        routed_axis=token_row.axis,
        routed_path=token_row.path,
        selected_laws=selected_laws,
        reason=reason,
    )
    return AnalysisCard(
        token=norm,
        axis=token_row.axis,
        path=token_row.path,
        decision=chosen_decision,
        law_ids=selected_laws,
        preventer=preventer,
        residuals=residuals,
        trace=trace,
        failure_code=failure_code,
    )


def evaluate_poc(
    samples: tuple[EvaluationSample, ...],
    stores: G0PoCStores,
) -> EvaluationReport:
    """Evaluate measurable PoC indicators over expected samples."""

    if not samples:
        raise G0PoCSchemaError("samples must be non-empty")

    cards = [
        analyze_token(sample.token, stores, f"trace://g0-poc/eval/{idx:03d}")
        for idx, sample in enumerate(samples, start=1)
    ]
    matching_decision_count = sum(
        1
        for card, sample in zip(cards, samples, strict=True)
        if card.decision is sample.expected_decision
    )
    expected_refused = [
        sample for sample in samples if sample.expected_decision is DecisionState.REFUSED
    ]
    refusal_hits = sum(
        1
        for card, sample in zip(cards, samples, strict=True)
        if (
            sample.expected_decision is DecisionState.REFUSED
            and card.decision is DecisionState.REFUSED
        )
    )
    deferred = sum(1 for card in cards if card.decision is DecisionState.DEFERRED)
    trace_complete = sum(
        1
        for card in cards
        if card.trace.trace_ref
        and card.trace.selected_laws
        and card.trace.reason
        and card.axis
        and card.path
    )

    coverage_counts: dict[str, int] = {}
    for card in cards:
        coverage_counts[card.path.value] = coverage_counts.get(card.path.value, 0) + 1

    gap_tokens = tuple(card.token for card in cards if card.decision is DecisionState.DEFERRED)
    total = len(samples)
    return EvaluationReport(
        total=total,
        accuracy=matching_decision_count / total,
        correct_refusal_rate=(refusal_hits / len(expected_refused)) if expected_refused else 1.0,
        deferred_rate=deferred / total,
        trace_completeness_rate=trace_complete / total,
        coverage=tuple(sorted(coverage_counts.items())),
        gap_tokens=gap_tokens,
    )


def decide_go_no_go(
    report: EvaluationReport,
    *,
    min_accuracy: float = 0.8,
    min_trace_completeness: float = 1.0,
    max_deferred_rate: float = 0.25,
) -> GoNoGoDecision:
    """Generate a Go/No-Go decision from report thresholds."""

    reasons: list[str] = []
    if report.accuracy < min_accuracy:
        reasons.append("ACCURACY_BELOW_THRESHOLD")
    if report.trace_completeness_rate < min_trace_completeness:
        reasons.append("TRACE_COMPLETENESS_BELOW_THRESHOLD")
    if report.deferred_rate > max_deferred_rate:
        reasons.append("DEFERRED_RATE_ABOVE_THRESHOLD")

    if reasons:
        return GoNoGoDecision(verdict="NO_GO", reasons=tuple(reasons))
    return GoNoGoDecision(verdict="GO", reasons=("THRESHOLDS_MET",))


__all__ = [
    "AnalysisAxis",
    "AnalysisCard",
    "AnalysisPath",
    "AnalysisTrace",
    "BoundaryStatus",
    "DecisionState",
    "EvaluationReport",
    "EvaluationSample",
    "G0PoCSchemaError",
    "G0PoCStores",
    "GoNoGoDecision",
    "LawRecord",
    "LexicalEvidence",
    "OntologyNode",
    "analyze_token",
    "declared_preventer_enum",
    "decide_go_no_go",
    "evaluate_poc",
    "load_g0_poc_stores",
]
