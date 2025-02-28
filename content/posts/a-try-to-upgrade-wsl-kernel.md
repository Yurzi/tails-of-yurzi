---
title: '记录一次升级WSL2内核的经历'
date: "2024-12-28T22:02:29+08:00"
lastmod: "2024-12-28T22:02:29+08:00"
author: ["Yurzi", "Lily"]
description: "升级 WSL2 的内核并修复 Docker Desktop 无法启动的问题"
keywords: 
  - WSL2
  - Linux Kernel
  - Docker Desktop
  - eBPF
tags:
  - Linux
  - WSL
  - Docker
  - eBPF
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

## 念起于鹅

总所周知，「鹅」（dae）{{<cref 1 "#cite-1">}}是一款基于 eBPF 的透明代理工具，
以其卓越的性能和灵活的配置而受到广泛关注。
而咱自然不能放弃这样尝鲜的机会，想着去折腾一下这玩意。

由于咱日常都在使用工位上的 Windows 计算机，其与鹅天生八字不合，
但是好在微软推出了 WSL2 这个有着 Linux 内核的子系统。
WSL2 有着自己的地址，同时咱记得有一种方法能让 WSL2 和主机获得同局域网的地址，
也就是说，可以让 WSL2 成为一个旁路由。
而鹅正好非常适合在有着 Linux 内核的旁路由上运行，这简直应该是天作之合。

但是理论存在，实践并不美好。其中首要的一个原因便是，
鹅所需要的 eBPF 内核模块在 WSL2 的原味内核中并不存在。
在咱撰写这篇文章时，WSL2 的原味内核版本为`5.15.167.4`，
它正好不支持 eBPF。

稍加咕噜咕噜一下之后，汝其实可以发现 WSL2 是搭载过 `6.6.y` 的内核的，
但出于一些原因回退到了现在的版本，
在 WSL2 内核的官方仓库{{<cref 2 "#cite-2">}}中可以看到新版内核的 Release。

所以说为了能养上鹅，咱们还得先整个新企鹅。

## 初试企鹅

### 编译

其实编译WSL内核的流程非常简单，
巨硬已经在 Readme 中写出了相关内容，
只要按照那个做就可以编译出一个可以在 WSL2 上启动的内核了。

不过由于咱偏好而且使用的是 ArchLinux on WSL2，所以有些许的不同，
故将流程记录如下：

1. 安装相关依赖

```sh
sudo pacman -Sy --need base-devel openssl libelf pahole python bc cpio
```

2. 克隆仓库并编译

```sh
git clone https://github.com/microsoft/WSL2-Linux-Kernel.git
cd WSL2-Linux-Kernel
make -j$(nproc) KCONFIG_CONFIG=Microsoft/config-wsl
```

内核编译后的产物位于 `arch/x86_64/boot` 下的 `bzImage`。只需要将的复制到 Windows 下就完成了。

### 安装

安装 WSL2 内核的方式非常的简单，根据巨硬的文档{{<cref 3 "#cite-3">}}，
只需要修改 `%USERPROFILE%\.wslconfig` 文件即可，在其中指定自己编译的内核路径即可。
例如下面这样：

```ini
[wsl2]
kernel=C:\\bzImage
```

在安装好后需要重启 WSL2 来让配置生效。

```powershell
wsl --shutdown
wsl

# 查看内核版本
uanme -a
```

## 鲸鱼的爆炸

当折腾完自定义内核之后，汝可能会发现 Docker Desktop 爆炸了。
根据 Github 上的 Issue{{<cref 4 "#cite-4">}}，
说是因为新的 `6.6.y` 版本的内核支持了内核模块的动态加载，
默认配置下的内核将很多模块移出了 builtin，
但是 WSL2 的自定义内核目前是不支持动态加载内核模块的，
于是 Docker Desktop 就此爆炸。

不过在这个 Issue 的中有一位人给出了一个 Workaround，
就是将那些被移除的模块重新内联。其中一位大佬给出了一份config{{<cref 6 "#cite-6">}}。

将这份配置稍加修改以满足当前系统和编译器的要求，同时遵循的这篇博客{{<cref 5 "#cite-5">}}开启 eBPF。
然后就可以重新编译新的内核并安装。
然后 Docker Desktop 就可以正常运作了。


## 结局

虽然内核的问题是解决了，但是要让 WSL2 作为旁路由运行鹅还需要进行网络设置。
但是当咱顺着回忆去寻找如何将桥接 WSL2 的时候发现，桥接模式的网络设置已经被废弃，
而新的镜像模式并不能做到让 Windows 的流量经过 WSL2 中 Linux 的网络栈。

所以说，这次试图在 Windows 上跑鹅的计划只能暂时搁置了。


## 参考文献

{{<cite 1 "[1] Github: daeuniverse/dae" "https://github.com/daeuniverse/dae">}}
{{<cite 2 "[2] Github: Microsoft/WSL2-Linux-Kernal" "https://github.com/microsoft/WSL2-Linux-Kernel">}}
{{<cite 3 "[3] Microsoft Learn: How to use the Microsoft Linux kernel v6 on Windows Subsystem for Linux version 2 (WSL2)" "https://learn.microsoft.com/en-us/community/content/wsl-user-msft-kernel-v6">}}
{{<cite 4 "[4] Github Issue: docker cannot start after installing linux-msft-wsl-6.6.y" "https://github.com/microsoft/WSL/issues/11742">}}
{{<cite 5 "[5] Massoud Asadi Blog: eBPF on WSL2 [kernel version 6.x] [ubuntu] [x64] [Arm64] [2024]" "https://massoudasadiblog.blogspot.com/2024/07/ebpf-on-wsl2-kernel-version-6x-ubuntu.html">}}
{{<cite 6 "[6]Github Gist: eapotapov/config-wsl" "https://gist.github.com/eapotapov/e64d8ce1d35064cf0dcd0dcd57577bdf">}}
