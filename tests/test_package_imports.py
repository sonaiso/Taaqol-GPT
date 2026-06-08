# Conformance smoke tests for the bare scaffold.
#
# PR-0 ships no behaviour; this test only proves the package is importable
# under the src layout so that PR-1 can begin from a known-green baseline.

import importlib


def test_package_imports() -> None:
    module = importlib.import_module("taaqqul_slot_geometry")
    assert module.__all__ == []
