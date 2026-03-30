---
title: "Anticipatory Planning for Multimodal AI Agents"
date: 2026-03-30 10:30:00 +0800
categories: [paper, agents, multimodal]
tags: [multimodal-agent, gui-agent, reinforcement-learning, planning, tool-use]
---

> 论文：**Anticipatory Planning for Multimodal AI Agents**  
> arXiv: 2603.16777  
> 作者：Yongyuan Liang, Shijie Zhou, Yu Gu, Hao Tan, Gang Wu, Franck Dernoncourt, Jihyung Kil, Ryan A. Rossi, Ruiyi Zhang  
> 机构：UMD / Ohio State / Adobe Research / SUNY Buffalo  
> 说明：这篇笔记基于 **arXiv 页面与 HTML 正文** 整理，不是逐图逐附录精读版。

## 一句话结论

这篇工作的核心价值不在于又做了一个 GUI agent，而在于它把“**先看几步，再只执行第一步**”这件事做成了可训练的强化学习目标。**作者声称**这样能让多模态 agent 从 reactive 决策，变成短视野但前瞻性的 anticipatory planner；从结果看，**实验观察**也确实支持它在 GUI 与 tool-use 两类任务上，比同量级开源基座更稳、更像真正会规划的 agent。**我的判断**是：这篇更像“agent 训练范式”的论文，而不是单点 benchmark hack，值得关注。

---

## 这篇论文在解决什么问题

很多 GUI / computer-use / tool-use agent 看起来会“多步推理”，但训练目标往往还是一步一步做局部最优：

- 当前看到什么，就决定下一步做什么；
- 奖励信号偏 step-level；
- 很少显式约束“后面几步是否连贯、是否可执行、是否朝同一个长程目标推进”。

**作者的判断**是：这类 agent 本质上还是 reactive 的，所以在长链任务里很容易出现：

- 早期一步没错，但后面逐渐偏航；
- 重复点击、重复调工具；
- 高层计划和底层执行脱节；
- 局部动作对，整体任务还是完不成。

这篇论文的目标，就是把“anticipatory reasoning / lookahead planning”直接写进训练流程里。

---

## 方法：TraceR1 在做什么

论文提出的框架叫 **TraceR1**。

它的 inference 逻辑很直观：

1. 给定当前观察（截图、历史、指令）；
2. 先预测一个**未来多步轨迹**；
3. 但真正只执行**第一步**；
4. 拿到环境反馈后再重新规划下一轮。

也就是一种 **plan–act loop**：

- 先对未来几步做 lookahead；
- 但不把整条计划硬执行到底；
- 每执行一步，就根据新反馈重规划。

这点很关键：它不是传统那种“先生成完整计划再严格执行”，而是**用短期前瞻提升当前动作质量**。

### 1) Stage 1：Trajectory-level RL

第一阶段做的是**轨迹级强化学习**。

不是只管某一步动作对不对，而是让模型去学习：

- 未来几步是否全局一致；
- 动作序列是不是围绕同一个任务目标；
- 是否存在无意义重复；
- 长链计划是否有时序上的合理性。

按论文描述，这一阶段的奖励设计强调：

- **trajectory alignment**：预测轨迹和参考轨迹的一致性；
- **repetition penalty**：惩罚重复、刷奖励式动作；
- **temporal discount**：对更远未来的信用分配做衰减，避免训练噪声失控。

### 2) Stage 2：Grounded Reinforcement Fine-Tuning

只做轨迹层的训练还不够，因为“计划看起来合理”不等于“每一步真能执行”。

所以第二阶段再加一个 **grounded RFT**：

- 把预测出的 step instruction 交给冻结的 tool agent / executor；
- 用真实执行反馈来修正 planner；
- 奖励不再只是抽象的“计划像不像”，而是看它是否真的可落地。

**作者声称**，这一阶段能把高层计划和低层执行重新对齐。  
**我的理解**：Stage 1 像是在教模型“想得更长”，Stage 2 像是在教模型“别想得太飘”。

---

## 这套方法为什么有意思

我觉得这篇最有意思的点有 3 个。

