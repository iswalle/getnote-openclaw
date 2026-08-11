# 搜索与结果展示

## 全局搜索

```bash
getnote search "用户要找的内容" --limit 10 -o json
```

## 知识库内搜索

先从 `getnote kbs -o json` 获取真实 `topic_id`，再运行：

```bash
getnote search "用户要找的内容" --kb "topic_id" --limit 10 -o json
```

不要自行把知识库名称当 ID，也不要把搜索拆成多个近义词反复调用。没有结果时如实说明，并让用户决定是否调整查询。

## 结果语义

- 结果按语义相关性排序；
- `note_type=NOTE` 时通常有 `note_id`；其他类型可能没有；
- 必须保留 CLI 返回的 `title`、字符串 `note_id`、`note_url`、摘要和相关性；
- 禁止自行拼接笔记链接；
- 用户只要求搜索时，返回搜索结果即可，不要自动修改、分享或移动笔记。

建议展示：

```text
1. 《标题》
   查看：真实 note_url
   摘要：CLI 返回的摘要
```

需要完整正文时，再对有 `note_id` 的普通笔记执行：

```bash
getnote note "笔记ID" -o json
```
