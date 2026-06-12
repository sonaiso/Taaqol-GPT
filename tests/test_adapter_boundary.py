"""Constitutional tests for the PR-8 adapter boundary.

Coverage mirrors the docs/18 *PR-8 binding* — the propositions the
first concrete adapter must prove:

1.  **The licensing chain** (docs/18 §1): ``ModelClient protocol →
    ConcreteAdapterCandidate → AdapterGuard → AuditedAnswer only``.
    The golden path admits and hands the declared completion onward
    *unchanged*; the end-to-end test walks an admitted client
    through the full ``AnswerAudit`` chain.
2.  **The §3 refusal table**, row by row: every refusal is an
    :class:`AdapterAdmission` value naming an existing
    :class:`FailureCode` — never a bare exception, never a synthesis.
3.  **Admission is not approval** (docs/18 §5): no rank, no graph,
    no output, no trace — the admission carrier structurally cannot
    hold them.
4.  **Guard purity and totality** (docs/18 §7): ``admit()`` never
    calls ``complete()`` and judges only declared structure —
    statically (PR-8.1): adapter-authored lookup machinery
    (metaclass hooks, descriptors, ``__getattribute__``) never runs
    while the guard is judging.
5.  **Forbidden adapter forms stay absent** (docs/18 §6, §8): static
    AST guards — in the shape the suite already uses for the audit
    layer — prove the adapters package imports no provider SDK, no
    network surface, no environment/filesystem lookup, and no kernel
    authority; and that exactly **one** concrete adapter ships, on
    exactly one transport.

Disciplines: wrong argument *types* are programmer mistakes refused
loudly with ``TypeError`` (the PR-6 audit surface); expected
constitutional refusals are named values. Verdict-producing tests
declare themselves through :class:`ConstitutionalChainTestCase`
(docs/12 §9) and are checked by :func:`assert_constitutional_case`.
"""

from __future__ import annotations

import ast
import dataclasses
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry import (
    CONFIDENCE_SURFACE_NAMES,
    LEDGER_SURFACE_NAMES,
    RANK_SURFACE_NAMES,
    SUCCESSOR_SURFACE_NAMES,
    VERDICT_SURFACE_NAMES,
    AdapterAdmission,
    AdapterGuard,
    AnswerAudit,
    Center,
    ClosureState,
    ConcreteAdapterCandidate,
    EvidenceContract,
    EvidenceSource,
    FailureCode,
    GenerationSource,
    InMemoryModelClient,
    Layer,
    ModelClient,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotState,
    TraceLedger,
    TraceRef,
    TransitionGate,
    TransitionState,
    TransportSurface,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_DOC = "docs/18_ADAPTER_BOUNDARY_LAW.md"
_REFUSAL_TABLE_REF = "docs/18_ADAPTER_BOUNDARY_LAW.md#3-the-adapterguard-refusal-table"
_PROMPT = "What is Q1?"
_ANSWER = "Q1 is the declared minimal claim."


# ---------------------------------------------------------------------------
# 0. The origin law itself must be present (the PR-1C guard shape).
# ---------------------------------------------------------------------------


def test_pr8_constitutional_document_is_present() -> None:
    """docs/13 — a PR's origin law must exist in the repository.

    PR-8 branches from docs/18; adapter code in a repository where
    the Adapter Boundary Law is absent or empty would be a
    ``FORBIDDEN_LEAP`` regardless of CI status.
    """

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC
    assert path.is_file(), f"missing PR-8 origin document: {_DOC}"
    assert path.read_text(encoding="utf-8").strip(), (
        f"PR-8 origin document is empty: {_DOC}"
    )


# ---------------------------------------------------------------------------
# Carrier factories — candidate axis varied per test; the slot-graph
# factories are identical in shape to the audit tests.
# ---------------------------------------------------------------------------


def _transcript() -> dict[str, str]:
    return {_PROMPT: _ANSWER}


def _client() -> InMemoryModelClient:
    return InMemoryModelClient(_transcript())


def _candidate(**overrides: object) -> ConcreteAdapterCandidate:
    declared: dict[str, object] = {
        "adapter_identity": "in-memory-transcript-adapter",
        "model_identity": "declared-transcript-v1",
        "transport_surface": TransportSurface.IN_MEMORY,
        "completion": _client(),
        "configuration": {},
    }
    declared.update(overrides)
    return ConcreteAdapterCandidate(**declared)  # type: ignore[arg-type]


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="adapter-test",
        refusal_codes=(FailureCode.BOUNDARY_MISSING,),
    )


