---
layout:     post
title:      "Pi Agent Harness 项目解读"
subtitle:   " \"一个可扩展的终端 Coding Agent 框架\""
date:       2026-07-03 17:52:00
author:     "zwt"
header-img: "img/LLMs.png"
catalog: true
tags:
    - LLM
    - Agent
    - Coding Agent
    - 工程实践
categories: [llm]
---
* TOC
{:toc}

# 项目信息

- 项目地址：[earendil-works/pi](https://github.com/earendil-works/pi)
- 官网文档：[pi.dev](https://pi.dev)
- npm 包：[@earendil-works/pi-coding-agent](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
- 代码版本：本文阅读基于 `c9715af`，仓库最后一次提交时间为 2026-07-03
- 一句话定位：Pi 是一个 TypeScript 写的终端 Coding Agent 框架，核心目标不是只做一个固定形态的 AI 编程助手，而是提供一个可扩展、可嵌入、可自定义的 Agent Harness。

# 这个项目在做什么

Pi 的表层形态和 Codex CLI、Claude Code、Gemini CLI 这一类工具很像：用户在终端里输入需求，模型可以读文件、改文件、执行命令，然后把结果反馈给用户。

但从代码结构看，它更强调两个方向：

1. **Agent Harness**：把模型调用、工具执行、上下文管理、会话持久化、TUI 展示拆成相对独立的模块。
2. **可扩展工作流**：通过 extensions、skills、prompt templates、themes、packages 等机制，让用户不 fork 主仓库也能改造自己的 agent 行为。

所以它不是一个简单的“LLM + bash + 文件编辑器”脚本，而是一个围绕 coding agent 构建的运行时框架。

# Monorepo 结构

仓库是 npm workspace 形式的 TypeScript monorepo，核心包如下：

| 包 | 作用 |
| --- | --- |
| `@earendil-works/pi-ai` | 多 provider LLM API 抽象，负责 OpenAI、Anthropic、Google、Bedrock、OpenRouter 等模型接入 |
| `@earendil-works/pi-agent-core` | Agent runtime，负责消息状态、工具调用循环、事件流 |
| `@earendil-works/pi-coding-agent` | 终端 Coding Agent CLI，是用户直接使用的主程序 |
| `@earendil-works/pi-tui` | 终端 UI 库，负责交互模式下的界面渲染 |
| `@earendil-works/pi-orchestrator` | 编排相关模块，当前不是最核心入口 |

根目录的 `package.json` 里可以看到主要开发命令：

```bash
npm install --ignore-scripts
npm run build
npm run check
./test.sh
./pi-test.sh
```

它要求 Node.js `>=22.19.0`，并使用 `tsgo`、`biome`、`vitest`、`esbuild`、`bun build --compile` 等工具完成构建、检查和二进制打包。

# 核心架构

可以把 Pi 的主链路理解成下面这条线：

```text
CLI 参数 / stdin / TUI 输入
        |
        v
packages/coding-agent/src/main.ts
        |
        v
AgentSession
        |
        v
@earendil-works/pi-agent-core 的 agentLoop
        |
        v
@earendil-works/pi-ai 调用模型
        |
        v
模型返回文本或 tool call
        |
        v
执行 read / write / edit / bash 等工具
        |
        v
工具结果进入上下文，继续下一轮模型调用
```

其中 `packages/coding-agent/src/cli.ts` 非常薄，只做了几件事：设置进程标题、标记 `PI_CODING_AGENT=true`、配置 HTTP dispatcher，然后调用 `main()`。

真正的 CLI 逻辑在 `packages/coding-agent/src/main.ts`：

- 解析参数和运行模式
- 读取 stdin 或文件参数
- 加载全局和项目配置
- 处理 session resume / fork / clone
- 处理模型选择和认证
- 根据模式启动 interactive、print、json 或 rpc

`AgentSession` 是 coding-agent 层最关键的抽象。它把底层 `Agent` 包装成一个完整的 coding agent 会话，额外管理：

- session 文件持久化
- 模型切换和 thinking level
- 自动和手动 compaction
- bash 执行
- built-in tools 的注册
- extensions 的生命周期事件
- session tree、branch、export、import 等功能

# Agent Loop 如何工作

`packages/agent/src/agent-loop.ts` 是理解这个项目的关键文件。

它的逻辑是一个标准的 ReAct 式循环：

1. 用户消息进入上下文。
2. 调用 LLM 生成 assistant message。
3. 如果 assistant message 里有 tool call，就执行对应工具。
4. 把 tool result 追加回上下文。
5. 如果还有工具调用或队列消息，就继续下一轮。
6. 没有后续动作时触发 `agent_end`。

这个 loop 还有几个工程化细节：

- 支持 streaming event，TUI 可以实时渲染模型输出。
- 支持 steering message，也就是用户可以在 agent 运行时继续输入，用来打断或补充方向。
- 支持 follow-up message，当前任务结束后再处理排队消息。
- 工具调用可以并行，也可以按工具要求退回顺序执行。
- 每个阶段都会发事件，比如 `agent_start`、`turn_start`、`message_update`、`tool_execution_start`、`tool_execution_end`。

这让上层 UI、扩展系统、session 记录都不用侵入 agent loop 本身，只需要订阅事件。

# 内置工具

Pi 的默认 coding tools 在 `packages/coding-agent/src/core/tools` 目录下，主要包括：

| 工具 | 作用 |
| --- | --- |
| `read` | 读取文件 |
| `write` | 写入文件 |
| `edit` | 基于 diff 或匹配逻辑编辑文件 |
| `bash` | 执行 shell 命令 |
| `grep` | 搜索文本 |
| `find` | 查找文件 |
| `ls` | 列目录 |

README 里说默认给模型暴露四个工具：`read`、`write`、`edit`、`bash`。代码里还能看到 read-only 工具集合，包括 `read`、`grep`、`find`、`ls`。这说明它既能做完整 coding agent，也可以收缩成只读分析工具。

`bash` 工具的实现值得注意：它抽象了 `BashOperations`，也就是说命令执行后端可以替换。文档里提到 Gondolin micro-VM、Docker、OpenShell 等隔离方案，本质上就是把“模型想执行命令”和“命令在哪里执行”解耦。

# 多模型 Provider 层

`@earendil-works/pi-ai` 是 Pi 的模型抽象层。它不是只接一个 OpenAI compatible endpoint，而是维护了一套 provider collection。

从 README 看，内置支持的 provider 很多，包括：

- OpenAI / Azure OpenAI / OpenAI Codex
- Anthropic
- Google Gemini / Vertex AI
- DeepSeek
- Mistral
- xAI
- Groq
- Cerebras
- OpenRouter
- Vercel AI Gateway
- Amazon Bedrock
- GitHub Copilot
- Moonshot / Kimi For Coding
- MiniMax
- Xiaomi MiMo
- 本地 OpenAI compatible API，比如 Ollama、vLLM、LM Studio

这层做的事情主要有：

- 统一 message、tool call、tool result 格式
- 统一 streaming event
- 统一 token 和 cost tracking
- 统一 API key、OAuth、provider credential 解析
- 处理不同模型的 thinking/reasoning 差异
- 支持跨 provider handoff

对于 coding agent 来说，这一层很重要。因为 agent loop 不应该关心某个 provider 的 SSE 格式、tool call 字段名、thinking block 格式、OAuth token 怎么刷新，这些都应该被模型层抹平。

# 会话、压缩和分支

Pi 的会话能力做得比较重，不只是保存聊天记录。

它支持：

- `/resume`：恢复历史 session
- `/new`：新建 session
- `/tree`：在 session 树里跳转
- `/fork`：从某条用户消息创建分支
- `/clone`：复制当前分支到新 session
- `/compact`：压缩上下文
- `/export`：导出 HTML 或 JSONL
- `/import`：导入 JSONL session

从 `AgentSession` 和 compaction 相关代码看，它把长上下文问题当成 agent runtime 的一等问题，而不是简单等模型报 context overflow。

这种设计对真实 coding task 很有价值，因为代码任务通常不是一次 prompt 就结束。中间会经历读代码、试错、跑测试、修复、再测试。如果没有 session branch 和 compaction，很容易出现上下文膨胀、恢复困难、无法复盘的问题。

# 扩展系统是项目的亮点

Pi 的最大特点之一是 extensions。

扩展是 TypeScript 模块，可以放在：

- `~/.pi/agent/extensions/`
- 当前项目的 `.pi/extensions/`
- 或者通过 `pi -e ./path.ts` 临时加载

扩展可以做的事很多：

- 注册自定义工具
- 拦截或阻止 tool call
- 注册 slash command
- 添加 UI widget
- 修改 compaction 行为
- 监听 session、model、tool、resource 生命周期事件
- 持久化扩展自己的状态
- 注册自定义 provider

仓库里的 examples 很丰富，比如：

- `confirm-destructive.ts`：危险命令确认
- `protected-paths.ts`：保护路径，阻止写入敏感文件
- `git-checkpoint.ts`：每轮创建 git checkpoint
- `custom-provider-anthropic`：自定义 provider
- `dynamic-tools.ts`：动态工具
- `todo.ts`：状态型工具
- `github-issue-autocomplete.ts`：GitHub issue 自动补全

这说明 Pi 的设计理念不是把所有功能塞进主程序，而是把主程序做成一个可插拔 runtime。

# 安全边界

Pi 的 README 和 security 文档写得比较直接：它没有内置沙箱。

默认情况下，Pi 以启动它的用户权限运行。模型能用的工具可以读文件、写文件、编辑文件、执行命令。Extensions 也是普通 TypeScript 模块，拥有同样的本地权限。

它提供了 project trust 机制，但这个机制只解决“项目本地配置和扩展是否自动加载”的问题，不是安全沙箱。也就是说：

- 信任项目后，项目内 `.pi/extensions` 等资源可以被加载。
- 不信任项目时，这些资源会被跳过。
- 但一旦你让 agent 在某个目录里执行任务，built-in tools 依然可以按当前进程权限操作文件和命令。

所以它适合可信代码库内的高效率工程协作；如果要处理不可信仓库或无人值守自动化，应该放进 Docker、VM、micro-VM 或其他系统级沙箱里跑。

# 和常见 Coding Agent 的差异

Pi 和常见 coding agent 最大的差异，不在于“能不能改代码”，而在于它把可扩展性放得更前。

我的理解是：

| 维度 | Pi 的倾向 |
| --- | --- |
| 使用形态 | 终端 TUI + print/json/rpc + SDK |
| 模型接入 | 多 provider，强调统一抽象 |
| 工具系统 | 内置 coding tools，同时支持扩展注册工具 |
| 工作流改造 | 通过 extensions、skills、prompt templates、packages |
| 会话管理 | session tree、branch、compact、export/import |
| 安全策略 | 明确不做内置沙箱，推荐系统级隔离 |
| 工程定位 | 更像可二次开发的 agent harness，而不是单一产品形态 |

如果只是想要一个开箱即用的编程助手，它可能比封闭产品更需要配置和理解。如果你想研究 coding agent 架构，或者想把 agent 嵌到自己的工具链里，它的代码结构很值得看。

# 如何快速运行

官方推荐的安装方式：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

或者：

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

使用 API key：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pi
```

也可以在交互界面里用：

```text
/login
```

如果从源码运行：

```bash
git clone https://github.com/earendil-works/pi.git
cd pi
npm install --ignore-scripts
npm run build
./pi-test.sh
```

# 适合学习的代码入口

如果想读源码，我建议按这个顺序：

1. `packages/coding-agent/src/cli.ts`：CLI 启动入口，很薄。
2. `packages/coding-agent/src/main.ts`：参数、模式、session、配置、模型选择。
3. `packages/coding-agent/src/core/agent-session.ts`：coding agent 会话的主抽象。
4. `packages/agent/src/agent-loop.ts`：agent 循环和工具调用。
5. `packages/coding-agent/src/core/tools/`：内置工具实现。
6. `packages/ai/src/`：provider 抽象和模型调用兼容层。
7. `packages/coding-agent/docs/extensions.md`：扩展系统设计。

# 总结

Pi 是一个工程味很重的 coding agent 项目。它没有把重点放在炫酷 UI 或单一模型能力上，而是把 agent runtime 中最容易变复杂的部分拆出来：模型 provider、工具执行、事件流、会话持久化、上下文压缩、TUI、扩展系统。

从学习角度看，它适合用来研究三个问题：

1. 一个真实 coding agent 的主循环应该如何组织。
2. 多模型 provider 如何被统一到同一套 tool calling 和 streaming 接口。
3. 如何把 agent 做成可扩展平台，而不是一次性脚本。

如果后续要基于它做二次开发，我会优先从 extension 入手，而不是 fork 主仓库。因为它的扩展系统已经覆盖了权限确认、工具增强、状态管理、自定义 provider、UI 组件、命令注册等常见改造点。只有当你需要改 agent loop 或底层 provider 兼容层时，才值得进入核心包修改源码。

# 参考

1. [earendil-works/pi GitHub 仓库](https://github.com/earendil-works/pi)
2. [Pi 官方文档](https://pi.dev/docs/latest)
3. [@earendil-works/pi-coding-agent npm 页面](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
