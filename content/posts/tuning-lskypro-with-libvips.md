---
title: "使用libvips优化Lskypro的图片处理"
date: "2024-03-28T20:30:31+08:00"
lastmod: "2024-03-28T20:30:31+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "使用libvips优化Lskypro的图片处理，并做一些bug修复"
keywords: [Lskypro, Tuning]
tags: [Tuning]
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

## 起因

一直以来，咱都有写文章的需求，随之而来的的就是媒体内容管理的需求了，对图床的需求自然而然的就出现了，
但使用公共图床服务总有一些痛点，要不是限制图片大小，要不就是限制容量。
而自己毕竟有着 All in Boom 的资源，所以考虑自建一个图床。

在调研了各种自建图床的方案之后，Lskypro (兰空图床)以其广泛的使用率和更多的生态支持成为了咱的选择。
于是在经过一系列和 PHP 项目艰难险阻的部署搏斗之后，
咱不出意外的发现了，该图床在上传时经常出现上传提示服务端出错，但图片却已经成功上传了的现象，
以及在进行并行上传时出现缩略图错配的现象。于是乎一场捉虫之旅就开始了。

## 源码结构分析

Lskypro 是基于 PHP Laravel 框架开发的，所以根据其MVC的设计模式，
很容易找到图片上传的相关处理逻辑在 `app/Services/ImageService.php` 文件里，
不过虽然咱没学过 PHP，但还是看出来其中最关键的函数 `ImageService::store` 是负责处理上传后的图片的。
主要关注这个函数里面的这些行。

```php
public function store(Request $request): Image {
	$file = $request->file('file');
   // ...
   	// 图片处理
  		$handleImage = InterventionImage::make($file)->save($format, $quality);
  		$file = new UploadedFile($handleImage->basePath(), $filename, $handleImage->mime());
  		// 水印
  		$file = new UploadedFile($watermarkImage->basePath(), $file->getClientOriginalName(), $file->getMimeType());
   // ...
  		// 存储图片
  		$filesystem->writeStream($pathname, $handle);
  	// ...
   // 生成缩略图
   $this->makeThumbnail($image, $file);
}

public function makeThumbnail(Image $image, mixed $data, int $max = 400, bool $force = false): void {
//...
	$img = InterventionImage::make($data);
   $img->fit($width, $height, fn($constraint) => $constraint->upsize())->encode('png', 60)->save($pathname);
//...
}
```

## 奇奇怪怪——多线程上传

首先咱决定先解决缩略图错配的问题，一开始咱以为是 Hash 冲突导致的，
但是经过多次测试之后，咱发现只有多张图在同时上传的时候会出现这个问题。

注意到源码中的缩略图生成是调用了 `ImageService::makeThumbnail` 来处理的，
观察函数入参，发现其对应的缩略图文件来自于变量`$file`

跟踪整个上传过程中 `$file` 的变化，最值得关注的在与图片处理流程中对其的新赋值。
通过阅读文档之后发现 `UploadedFile` 对象的构造方法的第一个入参代表了其 Handle 的文件的位置。

于是打印 `$handleImage-> basePath()` 发现其值为固定的 `$format` 变量的值，
通过阅读文档之后得知，该方法会返回图片的最后路径，所以可以发现其问题的根源在于上面的 `save` 中，
其使用一致文件名来暂存处理后的图片。

由于图床的多线程上传是通过前端多次调用接口实现的，
而 PHP 后端在处理请求时会用一个新的 worker 线程来处理脚本，从而实现多线程上传。
但这就和使用一致文件名产生了冲突，当上一个请求并未结束到生成缩略图而下一个请求已经到达图片处理的部分，
这就导致了多线程之间的 **资源冲突** 从而导致了缩略图的错配！

修复的方法也很简单，就是将 `save` 函数的第一个参数改为 `$filename` 即可。
同时这样修改还修复了一个更关键的问题，那就是图片格式转换不生效的问题。
因为`save`方法会通过文件扩展名来判断存储的图片的格式从而做格式转换，
而原来的入参并没有文件拓展名，所以导致文件格式转换并没有生效😅!

## 性能怪兽——图片处理

