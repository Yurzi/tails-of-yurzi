---
title: '为博客实现加密功能'
date: "2025-02-13T16:03:58+08:00"
lastmod: "2025-09-01T14:54:29+08:00"
author: ["Yurzi"]
description: "通过简单的方式为Hugo博客实现加密功能"
keywords:
  - Blog
  - Encryption
  - Hugo
tags:
  - Blog
  - Hugo
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

## 风云变换

一直以来，咱认为，咱的博客隐藏层层互联网覆盖下的，
即使咱有提交搜索引擎收录请求想必也是难以被检索到的，
于是咱向来都是有的没得都往博客上水。
但是在某天，咱水群的时候，突然被问起，这个是不是你的博客？
咱顿时汗流浃背，仿佛群友下一秒就要出现在咱家门口了。

同时，近日咱正好打算创作一些可能不太适合完全公开的内容，
遂趁此机会为博客添加一个简单的加密功能。

## 设计

咱的博客是基于 Hugo 的纯静态页面，这意味着当打开页面时，
被加密的信息已经发送到用户的设备上了，所以解密也需要在用户设备上进行。
这意味着需要在页面上存储加密后的密文，同时还需要存在一个解密逻辑。
那如何加密呢？

Hugo 是从 Markdown 文件生成静态页面的。所以实现加密有如下几个思路：

1. 在源 Markdown 里加密。
2. 在生成的 Html 里加密。
3. 让Hugo在生成的过程中加密。

首先，咱排除了第一种方案，因为这样会导致源文件被加密，这对于后续的修改文章内容会造成困扰。
第三种方案需要编写 Go 模块来实现，而 Hugo 使用 Go 模块需要将博客也转成模块的形式，
将现有的博客转为模块的形式是一个大工程遂放弃。于是只能使用第二种方案来实现加密了。

为了实现第二种方案的效果，需要三个部分：

1. Hugo 生成带有的标识的需要加密的 Html 元素和相关的加密信息。
2. Hugo 嵌入相关的解密逻辑。
3. 使用外部工具加密 Html。

至于加密算法的选择方面，咱选择了 AES-256-CBC-PKCS7，一个常见的对称加密算法。

## 实现

有了清晰的逻辑实现起来就不难了，只需要找到各个功能的实现方法然后拼凑在一起就好了。

### 特征 Html 生成

首先是 Hugo 这边的特征元素生成，咱使用 Hugo 的 Shortcode 来实现。
具体代码如下。

```html
{{ $passphrase := "" }}
{{- if .IsNamedParams }}
{{ $passphrase = (.Get "passphrase") | default "" }}
{{- else}}
{{ $passphrase = (.Get 0) | default ""}}
{{- end}}

{{- if .Page.Draft }}
  {{- with .Inner }}
  <div class="encrypted-block" data-unencrypted-content="{{ . | markdownify | base64Encode }}" data-passphrase="{{ $passphrase }}">
    {{ . | markdownify }}
  </div>
  {{- end }}
{{- else }}
  {{- with .Inner }}
  <div class="encrypted-block" data-unencrypted-content="{{ . | markdownify | base64Encode }}" data-passphrase="{{ $passphrase }}">
    <div class="decrypt-pad">
      <input type="password" class="decrypt-passphrase" placeholder="{{i18n "input_passphrase"}}"/>
      <button class="decrypt-button" onclick="decrypt_encryped_content(this)">{{i18n "decrypt"}}</button>
    </div>
  </div>
  {{- end }}
{{- end}}
```

为了防止 Hugo 自带的 Summary 或者主题自带的特性意外将明文暴露，
这里将明文和口令存储在 html 标签的 data-* 区域中用于确保不会被处理。
同时为了方便的在编写时能较好的预览，特殊处理页面是草稿的情况。

### 解密逻辑引入

由于现代浏览器并没有内置的 AES 加解密功能，同时由于 Hugo 也没有提供相关的能力，
所以只能导入外部的库来实现解密逻辑，这里选用 CryptoJS 来支持这个功能。

首先是如何引入 CryptoJS，这里涉及到 Hugo 对于外部资源文件的管理逻辑，
由于咱不太希望自己的博客过于依赖外部 CDN 的资源，所以使用了如下的方式来导入 CryptoJS。

```html
{{- $cryptoJS := resources.Get "js/crypto-js.min.js" -}}
  {{- with try (resources.GetRemote "https://cdn.jsdelivr.net/npm/crypto-js/crypto-js.js") }}
    {{ with .Err }}
      {{ errorf "%s" . }}
    {{ else with .Value }}
      {{ with resources.Copy "js/crypto-js.min.js" . }}
        {{ $cryptoJS = . }}
      {{ end }}
    {{ end }}
  {{- end }}
{{ $cryptoJS = $cryptoJS | fingerprint }}
<script
  defer
  crossorigin="anonymous"
  id="CryptoJS-script"
  src="{{ $cryptoJS.RelPermalink }}"
  integrity="{{ $cryptoJS.Data.Integrity }}"
></script>
```

