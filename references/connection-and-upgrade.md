# 连接、授权、诊断与升级

## 首次连接

```bash
getnote doctor -o json
```

`checks` 中至少关注：

- `cli`：CLI 可执行；
- `auth`：已授权得到大脑账号；
- `api`：OpenAPI 请求成功；
- `node` / `npx`：安装本地原子 Skills 时需要，不影响已安装 CLI 的普通命令。

未授权时：

```bash
getnote auth login
```

把 CLI 给出的浏览器授权方式交给用户。禁止向用户索要 API Key。

授权完成后再次运行 `getnote doctor -o json`。只有 `auth` 和 `api` 通过，才能说连接成功。

## 查看授权

```bash
getnote auth status
getnote auth logout
```

`logout` 会清除本机保存的凭证。用户没有明确要求退出时不要执行。

## 检查契约和版本

```bash
getnote capabilities -o json
getnote version --check-update
getnote update --check
```

Skill 2.0 依赖 `contract_version: "2.0"`。如果不存在该字段，说明 CLI 太旧。

## 升级 CLI

先征得用户同意，再执行一种方式：

```bash
getnote update
```

或 npm 完整升级：

```bash
npm install -g @getnote/cli@latest
```

升级后必须重新运行：

```bash
getnote version
getnote doctor -o json
getnote capabilities -o json
```

`getnote update` 只升级 CLI，不会更新 Skill 文档。Skill 本身由宿主平台的 SkillHub、ClawHub 或安装包更新机制升级。

宿主支持 ClawHub CLI 时，可单独检查并升级 Skill：

```bash
clawhub update getnote
```

不要在每次对话中自动升级。版本检查只在首次安装、能力契约不匹配、用户主动要求或故障排查时执行，避免无意义地修改用户环境。

## 安装 CLI 内置原子 Skills

本 Skill 是面向 OpenClaw / WorkBuddy 等平台的聚合导航。Codex、Claude Code、Cursor 等本地 Agent 可使用 CLI 仓库内置的五个原子 Skills：

```bash
getnote setup
```

或：

```bash
npx skills add iswalle/getnote-cli -y -g
```

两种 Skill 共享同一个 CLI 执行层，不需要重复实现 API。

## 卸载边界

Skill、CLI 和本机授权互相独立：

- 从 AI 平台移除 Skill，不会删除 CLI 或退出得到大脑账号；
- `npm uninstall -g @getnote/cli` 只删除 CLI，不会撤销服务端授权；
- 用户要求清除本机授权时，先运行 `getnote auth logout`；
- 只有用户明确要求完整卸载时，才依次退出授权、移除 CLI，并按宿主平台方式移除 Skill。
