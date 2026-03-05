---
name: getnotes
description: Get笔记 OpenAPI - 查询、新建、删除笔记，管理标签和知识库。支持纯文本、链接、图片笔记。
---

# Get笔记 OpenAPI

## 快速开始

**Base URL**: `https://openapi.biji.com`

**认证**: 所有请求需要 Header `Authorization: gk_live_<API_KEY>`

## Scope 权限说明

每个 API Key 关联一组 scope，调用接口时需要对应的 scope 权限：

| Scope | 说明 |
|-------|------|
| `note.content.read` | 笔记列表、内容读取 |
| `note.content.write` | 文字/链接/图片/音视频笔记写入 |
| `note.tag.write` | 添加、删除笔记标签 |
| `note.content.trash` | 笔记移入回收站 |
| `topic.read` | 知识库列表 |
| `topic.write` | 创建、删除知识库 |
| `note.topic.read` | 笔记所属知识库查询 |
| `note.topic.write` | 笔记加入/移出知识库 |
| `note.image.upload` | 获取上传图片签名 |
| `note.recall.read` | 笔记内容召回 |
| `note.topic.recall.read` | 知识库笔记召回 |

## API 列表

### 笔记接口
| 接口 | 方法 | 路径 | 所需 Scope |
|------|------|------|-----------|
| 笔记列表 | GET | `/open/api/v1/resource/note/list` | `note.content.read` |
| 笔记详情 | GET | `/open/api/v1/resource/note/detail` | `note.content.read` |
| 新建笔记（仅支持新建） | POST | `/open/api/v1/resource/note/save` | `note.content.write` |
| 查询笔记任务进度 | POST | `/api/v1/resource/note/task/progress` | `note.content.read` |
| 删除笔记 | POST | `/open/api/v1/resource/note/delete` | `note.content.trash` |
| 添加标签 | POST | `/open/api/v1/resource/note/tags/add` | `note.tag.write` |
| 删除标签 | POST | `/open/api/v1/resource/note/tags/delete` | `note.tag.write` |
| 图片上传凭证 | GET | `/open/api/v1/resource/image/upload_token` | `note.image.upload` |

### 知识库接口
| 接口 | 方法 | 路径 | 所需 Scope |
|------|------|------|-----------|
| 知识库列表 | GET | `/open/api/v1/resource/knowledge/list` | `topic.read` |
| 创建知识库 | POST | `/open/api/v1/resource/knowledge/create` | `topic.write` |
| 知识库笔记列表 | GET | `/open/api/v1/resource/knowledge/notes` | `note.topic.read` |
| 添加笔记到知识库 | POST | `/open/api/v1/resource/knowledge/note/batch-add` | `note.topic.write` |
| 从知识库移除笔记 | POST | `/open/api/v1/resource/knowledge/note/remove` | `note.topic.write` |

---

## 笔记接口

### 1. 笔记列表

```http
GET /open/api/v1/resource/note/list?limit=20&since_id=0
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 每页数量，默认 20，最大 100 |
| since_id | int64 | ✅ | 游标，返回 ID 小于此值的笔记。首次请求传 0 |

> ⚠️ `since_id` 必传，不传会导致分页异常。首次请求用 `since_id=0`，后续用上一页最后一条笔记的 ID。

**响应**:
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "id": 1901297236063695760,
        "title": "会议记录",
        "content": "Markdown 正文...",
        "ref_content": "引用/转写内容",
        "note_type": "meeting",
        "source": "app",
        "tags": [
          {"id": "123", "name": "工作", "type": "manual"}
        ],
        "parent_id": 0,
        "children_count": 2,
        "topics": [{"id": "abc123", "name": "工作笔记"}],
        "is_child_note": false,
        "created_at": "2026-02-25 10:00:00",
        "updated_at": "2026-02-25 10:30:00"
      }
    ],
    "has_more": true,
    "next_cursor": 1901297236063695759,
    "total": 20
  }
}
```

**笔记类型 (note_type)**:
- `plain_text` - 纯文本笔记（不支持图文）
- `img_text` - 图片笔记
- `link` - 链接笔记
- `meeting` - 会议笔记（录音卡）
- `recorder_audio` - 录音笔记（App 录制）