然后编写，对应的解密 Javascript 函数。

```html
<script>
function decrypt_encryped_content(button) {
  const block = button.closest('.encrypted-block');
  const encrypted_data = block.dataset.encryptedData;
  const passphrase = block.querySelector('.decrypt-passphrase').value.trim();

  try {
    const bytes = CryptoJS.AES.decrypt(encrypted_data, passphrase);
    const decrypted_content = bytes.toString(CryptoJS.enc.Utf8);
    const html_doc = CryptoJS.enc.Utf8.stringify(CryptoJS.enc.Base64.parse(decrypted_content));

    if(decrypted_content) {
      block.innerHTML = html_doc;
    }

  } catch (err) {
    alert('Error decrypting content: ' + err.message);
  }
}
</script>
```

至此，解密部分的所有组件就完成了，剩下的就是加密的部分的编写了。

### 加密 Html

为了方便起见，咱选择使用 Python 脚本来实现 Html 中特征元素的加密。
不过这里有个小困惑点，那就是 CryptoJS 的 AES 默认解密函数只需要传入密文和口令就可以实现解锁，
其对于口令长度并没有限制，而 AES 加密算法中对于密钥的长度是有明确限制的。
同时对于初始化向量的选择没有任何头绪。

于是在一番网上的调查后，
发现这篇文章[^1]中讲到了如何多语言兼容 CryptoJS 的 AES 的加解密算法。
遂有下面的 Python 实现的加密算法。
顺带展现一下加密功能的实现，{{<spoiler>}}口令：ciallo{{</spoiler>}}。

{{<encrypted "ciallo">}}

```python
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from typing import Tuple
from rich.console import Console

import hashlib
import base64
import os


DEFAULT_PASSPHRASE = "0721"


def gen_key_and_iv(salt: bytes, passphrase: str) -> Tuple[bytes, bytes]:
    passphrase_bytes = passphrase.encode()
    hash1 = hashlib.md5(passphrase_bytes + salt).digest()
    hash2 = hashlib.md5(hash1 + passphrase_bytes + salt).digest()
    hash3 = hashlib.md5(hash2 + passphrase_bytes + salt).digest()

    key = hash1 + hash2
    iv = hash3

    return key, iv


def encrypt_content(content, passphrase):
    # 生成密钥（SHA-256哈希处理passphrase）
    if len(passphrase) == 0:
        passphrase = DEFAULT_PASSPHRASE

    # 生成Salt
    salt = os.urandom(8)
    key, iv = gen_key_and_iv(salt, passphrase)

    # 创建AES-CBC加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 填充并加密内容
    padded_content = pad(content.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_content)
    ciphertext = b"Salted__" + salt + ciphertext

    # 组合IV和密文并进行Base64编码
    return base64.b64encode(ciphertext).decode("utf-8")


def process_html(input_file, output_file):
    # 读取并解析HTML
    with open(input_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 查找所有目标div
    for div in soup.find_all("div", class_="encrypted-content"):
        if "data-unencrypted-content" in div.attrs and "data-passphrase" in div.attrs:
            # 获取加密内容和密钥
            content = div["data-unencrypted-content"]
            passphrase = div["data-passphrase"]

            # 执行加密
            encrypted_data = encrypt_content(content, passphrase)

            # 更新属性
            div["data-encrypted-data"] = encrypted_data
            del div["data-unencrypted-content"]
            del div["data-passphrase"]

    # 保存修改后的HTML
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    # 遍历public文件夹下所有的html文件
    html_list = []
    for path, dir, file in os.walk("public"):
        for f in file:
            if f.endswith(".html"):
                input_file = os.path.join(path, f)
                output_file = os.path.join(path, f)
                html_list.append((input_file, output_file))

    console = Console()

    with console.status("Encrypting...", spinner="dots3") as status:
        for input_file, output_file in html_list:
            status.update(f"Encrypting {input_file}")
            process_html(input_file, output_file)
```

{{</encrypted>}}

## 总结

最后将一些新引入的 Html 元素编写相应的 CSS 使其和之前的主题契合，
就完成了这个简单的功能。不过的实现还有一个缺点，那就是无法在运行
`hugo server -D`时实时测试加密的内容。

最最后，如果你在咱的博客中看到了加密的但是想看的内容，
可以联系咱，或者尝试自己发现密钥！

## References

[^1]: [前后端对接，多语言实现 CryptoJS 的 AES 简单加密解密](https://juejin.cn/post/7365785904704798774)