def _filled_slot() -> Slot:
    return Slot(
        name="answer",
        value_state=SlotState.FILLED,
        boundary=_boundary(),
        opening=OpeningPolicy(allowed_potentials=frozenset({"yes", "no"})),
        required=True,
        value="yes",
    )


def _trace_ref() -> TraceRef:
    return TraceRef(anchor="trace://Q1", kind="DECLARED_ENTRY")


def _gated_graph() -> SlotGraph:
    return SlotGraph(
        center=Center(
            identity_claim="Q1",
            domain="reasoning",
            scope="adapter-test",
            trace_ref=TraceRef(anchor="trace://Q1", kind="TRANSITION_VERDICT"),
        ),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.HYPOTHESIS,
        output_boundary=OutputBoundary(
            declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT
        ),
        generation_source=GenerationSource.TRANSITION_VERDICT,
    )


def _gate() -> TransitionGate:
    return TransitionGate(name="slot-to-candidate", gate_rank=Rank.LICENSED)


def _strong_evidence() -> EvidenceContract:
    return EvidenceContract(
        sources=(
            EvidenceSource(
                name="e1",
                kind="declared-observation",
                rank=Rank.STRONG,
                trace_ref=_trace_ref(),
            ),
        )
    )


# ---------------------------------------------------------------------------
# Forged completions — each exposes exactly the one surface its
# docs/18 §3 row forbids, on top of a licit ``complete``.
# ---------------------------------------------------------------------------


class _PlainCompletion:
    """A protocol-satisfying completion with no forbidden surface."""

    def complete(self, prompt: str) -> str:
        return f"emitted:{prompt}"


class _VerdictCompletion(_PlainCompletion):
    """Offers a verdict — a judge, not a transport (docs/18 §6)."""

    def verdict(self) -> str:
        return "APPROVED"


class _JudgeAndRankCompletion(_VerdictCompletion):
    """Exposes a verdict *and* a rank claim — table order decides."""

    def __init__(self) -> None:
        self.rank = "CERTIFICATE"


class _ConfidenceCompletion(_PlainCompletion):
    """Offers model internals as evidence (docs/01 — never evidence)."""

    confidence = 0.97


class _LedgerCompletion(_PlainCompletion):
    """Offers a trace-ledger write surface (docs/07 — shell-owned)."""

    def append_trace(self, entry: object) -> None:
        return None


class _SuccessorCompletion(_PlainCompletion):
    """Offers successor construction (docs/17 §1 — verdicts generate)."""

    def emit_successor(self) -> object:
        return object()


class _RankClaimCompletion(_PlainCompletion):
    """Carries an instance-level rank claim (docs/05 — gate-only)."""

    def __init__(self) -> None:
        self.rank = "CERTIFICATE"


class _NetworkAmbitionCompletion(_PlainCompletion):
    """Declares a wider transport than its candidate licenses."""

    transport_surface = TransportSurface.NETWORK


class _TripwireCompletion:
    """Counts completions — proves the guard never runs the transport."""

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, prompt: str) -> str:
        self.calls += 1
        return f"emitted:{prompt}"


# ---------------------------------------------------------------------------
# Forged lookup machinery — PR-8.1: judged names offered only through
# hooks that detonate if the guard resolves anything *dynamically*
# while judging (docs/18 §7).
# ---------------------------------------------------------------------------

#: Every name the guard reads while judging: the five docs/18 §3
#: surface registries plus the §2 transport declaration.
_JUDGED_SURFACE_NAMES: frozenset[str] = (
    VERDICT_SURFACE_NAMES
    | CONFIDENCE_SURFACE_NAMES
    | LEDGER_SURFACE_NAMES
    | SUCCESSOR_SURFACE_NAMES
    | RANK_SURFACE_NAMES
    | {"transport_surface"}
)


class _DetonatingMeta(type):
    """Detonates when a judged name is resolved dynamically on the class.

    Scoped to the judged names only: protocol ``isinstance`` checks
    legitimately read class dunders (``__mro__``, ``__dict__``,
    ``__annotations__``) and those must stay live.
    """

    def __getattribute__(cls, name: str) -> object:
        if name in _JUDGED_SURFACE_NAMES:
            raise RuntimeError(
                f"dynamic class lookup of {name!r}: the guard executed "
                "adapter-authored machinery while judging (docs/18 §7)"
            )
        return type.__getattribute__(cls, name)


class _MachineryCompletion(metaclass=_DetonatingMeta):
    """A licit transport whose class-level lookups are booby-trapped."""

    def complete(self, prompt: str) -> str:
        return f"emitted:{prompt}"


