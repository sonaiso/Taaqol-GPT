"""Acceptance tests for docs/67 — Golden Closure Fixtures Law (CLOSE-4).

Origin law          : docs/67_GOLDEN_CLOSURE_FIXTURES_LAW.md
Branch              : CLOSE-4 (Golden closure fixtures)
Constitutional chain: ("CLOSE-3", "CLOSE-3.1", "CLOSE-4")
Category            : Category 2 — Contract / surface tests (docs/52 §4)

The suite enforces every proposition in docs/67 §8: schema (§3),
vocabularies (§4), curation rule (§5), forbidden surface (§6),
residual policy (§7), and chain-status synchronization (§10).
None of the refusals listed in docs/67 §9 corresponds to a global
``FailureCode`` member; they are local refusal labels for this
closure step.
"""

from __future__ import annotations

import json
import pathlib
import re

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import ResidualKind
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_67 = _REPO_ROOT / "docs" / "67_GOLDEN_CLOSURE_FIXTURES_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_FIXTURE_PACK = _REPO_ROOT / "data" / "golden_closure_fixtures.json"
_FAILURE_TAXONOMY = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "core" / "failure_taxonomy.py"
)
_RESIDUAL_POLICY = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "core" / "residual_policy.py"
)

_SCHEMA_KEYS = frozenset(
    {
        "chain_step_id",
        "family",
        "status",
        "origin_law_locators",
        "runtime_locators",
        "test_locators",
        "forbidden_outputs",
        "residual_kind",
        "evidence_note",
    }
)

_FAMILIES = frozenset(
    {
        "KERNEL",
        "AUDIT",
        "ADAPTER",
        "WEIGHT",
        "PRE_SEMANTIC",
        "FORMAL_SHAPE",
        "MUFRAD_DALALAH",
        "VERTICAL",
        "POST_VERTICAL",
        "GPT_REASONABLENESS",
        "EUCLIDEAN",
        "WADI",
        "COUPLED_DALALAH",
        "CLOSURE",
        "LAW_ONLY_RECORD",
    }
)

_STATUSES = frozenset({"DONE_RUNTIME", "DONE_LAW_ONLY", "DONE_CORRECTIVE"})

_FORBIDDEN_VOCAB = frozenset(
    {
        "PromotionWithoutGate",
        "HiddenResidual",
        "OpenedBranch",
        "BranchLicense",
        "ReadinessCertificate",
        "ReleaseTag",
        "ChainTruthOverride",
        "FabricatedLocator",
        "NewFailureCode",
        "NewResidualKind",
        "AdapterMutation",
        "AuditMutation",
    }
)

_DOC_67_SECTIONS = tuple(f"## §{i}" for i in range(1, 11))

_CLOSE_4_DONE = "CLOSE-4 Golden closure fixtures"
_CLOSE_5_LABEL = "CLOSE-5 Final closure audit"
_DAL_A4_DONE_LABEL = "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates"
_DAL_A4_ADMIT_DONE_LABEL = "DAL-A4-ADMIT post-CLOSE-6 admission decision (DAL-A4 scope only)"
_DAL_A5_ADMIT_DONE_LABEL = "DAL-A5-ADMIT admission boundary after DAL-A4 runtime"
_DAL_A5_DONE_LABEL = "DAL-A5  Syllable / transition / adjacency / S1-S5 gates"
_DAL_A6_ADMIT_DONE_LABEL = "DAL-A6-ADMIT admission boundary after DAL-A5 runtime"
_DAL_A6_DONE_LABEL = "DAL-A6  Detailed waqf / wasl closure"
_DAL_A7_DONE_LABEL = "DAL-A7  Usage / loan / unvocalized / deletion residual gates"
_DAL_A7_1_DONE_LABEL = "DAL-A7.1 Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics"
_DAL_A8_CURRENT_LABEL = "DAL-A8  DalAloneClosed -> LafziMadlulGate integration"


