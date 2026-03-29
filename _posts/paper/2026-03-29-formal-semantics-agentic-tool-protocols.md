---
layout: post
title: "Formal Semantics for Agentic Tool Protocols：把 SGD 与 MCP 放进 process calculus 之后，我们到底得到了什么"
subtitle: '"它真正有价值的，不是宣称 MCP 很强，而是试图把 agent 调工具协议从工程约定推进到可证明、可比较、可检查的形式化对象。"'
date: 2026-03-29 10:32:00
author: "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
  - paper
  - agent
  - tool-use
  - mcp
  - schema-guided-dialogue
  - formal-methods
  - process-calculus
  - verification
---

* TOC
{:toc}

# 0. 论文信息
- 标题：Formal Semantics for Agentic Tool Protocols: A Process Calculus Approach
- 中文意译：Agent 工具协议的形式语义：一种基于进程演算的方法
- 链接：<https://arxiv.org/abs/2603.24747>
- 时间：2026-03-25（arXiv 提交时间）
- 作者：Andreas Schlapbach
- 说明：**这篇笔记基于我今天拿到的 arXiv 摘要页与 PDF 正文可解析内容写成。** 因此下面会明确区分：
  - **论文正文可见事实**：我能在摘要或正文中直接确认到的内容；
  - **作者声称**：论文中的定理、命题、结论与价值主张；
  - **我的判断**：我对这篇工作的价值、边界和可能问题的分析。

# 1. 先说结论
**这篇值得读，但它更像一篇“agent protocol formalization / verification”论文，而不是一篇直接给你更强 benchmark 分数的应用 paper。**

它最值得看的地方有三点：
1. **它第一次把 SGD 和 MCP 都写进 process calculus / labeled transition system 里**，让两者可以被放到同一个形式化框架下比较；
2. **它试图证明 SGD 与 MCP 在一个前向映射 \(\Phi\) 下是结构双模拟（structurally bisimilar）的**，也就是“在某种观察层面，它们能表现出等价行为”；
3. **它进一步论证普通 MCP 到 SGD 的逆映射是部分且有损的**，再据此提出一个扩展版 **MCP+**，声称只要补足若干元数据字段，就能与 SGD 达到完整等价。

我的一句话判断：

> **这篇的核心价值不是“证明 MCP 万能”，而是把“agent 如何发现工具、校验参数、执行调用、处理失败、等待批准”这些工程约定，推进成可被证明、可被比较、可被检查的形式系统。**

但也要先泼冷水：

> **这篇基本是理论/形式化工作，不是实证导向论文。** 它最强的是建模与命题，不是实验验证；如果你想看大规模 benchmark、真实系统部署或严格 machine-checked proof，这篇还没走到那一步。

# 2. 它到底在解决什么问题
现在几乎所有 agent 系统都在调工具：function calling、schema-guided tool use、MCP server、JSON schema validation……

但现实里大家大多还是靠这几种方式维持系统正确性：
- prompt 约束；
- schema 写得尽量清楚；
- 运行时报错再补丁；
- 人工 review 高风险调用。

问题是：这些都**不等于形式化保证**。

论文在引言里举了一个银行转账 agent 的例子：
1. `verify_balance(account_id) -> balance`
2. `validate_transfer(amount, balance) -> authorized`
3. `execute_transfer(from, to, amount) -> confirmation`

它问的是这种级别的问题：
- agent **是否一定**会先查余额再转账？
- 第 3 步能不能绕过第 2 步审批直接执行？
- 如果第 3 步执行到一半失败，会不会留下不一致状态？
- 两个 agent 并发组合时，某些安全性质能不能被保留？

这些问题如果只靠“提示词写好一点”，是回答不了的。

所以这篇论文想干的事很明确：

> **为 agent–tool protocol 建一个形式语义层，让“工具调用是否安全、是否等价、是否可组合”变成可推理的问题。**

# 3. 论文的建模对象：SGD 与 MCP
论文选了两个对象：

## 3.1 SGD：Schema-Guided Dialogue
这里的 SGD 不是“随机梯度下降”，而是 **Schema-Guided Dialogue**。

