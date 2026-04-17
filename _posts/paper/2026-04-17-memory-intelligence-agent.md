---
layout: post
title: "Memory Intelligence Agent：把 deep research agent 的记忆从‘长上下文检索’改成‘可演化的规划记忆’"
subtitle: '"Manager-Planner-Executor + alternating RL + test-time learning，让 memory 真正参与 agent 演化"'
date: 2026-04-17 10:30:00
author: "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
  - paper
  - agent
  - memory
  - deep-research
  - multi-agent
  - reinforcement-learning
  - test-time-learning
---

* TOC
{:toc}

# 0. 论文信息
- 标题：Memory Intelligence Agent
- 中文意译：记忆智能体
- 链接：<https://arxiv.org/abs/2604.04503>
- HTML：<https://arxiv.org/html/2604.04503v3>
- 时间：2026-04-09 v3
- 作者：Weicheng Meng, Yu Cheng, Zhihang Lin, Zhizhong Zhang, Xin Tan, Jingyu Gong, Kun Shao, Yuan Xie
- 单位：East China Normal University, Shanghai Innovation Institute, Harbin Institute of Technology, Xiamen University, Shanghai Artificial Intelligence Laboratory 等
- 说明：这篇笔记主要依据 **arXiv 摘要 + arXiv HTML 正文** 写成；我没有进一步核对附录、代码仓库和补充材料，因此实现细节与全部实验设定以作者正文为准。

# 1. 先说结论
这篇**值得读**，尤其适合最近在看 **deep research agent / memory agent / tool-using LLM / test-time learning** 的人。

我先给结论：
- **作者声称**：现有 memory agent 大多还是“从长上下文里捞相似轨迹”，存储越来越大、检索越来越贵，而且真正帮助 planning 的效果有限。MIA 通过 **Manager-Planner-Executor** 三段式架构，把记忆分成 **非参数记忆** 和 **参数记忆** 两部分，同时让 Planner 在训练阶段和测试阶段都持续演化。
- **实验观察**：从正文表 3 和表 4 看，MIA 在 7 个多模态 deep research 数据集、4 个文本数据集上都比此前 memory baseline 更强。比如多模态上，LiveVQA 从 Memento 的 36.7 提升到 43.1；文本任务上，2Wiki 从 64.2 提升到 71.8，GAIA 从 22.3 提升到 31.1。作者还声称，在 GPT-5.4 这种强 executor 上，MIA 仍能继续带来增益。
- **我的判断**：这篇真正有价值的地方，不是“又加了一个 memory 模块”，而是它明确提出：**deep research agent 需要的是过程记忆与规划记忆，而不是简单把更多历史文本塞回上下文**。这是个很对的问题定义。

但我也先说局限：
- 论文的证据主要集中在作者自己搭的 agent 流水线和 benchmark 组合上；
- 强结果很依赖 RL 训练、Judger、Router、外部搜索工具和 memory compression 组件的共同工作；
- 目前还很难判断：这些增益里，究竟有多少来自“记忆范式变化”，多少来自“更强训练与更复杂系统工程”。

所以我的总体评价是：
> **这不是一篇“记忆即检索”的小修小补论文，而是一篇试图把 agent memory 从静态外挂升级为持续可演化能力的系统论文。方向是对的，结果也有说服力，但还需要更多独立复现来确认含金量。**

# 2. 这篇论文在解决什么问题
作者想解决的，不是普通聊天模型“记不住用户说过什么”，而是 **deep research agent 在多轮搜索、规划、工具调用中的长期经验积累问题**。

作者认为，现有做法的核心缺陷有四个：
1. **长上下文会稀释注意力**，让模型更难聚焦当前问题；
2. **记忆里夹杂很多弱相关内容**，容易把噪声一并喂回去；
3. **历史越来越长，存储成本越来越高**；
4. **检索成本随记忆增长而变大**，导致推理效率变差。

而且作者特别强调：
deep research agent 需要的不是“结果导向的知识记忆”，而更像是：
- 哪种搜索路径有效
- 哪种失败模式要规避
- 多跳问题通常怎么拆
- 哪种计划更容易带来可执行的 tool interaction

也就是说，它更需要的是 **process-oriented memory（过程记忆）**，而不是简单保存事实片段。

这个问题定义我基本认同。
很多 memory agent 工作其实默认：
> 只要把过去轨迹检索回来，模型自然会学会怎么做。

但真实情况常常是：
- 检索回来的例子太长；
- 例子相关但不关键；
- planner 不会抽象经验；
- executor 也不一定真能听懂 plan。

