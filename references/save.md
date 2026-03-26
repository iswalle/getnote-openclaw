# 保存笔记

## 概述

新建文本、链接、图片三种类型的笔记。文本笔记同步完成；链接和图片笔记是异步任务，需轮询进度。

---

## 新建笔记

```
POST https://openapi.biji.com/open/api/v1/resource/note/save
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

详细字段说明见 [api-details.md](api-details.md#新建笔记字段说明)。

- `plain_text`：同步返回，立即完成，响应中包含 `note_id`（字符串）
- `link` / `img_text`：返回 `task_id`，**必须轮询** `/task/progress`

---

## 查询任务进度

```
POST https://openapi.biji.com/open/api/v1/resource/note/task/progress
Content-Type: application/json
```

请求体：
```json
{"task_id": "task_abc123xyz"}
```

返回：
- `status`: `pending` | `processing` | `success` | `failed`
- `note_id`: 成功时返回笔记 ID（**字符串**）；任务进行中时值为 `"0"`，需过滤
- `error_msg`: 失败时返回错误信息

**建议 10-30 秒间隔轮询，直到 success 或 failed**。

---

## 链接笔记完整流程

> ⚠️ **必须遵循的体验流程**

**步骤 1**：提交任务
```
POST https://openapi.biji.com/open/api/v1/resource/note/save {note_type:"link", link_url:"https://..."}
```

返回结构：
```json
{
  "data": {
    "created_count": 1,
    "tasks": [{"task_id": "69c3995e99f5a67e", "url": "https://..."}],
    "message": "链接笔记任务已创建，请通过 /note/task/progress 接口查询处理状态"
  }
}
```

⚠️ **task_id 在 `data.tasks[0].task_id`**，不是 `data.task_id`。

拿到 task_id 后，**立即发消息给用户**：
> ✅ 链接已保存，正在抓取原文和生成总结，稍后告诉你结果...

> ⚠️ **重复链接说明**：OpenAPI 层不做 URL 去重，重复保存同一链接会创建新笔记任务。App 端有去重提示，API 调用方需自行判断。

**步骤 2**：后台轮询（10-30 秒间隔）
```
POST https://openapi.biji.com/open/api/v1/resource/note/task/progress {task_id} → 直到 status=success/failed
```

**步骤 3**：任务完成后，**调详情接口展示价值**
```
GET https://openapi.biji.com/open/api/v1/resource/note/detail?id={note_id}
```
然后发第二条消息：
> ✅ 笔记生成完成！
> - 📄 **原文**：已保存 {web_page.content 字数} 字
> - 📝 **总结**：{content 内容，即 AI 生成的摘要}
> - 🔗 **来源**：{web_page.url}

---

## 图片笔记完整流程

**步骤 1**：获取上传凭证
```
GET https://openapi.biji.com/open/api/v1/resource/image/upload_token?mime_type=jpg&count=1
```

参数：
- `mime_type`: `jpg` | `png` | `gif` | `webp`，默认 `png`
- `count`: 需要的 token 数量，默认 1，最大 9

⚠️ **mime_type 必须与实际文件格式一致**，否则 OSS 签名失败。

返回字段说明见 [api-details.md](api-details.md#图片上传凭证返回字段)。

**步骤 2**：上传文件到 OSS

> ⚠️ **字段顺序必须严格遵守**，否则 OSS 签名验证失败。

字段顺序：`key → OSSAccessKeyId → policy → signature → callback → Content-Type → file`

完整示例见 [api-details.md](api-details.md#oss-上传详细示例)。

**步骤 3**：提交任务
```
POST https://openapi.biji.com/open/api/v1/resource/note/save {note_type:"img_text", image_urls:[access_url]}
```
拿到 task_id 后，**立即发消息给用户**：
> ✅ 图片已保存，正在识别内容，稍后告诉你结果...

**步骤 4**：后台轮询
```
POST https://openapi.biji.com/open/api/v1/resource/note/task/progress {task_id} → 直到 status=success/failed
```

**步骤 5**：任务完成后，**调详情接口展示价值**
```
GET https://openapi.biji.com/open/api/v1/resource/note/detail?id={note_id}
```
然后发第二条消息：
> ✅ 图片笔记生成完成！
> - 📝 **识别内容**：{content 内容}
> - 🏷️ **标签**：{tags}