> 💡 **topics.id 说明**：笔记所属知识库列表中的 `id` 字段为 alias id（字符串类型），而非内部数字 ID。这样设计是为了方便开发者直接使用，可直接用于知识库相关接口的 `topic_id` 参数。

---

### 2. 笔记详情

```http
GET /open/api/v1/resource/note/detail?id=1901297236063695760
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int64 | ✅ | 笔记 ID |

**响应** (比列表多以下字段):
```json
{
  "success": true,
  "data": {
    "note": {
      "id": 1901297236063695760,
      "title": "会议记录",
      "content": "Markdown 正文...",
      "ref_content": "引用内容",
      "note_type": "meeting",
      "source": "app",
      "entry_type": "ai",
      "tags": [{"id": "123", "name": "工作", "type": "manual"}],
      "attachments": [
        {"type": "audio", "url": "https://...", "duration": 1260000}
      ],
      "audio": {
        "play_url": "https://...",
        "duration": 1260,
        "transcript": "🟢 说话人1 [00:00:00]\n内容..."
      },
      "web_page": {
        "url": "https://原始链接",
        "domain": "example.com",
        "excerpt": "摘要",
        "content": "链接原文"
      },
      "share_id": "abc123",
      "version": 1,
      "created_at": "2026-02-25 10:00:00",
      "updated_at": "2026-02-25 10:30:00"
    }
  }
}
```

**附件类型 (attachments.type)**: `audio` | `image` | `link` | `pdf`

---

### 3. 新建笔记

> ⚠️ **仅支持新建笔记，不支持编辑**。请勿传入 `id` 字段。

```http
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

**请求体**:
```json
{
  "title": "笔记标题",
  "content": "Markdown 内容",
  "note_type": "plain_text",  // plain_text | img_text | link
  "tags": ["工作", "重要"],
  "parent_id": 0,             // 创建子笔记时填父笔记 ID（父笔记的 is_child_note 必须为 false）
  "link_url": "https://...",  // link 类型必填
  "image_urls": ["https://..."] // img_text 类型必填
}
```

**响应（纯文本笔记）**:
```json
{
  "success": true,
  "data": {
    "id": 1901297236063695760,
    "title": "笔记标题",
    "created_at": "2026-02-25 10:00:00",
    "updated_at": "2026-02-25 10:00:00"
  }
}
```

**响应（链接笔记 `note_type: "link"`）**:
```json
{
  "success": true,
  "data": {
    "id": 1901297236063695760,
    "title": "笔记标题",
    "created_at": "2026-02-25 10:00:00",
    "updated_at": "2026-02-25 10:00:00",
    "message": "链接笔记创建成功，AI 正在后台处理...",
    "tasks": [
      {
        "task_id": "task_abc123xyz",
        "url": "https://example.com/article"
      }
    ],
    "created_count": 1,
    "duplicate_count": 0,
    "invalid_count": 0
  }
}
```

> ⚠️ 链接笔记创建后 AI 异步处理，约 3 分钟后可获取完整内容。创建时会返回 `tasks` 数组，可用其中的 `task_id` 查询处理进度。

**支持的笔记类型**
- **写入（save_note）**：目前只支持纯文本笔记和链接笔记
- **其他类型**（图片笔记、语音笔记等）：只支持在 App 或 Web 端创建，OpenAPI 可以读取

---

### 4. 查询创建笔记任务进度

> 用于查询链接笔记（`note_type: "link"`）异步创建任务的处理状态。

```http
POST /api/v1/resource/note/task/progress
Content-Type: application/json
```

**所需 Scope**: `note.content.read`

**请求体**:
```json
{
  "task_id": "task_abc123xyz"
}
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | string | ✅ | 任务 ID（创建链接笔记时返回） |

**响应**:
```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123xyz",
    "task_type": "link",
    "status": "success",
    "note_id": 1901297236063695760,
    "error_msg": "",
    "create_time": "2026-02-25 10:00:00",
    "update_time": "2026-02-25 10:02:30"
  }
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务 ID |
| task_type | string | 任务类型，目前为 `link` |
| status | string | 任务状态：`pending`（等待）/ `processing`（处理中）/ `success`（成功）/ `failed`（失败） |
| note_id | int64 | 笔记 ID（status 为 success 时返回） |
| error_msg | string | 错误信息（status 为 failed 时返回） |
| create_time | string | 任务创建时间 |
| update_time | string | 任务最后更新时间 |

