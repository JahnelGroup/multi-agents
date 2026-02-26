#!/bin/bash
# Multi-agent training repo -- GRADER
#
# Verifies that tutorial outputs, pipeline artifacts, and sandbox code
# are correct. Run this after completing exercises (as a human or agent)
# to grade the work.
#
# Usage:
#   ./test-all.sh              Grade all phases
#   ./test-all.sh --phase 1    Grade Sandbox only
#   ./test-all.sh --phase 2    Grade Foundation only
#   ./test-all.sh --phase 3    Grade Practitioner only
#   ./test-all.sh --phase 4    Grade Expert only
#
# To wipe previous outputs before a fresh run: make reset

set -uo pipefail
cd "$(dirname "$0")"

PHASE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase)  PHASE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--phase N]"
      echo "  --phase N  Grade only phase N (0, 1, 2, 3, 4)"
      echo ""
      echo "To wipe outputs first: make reset"
      exit 0 ;;
    *) echo "Unknown flag: $1"; exit 1 ;;
  esac
done

FAILED=0

run_section() {
  local name="$1"
  local cmd="$2"
  echo ""
  echo "========== $name =========="
  if eval "$cmd"; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name"
    FAILED=1
  fi
}

echo "========== GRADER (TESTING.md) =========="

if [[ -z "$PHASE" || "$PHASE" == "0" ]]; then
  run_section "Phase 0: Gitignore" "make phase-0"
fi
if [[ -z "$PHASE" || "$PHASE" == "1" ]]; then
  run_section "Phase 1: Sandbox" "make phase-1"
fi
if [[ -z "$PHASE" || "$PHASE" == "2" ]]; then
  run_section "Phase 2: Foundation tutorials" "make phase-2"
fi
if [[ -z "$PHASE" || "$PHASE" == "3" ]]; then
  run_section "Phase 3: Practitioner tutorials" "make phase-3"
fi
if [[ -z "$PHASE" || "$PHASE" == "4" ]]; then
  run_section "Phase 4: Expert tutorials" "make phase-4"
fi

echo ""
echo "========== SUMMARY =========="
if [[ "$FAILED" -eq 0 ]]; then
  echo "All phases PASS"
  exit 0
else
  echo "One or more phases FAILED"
  exit 1
fi