MIA 就是在针对这几个断点下手。

# 3. 核心思路一句话
**把 agent 的“记忆”拆成两层：**
- **非参数记忆**：保存被压缩过的历史工作流与成功/失败轨迹，供当前 planning 做参考；
- **参数记忆**：把历史经验进一步蒸馏进 Planner 参数里，让 Planner 在训练和测试时都能持续成长。

然后整个系统由三个角色组成：
- **Memory Manager**：负责压缩、存储、检索和更新记忆；
- **Planner**：负责根据问题和记忆生成 plan，并在必要时反思后重规划；
- **Executor**：负责按 plan 调工具、搜索信息、完成回答。

这比“一个 agent + 一个 memory store”清楚得多，因为它把 **记忆存储、规划抽象、执行落地** 这三件事明确拆开了。

# 4. 方法拆解

## 4.1 总体框架：Manager-Planner-Executor
作者的架构其实很直观：

### Memory Manager
它做两件事：
1. 保存历史 trajectories；
2. 把冗长轨迹压缩成结构化 workflow 和记忆单元。

图 4 对应的是：
- 把图像压成 caption；
- 把冗长交互轨迹压成结构化摘要；
- 再写回 memory buffer。

作者声称这样可以显著降低存储和检索负担。

### Planner
Planner 是系统的大脑。
它基于：
- 当前输入问题
- 检索到的历史记忆
- 当前 Executor 的执行反馈

来生成：
- 初始 plan
- 必要时的 reflection
- revised plan

这里最关键的是：Planner 不是 frozen prompt planner，而是一个 **可训练、可在线更新** 的参数化模块。

### Executor
Executor 负责：
- 按 Planner 给的计划执行
- 走 ReAct 式工具调用
- 搜索与分析外部信息
- 给出结果
- 把执行状态反馈回 Planner

作者把 Planner 看作 **Cognitive Hub**，把 Executor 看作 **Operational Terminal**。这个类比挺准确：前者更像策略层，后者更像执行层。

## 4.2 Memory Retrieval：检索不是只看相似度
MIA 的 memory retrieval 不是简单 embedding top-k，而是三维打分：
- **Semantic Similarity**：当前问题和历史问题/图像描述的语义相似度；
- **Value Reward**：优先高成功率的 memory unit；
- **Frequency Reward**：鼓励低频条目，避免永远只用热门经验。

作者的动机是：
如果只按语义相似度检索，会出现两个问题：
1. 找回来的案例可能“看起来像”，但其实质量很差；
2. 高频热门模板会过度垄断检索结果，导致长尾经验进不来。

**我的判断**：
这一步是合理增强，但并不新到让人惊讶。真正决定上限的不是“三维检索”本身，而是后面的 **轨迹压缩质量 + Planner 是否真能吸收这些记忆**。

## 4.3 Collaborative Reasoning：Planner 和 Executor 真正联动
MIA 的核心 loop 是：
1. Planner 读当前问题和 memory context，生成初始 plan；
2. Executor 根据 plan + 工具反馈执行；
3. Executor 报告执行状态；
4. Planner 判断是否反思并重规划；
5. 反思最多触发一次，然后终止。

作者特意限制 **Reflect-Replan 最多触发一次**，目的是控制推理时间。

这一点我觉得很现实。因为如果反思机制无限循环，系统很容易变成：
- 看起来更智能；
- 实际更慢、更贵、更不稳定。

把反思次数硬限制住，本质上是在做系统工程上的稳定性取舍。

## 4.4 Experience Consolidation：把轨迹压回记忆
执行结束后，MIA 用 LLM Judger 评估结果，再由 Manager 做两件事：

### 1）更新非参数记忆
- 成功轨迹里选最短的一条，作为正例 workflow；
- 失败轨迹里随机采一条，作为反例 workflow；
- 然后压缩后写回 memory。

### 2）更新参数记忆
- 用当前 batch 的问题、轨迹和结果去训练 Planner；
- 把 episodic memory 内化成 Planner 的参数能力；
- 更新完成后，还会选择性清理 memory units，避免 memory 爆炸。

这就是作者说的 **parametric ↔ non-parametric 的双向转换回路**。

**我的判断**：
这是全篇最值得记住的设计之一。它至少在概念上回答了一个老问题：
> 如果 memory 永远只是外挂检索库，它怎么可能真正“成长”为能力”？

MIA 的答案是：
- 显式记忆负责当下参考；
- 参数更新负责长期吸收。

这比“永远靠 retrieval 弥补模型短板”更像一个真正的学习系统。

