---
title: "Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents"
date: 2026-04-07 10:30:00 +0800
categories: [paper, agents, citation-reliability]
tags: [llm, deep-research, citations, hallucination, urlhealth, rag]
---

> 论文：**Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents**  
> arXiv: 2604.03173  
> 链接：https://arxiv.org/abs/2604.03173  
> 说明：这篇笔记与今天 10:00 已送达的轻量推荐保持同一选题。本文依据 **arXiv 摘要 + arXiv HTML 正文可访问部分** 整理；我拿到了主要方法、实验设定和核心结果，但**不是逐页精读完整 PDF**。下面会明确区分：**作者声称 / 实验观察 / 我的判断**。

## 一句话判断

这篇值得读，不是因为它又做了一个更强的 deep research agent，而是因为它把一个真实部署里非常致命、但经常被忽略的问题量化了：

> **模型给你的引用链接，到底是真的存在，还是只是“看起来像真的”？**

**我的判断**：这篇的价值很实。它既不是泛泛谈“citation quality”，也不是只做个小样本案例，而是把 **URL 是否存在** 这个更基础的问题拉成了可测量、可分解、可修正的系统问题。

---

## 它到底在研究什么

现在主流 LLM 和 deep research agent 都会给出引用链接，用户天然会把这些链接当成“证据”。

但这件事至少有三种不同失败方式：

- 链接打不开；
- 链接以前存在、现在失效；
- 链接压根从来没存在过，只是模型编出来的。

这篇论文专门研究第三类和第二类之间的区别。

作者把问题拆成 6 个研究问题：

1. 引用 URL 失效率到底有多高？
2. deep research agent 和 search-augmented LLM 谁更容易出错？
3. 不同学科领域差异大不大？
4. 失败里有多少是 fabrication，多少只是 link rot？
5. 给更多 citations 会不会提高单条 citation 的可靠性？
6. 能不能靠后处理 verification 把问题压下去？

这其实抓得很准。因为很多人一看到“模型给了很多引用”，就会误以为可验证性更强；而这篇恰恰在问：**量变是不是反而带来更多假链接。**

---

## 核心定义：它怎么区分不同错误

这是这篇最关键的地方之一。

作者把 URL 先分成：

### 1. Non-resolving URL

即链接无法正常解析，典型表现是：

- 4xx / 5xx
- 连接失败
- timeout

这是最宽的坏链接集合。

### 2. Hallucinated URL

这是 non-resolving URL 的子集。

定义是：

> 当前打不开，而且在 Wayback Machine 里也查不到任何历史快照。

作者把它视为“很可能从未存在过”的链接。

### 3. Stale URL

也是 non-resolving URL 的子集。

定义是：

> 现在打不开，但在 Wayback Machine 里能查到它以前存在过。

也就是链接腐烂，不是凭空捏造。

论文还给出一个很直接的关系：

> **Hallucinated URLs = Non-resolving URLs − Stale URLs**

**我的判断**：这个区分非常重要。因为这两类问题的产品修法完全不同：

- hallucinated URL 说明生成或 grounding 链路有问题；
- stale URL 更像索引陈旧、网页自然失效、或抓取 freshness 不够。

如果你把它们混在一起，只会得到一个模糊的“citation quality 不够好”。

---

## 实验怎么做的

### 数据集

作者用了两个数据源：

#### DRBench

- 100 个中英文 research queries
- 来自 finance / science / technology
- 用来做 **跨模型比较**
- 总计分析 **53,090 个 URL**

#### ExpertQA

- 2,177 个专家问题
- 覆盖 **32 个学科领域**
- 用来做 **领域分层分析**
- 总计分析 **168,021 个 URL**

这两个数据集配合得挺合理：

- DRBench 更适合横向看不同模型/agent；
- ExpertQA 更适合看领域差异和规模效应。

### 模型

DRBench 里他们最终分析了 10 个系统，来自 Google / OpenAI / Anthropic，包括两类：

- **deep research agents**：如 gemini-2.5-pro-deepresearch、openai-deepresearch
- **search-augmented LLMs**：如 gpt-4o-search-preview、claude-with-search、gemini-with-search 等

