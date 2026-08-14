#!/usr/bin/env python3
"""Build the uploadable GetNote Skill archive.

The archive contains the main Skill, five domain references and the runtime
installer. Developer-only validation scripts, GitHub workflows and README
material remain in the repository and are not shipped to an AI host.
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STAGE = DIST / "getnote-skill"
ARCHIVE = DIST / "getnote-skill.zip"
VERSION = "2.0.0"


def main() -> int:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if f'"version": "{VERSION}"' not in skill_text:
        raise RuntimeError("Skill metadata version and package version are inconsistent")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copy2(ROOT / "SKILL.md", STAGE / "SKILL.md")
    shutil.copytree(ROOT / "references", STAGE / "references")
    runtime_scripts = STAGE / "scripts"
    runtime_scripts.mkdir()
    shutil.copy2(ROOT / "scripts" / "install.sh", runtime_scripts / "install.sh")

    if ARCHIVE.exists():
        ARCHIVE.unlink()
    shutil.make_archive(str(ARCHIVE.with_suffix("")), "zip", DIST, STAGE.name)
    versioned_archive = DIST / f"getnote-skill-{VERSION}.zip"
    if versioned_archive.exists():
        versioned_archive.unlink()
    shutil.copy2(ARCHIVE, versioned_archive)
    print(ARCHIVE)
    print(versioned_archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
