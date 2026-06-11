"""Source hygiene guards ratified with PR-6.

The PR-5 judgment (§9) orders a permanent guard against Trojan-source
style hidden bidirectional Unicode controls (CVE-2021-42574 family) in
every tracked file. Direction marks needed by natural Arabic prose in
the constitutional documents are licensed only through the declared
exceptions list below — never silently. The tree is currently clean,
so the exceptions list is empty.

PR-6.1 hardening: enumeration prefers ``git ls-files``, but a missing
``git`` binary or a missing ``.git`` checkout (sdist unpack, minimal
CI runner) must hand over to a deterministic fallback walk of the
constitutional surface — the guard never hard-fails before inspecting
anything and never silently scans nothing.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent

# Hidden bidirectional / invisible direction controls. None of these
# may appear in any tracked file outside a declared exception.
_BIDI_CONTROLS = {
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202c": "POP DIRECTIONAL FORMATTING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
    "\u200e": "LEFT-TO-RIGHT MARK",
    "\u200f": "RIGHT-TO-LEFT MARK",
    "\u061c": "ARABIC LETTER MARK",
}

# Declared exceptions, as repository-relative POSIX paths. A path may
# only be added here together with a review note explaining why the
# direction mark is required (e.g. natural Arabic text in docs).
_DECLARED_EXCEPTIONS: tuple[str, ...] = ()


# Roots and top-level files the deterministic fallback enumerates when
# git is unavailable. The list is conservative on purpose: it covers the
# constitutional surface (kernel, tests, docs, project metadata) and
# never walks .git, virtual environments, build artefacts, caches, or
# packaging metadata.
_FALLBACK_ROOTS: tuple[str, ...] = ("src", "tests", "docs")
_FALLBACK_TOP_LEVEL_GLOBS: tuple[str, ...] = ("pyproject.toml", "CLAUDE.md", "README*")
_FALLBACK_EXCLUDED_PARTS: frozenset[str] = frozenset(
    {".git", ".venv", "build", "dist", "__pycache__"}
)


def _source_tree_files_fallback() -> list[Path]:
    """Deterministic git-free enumeration of the constitutional surface.

    Ratified with PR-6.1: when ``git ls-files`` cannot run, the guard
    walks only the declared roots and top-level files, sorted, so the
    scan stays reproducible across environments.
    """

    files: list[Path] = []
    for root_name in _FALLBACK_ROOTS:
        root = _REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative_parts = path.relative_to(_REPO_ROOT).parts
            if any(
                part in _FALLBACK_EXCLUDED_PARTS or part.endswith(".egg-info")
                for part in relative_parts
            ):
                continue
            files.append(path)
    for pattern in _FALLBACK_TOP_LEVEL_GLOBS:
        files.extend(path for path in sorted(_REPO_ROOT.glob(pattern)) if path.is_file())
    return files


def _tracked_files() -> list[Path]:
    try:
        listing = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=_REPO_ROOT,
            capture_output=True,
            check=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # No git binary or no .git checkout: fall back to the
        # deterministic source-tree walk instead of failing the
        # hygiene guard before it can inspect anything (PR-6.1).
        return _source_tree_files_fallback()
    return [_REPO_ROOT / name for name in listing.stdout.split("\0") if name]


def test_no_hidden_bidi_controls_in_tracked_source_files() -> None:
    violations: list[str] = []
    for path in _tracked_files():
        relative = path.relative_to(_REPO_ROOT).as_posix()
        if relative in _DECLARED_EXCEPTIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary artefacts carry no readable source text
        for offset, char in enumerate(text):
            if char in _BIDI_CONTROLS:
                violations.append(
                    f"{relative}: U+{ord(char):04X} "
                    f"({_BIDI_CONTROLS[char]}) at offset {offset}"
                )
    assert not violations, (
        "hidden bidirectional controls found in tracked files:\n"
        + "\n".join(violations)
    )


def test_tracked_files_falls_back_when_git_enumeration_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The hygiene guard must enumerate files even without git.

    Ratified with PR-6.1: ``git ls-files`` is preferred, but a missing
    ``git`` binary (``FileNotFoundError``) or a missing ``.git``
    checkout (``CalledProcessError``) must hand over to the
    deterministic fallback — never to an error and never to an empty
    scan, and the fallback must never enter forbidden roots.
    """

    def _no_git_binary(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError("git: command not found")

    def _no_git_checkout(*args: object, **kwargs: object) -> None:
        raise subprocess.CalledProcessError(128, ["git", "ls-files", "-z"])

    for broken_git in (_no_git_binary, _no_git_checkout):
        monkeypatch.setattr(subprocess, "run", broken_git)
        files = _tracked_files()
        relative = {path.relative_to(_REPO_ROOT).as_posix() for path in files}

        # The constitutional surface is present…
        assert "tests/test_source_hygiene.py" in relative
        assert "pyproject.toml" in relative
        assert "CLAUDE.md" in relative
        assert any(name.startswith("src/") for name in relative)
        assert any(name.startswith("docs/") for name in relative)
        # …and the forbidden roots and artefacts are absent.
        forbidden_prefixes = (".git/", ".venv/", "build/", "dist/")
        assert all(not name.startswith(forbidden_prefixes) for name in relative)
        assert all("__pycache__" not in name for name in relative)
        assert all(".egg-info" not in name for name in relative)
