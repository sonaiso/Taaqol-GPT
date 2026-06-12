"""Constitutional tests for the PR-8 adapter boundary.

Coverage mirrors the PR-8 binding of
``docs/18_ADAPTER_BOUNDARY_LAW.md`` — the obligations the first
concrete adapter must prove:

1.  **Declarations at birth** (§2): a ``ConcreteAdapterCandidate``
    carries adapter identity, model identity, declared transport,
    completion callable, and caller-supplied configuration — all
    required, no defaults, no synthesis.
2.  **The refusal table** (§3): ``AdapterGuard.admit`` walks every
    row in order and names each refusal with an *existing*
    :class:`FailureCode` — a value, never a bare exception.
3.  **The licensed I/O surface** (§4): the one adapter this chain
    step ships is ``IN_MEMORY`` — no network, no filesystem, no
    environment, no process surface anywhere in the subpackage, at
    import time or any other time.
4.  **Admission is not approval** (§5): an admitted transport's
    answers still walk the full ``Γ → TransitionGate →
    AnswerAudit`` pipeline; the straight line
    ``GuardAdmitted → ApprovedAnswer`` stays forbidden.
5.  **Guard purity and totality** (§7): admission is structural —
    the guard never calls ``complete()`` — and every candidate is
    either admitted or refused with a named code.

Disciplines: birth and domain guards refuse programmer mistakes
loudly (``TypeError`` / ``KeyError``), never as constitutional
verdicts; verdict-producing tests declare themselves through
:class:`ConstitutionalChainTestCase` (docs/12 §9) and are checked
by :func:`assert_constitutional_case`.
"""

from __future__ import annotations

import ast
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry import (
    AdapterAdmission,
    AdapterGuard,
    AnswerAudit,
    AuditedAnswer,
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

# ---------------------------------------------------------------------------
# 0. The governing law must be present (PR-8 binding, obligation 5).
# ---------------------------------------------------------------------------


def test_adapter_boundary_law_document_is_present() -> None:
    """docs/18 anchors every admission below; its absence unmoors them.

    The same cheap string-based discipline as the harness docs
    guards: fail any PR that ships adapter code without its
    governing law.
    """

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    relative = "docs/18_ADAPTER_BOUNDARY_LAW.md"
    path = repo_root / relative
    assert path.is_file(), f"missing constitutional law: {relative}"
    assert path.read_text(encoding="utf-8").strip(), (
        f"constitutional law is empty: {relative}"
    )


# ---------------------------------------------------------------------------
# Carrier factories — identical in shape to the audit tests; each
# adapter test varies only the single axis it exercises.
# ---------------------------------------------------------------------------

_DECLARED_PROMPT = "What is Q1?"
_DECLARED_ANSWER = "yes"


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


def _gated_graph() -> SlotGraph:
    """A graph that *is* the product of a prior transition verdict."""

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
                trace_ref=TraceRef(anchor="trace://Q1", kind="DECLARED_ENTRY"),
            ),
        )
    )


def _client() -> InMemoryModelClient:
    return InMemoryModelClient(((_DECLARED_PROMPT, _DECLARED_ANSWER),))


def _candidate(**overrides: object) -> ConcreteAdapterCandidate:
    """A fully-declared docs/18 §2 candidate; tests override one axis."""

    declarations: dict[str, object] = {
        "adapter_identity": "in-memory-fixture",
        "model_identity": "fixture-model-v0",
        "transport_surface": TransportSurface.IN_MEMORY,
        "completion": _client(),
        "configuration": (),
    }
    declarations.update(overrides)
    return ConcreteAdapterCandidate(**declarations)  # type: ignore[arg-type]


class _DeclaredClient:
    """The docs/01 surface and nothing else: a prompt in, a string out."""

    def complete(self, prompt: str) -> str:
        return _DECLARED_ANSWER


class _VerdictClient(_DeclaredClient):
    """A transport that has grown a judge's surface (docs/18 §6)."""

    def verdict(self) -> str:
        return "APPROVED"


class _ConfidenceClient(_DeclaredClient):
    """A transport offering self-reported confidence as evidence."""

    confidence = 0.99


class _LedgerClient(_DeclaredClient):
    """A transport that has grown a ledger writer's surface."""

    def append_trace(self) -> None:
        return None


class _SuccessorClient(_DeclaredClient):
    """A transport that has grown a generator's surface."""

    def emit_successor(self) -> None:
        return None


