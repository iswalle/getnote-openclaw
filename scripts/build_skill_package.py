#!/usr/bin/env python3
"""Build the minimal uploadable GetNote Skill archive.

The archive intentionally contains only runtime Skill files.  Developer
scripts, GitHub workflows and human-facing README material remain in the
repository and are excluded from the package uploaded to an AI host.
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STAGE = DIST / "getnote-skill"
ARCHIVE = DIST / "getnote-skill.zip"


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copy2(ROOT / "SKILL.md", STAGE / "SKILL.md")
    shutil.copytree(ROOT / "skills", STAGE / "skills")

    if ARCHIVE.exists():
        ARCHIVE.unlink()
    shutil.make_archive(str(ARCHIVE.with_suffix("")), "zip", DIST, STAGE.name)
    print(ARCHIVE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
