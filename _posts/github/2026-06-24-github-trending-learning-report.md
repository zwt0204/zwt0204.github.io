---
layout: post
title: "GitHub Trending 精读：mukul975/Anthropic-Cybersecurity-Skills (2026-06-24)"
subtitle: "每天只选一个开源项目深读"
date: 2026-06-24
author: "zwt"
header-img: "img/LLMs.png"
catalog: true
tags:
  - github
  - trending
  - open-source
  - learning
categories: [github]
---

# GitHub Trending 精读 2026-06-24

数据来源：[GitHub Trending Daily](https://github.com/trending?since=daily)。本篇自动抓取当日 Trending 仓库，但正文只选一个项目深读；其它项目只保留在候选表里，避免把日报写成一组浅摘要。

## 筛选逻辑

我会优先关注四类信号：

1. 是否代表一个正在变热的技术方向，例如 AI agent、LLM infra、数据库、编译器、云原生或安全工具。
2. 是否有明确的工程入口，适合顺着 README、示例、CLI/API 和测试一路读到核心实现。
3. 是否有足够的社区反馈，包括 star、fork、issue、release 或 topic。
4. 是否能沉淀可迁移经验，例如架构边界、扩展机制、错误处理、性能优化或文档组织。

## 今日重点项目

## 今日只读这一个：[mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)

- 语言：Python
- Stars：20,162，Forks：2,339，今日新增：1,041
- Topics：ai-agents、claude-code、cloud-security、cybersecurity、devsecops、ethical-hacking
- 官网/演示：[https://mahipal.engineer/Anthropic-Cybersecurity-Skills/](https://mahipal.engineer/Anthropic-Cybersecurity-Skills/)
- 学习价值评分：20/20
- 项目类型：AI/Agent 工程项目

**项目简介**：817 structured cybersecurity skills for AI agents · Mapped to 6 frameworks: MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, D3FEND, NIST AI RMF & MITRE F3 (Fight Fraud) · agentskills.io standard · Works with Claude Code, GitHub Copilot, Codex CLI, Cursor, Gemini CLI & 20+ platforms · 29 security domains · Apache 2.0

### 为什么今天选它，而不是泛读一堆

AI / LLM、大模型工程、智能体实践、安全工程、命令行工具设计、今日关注度极高、社区验证充分、主题标签清晰。今天的目标不是把 Trending 里所有项目都扫一遍，而是选一个最值得投入 30-60 分钟的样本。这个项目的价值不只在功能本身，更在于它能暴露一组可迁移的工程问题：用户入口如何定义、核心抽象是否稳定、外部依赖如何隔离、失败路径是否可观测。

### 这次精读要回答的核心问题

它是否把“模型调用”包装成了可靠的软件系统：任务状态如何保存，工具权限如何收口，失败后如何重试或回滚，日志是否足够复盘一次 agent 行为。

如果读完只能留下一个判断，就应该是：这个项目到底靠什么建立护城河，是增长热度、工程设计、生态位置，还是某个可复用的技术抽象。

### 建议顺着这条链路读

建议从用户入口读到 agent loop：先找 CLI/Web/API 入口，再追踪 request 如何变成 plan、tool call、observation、memory/context update，最后看结果如何返回给用户。

### README 和代码结构线索

- README 结构：Anthropic Cybersecurity Skills / The largest open-source cybersecurity skills library for AI agents / Give any AI agent the security skills of a senior analyst / Six frameworks, one skill library / 🆕 MITRE Fight Fraud Framework (F3) — 94 fraud-relevant skills / MITRE ATT&CK v19.1 — 754/754 skills mapped
- 开篇信息：> ⚠️ **Community Project** — This is an independent, community-created project. Not affiliated with Anthropic PBC. A junior analyst knows which Volatility3 plugin to run on a suspicious memory dump, which Sigma rules catch Kerberoasting, and how to scope a cloud breach across three providers. **Your AI agent doesn't — unless you give it these skills.** This repo contains **817 structured cybersecurity skills** spanning **29 security domains**, each following the [agentskills.io](https://agentskills.io) open standar

值得优先打开的文件或目录：

- `README.md`
- `mappings/README.md`
- `mappings/mitre-attack/README.md`
- `mappings/nist-csf/README.md`
- `mappings/owasp/README.md`
- `tools/README.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `skills/abusing-dpapi-for-credential-access/references/api-reference.md`
- `skills/abusing-dpapi-for-credential-access/scripts/agent.py`
- `skills/abusing-shadow-credentials-for-privesc/references/api-reference.md`
- `skills/abusing-shadow-credentials-for-privesc/scripts/agent.py`
- `skills/acquiring-disk-image-with-dd-and-dcfldd/references/api-reference.md`

具体可以按这个顺序推进：

1. 入口层：看它把 CLI、Web、SDK 或配置文件暴露成怎样的用户接口。
2. 核心层：找最稳定的领域模型、调度逻辑、状态管理或数据结构。
3. 边界层：关注外部服务、文件系统、网络请求、模型调用或数据库访问如何被隔离。
4. Agent/LLM 链路：重点看工具调用、上下文管理、权限控制、失败重试和可观测日志。

### 读代码时要特别检查的地方

1. 先读 README，确认项目解决的真实问题和目标用户。
2. 找最小可运行例子，顺着入口追到核心实现，不要停在安装命令。
3. 画出核心对象之间的关系：谁负责状态，谁负责 IO，谁负责策略，谁负责错误处理。
4. 对照测试、Issue、Release，看维护者真正花时间处理的是功能扩张、性能、兼容性还是稳定性。
5. 最后回看配置、日志、扩展点和失败回退，这些地方最能反映项目是否可长期维护。

### 风险与局限

重点警惕三类风险：工具调用边界不清导致越权，长上下文堆叠导致状态漂移，以及错误恢复只靠 prompt 而没有工程级保护。

Trending 项目还要额外注意热度偏差：短期 star 增长只能说明被看见，不等于架构成熟。精读时不要只看 README 的宣传语，要至少追一条真实执行路径。

### 可以带走的工程经验

真正可复用的经验通常在 provider 抽象、tool registry、权限模型、执行日志、配置加载和测试夹具里，而不是某个具体 prompt。

### 其它候选为什么先不展开

- [bytedance/deer-flow](https://github.com/bytedance/deer-flow)：评分 20/20，An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours.
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)：评分 19/20，The agent that grows with you
- [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)：评分 18/20，World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.
- [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template)：评分 18/20，Clone any website with one command using AI coding agents


## 全量候选列表

| 项目 | 语言 | Stars | 今日新增 | 简介 |
| --- | --- | ---: | ---: | --- |
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | Python | 17,145 | 3,592 | World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio. |
| [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) | Python | 47,768 | 1,119 | LLM 驱动的多市场股票智能分析系统：多源行情、实时新闻、决策看板与自动推送，支持零成本定时运行。  LLM-powered multi-market stock analysis system with multi-source market data, real-time news, decision dashboard, automated notifications, and cost-free scheduled runs. |
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | Python | 20,162 | 1,041 | 817 structured cybersecurity skills for AI agents · Mapped to 6 frameworks: MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, D3FEND, NIST AI RMF & MITRE F3 (Fight Fraud) · agentskills.io standard · Works with Claude Code, GitHub Copilot, Codex CLI, Cursor, Gemini CLI & 20+ platforms · 29 security domains · Apache 2.0 |
| [garrytan/gstack](https://github.com/garrytan/gstack) | TypeScript | 114,526 | 1,011 | Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | Python | 74,212 | 739 | An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours. |
| [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | TypeScript | 59,365 | 294 | Real-time global intelligence dashboard. AI-powered news aggregation, geopolitical monitoring, and infrastructure tracking in a unified situational awareness interface |
| [palmier-io/palmier-pro](https://github.com/palmier-io/palmier-pro) | Swift | 8,645 | 1,630 | macOS video editor built for AI |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Python | 30,987 | 77 | Official, Anthropic-managed directory of high quality Claude Code Plugins. |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | HTML | 59,841 | 344 | from vibe coding to agentic engineering - practice makes claude perfect |
| [revfactory/harness](https://github.com/revfactory/harness) | HTML | 7,548 | 128 | A meta-skill that designs domain-specific agent teams, defines specialized agents, and generates the skills they use. |
| [jamiepine/voicebox](https://github.com/jamiepine/voicebox) | TypeScript | 33,512 | 1,045 | The open-source AI voice studio. Clone, dictate, create. |
| [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | TypeScript | 18,822 | 826 | Clone any website with one command using AI coding agents |
| [byoungd/English-level-up-tips](https://github.com/byoungd/English-level-up-tips) | - | 54,648 | 125 | An advanced guide to learn English which might benefit you a lot 🎉 . 人生进阶指南 离谱的人生 离谱的英语学习指南/英语学习教程/英语学习/学英语 |
| [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | C | 13,591 | 1,300 | High-performance code intelligence MCP server. Indexes codebases into a persistent knowledge graph — average repo in milliseconds. 158 languages, sub-ms queries, 99% fewer tokens. Single static binary, zero dependencies. |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Python | 201,406 | 936 | The agent that grows with you |

---

生成时间：2026-06-24 17:01:34 CST
