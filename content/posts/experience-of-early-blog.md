---
title: "早期个人博客搭建经历"
date: "2021-05-01T21:43:36+08:00"
lastmod: "2024-03-27T14:56:36+08:00"
author: ["Yurzi", "Lily"]
description: "早年间搭建个人博客的心路历程"
lang: "zh-CN"
keywords:
  - Blog
  - Hexo
  - Experience
tags:
  - Blog
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

## 萌芽

第一次想到要搭建一个个人主页是在7年前，当时看到有个B站的up主整了个个人主页来发布资源，我就想着我也想并应该能整一个。于是乎一场历时将近7年的技术积累开始了。

## 准备

### 设备

作为一个学生党，起初我天真地以为，网页必须部署在一台自己拥有的服务器或者云服务器上，而贫穷的初中生并没有钱，于是乎想到用家里废弃的笔记本来充当服务器。
但是这就遇到了一个麻烦，笔记本上原先装的为winXP系统，而为了节省资源，应该使用Linux服务器系统。所以，我第一个倒腾的玩意，就是如何给电脑重装系统，并且是装不同的系统。

当时的我还是初一学生，理解能力并不强，看了网上好几篇装系统的教程，硬是没搞到所谓的BIOS，PE是什么玩意。
我当时就想，为什么装个系统要用另一个软件，系统自己难道不提供安装方法的吗？
带着这样的疑问，我继续找资料，过了一个月，看了文章，视频，渐渐的我开始认识到BIOS是什么东西，也知道了装系统除了用PE还可以将系统镜像录入U盘来安装。

虽然知道了这些知识，但是都是基于安装windows系统的，关于Linux系统的安装我毫无概念，
不要说如何将Linux的文件烧录到U盘了，我连当时Linux到底是个什么玩意都没整清楚，
一会是Ubuntu一会是CentOS，直到后来才有了Linux发行版的概念。
于是带着试试的心态我按着网上的教程去下Ubuntu来安装，经过迅雷漫长地下载，得到的iso文件我没一点想法，我知道是虚拟光驱文件，但是如何给它做成安装盘，还是得不断的找资料和试错。

最终，我找到了一个ISO烧录到U盘的万能工具Rufus，~~真的非常好用强烈推荐~~，用它我成功制作出了第一块能用的安装盘。
然后，经过一番周折，在老旧的笔记本上装上了Ubuntu16.04桌面版。至此，我成功积累了设备上的技术。

### 网络

网络层面的技术积累，得从游戏Minecraft(我的世界)谈起，当时我沉迷我的世界游戏，但是单人实在无聊，想着跟好友联机。
但是中国互联网的环境我们都知道————一个大内网，实现联机可谓是如登蜀道，翻遍网上的各种教程，有教蛤蟆吃~~（hamachi）~~的、有教花生壳的......
可谓是五花八门，除了用花生壳，总之其他软件我就没成功过，可是花生壳的效果也十分不理想。有人可能会说用樱花映射（Sakura frp），6年前还没有这些东西呢~~虽然好像听说有企划~~。

为了获得良好的游戏体验，我几乎翻遍了MCBBS中的联机教程，最终找到一篇内外网开服教程。教程讲述了如何进入电信的光猫去设置端口映射。于是我算是找到了突破口——进入光猫超级管理页面。
光猫是华为的而且根据型号去找超级密码的获取教程没一个对应的，所提供的工具都无法打开telnet端口，这就很让我绝望。
但是我不甘放弃，经历2个星期的寻找，最终找到了什么组播工具，成功地打开了光猫的telnet端口，从中下载到了配置文件，经过解码最终得到了超级管理员的密码，成功建立了映射。

在这之后，我又整上了DDNS。至此，成功将家里的内网与外网打通了，愉快地开起了Minecraft服务器，和基友快乐联机。

### Nginx