class _RankClient(_DeclaredClient):
    """A transport claiming a rank for its own answers."""

    rank = "CERTIFICATE"


class _TripwireClient:
    """A client whose completion must never run during admission."""

    def complete(self, prompt: str) -> str:
        raise AssertionError(
            "AdapterGuard.admit must never call complete() (docs/18 §7)"
        )


# The audit dual of the gate tests' mapping: the harness vocabulary
# is ClosureState, so a refused *move* is reported through the same
# table while an APPROVED move reports Γ's own closure verdict.
_TRANSITION_TO_CLOSURE: dict[TransitionState, ClosureState] = {
    TransitionState.DEFERRED: ClosureState.OPEN,
    TransitionState.BLOCKED: ClosureState.BLOCKED,
    TransitionState.REJECTED: ClosureState.INVALID,
    TransitionState.FORBIDDEN_LEAP: ClosureState.FORBIDDEN_LEAP,
}


def _result_from(audited: AuditedAnswer) -> ConstitutionalChainResult:
    state = (
        audited.gamma_state
        if audited.gate_state is TransitionState.APPROVED
        else _TRANSITION_TO_CLOSURE[audited.gate_state]
    )
    produced: set[str] = set()
    if audited.successor is not None:
        produced.add("SUCCESSOR_SLOTGRAPH")
        produced.add(f"RANK_{audited.successor.rank.name}")
    return ConstitutionalChainResult(
        state=state,
        failure_code=audited.failure_code,
        rank=audited.rank,
        residual_visibility=audited.residual_visibility,
        trace_present=bool(audited.trace_anchor),
        produced_outputs=frozenset(produced),
    )


# Each docs/18 §3 refusal mapped into the closure family its kernel
# precedent uses: structural absences are INVALID (Γ's
# IDENTITY_BROKEN / BOUNDARY_MISSING family), an empty required slot
# stays OPEN (Γ's REQUIRED_SLOT_EMPTY), boundary escapes are
# FORBIDDEN_LEAP (Γ's OUTPUT_EXCEEDS_LAYER and the registry's
# FORBIDDEN_STRAIGHT_LINE), a missing gate defers — OPEN (the gate's
# GATE_REQUIRED → DEFERRED), an unlicensed opening is structural —
# INVALID, and an ungated rank claim is INVALID (the gate's
# RANK_PROMOTION_WITHOUT_GATE → REJECTED).
_GUARD_REFUSAL_TO_CLOSURE: dict[FailureCode, ClosureState] = {
    FailureCode.IDENTITY_BROKEN: ClosureState.INVALID,
    FailureCode.BOUNDARY_MISSING: ClosureState.INVALID,
    FailureCode.REQUIRED_SLOT_EMPTY: ClosureState.OPEN,
    FailureCode.UNLICENSED_OPENING: ClosureState.INVALID,
    FailureCode.FORBIDDEN_STRAIGHT_LINE: ClosureState.FORBIDDEN_LEAP,
    FailureCode.OUTPUT_EXCEEDS_LAYER: ClosureState.FORBIDDEN_LEAP,
    FailureCode.GATE_REQUIRED: ClosureState.OPEN,
    FailureCode.RANK_PROMOTION_WITHOUT_GATE: ClosureState.INVALID,
}


