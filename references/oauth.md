# OAuth 授权配置

## 概述

使用 OAuth Device Flow 为用户授权并自动写入配置。适用于「配置 Get笔记」「连接 Get笔记」等场景，也是首次使用时自动触发的流程。

---

## 自动触发条件

每次调用 API 前，先检查 `$GETNOTE_API_KEY` 是否存在。若不存在，**自动发起 OAuth 授权流程**（无需用户主动说"配置"），告知用户需要先授权才能使用。

授权完成后，继续执行用户原本的请求。

---

## 手动配置（可选）

1. 前往 [Get笔记开放平台](https://www.biji.com/openapi) 创建应用
2. 获取 Client ID 和 API Key
3. 在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "getnote": {
        "apiKey": "gk_live_你的key",
        "env": {
          "GETNOTE_CLIENT_ID": "cli_你的id",
          "GETNOTE_OWNER_ID": "ou_你的飞书ID（可选，用于权限控制）"
        }
      }
    }
  }
}
```

---

## Device Flow 完整流程

### 步骤 1：申请授权码

```
POST https://openapi.biji.com/open/api/v1/oauth/device/code
Content-Type: application/json
```

请求体：
```json
{
  "client_id": "cli_a1b2c3d4e5f6789012345678abcdef90"
}
```

> ⚠️ **client_id 固定为 `cli_a1b2c3d4e5f6789012345678abcdef90`**，这是 Get笔记 为 OpenClaw 预注册的应用。

返回：
```json
{
  "success": true,
  "data": {
    "code": "abc123...",
    "verification_uri": "https://biji.com/openapi/oauth/authorize?code=abc123...",
    "user_code": "ABCD-1234",
    "expires_in": 600,
    "interval": 5
  }
}
```

| 字段 | 说明 |
|------|------|
| code | 授权码，轮询时使用 |
| verification_uri | 授权链接，**发送给用户点击** |
| user_code | 确认码，**必须展示给用户核对** |
| expires_in | 授权码有效期（秒），默认 600 |
| interval | 建议轮询间隔（秒），默认 5 |

### 步骤 2：展示授权链接

将 `verification_uri` 和 `user_code` 发送给用户：

> 🔗 请点击链接完成授权：
>
> {verification_uri}
>
> ⚠️ **请核对确认码**：`{user_code}`
>
> 授权页面会显示确认码，请确保与上面一致后再点击授权。授权码 10 分钟内有效。

**安全提醒**：`user_code` 用于防止钓鱼攻击。用户在授权页面看到的确认码必须与 Agent 展示的一致，不一致请勿授权。

**发送后立即启动后台轮询**（步骤 3）。

### 步骤 3：轮询等待授权

发送授权链接给用户后，**立即在后台启动轮询**，无需等待用户回复。

```
POST https://openapi.biji.com/open/api/v1/oauth/token
Content-Type: application/json
```

请求体：
```json
{
  "grant_type": "device_code",
  "client_id": "cli_a1b2c3d4e5f6789012345678abcdef90",
  "code": "{code}"
}
```

**轮询策略**：
- **间隔**：5 秒查询一次
- **超时**：最多轮询 10 分钟（与授权码有效期一致）
- **并行**：轮询在后台进行，不阻塞用户其他操作

**推荐：使用轮询脚本**

```bash
# 方式 1：后台轮询 + process poll 等待结果（OpenClaw 推荐）
exec: python scripts/oauth_poll.py "{code}"
  background: true

# 用 process poll 等待结果（最长等 10 分钟）
process: poll
  sessionId: {上一步返回的 sessionId}
  timeout: 600000

# 方式 2：简单等待（适合短时间）
result=$(python scripts/oauth_poll.py "{code}")
api_key=$(echo "$result" | jq -r '.api_key')
client_id=$(echo "$result" | jq -r '.client_id')
```

脚本会自动处理各种状态，成功时输出 JSON，失败时输出错误到 stderr。

**轮询响应状态**：

| 响应 | 说明 | 处理方式 |
|------|------|---------|
| `{"msg": "authorization_pending"}` | 用户尚未操作 | 继续轮询 |
| `{"msg": "rejected"}` | 用户拒绝授权 | **停止轮询**，告知用户已拒绝 |
| `{"msg": "expired_token"}` | 授权码已过期 | **停止轮询**，提示重新发起 |
| `{"msg": "already_consumed"}` | 授权码已使用 | **停止轮询**，可能已配置成功 |
| `{"api_key": "...", "client_id": "...", ...}` | **授权成功** | 进入步骤 4 |

**授权成功返回**：
```json
{
  "success": true,
  "data": {
    "client_id": "cli_a1b2c3d4e5f6789012345678abcdef90",
    "api_key": "gk_live_xxx",
    "key_id": "abc123",
    "expires_at": 1742000000
  }
}
```

| 字段 | 说明 |
|------|------|
| client_id | 应用 ID |
| api_key | API Key，**写入配置文件** |
| key_id | Key ID（管理用） |
| expires_at | 过期时间戳（Unix 秒），有效期 1 年 |

### 步骤 4：写入配置

将获取的凭证写入 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "getnote": {
        "apiKey": "{api_key}",
        "env": {
          "GETNOTE_CLIENT_ID": "{client_id}"
        }
      }
    }
  }
}
```

**告知用户**：

> ✅ Get笔记 配置完成！
>
> - API Key 有效期至 {expires_at 格式化日期}
> - 现在可以使用「记一下」「查笔记」等功能了
> - 如需注销授权，请访问：https://www.biji.com/openapi?tab=keys
