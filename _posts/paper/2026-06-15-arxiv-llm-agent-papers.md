---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-15)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-15 10:30:00 +0800
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

## [ClinHallu: A Benchmark for Diagnosing Stage-Wise Hallucinations in Medical MLLM Reasoning](http://arxiv.org/abs/2606.14697v1)

- arXiv：[2606.14697](http://arxiv.org/abs/2606.14697v1)
- PDF：[https://arxiv.org/pdf/2606.14697v1](https://arxiv.org/pdf/2606.14697v1)
- 作者：Sicheng Yang、Hangjie Yuan、Wenjun Zhang、Jinwang Wang、Yichen Qian、Weihua Chen、等
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.CV、cs.AI、cs.CL
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Building trustworthy medical multimodal large language models (MLLMs) is critical for reliable clinical decision support. Existing medical hallucination benchmarks mainly focus on data collection, but often ignore where hallucinations originate within the reasoning process.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](http://arxiv.org/abs/2606.14249v1)

- arXiv：[2606.14249](http://arxiv.org/abs/2606.14249v1)
- PDF：[https://arxiv.org/pdf/2606.14249v1](https://arxiv.org/pdf/2606.14249v1)
- 作者：Tingyang Chen、Shuo Lu、Kang Zhao、Weicheng Meng、Hanlin Teng、Tianhao Li、等
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.AI
- 主题标签：Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

AI agent performance depends critically on the runtime harness, comprising the prompts, tools, memory, and control flow that mediate how a model observes, reasons, and acts. Yet today's harnesses remain largely hand-crafted and static: each new model or task still demands bespoke scaffolding, and the rich traces produced during execution are rarely distilled back into systematic improvement.

### 为什么值得读

Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [CORA: Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment](http://arxiv.org/abs/2606.14691v1)

- arXiv：[2606.14691](http://arxiv.org/abs/2606.14691v1)
- PDF：[https://arxiv.org/pdf/2606.14691v1](https://arxiv.org/pdf/2606.14691v1)
- 作者：Jiayue Cao、Zhicong Lu、Xuehan Sun、Wei Jia、Hongling Zheng、Changyuan Tian、等
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.CL
- 主题标签：LLM、多模态、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Reinforcement learning with verifiable rewards (RLVR) has successfully elicited the reasoning capabilities of large language models, motivating its extension to multimodal scenarios. Existing methods primarily focus on improving the visual coverage of reasoning traces and mitigating visual hallucinations, but underestimate the semantic inconsistency between the reasoning process and the final answer.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、训练/后训练方法、推理效率或系统优化、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [AgentSpec: Understanding Embodied Agent Scaffolds Through Controlled Composition](http://arxiv.org/abs/2606.14674v1)

- arXiv：[2606.14674](http://arxiv.org/abs/2606.14674v1)
- PDF：[https://arxiv.org/pdf/2606.14674v1](https://arxiv.org/pdf/2606.14674v1)
- 作者：Jixuan Chen、Jianzhi Shen、Haoqiang Kang、Zhi Hong、Qingyi Jiang、Soham Bose、等
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.CL
- 主题标签：LLM、Agent、RAG/Memory、Reasoning
- 阅读价值评分：15/20

### 摘要速读

LLM agents are increasingly built not as single model calls, but as scaffolded systems that combine reasoning, memory, reflection, action execution, and learning. While such scaffolds often improve performance, they are often embedded in tightly coupled pipelines, making it difficult to isolate component contributions, compare alternative designs, or understand how module interactions shape agent behavior.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime](http://arxiv.org/abs/2606.14589v1)

- arXiv：[2606.14589](http://arxiv.org/abs/2606.14589v1)
- PDF：[https://arxiv.org/pdf/2606.14589v1](https://arxiv.org/pdf/2606.14589v1)
- 作者：Wei Wu
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.SE、cs.AI、cs.DC
- 主题标签：LLM、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

LLM agent systems increasingly run as long-lived autonomous runtimes: scheduling jobs, calling tools, maintaining memory, and pushing results to humans. We present a longitudinal study of silent failures in one such system: a personal-assistant agent runtime in continuous production since March 2026, with roughly 40 scheduled jobs, 8 LLM providers, a tool-governance proxy, and a knowledge-base memory plane, defended by 4,286 unit tests and 827 governance checks.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge](http://arxiv.org/abs/2606.14470v1)

- arXiv：[2606.14470](http://arxiv.org/abs/2606.14470v1)
- PDF：[https://arxiv.org/pdf/2606.14470v1](https://arxiv.org/pdf/2606.14470v1)
- 作者：Pavan C Shekar、Abhishek H S、Aswanth Krishnan
- 发布时间：2026-06-12，更新时间：2026-06-12
- 类别：cs.AI、cs.CL、cs.LG
- 主题标签：LLM、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Large language model (LLM) reasoning is ephemeral: chains of thought vanish with the context window, pruned search branches leave no record, and memory buffers cannot be diffed, merged, or audited. Every other complex software process (code, infrastructure, data, experiments) is version-controlled; reasoning is not.

### 为什么值得读

大模型核心方向、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、评测基准或数据集、类别与 LLM/Agent 高相关、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [ClinHallu: A Benchmark for Diagnosing Stage-Wise Hallucinations in Medical MLLM Reasoning](http://arxiv.org/abs/2606.14697v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-12 | Building trustworthy medical multimodal large language models (MLLMs) is critical for reliable clinical decision support. |
| [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](http://arxiv.org/abs/2606.14249v1) | Agent, RAG/Memory, Reasoning, Safety/Eval | 16 | 2026-06-12 | AI agent performance depends critically on the runtime harness, comprising the prompts, tools, memory, and control flow that mediate how a model observes, reasons, and acts. |
| [CORA: Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment](http://arxiv.org/abs/2606.14691v1) | LLM, 多模态, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-12 | Reinforcement learning with verifiable rewards (RLVR) has successfully elicited the reasoning capabilities of large language models, motivating its extension to multimodal scenarios. |
| [AgentSpec: Understanding Embodied Agent Scaffolds Through Controlled Composition](http://arxiv.org/abs/2606.14674v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-12 | LLM agents are increasingly built not as single model calls, but as scaffolded systems that combine reasoning, memory, reflection, action execution, and learning. |
| [When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime](http://arxiv.org/abs/2606.14589v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-12 | LLM agent systems increasingly run as long-lived autonomous runtimes: scheduling jobs, calling tools, maintaining memory, and pushing results to humans. |
| [GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge](http://arxiv.org/abs/2606.14470v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 15 | 2026-06-12 | Large language model (LLM) reasoning is ephemeral: chains of thought vanish with the context window, pruned search branches leave no record, and memory buffers cannot be diffed, merged, or audited. |
| [tap: A File-Based Protocol for Heterogeneous LLM Agent Collaboration](http://arxiv.org/abs/2606.14445v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-12 | Existing multi-agent software development systems have proposed many forms of agent collaboration, including role-based collaboration and automated code review. |
| [Running the Gauntlet: Re-evaluating the Capabilities of Agents Beyond Familiar Environments](http://arxiv.org/abs/2606.14397v1) | 多模态, Agent, Reasoning, Safety/Eval | 15 | 2026-06-12 | As agentic systems continue to evolve and are widely deployed in real-world scenarios, there is a growing demand to faithfully evaluate their capabilities. |
| [IndustryBench-MIPU: Benchmarking Multi-Image Attribute Value Extraction for Industrial Products](http://arxiv.org/abs/2606.14383v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-12 | Industrial products such as valves and circuit breakers are defined by dense technical specifications that govern procurement, compatibility, and safety across supply chains. |
| [SIMMER: Benchmarking Latent Failures in LLM Executable Planning with a World Model](http://arxiv.org/abs/2606.14574v1) | LLM, Agent, RAG/Memory, Reasoning, Safety/Eval | 14 | 2026-06-12 | Large language models (LLMs) are increasingly deployed as planners for autonomous agents in household environments. |
| [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](http://arxiv.org/abs/2606.14517v1) | LLM, Agent, Reasoning, Safety/Eval | 14 | 2026-06-12 | LLM-based guardrails have emerged as a highly effective defense against prompt injection and jailbreak attacks in autonomous agents. |
| [No Accidental Software Agent First Canonical Code for Human Code Entropy Reduction and 30 to 500 times Lower Frontier Model Requirements](http://arxiv.org/abs/2606.14357v1) | Agent, RAG/Memory, Reasoning | 14 | 2026-06-12 | Frontier coding models may spend substantial capacity learning not only program behavior, but also accidental entropy in human repositories. |
| [Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows](http://arxiv.org/abs/2606.14672v1) | LLM, Agent, Reasoning | 13 | 2026-06-12 | Large language models increasingly serve as execution engines for agentic systems, yet they still consume context through a sequential text interface. |
| [BayLing-Duplex: Native Full-Duplex Speech Dialogue with a Single Autoregressive LLM](http://arxiv.org/abs/2606.14528v1) | LLM | 13 | 2026-06-12 | Real-time, full-duplex speech interaction is a key feature of next-generation spoken chatbots, allowing the model to listen and speak at the same time and to handle natural phenomena such as overlap, hesitation, and barge-in. |
| [From Chatbot to Digital Colleague: The Paradigm Shift Toward Persistent Autonomous AI](http://arxiv.org/abs/2606.14502v1) | LLM, Agent, Skill/Tool, RAG/Memory, Reasoning, Safety/Eval | 13 | 2026-06-12 | Large Language Models (LLMs) are undergoing a fundamental transformation from conversational generators into integrated AI systems capable of reasoning, action, memory, and self-improvement. |
| [CausalMotion: Structured Physical Reasoning as Keyframe and Trajectory Guidance for Training-Free Video Generation](http://arxiv.org/abs/2606.14317v1) | LLM, 多模态, RAG/Memory, Reasoning | 13 | 2026-06-12 | Recent advances in diffusion-based video generation have significantly improved visual quality and short-term temporal coherence. |
| [What Drives Test-Time Adaptation for CLIP? A Controlled Empirical Study from an Update Perspective](http://arxiv.org/abs/2606.14299v1) | LLM, 多模态, Safety/Eval | 13 | 2026-06-12 | Vision-Language Models (VLMs) such as CLIP have become a standard backbone for open-vocabulary recognition, yet their zero-shot predictions remain vulnerable to distribution shifts encountered at deployment. |
| [OmniVideo-100K: A Dataset for Audio-Visual Reasoning through Structured Scripts and Evidence Chains](http://arxiv.org/abs/2606.14702v1) | 多模态, RAG/Memory, Reasoning, Safety/Eval | 12 | 2026-06-12 | Current automated pipelines for audio-visual Question Answering (QA) generally adopt a ``video-caption-QA'' paradigm. |
| [Instruct-Particulate: Scaling Feed-Forward 3D Object Articulation with Kinematic Control](http://arxiv.org/abs/2606.14699v1) | LLM, 多模态 | 12 | 2026-06-12 | Reconstructing articulated 3D objects is important for animation, gaming, and robotic simulations. |
| [LoSoNA: A Benchmark for Local Social Norm Adaptation in Group Conversations](http://arxiv.org/abs/2606.14600v1) | LLM, Agent, Safety/Eval | 12 | 2026-06-12 | Online group chats are social spaces with local conversational norms that are rarely stated explicitly. |
| [StreamMemBench: Streaming Evaluation of Agent Memory for Future-Oriented Assistance](http://arxiv.org/abs/2606.14571v1) | Agent, RAG/Memory, Safety/Eval | 12 | 2026-06-12 | A central role of personal-agent memory is to turn stored information and prior interactions into future-oriented assistance. |
| [Verifiable User Simulation for Search and Recommendation Systems](http://arxiv.org/abs/2606.14474v1) | LLM, Agent, Safety/Eval | 12 | 2026-06-12 | Large-language-model (LLM) based user simulation is increasingly adopted for evaluating search engines, recommender systems, and retrieval-augmented generation pipelines, yet most simulators remain opaque: it is difficult to determine why a simulated user made a particular choice or whether that choice is consistent with the intended user profile. |
| [Retrospective Progress-Aware Self-Refinement for LLM Agent Training](http://arxiv.org/abs/2606.14302v1) | LLM, Agent | 12 | 2026-06-12 | LLM-based agents trained with reinforcement learning optimize step-wise action prediction but lack metacognitive awareness of task progress, inducing a gap that hinders long-horizon scaling. |
| [AgentCyberRange: Benchmarking Frontier AI Systems in Realistic Cyber Ranges](http://arxiv.org/abs/2606.14295v1) | Agent, Skill/Tool, Reasoning, Safety/Eval | 12 | 2026-06-12 | Frontier AI systems are increasingly capable of cybersecurity tasks, including codebase inspection, vulnerability detection, and exploitation. |
| [Gaze Heads: How VLMs Look at What They Describe](http://arxiv.org/abs/2606.14703v1) | LLM, 多模态, Reasoning | 11 | 2026-06-12 | How a vision-language model internally solves the task of describing an image is far from obvious. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-15 16:36:10 CST
