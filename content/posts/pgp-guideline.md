---
title: "PGP使用实践指北"
date: "2022-10-22T22:37:49+08:00"
lastmod: "2024-03-27T23:37:49+08:00"
author: ["Yurzi"]
lang: "zh-CN"
description: "简单的介绍PGP的使用"
keywords:
  - Cryptography
  - PGP
tags:
  - Cryptography
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

在某天在 ArchLinux 上成功编译完成 <ruby>caffe<rp>(</rp><rt><del>炼丹炉</del></rt><rp>)</rp></ruby> 及 OHEM 层扩展后，突然想往 AUR 上提交具有此拓展的包，但在注册 AUR 账户时，注意到了「PGP密钥指纹」一项，对于初入开源社区的咱来说是一脸懵逼，于是旅途便开始了。

## 初来乍到

### 概念解析

一开始了解这方面的内容时，咱对于各种简称，例如 `GPG` `PGP` `OpenPGP` 等感到困惑，经过反复追本溯源的验证之后得出如下结论。

**PGP：** 早年间指代 「Pretty Good Privacy」一款商业软件，现在多指代「OpenPGP」

**OpenGPG：** 与「Pretty Good Privacy」兼容的IETF标准

**GPG：** 指代「GnuPG」因为它的命令行命令是 `gpg`

**GnuPG：** 也就是 Gnu 实现的基于 OpenGPG 标准的自由软件

**RNP：** 实现 OpenGPG 标准的工具和库的集合。

~~一边贴着 GnuPG 的图，一边用 PGP 做标题的玖只是屑~~

### 获取PGP客户端

首先，需要获取对应平台的 PGP 客户端，在 Linux 平台上这通常是 GnuPG，虽然在 Windows 上可以选择 GnuPG 或者 Gpg4win。不过或许也可以使用 RNP 的 CLI 。考虑到教程的丰富度，咱还是选择走 GnuPG 这条岔路。

至于如何获取，想必聪明的汝应该不至于懒到筷子的都懒得自己去取吧！不过如果汝是 Linux 用户，那「筷子」已经随<ruby>系统<rp>(</rp><rt><del>套餐</del></rt><rp>)</rp></ruby>附带了，如果是微软家的，咱推荐你使用 <ruby>scoop<rp>(</rp><rt><del>勺子</del></rt><rp>)</rp></ruby>包管理器来获取。

### 生成密钥对

这一步是这段旅途的真正意义上的开始，从这里开始不同的客户端虽然步骤大同小异，但还是有许多<ruby>稍<rp>(</rp><rt>xué</rt><rp>)</pr></ruby>微细节，如果汝选择了不同于咱的路，请自行查阅相关指南。

