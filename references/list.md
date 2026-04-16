# 笔记列表与详情

## 概述

浏览笔记列表、查看详情（含原文/转写）、更新笔记内容、删除笔记。

---

## 笔记列表

```
GET https://openapi.biji.com/open/api/v1/resource/note/list?cursor=0
```

参数：
- `cursor` (string, 可选) - 翻页游标，首次不传，后续将响应中的 `cursor` 字段直接传入即可

响应结构（`data` 下）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `notes` | array | 笔记列表 |
| `has_more` | bool | 是否还有更多 |
| `cursor` | string | 下一页游标（**推荐**，直接传入下次请求的 `cursor` 参数） |
| `next_cursor` | int | 下一页游标（向后兼容） |
| `total` | int | 本次返回条数（每次固定 20 条） |

`notes[]` 列表项字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `note_id` | string | 笔记 ID（字符串，推荐使用） |
| `id` | int64 | 笔记 ID（整数，向后兼容） |
| `title` | string | 笔记标题 |
| `content` | string | 正文（markdown） |
| `note_type` | string | 笔记类型，见下表 |
| `source` | string | 来源 |
| `tags` | array | 标签列表，每项包含 `id`、`name`、`type` |
| `topics` | array | 所属知识库列表，每项包含 `id`、`name` |
| `is_child_note` | bool | 是否为子笔记 |
| `children_count` | int | 子笔记数量 |
| `parent_id` | int64 | 父笔记 ID（是子笔记时才有） |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

**翻页方式**：将响应的 `cursor` 字段直接传入下次请求的 `cursor` 参数即可，无需任何转换。

> ⚠️ **响应 JSON 可能包含未转义的控制字符**（笔记 content 中的原始换行符），建议用支持容错解析的 JSON 库处理。

**笔记类型 note_type**：

| 值 | 说明 |
|----|------|
| `plain_text` | 纯文本 |
| `img_text` | 图片笔记 |
| `link` | 链接笔记 |
| `audio` | 即时录音 |
| `meeting` | 会议录音 |
| `local_audio` | 本地音频 |
| `internal_record` | 内录音频 |
| `class_audio` | 课堂录音 |
| `recorder_audio` | 录音卡长录 |
| `recorder_flash_audio` | 录音卡闪念 |

---

## 笔记详情

```
GET https://openapi.biji.com/open/api/v1/resource/note/detail?id={note_id}
```

参数：
- `id` (int64, 必填) - 笔记 ID
- `image_quality` (string, 可选) - 传 `original` 返回正文中图片的原图链接（无压缩）

**⚠️ 返回结构**：数据在 `data.note` 对象下，不是 `data` 直接取：
```json
{
  "data": {
    "note": {
      "id": "1234567890",
      "note_id": "1234567890",
      "title": "笔记标题",
      "content": "笔记内容",
      "tags": [...],
      ...
    }
  }
}
```

详情响应字段（`data.note` 下）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `note_id` | string | 笔记 ID（字符串，推荐使用） |
| `id` | int64 | 笔记 ID（整数，向后兼容） |
| `title` | string | 标题 |
| `content` | string | 正文（markdown） |
| `note_type` | string | 笔记类型 |
| `source` | string | 来源 |
| `entry_type` | string | 录入方式：ai / manual |
| `tags` | array | 标签列表，每项包含 `id`、`name`、`type` |
| `topics` | array | 所属知识库，每项包含 `id`、`name` |
| `is_child_note` | bool | 是否为子笔记 |
| `children_count` | int | 子笔记数量 |
| `children_ids` | string[] | 子笔记 ID 列表（有子笔记时才返回） |
| `parent_id` | int64 | 父笔记 ID（是子笔记时才有） |
| `attachments` | array | 附件列表，见下表 |
| `audio` | object | 音频信息（音频笔记才有） |
| `web_page` | object | 网页信息（链接笔记才有） |
| `share_id` | string | 分享 ID |
| `version` | int | 版本号 |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

**`attachments[]` 字段**：

| 字段 | 说明 |
|------|------|
| `type` | 类型：image / audio / link / pdf |
| `url` | 地址（图片为 720px 缩略图） |
| `original_url` | 原图地址（仅图片类型） |
| `title` | 标题 |
| `size` | 文件大小 |
| `duration` | 时长（音频/视频） |

**`audio` 字段**：`play_url`、`duration`（秒）、`transcript`（转录文本）、`original`（原始文本）

**`web_page` 字段**：`url`、`domain`、`excerpt`（摘要）、`favicon`、`content`（链接原文）

**正文原图**：传 `image_quality=original` 时，`content` 中的 markdown 图片链接返回原图（无压缩参数）。

---

## 更新笔记

```
POST https://openapi.biji.com/open/api/v1/resource/note/update
Content-Type: application/json
```

请求体：
```json
{
  "note_id": 123456789,
  "title": "新标题",
  "content": "新的 Markdown 内容",
  "tags": ["标签1", "标签2"]
}
```

参数说明：
- `note_id` (int64, **必填**) - 要更新的笔记 ID
- `title` (string, 可选) - 新标题，不传则不更新
- `content` (string, 可选) - 新内容，不传则不更新
- `tags` (string[], 可选) - 新标签列表，**替换**原有标签（不传则保持原标签）

> ⚠️ **至少需要传 title、content、tags 中的一个**，否则返回错误。

> ⚠️ **仅支持 plain_text 类型笔记**，链接笔记、图片笔记等暂不支持更新。

---

## 删除笔记

```
POST https://openapi.biji.com/open/api/v1/resource/note/delete
Content-Type: application/json
```

请求体：
```json
{"note_id": 123456789}
```

笔记移入回收站，需要 `note.content.trash` scope。

---

## 笔记分享

生成笔记的公开分享链接，需要 `note.content.read` scope。

```
POST https://openapi.biji.com/open/api/v1/resource/note/sharing
Content-Type: application/json
```

请求体：
```json
{
  "note_id": "1234567890123456789",
  "share_exclude_audio": true
}
```

参数说明：
- `note_id` (string, **必填**) — 要分享的笔记 ID（**字符串格式**）
- `share_exclude_audio` (bool, 可选) — 是否排除音频内容，默认 false

响应：
```json
{
  "note_id": "1234567890123456789",
  "share_id": "rBzdMlXrzgYVM",
  "share_url": "https://biji.com/note/share_note/rBzdMlXrzgYVM"
}
```

> ✅ 对同一笔记多次调用，返回同一个 `share_url`（幂等）。

---

## 展示模板

列表展示：
> 📋 最近 {N} 条笔记：
>
> 1. **{title}** · {note_type} · {created_at}
> 2. ...
>
> （回复笔记序号或标题可查看详情）

详情展示（链接笔记）：
> 📄 **{title}**
> 🔗 来源：{web_page.url}
> 📝 摘要：{content}
> 🏷️ 标签：{tags}
