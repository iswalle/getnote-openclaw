---
name: getnotes
description: Get笔记 OpenAPI - 查询、创建、编辑笔记，管理标签和知识库。支持纯文本、链接、图片笔记。
---

# Get笔记 OpenAPI

## 快速开始

**Base URL**: `https://openapi.biji.com`

**认证**: 所有请求需要 Header `Authorization: gk_live_<API_KEY>`

## API 列表

### 笔记接口
| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 笔记列表 | GET | `/open/api/v1/resource/note/list` | 分页获取笔记 |
| 笔记详情 | GET | `/open/api/v1/resource/note/detail` | 获取单条笔记完整信息 |
| 创建/编辑笔记 | POST | `/open/api/v1/resource/note/save` | 新建或更新笔记 |
| 添加标签 | POST | `/open/api/v1/resource/note/tags/add` | 给笔记添加标签 |
| 删除标签 | POST | `/open/api/v1/resource/note/tags/delete` | 删除笔记的标签 |

### 知识库接口
| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 知识库列表 | GET | `/open/api/v1/resource/knowledge/list` | 获取用户的知识库列表 |
| 创建知识库 | POST | `/open/api/v1/resource/knowledge/create` | 创建新知识库 |
| 知识库笔记列表 | GET | `/open/api/v1/resource/knowledge/notes` | 获取知识库内的笔记 |
| 添加笔记到知识库 | POST | `/open/api/v1/resource/knowledge/note/batch-add` | 批量添加笔记到知识库 |
| 从知识库移除笔记 | POST | `/open/api/v1/resource/knowledge/note/remove` | 从知识库移除笔记 |

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
        "topics": [{"id": 1, "name": "工作笔记"}],
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
- `plain_text` - 纯文本笔记
- `img_text` - 图片笔记
- `link` - 链接笔记
- `meeting` - 会议笔记（录音卡）
- `recorder_audio` - 录音笔记（App 录制）

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

### 3. 创建/编辑笔记

```http
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

**请求体**:
```json
{
  "id": 0,                    // 编辑时必填，创建时不填
  "title": "笔记标题",
  "content": "Markdown 内容",
  "note_type": "plain_text",  // plain_text（默认，文本/图文笔记）| link（链接笔记）
  "tags": ["工作", "重要"],
  "parent_id": 0,             // 创建子笔记时填父笔记 ID
  "link_url": "https://...",  // 链接笔记专用，链接地址
  "image_urls": ["https://..."] // 图片笔记专用，图片地址列表（从 upload_token 上传后得到）
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int64 | 否 | 笔记 ID，编辑时必填，创建时不填 |
| title | string | 否 | 笔记标题 |
| content | string | 否 | 正文内容 (Markdown)，链接笔记可为空 |
| note_type | string | 否 | 笔记类型：`plain_text`（默认，文本/图文笔记）、`link`（链接笔记） |
| tags | string[] | 否 | 标签列表，最多 5 个，每个标签不超过 20 字符。⚠️ 链接笔记不支持同时创建标签 |
| parent_id | int64 | 否 | 父笔记 ID，创建子笔记时使用 |
| image_urls | string[] | 否 | 图片笔记专用，图片地址列表（从 upload_token 上传后得到） |
| link_url | string | 否 | 链接笔记专用，链接地址 |

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1901297236063695760,
    "title": "笔记标题",
    "created_at": "2026-02-25 10:00:00",
    "updated_at": "2026-02-25 10:00:00",
    "message": "链接笔记创建成功，AI 正在后台处理..."
  }
}
```

> ⚠️ 链接笔记创建后 AI 异步处理，约 3 分钟后可获取完整内容。
> ⚠️ 链接笔记不支持同时创建标签，需要创建后再调用添加标签接口。

---

### 4. 添加标签

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

### 5. 删除标签

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

## 知识库接口

### 6. 知识库列表

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

### 7. 创建知识库

```http
POST /open/api/v1/resource/knowledge/create
Content-Type: application/json
```

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

### 8. 知识库笔记列表

```http
GET /open/api/v1/resource/knowledge/notes?topic_id=abc123&page=1&size=20
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic_id | string | ✅ | 知识库 ID |
| page | int | 否 | 页码，从 1 开始，默认 1 |
| size | int | 否 | 每页数量，默认 20，最大 100 |

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
    "has_more": false,
    "total": 10
  }
}
```

---

### 9. 添加笔记到知识库

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

### 10. 从知识库移除笔记

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

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 50000,
    "message": "错误信息"
  },
  "request_id": "xxx"
}
```

**常见错误码**:
| 错误码 | 说明 |
|--------|------|
| 10000 | 参数错误 |
| 20001 | 笔记不存在 |
| 30000 | 服务调用失败 |
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
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id=abc123' \
  -H 'Authorization: gk_live_xxx'
```
