---
title: "记三星平板SM-T805C刷机并使用LineageOS"
date: "2022-08-16T23:34:22+08:00"
lastmod: "2024-03-27T23:34:22+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "三星平板刷机，然后装上LineageOS"
keywords:
  - Android
  - Samsuang
  - Lineage
  - Flash
  - Root
tags:
  - Android
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

## 心血来潮

暑休于家，仍忙于网页设计之大作业，亟需多屏幕之支持。见咱窘境，父掏箱底得一三星平板，双手呈于咱，曰：「吾观汝之困，焦头烂额，何不尝用之？」。咱无言，心中略欣慰，脑中百转，遂生一计。于是以SpaceDesk驭之，甚喵，心中感叹：「此近十年之旧物仍有不逊于今某粮食平板之硬件配置，三星之理念不可谓不超前。」

此后，大作业完结矣，此板又赋闲于咱手边。咱日可用余光窥其，其亦窥咱，于是咱心中愧疚（bushi，便欲更其内里，重塑其风骨。虽咱可施以「时光逆转」之术，令其重回诞生之初之样貌。可因其为中国特供版，其内藏有某度之顽疾，令咱膈。于是乎，咱决定对齐施以「筋骨重塑」之术，刷之。

## 冷静分析

此方领域为咱从未涉足之地，对如何刷之可谓一头雾水，遂以科学之法投身与全球互联网知识之广袤海洋，于其中狗刨式整理遂得思路如后，汝若欲重走咱之路，需备以科学或魔法之术。

