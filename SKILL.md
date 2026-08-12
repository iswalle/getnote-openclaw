---
name: getnote
description: 把得到大脑连接到当前 AI，并把用户的保存、查询、搜索、知识库和标签需求路由给对应领域 Skill。用户说“安装/连接/更新得到大脑”“记一下”“帮我找笔记”“整理到知识库”或“管理标签”时使用。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["node", "npm"] },
      },
  }
---

# 得到大脑

本 Skill 是得到大脑的总入口，负责安装和升级官方执行组件、连接账号、选择正确的领域 Skill，并在领域任务之间保持统一的安全边界。不要自行拼 OpenAPI 请求，也不要把领域命令重新堆回主 Skill。

## 首次使用

1. 运行 `bash scripts/install.sh --ensure`。它会检查 Node.js、确保官方 `@getnote/cli` 可执行；缺失时由 Agent 安装，不把依赖安装甩给用户手工完成。
2. 执行 `getnote version` 和 `getnote auth status`。尚未授权时运行 `getnote auth login` 并让用户只在浏览器确认；不得索要 API Key、Cookie 或 Authorization。
3. 执行 `getnote doctor -o json`。只有 `success=true` 且 `cli`、`auth`、`api` 三项通过，才能说已经连接。
4. 独立 Skill 包已经包含 5 个领域 Skill。对于 Codex、Claude Code、Cursor 等本地 Agent，可运行 `getnote setup` 把 CLI 同源的领域 Skill 注册到平台；不要重复安装另一套实现。
5. 先运行 `getnote notes --limit 1 -o json` 做无写入验收。只有用户同意时才保存测试笔记，而且必须返回真实标题、字符串笔记 ID 和可打开的 `note_url` 才算完成。

## 路由

匹配用户意图后，必须读取并遵循对应领域 Skill：

- 登录、连接、配额、诊断和更新：[`skills/getnote-auth/SKILL.md`](skills/getnote-auth/SKILL.md)
- 保存、查看、修改、分享和深层内容：[`skills/getnote-note/SKILL.md`](skills/getnote-note/SKILL.md)
- 按主题或自然语言查找笔记：[`skills/getnote-search/SKILL.md`](skills/getnote-search/SKILL.md)
- 知识库、文件夹、博主订阅和直播：[`skills/getnote-kb/SKILL.md`](skills/getnote-kb/SKILL.md)
- 查看、添加和删除标签：[`skills/getnote-tag/SKILL.md`](skills/getnote-tag/SKILL.md)

一个任务涉及多个领域时，按实际步骤依次读取对应 Skill。例如“找到最近的客户反馈并放进客户档案”先读搜索，再读知识库。

## 统一规则

- 所有真实操作由官方 `getnote` CLI 完成；参数不确定时读取对应命令 `--help`，机器调用统一加 `-o json`。
- 退出码非 0 一律是失败。成功结果读取 `success=true` 和领域 Skill 指定的 `data` 字段；失败结果读取 `error.code/message/reason/retryable` 和可选 `request_id`，不能根据自然语言猜成功。
- ID 始终按字符串原样传递；链接只使用真实返回值，不自行拼接域名。
- 写操作结果不确定时先查询原任务或最近结果，禁止盲目重复创建。
- 删除、覆盖、替换全部标签、公开分享和批量移出必须先确认。
- 群聊或共享会话中不主动展开私密全文，先确认请求者和展示范围。
- 失败时说明真实原因、是否可重试和下一步，并保留 `request_id`；不能伪造成功。

## 用户要求更新

用户说“帮我更新得到大脑”已经构成更新授权。运行 `bash scripts/install.sh --update`，它会升级 CLI 并刷新当前 Skill 包；随后同步领域 Skill、运行诊断并验证读取能力。只有平台必须人工确认时才让用户完成唯一必要的点击。
