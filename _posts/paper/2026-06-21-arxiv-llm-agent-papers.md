---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-21)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-21 10:30:00 +0800
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

## [SARLO-80: Worldwide Slant SAR Language Optic Dataset 80cm](http://arxiv.org/abs/2606.20523v1)

- arXiv：[2606.20523](http://arxiv.org/abs/2606.20523v1)
- PDF：[https://arxiv.org/pdf/2606.20523v1](https://arxiv.org/pdf/2606.20523v1)
- 作者：Solène Debuysère、Nicolas Trouvé、Nathan Letheule、Elise Colin、Georgia Channing
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.CV、cs.AI、cs.DB
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：18/20

### 摘要速读

Multimodal foundation models have advanced rapidly thanks to large optical benchmarks, but comparable resources for synthetic aperture radar (SAR) remain limited. Existing SAR--optical datasets largely rely on low-resolution, intensity-only Ground Range Detected~(GRD) products and do not preserve complex-valued SAR measurements or native acquisition geometry, which restricts physically grounded multimodal learning.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [S-Agent: Spatial Tool-Use Elicits Reasoning for Spatial Intelligence](http://arxiv.org/abs/2606.20515v1)

- arXiv：[2606.20515](http://arxiv.org/abs/2606.20515v1)
- PDF：[https://arxiv.org/pdf/2606.20515v1](https://arxiv.org/pdf/2606.20515v1)
- 作者：Yalun Dai、Hao Li、Shulin Tian、Runmao Yao、Yuhao Dong、Fangzhou Hong、等
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.CV
- 主题标签：多模态、Agent、Skill/Tool、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：18/20

### 摘要速读

Real-world spatial intelligence requires reasoning over a continuous and evolving 3D world, yet existing VLMs and tool-augmented agents largely remain tied to static, stateless inference from isolated visual observations. We introduce \textbf{\textsc{S-Agent}}, a spatial tool-use agentic paradigm for understanding and reasoning over continuous multi-view images and videos.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、工具使用/技能学习、RAG、记忆或长上下文、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs](http://arxiv.org/abs/2606.20527v1)

- arXiv：[2606.20527](http://arxiv.org/abs/2606.20527v1)
- PDF：[https://arxiv.org/pdf/2606.20527v1](https://arxiv.org/pdf/2606.20527v1)
- 作者：Shaghayegh Kolli、Timo Cavelius、Nafiseh Nikeghbal、Samantha Dalal、Jana Diesner
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.CL、cs.CV
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Multimodal large language models (MLLMs) are increasingly deployed in personally and societally consequential settings, yet the visual cues that shape how these models judge people remain poorly understood. Prior work often compares different (groups of) individuals, making it difficult to separate appearance effects from identity differences.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [LLM agent safety, multi-turn red-teaming, jailbreak benchmarks, adversarial robustness, safety-critical systems](http://arxiv.org/abs/2606.20408v1)

- arXiv：[2606.20408](http://arxiv.org/abs/2606.20408v1)
- PDF：[https://arxiv.org/pdf/2606.20408v1](https://arxiv.org/pdf/2606.20408v1)
- 作者：Hanwool Lee、Dasol Choi、Bokyeong Kim、Seung Geun Kim、Haon Park
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.CR、cs.AI
- 主题标签：LLM、Agent、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Large language model (LLM) agents are increasingly proposed as supervisory components for safety-critical systems, yet their robustness under sustained, adaptive adversarial pressure remains poorly characterized. We present NRT-Bench, a benchmark for multi-turn red-teaming of LLM agents acting as operators of a safety-critical system, instantiated in a simulated nuclear power plant control room.

### 为什么值得读

大模型核心方向、Agent 与长程任务、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning](http://arxiv.org/abs/2606.20373v1)

- arXiv：[2606.20373](http://arxiv.org/abs/2606.20373v1)
- PDF：[https://arxiv.org/pdf/2606.20373v1](https://arxiv.org/pdf/2606.20373v1)
- 作者：Zepeng Li、Jie Ren、Zhanyong Tang、Jie Zheng、Zheng Wang
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.SE、cs.AI
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Large Language Models (LLMs) show promise for code compilation tasks, but applying them to runtime performance tuning is difficult due to complex microarchitectural effects and noisy runtime measurements. We present AutoPass, a multi-agent framework for compiler performance tuning that uses compiler and runtime evidence to guide LLM-generated optimization decisions.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [SPOT-E: Test-Time Entropy Shaping with Visual Spotlights for Frozen VLMs](http://arxiv.org/abs/2606.20244v1)

- arXiv：[2606.20244](http://arxiv.org/abs/2606.20244v1)
- PDF：[https://arxiv.org/pdf/2606.20244v1](https://arxiv.org/pdf/2606.20244v1)
- 作者：Bo Yin、Xiaobin Hu、Chengming Xu、Ruolin Shen、Mo Yang、Jiangning Zhang、等
- 发布时间：2026-06-18，更新时间：2026-06-18
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Vision-language models (VLMs) often underperform on evidence intensive tasks because decisive visual evidence are small, localized, and easy to overlook, leading to failures in evidence readout even when high-level reasoning is intact. Prior inference-time visual interventions can improve grounding without retraining, but they are largely open-loop and lack a mechanism to verify whether highlighted evidence is actually used.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、安全、对齐或鲁棒性、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [SARLO-80: Worldwide Slant SAR Language Optic Dataset 80cm](http://arxiv.org/abs/2606.20523v1) | LLM, 多模态, Reasoning, Safety/Eval | 18 | 2026-06-18 | Multimodal foundation models have advanced rapidly thanks to large optical benchmarks, but comparable resources for synthetic aperture radar (SAR) remain limited. |
| [S-Agent: Spatial Tool-Use Elicits Reasoning for Spatial Intelligence](http://arxiv.org/abs/2606.20515v1) | 多模态, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 18 | 2026-06-18 | Real-world spatial intelligence requires reasoning over a continuous and evolving 3D world, yet existing VLMs and tool-augmented agents largely remain tied to static, stateless inference from isolated visual observations. |
| [StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs](http://arxiv.org/abs/2606.20527v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-18 | Multimodal large language models (MLLMs) are increasingly deployed in personally and societally consequential settings, yet the visual cues that shape how these models judge people remain poorly understood. |
| [LLM agent safety, multi-turn red-teaming, jailbreak benchmarks, adversarial robustness, safety-critical systems](http://arxiv.org/abs/2606.20408v1) | LLM, Agent, Safety/Eval | 16 | 2026-06-18 | Large language model (LLM) agents are increasingly proposed as supervisory components for safety-critical systems, yet their robustness under sustained, adaptive adversarial pressure remains poorly characterized. |
| [AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning](http://arxiv.org/abs/2606.20373v1) | LLM, Agent, Reasoning, Safety/Eval | 16 | 2026-06-18 | Large Language Models (LLMs) show promise for code compilation tasks, but applying them to runtime performance tuning is difficult due to complex microarchitectural effects and noisy runtime measurements. |
| [SPOT-E: Test-Time Entropy Shaping with Visual Spotlights for Frozen VLMs](http://arxiv.org/abs/2606.20244v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-18 | Vision-language models (VLMs) often underperform on evidence intensive tasks because decisive visual evidence are small, localized, and easy to overlook, leading to failures in evidence readout even when high-level reasoning is intact. |
| [ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments](http://arxiv.org/abs/2606.20235v1) | LLM, Agent, Safety/Eval | 16 | 2026-06-18 | Academic paper search is a core step in scientific research, and LLM-based search agents are emerging as a promising paradigm for iterative, intent-driven literature exploration. |
| [TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living](http://arxiv.org/abs/2606.20561v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-18 | Long Video Question Answering (LVQA) requires identifying sparse, query-relevant evidence within hours-long untrimmed videos. |
| [Spectral Query-Key Product Weight Steering for Training-Free VLM Hallucination Mitigation](http://arxiv.org/abs/2606.20419v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 15 | 2026-06-18 | Vision-language models (VLMs) often generate fluent but visually unsupported descriptions, especially by mentioning objects absent from the image. |
| [Evaluating and Enhancing Negation Comprehension in Remote Sensing MLLMs](http://arxiv.org/abs/2606.20177v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-18 | Multimodal Large Language Models (MLLMs) have demonstrated remarkable success in various Remote Sensing (RS) tasks. |
| [Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems](http://arxiv.org/abs/2606.20493v1) | LLM, Agent, Safety/Eval | 14 | 2026-06-18 | When large language models serve as evaluators in multi-agent systems, their systematic evaluation biases propagate through the agent network. |
| [Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology](http://arxiv.org/abs/2606.20477v1) | LLM, 多模态, Safety/Eval | 14 | 2026-06-18 | We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. |
| [SoftSkill: Behavioral Compression for Contextual Adaptation](http://arxiv.org/abs/2606.20333v1) | LLM, Agent, Skill/Tool, Reasoning | 14 | 2026-06-18 | Agent skills are commonly deployed as natural-language Markdown files that encode answer policies, evidence-use habits, and task procedures. |
| [ELVA: Exploring Ranking-Driven Universal Multimodal Retrieval](http://arxiv.org/abs/2606.20280v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 14 | 2026-06-18 | Leveraging Multimodal Large Language Models (MLLMs) via contrastive learning has become a mainstream paradigm for improving the performance of Universal Multimodal Retrieval (UMR). |
| [Navigating Unreliable Parametric and Contextual Knowledge: Explicit Knowledge Conflict Resolution for LLM Inference](http://arxiv.org/abs/2606.20245v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-18 | Large language models (LLMs) have achieved strong performance across a wide range of language-based tasks by leveraging both extensive parametric knowledge and in-context learning ability, enabling them to incorporate external information provided in the input prompt. |
| [HilDA: Hierarchical Distillation with Diffusion for Advancing Self-Supervised LiDAR Pre-trainin](http://arxiv.org/abs/2606.20189v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-18 | Leveraging Vision Foundation Models (VFMs) for camera-to-LiDAR knowledge distillation offers a promising solution to the scarcity of annotated data needed to represent the immense geometric and kinematic diversity of real-world autonomous driving (AD). |
| [UNIEGO: Proxies as Mediators for Unified Egocentric Video Representation Learning](http://arxiv.org/abs/2606.20559v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-18 | Egocentric video understanding is inherently limited by the narrow perspective of wearable cameras: a single viewpoint, a single modality, a single model cannot capture the full richness of human action. |
| [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](http://arxiv.org/abs/2606.20512v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning | 13 | 2026-06-18 | LLM-based coding agents need higher-level operational knowledge about a repository (which files house which subsystems, how to run the test suite, which workflows have historically led to wrong fixes) that does not exist in the code itself. |
| [CRAX: Fast Safe Reinforcement Learning Benchmarking](http://arxiv.org/abs/2606.20376v1) | Agent, RAG/Memory, Safety/Eval | 13 | 2026-06-18 | Safety is a core concern for deploying reinforcement learning (RL) agents in real-world domains such as robotics and autonomous driving. |
| [Augmenting Game AI with Deep Reinforcement Learning](http://arxiv.org/abs/2606.20210v1) | 多模态, Agent, Reasoning | 13 | 2026-06-18 | Immersion in video games depends not only on graphics, audio, and game mechanics, but also on the quality of in-game characters. |
| [FlowMaps: Modeling Long-Term Multimodal Object Dynamics with Flow Matching](http://arxiv.org/abs/2606.20209v1) | 多模态, Agent, Reasoning | 13 | 2026-06-18 | Joint spatial and temporal understanding of 3D scenes is a crucial requirement for robots deployed in everyday household environments. |
| [Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving](http://arxiv.org/abs/2606.20537v1) | LLM, Agent, RAG/Memory, Reasoning | 12 | 2026-06-18 | Mainstream LLM serving systems reuse prefix work mainly through paged or radix key-value (KV) caches. |
| [HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining](http://arxiv.org/abs/2606.20521v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 12 | 2026-06-18 | Embodied foundation models are expected to benefit from data scaling like large language models, but face a much tighter data bottleneck. |
| [Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software](http://arxiv.org/abs/2606.20502v1) | LLM, Reasoning, Safety/Eval | 12 | 2026-06-18 | Whether LLMs scoring well on vulnerability benchmarks genuinely reason about security or merely pattern-match on contaminated data remains unresolved. |
| [Automating SKILL.md Generation for Computer-Using Agents via Interaction Trajectory Mining](http://arxiv.org/abs/2606.20363v1) | Agent, Skill/Tool, Safety/Eval | 12 | 2026-06-18 | Explicit skill libraries make computer-using agents easier to inspect, but it remains unclear whether such libraries can be mined from interaction data in a way that improves downstream policies. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-21 15:15:51 CST
