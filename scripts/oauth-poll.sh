#!/bin/bash
# Get笔记 OAuth 授权轮询脚本
#
# 用法: ./oauth-poll.sh <code> [client_id]
#
# 参数:
#   code       - 授权码（从 /oauth/device/code 获取的 code 字段）
#   client_id  - 应用 ID（可选，默认: cli_a1b2c3d4e5f6789012345678abcdef90）
#
# 返回:
#   成功: 输出 JSON {"api_key": "...", "client_id": "...", "key_id": "...", "expires_at": ...}
#   失败: 输出错误信息到 stderr，退出非零状态码
#
# 退出码:
#   0 - 授权成功
#   2 - 用户拒绝授权
#   3 - 授权码已过期
#   4 - 授权码已被使用
#   5 - 未知错误
#   6 - 轮询超时
#
# 示例:
#   # 后台运行轮询
#   ./oauth-poll.sh "abc123..." &
#   
#   # 获取结果并写入配置
#   result=$(./oauth-poll.sh "abc123...")
#   api_key=$(echo "$result" | jq -r '.api_key')

set -e

CODE="$1"
CLIENT_ID="${2:-cli_a1b2c3d4e5f6789012345678abcdef90}"

if [ -z "$CODE" ]; then
    echo "用法: $0 <code> [client_id]" >&2
    exit 1
fi

API_URL="https://openapi.biji.com/open/api/v1/oauth/token"
INTERVAL=15      # 轮询间隔（秒）
MAX_ATTEMPTS=40  # 最大尝试次数（15秒 * 40 = 10分钟）

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
    attempt=$((attempt + 1))
    
    response=$(curl -s -X POST "$API_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"grant_type\": \"device_code\", \"client_id\": \"$CLIENT_ID\", \"code\": \"$CODE\"}")
    
    # 检查是否授权成功（返回 api_key）
    api_key=$(echo "$response" | jq -r '.data.api_key // empty')
    if [ -n "$api_key" ]; then
        # 授权成功，输出结果
        echo "$response" | jq '.data'
        exit 0
    fi
    
    # 检查状态消息
    msg=$(echo "$response" | jq -r '.data.msg // empty')
    case "$msg" in
        "authorization_pending")
            # 继续等待
            sleep $INTERVAL
            ;;
        "rejected")
            echo "用户拒绝了授权" >&2
            exit 2
            ;;
        "expired_token")
            echo "授权码已过期，请重新发起" >&2
            exit 3
            ;;
        "already_consumed")
            echo "授权码已被使用" >&2
            exit 4
            ;;
        *)
            echo "未知响应: $response" >&2
            exit 5
            ;;
    esac
done

echo "轮询超时（10分钟），请重新发起授权" >&2
exit 6
