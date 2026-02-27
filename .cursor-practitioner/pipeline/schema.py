"""
JG pipeline artifact schema validator.
Usage: python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/plan.json
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT_LIB = str(Path(__file__).resolve().parents[2] / "lib")
if ROOT_LIB not in sys.path:
    sys.path.insert(0, ROOT_LIB)

from pipeline_schema_common import load_artifact, validate_required_keys  # noqa: E402


def validate_artifact(path: Path) -> list[str]:
    name, data, errors = load_artifact(path)
    if errors:
        return errors
    if data is None:
        return [f"Could not load artifact: {name}"]
    return validate_required_keys(name, data)


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "--validate":
        print("Usage: python schema.py --validate <path-to-artifact.json>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[2])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    errors = validate_artifact(path)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
