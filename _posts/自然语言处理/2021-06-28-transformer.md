---
layout:     post
title:      "transformer"
subtitle:   " \"transformer\""
date:       2024-03-09 10:46:00 
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - nlp
---
* TOC
{:toc}
# 来源

核心的原因在于考虑到rnn在计算中限制的顺序性，在具体的计算过程中没有办法并行化：
```
1.t时刻依赖t-1时刻的结果，限制并行
2.顺序计算过程中导致的信息丢失(梯度消失问题)
```
论文中的定义：
```
Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence aligned RNNs or convolution
```
# Transformer整体结构
![](../../img/自然语言处理/transformer.png)
整体架构如上图，包括编码层和解码层，每一块又是N个block堆叠。
![](../../img/transformer.png)
整体的transformer的结构是基于6层的编码层和6层的解码层组成，是一个典型的seq2seq模型结，只是在具体的编码解码模块做了替换。
Encoder结构：
![](../../img/自然语言处理/transformer1.png)
其中self-attention的计算：
$$
\operatorname{Attention}(Q, K, V)=\operatorname{softmax}\left(\frac{Q K^{T}}{\sqrt{d_{k}}}\right) V
$$
Feed Forward Neural Network的计算：
$$
\operatorname{FFN}(Z)=\max \left(0, Z W_{1}+b_{1}\right) W_{2}+b_{2}
$$
Decoder结构：
![](../../img/自然语言处理/transformer2.png)
Decoder 由 6 个完全相同的 Decoder Layer 组成，每个 Decoder Layer 由三个 Sub-Layer 组成：

```
1.Maked Multi-Head Attention，相比于 Encoder 的 Attention，它加入了掩码，遮住当前单词后面的内容；
2.Multi-Head Attention，用 Encoder 的输出作为 Key 和 Value，Query 由 Decoder 提供；
3.Feed Forward，与 Encoder 的一致，都是全连接层。Decoder 也采用了残差连接和 Layer Normalization，与 Encoder 一致。
```
![](../../img/自然语言处理/transformer9.png)
==注意编码层最终的输出才输入到解码层中，同时是输入到解码层的每一层中==

# 输入编码

首先基于外部预训练的词向量来初始化特征向量或者是随机初始化（论文中是==Xavier==初始化）。维度是512。在encoder的输入端，特征向量作为整体的输入。对于其他层的输入则是下层网络的输出。如图所示：
![](../../img/自然语言处理/transformer3.png)÷
==注意：每个token都共享block的参数，并行处理。如上图的thinking和machines是同时共享参数进行处理的。==

# self-Attention
![](../../img/自然语言处理/transformer4.png)
在self-attention中，每一个单词会被表示为三个不同的向量，分别是Query，Key，Value，长度均为64（因为8个头的缘故）。生成的方式是基于三个不同的权值矩阵与输入相乘得到，三个矩阵都是512*64维。
![](../../img/自然语言处理/transformer5.png)
整体的计算过程如下：
第一步：将输入转为向量模式
第二步：根据输入得到q，k，v三个向量
第三步：计算每个向量的score，$score=q.k^T$
第四步：为了梯度计算的稳定，将score归一化，除以$\sqrt d_k$(==为了使得score的值不极端，平滑一点==)
第五步：对score进行softmax计算
第六步：第五步计算结果与v点乘，得到加权的每个输入向量$z=\sum v$
![](../../img/自然语言处理/transformer6.png)
==注意:==在self中加入了残差网络来解决深层网络的梯度消失导致的退化问题，同时为了模型更快速稳定加入了Layer Normalization。$LayerNorm(x+SubLayer(x))$
![](../../img/自然语言处理/transformer7.png)

```python
def self_attention(query, key, value, dropout=None, mask=None):
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    # mask的操作在QK之后，softmax之前
    if mask is not None:
        mask.cuda()
        scores = scores.masked_fill(mask == 0, -1e9)
    self_attn = F.softmax(scores, dim=-1)
    if dropout is not None:
        self_attn = dropout(self_attn)
    return torch.matmul(self_attn, value), self_attn
```

