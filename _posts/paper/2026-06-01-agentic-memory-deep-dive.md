---
layout: post
title: "Agentic Memory 深入解读：把长短期记忆管理变成 agent 的一等动作"
subtitle: "从统一记忆管理看 LLM agent 为什么不该只靠 heuristic 和记忆外挂"
date: 2026-06-01 10:30:00 +0800
author: "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
  - paper
  - daily-paper
  - llm
  - agent
  - memory
  - reinforcement-learning
  - retrieval
categories: [paper, daily]
---

* TOC
{:toc}

# 0. 论文信息

- 标题：Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents
- arXiv：<https://arxiv.org/abs/2601.01885>
- PDF：<https://arxiv.org/pdf/2601.01885>
- 作者：Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu
- 时间：2026-01-05，后续修订到 2026-04-30
- 代码：arXiv 页面注明已有 GitHub 代码仓库

# 1. 先说结论

这篇值得读。

它最重要的地方，不是又提出了一个“更聪明的 memory 模块”，而是把问题定义得更准确：**LLM agent 的记忆管理，不该被拆成互相独立的长期记忆和短期记忆外挂，而应该直接进入 agent policy 里一起优化。**

如果你关心的是 long-horizon agent、记忆增强、RAG for agents，或者想知道“为什么很多 agent 记忆系统看起来能跑，但一到复杂任务就不稳”，这篇很对路。

一句话概括：

> 这篇论文在说，真正有用的 agent memory，不是固定规则里的检索和总结，而是能让 agent 自己决定何时写、何时读、何时改、何时删的统一控制系统。

# 2. 它在解决什么问题

论文一开始就把痛点说得很直接：LLM agent 的上下文窗口有限，长任务里信息会不断累积，单纯靠“把更多内容塞进 prompt”不够。

作者认为现有方法有两个常见问题：

1. **LTM 和 STM 分开做**，经常是 heuristic 或 auxiliary controller；
2. **记忆管理不是端到端优化的**，很多系统只能在局部看起来合理。

这会带来什么后果？

- 重要信息可能没被存进去；
- 噪声会堆进上下文；
- 记忆检索和任务执行脱节；
- 一次任务里学到的记忆策略，下一次还是要重来。

所以这篇的目标不是做一个更大的 memory bank，而是把记忆操作本身变成 agent 的可学习动作。

# 3. 方法核心

## 3.1 把记忆操作做成 tool-based actions

AgeMem 把 memory 操作暴露成工具动作，让 agent 自己决定：

- store
- retrieve
- update
- summarize
- discard

这里最关键的不是“有这些工具”，而是**这些工具直接属于 policy 的动作空间**。也就是说，记忆不是外包出去的附属系统，而是 agent 决策的一部分。

## 3.2 统一 LTM + STM

论文把 long-term memory 和 short-term memory 一起纳入统一框架：

- LTM 负责持久保存可复用知识；
- STM 负责当前上下文压缩、筛选和管理。

它不是简单地把两者拼起来，而是试图让 agent 在同一个策略里学会：什么时候该把信息放进长期记忆，什么时候该压缩当前上下文，什么时候该从长期记忆里取回东西。

## 3.3 三阶段渐进式 RL

作者设计了一个三阶段 progressive RL 流程：

1. casual interaction
2. distractor injection
3. formal QA / integrated reasoning

这个设计的意思很清楚：先学基础记忆操作，再学噪声下的上下文控制，最后才做完整任务推理。

## 3.4 Step-wise GRPO

这是我觉得方法里最有意思的点。

记忆操作的问题是：奖励通常很稀疏，而且很延迟。你早期做的一个 memory choice，可能到最后任务结束时才知道对不对。

作者用 step-wise GRPO 把终端奖励往前传播，让前面的 memory 决策也能收到学习信号。这个思路是合理的，因为它直接对应了 long-horizon credit assignment 的难题。