先以博大精深之中文为引，可得诸多结果，可其所适用目标之新，咱骇然。但经过咱之不懈努力，终于中文互联网中刨出了可用的[文章](https://onfix.cn/course/165?bid=3&mid=2765)。汝便无需再经历被各式信息所贯穿的痛苦惹。有此文章为引，再辅以其他搜索，咱可知适用于咱之平板的「筋骨重塑」之术的大概流程。

1. 安装驱动。
2. 使用Odin连接进入Download模式的设备。
3. 双清乃至多清
4. 使用ROM四件套刷之

## 狂热分析

至此，咱已知如何进行基础「筋骨重塑」之术，但追求极致的咱不会满足于此，欲彻更其血肉并作其真主。遂使用中洋文交迭搜寻，获二宝藏：[XDA-Developers](https://forum.xda-developers.com/)与[onfix](https://onfix.cn/rom)。前者有各路爱好者大神之教诲，后者有便捷的rom下载渠道，虽难以白嫖，但一元之资咱觉得还是可以接受的。

不过，于前时，咱并不知此二宝藏，只是不知方向的乱窜，此按下不表，从xda的这篇[文章](https://forum.xda-developers.com/t/rom-unofficial-10-lineageos-17-1-for-samsung-galaxy-tab-s-sm-t700-sm-t705-sm-t800-sm-t800-sm-p600.4270943/)中可以知道血肉更替之法，同时想必没人不会没听闻过TWRP和Magisk的大名吧。总结思路如下：

1. 以上面的方法刷入原厂的固件
2. 刷入匹配的TWRP
3. 双清乃至多清
4. 通过TWRP刷入LineageOS
5. 刷入Magisk

## 仔细准备

在有合适理论指导之后，那便是开始实操，但在此之前，需要准备所需的所有材料到一个文件夹内，同时要告诫自己养成备份的好习惯。所有材料的下载地址都贴于此，且遵循能官方渠道下载便官方渠道的原则：

- [三星驱动](https://developer.samsung.com/android-usb-driver)
- [Odin3.09](https://odindownload.com/download/Odin_v3.09.zip)(似乎这个版本的兼容性更好?)
- 固件：https://samfw.com/firmware/SM-T805C 或者 https://onfix.cn/rom/335345
- [TWRP](https://twrp.me/samsung/samsunggalaxytabs105lte.html)
- [LineageOS(deprecated)](https://forum.xda-developers.com/t/rom-unofficial-10-lineageos-17-1-for-samsung-galaxy-tab-s-sm-t700-sm-t705-sm-t800-sm-t800-sm-p600.4270943/)|[Self build](#自给自足)
- [Magisk](https://forum.xda-developers.com/t/rom-unofficial-10-lineageos-17-1-for-samsun-galaxy-tab-s-sm-t700-sm-t705-sm-t800-sm-t800-sm-p600.4270943/)

**切记，自己准备好ABD系列工具，并配置妥当，推荐前往谷歌官网[下载]([Android 调试桥 (adb) | Android 开发者 | Android Developers](https://developer.android.com/studio/command-line/adb?hl=zh-cn))**

## 开始施术

### 安装驱动与ADB，并启用USB调试

如果能正常启动平板，汝最好先进入开发者模式打开USB调试，已做好万全的准备，虽然咱经过测试发现并不需要，但是还是做一下为好呢。同时顺便开启OEM解锁，虽然咱手上的平板并不需解锁Bootloader，但打开也没有坏处。

驱动的安装和ADB的配置，想必汝也应该能自己胜任。

### 退出所有账户并备份

如果汝的平板上有重要的资料，建议先进行备份，备份的方式汝可以随喜好选择，比如使用ADB或者SD卡。同时请退出所有的账户，据说可以防止数据加密什么的，但是咱的平板早就恢复过出厂设置也担心这个，同时这个型号的平板也没这个功能（_＾-＾_）.

若汝是一个谨慎的人，也可以做好备份然后恢复出厂设置后在进行下面的步骤。

### 进入下载模式

进入下载模式的物理方法是：关机后，按住**音量-加电源键加Home键**，音量-是靠近电源键的那一个，汝可以先按好其他键再按电源键哦。进入后，不顾劝阻，直接继续，那就进入下载模式惹。

或者汝可以使用优雅的ADB进行`adb reboot download`

**退出下载模式方法是按住「电源键和音量-」**

### 使用Odin进行施法

对于如何启动Odin其实没有一个明确的时间，在插入前在插入后都可以，但是汝需要检查是否已经正确连接，如果正确连接，在Odin的消息提示框处会有消息提示，同时在上方的方框的地方有显示现在连接设备的COM端口。

#### 刷入原版固件

汝需要解压下载的三星原版的固件包，一般会有四个文件，然后将它们以名称匹配的方式分别置入Odin的BL、AP、CP、CSC。这些名称在解压出的文件的文件名上也存在。

若汝使用的Odin版本不同则这些按钮显示的英文也不同，请谨慎操作，这里特地的给一个类似的油管视频以供参考：[这里](https://www.youtube.com/watch?v=blcVfzEUk2A)。

在刷入完后，汝最好确认是否能够正常启动，但是咱当时莽的一并没有这么做(´。＿。｀)。

#### 刷入TWRP

再次进入下载模式。对于twrp汝需要的tar文件，将其置入到AP的位置，记得去掉Odin的reboot框，不然汝之辛苦就会随着屏幕一亮，欻的付之东流。然后只能悻悻地重新刷一遍。

在刷写完成后，汝只需要手动退出下载模式，然后长按**电源键和音量+和Home键**就可以进入recovery模式了。只要打开过一次twrp，那么它就不会被干掉惹。

在TWRP的设置中记得把屏幕设置为永不休眠。如果汝是非常谨慎之人，可以尝试进入系统，然后在twrp里进行备份。

汝操作完后别忘记双清乃至五清

### 刷入LineageOS

呼呼，现在刷入twrp的三星平板已经是如同被抬上手术台的病人，无论汝怎么对它，它都没有办法反抗惹，汝现在是不是很兴奋。如果汝没有别的追求的话，其实已经可以结束了。但咱还要更换其血肉——刷入LineageOS。

进入twrp，然后将下载好的zip镜像通过数据线传入到内置存储中，再点击"install"，选中对应的zip文件然后安装。

这样LineagOS就装上惹。

### 刷入Magisk

一般来说，每做完一步都需要进行可用性检查，并做好备份。但咱一般一步到位，可是还是建议汝做好备份。

对于Magisk的安装，网上的教程都说zip包，可是现在官方不提供zip包的下载，但是事实上只需要把apk的后缀改为zip便可以了。进入twrp，install的故技重施，Magisk就刷上了。汝可能会疑惑那Manager呢？其实只要进入系统后再安装改名前的apk包就有管理器了。

## 技术总结

在刷完这一条龙服务后，这块平板已经脱胎换骨，接下来的路途就是「海阔任鱼跃、天高任鸟飞」了。总的来说对于安卓设备的刷机遵循下面的流程：

1. 解锁Bootloader
2. 刷写最新的官方固件
3. 刷入TWRP
4. 刷入第三方OS[可选]
5. 刷入Magisk[可选]

但需要注意的是，所有的这些都需要按手机型号选择，并不是越新越好。

## 题外话

汝肯定听闻过大名鼎鼎的Xposed，但在本文发表的时间，Xposed早已停止更新很久惹。现在还在更新的是[Lsposed](https://github.com/LSPosed/LSPosed)。

再者汝可能也听说过面具的riru模块，但是现在riru也将被Magisk提出的zygisk取代，可以查看Magisk的设置开启。

再者就是Kernel的刷写，由于咱对于魔改内核来使用额外功能并不狂热，且非常的好吃懒做，于是并没有进行研究。反而是对于将Android设备当作类Linux服务器来跑非常感兴趣，所以在此推荐甚喵的项目叫[Termux](https://github.com/termux/termux-app#github)

### 自给自足

随着时间的推移，很多时候发现一些链接中的内容不再有效，这种时候如果还想前进就难免的需要自己自足。
在2023年4月23日，不知道为什么原有的非官方的LineageOS ROM作者删除了ROM包。这种时候就需要自己编译啦。以下是参考资料:

- [LineageOS Official Wiki](https://wiki.lineageos.org/devices/chagalllte/build)
- [Mystery's Guide](https://mystery00.github.io/2017/04/23/%E7%BC%96%E8%AF%91LineageOS/)

简单总结一下，便是拉取LineageOS的官方源码，然后加上自己设备相应的Vendor即可。
