---
title: '在 Linux 上使用 Easyconnect'
date: "2025-02-16T17:09:38+08:00"
lastmod: "2025-02-16T17:09:38+08:00"
author: ["Yurzi"]
description: "介绍如何在 Linux 上使用 Easyconnect"
keywords:
  - Easyconnect
  - VPN
  - Network
  - Linux
tags:
  - Tools
  - Network
  - Linux
# series:
# math: true
# mermaid: true
draft: false
disableCounter: false
#cover:
#  image: ""
#  caption: ""
#  alt: ""
#  relative: false
---

## 宿命

在咱将自己工作用设备重装为 ArchLinux 之后，还没蹦跶没几天就遇到了远程连接部门内网的需求。
本来想着在远程开个 frp 之类的，但是想到其中的法律风险，还是作罢。

行吧，那就只能用部门自己的 VPN 服务——Easyconnect 了。
但总所周知，Easyconnect 是由「臭名昭著」的深信服开发的，
所以自然虽然其有提供 Linux 版本的 Easyconnect，
但因为其有着不为人知的特权后台守护进程，
咱自然是不敢使用的。

于是乎顺着将未知的东西隔离起来的思想，
在互联网上一番简单的搜索之后，
找到了 Docker Easyconnect 项目 {{<cref "1" "#cite-1">}}。于是将咱如何使用这个项目的经历记录如下。

## 使用 Docker 运行 Easyconnect

虽然 docker-easyconnect 有提供 cli 口味的 docker 镜像，
但是其适用的场景还是太窄了，
咱选择带有图形界面的版本。

为了方便使用，咱将其封装为一个脚本，方便使用。

```bash
#!/bin/bash

docker run --rm --device /dev/net/tun --cap-add NET_ADMIN -dti \
-e PASSWORD=vnc_passwd \
-e VPN_TUN=tun0 \
-e URLWIN=1 \
-v $HOME/.ecdata:/root \
-p 127.0.0.1:5901:5901 \
-p 127.0.0.1:1080:1080 \
-p 127.0.0.1:8888:8888 \
hagb/docker-easyconnect:7.6.3
```

咱目前部门的 Easyconnect 需要 SMS 验证码，
所以咱还需要使用 VNC Client 连接到容器内的 Easyconnect 界面，输入验证码，这里咱使用 krdc 作为 Client，连接到5901端口。

成功登录之后，在浏览器里设置对应的 Http 代理和 Socks5 代理就可以正常使用浏览器访问内网了。

## References

{{<cite 1 "[1]: Github: docker-easyconnect/docker-easyconnect" "https://github.com/docker-easyconnect/docker-easyconnect">}}
