---
title: 'Neovim again'
date: "2024-12-25T15:52:35+08:00"
lastmod: "2024-12-25T15:52:35+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "体验了一众编辑器之后回到Neovim"
keywords: 
  - "Neovim"
  - "Lazyvim"
  - "Editor"
tags:
  - "Neovim"
# series:
# math: true
# mermaid: true
draft: true
disableCounter: true
#cover:
#  image: ""
#  caption: ""
#  alt: ""
#  relative: false
---

## 纠结

自咱开始使用终端编辑器起，一直秉持着一个原则，那就是「自主可控」。
于是自打尝试使用 Vim 开始，咱就一直自己手动的配置所有插件，并且争取搞明白所有的参数的意义。
这样做的好处也是显著的，那就是当第一次撰写配置文件时，总能给出最适合自己的配置。

但是但凡有人亲手配置过 Vim 就知道，VimScript 的语法之佶屈聱牙，维护起来非常的麻烦，
每次插件更新之后遇到一些不符合自己心意的，需要自定义修改的地方就非常的耗费心力。
于是乎，咱就被 Neovim 更好的特性和其使用 Lua 配置吸引了。

第一次接触 Neovim 时，感受着其「现代化」的特性，以及内置的 LSP 支持，
真的让咱付出了挺多的心血去研究如何设计一个好的配置文件架构和如何配置一个「现代化」的编辑器，或者说 IDE。

可是，Neovim 是有新潮的好的，同时也有新潮的坏的。咱使用 Neovim 半年之后，
由于经常更新，经常导致配置需要进行 Break Changes 的适配，
同时还有插件之间的生死迭代，也总是需要耗费大量的尽力去维护。
这以至于咱每次上工，启动 Neovim 并更新插件后，就得花费大概一个小时的时间去维护她。
虽然咱不曾抱怨，但外界的压力还是让咱屈服。让咱迫切的需要一个能每天早上开箱即用的编辑器。

咱对此进行了反思，怀想其刚用 Vim 的时候，当时没有任何插件的情况下也能用的很开心，
于是咱就认为是插件导致了咱的憔悴。对此，咱开始追求「原生」，甚至又用了一段时间没有任何插件的 Neovim 和 Vim。
也就是在这段时间里，咱得知了 Vim 维护者去世的消息，深感悲痛的同时也意识到时代车轮的切实的转动。

吃过细糠的咱最终还是无法接受木头年轮蛋糕，咱呼唤那可人的 Language Server，不是所有的项目都是 C！
这时 Helix 进入了咱的视野，一个开箱即用的具备内建 LSP 的类 Vim 的编辑器，哇！这太让人 Amazing 了！
立刻上手了 Helix。

## Helix 的美丽与不足

具备开箱即用的 Helix 是美丽的，简洁且适合绝大多场景的。你只需要安装她，然后就可以开始汝的工作，
无需过多的配置，且有内建的快捷键提示，这对于咱这种年岁大的生物来说实在是太友好了！

唯一需要关心的可能是需要自己安装 Language Server，
但是因为咱用的 ArchLinux 绝大多数的都可以直接从系统吃豆人 pacman 那里要到，
实在没有的也有热心人的 AUR 包。

于是在刚摸到 Helix 酱的那一刻咱就觉得这就是咱所想要的了，咱甚至大言不惭的说咱要之后的日子都与 Helix 酱过。
现在想来，咱也是没有真正评估自己的手癖了。

随着与 Helix 酱的日渐熟稔，咱开始在各个地方使用她，享受着她的优雅和简洁，虽然她还稚嫩，但总会逐渐变得强大。
但随着使用了一段时间后，问题开始显现，心中的不满最终溢出表面。

咱一般在使用 Language Server 的补全时不太喜欢自动弹出候选框和自动选中的，
在使用 Vim 的时候，咱习惯在需要的时候使用  Ctrl + n 来唤出，这些在 Helix 上都能设置，
但是这个癖好同时也让咱忽视了在没有 LSP 的时候 Vim/Neovim 的基于词的匹配了。

