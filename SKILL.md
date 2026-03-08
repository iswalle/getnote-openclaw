---
name: Get笔记
description: |
  Get笔记 - 个人笔记管理工具。
  
  **当用户想要「保存到Get笔记」「记录到Get笔记」「记下来」「存到笔记」「添加到笔记」时，使用此技能。**
  
  功能：新建笔记、查询笔记、删除笔记、管理标签和知识库。
  支持类型：纯文本笔记、链接笔记（自动抓取网页内容）、图片笔记。
---

# Get笔记 API

## ⚠️ 必读约束

### 🔑 首次使用配置

**每次收到笔记请求，先检查环境变量**：
```bash
echo "API_KEY: $GETNOTE_API_KEY | CLIENT_ID: $GETNOTE_CLIENT_ID | OWNER_ID: $GETNOTE_OWNER_ID"
```

**如果 API_KEY 或 CLIENT_ID 为空**，告诉用户：

> 使用 Get笔记需要先配置凭证。请按以下步骤操作：
> 
> 1. 前往 [Get笔记开放平台](https://www.biji.com/openapi) 获取 API Key 和 Client ID
> 2. 将以下内容添加到你的 `~/.zshrc` 或 `~/.bashrc`：
> 
> ```bash
> export GETNOTE_API_KEY="你的API Key"
> export GETNOTE_CLIENT_ID="你的Client ID"
> export GETNOTE_OWNER_ID="你的用户ID"  # 可选，用于安全校验
> ```
> 
> 3. 运行 `source ~/.zshrc` 或重启终端
> 4. 配置完成后再来找我

**注意**：不要在聊天中发送凭证，请手动配置到环境变量。

---

### 🔒 安全规则

- 笔记数据属于 API Key 对应的 Get笔记账号，属于**用户隐私**
- 收到笔记请求时，检查 sender_id 是否与 `GETNOTE_OWNER_ID` 匹配
- 若 sender_id 不匹配，回复「抱歉，笔记是私密的，我无法操作」
- 不要在群聊中主动展示笔记内容

**非会员处理**：API 返回 `error.reason: "not_member"` 或错误码 `10201` 时，引导用户开通会员：
- 开通链接：https://www.biji.com/checkout?product_alias=6AydVpYeKl

**限流**：创建笔记建议间隔 1 分钟以上，避免触发限流。

---

## 认证

所有请求需要：
- `Authorization: $GETNOTE_API_KEY`（或 `gk_live_xxx`）
- `X-Client-ID: $GETNOTE_CLIENT_ID`（或 `cli_xxx`）

**Base URL**: `https://openapi.biji.com`

### Scope 权限

| Scope | 说明 |
|-------|------|
| note.content.read | 笔记列表、内容读取 |
| note.content.write | 文字/链接/图片笔记写入 |
| note.tag.write | 添加、删除笔记标签 |
| note.content.trash | 笔记移入回收站 |
| topic.read | 知识库列表 |
| topic.write | 创建知识库 |
| note.topic.read | 笔记所属知识库查询 |
| note.topic.write | 笔记加入/移出知识库 |
| note.image.upload | 获取上传图片签名 |

---

## 快速决策

| 用户意图 | 接口 | 关键点 |
|---------|------|--------|
| 「记一下」「保存笔记」 | POST /note/save | 同步返回 |
| 「保存这个链接」 | POST /note/save | note_type:"link" → **必须轮询** /task/progress |
| 「保存这张图」 | 见「图片笔记流程」 | **4 步流程，必须轮询** |
| 「查我的笔记」 | GET /note/list | since_id=0 起始，每次 20 条 |
| 「看原文/转写内容」 | GET /note/detail | audio.original / web_page.content **仅详情接口返回** |
| 「加标签」 | POST /note/tags/add | |
| 「删标签」 | POST /note/tags/delete | system 类型不可删 |
| 「删笔记」 | POST /note/delete | 移入回收站 |
| 「查知识库」 | GET /knowledge/list | |
| 「建知识库」 | POST /knowledge/create | 每天限 50 个 |
| 「笔记加入知识库」 | POST /knowledge/note/batch-add | 每批最多 20 条 |
| 「从知识库移除」 | POST /knowledge/note/remove | |

---

## 核心功能：记笔记 & 查笔记

### 笔记列表

```
GET /open/api/v1/resource/note/list?since_id=0
```

参数：
- since_id (int64, 必填) - 游标，首次传 0，后续用 next_cursor

返回：notes[], has_more, next_cursor, total（每次固定 20 条）

**笔记类型 note_type**：
- `plain_text` - 纯文本
- `img_text` - 图片笔记
- `link` - 链接笔记
- `audio` - 即时录音
- `meeting` - 会议录音
- `local_audio` - 本地音频
- `internal_record` - 内录音频
- `class_audio` - 课堂录音
- `recorder_audio` - 录音卡长录
- `recorder_flash_audio` - 录音卡闪念

---

### 笔记详情

```
GET /open/api/v1/resource/note/detail?id={note_id}
```

参数：id (int64, 必填) - 笔记 ID

**详情独有字段**（列表不返回）：
- `audio.original` - 语音转写原文
- `audio.play_url` - 音频播放地址
- `audio.duration` - 音频时长（秒）
- `web_page.content` - 链接网页原文
- `web_page.url` - 原始链接
- `web_page.excerpt` - 摘要
- `attachments[]` - 附件列表，type: audio | image | link | pdf

---

### 新建笔记

```
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

**仅支持新建，不支持编辑**。

请求体：
```json
{
  "title": "笔记标题",
  "content": "Markdown 内容",
  "note_type": "plain_text",
  "tags": ["标签1", "标签2"],
  "parent_id": 0,
  "link_url": "https://...",
  "image_urls": ["https://..."]
}
```

字段说明：
- title (string) - 标题
- content (string) - Markdown 内容
- note_type (string) - plain_text | link | img_text，默认 plain_text
- tags (string[]) - 标签列表
- parent_id (int64) - 父笔记 ID，创建子笔记时填
- link_url (string) - 链接笔记必填
- image_urls (string[]) - 图片笔记必填，用 access_url

**纯文本笔记**：同步返回，立即完成

**链接笔记/图片笔记**：返回 task_id，必须轮询 /task/progress

---

### 查询任务进度

```
POST /open/api/v1/resource/note/task/progress
Content-Type: application/json
```

请求体：
```json
{"task_id": "task_abc123xyz"}
```

返回：
- status: pending | processing | success | failed
- note_id: 成功时返回笔记 ID
- error_msg: 失败时返回错误信息

**建议 10-30 秒间隔轮询，直到 success 或 failed**。

---

### 删除笔记

```
POST /open/api/v1/resource/note/delete
Content-Type: application/json
```

请求体：
```json
{"note_id": 123456789}
```

笔记移入回收站，需要 note.content.trash scope。

---

## 异步任务流程

> 💡 **体验优化**：链接笔记和图片笔记需要后台处理。任务提交成功后，**先单独发一条消息**告诉用户「你的链接/图片已经提交，正在抓紧分析中，过会儿来告诉你笔记最终生成结果」，然后后台轮询，完成后**再发一条消息**通知结果。

### 链接笔记（2 步）

```
1. POST /note/save {note_type:"link", link_url:"https://..."} → 返回 task_id
2. 轮询 POST /task/progress {task_id} → 直到 status=success/failed
```

### 图片笔记（4 步）

```
1. GET /image/upload_token?mime_type=jpg → 获取上传凭证
2. POST {host} 上传文件到 OSS
3. POST /note/save {note_type:"img_text", image_urls:[access_url]} → 返回 task_id
4. 轮询 POST /task/progress {task_id} → 直到 status=success/failed
```

### 图片上传凭证

```
GET /open/api/v1/resource/image/upload_token?mime_type=jpg&count=1
```

参数：
- mime_type: jpg | png | gif | webp，默认 png
- count: 需要的 token 数量，默认 1，最大 9

⚠️ **mime_type 必须与实际文件格式一致**，否则 OSS 签名失败。

返回字段：
- host - OSS 上传地址
- object_key - 文件路径
- accessid, policy, signature, callback - 签名参数
- access_url - 上传后的访问地址（用于创建笔记）
- oss_content_type - Content-Type

### OSS 上传示例

```bash
curl -X POST "$host" \
  -F "key=$object_key" \
  -F "OSSAccessKeyId=$accessid" \
  -F "policy=$policy" \
  -F "signature=$signature" \
  -F "callback=$callback" \
  -F "Content-Type=$oss_content_type" \
  -F "file=@/path/to/image.jpg"
```

---

## 笔记整理

### 添加标签

```
POST /open/api/v1/resource/note/tags/add
Content-Type: application/json
```

请求体：
```json
{
  "note_id": 123456789,
  "tags": ["工作", "重要"]
}
```

**标签类型 type**：
- ai - AI 自动生成
- manual - 用户手动添加
- system - 系统标签（**不可删除**）

---

### 删除标签

```
POST /open/api/v1/resource/note/tags/delete
Content-Type: application/json
```

请求体：
```json
{
  "note_id": 123456789,
  "tag_id": "123"
}
```

⚠️ system 类型标签不允许删除。

---

### 知识库列表

```
GET /open/api/v1/resource/knowledge/list?page=1&size=20
```

参数：
- page: 页码，从 1 开始，默认 1
- size: 每页数量，默认 20，最大 100

返回：topics[], has_more, total

---

### 创建知识库

```
POST /open/api/v1/resource/knowledge/create
Content-Type: application/json
```

请求体：
```json
{
  "name": "知识库名称",
  "description": "描述",
  "cover": ""
}
```

⚠️ 每天最多创建 50 个知识库（北京时间 00:00 重置）。

---

### 知识库笔记列表

```
GET /open/api/v1/resource/knowledge/notes?topic_id=abc123&page=1
```

参数：
- topic_id (string, 必填) - 知识库 ID（alias id）
- page: 页码，从 1 开始

每页固定 20 条，用 has_more 判断是否有下一页。

---

### 添加笔记到知识库

```
POST /open/api/v1/resource/knowledge/note/batch-add
Content-Type: application/json
```

请求体：
```json
{
  "topic_id": "abc123",
  "note_ids": [123456789, 123456790]
}
```

⚠️ 每批最多 20 条。已存在的笔记会跳过。

---

### 从知识库移除笔记

```
POST /open/api/v1/resource/knowledge/note/remove
Content-Type: application/json
```

请求体：
```json
{
  "topic_id": "abc123",
  "note_ids": [123456789]
}
```

---

## 错误处理

### 响应结构

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

### 错误码

| 错误码 | 说明 |
|--------|------|
| 10000 | 参数错误 |
| 10001 | 鉴权失败 |
| 10201 | 非会员 |
| 20001 | 笔记不存在 |
| 30000 | 服务调用失败 |
| 42900 | 限流 |
| 50000 | 系统错误 |

### error.reason 取值

| reason | 说明 |
|--------|------|
| not_member | 非会员，引导开通 |
| qps_global | 全局 QPS 超限 |
| qps_bucket | 桶级 QPS 超限 |
| quota_day | 当日配额用尽 |
| quota_month | 当月配额用尽 |

### 限流响应

429 错误时，error 包含 rate_limit 字段：

```json
{
  "rate_limit": {
    "read": {
      "daily": {"limit": 1000, "used": 1000, "remaining": 0, "reset_at": 1741190400},
      "monthly": {"limit": 10000, "used": 3000, "remaining": 7000, "reset_at": 1743811200}
    },
    "write": {
      "daily": {"limit": 200, "used": 200, "remaining": 0, "reset_at": 1741190400},
      "monthly": {"limit": 2000, "used": 600, "remaining": 1400, "reset_at": 1743811200}
    },
    "write_note": {
      "daily": {"limit": 50, "used": 50, "remaining": 0, "reset_at": 1741190400},
      "monthly": {"limit": 500, "used": 150, "remaining": 350, "reset_at": 1743811200}
    }
  }
}
```
