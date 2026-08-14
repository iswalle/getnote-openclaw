#!/usr/bin/env bash

# GetNote Skill runtime installer.
# --ensure: install or align the official CLI with the current latest release.
# --update: upgrade the CLI and refresh this Skill package from the latest release.

set -euo pipefail

PACKAGE_NAME="@getnote/cli"
MIN_NODE_MAJOR=20
RELEASE_API_DEFAULT="https://api.github.com/repos/iswalle/getnote-openclaw/releases/latest"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODE="ensure"

info() { printf '[getnote] %s\n' "$*"; }
fail() { printf '[getnote] %s\n' "$*" >&2; exit 1; }

case "${1:---ensure}" in
  --ensure) MODE="ensure" ;;
  --update) MODE="update" ;;
  --help|-h)
    printf '%s\n' 'Usage: bash scripts/install.sh [--ensure|--update]'
    printf '%s\n' '  --ensure  Ensure the official GetNote CLI is available (default).'
    printf '%s\n' '  --update  Upgrade the CLI and refresh this installed Skill package.'
    exit 0
    ;;
  *) fail "不支持的参数: $1" ;;
esac

command -v node >/dev/null 2>&1 || fail "需要 Node.js ${MIN_NODE_MAJOR}+；请先安装 Node.js 后重试。"
command -v npm >/dev/null 2>&1 || fail "未找到 npm；请修复 Node.js 安装后重试。"

NODE_VERSION="$(node --version | sed 's/^v//' | cut -d. -f1)"
case "$NODE_VERSION" in
  ''|*[!0-9]*) fail "无法识别 Node.js 版本。" ;;
esac
if [ "$NODE_VERSION" -lt "$MIN_NODE_MAJOR" ]; then
  fail "当前 Node.js 主版本为 ${NODE_VERSION}，需要 ${MIN_NODE_MAJOR}+。"
fi

# 始终从官方 npm 包校准 CLI。不能仅凭 PATH 中存在同名 `getnote`
# 就认定它是官方组件；npm 重复安装不会读写 ~/.getnote 授权凭证。
if [ "$MODE" = "update" ]; then
  info "正在升级官方得到大脑 CLI…"
else
  info "正在检查并安装官方得到大脑 CLI…"
fi
npm install -g "${PACKAGE_NAME}@latest"

# npm may install into a prefix whose bin directory is not yet in this
# process's PATH (common in desktop Agents and WorkBuddy sandboxes).
NPM_PREFIX="$(npm prefix -g 2>/dev/null || true)"
if [ -n "$NPM_PREFIX" ] && [ -d "$NPM_PREFIX/bin" ]; then
  PATH="$NPM_PREFIX/bin:$PATH"
  export PATH
fi

command -v getnote >/dev/null 2>&1 || fail "CLI 安装后仍不可执行，请检查 npm 全局 bin 是否已加入 PATH。"
info "CLI: $(getnote version 2>&1 | head -n 1)"

refresh_skill_package() {
  local release_url release_api release_json remote_version local_version tmp_dir archive package_root skill_file
  release_url="${GETNOTE_SKILL_RELEASE_URL:-}"
  release_api="${GETNOTE_SKILL_RELEASE_API:-$RELEASE_API_DEFAULT}"
  tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/getnote-skill-update.XXXXXX")"
  archive="$tmp_dir/getnote-skill.zip"

  if ! command -v curl >/dev/null 2>&1 || ! command -v unzip >/dev/null 2>&1; then
    info "已升级 CLI；当前环境没有 curl 或 unzip，Skill 文件请通过平台更新。"
    rm -rf "$tmp_dir"
    return 0
  fi
  if [ -z "$release_url" ]; then
    release_json="$tmp_dir/release.json"
    if curl -fsSL --connect-timeout 15 --max-time 30 "$release_api" -o "$release_json"; then
      remote_version="$(node -e '
const fs = require("fs");
const release = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
process.stdout.write(String(release.tag_name || "").replace(/^v/, ""));
' "$release_json")"
      release_url="$(node -e '
const fs = require("fs");
const release = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const assets = release.assets || [];
const preferred = assets.find((item) => item.name === "getnote-skill.zip")
  || assets.find((item) => /^getnote-skill-[0-9][0-9A-Za-z._-]*\.zip$/.test(item.name || ""));
if (preferred && preferred.browser_download_url) process.stdout.write(preferred.browser_download_url);
' "$release_json")"
      local_version="$(sed -n 's/^version: \([0-9][0-9.]*\)$/\1/p' "$SKILL_DIR/SKILL.md" | head -n 1)"
      if [ -n "$local_version" ] && [ -n "$remote_version" ] && ! node -e '
const current = process.argv[1].split(".").map(Number);
const remote = process.argv[2].split(".").map(Number);
for (let index = 0; index < Math.max(current.length, remote.length); index += 1) {
  const left = current[index] || 0;
  const right = remote[index] || 0;
  if (right > left) process.exit(0);
  if (right < left) process.exit(1);
}
process.exit(0);
' "$local_version" "$remote_version"; then
        info "已升级 CLI；线上 Skill ${remote_version} 早于当前 ${local_version}，当前 Skill 保持不变。"
        rm -rf "$tmp_dir"
        return 0
      fi
    fi
  fi
  if [ -z "$release_url" ] || ! curl -fsSL --connect-timeout 15 --max-time 90 "$release_url" -o "$archive"; then
    info "已升级 CLI；暂时没有可下载的新版 Skill 包，当前 Skill 保持不变。"
    rm -rf "$tmp_dir"
    return 0
  fi
  unzip -q "$archive" -d "$tmp_dir/unpacked"
  skill_file="$(find "$tmp_dir/unpacked" -type f -name SKILL.md -print | head -n 1)"
  package_root=""
  if [ -n "$skill_file" ]; then
    package_root="$(dirname "$skill_file")"
  fi
  if [ -z "$package_root" ] || [ ! -f "$package_root/scripts/install.sh" ] || [ ! -d "$package_root/references" ]; then
    info "已升级 CLI；下载的 Skill 包结构无效，当前 Skill 保持不变。"
    rm -rf "$tmp_dir"
    return 0
  fi
  cp "$package_root/SKILL.md" "$SKILL_DIR/SKILL.md"
  # 2.0 将领域资料统一放在 references；清理旧包遗留的 skills，避免 Agent 读取过期说明。
  if [ -d "$SKILL_DIR/skills" ]; then
    rm -rf "$SKILL_DIR/skills"
  fi
  rm -rf "$SKILL_DIR/references"
  mkdir -p "$SKILL_DIR/references"
  cp -R "$package_root/references/." "$SKILL_DIR/references/"
  cp "$package_root/scripts/install.sh" "$SKILL_DIR/scripts/install.sh"
  chmod +x "$SKILL_DIR/scripts/install.sh"
  rm -rf "$tmp_dir"
  info "已刷新得到大脑 Skill。"
}

if [ "$MODE" = "update" ]; then
  refresh_skill_package
fi
