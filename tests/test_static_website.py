"""Static website tests.

Origin law     : docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md
Branch         : Website readiness surface
Category       : Category 4 — Support / fixture tests (docs/52 §4)
"""

from __future__ import annotations

import re
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_WEBSITE = _REPO_ROOT / "website"
_INDEX = _WEBSITE / "index.html"
_STYLES = _WEBSITE / "styles.css"
_APP = _WEBSITE / "app.js"
_EXTERNAL_DEPENDENCY_PATTERN = re.compile(r"https?://|//cdn\.|@import\s+url")


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_name=branch_name,
        constitutional_chain=("CLOSE-2", "CLOSE-3", "WebsiteReadinessSurface"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("NetworkWebsiteDependency", "CertificationByStaticPage"),
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


def test_static_website_assets_exist_and_are_local() -> None:
    _declare("static website asset surface")
    assert _INDEX.exists()
    assert _STYLES.exists()
    assert _APP.exists()

    html = _INDEX.read_text(encoding="utf-8")

    assert 'lang="ar"' in html
    assert 'dir="rtl"' in html
    assert 'href="./styles.css"' in html
    assert 'src="./app.js"' in html


def test_static_website_has_no_external_network_dependencies() -> None:
    _declare("static website dependency boundary")
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in (_INDEX, _STYLES, _APP)
    )

    assert not _EXTERNAL_DEPENDENCY_PATTERN.search(combined)
    assert "fetch(" not in combined
    assert "XMLHttpRequest" not in combined
    assert "import " not in _APP.read_text(encoding="utf-8")


def test_static_website_exposes_required_project_validation_commands() -> None:
    _declare("static website validation workflow")
    html = _INDEX.read_text(encoding="utf-8")
    script = _APP.read_text(encoding="utf-8")

    assert 'pip install -e ".[dev]"' in html
    assert "ruff check ." in html
    assert "pytest" in html
    assert "العُقد الدلالية: التصريف -- الاشتقاق -- الجموع --" in html
    assert "TaaqolWebsiteTestEnvelope" in script
    assert "BLOCKED_BY_VISIBLE_RESIDUALS" in script
    assert "READY_FOR_REPOSITORY_TEST_COMMANDS" in script
