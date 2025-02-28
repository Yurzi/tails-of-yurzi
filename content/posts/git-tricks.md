---
title: 'Git Tricks'
date: "2025-01-16T16:52:38+08:00"
lastmod: "2025-01-16T16:52:38+08:00"
author: ["Yurzi", "Lily"]
description: "一些 Git 使用的小技巧"
keywords:
  - Git
  - Tricks
  - Tools
tags:
  - Tools
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

咱在日常工作生活中时经常会遇到一些奇妙的需求，而在这种危急关头，
Git 总能凭借其丰富的功能满足咱的需求。在这些技巧中不乏有许多使用到裸仓库、Hook 之类的特性。
遂，咱将这些一时间难以想到的 Git 使用小妙招记录在此。

## 同步 Dotfiles

在使用各种工具的时候，总是会有许多针对各个工具的自定义文件，一般称这些文件为「Dotfiles」。
而众所周知，一般的程序员都会在超过三台设备上工作，所以这种时候同步这些配置文件就成为了一个难题。
手动同步吧，也不是不行，但是总是不见得优雅，而且一旦跨平台且有文件发生修改，那就变得更加的棘手了。
所以仔细想想，这种处理文件差异的任务使用 Git 不是正好吗？

使用 Git Bare Repository 可以很好的解决这个问题，
这个方案的最早来源是「Git Bare Repository - A Better Way To Manage Dotfiles」{{<cref 1 "#cite-1">}}。

使用这个方案只需要简单的三步：

1. 建立一个裸仓库。
2. 将dotfiles的信息加入到裸仓库。
3. 创建一个dotfile与存储位置的链接。

### 什么是裸仓库

一般来说，一个常规初始化的 Git 仓库分为两个部分：「工作区」和「元信息」，
其中「工作区」就是存储文件的位置，而「元信息」则是存放于 `.git`文件夹中的内容。
而一个裸仓库，则就是一个只有「元信息」的仓库。

这样的仓库因为没有工作区而无法进行一些工作区才能进行的功能，比如检出、修改和提交等。
但是这也意味着裸仓库将更加关注于存储相关的功能。同时 Git 支持将元信息和工作区分别指定，
这意味着可以在不破坏一个文件夹原有约束的情况下（不引入额外项）的情况下跟踪其变更。

### 创建

为了实践使用裸仓库来管理 Doftiles，首先需要创建一个裸仓库，
并使用一个指定工作区的 Git 命令去操作工作区变更。

```sh
# 初始化一个裸仓库
git init --bare $HOME/.dotfiles

# 创建一个别名
alias dotmgr="git --git-dir $HOME/.dotfiles --work-tree=$HOME/.config"
```

在这里，咱默认将所有的配置文件存放在`$HOME/.config`文件夹下，
并将一些不在这个文件夹下的配置文件也移动到该文件夹下并使用软链接链接会原来的位置。
虽然存在一些更好的方式来管理这些不羁的文件，比如 Home Manager，但是咱也是比较懒的。

### 恢复

在新的环境下恢复也是比较简单的，首先是克隆裸仓库，然后使用别名来操作工作区。

```sh
# 是克隆裸仓库
git clone --bare <git_url> $HOME/.dotfiles

# 创建别名
alias dotmgr="git --git-dir $HOME/.dotfiles --work-tree=$HOME/.config"
```

然后就是简单的使用 checkout，来恢复工作区了。

```sh
dotmgr checkout
```

基于这套流程可以利用 Orphan Branch 来管理不同平台下的配置文件，同时也能方便的同步各个平台下通用的的部分。
另外有些人可能不喜欢在使用 `dotmgr status` 时看到未跟踪的文件，可以通过配置 `status.showUntrackedFiles` 来隐藏这些文件。

## 基于不同文件夹的单用户的多人协作

咱在工作的时候遇到一个问题，咱需要和另一位同事共享一个 Unix 用户在一台开发机上工作，同时咱又需要和同事对同一个项目进行更改，
这种时候自然而然的是想到使用 Git 来完成这种工作流的协同。
使用远程仓库显然是一个很好的选择，但是由于环境的特殊性，导致无法使用外部的远程仓库，而本地搭建一个 Gitlab 又不现实。
于是一些聪明的小伙伴就会直接抢答了「那你用裸仓库啊」。

是了，因为某种意义上 Github 之类的也是使用裸仓库来存储这些信息的，
于是可以通过下面的结构来实现的一个本地的类似于远程仓库的体验。

```sh
./
 |- bare_repo/
 |- local_repo1/
 |- local_repo2/
```

首先是需要初始化裸仓库，用于存储元信息。

```sh
cd bare_repo
git init --bare
```

然后是初始化本地仓库，用于存储工作区，并设置上游分支。

```sh
cd local_repo1
git init
git remote add origin ../bare_repo
git push -u origin main
```

最后是初始化另一个本地仓库，用于存储工作区，并设置上游分支。

```sh
cd local_repo2
git init
git remote add origin ../bare_repo
git push -u origin main
```

或者其实可以直接使用 `git clone` 来创建另一个本地仓库。

```sh
git clone ./bare_repo local_repo2
```

于是就这么简单，咱就可以和同事各自在不同的文件夹下修改内容，然后还能使用 Git 来管理版本和合并差异。

## References

{{<cite 1 "[1] Yutube: Git Bare Repository - A Better Way To Manage Dotfiles" "https://www.youtube.com/watch?v=tBoLDpTWVOM">}}
