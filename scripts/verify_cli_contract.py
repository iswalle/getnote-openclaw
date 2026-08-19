#!/usr/bin/env python3
"""Verify that every getnote command documented by the Skill exists in the CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAIN_SKILL = ROOT / "SKILL.md"
DOMAIN_REFERENCES = sorted((ROOT / "references").glob("*.md"))
CLI_SKILLS = Path(
    os.environ.get(
        "GETNOTE_CLI_SKILLS_DIR",
        str(ROOT.parent / "getnote-cli" / "skills"),
    )
)
CLI = os.environ.get("GETNOTE_CLI", "getnote")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [CLI, *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def fail(message: str) -> None:
    print(f"contract check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def skill_body(path: Path) -> str:
    """Return a CLI Skill body without its agent-only YAML front matter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return text
    _, _, body = text.split("---\n", 2)
    return body


capability_result = run("capabilities", "-o", "json")
if capability_result.returncode != 0:
    fail(f"cannot read CLI capabilities: {capability_result.stdout.strip()}")

try:
    capabilities = json.loads(capability_result.stdout)
except json.JSONDecodeError as exc:
    fail(f"capabilities is not JSON: {exc}")

contract_version = capabilities.get("contract_version")
if contract_version not in {"2.1", "2.2"}:
    fail(f"expected compatible contract 2.1 or 2.2, got {contract_version!r}")
if contract_version == "2.2":
    install_contract = capabilities.get("install", {})
    for key in ("detect_cli", "terminal", "platform_managed_cli", "verify", "success_condition", "managed_skill_boundary"):
        if not install_contract.get(key):
            fail(f"CLI install contract is missing {key}")
    upgrade_contract = capabilities.get("upgrade", {})
    for key in ("full", "verify", "managed_skill_boundary"):
        if not upgrade_contract.get(key):
            fail(f"CLI upgrade contract is missing {key}")

result_contracts = capabilities.get("result_contracts", {})
for key in (
    "common_success",
    "common_error",
    "save",
    "task",
    "notes",
    "note",
    "search",
    "knowledge",
    "tags",
):
    if not result_contracts.get(key):
        fail(f"CLI does not expose result contract {key}")

guarantees = capabilities.get("guarantees", {})
for key in (
    "ids_as_strings",
    "structured_business_errors",
    "final_async_save_result",
    "environment_note_url",
    "image_format_validation",
):
    if guarantees.get(key) is not True:
        fail(f"CLI does not guarantee {key}")

confirmation_flags = guarantees.get("confirmation_flags", {})
for command in (
    "note update content_or_tags",
    "note delete",
    "note share",
    "kb remove",
    "kb directory-delete",
):
    if confirmation_flags.get(command) != "--yes":
        fail(f"CLI does not expose the --yes confirmation contract for {command}")

if guarantees.get("safe_long_input") != ["--content-file", "--stdin"]:
    fail("CLI does not expose both safe long-input paths")

if guarantees.get("knowledge_scopes") != ["DEFAULT", "BOOKSPACE", "CUSTOMER", "TEAMSPACE"]:
	fail("CLI does not expose all four public knowledge scopes")

if guarantees.get("knowledge_features") != [
    "directories",
    "add_to_directory",
    "douyin_blogger_subscription",
]:
    fail("CLI does not expose the complete knowledge-management contract")

if guarantees.get("note_detail_views") != [
    "summary",
    "original",
    "transcript",
    "attachments",
    "timeline",
    "quick_note",
    "meeting_todos",
]:
    fail("CLI does not expose all first-class note detail views")

limits = guarantees.get("limits", {})
if limits.get("search_results") != 10 or limits.get("kb_note_batch") != 20:
    fail("CLI does not preserve search and knowledge-base batch limits")

available = {
    command
    for commands in capabilities.get("commands", {}).values()
    for command in commands
}
command_results = capabilities.get("command_results", {})
for command in sorted(available - {"auth", "tag"}):
    result = command_results.get(command)
    if not isinstance(result, dict) or not result.get("success_fields"):
        fail(f"CLI does not expose per-command result contract for {command!r}")
aliases = capabilities.get("command_aliases", {})
if aliases.get("gnote") != "getnote" or aliases.get("kb dir") != "kb directories":
    fail("CLI does not expose the compact gnote / kb dir aliases")

for alias, canonical in aliases.items():
    if alias == "gnote":
        continue
    if canonical not in available:
        fail(f"alias {alias!r} points to unknown command {canonical!r}")

main_text = MAIN_SKILL.read_text(encoding="utf-8")
if "version: 2.0.3" not in main_text:
    fail("main Skill must expose version 2.0.3")
