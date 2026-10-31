#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
LEAN_BIN="${LEAN_BIN:-lean}"
"$LEAN_BIN" --version
"$LEAN_BIN" --version | grep -F 'version 4.19.0'
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT
cp A116.lean "$tmp_dir/Positive.lean"
# Ask Lean about every named theorem, including transitive dependencies.
python3 - "$tmp_dir/Positive.lean" <<'PY'
import pathlib
import re
import sys
path = pathlib.Path(sys.argv[1])
source = path.read_text()
names = re.findall(r'^theorem\s+(\w+)', source, re.M)
path.write_text(source + '\n' + '\n'.join('#print axioms A116.' + n for n in names))
PY
"$LEAN_BIN" -DwarningAsError=true "$tmp_dir/Positive.lean" | tee "$tmp_dir/positive.log"
python3 - "$tmp_dir/positive.log" <<'PY'
import pathlib
import re
import sys
source = pathlib.Path('A116.lean').read_text()
names = set(re.findall(r'^theorem\s+(\w+)', source, re.M))
log = pathlib.Path(sys.argv[1]).read_text()
seen = set()
for line in log.splitlines():
    match = re.fullmatch(r"'A116\.(\w+)' (does not depend on any axioms|depends on axioms: \[(.*)\])", line)
    if not match:
        raise SystemExit('Unexpected Lean output: ' + line)
    seen.add(match[1])
    axioms = set(filter(None, (s.strip() for s in (match[3] or '').split(','))))
    if not axioms <= {'propext', 'Quot.sound', 'Classical.choice'}:
        raise SystemExit('Unapproved axioms: ' + repr(axioms))
if seen != names:
    raise SystemExit('Axiom report coverage mismatch')
print('PASS: all theorem axiom reports checked')
PY
cp A116.lean "$tmp_dir/Negative.lean"
cat >> "$tmp_dir/Negative.lean" <<'LEAN'

example : A116.Safe (A116.run A116.q0 [A116.k]) := by decide
LEAN
if "$LEAN_BIN" "$tmp_dir/Negative.lean" > "$tmp_dir/negative.log" 2>&1; then
  echo 'FAIL: false initial-sukun safety claim was accepted' >&2
  exit 1
fi
grep -F 'is false' "$tmp_dir/negative.log"
echo 'PASS: false safety claim rejected'