**论文正文可见事实**：
- 它把 SGD 视为一种研究框架：模型在运行时读取 schema，而不是只依赖训练时见过的固定 ontology；
- 关键对象包括 intent、slot、schema、state tracking；
- 其核心思想是：**agent 可以通过机器可读 schema 在零样本条件下泛化到新 API / 新服务。**

从 agent/tool use 视角看，SGD 很像一种“较学术化的 schema-first tool protocol”。

## 3.2 MCP：Model Context Protocol
**论文正文可见事实**：
- MCP 被论文描述为 Anthropic 提出的 industry standard；
- 核心原语包括 **Tools、Resources、Prompts**；
- 架构包括 host、client、server；
- schema 通常用 OpenAPI / JSON Schema 表达；
- 它支持能力协商、工具发现、参数校验、工具执行等流程。

这两个体系都在回答同一个问题：

> **agent 如何通过 schema 发现并调用外部能力，而不需要对每个工具重新训练。**

论文的洞察是：
- SGD 和 MCP 在工程直觉上看起来很像；
- 但它们的**形式关系**此前并没有被认真定义。

# 4. 核心方法：把它们都写成 process calculus
这篇论文的主轴就是：

> **把 SGD 和 MCP 都写成 π-calculus 风格的进程系统，再比较它们的状态转移与可观察行为。**

## 4.1 SGD 的形式化对象
论文把 SGD 过程写成一套语法项，包括：
- `Intent⟨n, d, R, O, t⟩`
- `Slot⟨name, type, vals⟩`
- `CollectSlot⟨s, v⟩.S`
- `Execute⟨intent, bindings⟩`
- `Result⟨output⟩`
- `Error⟨type, msg⟩`
- 以及并行组合、channel restriction、replication、null process 等标准进程演算构件。

这里有个很重要的字段：`t ∈ {true, false}`，表示 **transactionality**。

我的理解是：
- 这相当于把“这个操作是否是带副作用、需要确认的事务性动作”直接写进了协议语义；
- 这也为后面“审批必须先于执行”这类安全命题埋下了形式基础。

## 4.2 MCP 的形式化对象
论文把 MCP 也写成类似的进程项：
- `Tool⟨n, d, schema⟩`
- `Resource⟨uri, content⟩`
- `Prompt⟨template, args⟩`
- `Initialize⟨caps⟩`
- `ToolsList⟨metadata⟩`
- `ToolCall⟨n, params⟩`
- `Validate⟨params, schema⟩`
- `Result⟨output⟩`
- `Error⟨type, msg⟩`
- 外加并行/限制/复制等构造。

这一步的意义在于：
- SGD 不再只是“dialogue schema”语义；
- MCP 也不再只是“工程协议说明书”；
- 两者都被放进一个可比较的、带操作语义的统一框架。

## 4.3 Labeled Transition System：比较的是“可观察行为”
论文接着为 SGD 与 MCP 各自定义 labeled transition system（LTS）。

**论文正文可见事实**：
- SGD 的 labels 包括 `invoke(n,p)`、`collect(s,v)`、`execute`、`result(o)`、`error(t,m)`；
- MCP 的 labels 包括 `call(n,p)`、`τ`、`execute`、`result(o)`、`error(t,m)`、`read(u)`；
- 其中 `collect_slot`、`validate`、`negotiate` 等可以被视作 silent action（`τ`）。

这件事很重要，因为它意味着论文比较 SGD 和 MCP，不是比较“长得像不像”，而是在比较：

> **对外可观察到的调用、执行、返回、报错行为，是否能在某个映射下互相模拟。**

# 5. 前向映射 \(\Phi\)：论文最核心的一步
论文定义了一个从 SGD 到 MCP 的映射 \(\Phi\)。

## 5.1 它怎么映射
大意是：
- `Intent` 会被映射成 `Tool`；
- SGD 的 required / optional slots 会被映射成 JSON schema 的 `required` 与 `properties`；
- `Execute`、`Result`、`Error` 等执行态也会被对应到 MCP 侧的 tool call / result / error。

换句话说，论文在说：

> **SGD 里的 intent + slots 结构，本质上可以被翻译成 MCP 里的 tool + schema 结构。**

