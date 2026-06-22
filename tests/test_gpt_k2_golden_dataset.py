"""Acceptance tests for GPT-K2 minimal golden dataset surface.

Origin law     : docs/55 (Knowledge Origins Boundary Law)
Branch         : GPT-K2 (Minimal Golden Origins Dataset)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from taaqqul_slot_geometry.gpt.golden_origins_dataset import (
    default_coverage_matrix_path,
    load_golden_origins_dataset,
)


def test_dataset_file_exists() -> None:
    path = default_coverage_matrix_path()
    assert path.is_file()


def test_dataset_loads_with_required_gpt_k2_counts() -> None:
    dataset = load_golden_origins_dataset()
    assert dataset.branch_name == "GPT-K2"
    assert dataset.schema_version == "2.0"
    assert len(dataset.entities) == 50
    assert len(dataset.attributes) == 50
    assert len(dataset.relations) == 30
    assert len(dataset.references) == 20
    assert len(dataset.evidence_entries) == 50
    assert len(dataset.coverage_matrix) == 50


def test_coverage_matrix_contains_required_cases() -> None:
    dataset = load_golden_origins_dataset()
    index = {case.text: case for case in dataset.coverage_matrix}

    assert index["مِنْ"].expected_result == "PASS"
    assert index["مِنْ"].expected_path == "BUILT"

    assert index["ضَرَبَ"].expected_result == "PASS"
    assert index["ضَرَبَ"].expected_path == "EVENT"

    assert index["جَبَل"].expected_result == "PASS"
    assert index["جَبَل"].expected_path == "JAMID"

    assert index["أَكْرَمَ"].expected_result == "FAIL"
    assert index["أَكْرَمَ"].expected_stage == "M7"

    assert index["ضَرَبْتُ"].expected_result == "PASS"
    assert index["ضَرَبْتُ"].expected_path == "EVENT"

    assert index["بْ"].expected_result == "FAIL"
    assert index["بْ"].expected_stage == "M1/M4"


def test_loaded_surface_is_immutable_dataclass_style() -> None:
    dataset = load_golden_origins_dataset()
    try:
        dataset.coverage_matrix = ()
    except Exception as exc:  # noqa: BLE001
        assert type(exc).__name__ in {"FrozenInstanceError", "AttributeError"}
    else:
        raise AssertionError("dataset must be immutable")
