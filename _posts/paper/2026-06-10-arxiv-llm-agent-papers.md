---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-10)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-10 10:30:00 +0800
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

## [Pushing the Limits of LLM Tool Calling via Experiential Knowledge Integration and Activation](http://arxiv.org/abs/2606.10875v1)

- arXiv：[2606.10875](http://arxiv.org/abs/2606.10875v1)
- PDF：[https://arxiv.org/pdf/2606.10875v1](https://arxiv.org/pdf/2606.10875v1)
- 作者：Yupu Hao、Zhuoran Jin、Huanxuan Liao、Kang Liu、Jun Zhao
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.CL
- 主题标签：LLM、Agent、Skill/Tool、Reasoning
- 阅读价值评分：18/20

### 摘要速读

Large language models (LLMs) rely on tool use to act as autonomous agents, yet often fail in multi-step execution due to insufficient tool-related knowledge and ineffective knowledge activation. Therefore, we present a systematic study on how knowledge influences tool-use performance, covering the stages of knowledge acquisition, activation, and internalization.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Multi-Faceted Interactivity Alignment in Full-Duplex Speech Models](http://arxiv.org/abs/2606.11167v1)

- arXiv：[2606.11167](http://arxiv.org/abs/2606.11167v1)
- PDF：[https://arxiv.org/pdf/2606.11167v1](https://arxiv.org/pdf/2606.11167v1)
- 作者：Atsumoto Ohashi、Neil Zeghidour、Alexandre Défossez、Eugene Kharitonov
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.CL、eess.AS
- 主题标签：LLM、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Full-duplex spoken dialogue models can listen and speak simultaneously, making them a promising architecture for natural conversation. However, current models are trained solely with supervised learning through token-level likelihood maximization, which does not directly optimize interaction-level behaviors, causing interactivity issues such as excessive silence and ill-timed turn-taking.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像评测/数据集型工作，阅读重点应放在任务定义、数据构造、评价指标和 baseline 是否合理。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 评测指标能否解释真实使用风险，还是只覆盖了可测的表层行为？

## [FADA: Accessible fetal ultrasound interpretation and annotation with a selectively distilled unified vision-language model](http://arxiv.org/abs/2606.11106v1)

- arXiv：[2606.11106](http://arxiv.org/abs/2606.11106v1)
- PDF：[https://arxiv.org/pdf/2606.11106v1](https://arxiv.org/pdf/2606.11106v1)
- 作者：Mahmood Alzubaidi、Uzair Shah、Raden Muaz、Ines Abbes、Nader Mohammed、Abdullatif Magram、等
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Agent、Skill/Tool、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

A global shortage of trained sonographers limits prenatal ultrasound screening in low- and middle-income countries, where over half of pregnant women receive no skilled sonography. Current deep learning approaches address detection, segmentation, or classification in isolation, each demanding a separate model and expert-specified labels at inference.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Data Journalist Agent: Transforming Data into Verifiable Multimodal Stories](http://arxiv.org/abs/2606.11176v1)

- arXiv：[2606.11176](http://arxiv.org/abs/2606.11176v1)
- PDF：[https://arxiv.org/pdf/2606.11176v1](https://arxiv.org/pdf/2606.11176v1)
- 作者：Kevin Qinghong Lin、Batu EI、Yuhong Shi、Pan Lu、Philip Torr、James Zou
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.CV、cs.CL、cs.CY、cs.HC
- 主题标签：多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Data tells stories that shape society; the data journalist's job is to turn raw information into stories non-experts can trust. A high-quality news feature takes a newsroom team weeks: hunting for context, running statistics, choosing an angle, and designing visuals.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、工具使用/技能学习、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [IDEAL: In-DEpth ALignment Makes A Discrete Representation AutoEncoder](http://arxiv.org/abs/2606.11096v1)

- arXiv：[2606.11096](http://arxiv.org/abs/2606.11096v1)
- PDF：[https://arxiv.org/pdf/2606.11096v1](https://arxiv.org/pdf/2606.11096v1)
- 作者：Yitong Chen、Zijie Diao、Junke Wang、Lingyu Kong、Yixuan Ren、Bo He、等
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.CV
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Built on pretrained vision foundation models (VFMs), representation autoencoders (RAEs) have recently emerged as a promising approach for constructing semantically rich latent spaces for image generation. However, their reconstruction quality often remains suboptimal, largely because deep VFM representations do not preserve sufficient fine-grained visual detail.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、安全、对齐或鲁棒性、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [A History-Aware Visually Grounded Critic for Computer Use Agents](http://arxiv.org/abs/2606.11078v1)

- arXiv：[2606.11078](http://arxiv.org/abs/2606.11078v1)
- PDF：[https://arxiv.org/pdf/2606.11078v1](https://arxiv.org/pdf/2606.11078v1)
- 作者：Jaewoo Lee、Zaid Khan、Archiki Prasad、Justin Chih-Yao Chen、Supriyo Chakraborty、Kartik Balasubramaniam、等
- 发布时间：2026-06-09，更新时间：2026-06-09
- 类别：cs.AI、cs.CL、cs.CV
- 主题标签：多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Various test-time interventions for Computer Use Agents (CUAs), including critic models, have been developed to improve performance through pre-execution action evaluation in complex Graphical User Interface (GUI) environments. However, existing critics suffer from two key limitations: they (1) focus primarily on short-sighted decision loops (e.g., forgetting earlier actions) and (2) lack the visual grounding needed to detect flawed actions (e.g., clicking wrong UI elements).

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [Pushing the Limits of LLM Tool Calling via Experiential Knowledge Integration and Activation](http://arxiv.org/abs/2606.10875v1) | LLM, Agent, Skill/Tool, Reasoning | 18 | 2026-06-09 | Large language models (LLMs) rely on tool use to act as autonomous agents, yet often fail in multi-step execution due to insufficient tool-related knowledge and ineffective knowledge activation. |
| [Multi-Faceted Interactivity Alignment in Full-Duplex Speech Models](http://arxiv.org/abs/2606.11167v1) | LLM, Safety/Eval | 17 | 2026-06-09 | Full-duplex spoken dialogue models can listen and speak simultaneously, making them a promising architecture for natural conversation. |
| [FADA: Accessible fetal ultrasound interpretation and annotation with a selectively distilled unified vision-language model](http://arxiv.org/abs/2606.11106v1) | LLM, 多模态, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-09 | A global shortage of trained sonographers limits prenatal ultrasound screening in low- and middle-income countries, where over half of pregnant women receive no skilled sonography. |
| [Data Journalist Agent: Transforming Data into Verifiable Multimodal Stories](http://arxiv.org/abs/2606.11176v1) | 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-09 | Data tells stories that shape society; the data journalist's job is to turn raw information into stories non-experts can trust. |
| [IDEAL: In-DEpth ALignment Makes A Discrete Representation AutoEncoder](http://arxiv.org/abs/2606.11096v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-09 | Built on pretrained vision foundation models (VFMs), representation autoencoders (RAEs) have recently emerged as a promising approach for constructing semantically rich latent spaces for image generation. |
| [A History-Aware Visually Grounded Critic for Computer Use Agents](http://arxiv.org/abs/2606.11078v1) | 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-09 | Various test-time interventions for Computer Use Agents (CUAs), including critic models, have been developed to improve performance through pre-execution action evaluation in complex Graphical User Interface (GUI) environments. |
| [T1-Bench: Benchmarking Multi-Scenario Agents in Real-World Domains](http://arxiv.org/abs/2606.11070v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-09 | Recent advances in reasoning and tool-calling capabilities of large language models (LLMs) have enabled increasingly capable agentic systems. |
| [Architect-Ant: Editable Automatic Furnishing of Architectural Floor Plans](http://arxiv.org/abs/2606.10953v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-09 | Furnished floor plans are fundamental to real estate visualization, interior design, and architectural workflows. |
| [EEVEE: Towards Test-time Prompt Learning in the Real World for Self-Improving Agents](http://arxiv.org/abs/2606.11182v1) | LLM, Agent, RAG/Memory, Safety/Eval | 15 | 2026-06-09 | In this paper, we propose EEVEE, the first multi-dataset test-time prompt learning framework for LLM agents, enabling test-time prompt learning under real-world task streams. |
| [P3D-Bench: Benchmarking MLLMs for Parametric 3D Generation and Structural Reasoning](http://arxiv.org/abs/2606.11152v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-09 | Multimodal large language models can write code to produce complex programs as well as use programs to do 3D modeling, which opens up a new avenue for 3D generation powered by their priors, world knowledge and reasoning. |
| [ABC-Bench: An Agentic Bio-Capabilities Benchmark for Biosecurity](http://arxiv.org/abs/2606.11150v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-09 | Large language models (LLMs) are rapidly acquiring capabilities relevant to biological research, from literature synthesis to interpretation of experimental data. |
| [TRACE: A Unified Rollout Budget Allocation Framework for Efficient Agentic Reinforcement Learning](http://arxiv.org/abs/2606.11119v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-09 | Reinforcement learning with verifiable rewards (RLVR) is a promising approach for enhancing reasoning and agentic behavior in large language models. |
| [Mind the Gap: Can Frontier LLMs Pass a Standardized Office Proficiency Exam?](http://arxiv.org/abs/2606.10956v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-09 | The deployment of Large Language Model (LLM) agents for computer automation is accelerating, yet their ability to navigate complex, professional-grade productivity software is largely untested. |
| [Trace Only What You Need: Structure-Aware On-Demand Hypergraph Memory for Long-Document Question Answering](http://arxiv.org/abs/2606.10921v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-09 | Long-document question answering (QA) requires large language models (LLMs) to reason over evidence scattered across lengthy documents, where answers often depend on event order, section-level context, and cross-part evidence connections. |
| [The Shibboleth Effect: Auditing the Cross-Lingual Distributional Skew of Large Language Models](http://arxiv.org/abs/2606.11082v1) | LLM, Agent, Safety/Eval | 14 | 2026-06-09 | This study investigates cross-lingual distributional skew (the Shibboleth Effect) in frontier large language models (LLMs) subjected to sustained adversarial conditions. |
| [LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination](http://arxiv.org/abs/2606.10862v1) | 多模态, Reasoning, Safety/Eval | 14 | 2026-06-09 | Vision-Language-Action (VLA) models achieve strong performance on standard manipulation benchmarks, but most evaluations assume that task-relevant objects are fully visible. |
| [Next Forcing: Causal World Modeling with Multi-Chunk Prediction](http://arxiv.org/abs/2606.11187v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 13 | 2026-06-09 | Autoregressive video generation has emerged as a powerful paradigm for World Action Models (WAMs). |
| [AuRA: Internalizing Audio Understanding into LLMs as LoRA](http://arxiv.org/abs/2606.11033v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-09 | Recent efforts to extend large language models (LLMs) to speech inputs typically rely on cascaded ASR-LLM pipelines, end-to-end speech-language models, or bridge/distillation-based adaptation. |
| [Task Robustness via Re-Labelling Vision-Action Robot Data](http://arxiv.org/abs/2606.10918v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-09 | The recent trend in scaling models for robot learning has resulted in impressive policies that can perform various manipulation tasks and generalize to novel scenarios. |
| [AnyMod-LLVE: Low-Light Video Enhancement with Modality-Agnostic Inference](http://arxiv.org/abs/2606.11186v1) | 多模态, Reasoning | 12 | 2026-06-09 | Low-light video enhancement (LLVE) remains a challenging task due to severe information degradation under low-illumination conditions. |
| [Modeling Complex Behaviors: Multi-Personality Composition and Dynamic Switching in Vision-Language Models](http://arxiv.org/abs/2606.11074v1) | LLM, 多模态, Reasoning, Safety/Eval | 12 | 2026-06-09 | With the widespread deployment of Multimodal Large Language Models (MLLMs) in social interaction, understanding and controlling their behavior under complex personality conditions is essential. |
| [Recalling Too Well: Sycophancy Evaluation and Mitigation in Memory-Augmented Models](http://arxiv.org/abs/2606.10949v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-09 | Persistent memory systems promise to make LLMs more helpful by storing user beliefs over time. |
| [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](http://arxiv.org/abs/2606.10933v1) | LLM, Agent, Reasoning, Safety/Eval | 12 | 2026-06-09 | LLM-based coding agents are usually evaluated in familiar software settings: mainstream languages, common libraries, and public repositories. |
| [Role-Agent: Bootstrapping LLM Agents via Dual-Role Evolution](http://arxiv.org/abs/2606.10917v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-09 | Although Large Language Model (LLM) agents have demonstrated strong performance on complex tasks, their learning is often limited by inefficient interaction feedback and static training environments, which hinder broader generalization. |
| [Piper: A Programmable Distributed Training System](http://arxiv.org/abs/2606.11169v1) | LLM, RAG/Memory | 11 | 2026-06-09 | Large-scale model training increasingly relies on composing multiple parallelism strategies, such as data, pipeline, and expert parallelism, together with memory-saving optimizations like ZeRO. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-10 14:48:52 CST