class _DetonatingDescriptor:
    """Counts ``__get__`` invocations and detonates — proof of stillness."""

    def __init__(self) -> None:
        self.reads = 0

    def __get__(self, obj: object, objtype: type | None = None) -> object:
        self.reads += 1
        raise RuntimeError(
            "descriptor __get__ executed while the guard was judging (docs/18 §7)"
        )


class _BoobyTrappedVerdictCompletion(_PlainCompletion):
    """Offers a verdict surface through a detonating descriptor."""

    verdict = _DetonatingDescriptor()


class _ComputedTransportCompletion(_PlainCompletion):
    """Computes a transport on access — a lookup, not a declaration."""

    transport_surface = _DetonatingDescriptor()


class _DictHidingRankCompletion:
    """Hides its ``__dict__`` (and the rank claim inside) behind a hook."""

    def __init__(self) -> None:
        self.rank = "CERTIFICATE"

    def complete(self, prompt: str) -> str:
        return f"emitted:{prompt}"

    def __getattribute__(self, name: str) -> object:
        if name == "__dict__":
            raise RuntimeError(
                "dynamic __dict__ access executed while judging (docs/18 §7)"
            )
        return object.__getattribute__(self, name)


# The admission dual of the audit tests' mapping: the harness
# vocabulary is ClosureState. A misdeclared candidate is INVALID, an
# unfilled required slot leaves it OPEN (docs/03), and a completion
# reaching for authority beyond transport is a FORBIDDEN_LEAP.
_ADMISSION_TO_CLOSURE: dict[FailureCode, ClosureState] = {
    FailureCode.IDENTITY_BROKEN: ClosureState.INVALID,
    FailureCode.BOUNDARY_MISSING: ClosureState.INVALID,
    FailureCode.REQUIRED_SLOT_EMPTY: ClosureState.OPEN,
    FailureCode.UNLICENSED_OPENING: ClosureState.INVALID,
    FailureCode.FORBIDDEN_STRAIGHT_LINE: ClosureState.FORBIDDEN_LEAP,
    FailureCode.OUTPUT_EXCEEDS_LAYER: ClosureState.FORBIDDEN_LEAP,
    FailureCode.GATE_REQUIRED: ClosureState.FORBIDDEN_LEAP,
    FailureCode.RANK_PROMOTION_WITHOUT_GATE: ClosureState.FORBIDDEN_LEAP,
}


def _admission_result(admission: AdapterAdmission) -> ConstitutionalChainResult:
    produced: set[str] = set()
    if not admission.is_refusal:
        produced.add("ADMITTED_TRANSPORT")
    assert admission.failure_code is None or admission.failure_code in _ADMISSION_TO_CLOSURE
    return ConstitutionalChainResult(
        state=(
            ClosureState.MINIMALLY_CLOSED
            if admission.failure_code is None
            else _ADMISSION_TO_CLOSURE[admission.failure_code]
        ),
        failure_code=admission.failure_code,
        # docs/18 §5 — admission grants no rank and writes no trace;
        # the named message *is* the visible residual surface.
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=False,
        produced_outputs=frozenset(produced),
    )


def _assert_admission_refusal(
    case: ConstitutionalChainTestCase,
    candidate: ConcreteAdapterCandidate,
) -> None:
    admission = AdapterGuard.admit(candidate)
    assert admission.is_refusal
    assert admission.client is None, "a refusal hands no client onward (docs/18 §1)"
    assert admission.failure_code is case.expected_failure_code
    assert "docs/18" in admission.message
    assert_constitutional_case(case, _admission_result(admission))


def _refusal_case(
    *,
    origin_law: str,
    branch_name: str,
    expected_failure_code: FailureCode,
    branch_of_origin: str,
    forbidden_shortcut: str,
) -> ConstitutionalChainTestCase:
    """The shared docs/18 §3 declaration surface of every refusal row."""

    return ConstitutionalChainTestCase(
        origin_law=origin_law,
        branch_name=branch_name,
        constitutional_chain=(
            "ModelClientProtocol",
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "AdapterAdmission",
        ),
        expected_state=_ADMISSION_TO_CLOSURE[expected_failure_code],
        expected_failure_code=expected_failure_code,
        forbidden_outputs=("ADMITTED_TRANSPORT",),
        max_rank=Rank.ZERO,
        required_trace=False,
        required_residual_visibility=True,
        chain_position="AdapterBoundary.guard.Admission",
        origin_law_ref=_REFUSAL_TABLE_REF,
        branch_of_origin=branch_of_origin,
        forbidden_shortcut_assertions=(forbidden_shortcut,),
    )


# ---------------------------------------------------------------------------
# 1. The protocol surface — the adapter satisfies it and adds nothing.
# ---------------------------------------------------------------------------