def _assert_guard_refusal(
    *,
    branch_name: str,
    branch_of_origin: str,
    candidate: ConcreteAdapterCandidate,
    expected_code: FailureCode,
    message_fragment: str,
) -> None:
    """Walk one docs/18 §3 row as a constitutional chain case."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/18 §3 — the AdapterGuard refusal table",
        branch_name=branch_name,
        constitutional_chain=(
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "FailureTaxonomy",
        ),
        expected_state=_GUARD_REFUSAL_TO_CLOSURE[expected_code],
        expected_failure_code=expected_code,
        forbidden_outputs=("ADMITTED_TRANSPORT", "APPROVED_ANSWER"),
        max_rank=Rank.ZERO,
        required_trace=False,
        required_residual_visibility=True,
        chain_position="AdapterLicensingChain.step.3.AdapterGuard",
        origin_law_ref="docs/18_ADAPTER_BOUNDARY_LAW.md#3-the-adapterguard-refusal-table",
        branch_of_origin=branch_of_origin,
        forbidden_shortcut_assertions=("GuardAdmitted → ApprovedAnswer",),
    )
    admission = AdapterGuard().admit(candidate)
    assert admission.is_refusal
    assert admission.candidate is None
    assert admission.failure_code is expected_code
    assert message_fragment in admission.message
    # A guard refusal is fully named and fully visible: the code and
    # its reason *are* the residual surface — nothing hidden, no rank
    # granted, no trace written, nothing produced.
    assert_constitutional_case(
        case,
        ConstitutionalChainResult(
            state=case.expected_state,
            failure_code=admission.failure_code,
            rank=Rank.ZERO,
            residual_visibility=True,
            trace_present=False,
            produced_outputs=frozenset(),
        ),
    )


# ---------------------------------------------------------------------------
# 1. The one licensed adapter — IN_MEMORY, declared table, no synthesis.
# ---------------------------------------------------------------------------


def test_in_memory_client_satisfies_the_model_client_protocol() -> None:
    """docs/18 §1 step 1 — the adapter satisfies the PR-6 protocol.

    And docs/18 §2 — it answers only what was declared at birth:
    an unmapped prompt is a fixture-wiring mistake refused loudly,
    never a synthesised answer.
    """

    client = _client()
    assert isinstance(client, ModelClient)
    assert client.complete(_DECLARED_PROMPT) == _DECLARED_ANSWER
    with pytest.raises(TypeError):
        client.complete(42)  # type: ignore[arg-type]
    with pytest.raises(KeyError):
        client.complete("undeclared prompt")


def test_in_memory_client_refuses_malformed_birth_declarations() -> None:
    """docs/18 §2 — malformed declarations are programmer mistakes."""

    with pytest.raises(TypeError):
        InMemoryModelClient([(_DECLARED_PROMPT, _DECLARED_ANSWER)])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        InMemoryModelClient(((_DECLARED_PROMPT,),))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        InMemoryModelClient(((_DECLARED_PROMPT, 42),))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        InMemoryModelClient(((_DECLARED_PROMPT, "a"), (_DECLARED_PROMPT, "b")))


# ---------------------------------------------------------------------------
# 2. Birth guards — §2 declarations are required, typed, and loud.
# ---------------------------------------------------------------------------


def test_candidate_birth_requires_all_five_declarations() -> None:
    """docs/18 §2 — no defaults, no synthesis: an unsupplied
    declaration is a programmer mistake refused loudly at birth.
    """

    declarations: dict[str, object] = {
        "adapter_identity": "in-memory-fixture",
        "model_identity": "fixture-model-v0",
        "transport_surface": TransportSurface.IN_MEMORY,
        "completion": _client(),
        "configuration": (),
    }
    for missing in declarations:
        partial = {key: value for key, value in declarations.items() if key != missing}
        with pytest.raises(TypeError):
            ConcreteAdapterCandidate(**partial)  # type: ignore[arg-type]


def test_candidate_birth_refuses_malformed_declaration_types() -> None:
    with pytest.raises(TypeError):
        _candidate(adapter_identity=42)
    with pytest.raises(TypeError):
        _candidate(model_identity=42)
    with pytest.raises(TypeError):
        _candidate(transport_surface="NETWORK")
    with pytest.raises(TypeError):
        _candidate(configuration=[("endpoint", "value")])
    with pytest.raises(TypeError):
        _candidate(configuration=(("endpoint",),))
    with pytest.raises(TypeError):
        _candidate(configuration=((42, "value"),))


def test_admission_schema_refuses_inconsistent_values() -> None:
    """The XOR invariant of the admission value: exactly one of
    candidate / failure_code, so a refusal can never be silently
    treated as an admission.
    """

    with pytest.raises(TypeError):
        AdapterAdmission(candidate=None, failure_code=None, message="")
    with pytest.raises(TypeError):
        AdapterAdmission(
            candidate=_candidate(),
            failure_code=FailureCode.IDENTITY_BROKEN,
            message="",
        )
    with pytest.raises(TypeError):
        AdapterAdmission(
            candidate=None,
            failure_code=FailureCode.IDENTITY_BROKEN,
            message=42,  # type: ignore[arg-type]
        )


def test_guard_requires_a_candidate_value() -> None:
    """docs/18 §3 — a wrong *type* handed to the guard is a
    programmer mistake refused loudly, never a named verdict.
    """

    guard = AdapterGuard()
    for wrong in (object(), None, "candidate", _client()):
        with pytest.raises(TypeError):
            guard.admit(wrong)


# ---------------------------------------------------------------------------
# 3. The §3 refusal table — every row, in the table's own order.
# ---------------------------------------------------------------------------


def test_guard_refuses_missing_or_empty_adapter_identity() -> None:
    for degenerate in ("", "   "):
        _assert_guard_refusal(
            branch_name="adapter-identity-empty",
            branch_of_origin="Adapter identity missing or empty → IDENTITY_BROKEN.",
            candidate=_candidate(adapter_identity=degenerate),
            expected_code=FailureCode.IDENTITY_BROKEN,
            message_fragment="adapter identity",
        )


def test_guard_refuses_missing_or_empty_model_identity() -> None:
    _assert_guard_refusal(
        branch_name="model-identity-empty",
        branch_of_origin="Model identity missing or empty → IDENTITY_BROKEN.",
        candidate=_candidate(model_identity=""),
        expected_code=FailureCode.IDENTITY_BROKEN,
        message_fragment="model identity",
    )


def test_guard_refuses_undeclared_transport_surface() -> None:
    _assert_guard_refusal(
        branch_name="transport-surface-undeclared",
        branch_of_origin="Transport surface undeclared → BOUNDARY_MISSING.",
        candidate=_candidate(transport_surface=None),
        expected_code=FailureCode.BOUNDARY_MISSING,
        message_fragment="transport surface",
    )


def test_guard_refuses_completion_that_is_not_a_model_client() -> None:
    for not_a_client in (object(), None):
        _assert_guard_refusal(
            branch_name="completion-not-model-client",
            branch_of_origin=(
                "Completion callable missing / not ModelClient → REQUIRED_SLOT_EMPTY."
            ),
            candidate=_candidate(completion=not_a_client),
            expected_code=FailureCode.REQUIRED_SLOT_EMPTY,
            message_fragment="completion callable",
        )


def test_guard_refuses_persistence_configuration() -> None:
    """docs/18 §4 rule 3 — no persistence on any transport surface."""

    _assert_guard_refusal(
        branch_name="configuration-declares-persistence",
        branch_of_origin=(
            "I/O beyond the declared, licensed surface (§4) → UNLICENSED_OPENING."
        ),
        candidate=_candidate(configuration=(("cache_dir", "/var/cache/adapter"),)),
        expected_code=FailureCode.UNLICENSED_OPENING,
        message_fragment="cache_dir",
    )


def test_guard_refuses_network_configuration_on_in_memory_transport() -> None:
    """docs/18 §4 rule 5 — only the declared surface is licensed.

    The same endpoint key is licit on a declared ``NETWORK``
    surface: the refusal is about the boundary, not the key. (The
    completion below stays the in-memory fixture — PR-8 ships no
    network adapter; only the guard's direction is exercised.)
    """

    network_configuration = (("endpoint", "https://example.invalid/v1"),)
    _assert_guard_refusal(
        branch_name="network-configuration-on-in-memory-transport",
        branch_of_origin=(
            "I/O beyond the declared, licensed surface (§4) → UNLICENSED_OPENING."
        ),
        candidate=_candidate(configuration=network_configuration),
        expected_code=FailureCode.UNLICENSED_OPENING,
        message_fragment="endpoint",
    )
    admitted = AdapterGuard().admit(
        _candidate(
            transport_surface=TransportSurface.NETWORK,
            configuration=network_configuration,
        )
    )
    assert not admitted.is_refusal


def test_guard_refuses_a_verdict_surface() -> None:
    _assert_guard_refusal(
        branch_name="adapter-exposes-verdict-surface",
        branch_of_origin="Adapter exposes a verdict surface → FORBIDDEN_STRAIGHT_LINE.",
        candidate=_candidate(completion=_VerdictClient()),
        expected_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        message_fragment="verdict",
    )


def test_guard_refuses_confidence_as_evidence_surface() -> None:
    _assert_guard_refusal(
        branch_name="adapter-exposes-confidence-as-evidence",
        branch_of_origin=(
            "Adapter exposes confidence / internals as evidence "
            "(Tool/Number/LCNV → Knowledge) → FORBIDDEN_STRAIGHT_LINE."
        ),
        candidate=_candidate(completion=_ConfidenceClient()),
        expected_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        message_fragment="confidence",
    )


def test_guard_refuses_a_trace_ledger_write_surface() -> None:
    _assert_guard_refusal(
        branch_name="adapter-exposes-ledger-write-surface",
        branch_of_origin=(
            "Adapter exposes a TraceLedger write surface → OUTPUT_EXCEEDS_LAYER."
        ),
        candidate=_candidate(completion=_LedgerClient()),
        expected_code=FailureCode.OUTPUT_EXCEEDS_LAYER,
        message_fragment="trace-ledger",
    )


def test_guard_refuses_a_successor_graph_surface() -> None:
    _assert_guard_refusal(
        branch_name="adapter-exposes-successor-surface",
        branch_of_origin="Adapter exposes a successor-graph surface → GATE_REQUIRED.",
        candidate=_candidate(completion=_SuccessorClient()),
        expected_code=FailureCode.GATE_REQUIRED,
        message_fragment="successor",
    )


def test_guard_refuses_a_rank_claim_surface() -> None:
    _assert_guard_refusal(
        branch_name="adapter-claims-a-rank",
        branch_of_origin=(
            "Adapter exposes a rank claim → RANK_PROMOTION_WITHOUT_GATE."
        ),
        candidate=_candidate(completion=_RankClient()),
        expected_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        message_fragment="rank",
    )


def test_guard_walks_the_table_in_order_first_refusal_wins() -> None:
    """docs/18 §3 — the table is ordered: a many-ways-degenerate
    candidate is named by its *first* violated row.
    """

    admission = AdapterGuard().admit(
        ConcreteAdapterCandidate(
            adapter_identity="",
            model_identity="",
            transport_surface=None,
            completion=object(),
            configuration=(("cache_dir", "/var/cache/adapter"),),
        )
    )
    assert admission.is_refusal
    assert admission.failure_code is FailureCode.IDENTITY_BROKEN


# ---------------------------------------------------------------------------
# 4. Guard purity + the admission surface (§5, §7).
# ---------------------------------------------------------------------------


def test_guard_admission_is_structural_and_never_calls_complete() -> None:
    """docs/18 §7 — admission is structural: the guard never calls
    ``complete()`` and performs no I/O.
    """

    admission = AdapterGuard().admit(_candidate(completion=_TripwireClient()))
    assert not admission.is_refusal
    assert admission.failure_code is None


def test_admission_carries_no_verdict_rank_trace_or_successor_surface() -> None:
    """docs/18 §5 — admission is of a transport, never approval of an
    answer: the admission value structurally cannot carry one.
    """

    admission = AdapterGuard().admit(_candidate())
    assert not admission.is_refusal
    assert admission.candidate is not None
    for granted in (
        "rank",
        "verdict",
        "gamma_state",
        "gate_state",
        "ledger",
        "trace_anchor",
        "successor",
    ):
        assert not hasattr(admission, granted), (
            f"AdapterAdmission must not expose {granted!r} (docs/18 §5)"
        )


# ---------------------------------------------------------------------------
# 5. The licensing chain end-to-end — answers only through AnswerAudit.
# ---------------------------------------------------------------------------


def test_admitted_adapter_reaches_caller_only_through_answer_audit() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/18 §1 — the licensing chain",
        branch_name="admitted-transport-audited-answer",
        constitutional_chain=(
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "ModelClient",
            "SlotGraph",
            "Gamma",
            "TransitionGate",
            "AuditedAnswer",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RAW_ADAPTER_STRING", "RANK_CERTIFICATE"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="AdapterLicensingChain.step.4.AuditedAnswerOnly",
        origin_law_ref="docs/18_ADAPTER_BOUNDARY_LAW.md#1-the-licensing-chain",
        branch_of_origin="Answers reach a caller only through AnswerAudit.",
        forbidden_shortcut_assertions=("GuardAdmitted → ApprovedAnswer",),
    )
    admission = AdapterGuard().admit(_candidate())
    assert not admission.is_refusal
    assert admission.candidate is not None

    ledger = TraceLedger()
    audit = AnswerAudit(admission.candidate.completion, ledger)
    audited = audit.audit(
        _DECLARED_PROMPT, _gated_graph(), _gate(), Layer.CANDIDATE, _strong_evidence()
    )

    assert audited.answer == _DECLARED_ANSWER
    assert audited.gate_state is TransitionState.APPROVED
    assert audited.gamma_state is ClosureState.MINIMALLY_CLOSED
    assert audited.rank is Rank.HYPOTHESIS
    # The approval is the gate's, recorded by the audit shell — never
    # the guard's: the full gamma → gate → audit chain is on the
    # ledger (docs/18 §5; docs/07).
    assert len(ledger) == 3
    assert [entry.stage for entry in ledger.entries] == ["gamma", "gate", "audit"]
    assert_constitutional_case(case, _result_from(audited))


def test_admitted_adapter_still_walks_the_gate() -> None:
    """docs/18 §5 — admission is not approval: with empty evidence
    the gate defers exactly as for any other client; the admitted
    transport buys no shortcut past the kernel.
    """

    case = ConstitutionalChainTestCase(
        origin_law="docs/18 §5 — admission is not approval",
        branch_name="admitted-transport-gate-still-defers",
        constitutional_chain=(
            "ConcreteAdapterCandidate",
            "AdapterGuard",
            "ModelClient",
            "SlotGraph",
            "Gamma",
            "TransitionGate",
            "AuditedAnswer",
        ),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.GATE_REQUIRED,
        forbidden_outputs=("SUCCESSOR_SLOTGRAPH", "ADMITTED_APPROVAL"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="AdapterLicensingChain.step.4.AuditedAnswerOnly",
        origin_law_ref="docs/18_ADAPTER_BOUNDARY_LAW.md#5-admission-is-not-approval",
        branch_of_origin="GuardAdmitted → ApprovedAnswer stays forbidden.",
        forbidden_shortcut_assertions=("GuardAdmitted → ApprovedAnswer",),
    )
    admission = AdapterGuard().admit(_candidate())
    assert not admission.is_refusal
    assert admission.candidate is not None

    audit = AnswerAudit(admission.candidate.completion, TraceLedger())
    audited = audit.audit(
        _DECLARED_PROMPT, _gated_graph(), _gate(), Layer.CANDIDATE, EvidenceContract()
    )

    assert audited.gate_state is TransitionState.DEFERRED
    assert audited.successor is None
    assert audited.rank is Rank.ZERO
    assert_constitutional_case(case, _result_from(audited))


# ---------------------------------------------------------------------------
# 6. Static guards — the subpackage stays a transport (§4, §6).
# ---------------------------------------------------------------------------

_ADAPTER_MODULES = (
    "taaqqul_slot_geometry.adapters",
    "taaqqul_slot_geometry.adapters.adapter_boundary",
    "taaqqul_slot_geometry.adapters.in_memory",
)

# The PR-6 audit-layer set plus every filesystem / environment /
# process root docs/18 §4 leaves unlicensed for an IN_MEMORY
# transport (rule 5 — no I/O at all, rule 1 — not even at import).
_FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "anthropic",
    "http",
    "httpx",
    "openai",
    "os",
    "pathlib",
    "requests",
    "shutil",
    "socket",
    "sqlite3",
    "ssl",
    "subprocess",
    "sys",
    "tempfile",
    "urllib",
}

# Kernel judgment surfaces no transport may reference (docs/18 §6 —
# an adapter is a transport, not a judge): touching any of these
# would let an adapter judge, record, emit, or rank.
_FORBIDDEN_KERNEL_NAMES = {
    "AnswerAudit",
    "AuditedAnswer",
    "ClosureState",
    "Rank",
    "RankLattice",
    "SlotGraph",
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


def test_adapter_layer_ships_no_network_filesystem_or_provider_surface() -> None:
    """docs/18 §4 — IN_MEMORY means no I/O at all, ever.

    The whole subpackage must import no model SDK, no network stack,
    and no filesystem / environment / process surface — import-time
    I/O is forbidden too (§4 rule 1), so the imports themselves are
    the surface under test.
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
            f"{module_name} imports forbidden transport/provider modules: "
            f"{sorted(leaked)} (docs/18 §4)"
        )


def test_adapter_layer_never_touches_kernel_judgment_surfaces() -> None:
    """docs/18 §6, §8 — a transport cannot judge, record, emit, or
    rank: the subpackage must neither import nor reference ``Γ``,
    the gate, the ledger, the emission half, or the audit shell.
    """

    kernel_module_fragments = (
        "gamma",
        "slot_graph",
        "successor",
        "trace_ledger",
        "transition_gate",
    )
    for module_name in _ADAPTER_MODULES:
        imported: set[str] = set()
        referenced: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module)
                for alias in node.names:
                    referenced.add(alias.name)
            elif isinstance(node, ast.Name):
                referenced.add(node.id)
            elif isinstance(node, ast.Attribute):
                referenced.add(node.attr)
        touched = referenced & _FORBIDDEN_KERNEL_NAMES
        assert not touched, (
            f"{module_name} references kernel judgment surfaces: "
            f"{sorted(touched)} (docs/18 §6)"
        )
        for fragment in kernel_module_fragments:
            leaked = [module for module in imported if fragment in module]
            assert not leaked, (
                f"{module_name} imports kernel judgment modules: "
                f"{leaked} (docs/18 §6)"
            )
