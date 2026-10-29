#!/usr/bin/env python3
"""SLGE ⇐ البرهان: بناء خانات SLGE الفعليّة من بيان الخانات الذي يصدره Lean.

الفحص ثلاث مراحل، كلّها قراءة فقط لشيفرة ``src`` (لا تعديل تشغيليّ):

1. **دريفت**: البيان الذي يصدره ``arabic_slots`` الآن مطابق للملفّ المودَع
   ``slots_manifest.json`` (فلا تتغيّر الشيفرة البرهانيّة دون أن يتغيّر البيان).
2. **التمثيل**: كلّ خانة في البيان تُبنى خانةً حقيقيّة في
   ``taaqqul_slot_geometry.core.slot_graph`` بـ``allowed_potentials`` = تعداد البرهان
   بعينه، وكلّ توفيقٍ يرخّصه البرهان (صنف × حالة ⇒ علامة؛ دور ⇒ حالة/عامل؛
   علامة ⇒ خلية) يُملأ به الخانة فتقبله، ويُغلق الرسم البياني بـ``Γ`` إغلاقًا أدنى.
3. **الرفض**: كلّ ما يرفضه البرهان (حالة ممتنعة لصنف، قيمة خارج التعداد، خلية
   خارج A116) ترفضه خانة SLGE بـ``UNLICENSED_OPENING`` عند البناء.

الاستعمال: ``python3 check_slots.py [--write]`` من داخل ``proofs/arabic`` بعد ``lake build``.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "src"))

from taaqqul_slot_geometry.core.closure_state import ClosureState  # noqa: E402
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode  # noqa: E402
from taaqqul_slot_geometry.core.gamma import gamma  # noqa: E402
from taaqqul_slot_geometry.core.rank_lattice import Rank  # noqa: E402
from taaqqul_slot_geometry.core.slot_graph import (  # noqa: E402
    Center,
    EntryBoundary,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceRef,
)

MANIFEST = HERE / "slots_manifest.json"
TRACE = "proofs/arabic/Arabic/Slots.lean"


def emitted_manifest() -> dict:
    exe = HERE / ".lake" / "build" / "bin" / "arabic_slots"
    if not exe.exists():
        subprocess.run(["lake", "build", "arabic_slots"], cwd=HERE, check=True)
    out = subprocess.run([str(exe)], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def cell_tag(c: dict) -> str:
    return f"{c['carrier']}:{c['mark']}"


def boundary(scope: str) -> SlotBoundary:
    return SlotBoundary(
        domain="arabic-proof",
        scope=scope,
        refusal_codes=(FailureCode.UNLICENSED_OPENING,),
        licensed_operations=("fill-from-proof",),
    )


def slot(name: str, allowed: set[str], value: str) -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.FILLED,
        boundary=boundary(name),
        opening=OpeningPolicy(allowed_potentials=frozenset(allowed)),
        required=True,
        value=value,
    )


def expect_refusal(name: str, allowed: set[str], value: str) -> None:
    try:
        slot(name, allowed, value)
    except SlotGraphSchemaError as e:
        assert FailureCode.UNLICENSED_OPENING.value in str(e), e
        return
    raise AssertionError(f"SLGE accepted what the proof refuses: {name}={value!r}")


def graph(slots: tuple[Slot, ...], claim: str) -> SlotGraph:
    return SlotGraph(
        center=Center(
            identity_claim=claim,
            domain="arabic-proof",
            scope="slot-partition",
            trace_ref=TraceRef(anchor=TRACE, kind="PROOF"),
        ),
        slots=slots,
        boundary=boundary("slot-partition"),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=OutputBoundary(declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=EntryBoundary(
            declared_entry_kind="LEAN_SLOT_MANIFEST",
            representation_status="REPRESENTATIONAL_OF_PRIOR",
            ontological_status="NOT_AN_ORIGIN",
            sound_status="NOT_A_SOUND",
            meaning_status="NOT_A_MEANING",
            prior_trace_status="OUT_OF_CURRENT_EXECUTION",
            produces_only="TEXT_TRACE_CANDIDATE",
        ),
    )


def check_representation(m: dict) -> tuple[int, int]:
    cells = {cell_tag(c) for c in m["cells"]}
    assert len(cells) == 116 == len(m["cells"]), "A116 partition is not 116 distinct cells"
    marks, cases, endings = set(m["marks"]), set(m["cases"]), {e["ending"] for e in m["endings"]}
    classes = {c["class"] for c in m["classes"]}
    roles, governors = {r["role"] for r in m["roles"]}, set(m["governors"])
    accepted = closed = 0

    # ending ⇒ cell: every ending cell is inside A116
    for e in m["endings"]:
        g = graph(
            (slot("ending", endings, e["ending"]), slot("ending.cell", cells, cell_tag(e["cell"]))),
            f"ending:{e['ending']}",
        )
        accepted += 1
        closed += gamma(g).state is ClosureState.MINIMALLY_CLOSED

    # class × case ⇒ ending (the licensed 2/3 of the 48 pairs)
    for c in m["classes"]:
        for case, ending in c["endings"].items():
            if ending is None:
                continue
            g = graph(
                (
                    slot("class", classes, c["class"]),
                    slot("case", cases, case),
                    slot(f"ending@{c['class']}", {v for v in c["endings"].values() if v}, ending),
                ),
                f"{c['class']}×{case}",
            )
            accepted += 1
            closed += gamma(g).state is ClosureState.MINIMALLY_CLOSED

    # role ⇒ case, governor
    for r in m["roles"]:
        g = graph(
            (
                slot("role", roles, r["role"]),
                slot("role.case", cases, r["case"]),
                slot("role.governor", governors, r["governor"]),
            ),
            f"role:{r['role']}",
        )
        accepted += 1
        closed += gamma(g).state is ClosureState.MINIMALLY_CLOSED

    # structural shapes
    for key in ("jumla_shapes", "khabar_shapes", "shibh_shapes"):
        for v in m[key]:
            g = graph((slot(key, set(m[key]), v),), f"{key}:{v}")
            accepted += 1
            closed += gamma(g).state is ClosureState.MINIMALLY_CLOSED

    for mk in m["marks"]:
        for carrier in m["carriers"]:
            idx = m["carriers"].index(carrier)
            slot("cell", cells, f"{idx}:{mk}")
            accepted += 1
    assert marks and cases, "empty enumerations"
    return accepted, closed


def check_refusals(m: dict) -> int:
    cells = {cell_tag(c) for c in m["cells"]}
    cases = set(m["cases"])
    refused = 0
    # a case the proof forbids for a class (nominal ⇒ no jazm; verbal ⇒ no jarr)
    for c in m["classes"]:
        allowed_cases = {k for k, v in c["endings"].items() if v}
        for case in cases - allowed_cases:
            expect_refusal(f"case@{c['class']}", allowed_cases, case)
            refused += 1
        assert ("jazm" not in allowed_cases) == c["nominal"], c
        assert ("jarr" not in allowed_cases) == (not c["nominal"]), c
    # outside the enumerations
    expect_refusal("ending", {e["ending"] for e in m["endings"]}, "tanwin")
    expect_refusal("cell", cells, "29:fatha")
    expect_refusal("cell", cells, "0:shadda")
    expect_refusal("role", {r["role"] for r in m["roles"]}, "hal")
    expect_refusal("jumla_shapes", set(m["jumla_shapes"]), "shartiyya")
    refused += 5
    return refused


def main(argv: list[str]) -> int:
    emitted = emitted_manifest()
    if "--write" in argv:
        MANIFEST.write_text(json.dumps(emitted, ensure_ascii=False, indent=1) + "\n")
    if not MANIFEST.exists():
        print("FAIL: slots_manifest.json missing (run with --write)")
        return 1
    stored = json.loads(MANIFEST.read_text())
    if stored != emitted:
        print("FAIL: slots_manifest.json drifted from Arabic/Slots.lean output")
        return 1
    accepted, closed = check_representation(emitted)
    refused = check_refusals(emitted)
    print(
        f"PASS: SLGE slots from proof manifest: {accepted} licensed fillings accepted, "
        f"{closed} graphs MINIMALLY_CLOSED by Γ, {refused} proof-refused fillings refused"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
