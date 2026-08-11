# 笔记操作

## 保存笔记

普通文字、URL 或本地图片：

```bash
getnote save "内容、URL 或本地图片路径" -o json
```

长文本不要硬塞进命令行：

```bash
getnote save --content-file ./long-note.md --title "标题" -o json
printf '%s' "$CONTENT" | getnote save --stdin --title "标题" -o json
```

常用参数：

| 参数 | 含义 |
|---|---|
| `--title` | 指定标题 |
| `--tag` | 添加标签，可重复 |
| `--topic-id` | 存入指定自有知识库 |
| `--parent-id` | 创建为指定笔记的子笔记 |
| `--idempotency-key` | 同一次保存重试时复用的稳定键 |
| `--content-file` | 从 UTF-8 文件读取长文本 |
| `--stdin` | 从标准输入读取长文本 |

用户未指定知识库、父笔记或标签时不要自行补充。链接和图片可能异步处理；CLI 会等待最终结果。只有结构化结果明确成功并返回 `note_url`，才能回复“保存成功”。

## 查看最近笔记

```bash
getnote notes --limit 20 -o json
getnote notes --cursor "上一页返回的游标" --limit 20 -o json
```

`cursor` 是字符串，原样传递。用户没有指定数量时默认展示 20 条。

## 查看详情和原文

```bash
getnote note "笔记ID" -o json
```

按字段提取：

```bash
getnote note "笔记ID" --field title
getnote note "笔记ID" --field content
getnote note "笔记ID" --field web_content
getnote note "笔记ID" --field audio_original
```

`content` 对链接、录音等类型通常是 AI 总结。用户要求原文时先查看 `note_type`：

| 类型 | 原文 | 总结 |
|---|---|---|
| 普通文字 | `content` | `content` |
| 链接/网页 | `web_content` | `content` |
| 录音 | `audio_original` | `content` |

## 修改

```bash
getnote note update "笔记ID" --title "新标题" -o json
getnote note update "笔记ID" --content "新正文" -o json
getnote note update "笔记ID" --tag "标签1,标签2" -o json
```

- `--content` 只支持普通文字笔记并会覆盖正文；
- `--tag` 会替换全部标签；
- 执行前必须确认。

## 删除

```bash
getnote note delete "笔记ID" --yes -o json
```

删除会将笔记移入回收站。必须先确认，确认后才使用 `--yes`。

## 分享

```bash
getnote note share "笔记ID" -o json
getnote note share "笔记ID" --exclude-audio -o json
```

这是公开分享。必须先确认，并原样返回 CLI 给出的 `share_url`。
