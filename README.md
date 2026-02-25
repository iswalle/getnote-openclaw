# Get笔记 OpenClaw Skill

通过 Get笔记 Open API 管理笔记的 OpenClaw Skill。

## 🚀 快速开始

**在 OpenClaw 中说：**

> 帮我安装 Get笔记 skill，地址是 https://github.com/iswalle/getnote-openclaw

或者手动安装：

```bash
curl -sL https://raw.githubusercontent.com/iswalle/getnote-openclaw/main/install.sh | bash
```

## 🔑 配置 API Key

安装后，你需要提供 Get笔记 API Key 才能使用。API Key 格式为 `gk_live_xxx.xxx`。

**获取方式：**
1. 登录 Get笔记 APP
2. 进入设置 → 开发者选项
3. 创建 API Key

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 📝 创建笔记 | 支持纯文本、图片、链接笔记 |
| 📋 查询笔记 | 获取笔记列表和详情 |
| 🎙️ 录音笔记 | 获取 AI 总结和原始转写 |
| 🏷️ 标签管理 | 添加、删除笔记标签 |
| 🗑️ 删除笔记 | 删除指定笔记 |

## 💬 使用示例

```
「帮我查一下最近的笔记」
「创建一个笔记，标题是今日待办，内容是...」
「给笔记 xxx 添加标签：重要」
「删除笔记 xxx」
```

## 📖 API 文档

详见 [SKILL.md](./SKILL.md)

## 📦 版本

- **v1.1.0** (2026-02-25)
  - 更新 API 域名为 `openapi.biji.com`
  - 完善笔记列表/详情接口文档
  - 新增录音笔记原始转写字段说明

## 📜 许可证

MIT
