#!/usr/bin/env bash
# check-docs.sh — docs integrity checks (broken links + known-bad URLs + mirror drift)
# Usage: ./scripts/check-docs.sh
# Exit code: 0 = all checks pass, 1 = failures found

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0

echo "=== Docs integrity checks ==="

# 1. Detect known-bad URLs in first-party markdown files
echo ""
echo "--- Check 1: known-bad URLs ---"
BAD_URLS=(
  "cursor.com/learn/developing-features"
)
for URL in "${BAD_URLS[@]}"; do
  MATCHES=$(grep -r --include="*.md" --include="*.mdc" \
    --exclude-dir=node_modules --exclude-dir=.git \
    -l "$URL" "$ROOT" 2>/dev/null || true)
  if [ -n "$MATCHES" ]; then
    echo "FAIL: Found banned URL '$URL' in:"
    echo "$MATCHES" | sed 's/^/  /'
    FAIL=1
  else
    echo "PASS: No occurrences of '$URL'"
  fi
done

# 2. Detect broken local markdown links (missing targets)
echo ""
echo "--- Check 2: broken local markdown links ---"
python3 - <<PY
import re, sys
from pathlib import Path

root = Path("$ROOT")
exclude = {"node_modules", ".git", "dist", "build"}
link_re = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
errors = []

for f in root.rglob("*"):
    if not f.is_file():
        continue
    if f.suffix.lower() not in {".md", ".mdc"}:
        continue
    if set(f.parts) & exclude:
        continue
    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for m in link_re.finditer(text):
        target = m.group(2).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = target.split("#", 1)[0].strip()
        if not path_part:
            continue
        candidate = (root / path_part.lstrip("/")) if path_part.startswith("/") else (f.parent / path_part)
        if not candidate.exists():
            errors.append(f"  BROKEN: {f.relative_to(root)} -> {target}")

if errors:
    print("FAIL: broken local links found:")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("PASS: no broken local links")
PY
[ $? -eq 0 ] || FAIL=1

# 3. Mirror drift: check that .cursor/ matches .cursor-expert/
echo ""
echo "--- Check 3: .cursor/ vs .cursor-expert/ mirror drift ---"
python3 - <<PY
import sys
from pathlib import Path

root = Path("$ROOT")
expert = root / ".cursor-expert"
active = root / ".cursor"

drifted = []
for src in expert.rglob("*"):
    if not src.is_file():
        continue
    rel = src.relative_to(expert)
    dst = active / rel
    if not dst.exists():
        drifted.append(f"  MISSING in .cursor/: {rel}")
    elif src.read_bytes() != dst.read_bytes():
        drifted.append(f"  DIFFERS: {rel}")

if drifted:
    print("WARN: .cursor/ is out of sync with .cursor-expert/:")
    for d in drifted:
        print(d)
    print("  Run: cp -r .cursor-expert/. .cursor/")
    # Warning only — don't fail CI for this
else:
    print("PASS: .cursor/ matches .cursor-expert/")
PY

echo ""
if [ $FAIL -eq 0 ]; then
  echo "=== All checks PASS ==="
  exit 0
else
  echo "=== FAILURES found — see above ==="
  exit 1
fi
