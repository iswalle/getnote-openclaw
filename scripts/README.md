# 开发脚本与运行时安装器

- `install.sh`：**随独立 Skill 安装包一起发布**。Agent 在首次使用时执行 `bash scripts/install.sh --ensure`；用户要求升级时执行 `bash scripts/install.sh --update`。它负责确保官方 CLI 存在、升级 CLI，并在有新发布包时刷新当前 Skill 文件。
- `sync_cli_skills.py`：开发时把 CLI 仓库的 5 个领域 Skill 同步到独立 Skill 包，并可用 `--check` 检查两者是否逐字一致。不会发布到安装包。
- `verify_cli_contract.py`：开发时读取 `getnote capabilities -o json`，验证 Skill 提到的命令、别名、安全承诺和结果契约都真实存在。不会发布到安装包。
- `build_skill_package.py`：生成 `dist/getnote-skill.zip`，供 GitHub Release 和“上传安装包”使用；发布内容为主 Skill、五个领域 Skill 与 `scripts/install.sh`。

最终包不包含 Python 开发脚本、GitHub 工作流或 README；它们不会进入 ClawHub/SkillHub 的最终内容。`install.sh` 是唯一需要随包运行的脚本。
