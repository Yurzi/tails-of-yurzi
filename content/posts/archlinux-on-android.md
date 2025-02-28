---
title: "在安卓上跑一个Archlinux ARM"
date: "2024-01-01T23:42:05+08:00"
lastmod: "2024-03-27T23:42:05+08:00"
author: ["Yurzi", "Lily"]
description: "在安卓机子上运行一个完整的ArchLinux！"
keywords:
  - Linux
  - Android
  - ArchLinux
tags:
  - Android
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

## 始

终于在经历了漫长的等等之后，还是将手上的已经是伊拉克成色的手机换掉了。考虑到其虽然屏幕裂开了，但其仍然具有算力资源可以榨取，所以就琢磨着如何将其利用起来。

在将其空置了一个多月之后，突然想起之前折腾过 Termux 的经历，以及使用 chroot 的经验，于是决定在这个手机上 chroot 一个 Linux 发行版了。至于为什么是 Archlinux ARM，自然是由于咱的个人喜好了。

## 准备

首先，由于要使用 chroot，所以肯定是需要先将手机 root 的。然后是检查是否可以正常使用 mount 和 chroot 指令，如果不能正常使用的话，可能需要检查下权限，或者考虑整个 busybox 套件塞进去。

然后，是去 Archlinux ARM 的官网/镜像站，下载合适版本的系统镜像文件并将其解压放置到一个合适的位置，咱放的位置是`/data/local/archlinux_arm`。

~~有人忘记创建文件夹直接解压，导致文件溢的到处都是，咱就不说是谁了 >\_<~~

## 「安装」

说是安装，其实是一系列为 chroot 准备的步骤，这里需要将一些必要的目录 `rbind` 到 chroot 内部。

```
mount --rbind /dev /data/local/archlinux_arm/dev
mount --rbind /sys /data/local/archlinux_arm/sys
mount --rbind /proc /data/local/archlinux_arm/proc
mount -t tmpfs tmpfs /data/local/archlinux_arm/tmp
```

**这些 `rbind` 并不是永久的，如果你重启了手机，则需要重新绑定。**

## ▢▢，启动！

现在是时候切换到 chroot 环境了，使用下面的命令就可以进入到 Archlinux ARM 的 bash 中了

```shell
chroot /data/local/archlinux_arm /bin/bash --login
```

不出意外的话，bash 亲切的界面就会出现在你的面前，虽然现在其行为可能有些异常，比如工作目录是根目录之类的。

## 联网

由于[Android内核特殊的权限机制](https://stackoverflow.com/questions/36451444/what-can-cause-a-socket-permission-denied-error#answers)，网络需要额外的配置。

```shell
groupadd -g 3001 aid_bt
groupadd -g 3002 aid_bt_net
groupadd -g 3003 aid_inet
groupadd -g 3004 aid_net_raw
groupadd -g 3005 aid_admin

usermod -a -G aid_bt,aid_bt_net,aid_inet,aid_net_raw,aid_admin root

newgrp aid_inet    # 立刻切换到 aid_inet 组
```

**如果你有使用到其他的用户，比如 www，请记得为其也添加相应的网络权限！**

然后是和早期的 WSL2 类似的，由于 Archlinux 的网络和解析默认是通过 systemd 管理的，而在 chroot 环境下 systemd 并不会工作，所以需要手动指定 DNS 服务器

```shell
rm /etc/resolv.conf    # 删掉原有的符号链接
echo 'your prefer nameserver ip' > /etc/resolv.conf
```

## 常用服务

### Pacman

pacman 的使用和在原生发行版上没有明显的区别，你可能需要遵循第一次使用 pacman 的流程来初始化密钥环和验证主密钥之类的，或者切换镜像。详细的内容可以参照 Arch Wiki，这里给出简明的命令。

```shell
# 初始化密钥环
pacman-key --init
# 验证主密钥
pacman-key --populate
# 切换镜像
echo 'Server = http://mirrors.tuna.tsinghua.edu.cn/archlinuxarm/$arch/$repo' > /etc/pacman.d/mirrorlist
```

有些人在使用 pacman 的时候会遇到所谓的空间检查失败的问题，而明明自己还有很多的硬盘空间，有一个可以用的 Workaround 是，去 `/etc/pacman.conf` 将 `CheckSpace` 注释掉即可。

## SSH

由于没有 `systemd` 所以需要自己手动启动 sshd

```shell
# 生成主机密钥对
ssh-keygen -A

# 使用全路径启动sshd
/usr/sbin/sshd
```

不过在某些情况下，使用 ssh 和 screen 等涉及到 pts 的可能会出现问题，比如出现无法打开 channel，而导致无法正常的使用，有一个 [Workaround](https://stackoverflow.com/questions/27021641/how-to-fix-request-failed-on-channel-0) 是重新挂载 `/dev/pts`

```shell
umount /dev/pts
mount devpts /dev/pts -t devpts
```

## 尾声

到此为止，一个可以使用的 Archlinux ARM 就在安卓上成功的跑起来了，可以用它部署一些简单的小服务，比如 Transmission 之类的离线下载器，或者是 Minecraft 服务器，或者是 Web Server 等等，一切你可以想到的内容了。

祝大家玩的愉快！
