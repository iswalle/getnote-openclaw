---
name: getnote
description: 使用得到大脑保存文字、链接和图片，查看、搜索或维护笔记、标签与知识库。用户说“记一下”“保存这个链接/图片”“最近有哪些笔记”“帮我找笔记”“查看/修改/分享这条笔记”“整理到知识库”或需要连接、诊断、升级得到大脑时使用。只负责理解意图和导航，所有真实操作通过 getnote CLI 完成。
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

把用户意图翻译成 `getnote` CLI 命令。CLI 是鉴权、参数、ID、上传、异步任务、幂等和 API 行为的唯一事实源；不要自己拼 OpenAPI 请求或编造结果。

## 准备执行

- 正常任务直接执行对应命令，不要每次运行兼容检查。
- 首次使用、升级后或排查故障时运行 `getnote doctor -o json`。
- 需要确认能力兼容时运行 `getnote capabilities -o json`；contract 不是 `2.0` 时先征得同意，再运行 `getnote update`。
- 未授权时运行 `getnote auth login`，让用户在浏览器完成授权。
- 找不到 `getnote` 时说明需要安装执行组件；获得同意后运行 `npm install -g @getnote/cli@latest`。
- 不确定参数时运行当前命令的 `--help`，不要根据 Skill 文档猜参数。

## 路由到 CLI

| 用户意图 | 命令入口 |
|---|---|
| 保存文字、链接、图片或长笔记 | `getnote save` |
| 查询异步保存任务 | `getnote task` |
| 查看最近笔记 | `getnote notes` |
| 查看笔记详情 | `getnote note` |
| 修改、删除或公开分享 | `getnote note update` / `getnote note delete` / `getnote note share` |
| 语义搜索 | `getnote search` |
| 自有或订阅知识库 | `getnote kbs` / `getnote kbs-sub` |
| 查看、创建或维护知识库 | `getnote kb`；继续操作前运行 `getnote kb --help` |
| 查看、添加或删除标签 | `getnote tag`；继续操作前运行 `getnote tag --help` |
| 查看配额 | `getnote quota` |
| 登录、状态和退出 | `getnote auth` |
| 诊断、版本和升级 | `getnote doctor` / `getnote version` / `getnote update` |

## 执行规则

1. 机器调用添加 `-o json`，以退出码和结构化结果为准；HTTP 200 不代表业务成功。
2. 笔记、知识库、任务、标签和游标 ID 始终按字符串原样传递。
3. 长文本使用 `getnote save --content-file` 或 `getnote save --stdin`，不要硬塞进命令行参数。
4. 保存、列表和搜索只返回 CLI 给出的 `note_url`，禁止自行拼接链接。
5. 链接和图片保存必须等待 CLI 给出最终状态；处理中不能说成保存成功。
6. 同一次创建的安全重试复用原 `--idempotency-key`；状态不确定时先核实，不要重复写入。
7. 不擅自添加知识库、父笔记、标签或公开分享参数。
8. CLI 失败时保留真实原因和 `request_id`，只在明确可重试时重试。

## 必须确认

执行删除笔记、覆盖正文、替换全部标签、公开分享或批量移出知识库前，先向用户确认。用户未要求公开分享时，只返回私有 `note_url`。

## 回复结果

- 保存成功：返回真实标题和可点击的 `note_url`。
- 列表或搜索：按用户要求展示标题、字符串 ID 和 `note_url`。
- 失败：说明失败步骤、CLI 返回的原因和下一步；不得把安装完成说成授权完成，也不得吞掉错误。

## 升级边界

- `getnote update` 只升级 CLI。
- Skill 由当前平台的 SkillHub、ClawHub 或安装包更新。
- 两者版本独立；CLI 帮助与结构化输出始终优先于 Skill 中的描述。
