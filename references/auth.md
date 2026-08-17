
# 得到大脑连接、诊断与升级

负责把“用户想用得到大脑”推进到真正可执行的状态。不要只说“已安装”：CLI 可执行、账号已授权、API 可读三项都通过才算连接成功。

## 首次连接闭环

按顺序执行，已经满足的步骤直接跳过：

1. 用 `command -v getnote` 检查官方 CLI。缺失时停止任务并让平台使用 `SKILL.md` 中声明的 `@getnote/cli` 安装项；不要自行运行 npm、下载脚本或修改 Skill 文件。
2. 执行 `getnote version`，必须能够正常启动。
3. 执行 `getnote auth status`。未登录时运行 `getnote auth login`，让用户只在浏览器中确认，不索要 API Key、Cookie 或 Authorization。
4. 执行 `getnote doctor -o json`。只有 `success=true`，且 `checks` 中 `cli`、`auth`、`api` 均为 `ok=true`，才能宣布连接完成。
5. 独立 Skill 已携带领域参考，不运行 `getnote setup` 改写本机 Skill。只有用户明确要求为其他本机 Agent 同步 CLI 内置 Skill 时才执行该命令，并说明它会写入对应 Agent 的 Skill 目录。
6. 先用 `getnote notes --limit 1 -o json` 做无写入验收。只有用户同意创建测试内容时，才保存测试笔记。

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
| `getnote doctor -o json` | `success`、`cli_version`、`checks[].name/ok/message`、`platforms[]` | 只有 `cli`、`auth`、`api` 均为 `ok=true` 才宣布可用。 |
| `getnote capabilities -o json` | `contract_version`、`commands`、`command_aliases`、`command_results`、`guarantees` | 只在安装、升级或兼容排查时读取；这是命令和结果字段的唯一事实源。 |
| `getnote setup -o json` | `success`、`targets[]`、`installed_skills`、`authenticated`、`next` | 仅同步本机 Agent 的领域 Skill；没有可识别目标不等于账号失败。 |
| `getnote quota -o json` | `data.read/write/write_note` 下的 `daily/monthly.limit/used/remaining/reset_at` | 按真实桶说明剩余额度，不自行换算或合并桶。 |
| `getnote version` | 版本文本 | 只用于展示版本；机器契约仍以 `capabilities -o json` 为准。 |
| `getnote update --check` | 当前/可用新版本文本 | 有新版本再运行 `getnote update`。 |
| `getnote update` | 更新完成文本 | 必须再运行 `version` 和 `doctor -o json`，通过后才能说升级完成。 |

所有命令以退出码为第一判断：退出码非 0 即失败。使用 `-o json` 的 API 与本地错误均返回 `success=false`、`data=null`、`error.code/message/reason/retryable` 和可选 `request_id`；不能把 HTTP 200 或“命令运行过”当成成功。

## CLI 更新闭环

用户明确要求升级得到大脑 CLI 后执行：

1. 只有用户明确要求升级 CLI 时才执行 `getnote update --check`；有新版本时执行 `getnote update`。
2. 如果 CLI 明确要求由包管理器升级，停止并让用户通过平台声明的 `@getnote/cli` 安装项完成，不直接执行 npm。
3. 执行 `getnote version` 和 `getnote doctor -o json`。
4. 不运行 `getnote setup`，也不覆盖当前独立 Skill；Skill 更新由 ClawHub/OpenClaw 管理。
5. 用最近笔记读取做验收，再告诉用户版本、诊断结果和仍需动作。

## 安全与恢复

- 不展示或记录完整凭证；`auth status` 只能出现掩码。
- 用户未明确要求时不退出登录。
- 授权超时、拒绝或验证码过期时重新启动一次登录流程，不复用旧 code。
- 失败时保留执行步骤、错误原因和 `request_id`；不要只回复“连接失败”。
