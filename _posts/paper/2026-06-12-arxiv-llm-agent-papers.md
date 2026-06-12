---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-12)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-12 10:30:00 +0800
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

## [InterleaveThinker: Reinforcing Agentic Interleaved Generation](http://arxiv.org/abs/2606.13679v1)

- arXiv：[2606.13679](http://arxiv.org/abs/2606.13679v1)
- PDF：[https://arxiv.org/pdf/2606.13679v1](https://arxiv.org/pdf/2606.13679v1)
- 作者：Dian Zheng、Harry Lee、Manyuan Zhang、Kaituo Feng、Zoey Guo、Ray Zhang、等
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.CV
- 主题标签：多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Recent image generators have demonstrated impressive photorealism and instruction-following capabilities in single-image generation and editing. However, constrained by their architectures, they cannot achieve interleaved generation (text-image sequence), which has crucial applications in visual narratives, guidance, and embodied manipulation.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、训练/后训练方法、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Agents-K1: Towards Agent-native Knowledge Orchestration](http://arxiv.org/abs/2606.13669v1)

- arXiv：[2606.13669](http://arxiv.org/abs/2606.13669v1)
- PDF：[https://arxiv.org/pdf/2606.13669v1](https://arxiv.org/pdf/2606.13669v1)
- 作者：Zongsheng Cao、Bihao Zhan、Jinxin Shi、Jiong Wang、Fangchen Yu、Zhijie Zhong、等
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.AI
- 主题标签：LLM、多模态、Agent、Reasoning
- 阅读价值评分：17/20

### 摘要速读

Current LLM-based research agents have advanced through agent orchestration, yet largely overlook scientific knowledge orchestration. Existing works often reduce papers to abstracts, surface mentions, and flat \texttt{cites} edges, omitting key entities, claims, evidence, mechanisms, and method lineages essential for scientific reasoning.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [EurekAgent: Agent Environment Engineering is All You Need For Autonomous Scientific Discovery](http://arxiv.org/abs/2606.13662v1)

- arXiv：[2606.13662](http://arxiv.org/abs/2606.13662v1)
- PDF：[https://arxiv.org/pdf/2606.13662v1](https://arxiv.org/pdf/2606.13662v1)
- 作者：Amy Xin、Jiening Siow、Junjie Wang、Zijun Yao、Fanjin Zhang、Jian Song、等
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.AI、cs.CL
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

LLM-based agents have shown increasing potential in automating scientific discovery. Given an optimizable metric and an execution environment, they can propose, validate, and iterate scientific solutions, and have produced results that outperform human-designed approaches.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [IterCAD: An Iterative Multimodal Agent for Visually-Grounded CAD Generation and Editing](http://arxiv.org/abs/2606.13368v1)

- arXiv：[2606.13368](http://arxiv.org/abs/2606.13368v1)
- PDF：[https://arxiv.org/pdf/2606.13368v1](https://arxiv.org/pdf/2606.13368v1)
- 作者：Tao Hu、Jiaxin Ai、Licheng Wen、Xueheng Li、Shu Zou、Siqi Li、等
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.AI、cs.CV
- 主题标签：多模态、Agent、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Computer-Aided Design is pivotal in modern manufacturing, yet existing automated methods predominantly rely on open-loop, one-shot generation, creating a mismatch with iterative real-world practices. In this paper, we present IterCAD, a unified multimodal agent framework for closed-loop, interactive CAD generation and editing.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments](http://arxiv.org/abs/2606.13681v1)

- arXiv：[2606.13681](http://arxiv.org/abs/2606.13681v1)
- PDF：[https://arxiv.org/pdf/2606.13681v1](https://arxiv.org/pdf/2606.13681v1)
- 作者：Jundong Xu、Qingchuan Li、Jiaying Wu、Yihuai Lan、Shuyue Stella Li、Huichi Zhou、等
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.CL
- 主题标签：LLM、Agent、Skill/Tool、RAG/Memory、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Large language model (LLM) agents have achieved strong performance on a wide range of benchmarks, yet most evaluations assume static environments. In contrast, real-world deployment is inherently dynamic, requiring agents to continually align their knowledge, skills, and behavior with changing environments and updated task conditions.

### 为什么值得读

大模型核心方向、Agent 与长程任务、工具使用/技能学习、RAG、记忆或长上下文、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages](http://arxiv.org/abs/2606.13572v1)

- arXiv：[2606.13572](http://arxiv.org/abs/2606.13572v1)
- PDF：[https://arxiv.org/pdf/2606.13572v1](https://arxiv.org/pdf/2606.13572v1)
- 作者：Tanmoy Kanti Halder、Akash Ghosh、Subhadip Baidya、Arijit Roy、Sriparna Saha
- 发布时间：2026-06-11，更新时间：2026-06-11
- 类别：cs.CL、cs.AI
- 主题标签：LLM、多模态、Agent、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [InterleaveThinker: Reinforcing Agentic Interleaved Generation](http://arxiv.org/abs/2606.13679v1) | 多模态, Agent, Reasoning, Safety/Eval | 17 | 2026-06-11 | Recent image generators have demonstrated impressive photorealism and instruction-following capabilities in single-image generation and editing. |
| [Agents-K1: Towards Agent-native Knowledge Orchestration](http://arxiv.org/abs/2606.13669v1) | LLM, 多模态, Agent, Reasoning | 17 | 2026-06-11 | Current LLM-based research agents have advanced through agent orchestration, yet largely overlook scientific knowledge orchestration. |
| [EurekAgent: Agent Environment Engineering is All You Need For Autonomous Scientific Discovery](http://arxiv.org/abs/2606.13662v1) | LLM, Agent, Reasoning, Safety/Eval | 17 | 2026-06-11 | LLM-based agents have shown increasing potential in automating scientific discovery. |
| [IterCAD: An Iterative Multimodal Agent for Visually-Grounded CAD Generation and Editing](http://arxiv.org/abs/2606.13368v1) | 多模态, Agent, Reasoning, Safety/Eval | 17 | 2026-06-11 | Computer-Aided Design is pivotal in modern manufacturing, yet existing automated methods predominantly rely on open-loop, one-shot generation, creating a mismatch with iterative real-world practices. |
| [EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments](http://arxiv.org/abs/2606.13681v1) | LLM, Agent, Skill/Tool, RAG/Memory, Safety/Eval | 16 | 2026-06-11 | Large language model (LLM) agents have achieved strong performance on a wide range of benchmarks, yet most evaluations assume static environments. |
| [ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages](http://arxiv.org/abs/2606.13572v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning | 16 | 2026-06-11 | Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. |
| [An LLM System for Autonomous Variational Quantum Circuit Design](http://arxiv.org/abs/2606.13380v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-11 | The design of high performing quantum circuits remains largely dependent on human expertise. |
| [SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning](http://arxiv.org/abs/2606.13673v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-11 | Spatial reasoning, the ability to determine where objects are, how they relate, and how they move in 3D, remains a fundamental challenge for vision-language models (VLMs). |
| [HyperTool: Beyond Step-Wise Tool Calls for Tool-Augmented Agents](http://arxiv.org/abs/2606.13663v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning | 15 | 2026-06-11 | Tool-augmented LLM agents commonly rely on step-wise atomic tool calls, where each invocation, observation, and value transfer is exposed in the main reasoning trace. |
| [MiniMax Sparse Attention](http://arxiv.org/abs/2606.13392v1) | LLM, 多模态, Agent, RAG/Memory, Reasoning | 15 | 2026-06-11 | Ultra-long-context capability is becoming indispensable for frontier LLMs: agentic workflows, repository-scale code reasoning, and persistent memory all require the model to jointly attend over hundreds of thousands to millions of tokens, yet the quadratic cost of softmax attention makes this untenable at deployment scale. |
| [Learning to Reason by Analogy via Retrieval-Augmented Reinforcement Fine-Tuning](http://arxiv.org/abs/2606.13680v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-11 | Retrieval-augmented generation (RAG) has become a standard mechanism for grounding language models in external knowledge, yet conventional retrieval based on lexical or semantic similarity is poorly suited for complex reasoning tasks: a semantically similar problem may demand an entirely different solution strategy, while a superficially different problem may share the same underlying reasoning pattern. |
| [Dense Supervision, Sparse Updates: On the Sparsity and Geometry of On-Policy Distillation](http://arxiv.org/abs/2606.13657v1) | LLM, 多模态 | 14 | 2026-06-11 | On-policy distillation (\textsc{OPD}) has recently become a prominent post-training recipe as it combines two desirable ingredients: on-policy student trajectories and dense teacher supervision, yet how this hybrid changes a model's parameters remains unclear. |
| [SkMTEB: Slovak Massive Text Embedding Benchmark and Model Adaptation](http://arxiv.org/abs/2606.13647v1) | RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-11 | We introduce SkMTEB, the first comprehensive MTEB-style text embedding benchmark for Slovak, a low-resource West Slavic language, comprising 31 datasets across 7 task types -- nearly 4$\times$ the depth of existing multilingual benchmark coverage for Slovak. |
| [Adaptive Turn-Taking for Real-time Multi-Party Voice Agents](http://arxiv.org/abs/2606.13544v1) | LLM, Agent, Reasoning | 14 | 2026-06-11 | Turn-taking in multi-party spoken conversations remains a fundamental challenge for voice-based agents, particularly under dynamic floor competition and varying user expectations. |
| [Reinforcement Learning for Neural Model Editing](http://arxiv.org/abs/2606.13461v1) | 多模态, Agent | 14 | 2026-06-11 | Editing pretrained neural networks requires specialized algorithms tailored to specific objectives. |
| [Who Pays the Price? Stakeholder-Centric Prompt Injection Benchmarking for Real-world Web Agents](http://arxiv.org/abs/2606.13385v1) | LLM, Agent, Safety/Eval | 14 | 2026-06-11 | Web agents driven by large language models (LLMs) are increasingly deployed in real-world environments, where they operate over untrusted web content and execute actions with direct consequences. |
| [SkillCAT: Contrastive Assessment and Topology-Aware Skill Self-Evolution for LLM Agents](http://arxiv.org/abs/2606.13317v1) | LLM, Agent, Skill/Tool, RAG/Memory, Safety/Eval | 14 | 2026-06-11 | Skill self-evolution methods for LLM agents aim to turn execution trajectories into reusable skill documents, but current pipelines typically learn from one trajectory per task, merge candidate skill patches before checking them, and load the full skill corpus before inference. |
| [Reward Modeling for Multi-Agent Orchestration](http://arxiv.org/abs/2606.13598v1) | LLM, Agent, RAG/Memory, Reasoning | 13 | 2026-06-11 | Multi-Agent Systems (MAS) built on Large Language Models (LLMs) require effective orchestration to coordinate specialized agents, yet training such orchestrators is hindered by limited supervision and high computational cost. |
| [From Passive Generation to Investigation: A Proactive Scientific Peer Review Agent](http://arxiv.org/abs/2606.13349v1) | LLM, Agent, RAG/Memory, Safety/Eval | 13 | 2026-06-11 | Large language models (LLMs) have shown promise in automating scientific peer review. |
| [Mana: Dexterous Manipulation of Articulated Tools](http://arxiv.org/abs/2606.13677v1) | Skill/Tool, Reasoning | 12 | 2026-06-11 | Articulated tool manipulation remains a major challenge in dexterous robotics due to the need to coordinate internal degrees of freedom and contact-rich interactions. |
| [Recursive Agent Harnesses](http://arxiv.org/abs/2606.13643v1) | LLM, Agent, Reasoning, Safety/Eval | 12 | 2026-06-11 | Recursive language models (RLMs) showed that recursion over model calls is an effective strategy for long-context reasoning, and production coding agents have begun to write code that spawns subagents at scale, most recently in Anthropic's dynamic workflows. |
| [One Polluted Page Is Enough: Evaluating Web Content Pollution in Generative Recommenders](http://arxiv.org/abs/2606.13610v1) | LLM, Reasoning, Safety/Eval | 12 | 2026-06-11 | Search-augmented LLMs increasingly mediate everyday consumer recommendations by retrieving live web content. |
| [AgentBeats: Agentifying Agent Assessment for Openness, Standardization, and Reproducibility](http://arxiv.org/abs/2606.13608v1) | LLM, Agent, RAG/Memory, Safety/Eval | 12 | 2026-06-11 | Agent systems are advancing quickly across domains, but their evaluation remains fragmented. |
| [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](http://arxiv.org/abs/2606.13497v1) | LLM, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-11 | This work introduces Spatial Annotations from Robot Demonstrations with Reliability Calibration (SPARC), a risk-aware framework that automatically labels robot demonstrations with structured spatial annotations and assigns each annotation a reliability score. |
| [RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue](http://arxiv.org/abs/2606.13310v1) | LLM, Agent, Safety/Eval | 12 | 2026-06-11 | The original Turing Test asks a human judge to distinguish a machine from a person through dialogue. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-12 15:05:02 CST
