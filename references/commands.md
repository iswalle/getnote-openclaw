# getnote CLI 稳定命令

调用前优先使用 `getnote <command> --help` 获取当前版本参数。下面只列跨平台 Skill 依赖的稳定入口。

| 用户意图 | 命令 |
|---|---|
| 检查连接 | `getnote doctor -o json` |
| 查看能力 | `getnote capabilities -o json` |
| 登录授权 | `getnote auth login` |
| 保存文字/链接/图片 | `getnote save "内容或路径" -o json` |
| 最近笔记 | `getnote notes --limit 20 -o json` |
| 笔记详情 | `getnote note "ID" -o json` |
| 搜索笔记 | `getnote search "查询" --limit 10 -o json` |
| 知识库列表 | `getnote kbs -o json` |

更新、删除、分享、标签和知识库写操作必须先读取对应 `--help`，并按风险要求向用户确认。
