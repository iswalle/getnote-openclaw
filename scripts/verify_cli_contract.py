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
SKILL = ROOT / "SKILL.md"
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
):
    if confirmation_flags.get(command) != "--yes":
        fail(f"CLI does not expose the --yes confirmation contract for {command}")

if guarantees.get("safe_long_input") != ["--content-file", "--stdin"]:
    fail("CLI does not expose both safe long-input paths")

if guarantees.get("knowledge_scopes") != ["DEFAULT", "BOOKSPACE", "CUSTOMER"]:
    fail("CLI does not preserve DEFAULT, BOOKSPACE and CUSTOMER knowledge scopes")

limits = guarantees.get("limits", {})
if limits.get("search_results") != 10 or limits.get("kb_note_batch") != 20:
    fail("CLI does not preserve search and knowledge-base batch limits")

available = {
    command
    for commands in capabilities.get("commands", {}).values()
    for command in commands
}

skill_text = SKILL.read_text(encoding="utf-8")
mentioned: set[str] = set()
for match in re.finditer(r"`getnote\s+([^`]+)`", skill_text):
    tokens = match.group(1).split()
    if not tokens or tokens[0].startswith(("<", "--")):
        continue
    for length in range(min(3, len(tokens)), 0, -1):
        candidate = " ".join(tokens[:length])
        if candidate in available:
            mentioned.add(candidate)
            break

    else:
        fail(f"documented command is absent from capabilities: getnote {match.group(1)}")

missing = sorted(mentioned - available)
if missing:
    fail(f"commands missing from capabilities: {', '.join(missing)}")

if not mentioned:
    fail("no getnote commands found in SKILL.md")

for command in sorted(mentioned):
    result = run(*command.split(), "--help")
    if result.returncode != 0:
        fail(f"{command} --help exited {result.returncode}: {result.stdout.strip()}")
    if "Usage:" not in result.stdout or "-h, --help" not in result.stdout:
        fail(f"{command} has incomplete help")

print(
    f"contract 2.0 verified: {len(mentioned)} documented command paths all exist"
)
