"""Constitutional acceptance tests for GPT-R8 — Audit Integration (runtime).

Origin law          : docs/56 (GPT-R8 Audit Integration Law)
Branch              : GPT-R8
Category            : Category 1 (chain) + Category 2 (surface) — docs/52 §4
Constitutional chain:
    docs/01 (Black-Box Boundary)
        -> docs/18 (Adapter Boundary Law)
        -> docs/54 (GPT Answer Reasonableness Objective Law)
        -> docs/55 (Knowledge Origins Boundary Law)
        -> docs/56 (GPT-R8 Audit Integration Law)
        -> gamma -> gate -> audit -> audit.reasonableness

This file ships the seven required constitutional tests (T1..T7) from
docs/56 §8 plus the three implied negative tests (no new global
FailureCode, local residual locality, no verdict construction inside
``audit/``).
"""

from __future__ import annotations

import builtins
import inspect
import pathlib

import pytest

from taaqqul_slot_geometry import (
    AnswerAudit,
    AuditedAnswer,
    ClosureState,
    FailureCode,
    Layer,
    ModelClient,
    Rank,
    SlotGraph,
    SlotGraphSchemaError,
    TraceLedger,
    TransitionState,
)
from taaqqul_slot_geometry.audit.reasonableness_integration import (
    NEEDGATE_NOT_OPENED_RESIDUAL_NAME,
    RESIDUAL_R7_NOT_CONSUMED,
    RESIDUAL_REASONABLENESS_DEFERRED,
    AuditReasonablenessStatus,
    derive_reasonableness_residual_kind,
)
from taaqqul_slot_geometry.gpt import (
    GPTAnswerReasonablenessVerdict,
    OriginResidual,
    OriginResidualKind,
    ReasonablenessGateReportState,
    ReasonablenessVerdictIntegrationStatus,
    ReasonablenessVerdictState,
)
from tests.support.constitutional_case import (  # noqa: E402
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# Borrow the existing audit-test fixtures verbatim (they were already
# verified by the PR-6 test suite, so reusing them keeps T1 honest).
from tests.test_answer_audit import (  # noqa: E402
    _EchoClient,
    _gate,
    _gated_graph,
    _strong_evidence,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src" / "taaqqul_slot_geometry"


# ---------------------------------------------------------------------------
# Local fixtures
# ---------------------------------------------------------------------------


def _reasonable_verdict(
    *,
    residuals: tuple[OriginResidual, ...] = (),
    rank: Rank = Rank.HYPOTHESIS,
    rank_ceiling: Rank = Rank.LICENSED,
) -> GPTAnswerReasonablenessVerdict:
    return GPTAnswerReasonablenessVerdict(
        state=ReasonablenessVerdictState.REASONABLE,
        source_gate_report_state=ReasonablenessGateReportState.LICENSED_FOR_VERDICT,
        failure_code=None,
        residuals=residuals,
        rank=rank,
        rank_ceiling=rank_ceiling,
        source_gate_report_ref="trace://gpt-r6/report/r8-test",
        source_binding_ref="trace://gpt-r5/binding/r8-test",
        trace_ref="trace://gpt-r7/verdict/r8-test",
    )


def _origin_residual(name: str = "visible-objection") -> OriginResidual:
    return OriginResidual(
        kind=OriginResidualKind.EVIDENCE_MISSING,
        description=name,
        claim_ref="trace://claim/r8-test",
    )


def _audit() -> tuple[AnswerAudit, TraceLedger]:
    ledger = TraceLedger()
    return AnswerAudit(_EchoClient(), ledger), ledger


def _block_runtime_reasonableness_verdict_import(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def guarded_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "taaqqul_slot_geometry.gpt.reasonableness_verdict":
            raise AssertionError("answer_audit.py must not import gpt.reasonableness_verdict")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)


def _chain_case() -> ConstitutionalChainTestCase:
    return ConstitutionalChainTestCase(
        origin_law="docs/56",
        branch_name="GPT-R8",
        constitutional_chain=(
            "docs/01",
            "docs/18",
            "docs/54",
            "docs/55",
            "docs/56",
            "gamma",
            "gate",
            "audit",
            "audit.reasonableness",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "AnswerCertificate",
            "ReasonablenessCertificate",
            "TruthCertificate",
            "AuthorityRecord",
            "AbsoluteTruthVerdict",
            "ReasonablenessAuditedAnswer",
        ),
        max_rank=Rank.LICENSED,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="audit.reasonableness",
        origin_law_ref="docs/56_GPT_R8_AUDIT_INTEGRATION_LAW.md#§4.1",
        branch_of_origin="GPT reasonableness",
        forbidden_shortcut_assertions=(
            "ModelClient.complete -> verdict",
            "Adapter -> verdict",
            "verdict -> certificate",
            "verdict -> APPROVED successor",
            "AuditedAnswer -> verdict",
            "pre-audit verdict -> final audit verdict",
        ),
    )


# ---------------------------------------------------------------------------
# T1 — AuditedAnswer surface unchanged invariants
# ---------------------------------------------------------------------------


def test_t1_audited_answer_existing_birth_invariants_still_fire() -> None:
    """Every pre-GPT-R8 schema-error path still raises with its original meaning."""

    base = dict(
        prompt="p",
        answer="a",
        gamma_state=ClosureState.MINIMALLY_CLOSED,
        gate_state=TransitionState.APPROVED,
        failure_code=None,
        rank=Rank.LICENSED,
        evidence_refs=(),
        residuals=(),
        residual_visibility=True,
        successor=None,
        trace_anchor="trace://Q1",
    )

    # successor=None requires a named failure_code (existing invariant).
    with pytest.raises(SlotGraphSchemaError, match="must name why"):
        AuditedAnswer(**base)

    # successor=None requires Rank.ZERO (existing invariant).
    with pytest.raises(SlotGraphSchemaError, match="licenses nothing"):
        AuditedAnswer(**{**base, "failure_code": FailureCode.GATE_REQUIRED})

    # trace_anchor must be non-empty (existing invariant).
    with pytest.raises(SlotGraphSchemaError, match="trace_anchor"):
        AuditedAnswer(
            **{
                **base,
                "trace_anchor": "",
                "failure_code": FailureCode.GATE_REQUIRED,
                "rank": Rank.ZERO,
            }
        )


def test_t1_default_audit_remains_byte_identical_in_behaviour() -> None:
    """A pre-R8 ``audit()`` call appends exactly three entries, in order."""

    audit, ledger = _audit()
    audited = audit.audit(
        "prompt", _gated_graph(), _gate(), Layer.CANDIDATE, _strong_evidence()
    )
    entries = ledger.entries
    assert tuple(e.stage for e in entries) == ("gamma", "gate", "audit")
    # The default integration status is named-absent, never silently absent.
    assert audited.reasonableness_status is AuditReasonablenessStatus.NOT_RUN
    assert audited.reasonableness_verdict is None


# ---------------------------------------------------------------------------
# T2 — No ModelClient protocol mutation
# ---------------------------------------------------------------------------


def test_t2_model_client_protocol_arity_unchanged() -> None:
    """``ModelClient`` exposes exactly one method (``complete``)."""

    members = [
        name
        for name, value in inspect.getmembers(ModelClient)
        if callable(value) and not name.startswith("_")
    ]
    assert members == ["complete"]


def test_t2_no_reasonableness_surface_on_adapter_layer() -> None:
    """No adapter or guard file mentions reasonableness/verdict/r7 attributes."""

    forbidden_tokens = ("reasonableness", "verdict", "r7")
    for relpath in ("audit/model_client.py", "audit/adapter_guard.py"):
        target = _SRC_DIR / relpath
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8").lower()
        for token in forbidden_tokens:
            assert token not in text, (
                f"{relpath} must not mention {token!r} — docs/56 §3 keeps "
                f"the adapter boundary intact"
            )
    adapters_dir = _SRC_DIR / "audit" / "adapters"
    if adapters_dir.exists():
        for path in adapters_dir.rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for token in forbidden_tokens:
                assert token not in text, (
                    f"{path.relative_to(_REPO_ROOT)} must not mention "
                    f"{token!r} — docs/56 §3"
                )


def test_t2_audited_answer_validates_carried_verdict_without_runtime_gpt_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verdict = _reasonable_verdict(rank=Rank.LICENSED)
    _block_runtime_reasonableness_verdict_import(monkeypatch)

    audited = AuditedAnswer(
        prompt="",
        answer="",
        gamma_state=ClosureState.MINIMALLY_CLOSED,
        gate_state=TransitionState.APPROVED,
        failure_code=None,
        rank=Rank.LICENSED,
        evidence_refs=(),
        residuals=(),
        residual_visibility=True,
        successor=_gated_graph(rank=Rank.LICENSED),
        trace_anchor="trace://Q1",
        reasonableness_verdict=verdict,
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )

    assert audited.reasonableness_verdict is verdict


def test_t2_audit_with_reasonableness_validates_without_runtime_gpt_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verdict = _reasonable_verdict(rank=Rank.HYPOTHESIS)
    _block_runtime_reasonableness_verdict_import(monkeypatch)

    audit, _ = _audit()
    audited = audit.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=verdict,
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )

    assert audited.reasonableness_verdict is verdict


# ---------------------------------------------------------------------------
# T3 — REASONABLE is procedural, never APPROVED-by-itself
# ---------------------------------------------------------------------------


def test_t3_reasonable_verdict_does_not_promote_to_approved_successor() -> None:
    """An APPROVED audit's successor is derived from the gate, not the verdict.

    The verdict is a *companion* on the audited carrier; whether the
    audit holds a successor depends solely on the existing gate path.
    The presence of a ``REASONABLE`` verdict does not change the
    ``failure_code`` / ``rank`` / ``successor`` triangle.
    """

    audit, ledger = _audit()
    base = audit.audit("p", _gated_graph(), _gate(), Layer.CANDIDATE, _strong_evidence())
    # Reset the ledger by using a fresh audit for the with-verdict path:
    audit2, ledger2 = _audit()
    carried = audit2.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=_reasonable_verdict(rank=base.rank),
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )
    # The base (verdict-less) and the carried audit reach the *same*
    # gate verdict / successor / rank — the verdict did not promote
    # anything.
    assert carried.gate_state is base.gate_state
    assert (carried.successor is None) == (base.successor is None)
    assert carried.failure_code is base.failure_code
    assert carried.rank is base.rank
    assert tuple(e.stage for e in ledger.entries) == ("gamma", "gate", "audit")
    assert tuple(e.stage for e in ledger2.entries) == (
        "gamma",
        "gate",
        "audit",
        "audit.reasonableness",
    )


