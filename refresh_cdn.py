import hashlib
import hmac
import json
import os
import time
from datetime import UTC, datetime
from http.client import HTTPSConnection
from typing import Iterable, List, Optional, Tuple

from lxml import etree


def get_secret_pair() -> Tuple[str, str]:
    secret_id = os.getenv("SECRET_ID")
    secret_key = os.getenv("SECRET_KEY")

    if secret_id is None or secret_key is None:
        raise KeyError("Secert pair not found compeletly")

    return secret_id, secret_key


def get_urls(sitemaps_path: List[str], delta_second: int) -> list[str]:
    urls: List[str] = list()

    for sitemap_path in sitemaps_path:
        tree = etree.parse(sitemap_path)
        root = tree.getroot()
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        # 遍历所有的 <url> 元素
        for url in root.xpath("//sitemap:url", namespaces=namespace):
            # 从每个 <url> 元素中获取 <loc> 和 <lastmod> 的值
            loc = url.find("sitemap:loc", namespaces=namespace)
            lastmod = url.find("sitemap:lastmod", namespaces=namespace)
            if loc is None or lastmod is None:
                continue
            loc = loc.text
            lastmod = lastmod.text

            if loc is None or lastmod is None:
                continue

            now = datetime.now(UTC)
            delta = now - datetime.fromisoformat(lastmod)
            if delta.total_seconds() <= delta_second:
                urls.append(loc)

    return urls


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def refresh_urls(
    urls: Iterable,
    key_pair: Tuple[str, str],
    region: Optional[str] = None,
    token: Optional[str] = None,
):
    secret_id, secret_key = key_pair
    service = "cdn"
    host = "cdn.tencentcloudapi.com"
    version = "2018-06-06"
    action = "PurgeUrlsCache"
    params = {"Urls": []}
    for url in urls:
        params["Urls"].append(url)
    payload = json.dumps(params)
    endpoint = "https://cdn.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (
        ct,
        host,
        action.lower(),
    )
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (
        http_request_method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + hashed_request_payload
    )

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    string_to_sign = (
        algorithm
        + "\n"
        + str(timestamp)
        + "\n"
        + credential_scope
        + "\n"
        + hashed_canonical_request
    )

    # ************* 步骤 3：计算签名 *************
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (
        algorithm
        + " "
        + "Credential="
        + secret_id
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )

    # ************* 步骤 5：构造并发起请求 *************
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": timestamp,
        "X-TC-Version": version,
    }
    if region:
        headers["X-TC-Region"] = region
    if token:
        headers["X-TC-Token"] = token

    try:
        req = HTTPSConnection(host)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        print(resp.read())
    except Exception as err:
        print(err)


SITEMAP_PATHS = ["public/en/sitemap.xml", "public/zh/sitemap.xml"]
MUST_REFRESH_URLS = [
    "https://blog.yurzi.net/archives/",
    "https://blog.yurzi.net/en/archives/",
]

if __name__ == "__main__":
    key_pair = get_secret_pair()
    urls = get_urls(SITEMAP_PATHS, 3 * 3600)
    if len(urls) != 0:
        urls.extend(MUST_REFRESH_URLS)
        urls = set(urls)
        print("Thess urls will be refresh: ")
        print(urls)
        refresh_urls(urls, key_pair)
