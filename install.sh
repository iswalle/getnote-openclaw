#!/bin/bash
# Get笔记 OpenClaw Skill 安装脚本

set -e

SKILL_NAME="getnotes"
SKILL_DIR="${HOME}/.openclaw/workspace/skills/${SKILL_NAME}"
REPO_BASE="https://raw.githubusercontent.com/iswalle/getnote-openclaw/main"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "📦 Get笔记 Skill 安装程序"
echo ""

# 检查是否已安装
if [ -f "$SKILL_DIR/package.json" ]; then
    CURRENT_VERSION=$(grep '"version"' "$SKILL_DIR/package.json" | sed 's/.*"version": *"\([^"]*\)".*/\1/')
    echo -e "${YELLOW}⚠️  检测到已安装版本: v${CURRENT_VERSION}${NC}"
    echo "   正在更新..."
    echo ""
fi

# 创建目录
mkdir -p "$SKILL_DIR"

# 下载文件函数
download_file() {
    local file=$1
    local url="${REPO_BASE}/${file}"
    local dest="${SKILL_DIR}/${file}"
    
    if curl -sfL "$url" -o "$dest"; then
        echo -e "  ${GREEN}✓${NC} ${file}"
    else
        echo -e "  ${RED}✗${NC} ${file} 下载失败"
        return 1
    fi
}

echo "📥 下载文件..."
download_file "SKILL.md"
download_file "package.json"
download_file "README.md"

# 获取新版本号
NEW_VERSION=$(grep '"version"' "$SKILL_DIR/package.json" | sed 's/.*"version": *"\([^"]*\)".*/\1/')

echo ""
echo -e "${GREEN}✅ 安装完成！${NC} (v${NEW_VERSION})"
echo ""
echo "📖 使用方法："
echo "   在 OpenClaw 中说：「帮我查一下最近的笔记」"
echo "   或：「创建一个笔记，标题是...」"
echo ""
echo "🔑 首次使用需要配置 API Key（格式：gk_live_xxx.xxx）"
