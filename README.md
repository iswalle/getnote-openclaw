# 得到大脑（Get笔记）Skill 2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

把得到大脑装进你常用的 AI。随时记录，需要时召回。

适用于 WorkBuddy、OpenClaw / QClaw 等支持 Skill 的 AI。安装后可以直接用自然语言保存、查询和整理笔记，不需要理解 API、MCP 或命令参数。

## ✨ 能做什么

| 能力 | 使用效果 |
|---|---|
| **📎 保存链接** | 发来网页、公众号、小红书、B 站等公开链接，等待内容处理完成后返回可打开的笔记链接 |
| **🖼 保存图片** | 上传本地图片，自动完成上传、OCR 与内容生成，完成后返回笔记链接 |
| **✍️ 保存文字和长内容** | 一句话、会议要点和长文都能保存；长内容不会因为命令行长度限制而被截断 |
| **🔍 查询与语义搜索** | 查看最近笔记，或按主题、关键词和自然语言找回相关内容 |
| **📚 整理知识库** | 管理普通知识库、书籍和客户档案，也能查询订阅知识库、博主内容和直播总结 |
| **🏷 管理标签** | 查看、添加和按真实标签 ID 删除标签 |
| **🎤 查看原文** | 按需读取链接原文、录音转写和笔记详情，不把摘要假装成原文 |
| **🔗 笔记内链与分享** | 用笔记内链串联内容；只有明确确认后才创建公开分享链接 |

### 完整能力范围

- **保存与维护**：保存文字、长文、链接和图片，查看异步任务，继续更新正文、标题和标签；
- **查找与阅读**：最近笔记、语义搜索、笔记详情、链接原文、录音转写、附件、时间线和快捷笔记；
- **知识整理**：默认、书籍、客户档案和团队知识库，目录创建/移动/删除，以及把笔记加入指定目录；
- **内容订阅**：订阅抖音博主，查看博主内容，也保留直播订阅与直播总结能力；
- **关系与协作**：父子笔记、笔记内链、私有链接和经用户确认后的公开分享；
- **可靠执行**：字符串雪花 ID、长文本安全输入、异步完成态、幂等重试、结构化错误和环境正确链接。

## 💡 常见使用场景

### 随手记录

> 👤 记一下：支付流程可以加一个进度提示，让用户等待时不焦虑。
>
> 🤖 已保存《支付流程优化想法》<br>
> https://www.biji.com/note/真实笔记ID

### 保存文章或图片

> 👤 帮我保存这个链接：https://example.com/article
>
> 🤖 正在抓取文章内容并生成笔记……<br>
> 已保存《文章标题》<br>
> https://www.biji.com/note/真实笔记ID

链接和图片需要异步处理。Skill 会等待 CLI 确认最终结果，不会在内容还没生成时提前说“保存成功”。

### 写周报时找回记录

> 👤 帮我找找这周记录过的客户反馈。
>
> 🤖 找到 5 条相关笔记，并返回每条笔记的标题和可打开链接。

### 整理到指定知识库

> 👤 把这篇笔记放进“客户档案”知识库。
>
> 🤖 先读取你实际拥有的知识库并确认目标，再使用真实 `topic_id` 执行，不会仅查询默认知识库或凭名称猜 ID。

### 整理到知识库文件夹

> 👤 在“产品研究”知识库里创建“竞品 / AI 助手”文件夹，把刚才那篇笔记放进去。
>
> 🤖 先确认知识库和现有目录，再创建缺少的目录并完成归档。团队知识库也遵循成员权限，不会绕过企业管理员设置。

### 读取录音、会议和链接原文

> 👤 把这条会议笔记的完整转写给我，再列出里面的附件和时间点。
>
> 🤖 分别调用转写、附件和时间线能力，返回真实结果；不会把 AI 摘要当作录音原文。

### 订阅抖音博主

> 👤 把这个抖音博主订阅到“行业观察”知识库：https://www.douyin.com/user/example
>
> 🤖 先确认目标知识库和写权限，再创建订阅。之后可以继续查询该博主的内容列表和详情。

## 📦 安装

### 方式一：直接让 AI 安装

在支持安装 Skill 的 AI 中发送：

> 请从 GitHub 仓库 https://github.com/iswalle/getnote-openclaw 安装得到大脑 Skill，安装完成后引导我登录并保存一条测试笔记。

WorkBuddy 也可以直接说：

> 帮我安装 SkillHub 中的 getnote，安装后引导我完成得到大脑授权。

### 方式二：从技能市场安装

