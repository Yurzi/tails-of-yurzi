---
title: "在Linux上设置某大学的校园网"
date: "2024-10-14T17:09:35+08:00"
lastmod: "2024-10-14T17:09:35+08:00"
author: ["Yurzi", "Lily"]
description: "记录如何在Linux设备上设置某大学的校园网"
keywords:
  - SYSU
  - Network
  - Linux
tags:
  - Network
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

## 前言

经过一番在现实生活中的奔波后，还是找到了一个合适的安生之所，来到了一所新的大学。
在解决了最基础的生存需求后，最终还是到了得解决网络需求的地步了。
虽然学校有提供无线网络连接，但是这个无线网络她喵的没有 IPv6！而且对于连接到同 WIFI 的设备之间无法互相访问，
这导致咱的一些用于多设备之间交流的设置直接失效了，在忍耐了 ~~114514s~~ 后，终于还是不得不开始折腾。

## 调研

通过访问学校网络中心的官网和结合搜索引擎的结果，咱发现自己所待这所大学使用的锐捷 v4 的认证方式。
锐捷认证之臭名，就算是小白如咱也是如雷贯耳，于是心中顿觉一时成功的可能性不大。

考虑到这破大学似乎有着非常完善的网络服务流程，于是咱在某位E人的撺掇下，决定致信网络服务中心以表明 Linux 平台难以使用校园网的困境，并期望获得一个官方的解决方案。
但最终的只得到了一个 Oracle：「存在一个第三方客户端可以用于校园网的认证并被网络中心允许使用」。

于是通过在著名交友社区 「Gayhub」上简单的检索就可以发现有一个名叫 「mentohust」{{<cref 1>}}项目能够处理锐捷认证同时支持 v4 算法，但经过测试之后发现其在咱所处破落学校之网络环境下，水土不服无法运行。

但好在该工具的维护者于 README 中推荐了另一个工具「minieap」{{<cref 2>}}，遂继续尝试，发现该工具可以认证成功，但是似乎无法保活，并给出报错信息「在 4 状态已经停留了 3 次，达到指定次数，正在退出……」。

于是乎，现在的挑战就在于如何使用 minieap 实现保活。

## 实现保活

通过围绕报错信息进行检索，在 minieap 项目中的一个 issue {{<cref 3>}} 启发了咱，通过观察日志，发现咱这学校也似乎确实是使用认证信息进行心跳的，遂修改 minieap 源码：

```c
 338   │     if (PRIV->state == EAP_STATE_IDENTITY_SENT) {
 339   │       // jump out from the exit trap for sxxu
 340   │       PRIV->state_last_count = 0;
 341   │     }
 342   │     if (PRIV->state_last_count == _cfg->max_retries) {
 343   │       PR_ERR("在 %d 状态已经停留了 %d 次，达到指定次数，正在退出……", PRIV->state, _cfg->max_retries);
 344   │       exit(EXIT_FAILURE);
 345   │     }

```

唯一的修改就是在 `switch_to_state` 函数中加入特判来防止退出。咱也知道这是非常 naive 的修改方式，但以咱这 C 语言水平是一点看不懂原作者是怎么写的，遂只能做如此简单的修改了。

## 新的挑战

在对 minieap 进行修改后确实能实现认证和保活了，但是当网络链路发生波动时，minieap 会重新回到查找认证服务器的状态，而此时必定会触发一个段错误。

经过对 coredump 文件的分析发现，是 minieap 在检查接受到的帧是否是 MD5 帧时出现了访问非法地址的问题，
其中对于帧中的 header 和 content 由于使用了 union 共享内存，
从而导致了当出现非法的 content 时，访问 header 以确定是否为 MD5 帧会出现非法访问。
但经过86400秒的排查之后，咱还是没有发现出现这种问题的根源，遂只能放弃，并使用重启大法来 workaround。

## 结论

虽然在这次的折腾过程中，最终生效的代码只有短短一行，但是极大地提升了我对于 C 语言项目的理解能力。

同时最终的结果虽然不是尽善尽美，但最终也是完成了咱在 Linux 环境下使用校园网的目标，同时也为后续配置自己的小内网做铺垫了。

## References

{{<cite 1 "[1] Github: mentohust: mentohust加入v4支持" "https://github.com/hyrathb/mentohust">}}
{{<cite 2 "[2] Github: minieap: 可扩展的 802.1x 客户端，带有锐捷 v3 (v4) 算法插件支持" "https://github.com/updateing/minieap">}}
{{<cite 3 "[3] GIthubIssue: minieap: #83 能认证成功，但无法心跳" "https://github.com/updateing/minieap/issues/83#issuecomment-2323197143">}}
