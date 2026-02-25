---
name: getnotes
description: Create and manage notes via Get笔记 API. Use when user wants to save notes, create image notes from photos, save web links as notes, manage note tags, or query existing notes. Supports plain text, image, link, meeting, and audio note types.
---

# Get笔记 API

操作 Get笔记的 API 接口，支持查询笔记、创建笔记、图片笔记、链接笔记、管理标签。

## 认证

所有请求需要 Header：
```
Authorization: gk_live_<API_KEY>
```

API 基础地址：`https://openapi.biji.com`

## API 接口

### 1. 获取笔记列表

```
GET /open/api/v1/resource/note/list?limit=10&since_id=0
```

参数：
- `limit`: 每页数量，默认 10，最大 100
- `since_id`: 游标，返回 ID 大于此值的笔记（用于分页）

返回：
```json
{
  "success": true,
  "data": {
    "notes": [{
      "id": 1901297236063695760,
      "title": "笔记标题",
      "content": "完整 Markdown 内容，包含智能总结、章节概要、金句精选、待办事项等",
      "summary": "HTML 格式摘要",
      "note_type": "meeting|recorder_audio|plain_text|img_text|link",
      "source": "app|yoda|gethub",
      "tags": [{"id": "123456", "name": "工作"}],
      "children_count": 0,
      "topics": [],
      "is_child_note": false,
      "created_at": "2026-02-10 18:36:12",
      "updated_at": "2026-02-10 18:36:12"
    }],
    "has_more": true,
    "next_cursor": 1899321837796601704,
    "total": 10
  },
  "error": null,
  "meta": {"timestamp": 1772007500},
  "request_id": "xxx"
}
```

**笔记类型 (note_type)**：
- `meeting`: 会议笔记（录音卡录制）
- `recorder_audio`: 录音笔记（APP 录制）
- `plain_text`: 纯文本笔记
- `img_text`: 图片笔记
- `link`: 链接笔记

### 2. 获取笔记详情

```
GET /open/api/v1/resource/note/detail?id=123456789
```

返回比列表更详细的信息：
```json
{
  "success": true,
  "data": {
    "note": {
      "id": 1901297236063695760,
      "title": "笔记标题",
      "content": "完整 Markdown 内容",
      "summary": "HTML 格式摘要",
      "ref_content": "引用内容",
      "note_type": "meeting",
      "source": "app",
      "entry_type": "ai",
      "tags": [{"id": "123456", "name": "工作"}],
      "children_count": 0,
      "topics": null,
      "is_child_note": false,
      "attachments": [{
        "type": "audio",
        "url": "https://mediacdn.example.com/audio.mp3",
        "title": "",
        "duration": 1260720
      }],
      "audio": {
        "transcript": "🟢 说话人1 [00:00:00]\n内容...\n\n🟣 说话人2 [00:00:24]\n内容..."
      },
      "version": 0,
      "created_at": "2026-02-10 18:36:12",
      "updated_at": "2026-02-10 18:58:49"
    }
  }
}
```

**额外字段**：
- `attachments`: 附件列表（图片、音频、视频等）
  - `type`: audio/image/video/file
  - `url`: 资源地址
  - `duration`: 音频/视频时长（毫秒）
- `audio.transcript`: 原始转写文本（带时间戳和说话人标记）
- `ref_content`: 引用内容
- `version`: 版本号

### 3. 获取图片上传配置

```
GET /open/api/v1/resource/image/config
```

返回支持的图片格式和限制：
```json
{
  "success": true,
  "data": {
    "support_extensions": ["jpg", "png", "gif", "webp"],
    "max_size_bytes": 10485760,
    "max_count": 10
  }
}
```

### 4. 获取图片上传 Token

```
GET /open/api/v1/resource/image/upload_token?mime_type=jpg&count=1
```

返回预签名 URL：
```json
{
  "success": true,
  "data": {
    "tokens": [{
      "sign_url": "https://oss.aliyuncs.com/xxx?signature=xxx",
      "get_url": "https://cdn.example.com/xxx.jpg",
      "object_key": "xxx/xxx.jpg",
      "mime_type": "image/jpeg"
    }]
  }
}
```