这一步非常合理，因为两边都在表达：
- 工具叫什么；
- 参数有哪些；
- 哪些必填；
- 参数类型与枚举范围是什么；
- 调用成功/失败后怎么转移。

## 5.2 Action equivalence：`invoke ≈ call`
论文进一步定义 action equivalence：
- `invoke(n,p) ≈ call(n,p)`
- `collect(s,v) ≈ τ`
- `execute ≈ execute`
- `result(o) ≈ result(o)`
- `error(t,m) ≈ error(t,m)`

直白说就是：
- SGD 里收 slot 的过程在 MCP 那边不一定显式暴露，所以可以折叠成 silent action；
- 真正重要的是发起调用、执行、返回和报错这些外部可观察事件。

## 5.3 论文声称的主要理论结果：`SGD ∼ MCP under Φ`
**作者声称 / 论文正文可见事实**：
- Theorem 4.4 给出了核心结论：`∀S ∈ SGD. S ∼ Φ(S)`；
- 论文通过 structural induction 证明 relation `R = {(S, Φ(S))}` 是一个 bisimulation。

这意味着在作者的定义下：

> **任意一个 SGD 过程，都能在映射到 MCP 后保留其结构与行为上的可观察等价。**

我的判断：
- 这一步是全文含金量最高的部分之一；
- 它把“SGD 和 MCP 很像”这种工程直觉，推进成了一个可以写成 theorem 的形式化结论。

# 6. 为什么逆映射 \(\Phi^{-1}\) 不成立：论文最有意思的批判部分
如果论文只做到 “SGD 可以映射到 MCP”，那它只是“把 SGD 翻译成 MCP”。

真正有意思的是它接着问：

> **那反过来，MCP 能不能完整还原成 SGD？**

论文的答案是：**不能，至少普通 MCP 不行。**

## 6.1 逆映射是 partial and lossy
**作者声称 / 论文正文可见事实**：
- Theorem 5.2：\(\Phi^{-1}\) 是 partial；
- Theorem 5.4：round-trip `Φ^{-1} ◦ Φ ≠ id_SGD`，即存在信息损失；
- Theorem 5.5：在定义域内，`Φ^{-1}` 也不是 injective。

这三条合起来说明：
- 有些 MCP 对象根本无法映回 SGD；
- 即便能映，也可能丢语义；
- 甚至两个不同的 MCP 对象，可能会塌缩成同一个 SGD 表示。

## 6.2 论文具体指出了哪些“丢失”
### (1) transactionality / approval 信息丢失
论文给的一个核心反例是：
- 在 SGD 里，`Intent⟨..., t=true⟩` 明确表示这是事务性动作；
- 但普通 MCP 的 `Tool⟨name, description, schema⟩` 里，没有一个等价、机器可读、可验证的 `is_transactional` 字段。

结果是：
- 你可以从 SGD 映到 MCP；
- 但再从 MCP 映回来时，`t` 已经恢复不出来了。

这很关键，因为它直接关系到：
- 是否需要批准；
- 是否有副作用；
- 执行前是否必须插入 human-in-the-loop。

### (2) MCP 的 `Resource` 无法映到 SGD
论文直接举了 `Resource⟨uri, content⟩` 的反例。

这类对象是**被动上下文**，不是一个可执行 intent。

也就是说：
- MCP 不只是“工具调用协议”；
- 它还显式包含 read-only context。

而 SGD 没有这个原语。

### (3) capability negotiation / dynamic discovery 无法映到 SGD
MCP 里有 `Initialize⟨caps⟩` 和 `ToolsList⟨...⟩` 这类能力协商与运行时发现机制。

论文认为：
- SGD 默认假设 schema 是 upfront 给定的；
- 它没有天然对应 capability negotiation 的过程项。

### (4) failure modes / dependencies / approval protocol 缺少结构化表示
论文在 gap summary 里总结：普通 MCP 缺少以下机器可读表达：
- transactionality / explicit action boundary；
- structured error recovery paths；
- explicit inter-tool dependency declaration；
- formal human-in-the-loop approval protocol。

我的判断：

> **这是全文最有批判锋芒的部分。** 它不是简单吹 SGD，也不是简单吹 MCP，而是在说：MCP 作为工业协议很实用，但从“可形式验证”的角度看，它还有若干语义缺口。

