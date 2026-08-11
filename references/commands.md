# getnote CLI 命令索引

当前 Skill 依赖 CLI contract `2.0`。先运行：

```bash
getnote capabilities -o json
```

任何命令的当前参数以 `getnote <command> --help` 为准。

## 连接、安装与版本

| 意图 | 命令 |
|---|---|
| 检查本机、授权和 API | `getnote doctor -o json` |
| 只做离线环境检查 | `getnote doctor --offline -o json` |
| 查看稳定能力契约 | `getnote capabilities -o json` |
| 登录 | `getnote auth login` |
| 查看登录状态 | `getnote auth status` |
| 退出登录 | `getnote auth logout` |
| 为本机 AI 安装原子 Skills | `getnote setup` |
| 查看版本 | `getnote version` |
| 检查更新 | `getnote update --check` |
| 升级 CLI | `getnote update` |

## 笔记

| 意图 | 命令 |
|---|---|
| 保存文字、链接或本地图片 | `getnote save "内容或路径" -o json` |
| 从文件保存长文本 | `getnote save --content-file ./note.md -o json` |
| 从标准输入保存长文本 | `getnote save --stdin -o json` |
| 查询异步任务 | `getnote task "任务ID" -o json` |
| 最近笔记 | `getnote notes --limit 20 -o json` |
| 下一页 | `getnote notes --cursor "游标" -o json` |
| 笔记详情 | `getnote note "笔记ID" -o json` |
| 提取单个字段 | `getnote note "笔记ID" --field content` |
| 修改笔记 | `getnote note update "笔记ID" ... -o json` |
| 删除笔记 | `getnote note delete "笔记ID" --yes -o json` |
| 创建公开分享 | `getnote note share "笔记ID" -o json` |

## 搜索

| 意图 | 命令 |
|---|---|
| 全局语义搜索 | `getnote search "查询" --limit 10 -o json` |
| 在知识库中搜索 | `getnote search "查询" --kb "知识库ID" --limit 10 -o json` |

## 知识库

| 意图 | 命令 |
|---|---|
| 自有知识库列表 | `getnote kbs -o json` |
| 订阅知识库列表 | `getnote kbs-sub -o json` |
| 知识库内笔记 | `getnote kb "知识库ID" -o json` |
| 新建知识库 | `getnote kb create "名称" --desc "描述" -o json` |
| 加入笔记 | `getnote kb add "知识库ID" "笔记ID" -o json` |
| 移出笔记 | `getnote kb remove "知识库ID" "笔记ID" -o json` |
| 订阅博主 | `getnote kb bloggers "知识库ID" -o json` |
| 博主内容列表 | `getnote kb blogger-contents "知识库ID" "follow_id" -o json` |
| 博主内容详情 | `getnote kb blogger-content "知识库ID" "post_id" -o json` |
| 已完成直播 | `getnote kb lives "知识库ID" -o json` |
| 直播详情 | `getnote kb live "知识库ID" "live_id" -o json` |
| 订阅得到直播 | `getnote kb live-follow "知识库ID" "直播链接" -o json` |

## 标签和配额

| 意图 | 命令 |
|---|---|
| 查看笔记标签 | `getnote tag list "笔记ID" -o json` |
| 添加标签 | `getnote tag add "笔记ID" "标签名" -o json` |
| 按标签 ID 删除 | `getnote tag remove "笔记ID" "标签ID" -o json` |
| 查看 API 配额 | `getnote quota -o json` |
