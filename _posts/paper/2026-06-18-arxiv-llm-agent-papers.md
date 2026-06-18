---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent (2026-06-18)"
subtitle: "自动筛选值得精读的新论文"
date: 2026-06-18 10:30:00 +0800
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

## [Native Active Perception as Reasoning for Omni-Modal Understanding](http://arxiv.org/abs/2606.19341v1)

- arXiv：[2606.19341](http://arxiv.org/abs/2606.19341v1)
- PDF：[https://arxiv.org/pdf/2606.19341v1](https://arxiv.org/pdf/2606.19341v1)
- 作者：Zhenghao Xing、Ruiyang Xu、Yuxuan Wang、Jinzheng He、Ziyang Ma、Qize Yang、等
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.CV、cs.CL、cs.SD
- 主题标签：多模态、Agent、RAG/Memory、Reasoning、Safety/Eval
- 阅读价值评分：19/20

### 摘要速读

Passive models for long video understanding typically rely on a "watch-it-all" paradigm, processing frames uniformly regardless of query difficulty, causing computational cost to grow with video duration. Although interactive frameworks have emerged, they often rely on global pre-scanning, and their context cost still scales with video length.

### 为什么值得读

多模态/视觉语言模型、Agent 与长程任务、RAG、记忆或长上下文、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: From Evaluation to Diagnosis](http://arxiv.org/abs/2606.19053v1)

- arXiv：[2606.19053](http://arxiv.org/abs/2606.19053v1)
- PDF：[https://arxiv.org/pdf/2606.19053v1](https://arxiv.org/pdf/2606.19053v1)
- 作者：Hong-Tao Yu、Chen-Wei Xie、Yuxin Peng、Serge Belongie、Xiu-Shen Wei
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.CV
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：17/20

### 摘要速读

Recent advancements in Large Vision-Language Models (LVLMs) have demonstrated remarkable multimodal perception and reasoning capabilities. While numerous benchmarks have evaluated LVLMs from holistic or task-specific perspectives, their capabilities on fine-grained image tasks-fundamental to computer vision-remain insufficiently understood.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、安全、对齐或鲁棒性、视觉/多模态类别匹配、方法贡献明确、可能有代码或数据可复现。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [STARE: Surprisal-Guided Token-Level Advantage Reweighting for Policy Entropy Stability](http://arxiv.org/abs/2606.19236v1)

- arXiv：[2606.19236](http://arxiv.org/abs/2606.19236v1)
- PDF：[https://arxiv.org/pdf/2606.19236v1](https://arxiv.org/pdf/2606.19236v1)
- 作者：Haipeng Luo、Qingfeng Sun、Songli Wu、Can Xu、Wenfeng Deng、Han Hu、等
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.LG、cs.AI、cs.CL
- 主题标签：LLM、Skill/Tool、RAG/Memory、Reasoning
- 阅读价值评分：16/20

### 摘要速读

Reinforcement Learning with Verifiable Rewards algorithms like GRPO have emerged as the dominant post-training paradigm for complex reasoning in LLMs, yet commonly suffer from policy entropy collapse during training. We conduct a first-order gradient analysis of token-level entropy dynamics under GRPO and identify a token-level credit assignment mismatch: the per-token entropy variation decomposes into the product of the trajectory-level advantage and an entropy sensitivity function over the next-token distribut...

### 为什么值得读

大模型核心方向、工具使用/技能学习、推理、代码或复杂任务、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、可能有代码或数据可复现、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [ThinkDeception: A Progressive Reinforcement Learning Framework for Interpretable Multimodal Deception Detection](http://arxiv.org/abs/2606.18988v1)

- arXiv：[2606.18988](http://arxiv.org/abs/2606.18988v1)
- PDF：[https://arxiv.org/pdf/2606.18988v1](https://arxiv.org/pdf/2606.18988v1)
- 作者：Jinhao Song、Shan Liang、Yiqun Yue、Zhuhuayang Zhang、Tianqi Gao
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.AI
- 主题标签：LLM、多模态、Reasoning、Safety/Eval
- 阅读价值评分：16/20

### 摘要速读

Multimodal deception detection is critical for identifying fraudulent intentions, yet existing approaches predominantly rely on end to end black--box paradigms. These methods suffer from a severe lack of interpretability failing to provide transparent reasoning trajectories and struggling to explicitly capture the subtle, cross modal inconsistencies inherent in deceptive behaviors.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、推理、代码或复杂任务、评测基准或数据集、训练/后训练方法、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？

## [Beyond the Current Observation: Evaluating Multimodal Large Language Models in Controllable Non-Markov Games](http://arxiv.org/abs/2606.19338v1)

- arXiv：[2606.19338](http://arxiv.org/abs/2606.19338v1)
- PDF：[https://arxiv.org/pdf/2606.19338v1](https://arxiv.org/pdf/2606.19338v1)
- 作者：Shengyuan Ding、Xilin Wei、Xinyu Fang、Haodong Duan、Dahua Lin、Jiaqi Wang、等
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.CV
- 主题标签：LLM、多模态、Agent、Skill/Tool、RAG/Memory、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Deploying multimodal foundation models as closed-loop policies increasingly requires conditioning actions on observations that are no longer visible. However, existing benchmarks either expose the full state, conflate hidden-state reconstruction with other agent skills, or test recall only after an episode has ended.

### 为什么值得读

大模型核心方向、多模态/视觉语言模型、Agent 与长程任务、工具使用/技能学习、RAG、记忆或长上下文、评测基准或数据集、训练/后训练方法、视觉/多模态类别匹配、方法贡献明确。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？

## [Enhancing Decision-Making with Large Language Models through Multi-Agent Fictitious Play](http://arxiv.org/abs/2606.19308v1)

- arXiv：[2606.19308](http://arxiv.org/abs/2606.19308v1)
- PDF：[https://arxiv.org/pdf/2606.19308v1](https://arxiv.org/pdf/2606.19308v1)
- 作者：Leyang Shen、Yang Zhang、Xiaoyan Zhao、Chun Kai Ling、Tat-Seng Chua
- 发布时间：2026-06-17，更新时间：2026-06-17
- 类别：cs.CL、cs.MA
- 主题标签：LLM、Agent、Reasoning、Safety/Eval
- 阅读价值评分：15/20

### 摘要速读

Large language model (LLM)-based multi-agent systems (MAS) have demonstrated great potential in solving tasks with execution complexity, by distributing subtasks across cooperative agents. However, this divide-and-conquer paradigm falls short on decision-making tasks that are also prevalent in the real world.

### 为什么值得读

大模型核心方向、Agent 与长程任务、推理、代码或复杂任务、安全、对齐或鲁棒性、类别与 LLM/Agent 高相关、方法贡献明确、摘要中有实验或对比信号。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。

### 精读时重点追问

- 论文解决的是新问题，还是对已有问题换了一个实验设置？
- 核心结论是否依赖特定模型、数据集或 prompt 模板？
- 如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？


# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
| [Native Active Perception as Reasoning for Omni-Modal Understanding](http://arxiv.org/abs/2606.19341v1) | 多模态, Agent, RAG/Memory, Reasoning, Safety/Eval | 19 | 2026-06-17 | Passive models for long video understanding typically rely on a "watch-it-all" paradigm, processing frames uniformly regardless of query difficulty, causing computational cost to grow with video duration. |
| [Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: From Evaluation to Diagnosis](http://arxiv.org/abs/2606.19053v1) | LLM, 多模态, Reasoning, Safety/Eval | 17 | 2026-06-17 | Recent advancements in Large Vision-Language Models (LVLMs) have demonstrated remarkable multimodal perception and reasoning capabilities. |
| [STARE: Surprisal-Guided Token-Level Advantage Reweighting for Policy Entropy Stability](http://arxiv.org/abs/2606.19236v1) | LLM, Skill/Tool, RAG/Memory, Reasoning | 16 | 2026-06-17 | Reinforcement Learning with Verifiable Rewards algorithms like GRPO have emerged as the dominant post-training paradigm for complex reasoning in LLMs, yet commonly suffer from policy entropy collapse during training. |
| [ThinkDeception: A Progressive Reinforcement Learning Framework for Interpretable Multimodal Deception Detection](http://arxiv.org/abs/2606.18988v1) | LLM, 多模态, Reasoning, Safety/Eval | 16 | 2026-06-17 | Multimodal deception detection is critical for identifying fraudulent intentions, yet existing approaches predominantly rely on end to end black--box paradigms. |
| [Beyond the Current Observation: Evaluating Multimodal Large Language Models in Controllable Non-Markov Games](http://arxiv.org/abs/2606.19338v1) | LLM, 多模态, Agent, Skill/Tool, RAG/Memory, Safety/Eval | 15 | 2026-06-17 | Deploying multimodal foundation models as closed-loop policies increasingly requires conditioning actions on observations that are no longer visible. |
| [Enhancing Decision-Making with Large Language Models through Multi-Agent Fictitious Play](http://arxiv.org/abs/2606.19308v1) | LLM, Agent, Reasoning, Safety/Eval | 15 | 2026-06-17 | Large language model (LLM)-based multi-agent systems (MAS) have demonstrated great potential in solving tasks with execution complexity, by distributing subtasks across cooperative agents. |
| [A Multi-Domain Benchmark for Detecting AI-Generated Text-Rich Images from GPT-Image-2](http://arxiv.org/abs/2606.19259v1) | LLM, 多模态, RAG/Memory, Safety/Eval | 15 | 2026-06-17 | Text-rich images often contain privacy-sensitive, transactional, or decision-relevant information. |
| [AMALIA-VL: A Native European Portuguese Open-Source Vision and Language Model](http://arxiv.org/abs/2606.19100v1) | LLM, 多模态, Reasoning, Safety/Eval | 15 | 2026-06-17 | Large Vision and Language Models (LVLMs) have advanced rapidly, yet European Portuguese (pt-PT) remains systematically underserved by existing open-source multimodal models, which either conflate it with Brazilian Portuguese or severely under-represent it in their training data mixes. |
| [Taming I2V models for Image HOI Editing: A Cognitive Benchmark and Agentic Self-Correcting Framework](http://arxiv.org/abs/2606.19073v1) | 多模态, Agent, Reasoning, Safety/Eval | 15 | 2026-06-17 | Current image editing methods excel at static attributes but fail at complex Human-Object Interactions (HOI), a critical challenge unaddressed by existing benchmarks that conflate HOI with static attributes, relying on global metrics incapable of simultaneously assessing dynamic interaction validity and entangled human-object pair preservation. |
| [RODS: Reward-Driven Online Data Synthesis for Multi-Turn Tool-Use Agents](http://arxiv.org/abs/2606.19047v1) | Agent, Skill/Tool | 15 | 2026-06-17 | Multi-turn tool-use RL is bottlenecked by the rapid depletion of informative samples in static datasets. |
| [EfficientRollout: System-Aware Self-Speculative Decoding for RL Rollouts](http://arxiv.org/abs/2606.18967v1) | LLM, Agent, RAG/Memory, Reasoning | 15 | 2026-06-17 | Reinforcement learning (RL) has become a representative post-training paradigm for LLMs, enabling strong reasoning and agentic capabilities. |
| [Does VLA Even Know the Basics? Measuring Commonsense and World Knowledge Retention in Vision-Language-Action Models](http://arxiv.org/abs/2606.19297v1) | 多模态, Agent, Safety/Eval | 14 | 2026-06-17 | Embodied Vision-Language-Action (VLA) models are typically obtained by fine-tuning powerful pretrained VLMs on robotics data, yet it is unclear how much commonsense and factual knowledge they retain after adaptation. |
| [Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance](http://arxiv.org/abs/2606.19195v1) | LLM, 多模态, Safety/Eval | 14 | 2026-06-17 | While 10B-level industrial foundation models have pushed the boundaries of image inpainting, their prohibitive computational costs severely hinder practical deployment. |
| [Beyond Safe Data: Pretraining-Stage Alignment with Regular Safety Reflection](http://arxiv.org/abs/2606.19168v1) | LLM, Reasoning, Safety/Eval | 14 | 2026-06-17 | To achieve deeper safety alignment for large language models (LLMs), recent efforts have studied how to push safety interventions earlier into the pretraining stage, primarily by filtering unsafe data or rewriting it into safer forms. |
| [OpenAnt: LLM-Powered Vulnerability Discovery Through Code Decomposition, Adversarial Verification, and Dynamic Testing](http://arxiv.org/abs/2606.19149v1) | LLM, Reasoning, Safety/Eval | 14 | 2026-06-17 | Automated vulnerability discovery in large codebases remains challenging: traditional static analysis produces high false-positive rates, while dynamic approaches such as fuzzing require substantial infrastructure and often target narrow classes of bugs. |
| [A Technical Taxonomy of LLM Agent Communication Protocols](http://arxiv.org/abs/2606.19135v1) | LLM, Agent, RAG/Memory | 14 | 2026-06-17 | As large language models (LLMs) advance and multi-agent systems aim to overcome the limits of standalone agents, robust communication protocols are becoming essential infrastructure for distributed agent networks. |
| [Seeing Before Reasoning: Decoupling Perception and Reasoning for Shortcut-Resilient Multimodal On-Policy Self-Distillation](http://arxiv.org/abs/2606.19120v1) | LLM, 多模态, Reasoning, Safety/Eval | 14 | 2026-06-17 | On-policy self-distillation (OPSD) trains a model on its own rollouts and uses a frozen copy to provide dense token-level targets conditioned on a reference target. |
| [DREAM: Extending Vision-Language Models with Dual-Objective Encoding for Cross-Modal Retrieval](http://arxiv.org/abs/2606.19062v1) | LLM, 多模态, Reasoning, Safety/Eval | 14 | 2026-06-17 | In today's media-driven world, the exponential growth of video content across domains such as surveillance, education, and entertainment has made retrieving semantically relevant videos via natural language queries increasingly critical. |
| [TRAP: Benchmark for Task-completion and Resistance to Active Privacy-extraction](http://arxiv.org/abs/2606.18996v1) | Agent, Safety/Eval | 14 | 2026-06-17 | Agents are increasingly deployed in document-intensive workflows where sensitive private information is not an edge case but a routine input, e.g., an agent booking a flight needs passport numbers. |
| [CAPRA: Scaling Feedback on Software Architecture Deliverables with a Multi-Agent LLM System](http://arxiv.org/abs/2606.18976v1) | LLM, 多模态, Agent, Reasoning, Safety/Eval | 14 | 2026-06-17 | Automated assessment in software engineering education has advanced significantly for code grading and essay scoring. |
| [Learning User Simulators with Turing Rewards](http://arxiv.org/abs/2606.19336v1) | LLM, Agent, Safety/Eval | 13 | 2026-06-17 | Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. |
| [Optimal scenario design for climate emulation](http://arxiv.org/abs/2606.19302v1) | Agent, Skill/Tool | 13 | 2026-06-17 | As deep learning for physical systems continues to grow in popularity, efforts to improve generalizability have primarily focused on designing architectures that embed physical constraints. |
| [A Unified Framework for Efficient Remote Sensing Visual Question Answering: Adapting Dual, Hybrid, and Encoder-Decoder Architectures](http://arxiv.org/abs/2606.19277v1) | LLM, 多模态, Reasoning | 13 | 2026-06-17 | Visual Question Answering (VQA) in the Remote Sensing (RS) domain presents unique challenges due to the high resolution, multi scale object distribution, and semantic complexity of aerial imagery. |
| [TxBench-PP: Analyzing AI Agent Performance on Small-Molecule Preclinical Pharmacology](http://arxiv.org/abs/2606.19245v1) | Agent, Reasoning, Safety/Eval | 13 | 2026-06-17 | Artificial intelligence (AI) agents promise to accelerate drug discovery by compressing interpretation and decision-making loops, but practical deployment requires trusted evaluation on realistic program decisions. |
| [FoMoE: Breaking the Full-Replica Barrier with a Federation of MoEs](http://arxiv.org/abs/2606.19025v1) | LLM, RAG/Memory | 13 | 2026-06-17 | Pre-training Large Language Models (LLMs) typically demands large-scale infrastructure with tightly coupled hardware accelerators. |

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

生成时间：2026-06-18 15:16:05 CST
