"""فهرس التغطية: كل قاعدة معلنة في rules.json يجب أن تشير إلى مبرهنة موجودة فعلًا في الشيفرة،
وكل شاهد مصدري يجب أن يطابق السطر المذكور في ملف المصدر المثبّت بالبصمة."""
import hashlib, json, os, pathlib, re, sys

root = pathlib.Path(__file__).parent
rules = json.loads((root / "rules.json").read_text())
# ARABIC_SOURCE_DIR يسمح لـCI بتقديم المصادر المثبّتة من مكان آخر؛ البصمة تبقى الحَكَم.
src_dir = os.environ.get("ARABIC_SOURCE_DIR")


def source_path(src):
    return pathlib.Path(src_dir) / pathlib.Path(src["path"]).name if src_dir else pathlib.Path(src["path"])


theorems = set()
for p in (root / "Arabic").glob("*.lean"):
    theorems |= set(re.findall(r"^\s*(?:theorem|lemma)\s+([\w.]+)", p.read_text(), re.M))

for src in rules["sources"]:
    path = source_path(src)
    if not path.exists():
        if os.environ.get("ARABIC_SOURCES_REQUIRED"):
            sys.exit(f"source absent: {path}")
        print(f"SKIP (source absent): {path}"); continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != src["sha256"]:
        sys.exit(f"source digest mismatch for {src['path']}: {digest}")

missing = []
for r in rules["rules"]:
    for t in r["theorems"]:
        if t not in theorems:
            missing.append((r["id"], t))
if missing:
    sys.exit(f"rules referencing missing theorems: {missing}")

by_path = {s["id"]: source_path(s) for s in rules["sources"]}
for r in rules["rules"]:
    for sh in r.get("shawahid", []):
        path = by_path[sh["source"]]
        if not path.exists():
            continue
        line = path.read_text().splitlines()[sh["line"] - 1]
        if sh["quote"] not in line:
            sys.exit(f"quote not at {sh['source']}:{sh['line']} for rule {r['id']}")

# شواهد Awamil.lean المضمَّنة: كل (مبرهنة، مسار، سطر، اقتباس) يُفحص ضد المصدر الفعلي.
awamil = (root / "Arabic" / "Awamil.lean").read_text()
emb = re.findall(r'\(\s*"([\w.]+)",\s*⟨(\w+Path),\s*(\d+),\s*"([^"]+)"⟩\s*\)', awamil)
if len(emb) < 40:
    sys.exit(f"expected ≥40 embedded Awamil shawahid, parsed {len(emb)}")
path_ids = {"qatrPath": "qatr", "alfiyyaPath": "alfiyya", "mughniPath": "mughni"}
for name, pvar, line_no, quote in emb:
    if name not in theorems:
        sys.exit(f"Awamil shahid refers to missing theorem {name}")
    path = by_path[path_ids[pvar]]
    if not path.exists():
        continue
    line = path.read_text().splitlines()[int(line_no) - 1]
    for part in quote.split(" ... "):
        if part not in line:
            sys.exit(f"Awamil shahid for {name}: quote part '{part}' not at {pvar}:{line_no}")
print(f"PASS: {len(emb)} embedded Awamil shawahid verified against sources")

layers = {}
for r in rules["rules"]:
    layers.setdefault(r["layer"], 0); layers[r["layer"]] += 1
print(f"PASS: {len(rules['rules'])} rules → {sum(len(r['theorems']) for r in rules['rules'])} theorem refs; layers={layers}")
print(f"      total theorems in package: {len(theorems)}")
