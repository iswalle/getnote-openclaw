# Get笔记 OpenClaw Skill

> 通过自然语言管理你的 [Get笔记](https://biji.com) 笔记和知识库。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🧠 项目介绍

**Get笔记 OpenClaw Skill** 是一个为 [OpenClaw](https://openclaw.com) AI 助手设计的 Skill 插件，接入 Get笔记 Open API，让你可以直接用自然语言：

- 📝 查询、创建、编辑笔记
- 🔖 管理标签
- 📚 创建和管理知识库
- 🎙️ 读取 AI 会议总结和语音转写

> 💡 说人话就能记笔记，比打开 App 快多了。

> 🔑 **获取 API Key**：https://www.biji.com/openapi

---

## 📦 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install getnote
```

### 方式二：在 OpenClaw 中安装

直接告诉你的 AI 助手：

> 帮我安装 Get笔记 skill，地址是 https://github.com/iswalle/getnote-openclaw

### 方式三：手动安装

```bash
# 进入 OpenClaw Skill 目录
mkdir -p ~/.openclaw/workspace/skills/getnote
cd ~/.openclaw/workspace/skills/getnote

# 下载 Skill 文件
curl -sL https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/SKILL.md -o SKILL.md
curl -sL https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/package.json -o package.json
```

---

## 🔑 配置 API Key

安装后，还需要配置 Get笔记 API Key 才能使用。

### 获取 API Key 和 Client ID

1. 访问 **https://www.biji.com/openapi**
2. 登录后创建 API Key
3. 复制 API Key（格式：`gk_live_xxx`）和 Client ID（格式：`cli_xxx`）

### 配置到环境变量（推荐）

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export GETNOTE_API_KEY=gk_live_xxx
export GETNOTE_CLIENT_ID=cli_xxx
```

> ⚠️ **安全提示**：不要在群聊中发送 API Key。建议使用环境变量配置，避免密钥泄露。

---

## 🚀 快速开始

安装并配置好 API Key 后，直接开说：

```
# 查笔记
「帮我查一下最近的笔记」
「显示最近 5 条笔记」

# 创建笔记
「创建一个笔记，标题是今日待办，内容是买菜、开会、写报告」
「保存这个链接到笔记：https://example.com/article」

# 标签管理
「给上一条笔记加上「工作」标签」
「删除笔记 xxx 的「临时」标签」

# 知识库
「看看我的知识库列表」
「创建一个知识库叫"读书笔记"」
「把这条笔记加到「工作」知识库」
```

---

## 🔐 Scope 权限说明

安装 Skill 时，AI 助手会申请以下权限：

| Scope | 说明 | 用途 |
|-------|------|------|
| `notes:read` | 读取笔记 | 查询笔记列表和详情 |
| `notes:write` | 写入笔记 | 创建和编辑笔记 |
| `notes:tags` | 管理标签 | 添加/删除笔记标签 |
| `knowledge:read` | 读取知识库 | 查询知识库列表和内容 |
| `knowledge:write` | 写入知识库 | 创建知识库、管理笔记归属 |

> ⚠️ API Key 本身具有你账号的完整权限，请妥善保管，不要分享给他人。

---

## ⚠️ 使用限制

| 限制项 | 说明 |
|--------|------|
| 每日知识库创建上限 | 每个账号每天最多创建 **50 个知识库** |
| 重置时间 | 按 **北京时间 (Asia/Shanghai)**自然日 00:00 重置 |

---

## 🛠 支持的笔记类型

| 类型 | 说明 | 写入支持 |
|------|------|----------|
| `plain_text` | 纯文本笔记 | ✅ 支持读写 |
| `link` | 链接笔记（自动抓取正文） | ✅ 支持读写 |
| `img_text` | 图片笔记 | ✅ 支持创建（需先上传图片获取 URL） |
| `meeting` | 会议笔记（含 AI 摘要） | ⚠️ 仅支持读取 |
| `recorder_audio` | 录音笔记 | ⚠️ 仅支持读取 |

> 📖 完整 API 文档（含接口列表、参数、响应示例）见 [SKILL.md](./SKILL.md)

---

## 📜 许可证

MIT © [Get笔记](https://biji.com)
