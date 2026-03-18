#!/usr/bin/env python3
"""
Get笔记 OAuth 授权轮询脚本

用法:
    python oauth_poll.py <code> [client_id]

参数:
    code       - 授权码（从 /oauth/device/code 获取的 code 字段）
    client_id  - 应用 ID（可选，默认: cli_a1b2c3d4e5f6789012345678abcdef90）

返回:
    成功: 输出 JSON {"api_key": "...", "client_id": "...", "key_id": "...", "expires_at": ...}
    失败: 输出错误信息到 stderr，退出非零状态码

退出码:
    0 - 授权成功
    2 - 用户拒绝授权
    3 - 授权码已过期
    4 - 授权码已被使用
    5 - 未知错误
    6 - 轮询超时

示例:
    result=$(python oauth_poll.py "abc123...")
    api_key=$(echo "$result" | jq -r '.api_key')
"""

import sys
import time
import json
import urllib.request
import urllib.error

API_URL = "https://openapi.biji.com/open/api/v1/oauth/token"
DEFAULT_CLIENT_ID = "cli_a1b2c3d4e5f6789012345678abcdef90"
INTERVAL = 5       # 轮询间隔（秒）
MAX_ATTEMPTS = 120 # 最大尝试次数（5秒 * 120 = 10分钟）


def poll_token(code: str, client_id: str) -> dict:
    """轮询授权状态，返回授权结果或抛出异常"""
    
    payload = json.dumps({
        "grant_type": "device_code",
        "client_id": client_id,
        "code": code
    }).encode('utf-8')
    
    headers = {"Content-Type": "application/json"}
    
    for attempt in range(MAX_ATTEMPTS):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except urllib.error.URLError as e:
            print(f"网络错误: {e}", file=sys.stderr)
            time.sleep(INTERVAL)
            continue
        
        # 检查是否授权成功
        if data.get("success") and data.get("data", {}).get("api_key"):
            return data["data"]
        
        # 检查状态消息
        msg = data.get("data", {}).get("msg", "")
        
        if msg == "authorization_pending":
            time.sleep(INTERVAL)
            continue
        elif msg == "rejected":
            print("用户拒绝了授权", file=sys.stderr)
            sys.exit(2)
        elif msg == "expired_token":
            print("授权码已过期，请重新发起", file=sys.stderr)
            sys.exit(3)
        elif msg == "already_consumed":
            print("授权码已被使用", file=sys.stderr)
            sys.exit(4)
        else:
            print(f"未知响应: {data}", file=sys.stderr)
            sys.exit(5)
    
    print("轮询超时（10分钟），请重新发起授权", file=sys.stderr)
    sys.exit(6)


def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <code> [client_id]", file=sys.stderr)
        sys.exit(1)
    
    code = sys.argv[1]
    client_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CLIENT_ID
    
    result = poll_token(code, client_id)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