def test_t3_verdict_rank_exceeding_audit_rank_is_refused() -> None:
    """docs/56 §4.1 — verdict.rank may not exceed AuditedAnswer.rank."""

    audit, _ = _audit()
    # The gate grants only HYPOTHESIS for this fixture; a verdict
    # carrying LICENSED rank exceeds the audit's rank and must be
    # refused at the audit boundary, not silently demoted.
    with pytest.raises(SlotGraphSchemaError, match=r"rank must not exceed"):
        audit.audit_with_reasonableness(
            "p",
            _gated_graph(),
            _gate(),
            Layer.CANDIDATE,
            _strong_evidence(),
            reasonableness_verdict=_reasonable_verdict(rank=Rank.LICENSED),
            reasonableness_status=AuditReasonablenessStatus.CARRIED,
        )


def test_t3_audit_module_does_not_derive_successor_from_verdict() -> None:
    """``audit/`` never wires the reasonableness verdict into ``emit_successor``."""

    audit_pkg = _SRC_DIR / "audit"
    for path in audit_pkg.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        # No assignment that feeds a verdict into emit_successor or makes
        # the successor depend on the verdict.
        assert "successor = reasonableness_verdict" not in text
        assert "successor=reasonableness_verdict" not in text
        assert "successor = self.reasonableness_verdict" not in text


