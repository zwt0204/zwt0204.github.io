---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-17)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-17 10:30:00 +0800
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

## [Seeing Is Not Screening: Multimodal Hidden Instruction Attacks on Agent Skill Scanners](http://arxiv.org/abs/2606.18198v1)

- arXiv：[2606.18198](http://arxiv.org/abs/2606.18198v1)
- PDF：[https://arxiv.org/pdf/2606.18198v1](https://arxiv.org/pdf/2606.18198v1)
- 作者：Xiaojun Jia、Jie Liao、Simeng Qin、Ke Ma、Wenbo Guo、Yebo Feng、等
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.CR、cs.CV
- 主题标签：LLM、多模态、Agent、Skill/Tool、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Agent skills are emerging as an important attack surface in LLM-based systems. Through an empirical study of existing skill scanners, we find that current defenses primarily rely on textual descriptions, manifests, and source code as the main signals for security analysis, which can leave visually conveyed malicious intent insufficiently examined.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、工具使用/技能学习、推理、代码或复杂任务、安全、对齐或鲁棒性、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [When LLMs Analyze Scars: From Images to Clinically-Meaningful Features](http://arxiv.org/abs/2606.18063v1)

- arXiv：[2606.18063](http://arxiv.org/abs/2606.18063v1)
- PDF：[https://arxiv.org/pdf/2606.18063v1](https://arxiv.org/pdf/2606.18063v1)
- 作者：Ruman Wang、Hangting Ye
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.CV、cs.AI、cs.LG
- 主题标签：LLM、多模态、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Medical image classification faces a fundamental dilemma: while deep learning models achieve remarkable performance at scale, real-world clinical scenarios often suffer from severe data scarcity due to annotation costs, privacy constraints, and disease rarity. This challenge is particularly pronounced in pathological scar classification, where differentiating keloids from hypertrophic scars requires subtle expert knowledge and labeled images are extremely limited.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、安全、对齐或鲁棒性、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents](http://arxiv.org/abs/2606.18037v1)

- arXiv：[2606.18037](http://arxiv.org/abs/2606.18037v1)
- PDF：[https://arxiv.org/pdf/2606.18037v1](https://arxiv.org/pdf/2606.18037v1)
- 作者：Ander Alvarez、Santhiya Rajan、Samuel Mugel、Román Orús
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.AI、cs.CL、cs.MA
- 主题标签：LLM、Agent、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Tool-using LLM agents increasingly use the Model Context Protocol (MCP) to answer from heterogeneous evidence sources, including search, APIs, databases, clinical records, and formulary tools. Standard factuality metrics usually test whether an answer is supported by pooled evidence, missing a provenance-sensitive failure mode: a claim may be supported somewhere while being attributed to the wrong source.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Future Dynamic 3D Reconstruction: A 3D World Model with Disentangled Ego-Motion](http://arxiv.org/abs/2606.18250v1)

- arXiv：[2606.18250](http://arxiv.org/abs/2606.18250v1)
- PDF：[https://arxiv.org/pdf/2606.18250v1](https://arxiv.org/pdf/2606.18250v1)
- 作者：Nils Morbitzer、Jonathan Evers、Artem Savkin、Thomas Stauner、Nassir Navab、Federico Tombari、等
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.CV
- 主题标签：LLM、多模态、Agent、RAG/Memory
- 阅读价值评分：15/20

### 摘要速读

Forecasting the evolution of dynamic environments is crucial for autonomous agents. While generative world models have recently achieved high photorealism in 2D video synthesis by mixing ego-motion and environmental dynamics within the image plane, they exhibit physical inconsistencies, such as morphing or vanishing objects, especially over long time horizons.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、训练/后训练方法、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [EventDrive: Event Cameras for Vision-Language Driving Intelligence](http://arxiv.org/abs/2606.18242v1)

- arXiv：[2606.18242](http://arxiv.org/abs/2606.18242v1)
- PDF：[https://arxiv.org/pdf/2606.18242v1](https://arxiv.org/pdf/2606.18242v1)
- 作者：Dongyue Lu、Rong Li、Ao Liang、Lingdong Kong、Wei Yin、Lai Xing Ng、等
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.CV
- 主题标签：LLM、多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Event cameras sense the world through asynchronous brightness changes with microsecond latency and high dynamic range, offering motion fidelity far beyond frame-based sensors and capturing temporal structure that conventional exposures often miss. These properties make events a powerful complement to RGB in autonomous driving, especially under blur, glare, and rapid motion, where frame-based perception can become unreliable.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [RubricsTree: Scalable and Evolving Open-Ended Evaluation of Personal Health Agents across Health Memory and Medical Skills](http://arxiv.org/abs/2606.18203v1)

- arXiv：[2606.18203](http://arxiv.org/abs/2606.18203v1)
- PDF：[https://arxiv.org/pdf/2606.18203v1](https://arxiv.org/pdf/2606.18203v1)
- 作者：Weizhi Zhang、Zechen Li、Hamid Palangi、Ben Graef、A. Ali Heydari、Simon A. Lee、等
- 发布时间：2026-06-16，更新时间：2026-06-16
- 类别：cs.CL、cs.AI
- 主题标签：LLM、Agent、Skill/Tool、RAG/Memory、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

The LLM-empowered personal health agents with user health (sensor) metrics have offered a promising pathway to alleviate global disparities in healthcare access. However, large-scale clinical deployment remains constrained by an open-ended evaluation bottleneck: physician annotation is reliable but costly and unscalable, while LLM-as-a-judge evaluators are scalable but subjective, inconsistent, and sometimes clinically misaligned.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、RAG、记忆或长上下文、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [Seeing Is Not Screening: Multimodal Hidden Instruction Attacks on Agent Skill Scanners](http://arxiv.org/abs/2606.18198v1) | LLM, 多模态, Agent, Skill/Tool, Reasoning | 16 | 2026-06-16 | Agent skills are emerging as an important attack surface in LLM-based systems. |
| [When LLMs Analyze Scars: From Images to Clinically-Meaningful Features](http://arxiv.org/abs/2606.18063v1) | LLM, 多模态, Reasoning | 16 | 2026-06-16 | Medical image classification faces a fundamental dilemma: while deep learning models achieve remarkable performance at scale, real-world clinical scenarios often suffer from severe data scarcity due to annotation costs, privacy constraints, and disease rarity. |
| [ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents](http://arxiv.org/abs/2606.18037v1) | LLM, Agent, Safety/Eval | 16 | 2026-06-16 | Tool-using LLM agents increasingly use the Model Context Protocol (MCP) to answer from heterogeneous evidence sources, including search, APIs, databases, clinical records, and formulary tools. |
| [Future Dynamic 3D Reconstruction: A 3D World Model with Disentangled Ego-Motion](http://arxiv.org/abs/2606.18250v1) | LLM, 多模态, Agent, RAG/Memory | 15 | 2026-06-16 | Forecasting the evolution of dynamic environments is crucial for autonomous agents. |
| [EventDrive: Event Cameras for Vision-Language Driving Intelligence](http://arxiv.org/abs/2606.18242v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 15 | 2026-06-16 | Event cameras sense the world through asynchronous brightness changes with microsecond latency and high dynamic range, offering motion fidelity far beyond frame-based sensors and capturing temporal structure that conventional exposures often miss. |
| [RubricsTree: Scalable and Evolving Open-Ended Evaluation of Personal Health Agents across Health Memory and Medical Skills](http://arxiv.org/abs/2606.18203v1) | LLM, Agent, Skill/Tool, RAG/Memory, Safety/Eval | 15 | 2026-06-16 | The LLM-empowered personal health agents with user health (sensor) metrics have offered a promising pathway to alleviate global disparities in healthcare access. |
| [WEQA: Wearable hEalth Question Answering with Query-Adaptive Agentic Reasoning](http://arxiv.org/abs/2606.18147v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-16 | Language models are remarkably capable at medical question answering, in some cases surpassing the accuracy of general physicians. |
| [OmniPlan: An Adaptive Framework for Timely and Near-Optimal Network Planning Optimization](http://arxiv.org/abs/2606.18105v1) | LLM, RAG/Memory, Reasoning | 15 | 2026-06-16 | Network planning optimization is a fundamental problem across diverse domains, including transportation systems, communication networks, and power grids. |
| [Agentic AI-based Framework for Mitigating Premature Diagnostic Handoff and Silent Hallucination in Healthcare Applications](http://arxiv.org/abs/2606.18068v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-16 | Recent advances in Large Language Models (LLMs) and multi-agent systems have driven the rise of Agentic AI, showing promise for medical reasoning. |
| [PseudoBench: Measuring How Agentic Auto-Research Fuels Pseudoscience](http://arxiv.org/abs/2606.18060v1) | LLM, Agent, Safety/Eval | 15 | 2026-06-16 | As Large Language Model based agents enter autonomous scientific research, their ability to resist pseudoscience becomes increasingly important. |
| [Compositional Skill Routing for LLM Agents: Decompose, Retrieve, and Compose](http://arxiv.org/abs/2606.18051v1) | LLM, Agent, Skill/Tool, Reasoning, Safety/Eval | 15 | 2026-06-16 | LLM agents increasingly rely on external skills -- reusable tool specifications -- but real-world tasks often require composing multiple skills, not just selecting one. |
| [PhaseWin: An Efficient Search Algorithm for Faithful Visual Attribution](http://arxiv.org/abs/2606.18008v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-16 | Visual attribution is a fundamental tool for interpreting modern vision and vision-language models, particularly when their decisions must be inspected, diagnosed, or audited. |
| [ReproRepo: Scaling Reproducibility Audits with GitHub Repository Issues](http://arxiv.org/abs/2606.18237v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-16 | Reproducing research results from papers and released code is central to scientific progress. |
| [EvolveNav: Proactive Preflection and Self-Evolving Memory for Zero-Shot Object Goal Navigation](http://arxiv.org/abs/2606.18235v1) | LLM, Agent, RAG/Memory | 14 | 2026-06-16 | Zero-Shot Object-Goal Navigation (ZS-OGN) requires embodied agents to explore and locate target objects without any prior training. |
| [Darshana Graph: A Parallel Commentary Corpus for Comparative Indian Philosophy, with Stylometric and Exploratory Graph Analyses](http://arxiv.org/abs/2606.18222v1) | LLM, Reasoning, Safety/Eval | 14 | 2026-06-16 | We introduce Darshana Graph, a corpus of over 125,000 text records spanning classical Hindu, Buddhist, and Jain philosophical traditions, drawn from public-domain and openly licensed translations of sources including the Bhagavad Gita, Brahma Sutras, principal Upanishads, the Pali Canon, and core Jain texts. |
| [Zone of Proximal Policy Optimization: Teacher in Prompts, Not Gradients](http://arxiv.org/abs/2606.18216v1) | LLM, 多模态, Safety/Eval | 14 | 2026-06-16 | Knowledge distillation transfers a teacher's competence to a small student but is brittle in the small-student regime: forcing the student to imitate logits from a much larger teacher concentrates it on the teacher's sharpest modes, hurting generalization on benchmark families beyond the training corpus. |
| [Learning from the Self-future: On-policy Self-distillation for dLLMs](http://arxiv.org/abs/2606.18195v1) | LLM, Reasoning, Safety/Eval | 14 | 2026-06-16 | On-policy self-distillation (OPSD) has proven effective for post-training large language models (LLMs), yet its application to diffusion LLMs (dLLMs) remains unexplored. |
| [EgoCS-400K: An Egocentric Gameplay Dataset for World Models](http://arxiv.org/abs/2606.18180v1) | 多模态, Agent, RAG/Memory, Safety/Eval | 14 | 2026-06-16 | The shift from video generation to interactive world modeling places new demands on data: beyond captioned videos, world models require temporally aligned video-action-language trajectories grounded in the actions, camera motion, states, and events that drive future scene changes. |
| [A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics](http://arxiv.org/abs/2606.17962v1) | LLM, Agent, Reasoning | 14 | 2026-06-16 | Reasoning about what agents can achieve through strategic interaction is a core challenge in Multi-Agent Systems (MAS). |
| [Learning Cardiac Electrophysiology Digital Twins Through Agentic Discovery of Hybrid Structure](http://arxiv.org/abs/2606.18154v1) | LLM, Agent, Reasoning | 13 | 2026-06-16 | Building personalized cardiac electrophysiology (EP) digital twins requires identifying the appropriate model structure for each patient, not merely fitting parameters. |
| [LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling](http://arxiv.org/abs/2606.18023v1) | Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-16 | Looped Transformers scale latent computation by repeatedly applying shared blocks, but sequential looping increases latency and KV-cache memory with the loop count. |
| [Beyond Visual Cues: CoT-Enhanced Reasoning for Semi-supervised Medical Image Segmentation](http://arxiv.org/abs/2606.17958v1) | LLM, 多模态, RAG/Memory, Reasoning | 13 | 2026-06-16 | Semi-supervised medical image segmentation has emerged as a dominant research problem in medical image analysis, mitigating annotation scarcity by leveraging consistency regularization on unlabeled data. |
| [The Stanford EDGAR Filings Dataset: Reconstructing U.S. Corporate and Financial Disclosures into Layout-Faithful and Token-Efficient Pretraining Data](http://arxiv.org/abs/2606.18192v1) | LLM, Reasoning, Safety/Eval | 12 | 2026-06-16 | As high-quality public web corpora become increasingly exhausted, clean long-context documents have become a scarce and expensive source of training data for large language models (LLMs). |
| [Qwen-RobotNav Technical Report: A Scalable Navigation Model Designed for an Agentic Navigation System](http://arxiv.org/abs/2606.18112v1) | 多模态, Agent, Reasoning, Safety/Eval | 12 | 2026-06-16 | Agentic navigation systems require a base navigation model whose observation strategy can be externally reconfigured at inference time, because instruction following, object search, target tracking, and autonomous driving share the same perception-planning backbone yet demand fundamentally different strategies for consuming the visual stream. |
| [Trust the Right Teacher: Quality-Aware Self-Distillation for GUI Grounding](http://arxiv.org/abs/2606.18101v1) | LLM, 多模态, Safety/Eval | 12 | 2026-06-16 | Graphical user interface (GUI) grounding requires vision-language models (VLMs) to identify small target elements in high-resolution screenshots and predict precise screen coordinates. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-17 15:33:46 CST