在 ClawHub、SkillHub 或平台自己的技能市场中搜索“得到大脑”或 `getnote`。OpenClaw、QClaw、AutoClaw、Kimi Claw 等兼容生态优先使用平台提供的安装入口。

### 方式三：上传 Skill 安装包

如果平台支持上传 Skill 压缩包，可以从 GitHub 下载仓库压缩包后上传。Skill 会声明所需的 `@getnote/cli` 执行组件；平台允许自动安装依赖时会一并完成。

### 方式四：手动安装 CLI

适合使用 Codex、Claude Code、Cursor 或自动化脚本的用户：

```bash
npm install -g @getnote/cli@latest
getnote auth login
getnote doctor -o json
```

Skill 负责教会 AI 如何使用，CLI 负责真正执行。已经安装 CLI 的用户不需要再维护一份 API 实现。

## 🔑 首次授权与安装验收

首次使用时，AI 会运行 `getnote auth login` 并打开浏览器。请核对页面上的确认码后完成授权，不要在聊天中粘贴 API Key、Cookie 或 Authorization。

授权完成后可以说：

> 帮我保存一条测试笔记：得到大脑 Skill 2.0 安装完成。

只有同时满足以下条件，才算真正安装成功：

- CLI 连接与授权检查通过；
- 保存接口返回真实成功结果；
- 回复中包含真实标题、字符串笔记 ID 和可打开的 `note_url`；
- 测试环境和生产环境返回各自正确的笔记域名。

## 🧭 常用能力与 CLI 对照

普通用户直接说自然语言即可。下面的命令供需要排查或自动化的用户参考：

| 想做什么 | CLI 入口 |
|---|---|
| 保存文字、链接或图片 | `getnote save` |
| 查看最近笔记 | `getnote notes` |
| 查看笔记详情 | `getnote note` |
| 读取链接原文或文字原文 | `getnote note original` |
| 读取录音、会议或课堂转写 | `getnote note transcript` |
| 列出图片、音频和文件附件 | `getnote note attachments` |
| 读取录音或会议时间线 | `getnote note timeline` |
| 读取录音快捷笔记 | `getnote note quick-note` |
| 搜索笔记 | `getnote search` |
| 查看自有 / 订阅知识库 | `getnote kbs` / `getnote kbs-sub` |
| 管理知识库 | `getnote kb` |
| 管理知识库文件夹 | `getnote kb directories` / `directory-create` / `directory-update` / `directory-delete` |
| 订阅抖音博主 | `getnote kb blogger-follow` |
| 管理标签 | `getnote tag` |
| 查看配额 | `getnote quota` |
| 登录与诊断 | `getnote auth` / `getnote doctor` |
| 检查和升级 CLI | `getnote update --check` / `getnote update` |

具体参数始终以当前 CLI 的 `--help` 为准。例如：

```bash
getnote save --help
getnote note --help
getnote kb --help
```

## 🛠 支持的笔记与内容类型

| 类型 | 支持情况 |
|---|---|
| 纯文本 | ✅ 创建、读取、更新 |
| 普通网页链接 | ✅ 创建并等待抓取完成 |
| 得到大脑分享链接 | ✅ 直接保存 |
| 本地图片 | ✅ 上传并等待识别完成 |
| 录音、会议、课堂和录音卡笔记 | 📖 读取摘要与转写原文 |

创建时还支持：

- 保存到普通（DEFAULT）、书籍（BOOKSPACE）、客户档案（CUSTOMER）或团队（TEAMSPACE）知识库；
- 浏览和管理知识库文件夹，并在加入笔记时直接选择目标文件夹；
- 在知识库中订阅抖音博主，继续读取博主内容列表、摘要与原文；
- 直接读取笔记附件、录音/会议时间线和快捷笔记，不必让 AI 从完整详情中猜字段；
- 使用字符串父笔记 ID 创建子笔记；
- 使用幂等键避免网络重试造成重复笔记；
- 返回与当前环境一致的私有笔记链接。

## 🔐 隐私和安全

- 笔记 ID 全程作为字符串处理，避免 JavaScript 等环境出现精度损失；
- 群聊或共享会话中不主动展开私密笔记全文；
- 不向用户索要或展示 API Key、Cookie、Authorization 等完整凭证；
- 删除笔记、覆盖正文、替换全部标签、公开分享和批量移出知识库前必须确认；
- 默认返回仅本人可见的笔记链接，除非用户明确要求公开分享；
- API 返回失败时保留真实原因和 `request_id`，不会把 HTTP 200 错当成业务成功；
- 保存状态不确定时先核实，不自动重复创建笔记。

## 🚀 进阶用法：用笔记内链串联项目记录

