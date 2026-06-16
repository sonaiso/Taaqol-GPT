"""Acceptance tests for docs/53 — Project Methodology, Objectives, and KPI Plan.

These are Layer 1 (document existence) and Layer 2 (contract surface)
tests per docs/53 §12.1. They verify that docs/53 exists and contains
the constitutionally required sections.

Origin law     : docs/53 (Project Methodology, Objectives, and KPI Plan)
Branch         : CLOSE-2 (project methodology contract)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

_DOCS_DIR = pathlib.Path(__file__).resolve().parent.parent / "docs"
_DOC_53 = _DOCS_DIR / "53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md"


# ---------------------------------------------------------------------------
# Layer 1 — Document existence
# ---------------------------------------------------------------------------


class TestDocs53Exists:
    """docs/53 must exist as the methodology/objectives/KPI document."""

    def test_docs_53_exists(self) -> None:
        assert _DOC_53.exists(), (
            "docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md must exist"
        )

    def test_docs_53_is_not_empty(self) -> None:
        content = _DOC_53.read_text(encoding="utf-8")
        assert len(content) > 100, "docs/53 must not be empty"


# ---------------------------------------------------------------------------
# Layer 2 — Contract surface (required sections)
# ---------------------------------------------------------------------------


def _read_doc() -> str:
    """Read docs/53 content, skipping if missing."""
    if not _DOC_53.exists():
        pytest.skip("docs/53 not yet created")
    return _DOC_53.read_text(encoding="utf-8")


class TestDocs53DeclaresProjectOrigin:
    """docs/53 must declare the project's governing origin."""

    def test_docs_53_declares_project_origin(self) -> None:
        content = _read_doc()
        assert "Governing Origin" in content or "governing origin" in content, (
            "docs/53 must declare the project's governing origin (§1)"
        )

    def test_docs_53_origin_mentions_trace(self) -> None:
        content = _read_doc()
        assert "No output without Trace" in content or "No output without trace" in content, (
            "docs/53 origin must include trace requirement"
        )


class TestDocs53DeclaresLicensedInputs:
    """docs/53 must declare licensed inputs."""

    def test_docs_53_declares_licensed_inputs(self) -> None:
        content = _read_doc()
        assert "Licensed Inputs" in content or "licensed inputs" in content, (
            "docs/53 must have a Licensed Inputs section (§3)"
        )

    def test_docs_53_forbids_raw_text_to_meaning(self) -> None:
        content = _read_doc()
        assert "Raw text" in content or "raw_text" in content or "raw text" in content, (
            "docs/53 must forbid raw text as ontological origin"
        )


class TestDocs53DeclaresLicensedOutputs:
    """docs/53 must declare licensed outputs."""

    def test_docs_53_declares_licensed_outputs(self) -> None:
        content = _read_doc()
        assert "Licensed Outputs" in content or "licensed outputs" in content, (
            "docs/53 must have a Licensed Outputs section (§4)"
        )


class TestDocs53DeclaresForbiddenOutputs:
    """docs/53 must declare forbidden outputs with named symbols."""

    def test_docs_53_declares_forbidden_outputs(self) -> None:
        content = _read_doc()
        assert "Forbidden Outputs" in content or "forbidden outputs" in content, (
            "docs/53 must have a Forbidden Outputs section (§5)"
        )

    def test_docs_53_has_at_least_10_forbidden_symbols(self) -> None:
        content = _read_doc()
        # Count FO-N patterns
        fo_count = content.count("FO-")
        assert fo_count >= 10, (
            f"docs/53 must declare at least 10 forbidden output symbols, found {fo_count}"
        )

    def test_docs_53_forbids_candidate_certificate_leap(self) -> None:
        content = _read_doc()
        assert "candidate" in content.lower() and "certificate" in content.lower(), (
            "docs/53 must forbid candidate → certificate leap"
        )


class TestDocs53DeclaresBranchContract:
    """docs/53 must declare the BranchContract template."""

    def test_docs_53_declares_branch_contract(self) -> None:
        content = _read_doc()
        assert "BranchContract" in content, (
            "docs/53 must declare the BranchContract template (§8)"
        )

    def test_docs_53_branch_contract_has_14_fields(self) -> None:
        content = _read_doc()
        required_fields = [
            "original_origin",
            "branch_name",
            "sabab",
            "shart",
            "mani",
            "input_contract",
            "output_contract",
            "forbidden_outputs",
            "evidence_contract",
            "rank_ceiling",
            "residual_policy",
            "trace_contract",
            "upstream_dependency",
            "downstream_effect",
        ]
        for field in required_fields:
            assert field in content, (
                f"BranchContract must declare field '{field}'"
            )

    def test_docs_53_branch_not_admitted(self) -> None:
        content = _read_doc()
        assert "BRANCH_NOT_ADMITTED" in content, (
            "docs/53 must declare BRANCH_NOT_ADMITTED verdict"
        )


class TestDocs53DeclaresKpiMatrix:
    """docs/53 must declare the KPI matrix."""

    def test_docs_53_declares_kpi_matrix(self) -> None:
        content = _read_doc()
        assert "KPI Matrix" in content or "KPI matrix" in content, (
            "docs/53 must have a KPI Matrix section (§11)"
        )

    def test_docs_53_kpi_has_strategic_objectives(self) -> None:
        content = _read_doc()
        assert "SO-1" in content and "SO-5" in content, (
            "KPI matrix must reference strategic objectives SO-1 through SO-5"
        )

    def test_docs_53_kpi_has_long_term_objectives(self) -> None:
        content = _read_doc()
        assert "LTO-1" in content and "LTO-4" in content, (
            "KPI matrix must reference long-term objectives"
        )

    def test_docs_53_kpi_has_medium_term_objectives(self) -> None:
        content = _read_doc()
        assert "MTO-1" in content and "MTO-4" in content, (
            "KPI matrix must reference medium-term objectives"
        )


class TestDocs53DeclaresFutureBranchOriginRule:
    """docs/53 must declare the future branch admission rule."""

    def test_docs_53_declares_future_branch_origin_rule(self) -> None:
        content = _read_doc()
        assert "Branch Admission" in content or "branch admission" in content, (
            "docs/53 must declare the future branch admission rule (§13)"
        )

    def test_docs_53_admission_requires_12_questions(self) -> None:
        content = _read_doc()
        # The 12 admission questions should be enumerated
        assert "1." in content and "12." in content, (
            "docs/53 admission rule must enumerate 12 questions"
        )