# 7. 五条原则：作者想补齐什么
论文最核心的设计输出，是从双向分析里提出五条原则。

## 7.1 五条原则分别是什么
**论文正文可见事实**：论文列出的五条原则是：
1. **Semantic completeness**
2. **Explicit action boundaries**
3. **Failure mode documentation**
4. **Progressive disclosure compatibility**
5. **Inter-tool relationship declaration**

下面我按“论文内容 + 我的理解”拆开说。

## 7.2 Principle 1：Semantic completeness
论文的意思不是“description 越长越好”，而是：

> **schema 描述要提供足够语义密度，说明参数为什么存在、约束是什么，而不只是写一个类型。**

论文甚至定义了 `semantic density` 这样的量，并给出类型规则，要求 description 不能空洞到只剩字段名复述。

我的判断：
- 这点跟实际 tool calling 非常相关；
- 很多 tool schema 不是真的“不可用”，而是“形式上合规、语义上贫瘠”；
- 如果把 schema quality 纳入可检查性质，这对 agent routing / tool selection 很有价值。

## 7.3 Principle 2：Explicit action boundaries
这是我觉得最实用的一条。

论文要求工具显式标注：
- `side_effects ∈ {read, write, delete, none}`
- 对 `write/delete` 要求 `requires_approval = true`

然后它把这件事写成类型规则与过程约束，导出一个安全性质：

> **有副作用的执行必须先经过 approval。**

我的判断：
- 这条非常接近真实 agent system 的安全需求；
- 如果 MCP 真能把这类字段做成标准化元数据，就不该再只靠 description 里写“dangerous”来提醒模型。

## 7.4 Principle 3：Failure mode documentation
论文要求工具显式声明：
- 可能的 error types；
- 对应 recovery strategy，例如 retry / fallback / user prompt / abort。

这一步很重要，因为它把“错误处理策略”从运行时经验主义，推到了 schema / protocol 层。

我的判断：
- 现实中的 agent 失败往往不是“调错工具”，而是**调对了工具但对失败路径没有结构化认知**；
- 这条原则很像把“异常语义”也纳入协议签名。

## 7.5 Principle 4：Progressive disclosure compatibility
论文注意到：真实系统里工具很多，description 很长，token 成本高。

所以它提出一个两级描述机制：
- discovery 阶段只给 summary；
- invocation 阶段再拉 full description / full schema。

论文还给出一个 token reduction theorem，声称在实际只调用少量工具的场景下，progressive disclosure 可以把 token 开销显著压下去。

我的判断：
- 这条更多是“工程可扩展性原则”，不是理论核心；
- 论文自己也承认：它对严格等价不是必要条件，但对实际部署很关键。

## 7.6 Principle 5：Inter-tool relationship declaration
论文要求工具显式声明依赖关系，例如：
- `Requires`
- `ProducesInputFor`
- `ExclusiveWith`

然后它给出依赖安全性命题：

> **如果 Ti 依赖 Tj，则在所有合法执行轨迹中，`execute(Tj)` 必须先于 `execute(Ti)`。**

我的判断：
- 这条很像把 workflow DAG / planning constraint 直接写进工具协议；
- 如果未来 agent protocol 真能支持这一层，就会从“自由 prompt 规划”往“受约束的可验证 orchestration”迈一步。

# 8. MCP+：作者提出的扩展版协议
论文没有停在批评普通 MCP，而是提出 **MCP+**。

## 8.1 MCP+ 加了什么
**论文正文可见事实**：MCP+ 在 `Tool+` 中加入这些 metadata：
- `side_effects`
- `requires_approval`
- `failure_modes`
- `summary`
- `dependencies`

然后定义扩展映射 `Φ+` 与其逆映射 `(Φ+)^{-1}`。

## 8.2 论文的最强主张：`MCP+ ≅ SGD`
**作者声称 / 论文正文可见事实**：
- Theorem 7.1 声称 `MCP+ ∼= SGD`；
- 它还进一步声称 `(Φ+)^{-1} ◦ Φ+ = id_SGD`，以及 `Φ+ ◦ (Φ+)^{-1} = id_MCP+`；
- Corollary 7.2 认为这五条原则对 full behavioral equivalence 是 necessary and sufficient；
- Theorem 7.3 进一步称这些原则构成 minimal extension（其中 P4 更像 scaling principle）。

