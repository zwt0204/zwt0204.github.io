---
layout:     post
title:      "组件优化"
subtitle:   " \"组件优化\""
date:       2024-03-04 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - llms
---
* TOC
{:toc}

## RMSNorm 
layerNorm计算如下：
$$
\begin{aligned}
&a_i=\sum_{j=1}^m w_{i j} x_j, \quad y_i=f\left(a_i+b_i\right),\\
&\bar{a}_i=\frac{a_i-\mu}{\sigma} g_i, \quad y_i=f\left(\bar{a}_i+b_i\right),\\
&\mu=\frac{1}{n} \sum_{i=1}^n a_i, \quad \sigma=\sqrt{\frac{1}{n} \sum_{i=1}^n\left(a_i-\mu\right)^2} .
\end{aligned}
$$
第一行表示未经过归一化。第二行表示经过layerNorm，第三行表示均值和方差的计算。
rmsnorm计算如下：
$$
\bar{a}_i=\frac{a_i}{\operatorname{RMS}(\mathbf{a})} g_i, \quad \text { where } \operatorname{RMS}(\mathbf{a})=\sqrt{\frac{1}{n} \sum_{i=1}^n a_i^2} .
$$

## AdamW
![](https://zwt0204.github.io//img//llm//adamw.jpg)

如上如所示：
AdamW相对与Adam的改动是其将权重衰减项从梯度的计算中拿出来直接加在了最后的权重更新步骤上（图式12）。
其提出的动机在于：原先Adam的实现中如果采用了L2权重衰减，则相应的权重衰减项会被直接加在loss里，从而导致动量的一阶与二阶滑动平均均考虑了该权重衰减项（图1式6），而这影响了Adam的优化效果，而将权重衰减与梯度的计算进行解耦能够显著提升Adam的效果。目前，AdamW现在已经成为transformer训练中的默认优化器了。

==为什么要用这些占显存很大的优化器，基本扩大模型参数了四倍==

## SwiGLU 
### GLU
[GLU](https://arxiv.org/pdf/1612.08083.pdf) 全称为 Gated Linear Unit，即门控线性单元函数。
公式：
$$
\begin{aligned} \operatorname{GLU}(x) & =A \otimes \sigma(B) \\ & =(x \cdot W+b) \otimes \sigma(x \cdot V+c) \end{aligned}
$$
输入x经过两个独立的卷积或者是MLP层，得到向量A，B，此时，向量A和B的计算公式为$A = x.W+b，B=x.V + c$。然后向量B经过一个sigmod函数之后，$\sigma(B)$中的每个元素都变为0-1之间的值，这就起来到控制信息是否通过的作用。将向量A与之逐元素相乘之后就得到了GLU层的最终输出结果。
GLU正式使用的时候计算公式为$GLU(x) = x \otimes \sigma(g(x))$,其中$g(x)$表示x经过MLP或者卷积的结果。当$\sigma(g(x))$趋于0表示对x阻断，趋于1表示允许x通过。
### SwiGLU

## causal multi-head attention

## all_reduce 

分布式训练一般分为同步训练和异步训练，同步训练中所有的worker读取mini-batch的不同部分，同步计算损失函数的gradient，最后将每个worker的gradient整合之后更新模型。异步训练中每个worker独立读取训练数据，异步更新模型参数。通常同步训练利用AllReduce来整合不同worker计算的gradient，异步训练则是基于参数服务器架构（parameter server）。

AllReduce其实是一类算法，目标是高效得将不同机器中的数据整合（reduce）之后再把结果分发给各个机器。在深度学习应用中，数据往往是一个向量或者矩阵，通常用的整合则有Sum、Max、Min等。图一展示了AllReduce在有四台机器，每台机器有一个长度为四的向量时的输入和输出。

![](https://zwt0204.github.io//img//llm//allreduce.jpg)

[ring allreduce](http://andrew.gibiansky.com/)算法分为两个阶段:
第一阶段，将N个worker分布在一个环上，并且把每个worker的数据分成N份。

![](https://zwt0204.github.io//img//llm//allreduce2.png)

接下来我们具体看第k个worker，这个worker会把第k份数据发给下一个worker，同时从前一个worker收到第k-1份数据。

![](https://zwt0204.github.io//img//llm//allreduce3.png)

之后worker会把收到的第k-1份数据和自己的第k-1份数据整合，再将整合的数据发送给下一个worker。

![](https://zwt0204.github.io//img//llm//allreduce4.png)

以此循环N次之后，每一个worker都会包含最终整合结果的一份。

![](https://zwt0204.github.io//img//llm//allreduce5.png)

第二阶段，每个worker将整合好的部分发送给下一个worker。worker在收到数据之后更新自身数据对应的部分即可。

假设每个worker的数据是一个长度为S的向量，那么个Ring AllReduce里，每个worker发送的数据量是O(S)，和worker的数量N无关。这样就避免了主从架构中master需要处理O(S*N)的数据量而成为网络瓶颈的问题。


## a cosine learning rate schedule



# 参考
1. [all-reduce](https://zhuanlan.zhihu.com/p/100012827)

