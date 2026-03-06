#!/bin/bash
#
# Get笔记图片上传脚本
# 用法: ./upload_image.sh <本地图片路径> [API_KEY]
#
# 示例:
#   ./upload_image.sh /path/to/image.jpg
#   ./upload_image.sh /path/to/image.jpg gk_live_xxx
#
# 环境变量:
#   GETNOTE_API_KEY - API Key（如未提供参数则使用此变量）
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 参数检查
IMAGE_PATH="$1"
API_KEY="${2:-$GETNOTE_API_KEY}"

if [ -z "$IMAGE_PATH" ]; then
    echo -e "${RED}错误: 请提供图片路径${NC}"
    echo "用法: $0 <本地图片路径> [API_KEY]"
    exit 1
fi

if [ ! -f "$IMAGE_PATH" ]; then
    echo -e "${RED}错误: 文件不存在: $IMAGE_PATH${NC}"
    exit 1
fi

if [ -z "$API_KEY" ]; then
    echo -e "${RED}错误: 请提供 API Key（参数或环境变量 GETNOTE_API_KEY）${NC}"
    exit 1
fi

# 获取文件 MIME 类型
get_mime_type() {
    local ext="${1##*.}"
    case "$ext" in
        jpg|jpeg) echo "image/jpeg" ;;
        png) echo "image/png" ;;
        gif) echo "image/gif" ;;
        webp) echo "image/webp" ;;
        *) echo "image/jpeg" ;;
    esac
}

MIME_TYPE=$(get_mime_type "$IMAGE_PATH")

echo -e "${YELLOW}[1/3] 获取上传凭证...${NC}"

# 步骤 1: 获取上传凭证
TOKEN_RESP=$(curl -s -X GET \
    "https://openapi.biji.com/open/api/v1/resource/image/upload_token?count=1&mime_type=$MIME_TYPE" \
    -H "Authorization: $API_KEY")

# 检查响应
SUCCESS=$(echo "$TOKEN_RESP" | grep -o '"success":\s*true' || true)
if [ -z "$SUCCESS" ]; then
    echo -e "${RED}获取凭证失败:${NC}"
    echo "$TOKEN_RESP" | python3 -m json.tool 2>/dev/null || echo "$TOKEN_RESP"
    exit 1
fi

# 解析响应
SIGN_URL=$(echo "$TOKEN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['tokens'][0]['sign_url'])" 2>/dev/null)
GET_URL=$(echo "$TOKEN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['tokens'][0]['get_url'])" 2>/dev/null)

if [ -z "$SIGN_URL" ]; then
    echo -e "${RED}解析凭证失败${NC}"
    echo "$TOKEN_RESP"
    exit 1
fi

echo -e "${GREEN}✓ 凭证获取成功${NC}"

echo -e "${YELLOW}[2/3] 上传图片到 OSS...${NC}"

# 步骤 2: 上传到 OSS
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT \
    -H "Content-Type: $MIME_TYPE" \
    --data-binary "@$IMAGE_PATH" \
    "$SIGN_URL")

if [ "$HTTP_CODE" != "200" ]; then
    echo -e "${RED}上传失败: HTTP $HTTP_CODE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 上传成功${NC}"

echo -e "${YELLOW}[3/3] 完成${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}图片上传成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "访问 URL: ${YELLOW}$GET_URL${NC}"
echo ""
echo -e "💡 创建图片笔记:"
echo -e "   curl -X POST \"https://openapi.biji.com/open/api/v1/resource/note/save?task_id=...\""
echo -e "     -H \"Authorization: \$GETNOTE_API_KEY\""
echo -e "     -H \"Content-Type: application/json\""
echo -e "     -d '{\"type\":\"img_text\",\"image_urls\":[\"$GET_URL\"]}'"
