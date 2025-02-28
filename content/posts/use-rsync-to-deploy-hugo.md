---
title: "使用Rsync来发布Hugo博客"
date: "2024-03-28T16:53:00+08:00"
lastmod: "2024-03-28T16:53:00+08:00"
author: ["Yurzi", "Lily"]
description: "使用Rsync将博客自动发布到远程服务器"
keywords:
  - Rsync
  - Hugo
  - Deploy
tags:
  - Hugo
  - Linux
# series:
# math: true
# mermaid: true
draft: false
#cover:
#  image: ""
#  caption: ""
#  alt: ""
#  relative: false
---

经历了一番大折腾之后，咱终于成功的将博客从 Typecho 迁移到了 Hugo，但是受限于 Hugo 静态博客的特性，咱无法实时编辑博客哩:triumph:，
于是只能探索一下如何能快捷的将博客同步到服务器上去了，不过好在 Hugo 的文档给出了一些方案{{<cref 1 "#cite-1">}}。
在简单浏览之后决定选择使用 `rsync` 的方式。

## 简单用法

虽然在很早之前就了解到了 `rsync` 但是并没有实际的用过，在简单查阅了ArchWiki{{<cref 2 "#cite-2">}}上相关的内容之后，并结合 `rsync` 自己的 help 输出之后
咱总结出只需要在 Hugo 的工作目录使用下面的命令就能将内容上传到远程了。

```sh
rsync -avuz --progress --delete public/ <username>@<retmote_host>:</target/path>
```

这句命令中的参数 `-a` 表示归档的方式来传输文件，这等同于 `-rlptgoD`，这意味着它会递归的把文件复制到远程，同时保留文件的元信息，包括所属、权限、链接等信息;
而 `-u` 表示仅更新，用于增量传输；`-v` 表示输出详细信息，`-z` 表示压缩，`--progress` 表示显示过程。
最关键的是 `--delete` 会将远程与本地不符的文件删除。

不过这样上传的文件会导致其文件所属为本地的用户，即使使用 `--no-og` 也会导致远程的文件所属变为SSH登陆的用户，而咱的 Nginx 运行在 http 用户下，
从而导致权限问题。

在经过一番研究之后，发现使用 `rsyncd` 配置中的 `module` 可以解决指定远程文件所属的需求，这也就是本文的重点啦´ ▽ \` )ﾉ`

## 使用 rsyncd

### 配置 rsyncd

首先是在远程服务器上安装好 `rsync`，绝大多数Linux发行版都会提供这个包。然后编辑配置文件 `/etc/rsyncd.conf`,

```conf
uid = root # 使用root运行rsyncd来使其能正确处理权限
gid = root
use chroot = yes # 使用chroot防止路径逃逸保证安全
max connections = 4
syslog facility = local5
pid file = /run/rsyncd.pid

[blog] # 设置模块名为 blog
path = /srv/http/your_path # 博客所在的位置
comment = Blog directory # 注释
uid = http # 要求上传后文件的所属
gid = http
read only = false # 关闭只读，使其可写
auth users = your_username # 认证用的用户名
secrets file = /etc/rsyncd.secrets # 认证用的用户名和密码
```

值得注意的是，这里设置的 `auth users` 并不是 Linux 用户，所以可以随便指定，主要是定义在 `/etc/rsyncd.secrets` 中的。

接下来在 `/etc/rsyncd.secrets` 中按照以下格式写入你的用户名和密码，
(可以把这个文件创建在任何你觉得合适的地方)

```
# /etc/rsyncd.secrets

your_username:your_passwd
```

并设置为只有 `rsyncd` 运行用户可读写的权限，这里是 `root` 用户。

```sh
chmod 600 /etc/rsyncd.secrets
```

最后，别忘了启动 `rsyncd`，以及在防火墙上开放 TCP 873 端口，`rsyncd` 默认监听在这个端口，
如果需要调整可以在 `/etc/rsyncd.conf` 里添加 `port <prefer_port>` 来设置

```sh
systemctl enable --now rsyncd
```

### 使用 rsync 上传

由于使用了 rsyncd，所以上传用的指令也发生了变化

```sh
rsync -avuz --progress --password-file=<your_passwd_file> --delete public/ <auth_username>@<remote_host>::<module_name/inner_path>
```

这里的 `--password-file` 指向本地存储密码的文件，注意其权限也需要只有当前用户可读写，
然后是后面的远程路径使用了双冒号来指定使用 `rsync` 协议，冒号后跟的是设置的模块名和模块内路径了。

## 总结

至此，就能方便的使用 rsync 将生成好的博客网站快速的同步到远程服务器，如果觉的命令太长，可以写个shell脚本来方便使用。

## 参考文献

{{<cite 1 "[1] Hugo: Hosting and deployment" "https://gohugo.io/hosting-and-deployment/">}}
{{<cite 2 "[2] ArchWiki: rsync" "https://wiki.archlinux.org/title/Rsync">}}
