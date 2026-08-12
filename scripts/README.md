# 开发校验脚本

这些脚本只服务于开发和持续集成，不会打进 ClawHub 或上传给用户的 Skill 安装包：

- `sync_cli_skills.py`：把 CLI 仓库的 5 个领域 Skill 同步到独立 Skill 包，并可用 `--check` 检查两者是否逐字一致；
- `verify_cli_contract.py`：读取 `getnote capabilities -o json`，验证 Skill 提到的命令、别名、安全承诺和结果契约都真实存在；
- `build_skill_package.py`：生成只含 `SKILL.md` 和 `skills/` 的 `dist/getnote-skill.zip`，供 GitHub Release 和“上传安装包”使用。

它们不是安装依赖，用户和 Agent 不需要手工运行。