对于 GnuPG 来说，咱觉得这几位位前辈写的非常不错，当然汝仍可能需要在互联网上寻找其他的指南：
[gpg使用介绍与配置说明 - Even](https://blog.logc.icu/post/2020-08-02_09-39/)
[GPG Short Guide - hedzr](https://hedzr.com/security/gpg/gpg-short-guide/)
[2021年，用更现代的方法使用PGP（上）- UlyC](https://ulyc.github.io/2021/01/13/2021%E5%B9%B4-%E7%94%A8%E6%9B%B4%E7%8E%B0%E4%BB%A3%E7%9A%84%E6%96%B9%E6%B3%95%E4%BD%BF%E7%94%A8PGP-%E4%B8%8A/)

**1. 在汝整明白PGP网络之前，千万千万不要跟随任何教程，将公钥上传到密钥服务器**

2. 如果汝已经明白了PGP网络，并向上传公钥，建议使用「 [Keys OpenPGP](https://keys.openpgp.org/) 」，一个可删除的公钥服务器

在这里，咱生成的是 「ECC与ECC」密钥对。虽然有研究称 RSA-4096 相交 ECC-256 更安全，但 ECC 的计算速度更快，长度更短，可以节约些地球的资源嘛。再者是对于 uid 的设置，虽然在之后可以更改，但如果汝将公钥上传到了去中心化的公钥服务器池，那就永远删不掉啦，所以请慎重考虑。

咱推荐汝在生成密钥对的时候设置过期时间，以确保「失能机制」

可以使用 `22020202T000000Z` 的格式指定绝对时间，其中 `T` 为分隔符，`Z` 代表 `UTC`

**记得一定一定要生成一张吊销证书，并妥善保存。**

### 子密钥对

现在，汝应该有一个主密钥对了，同时看完教程的汝可能已经尝试生成了一些子密钥对。对于子密钥对下面是咱的一些理解：

1. 除了给其他密钥或者密钥标识签名和生成新的子密钥对，都不要使用主密钥对
2. 应该为每种用途生成一个子密钥对，并设置相应的有效期
3. 子密钥对的公钥，在导出时必定包含主公钥
4. 子密钥对的私钥，可以脱离主私钥存在
5. 导出子密钥对的私钥时，应当剥离包括主私钥在内的其他私钥

### 导出与备份

按原则上，汝的主密钥需要保持离线，也就是说，汝最后需要删除现有客户端中的主密钥，所以需要导出相应的密钥来进行备份。咱的导出原则如下：

1. 导出完整的主私钥和主公钥
2. 导出剥离所有子密钥对的主私钥和主公钥
3. 导出剥离主私钥和其他子密钥的每个子密钥的私钥和公钥
4. 导出需要一起使用的剥离主私钥和其他子密钥的子密钥的私钥和公钥，也就是多个子密钥在一起的文件（可能需要使用 `>` 来写入文件）
5. 导出吊销证书

## 闲庭信步

在有了一套子密钥对后，就可以玩起来。这时候主私钥相关已经可以被雪藏了，完整的主公钥可以用来发布，当然汝也可以发布不完整的。至于如何玩，Uiyc前辈总结的很好——[2021年，用更现代的方法使用PGP（中）- UlyC](https://ulyc.github.io/2021/01/18/2021%E5%B9%B4-%E7%94%A8%E6%9B%B4%E7%8E%B0%E4%BB%A3%E7%9A%84%E6%96%B9%E6%B3%95%E4%BD%BF%E7%94%A8PGP-%E4%B8%AD/)。这里咱只给出一些实践上的经验。

### 为 Git commit 签名

在实际配置的过程中，会遇到一些问题。

首先是对于 Windows 平台下使用的 msys2 子系统内的 GnuPG 无法和 Git 联动，可能因为 Git 其实运行在另一个 msys2 子系统下，并且其 Git Bash 也内置了一个`gpg`（是的，汝没看错。

如果汝不想使用 Git Bash，那么就需要安装一个 Windows上的 GnuPG。

再者是在无界面的 Linux 系统上，可能需要使用 `export GPG_TTY=$(tty)` 来使 GnuPG 使用基于命令行字符的密码输入框。

#### 使用匿名邮箱

如果汝在 GitHub 上使用了「Block command line pushes that expose my email」选项，那么汝需要使用完整的主私钥在密钥对中加入一个新的 uid 并指定其邮箱为 GitHub 提供的一个格式为 `{random-number}+{user-id}@users.noreply.github.com`的邮箱。

### 加密邮件

对于加密邮件是收发，在 PC 上咱使用的「Mozilla ThunderBird」，一个开源的邮件客户端，其内置了基于「RNP」实现的 OpenGPG 密钥管理器。汝只需要做的是导入具有汝所用邮箱地址 uid 的一份加密用子私钥和一份签名用子私钥。

至于在安卓手机上，咱用的是「K9-Mail」，也是一个开源的邮件客户端，但其 PGP 需要另一个应用「OpenKeychain」来作为依赖。

## 炉火纯青

### 配置WKD服务

如果汝要配置WKD服务来发布自己的公钥，汝首先要有一个自己的域名和一个可以用自己的域名收发的邮箱。

#### 对于邮箱

这个邮箱可以是自建的，或者是基于现有的一些企业邮箱服务提供的邮箱域名自定义服务。不过其实存在不存在邮箱对于WKD的公钥发布来说意义不大，其唯一的作用就是，让 WKD 真的能嵌入到给汝发邮件的时候。

#### 对于WKD配置

可以参考[为 PGP Key 部署 Web Key Directory (WKD) 托管 | 欠陥電気の摸鱼小池 (atri.tk)](https://blog.atri.tk/2021/host-a-web-key-directory/)。

咱虽然有自己的Server，但出于偷懒还是使用了「 [Keys OpenPGP](https://keys.openpgp.org/) 」的 WKD Service。所以，现在汝可以使用`yurzi@yurzi.cn`来直接获取到咱的公钥，公钥的指纹在[关于咱](https://blog.yurzi.net/about.html)中。

```shell
gpg --locate-key yurzi@yurzi.cn
```

## 对 PGP 的思考

PGP 的历史其实也很长了，事实上现在对于PGP的使用也仅仅存在于一些小众的场景，更多是一种个人或者极客的玩具。不过这并不是说这场旅途没有意义。现代 PGP 更多的代表了一致隐私和加密的符号象征。

对于现代密码学来说，PGP 的设计是简陋和原始的，参考阅读：

[「译」PGP的问题（上）- UlyC](https://ulyc.github.io/2022/09/05/tr-pgp-problem-1/)

[「译」PGP的问题（下）- UlyC](https://ulyc.github.io/2022/09/07/tr-pgp-problem-2/)

不过，就算如此，这次 PGP 的旅途对咱的意义在于带咱回到小学，为了传写有不想让其他人知道小秘密的小纸条时的那份思考的时光，以及最后发明了一种方法之后的喜悦以及因为过于复杂而无人使用的落寞吧。

所以，欢迎汝能和咱传「小纸条」捏！😊