if "/open/api/" in main_text:
    fail("main Skill must not contain OpenAPI paths")
for required in (
    'bins: ["getnote"]',
    'package: "@getnote/cli"',
    "getnote auth login",
    "getnote doctor -o json",
):
    if required not in main_text:
        fail(f"main Skill is missing installation or verification step: {required}")
for path in DOMAIN_REFERENCES:
    expected_link = f"references/{path.name}"
    if expected_link not in main_text:
        fail(f"main Skill does not route to {expected_link}")

if not DOMAIN_REFERENCES:
    fail("no domain references found")

reference_sources = {
    "auth.md": "getnote-auth",
    "kb.md": "getnote-kb",
    "note.md": "getnote-note",
    "search.md": "getnote-search",
    "tag.md": "getnote-tag",
}
if {path.name for path in DOMAIN_REFERENCES} != set(reference_sources):
    fail("independent Skill references do not match the five supported domains")
for reference_name, cli_skill_name in reference_sources.items():
    # The independent package has platform-managed dependency installation and
    # deliberately keeps auth lifecycle instructions separate from CLI-bundled
    # Skill installation instructions.
    if reference_name == "auth.md":
        continue
    reference = ROOT / "references" / reference_name
    cli_skill = CLI_SKILLS / cli_skill_name / "SKILL.md"
    if not cli_skill.is_file() or reference.read_text(encoding="utf-8") != skill_body(cli_skill):
        fail(f"reference {reference_name} drifted from CLI Skill {cli_skill_name}")

if (ROOT / "scripts" / "install.sh").exists():
    fail("uploadable Skill must not ship a self-install or self-update script")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
if readme.count("### 方式") != 2:
    fail("README must expose exactly two installation methods")
for required in (
    "https://github.com/iswalle/getnote-openclaw",
    "https://github.com/iswalle/getnote-openclaw/releases/latest",
    "下载最新版 ZIP",
    "Skill 本身不会执行下载脚本或自行覆盖文件",
    "**v2.0.3**",
):
    if required not in readme:
        fail(f"README is missing user-facing installation information: {required}")

builder_text = (ROOT / "scripts" / "build_skill_package.py").read_text(encoding="utf-8")
if 'ROOT / "README.md"' in builder_text:
    fail("uploadable Skill archive must contain runtime Skill files only")
if 'ARCHIVE = DIST / f"getnote-skill-{VERSION}.zip"' not in builder_text:
    fail("builder must create a versioned Skill package")
if 'shutil.copy2(ARCHIVE, versioned_archive)' in builder_text:
    fail("builder must not create duplicate stable and versioned packages")

mentioned: set[str] = set()
for reference_path in DOMAIN_REFERENCES:
    skill_text = reference_path.read_text(encoding="utf-8")
    if "/open/api/" in skill_text:
        fail(f"{reference_path} must not contain OpenAPI paths")
    if (
        "结果与回复格式" not in skill_text
        and "命令结果与回复格式" not in skill_text
        and "结果与下一步" not in skill_text
        and "命令结果与用户呈现" not in skill_text
    ):
        fail(f"{reference_path} does not define per-command result guidance")
    for match in re.finditer(r"`(?:getnote|gnote)\s+([^`]+)`", skill_text):
        tokens = match.group(1).split()
        if not tokens or tokens[0].startswith(("<", "--")):
            continue
        for length in range(min(3, len(tokens)), 0, -1):
            candidate = " ".join(tokens[:length])
            canonical = aliases.get(candidate, candidate)
            if canonical in available:
                mentioned.add(canonical)
                break
        else:
            fail(f"documented command is absent from capabilities: {match.group(0)}")

missing = sorted(mentioned - available)
if missing:
    fail(f"commands missing from capabilities: {', '.join(missing)}")

uncovered = sorted(
    command
    for command in available - mentioned
    if not any(item.startswith(command + " ") for item in mentioned)
)
if uncovered:
    fail("CLI commands missing from domain Skills: " + ", ".join(uncovered))

for command in sorted(mentioned):
    if command not in {"auth", "tag"} and command not in command_results:
        fail(f"documented command has no per-command result contract: {command}")
    result = run(*command.split(), "--help")
    if result.returncode != 0:
        fail(f"{command} --help exited {result.returncode}: {result.stdout.strip()}")
    if "Usage:" not in result.stdout or "-h, --help" not in result.stdout:
        fail(f"{command} has incomplete help")

print(
    f"contract {contract_version} verified: {len(mentioned)} documented command paths, result contracts and help all exist"
)
