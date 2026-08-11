# 知识库导航

## 先区分自有与订阅

```bash
getnote kbs -o json
getnote kbs-sub -o json
```

- `kbs`：用户自有知识库，包括默认、书籍和客户档案等 Scope；
- `kbs-sub`：用户订阅的知识库，通常只读；
- 保存到指定知识库时必须使用返回的 `topic_id`，不能只拉默认 Scope，也不能用名称代替 ID。

## 查看知识库笔记

```bash
getnote kb "topic_id" --limit 20 -o json
getnote kb "topic_id" --all --no-content -o json
```

## 新建知识库

```bash
getnote kb create "名称" --desc "描述" -o json
```

## 加入或移出笔记

```bash
getnote kb add "topic_id" "note_id" -o json
getnote kb remove "topic_id" "note_id" -o json
```

可一次传多个 `note_id`。订阅知识库不是本人管理时不能写入；移出前需确认。

## 博主内容

```bash
getnote kb bloggers "topic_id" -o json
getnote kb blogger-contents "topic_id" "follow_id" -o json
getnote kb blogger-content "topic_id" "post_id" -o json
```

先从 bloggers 获取 `follow_id`，再取内容列表；详情中的 `post_media_text` 是原文。

## 直播

```bash
getnote kb lives "topic_id" -o json
getnote kb live "topic_id" "live_id" -o json
getnote kb live-follow "topic_id" "得到直播链接" -o json
```

`live-follow` 当前只支持得到 App 直播链接。直播详情中 `post_summary` 是总结，`post_media_text` 是原文。
