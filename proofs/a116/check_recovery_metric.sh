#!/usr/bin/env bash
set -euo pipefail
# Run from a mathlib v4.19.0 checkout with cached dependencies and Lean 4.19.0.
source_file="$1"
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
python3 - "$source_file" "$workdir/Checked.lean" <<'PY'
from pathlib import Path
import re,sys
s=Path(sys.argv[1]).read_text()
if re.search(r'\b(sorry|admit|axiom|native_decide)\b',s):
    raise SystemExit('Forbidden proof escape')
names=re.findall(r'^theorem\s+(\w+)',s,re.M)
Path(sys.argv[2]).write_text(s+'\n'+'\n'.join('#print axioms RecoveryMetric.'+n for n in names)+'\n')
print('THEOREMS',len(names))
PY
lake env lean "$workdir/Checked.lean" | tee "$workdir/axioms.log"
python3 - "$source_file" "$workdir/axioms.log" <<'PY'
from pathlib import Path
import re,sys
names=set(re.findall(r'^theorem\s+(\w+)',Path(sys.argv[1]).read_text(),re.M))
s=Path(sys.argv[2]).read_text()
seen=set()
for m in re.finditer(r"'RecoveryMetric\.(\w+)' (?:does not depend on any axioms|depends on axioms: \[([^\]]*)\])",s):
    seen.add(m[1]); dependencies=set((m[2] or '').replace('\n','').replace(' ','').split(','))-{''}
    if not dependencies <= {'propext','Quot.sound','Classical.choice'}:
        raise SystemExit('Unapproved dependency: '+str(dependencies))
if seen != names: raise SystemExit('Incomplete axiom audit')
print('PASS AXIOM AUDIT',len(seen))
PY
cat > "$workdir/False.lean" <<'LEAN'
import Mathlib
example : (0 : Fin 5) = 1 := by decide
LEAN
if lake env lean "$workdir/False.lean" > "$workdir/false.log" 2>&1; then
    echo 'ERROR: false claim accepted'; exit 1
fi
grep -F 'is false' "$workdir/false.log"
echo 'PASS FALSE CLAIM REJECTED'