ExpertQA 上则评测了 3 个 search-augmented 模型：

- claude-sonnet-4-5
- gemini-2.5-pro
- gpt-5.1

### 检测流程

作者的 URL pipeline 很朴素，但足够扎实：

1. 从模型输出里抽取 URL
2. 先做 HTTP HEAD 检查
3. 某些情形下 fallback 到 GET
4. 对非正常解析 URL，再去查 Wayback Machine
5. 有历史快照 → stale；无历史快照 → hallucinated

他们还单独讨论了 403、bot-blocking、UNKNOWN response 这些边界情况，没有直接全算死链。

**我的判断**：这套管线不花哨，但比“简单抓一下 404”严谨很多，尤其是把 Wayback Machine 拉进来以后，至少能把“从未存在”与“曾经存在但现在挂了”分开。

---

## 关键结果一：坏链接问题是真实且不小的

这是全文最核心的 headline。

### 在 DRBench 上

作者报告：

- **non-resolving URL rate：5%–18%**
- **hallucinated URL rate：3%–13%**

其中最高的一个是：

- **gemini-2.5-pro-deepresearch**：hallucinated URL rate **13.3%**

也就是说，某些系统给出的每 100 条 citation URL 里，大概有 13 条很可能从来没存在过。

### 在 ExpertQA 上

整体 non-resolving URL rate 是：

- **8.22%**

按模型看：

- **gpt-5.1**：8.47%
- **claude-sonnet-4-5**：9.38%
- **gemini-2.5-pro**：4.20%

**实验观察**：即便在带搜索/检索增强的系统里，URL 不可靠问题也没有消失，只是程度不同。

**我的判断**：这点很值得重视。很多人默认“只要接了搜索，引用就靠谱很多”，但这篇说明事实并非如此。检索增强可以减少一部分自由发挥，但**不能自动消灭 URL fabrication**。

---

## 关键结果二：deep research agent 给的引用更多，但错得也更多

作者特别对比了两类系统：

- deep research agents
- search-augmented LLMs

结论很直接：

### 引用数量

deep research agents 的 citation 数远高于普通 search-augmented LLM。

例如：

- gemini-2.5-pro-deepresearch：**113.1 URLs/query**
- openai-deepresearch：**41.2 URLs/query**
- search-augmented models：约 **3.0–24.3 URLs/query**

### 但 hallucination rate 更高

聚合后：

- **deep research agents hallucination rate：10.7%**
- **search-augmented LLMs hallucination rate：4.8%**

non-resolving rate 也一样：

- deep research agents：**16.2%**
- search-augmented：**6.8%**

**作者声称**：multi-step retrieval + synthesis 可能会放大错误，把不同页面的 URL pattern 混在一起，生成“看起来合理但不存在”的地址。

**我的判断**：这个解释很 plausible。deep research agent 的工作流更长、更复杂，也更有机会把“检索到的信息片段”与“模型自己脑补的链接格式”糅在一起。它的可读报告更像成品，但并不自动代表证据链更干净。

---

## 关键结果三：不同领域差异很大

在 ExpertQA 的 32 个学科里，作者发现领域差异很明显。

总体 non-resolving rate 从：

- **Business：5.4%**
- 到 **Theology：11.4%**

大约差 **2 倍**。

更细一点看，某些模型在不同领域的波动更夸张。比如 Claude Sonnet 4.5：

- Mathematics：**4.0%**
- Healthcare/Medicine：**17.4%**

接近 **4.3 倍差异**。

**实验观察**：医疗、神学、古典研究这类内容更容易出现坏链接；商业、建筑、新闻这类内容更稳定。

**我的判断**：这很合理。网页生态本来就不均匀：

- 有些领域内容更碎、更旧、更封闭；
- 有些领域链接更新快、站点迁移多、paywall 多；
- 有些领域则长期挂在比较稳定的大站上。

这意味着 citation verification 不能只看“模型平均表现”，还得看**你实际部署在哪个领域**。医疗场景下 17% 级别的坏引用，是不能靠“平均还行”来安慰自己的。

---