# 4. 实验怎么做

论文在 5 个 long-horizon benchmark 上评估：

- ALFWorld
- SciWorld
- PDDL
- BabyAI
- HotpotQA

对比基线包括：

- LangMem
- A-Mem
- Mem0
- Mem0g
- AgeMem-noRL

基础模型用了：

- Qwen2.5-7B-Instruct
- Qwen3-4B-Instruct

## 结果

论文给出的主结果很强：

- Qwen2.5-7B-Instruct 上平均 41.96%
- Qwen3-4B-Instruct 上平均 54.31%
- 相比最佳基线平均提升 4.82 和 8.57 个百分点
- 相比 AgeMem-noRL，RL 带来 8.53 和 8.72 个百分点提升

记忆质量方面：

- HotpotQA 上 MQ 达到 0.533 / 0.605

STM token 使用也更省：

- Qwen2.5-7B-Instruct 上 token 平均减少 3.1%
- Qwen3-4B-Instruct 上 token 平均减少 5.1%

这些结果说明它不是只把 memory 做得“更会存”，也让上下文更省。

# 5. 我觉得它真正新的地方

## 5.1 不是外挂 memory，而是 agent policy 里的 memory

这点很重要。

很多系统把 memory 当外部知识库，agent 只是会查。AgeMem 更进一步，把 memory 管理动作变成可学习策略的一部分。

这意味着它更接近真实 agent 的工作方式：不是“查不查”的二选一，而是“当前该怎么管记忆”。

## 5.2 不是只优化答案，而是优化记忆质量

论文不只是看任务完成率，还看存下来的 memory 质量，以及上下文 token 使用。

这比单看 final answer 更像工程系统，因为你会关心：

- 记忆是不是可复用
- 会不会越跑越乱
- 会不会不断膨胀

## 5.3 三阶段 RL 的工程感很强

它不是把训练直接扔给一个黑盒优化器，而是分阶段推进，让 agent 先学会动作，再学会抗噪，再学会完整推理。

这类设计通常更像真工程，而不是纯 benchmark trick。

# 6. 局限也很明显

第一，**训练和评估还是有明显的 benchmark 约束**。

论文用 HotpotQA 做 RL，再外推到其他任务。这个设计有价值，但和真实产品环境仍然不是一回事。

第二，**tool set 是固定的**。

目前是一个清晰好用的抽象，但未来如果要覆盖更复杂的 agent 记忆，工具粒度可能还需要继续细化。

第三，**memory 质量的评估天然难**。

论文用了 LLM-based evaluator，这在研究里很常见，但真实场景里仍然要小心“评估器也会漂”。

# 7. 我怎么看

如果把这篇和很多“记忆外挂”类工作放在一起看，我会把它理解成一个方向信号：

**LLM agent 的下一阶段，不只是更会推理，而是更会管理自己的上下文和记忆。**

这篇的价值在于它把 memory 从“检索组件”抬成了“策略问题”。

这也和我前面写过的很多 agent 文章连上了：

- long-horizon task 的瓶颈不只是 reasoning
- 很多失败不是答案错，而是过程里记错、漏记、乱记
- 真正的复利来自可积累的上下文管理

所以如果你现在在做 agent 系统，我会把这篇归为值得认真读的那一类。

# 8. 适合谁读

- 做 agent memory / RAG / long-context 系统的人
- 做多轮任务、长期任务、工作流 agent 的人
- 想把“记忆管理”从规则系统升级到可学习策略的人
- 想理解 RL 在 agent memory 上怎么落地的人

# 9. 推荐度

**推荐读。**

如果你只想看一个结论，那就是：

> 记忆不是 agent 的附属功能，而是 agent 本体的一部分。

# 10. 参考链接

- <https://arxiv.org/abs/2601.01885>
- <https://arxiv.org/pdf/2601.01885>
- <https://github.com/y1y5/AgeMem>
