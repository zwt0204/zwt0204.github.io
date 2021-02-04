---
layout:     post
title:      "数据抓取"
subtitle:   " \"crawl\""
date:       2021-02-03 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 爬虫
---
* TOC
{:toc}

# 注意

## 需要添加headers
```
headers = {
    'Cookie': 'OCSSID=4df0bjva6j7ejussu8al3eqo03',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
```
## 代理

```
proxy_list = [
        {"http": "49.87.10.131"},
        {"http": "112.111.217.226"},
        {"http": "183.166.133.49"},
        {"http": "113.194.48.237"},
        {"http": "49.86.178.14"},
        {"http": "36.248.132.135"},
        {"http": "113.121.21.253"},
        {"http": "175.43.57.52"},
        {"http": "117.69.13.239"},
        {"http": "58.22.177.116"}
    ]
    # 随机选择一个代理
    proxy = random.choice(proxy_list)
    # 使用选择的代理构建代理处理器对象
    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    opener.addheaders = [headers]
```


# 参考