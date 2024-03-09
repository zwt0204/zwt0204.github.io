---
layout:     post
title:      "huggingface"
subtitle:   " \"huggingface\""
date:       2023-11-03 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - llms
---
* TOC
{:toc}

# 国内镜像下载 
huggingfacec
```
export HF_ENDPOINT=https://hf-mirror.com
from huggingface_hub import snapshot_download
snapshot_download(repo_id='defog/sqlcoder2',repo_type='model',local_dir='.',resume_download=True)
```
魔搭
```
model_dir = snapshot_download("baichuan-inc/Baichuan2-7B-Chat", revision='v1.0.4',cache_dir="/home/modelscope_modules")
```