### A. 它强调的是“前瞻性规划”，不是单纯 CoT 变长

很多 agent 工作会把更长的 reasoning trace 当成 planning 提升，但这篇不是只拉长文本链路，而是明确要求模型去预测**未来动作轨迹**。

也就是说，重点不是“解释更多”，而是：

- 后面大概会发生什么；
- 当前动作会不会把后面带偏；
- 哪些未来分支明显不可执行。

这是更接近 agent planning 的训练目标。

### B. 它把 planning 和 grounding 拆成两层

纯 planning 容易虚，纯 grounding 容易短视。  
TraceR1 的两阶段训练，本质是在做一个折中：

- Stage 1 学全局一致性；
- Stage 2 学局部可执行性。

这个结构其实挺像人做复杂任务：

- 先脑子里过几步；
- 再按当前反馈修最近一步。

### C. 它尝试统一 GUI agent 和一般 tool-use

很多方法只在 computer-use 上成立，或者只在 tool benchmark 上成立。  
这篇工作的 ambition 更大：想用一个 anticipatory planning recipe，同时覆盖：

- 在线 GUI benchmark；
- 离线 GUI benchmark；
- 多模态 tool-use / reasoning benchmark。

如果这个训练范式后面被更多团队复用，它的影响力可能会超过单篇 benchmark paper。

---

## 实验里最值得看的结果

## 1. 在线 GUI benchmark：开源同量级里明显变强

论文在 **AndroidWorld** 和 **OSWorld-Verified** 上做了在线评测。

其中比较关键的一组结果：

- **Qwen3-VL-32B-Thinking**：OSWorld-Verified 从 **35.6** 提升到 **41.2**；
- **UI-TARS-1.5-7B**：OSWorld-Verified 从 **27.4** 提升到 **30.9**；
- 同时在 AndroidWorld 上，作者给出的 TraceR1 版本达到 **64.8**。

**实验观察**：作者强调这是相对同规模开源模型的显著提升，并称其达到或接近部分 proprietary planner 的水平。  
**我的判断**：OSWorld 这类长程桌面任务本来就很容易在多步交互里崩掉，所以这里的提升比纯离线 step 指标更有说服力。

## 2. 离线 GUI benchmark：高层任务规划能力也更稳

在 **AndroidControl-High / GUI-Odyssey / Multimodal-Mind2Web** 上，论文给出的 TraceR1（UI-TARS-7B + Ours）成绩是：

- AndroidControl-High: **75.3**
- GUI-Odyssey: **88.2**
- Multimodal-Mind2Web: **65.3**

对比一些开源基线：

- UI-TARS-7B：72.5 / 87.0 / 63.1
- UI-TARS-32B：74.7 / 88.6 / 64.7
- GUI-R1-7B：51.7 / 38.8 / -

**实验观察**：TraceR1 在同量级开源模型里很强，尤其 AndroidControl-High 提升明显。  
**我的判断**：这说明它不只是会“多想一点”，而是真的把高层 instruction 分解成低层动作的稳定性做上去了。

## 3. GAIA / GTA：不仅是 GUI，有一般工具推理收益

在更一般的 tool-use / multimodal reasoning benchmark 上：

- **GAIA answer accuracy**：TraceR1 **40.2**，高于 GPT-4o 的 **33.4**；
- 相比 **Qwen3-VL-8B** 的 **31.5**，提升 **+8.7**；
- 在 **GTA** 上，TraceR1 的结果为：
  - AnsAcc: **56.7**
  - ToolAcc: **65.7**
  - CodeExec: **87.4**

**实验观察**：作者把这个结果解释为 anticipatory planning 对 tool selection、code execution reliability 也有帮助。  
**我的判断**：这部分结果挺重要，因为它说明“看几步再走一步”的训练目标，可能不是 GUI 独有技巧，而是一种更一般的 agent 训练 bias。

---

## 消融实验告诉了我们什么

这篇消融不花哨，但信息量够用。

### 1. Stage 2 很重要

去掉 grounded RFT 之后，作者报告在 AndroidWorld / OSWorld-Verified / GTA 上平均会掉大约 **6%**。