在使用 Helix 编写大型 Python 项目时，时常会出现因为代码中没有 Typing 而导致 LS 响应缓慢甚至崩溃的情况，
这时候就只能依靠 Copliot 或者内建的基于词法的补全了，但是可惜的是的 Helix 上两者都不可用。
但也不是说完全不可用，而是有其他的第三方的 LS 实现了这些功能。但问题在于如何全局的配置一个 LS 呢？
汝要知道 Helix 的 LS  是和语言绑定的。

另外的一个问题在于，Helix 一直难产的插件系统，而且可以知道的是，其插件系统可能会使用一种 Lisp 的方言实现，
这让咱有了 VimScript 的感觉。

在忍受了许久的 Ctrl + n 不工作之后，咱终于决定暂时的抛弃 Helix，但是用什么呢？

## LazyVim 劳苦大众的开箱即用解决方案

在咱被 Helix 骗走的这段时间里，Neovim 社区里正在发生一些改变，一些东西在变得标准化，最终她出现在了咱的视野中——LazyVim。

其实对于 Lazyvim，在咱刚刚接触 Neovim 的配置时就有所耳闻，但当时年轻的咱心高气傲，
对此不屑一顾。而现在经过时间的打磨之后，咱最终还是变的 Lazy。

### 自认为 LazyVim 的优势

其实在咱在 Neovim 的时候重构过两次配置文件的结构，第二次的时候咱就使用了 Lazy 作为插件管理器。
所以说 LazyVim 的设计是遵循一种 Neovim 社区里普遍的基于 Lazy 管理器配置文件设计范式的。

其使用 lua/plugins 文件夹来存储插件的 Specification，可以发现当汝即使不使用 LazyVim 也会很自然的组织出类似的结构，
但 LazyVim 相较于自己裸基于 Lazy 编写的配置有一个好处就是有一个默认的但非插件默认的配置，同时也有人专门维护这些底层的配置。
汝可以再这个基础上做覆盖和新增。
这在某种意义上减缓了插件的新旧迭代和 Break Changes 对于配置文件的毁灭性打击，
毕竟再不济也不过是删除自己加的部分，同时保证了一个IDE的基础功能正常运作。

### 自认为 LazyVim 的问题

LazyVim 对于Lazy的新人和对于Lazy的老人来说都是\*\*ao\*\*的，但是对于一个没有自己构建过配置结构的人来说，
LazyVim 的实现就将一系列的原理掩盖了，虽然其官网有详尽的默认配置细节但还是无法较为准确的理解到底发生了什么。

## 会使用 LazyVim 多久呢

虽然咱现在已经使用 LazyVim 三个月了，期间也经历了两次大版本的变革，虽然还是有早晨更新完插件之后就发现变天了的情况，
但至少没有出现更新完之后不可用的情况，而且 LazyVim 的大版本更新会给出较为详尽的更新日志还是非常不错的。

### 目前遇到的痛点

在 LazyVim 换用 Blink 后的边框消失，但是如果采用 Blink 的边框设置就会导致其非常的丑陋，
对此目前也没有什么好的方法，或许可以通过修改主题插件的设置来修复？
但咱选择摆烂，因为时间会修复一切。

另外的一个痛点也是 Blink 带来的，或者说是Copilot 带来的，就是在使用 Copilot 时，其 Ghost Text 会因为非常长而导致光标乱飞。
目前解决办法也只能是要不关闭 Ghost Text 要不让的 Copilot 的建议不显示或者说让其不在 Markdown 之类的文件里进行补全。

## 好看的前端 Neovide

虽然咱在很多时候追求性能，其实咱还是颜值党来着，所以咱对于 Neovide 这种带有丝滑动画的前端几乎没有抵抗力。
但是可惜的是在 Windows 上 Neovide 还是有许多特性不支持，比如咱最喜欢的 Blur。

## 总结

总的来说，这次回到 Neovim 的体验是丝滑的，而且让人安心。虽然缺少了年轻时候的自信，多了变老之后的 Lazy。