你可以让 AI 先搜索相关笔记，再把真实笔记链接写进新笔记：

> 帮我创建今天的项目日志，并关联“支付流程方案”和“客户反馈”两条笔记。

正文中的私有内链格式为：

```text
https://www.biji.com/note/{note_id}
```

Skill 会使用 CLI 返回的环境正确链接，不会自行拼接 ID 或把私有内链误当成公开分享链接。

## 🔄 Skill 2.0 如何工作

新版采用“Skill 理解意图，CLI 确定执行”的结构：

- **独立 Skill**：识别自然语言意图、安排操作流程、处理确认和结果展示；
- **CLI 内置原子 Skills**：按认证、笔记、搜索、知识库和标签五个领域，为本地 Agent 提供同一套导航；
- **`@getnote/cli`**：统一负责授权、参数校验、长文本输入、图片上传、异步轮询、幂等、错误处理和结构化输出；
- **OpenAPI**：统一的数据、权限和配额底座。

命令事实只维护一份：CLI 的 `--help` 和 `getnote capabilities -o json`。Skill 不再复制整套 API 文档和参数表，从而避免不同平台上的说明长期漂移。

这不意味着 README 也要精简。`README.md` 面向人，保留产品能力、安装方式、使用示例、验收标准和排障信息；只有给 AI 每次加载的 `SKILL.md` 避免重复整套参数表。

## ⬆️ 更新

CLI 和 Skill 是两个独立版本：

```bash
getnote update --check
getnote update
```

- `getnote update` 只升级 CLI；
- Skill 通过当前平台的 SkillHub、ClawHub、GitHub 仓库或安装包更新；
- 升级后运行 `getnote doctor -o json` 检查授权和连接；
- 平台支持自动更新时可跟随技能市场更新；否则由 AI 在兼容检查发现版本过低后征得同意再升级。

## ❓ 常见问题

### 安装完成，为什么还不能读取笔记？

“Skill 已安装”和“得到大脑账号已授权”是两件事。首次使用仍需运行 `getnote auth login`，在浏览器核对确认码并授权。不要把 API Key 直接发到聊天里。

### 为什么保存链接或图片没有立刻返回？

链接需要抓取正文，图片需要上传、OCR 和内容生成。CLI 会持续查询任务最终状态；处理中只应该显示进度，拿到真实标题和 `note_url` 后才算完成。中途状态不确定时不会盲目重复保存。

### 为什么“原文”返回的内容不一样？

网页和文字笔记读取链接/正文原文；录音、会议和课堂笔记读取完整转写。Skill 会先判断笔记类型，不用摘要冒充原文。附件、时间线和快捷笔记也都有独立入口。

### 能使用团队知识库吗？

可以列出当前账号可访问的团队知识库，并按团队角色读取或维护目录、加入笔记。普通成员没有写权限时会明确失败，不会假装归档成功。

### Skill 与 CLI 应该更新哪一个？

- 自然语言理解、路由和安全提示变化：更新 Skill；
- 命令、接口、上传、轮询或错误处理变化：更新 CLI；
- 升级后运行 `getnote doctor -o json`，必要时再用 `getnote capabilities -o json` 核对契约。

### 遇到失败应该提供什么信息？

保留失败时间、执行的命令、错误原因和 `request_id` 即可。请先移除 API Key、Authorization、Cookie 等敏感内容，再提交问题；不要只提供一句“调用失败”。

## 🧑‍💻 项目结构与开发验收

- `SKILL.md`：给 AI 使用的精简运行时导航；
- `README.md`：给用户和开发者阅读的完整产品说明；
- `scripts/verify_cli_contract.py`：检查 Skill 引用的 CLI 命令和安全保证是否真实存在；
- `.github/workflows/validate.yml`：持续集成中的契约校验；
- `.clawhubignore`：控制最终发布包内容。

开发验证：

```bash
python3 /Users/walle/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python3 scripts/verify_cli_contract.py
getnote doctor -o json
```

Skill 2.0 以 CLI contract 2.0 为执行契约。发布前需要同时验证 CLI、Skill 和真实账号调用。

## 📜 相关链接

- [得到大脑官网](https://www.biji.com)
- [开放平台](https://www.biji.com/openapi)
- [GitHub 仓库](https://github.com/iswalle/getnote-openclaw)
- [ClawHub](https://clawhub.ai/iswalle/getnote)
- [开通会员](https://www.biji.com/checkout?product_alias=9Ab36BB3ZD&spm=openapi_skill)

## License

MIT · Published on [ClawHub](https://clawhub.ai)