# multi-head Atterntion
Multi-Head Attention相当于 8 个不同的self-attention的集成（ensemble）具体可以分为三个步骤：
第一步：将输入分别输入到8个相同的selfattention结构中，得到8个加权的特征矩阵
第二步：将8个特征向量拼接
第三步：拼接后的特征向量经过一层全连接转换为z
![](../../img/自然语言处理/transformer8.png)

```python
class MultiHeadAttention(nn.Module):

    def __init__(self):
        super(MultiHeadAttention, self).__init__()

    def forward(self,  head, d_model, query, key, value, dropout=0.1,mask=None):
        """
        :param head: 头数，默认 8
        :param d_model: 输入的维度 512
        :param query: Q
        :param key: K
        :param value: V
        :param dropout:
        :param mask:
        :return:
        """
        assert (d_model % head == 0)
        self.d_k = d_model // head
        self.head = head
        self.d_model = d_model

        self.linear_query = nn.Linear(d_model, d_model)
        self.linear_key = nn.Linear(d_model, d_model)
        self.linear_value = nn.Linear(d_model, d_model)

        # 自注意力机制的 QKV 同源，线性变换

        self.linear_out = nn.Linear(d_model, d_model)

        self.dropout = nn.Dropout(p=dropout)
        self.attn = None

        # if mask is not None:
        #     # 多头注意力机制的线性变换层是4维，是把query[batch, frame_num, d_model]变成[batch, -1, head, d_k]
        #     # 再1，2维交换变成[batch, head, -1, d_k], 所以mask要在第一维添加一维，与后面的self attention计算维度一样
        #     mask = mask.unsqueeze(1)
        n_batch = query.size(0)
        # 多头需要对这个 X 切分成多头
        # query==key==value
        # [b,1,512]
        # [b,8,1,64]

        # [b,32,512]
        # [b,8,32,64]
        query = self.linear_query(query).view(n_batch, -1, self.head, self.d_k).transpose(1, 2)  # [b, 8, 32, 64]
        key = self.linear_key(key).view(n_batch, -1, self.head, self.d_k).transpose(1, 2)  # [b, 8, 32, 64]
        value = self.linear_value(value).view(n_batch, -1, self.head, self.d_k).transpose(1, 2)  # [b, 8, 32, 64]
        x, self.attn = self_attention(query, key, value, dropout=self.dropout, mask=mask)
        # [b,8,32,64]
        # [b,32,512]
        # 变为三维， 或者说是concat head
        x = x.transpose(1, 2).contiguous().view(n_batch, -1, self.head * self.d_k)

        return self.linear_out(x)
```
# Encoder-Decoder Attention
这个是在解码器中多出来的一部分，在其内部，q来自于解码器的上一个输出，k，v泽来自于编码器的输出。
注意在进行机器翻译的工作时：
```
解码过程是一个顺序操作的过程，也就是当解码第 k个特征向量时，我们只能看到第 k-1 及其之前的解码结果，论文中把这种情况下的multi-head attention叫做masked multi-head attention。
```
# 损失层
解码器解码之后，解码的特征向量经过一层激活函数为softmax的全连接层之后得到反映每个单词概率的输出向量。此时我们便可以通过CTC等损失函数训练模型了。

