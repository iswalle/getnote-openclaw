# Get笔记 OpenClaw Skill

通过 Get笔记 Open API 管理笔记和知识库的 OpenClaw Skill。

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

### 📝 笔记管理
- **创建笔记** - 支持纯文本、链接、图片笔记
- **查询笔记** - 获取笔记列表、详情、搜索
- **编辑笔记** - 更新笔记标题和内容
- **标签管理** - 给笔记添加、删除标签

### 📚 知识库
- **创建知识库** - 按主题组织你的笔记
- **管理知识库** - 添加/移除笔记到知识库
- **浏览知识库** - 查看知识库内的所有笔记

### 🎙️ 录音笔记
- 获取 AI 生成的会议总结
- 查看完整的语音转写内容
- 支持多说话人识别

## 💬 使用示例

```
「帮我查一下最近的笔记」
「创建一个笔记，标题是今日待办，内容是...」
「保存这个链接到笔记：https://example.com/article」
「给笔记 xxx 添加标签：重要」
「创建一个知识库叫"读书笔记"」
「把这几条笔记加到"工作"知识库里」
「看看我的知识库列表」
```

## 📖 API 文档

详见 [SKILL.md](./SKILL.md)

## 📜 许可证

[MIT](./LICENSE) - 可自由使用、修改、分发，需保留版权声明。