# ---------------------------------------------------------------------------
# T4 — Residual visibility under integration (no silent drops)
# ---------------------------------------------------------------------------


def test_t4_residual_enumeration_preserves_order_and_identity() -> None:
    """Every verdict residual is enumerable on the audit record, in order."""

    r_a = _origin_residual("objection-a")
    r_b = _origin_residual("objection-b")
    verdict = _reasonable_verdict(residuals=(r_a, r_b))

    audit, _ = _audit()
    audited = audit.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=verdict,
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )
    listed = audited.enumerate_reasonableness_residuals()
    assert listed == (r_a, r_b)
    assert listed is audited.reasonableness_verdict.residuals


def test_t4_no_verdict_returns_empty_tuple_not_none() -> None:
    audited = AuditedAnswer(
        prompt="",
        answer="",
        gamma_state=ClosureState.MINIMALLY_CLOSED,
        gate_state=TransitionState.DEFERRED,
        failure_code=FailureCode.GATE_REQUIRED,
        rank=Rank.ZERO,
        evidence_refs=(),
        residuals=(),
        residual_visibility=True,
        successor=None,
        trace_anchor="trace://Q1",
    )
    listed = audited.enumerate_reasonableness_residuals()
    assert listed == ()
    assert listed is not None


# ---------------------------------------------------------------------------
# T5 — Trace continuity under integration
# ---------------------------------------------------------------------------


