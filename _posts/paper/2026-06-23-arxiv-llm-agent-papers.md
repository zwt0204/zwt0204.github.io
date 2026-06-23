---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-23)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-23 10:30:00 +0800
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

## [Detecting Malicious Agent Skills in the Wild using Attention](http://arxiv.org/abs/2606.23416v1)

- arXiv：[2606.23416](http://arxiv.org/abs/2606.23416v1)
- PDF：[https://arxiv.org/pdf/2606.23416v1](https://arxiv.org/pdf/2606.23416v1)
- 作者：Bacem Etteib、Daniele Lunghi、Tégawendé F. Bissyandé
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.CR、cs.AI
- 主题标签：LLM、Agent、Skill/Tool
- 阅读价值评分：17/20

### 摘要速读

LLM agents increasingly load skills, file-based packages of natural-language instructions written by third parties and distributed through marketplaces, that execute with the user's privileges. A single malicious skill can exfiltrate data, hijack the agent, or persist as a supply-chain foothold, which turns the skill marketplace into a new attack surface for agentic systems.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [VideoAgent: All-in-One Framework for Video Understanding and Editing](http://arxiv.org/abs/2606.23327v1)

- arXiv：[2606.23327](http://arxiv.org/abs/2606.23327v1)
- PDF：[https://arxiv.org/pdf/2606.23327v1](https://arxiv.org/pdf/2606.23327v1)
- 作者：Hengji Zhou、Lingxuan Huang、Jian Wang、Bing Zhou、Si Wu、Lianghao Xia、等
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Video editing has become essential in digital media creation, yet existing automated systems are restricted to short segment processing and domain-specific tasks. They face two critical limitations: i) inability to handle diverse video comprehension and editing operations, and ii) lack of long-video understanding for coherent narrative creation.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Tmax: A simple recipe for terminal agents](http://arxiv.org/abs/2606.23321v1)

- arXiv：[2606.23321](http://arxiv.org/abs/2606.23321v1)
- PDF：[https://arxiv.org/pdf/2606.23321v1](https://arxiv.org/pdf/2606.23321v1)
- 作者：Hamish Ivison、Junjie Oscar Yin、Rulin Shao、Teng Xiao、Nathan Lambert、Hannaneh Hajishirzi
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.CL
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Terminal-using agents have quickly become the most popular downstream application of language models (LMs). Despite their prevalence, relatively little academic work has examined RL-based training of these models, likely due to difficult benchmarks, a lack of data, and a lack of simple baseline recipes.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [AIR: Adaptive Interleaved Reasoning with Code in MLLMs](http://arxiv.org/abs/2606.23678v1)

- arXiv：[2606.23678](http://arxiv.org/abs/2606.23678v1)
- PDF：[https://arxiv.org/pdf/2606.23678v1](https://arxiv.org/pdf/2606.23678v1)
- 作者：Cong Han、Xiaohan Lan、Haibo Qiu、Yujie Zhong
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Skill/Tool、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Following the paradigm shift initiated by OpenAI o3, interleaved reasoning with code to enhance multimodal large language models (MLLMs) has become a pivotal research frontier. The existing literature focuses primarily on tool-use within vision-perception tasks.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、工具使用/技能学习、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [TailorMind: Towards Preference-Aligned Multimodal Content Generation](http://arxiv.org/abs/2606.23643v1)

- arXiv：[2606.23643](http://arxiv.org/abs/2606.23643v1)
- PDF：[https://arxiv.org/pdf/2606.23643v1](https://arxiv.org/pdf/2606.23643v1)
- 作者：Hengji Zhou、Ye Liu、Yufeng Liu、Si Wu、Lianghao Xia、Liqiang Nie
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.AI
- 主题标签：多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Personalized content systems depend on available UGC and struggle when suitable content is absent, delayed, or costly to create. Although multimodal generators can synthesize content on demand, how to translate behavioral traces into generation-ready preferences remains underexplored.

### 为什么值得读

多模态/视觉语言模型、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [VeriEvol: Scaling Multimodal Mathematical Reasoning via Verifiable Evol-Instruct](http://arxiv.org/abs/2606.23543v1)

- arXiv：[2606.23543](http://arxiv.org/abs/2606.23543v1)
- PDF：[https://arxiv.org/pdf/2606.23543v1](https://arxiv.org/pdf/2606.23543v1)
- 作者：Haoling Li、Kai Zheng、Jie Wu、Can Xu、Qingfeng Sun、Han Hu、等
- 发布时间：2026-06-22，更新时间：2026-06-22
- 类别：cs.AI、cs.CL、cs.CV、cs.LG
- 主题标签：多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Scaling reinforcement learning for visual mathematical reasoning requires more than generating harder questions: as data volume grows, the reward labels themselves must remain reliable. Yet existing data pipelines scale supervision while trusting the labeller, and policy-side methods assume the underlying answers are already correct.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [Detecting Malicious Agent Skills in the Wild using Attention](http://arxiv.org/abs/2606.23416v1) | LLM, Agent, Skill/Tool | 17 | 2026-06-22 | LLM agents increasingly load skills, file-based packages of natural-language instructions written by third parties and distributed through marketplaces, that execute with the user's privileges. |
| [VideoAgent: All-in-One Framework for Video Understanding and Editing](http://arxiv.org/abs/2606.23327v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 17 | 2026-06-22 | Video editing has become essential in digital media creation, yet existing automated systems are restricted to short segment processing and domain-specific tasks. |
| [Tmax: A simple recipe for terminal agents](http://arxiv.org/abs/2606.23321v1) | LLM, Agent, Reasoning, Safety/Eval | 17 | 2026-06-22 | Terminal-using agents have quickly become the most popular downstream application of language models (LMs). |
| [AIR: Adaptive Interleaved Reasoning with Code in MLLMs](http://arxiv.org/abs/2606.23678v1) | LLM, 多模态, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-22 | Following the paradigm shift initiated by OpenAI o3, interleaved reasoning with code to enhance multimodal large language models (MLLMs) has become a pivotal research frontier. |
| [TailorMind: Towards Preference-Aligned Multimodal Content Generation](http://arxiv.org/abs/2606.23643v1) | 多模态, Reasoning, Safety/Eval | 16 | 2026-06-22 | Personalized content systems depend on available UGC and struggle when suitable content is absent, delayed, or costly to create. |
| [VeriEvol: Scaling Multimodal Mathematical Reasoning via Verifiable Evol-Instruct](http://arxiv.org/abs/2606.23543v1) | 多模态, Agent, Reasoning, Safety/Eval | 16 | 2026-06-22 | Scaling reinforcement learning for visual mathematical reasoning requires more than generating harder questions: as data volume grows, the reward labels themselves must remain reliable. |
| [TriggerBench: Investigating Prospective Memory for Large Language Models](http://arxiv.org/abs/2606.23459v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-22 | While Large Language Models (LLMs) are increasingly deployed in long interactions, existing evaluations focus predominantly on retrospective memory (RM) via explicit queries. |
| [Towards Root Memories: Benchmarking and Enhancing Implicit Logical Memory Retrieval for Personalized LLMs](http://arxiv.org/abs/2606.23283v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-22 | Memory systems are essential for personalized Large Language Models (LLMs). |
| [On the Limits of Prompt-Conditioned Language Models as General-Purpose Learners](http://arxiv.org/abs/2606.23668v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-22 | Large Language Models (LLMs) are frequently portrayed as general-purpose solvers capable of solving arbitrary tasks. |
| [Dense Reward for Multi-View 3D Reasoning with Global Maps and Local Views](http://arxiv.org/abs/2606.23557v1) | LLM, 多模态, Reasoning | 15 | 2026-06-22 | Multi-view 3D Visual Question Answering (MV3D-VQA) requires integrating partial observations into a coherent 3D scene representation and selecting informative viewpoints for multi-step spatial reasoning. |
| [LightSTAR: Efficient Visual Document Retrieval via Lightweight Selection with Vision-Adaptive Refinement](http://arxiv.org/abs/2606.23539v1) | LLM, 多模态, Reasoning | 15 | 2026-06-22 | Visual document retrieval requires rapidly locating relevant pages from large multi-modal corpora in response to user queries. |
| [Self-Compacting Language Model Agents](http://arxiv.org/abs/2606.23525v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-22 | Long agent traces composed of chains of thought and tool calls accumulate stale content that anchor subsequent generations, and eventually outgrow the context window. |
| [Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference](http://arxiv.org/abs/2606.23521v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-22 | Long-running LLM agents keep valuable state resident on GPUs: KV caches, request schedulers, communication state, and sometimes online adapters. |
| [Semantic Browsing: Controllable Diversity for Image Generation](http://arxiv.org/abs/2606.23679v1) | LLM, 多模态, Agent, RAG/Memory | 14 | 2026-06-22 | Modern text-to-image models excel in visual fidelity and prompt adherence. |
| [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](http://arxiv.org/abs/2606.23654v1) | Agent, Skill/Tool, Reasoning, Safety/Eval | 14 | 2026-06-22 | Enterprise agents increasingly operate inside workspaces: they read heterogeneous files, invoke tools, and deliver business artifacts. |
| [HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](http://arxiv.org/abs/2606.23565v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-22 | LLM agents follow a practical execution loop in digital environments: they reason over structured states, invoke tools, inspect feedback, and revise actions. |
| [AOHP: An Open-Source OS-Level Agent Harness for Personalized, Efficient and Secure Interaction](http://arxiv.org/abs/2606.23449v1) | Agent, RAG/Memory, Safety/Eval | 14 | 2026-06-22 | AI agents are driving a new software paradigm, with the ability to autonomously call tools, extract information, manage memory, and complete tasks that span applications and data sources. |
| [Litmus: Zero-Label, Code-Driven Metric Specification for Evaluating AI Systems](http://arxiv.org/abs/2606.23403v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-22 | As agentic LLM systems move from prototypes to deployment across increasingly diverse domains, evaluating them has become both more important and more difficult. |
| [GRINQH: Graded Input-based Quantization Hierarchy for Efficient LLM Generation](http://arxiv.org/abs/2606.23419v1) | LLM, RAG/Memory | 13 | 2026-06-22 | Autoregressive decoding with LLMs is primarily bottlenecked by GPU memory bandwidth, especially in edge-computing settings. |
| [HyperQuant: A Rate-Distortion-Optimal Quantization Pipeline for Large Language and Diffusion Models](http://arxiv.org/abs/2606.23406v1) | LLM, 多模态, Reasoning | 13 | 2026-06-22 | We present HyperQuant (Hadamard, optimallY Packing, Entropy Rice-coding), a unified post-training quantization pipeline for the weights and the KV cache of large language and diffusion transformers. |
| [Faithful Grounded Visual Reasoning via Learned Proxy-Tokens](http://arxiv.org/abs/2606.23354v1) | LLM, 多模态, RAG/Memory, Reasoning | 13 | 2026-06-22 | Multimodal Large Language Models (MLLMs) have achieved remarkable success in Visual Question Answering (VQA), yet their "black-box" nature hinders deployment in critical domains. |
| [Data Selection Through Iterative Self-Filtering for Vision-Language Settings](http://arxiv.org/abs/2606.23611v1) | LLM, 多模态 | 12 | 2026-06-22 | The availability of large amounts of clean data is paramount to training neural networks. |
| [Distribution-Aware Diffusion-LLM for Robust Ultra-Long-Term Time Series Forecasting](http://arxiv.org/abs/2606.23391v1) | LLM, 多模态, Safety/Eval | 12 | 2026-06-22 | Time series forecasting is a fundamental machine learning task. |
| [Randomized YaRN Improves Length Generalization for Long-Context Reasoning](http://arxiv.org/abs/2606.23687v1) | LLM, Reasoning, Safety/Eval | 11 | 2026-06-22 | Large language models (LLMs) are typically pretrained on short sequences and then extended to work on longer sequences with additional training. |
| [MAS-PromptBench: When Does Prompt Optimization Improve Multi-Agent LLM Systems?](http://arxiv.org/abs/2606.23664v1) | LLM, Agent, Safety/Eval | 11 | 2026-06-22 | Multi-agent systems (MAS) offer a scalable path forward for agentic AI, comprising multiple LLM-based agents, each assigned a system prompt and a position within a workflow that governs inter-agent coordination and output aggregation. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-23 14:32:01 CST