def _declare(branch_note: str) -> None:
    """Assert this test module itself satisfies docs/12 + docs/52 discipline."""
    case = ConstitutionalTestCase(
        origin_law="docs/67_GOLDEN_CLOSURE_FIXTURES_LAW.md",
        branch_name=f"CLOSE-4 ({branch_note})",
        constitutional_chain=("CLOSE-3", "CLOSE-3.1", "CLOSE-4"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "PromotionWithoutGate",
            "HiddenResidual",
            "OpenedBranch",
            "BranchLicense",
            "ReadinessCertificate",
            "ReleaseTag",
            "ChainTruthOverride",
            "FabricatedLocator",
            "NewFailureCode",
            "NewResidualKind",
            "AdapterMutation",
            "AuditMutation",
        ),
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


def _load_pack() -> list[dict[str, object]]:
    text = _FIXTURE_PACK.read_text(encoding="utf-8")
    return json.loads(text)


# --- docs/67 presence and shape ------------------------------------------------


def test_docs_67_exists_and_declares_sections_1_through_10() -> None:
    _declare("docs/67 presence and section coverage")
    assert _DOC_67.exists(), "docs/67_GOLDEN_CLOSURE_FIXTURES_LAW.md must exist"
    body = _DOC_67.read_text(encoding="utf-8")
    for marker in _DOC_67_SECTIONS:
        assert marker in body, f"docs/67 must declare {marker} (per §8.1)"


# --- fixture pack presence, JSON validity, schema shape ------------------------


def test_fixture_pack_is_valid_json_list() -> None:
    _declare("fixture pack JSON validity")
    assert _FIXTURE_PACK.exists(), "data/golden_closure_fixtures.json must exist"
    pack = _load_pack()
    assert isinstance(pack, list) and pack, "fixture pack must be a non-empty list"


def test_every_entry_has_exact_schema_keys() -> None:
    _declare("schema-shape check (SchemaShapeViolation refusal)")
    for entry in _load_pack():
        assert isinstance(entry, dict), "each fixture must be a JSON object"
        keys = frozenset(entry.keys())
        assert keys == _SCHEMA_KEYS, (
            f"SchemaShapeViolation in {entry.get('chain_step_id', '<unknown>')}: "
            f"missing={_SCHEMA_KEYS - keys} extra={keys - _SCHEMA_KEYS}"
        )


# --- vocabulary checks (§4) ----------------------------------------------------


def test_family_status_and_residual_kind_drawn_from_closed_vocab() -> None:
    _declare("§4 closed vocabularies")
    valid_kinds = {kind.value for kind in ResidualKind}
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        assert entry["family"] in _FAMILIES, f"UnknownFamily in {sid}: {entry['family']}"
        assert entry["status"] in _STATUSES, f"UnknownStatus in {sid}: {entry['status']}"
        assert entry["residual_kind"] in valid_kinds, (
            f"UnknownResidualKind in {sid}: {entry['residual_kind']}"
        )


def test_residual_kind_is_explanatory_for_every_entry() -> None:
    _declare("§7 residual policy")
    for entry in _load_pack():
        assert entry["residual_kind"] == ResidualKind.EXPLANATORY.value, (
            f"ResidualKindNotExplanatory in {entry['chain_step_id']}: "
            f"{entry['residual_kind']}"
        )


# --- locator existence (§8.8) --------------------------------------------------


def test_every_locator_path_exists_on_disk() -> None:
    _declare("§8.8 FabricatedLocator refusal")
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        for key in ("origin_law_locators", "runtime_locators", "test_locators"):
            paths = entry[key]
            assert isinstance(paths, list), f"{sid}.{key} must be a list"
            for relative in paths:
                assert isinstance(relative, str) and relative, (
                    f"{sid}.{key} contains non-string entry"
                )
                assert (_REPO_ROOT / relative).is_file(), (
                    f"FabricatedLocator in {sid}.{key}: {relative}"
                )


def test_origin_law_and_test_locators_non_empty() -> None:
    _declare("§3 non-empty origin and test locators")
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        assert entry["origin_law_locators"], (
            f"{sid}: origin_law_locators must be non-empty (§3)"
        )
        assert entry["test_locators"], (
            f"EmptyTestLocators in {sid} (§3)"
        )


# --- status / runtime locator coupling (§8.6, §8.7) ----------------------------


def test_done_runtime_has_runtime_locators_and_done_law_only_has_none() -> None:
    _declare("§8.6 / §8.7 status-runtime coupling")
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        runtime = entry["runtime_locators"]
        if entry["status"] == "DONE_RUNTIME":
            assert runtime, f"EmptyRuntimeLocatorsForRuntime in {sid}"
        elif entry["status"] == "DONE_LAW_ONLY":
            assert runtime == [], f"NonEmptyRuntimeLocatorsForLawOnly in {sid}"


# --- forbidden outputs (§6, §8.9) ---------------------------------------------


def test_forbidden_outputs_non_empty_and_drawn_from_vocabulary() -> None:
    _declare("§6 forbidden surface and §8.9 vocabulary check")
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        forbidden = entry["forbidden_outputs"]
        assert isinstance(forbidden, list) and forbidden, (
            f"EmptyForbiddenOutputs in {sid}"
        )
        for name in forbidden:
            assert name in _FORBIDDEN_VOCAB, (
                f"ForbiddenOutOfVocabulary in {sid}: {name!r} not in §6"
            )


# --- evidence_note bounds (§3, §8 refusal table) ------------------------------


def test_evidence_note_is_bounded_and_single_line() -> None:
    _declare("§3 evidence_note bounds")
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        note = entry["evidence_note"]
        assert isinstance(note, str), f"{sid}: evidence_note must be a string"
        stripped = note.strip()
        assert stripped, f"EvidenceNoteOutOfBounds in {sid}: empty note"
        assert len(stripped) <= 240, (
            f"EvidenceNoteOutOfBounds in {sid}: {len(stripped)} chars > 240"
        )
        assert "\n" not in stripped, (
            f"EvidenceNoteOutOfBounds in {sid}: must be a single line"
        )


# --- chain_step_id uniqueness and roadmap presence (§8.4) ---------------------


def _roadmap_text() -> str:
    return _DOC_14.read_text(encoding="utf-8")


def _claude_text() -> str:
    return _CLAUDE.read_text(encoding="utf-8")


def _step_done_pattern(step_id: str) -> re.Pattern[str]:
    # Match a "row" beginning with the step id (anchored at line start with
    # a word break) and reaching the "✓ done" marker within ~400 characters,
    # so that multi-line CLAUDE.md / docs/14 rows whose marker sits on a
    # continuation line still count. This mirrors the chain table format
    # used in both files.
    return re.compile(
        r"^" + re.escape(step_id) + r"\b[\s\S]{0,400}?✓\s*done",
        re.MULTILINE,
    )


def test_chain_step_ids_are_unique_in_the_pack() -> None:
    _declare("§8.4 NonUniqueChainStepId refusal")
    seen: dict[str, int] = {}
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        seen[sid] = seen.get(sid, 0) + 1
    duplicates = {k: v for k, v in seen.items() if v > 1}
    assert not duplicates, f"NonUniqueChainStepId in pack: {duplicates}"


def test_every_chain_step_id_is_registered_done_in_docs_14_and_claude() -> None:
    _declare("§8.4 ChainStepIdNotInRoadmap refusal")
    roadmap = _roadmap_text()
    claude = _claude_text()
    for entry in _load_pack():
        sid = entry["chain_step_id"]
        pattern = _step_done_pattern(sid)
        assert pattern.search(roadmap), (
            f"ChainStepIdNotInRoadmap (docs/14): {sid} not registered as ✓ done"
        )
        assert pattern.search(claude), (
            f"ChainStepIdNotInRoadmap (CLAUDE.md): {sid} not registered as ✓ done"
        )


# --- curation rule (§5, §8.11) ------------------------------------------------


def test_every_declared_family_has_at_least_one_landmark() -> None:
    _declare("§5 / §8.11 NonRepresentativePack refusal")
    covered = {entry["family"] for entry in _load_pack()}
    missing = _FAMILIES - covered
    assert not missing, f"NonRepresentativePack: families with no landmark: {missing}"


# --- chain status synchronization (§8.12) -------------------------------------


def _has_done_marker(text: str, prefix: str) -> bool:
    pattern = re.compile(
        r"^" + re.escape(prefix) + r".*✓\s*done", re.MULTILINE
    )
    return bool(pattern.search(text))


def _has_current_marker(text: str, prefix: str) -> bool:
    pattern = re.compile(
        r"^" + re.escape(prefix) + r".*→\s*current", re.MULTILINE
    )
    return bool(pattern.search(text))


def test_close_4_and_close_5_are_done_and_dal_a8_is_current_in_roadmap_and_claude() -> None:
    _declare("§8.12 CLOSE-4/CLOSE-5/DAL-A8 chain status synchronization")
    roadmap = _roadmap_text()
    claude = _claude_text()
    assert _has_done_marker(roadmap, _CLOSE_4_DONE), (
        "CloseFourStatusMissing: docs/14 must mark CLOSE-4 as ✓ done"
    )
    assert _has_done_marker(claude, _CLOSE_4_DONE), (
        "CloseFourStatusMissing: CLAUDE.md must mark CLOSE-4 as ✓ done"
    )
    assert _has_done_marker(roadmap, _CLOSE_5_LABEL), (
        "CloseFiveDoneMissing: docs/14 must mark CLOSE-5 as ✓ done"
    )
    assert _has_done_marker(claude, _CLOSE_5_LABEL), (
        "CloseFiveDoneMissing: CLAUDE.md must mark CLOSE-5 as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A4_DONE_LABEL), (
        "DalA4DoneMissing: docs/14 must mark DAL-A4 as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A4_DONE_LABEL), (
        "DalA4DoneMissing: CLAUDE.md must mark DAL-A4 as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A4_ADMIT_DONE_LABEL), (
        "DalA4AdmitDoneMissing: docs/14 must mark DAL-A4-ADMIT as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A4_ADMIT_DONE_LABEL), (
        "DalA4AdmitDoneMissing: CLAUDE.md must mark DAL-A4-ADMIT as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A5_ADMIT_DONE_LABEL), (
        "DalA5AdmitDoneMissing: docs/14 must mark DAL-A5-ADMIT as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A5_ADMIT_DONE_LABEL), (
        "DalA5AdmitDoneMissing: CLAUDE.md must mark DAL-A5-ADMIT as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A5_DONE_LABEL), (
        "DalA5DoneMissing: docs/14 must mark DAL-A5 as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A5_DONE_LABEL), (
        "DalA5DoneMissing: CLAUDE.md must mark DAL-A5 as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A6_ADMIT_DONE_LABEL), (
        "DalA6AdmitDoneMissing: docs/14 must mark DAL-A6-ADMIT as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A6_ADMIT_DONE_LABEL), (
        "DalA6AdmitDoneMissing: CLAUDE.md must mark DAL-A6-ADMIT as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A6_DONE_LABEL), (
        "DalA6DoneMissing: docs/14 must mark DAL-A6 as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A6_DONE_LABEL), (
        "DalA6DoneMissing: CLAUDE.md must mark DAL-A6 as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A7_DONE_LABEL), (
        "DalA7DoneMissing: docs/14 must mark DAL-A7 as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A7_DONE_LABEL), (
        "DalA7DoneMissing: CLAUDE.md must mark DAL-A7 as ✓ done"
    )
    assert _has_done_marker(roadmap, _DAL_A7_1_DONE_LABEL), (
        "DalA71DoneMissing: docs/14 must mark DAL-A7.1 as ✓ done"
    )
    assert _has_done_marker(claude, _DAL_A7_1_DONE_LABEL), (
        "DalA71DoneMissing: CLAUDE.md must mark DAL-A7.1 as ✓ done"
    )
    assert _has_current_marker(roadmap, _DAL_A8_CURRENT_LABEL), (
        "DalA8CurrentMissing: docs/14 must mark DAL-A8 as → current"
    )
    assert _has_current_marker(claude, _DAL_A8_CURRENT_LABEL), (
        "DalA8CurrentMissing: CLAUDE.md must mark DAL-A8 as → current"
    )


# --- enum-extension guard (§8.13, §8.14) --------------------------------------


# Expected enum sizes are captured as a snapshot at the time CLOSE-4 lands.
# These constants are hand-verified against the current kernel source; any
# constitutional licensing PR that adds a new FailureCode or ResidualKind
# member must also update these counts in the same PR. CLOSE-4 itself adds
# neither, so its acceptance suite refuses any change.
_EXPECTED_FAILURECODE_MEMBERS = 92
_EXPECTED_RESIDUALKIND_MEMBERS = 5


def test_failure_code_enum_is_not_extended_by_close_4() -> None:
    _declare("§8.13 NewFailureCodeIntroduced guard")
    # CLOSE-4 must be additive in fixture-pack form only; it must not extend
    # the global FailureCode enum. The runtime member count must equal the
    # snapshot captured when this test was authored.
    members = list(FailureCode)
    assert len(members) == _EXPECTED_FAILURECODE_MEMBERS, (
        "NewFailureCodeIntroduced: FailureCode enum size changed during CLOSE-4 "
        f"(expected {_EXPECTED_FAILURECODE_MEMBERS}, got {len(members)})"
    )


def test_residual_kind_enum_is_not_extended_by_close_4() -> None:
    _declare("§8.14 NewResidualKindIntroduced guard")
    members = list(ResidualKind)
    assert len(members) == _EXPECTED_RESIDUALKIND_MEMBERS, (
        "NewResidualKindIntroduced: ResidualKind enum size changed during "
        f"CLOSE-4 (expected {_EXPECTED_RESIDUALKIND_MEMBERS}, got {len(members)})"
    )
