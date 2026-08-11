# 得到大脑 Skill 2.0

让 WorkBuddy、QClaw、OpenClaw 等支持 Skill 的 AI，能够可靠地保存、查询和整理得到大脑笔记。

新版采用“Skill 理解意图，CLI 确定执行”的结构：

- Skill：判断用户想保存、查询还是整理，并在高风险操作前确认。
- `@getnote/cli`：负责授权、参数校验、图片上传、异步轮询、错误恢复和真实结果。
- OpenAPI：仍是统一的数据与权限底座，但不再让模型直接拼请求。

与把 CLI 运行时代码直接打进 Skill 的方案不同，本仓库只维护意图导航、操作边界和结果解释，运行时统一使用独立发布的 `@getnote/cli`。这样独立 Skill、CLI 内置原子 Skills 和人工命令行不会各自维护一套 API 实现。

## Skill 结构

- `SKILL.md`：总入口、意图路由、确认规则和执行协议；
- `references/connection-and-upgrade.md`：安装、授权、诊断和升级；
- `references/note-operations.md`：保存、列表、详情、修改、删除和分享；
- `references/search-and-results.md`：语义搜索和结果展示；
- `references/knowledge-bases.md`：自有、订阅知识库、博主与直播；
- `references/tags-and-quota.md`：标签与配额；
- `references/errors-and-output.md`：结构化结果、错误和安全重试；
- `references/commands.md`：CLI contract 2.0 的完整命令索引。

正文只保留跨任务都要遵守的规则，执行具体任务时再读取对应 reference，避免一次把所有命令和参数塞给模型。

## 安装

### WorkBuddy

对 WorkBuddy 说：

> 帮我安装 SkillHub 中的 getnote

也可以下载本仓库 Skill 包后上传安装。

### OpenClaw / QClaw 等 Claw 生态

在技能市场安装“得到大脑”，或使用平台支持的官方安装命令。Skill 会声明并安装依赖的 `@getnote/cli`。

### 本地验证

```bash
npm install -g @getnote/cli
getnote doctor -o json
```

首次使用根据提示完成授权，然后说：

> 帮我保存一条测试笔记：得到大脑 Skill 2.0 安装完成

只有返回真实的笔记标题和可打开的 `note_url`，才算安装完成。

## 开发验收

```bash
python3 /Users/walle/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
getnote capabilities -o json
getnote doctor -o json
```

Skill 2.0 要求 `@getnote/cli` 版本不低于 1.4.0，并以 CLI 输出的 contract 2.0 为执行契约。发布前必须同时验证 CLI、Skill 和真实账号只读调用。