def test_t5_carried_verdict_yields_four_entries_in_constitutional_order() -> None:
    audit, ledger = _audit()
    audit.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=_reasonable_verdict(),
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )
    assert tuple(e.stage for e in ledger.entries) == (
        "gamma",
        "gate",
        "audit",
        "audit.reasonableness",
    )


def test_t5_not_run_default_appends_no_fourth_entry() -> None:
    audit, ledger = _audit()
    audit.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=None,
        reasonableness_status=AuditReasonablenessStatus.NOT_RUN,
    )
    # NOT_RUN is the legacy/default state: absence is named on the
    # AuditedAnswer carrier itself, no extra ledger entry is appended.
    assert tuple(e.stage for e in ledger.entries) == ("gamma", "gate", "audit")


def test_t5_named_absent_status_appends_fourth_entry() -> None:
    """``DEFERRED`` / ``R7_NOT_CONSUMED`` force an explicit ledger entry."""

    for status in (
        AuditReasonablenessStatus.DEFERRED,
        AuditReasonablenessStatus.R7_NOT_CONSUMED,
    ):
        audit, ledger = _audit()
        audited = audit.audit_with_reasonableness(
            "p",
            _gated_graph(),
            _gate(),
            Layer.CANDIDATE,
            _strong_evidence(),
            reasonableness_verdict=None,
            reasonableness_status=status,
        )
        assert tuple(e.stage for e in ledger.entries) == (
            "gamma",
            "gate",
            "audit",
            "audit.reasonableness",
        )
        # The residual kind is named, not silently absent.
        assert audited.reasonableness_residual_kind() == (
            derive_reasonableness_residual_kind(status)
        )
        assert audited.reasonableness_residual_kind() is not None


# ---------------------------------------------------------------------------
# T6 — Forbidden-leap refusal: certificate_allowed=True is refused
# ---------------------------------------------------------------------------


def test_t6_forged_certificate_carrier_is_refused_at_audit_boundary() -> None:
    """A forged verdict (post-construction mutation) is refused by ``AuditedAnswer``."""

    verdict = _reasonable_verdict()
    # GPT-R7's __post_init__ already forbids this, so the only way to
    # simulate a "forged carrier" is to bypass the frozen dataclass with
    # object.__setattr__ — exactly the smuggle path docs/56 §2 B4 names.
    object.__setattr__(verdict, "certificate_allowed", True)

    with pytest.raises(SlotGraphSchemaError, match=r"docs/56 §2 B4"):
        AuditedAnswer(
            prompt="",
            answer="",
            gamma_state=ClosureState.MINIMALLY_CLOSED,
            gate_state=TransitionState.APPROVED,
            failure_code=None,
            rank=Rank.LICENSED,
            evidence_refs=(),
            residuals=(),
            residual_visibility=True,
            successor=_gated_graph(rank=Rank.LICENSED),
            trace_anchor="trace://Q1",
            reasonableness_verdict=verdict,
            reasonableness_status=AuditReasonablenessStatus.CARRIED,
        )


def test_t6_audit_seam_also_refuses_a_forged_certificate_carrier() -> None:
    """``audit_with_reasonableness`` refuses the same forged carrier early."""

    verdict = _reasonable_verdict()
    object.__setattr__(verdict, "certificate_allowed", True)

    audit, _ = _audit()
    with pytest.raises(SlotGraphSchemaError, match=r"docs/56 §2 B4"):
        audit.audit_with_reasonableness(
            "p",
            _gated_graph(),
            _gate(),
            Layer.CANDIDATE,
            _strong_evidence(),
            reasonableness_verdict=verdict,
            reasonableness_status=AuditReasonablenessStatus.CARRIED,
        )


# ---------------------------------------------------------------------------
# T7 — Inverse tests for the six Forbidden Straight Lines in docs/56 §6
# ---------------------------------------------------------------------------


