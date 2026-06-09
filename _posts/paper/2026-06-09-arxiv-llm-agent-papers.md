---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-09)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-09 10:30:00 +0800
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

## [SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks](http://arxiv.org/abs/2606.09669v1)

- arXiv：[2606.09669](http://arxiv.org/abs/2606.09669v1)
- PDF：[https://arxiv.org/pdf/2606.09669v1](https://arxiv.org/pdf/2606.09669v1)
- 作者：Hongcheng Gao、Hailong Qu、Jingyi Tang、Jiahao Wang、Zihao Huang、Hengkang Qiao、等
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.AI、cs.CL
- 主题标签：LLM、多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Spatial reasoning is a foundational capability for multimodal large language models (MLLMs) to perceive and operate within the physical world. However, existing benchmarks predominantly rely on passive evaluation (e.g., static VQA) or simulator-specific pipelines, failing to assess general interactive spatial understanding.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Streaming Interventions: Can Video Large Language Models Correct Mistakes as They Occur?](http://arxiv.org/abs/2606.09547v1)

- arXiv：[2606.09547](http://arxiv.org/abs/2606.09547v1)
- PDF：[https://arxiv.org/pdf/2606.09547v1](https://arxiv.org/pdf/2606.09547v1)
- 作者：Apratim Bhattacharyya、Shweta Mahajan、Sanjay Haresh、Rajeev Yasarla、Reza Pourreza、Litian Liu、等
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.CV、cs.LG
- 主题标签：LLM、多模态、Skill/Tool、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Learning everyday skills, like cooking a dish, relies increasingly on instructional media such as online videos. This opens the door to the use of video (and multimodal) large language models (LLMs) as task guidance assistants.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、工具使用/技能学习、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [iOSWorld: A Benchmark for Personally Intelligent Phone Agents](http://arxiv.org/abs/2606.09764v1)

- arXiv：[2606.09764](http://arxiv.org/abs/2606.09764v1)
- PDF：[https://arxiv.org/pdf/2606.09764v1](https://arxiv.org/pdf/2606.09764v1)
- 作者：Lawrence Keunho Jang、Mareks Woodside、Geronimo Carom、Andrew Keunwoo Jang、Jing Yu Koh、Ruslan Salakhutdinov
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.LG、cs.CL
- 主题标签：Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

A useful phone agent needs to be personally intelligent. It should reason over a user's identity, history, and preferences as they exist on the device, not just follow isolated instructions in an impersonal sandbox.

### 为什么值得读

Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [IS-CoT: Breaking the Long-form Generation Collapse via Interleaved Structural Thinking](http://arxiv.org/abs/2606.09709v1)

- arXiv：[2606.09709](http://arxiv.org/abs/2606.09709v1)
- PDF：[https://arxiv.org/pdf/2606.09709v1](https://arxiv.org/pdf/2606.09709v1)
- 作者：Zechen Sun、Yuyang Sun、Zecheng Tang、Juntao Li、Wenpeng Hu、Wenliang Chen、等
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.CL
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Generating coherent and controllable long-form content remains a persistent challenge for Large Language Models (LLMs). While reasoning-enhanced models have demonstrated success in logic-intensive domains, our evaluation reveals that they suffer from a severe length collapse in open-ended writing, where performance degrades sharply as target lengths exceed 2,000 words.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Civil Court Simulation with Large Language Models](http://arxiv.org/abs/2606.09632v1)

- arXiv：[2606.09632](http://arxiv.org/abs/2606.09632v1)
- PDF：[https://arxiv.org/pdf/2606.09632v1](https://arxiv.org/pdf/2606.09632v1)
- 作者：Yifan Chen、Haitao Li、Kaiyuan Zhang、Yueyue Wu、Qingyao Ai、Yiqun Liu
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.CL
- 主题标签：LLM、Agent、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Court simulation bridges legal education and judicial practice, yet human-based simulations are costly and difficult to scale. Large language models (LLMs) offer a scalable alternative, but existing court-simulation research mainly focuses on criminal cases.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [AI Scientists Are Only as Good as Their Evidence: A Stratified Ablation of Proprietary Data and Reasoning Skills in Drug-Asset Valuation](http://arxiv.org/abs/2606.09556v1)

- arXiv：[2606.09556](http://arxiv.org/abs/2606.09556v1)
- PDF：[https://arxiv.org/pdf/2606.09556v1](https://arxiv.org/pdf/2606.09556v1)
- 作者：Yinan Wang
- 发布时间：2026-06-08，更新时间：2026-06-08
- 类别：cs.AI
- 主题标签：LLM、Agent、Skill/Tool、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

AI Scientist agents are often evaluated as if capability were mainly a function of model quality, prompting, or reasoning scaffolds. We test a different hypothesis in drug-asset valuation: for knowledge-intensive scientific decisions, the limiting factor is often the evidence substrate the agent can access.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks](http://arxiv.org/abs/2606.09669v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-08 | Spatial reasoning is a foundational capability for multimodal large language models (MLLMs) to perceive and operate within the physical world. |
| [Streaming Interventions: Can Video Large Language Models Correct Mistakes as They Occur?](http://arxiv.org/abs/2606.09547v1) | LLM, 多模态, Skill/Tool, Safety/Eval | 17 | 2026-06-08 | Learning everyday skills, like cooking a dish, relies increasingly on instructional media such as online videos. |
| [iOSWorld: A Benchmark for Personally Intelligent Phone Agents](http://arxiv.org/abs/2606.09764v1) | Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-08 | A useful phone agent needs to be personally intelligent. |
| [IS-CoT: Breaking the Long-form Generation Collapse via Interleaved Structural Thinking](http://arxiv.org/abs/2606.09709v1) | LLM, Agent, Reasoning, Safety/Eval | 16 | 2026-06-08 | Generating coherent and controllable long-form content remains a persistent challenge for Large Language Models (LLMs). |
| [Civil Court Simulation with Large Language Models](http://arxiv.org/abs/2606.09632v1) | LLM, Agent, RAG/Memory, Reasoning | 16 | 2026-06-08 | Court simulation bridges legal education and judicial practice, yet human-based simulations are costly and difficult to scale. |
| [AI Scientists Are Only as Good as Their Evidence: A Stratified Ablation of Proprietary Data and Reasoning Skills in Drug-Asset Valuation](http://arxiv.org/abs/2606.09556v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-08 | AI Scientist agents are often evaluated as if capability were mainly a function of model quality, prompting, or reasoning scaffolds. |
| [FASE: Fast Adaptive Semantic Entropy for Code Quality](http://arxiv.org/abs/2606.09800v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-08 | Multi-agent code generation offers a promising paradigm for autonomous software development by simulating the human software engineering lifecycle. |
| [SIGA: Self-Evolving Coding-Agent Adapters for Scientific Simulation](http://arxiv.org/abs/2606.09774v1) | Agent, RAG/Memory, Reasoning | 15 | 2026-06-08 | Advanced scientific simulators expose specialized input languages that turn simulation goals into executable configurations, but learning them can cost domain scientists hours to days. |
| [Observability for Delegated Execution in Agentic AI Systems](http://arxiv.org/abs/2606.09692v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-08 | Delegation-scoped execution is not identifiable from standard observables: audit logs and execution traces can be identical under multiple incompatible delegation assignments. |
| [OmniGameArena: A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics](http://arxiv.org/abs/2606.09826v1) | LLM, 多模态, Agent, Skill/Tool, Safety/Eval | 14 | 2026-06-08 | Vision-language model (VLM) agents are increasingly deployed in interactive game environments. |
| [SearchSwarm: Towards Delegation Intelligence in Agentic LLMs for Long-Horizon Deep Research](http://arxiv.org/abs/2606.09730v1) | LLM, Agent, Reasoning | 14 | 2026-06-08 | Large language models are increasingly expected to handle complex, long-horizon real-world tasks whose context demands can grow without bound, yet model context windows remain inherently finite. |
| [End-to-End Context Compression at Scale](http://arxiv.org/abs/2606.09659v1) | LLM, Agent, RAG/Memory, Reasoning | 14 | 2026-06-08 | Long-context language model inference is bottlenecked by memory, as the KV cache grows with context length. |
| [Where Does the Answer Come From? Benchmarking View-Level Visual Evidence Identification in Multi-View MLLMs for Autonomous Driving](http://arxiv.org/abs/2606.09644v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 14 | 2026-06-08 | Multimodal large language models (MLLMs) achieve strong results on visual reasoning benchmarks, but answer accuracy alone does not indicate whether a model relied on the correct visual evidence. |
| [MAVIS: Multi-Agent Video Retrieval via Structured Video Understanding](http://arxiv.org/abs/2606.09641v1) | 多模态, Agent, Reasoning | 14 | 2026-06-08 | The dominant paradigm in video retrieval relies on embedding-based full-corpus scanning, which suffers from inherent computational inefficiency and the semantic asymmetry between information-dense videos and sparse textual queries. |
| [Gradient-Guided Reward Optimization for Inference-time Alignment](http://arxiv.org/abs/2606.09635v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-08 | Ensuring the reliability of Large Language Models (LLMs) under distribution drift requires inference-time adaptation. |
| [AGENTSERVESIM: A Hardware-aware Simulator for Multi-Turn LLM Agent Serving](http://arxiv.org/abs/2606.09613v1) | LLM, Agent, RAG/Memory | 14 | 2026-06-08 | Multi-turn LLM agents interleave model calls with external tool invocations, shifting serving from stateless request processing to stateful program execution. |
| [Automated IEP Generation from Traditional Chinese Parent-Teacher Interviews via Corpus-Grounded Feature Diffusion](http://arxiv.org/abs/2606.09603v1) | LLM, Safety/Eval | 14 | 2026-06-08 | Writing Individualized Education Programs (IEPs) is a high-labor, knowledge-intensive document burden; English-language research has demonstrated that generative AI can significantly reduce drafting time, yet automated IEP generation in Traditional Chinese remains virtually unexplored due to domain data scarcity, strict privacy regulations, and the absence of local evaluation benchmarks. |
| [Collaborative Human-Agent Protocol (CHAP)](http://arxiv.org/abs/2606.09751v1) | LLM, Agent, RAG/Memory, Reasoning | 13 | 2026-06-08 | Foundation models are moving from response generation into operational roles. |
| [HDSL: A Hierarchical Domain-Specific Language for Structured 3D Indoor Scene Generation and Localized Editing with LLM Agents](http://arxiv.org/abs/2606.09738v1) | LLM, 多模态, Agent, RAG/Memory, Safety/Eval | 13 | 2026-06-08 | Text-driven indoor scene generation and editing require an intermediate representation that language models can both produce and revise. |
| [FMplex: Model Virtualization for Serving Extensible Foundation Models](http://arxiv.org/abs/2606.09643v1) | LLM, 多模态, RAG/Memory | 13 | 2026-06-08 | Foundation models (FMs) are increasingly used as backbones for downstream tasks across language, vision, time-series, and multimodal applications. |
| [TABVERSE: Benchmarking Cross-Format Table Understanding in LLMs and VLMs](http://arxiv.org/abs/2606.09578v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-08 | Large Language Models (LLMs) and Vision-Language Models (VLMs) are increasingly evaluated on table reasoning tasks, but the role of table representation remains under-explored. |
| [PRISM: Recovering Instruction Sets from Language Model Activations](http://arxiv.org/abs/2606.09563v1) | LLM, Agent, Reasoning | 13 | 2026-06-08 | As LLMs are deployed as agents, reliable monitoring requires knowing not only what they output, but which instructions are steering their behavior. |
| [Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models](http://arxiv.org/abs/2606.09749v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 12 | 2026-06-08 | Vision-Language-Action (VLA) models have demonstrated impressive end-to-end performance across a variety of robotic manipulation tasks. |
| [Optical Reasoning: Rethinking Images as an Expressive Reasoning Medium Beyond Text](http://arxiv.org/abs/2606.09585v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-08 | Chain-of-Thought (CoT) improves the performance of Large Language Models (LLMs) and has been extended to Multimodal Large Language Models (MLLMs). |
| [Code Is More Than Text: Uncertainty Estimation for Code Generation](http://arxiv.org/abs/2606.09577v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-08 | Large language models (LLMs) are increasingly deployed as code generators, where silently wrong programs pose real safety and reliability risks. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-09 14:32:07 CST