虽然上文修好了多线程冲突的问题，但是咱发现图片上传服务端出错的问题还是没有好，
于是咱注意到在 Github 的 issue 里有人提到了因为内存不足而导致的图片上传失败，
同时结合作者在处理缩略图调大了脚本的运行内存限制和咱上传时虽然失败但仍成功上传了图片的表现来看，
应该是在处理缩略图的时候出现了异常。咱意识到缩略图处理可能是非常消耗性能的。
于是在网上搜素相关的内容，发现确实有人指出了这种问题{{<cref 1 "#cite-1">}}。
而且非常不巧的是，这个图床的实现也是使用的 ImageMagick。

于是经过简单的思考，和利弊权衡，以及考虑到自己几乎没有的 PHP 编程经验，
咱决定使用 `libvips` 来优化 ~~（劣化~~ 这块图片处理的逻辑。

首先是轮子的选用，经过简单的搜索很容易就可以找到`php-vips`{{<cref 2 "#cite-2">}} 这个库。
在开发环境里装上`php-vips`，将相关的图片处理的逻辑代码改为以下内容。

首先是图片格式转换，这里存在的一个问题是如果用户使用了webp作为目标格式而图片大小过大，就会导致保存失败，
于是咱选择了最简单的回落到原图的方法 ~~同时很偷懒的没做质量修改~~，
如果汝觉得还是做一下质量修改可以将 上面的的 `try` 块里的代码再写一次，但是使用 `$file-getClientOriginalName()`

```php
// 获取拓展名，判断是否需要转换
	                  $format = $format ?: $extension;
	                  $filename = Str::replaceLast($extension, $format, $file->getClientOriginalName());
	                  $is_success = true;
	                  try {
	                      $handleImage = VipsImage::newFromFile($file, ['access' => 'sequential']);
	                      $handleImage->writeToFile($filename, ["Q" => $quality]);
	                  } catch (\Throwable $e) {
	                      // 或许目标格式不合适，回落到原图
	                      unlink($filename);
	                      $is_success = false;
	                  }
	                  if ($is_success) {
	                      $file = new UploadedFile($filename, $filename, mime_content_type($filename));
	                      // 重新设置拓展名
	                      $extension = $format;
	                  }
```

然后是重量级的缩略图生成的逻辑，改为如下内容。这里使用了 webp 来作为缩略图格式，似乎相较于原来的 png 来说更好一些，
不过这也意味着需要顺带修改作者在 `Image::getThumbnailPathname` 里的硬编码了。
如果你已经是有一些缩略图了，那就会导致兼容问题了，那建议还是把 `webpsave` 改为 `pngsave` 来更加的合理🥰

```php
@ini_set('memory_limit', '512M');

$img = VipsImage::newFromFile($data, ['access' => 'sequential']);

$width = $w = $image->width;
$height = $h = $image->height;

if ($w > $max && $h > $max) {
    $scale = min($max / $w, $max / $h);
    $width  = (int)($w * $scale);
    $height = (int)($h * $scale);
}

$img = $img->thumbnail_image($width, ['height' => $height]);
$img->webpsave($pathname);
```

## 总结

至此对于 Lskypro 的 bug 修复和性能调优就结束了，咱也收获了一个更好用的图床，
也能轻松的完成大佬文中提到的高分辨率图片的挑战{{<cref 1 "#cite-1">}}。
不过这对于自己这个 PHP 零基础的杂鱼来说还是太累了。同时也对国内的一些开源项目的代码质量感到担忧和对国内开源环境的现状感到担忧。

为什么不提交PR？这主要是出于咱的某种社恐，毕竟这些代码是对 PHP 零基础的小白写出来的，非常的丑陋。
此外是咱观原项目的活跃状态似乎是有些难以处理PR的状态了😅。于是咱还是自己 fork 了一份来用{{<cref 3 "#cite-3">}}。

## 参考文献

{{<cite 1 "[1] 记一次 ImageMagick jpeg 缩放性能调优" "https://tomwei7.com/2020/10/11/imagemagick-tuning/">}}
{{<cite 2 "[2] php-vips" "https://github.com/libvips/php-vips">}}
{{<cite 3 "[3] Lskypro: Yurzi favor" "https://github.com/Yurzi/lsky-pro/tree/yurzi-favor">}}
