---
layout:     post
title:      "tensorflow"
subtitle:   " \"tf\""
date:       2020-12-01 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# tensorflow

限制gpu：
```
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
# 动态增长
# config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))
```