# 位置编码
当前已经介绍的内容并没有涉及到模型对序列化顺序的处理能力，也就是说句子顺序打乱并不会影响模型的结果，从这个角度分析，其只能说是一个更为强大的词袋模型。
为了解决顺序性问题，transformer中引入了位置编码。位置编码的引入有两种，一种是根据数据取学习，一种是自己设计编码规则。在transformer中是基于第二种所设计的。
![](../../img/自然语言处理/transformer10.png)
在论文中给出的公式为：
$$
\begin{gathered}
P E(\text { pos }, 2 i)=\sin \left(\frac{\text { pos }}{10000 \frac{2 i}{d_{\text {model }}}}\right) \\
P E(\text { pos }, 2 i+1)=\cos \left(\frac{\text { pos }}{10000 \frac{2 i}{d_{\text {model }}}}\right)
\end{gathered}
$$
其中pos表示单词的位置，i表示单词的维度。
设计此公式的目的是考虑单词之间的相对位置。根据公式$\sin (\alpha+\beta)=\sin \alpha \cos \beta+\cos \alpha \sin \beta, \cos (\alpha+\beta)=\cos \alpha \cos \beta-\sin \alpha \sin \beta$可以看出来，位置k+p的位置向量可以通过位置k的特征向量线性变化而来，这就可以辅助模型来捕获单词之间的相对位置。
# 并行
## encoder
encoder并行可以直观的解释为：主要是自注意层的并行化，自注意力就是基于$x_i$之间两两相关性作为权重的一种加权平均，进而将每一个$x_i$都映射到$z_i$。假设有两个词$x_1,x_2$，自注意力机制首先计算$x_1$与$x_1,x_2$的相关性，记作$\alpha_{11},\alpha_{12}$，$z_1 =\alpha_{11} * x_1 + \alpha_{12} * x_2 $,同样的方式也可以得到$z_2$。此时可以说$z_1,z_2$已经考虑了其他元素之间的依赖关系。
## decoder
注意：这个并行化只是在训练的阶段有效，预测阶段是顺序执行的
decoder并行依赖于两个关键点：
1.teacher force
2.masked self attention
teacher force表示：
```
在训练的时候强制使用正确的单词，而不是上一轮的预测结果。
示例：
假设第一轮解码器输入<start>和编码器的输出，解码器输出为I
第二轮的时候输入<start> I 和编码器的输出，解码器输出为want
第三轮的时候解码器的输入仍然是<start> I love和编码器的输出
```
通过此种方式可以避免中间预测结果错误导致后续序列的预测，同时可以加快训练速度。
Transformer实现Decoder部分训练并行化，就是一次性将整个目标句子（假设长度为4）输入给decoder，然后利用masked自注意力算法计算出 $z_{1:4}$ ，往后面网络继续传递，最后计算出4个预测值，分别对应4个时刻的输出。

# 总结
优点：
（1）虽然Transformer最终也没有逃脱传统学习的套路，Transformer也只是一个全连接（或者是一维卷积）加Attention的结合体。但是其设计已经足够有创新，因为其抛弃了在NLP中最根本的RNN或者CNN并且取得了非常不错的效果，算法的设计非常精彩，值得每个深度学习的相关人员仔细研究和品位。
（2）Transformer的设计最大的带来性能提升的关键是将任意两个单词的距离是1，这对解决NLP中棘手的长期依赖问题是非常有效的。
（3）Transformer不仅仅可以应用在NLP的机器翻译领域，甚至可以不局限于NLP领域，是非常有科研潜力的一个方向。
（4）算法的并行性非常好，符合目前的硬件（主要指GPU）环境。

缺点：
（1）粗暴的抛弃RNN和CNN虽然非常炫技，但是它也使模型丧失了捕捉局部特征的能力，RNN + CNN + Transformer的结合可能会带来更好的效果。
（2）Transformer失去的位置信息其实在NLP中非常重要，而论文中在特征向量中加入Position Embedding也只是一个权宜之计，并没有改变Transformer结构上的固有缺陷。

# 参考
1.[详解Transformer](https://zhuanlan.zhihu.com/p/48508221)
2.[回顾transformer](https://mp.weixin.qq.com/s/wC5-9Elc0LtHH484W5oNDQ)
3.[并行化](https://www.zhihu.com/question/307197229/answer/1859981235)
4.[详解2](https://zhuanlan.zhihu.com/p/338817680)
5.[代码](https://www.cnblogs.com/nickchen121/p/16526123.html)