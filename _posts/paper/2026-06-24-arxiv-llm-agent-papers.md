---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-24)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-24 10:30:00 +0800
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

## [UniDrive: A Unified Vision-Language and Grounding Framework for Interpretable Risk Understanding in Autonomous Driving](http://arxiv.org/abs/2606.24759v1)

- arXiv：[2606.24759](http://arxiv.org/abs/2606.24759v1)
- PDF：[https://arxiv.org/pdf/2606.24759v1](https://arxiv.org/pdf/2606.24759v1)
- 作者：Xiaowei Gao、Pengxiang Li、Yitai Cheng、Ruihan Xu、James Haworth、Stephen Law、等
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：19/20

### 摘要速读

Recent multimodal large language models (MLLMs) have shown strong potential for autonomous driving scene understanding, yet existing methods still face a fundamental trade-off between temporal reasoning and spatial precision. Models that rely on single-frame or low-resolution inputs often miss small, distant, or partially occluded hazards, while language-centric driving models frequently provide limited grounded evidence for their explanations.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [CineCap: Structured Reasoning with Spatio-Temporal Anchors for Cinematographic Video Captioning](http://arxiv.org/abs/2606.24636v1)

- arXiv：[2606.24636](http://arxiv.org/abs/2606.24636v1)
- PDF：[https://arxiv.org/pdf/2606.24636v1](https://arxiv.org/pdf/2606.24636v1)
- 作者：Xinyu Mao、Yuhui Zeng、Xiaokun Liu、Wenyu Qin、Meng Wang、Xin Tao、等
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.AI
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：18/20

### 摘要速读

Cinematographic captioning aims to describe how a video is filmed using professional film-language concepts such as camera movement, shot size, depth of field, composition, and shooting angle. This capability is important for fine-grained video understanding and controllable movie-quality video generation, yet remains underexplored in existing multimodal large language models.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [EG-VQA: Benchmarking Verifiable Video Question Answering with Grounded Temporal Evidence](http://arxiv.org/abs/2606.24797v1)

- arXiv：[2606.24797](http://arxiv.org/abs/2606.24797v1)
- PDF：[https://arxiv.org/pdf/2606.24797v1](https://arxiv.org/pdf/2606.24797v1)
- 作者：Linpeng Huang、Weixing Chen、Zexin Chen、Yang Liu、Liang Lin
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Recent advances in Video Large Language Models (Video-LLMs) have yielded promising performance on video question answering (VideoQA). Nevertheless, existing benchmarks are predominantly evaluated through answer correctness, while the grounding of predictions in relevant video evidence remains largely unexamined.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Evaluating the Interpretability of Sparse Autoencoders with Concept Annotations](http://arxiv.org/abs/2606.24716v1)

- arXiv：[2606.24716](http://arxiv.org/abs/2606.24716v1)
- PDF：[https://arxiv.org/pdf/2606.24716v1](https://arxiv.org/pdf/2606.24716v1)
- 作者：Jonas Klotz、Cassio F. Dantas、Pallavi Jain、Diego Marcos、Begüm Demir
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Sparse autoencoders (SAEs) are increasingly used to extract interpretable concepts from vision and vision language models, yet existing evaluation methods largely rely on proxy metrics or qualitative inspection rather than measuring semantic correspondence. We present a human-grounded evaluation framework that quantifies alignment between SAE latents and human-annotated concepts, without requiring user studies, and validate this matching through targeted attribute perturbations.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [IV-CoT: Implicit Visual Chain-of-Thought for Structure-Aware Text-to-Image Generation](http://arxiv.org/abs/2606.24849v1)

- arXiv：[2606.24849](http://arxiv.org/abs/2606.24849v1)
- PDF：[https://arxiv.org/pdf/2606.24849v1](https://arxiv.org/pdf/2606.24849v1)
- 作者：Zixuan Li、Haokun Lin、Yicheng Xiao、Zhiwei Li、Xinyang Song、Zelong Zheng、等
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Unified multi-modal large language models (MLLMs) have achieved strong text-to-image generation quality, but still struggle with structure-aware prompt following, where object counts, spatial relations, attribute bindings, and coarse layouts must be preserved. We attribute this limitation in part to the entanglement of structural planning and appearance rendering within a single conditioning stream.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [SHERLOC: Structured Diagnostic Localization for Code Repair Agents](http://arxiv.org/abs/2606.24820v1)

- arXiv：[2606.24820](http://arxiv.org/abs/2606.24820v1)
- PDF：[https://arxiv.org/pdf/2606.24820v1](https://arxiv.org/pdf/2606.24820v1)
- 作者：Hovhannes Tamoyan、Sean Narenthiran、Erik Arakelyan、Mira Mezini、Boris Ginsburg
- 发布时间：2026-06-23，更新时间：2026-06-23
- 类别：cs.CL
- 主题标签：LLM、Agent、Skill/Tool、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

LLM agents solve repository-level coding tasks through multi-turn tool use, but utilize half their budget on locating faults before editing. Dedicated localization frameworks have emerged, yet are still evaluated as file retrieval rather than actionable diagnosis, producing locations without the diagnostic context a repair agent needs.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [UniDrive: A Unified Vision-Language and Grounding Framework for Interpretable Risk Understanding in Autonomous Driving](http://arxiv.org/abs/2606.24759v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 19 | 2026-06-23 | Recent multimodal large language models (MLLMs) have shown strong potential for autonomous driving scene understanding, yet existing methods still face a fundamental trade-off between temporal reasoning and spatial precision. |
| [CineCap: Structured Reasoning with Spatio-Temporal Anchors for Cinematographic Video Captioning](http://arxiv.org/abs/2606.24636v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 18 | 2026-06-23 | Cinematographic captioning aims to describe how a video is filmed using professional film-language concepts such as camera movement, shot size, depth of field, composition, and shooting angle. |
| [EG-VQA: Benchmarking Verifiable Video Question Answering with Grounded Temporal Evidence](http://arxiv.org/abs/2606.24797v1) | LLM, 多模态, Reasoning, Safety/Eval | 17 | 2026-06-23 | Recent advances in Video Large Language Models (Video-LLMs) have yielded promising performance on video question answering (VideoQA). |
| [Evaluating the Interpretability of Sparse Autoencoders with Concept Annotations](http://arxiv.org/abs/2606.24716v1) | LLM, 多模态, Reasoning, Safety/Eval | 17 | 2026-06-23 | Sparse autoencoders (SAEs) are increasingly used to extract interpretable concepts from vision and vision language models, yet existing evaluation methods largely rely on proxy metrics or qualitative inspection rather than measuring semantic correspondence. |
| [IV-CoT: Implicit Visual Chain-of-Thought for Structure-Aware Text-to-Image Generation](http://arxiv.org/abs/2606.24849v1) | LLM, 多模态, RAG/Memory, Reasoning | 16 | 2026-06-23 | Unified multi-modal large language models (MLLMs) have achieved strong text-to-image generation quality, but still struggle with structure-aware prompt following, where object counts, spatial relations, attribute bindings, and coarse layouts must be preserved. |
| [SHERLOC: Structured Diagnostic Localization for Code Repair Agents](http://arxiv.org/abs/2606.24820v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning | 16 | 2026-06-23 | LLM agents solve repository-level coding tasks through multi-turn tool use, but utilize half their budget on locating faults before editing. |
| [Are We Ready For An Agent-Native Memory System?](http://arxiv.org/abs/2606.24775v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-23 | Memory for large language model (LLM) agents has rapidly evolved from simple retrieval-augmented mechanisms into a data management system that supports persistent information storage, retrieval, update, consolidation, and dynamic lifecycle governance throughout agent execution. |
| [SAFARI: Scaling Long Horizon Agentic Fault Attribution via Active Investigation](http://arxiv.org/abs/2606.24626v1) | LLM, Agent, RAG/Memory, Reasoning | 16 | 2026-06-23 | As autonomous agents tackle increasingly complex multi-step, multi-agent tasks, their execution trajectories have scaled beyond the constraints of even the largest context windows. |
| [Privacy-Preserving RAG via Multi-Agent Semantic Rewriting: Achieving Confidentiality Without Compromising Contextual Fidelity](http://arxiv.org/abs/2606.24623v1) | LLM, Agent, RAG/Memory, Reasoning | 16 | 2026-06-23 | Retrieval-Augmented Generation enhances large language models by incorporating external knowledge, but deploying it in sensitive scenarios risks privacy leakage via malicious prompts. |
| [Qwen-AgentWorld: Language World Models for General Agents](http://arxiv.org/abs/2606.24597v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-23 | A world model predicts environment dynamics based on current observations and actions, serving as a core cognitive mechanism for reasoning and planning. |
| [Are Text-to-Image Models Inductivist Turkeys? A Counterfactual Benchmark for Causal Reasoning](http://arxiv.org/abs/2606.24548v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-23 | Text-to-image (T2I) generation models have achieved remarkable progress in producing visually realistic images from natural language prompts. |
| [Reinforcement Learning for Computer-Use Agents with Autonomous Evaluation](http://arxiv.org/abs/2606.24515v1) | LLM, 多模态, Agent, RAG/Memory, Safety/Eval | 16 | 2026-06-23 | Computer-Use Agents (CUAs) execute high-level user goals by perceiving and acting directly within graphical user interfaces. |
| [VisCritic: Visual State Comparison as Process Reward for GUI Agents](http://arxiv.org/abs/2606.24525v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 15 | 2026-06-23 | GUI agents powered by vision-language models show strong potential for automating digital tasks, yet frequently fail in long-horizon scenarios due to the absence of step-level verification. |
| [CANDLE: Character-level Arabic Noise Deduplication using Lightweight Encoder](http://arxiv.org/abs/2606.24758v1) | LLM, Reasoning, Safety/Eval | 14 | 2026-06-23 | Handling repeated characters in text can be tricky, since they can represent either the correct spelling of a word or informal character elongation often seen in social media posts. |
| [Agentic Collaborative Cognition for Zero-Shot 3D Understanding](http://arxiv.org/abs/2606.24649v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-23 | Recent advancements have explored agentic zero-shot 3D understanding by reformulating it as video keyframe understanding with Multimodal Large Language Models (MLLMs). |
| [ASALT: Adaptive State Alignment for Lateral Transfer in Multi-agent Reinforcement Learning](http://arxiv.org/abs/2606.24601v1) | Agent, Safety/Eval | 14 | 2026-06-23 | Multi-agent reinforcement learning (MARL) addresses the problem of training multiple agents that pursue collaborative, competitive, or mixed objectives. |
| [MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery](http://arxiv.org/abs/2606.24595v1) | LLM, Agent, RAG/Memory, Safety/Eval | 14 | 2026-06-23 | Long-term memory promises LLM agents that grow more capable across sessions, maintaining an accurate, evolving understanding of the user that interaction forms. |
| [AGORA: An Archive-Grounded Benchmark for Agentic Workplace Document Reasoning](http://arxiv.org/abs/2606.24526v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-23 | Large language models are increasingly deployed as agents that reason over documents rather than answer from parametric knowledge. |
| [DeepBD: A Grounded Agentic Workflow for Variant Prioritization and Diagnosis of Genetic Birth Defects](http://arxiv.org/abs/2606.24779v1) | LLM, Agent, Safety/Eval | 13 | 2026-06-23 | Birth defects are a major cause of fetal loss, neonatal morbidity and long-term disability. |
| [Scaling Laws for Task-Specific LLM Distillation](http://arxiv.org/abs/2606.24747v1) | LLM, Reasoning, Safety/Eval | 13 | 2026-06-23 | Large Language Models (LLMs) achieve strong performance across a growing range of domains, yet their scale poses deployment challenges in applications where latency and cost constraints are critical. |
| [BioMedVR: Confusion-Aware Mixture-of-Prompt Experts for Biomedical Visual Reprogramming](http://arxiv.org/abs/2606.24740v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 13 | 2026-06-23 | Recent advances in vision-language models (VLMs) such as CLIP have demonstrated strong generalization across natural-image domains. |
| [FlowPipe: LLM-Enhanced Conditional Generative Flow Networks for Data Preparation Pipeline Construction](http://arxiv.org/abs/2606.24679v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-23 | Data preparation pipelines improve data quality in machine learning by transforming raw tables into learning-ready data through sequential cleaning and feature transformation operators. |
| [ViTexQA: A Multi-Frame Temporal Perception Dataset for Video Text Question Answering](http://arxiv.org/abs/2606.24602v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-23 | Despite remarkable progress in multimodal understanding, current MLLMs still exhibit limitations in video text understanding, particularly when semantics emerge through the integration of temporally distributed textual cues across multiple frames. |
| [AdversaBench: Automated LLM Red-Teaming with Multi-Judge Confirmation and Cross-Model Transferability](http://arxiv.org/abs/2606.24589v1) | LLM, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-23 | Scaling adversarial evaluation of large language models requires both a method for generating hard inputs and a reliable way to confirm that resulting failures are real. |
| [PointVG-R: Internalizing Geometric Reasoning in MLLMs for Precise Pointing Localization via Visual Chain of Thought](http://arxiv.org/abs/2606.24539v1) | LLM, 多模态, Reasoning | 13 | 2026-06-23 | Pointing-based visual grounding requires models to precisely locate target objects by deciphering complex spatial relationships between the visual scene and pointing gestures. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-24 14:28:52 CST
