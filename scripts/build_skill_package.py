#!/usr/bin/env python3
"""Build the uploadable GetNote Skill archive.

The archive contains the main Skill and five domain references. Dependency
installation is declared in SKILL.md and remains under the host platform's
approval flow; no executable installer ships in the archive.
"""

from __future__ import annotations

import shutil
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STAGE = DIST / "getnote-skill"
SKILL_TEXT = (ROOT / "SKILL.md").read_text(encoding="utf-8")
VERSION_MATCH = re.search(r"(?m)^version:\s*([^\s]+)\s*$", SKILL_TEXT)
if VERSION_MATCH is None:
    raise RuntimeError("SKILL.md is missing a version")
VERSION = VERSION_MATCH.group(1)
ARCHIVE = DIST / f"getnote-skill-{VERSION}.zip"
LEGACY_ARCHIVE = DIST / "getnote-skill.zip"


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copy2(ROOT / "SKILL.md", STAGE / "SKILL.md")
    shutil.copytree(ROOT / "references", STAGE / "references")
    if LEGACY_ARCHIVE.exists():
        LEGACY_ARCHIVE.unlink()
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    shutil.make_archive(str(ARCHIVE.with_suffix("")), "zip", DIST, STAGE.name)
    print(ARCHIVE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