def test_in_memory_adapter_satisfies_the_protocol_without_widening_it() -> None:
    """docs/18 §8 (no-extension) — the adapter adds nothing to docs/01.

    The structural check passes, the declared transport is readable
    without executing anything, and the only public callable is
    ``complete`` — no verdicts, no streaming, no configuration
    mutation surface.
    """

    client = _client()
    assert isinstance(client, ModelClient)
    assert InMemoryModelClient.transport_surface is TransportSurface.IN_MEMORY
    public_callables = {
        name
        for name in dir(InMemoryModelClient)
        if not name.startswith("_") and callable(getattr(InMemoryModelClient, name))
    }
    assert public_callables == {"complete"}, (
        "the adapter must not widen the ModelClient protocol (docs/18 §8)"
    )


# ---------------------------------------------------------------------------
# 2. Golden admission — the chain's happy path, and only the happy path.
# ---------------------------------------------------------------------------


def test_golden_admission_hands_back_the_declared_completion_unchanged() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/18 §1 — ConcreteAdapterCandidate → AdapterGuard → admission",
        branch_name="fully-declared-candidate-is-admitted",
        constitutional_chain=(
            "ModelClientProtocol",
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "AdapterAdmission",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RANK_GRANT", "SUCCESSOR_SLOTGRAPH", "TRACE_ENTRY"),
        max_rank=Rank.ZERO,
        required_trace=False,
        required_residual_visibility=True,
        chain_position="AdapterBoundary.guard.Admission",
        origin_law_ref="docs/18_ADAPTER_BOUNDARY_LAW.md#1-the-licensing-chain",
        branch_of_origin="A full §2 declaration admits; admission is not approval.",
        forbidden_shortcut_assertions=(
            "GuardAdmitted → ApprovedAnswer",
            "Adapter → Output",
        ),
    )
    client = _client()

    admission = AdapterGuard.admit(_candidate(completion=client))

    assert not admission.is_refusal
    assert admission.failure_code is None
    # The guard hands the declared completion onward *unchanged* —
    # it wraps nothing, rewrites nothing, licenses nothing extra.
    assert admission.client is client
    assert "docs/18 §5" in admission.message
    # docs/18 §5 — the admission carrier structurally cannot hold a
    # rank, a graph, an output, or a trace entry.
    field_names = {field.name for field in dataclasses.fields(AdapterAdmission)}
    assert field_names == {"client", "failure_code", "message"}, (
        "AdapterAdmission must not grow approval surfaces (docs/18 §5)"
    )
    assert_constitutional_case(case, _admission_result(admission))


# ---------------------------------------------------------------------------
# 3. The docs/18 §3 refusal table — every row, in its own branch.
# ---------------------------------------------------------------------------


def test_missing_adapter_identity_is_identity_broken() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — adapter identity missing or empty",
        branch_name="empty-adapter-identity-is-refused",
        expected_failure_code=FailureCode.IDENTITY_BROKEN,
        branch_of_origin="An unnamed transport cannot be admitted.",
        forbidden_shortcut="UnnamedAdapter → Admission",
    )
    _assert_admission_refusal(case, _candidate(adapter_identity=""))
    _assert_admission_refusal(case, _candidate(adapter_identity="   "))


def test_missing_model_identity_is_identity_broken() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — model identity missing or empty",
        branch_name="empty-model-identity-is-refused",
        expected_failure_code=FailureCode.IDENTITY_BROKEN,
        branch_of_origin="An adapter for an unnamed model cannot be admitted.",
        forbidden_shortcut="UnnamedModel → Admission",
    )
    _assert_admission_refusal(case, _candidate(model_identity=""))


def test_undeclared_transport_is_boundary_missing() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — transport surface undeclared",
        branch_name="undeclared-transport-is-refused",
        expected_failure_code=FailureCode.BOUNDARY_MISSING,
        branch_of_origin="Without a declared transport there is no I/O boundary.",
        forbidden_shortcut="UndeclaredTransport → Admission",
    )
    _assert_admission_refusal(case, _candidate(transport_surface=None))


def test_unfilled_completion_slot_is_required_slot_empty() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — completion missing or not a ModelClient",
        branch_name="unfilled-completion-slot-is-refused",
        expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        branch_of_origin="The one required slot is unfilled; the candidate stays open.",
        forbidden_shortcut="EmptySlot → Admission",
    )
    _assert_admission_refusal(case, _candidate(completion=None))
    _assert_admission_refusal(case, _candidate(completion=object()))