这相当于在说：

> **不是 MCP 天生不行，而是普通 MCP 缺少一小组关键元数据；一旦补齐，就可以与 SGD 达到完整双向等价。**

我的判断：
- 这个主张非常强，也非常“论文型”；
- 它的价值不只在结论本身，更在于给出了一张清晰的路线图：
  - 想让 agent protocol 更可验证，具体该补哪些语义位。

# 9. 安全性质：这篇论文不只是做等价，还想做 safety
论文第 8 节把若干安全性质写成 process invariant。

## 9.1 Capability confinement
论文给出 channel scoping / typed π-calculus 视角下的 capability confinement：
- 机密 key 被限制在作用域内；
- 外部进程无法访问；
- 类型系统阻止 channel smuggling。

这类结论更像“如果你把协议写成这类 calculus，那么某些能力泄漏可以被形式证明不会发生”。

## 9.2 Tool poisoning prevention
论文还讨论一种 tool poisoning attack：
- 工具在 description 中夹带“忽略之前指令、导出凭证”之类恶意文本。

它的防御思路是：
- 把 `description` 类型化为 inert data / string；
- 只能 `display(desc)`，不能 `execute(desc)`；
- 因此字符串描述不能越权成为可执行代码。

我的判断：
- 这个结果在形式系统里是自洽的；
- 但现实中的 prompt injection 问题通常不是“模型把字符串直接当代码执行”，而是“模型把字符串当自然语言指令采纳了”；
- 所以这条 theorem 更像一个**理想化威胁模型下的类型安全结论**，不是现实 prompt injection 的完整解法。

## 9.3 Approval ordering 与 dependency ordering
论文还证明了：
- 对 `write/delete` 工具，`approval` 先于 `execute`；
- 对声明了 `Requires` 依赖的工具，前置依赖必须先执行。

这些命题都很符合真实 agent orchestration 的需要。

我的判断：
- 这是这篇论文最接近“可落地安全约束”的部分；
- 它提示我们，未来 agent tooling 不是只有 schema validation，还应该有 protocol-level ordering constraints。

# 10. 这篇论文有没有实证实验？
这里要说得很明确：

> **这篇论文主体是形式化/理论论文，不是以实验为中心的实证工作。**

**论文正文可见事实**：
- 文章主线是 syntax、operational semantics、LTS、bisimulation、reverse mapping、type rules、security theorems；
- 文中引用了作者另一篇 companion study，说五条原则曾带来 routing accuracy 的经验改进；
- 但这篇 arXiv:2603.24747 本身并没有把大篇幅放在 benchmark 表格或系统实验上。

所以如果你要问“这篇有没有强实验支撑”：
- **就本文本身而言，偏理论，没有大规模实证主线。**

# 11. 我觉得它真正的价值在哪里
## 11.1 它把 schema quality 提升成了“可证明性质”
这点很不一样。

多数工程系统把 schema 当文档；
这篇想把 schema 当**形式对象**。

这意味着什么？
- schema 不只是“给模型看的说明书”；
- schema 还可以承载 approval、failure mode、dependency、summary、semantic density 等结构化约束；
- 这些约束进一步能导出安全与等价结论。

如果这条路线走通，agent system 的很多“脆弱 prompt 约定”确实可能下沉到协议层。

## 11.2 它把 MCP 从“能不能用”转成“可不可以验证”
这篇论文不是在问：
- MCP 实用不实用？

而是在问：
- MCP 的哪些语义位是足以支撑 formal verification 的？
- 哪些位缺失了，所以逆映射会失败？

这会让很多关于 MCP 的讨论从“范式站队”转向“语义完备性”。

## 11.3 它给未来 agent infrastructure 提供了非常清晰的补课清单
如果你是做 agent infra / tool protocol 的，这篇至少给了一份 checklist：
- 是否显式标注 side effects？
- 是否有 approval 语义？
- 是否声明 failure modes？
- 是否区分 summary 与 full description？
- 是否声明 inter-tool dependencies？

