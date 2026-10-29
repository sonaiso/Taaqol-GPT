#!/usr/bin/env bash
# فحص حزمة البرهان العربي: بناء، تدقيق البديهيات لكل مبرهنة، رفض ادعاءات خاطئة، تغطية القواعد.
set -euo pipefail
cd "$(dirname "$0")"
export PATH="${LEAN_BIN_DIR:-$(dirname "$(command -v lean)")}:$PATH"
export LEAN_PATH="$PWD/.lake/build/lib/lean"
lean --version | grep -F 'version 4.19.0'
lake build 2>&1 | grep -v '^trace' | tee build.log
if grep -q 'warning' build.log; then echo 'FAIL: warnings present' >&2; exit 1; fi
rm -f build.log
grep -rn 'sorry' Arabic/ && { echo 'FAIL: sorry found' >&2; exit 1; }
python3 check_axioms.py
python3 check_coverage.py
bash negative.sh
echo 'PASS: arabic proof package'
