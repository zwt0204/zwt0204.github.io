---
layout: post
title: "GitHub Trending 精读：asgeirtj/system_prompts_leaks (2026-07-10)"
subtitle: "单个开源项目深度拆解"
date: 2026-07-10
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

# GitHub Trending 精读 2026-07-10

数据来源：[GitHub Trending Daily](https://github.com/trending?since=daily)。本篇围绕一个开源项目做介绍、结构线索梳理和源码阅读拆解。

## 分析目标

这篇文章关注四类问题：

1. 项目试图解决什么具体问题。
2. README 和目录结构透露了怎样的实现边界。
3. 源码阅读应该从哪条主链路进入。
4. 哪些工程经验可以迁移到自己的项目里。

## 项目拆解

## [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks)

- 语言：JavaScript
- Stars：55,320，Forks：9,040，今日新增：1,125
- Topics：ai、ai-agents、anthropic、awesome、chatbot、chatgpt
- 项目类型：AI/Agent 工程项目

**项目简介**：Extracted system prompts from Anthropic - Claude Fable 5, Opus 4.8, Claude Code, Claude Design. OpenAI - ChatGPT 5.5 Thinking, GPT 5.5 Instant, Codex. Google - Gemini 3.5 Flash, 3.1 Pro, Antigravity. xAI - Grok, Cursor, Copilot, VS Code, Perplexity, and more. Updated regularly.

### 项目定位

从仓库描述、主题标签和语言栈看，这是一个 AI/Agent 工程项目。拆解它时，重点放在它如何定义用户入口、组织核心抽象、隔离外部依赖，以及是否具备可复用的工程边界。

### 核心问题

它是否把“模型调用”包装成了可靠的软件系统：任务状态如何保存，工具权限如何收口，失败后如何重试或回滚，日志是否足够复盘一次 agent 行为。

如果读完只能留下一个判断，就应该是：这个项目到底靠什么建立护城河，是工程设计、生态位置、领域知识组织，还是某个可复用的技术抽象。

### 一张图看架构

![asgeirtj/system_prompts_leaks 架构拆解图](/img/daily-reports/2026-07-10-github-asgeirtj-system-prompts-leaks-architecture.svg)

这张图的读法是从左到右追输入、加工、执行和反馈：每一层都要问清楚“它吃什么、产出什么、失败时谁兜底”。只有这条链路清楚，后面的源码阅读才不会停留在目录浏览。

### 架构拆分

1. **用户入口层**：先确认项目暴露的是 CLI、Web、SDK、插件还是配置文件。入口决定用户目标如何进入系统。
2. **任务编排层**：看任务如何被拆成 plan、tool call、observation、state update，以及失败后如何回到上一层。
3. **工具注册层**：关注工具 schema、权限、参数校验、超时、重试和日志。agent 项目的稳定性通常卡在这里。
4. **上下文/记忆层**：看 prompt、短期状态、长期记忆、检索结果如何合并，以及是否有预算控制。
5. **模型适配层**：看不同模型 provider 是否被隔离，错误码、速率限制、流式输出和成本统计是否有统一封装。
6. **观测与测试层**：重点看 trace、事件日志、回放、fixtures 和端到端测试，否则很难复盘长任务失败。

### 关键细节拆解

- **状态对象**：确认任务状态是否有显式结构，而不是散落在 prompt 字符串里。
- **工具 schema**：看工具参数是否强类型、是否有权限描述、是否能表达危险操作。
- **失败恢复**：重点找 timeout、rate limit、tool error、模型拒答、上下文过长时的处理。
- **可观测性**：长任务必须能回放每一步输入、输出、工具结果和中间状态。
- **扩展点**：判断新增工具、模型 provider、memory backend 是否需要改核心代码。

### 代码调用链路

![asgeirtj/system_prompts_leaks 代码调用链图](/img/daily-reports/2026-07-10-github-asgeirtj-system-prompts-leaks-call-chain.svg)

1. **入口函数**：找到 CLI/Web/API 如何把用户输入变成任务对象。
2. **任务编排**：追踪任务对象如何进入 planner 或 executor。
3. **工具调用**：看 tool schema、权限校验和参数序列化。
4. **结果回流**：看 observation 如何更新上下文、记忆或状态机。
5. **错误处理**：找 timeout、rate limit、tool error 的分支。
6. **日志与回放**：确认能否复盘每一步模型输入、工具输出和最终决策。

### 建议顺着这条链路读

建议从用户入口读到 agent loop：先找 CLI/Web/API 入口，再追踪 request 如何变成 plan、tool call、observation、memory/context update，最后看结果如何返回给用户。

### README 和代码结构线索

- README 结构：System Prompts Leaks / Recently Updated / Anthropic — Claude / OpenAI — ChatGPT / Google — Gemini / xAI — Grok
- 开篇信息：> **As seen in The Washington Post:** [See the hidden rules behind AI. Then use them to rewrite this article.](https://wapo.st/49t4gSb) (May 11, 2026) The purpose of this repo is to document the System Prompt instructions for all the AI chatbots out there - Claude, ChatGPT, Gemini etc. > 🆕 **[Diff: Claude Opus 4.8 → Claude Fable 5](https://www.diffchecker.com/QJn9jFNk/)** — see exactly what changed in the claude.ai system prompt for Anthropic's newest model

值得优先打开的文件或目录：

- `Anthropic/Claude Code/bundled-skills/code-review/README.md`
- `Anthropic/Official/README.md`
- `OpenAI/API/README.md`
- `README.md`
- `Anthropic/Claude Code/bundled-skills/claude-api.md`
- `Anthropic/Claude Code/bundled-skills/code-review/report-findings-tool.md`
- `Anthropic/Claude Code/bundled-skills/run-skill-generator/examples/cli.md`
- `Anthropic/Claude Code/bundled-skills/run-skill-generator/examples/server.md`
- `Anthropic/Claude Code/bundled-skills/update-config.md`
- `Anthropic/Claude Code/deferred-tools.md`
- `Anthropic/Claude Code/glob-tool.md`
- `Anthropic/Claude Code/grep-tool.md`

### 关键文件怎么读

| 文件/目录 | 阅读重点 |
| --- | --- |
| `Anthropic/Claude Code/bundled-skills/code-review/README.md` | 确认项目承诺、安装方式、核心概念和使用边界。 |
| `Anthropic/Official/README.md` | 确认项目承诺、安装方式、核心概念和使用边界。 |
| `OpenAI/API/README.md` | 确认项目承诺、安装方式、核心概念和使用边界。 |
| `README.md` | 确认项目承诺、安装方式、核心概念和使用边界。 |
| `Anthropic/Claude Code/bundled-skills/claude-api.md` | 用于定位项目的核心边界和上下游依赖。 |
| `Anthropic/Claude Code/bundled-skills/code-review/report-findings-tool.md` | 看工具注册、权限、参数 schema、超时和失败回退。 |
| `Anthropic/Claude Code/bundled-skills/run-skill-generator/examples/cli.md` | 用于定位项目的核心边界和上下游依赖。 |
| `Anthropic/Claude Code/bundled-skills/run-skill-generator/examples/server.md` | 用于定位项目的核心边界和上下游依赖。 |
| `Anthropic/Claude Code/bundled-skills/update-config.md` | 看配置约束、默认行为、兼容平台和发布/集成方式。 |
| `Anthropic/Claude Code/deferred-tools.md` | 看工具注册、权限、参数 schema、超时和失败回退。 |
| `Anthropic/Claude Code/glob-tool.md` | 看工具注册、权限、参数 schema、超时和失败回退。 |
| `Anthropic/Claude Code/grep-tool.md` | 看工具注册、权限、参数 schema、超时和失败回退。 |

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


---

生成时间：2026-07-10 13:59:05 CST
