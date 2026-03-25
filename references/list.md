# 笔记列表与详情

## 概述

浏览笔记列表、查看详情（含原文/转写）、更新笔记内容、删除笔记。

---

## 笔记列表

```
GET https://openapi.biji.com/open/api/v1/resource/note/list?since_id=0
```

参数：
- `since_id` (int64, 必填) - 游标，首次传 `0`，后续用上次返回的 `next_cursor`

返回：`notes[]`、`has_more`、`next_cursor`、`total`（每次固定 20 条）

> ⚠️ **响应 JSON 可能包含未转义的控制字符**（笔记 content 中的原始换行符），建议用支持容错解析的 JSON 库处理。

> ⚠️ **`id`、`next_cursor`、`parent_id` 均为 int64**，JavaScript 环境必须在 `JSON.parse` 前做字符串化处理（见主文档「笔记 ID 处理规则」）。务必用字符串保存这些值，后续操作直接透传字符串即可。

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

**字段说明**：
- `note_id` (string) - 笔记 ID 的字符串格式，便于 AI Agent 解析，避免 int64 精度问题
- `children_ids` (string[]) - 子笔记 ID 列表（字符串格式），仅当有子笔记时返回

**图片附件**：`attachments[]` 中每个图片包含：
- `url` - 缩略图 URL（720px 压缩）
- `original_url` - 原图 URL（无压缩，适合需要高清图的场景）

**正文原图**：传 `image_quality=original` 时，`content` 中的 markdown 图片链接会返回原图（去掉 OSS 压缩参数）。

**详情独有字段**（列表不返回）：`audio.original`、`audio.play_url`、`audio.duration`、`web_page.content`、`web_page.url`、`web_page.excerpt`、`attachments[]`、`children_ids`。

完整字段说明见 [api-details.md](api-details.md#笔记详情独有字段)。

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
