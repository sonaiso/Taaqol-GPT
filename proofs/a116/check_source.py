"""Bounded source-translation check, not a linguistic or Lean certificate.

Origin: docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md; branch: draft A116 proof.
Chain: pinned source -> extracted model -> finite comparison -> visible limits.
Usage: python check_source.py /path/to/pinned/a116_bridge_licence.py
No producer imports; exact AST definitions are evaluated only after hash matching.
"""

import ast
import hashlib
import itertools
import json
import sys
from enum import Enum
from pathlib import Path

SOURCE_SHA256 = "636fa867ad4aeffd5166863bae8b815df3c50f70bd25a0a9bfff68f81c728f7b"
COMMIT = "5bcd8ffdf0f288e5df54064b4efc3423269733cc"
CARRIERS = tuple("ابتثجحخدذرزسشصضطظعغفقكلمنهويء")
MARKS = ("َ", "ُ", "ِ", "ْ")


def inspect(path: Path) -> dict:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("SOURCE_IDENTITY_MISMATCH")
    tree = ast.parse(raw.decode("utf-8"))
    names = {"SyllableState", "step", "run_declared_model"}
    nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names
    ]
    if len(nodes) != len(names):
        raise ValueError("SOURCE_DEFINITION_MISSING")
    cells = tuple(itertools.product(CARRIERS, MARKS))
    namespace = {
        "Enum": Enum,
        "Sequence": list,
        "SUKUN": "ْ",
        "A116BridgeLicenceError": ValueError,
        "_cell_index": lambda: frozenset(cells),
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    states = list(namespace["SyllableState"])
    step, run = namespace["step"], namespace["run_declared_model"]
    waiting, vowelled, rejected = states
    # A separately written table specification over the same declared model.
    table = {
        waiting: (vowelled, vowelled, vowelled, rejected),
        vowelled: (vowelled, vowelled, vowelled, waiting),
        rejected: (rejected, rejected, rejected, rejected),
    }
    transition_checks = 0
    for state in states:
        for cell in cells:
            if step(state, cell) != table[state][MARKS.index(cell[1])]:
                raise ValueError("TRANSITION_MISMATCH")
            transition_checks += 1
    counts = []
    for length in range(3):
        safe_count = 0
        for word in itertools.product(cells, repeat=length):
            safe = run(word) != rejected
            direct = (not word or word[0][1] != "ْ") and all(
                not (left[1] == right[1] == "ْ") for left, right in zip(word, word[1:], strict=False)
            )
            if safe != direct:
                raise ValueError("SAFETY_SPECIFICATION_MISMATCH")
            safe_count += safe
        counts.append({"length": length, "enumerated": len(cells) ** length, "safe": safe_count})
    reached, sizes = {waiting}, [1]
    while True:
        grown = reached | {step(q, a) for q in reached for a in cells}
        if grown == reached:
            break
        reached = grown
        sizes.append(len(reached))
    return {
        "source_repository": "Saleh1967/Alghanem",
        "source_commit": COMMIT,
        "source_path": "src/alghanem/arabic/a116_bridge_licence.py",
        "source_utf8_sha256": SOURCE_SHA256,
        "method": (
            "hash-checked AST extraction; vocabulary and marks manually transcribed "
            "from pinned source modules"
        ),
        "transition_checks": transition_checks,
        "transition_mismatches": 0,
        "sequence_checks": counts,
        "saturation_sizes": sizes,
        "safe_definition": "state != FELL_OUT_OF_THE_MODEL",
        "linguistic_license": False,
        "lean_status": "see GitHub proof job; this JSON is Python evidence only",
    }


if __name__ == "__main__":
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))
