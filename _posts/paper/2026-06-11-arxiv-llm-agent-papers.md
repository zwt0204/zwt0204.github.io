---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-11)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-11 10:30:00 +0800
author: "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
  - paper
  - daily-paper
  - arxiv
  - llm
  - agent
  - multimodal
categories: [paper, daily]
---

* TOC
{:toc}

# 0. 说明

数据来源：[arXiv API](https://export.arxiv.org/api/query)。本篇自动检索近期与 LLM、多模态、Agent、工具使用、Skill、RAG、长上下文和模型评测相关的论文，并按研究价值、工程启发和可复现线索进行排序。

筛选不是简单看标题热词，而是优先考虑：

1. 是否切中 LLM / multimodal / agent 方向的关键问题；
2. 是否有清晰的方法贡献、评测基准或系统实现；
3. 是否能给实际工程带来可迁移经验；
4. 是否值得进一步精读 introduction、method、experiment 和 limitation。

# 1. 今日最值得读的论文

## [InternVideo3: Agentify Foundation Models with Multimodal Contextual Reasoning](http://arxiv.org/abs/2606.12195v1)

- arXiv：[2606.12195](http://arxiv.org/abs/2606.12195v1)
- PDF：[https://arxiv.org/pdf/2606.12195v1](https://arxiv.org/pdf/2606.12195v1)
- 作者：Ziang Yan、Sheng Xia、Jiashuo Yu、Yue Wu、Tianxiang Jiang、Songze Li、等
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.CV
- 主题标签：LLM、多模态、Agent、Skill/Tool、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：18/20

### 摘要速读

Recent progress in foundation models has shifted toward agentic behavior involving multi-step reasoning and tool use. However, open-source efforts largely focus on text-dominant settings, leaving long-horizon multimodal tasks underexplored.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、工具使用/技能学习、RAG、记忆或长上下文、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [OpenMedReason: Scientific Reasoning Supervision for Medical Vision-Language Models](http://arxiv.org/abs/2606.12169v1)

- arXiv：[2606.12169](http://arxiv.org/abs/2606.12169v1)
- PDF：[https://arxiv.org/pdf/2606.12169v1](https://arxiv.org/pdf/2606.12169v1)
- 作者：Negin Baghbanzadeh、Pritam Sarkar、Michael Colacci、Abeer Badawi、Adibvafa Fallahpour、Arash Afkanpour、等
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.CV、cs.AI、cs.CL、cs.LG
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：18/20

### 摘要速读

High-stakes clinical use of large vision-language models (LVLMs) requires reasoning that is grounded in visual evidence and clinical knowledge, not just correct final answers. We introduce OpenMedReason, a large-scale, open multimodal medical reasoning corpus comprising approximately 450K image-question-answer instances whose reasoning traces are primarily derived from curated biomedical, human-authored scientific articles.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models](http://arxiv.org/abs/2606.12412v1)

- arXiv：[2606.12412](http://arxiv.org/abs/2606.12412v1)
- PDF：[https://arxiv.org/pdf/2606.12412v1](https://arxiv.org/pdf/2606.12412v1)
- 作者：Cheng-Yu Yang、Shao-Yuan Lo、Yu-Lun Liu
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Vision-language models (VLMs) project images into hundreds to thousands of visual tokens, making decoder inference expensive in both attention computation and KV-cache memory. Existing visual-token reduction methods largely follow a rank-and-remove paradigm: they score visual tokens, keep a compact subset, and permanently discard the rest.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、RAG、记忆或长上下文、推理、代码或复杂任务、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners?](http://arxiv.org/abs/2606.12402v1)

- arXiv：[2606.12402](http://arxiv.org/abs/2606.12402v1)
- PDF：[https://arxiv.org/pdf/2606.12402v1](https://arxiv.org/pdf/2606.12402v1)
- 作者：Jadelynn Dao、Milan Ganai、Yasmina Abukhadra、Ajay Sridhar、Mozhgan Nasr Azadani、Katie Luo、等
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.RO、cs.AI、cs.CV
- 主题标签：LLM、多模态、Agent、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Vision-Language Models (VLMs) are increasingly deployed as high-level planners for embodied agents, with an emerging strategy of scaling test-time compute to improve capability. However, we observe that doing so increases latency, token usage, and FLOPs while yielding uneven, often diminishing gains in downstream success, limiting where embodied agents can be deployed.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、RAG、记忆或长上下文、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling](http://arxiv.org/abs/2606.12370v1)

- arXiv：[2606.12370](http://arxiv.org/abs/2606.12370v1)
- PDF：[https://arxiv.org/pdf/2606.12370v1](https://arxiv.org/pdf/2606.12370v1)
- 作者：Yucheng Li、Huiqiang Jiang、Yang Xu、Jianxin Yang、Yi Zhang、Yizhong Cao、等
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.LG、cs.CL
- 主题标签：LLM、Agent、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Reinforcement learning (RL) has become a key component in modern large language models, yet the rollout stage remains the key bottleneck in RL training pipelines. Although Multi-Token Prediction (MTP) offers a natural solution to accelerate rollouts through speculative decoding, many studies have observed that MTP acceptance rates degrade significantly during RL training, leading to limited speedup performance.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Doc-to-Atom: Learning to Compile and Compose Memory Atoms](http://arxiv.org/abs/2606.12400v1)

- arXiv：[2606.12400](http://arxiv.org/abs/2606.12400v1)
- PDF：[https://arxiv.org/pdf/2606.12400v1](https://arxiv.org/pdf/2606.12400v1)
- 作者：Xingjian Diao、Wenbo Li、Yashas Malur Saidutta、Avinash Amballa、Lazar Valkov、Srinivas Chappidi
- 发布时间：2026-06-10，更新时间：2026-06-10
- 类别：cs.CL、cs.IR
- 主题标签：LLM、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Long input sequences are central to document understanding and multi-step reasoning in Large Language Models, yet the quadratic cost of attention makes inference both memory-intensive and slow. Context distillation mitigates this by compressing contextual information into model parameters, and recent work such as Doc-to-LoRA amortizes context distillation into a single forward pass that generates one LoRA adapter per document.

### 为什么值得读

大模型核心方向、RAG、记忆或长上下文、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像知识增强或记忆系统工作，阅读重点应放在检索粒度、上下文压缩、状态更新和噪声控制。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 检索/记忆模块在噪声、过期信息和长上下文压力下是否仍然稳定？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [InternVideo3: Agentify Foundation Models with Multimodal Contextual Reasoning](http://arxiv.org/abs/2606.12195v1) | LLM, 多模态, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 18 | 2026-06-10 | Recent progress in foundation models has shifted toward agentic behavior involving multi-step reasoning and tool use. |
| [OpenMedReason: Scientific Reasoning Supervision for Medical Vision-Language Models](http://arxiv.org/abs/2606.12169v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 18 | 2026-06-10 | High-stakes clinical use of large vision-language models (LVLMs) requires reasoning that is grounded in visual evidence and clinical knowledge, not just correct final answers. |
| [Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models](http://arxiv.org/abs/2606.12412v1) | LLM, 多模态, RAG/Memory, Reasoning | 16 | 2026-06-10 | Vision-language models (VLMs) project images into hundreds to thousands of visual tokens, making decoder inference expensive in both attention computation and KV-cache memory. |
| [DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners?](http://arxiv.org/abs/2606.12402v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning | 16 | 2026-06-10 | Vision-Language Models (VLMs) are increasingly deployed as high-level planners for embodied agents, with an emerging strategy of scaling test-time compute to improve capability. |
| [Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling](http://arxiv.org/abs/2606.12370v1) | LLM, Agent, Reasoning | 16 | 2026-06-10 | Reinforcement learning (RL) has become a key component in modern large language models, yet the rollout stage remains the key bottleneck in RL training pipelines. |
| [Doc-to-Atom: Learning to Compile and Compose Memory Atoms](http://arxiv.org/abs/2606.12400v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-10 | Long input sequences are central to document understanding and multi-step reasoning in Large Language Models, yet the quadratic cost of attention makes inference both memory-intensive and slow. |
| [TAHOE: Text-to-SQL with Automated Hint Optimization from Experience](http://arxiv.org/abs/2606.12387v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-10 | Large Language Models (LLMs) have democratized database access through Text-to-SQL, but moving from prototypes to production remains difficult. |
| [APPO: Agentic Procedural Policy Optimization](http://arxiv.org/abs/2606.12384v1) | LLM, Agent, Skill/Tool, Safety/Eval | 15 | 2026-06-10 | Recent advances in agentic Reinforcement Learning (RL) have substantially improved the multi-turn tool-use capabilities of large language model agents. |
| [Natural-Language Temporal Grounding in Hour-Long Videos is a Search Problem: A Benchmark and Empirical Decomposition](http://arxiv.org/abs/2606.12300v1) | LLM, 多模态, Safety/Eval | 15 | 2026-06-10 | Temporal grounding--returning the interval $[t_s, t_e]$ for a natural-language query over a video--is the language interface to long-form video, yet has been studied on short videos; the dynamics of hour-scale natural-language grounding remain underexplored. |
| [CCKS: Consensus-based Communication and Knowledge Sharing](http://arxiv.org/abs/2606.12281v1) | Agent, Reasoning | 15 | 2026-06-10 | In Decentralized Training and Decentralized Execution (DTDE) for cooperative Multi-Agent Reinforcement Learning (MARL), action-advising-based knowledge sharing promotes interpretable and scalable cooperation among agents. |
| [Implicit Neural Representations of Individual Behavior](http://arxiv.org/abs/2606.12200v1) | 多模态, Agent, Reasoning | 15 | 2026-06-10 | We study policy representation learning from unlabeled multi-policy behavioral data. |
| [System Report for CCL25-Eval Task 5: New Dataset and LoRA-Fine-Tuned Qwen2.5](http://arxiv.org/abs/2606.12392v1) | LLM, Safety/Eval | 14 | 2026-06-10 | Recently, large language models (LLMs) have achieved promising progress in the fields of classical Chinese translation and the generation of classical poetry. |
| [Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs](http://arxiv.org/abs/2606.12385v1) | LLM, Agent, RAG/Memory, Safety/Eval | 14 | 2026-06-10 | Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. |
| [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](http://arxiv.org/abs/2606.12344v1) | Agent, Skill/Tool, Safety/Eval | 14 | 2026-06-10 | General-purpose agents such as OpenClaw are increasingly used as autonomous tool users, but their coding ability is difficult to measure under SWE-bench: a generic agent does not by itself satisfy the clean Docker workspace, patch, and prediction contract required for scoring. |
| [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](http://arxiv.org/abs/2606.12329v1) | Agent, RAG/Memory, Reasoning | 14 | 2026-06-10 | AI coding assistants now support a growing share of software work, from quick scripts to production applications. |
| [DrivingAgent: Design and Scheduling Agents for Autonomous Driving Systems](http://arxiv.org/abs/2606.12236v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-10 | Many autonomous driving systems are increasingly incorporating foundation models to improve generalization and handle long-tail scenarios. |
| [AerialClaw: An Open-Source Framework for LLM-Driven Autonomous Aerial Agents](http://arxiv.org/abs/2606.12142v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-10 | Unmanned aerial vehicles (UAVs) are increasingly used in inspection, search and rescue, environmental monitoring, and emergency response. |
| [Soft-Prompt Tuning for Fair and Efficient LLM Benchmark Evaluation](http://arxiv.org/abs/2606.12117v1) | LLM, RAG/Memory, Safety/Eval | 14 | 2026-06-10 | Benchmark scores often misrepresent a large language model's (LLM's) knowledge, because they rely, e.g., on the model's ability to follow specific formatting requirements. |
| [Bridging the Morphology Gap: Adapting VLA Models to Dexterous Manipulation via Intent-Conditioned Fine-Tuning](http://arxiv.org/abs/2606.12109v1) | 多模态, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-10 | Vision-Language-Action (VLA) models have demonstrated remarkable zero-shot generalization in robotic manipulation, yet the vast majority of pre-trained pipelines remain strictly confined to low-DoF parallel grippers. |
| [Context-Driven Incremental Compression for Multi-Turn Dialogue Generation](http://arxiv.org/abs/2606.12411v1) | Agent, RAG/Memory, Safety/Eval | 13 | 2026-06-10 | Modern conversational agents condition on an ever-growing dialogue history at each turn, incurring redundant attention and encoding costs that grow with conversation length. |
| [UniIntervene: Agentic Intervention for Efficient Real-World Reinforcement Learning](http://arxiv.org/abs/2606.12372v1) | Agent, RAG/Memory | 13 | 2026-06-10 | Human-in-the-loop reinforcement learning (HiL-RL) has emerged as an effective paradigm for real-world robotic manipulation, enabling online policy improvement with human guidance. |
| [On Subquadratic Architectures: From Applications to Principles](http://arxiv.org/abs/2606.12364v1) | LLM, RAG/Memory, Reasoning | 13 | 2026-06-10 | Transformers dominate modern sequence modeling, but their quadratic attention incurs substantial computational cost. |
| [ALIGNBEAM : Inference-Time Alignment Transfer via Cross-Vocabulary Logit Mixing](http://arxiv.org/abs/2606.12342v1) | LLM, Safety/Eval | 13 | 2026-06-10 | Domain fine-tuning degrades the safety of large language models: fine-tuned specialists readily comply with harmful prompts framed in domain language. |
| [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](http://arxiv.org/abs/2606.12320v1) | Agent, Reasoning, Safety/Eval | 13 | 2026-06-10 | Enterprise security was built to govern data boundaries: the protected surface was data at rest and in transit, and the controls -- access control, data-loss prevention, perimeter inspection -- governed crossings of that boundary. |
| [Bridging Day and Night: Unsupervised Cross-Domain Re-Identification with Synergistic Prompt and Prototype Learning](http://arxiv.org/abs/2606.12258v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 13 | 2026-06-10 | Cross-domain day-night re-identification (ReID) is fundamentally challenged by the substantial visual appearance discrepancies between daytime and nighttime scenes. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-11 15:14:37 CST
