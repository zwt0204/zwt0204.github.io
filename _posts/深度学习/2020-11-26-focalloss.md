---
layout:     post
title:      "focal-loss"
subtitle:   " \"损失函数\""
date:       2020-11-26 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 深度学习
---
* TOC
{:toc}

# 目的

Focal Loss 就是一个解决**分类问题中类别不平衡、分类难度差异**的一个 loss。
自动鉴别样本的难和易，从而让模型在后期尽量去学习那些hard example

# 详述

通常计算分类的损失为：
$$
C E=\left\{\begin{aligned}
-\log (p), & \text { if } \quad y=1 \\
-\log (1-p), & \text { if } \quad y=0
\end{aligned}\right.
$$
为了解决样本不均衡问题，通常会在其中加入样本调节参数$\alpha$:
$$
C E=\left\{\begin{aligned}
-\alpha \log (p), & \text { if } & y=1 \\
-(1-\alpha) \log (1-p), & \text { if } & y=0
\end{aligned}\right.
$$
但是这不能解决全部的问题，根据样本的难分程度分为以下几类：
```
正难、正易、负难、负易
```
加入参数$\alpha$后可以缓解正负样本，但是对于难易样本的不平衡没有帮助。在实际的任务中，往往易分样本占大多数。这些样本损失小，但是数量多，最终主导了总的损失。同时易分样本对于模型的提升帮助也很小，模型应该更加关注难分样本。
可以简单想，将高置信度的样本损失降低就可以了：
$$
F L=\left\{\begin{array}{rll}
-(1-p)^{\gamma} \log (p), & \text { if } & y=1 \\
-p^{\gamma} \log (1-p), & \text { if } & y=0
\end{array}\right.
$$
如上面的公式，在$\gamma = 2$的时候，p=0.968，$(1-0.968)^2 = 0.001$，也就是损失衰减1000倍。Focal loss结合平衡样本以及关注难分样本：
$$
F L=\left\{\begin{aligned}
-\alpha(1-p)^{\gamma} \log (p), & \text { if } & y=1 \\
-(1-\alpha) p^{\gamma} \log (1-p), & \text { if } & y=0
\end{aligned}\right.
$$
在原始论文中$\gamma = 2, \alpha = 1$时效果最好

![](https://zwt0204.github.io//img/focalloss.png)


# 参考
1. [focalloss知乎](https://zhuanlan.zhihu.com/p/80594704)