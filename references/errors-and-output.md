# 结构化输出、错误与重试

## 成功判断

- 机器调用统一使用 `-o json`；
- 退出码为 0 且结构化结果明确成功，才算成功；
- 保存链接或图片时，必须等 CLI 完成异步轮询；
- 最终没有 `note_url` 时不要自行拼接。

## 错误字段

CLI 会尽量保留：

- `code` / `message` / `reason`；
- `retryable`；
- `field` / `constraint` / `expected_type`；
- `request_id`。

向用户说明可理解的原因和下一步，同时保留 `request_id` 供排查。不要输出 API Key、Authorization、Cookie 或完整凭证。

## 重试

- 仅当 `retryable=true` 或命令明确提示可重试时自动重试；
- 创建笔记重试必须复用原 `--idempotency-key`；
- 网络中断且无法确认是否写入时，先用 `notes` 或任务状态核实，不能直接重新创建；
- 参数错误先按 `field`、`constraint`、`expected_type` 修正，禁止原样重试；
- 未授权时运行 `getnote auth login`，授权成功后再重试原命令；
- 配额或会员限制按 CLI 返回的购买/恢复提示交给用户决定。
