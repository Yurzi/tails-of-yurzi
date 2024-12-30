---
title: "在WSL2中安装ArchLinux"
date: "2022-07-08T00:38:03+08:00"
lastmod: "2024-03-27T23:30:03+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "在WSL2上安装ArchLinux"
keywords:
  - Windows
  - ArchLinux
  - WSL
tags:
  - WSL
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

## 准备工作

### WSL的安装

**如果**你使用的是Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11。

那么你可以在微软应用商店安装，或者直接使用如下命令安装WSL，该命令会完成一条龙操作，诸如开启指定功能，安装必须的组件，详情请参考[微软官方指南](https://docs.microsoft.com/zh-cn/windows/wsl/install)

```shell
wsl --install
```

**如果**是更老的Windows 10版本，则可以参考旧版WSL的[微软官方安装指南](https://docs.microsoft.com/zh-cn/windows/wsl/install-manual)进行手动安装。

### 升级到WSL2

WSL1和WSL2的区别详情查看[官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/compare-versions)，简单来说就是WSL2是具有Linux内核的轻量虚拟机。ArchLinux需要在WSL2上才能原生运行，否则需要使用修改的glibc，详见[这里](https://wsldl-pg.github.io/ArchW-docs/locale/zh-CN/Known-issues/#glibc)

如果使用的微软商店和一条龙命令安装的WSL则默认的版本就是WSL2不需要进行额外的操作。否则则需要使用 `wsl --set-default-version 2`来将WSL的默认版本设置为WLS2。

`wsl --set-version` 命令可用于从 WSL 2 降级到 WSL 1，或将以前安装的 Linux 发行版从 WSL 1 更新到 WSL 2。

同时需要注意，如果没有安装过内核，则可以[手动下载](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)安装，或者执行 `wsl --update`命令来安装。

### WSL的高级配置

WSL有着很多配置，了解这些对于以后更好的使用WSL有着重要的意义，详情请参考[官网文档](https://docs.microsoft.com/zh-cn/windows/wsl/wsl-config)。

### 安装Windows Terminal(可选)

Windows Terminal是微软开发的一款现代终端模拟器，有着高颜值的特点，同时可以自动兼容WSL中的发行版，动态生成相应的配置，是居家旅行不可或缺之良品（大雾

## 安装配置ArchLinux

### 安装

安装ArchLinux的方法有2种，一种是利用[ArchWSL](https://github.com/yuk7/ArchWSL)项目来安装，另一种是使用[LxRunOffline](https://github.com/DDoSolitary/LxRunOffline)(一个第三方WSL管理工具)来安装。本文将分别介绍2种方法。

#### ArchWSL

根据ArchWSL项目给出的[文档](https://wsldl-pg.github.io/ArchW-docs/locale/zh-CN/How-to-Setup/)安装方法，可以使用小白式的双击**解压**后文件夹内的exe文件直接安装。**exe文件的名称就是WSL中是实例名称**，所以需要安装多个实例时需要对exe文件进行重命名。事实上只要压缩包中的rootfs.tar.gz就可以用LxRunOffline来进行安装，或者进一步解压为tar后使用 `wsl --import <实例名称> <安装位置> <安装tar>`进行安装，详情请查看 `wsl --help`

另一种方法是通过appx的方法安装，这里不再赘述。

#### LxRunOffline

使用LxRunOffline不仅可以安装ArchLinux，还可以安装很多其他发行版，只需要获得对应发行版的系统镜像即可，但使用系统镜像安装的系统只能在WSL2上才能正常启动。而上述ArchWSL提供的ArchLinux则可以在WSL1下运行。

**第一步 安装LxRunOffline**

建议使用chocolatey或者scoop等包管理器安装，[项目主页](https://github.com/DDoSolitary/LxRunOffline)也有给出安装指南，或者直接下载二进制文件后自己添加进环境变量使用。

**第二步 下载安装ArchLinux**

前往[清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/archlinux/iso/latest/)下载形如 `archlinux-bootstrap-x86_64.tar.gz`的最新bootstrap包。然后使用如下命令进行安装。

```shell
lxrunoffline install -n <实例名称> -d <安装位置> -f <安装文件位置> -r root.x86_64
```

### 配置

如果WSL中只有一个实例，则直接使用 `wsl`命令即可以开始运行，这个命令会进入设置的默认发行版并以默认身份，可以查阅[WSL高级配置](https://docs.microsoft.com/zh-cn/windows/wsl/wsl-config)来设置，或者使用 `wsl -d <发行版> -u <用户名>`命令来进入发行版。如果无法运行发行版，请检查是否为WSL2运行并检查内核是否安装。想以WSL1运行ArchLinux需要[特殊操作](https://wsldl-pg.github.io/ArchW-docs/locale/zh-CN/Known-issues/#glibc)

#### 网络与包管理器

首先删除 `/etc/resolv.conf`，退出 WSL 再重新进入使 Windows 自动生成这个文件。

```shell
rm /etc/resolv.conf    	# 删除这个DNS设置文件以让wsl自动生成，，否则会有上不了网的问题
exit 0
wsl --shutdown
wsl 			# 重启wsl以让其自动生成resolv.conf
```

然后再次进入对应的实例之后，因为此时的ArchLinux中并没有安装任何的文本编辑器（哪怕是vi），只能通过其他手段来修改pacman的镜像源。

通过windows资源管理器和文本编辑器修改 `/etc/pacman.d/mirrorlist`，当然也可以使用 `cat` 和 `echo 'Server = <你选择的镜像服务器>' >>`来修改镜像服务器，不过建议在安装了文本编辑器后重新整理结构。

```shell
cd /etc/
explorer.exe . 	# wsl中可以直接调用windows进程，详细设置见WSL高级配置
```

以类似的方法修改 `/etc/pacman.conf`，往其中添加如下内容以将中文ArchLinux社区源加入pacman中

```shell
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

在之后初始化pacman，生成密钥环，安装系统必要组件。

```shell
pacman-key --init 			# 初始化密钥环
pacman-key --populate archlinux		# 验证密钥
# 更新包列表和系统，并安装基础组件和中文社区密钥环
pacman -Syyu --needed base base-devel
pacman -S archlinuxcn-keyring
pacman -S neovim 			# 安装neovim文本编辑器，也可以安装别的文本编辑器
pacman -S yay 				# 获取AUR支持，也可以选择使用aurman
```

#### 时区与本地化

使用 vi 或 nano 编辑 `/etc/locale.gen`，取消注释需要使用的语言（一般是 `en_US.UTF-8 UTF-8` 和 `zh_CN.UTF-8 UTF-8`），输入 `locale-gen` 生成语言文件。

输入 `ln -sf /usr/share/zoneinfo/<区域>/<子区域> /etc/localtime` 来设置时区，对于在中国的我来说是：

```shell
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

再者是关于本地化的语言的设置，详情请参见[Arch Wiki](<https://wiki.archlinux.org/title/Localization_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)/Simplified_Chinese_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)>)。

#### 权限管理与用户

添加新的用户并设置密码

```shell
useradd -m -G wheel -s /bin/bash <用户名>
passwd root
passwd <用户名>
```

使用visudo来设置权限

```shell
EDITOR=nvim visudo
```

然后设置默认登录用户，这里有两种方法。

**使用LxRunOffline**

首先，在WSL内使用 `id -u <用户名>`获得指定用户的用户id，然后使用以下命令来设置默认登录用户。

```shell
lxrunoffline set-uid -n <实例名称> -v <UID>
```

**使用wsl.conf**

详情参考[WSL高级配置](https://docs.microsoft.com/zh-cn/windows/wsl/wsl-config)，该文件存在于 `/etc/wsl.conf`，若不存在则新建。

### 最后

至此，满足一般使用的ArchLinux的安装已经完成，虽然此时系统内还有一些无用的用于安装系统的软件，强迫症可以输入以下命令卸载它们：

```shell
sudo pacman -R arch-install-scripts
```

此外，由于WSL在启动实例时并不会使用systemd，它使用init的方式来启动系统，但是使用的init方法也并不同于一般的虚拟机或者物理机上的Linux，如果你有dbus乃至systemd的需求，可以继续阅读下文。

## DBus与systemd

### DBus

将DBus和systemd分开讲解是为了满足一些只需要DBus的情况。对于在WSL1中使用DBus参考[这里](https://wsldl-pg.github.io/ArchW-docs/locale/zh-CN/Known-issues/#d-bus)给出的方法，或者尝试以下方法。

#### Session Bus

Session Bus 用于用户自己的程序之间相互沟通，输入法等的运作需要 Session Bus 才能正确工作。首先安装需要的软件包

- `daemonize`
- `dbus-daemon`

然后在 ~/.bash_profile` (或者随便哪个觉得合适的地方) 加上

```shell
daemonize -e /tmp/dbus-${USER}.log -o /tmp/dbus-${USER}.log -p /tmp/dbus-${USER}.pid -l /tmp/dbus-${USER}.pid -a /usr/bin/dbus-daemon --address="unix:path=$XDG_RUNTIME_DIR/bus" --session --nofork  >>/dev/null 2>&1
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
```

原理很简单，就是 `/tmp/dbus-${USER}.pid` 作为 lockfile 保证 dbus 是单实例的，监听地址就在 `unix:path=$XDG_RUNTIME_DIR/bus`，也就是 XDG 规定的默认地址。并设置环境变量。

#### System Bus

System Bus 用到的情况就要少一点了，因为权限的问题，最好借助 WSL 自己的 boot 功能实现。

首先准备一个脚本，我放到了 `/usr/local/bin/boot.sh`，内容是

```shell
#!/bin/bash

/usr/bin/mkdir -p /run/dbus/
/usr/bin/dbus-daemon --system
```

然后在 `/etc/wsl.conf` 中添加以下字段

```shell
[boot]
command=/usr/local/bin/boot.sh
```

这里需要写完整路径，因为此时的还没有 `PATH`环境变量的存在。

### systemd

systemd的设置就较为复杂，如果你使用WSL1，那么只能考虑使用模拟的systemctl的脚本，不过只能部分兼容 systemctl。下载 [systemd-altctl-1.4.4181-1-any.pkg.tar.xz](https://github.com/yuk7/arch-systemctl-alt/releases/download/1.4.4181-1/systemd-altctl-1.4.4181-1-any.pkg.tar.xz) 然后运行 `pacman -U systemd-altctl-1.4.4181-1-any.pkg.tar.xz` 以安装。

如果你使用WSL2，则可以考虑 systemd 容器，比如 [subsystemctl](https://github.com/sorah/subsystemctl) 、 [genie](https://github.com/arkane-systems/genie) 或者是 [distord](https://github.com/nullpo-head/wsl-distrod)。同时也可以考虑使用[wsl2-hacks](https://github.com/shayne/wsl2-hacks)提供的一种基于手工替换 `root`用户的login shell + 脚本nsenter执行systemd的思路，这个方法需要保证wsl的默认登录用户为 `root`，详情可以参考其项目 `README`

相比之下，distord可能是更好的选择。但是！微软的WSL2自支持systemd惹！

#### 启用WSL2的systemd支持

首先，要使用 WSL2 的 systemd 需要 WSL2 的版本在 0.67.6 之上。可以使用 `wsl --version` 来查看。

然后，在相应的发行版中编辑 `/etc/wsl.conf` 文件，添加如下内容：

```shell
[boot]
systemd = true
```

最后，使用 `wsl --shutdown` 来重启 WSL 实例即可在相应的发行版中使用 systemd 了。详细内容可以参考微软的[博客](https://devblogs.microsoft.com/commandline/systemd-support-is-now-available-in-wsl/)

## 其他问题

### 宿主机ip获取

在WSL1，子系统和Windows共同使用同一张网卡，表现为端口资源共用等行为。而WSL2作为轻量化的虚拟机，以NAT的方式连接到外网。因此在每次启动WSL时，会动态分配ip地址，从而难以获取到宿主机的ip地址。

以下提供两种方式获取宿主机的ip。

**第一种 shell脚本**

每次启动实例，wsl都会设置实例中的 `/etc/resolv.conf`，将域名解析服务器指向Windows自身，所以可以使用脚本截取其中的IP作为宿主机IP。

```shell
host_ip=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}')
```

**第二种 python脚本**

读取网口配置并将NAT网卡eth0的网关IP地址写入到 `/etc/hosts`，主机名为 `windows`

```python
import os
import re
from functools import reduce

HOST_MACHINE_NAME = 'windows'
HOST_MACHINE_IP_FILE = '/run/host-ip'

IP_PATTERN = re.compile(r'inet\s+(?P<ip>\d+(\.\d+){3})/(?P<bits>\d+)')

def getHostMachineIpAddr():
   for line in os.popen('/usr/bin/ip -4 addr show eth0'):
	match = IP_PATTERN.search(line)
	if (match):
            local_ip = reduce(lambda x, y: x * 256 + y, map(int, match.group('ip').split('.')))
	    subnet_bits = int(match.group('bits'))
	    subnet_mask = (( 1 << subnet_bits) -1) << (32 - subnet_bits)
    	    host_ip = (local_ip & subnet_mask) +1
            return '.'.join(map(str, [255 & (host_ip >> (8* (3 - i))) for i in range(4)]))

if (__name__ == '__main__'):
    with open('/etc/hosts', 'a') as hosts, open(HOST_MACHINE_IP_FILE, 'w') as ip_file:
	hosts.write('\n')
	hosts.write('# generated by wsl-host\n')
	host_machine_ip_addr = getHostMachineIpAddr()
	if host_machine_ip_addr:
	    hosts.write('%s %s\n' %(host_machine_ip_addr, HOST_MACHINE_NAME))
	    ip_file.write(host_machine_ip_addr)
```

### 磁盘占用问题

使用一段时间后，WSL2虚拟机的磁盘镜像往往会因为一些未回收的数据块而变得臃肿。

可以通过专业版Windows安装Hyper-V功能后提供的 `Optimize-VHD`cmd-let或者 `diskpart`工具的 `compact`指令来减少虚拟磁盘镜像的空间占用。相关[讨论](https://github.com/microsoft/WSL/issues/4699)。

Powershell脚本如下：

```powershell
Write-Output "Shutdown WSL2";
wsl - e sudo fstrim /
wsl --shutdown

$vhdx = "<安装的路径>\ext4.vhdx";
Write-Output "Compact $vhdx"

@"
select vdisk file=$vhdx
attach vdisk readonly
compact vdisk
detach vdisk
exit
"@ | diskpart
```

## 参考

- [微软官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/)
- [WSL2 下 Arch Linux 安装配置备忘 - hucsmn](https://hucsmn.com/wsl2-installation-note/)
- [用 LxRunOffline 安装 Arch Linux | Paro 的博客](https://paro.one/research/20180215-use-lxrunoffline-to-install-arch-linux/)
- [如何安装 | ArchWSL official documentation](https://wsldl-pg.github.io/ArchW-docs/locale/zh-CN/How-to-Setup/)