装上了Ubuntu server,有了外网环境，我开始研究如何建立一个web站点，经过多方查找，结合手上机器的性能，我觉得应该使用一个叫Nginx的玩意，
~~(别和我说宝塔面板和Apache，当时我根本没找到一点教程，还是初中生，认知能力较浅)~~ 于是乎我又去看了Nginx的教程，发现是真的博大精深，不是当时我所能看懂的，
但是我所求的也不是什么高级功能，我决定照样画葫芦试试,照着教程开始配置nginx.conf，一通照搬猛如虎啊，感觉自己可行了
。改完一跑啊，原本的welcome都没了，404也见不到了。就这样折腾了一个月，模模糊糊的对nginx理解了大概有了一定的对象思想，然后因为学业压力，暂时搁置了。

直到最近，大学的我重新拾起了建个人博客的兴趣，看到了一篇[教程](https://zhuanlan.zhihu.com/p/58654392)，加上多年来的沉淀，我终于明白了正确使用Nginx的方式:cry:conf文件几乎完全不用动……

## 行动

### Hexo

使用Hexo其实是一种偷懒，本来最初我是想自己学习web开发来自己写一个个人主页的，
但是后来当我向我学前端的姐姐提出了要搭建个人博客的想法，并试图白嫖引擎时，她向我指出了[Hexo](https://hexo.io/zh-cn/index.html)。
在看了相关教程和Hexo的文档后，觉得确实容易上手，这里要特别感谢此博客所用主题[Stun](https://theme-stun.github.io/docs/zh-CN/)提供了不仅主题，
而且还有Hexo原版的配置教程，甚至还有第三方已经辅助优化的教程，这种堪称小白级的教程，真的让我省了不少功夫。

在稍微学了下npm的相关知识后，当我将`npx hexo d`按下之后，博客的雏形就形成了，让我切实的体会到了有成果的成就感，那是一种难以言表的快乐，
比打游戏还来得让人舒爽与充实，这么多的时间并没有白费。

_你可以通过[~~此处(Deprecated)~~](https://yurzi.github.io)来访问我部署在GitHub上的同样内容_

### 域名与Https

域名还是比较容易获得的东西，就是要吃几日土，为了梦想还是值得的。

除去域名，为什么要折腾https呢？因为我想将站点部署到自己的服务器上，这样可以不必要使用在线图床，而使用服务器上的图片，~~_就是闲着慌_~~。

https的关键就是申请证书，基于我在自己搭建科学上网工具上的经验，我立刻想起了Let's Encrypt，顺着这个线索也就自然地找到了[acme.sh](https://github.com/acmesh-official/acme.sh)。
acme的使用的教程还是比较多的，以及其提供的文档也很丰富，我照猫画虎也很快上手并申请到了证书。

申请到证书之后就是讲证书部署到nginx上，一开始我是照着网上一个看着很简单的教程来做的，但是效果并不是很好 ~~_（完全不能用）_~~:sweat_smile:，
最终acme的文档给出了一个优质[教程](https://www.cyberciti.biz/faq/how-to-configure-nginx-with-free-lets-encrypt-ssl-certificate-on-debian-or-ubuntu-linux/)，结合着这篇文章，最终配置成功了。

~~_最后说成功其实并没有成功，因为国内域名备案后才能解析到国内的服务器空间，而且运营商还限制相关端口，备案对于我难度过大，而通过国外服务器空间来搭建反向代理还不如将站点整个部署到国外的服务器上，于是乎就这样了_~~

## 总结

经过这长达6年断断续续的准备和研究，最终梦想得以实现，令我内心感到由衷的喜悦和充实，再一次让我更加肯定自身的个人价值，提升了我的自信；
同时，在这个过程中，我也学习并掌握了很多技术，虽然可能只是一点皮毛，但也确实拓宽了视野，提升了能力。

最后我要由衷地感谢撰写教程和文档的朋友，你们的分享精神，让许多像我这样的人得以收益，得以去实现自己的梦想。

（End)