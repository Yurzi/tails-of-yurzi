---
title: "萌萌计数器 Moe Counter"
date: "2024-05-16T15:19:42+08:00"
lastmod: "2024-05-16T15:19:42+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "如何将Moe Counter部署到自己的服务器上, 并集成进 Hugo 博客"
keywords:
  - Deploy
  - Moe Counter
  - Hugo
tags:
  - Linux
  - Hugo
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

## 初遇

由于经常在互联网的深海里刨东西，所以咱经常会找到一些个人网页或者开源项目里有几只兽耳娘举牌牌的图片，时常觉得可爱并且自己也想在博客里集成一个。
但是由于不知道项目用途和名称，以及咱社恐不敢询问，直到最近才依据「蛛丝马迹」在 Github 上找到里该项目 —— Moe Counter {{<cref "1" "#cite-1">}}

于是很快啊, 咱立刻就开始着手部署这个有趣的小工具了，但是在整个部署过程中确实遭遇了许多坎坷，着实让咱喝了一壶，于是在此记录。

## 部署

由于 Moe Counter 项目是有后端的，所以需要部署在一个服务器上，虽然在 Github 上也有大佬提供的白嫖Replit{{<cref "1" "#cite-1">}}、
CloudFlare{{<cref "2" "#cite-2">}}{{<cref "3" "#cite-3">}}
和Vercel{{<cref "4" "#cite-4">}} 的方案，但考虑到自己有着一些空闲机子的因素，于是决定自己部署。

首先咱的部署环境为 `Debian 12.5`，安装 `Nginx` 等内容不展开了，
为了能应对未来较大字典查询的应用场景，决定使用 MongoDB 作为数据库后端。{{<spoiler>}}于是就因为过于自信而翻车XD{{</spoiler>}}

### 安装 MongoDB

由于 MongoDB 一些众所周知的问题，Debian 的仓库里不再提供相关的软件包，所以只能参考官方自己给出的安装手册{{<cref 5 "#cite-5">}}进行安装了。

```shell
# 前置依赖
sudo apt-get install gnupg curl
# 导入签名
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
# 导入第三方软件源
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
# 更新软件源索引
sudo apt-get update
# 安装
sudo apt-get install -y mongodb-org
# 启动
sudo systemctl enable --now mongod
```

然后由于 Moe Counter 项目的需要，需要开启MongoDB的验证并创建相应的用户。

先创建相关的用户,

```shell
# 连接db
mongosh

# 创建管理用户
test> use admin
admin> db.createUser({
  user: "admin",
  pwd: "ciallo",
  roles: [
    {role: "root", db: "admin"}
  ]
})
# 创建 Moe counter 用户
admin> db.createUser({
  user: "moe-counter,"
  pwd: "<your-passwd>",
  roles: [
    {role: "readWrite", db: "moe_counter"}
  ]
})
admin> quit
```

然后编辑 `/etc/mongod.conf` 在其中的修改 `security` 如下来开启用户验证，

```yaml
security:
  authorization: enabled
```

然后使用 systemd 来重启数据库，即可通过用户名密码的方式连接数据库了。

```shell
sudo systemctl restart mongod
```

为什么要这样做？因为经过测试发现在不开启验证的情况下，即使存在用户也无法使得 Moe Counter 正确的连接数据库进行操作。

### 部署 Moe Counter

在机器上找个位置，例如 `/srv/Moe-Counter`，按照作者所说{{<cref "1" "#cite-1">}}来部署项目，由于Debian的官方仓库中 `yarn` 被更名为 `yarnpkg` 所以在使用 `apt` 安装时需要注意。

同时为了方便管理和安全，个人将整个 Moe Counter 项目分配给 `www-data` 用户运行，同时使用systemd进行管理。

```conf
# /etc/systemd/system/moe-counter.conf

[Unit]
Description=Moe Counter Service
After=network.target mongodb.service

[Service]
User=www-data
WorkingDirectory=/srv/Moe-Counter
Environment="DB_URL=mongodb://moe-counter:<your-passwd>@127.0.0.1/moe_counter"
ExecStart=/usr/bin/yarnpkg start
Restart=always

[Install]
WantedBy=multi-user.target

```

最后将Nginx的反向代理配置好，一个萌萌计数器就可以使用啦！下面的是 Demo 展示

**meoboour**
{{<moe-counter "demo" "meobooru">}}

**asoul**
{{<moe-counter "demo" "asoul">}}

**rule34**
{{<moe-counter "demo" "rule34">}}

**gelbooru**
{{<moe-counter "demo" "gelbooru">}}

## 与 Hugo 集成

首先是对于模板的修改，根据不同的主题可能有不一样的位置，
咱插入了以下的代码，需要注意的是，如果代码所在的位置为使用 `partialCached` 的方式导入的话会出现问题，所以请修改为 `partial` 导入。

```html

<!--对于主页-->
<div style="align-items: center; display: flex; justify-content: center">
  <img
    src="https://count.yurzi.net/get/@{{ replace site.Title " " "-" | lower }}"
    alt="tails-of-yurzi-visitor-counter"
  />
</div>

<!--对于其他页面-->
{{- if not (.Param "disableCounter") }}
  {{- if not .Layout | and .IsPage }}
    <div style="align-items: center; display: flex; justify-content: center">
      <img
        src="https://count.yurzi.net/get/@{{ replace .Title " " "-" | lower }}"
        alt="{{ replace .Title " " "-" | lower }}-visitor-counter"
      />
    </div>
  {{- end }}
{{- end }}

```

咱还写了一个 `shortcode` 方便在文章中直接使用

```
{{- if .IsNamedParams }}
  {{ $theme := (.Get "theme") | default "moebooru" | safeURL }}
  {{ $align := (.Get "align") | default "center" | safeCSS }}
  {{ with .Get "id" }}
    <div style="align-items: center; display: flex; justify-content: {{ $align }}">
      <img
        src="http://count.yurzi.net/get/@{{ . | safeURL }}?theme={{ $theme }}"
        alt="{{ . | safeHTMLAttr }}-counter"
      />
    </div>
  {{ end }}
{{- else }}
  {{ $theme := (.Get 1) | default "moebooru" | safeURL }}
  {{ $align := (.Get 2) | default "center" | safeCSS }}
  {{ with .Get 0 }}
    <div style="align-items: center; display: flex; justify-content: {{ $align }}">
      <img
        src="http://count.yurzi.net/get/@{{ . | safeURL }}?theme={{ $theme }}"
        alt="{{ . | safeHTMLAttr }}-counter"
      />
    </div>
  {{ end }}
{{- end }}
```

## 总结

至此，咱终于也有属于自己的萌萌计数器哩🎉。

## 参考文献

{{<cite 1 "[1] GitHub: journey-ad/Moe-Counter: 多种风格可选的萌萌计数器" "https://github.com/journey-ad/Moe-Counter">}}
{{<cite 2 "[2] champhoon, moe-counter-cf：将萌萌计数器部署到 Cloudflare Workers" "https://champhoon.xyz/note/moe-counter-cf/">}}
{{<cite 3 "[3] Shirakii, 将萌萌计数器部署到 Cloudflare Workers" "https://www.shirakii.com/post/moe-counter-cf/">}}
{{<cite 4 "[4] Github: grbnb/moe-counter-vercel: vercel平台一键部署Moc-Counter" "https://github.com/grbnb/moe-counter-vercel">}}
{{<cite 5 "[5] Install MongoDB Community Edition on Debian" "https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/">}}
