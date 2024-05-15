---
title: "Visidata 简要介绍"
date: "2024-04-04T22:06:58+08:00"
lastmod: "2024-04-07T15:44:58+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "简单介绍Visidata的使用"
keywords:
  - Visidata
  - Guide
tags:
  - Tools
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

## 前言

在日常的工作中，总是需要浏览实验结果的数据表格，其体量大多非常巨大，
而在 Linux 的环境下，常规的 Excel 图形程序总是加载很慢 ~~(可能咱电脑太垃圾了)~~，
而且有着容易崩溃的风险，于是偏好终端界面 (TUI) 的咱就找到了这个工具 —— [Visidata](https://www.visidata.org/)，
一个快速的基于 TUI 的，支持多种格式及有着丰富功能的数据表格处理工具。

## 安装

由于咱使用的是 ArchLinux 发行版所以可以直接从系统包管理器里安装，对于其他的平台，可以使用 `pip` 的方式进行安装{{<cref "2" "https://jsvine.github.io/intro-to-visidata/the-big-picture/installation/">}}。

{{<collapse summary="Lily">}}
不会有人连如何从pip安装应用都不会吧，不会吧～不会吧～，那可真是 zako喵～ zako喵～
{{</collapse>}}

## 使用

就如何使用这块官方给的文档{{<cref "1" "#cite-1">}}{{<cref "2" "#cite-2">}}其实有非常详细的讲述，咱这里只是将咱经常会用到的功能做了一个汇总。

首先是界面的操作逻辑其实类似于 vim，所以能熟练使用 vim 的大家都能很快的上手 ~~君tui本当上手~~。

然后是一些通用的操作：

- `!` : 摘出选中的列
- `+` : 在当前列上附加计算
- `<space>`: 打开命令输入窗口
- `:` : 打开正则搜索窗口

### 打开表格

对于简单的 csv 格式的表格，只需要简单的是使用

```shell
vd <datasheet>.csv
```

就可以轻松的打开。但是由于实验数据过大，咱一般使用 xlsx 的表格，这时候就需要按照官方的指引{{<cref "3" "#cite-3">}}，先安装相应的 python 拓展 `xlrd`和`openpyxl`才能正确打开了。
同时在打开后需要选择对应的 `sheet` 才能和 csv 一样直接打开数据视图。

### 按列排序

对于选中的列，只需要按下 `[` 或者 `]` 就可以进行升序或者降序排列，visidata还支持多关键字的排列，这种高级功能还是翻看文档罢（无慈悲，
值得注意的是，可以使用 `#` 将一列数据标记为是 `numeric`，毕竟默认的排序不是按数字序排的。

### 筛选

对于选中的列，按下 `|` 使用正则匹配来匹配选中对应的关键字的行，然后使用 `"` 来将这些列复制到新的临时表格里就完成了筛选的功能。

### 统计

在 Visidata 里，有许多高级的统计用法。但是最简单的就是在任意列按下 `shift+f` 就可以继续关键字的频率统计。
使用 `+` 可以为当前列附上一些函数从而在后续的频率统计中使用，当然你也可以使用 `z+` 来在数字列上快速的调用一些运算函数。

## 总结

Visidata 总的来说是一个非常强大的工具，但是很多功能还有待发现和熟练使用。
同时个人觉得这种使用字符界面的表格工具，有一种回到上世纪的氛围感。

同时咱也发现，现代计算机中工作中的绝大多数需求对于计算机性能的消耗其实可能并不需要很高，
但是丰富的图形界面使得开销大大的增加哩。

## 参考文献

{{<cite 1 "[1] Visidata: Quick Reference" "https://www.visidata.org/man/">}}
{{<cite 2 "[2] Visidata: An Introduction to VisiData" "https://jsvine.github.io/intro-to-visidata/">}}
{{<cite 3 "[3] Visidata: Opening Files" "https://jsvine.github.io/intro-to-visidata/basics/opening-files/#tabular-data">}}