## 关键结果四：有些模型的坏链接几乎全是编的

这是我觉得最扎眼的发现之一。

作者发现，某些 OpenAI search-augmented 模型里：

> **non-resolving rate = hallucinated rate**

也就是说，所有打不开的链接都没有 Wayback 历史快照；换句话说：

> **一旦错，就是纯 fabrication，不是 link rot。**

相反，另一些模型（比如 openai-deepresearch、Claude、Gemini deep research）会表现出明显的 stale fraction，说明它们的坏链接里至少有一部分是真的抓到过真实网页，只是后来失效。

**我的判断**：这个结果很有诊断价值。因为它暗示不同系统的失败机制并不一样：

- 有的系统像是在“生成 URL”；
- 有的系统像是在“真的检索到了网页，但索引或网页本身过期”。

这两类系统后续该修哪里，完全不同。

---

## 关键结果五：引用更多，不代表每条更可靠

很多人会天然觉得：

- 给的 citations 多，说明查得更充分；
- 查得更充分，每条 citation 应该更可靠。

这篇直接反驳了这个直觉。

作者发现：

- **gpt-5.1** 平均每题 **46.4 URLs**，但 non-resolving rate **8.5%**
- **gemini-2.5-pro** 平均每题 **10.7 URLs**，但 non-resolving rate **4.2%**

也就是说，citation 数量增加，并没有自动提升 per-citation quality。

deep research 里这个现象更明显：

- URL 产出最多的 gemini-2.5-pro-deepresearch，恰好也是 hallucination 率最高的一个。

**我的判断**：这对产品很重要。很多 agent 系统喜欢把“更长报告 + 更多引用”包装成能力增强，但这篇提醒你：

> **引用数量不是质量代理变量。**

如果没有 verification，这甚至可能只是“更大规模地产出潜在垃圾链接”。

---

## 解决方案：urlhealth

论文不是只做现象描述，还做了一个 mitigation tool：**urlhealth**。

它是一个很轻量的工具，输入一个 URL，输出四类结果：

- **LIVE**：HTTP 200
- **DEAD**：404 且有 Wayback 记录，对应 stale URL
- **LIKELY_HALLUCINATED**：404 且没 Wayback 记录
- **UNKNOWN**：其他模糊状态，需要人工进一步看

作者说实现只有 **83 行 Python**，同时提供 pip package 和 agent tool 形式。

**我的判断**：这类工具看上去不“酷”，但恰恰是最可能被直接接进产品链路的东西。相比再训一个 judge model，这种后处理组件更容易上线。

---

## 自我修正实验：后处理真的能把问题压下去

这是全文第二个最有价值的部分。

作者做了 agentic self-correction 实验：

- 让模型先正常回答并给引用；
- 再让模型调用 urlhealth 检查这些 URL；
- 然后迭代修正。

在 435 个 ExpertQA 样本上，他们报告：

- **GPT-5.1**：non-resolving rate 从 **16.0% → 0.6%**，约 **26×** 改善
- **Gemini 2.5 Pro**：**6.1% → 0.1%**，约 **79×** 改善
- **Claude Sonnet 4.5**：**4.9% → 0.8%**，约 **6.4×** 改善

最终都把 non-resolving URL 压到了 **1% 以下**。

### 但 tool access ≠ tool competence

作者还补了一个很关键的观察：

- 小模型 **gpt-5-nano** 虽然能调用工具，
- 但它常常**不会真的根据工具结果修正**，甚至会反复重新提出已经被标红的坏 URL。

所以作者结论是：

> 工具可用，不等于模型会正确用工具。

**我的判断**：这点很重要，而且很像真实 agent 系统会踩的坑。大家容易把“接入工具”理解成“系统问题已解决”，但实际上：

- 模型要会读工具输出；
- 要会根据结果重写答案；
- 要避免 stubborn repetition。

否则 verification 只会变成摆设。

---

## 这篇论文真正贡献了什么

### 1. 它把“citation existence”从附属问题提升成主问题

以前很多工作只问：

- citation 是否支持 claim？
- 引文是不是 semantic match？

这篇先问一个更底层的问题：

> **这个 source 先得存在。**

