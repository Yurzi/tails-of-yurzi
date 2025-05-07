---
title: '记一次噩梦般的五一服务迁移'
date: "2025-05-07T09:54:05+08:00"
lastmod: "2025-05-07T09:54:05+08:00"
author: ["Yurzi", "Lily"]
description: "一段对于消失的五一假期的纪念"
keywords:
  - Linux
  - Migration
  - Self-host
tags:
  - Linux
  - Network
  - Self-host
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

## 万恶之源

在过去的一个标准年里，咱一直沉浸在白嫖了某云服务商 300 米
然后只花了 600 米就可以获得一台在香港的 2C4G 30Mbps 的轻量应用服务器一年的使用权的喜悦里。
同时根据该云服务商的这个白嫖政策，咱应该还能白嫖好几年的 300 米。
虽然性能和带宽都不高，但它位于香港，有着较好的国际连通性，
这恰好满足了咱部署 Matrix Homeserver 的需求。

在这样的美妙幻想里，咱将所有的自建服务都 ALL IN BOOM 地部署到这台服务器上了，
包括：

- 博客：hugo pages
- 访问计数器：moe-counter-rs
- 图床：lskypro
- Matrix Homeserver：synapse + matrix-media-repo
- 密码管理器：vaultwarden
- 云盘：cloudreve
- 通知推送：ntfy

同时不知道当时咱抽了什么风，所有的服务都不是使用 Docker 的方式部署的，
这为后续故事的曲折发展埋下了伏笔。

有了前面的铺垫，自然而然的咱在这一标准年的4月份收到了云服务商的到期提醒，
于是咱就又屁颠屁颠的前去白嫖 300 米。
不出预料的，米是白嫖到手了，可是等到给旧的实例续费的时候咱懵逼了，
为什么这个米没法再一次用在这个之前可以用的实例上呢？

看了一圈发现，诶？！今年它改范围了，将香港实例排除在外了，
同时对于内地省份的实例，只能买特定规格的特定时长才能用米。

这下咱傻眼了，不能买香港的直接就干碎了咱对于国际连通性的幻想。
那现在该怎么办呢？船大难掉头，暂时没有想法的咱只能先忍痛原价续费了一个月。

险恶的社会给了天真的咱狠狠地打击，咱只好继续和梨鲤复盘现有的资源和预期。

事实上，咱是不缺计算资源和存储资源的，在今年里，得益于梨鲤的劳动付出，
咱已经在本地搭建了一个小型的 HomeLab 集群，集群内资源盈余非常严重，
严重到除了一个 dae 和一个 qbittorrent 外几乎没有东西在跑。
但制约咱将这些自建服务部署到 HomeLab 里的唯一桎梏在于没有公网和国际连通性。
一方面是本地充沛的硬件资源和孱弱的网络接入，一方面是国内云服务商提供的可怜的硬件资源和可怜的网络以及昂贵价格，
另一方面是国外云服务商对于国内的差连通性和没有合适的境外支付手段。

一个月很快就过去了，云服务商的续费提醒又到了。正当咱登上后台准备再续费一个月时，
咱突然注意到，今年云服务商的同产品线的新实例提高了带宽的限制，同时移除了对于流量的限额。
震惊于此的咱，随即重新调研了一下国内的云服务商类似产品的价格和参数。
一个新计划酝酿而出。

## 新架构

经过简单调研后发现，国内的好几家云服务商都推出了高带宽（指高达200Mpbs, bushi）且不限流量的产品，
同时其最低性能的配置下每月的价格大概在三十左右。
这意味着什么？这意味着完全可以在这种实例上运行内网穿透来实现将云服务器的网络接入 HomeLab 的同时，
还有着比较不错的纸面带宽参数，而且只需要相当于每月多交一个视频会员的钱。
但是如果咱有 HomeLab，咱为什么需要交视频会员的钱？

遂咱最终提出了咱的 HomeLab 架构 3.0，
特别的在的软路由上部署 Nginx 来反向代理局域网内其他节点上部署的应用服务。

```txt
          +----------+
          | Internet |
          +----------+
               ↕
               ↕
               ↕
          +----------+
          |   VPS    |
          +----------+              [rathole]
               ↕
               ↕
               ↕
    +---------------------------+   [rathole]
    |  HomeLab Software Rounter |
    +---------------------------+   [nginx]
               ↕
               ↕ 
               ↕
          HomeLab Network
```

## 服务的迁移与迭代

既然已经面临一次大动作，咱秉着不嫌事大的原则，对于咱的自建服务顺带进行一波迭代。

- 博客：hugo pages [keep]
- 访问计数器：moe-counter-rs [keep]
- 图床：lskypro -> immich
- Matrix Homeserver：synapse + matrix-media-repo [delete]
- 密码管理器：vaultwarden [keep]
- 云盘：cloudreve -> alist
- 通知推送：ntfy [keep]

首先最重中之重的决定在于移除 Matrix Homeserver，自从 Matrix 被 Element 一家之言之后，
虽然其确实改进了Matrix标准中很多不合理的地方，但同样的也使得维护难度变得大了起来，
诸如 sync v3、signed media 之类的特性的加入，让本就很难维护的 Matrix Homeserver 变得雪上加霜，
同时最重要的一点在于咱其实并不重度依赖 Matrix，所以为了降低迁移难度，咱直接将其移除。

