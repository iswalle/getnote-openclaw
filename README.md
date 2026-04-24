# Get笔记 Skill

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)

让 AI 成为你的第二大脑。随时记录，需要时召回。

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| **📎 一键保存链接** | 发个链接就能保存，自动抓取原文、生成摘要。支持小宇宙播客、小红书、微信公众号、B站、抖音及任意公开网页 |
| **🖼 图片秒变笔记** | 发张图片自动 OCR 识别文字、AI 分析图片内容 |
| **🔍 语义搜索** | 不用翻全部笔记，直接搜关键词，AI 语义召回相关内容 |
| **📚 知识库管理** | 用知识库和标签整理笔记，还能订阅博主、获取直播总结 |
| **🎤 语音笔记原文** | 录音笔记支持获取完整转写文本 |
| **🔗 笔记内链** | 在笔记正文里引用另一条笔记，用 `biji.com/note/{id}` 格式互相串联 |
| **📤 生成分享链接** | 任意笔记一键生成公开链接，发给别人直接查看 |

---

## 💡 使用场景

### ✏️ 随手记录

**通勤路上想到一个点子**

> 👤 记一下笔记：支付流程可以加一个进度条，用户等待时不焦虑
>
> 🤖 已记录，自动打上「产品优化」标签。

**听播客时有感触**

> 👤 刚听到一个观点挺好的，记一下：好的产品是让用户少做选择，不是多做选择
>
> 🤖 已记录。

**开完会**

> 👤 帮我记下刚才会上定的几件事：1. 下周三前完成设计稿 2. 找小王对接接口 3. 周五前给老板汇报进度
>
> 🤖 已记录。

---

### 🔍 要用时召回

**写周报时**

> 👤 帮我找找这周我记过的工作相关的东西
>
> 🤖 找到 5 条相关笔记：周一你记了客户反馈的问题、周三记了技术方案讨论、周四......

**被领导问到**

> 👤 上次我们讨论过用户分层的事，当时怎么说的来着？
>
> 🤖 11月8号你记过：高价值用户定义为月消费超过500元，占比约12%......

**写文章找素材**

> 👤 我想写篇关于做产品的文章，帮我找找我之前的相关想法
>
> 🤖 找到 8 条相关笔记，已按时间排序整理给你。

---

### 🔗 保存链接和图片

**看到好文章**

> 👤 存到笔记 https://example.com/article
>
> 🤖 链接已提交，正在抓取分析中...
> 🤖 搞定 ✓ 已保存：《如何做好产品设计》

**拍到有用的东西**

> 👤 [发送图片]
>
> 🤖 存到笔记？
>
> 👤 对
>
> 🤖 搞定 ✓ 图片已保存。

**探店记录**

> 👤 记一下，这家店叫船歌鱼水饺，招牌是鲅鱼饺子，人均80
>
> 🤖 已记录，打上「美食」标签。

---

## 📦 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install getnote
```

### 方式二：让 AI 助手安装

> 帮我安装 Get笔记 skill，地址是 https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/SKILL.md

### 方式三：手动安装

```bash
mkdir -p ~/.openclaw/workspace/skills/getnote
cd ~/.openclaw/workspace/skills/getnote
curl -sL https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/SKILL.md -o SKILL.md
curl -sL https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/package.json -o package.json
```

---

## 🔑 配置

### 自动配置（默认）

安装后首次使用时，AI 会自动发起 OAuth 授权：

1. 你说「存到笔记」或任何笔记相关操作
2. AI 检测到未配置，自动生成授权链接
3. 点击链接，授权
4. 自动配置完成，继续执行你的请求

无需手动配置，无需记忆任何命令。

### 手动配置（可选）

1. 前往 **[Get笔记开放平台](https://www.biji.com/openapi)** 获取 API Key 和 Client ID
2. 在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "getnote": {
        "apiKey": "gk_live_xxx",
        "env": {
          "GETNOTE_CLIENT_ID": "cli_xxx",
          "GETNOTE_OWNER_ID": "ou_xxx"
        }
      }
    }
  }
}
```