### 5. 上传图片到 OSS

用 `sign_url` 直传图片：

```bash
curl -X PUT "${sign_url}" \
  -H "Content-Type: image/jpeg" \
  --data-binary @image.jpg
```

上传成功后，用 `get_url` 作为图片地址。

### 6. 创建笔记

```
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

**纯文本笔记：**
```json
{
  "title": "笔记标题",
  "content": "笔记内容"
}
```

**图片笔记：**
```json
{
  "title": "图片笔记",
  "content": "图片说明",
  "note_type": "img_text",
  "image_urls": ["https://cdn.example.com/xxx.jpg"]
}
```

**链接笔记：**
```json
{
  "title": "链接标题",
  "content": "链接说明",
  "note_type": "link",
  "link_url": "https://example.com/article"
}
```

返回：
```json
{
  "success": true,
  "data": {
    "id": 123456789,
    "title": "笔记标题",
    "created_at": "2026-02-24 10:00:00",
    "updated_at": "2026-02-24 10:00:00",
    "message": "链接笔记创建成功，AI 正在后台处理..."
  }
}
```

> ⚠️ **链接笔记说明**：链接笔记创建后，AI 会在后台异步处理网页内容。如需获取 AI 处理结果（摘要、正文提取等），请在约 **3 分钟后**通过笔记详情接口获取完整内容。

### 7. 添加笔记标签

```
POST /open/api/v1/resource/note/tags/add
Content-Type: application/json
```

```json
{
  "note_id": 123456789,
  "tags": ["工作", "重要"]
}
```

返回添加后的完整标签列表（包含 id 和 name）。

### 8. 删除笔记标签

```
POST /open/api/v1/resource/note/tags/delete
Content-Type: application/json
```

```json
{
  "note_id": 123456789,
  "tag_id": 987654321
}
```

## 图片笔记完整流程

创建图片笔记需要三步：

1. **获取上传 Token**
   ```
   GET /open/api/v1/resource/image/upload_token?mime_type=jpg&count=1
   ```

2. **上传图片到 OSS**
   ```bash
   curl -X PUT "${sign_url}" \
     -H "Content-Type: image/jpeg" \
     --data-binary @photo.jpg
   ```

3. **创建图片笔记**
   ```json
   POST /open/api/v1/resource/note/save
   {
     "title": "我的照片",
     "content": "照片说明",
     "note_type": "img_text",
     "image_urls": ["${get_url}"]
   }
   ```

## 笔记内容结构

录音/会议笔记的 content 字段通常包含以下 Markdown 结构：

```markdown
### 📑 智能总结

#### 录音信息
- **录音时间**：2026-02-10 18:36:12 ~ 2026-02-10 18:57:12
- **时长**：约 0小时21分钟
- **参与人数**：约 6人
- **内容类型**：工作会议

#### 录音总结
会议主题和核心内容...

**主题一**
* **要点1**：详细内容...
* **要点2**：详细内容...

### 📅 章节概要
[00:00:00](https://getnotes.seek:0) **章节标题**
章节内容摘要...

### ✨ 金句精选
- "金句内容" (分类标签)

### 📋 待办事项
- 负责人：具体任务
```

## 错误处理

所有接口统一返回格式：
```json
{
  "success": true,
  "data": {...},
  "error": null,
  "meta": {"timestamp": 1772007500},
  "request_id": "xxx"
}
```

错误时：
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

## 常见用法

**查询最近笔记：**
```bash
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/note/list?limit=10' \
  -H 'Authorization: gk_live_xxx'
```

**获取笔记详情（含原始转写）：**
```bash
curl -X GET 'https://openapi.biji.com/open/api/v1/resource/note/detail?id=xxx' \
  -H 'Authorization: gk_live_xxx'
```

**创建纯文本笔记：**
```bash
curl -X POST 'https://openapi.biji.com/open/api/v1/resource/note/save' \
  -H 'Authorization: gk_live_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"title":"标题","content":"内容"}'
```
