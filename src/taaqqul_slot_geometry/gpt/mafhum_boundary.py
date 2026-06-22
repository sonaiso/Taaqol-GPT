"""GPT-R4 — MafhumGPT licensed implication boundary.

Binding:
- docs/54 §3.3 (MafhumGPT)
- docs/14 chain row GPT-R4 (implications derived from MantuqGPT)

MafhumGPT is a trace-bound implication candidate licensed by an explicit
MantuqGPT claim, a restriction, a scope, a non-mentioned counterpart, and a
preventer check. It is not origin binding and not a final reasonableness verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt.mantuq_boundary import MantuqGPT
from taaqqul_slot_geometry.x0r import TransitionContract


class MafhumGPTSchemaError(TypeError):
    """A GPT-R4 mafhum carrier was constructed with malformed fields."""


class RestrictionKind(StrEnum):
    """Explicit restriction kinds that may open a MafhumGPT field."""

    CONDITION = "CONDITION"
    DESCRIPTION = "DESCRIPTION"
    ENDPOINT = "ENDPOINT"
    NUMBER = "NUMBER"
    EXCLUSIVITY = "EXCLUSIVITY"
    TITLE = "TITLE"


class MafhumType(StrEnum):
    """Licensed MafhumGPT classification labels."""

    MUWAFAQAH = "MUWAFAQAH"
    MUKHALAFAH = "MUKHALAFAH"
    CONDITION = "CONDITION"
    DESCRIPTION = "DESCRIPTION"
    ENDPOINT = "ENDPOINT"
    NUMBER = "NUMBER"
    EXCLUSIVITY = "EXCLUSIVITY"


class PreventerKind(StrEnum):
    """Preventers that block or weaken a MafhumGPT candidate."""

    NONE_VISIBLE = "NONE_VISIBLE"
    COMMON_CASE = "COMMON_CASE"
    EMPHASIS_NOT_PRECAUTION = "EMPHASIS_NOT_PRECAUTION"
    BROADER_EVIDENCE = "BROADER_EVIDENCE"
    NON_REPORTING_MAQAM = "NON_REPORTING_MAQAM"
    BARE_TITLE = "BARE_TITLE"
    STRONGER_MANTUQ_CONFLICT = "STRONGER_MANTUQ_CONFLICT"


class MafhumGPTState(StrEnum):
    """Candidate state for GPT-R4; never a truth or reasonableness verdict."""

    LICENSED = "LICENSED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


GPT_MAFHUM_TRANSITION_CONTRACT = TransitionContract(
    declared_transitions=frozenset(
        {
            ("MaqamGPT", "MantuqGPT", "preserve_explicit_claims", "gpt_reasonableness"),
            ("MantuqGPT", "ClaimBoundary", "select_explicit_claim", "gpt_reasonableness"),
            ("ClaimBoundary", "ExplicitRestriction", "find_restriction", "gpt_reasonableness"),
            ("ExplicitRestriction", "ScopeBoundary", "bound_scope", "gpt_reasonableness"),
            ("ScopeBoundary", "SilenceNonMention", "identify_non_mention", "gpt_reasonableness"),
            ("SilenceNonMention", "MafhumType", "classify_mafhum", "gpt_reasonableness"),
            ("MafhumType", "PreventerGate", "check_preventer", "gpt_reasonableness"),
            ("PreventerGate", "MafhumCandidate", "license_candidate", "gpt_reasonableness"),
        }
    )
)


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MafhumGPTSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_tuple_of_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise MafhumGPTSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise MafhumGPTSchemaError(
                f"{cls_name}.{field} must contain only non-empty strings"
            )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise MafhumGPTSchemaError(f"{cls_name}.{field} must start with 'trace://'")


@dataclass(frozen=True, slots=True)
class ExplicitRestriction:
    """A restriction found inside an explicit MantuqGPT claim."""

    source_claim_ref: str
    kind: RestrictionKind
    text: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        if not isinstance(self.kind, RestrictionKind):
            raise MafhumGPTSchemaError(f"{cls}.kind must be a RestrictionKind member")
        _require_nonempty_str(cls, "text", self.text)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class ScopeBoundary:
    """The bounded field where a restriction may affect a non-mentioned case."""

    source_claim_ref: str
    domain: str
    scope: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        _require_nonempty_str(cls, "domain", self.domain)
        _require_nonempty_str(cls, "scope", self.scope)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class SilenceNonMention:
    """The non-mentioned counterpart tested only as a candidate."""

    source_claim_ref: str
    counterpart: str
    relation: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        _require_nonempty_str(cls, "counterpart", self.counterpart)
        _require_nonempty_str(cls, "relation", self.relation)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class PreventerGateResult:
    """Visible preventer result; it blocks or licenses only a candidate."""

    source_claim_ref: str
    preventer: PreventerKind
    explanation: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        if not isinstance(self.preventer, PreventerKind):
            raise MafhumGPTSchemaError(
                f"{cls}.preventer must be a PreventerKind member"
            )
        _require_nonempty_str(cls, "explanation", self.explanation)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class MafhumGPT:
    """Trace-bound implication candidate derived from MantuqGPT."""

    source_mantuq_ref: str
    source_claim_ref: str
    restriction: ExplicitRestriction
    scope_boundary: ScopeBoundary
    unmentioned_counterpart: SilenceNonMention
    transition_basis: str
    mafhum_type: MafhumType
    preventer: PreventerGateResult
    state: MafhumGPTState
    residuals: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_trace_ref(cls, "source_mantuq_ref", self.source_mantuq_ref)
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        if not isinstance(self.restriction, ExplicitRestriction):
            raise MafhumGPTSchemaError(
                f"{cls}.restriction must be an ExplicitRestriction"
            )
        if not isinstance(self.scope_boundary, ScopeBoundary):
            raise MafhumGPTSchemaError(f"{cls}.scope_boundary must be a ScopeBoundary")
        if not isinstance(self.unmentioned_counterpart, SilenceNonMention):
            raise MafhumGPTSchemaError(
                f"{cls}.unmentioned_counterpart must be a SilenceNonMention"
            )
        _require_nonempty_str(cls, "transition_basis", self.transition_basis)
        if not isinstance(self.mafhum_type, MafhumType):
            raise MafhumGPTSchemaError(
                f"{cls}.mafhum_type must be a MafhumType member"
            )
        if not isinstance(self.preventer, PreventerGateResult):
            raise MafhumGPTSchemaError(
                f"{cls}.preventer must be a PreventerGateResult"
            )
        if not isinstance(self.state, MafhumGPTState):
            raise MafhumGPTSchemaError(f"{cls}.state must be a MafhumGPTState member")
        _require_tuple_of_nonempty_str(cls, "residuals", self.residuals)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        _require_same_claim_ref(
            self.source_claim_ref,
            self.restriction,
            self.scope_boundary,
            self.unmentioned_counterpart,
            self.preventer,
        )
        if (
            self.state is MafhumGPTState.LICENSED
            and self.preventer.preventer is not PreventerKind.NONE_VISIBLE
        ):
            raise MafhumGPTSchemaError(
                f"{cls}.state cannot be LICENSED with a visible preventer"
            )
        if (
            self.state is MafhumGPTState.BLOCKED
            and self.preventer.preventer is PreventerKind.NONE_VISIBLE
        ):
            raise MafhumGPTSchemaError(
                f"{cls}.state cannot be BLOCKED without a visible preventer"
            )


@dataclass(frozen=True, slots=True)
class MafhumGPTResult:
    """Result surface for opening a MafhumGPT candidate."""

    state: MafhumGPTState
    candidate: MafhumGPT | None
    failure_code: FailureCode | None
    residuals: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, MafhumGPTState):
            raise MafhumGPTSchemaError(f"{cls}.state must be a MafhumGPTState member")
        if self.candidate is not None and not isinstance(self.candidate, MafhumGPT):
            raise MafhumGPTSchemaError(f"{cls}.candidate must be a MafhumGPT or None")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise MafhumGPTSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_tuple_of_nonempty_str(cls, "residuals", self.residuals)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.state is MafhumGPTState.LICENSED and self.candidate is None:
            raise MafhumGPTSchemaError(f"{cls}.LICENSED requires a candidate")
        if self.state is not MafhumGPTState.LICENSED and self.failure_code is None:
            raise MafhumGPTSchemaError(
                f"{cls}.{self.state.value} requires a named failure_code"
            )


def build_mafhum_gpt(
    mantuq: MantuqGPT,
    *,
    source_claim_ref: str,
    restriction: ExplicitRestriction | None,
    scope_boundary: ScopeBoundary | None,
    unmentioned_counterpart: SilenceNonMention | None,
    mafhum_type: MafhumType,
    preventer: PreventerGateResult,
    residuals: tuple[str, ...],
    trace_ref: str,
) -> MafhumGPTResult:
    """Build a GPT-R4 MafhumGPT candidate through the licensed sequence."""

    if not isinstance(mantuq, MantuqGPT):
        return _result(
            MafhumGPTState.REFUSED,
            FailureCode.MAFHUM_BEFORE_MANTUQ,
            residuals=("No MantuqGPT source was provided.",),
            trace_ref=trace_ref,
        )
    if not isinstance(restriction, ExplicitRestriction):
        return _result(
            MafhumGPTState.REFUSED,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=("No explicit restriction licenses MafhumGPT.",),
            trace_ref=trace_ref,
        )
    if not isinstance(scope_boundary, ScopeBoundary):
        return _result(
            MafhumGPTState.DEFERRED,
            FailureCode.SCOPE_MISSING,
            residuals=("No scope boundary was provided for the restriction.",),
            trace_ref=trace_ref,
        )
    if not isinstance(unmentioned_counterpart, SilenceNonMention):
        return _result(
            MafhumGPTState.REFUSED,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=("No non-mentioned counterpart was provided.",),
            trace_ref=trace_ref,
        )
    if not isinstance(preventer, PreventerGateResult):
        return _result(
            MafhumGPTState.REFUSED,
            FailureCode.GATE_REQUIRED,
            residuals=("No preventer gate result was provided.",),
            trace_ref=trace_ref,
        )
    if not isinstance(mafhum_type, MafhumType):
        return _result(
            MafhumGPTState.REFUSED,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=("No licensed MafhumGPT type was provided.",),
            trace_ref=trace_ref,
        )
    _require_nonempty_str("MafhumGPT", "source_claim_ref", source_claim_ref)
    _require_trace_ref("MafhumGPT", "trace_ref", trace_ref)
    _require_tuple_of_nonempty_str("MafhumGPT", "residuals", residuals)
    _require_same_claim_ref(
        source_claim_ref,
        restriction,
        scope_boundary,
        unmentioned_counterpart,
        preventer,
    )

    state = (
        MafhumGPTState.LICENSED
        if preventer.preventer is PreventerKind.NONE_VISIBLE
        else MafhumGPTState.BLOCKED
    )
    candidate = MafhumGPT(
        source_mantuq_ref=mantuq.trace_ref,
        source_claim_ref=source_claim_ref,
        restriction=restriction,
        scope_boundary=scope_boundary,
        unmentioned_counterpart=unmentioned_counterpart,
        transition_basis=unmentioned_counterpart.relation,
        mafhum_type=mafhum_type,
        preventer=preventer,
        state=state,
        residuals=residuals,
        trace_ref=trace_ref,
    )
    return MafhumGPTResult(
        state=state,
        candidate=candidate,
        failure_code=(
            None
            if state is MafhumGPTState.LICENSED
            else FailureCode.BLOCKING_RESIDUAL_PRESENT
        ),
        residuals=residuals,
        trace_ref=trace_ref,
    )


def _result(
    state: MafhumGPTState,
    failure_code: FailureCode,
    *,
    residuals: tuple[str, ...],
    trace_ref: str,
) -> MafhumGPTResult:
    return MafhumGPTResult(
        state=state,
        candidate=None,
        failure_code=failure_code,
        residuals=residuals,
        trace_ref=trace_ref,
    )


def _require_same_claim_ref(
    expected: str,
    restriction: ExplicitRestriction,
    scope_boundary: ScopeBoundary,
    unmentioned_counterpart: SilenceNonMention,
    preventer: PreventerGateResult,
) -> None:
    if any(
        item.source_claim_ref != expected
        for item in (
            restriction,
            scope_boundary,
            unmentioned_counterpart,
            preventer,
        )
    ):
        raise MafhumGPTSchemaError("all MafhumGPT boundaries must share source_claim_ref")


__all__ = [
    "ExplicitRestriction",
    "GPT_MAFHUM_TRANSITION_CONTRACT",
    "MafhumGPT",
    "MafhumGPTResult",
    "MafhumGPTSchemaError",
    "MafhumGPTState",
    "MafhumType",
    "PreventerGateResult",
    "PreventerKind",
    "RestrictionKind",
    "ScopeBoundary",
    "SilenceNonMention",
    "build_mafhum_gpt",
]
