---
name: getnotes
description: Get笔记 OpenAPI - 查询、创建、编辑、删除笔记，管理标签。支持纯文本、链接、图片笔记。
---

# Get笔记 OpenAPI

## 快速开始

**Base URL**: `https://openapi.biji.com`

**认证**: 所有请求需要 Header `Authorization: gk_live_<API_KEY>`

## API 列表

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 笔记列表 | GET | `/open/api/v1/resource/note/list` | 分页获取笔记 |
| 笔记详情 | GET | `/open/api/v1/resource/note/detail` | 获取单条笔记完整信息 |
| 创建/编辑笔记 | POST | `/open/api/v1/resource/note/save` | 新建或更新笔记 |
| 删除笔记 | POST | `/open/api/v1/resource/note/delete` | 删除笔记 |
| 添加标签 | POST | `/open/api/v1/resource/note/tags/add` | 给笔记添加标签 |
| 删除标签 | POST | `/open/api/v1/resource/note/tags/delete` | 删除笔记的标签 |
| 图片上传凭证 | GET | `/open/api/v1/resource/image/upload_token` | 获取图片上传 token |

---

## 1. 笔记列表

```http
GET /open/api/v1/resource/note/list?limit=20&since_id=0
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 每页数量，默认 20，最大 100 |
| since_id | int64 | 否 | 游标，返回 ID 小于此值的笔记 |

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

## 2. 笔记详情

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

## 3. 创建/编辑笔记

```http
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

**请求体**:
```json
{
  "id": 0,                    // 编辑时必填，创建时不填或填 0
  "title": "笔记标题",
  "content": "Markdown 内容",
  "note_type": "plain_text",  // plain_text | img_text | link
  "tags": ["工作", "重要"],
  "parent_id": 0,             // 创建子笔记时填父笔记 ID
  "link_url": "https://...",  // link 类型必填
  "image_urls": ["https://..."] // img_text 类型必填
}
```

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

---

## 4. 删除笔记

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

---

## 5. 添加标签

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

## 6. 删除标签

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

## 7. 图片上传凭证

```http
GET /open/api/v1/resource/image/upload_token?count=1
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 否 | 需要的 token 数量，默认 1 |

用于创建图片笔记前获取上传凭证。

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
