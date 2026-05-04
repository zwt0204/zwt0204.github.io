---
layout: post
title: "When LLMs Stop Following Steps：程序不等于推理，过程执行本身就是问题"
date: 2026-05-04 10:30:00 +0800
categories: [paper, daily]
tags: [daily-paper, llm, reasoning, agent, tool-use, execution, benchmark]
---

## 一句话结论

**这篇值得读。**

它最有价值的点，不是再证明一次“长链推理会掉点”，而是把问题拆得更准：**很多模型不是不会给最终答案，而是不会忠实执行你要求的步骤。** 对 agent、tool use、workflow automation 来说，这比单看 final answer accuracy 更接近真实风险。

> 说明：这篇笔记**主要依据 arXiv 摘要页与元信息**完成；我这次**没有拿到正文全文做细读**，所以下面的实验细节、分模型差异和具体 benchmark 构造，都只按摘要里能确认的部分来写。

## 论文信息

- 标题：**When LLMs Stop Following Steps: A Diagnostic Study of Procedural Execution in Language Models**
- arXiv：<https://arxiv.org/abs/2605.00817>
- 提交时间：2026-05-01
- 作者：Sailesh Panda, Pritam Kadasi, Abhishek Upperwal, Mayank Singh
- 备注：arXiv 标注 **77 pages, 109 figures**，说明正文大概率是一次比较系统的诊断研究，而不是短 paper。

## 它在解决什么问题

很多 reasoning benchmark 只看一件事：

- **最后答对没有？**

但这会掩盖一个更关键的问题：

- **模型是不是按你要求的 procedure 真做了一遍？**

如果模型只是“看起来会推理”，但实际上会：
- 中途跳步；
- 提前作答；
- 漏掉中间变量更新；
- 自己补出 prompt 里没要求的步骤；

那它在 agent / workflow 场景里就会变得很危险。因为真实系统里，**过程正确性**常常比“最后碰巧答对”更重要。

我的理解是：

> 这篇论文盯住的是 **faithful instruction execution**，而不只是 reasoning style output。

这件事很重要，因为很多 agent 失败并不是“知识不够”，而是**执行链条不可靠**。

## 作者做了什么

### 作者声称

根据摘要，作者构造了一个**受控的 procedural execution 诊断基准**：

1. 给模型一套**分步算术算法**；
2. 再给两个数字输入；
3. 要求模型按指定步骤执行，并返回最终计算结果；
4. 任务本身的算术操作不复杂；
5. 难度主要来自两件事：
   - **算法长度增加**；
   - **对中间变量的 look-back dependency**，也就是后续步骤需要正确回看前面产生的中间状态。

这个设计很聪明，因为它尽量把“世界知识”“模糊语言理解”“外部检索”等杂质拿掉，专门测：

- 你会不会老老实实按步骤做；
- 你能不能在更长程序里维持执行一致性；
- 你会不会在中间状态管理上失真。

## 关键结果

### 实验观察（摘要可确认）

摘要里能直接确认的结果有三点：

1. 跨 **14 个模型、55 个数据集**做了系统评测；
2. 平均 **first-answer accuracy** 从 **5-step 程序上的 61%**，下降到 **95-step 程序上的 20%**；
3. 生成层面的失败模式不只是“算错”，还包括：
   - **missing answers**（漏答）
   - **premature answers**（还没执行完就提前作答）
   - **self-correction after an initial error**（先错后改）
   - **under-executed traces**（步骤没真正跑完）
   - **hallucinated extra steps**（幻觉出额外步骤）

### 我的判断

我觉得这里最关键的不是 61% → 20% 这个数字本身，而是它说明：

> **模型的“推理能力”里，混着相当多“程序执行不忠实”的成分。**

换句话说，某些 benchmark 上的好成绩，可能部分来自模式匹配、结果猜测、短程启发式，而不是真正稳定的 step-by-step execution。

## 这篇论文为什么值得 agent 圈关心

### 1. 它提醒我们：final answer 不等于可靠执行

对聊天问答来说，最终答案错了当然重要；但对 agent 来说，更常见的风险是：

- 工具调用顺序错了；
- 本该确认中间状态却跳过去了；
- 只执行了一半流程就给出“完成”信号；
- 擅自补动作、改动作。

这篇工作虽然用的是算术 procedure，但它在测的其实是更一般的问题：

**模型有没有把“程序”当程序执行，而不是当一道可以蒙答案的题。**

### 2. 它很可能能迁移到 tool-use / workflow evaluation

我的判断是，这套思路很适合被迁移到：

- browser/computer-use agent；
- enterprise workflow agent；
- coding / ops / ETL 多步自动化；
- 任何要求“先做 A，再做 B，最后才能做 C”的系统。

原因很简单：这些场景真正关心的不是“最终输出像不像”，而是：

- 有没有按顺序执行；
- 有没有正确维护中间状态；
- 有没有在长链里逐步漂移。

### 3. 它也在挑战“chain-of-thought 看起来很长 = 推理更强”这个直觉

如果一个模型能写很长的 reasoning trace，但其中大量步骤：

- 没执行；
- 执行错；
- 回看错状态；
- 自己脑补了不该有的步骤；

那这个 trace 更像是一种**解释性文本生成**，而不一定是可靠 computation。

这点我觉得很重要，也很值得拿来校准我们对 reasoning model 的预期。

## 这篇工作的边界

### 作者声称

作者的结论是：表面上的 reasoning ability，可能掩盖了**忠实执行指令**上的明显弱点。

### 我的判断

这个结论大概率成立，但它的外推边界还要看正文：

1. **算术程序**与真实 agent task 的对应关系有多强？
   - 它测得很干净，但也可能比真实工具调用更“程序化”。
2. 不同模型的失败模式分布是否一致？
   - 有些模型可能更容易提前作答，有些可能更容易漏步骤。
3. prompt 形式、sampling 策略、是否允许 scratchpad，会不会显著改变结果？
4. 95-step 这种超长 procedure，到底是在测执行失败，还是已经混入了 context management / attention degradation 问题？

这些都得看正文和附录才能下更硬的判断。

## 如果你只想抓重点，建议重点看什么

如果后面要精读正文，我建议优先看四块：

1. **benchmark construction**：它怎么生成 55 个数据集、怎么控制难度；
2. **failure taxonomy**：各种失败模式是如何定义和统计的；
3. **look-back dependency**：中间变量回看依赖是怎么设计的；
4. **per-model breakdown**：到底是所有模型都掉得厉害，还是少数模型拖了均值。

## 最后判断

**我会把这篇归类为“值得读的 agent reliability / execution diagnosis 论文”。**

不是因为它直接给出了更强系统，而是因为它问了一个更基础也更危险的问题：

> **当我们说一个 LLM“会推理”时，它到底是在可靠执行程序，还是只是经常能把结果说得像对？**

对做 agent、tool use、workflow automation 的人来说，这不是学术洁癖，而是上线前必须搞清楚的事。

如果后续我拿到正文，我会优先补：
- benchmark 生成细节；
- 14 个模型的分项表现；
- 哪类失败最常见；
- 这套诊断能不能迁移成 agent execution benchmark。
