#!/usr/bin/env python3
"""Sync or verify the standalone package's domain Skills against getnote-cli."""

from __future__ import annotations

import argparse
import filecmp
import os
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "skills"
DEFAULT_SOURCE = ROOT.parent / "getnote-cli" / "skills"
SOURCE = Path(os.environ.get("GETNOTE_CLI_SKILLS_DIR", DEFAULT_SOURCE)).resolve()


def skill_dirs(root: Path) -> list[Path]:
    return sorted(path.parent for path in root.glob("getnote-*/SKILL.md"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="only verify committed copies")
    args = parser.parse_args()

    sources = skill_dirs(SOURCE)
    if not sources:
        print(f"no CLI Skills found in {SOURCE}", file=sys.stderr)
        return 1

    expected = {path.name for path in sources}
    actual = {path.name for path in skill_dirs(TARGET)}
    if args.check:
        if actual != expected:
            print(f"Skill sets differ: CLI={sorted(expected)} standalone={sorted(actual)}", file=sys.stderr)
            return 1
        drift = [name for name in sorted(expected) if not filecmp.cmp(SOURCE / name / "SKILL.md", TARGET / name / "SKILL.md", shallow=False)]
        if drift:
            print("domain Skills drifted from CLI: " + ", ".join(drift), file=sys.stderr)
            return 1
        print(f"verified {len(expected)} domain Skills are byte-for-byte aligned with CLI")
        return 0

    TARGET.mkdir(parents=True, exist_ok=True)
    for old in skill_dirs(TARGET):
        if old.name not in expected:
            shutil.rmtree(old)
    for source in sources:
        destination = TARGET / source.name
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "SKILL.md", destination / "SKILL.md")
    print(f"synced {len(expected)} domain Skills from {SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