# 5. 训练：为什么要两阶段交替 RL
作者提出了 **Two-Stage Alternating RL Training**。

## 5.1 第一阶段：训练 Executor
目标是让 Executor 学会：
- 理解 Planner 给的 plan
- 按 ReAct 方式调用工具
- 在执行中保持格式规范
- 输出正确答案

奖励函数由三部分组成：
- 最终答案正确性（0.7）
- 工具调用是否成功规范（0.2）
- 输出格式是否合规（0.1）

这里的直觉很简单：
如果 Executor 连 plan 都读不懂，那 Planner 再强也没用。

## 5.2 第二阶段：训练 Planner
有了能执行的 Executor 后，再反过来训练 Planner，让它学会：
- 更好利用 memory context
- 生成更有效的初始 plan
- 什么时候该 reflection
- reflection 后怎么改 plan

Planner 的奖励同时考虑：
- 中间答案正确性
- 最终答案正确性
- 是否在该反思时反思、不该反思时不反思
- 格式合规

**我的判断**：
这个交替训练思路是有道理的。因为 Planner 和 Executor 的耦合确实很强：
- Planner 太弱，Executor 没方向；
- Executor 太弱，Planner 学不到真实反馈。

不过它的代价也很明显：
整个系统训练链更长、更复杂、调参更重，也更难独立复现。

# 6. Test-Time Learning：测试时继续长记性
这篇另一个亮点，是它不只做 offline training，还做 **test-time learning (TTL)**。

## 6.1 TTL 在做什么
作者的做法是：
- 测试时 Planner 不冻结，继续根据当前问题产生多个 plan rollout；
- Executor 执行这些 rollout；
- 用结果计算 reward；
- 一边把高质量 workflow 写进非参数记忆；
- 一边更新 Planner 参数。

也就是说，测试阶段也不是纯推理，而是：
> **探索 → 获取反馈 → 抽取 workflow → 更新 Planner**

## 6.2 为什么只更新 Planner，不更新 Executor
作者明确说：
- Executor 冻结，保证执行稳定；
- Planner 作为“认知中枢”负责持续成长。

这个选择我觉得非常理性。
如果测试时连 Executor 一起动，系统大概率会更不稳定、更难控。

## 6.3 Router 和 Meta Plan Memory
TTL 阶段里，Planner 会产生多个 rollout。作者再用一个 Router 从这些候选中挑最优计划与轨迹输出。

而且如果 rollout 里既有成功也有失败，系统会保留：
- 最短成功 plan
- 一个随机失败 plan

形成对比记忆，供之后选择计划时参考。

这个设计的意义在于：
它不是只积累“做对了什么”，还积累“哪些路看起来像样但其实会错”。

# 7. 无监督自演化：作者最想讲的新意之一
作者认为，在真实开放世界里，用户不会一直给 gold answer，所以不能总靠监督信号更新 memory。

于是他们提出一个 **模拟学术评审的无监督评估框架**：
- 一个 reviewer 看逻辑一致性；
- 一个 reviewer 看信息来源与可信度；
- 一个 reviewer 看结果完成度；
- 再由一个 Area Chair 汇总做最终裁决。

作者的核心动机是：
如果一个 reasoning trajectory：
- 逻辑严谨
- 证据来源可靠
- 幻觉较少
- 结果完成度足够

那它即便没有 gold answer，也可以作为近似监督信号，支持 memory 选择和 Planner 更新。

**我的判断**：
这部分概念上很吸引人，但也是我最保留的一块。

原因很简单：
- LLM judge 套 LLM judge，本身就有很强系统依赖；
- 多 reviewer + AC 比单一 judge 更稳，但仍然不等于真实可靠监督；
- 它更像“比单个打分器更可信”，但还远没到“可替代真标签”。

所以这部分我会看作：
**一个有前景的 open-world 训练近似方案**，但不是已经被彻底证明的答案。

# 8. 实验结果怎么读

## 8.1 多模态任务：MIA 确实把 memory baseline 拉开了
表 3 里，多模态 7 个数据集上，MIA 基本都优于其他 memory 方法。

几个比较显眼的点：
- **LiveVQA**：MIA 43.1，高于 Memento 的 36.7；
- **InfoSeek**：MIA 65.5，高于 Memento 的 57.3；
- **In-house 1**：MIA 31.8，高于 Memento 的 22.7；
- **In-house 2**：MIA 37.7，高于 Memento 的 30.7。

