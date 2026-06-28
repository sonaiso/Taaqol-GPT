"""Acceptance tests for docs/65 — Local Dynamic Web Matrix Record.

Origin law     : docs/65 (Local Dynamic Web Matrix Record)
Branch         : WEB-M0 (law-only public-readiness matrix record)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "65_LOCAL_DYNAMIC_WEB_MATRIX_RECORD.md"
ROADMAP = ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
WEBSITE_JS = ROOT / "website" / "app.js"


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/65_LOCAL_DYNAMIC_WEB_MATRIX_RECORD.md",
        branch_name=branch_name,
        constitutional_chain=("CLOSE-3.1", "WEB-M0", "LocalDynamicWebMatrixRecord"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=forbidden_outputs,
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def test_local_dynamic_web_matrix_record_exists_and_is_law_only() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "WEB-M0 is a law-only `PUBLIC_READINESS` matrix record" in text
    assert "It does not create an API." in text
    assert "It does not create a server." in text
    assert "It does not alter `/website`." in text
    assert "It does not add runtime dependencies." in text
    _declare("law-only matrix record")


def test_local_dynamic_web_matrix_record_contains_docs_64_fields() -> None:
    text = DOC.read_text(encoding="utf-8")

    for field in (
        "condition_id",
        "ban_class",
        "condition_text",
        "evidence_kind",
        "evidence_locator",
        "owner",
        "test_kind",
        "failure_code",
        "rank_ceiling",
        "residual_policy",
        "decision",
    ):
        assert field in text

    assert "decision         : LIFT_PERMITTED" in text
    assert "decision         : LIFT_DEFERRED_TO_LAW(CLOSE-5)" in text
    _declare("complete matrix schema")


def test_local_dynamic_web_lift_is_boundary_law_only() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Lift only the permission to draft a future, separate `WEB-L0`" in text
    assert "WEB-M0 does not create or license runtime endpoint code." in text
    assert "This shape remains descriptive until WEB-L0 is ratified." in text
    _declare("boundary-law-only lift", ("RuntimeEndpoint", "DynamicApi"))


def test_static_website_remains_network_free_after_matrix_record() -> None:
    script = WEBSITE_JS.read_text(encoding="utf-8")
    text = DOC.read_text(encoding="utf-8")

    assert "STATIC_FALLBACK_REQUIRED" in text
    assert "static fallback" in text
    assert all(token not in script for token in ("fetch(", "XMLHttpRequest", "WebSocket"))
    _declare("static fallback remains intact", ("StaticWebsiteNetworkCall",))


def test_runtime_dependency_public_model_and_storage_surfaces_remain_forbidden() -> None:
    text = DOC.read_text(encoding="utf-8")

    for phrase in (
        "RUNTIME_DEPENDENCY_UNLICENSED",
        "PUBLIC_DEPLOYMENT_UNLICENSED",
        "MODEL_CALL_UNLICENSED",
        "PERSISTENCE_UNLICENSED",
        "TELEMETRY_UNLICENSED",
    ):
        assert phrase in text

    assert "No runtime web dependency is added unless a separate `DEPENDENCY_EXPANSION`" in text
    _declare("runtime and public surfaces remain forbidden", ("PublicDeployment", "ModelCall"))


def test_future_api_outputs_must_expose_residuals_trace_and_refusals() -> None:
    text = DOC.read_text(encoding="utf-8")

    for phrase in (
        "reasonableness verdict",
        "residuals",
        "rank",
        "trace refs",
        "named failure codes",
        "visible refusal or deferral",
    ):
        assert phrase in text

    assert "never a simulated success" in text
    _declare("future response shape exposes audit surface", ("HiddenResidual", "TraceOmitted"))


def test_roadmap_records_web_m0_without_advancing_runtime_web() -> None:
    roadmap = ROADMAP.read_text(encoding="utf-8")

    assert "WEB-M0  Local Dynamic Web Matrix Record" in roadmap
    assert "CLOSE-4 Golden closure fixtures" in roadmap
    assert "no runtime API, server, dependency, public deployment" in roadmap
    _declare("roadmap records matrix without runtime implementation", ("RuntimeWebImplementation",))
