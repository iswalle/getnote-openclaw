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
DOMAIN_SKILLS = sorted((ROOT / "skills").glob("getnote-*/SKILL.md"))
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


capability_result = run("capabilities", "-o", "json")
if capability_result.returncode != 0:
    fail(f"cannot read CLI capabilities: {capability_result.stdout.strip()}")

try:
    capabilities = json.loads(capability_result.stdout)
except json.JSONDecodeError as exc:
    fail(f"capabilities is not JSON: {exc}")

if capabilities.get("contract_version") != "2.0":
    fail(f"expected contract 2.0, got {capabilities.get('contract_version')!r}")

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
    fail("CLI does not expose all four knowledge scopes")

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
aliases = capabilities.get("command_aliases", {})
if aliases.get("gnote") != "getnote" or aliases.get("kb dir") != "kb directories":
    fail("CLI does not expose the compact gnote / kb dir aliases")

for alias, canonical in aliases.items():
    if alias == "gnote":
        continue
    if canonical not in available:
        fail(f"alias {alias!r} points to unknown command {canonical!r}")

main_text = MAIN_SKILL.read_text(encoding="utf-8")
if "/open/api/" in main_text:
    fail("main Skill must not contain OpenAPI paths")
for path in DOMAIN_SKILLS:
    expected_link = f"skills/{path.parent.name}/SKILL.md"
    if expected_link not in main_text:
        fail(f"main Skill does not route to {expected_link}")

if not DOMAIN_SKILLS:
    fail("no domain Skills found")

mentioned: set[str] = set()
for skill_path in DOMAIN_SKILLS:
    skill_text = skill_path.read_text(encoding="utf-8")
    if "/open/api/" in skill_text:
        fail(f"{skill_path} must not contain OpenAPI paths")
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
    result = run(*command.split(), "--help")
    if result.returncode != 0:
        fail(f"{command} --help exited {result.returncode}: {result.stdout.strip()}")
    if "Usage:" not in result.stdout or "-h, --help" not in result.stdout:
        fail(f"{command} has incomplete help")

print(
    f"contract 2.0 verified: {len(mentioned)} documented command paths all exist"
)
