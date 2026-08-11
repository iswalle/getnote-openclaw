---
name: getnote
description: 使用得到大脑保存文字、链接和图片，查看或搜索笔记，维护标签与知识库。用户说“记一下”“保存这个链接/图片”“最近有哪些笔记”“帮我找笔记”“查看/修改/分享这条笔记”“整理到知识库”或需要连接、诊断、升级得到大脑时使用。Skill 只负责识别意图和导航，所有真实操作必须通过 getnote CLI 完成。
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

这个 Skill 是 `getnote` CLI 的使用导航：你负责理解用户意图、选择命令、确认高风险操作并解释结果；CLI 负责鉴权、参数校验、雪花 ID、图片上传、异步轮询、幂等和真实 API 调用。

禁止自己拼接 OpenAPI 请求，禁止绕过 CLI，禁止编造执行结果。

## 先确认可用

首次使用、运行失败或用户要求检查连接时：

```bash
getnote doctor -o json
getnote capabilities -o json
```

按结果处理：

1. 找不到 `getnote`，或没有 `doctor` / `capabilities`：向用户说明需要安装或升级执行组件；获得确认后运行 `npm install -g @getnote/cli@latest`。
2. `auth` 未通过：运行 `getnote auth login`，让用户在浏览器完成授权。
3. `api` 未通过：保留 CLI 返回的错误和 `request_id`，不要反复重试。
4. 再次运行 `getnote doctor -o json`；只有 `auth` 与 `api` 都通过，才能说“已连接”。

不得向用户索要或展示 API Key。安装 Skill、安装 CLI 和完成账号授权是三件不同的事。

安装、授权、诊断和升级的完整规则见 [references/connection-and-upgrade.md](references/connection-and-upgrade.md)。

## 根据用户意图选择命令

| 用户要做什么 | CLI 入口 | 详细导航 |
|---|---|---|
| 保存文字、链接、图片或长笔记 | `getnote save` | [笔记操作](references/note-operations.md) |
| 查看最近笔记、笔记详情 | `getnote notes` / `getnote note` | [笔记操作](references/note-operations.md) |
| 修改、删除或公开分享笔记 | `getnote note update/delete/share` | [笔记操作](references/note-operations.md) |
| 按语义搜索笔记 | `getnote search` | [搜索与结果](references/search-and-results.md) |
| 查看、新建或整理知识库 | `getnote kbs` / `getnote kb ...` | [知识库](references/knowledge-bases.md) |
| 查看订阅知识库、博主和直播 | `getnote kbs-sub` / `getnote kb ...` | [知识库](references/knowledge-bases.md) |
| 查看、添加或删除标签 | `getnote tag ...` | [标签与配额](references/tags-and-quota.md) |
| 查看调用配额 | `getnote quota` | [标签与配额](references/tags-and-quota.md) |
| 检查连接、版本或升级 | `getnote doctor/version/update` | [连接与升级](references/connection-and-upgrade.md) |

跨平台依赖的完整命令索引见 [references/commands.md](references/commands.md)。不确定参数时，先运行 `getnote <command> --help`，不要凭记忆猜参数。

## 执行协议

每次真实操作都遵守：

1. 识别用户意图和输入，不擅自补充知识库、父笔记、标签或公开分享等参数。
2. 不确定参数、字段或限制时，先运行对应命令的 `--help`。
3. 机器可读调用统一添加 `-o json`。
4. 以退出码、JSON `success` 和错误字段为准；HTTP 成功不等于业务成功。
5. 笔记 ID、知识库 ID、任务 ID 和游标始终作为字符串原样传递，禁止转成浮点数。
6. 保存、列表和搜索成功后使用 CLI 返回的 `note_url`，禁止自行拼接链接。
7. 异步保存必须等待 CLI 返回最终结果；“处理中”不能说成“已完成”。
8. 同一次创建操作的重试必须复用同一个 `--idempotency-key`。

### 高风险操作

执行以下操作前必须向用户确认：

- `getnote note delete`：笔记移入回收站；
- `getnote note update --content`：替换文字笔记正文；
- `getnote note update --tag`：替换全部标签；
- `getnote note share`：创建公开分享链接；
- 批量从知识库移除笔记。

用户未明确要求公开分享时，只返回私有 `note_url`，不要调用 `note share`。

## 回复用户

成功保存时：

```text
已保存《CLI 返回的真实标题》
查看笔记：CLI 返回的真实 note_url
```

列表或搜索时：

- 按时间或相关性展示用户要求的数量；
- 每条保留标题、字符串笔记 ID 和可点击 `note_url`；
- 不在群聊中主动展开私密笔记全文。

失败时说明：哪一步失败、CLI 的真实原因、用户下一步怎么做；有 `request_id` 时一并保留。错误契约与重试规则见 [references/errors-and-output.md](references/errors-and-output.md)。

## Skill 与 CLI 的升级边界

- `getnote update` 或 `npm install -g @getnote/cli@latest` 只升级 CLI 执行组件。
- Skill 文档由当前 AI 平台的 SkillHub / ClawHub / 安装包更新能力升级，不能把“CLI 已升级”说成“Skill 已升级”。
- 当前 Skill 依赖 CLI contract `2.0`；用 `getnote capabilities -o json` 检查 `contract_version`。
- CLI 能力与本 Skill 描述冲突时，以当前 CLI 的 `--help` 和结构化输出为准，并提示用户升级 Skill。

## 严格禁止

- 禁止用 `curl`、Python、JavaScript 或 MCP 绕过 CLI 调用得到大脑 API。
- 禁止编造 note_id、note_url、标题、保存状态、搜索结果或配额。
- 禁止把安装完成说成授权完成，把提交任务说成保存完成。
- 禁止在失败后随意换参数、重复创建或吞掉错误。
- 禁止未经确认删除、覆盖、公开分享或批量移除内容。
