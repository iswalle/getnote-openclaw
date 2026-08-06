# 得到大脑 Skill 2.0

让 WorkBuddy、QClaw、OpenClaw 等支持 Skill 的 AI，能够可靠地保存、查询和整理得到大脑笔记。

新版采用“Skill 理解意图，CLI 确定执行”的结构：

- Skill：判断用户想保存、查询还是整理，并在高风险操作前确认。
- `@getnote/cli`：负责授权、参数校验、图片上传、异步轮询、错误恢复和真实结果。
- OpenAPI：仍是统一的数据与权限底座，但不再让模型直接拼请求。

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

当前 2.0 分支用于本地联调，尚未发布到 ClawHub。
