"""Source hygiene guards ratified with PR-6.

The PR-5 judgment (§9) orders a permanent guard against Trojan-source
style hidden bidirectional Unicode controls (CVE-2021-42574 family) in
every tracked file. Direction marks needed by natural Arabic prose in
the constitutional documents are licensed only through the declared
exceptions list below — never silently. The tree is currently clean,
so the exceptions list is empty.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

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


def _tracked_files() -> list[Path]:
    listing = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=_REPO_ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
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
