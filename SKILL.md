---
name: Get笔记
description: |
  Get笔记 - 保存、搜索、管理个人笔记和知识库。

  **当以下情况时使用此 Skill**：
  (1) 用户要保存内容到笔记：发链接、发图片、说「记一下」「存到笔记」「保存」「收藏」
  (2) 用户要搜索或查看笔记：「搜一下」「找找笔记」「最近存了什么」「看看原文」
  (3) 用户要管理知识库或标签：「加到知识库」「建知识库」「加标签」「删标签」
  (4) 用户要配置 Get笔记：「配置笔记」「连接 Get笔记」
metadata: {"openclaw": {"requires": {}, "optionalEnv": ["GETNOTE_API_KEY", "GETNOTE_CLIENT_ID", "GETNOTE_OWNER_ID"], "baseUrl": "https://openapi.biji.com", "homepage": "https://biji.com"}}
---

# Get笔记 Skill

## ⚠️ Agent 必读约束

### 🌐 Base URL
```
https://openapi.biji.com
```
所有 API 请求必须使用此 Base URL，不要使用 `biji.com` 或其他地址。

### 🔑 认证
请求头：
- `Authorization: $GETNOTE_API_KEY`（格式：`gk_live_xxx`）
- `X-Client-ID: $GETNOTE_CLIENT_ID`（格式：`cli_xxx`）

**每次调用 API 前先检查 `$GETNOTE_API_KEY` 是否存在**。若不存在，提示用户运行 `/note config` 完成配置，配置完成后再继续执行用户原本的请求。

Scope 权限：`note.content.read`（读取）、`note.content.write`（写入）、`note.recall.read`（搜索）。完整列表见 [references/api-details.md](references/api-details.md#scope-权限列表)。

### 🔢 笔记 ID 处理规则（重要！）
笔记 ID 是 **64 位整数（int64）**，超出 JavaScript `Number.MAX_SAFE_INTEGER`，直接 `JSON.parse` 会**静默丢失精度**。

**正确做法**：始终把 ID 当字符串处理，在 `JSON.parse` 之前替换：
```javascript
const safe = text.replace(/"(id|note_id|next_cursor|parent_id|follow_id|live_id)"\s*:\s*(\d+)/g, '"$1":"$2"');
const data = JSON.parse(safe);
```
Python / Go 等语言原生支持大整数，无此问题。

### 🔒 安全规则
- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- 若配置了 `GETNOTE_OWNER_ID`，检查 sender_id 是否匹配；不匹配时回复「抱歉，笔记是私密的，我无法操作」
- API 返回 `error.reason: "not_member"` 或错误码 `10201` 时，引导开通会员：https://www.biji.com/checkout?product_alias=6AydVpYeKl
- 创建笔记建议间隔 1 分钟以上，避免触发限流

---

## 指令路由表

> 匹配指令后，用 **read 工具**读取对应的 `references/xxx.md` 获取完整 API 文档。

| 指令 | 角色 | 说明 | 详细文档 |
|------|------|------|---------|
| `/note save` 或「记一下」| 📝 速记员 | 保存文本/链接/图片笔记（含异步轮询流程） | [references/save.md](references/save.md) |
| `/note search` 或「搜一下」| 🔍 搜索官 | 全局语义搜索 + 知识库语义搜索 | [references/search.md](references/search.md) |
| `/note list` 或「最近的笔记」| 📋 整理师 | 浏览列表、查看详情、更新、删除 | [references/list.md](references/list.md) |
| `/note kb` 或「知识库」| 📚 图书管理员 | 知识库 CRUD + 博主订阅 + 直播订阅 | [references/knowledge.md](references/knowledge.md) |
| `/note tag` 或「加标签」| 🏷️ 标签员 | 添加/删除标签 | [references/tags.md](references/tags.md) |
| `/note config` 或「配置笔记」| ⚙️ 配置 | 配置 API Key 和 Client ID | [references/oauth.md](references/oauth.md) |

---

## 自然语言路由

```
包含 URL                    → /note save（link 模式）
包含图片                    → /note save（image 模式）
「记/存/保存/收藏」          → /note save（text 模式）
「搜/找找/有没有 XX」        → /note search
「最近/列表/看看/查笔记」    → /note list
「改/更新/编辑笔记」         → /note list（更新笔记）
「知识库」相关              → /note kb
「标签」相关                → /note tag
「配置/授权/连接笔记」       → /note config
```

**决策原则**：优先匹配最具体的意图。有 URL 就是 `/save link`，有图片就是 `/save image`，不确定时询问用户。

---

## 通用错误处理

```json
{
  "success": false,
  "error": {
    "code": 10001,
    "message": "unauthorized",
    "reason": "not_member"
  },
  "request_id": "xxx"
}
```

| 错误码 | 说明 | 处理方式 |
|--------|------|---------|
| 10000 | 参数错误 | 检查请求参数 |
| 10001 | 鉴权失败 | 检查 API Key 和 Client ID，或重新授权 |
| 10100 | 数据不存在 | 确认笔记/知识库 ID 正确 |
| 10201 | 非会员 | 引导开通：https://www.biji.com/checkout?product_alias=6AydVpYeKl |
| 10202 | QPS 限流 | 降低频率，查看 rate_limit 字段 |
| 30000 | 服务调用失败 | 稍后重试 |
| 50000 | 系统错误 | 稍后重试 |

详细错误码和限流结构见 [references/api-details.md](references/api-details.md)。
