# 微信聊天记录清理 for macOS

> 正在开发中……

## 功能

- 根据日期清理旧的聊天图片、文件等
- 用户指定的部分好友可以采取不同的清理策略

## 使用

> 现阶段本程序没有图形界面

### 环境需求

Python >= 3.6

### 运行

```shell
$ python3 main.py
Ready to clean up?(y/[n])
```

在输入回答前，会弹出一个访达（Finder）目录，其中列出了待清理的目录的软链接，用户如不想删除其中的部分目录，只需要删除该软链接。

最后在命令行中输入 `y`，本程序会根据剩下的软链接把相应文件放入废纸篓。

## 主要问题

1. 微信不同用户的目录是 MD5 码，难以反向得知每个目录对应了哪位好友，目前需要用户手动关联好友与 MD5 码。希望能找到更好的方式。

2. 目前借助访达和软链接来做交互，有图形界面会更好。