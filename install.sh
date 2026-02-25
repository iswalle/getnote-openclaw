#!/bin/bash
# Get笔记 OpenClaw Skill 安装脚本

SKILL_DIR="${HOME}/.openclaw/workspace/skills/getnotes"

echo "📦 安装 Get笔记 Skill..."

# 创建目录
mkdir -p "$SKILL_DIR"

# 下载文件
curl -sL "https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/SKILL.md" -o "$SKILL_DIR/SKILL.md"
curl -sL "https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/package.json" -o "$SKILL_DIR/package.json"

echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  在 OpenClaw 中说：「帮我查一下最近的笔记」"
echo "  或：「创建一个笔记，标题是...」"
