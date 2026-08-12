---
name: getnote
description: 把得到大脑连接到当前 AI，并把用户的保存、查询、搜索、知识库和标签需求路由给对应领域 Skill。用户说“安装/连接/更新得到大脑”“记一下”“帮我找笔记”“整理到知识库”或“管理标签”时使用。
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
              "bins": ["getnote", "gnote"],
              "label": "安装得到大脑执行组件",
            },
          ],
      },
  }
---

# 得到大脑

本 Skill 是得到大脑的总入口，只负责三件事：连接账号、选择正确的领域 Skill、在领域任务之间保持统一的安全边界。不要在这里维护完整命令表或自行拼 OpenAPI 请求。

## 首次使用

1. 缺少执行组件时自动安装，不要求用户理解 CLI、npm 或依赖关系。
2. 尚未授权时启动浏览器授权；不得向用户索要 API Key、Cookie 或 Authorization。
3. 安装或升级后运行 `getnote setup`，把 CLI 内置的 5 个领域 Skill 同步到当前 AI；平台无法注册多个 Skill 时，继续使用本包内完全一致的领域文件。
4. 用户允许时保存一条测试笔记；只有返回真实标题和可打开的笔记链接才算完成。

## 路由

匹配用户意图后，必须读取并遵循对应领域 Skill：

- 登录、连接、配额、诊断和更新：[`skills/getnote-auth/SKILL.md`](skills/getnote-auth/SKILL.md)
- 保存、查看、修改、分享和深层内容：[`skills/getnote-note/SKILL.md`](skills/getnote-note/SKILL.md)
- 按主题或自然语言查找笔记：[`skills/getnote-search/SKILL.md`](skills/getnote-search/SKILL.md)
- 知识库、文件夹、博主订阅和直播：[`skills/getnote-kb/SKILL.md`](skills/getnote-kb/SKILL.md)
- 查看、添加和删除标签：[`skills/getnote-tag/SKILL.md`](skills/getnote-tag/SKILL.md)

一个任务涉及多个领域时，按实际步骤依次读取对应 Skill。例如“找到最近的客户反馈并放进客户档案”先读搜索，再读知识库。

## 统一规则

- 所有真实操作由得到大脑执行组件完成；参数不确定时读取对应命令帮助。
- ID 始终按字符串原样传递；链接只使用真实返回值，不自行拼接域名。
- 写操作结果不确定时先查询原任务或最近结果，禁止盲目重复创建。
- 删除、覆盖、替换全部标签、公开分享和批量移出必须先确认。
- 群聊或共享会话中不主动展开私密全文，先确认请求者和展示范围。
- 失败时说明真实原因、是否可重试和下一步，并保留 `request_id`；不能伪造成功。

## 用户要求更新

用户说“帮我更新得到大脑”已经构成更新授权。自动完成可处理的更新、同步领域 Skill、运行诊断并验证读取能力；只有平台必须人工确认时才让用户完成唯一必要的点击。