def test_transport_wider_than_declared_is_unlicensed_opening() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3, §4 — I/O beyond the declared surface",
        branch_name="network-ambition-under-in-memory-licence-is-refused",
        expected_failure_code=FailureCode.UNLICENSED_OPENING,
        branch_of_origin="A NETWORK completion under an IN_MEMORY licence opens unlicensed I/O.",
        forbidden_shortcut="WiderTransport → Admission",
    )
    _assert_admission_refusal(
        case, _candidate(completion=_NetworkAmbitionCompletion())
    )


def test_verdict_surface_is_forbidden_straight_line() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3, §6 — an adapter is a transport, not a judge",
        branch_name="verdict-surface-is-refused",
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        branch_of_origin="A completion offering verdicts has judged; transports never judge.",
        forbidden_shortcut="Adapter → Verdict",
    )
    _assert_admission_refusal(case, _candidate(completion=_VerdictCompletion()))
    # Table order is binding: a completion exposing a verdict *and* a
    # rank claim is named by the verdict row, the first to fire.
    _assert_admission_refusal(case, _candidate(completion=_JudgeAndRankCompletion()))


def test_confidence_surface_is_forbidden_straight_line() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — model internals are never evidence (docs/01)",
        branch_name="confidence-surface-is-refused",
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        branch_of_origin="Confidence offered as evidence is the forbidden straight line.",
        forbidden_shortcut="Confidence → Evidence",
    )
    _assert_admission_refusal(case, _candidate(completion=_ConfidenceCompletion()))


def test_ledger_write_surface_is_output_exceeds_layer() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — the AnswerAudit shell owns the ledger (docs/07)",
        branch_name="ledger-write-surface-is-refused",
        expected_failure_code=FailureCode.OUTPUT_EXCEEDS_LAYER,
        branch_of_origin="An adapter that can append trace has exceeded its layer.",
        forbidden_shortcut="Adapter → TraceLedger",
    )
    _assert_admission_refusal(case, _candidate(completion=_LedgerCompletion()))


def test_successor_surface_is_gate_required() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — only an APPROVED verdict generates (docs/17 §1)",
        branch_name="successor-surface-is-refused",
        expected_failure_code=FailureCode.GATE_REQUIRED,
        branch_of_origin="Successor construction without a gate verdict is ungated generation.",
        forbidden_shortcut="Adapter → SuccessorGraph",
    )
    _assert_admission_refusal(case, _candidate(completion=_SuccessorCompletion()))


def test_rank_claim_is_rank_promotion_without_gate() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3 — no adapter holds rank authority (docs/05)",
        branch_name="rank-claim-surface-is-refused",
        expected_failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        branch_of_origin="A rank claim on the transport is promotion outside the gate.",
        forbidden_shortcut="Adapter → Rank",
    )
    # Instance-level claims are seen too, not only class attributes.
    _assert_admission_refusal(case, _candidate(completion=_RankClaimCompletion()))


# ---------------------------------------------------------------------------
# 4. Guard purity and totality (docs/18 §7) + loud domain guards.
# ---------------------------------------------------------------------------


def test_guard_never_calls_the_completion_it_judges() -> None:
    """docs/18 §7 — judging a candidate performs no I/O.

    The tripwire counts ``complete()`` calls; admission must leave
    it at zero. The guard reads declared structure only.
    """

    tripwire = _TripwireCompletion()
    admission = AdapterGuard.admit(_candidate(completion=tripwire))
    assert not admission.is_refusal
    assert tripwire.calls == 0, "the guard must never run the transport (docs/18 §7)"


def test_guard_judging_never_resolves_judged_names_dynamically() -> None:
    """docs/18 §7 (PR-8.1) — judging is static, not dynamic lookup.

    The completion's metaclass detonates if any judged name — the
    five §3 surface registries or ``transport_surface`` — is
    resolved dynamically on the class. The arming check proves the
    trap is live; a clean admission then proves the guard read
    declared structure only, executing none of the machinery.
    """

    with pytest.raises(RuntimeError):
        getattr(_MachineryCompletion, "verdict")  # the tripwire is armed

    admission = AdapterGuard.admit(_candidate(completion=_MachineryCompletion()))
    assert not admission.is_refusal, admission.message


def test_booby_trapped_verdict_surface_is_refused_without_execution() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3, §7 — a descriptor-borne verdict surface, judged statically",
        branch_name="booby-trapped-verdict-descriptor-is-seen-never-run",
        expected_failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        branch_of_origin="A verdict offered through __get__ is still a verdict surface.",
        forbidden_shortcut="GuardJudging → AdapterExecution",
    )
    _assert_admission_refusal(
        case, _candidate(completion=_BoobyTrappedVerdictCompletion())
    )
    descriptor = vars(_BoobyTrappedVerdictCompletion)["verdict"]
    assert descriptor.reads == 0, (
        "the guard executed a descriptor while judging (docs/18 §7)"
    )
    with pytest.raises(RuntimeError):
        _BoobyTrappedVerdictCompletion().verdict  # the tripwire is armed
    assert descriptor.reads == 1


