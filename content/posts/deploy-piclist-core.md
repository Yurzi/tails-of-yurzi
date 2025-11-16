---
title: 部署 PicList-Core
date: 2025-11-17T05:37:29+08:00
lastmod: 2025-11-17T05:37:29+08:00
author:
  - Yurzi
  - Lily
description: 关于如何部署和配置 PicList，并使用其 server 模式
keywords:
  - PicList
  - PicList-Core
  - Deploy
tags:
  - Self-host
  - Image
  - Hugo
  - Linux
draft: false
disableCounter: false
---
近日，咱案牍劳形，且书录日繁，致疏于侍弄私属之务。兼以多设备并用，乃思统其规约，简其流程，遂起设图片上传服务之念，望统多端于一端。

然何者可任此重职？咱念 PicList 之便利，遂择 PicList-Core[^1]。

## 思之
依托鲸鱼「Docker」之便，咱可轻取其镜像，速建其容器，须臾间 PicList-Core 便可俨然就职，勤勤恳恳，此非难焉。

但因咱之矫情，于十美分云「Tencent Cloud」上拥多个存储之库，而 一只 PicList-Core 只可处理一桶。咱望统多端于一端，而此却难统多后端于一端，一时错愕，顿感棘手。遇此困，梨鲤谏曰：「虽二者趋同，但仍有异，可借「Nginx」之力，取异协同，于前端路由，使二者幻为一端，此结可解」。

思念至此，念头通达，遂置之。
## 置之
### 置 PicList-Core
先以常法启 PicList-Core 容器，复入其内，行 CLI 之令以调其参。咱之配置如下：
{{<collapse>}}
```json
{
  "picBed": {
    "current": "tcyun",
    "uploader": "tcyun",
    "tcyun": {
      "version": "v5",
      "secretId": "<secretId>",
      "secretKey": "<secretKey>",
      "bucket": "<bucketId>",
      "appId": "<appId>",
      "area": "<bucketArea>",
      "endpoint": "",
      "path": "",
      "webPath": "",
      "customUrl": "https://examples.url",
      "options": "",
      "slim": false
    }
  },
  "picgoPlugins": {},
  "buildIn": {
    "compress": {
      "quality": -1,
      "isConvert": true,
      "convertFormat": "webp",
      "formatConvertObj" : {
          "webp": "webp",
          "avif": "avif"
      },
      "isReSize": false,
      "reSizeWidth": 500,
      "reSizeHeight": 500,
      "skipReSizeOfSmallImg": false,
      "isReSizeByPercent": false,
      "reSizePercent": 50,
      "isFlip": false,
      "isFlop": false,
      "isRotate": false,
      "rotateDegree": 0,
      "isRemoveExif": true
    },
    "rename": {
      "format": "{Y}/{m}/{md5-16}-{filename}",
      "enable": true
    },
    "skipProcess": {
      "skipProcessExtList": "zip,rar,7z,tar,gz,tar.gz,tar.bz2,tar.xz"
    }
  },
  "skipProcess": {
    "skipProcessExtList": "zip,rar,7z,tar,gz,tar.gz,tar.bz2,tar.xz"
  },
  "rename": {
    "enable": true,
    "format": "{Y}/{m}/{timestamp}-{filename}"
  }
}
```
{{</collapse>}}
权衡全图片之质与容量之缺，择「WebP」为统一格式，且禁 PicList-Core 压缩之特性。且借MD5之便，行去重之事。

### 置 Nginx
遵 PicList 之设定，借其 `configName` 于 Nginx 中反代路由之。片段如下：

{{<collapse>}}
```nginx
location / {
  proxy_http_version 1.1;
  proxy_set_header Host $http_host;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_connect_timeout 3m;
  proxy_send_timeout 3m;
  proxy_read_timeout 3m;
  client_max_body_size 0;

  if ($arg_configName = 'Assets') {
    proxy_pass http://piclist-assets;
  }
  if ($arg_configName = 'AssetsMD') {
    proxy_pass http://piclist-assets-md;
  }
}
```
{{</collapse>}}

## 结语
今得此器，可统御众端，解案牍之困。虽务繁而心不乱。不可不谓念头通达，豁然开朗。自建之乐，在于以己之智解己之困，此中快意，非外人可道也。

今执此笔，录此心得，愿为同困者鉴。

{{<spoiler>}}才不是水文章喵，哼！～ฅ(•ㅅ•❀)ฅ{{</spoiler>}}

## References
[^1]: [Github: Kuingsmile/PicList-Core](https://github.com/Kuingsmile/PicList-Core)
