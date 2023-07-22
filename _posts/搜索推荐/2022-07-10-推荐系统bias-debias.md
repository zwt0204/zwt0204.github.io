---
layout:     post
title:      "推荐系统bias and debias"
subtitle:   " \"recommend\""
date:       2020-05-27 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 推荐系统
---
* TOC
{:toc}
# bias产生的阶段
## user->data
```python
1.选择偏置：用户对推荐内容可以自由的反馈，一般一会对自己感兴趣或者没有兴趣的内容进行反馈，并不是对所有的内容进行反馈。
2.曝光偏置：用户做出的行为都是针对曝光内容，对于没有曝光的数据，也不能说用户是不感兴趣的。
3.一致性偏置：用户发生行为的时候可能不是自己的意愿，而实基于大部分群体做出的相似选择。
4.位置偏置：有行为的内容往往是位置靠前的item，但是位置靠前的item不一定是和用户最相关的。
```
## data->model
```python
1.推断偏置：模型的学习是通过对用户历史的数据进行建模来对当前的时间点进行喜好程度的判断
```
## model->user
```python
1.热度偏置：马太效应导致的热度高的内容出现更频繁
2.不公平现象：对某类人或者群组出现偏袒或者歧视现象
```
# debais
## 选择偏置
### 

# 参考
1.[推荐系统bias](https://mp.weixin.qq.com/s/LRv5Yf-g8ZEnCsihiS-idg)
2.[推荐系统bias](https://mp.weixin.qq.com/s/2FP_Nn1E4U8bPI70u_rGWg)
3.[Bias and Debias in Recommender System: A Survey and Future
Directions](https://arxiv.org/pdf/2010.03240.pdf)
4.[推荐生态中的bias和debias](https://zhuanlan.zhihu.com/p/342905546)