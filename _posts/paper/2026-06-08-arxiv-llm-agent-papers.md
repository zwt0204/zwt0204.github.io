---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-08)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-08 10:30:00 +0800
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

## [MemDreamer: Decoupling Perception and Reasoning for Long Video Understanding via Hierarchical Graph Memory and Agentic Retrieval Mechanism](http://arxiv.org/abs/2606.07512v1)

- arXiv：[2606.07512](http://arxiv.org/abs/2606.07512v1)
- PDF：[https://arxiv.org/pdf/2606.07512v1](https://arxiv.org/pdf/2606.07512v1)
- 作者：Cong Chen、Guo Gan、Kaixiang Ji、ChaoYang Zhang、Zhen Yang、Guangming Yao、等
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.CV、cs.AI、cs.CL
- 主题标签：LLM、多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Current Vision-Language Models struggle with hours-long videos because processing full-length visual sequences induces prohibitive token explosion and attention dilution. To overcome this, we introduce MemDreamer to decouple perception and reasoning, shifting long-video understanding into an agentic exploration process.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Closed-Form Spectral Regularization for Multi-Task Model Merging](http://arxiv.org/abs/2606.07289v1)

- arXiv：[2606.07289](http://arxiv.org/abs/2606.07289v1)
- PDF：[https://arxiv.org/pdf/2606.07289v1](https://arxiv.org/pdf/2606.07289v1)
- 作者：Yongxian Wei、Runxi Cheng、Xingxuan Zhang、Li Shen、Chun Yuan、Peng Cui、等
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.LG、cs.CV
- 主题标签：LLM、多模态、RAG/Memory、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Model merging combines several independently fine-tuned experts into a single multi-task model without any training data, reducing the storage, serving, and decentralized-development costs of large foundation models. State-of-the-art merging methods formulate merging as a layer-wise quadratic interference minimization problem.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、RAG、记忆或长上下文、评测基准或数据集、安全、对齐或鲁棒性、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [MMAE: A Massive Multitask Audio Editing Benchmark](http://arxiv.org/abs/2606.07229v1)

- arXiv：[2606.07229](http://arxiv.org/abs/2606.07229v1)
- PDF：[https://arxiv.org/pdf/2606.07229v1](https://arxiv.org/pdf/2606.07229v1)
- 作者：Ziyang Ma、Ruiqi Yan、Ruiyang Xu、Jie Fang、Zhikang Niu、Yi-Wen Chao、等
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.SD、cs.CL、cs.MM
- 主题标签：多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

We introduce MMAE, a Massive Multitask Audio Editing benchmark, serving as the first comprehensive evaluation testbed designed for general-purpose instruction-based audio editing. Spurred by the shift toward intelligent creation, interactive editing has rapidly expanded from visual domains, pioneered by models like Nano-banana 2 for images and Gemini-Omni for video, into audio.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Watch, Remember, Reason: Human-View Video Understanding with MLLMs](http://arxiv.org/abs/2606.07433v1)

- arXiv：[2606.07433](http://arxiv.org/abs/2606.07433v1)
- PDF：[https://arxiv.org/pdf/2606.07433v1](https://arxiv.org/pdf/2606.07433v1)
- 作者：Jiahao Meng、Yue Tan、Qi Xu、Kuan Gao、Weisong Liu、Yanwei Li、等
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.CV、cs.AI、cs.MM
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Video understanding is being rapidly transformed by multimodal large language models (MLLMs), as research moves from short clips to long, multimodal, and knowledge-intensive video scenarios. These scenarios require models to handle sparse evidence, long-range dependencies, multimodal alignment, and reliable inference under limited computational budgets.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Self-evolving LLM agents with in-distribution Optimization](http://arxiv.org/abs/2606.07367v1)

- arXiv：[2606.07367](http://arxiv.org/abs/2606.07367v1)
- PDF：[https://arxiv.org/pdf/2606.07367v1](https://arxiv.org/pdf/2606.07367v1)
- 作者：Yudi Zhang、Meng Fang、Zhenfang Chen、Mykola Pechenizkiy
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.LG
- 主题标签：LLM、Agent、RAG/Memory、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Large Language Models (LLMs) have recently emerged as powerful controllers for interactive agents in complex environments, yet training them to perform reliable long-horizon decision making remains a fundamental challenge. A key difficulty lies in credit assignment: agents often receive delayed rewards only at the end of episodes.

### 为什么值得读

大模型核心方向、Agent 与长程任务、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [VeriDrive: Verifiable Counterfactual Supervision for Cost-Efficient Vision-Language Planning](http://arxiv.org/abs/2606.07338v1)

- arXiv：[2606.07338](http://arxiv.org/abs/2606.07338v1)
- PDF：[https://arxiv.org/pdf/2606.07338v1](https://arxiv.org/pdf/2606.07338v1)
- 作者：Zikai Zhang、Hubert P. H. Shum、Toby P. Breckon
- 发布时间：2026-06-05，更新时间：2026-06-05
- 类别：cs.CV
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Vision-language driving models increasingly use reasoning supervision to bridge perception, prediction, and planning, but existing driving rationales are often free-form and expensive to generate with frontier models. We present VeriDrive, a framework for constructing planning-oriented, verifiable counterfactual supervision.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [MemDreamer: Decoupling Perception and Reasoning for Long Video Understanding via Hierarchical Graph Memory and Agentic Retrieval Mechanism](http://arxiv.org/abs/2606.07512v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-05 | Current Vision-Language Models struggle with hours-long videos because processing full-length visual sequences induces prohibitive token explosion and attention dilution. |
| [Closed-Form Spectral Regularization for Multi-Task Model Merging](http://arxiv.org/abs/2606.07289v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 17 | 2026-06-05 | Model merging combines several independently fine-tuned experts into a single multi-task model without any training data, reducing the storage, serving, and decentralized-development costs of large foundation models. |
| [MMAE: A Massive Multitask Audio Editing Benchmark](http://arxiv.org/abs/2606.07229v1) | 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-05 | We introduce MMAE, a Massive Multitask Audio Editing benchmark, serving as the first comprehensive evaluation testbed designed for general-purpose instruction-based audio editing. |
| [Watch, Remember, Reason: Human-View Video Understanding with MLLMs](http://arxiv.org/abs/2606.07433v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-05 | Video understanding is being rapidly transformed by multimodal large language models (MLLMs), as research moves from short clips to long, multimodal, and knowledge-intensive video scenarios. |
| [Self-evolving LLM agents with in-distribution Optimization](http://arxiv.org/abs/2606.07367v1) | LLM, Agent, RAG/Memory, Safety/Eval | 16 | 2026-06-05 | Large Language Models (LLMs) have recently emerged as powerful controllers for interactive agents in complex environments, yet training them to perform reliable long-horizon decision making remains a fundamental challenge. |
| [VeriDrive: Verifiable Counterfactual Supervision for Cost-Efficient Vision-Language Planning](http://arxiv.org/abs/2606.07338v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-05 | Vision-language driving models increasingly use reasoning supervision to bridge perception, prediction, and planning, but existing driving rationales are often free-form and expensive to generate with frontier models. |
| [Seeing Without Exposing: Adaptive Privacy Control for Open-World, Context-Hungry MLLMs](http://arxiv.org/abs/2606.07175v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-05 | Multimodal large language models (MLLMs) have raised new privacy challenges. |
| [Planning-aligned Token Compression for Long-Context Autonomous Driving](http://arxiv.org/abs/2606.07464v1) | Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-05 | Monolithic vision-action models represent an emerging paradigm in autonomous driving. |
| [Act As a Real Researcher: A Suite of Benchmarks Evaluating Frontier LLMs and Agentic Harnesses in Research Lifecycle](http://arxiv.org/abs/2606.07462v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-05 | As foundation models advance and agent scaffolding becomes increasingly sophisticated, agents have demonstrated remarkable proficiency in complex, long-horizon coding tasks and even autonomous experiment execution. |
| [Skill-3D: Evolving Scene-Aware Skills for Agentic 3D Spatial Reasoning](http://arxiv.org/abs/2606.07436v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning | 15 | 2026-06-05 | This paper explores agentic 3D spatial understanding, i.e., MLLM agents performing 3D reasoning through tool use. |
| [Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills](http://arxiv.org/abs/2606.07412v1) | LLM, Agent, Skill/Tool, Safety/Eval | 15 | 2026-06-05 | LLM-driven software engineering agents have become a central testbed for real-world language-model capability, yet their training remains limited by the availability of high-quality SWE tasks. |
| [A robust PPG foundation model using multimodal physiological supervision](http://arxiv.org/abs/2606.07365v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 15 | 2026-06-05 | Photoplethysmography (PPG), a non-invasive measure of changes in blood volume, is widely used in both wearable devices and clinical settings. |
| [Hierarchical Certified Semantic Commitment for Byzantine-Resilient LLM-Agent Collaboration](http://arxiv.org/abs/2606.07316v1) | LLM, Agent, RAG/Memory, Safety/Eval | 15 | 2026-06-05 | Byzantine collaboration among large-language-model agents requires a finality-control primitive: given delivered stochastic, structured natural-language proposals, the protocol must decide whether the round supports a commit, what kind of commit, or a typed safe abort. |
| [SWE-Explore: Benchmarking How Coding Agents Explore Repositories](http://arxiv.org/abs/2606.07297v1) | Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-05 | Repository-level coding benchmarks such as SWE-bench have driven a rapid surge in the capabilities of coding agents. |
| [TEVI: Text-Conditioned Editing of Visual Representations via Sparse Autoencoders for Improved Vision-Language Alignment](http://arxiv.org/abs/2606.07451v1) | LLM, 多模态, Reasoning, Safety/Eval | 14 | 2026-06-05 | Vision-language models such as CLIP are highly useful for diverse tasks due to their shared image-text embedding space. |
| [When Recovery Matters: The Blind Spot of Surrogate Privacy in MLLM Editing](http://arxiv.org/abs/2606.07171v1) | LLM, 多模态, Safety/Eval | 14 | 2026-06-05 | Multimodal Large Language Models (MLLMs) enable flexible instruction-driven image editing, but privacy risks arise when user images expose diverse and user-specific private content. |
| [TraRA: Trajectory-level Recognition Aggregation for Video Text Spotting in Urban Surveillance](http://arxiv.org/abs/2606.07161v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-05 | Video Text Spotting (VTS) is essential for urban surveillance and intelligent transportation systems, enabling automated reading of street signs, vehicle markings, and scene text in video streams. |
| [M$^3$Exam: Benchmarking Multimodal Memory for Realistic User-Agent Interactions](http://arxiv.org/abs/2606.07402v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-05 | Language agents are increasingly deployed over accumulating multimodal information, yet existing benchmarks assume a human-human form with sparse visuals and straightforward content, evaluating neither reasoning over authentic multimodal file interaction nor the interpretation of concealed user information. |
| [Beyond Waypoints: A Trajectory-Centric Waypointing Paradigm for Vision-Language Navigation](http://arxiv.org/abs/2606.07244v1) | 多模态, Agent, Reasoning, Safety/Eval | 13 | 2026-06-05 | Vision-Language Navigation in Continuous Environments (VLN-CE) requires agents to follow natural-language instructions while navigating in real-world-like environments. |
| [LLM-Guided Evolution for Medical Decision Pipelines](http://arxiv.org/abs/2606.07342v1) | LLM, 多模态, Safety/Eval | 12 | 2026-06-05 | Adapting large language models (LLMs) to clinical workflows often requires costly fine-tuning or manual prompt and pipeline engineering. |
| [HKVM-RAG: Key-Value-Separated Hypergraph Evidence Organization for Multi-Hop RAG](http://arxiv.org/abs/2606.07218v1) | LLM, RAG/Memory, Safety/Eval | 12 | 2026-06-05 | Multi-hop RAG poses a data-engineering problem beyond passage matching: under fixed retrieval budgets, a system must organize retrieved text into evidence units that expose answer chains. |
| [From Correctness to Utility: Gain-Based Prefix Evaluation for LLM Reasoning](http://arxiv.org/abs/2606.07190v1) | LLM, Reasoning, Safety/Eval | 12 | 2026-06-05 | Reasoning prefixes shape the future trajectory of LLM problem solving, yet existing process reward models usually evaluate them through local step correctness. |
| [Agentopia: Long-Term Life Simulation and Learning in Agent Societies](http://arxiv.org/abs/2606.07513v1) | LLM, Agent, RAG/Memory, Safety/Eval | 11 | 2026-06-05 | Humans learn from social life. |
| [Your UnEmbedding Matrix is Secretly a Feature Lens for Text Embeddings](http://arxiv.org/abs/2606.07502v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 11 | 2026-06-05 | Large language models exhibit impressive zero-shot capabilities across a wide range of downstream tasks. |
| [Sycophantic Praise: Evaluating Excessive Praise in Language Models](http://arxiv.org/abs/2606.07441v1) | LLM, Reasoning, Safety/Eval | 11 | 2026-06-05 | Sycophancy in language models is typically studied as excessive agreement or validation, while explicit praise and flattery have received comparatively little attention. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-08 18:22:23 CST