作者据此得出一个结论：
传统 contextual memory（RAG、Mem0、A-Mem）有时甚至不如 **No Memory**，说明长上下文 memory 确实会引噪声；而 MIA 这种“高层 plan + 双记忆演化”方式更有效。

这个结论我觉得是成立的，而且是这篇论文最重要的实证之一。

## 8.2 文本任务：增益更稳定
表 4 的文本结果也挺漂亮：
- SimpleQA：47.7 vs Memento 42.4
- 2Wiki：71.8 vs 64.2
- HotpotQA：63.5 vs 55.2
- GAIA：31.1 vs 22.3

这里尤其值得注意的是 **GAIA**，因为它更综合，更像 open-world agent 评测。MIA 在这类任务上的提升，比在封闭 QA 上更能说明问题。

## 8.3 对闭源强 executor 也有效
作者还测了把 Executor 换成：
- GPT-5.4
- Gemini-3-Flash
- Claude-Sonnet-4.6

结果作者声称：
MIA 仍能继续提升这些强模型，且基座越强，依然有稳健收益。

如果这个结论成立，那它说明 MIA 并不是“只对弱模型补短板”，而是确实在 **规划与记忆组织** 层面带来增益。

# 9. 我怎么看它的真实贡献

## 9.1 它重新定义了 memory 的位置
过去很多 agent memory 工作，本质上还是：
- 存一些轨迹
- 检索一些相似例子
- 拼进 prompt
- 希望模型自己悟出来

MIA 更进一步：
- 记忆要先被压缩成 workflow
- workflow 不只是提示词，还要成为 Planner 的训练素材
- Planner 要持续内化这些经验

也就是说，**记忆不是外挂，而是 agent 认知演化管线的一部分。**

## 9.2 它把 deep research agent 的“经验”定义成流程而不是知识片段
这是我很认同的一点。
很多复杂 agent 任务里，真正值钱的是：
- 先搜什么
- 遇到什么信号该换计划
- 哪些工具组合更有效
- 哪类错误值得尽早止损

这些都更接近 **workflow knowledge**，而不是百科知识。

MIA 至少在建模上承认了这件事。

## 9.3 它把 test-time learning 真正做进了 agent loop
很多 TTL 论文还是比较“模型内”；
这篇则把 TTL 放在一个真实 agent 流水线里，和 memory、router、judger、reflection 一起工作。

这会让系统更复杂，但也更接近真实 agent 的工作形态。

# 10. 局限与该追问的问题

## 10.1 系统太复杂，独立复现门槛高
这套系统依赖：
- Planner
- Executor
- Memory Manager
- LLM Judger
- Router
- RL training
- TTL online update

它不是一个轻量方法，而是一个重系统。
所以任何单点增益，都可能混杂系统集成收益。

## 10.2 “无监督自演化”仍然可能被 judge 偏差绑架
即便用了 reviewer + AC，多 LLM 评审仍然存在：
- 评分漂移
- 风格偏置
- 事实核验不足
- 对伪严谨推理过度打高分

这意味着，无监督自演化目前更像可用近似，而不是真可靠监督。

## 10.3 内存压缩是否损失关键信息
作者强调 memory compression，但压缩一定会带来信息损失。
值得追问的是：
- 哪些任务更适合 workflow summary
- 哪些任务必须保留更完整中间证据
- 压缩错了以后，会不会把坏策略固化进 Planner 参数里

## 10.4 真实部署下的成本问题
虽然作者想解决“长记忆越来越贵”的问题，但他们引入的 RL、TTL、judger、router 本身也不便宜。
所以最终成本是否真优，还得看实际部署配置。

# 11. 值不值得读
我的建议是：**值得读，而且不是只读 abstract。**

适合的人：
- 在做 research agent / search agent / deep research assistant
- 对 agent memory 不满足于“RAG + trajectory retrieval”
- 想看 RL、reflection、TTL 如何串进一个 agent 系统
- 想研究 Planner / Executor 解耦的人

如果你时间很少，优先看：
1. Introduction：它怎么批判 long-context memory
2. Figure 3 / 3.2：Planner-Executor-Memory loop
3. 3.3 / 3.4：alternating RL + TTL
4. Table 3 / Table 4：看增益是不是普遍存在

# 12. 一句话总结
**MIA 最重要的启发是：deep research agent 的 memory 不该只是“把旧轨迹塞回 prompt”，而应该是一套能把历史 workflow 压缩、检索、反思并内化进 Planner 的持续演化机制。**

如果这个方向继续做下去，未来更强的 agent memory，可能不再像一个外挂数据库，而更像一个会不断长经验的“策略器官”。
