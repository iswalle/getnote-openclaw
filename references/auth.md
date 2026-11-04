
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
| 查看开放平台调用额度 | `getnote quota -o json` |
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
| `getnote capabilities -o json` | `contract_version`、`commands`、`command_aliases`、`command_results`、`guarantees` | 只在安装、升级或兼容排查时读取；这是命令和结果字段的唯一事实源。限流恢复还要核对 `guarantees.same_identity_request_queue/safe_not_started_retries/upload_operation_recovery`，并读取服务当前 runtime；不能只凭版本推定已启用。 |
| `getnote setup -o json` | `success`、`targets[]`、`installed_skills`、`authenticated`、`next` | 仅同步本机 Agent 的领域 Skill；没有可识别目标不等于账号失败。 |
| `getnote quota -o json` | `data.read/write/write_note` 下的 `daily/monthly.limit/used/remaining/reset_at` 及可选实时速率策略 | 按真实桶、作用域和速率说明额度，不自行换算、合并桶或假定固定频率。 |
| `getnote version` | 版本文本 | 只用于展示版本；机器契约仍以 `capabilities -o json` 为准。 |
| `getnote update --check` | 当前/可用新版本文本 | 有新版本再运行 `getnote update`。 |
| `getnote update` | CLI 更新、五个领域 Skill 同步和 doctor 结果 | 命令会执行完整更新闭环；独立聚合 Skill 仍由宿主平台更新。 |

所有命令以退出码为第一判断：退出码非 0 即失败。使用 `-o json` 的 API 与本地错误均返回 `success=false`、`error.code/message/reason/retryable` 和可选 `request_id`；`data` 通常为空，但恢复失败可携带 `upload_recovery` 或 `uploaded_image`，必须保留并按笔记/文件流程续接；不能把 HTTP 200 或“命令运行过”当成成功。

## CLI 更新闭环

用户说“更新得到大脑”已经构成完整更新授权，不要求用户选择内部组件：

1. 执行 `getnote update --check`，随后执行 `getnote update`；默认流程会升级 CLI、同步五个领域 Skill 并运行 doctor。
2. 如果 CLI 明确要求由宿主或包管理器完成升级，使用平台声明的 `@getnote/cli` 安装流程，不下载或执行本地脚本。
3. 使用 ClawHub/OpenClaw 的宿主流程检查当前独立 Skill；需要用户确认时只提供唯一必要的确认动作。
4. 确认更新输出中的 CLI 版本、Skills 同步结果和 doctor 结果；再用最近笔记读取做验收。
5. CLI 不覆盖当前独立 Skill；独立 Skill 只由宿主平台更新。

## 限流与同一操作恢复

调用额度、上传对象日/滚动额度、OSS 字节上传、异步笔记或文件处理是不同阶段，分别核对结果。同一账号在普通 API、渠道和云 MCP 间共享用户预算；企业委托还可能按客户端在不同授权和用户间共享预算。按实时 quota/runtime 的 `scope_type/scope_id`、`algorithm`、`sustained_rate_per_second/burst` 判断，不硬编码 1 QPS，也不靠换 token 或授权绕过。

客户端只协调进程内的同一身份请求，不能协调其它 CLI 进程、工具或 MCP 副本；Agent 要把仍共享预算的任务排队，避免并发放大。客户端已对明确安全的未执行请求做最多额外 2 次、累计等待不超过 5 秒的重试；Agent 不在外层再套重试循环或启动并行补偿。

失败读取 `error.code/message/reason/retryable`、`request_id` 和完整 `error.rate_limit_detail`（MCP 错误中的同名字段）。保留 `dimension/bucket/algorithm/scope_type/scope_id`、速率/突发、`limit/remaining/reset_at`、`retry_after_ms/retry_after_seconds`、`request_execution/retry_action`，按以下决策行动：

| 真实返回 | 下一步 |
|---|---|
| QPS 拒绝（10202）、`retryable=true`、`request_execution=not_started` 且 `retry_action=retry_same_operation` | 当前步骤未执行。客户端在上述预算内复用原参数、`client_request_id` / 幂等键及已上传对象；写操作也不能一概判为不可重试。客户端已返回最终失败时按建议等待并报告，停止本轮自动重试，不另开 CLI/MCP 重跑整条上传流程。 |
| 日/月额度，`pause_until_reset` | 停止短周期重试，说明真实桶和 `reset_at`；到重置后再继续。 |
| 上传滚动额度，`complete_existing` | 停止申请新凭证，优先核对并完成已有对象/任务；不重传字节。 |
| 零限额，`contact_admin` | 停止调用并联系管理员；等待一秒或换授权无效。 |
| 配置或状态不可用，503 / `pause` | 暂停，保留原操作标识和 `request_id`，待服务恢复后先核对原结果。 |
| 只有 `retryable=true`，缺少安全未执行证据，或写入结果未知 | 先查询原任务/既有结果，不能据此重复创建。 |

向用户用大白话说明“等多久”“暂时停止”“复用哪一步”和真实 `request_id`。不展示 API Key、token、签名、签名 URL 或上传对象私有地址。

## 安全与恢复

- 不展示或记录完整凭证；`auth status` 只能出现掩码。
- 用户未明确要求时不退出登录。
- 授权超时、拒绝或验证码过期时重新启动一次登录流程，不复用旧 code。
- 失败时保留执行步骤、错误原因和 `request_id`；不要只回复“连接失败”。
