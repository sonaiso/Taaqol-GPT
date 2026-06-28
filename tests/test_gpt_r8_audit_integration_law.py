"""Acceptance tests for docs/56 — GPT-R8 Audit Integration Law.

Origin law     : docs/56 (GPT-R8 Audit Integration Law)
Branch         : GPT-R8L (law-only audit-integration licensing)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
Constitutional chain:
    docs/01 (Black-Box Boundary)
        -> docs/18 (Adapter Boundary Law)
        -> docs/54 (GPT Answer Reasonableness Objective Law)
        -> docs/55 (Knowledge Origins Boundary Law)
        -> docs/56 (GPT-R8 Audit Integration Law, this document)
        -> GPT-R8 (runtime, deferred)

These tests verify the law-only surface only. They do not import any
runtime code, do not exercise AnswerAudit, and do not run a verdict.
"""

from __future__ import annotations

import pathlib
import re

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOCS_DIR = _REPO_ROOT / "docs"
_DOC_56 = _DOCS_DIR / "56_GPT_R8_AUDIT_INTEGRATION_LAW.md"
_DOC_14 = _DOCS_DIR / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_README = _REPO_ROOT / "README.md"
_SRC_DIR = _REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _read_doc_56() -> str:
    assert _DOC_56.exists(), "docs/56 must exist for GPT-R8L acceptance tests"
    return _DOC_56.read_text(encoding="utf-8")


# --- Law surface ------------------------------------------------------------


def test_docs_56_exists_as_law_only_surface() -> None:
    content = _read_doc_56()
    assert "law-only" in content
    assert "does **not** add runtime code" in content
    assert "mutate `AnswerAudit.audit()`" in content
    assert "does **not** introduce new" in content
    assert "FailureCode" in content


def test_law_cites_constitutional_origins() -> None:
    content = _read_doc_56()
    for origin in (
        "docs/01",
        "docs/07",
        "docs/18",
        "docs/46",
        "docs/47",
        "docs/54",
        "docs/55",
    ):
        assert origin in content, f"docs/56 must cite {origin}"


def test_six_inviolable_integration_boundaries_are_named() -> None:
    content = _read_doc_56()
    for tag in ("B1", "B2", "B3", "B4", "B5", "B6"):
        assert re.search(rf"\b{tag}\b", content), f"boundary tag {tag} missing"
    # The B4 anti-truth declaration must be explicit.
    assert "No certificate, no authority, no truth" in content
    # B2 ownership of ledger writes must be explicit.
    assert "AnswerAudit owns the only TraceLedger writes" in content


def test_adapter_boundary_clarifications_are_explicit() -> None:
    content = _read_doc_56()
    assert "ModelClient" in content
    assert "AdapterGuard" in content
    assert "MUST NOT add a new method to the" in content
    assert "ModelClient protocol" in content
    assert "complete(prompt: str) -> str" in content


def test_two_licensed_integration_shapes_are_declared() -> None:
    content = _read_doc_56()
    assert "Shape A" in content
    assert "Shape B" in content
    assert "Additive Field on `AuditedAnswer`" in content
    assert "Sibling Wrapper Over `AuditedAnswer`" in content
    # No third shape.
    assert "no third shape is licensed" in content


def test_forbidden_outputs_include_certificate_and_authority() -> None:
    content = _read_doc_56()
    for forbidden in (
        "AnswerCertificate",
        "ReasonablenessCertificate",
        "TruthCertificate",
        "AuthorityRecord",
        "AbsoluteTruthVerdict",
    ):
        assert forbidden in content, f"forbidden output {forbidden} must be named"


def test_forbidden_straight_lines_inverse_tests_are_named() -> None:
    content = _read_doc_56()
    for line in (
        "ModelClient.complete -> Reasonableness verdict",
        "Adapter -> Reasonableness verdict",
        "Reasonableness verdict -> Certificate",
        "Reasonableness verdict -> Approved successor",
        "AuditedAnswer -> Reasonableness verdict",
        "Pre-audit verdict -> Final audit verdict",
    ):
        assert line in content, f"forbidden straight line missing: {line}"


def test_local_residual_vocabulary_is_reserved() -> None:
    content = _read_doc_56()
    for residual in (
        "RESIDUAL_REASONABLENESS_DEFERRED",
        "RESIDUAL_NEEDGATE_NOT_OPENED",
        "RESIDUAL_R7_NOT_CONSUMED",
    ):
        assert residual in content
    # The residuals must be declared local, not global.
    assert "widen the global residual policy" in content


