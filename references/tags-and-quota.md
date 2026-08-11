# 标签与配额

## 查看标签

```bash
getnote tag list "笔记ID" -o json
```

返回标签 ID、名称与类型。删除标签必须使用标签 ID。

## 添加标签

```bash
getnote tag add "笔记ID" "标签名" -o json
```

## 删除标签

先查看标签，再按 ID 删除：

```bash
getnote tag list "笔记ID" -o json
getnote tag remove "笔记ID" "标签ID" -o json
```

系统标签不能删除。不要把标签名传给 `tag remove`。

## 查看配额

```bash
getnote quota -o json
```

按 CLI 返回展示读、写和保存笔记等配额的已用、剩余与重置时间。不要自行合并或推算服务端未返回的额度。
