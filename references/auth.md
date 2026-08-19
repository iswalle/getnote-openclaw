
# 得到大脑连接、诊断与升级

负责把“用户想用得到大脑”推进到真正可执行的状态。不要只说“已安装”：CLI 可执行、账号已授权、API 可读三项都通过才算连接成功。

## 首次连接闭环

按顺序执行，已经满足的步骤直接跳过：

1. 用 `command -v getnote` 检查官方 CLI。缺失时调用平台根据 `SKILL.md` frontmatter 提供的 `@getnote/cli` 安装流程；不要让用户选择安装方式，不查找或运行 `scripts/install.sh`。
2. 执行 `getnote setup`，让 CLI 检测本机 AI、同步五个领域 Skill 并引导授权。独立聚合 Skill 仍由 ClawHub/OpenClaw 管理，不由 CLI 覆盖。
3. 执行 `getnote version` 和 `getnote auth status`。未登录时运行 `getnote auth login`，让用户只在浏览器中确认，不索要 API Key、Cookie 或 Authorization。
4. 执行 `getnote doctor -o json`。只有退出码为 0、`diagnostics_completed=true` 且 `ready=true`，才能宣布连接完成；先处理 `issues[].blocking=true`，再按 `next_actions[]` 修复。
5. 先用 `getnote notes --limit 1 -o json` 做无写入验收。只有用户同意创建测试内容时，才保存测试笔记。

## 日常路由

| 意图 | 命令 |
|---|---|
| 登录 | `getnote auth login` |
| 查看登录状态 | `getnote auth status` |
| 退出登录 | `getnote auth logout` |
| 诊断连接 | `getnote doctor -o json` |
| 查看 CLI 能力契约 | `getnote capabilities -o json` |
| 为本机 AI 同步领域 Skill | `getnote setup` |
| 查看 AI 对话额度 | `getnote quota -o json` |
| 查看版本 | `getnote version` |
| 检查升级 | `getnote update --check` |
| 执行升级 | `getnote update` |

参数不确定时读取对应命令的 `--help`，不要凭旧文档猜参数。

## 每条命令的结果与下一步

| 命令 | 成功后读取/确认 | 成功后怎么做 |
|---|---|---|
| `getnote auth login` | 浏览器已确认，凭证已写入本机 | 再运行 `doctor -o json`；不在聊天中展示凭证。 |
| `getnote auth status` | `Authenticated` / `Not authenticated` 或环境变量登录状态 | 未登录才启动 `auth login`；状态里只能出现掩码。 |
| `getnote auth logout` | `Logged out successfully.` | 只说明本机已退出；不声称已撤销服务端授权。 |
| `getnote doctor -o json` | `diagnostics_completed`、`ready`、`status`、`checks[]`、`issues[]`、`next_actions[]`、`integrations[]` | 退出码为 0 且 `ready=true` 才宣布核心连接可用；`status=degraded` 时继续处理警告。 |
| `getnote capabilities -o json` | `contract_version`、`commands`、`command_aliases`、`command_results`、`guarantees` | 只在安装、升级或兼容排查时读取；这是命令和结果字段的唯一事实源。 |
| `getnote setup -o json` | `success`、`targets[]`、`installed_skills`、`authenticated`、`next` | 仅同步本机 Agent 的领域 Skill；没有可识别目标不等于账号失败。 |
| `getnote quota -o json` | `data.read/write/write_note` 下的 `daily/monthly.limit/used/remaining/reset_at` | 按真实桶说明剩余额度，不自行换算或合并桶。 |
| `getnote version` | 版本文本 | 只用于展示版本；机器契约仍以 `capabilities -o json` 为准。 |
| `getnote update --check` | 当前/可用新版本文本 | 有新版本再运行 `getnote update`。 |
| `getnote update` | CLI 更新、五个领域 Skill 同步和 doctor 结果 | 命令会执行完整更新闭环；独立聚合 Skill 仍由宿主平台更新。 |

所有命令以退出码为第一判断：退出码非 0 即失败。使用 `-o json` 的 API 与本地错误均返回 `success=false`、`data=null`、`error.code/message/reason/retryable` 和可选 `request_id`；不能把 HTTP 200 或“命令运行过”当成成功。

## CLI 更新闭环

用户说“更新得到大脑”已经构成完整更新授权，不要求用户选择内部组件：

1. 执行 `getnote update --check`，随后执行 `getnote update`；默认流程会升级 CLI、同步五个领域 Skill 并运行 doctor。
2. 如果 CLI 明确要求由宿主或包管理器完成升级，使用平台声明的 `@getnote/cli` 安装流程，不下载或执行本地脚本。
3. 使用 ClawHub/OpenClaw 的宿主流程检查当前独立 Skill；需要用户确认时只提供唯一必要的确认动作。
4. 确认更新输出中的 CLI 版本、Skills 同步结果和 doctor 结果；再用最近笔记读取做验收。
5. CLI 不覆盖当前独立 Skill；独立 Skill 只由宿主平台更新。

## 安全与恢复

- 不展示或记录完整凭证；`auth status` 只能出现掩码。
- 用户未明确要求时不退出登录。
- 授权超时、拒绝或验证码过期时重新启动一次登录流程，不复用旧 code。
- 失败时保留执行步骤、错误原因和 `request_id`；不要只回复“连接失败”。
