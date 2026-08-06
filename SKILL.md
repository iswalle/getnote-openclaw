---
name: getnote
description: 使用得到大脑保存、查询、查看、整理笔记和知识库。用户说“记一下”“保存这个链接/图片”“最近有哪些笔记”“帮我找笔记”“查看这条笔记”“整理到知识库”或需要连接得到大脑时使用。所有真实操作必须通过 getnote CLI 完成，禁止自己拼接 OpenAPI 请求或编造执行结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["getnote"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@getnote/cli",
              "bins": ["getnote"],
              "label": "安装得到大脑 CLI",
            },
          ],
      },
  }
---

# 得到大脑

你负责理解用户想做什么；`getnote` CLI 负责确定地执行。不要直接调用 OpenAPI，不要自己处理 API Key、雪花 ID、图片上传或异步轮询。

## 首次使用

1. 先运行 `getnote doctor -o json`。
2. 如果系统找不到 `getnote`，或当前版本没有 `doctor`，先向用户说明“需要安装或升级得到大脑执行组件”；用户确认后运行 `npm install -g @getnote/cli@latest`，再重新检查。OpenClaw 若已按 metadata 自动补齐依赖，则不重复安装。
3. 如果 `auth` 未通过，运行 `getnote auth login`，把 CLI 输出的授权方式交给用户完成。
4. 再运行 `getnote doctor -o json`。只有 `auth` 与 `api` 均通过，才能声称连接成功。
5. 如需确认当前版本支持什么，运行 `getnote capabilities -o json`。

不得向用户索要或展示 API Key。不得把“已安装 Skill”说成“已完成账号授权”。

## 执行约定

- 机器可读调用统一添加 `-o json`；以 JSON 中的 `success` 和错误信息为准。
- 笔记 ID 始终当字符串原样传给 CLI，不转成浮点数。
- 保存成功后必须返回 CLI 给出的 `note_url`；没有 `note_url` 时只报告真实状态，不自行拼链接。
- 搜索和列表结果必须保留标题、笔记 ID 与 `note_url`，方便用户核对和打开。
- 用户未明确要公开分享时，只返回私有笔记链接，不调用 `note share`。
- 删除、覆盖正文、取消分享等不可逆或高风险操作，执行前向用户确认。
- API 或任务失败时说明真实原因；不要用模型推测补全结果，也不要把“处理中”说成“已完成”。

## 最常用操作

### 保存

```bash
getnote save "用户给出的文字、URL 或本地图片路径" -o json
```

可选参数：

- `--title "标题"`
- `--tag "标签"`，可重复
- `--topic-id "知识库ID"`
- `--parent-id "父笔记ID"`
- `--idempotency-key "本次稳定请求标识"`

同一次保存重试必须复用相同的 `--idempotency-key`。不要把多段长内容硬塞进命令行；长内容优先使用 CLI 已支持的安全输入方式。

### 最近笔记

```bash
getnote notes --limit 20 -o json
```

用户指定数量时使用 `--limit`。需要下一页时使用返回的字符串 `cursor`，不要使用旧式 `since_id`。

### 查看详情

```bash
getnote note "笔记ID" -o json
```

### 搜索

```bash
getnote search "用户要找的内容" --limit 10 -o json
```

限定知识库时添加 `--kb "知识库ID"`。

## 其他能力

需要更新、删除、分享、标签或知识库操作时，先运行对应命令的 `--help`，再按 CLI 的真实参数执行：

```bash
getnote note --help
getnote tag --help
getnote kbs --help
getnote kb --help
```

不要根据记忆猜参数。完整且稳定的命令参考见 [references/commands.md](references/commands.md)。

## 回复用户的格式

成功时简洁说明：

```text
已保存《标题》
查看笔记：https://www.biji.com/note/真实ID
```

列表或搜索时按相关性或时间列出，最多先展示用户要求的数量；每条都带标题和真实链接。

失败时说明：

1. 哪一步失败；
2. CLI 返回的原因；
3. 用户可以采取的下一步；
4. 有 `request_id` 时一并保留，便于排查。

## 严格禁止

- 禁止使用 `curl`、Python 或 JavaScript 绕过 CLI 直连得到大脑 OpenAPI。
- 禁止编造 note_id、note_url、标题、保存成功或搜索结果。
- 禁止在群聊中主动展开用户的私密笔记正文。
- 禁止为了“看起来成功”而吞掉错误或跳过异步任务完成确认。