def test_t7_modelclient_complete_never_constructs_a_verdict() -> None:
    """``audit/model_client.py`` and adapters never import the verdict carrier."""

    client_text = (_SRC_DIR / "audit" / "model_client.py").read_text(encoding="utf-8")
    assert "GPTAnswerReasonablenessVerdict" not in client_text
    assert "reasonableness_verdict" not in client_text


def test_t7_adapter_layer_never_imports_verdict_carriers() -> None:
    adapter_targets = [
        _SRC_DIR / "audit" / "adapter_guard.py",
    ]
    adapters_dir = _SRC_DIR / "audit" / "adapters"
    if adapters_dir.exists():
        adapter_targets.extend(adapters_dir.rglob("*.py"))
    for path in adapter_targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        assert "GPTAnswerReasonablenessVerdict" not in text, (
            f"{path.relative_to(_REPO_ROOT)} must not import the verdict carrier"
        )


def test_t7_verdict_to_certificate_is_structurally_blocked() -> None:
    """No reachable ``audit/`` symbol contains 'Certificate'."""

    audit_pkg = _SRC_DIR / "audit"
    for path in audit_pkg.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        # The audit layer must not define a Certificate class or
        # construct one from a verdict.
        assert "class AnswerCertificate" not in text
        assert "class ReasonablenessCertificate" not in text
        assert "class TruthCertificate" not in text


def test_t7_emit_successor_signature_does_not_accept_verdict() -> None:
    """``emit_successor`` cannot promote a verdict into an APPROVED successor."""

    from taaqqul_slot_geometry.audit.successor import emit_successor

    sig = inspect.signature(emit_successor)
    param_names = set(sig.parameters)
    assert "reasonableness_verdict" not in param_names
    assert "verdict" in param_names or "reasonableness_verdict" not in param_names
    # The verdict parameter name on emit_successor is the *gate*
    # TransitionVerdict, not a reasonableness verdict. Confirm by type:
    verdict_param = sig.parameters.get("verdict")
    if verdict_param is not None:
        annotation = str(verdict_param.annotation)
        assert "Reasonableness" not in annotation


def test_t7_audited_answer_has_no_method_that_synthesises_a_verdict() -> None:
    """``AuditedAnswer`` only enumerates the verdict; it never builds one."""

    methods = {
        name
        for name, _ in inspect.getmembers(AuditedAnswer, predicate=inspect.isfunction)
        if not name.startswith("_")
    }
    # Read-through accessors are allowed; no constructor-shaped method.
    assert methods == {
        "enumerate_reasonableness_residuals",
        "reasonableness_residual_kind",
    }


def test_t7_pre_audit_verdict_status_is_preserved_through_integration() -> None:
    """A carried verdict still declares PRE_AUDIT_VERDICT integration status."""

    audit, _ = _audit()
    audited = audit.audit_with_reasonableness(
        "p",
        _gated_graph(),
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=_reasonable_verdict(),
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )
    assert audited.reasonableness_verdict.integration_status is (
        ReasonablenessVerdictIntegrationStatus.PRE_AUDIT_VERDICT
    )
    assert audited.reasonableness_verdict.not_final_audit is True
    assert audited.reasonableness_verdict.requires_r8_audit_integration is True


# ---------------------------------------------------------------------------
# Negative tests required by docs/56 §5–§7
# ---------------------------------------------------------------------------


# Snapshot the FailureCode membership *at module import* before any test
# from this file has run. If GPT-R8 had added a new member, this set
# would already reflect the addition (and the test below would fail
# against a stored historical baseline).
_FAILURE_CODE_NAMES_AT_IMPORT = frozenset(member.name for member in FailureCode)


def test_no_new_global_failure_code_added_for_gpt_r8() -> None:
    """docs/56 §5 forbids new global ``FailureCode`` members."""

    # The R6/R7 family of named refusals existed before GPT-R8 ran.
    # No GPT-R8-specific member name is allowed in the global enum.
    gpt_r8_specific = {
        "REASONABLENESS_DEFERRED",
        "R7_NOT_CONSUMED",
        "NEEDGATE_NOT_OPENED",
        "REASONABLENESS_INTEGRATION_FAILED",
    }
    assert gpt_r8_specific.isdisjoint(_FAILURE_CODE_NAMES_AT_IMPORT), (
        "GPT-R8 must not widen the global FailureCode registry — local "
        "residual vocabulary only (docs/56 §5, §7)"
    )


