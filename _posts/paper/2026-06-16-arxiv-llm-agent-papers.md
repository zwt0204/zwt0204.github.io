---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-16)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-16 10:30:00 +0800
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

## [Decoupling Semantics from Distortions: Multi-Scale Two-Stream Vision-Language Alignment for AI-Generated Image Quality Assessment](http://arxiv.org/abs/2606.16799v1)

- arXiv：[2606.16799](http://arxiv.org/abs/2606.16799v1)
- PDF：[https://arxiv.org/pdf/2606.16799v1](https://arxiv.org/pdf/2606.16799v1)
- 作者：Zijie Meng
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Existing vision-language model (VLM)-based AI-generated image quality assessment (AIGIQA) methods suffer from a fundamental semantic-distortion dimensional conflict: monolithic representations optimized for semantic discrimination inherently entangle compositional understanding with low-level perceptual sensitivity, rendering them blind to fine-grained quality degradations. We introduce MST-CLIPIQA, a multi-scale two-stream framework that achieves hierarchical vision-language alignment through explicit represent...

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Structure-aware Knowledge-guided Heterogeneous Mamba for Zygomaticomaxillary Suture Assessment](http://arxiv.org/abs/2606.16749v1)

- arXiv：[2606.16749](http://arxiv.org/abs/2606.16749v1)
- PDF：[https://arxiv.org/pdf/2606.16749v1](https://arxiv.org/pdf/2606.16749v1)
- 作者：Xiaoqi Guo、Birui Chen、Xinquan Yang、Chaoyun Zhang、Xuefen Liu、Mianjie Zheng、等
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CV
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

The Zygomaticomaxillary Suture is a key circummaxillary structure that connects the zygomatic bone and the maxilla, which serves as a primary site of resistance during maxillary advancement, and its maturation status directly influences the timing and efficacy of orthopedic interventions. However, accurate staging of ZMS maturation remains challenging due to subtle high-frequency transitions in suture lines and the global semantic ambiguity between adjacent stages.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Context-Aware RL for Agentic and Multimodal LLMs](http://arxiv.org/abs/2606.17053v1)

- arXiv：[2606.17053](http://arxiv.org/abs/2606.17053v1)
- PDF：[https://arxiv.org/pdf/2606.17053v1](https://arxiv.org/pdf/2606.17053v1)
- 作者：Peiyang Xu、Bangzheng Li、Sijia Liu、Karthik R. Narasimhan、Pramod Viswanath、Prateek Mittal、等
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CL、cs.CV
- 主题标签：LLM、多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Large language models (LLMs) often fail when answering requires identifying a small but decisive piece of evidence within a long or complex context, such as a single line in a tool trace or a subtle detail in an image. We propose ContextRL, a context-aware reinforcement learning (RL) method that improves long-horizon reasoning and multimodal performance through an \emph{indirect} auxiliary objective.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents](http://arxiv.org/abs/2606.17029v1)

- arXiv：[2606.17029](http://arxiv.org/abs/2606.17029v1)
- PDF：[https://arxiv.org/pdf/2606.17029v1](https://arxiv.org/pdf/2606.17029v1)
- 作者：Minghang Zhu、Chuyang Wei、Junhao Xu、Yilin Cheng、Zhumin Chen、Jiyan He
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CL
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio](http://arxiv.org/abs/2606.17041v1)

- arXiv：[2606.17041](http://arxiv.org/abs/2606.17041v1)
- PDF：[https://arxiv.org/pdf/2606.17041v1](https://arxiv.org/pdf/2606.17041v1)
- 作者：Anzhe Xie、Weihang Su、Yujia Zhou、Yiqun Liu、Qingyao Ai
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CL、cs.IR
- 主题标签：LLM、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [FusionRS: A Large-Scale RGB-Infrared Remote Sensing Dataset for Dual-Modal Vision-Language Foundation Models](http://arxiv.org/abs/2606.17020v1)

- arXiv：[2606.17020](http://arxiv.org/abs/2606.17020v1)
- PDF：[https://arxiv.org/pdf/2606.17020v1](https://arxiv.org/pdf/2606.17020v1)
- 作者：Jiaju Han、Ben Zhang、Xuemeng Sun、Qike Zhang、Yuxian Dong、Chengyin Hu、等
- 发布时间：2026-06-15，更新时间：2026-06-15
- 类别：cs.CV、cs.AI
- 主题标签：LLM、多模态、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Remote sensing vision-language models have advanced Earth observation understanding, but most existing work remains centered on RGB imagery, leaving the complementary information in infrared data underexplored. Infrared images provide distinctive cues, including thermal intensity structures, object boundaries, and illumination-invariant scene features, which can enrich visual-language learning beyond conventional RGB observations.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、评测基准或数据集、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [Decoupling Semantics from Distortions: Multi-Scale Two-Stream Vision-Language Alignment for AI-Generated Image Quality Assessment](http://arxiv.org/abs/2606.16799v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-15 | Existing vision-language model (VLM)-based AI-generated image quality assessment (AIGIQA) methods suffer from a fundamental semantic-distortion dimensional conflict: monolithic representations optimized for semantic discrimination inherently entangle compositional understanding with low-level perceptual sensitivity, rendering them blind to fine-grained quality degradations. |
| [Structure-aware Knowledge-guided Heterogeneous Mamba for Zygomaticomaxillary Suture Assessment](http://arxiv.org/abs/2606.16749v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 17 | 2026-06-15 | The Zygomaticomaxillary Suture is a key circummaxillary structure that connects the zygomatic bone and the maxilla, which serves as a primary site of resistance during maxillary advancement, and its maturation status directly influences the timing and efficacy of orthopedic interventions. |
| [Context-Aware RL for Agentic and Multimodal LLMs](http://arxiv.org/abs/2606.17053v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-15 | Large language models (LLMs) often fail when answering requires identifying a small but decisive piece of evidence within a long or complex context, such as a single line in a tool trace or a subtle detail in an image. |
| [DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents](http://arxiv.org/abs/2606.17029v1) | LLM, Agent, Reasoning, Safety/Eval | 16 | 2026-06-15 | Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. |
| [Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio](http://arxiv.org/abs/2606.17041v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-15 | Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. |
| [FusionRS: A Large-Scale RGB-Infrared Remote Sensing Dataset for Dual-Modal Vision-Language Foundation Models](http://arxiv.org/abs/2606.17020v1) | LLM, 多模态, Safety/Eval | 15 | 2026-06-15 | Remote sensing vision-language models have advanced Earth observation understanding, but most existing work remains centered on RGB imagery, leaving the complementary information in infrared data underexplored. |
| [TokenPilot: Cache-Efficient Context Management for LLM Agents](http://arxiv.org/abs/2606.17016v1) | LLM, Agent, RAG/Memory | 15 | 2026-06-15 | As LLM agents are deployed in long-horizon sessions, context accumulation drives up inference costs. |
| [Binary Tracking for Spatial QA and Navigation with Open Vision-Language Models](http://arxiv.org/abs/2606.16902v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-15 | This work addresses spatial question answering for service robots traversing long egocentric routes. |
| [Semantic Flip: Synthetic OOD Generation for Robust Refusal in Embodied Question Answering and Spatial Localization](http://arxiv.org/abs/2606.16898v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-15 | Detecting unanswerable user queries remains essential for the reliable deployment of real-world embodied agents. |
| [How Much Can We Trust LLM Search Agents? Measuring Endorsement Vulnerability to Web Content Manipulation](http://arxiv.org/abs/2606.16821v1) | LLM, Agent, Skill/Tool, Safety/Eval | 15 | 2026-06-15 | Large language model (LLM)-based search agents synthesize open-web content into actionable recommendations on behalf of users, creating a risk that attacker-published pages are transformed into endorsed claims. |
| [LabOSBench: Benchmarking Computer Use Agents for Scientific Instrument Control](http://arxiv.org/abs/2606.16802v1) | LLM, 多模态, Agent, Safety/Eval | 15 | 2026-06-15 | Current computer-use benchmarks primarily focus on software operation tasks in virtualized systems, whereas scientific instrumentation scenarios require coordinated control over complex interfaces, and feedback-driven parameter adjustment. |
| [OpenClaw-Skill: Collective Skill Tree Search for Agentic Large Language Models](http://arxiv.org/abs/2606.16774v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-15 | Equipping Large Language Model (LLM) agents with effective skills is crucial for solving complex tasks in real-world systems like OpenClaw. |
| [Skill-to-LoRA: From Using Skills to Learning Behaviors for Token-Efficient LLM Agents](http://arxiv.org/abs/2606.16769v1) | LLM, Agent, Skill/Tool, Reasoning, Safety/Eval | 15 | 2026-06-15 | Agent skills are commonly distributed as SKILL.md files: human-readable procedural documents that describe workflows, tools, resources, and domain conventions. |
| [Consensus-based Agentic Large Language Model Framework for Harmonized Tariff Schedule Code Classification](http://arxiv.org/abs/2606.16987v1) | LLM, Agent, Reasoning | 14 | 2026-06-15 | Accurate Harmonized Tariff Schedule (HTS) code classification is essential for customs clearance, duty assessment, trade statistics, and regulatory compliance in maritime logistics. |
| [GIST-CMTF: Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents](http://arxiv.org/abs/2606.16813v1) | LLM, Agent, Skill/Tool | 14 | 2026-06-15 | Tool-augmented LLM agents rely on runtime filtering to decide which tools should be visible at each step. |
| [The Art of Mixology: Mixup-based Obfuscation for Privacy-Preserving Split Learning in Large Language Models](http://arxiv.org/abs/2606.16801v1) | LLM | 14 | 2026-06-15 | Split learning provides a practical paradigm for resource-constrained users to train Large Language Models (LLMs) by offloading computation-intensive layers to a server while keeping raw data local. |
| [A Multi-Center Benchmark for Abdominal Disease Diagnosis and Report Generation from Non-Contrast CT](http://arxiv.org/abs/2606.16991v1) | 多模态, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-15 | Multiphasic contrast-enhanced CT (CECT) is widely used for abdominal lesion characterization, yet it carries inherent risks of contrast-induced nephropathy, escalates acquisition burden, and heavily contributes to radiologist workload. |
| [Robust Dual-Signal Fusion: Hybrid Neuro-Symbolic Gating with Compressed Chain-of-Thought Refinement for Irony Detection in Social Media Texts](http://arxiv.org/abs/2606.16845v1) | LLM, Reasoning, Safety/Eval | 13 | 2026-06-15 | Large Language Models (LLMs) natively default to literal semantic interpretations, making zero-shot irony detection a persistent challenge. |
| [ATOM-Bench: A Real-World Benchmark for Atomic Skills and Compositional Generalization in Manipulation Policies](http://arxiv.org/abs/2606.16826v1) | LLM, Skill/Tool, Safety/Eval | 13 | 2026-06-15 | Generalist manipulation policies are increasingly presented as foundation models for robotic control, but their real-world generalization remains difficult to diagnose. |
| [Tying the Loop -- Tied Expert Layers in Mixture-of-Experts Language Models](http://arxiv.org/abs/2606.16825v1) | LLM, RAG/Memory | 13 | 2026-06-15 | Mixture-of-Experts (MoE) architectures efficiently scale Large Language Models (LLMs) by activating only a small fraction of their experts per token, yet the full parameter count - dominated by the expert parameters - must be held in training and inference memory. |
| [Understanding the Behaviors of Environment-aware Information Retrieval](http://arxiv.org/abs/2606.16817v1) | LLM, RAG/Memory, Reasoning | 13 | 2026-06-15 | Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. |
| [LLM-based Visual Code Completion for Aerospace Geometric Design](http://arxiv.org/abs/2606.16806v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-15 | Recent advances in both Large Language Models (LLMs) and Vision Language Models (VLMs) have seen a step change in their ability to perform visual code completion, but the aerospace industry, which prioritizes safety and explainabilty over rapid LLM adoption, currently has no publicly announced LLM-based geometric design copilot systems in commercial use by aerospace Original Equipment Manufacturers (OEMs). |
| [Gen-VCoT: Generative Visual Chain-of-Thought Reasoning via Diffusion-Based RGB Intermediate Representations](http://arxiv.org/abs/2606.16783v1) | LLM, 多模态, Reasoning, Safety/Eval | 13 | 2026-06-15 | Multimodal large language models (MLLMs) excel at visual reasoning but rely on text-based chain-of-thought (CoT), lacking interpretable visual intermediates. |
| [GD$^2$PO: Mitigating Multi-Reward Conflicts via Group-Dynamic reward-Decoupled Policy Optimization](http://arxiv.org/abs/2606.16771v1) | LLM, Reasoning, Safety/Eval | 13 | 2026-06-15 | As LLMs advance, post-training reinforcement learning (RL) increasingly relies on multi-dimensional rewards to cultivate comprehensive capabilities. |
| [Geometric Action Model for Robot Policy Learning](http://arxiv.org/abs/2606.17046v1) | LLM, 多模态, Reasoning, Safety/Eval | 12 | 2026-06-15 | Generalist robot policies must follow user instructions while reasoning about how objects, cameras, and robot actions interact in the 3D physical world. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-16 16:27:00 CST
