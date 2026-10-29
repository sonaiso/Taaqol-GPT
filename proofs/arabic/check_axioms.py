"""يطلب من Lean بديهيات كل مبرهنة في كل وحدة ويرفض أي بديهية خارج السياسة."""
import pathlib, re, subprocess, sys, tempfile

ALLOWED = {"propext", "Quot.sound", "Classical.choice"}
root = pathlib.Path(__file__).parent
modules = sorted(p for p in (root / "Arabic").glob("*.lean"))
names = {}
FORBIDDEN = re.compile(r"\b(sorry|native_decide|axiom|unsafe|implemented_by|extern|partial|opaque|admit)\b")
for p in modules:
    src = p.read_text()
    for i, line in enumerate(src.splitlines(), 1):
        if FORBIDDEN.search(line):
            sys.exit(f"forbidden escape hatch in {p.name}:{i}: {line.strip()}")
    found = re.findall(r"^\s*(?:theorem|lemma)\s+([\w.]+)", src, re.M)
    names[p.stem] = found
total = sum(len(v) for v in names.values())
if total == 0:
    sys.exit("no theorems found")
with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=root, delete=False) as f:
    for m in names:
        f.write(f"import Arabic.{m}\n")
    for m, ns in names.items():
        for n in ns:
            f.write(f"#print axioms Arabic.{n}\n")
    tmp = pathlib.Path(f.name)
try:
    out = subprocess.run(
        ["lean", str(tmp)], cwd=root, capture_output=True, text=True,
        env={**__import__("os").environ, "LEAN_PATH": str(root / ".lake/build/lib/lean")},
    )
finally:
    tmp.unlink()
if out.returncode != 0:
    sys.exit(out.stdout + out.stderr)
seen = set()
for line in out.stdout.splitlines():
    m = re.fullmatch(r"'Arabic\.([\w.]+)' (does not depend on any axioms|depends on axioms: \[(.*)\])", line)
    if not m:
        sys.exit("Unexpected Lean output: " + line)
    seen.add(m[1])
    axioms = {s.strip() for s in (m[3] or "").split(",") if s.strip()}
    if not axioms <= ALLOWED:
        sys.exit(f"Unapproved axioms in {m[1]}: {axioms}")
expected = {n for ns in names.values() for n in ns}
if seen != expected:
    sys.exit(f"coverage mismatch: missing {expected - seen}, extra {seen - expected}")
print(f"PASS: {total} theorems, axioms within policy")