def test_constitutional_tests_required_are_enumerated() -> None:
    content = _read_doc_56()
    for tag in ("T1", "T2", "T3", "T4", "T5", "T6", "T7"):
        assert re.search(rf"\b{tag}\b", content), f"required-test tag {tag} missing"
    assert "ConstitutionalTestCase" in content
    assert "origin_law=docs/56" in content


def test_kpi_table_is_present_and_zero_targets_declared() -> None:
    content = _read_doc_56()
    assert "KPI" in content
    for must_be_zero in (
        "Reasonableness → APPROVED auto-promotions",
        "Residual silent drops at integration boundary",
        "Certificate / authority promotions",
        "New global FailureCode members",
    ):
        assert must_be_zero in content
    # No-mutation invariant.
    assert "ModelClient protocol arity unchanged" in content


def test_binding_declarations_close_the_law() -> None:
    content = _read_doc_56()
    assert "GPT-R8L licenses GPT-R8 and nothing else" in content
    assert "No global FailureCode expansion is licensed by this law" in content
    assert "No mutation of the ModelClient protocol is licensed" in content


# --- Chain-state coherence --------------------------------------------------


def test_roadmap_registers_gpt_r8l_as_current_and_keeps_gpt_r8_as_next() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    assert re.search(
        r"GPT-R8L\s+GPT-R8 Audit Integration Law\s+→ current", doc_14
    )
    assert re.search(r"GPT-R8\s+Audit Integration\s+→ next", doc_14)
    # The §1 per-step boundary blocks must both exist.
    assert "GPT-R8L\n    Origin   :" in doc_14
    assert "GPT-R8\n    Origin   :" in doc_14
    # The Amendment record must be registered.
    assert "Amendment-49 (GPT-R8L" in doc_14


def test_claude_md_pr_staging_mirrors_chain_state() -> None:
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")
    assert re.search(
        r"GPT-R8L\s+GPT-R8 Audit Integration Law\s+→ current", claude_md
    )
    assert re.search(r"GPT-R8 Audit Integration\s+→ next", claude_md)


def test_readme_reflects_law_step_is_current() -> None:
    readme = _README.read_text(encoding="utf-8")
    assert "GPT-R8L" in readme
    assert "docs/56" in readme
    assert "`GPT-R8` audit integration is now next" in readme


def test_reading_order_includes_doc_56() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    assert (
        "docs/56_GPT_R8_AUDIT_INTEGRATION_LAW.md   (GPT-R8 audit integration law)"
        in doc_14
    )


# --- No-runtime-leak guard --------------------------------------------------


def test_no_runtime_code_added_for_gpt_r8l() -> None:
    """GPT-R8L is law-only. No src/ file may carry an R8L runtime symbol."""

    forbidden_symbols = (
        "GptR8AuditIntegration",
        "R8AuditIntegration",
        "ReasonablenessAuditedAnswer",
    )
    for path in _SRC_DIR.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for symbol in forbidden_symbols:
            assert symbol not in text, (
                f"GPT-R8L is law-only; runtime symbol {symbol!r} must not appear "
                f"in {path.relative_to(_REPO_ROOT)}"
            )


def test_model_client_protocol_arity_unchanged() -> None:
    """Constitutional invariant: GPT-R8L must not mutate the protocol."""

    model_client = (_SRC_DIR / "audit" / "model_client.py").read_text(encoding="utf-8")
    # Exactly one method on the ModelClient protocol: complete().
    method_defs = re.findall(r"^\s{4}def\s+(\w+)\s*\(", model_client, re.MULTILINE)
    assert method_defs.count("complete") == 1, (
        "ModelClient.complete must remain the only protocol method (docs/56 §3)"
    )
    # No new method named after reasonableness/verdict surfaces snuck in.
    for forbidden in ("reasonableness", "verdict", "audit_reasonableness"):
        assert forbidden not in method_defs, (
            f"ModelClient must not gain a {forbidden!r} method (docs/56 §3)"
        )


def test_audited_answer_surface_unchanged_for_gpt_r8l() -> None:
    """GPT-R8L is law-only: AuditedAnswer must not carry an R7 verdict field yet."""

    answer_audit = (_SRC_DIR / "audit" / "answer_audit.py").read_text(encoding="utf-8")
    for forbidden_field in (
        "reasonableness_verdict",
        "gpt_reasonableness_verdict",
        "r7_verdict",
    ):
        assert forbidden_field not in answer_audit, (
            f"GPT-R8L is law-only; AuditedAnswer must not yet carry "
            f"{forbidden_field!r} (that is GPT-R8 runtime work)"
        )