> 💡 建议以 10~30 秒的间隔轮询此接口，直到 status 变为 `success` 或 `failed`。

---

### 5. 删除笔记

```http
POST /open/api/v1/resource/note/delete
Content-Type: application/json
```

**请求体**:
```json
{
  "note_id": 1901297236063695760
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "note_id": 1901297236063695760
  }
}
```

> 💡 删除操作将笔记移入回收站，需要 `note.content.trash` scope。

---

### 6. 添加标签

```http
POST /open/api/v1/resource/note/tags/add
Content-Type: application/json
```

**请求体**:
```json
{
  "note_id": 1901297236063695760,
  "tags": ["工作", "重要"]
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "note_id": 1901297236063695760,
    "tags": [
      {"id": "123", "name": "工作", "type": "manual"},
      {"id": "124", "name": "重要", "type": "manual"}
    ]
  }
}
```

**标签类型 (type)**:
- `ai` - AI 自动生成
- `manual` - 用户手动添加
- `system` - 系统标签（⚠️ 不可删除）

---

### 7. 删除标签

```http
POST /open/api/v1/resource/note/tags/delete
Content-Type: application/json
```

**请求体**:
```json
{
  "note_id": 1901297236063695760,
  "tag_id": "123"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "note_id": 1901297236063695760,
    "tags": []
  }
}
```

> ⚠️ 系统标签（`type: "system"`）不允许删除，会返回错误。

---

### 8. 图片上传凭证

```http
GET /open/api/v1/resource/image/upload_token?count=1
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 否 | 需要的 token 数量，默认 1 |

用于创建图片笔记前获取上传凭证。

---

## 知识库接口

### 9. 知识库列表

```http
GET /open/api/v1/resource/knowledge/list?page=1&size=20
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，从 1 开始，默认 1 |
| size | int | 否 | 每页数量，默认 20，最大 100 |

**响应**:
```json
{
  "success": true,
  "data": {
    "topics": [
      {
        "id": "abc123",
        "name": "工作笔记",
        "description": "工作相关的笔记",
        "cover": "https://...",
        "scope": "DEFAULT",
        "created_at": 1740000000,
        "updated_at": 1740000000
      }
    ],
    "has_more": false,
    "total": 5
  }
}
```

---

### 10. 创建知识库

```http
POST /open/api/v1/resource/knowledge/create
Content-Type: application/json
```

> ⚠️ **创建限制**：每个账号每天最多创建 **50 个知识库**，按 Europe/Berlin 时区自然日 00:00 重置。

**请求体**:
```json
{
  "name": "工作笔记",
  "description": "工作相关的笔记",
  "cover": ""
}
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 知识库名称 |
| description | string | 否 | 知识库描述 |
| cover | string | 否 | 封面图片 URL |

**响应**:
```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "name": "工作笔记",
    "description": "工作相关的笔记",
    "cover": "",
    "scope": "DEFAULT"
  }
}
```

---

### 11. 知识库笔记列表

```http
GET /open/api/v1/resource/knowledge/notes?topic_id=abc123&page=1
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic_id | string | ✅ | 知识库 ID |
| page | int | 否 | 页码，从 1 开始，默认 1 |

> ⚠️ 每页固定返回 20 条笔记，不支持自定义 size。

**响应**:
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "note_id": 1901297236063695760,
        "title": "会议记录",
        "content": "笔记内容摘要...",
        "note_type": "meeting",
        "tags": ["工作", "重要"],
        "is_ai": true,
        "created_at": "2026-02-25 10:00:00",
        "edit_time": "2026-02-25 10:30:00"
      }
    ],
    "has_more": true,
    "total": 50
  }
}
```

**分页说明**:
- `has_more`: 是否有下一页，`true` 表示还有更多数据
- 翻页：当 `has_more` 为 `true` 时，将 `page` 加 1 继续请求
- `total`: 该知识库内的笔记总数

---

### 12. 添加笔记到知识库

```http
POST /open/api/v1/resource/knowledge/note/batch-add
Content-Type: application/json
```

**请求体**:
```json
{
  "topic_id": "abc123",
  "note_ids": [1901297236063695760, 1901297236063695761]
}
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic_id | string | ✅ | 知识库 ID |
| note_ids | int64[] | ✅ | 笔记 ID 列表，最多 20 个 |

