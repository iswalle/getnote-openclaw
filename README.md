# 得到大脑 Skill 2.0

让 WorkBuddy、QClaw、OpenClaw 等支持 Skill 的 AI，能够可靠地保存、查询和整理得到大脑笔记。

新版采用“Skill 理解意图，CLI 确定执行”的结构：

- Skill：判断用户想保存、查询还是整理，并在高风险操作前确认。
- `@getnote/cli`：负责授权、参数校验、图片上传、异步轮询、错误恢复和真实结果。
- OpenAPI：仍是统一的数据与权限底座，但不再让模型直接拼请求。

与把 CLI 运行时代码直接打进 Skill 的方案不同，本仓库只维护意图导航、操作边界和结果解释，运行时统一使用独立发布的 `@getnote/cli`。这样独立 Skill、CLI 内置原子 Skills 和人工命令行不会各自维护一套 API 实现。

## Skill 结构

- `SKILL.md`：唯一运行时文档，只保留意图路由、执行规则和安全边界；
- `scripts/verify_cli_contract.py`：开发时检查 Skill 提到的命令是否真实存在；
- `.github/workflows/validate.yml`：PR 阶段使用已发布 CLI 自动执行契约检查；
- `.clawhubignore`：发布时排除 README、开发脚本和仓库配置，最终 Skill 包只包含 `SKILL.md` 与许可证。

命令参数、输出字段和可用子命令不在 Skill 中复制，统一以 CLI 的 `--help` 与 `capabilities` 为事实源。

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
python3 scripts/verify_cli_contract.py
getnote doctor -o json
```

Skill 2.0 要求 `@getnote/cli` 版本不低于 1.4.0，并以 CLI 输出的 contract 2.0 为执行契约。发布前必须同时验证 CLI、Skill 和真实账号只读调用。