然后是图床的变迁，lskypro 的开源版本已经不再维护，同时咱一直不喜欢使用 PHP 编写的应用服务，
此外更不提现有的 lskypro 开源版本有着非常严重的性能问题导致的体验不佳，所以咱直接替换它。
至于 immich，其实它并非图床，而更是一种相册，但也可以被用来当图床（什么万物皆可当图床），
此外 immich 可以用于管理和同步相册，可以缓解云盘换为 alist 之后的一些问题。

云盘选择 alist 其实没有太多可解释的，只是单纯的我并不需要 cloudreve 提供的一些「多余的功能」罢了，
同时 cloudreve 由于其复杂性，其实在之前的使用中一直有一些 bug 难以解决。

## Matrix HS 的移除

一直以来网上流传着 Matrix Federation 的传说：「联邦将会一直攻击背叛者，直到永远！」
但这事实上不只是玩笑，如果你只是简单的在本地关停了 HS 并移除，
那你的二级域名以及用于 Matrix Federation 的域名将被联邦里的相关参与者持续不断的尝试连接，
最终形成一种类似 DDOS 的效果。

根据 Matrix Spec. 对于 Server-Server API 的描述，HS 只会将事件广播给房间中的其他 HS，
也就是说，对于一个没在任何房间中的 HS 其应该并不会受到任何外来的广播消息。

所以，在移除 HS 之前需要先移除掉 HS 上用户参与的所有的房间，让所有的用户不再任何非本 HS 的房间里。
同时需要注意的一点是，由于 HS 对于请求的实现是异步且非实时的，不能在完成移除房间的操作后立刻停止实例，
这可能导致退出房间的消息没有完全在联邦中广播到位。

## Immich 部署和使用

虽然咱建议使用容器部署 Immich，但是在 Archlinux AUR 中存在一个名为 `immich-server` 可以不使用容器来部署的包。
下面咱将基于这个 AUR 包来部署和配置 Immich 和 Immich Machine Learning.

首先是安装过程，`immich-server` 的依赖项中有 `redis` 但是在咱折腾的这一时刻，社区已经宣布决定移除 `redis` 并使用 `valkey` 替代了，
所以在安装时，选择安装 `valkey`，但这会导致这个包携带的 systemd unit 文件产生错误而无法启动，
使用 `systemctl edit --full` 来将其中的 redis 依赖修改为 valkey。

在遵循安装后提示做完相关的操作后就可以启动Immich了，相关的配置文件在 `/etc/immich.conf`，同时数据文件存储在 `/var/lib/immich`下。
如果你想要修改存储位置，或者使用软链接等方式，记得修改 systemd unit 文件中对于路径的权限设置，需要将软链接的目的位置也加入到允许列表中。

### 数据库配置

由于 Immich 需要进行向量相似度搜索，所以需要在postgresql中安装额外的扩展，
对此，`immich-server` 会依赖一个 `pgvecto.rs-immich[-bin]` 的包，根据AUR的评论区建议安装
`pgvecto.rs-immich-bin` 以使用 0.3.0 版本。

安装了插件之后还需要在数据库中配置：

```sh
# 加载插件
psql -U postgres -c 'ALTER SYSTEM SET shared_preload_libraries = "vectors.so"'
# 设置数据库的搜索路径
psql -U postgres -c 'ALTER DATABASE immich SET search_path TO "$user", public, vectors'
# 重启 postgresql
sudo systemctl restart postgresql.service 

# 然后在数据库中启用插件
immich=#
DROP EXTENSION IF EXISTS vectors;
CREATE EXTENSION vectors;
```

对于 Immich 来说，最好使用一个带有管理员权限的账户，因为一般的普通账户没有权限操作数据库的扩展，以及无法操作对应扩展的 schema。
当然也可以通过给其相关授权的方法解决，但是需要多次尝试才能知道 Immich 需要哪些拓展和权限。

### 语义搜索和人脸识别

`immich-server` 携带了 immich-machine-learning 服务，并将项目放置在 `/opt` 下，
但是其所能使用的 CLIP 模型的目录在于 `/var/lib/immich/.cache/clip` 下。
虽然可以直接通过在管理后台修改对应的模型名称就可以实现自动下载并切换模型，
但是由于国内网络和 HuggingFace 的「兼容」问题，最好还是手动下载一下放在对应位置。

对于中文的语义搜索，咱选用 `XLM-Roberta-Large-Vit-B-16Plus` 模型，其可以在官方的 [HuggingFace](https://huggingface.co/immich-app) 上获取到。
对于人脸识别模型，咱选用`antelopev2`，但它其实没法很好的识别二次元角色。

### 中文化地理信息

Immich 默认的地理信息显示是英文，可以参考 [这个仓库](https://github.com/ZingLix/immich-geodata-cn) 来将地理信息优化为中文。

### 图床用法

对于 Immich 来说，存在相册共享，所以可以创建一个专门用于图床的相册，然后从中获取可以访问的图片链接即可。

## AList 部署

由于咱使用是 Archlinux，可以直接从 AUR 中拉取到 AList，经过简单的配置之后就可以直接开始使用了。

## 消失的五一

为了完成这个浩大的重构和迁移操作，咱的五一直接就莫名奇妙的消失了，
每天在命令行里敲敲打打到凌晨六点，
在各种语言的网页和文档里搜索解决方案，然后白天睡觉，晚上工作，一日不定几餐的过了五天。

对于这个五一来说，最大的收获应该在于掌握了 ostgresql 的插件的安装和使用方法——为了解决 Immich 的数据库问题。
但是唯一的缺陷在于 picgo 的 immich 插件无法使用，以及 Immich 对于动漫角色的识别比较失败。

原本这个五一咱还计划通关俩款游戏，这下什么都没有了，呜呜呜😭。