def test_computed_transport_is_not_a_declaration_and_never_runs() -> None:
    """docs/18 §2, §7 (PR-8.1) — a computed transport is undeclared.

    A descriptor that would *compute* ``transport_surface`` on
    access is a lookup, not a declaration (docs/18 §2 — the adapter
    never looks anything up). The guard counts it as undeclared
    without ever invoking it: the candidate's declared ceiling
    stands, and the descriptor stays cold.
    """

    completion = _ComputedTransportCompletion()
    admission = AdapterGuard.admit(_candidate(completion=completion))
    assert not admission.is_refusal, admission.message
    descriptor = vars(_ComputedTransportCompletion)["transport_surface"]
    assert descriptor.reads == 0, (
        "the guard executed a transport descriptor while judging (docs/18 §7)"
    )
    with pytest.raises(RuntimeError):
        completion.transport_surface  # the tripwire is armed
    assert descriptor.reads == 1


def test_dynamic_dict_hiding_cannot_conceal_an_instance_rank_claim() -> None:
    case = _refusal_case(
        origin_law="docs/18 §3, §7 — instance claims are read statically (docs/05)",
        branch_name="dict-hiding-hook-cannot-conceal-a-rank-claim",
        expected_failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        branch_of_origin="A __getattribute__ hook over __dict__ neither runs nor conceals.",
        forbidden_shortcut="LookupHook → HiddenRank",
    )
    completion = _DictHidingRankCompletion()
    with pytest.raises(RuntimeError):
        getattr(completion, "__dict__")  # the tripwire is armed
    _assert_admission_refusal(case, _candidate(completion=completion))


def test_guard_refuses_non_candidates_loudly() -> None:
    """A wrong *type* is a programmer mistake, never a verdict."""

    with pytest.raises(TypeError):
        AdapterGuard.admit("not-a-candidate")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        AdapterGuard.admit(_client())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 5. Birth guards — declarations are total and frozen (docs/18 §2).
# ---------------------------------------------------------------------------


def test_candidate_birth_refuses_wrong_types_loudly() -> None:
    with pytest.raises(TypeError):
        _candidate(adapter_identity=42)
    with pytest.raises(TypeError):
        _candidate(model_identity=None)
    with pytest.raises(TypeError):
        _candidate(transport_surface="IN_MEMORY")
    with pytest.raises(TypeError):
        _candidate(configuration="not-a-mapping")
    with pytest.raises(TypeError):
        _candidate(configuration={"key": 42})
    with pytest.raises(TypeError):
        # docs/18 §2 — every declaration is filled at birth; there
        # are no defaults to fall back on.
        ConcreteAdapterCandidate(  # type: ignore[call-arg]
            adapter_identity="in-memory-transcript-adapter",
            model_identity="declared-transcript-v1",
            transport_surface=TransportSurface.IN_MEMORY,
        )


def test_candidate_configuration_is_frozen_at_birth() -> None:
    """docs/18 §2 — configuration is constructor args only.

    A declared candidate cannot drift: later mutation of the source
    mapping never reaches it, its own mapping refuses writes, and
    the dataclass itself is frozen.
    """

    source = {"transcript": "Q1"}
    candidate = _candidate(configuration=source)
    source["transcript"] = "tampered"
    assert candidate.configuration["transcript"] == "Q1"
    with pytest.raises(TypeError):
        candidate.configuration["transcript"] = "mutated"  # type: ignore[index]
    with pytest.raises(dataclasses.FrozenInstanceError):
        candidate.adapter_identity = "other"  # type: ignore[misc]


def test_admission_birth_enforces_admitted_xor_refused() -> None:
    """An admission both (or neither) admitted and refused is a bug."""

    with pytest.raises(TypeError):
        AdapterAdmission(client=None, failure_code=None, message="neither")
    with pytest.raises(TypeError):
        AdapterAdmission(
            client=_client(),
            failure_code=FailureCode.IDENTITY_BROKEN,
            message="both",
        )
    with pytest.raises(TypeError):
        AdapterAdmission(client=_client(), failure_code=None, message="   ")
    with pytest.raises(TypeError):
        AdapterAdmission(
            client=None,
            failure_code="IDENTITY_BROKEN",  # type: ignore[arg-type]
            message="stringly-typed code",
        )