> 💡 `GETNOTE_OWNER_ID` 可选，配置后只有你能操作笔记（群聊安全）

> 💡 需要 [Get笔记会员](https://www.biji.com/checkout?product_alias=6AydVpYeKl) 才能使用 API

---

## 🔐 安全说明

> ⚠️ **隐私保护**：笔记是你的私密数据，AI 会严格校验身份。

- 配置 `GETNOTE_OWNER_ID` 后，只有你能操作笔记
- 群聊中其他人无法通过 AI 读取你的笔记
- **不要在聊天中发送 API Key**，请手动配置到环境变量

---

## 🛠 支持的笔记类型

| 类型 | 说明 | 支持 |
|------|------|------|
| `plain_text` | 纯文本笔记 | ✅ 读写 |
| `link` | 链接笔记（自动抓取正文） | ✅ 读写 |
| `img_text` | 图片笔记 | ✅ 读写 |
| `audio` | 即时录音 | 📖 仅读取 |
| `meeting` | 会议录音 | 📖 仅读取 |
| `local_audio` | 本地音频 | 📖 仅读取 |
| `internal_record` | 内录音频 | 📖 仅读取 |
| `class_audio` | 课堂录音 | 📖 仅读取 |
| `recorder_audio` | 录音卡长录 | 📖 仅读取 |
| `recorder_flash_audio` | 录音卡闪念 | 📖 仅读取 |

> 💡 语音类笔记可读取 AI 摘要和转写原文，需调用详情接口获取。

---

## 🚀 进阶用法：用笔记内链实践柳比歇夫时间日志法

柳比歇夫时间日志法的核心是**每天记录自己把时间花在了哪里**，事后统计、复盘、改进。

结合 Get笔记内链，AI 可以帮你自动串联：

**每天早上**

> 👤 帮我记一条今日工作日志，内链到「产品设计方案」和「客户反馈」这两条笔记
>
> 🤖 已记录「2026-04-24 工作日志」，正文已插入两条内链。

**每周复盘**

> 👤 找找我这周的工作日志，整理一下时间分配
>
> 🤖 找到 5 条日志，你这周：产品设计 12h、客户沟通 6h、开会 4h……

**内链格式**：在笔记正文里用 `https://biji.com/note/{note_id}` 引用其他笔记。示例：

```
参考上次的讨论：https://biji.com/note/1234567890000000001
```

告诉 AI 要内链到哪条笔记，AI 会自动获取对应 note_id 插入。

---

## 🆕 更新日志

| 日期 | 版本 | 新能力 | 适合怎么用 |
|------|------|--------|------------|
| 2026-04-23 | **v1.8.0** | 1. 笔记内链<br>2. 保存分享链接自动变笔记 | 1. 用内链串联每天的工作日志和项目笔记，实践时间日志法<br>2. 收到别人发来的分享链接直接存入笔记 |
| 2026-04-16 | **v1.7.0** | 1. 生成笔记分享链接<br>2. 知识库订阅得到直播 | 1. 把笔记一键分享给朋友<br>2. 在知识库里订阅得到直播课，直播结束后 AI 摘要自动入库 |
| 2026-03-26 | **v1.5.6** | 获取我订阅的知识库，支持语义搜索 | 开通了某个知识库，可以直接问 AI：「在我订阅的 XXX 知识库里搜一下时间管理」 |
| 2026-03-12 | **v1.2.0** | 查看订阅博主内容、直播摘要和转写原文 | 把别人的知识变成自己可检索的笔记库 |

---

## 📜 相关链接

- [Get笔记官网](https://biji.com)
- [开放平台](https://www.biji.com/openapi)
- [ClawHub](https://clawhub.ai/iswalle/getnote)
- [开通会员](https://www.biji.com/checkout?product_alias=6AydVpYeKl)

---

## License

MIT-0 (MIT No Attribution) · Published on [ClawHub](https://clawhub.ai)
