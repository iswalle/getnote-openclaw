#!/usr/bin/env bash

# GetNote Skill runtime installer.
# --ensure: make the official CLI available without upgrading an existing CLI.
# --update: upgrade the CLI and refresh this Skill package from the latest release.

set -euo pipefail

PACKAGE_NAME="@getnote/cli"
MIN_NODE_MAJOR=20
RELEASE_URL_DEFAULT="https://github.com/iswalle/getnote-openclaw/releases/latest/download/getnote-skill.zip"

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

if ! command -v getnote >/dev/null 2>&1; then
  info "正在安装官方得到大脑 CLI…"
  npm install -g "${PACKAGE_NAME}@latest"
elif [ "$MODE" = "update" ]; then
  info "正在升级官方得到大脑 CLI…"
  npm install -g "${PACKAGE_NAME}@latest"
else
  info "已检测到官方得到大脑 CLI。"
fi

command -v getnote >/dev/null 2>&1 || fail "CLI 安装后仍不可执行，请检查 npm 全局 bin 是否已加入 PATH。"
info "CLI: $(getnote version 2>&1 | head -n 1)"

refresh_skill_package() {
  local release_url tmp_dir archive package_root skill_file
  release_url="${GETNOTE_SKILL_RELEASE_URL:-$RELEASE_URL_DEFAULT}"
  tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/getnote-skill-update.XXXXXX")"
  archive="$tmp_dir/getnote-skill.zip"

  if ! command -v curl >/dev/null 2>&1 || ! command -v unzip >/dev/null 2>&1; then
    info "已升级 CLI；当前环境没有 curl 或 unzip，Skill 文件请通过平台更新。"
    rm -rf "$tmp_dir"
    return 0
  fi
  if ! curl -fsSL --connect-timeout 15 --max-time 90 "$release_url" -o "$archive"; then
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
