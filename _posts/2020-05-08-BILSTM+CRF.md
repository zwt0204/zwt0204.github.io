---
layout:     post
title:      "BILSTM+CRF"
subtitle:   " \"信息抽取\""
date:       2020-05-18 18:00:00
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - NER
---
* TOC
{:toc}
# 任务描述
1. 假设要抽取两类实体、人名加机构名，采用BIO标签，则标签有5个分别为
$$
B-Person （人名的开始部分）\\
I- Person （人名的中间部分）\\
B-Organization （组织机构的开始部分）\\
I-Organization （组织机构的中间部分）\\
O （非实体信息）
$$
2. 输入一句话，需要对其中每个词打标签，判断那个词是人名，那个词是机构名

# BiLSTM+softmax

![](https://zwt0204.github.io//img/bilstm+softmax.jpg)
1. bilstm进行特征的抽取，然后接softmax对每一个词都去取概率最大的一个标签。
2. 这样会导致，B后面也会跟B或者跟O，因为softmax只会取当前预测的最大值，不会考虑前后的标签约束。

# BiLSTM+CRF
![](https://zwt0204.github.io//img/bilstm+crf.jpg)

1. 基于bilstm进行特征抽取，抽取特征作为crf的输入，学习句子约束进行全局的归一化。

# crf
1. crf层学习句子的约束条件、约束条件为自动学习
2. 