**作者声称**：如果没有执行反馈，planner 容易学出“看起来对、实际上不可执行”的轨迹。  
**我的判断**：这很合理。纯 trajectory reward 容易把 agent 训成“会想不会做”。

### 2. 预测 horizon 不是越长越好

作者测试了不同 horizon 长度，结论是：

- 适度 lookahead 会提升效果；
- 但 **T > 10** 后性能明显下降。

这点我很认可。因为未来越远，不确定性越大，credit assignment 会越来越脏。  
所以真正有效的不是“无限长规划”，而是**有限前瞻 + 持续重规划**。

### 3. repetition penalty 和 temporal discount 都有用

去掉重复惩罚或去掉时间折扣，性能都会掉。

作者给出的解释是：

- 没有 repetition penalty，模型会出现 reward hacking，反复做冗余动作；
- 没有 temporal discount，远期预测噪声会污染训练。

这说明这篇论文不是光靠“大力出奇迹”，而是 reward design 上确实认真想过 agent planning 的病灶。

---

## 我怎么看这篇论文的真实价值

### 值得肯定的地方

**第一，问题定义是对的。**  
现在很多 agent 论文默认“多步执行失败”是 grounding 不够强，但这篇明确指出：很多失败其实来自**没有显式前瞻规划**。

**第二，方法结构很干净。**  
两阶段：先学 anticipatory trajectory，再学 grounded executability，逻辑清楚，也容易被后续工作继承。

**第三，跨任务类型的一致收益很关键。**  
GUI 和一般 tool-use 都涨，说明这不是单 benchmark overfit 的味道。

### 我保留意见的地方

**1. 目前还是短视野 anticipatory planning，不是强世界模型。**  
它能“提前看几步”，但离真正会模拟环境 dynamics 的 planner 还有距离。

**2. 执行器是冻结外部 tool agents。**  
这很实用，但也意味着 planner 的上限部分受 executor 影响；如果 executor 很弱，planner 再会想也可能落不了地。

**3. benchmark 仍然偏受控。**  
虽然已经覆盖 7 个 benchmark，但离真实开放世界 computer use 还有差距。  
尤其人在真实电脑上碰到的脏 UI、异常弹窗、账号态、页面漂移，未必能被这些结果完全代表。

**4. 论文主打“comparable to proprietary systems”，但离顶级闭源还有差距。**  
比如 GAIA 上，GPT-5 还是明显更强。  
所以更准确的说法是：**它把开源 agent planner 往前推了一步，但还没有追平最强闭源通用 agent。**

---

## 这篇论文最适合谁看

我觉得有三类人值得看：

1. **做 GUI / computer-use agent 的人**  
   可以直接借鉴“predict trajectory, execute first step, re-plan”这套训练和推理思路。

2. **做 tool-use agent / multimodal agent training 的人**  
   这篇给了一个比 step-level SFT / RL 更像 planning 的训练目标。

3. **关心 agent 为什么总在长任务里变笨的人**  
   这篇至少给了一个很具体的答案：不是它不会下一步，而是它没被训练成会提前看几步。

---

## 如果我要继续追这条线，我会看什么

后续我会重点追 4 个问题：

1. **这种 anticipatory training 能否迁移到真实在线 web / desktop agent？**
2. **planner 和 executor 能否联合训练，而不只是 planner 吃 executor 反馈？**
3. **短视野 planning 如何和长期 memory / subgoal decomposition 结合？**
4. **如果 benchmark 更开放、更脏，这个收益还剩多少？**

---

## 最后的判断

**我的结论**：这篇论文值得读，尤其如果你关心 agent planning。它不是那种“换个 backbone 再刷几个点”的 paper，而是在认真回答一个核心问题：**怎样把前瞻性规划变成一个能训练出来的能力。**

如果只看一句话版：

> **TraceR1 的核心贡献，是把“先预测几步未来、再只执行第一步并持续重规划”做成了一个可落地的 RL 训练范式；它未必是终点，但很可能是开源 multimodal agent 从 reactive 走向真正 planning-aware 的一块关键垫脚石。**