**响应**:
```json
{
  "success": true,
  "data": {
    "added_count": 2,
    "failed_note_ids": []
  }
}
```

> ⚠️ 每批最多添加 20 条笔记。已存在于知识库的笔记会被跳过。

---

### 13. 从知识库移除笔记

```http
POST /open/api/v1/resource/knowledge/note/remove
Content-Type: application/json
```

**请求体**:
```json
{
  "topic_id": "abc123",
  "note_ids": [1901297236063695760]
}
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic_id | string | ✅ | 知识库 ID |
| note_ids | int64[] | ✅ | 笔记 ID 列表 |

**响应**:
```json
{
  "success": true,
  "data": {
    "removed_count": 1,
    "failed_note_ids": []
  }
}
```

---

## 错误响应

所有错误均返回统一的响应结构：

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 10001,
    "message": "unauthorized",
    "reason": "not_member"
  },
  "meta": {"timestamp": 1741161600},
  "request_id": "xxx"
}
```

**限流错误（429）时，`error` 还包含 `rate_limit` 字段**：

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 42900,
    "message": "rate limit exceeded",
    "reason": "quota_day",
    "rate_limit": {
      "read": {
        "daily":   {"limit": 1000, "used": 1000, "remaining": 0, "reset_at": 1741190400},
        "monthly": {"limit": 10000, "used": 3000, "remaining": 7000, "reset_at": 1743811200}
      },
      "write": {
        "daily":   {"limit": 200, "used": 200, "remaining": 0, "reset_at": 1741190400},
        "monthly": {"limit": 2000, "used": 600, "remaining": 1400, "reset_at": 1743811200}
      },
      "write_note": {
        "daily":   {"limit": 50, "used": 50, "remaining": 0, "reset_at": 1741190400},
        "monthly": {"limit": 500, "used": 150, "remaining": 350, "reset_at": 1743811200}
      }
    }
  },
  "meta": {"timestamp": 1741161600},
  "request_id": "xxx"
}
```

**`error.reason` 取值**：
| reason | 说明 |
|--------|------|
| `not_member` | 非会员，无调用权限 |
| `qps_global` | 全局 QPS 超限 |
| `qps_bucket` | 桶级 QPS 超限 |
| `quota_day` | 当日配额已用尽 |
| `quota_month` | 当月配额已用尽 |

**常见错误码**:
| 错误码 | 说明 |
|--------|------|
| 10000 | 参数错误 |
| 10001 | 鉴权失败（未授权） |
| 20001 | 笔记不存在 |
| 30000 | 服务调用失败 |
| 42900 | 限流（配额超限） |
| 50000 | 系统错误 |

---

## 常见用法示例

### 查询最近 10 条笔记
```bash
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/note/list?limit=10' \
  -H 'Authorization: gk_live_xxx'
```

### 创建纯文本笔记
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/note/save' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"title":"标题","content":"内容"}'
```

### 创建链接笔记
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/note/save' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"title":"文章标题","note_type":"link","link_url":"https://example.com/article"}'
```

### 查询链接笔记任务进度
```bash
curl -X POST 'https://openapi.biji.com/api/v1/resource/note/task/progress' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"task_abc123xyz"}'
```

### 给笔记添加标签
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/note/tags/add' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"note_id":123456789,"tags":["工作","重要"]}'
```

### 删除笔记
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/note/delete' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"note_id":123456789}'
```

### 获取知识库列表
```bash
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/knowledge/list' \
  -H 'Authorization: gk_live_xxx'
```

### 创建知识库
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/knowledge/create' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"name":"我的知识库","description":"存放重要笔记"}'
```

### 添加笔记到知识库
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"topic_id":"abc123","note_ids":[1901297236063695760]}'
```

### 获取知识库内的笔记
```bash
# 第一页
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id=abc123&page=1' \
  -H 'Authorization: gk_live_xxx'

# 如果响应 has_more=true，请求下一页
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id=abc123&page=2' \
  -H 'Authorization: gk_live_xxx'
```
