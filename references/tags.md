# 标签管理

## 概述

为笔记添加或删除标签。标签分为 AI 自动生成、用户手动添加、系统标签三种类型，其中系统标签不可删除。

---

## 添加标签

```
POST https://openapi.biji.com/open/api/v1/resource/note/tags/add
Content-Type: application/json
```

请求体：
```json
{
  "note_id": 123456789,
  "tags": ["工作", "重要"]
}
```

返回：`note_id`（string）+ `tags[]` 数组，每项包含：
- `id`：标签 ID（**删除时传入此值作为 `tag_id`**）
- `name`：标签名
- `type`：`ai` / `manual` / `system`

**标签类型 type**：

| 值 | 说明 |
|----|------|
| `ai` | AI 自动生成 |
| `manual` | 用户手动添加 |
| `system` | 系统标签（**不可删除**）|

---

## 删除标签

```
POST https://openapi.biji.com/open/api/v1/resource/note/tags/delete
Content-Type: application/json
```

请求体：
```json
{
  "note_id": 123456789,
  "tag_id": "123"
}
```

> `tag_id` 来自 `tags/add` 返回或 `GET /note/detail` 中 `tags[].id` 字段。

⚠️ `system` 类型标签不允许删除，尝试删除会返回错误。

---

## 展示模板

添加成功：
> 🏷️ 已为笔记「{title}」添加标签：{tags}

删除成功：
> ✅ 已删除标签「{tag_name}」