这些问题都比“再加几条例子让模型更听话”更底层。

# 12. 这篇论文的边界与可能问题
## 12.1 证明目前还是 paper proof，不是 machine-checked proof
**论文正文可见事实**：
- 作者在 future work 里明确承认，当前 bisimulation proofs 是 pen-and-paper arguments；
- 未来才考虑放进 Isabelle/HOL 或 Coq。

所以这里不能夸大成“已经完全机器验证”。

## 12.2 威胁模型偏理想化
像 tool poisoning prevention 这类结论，更多是在一个类型系统清晰、执行边界明确的模型里成立。

现实世界里：
- LLM 会把 description 当 reasoning input；
- injection 往往不是“执行字符串”，而是“采纳字符串建议”；
- 因此从 type safety 到真实 prompt security，中间还有一大截。

## 12.3 把实际协议抽象成 calculus 时，可能会遗漏工程细节
形式化一定要抽象。

问题在于：
- 真实 MCP server 的行为比论文里的 `Tool / Validate / Execute / Result` 更脏；
- 有版本漂移、上下文污染、tool result serialization、host policy、权限模型、异步中断、streaming、UI approval 等现实复杂度。

所以这篇给的是一个高层语义骨架，不是完整工业语义规范。

## 12.4 `MCP+ ≅ SGD` 的结论很强，但是否是“唯一最好”的扩展还可讨论
论文把五条原则论证为 minimal extension，这在其定义体系里成立。

但从更广泛工程视角看，还可以问：
- 有没有别的元数据设计也能达到类似等价？
- 这些原则是否过度贴合 SGD，而不一定是 future agent protocol 的唯一自然分解？

所以我会把它看成：
- **一个很强、很清晰的 formal proposal**，
而不是
- **已经定于一尊的协议真理。**

# 13. 读这篇时我建议重点盯哪几处
如果你只打算花有限时间，我建议看这几块：

## 13.1 Theorem 4.4：为什么前向双模拟能成立
这是全文的地基。

## 13.2 Section 5：逆映射为什么失败
这是全文最有洞察的部分，因为它告诉你普通 MCP 究竟缺在哪。

## 13.3 Section 6-7：五条原则与 MCP+
这是论文最有工程启发的输出。

## 13.4 Section 8：安全性质
尤其看 approval ordering、dependency ordering 这两条，和真实 agent orchestration 最接近。

# 14. 最后一句判断：值不值得深读？
**值得，但要带着正确预期去读。**

如果你关心的是：
- agent tool calling 的形式化基础；
- MCP / schema-first protocol 的可验证性；
- tool metadata 应该如何设计得更安全、更可检查；
- 多工具 orchestration 的依赖与审批语义；

那这篇很值得看。

但如果你关心的是：
- 新 benchmark 分数；
- 更强 agent policy；
- 大规模真实系统实验；

那它不是这类论文。

我的最终判断：

> **这篇更像一篇“给未来 agent protocol 补理论底座”的论文。它的真正价值不在于立刻让 agent 更聪明，而在于逼着我们把‘工具调用协议到底包含哪些可验证语义’这件事说清楚。**

对现在的 agent 系统来说，这类工作未必马上带来产品分数提升，但它很可能决定你未来能不能把系统从“靠约定维持”升级到“靠协议证明约束”。

# 15. 一个适合带走的 checklist
最后给个我觉得最实用的 takeaway。以后你审视一个 tool protocol / MCP schema，可以直接问这 5 个问题：

1. **语义够不够完整？** 还是只有字段名和类型？
2. **副作用边界写清楚了吗？** 哪些 read，哪些 write/delete？
3. **失败路径写清楚了吗？** 出错后 retry/fallback/user prompt/abort 怎么走？
4. **有没有 progressive disclosure？** 选择时看摘要，调用时再拉详细 schema。
5. **工具间依赖关系是不是显式的？** 哪些必须先做，哪些互斥，哪些产物给下游用？

如果这些都没有，那你现在拥有的更像“模型能凑合调用的接口”，而不是“可以被验证的 agent protocol”。

这就是这篇论文真正想提醒我们的事。