# 知识库管理

## 概述

知识库的 CRUD 操作，以及知识库内笔记管理、博主订阅内容、直播订阅内容的查询。

---

## 我的知识库列表

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/list?page=1
```

参数：
- `page`: 页码，从 1 开始，默认 1（固定每页 20 条）

返回：`topics[]`、`has_more`、`total`

每个 topic 包含：
- `topic_id`：知识库 ID（字符串，后续所有操作接口的 `topic_id` 参数均传此值）
- `name`、`description`、`cover`
- `created_at` / `updated_at`：时间字符串（YYYY-MM-DD HH:MM:SS）
- `stats`：统计数据
  - `note_count`：笔记数
  - `file_count`：文件数
  - `blogger_count`：订阅博主数
  - `live_count`：已完成直播数

---

## 订阅知识库列表

获取当前用户订阅（但非自己创建）的知识库列表。

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/subscribe/list?page=1
```

参数：
- `page`: 页码，从 1 开始，默认 1（固定每页 20 条）

返回字段与"我的知识库列表"相同：`topics[]`、`has_more`、`total`

> 与 `/knowledge/list` 的区别：该接口只返回他人分享/公开的知识库，不包含自己创建的。

**订阅知识库的限制**：
- ⚠️ **无法添加笔记**：订阅的知识库只读，不能向其中添加笔记
- ⚠️ **查看源内容受限**：若知识库管理员关闭了「查看源文件」，则无法获取笔记原文，只能对该知识库进行语义搜索（`/recall/knowledge`）

---

## 创建知识库

```
POST https://openapi.biji.com/open/api/v1/resource/knowledge/create
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

## 知识库笔记列表

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id=abc123&page=1
```

参数：
- `topic_id` (string, 必填) - 知识库 ID（来自 `/knowledge/list` 的 `topic_id` 字段）
- `page`: 页码，从 1 开始，默认 1（固定每页 20 条）

返回 `notes[]`，每项字段：
- `note_id`：笔记 ID（**字符串**）
- `title`、`content`、`note_type`、`tags`、`created_at`、`edit_time`

用 `has_more` 判断是否有下一页。

---

## 知识库选择逻辑

当用户说「存到对应的知识库」或「存到相关知识库」时：
1. 先调用 `GET /knowledge/list` 获取所有知识库列表
2. 根据笔记标题、内容、标签，与知识库名称和描述做模糊匹配
3. 匹配置信度高时直接执行，并告知用户存入了哪个知识库
4. 置信度低或有歧义时，列出候选知识库让用户选择
5. 用户未提及知识库时，**不要擅自存入**任何知识库

---

## 添加笔记到知识库

```
POST https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add
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

## 从知识库移除笔记

```
POST https://openapi.biji.com/open/api/v1/resource/knowledge/note/remove
Content-Type: application/json
```

请求体：
```json
{
  "topic_id": "abc123",
  "note_ids": [123456789]
}
```

返回：
```json
{"removed_count": 1}
```

---

## 博主订阅

### 博主列表

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/bloggers?topic_id={topic_id}&page=1
```

参数：
- `topic_id` (string, 必填) - 知识库 ID（来自 `/knowledge/list` 的 `topic_id` 字段）
- `page`: 页码，从 1 开始

每页固定 20 条，用 `has_more` 判断。

返回 `bloggers[]`，每项字段：

| 字段 | 说明 |
|------|------|
| follow_id | 订阅关系 ID，**查博主内容时必用** |
| account_name | 博主名称 |
| account_icon | 博主头像 |
| platform | 平台（如 DEDAO）|
| account_url | 博主主页链接 |
| follow_time | 订阅时间（YYYY-MM-DD HH:MM:SS）|

### 博主内容列表

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/blogger/contents?topic_id={topic_id}&follow_id={follow_id}&page=1
```

参数：`topic_id`（知识库 ID）、`follow_id`（博主订阅 ID）、`page`（页码）

返回 `contents[]`，关键字段：`post_id_alias`（详情必用）、`post_title`、`post_summary`。

> 列表不含原文，需要原文请调详情接口。完整字段见 [api-details.md](api-details.md#博主内容字段说明)。

### 博主内容详情（含原文）

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/blogger/content/detail?topic_id={topic_id}&post_id={post_id_alias}
```

参数：`topic_id`（知识库 ID）、`post_id`（内容 ID，来自列表的 `post_id_alias`）

返回完整内容，包含 `post_media_text`（原文）。

---

## 直播订阅

### 已完成直播列表

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/lives?topic_id={topic_id}&page=1
```

参数：`topic_id`（知识库 ID）、`page`（页码）

返回 `lives[]`，关键字段：
- `live_id`：直播 ID（**字符串**，详情接口传此值）
- `name`、`status`

**只返回已结束且 AI 已处理完的直播。** 完整字段见 [api-details.md](api-details.md#直播字段说明)。

### 直播详情（总结 + 原文）

```
GET https://openapi.biji.com/open/api/v1/resource/knowledge/live/detail?topic_id={topic_id}&live_id={live_id}
```

参数：
- `topic_id`（知识库 ID）
- `live_id`（**字符串**，来自列表的 `live_id` 字段）

返回完整内容，包含 `post_summary`（AI 摘要）和 `post_media_text`（原文转写）。

---

## 展示模板

知识库列表：
> 📚 你有 {N} 个知识库：
>
> 1. **{name}** — {description}（{note_count} 篇笔记，{blogger_count} 个博主）
> 2. ...

添加成功：
> ✅ 已将「{note_title}」加入知识库「{kb_name}」