这个顺序是对的。不存在的源，根本没资格进入后续 attribution 讨论。

### 2. 它把 failure taxonomy 做实了

不是所有坏引用都一样：

- fabricated
- stale
- blocked/unknown

分清之后，后面的产品动作和研究动作才会对。

### 3. 它给了一个真能落地的 mitigation

不是泛泛建议“加强 grounding”，而是给了一个简单、外插性强、对现有系统侵入小的验证工具。

**我的判断**：很多论文的问题分析不错，但落到工程上没抓手；这篇相对少见，确实给了一个可以马上接到后处理链路里的东西。

---

## 它的局限和该追问的地方

这篇不错，但也有几个边界要看清。

### 1. Hallucinated 的定义仍然是 operational definition

作者自己也承认：

- Wayback Machine 覆盖不完整；
- 没有快照，不等于 100% 从未存在过。

所以“hallucinated”其实更严格说是：

> **没有历史存在证据的 non-resolving URL**

而不是数学上绝对证明的“从未存在”。

### 2. 它主要验证的是 URL existence，不是 evidence correctness

一个 URL 可能：

- 存在；
- 甚至是 live；
- 但并不支持模型写下的 claim。

这篇没有试图一次性解决所有 citation failure mode。它解决的是**更前置的 existence problem**。

### 3. deep research failure 机制仍然主要是推测

作者提出 multi-step synthesis 可能放大 fabrication，但因为拿不到商业系统内部检索链路，他们没法真正验证内部机制。

所以这里更像合理推断，而不是机制层实锤。

### 4. UNKNOWN 仍然不小

bot-blocking、paywall、奇怪响应这些现实网页问题，会让自动 verification 遇到上限。

作者虽然做了 headless-browser audit，但这依然说明：

> 全自动 URL verification 在现实互联网里有天花板。

---

## 如果你在做 agent / RAG / deep research，最该拿走什么

我觉得可以直接拿走 4 点：

### 1. 不要把“有 citation”当成“可验证”

模型能吐链接，不代表这些链接真的存在。

### 2. Citation pipeline 里要显式区分 stale vs hallucinated

因为二者的系统根因不同。

### 3. 把 URL verification 接到 generation 后处理里

这篇最强的产品启发，不是新架构，而是：

> **先生成，再验证，再修正。**

这是非常现实的系统改造路径。

### 4. 评估 deep research agent 时，citation quantity 不能代替 citation quality

报告更长、引用更多，甚至可能只是让错误规模一起变大。

---

## 作者声称 vs 我的判断

### 作者声称

作者的核心主张大致是：

1. 商业 LLM 与 deep research agent 的 citation URL 问题可以被系统测量；
2. hallucinated URL 在现实系统里并不少见；
3. deep research agent 不一定比普通 search-augmented LLM 更可靠；
4. urlhealth 这类后处理工具可以把问题大幅压下去。

### 我的判断

我基本认同，而且我觉得这篇最有价值的不是 headline 数字，而是它把一个常被混成“citation quality 不好”的问题拆开了：

- **存在性**
- **时效性**
- **归因正确性**

这篇先把第一层打实，已经很有价值。

如果你在做：

- deep research agent
- 报告生成 agent
- 医疗/法律/学术类 RAG
- 任何会把 URL 当证据给用户看的系统

这篇都应该列入高优先级阅读。

---

## 最后结论

### 值不值得读？

**值得。**

### 为什么值得？

因为它研究的不是“怎样让 agent 看起来更会研究”，而是：

> **怎样避免 agent 把根本不存在的证据递给用户。**

这比再多一层规划、更长一份报告、更花哨的 multi-agent 协作都更接近“系统真的能不能用”。

### 我会怎么用这篇

如果我要把它转成工程动作，我会直接做三件事：

1. 在引用输出后接一个 URL liveness / Wayback check；
2. 把 citation failure 拆成 stale / hallucinated / unknown 三类监控；
3. 在最终回答前增加一轮基于 verification 结果的自我修正。

**一句话总结**：这篇不是最炫的 agent paper，但很可能是最近最接近真实产品可靠性的一篇。