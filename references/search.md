# 语义搜索

## 概述

在笔记中进行语义召回，支持全局搜索和指定知识库搜索。无需拉取全部数据，直接返回相关片段。

---

## 全局语义搜索

> 适用场景：「搜一下」「找找我哪些笔记提到了 XX」

**所需 scope**: `note.recall.read`

```
POST https://openapi.biji.com/open/api/v1/resource/recall
Content-Type: application/json
```

请求体：
```json
{
  "query": "搜索关键词",
  "top_k": 3
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| query | string, 必填 | 搜索关键词或语义描述 |
| top_k | int, 可选 | 返回数量，默认 **3**，最大 **10** |

返回结构（结果已按相关度**从高到低**排序）：

```json
{
  "results": [
    {
      "note_id": "1896830231705320746",
      "note_type": "NOTE",
      "title": "笔记标题",
      "content": "笔记内容片段",
      "created_at": "2025-12-24 15:20:15"
    }
  ]
}
```

---

## 知识库语义搜索

> 适用场景：「在我的 XX 知识库搜一下 XX」

**所需 scope**: `note.topic.recall.read`

```
POST https://openapi.biji.com/open/api/v1/resource/recall/knowledge
Content-Type: application/json
```

请求体：
```json
{
  "topic_id": "qnNX75j0",
  "query": "搜索关键词",
  "top_k": 3
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| topic_id | string, 必填 | 知识库 ID（来自 `/knowledge/list` 的 `topic_id` 字段） |
| query | string, 必填 | 搜索关键词或语义描述 |
| top_k | int, 可选 | 返回数量，默认 **3**，最大 **10** |

返回结构同全局搜索。

---

## 召回结果字段说明

| 字段 | 说明 |
|------|------|
| note_id | 笔记 ID（string）；**仅 `NOTE` 类型有值**，其余类型均为空 |
| note_type | 内容类型：`NOTE` / `FILE` / `BLOGGER` / `LIVE` / `URL` / `DEDAO` |
| title | 笔记/文档标题 |
| content | 相关内容片段 |
| created_at | 创建/发布时间（YYYY-MM-DD HH:MM:SS）|
| page_no | `FILE` 类型时表示文件页码，其余类型省略 |

> **后续操作**：`NOTE` 类型可调详情接口获取全文，其余类型只能展示召回片段。

---

## 示例对话

> 用户：「找找我哪些笔记提到了大模型 API」
> → `POST /recall` `{ "query": "大模型 API", "top_k": 3 }`

> 用户：「在我的 AI 学习知识库里搜一下 RAG」
> → 先调 `/knowledge/list` 找到对应知识库的 `topic_id`，再 `POST /recall/knowledge` `{ "topic_id": "xxx", "query": "RAG", "top_k": 3 }`

---

## 展示模板

搜索完成后：
> 🔍 找到 {N} 条相关笔记：
>
> 1. **{title}** （{created_at}）
>    {content 片段}
>
> 2. ...
>
> （`NOTE` 类型可回复「看原文」获取完整内容）