# ---------------------------------------------------------------------------
# 6. The transcript adapter — verbatim, declared, never synthesising.
# ---------------------------------------------------------------------------


def test_in_memory_client_emits_verbatim_and_never_synthesises() -> None:
    """docs/18 §4 — one prompt in, one verbatim string out; §2 — no
    synthesis: an undeclared prompt is refused loudly, never invented.
    """

    client = _client()
    assert client.complete(_PROMPT) == _ANSWER
    assert client.complete(_PROMPT) == _ANSWER, "no state drift between calls"
    with pytest.raises(KeyError):
        client.complete("an undeclared prompt")


def test_in_memory_client_copies_its_declared_transcript() -> None:
    """docs/18 §2 — declarations are sealed at birth."""

    transcript = _transcript()
    client = InMemoryModelClient(transcript)
    transcript[_PROMPT] = "tampered"
    assert client.complete(_PROMPT) == _ANSWER


def test_in_memory_client_birth_refuses_wrong_types_loudly() -> None:
    with pytest.raises(TypeError):
        InMemoryModelClient("not-a-mapping")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        InMemoryModelClient({_PROMPT: 42})  # type: ignore[dict-item]
    with pytest.raises(TypeError):
        _client().complete(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 7. End to end — the chain of docs/18 §1, walked whole.
# ---------------------------------------------------------------------------


def test_admitted_adapter_walks_the_full_audit_chain() -> None:
    """docs/18 §1 — ``→ AuditedAnswer only``; §5 — admission decided
    nothing: the verdicts on the answer come from ``Γ`` and the gate,
    and the emitted string crosses the whole chain verbatim.
    """

    case = ConstitutionalChainTestCase(
        origin_law="docs/18 §1 — the licensing chain ends at AuditedAnswer only",
        branch_name="admitted-transport-walks-the-audit-chain",
        constitutional_chain=(
            "ModelClientProtocol",
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "AnswerAudit",
            "AuditedAnswer",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("ADAPTER_VERDICT", "ADAPTER_RANK_GRANT", "RANK_CERTIFICATE"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="AdapterBoundary.audit.AuditedAnswer",
        origin_law_ref="docs/18_ADAPTER_BOUNDARY_LAW.md#1-the-licensing-chain",
        branch_of_origin="An admitted transport's answer still walks the full audit chain.",
        forbidden_shortcut_assertions=(
            "Adapter → Output",
            "GuardAdmitted → ApprovedAnswer",
        ),
    )
    admission = AdapterGuard.admit(_candidate())
    assert not admission.is_refusal
    assert admission.client is not None

    ledger = TraceLedger()
    audit = AnswerAudit(admission.client, ledger)
    audited = audit.audit(
        _PROMPT, _gated_graph(), _gate(), Layer.CANDIDATE, _strong_evidence()
    )

    # The gate — not the adapter, not the admission — approved.
    assert audited.gate_state is TransitionState.APPROVED
    assert audited.failure_code is None
    # Verbatim through adapter, guard, and audit shell alike.
    assert audited.answer == _ANSWER
    assert audited.prompt == _PROMPT
    # Rank came from the gate's bounded meet, not from the adapter.
    assert audited.rank is Rank.HYPOTHESIS
    assert audited.evidence_refs == ("trace://Q1",)
    successor = audited.successor
    assert successor is not None
    assert successor.center.trace_ref.anchor == "trace://Q1/gate/slot-to-candidate"
    # The full docs/07 chain: gamma → gate → audit, exactly once.
    gamma_entry, gate_entry, audit_entry = ledger.entries
    assert (gamma_entry.stage, gate_entry.stage, audit_entry.stage) == (
        "gamma",
        "gate",
        "audit",
    )
    assert_constitutional_case(
        case,
        ConstitutionalChainResult(
            state=audited.gamma_state,
            failure_code=audited.failure_code,
            rank=audited.rank,
            residual_visibility=audited.residual_visibility,
            trace_present=bool(audited.trace_anchor),
            produced_outputs=frozenset(
                {"SUCCESSOR_SLOTGRAPH", f"RANK_{audited.rank.name}", "VERBATIM_ANSWER"}
            ),
        ),
    )


# ---------------------------------------------------------------------------
# 8. Static guards — forbidden adapter forms stay absent (docs/18 §6, §8).
# ---------------------------------------------------------------------------

_ADAPTER_MODULES = (
    "taaqqul_slot_geometry.adapters",
    "taaqqul_slot_geometry.adapters.adapter_boundary",
    "taaqqul_slot_geometry.adapters.in_memory",
)

_FORBIDDEN_IMPORT_ROOTS = {
    # Provider SDKs and the network surface (docs/18 §6 — the same
    # set the audit-layer guard enforces).
    "aiohttp",
    "anthropic",
    "http",
    "httpx",
    "openai",
    "requests",
    "socket",
    "urllib",
    # docs/18 §2 — configuration is constructor args only: the
    # adapter never looks up environment, filesystem, or processes.
    "dotenv",
    "os",
    "pathlib",
    "shutil",
    "subprocess",
    "tempfile",
}

#: docs/18 §8 — the adapter layer may see exactly the protocol and
#: the refusal vocabulary; importing anything else is a leak.
_ALLOWED_FIRST_PARTY_IMPORTS = {
    "taaqqul_slot_geometry.adapters.adapter_boundary",
    "taaqqul_slot_geometry.adapters.in_memory",
    "taaqqul_slot_geometry.audit.model_client",
    "taaqqul_slot_geometry.core.failure_taxonomy",
}

#: Kernel authority that must stay unreachable from the adapter layer
#: (docs/18 §8 — no-judge, no-ledger, no-successor, no-promotion).
_KERNEL_AUTHORITY_NAMES = {
    "AnswerAudit",
    "AuditedAnswer",
    "ClosureState",
    "Gamma",
    "GammaResult",
    "Rank",
    "RankLattice",
    "SlotGraph",
    "TraceEntryCandidate",
    "TraceLedger",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    "emit_successor",
    "gamma",
}


def _module_tree(module_name: str) -> ast.Module:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    return ast.parse(source)


def test_adapter_layer_ships_no_network_or_lookup_surface() -> None:
    """docs/18 §2, §4, §6 — IN_MEMORY means no I/O of any kind.

    The adapters package must not import any provider SDK, network
    module, or environment/filesystem/process lookup surface.
    """

    for module_name in _ADAPTER_MODULES:
        imported: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        leaked = imported & _FORBIDDEN_IMPORT_ROOTS
        assert not leaked, (
            f"{module_name} imports forbidden transport/lookup modules: "
            f"{sorted(leaked)} (docs/18 §2, §6)"
        )


def test_adapter_layer_imports_no_kernel_authority() -> None:
    """docs/18 §8 — the adapter layer sees the protocol and the
    refusal vocabulary, nothing else of the kernel.
    """

    for module_name in _ADAPTER_MODULES:
        first_party: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("taaqqul_slot_geometry"):
                        first_party.add(alias.name)
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("taaqqul_slot_geometry")
            ):
                first_party.add(node.module)
        leaked = first_party - _ALLOWED_FIRST_PARTY_IMPORTS
        assert not leaked, (
            f"{module_name} imports kernel modules beyond its licence: "
            f"{sorted(leaked)} (docs/18 §8)"
        )


def test_adapter_layer_references_no_kernel_authority() -> None:
    """The PR-2 purity-guard pattern: no judge, ledger, successor, or
    rank authority is even *named* inside the adapters package.
    """

    for module_name in _ADAPTER_MODULES:
        referenced: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Name):
                referenced.add(node.id)
            elif isinstance(node, ast.Attribute):
                referenced.add(node.attr)
        leaked = referenced & _KERNEL_AUTHORITY_NAMES
        assert not leaked, (
            f"{module_name} references kernel authority: {sorted(leaked)} "
            "(docs/18 §8)"
        )


def test_pr8_ships_exactly_one_concrete_adapter() -> None:
    """docs/18 PR-8 binding — exactly one adapter, one transport."""

    adapters: set[str] = set()
    for module_name in _ADAPTER_MODULES:
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.ClassDef):
                methods = {
                    item.name
                    for item in node.body
                    if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
                }
                if "complete" in methods:
                    adapters.add(node.name)
    assert adapters == {"InMemoryModelClient"}, (
        "PR-8 licenses exactly one concrete adapter (docs/18 — PR-8 binding)"
    )


def test_surface_registries_are_disjoint_and_named() -> None:
    """One name, one §3 row — overlapping registries would let a
    single surface fire two rows and blur the named refusal.
    """

    registries = (
        VERDICT_SURFACE_NAMES,
        CONFIDENCE_SURFACE_NAMES,
        LEDGER_SURFACE_NAMES,
        SUCCESSOR_SURFACE_NAMES,
        RANK_SURFACE_NAMES,
    )
    for registry in registries:
        assert registry, "an empty registry guards nothing (docs/18 §3)"
    union: frozenset[str] = frozenset().union(*registries)
    assert len(union) == sum(len(registry) for registry in registries), (
        "the five docs/18 §3 surface registries must not overlap"
    )