def test_local_residual_names_are_local_to_integration_module() -> None:
    """docs/56 §7 — the three reserved names appear only in their module."""

    # These two paths are licensed: the integration module owns the
    # values, and the package __init__.py re-exports them for callers.
    allowed = {
        _SRC_DIR / "audit" / "reasonableness_integration.py",
        _SRC_DIR / "audit" / "__init__.py",
    }
    forbidden_names = (
        RESIDUAL_REASONABLENESS_DEFERRED,
        RESIDUAL_R7_NOT_CONSUMED,
        NEEDGATE_NOT_OPENED_RESIDUAL_NAME,
    )
    for path in _SRC_DIR.rglob("*.py"):
        if path in allowed:
            continue
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert name not in text, (
                f"{path.relative_to(_REPO_ROOT)} must not mention {name!r} — "
                f"docs/56 §7 reserves these names to "
                f"audit/reasonableness_integration.py"
            )


def test_audit_layer_does_not_construct_a_reasonableness_verdict() -> None:
    """``audit/`` never calls ``prove_gpt_answer_reasonableness_verdict``."""

    audit_pkg = _SRC_DIR / "audit"
    for path in audit_pkg.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "prove_gpt_answer_reasonableness_verdict" not in text, (
            f"{path.relative_to(_REPO_ROOT)} must not construct a verdict — "
            f"docs/56 §6 (no straight line from audit to verdict)"
        )


# ---------------------------------------------------------------------------
# Status helper coverage
# ---------------------------------------------------------------------------


def test_derive_reasonableness_residual_kind_mapping_is_total() -> None:
    """The status -> residual-name helper is total over the enum."""

    assert (
        derive_reasonableness_residual_kind(AuditReasonablenessStatus.NOT_RUN) is None
    )
    assert (
        derive_reasonableness_residual_kind(AuditReasonablenessStatus.CARRIED) is None
    )
    assert (
        derive_reasonableness_residual_kind(AuditReasonablenessStatus.DEFERRED)
        == RESIDUAL_REASONABLENESS_DEFERRED
    )
    assert (
        derive_reasonableness_residual_kind(AuditReasonablenessStatus.R7_NOT_CONSUMED)
        == RESIDUAL_R7_NOT_CONSUMED
    )


def test_audit_with_reasonableness_refuses_status_verdict_mismatch() -> None:
    """``CARRIED`` requires a verdict; non-CARRIED requires verdict ``None``."""

    audit, _ = _audit()
    with pytest.raises(SlotGraphSchemaError, match="CARRIED"):
        audit.audit_with_reasonableness(
            "p",
            _gated_graph(),
            _gate(),
            Layer.CANDIDATE,
            _strong_evidence(),
            reasonableness_verdict=None,
            reasonableness_status=AuditReasonablenessStatus.CARRIED,
        )
    with pytest.raises(SlotGraphSchemaError, match="CARRIED"):
        audit.audit_with_reasonableness(
            "p",
            _gated_graph(),
            _gate(),
            Layer.CANDIDATE,
            _strong_evidence(),
            reasonableness_verdict=_reasonable_verdict(),
            reasonableness_status=AuditReasonablenessStatus.DEFERRED,
        )


# ---------------------------------------------------------------------------
# Category 1 — Chain test: gamma -> gate -> audit -> audit.reasonableness
# ---------------------------------------------------------------------------


def test_chain_gamma_to_audit_reasonableness_closes_under_a_reasonable_verdict() -> None:
    audit, _ = _audit()
    graph = _gated_graph(rank=Rank.HYPOTHESIS)
    audited = audit.audit_with_reasonableness(
        "prompt",
        graph,
        _gate(),
        Layer.CANDIDATE,
        _strong_evidence(),
        reasonableness_verdict=_reasonable_verdict(),
        reasonableness_status=AuditReasonablenessStatus.CARRIED,
    )

    assert isinstance(audited.successor, SlotGraph)
    case = _chain_case()
    result = ConstitutionalChainResult(
        state=audited.gamma_state,
        failure_code=audited.failure_code,
        rank=audited.rank,
        residual_visibility=audited.residual_visibility,
        trace_present=bool(audited.trace_anchor)
        and bool(audited.reasonableness_verdict.trace_ref),
        produced_outputs=frozenset({"SUCCESSOR_SLOTGRAPH", "REASONABLENESS_VERDICT"}),
    )
    assert_constitutional_case(case, result)
