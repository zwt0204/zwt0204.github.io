#!/usr/bin/env python3
"""Fetch recent arXiv papers and publish a Chinese reading report."""

from __future__ import annotations

import html
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "_posts" / "paper"
DATA_PATH = ROOT / "docs" / "arxiv-papers.json"
ARXIV_API = "https://export.arxiv.org/api/query"
AR5IV_HTML = "https://ar5iv.labs.arxiv.org/html/{arxiv_id}"
USER_AGENT = "zwt0204.github.io arxiv paper learner bot"
LOCAL_TZ = ZoneInfo("Asia/Shanghai")
MAX_RESULTS = 60
MAX_TABLE_PAPERS = 25

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

SEARCH_QUERY = """
(
  all:"large language model"
  OR all:LLM
  OR all:"foundation model"
  OR all:"vision language model"
  OR all:"vision-language"
  OR all:multimodal
  OR all:"multi-modal"
  OR all:"AI agent"
  OR all:"language agent"
  OR all:"autonomous agent"
  OR all:"multi-agent"
  OR all:"tool use"
  OR all:"tool learning"
  OR all:"function calling"
  OR all:skill
  OR all:skills
  OR all:RAG
  OR all:"retrieval augmented generation"
  OR all:"long context"
  OR all:"agentic"
)
AND
(
  cat:cs.CL
  OR cat:cs.AI
  OR cat:cs.CV
  OR cat:cs.LG
  OR cat:cs.HC
  OR cat:stat.ML
)
"""


@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    authors: tuple[str, ...]
    abs_url: str
    pdf_url: str
    published: str
    updated: str
    primary_category: str
    categories: tuple[str, ...]
    comment: str = ""


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:90].strip("-") or "arxiv-paper"


def markdown_escape(value: str) -> str:
    return normalize_text(value).replace("|", "\\|")


def yaml_escape(value: str) -> str:
    return normalize_text(value).replace("\\", "\\\\").replace('"', '\\"')


def get_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and 400 <= exc.code < 500:
                raise
            time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def fetch_papers() -> list[Paper]:
    query = " ".join(line.strip() for line in SEARCH_QUERY.splitlines() if line.strip())
    url = ARXIV_API + "?" + urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": MAX_RESULTS,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    root = ET.fromstring(get_url(url))
    papers: list[Paper] = []
    seen: set[str] = set()

    for entry in root.findall("atom:entry", ATOM_NS):
        abs_url = text_of(entry, "atom:id")
        arxiv_id = parse_arxiv_id(abs_url)
        if not arxiv_id or arxiv_id in seen:
            continue
        seen.add(arxiv_id)

        links = entry.findall("atom:link", ATOM_NS)
        pdf_url = ""
        for link in links:
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break
        if not pdf_url:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        authors = tuple(
            normalize_text(author.findtext("atom:name", default="", namespaces=ATOM_NS))
            for author in entry.findall("atom:author", ATOM_NS)
        )
        categories = tuple(
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", ATOM_NS)
            if category.attrib.get("term")
        )
        primary = entry.find("arxiv:primary_category", ATOM_NS)

        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=normalize_text(text_of(entry, "atom:title")),
                abstract=normalize_text(text_of(entry, "atom:summary")),
                authors=tuple(author for author in authors if author),
                abs_url=abs_url,
                pdf_url=pdf_url,
                published=text_of(entry, "atom:published"),
                updated=text_of(entry, "atom:updated"),
                primary_category=primary.attrib.get("term", "") if primary is not None else "",
                categories=categories,
                comment=normalize_text(text_of(entry, "arxiv:comment")),
            )
        )

    return papers


class OutlineParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[str] = []
        self._capture = False
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h1", "h2", "h3"}:
            self._capture = True
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag in {"h1", "h2", "h3"}:
            heading = normalize_text(" ".join(self._text))
            if heading and len(heading) < 180 and heading not in self.headings:
                self.headings.append(heading)
            self._capture = False
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._text.append(data)


def fetch_paper_outline(paper: Paper) -> tuple[str, ...]:
    url = AR5IV_HTML.format(arxiv_id=paper.arxiv_id)
    try:
        parser = OutlineParser()
        parser.feed(get_url(url))
        return tuple(parser.headings[:12])
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        print(f"warning: failed to fetch ar5iv outline for {paper.arxiv_id}: {exc}", file=sys.stderr)
        return ()


def text_of(node: ET.Element, path: str) -> str:
    return node.findtext(path, default="", namespaces=ATOM_NS)


def parse_arxiv_id(abs_url: str) -> str:
    match = re.search(r"arxiv\.org/abs/([^/]+)$", abs_url)
    if not match:
        return ""
    return re.sub(r"v\d+$", "", match.group(1))


def paper_score(paper: Paper) -> tuple[int, list[str]]:
    topic_score = 0
    reasons: list[str] = []
    text = f"{paper.title} {paper.abstract} {paper.comment}".lower()
    categories = set(paper.categories)

    signals = (
        (("large language model", "llm", "foundation model", "language model"), "大模型核心方向", 3),
        (("multimodal", "multi-modal", "vision-language", "vision language", "vlm", "image", "video", "audio"), "多模态/视觉语言模型", 3),
        (("agent", "agents", "agentic", "autonomous agent", "multi-agent", "planning"), "Agent 与长程任务", 4),
        (("tool use", "tool-use", "tool learning", "function calling", "api calling", "skill", "skills"), "工具使用/技能学习", 3),
        (("rag", "retrieval augmented", "retrieval-augmented", "memory", "long context", "context compression"), "RAG、记忆或长上下文", 3),
        (("reasoning", "math", "code", "programming", "swe-bench", "debugging"), "推理、代码或复杂任务", 2),
        (("benchmark", "dataset", "evaluation", "eval", "leaderboard"), "评测基准或数据集", 2),
        (("alignment", "safety", "hallucination", "robustness", "privacy", "security"), "安全、对齐或鲁棒性", 2),
        (("reinforcement learning", "rlhf", "grpo", "dpo", "post-training", "distillation", "fine-tuning"), "训练/后训练方法", 2),
        (("inference", "serving", "efficiency", "quantization", "compression", "moe"), "推理效率或系统优化", 1),
    )

    for keys, reason, weight in signals:
        if any(has_phrase(text, key) for key in keys):
            topic_score += weight
            reasons.append(reason)

    score = min(topic_score, 12)
    if {"cs.CL", "cs.AI", "cs.LG"} & categories:
        score += 1
        reasons.append("类别与 LLM/Agent 高相关")
    if "cs.CV" in categories and any(has_phrase(text, key) for key in ("multimodal", "vision", "video", "image")):
        score += 1
        reasons.append("视觉/多模态类别匹配")
    if any(phrase in text for phrase in ("we introduce", "we propose", "we present", "we develop")):
        score += 2
        reasons.append("方法贡献明确")
    if any(phrase in text for phrase in ("we release", "open-source", "open source", "code is available", "dataset is available")):
        score += 2
        reasons.append("可能有代码或数据可复现")
    if any(phrase in text for phrase in ("outperform", "state-of-the-art", "significant", "ablation", "experiments show")):
        score += 1
        reasons.append("摘要中有实验或对比信号")

    return min(score, 20), dedupe(reasons)


def has_phrase(text: str, phrase: str) -> bool:
    if re.search(r"[^a-z0-9]", phrase):
        return phrase in text
    return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text) is not None


def dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def first_sentences(text: str, limit: int = 2) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    value = " ".join(part for part in parts[:limit] if part)
    if len(value) > 520:
        return value[:517].rstrip() + "..."
    return value


def authors_text(paper: Paper, limit: int = 6) -> str:
    if not paper.authors:
        return "未知"
    shown = list(paper.authors[:limit])
    if len(paper.authors) > limit:
        shown.append("等")
    return "、".join(shown)


def date_only(value: str) -> str:
    return value[:10] if value else ""


def topic_tags(paper: Paper) -> list[str]:
    text = f"{paper.title} {paper.abstract}".lower()
    tags: list[str] = []
    mapping = (
        ("LLM", ("llm", "large language model", "language model", "foundation model")),
        ("多模态", ("multimodal", "multi-modal", "vision-language", "vision language", "vlm", "image", "video")),
        ("Agent", ("agent", "agentic", "multi-agent", "autonomous")),
        ("Skill/Tool", ("skill", "tool use", "tool-use", "tool learning", "function calling")),
        ("RAG/Memory", ("rag", "retrieval augmented", "memory", "long context")),
        ("Reasoning", ("reasoning", "math", "code", "planning")),
        ("Safety/Eval", ("safety", "alignment", "benchmark", "evaluation", "hallucination", "robustness")),
    )
    for tag, keys in mapping:
        if any(key in text for key in keys):
            tags.append(tag)
    return tags or ["AI"]


def method_guess(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "agent" in text or "tool" in text or "skill" in text:
        return "这篇更像 agent 能力构建工作，阅读重点应放在动作空间、工具接口、任务分解、反馈信号和失败恢复。"
    if "multimodal" in text or "vision" in text or "video" in text or "image" in text:
        return "这篇更像多模态建模工作，阅读重点应放在模态对齐、数据配比、视觉编码器/语言模型连接方式和推理链路。"
    if "retrieval" in text or "memory" in text or "long context" in text:
        return "这篇更像知识增强或记忆系统工作，阅读重点应放在检索粒度、上下文压缩、状态更新和噪声控制。"
    if "benchmark" in text or "dataset" in text or "evaluation" in text:
        return "这篇更像评测/数据集型工作，阅读重点应放在任务定义、数据构造、评价指标和 baseline 是否合理。"
    if "training" in text or "post-training" in text or "reinforcement learning" in text:
        return "这篇更像训练方法工作，阅读重点应放在目标函数、数据来源、训练稳定性、消融实验和泛化边界。"
    return "这篇需要先确认问题定义，再顺着方法模块、实验设置和失败案例判断真实价值。"


def contribution_lens(paper: Paper) -> tuple[str, str, str, str]:
    text = f"{paper.title} {paper.abstract}".lower()
    if "agent" in text or "tool" in text or "skill" in text:
        problem_lens = "把它当成一篇 agent 系统论文来读：核心不是模型会不会回答，而是长程任务里状态、工具、反馈和失败恢复如何被组织。"
        method_lens = "方法部分重点找三件事：任务如何分解，动作/工具空间如何定义，执行后的 observation 如何影响下一步决策。"
        experiment_lens = "实验部分不要只看平均分，要看任务长度、失败类型、baseline 是否公平，以及是否有 trace 级别的错误分析。"
        limitation_lens = "如果论文没有讲权限边界、状态漂移、工具调用错误和成本控制，那工程落地价值要打折。"
    elif "multimodal" in text or "vision" in text or "video" in text or "image" in text or "audio" in text:
        problem_lens = "把它当成一篇多模态系统论文来读：关键是它解决了感知、对齐、长上下文或推理链路里的哪一个瓶颈。"
        method_lens = "方法部分重点看模态表示如何进入语言模型，是否引入检索/记忆/压缩模块，以及训练和推理阶段是否一致。"
        experiment_lens = "实验部分要看数据集是否覆盖真实复杂场景，指标是否能反映推理质量，而不只是某个 benchmark 的选择题准确率。"
        limitation_lens = "如果收益依赖特定数据集、特定 backbone 或昂贵 token budget，就需要谨慎判断可迁移性。"
    elif "retrieval" in text or "memory" in text or "long context" in text:
        problem_lens = "把它当成一篇记忆/长上下文论文来读：核心是信息如何被选择、压缩、更新，并在噪声下保持可用。"
        method_lens = "方法部分重点看记忆粒度、写入策略、检索策略、上下文预算和过期信息处理。"
        experiment_lens = "实验部分要看长程依赖、干扰信息、时间跨度和消融实验，而不是只看短上下文任务上的提升。"
        limitation_lens = "如果没有噪声、遗忘、过期信息或成本分析，说明它还没完全回答真实系统问题。"
    elif "benchmark" in text or "dataset" in text or "evaluation" in text:
        problem_lens = "把它当成一篇评测论文来读：最重要的是任务定义是否真实，指标是否能逼出模型的关键短板。"
        method_lens = "方法部分重点看数据构造、标注流程、过滤规则、评测协议和 baseline 选择。"
        experiment_lens = "实验部分要看不同模型族、不同设置和失败案例，而不只是排行榜排序。"
        limitation_lens = "如果任务可以被模板、数据泄漏或 judge 偏差轻易利用，评测价值就有限。"
    else:
        problem_lens = "先把它当成一篇方法论文来读：确认它到底提出了新问题、新算法、新系统，还是对已有路线做工程组合。"
        method_lens = "方法部分重点找最小核心贡献：哪一个模块是必要的，哪一个只是包装，哪些假设决定了方法边界。"
        experiment_lens = "实验部分重点看主表、消融、失败案例和泛化设置，判断结论是否被充分支撑。"
        limitation_lens = "如果论文只给结果、不解释失败模式或适用边界，就不适合作为今天的深读样本。"
    return problem_lens, method_lens, experiment_lens, limitation_lens


def questions_for(paper: Paper) -> list[str]:
    tags = set(topic_tags(paper))
    questions = [
        "论文解决的是新问题，还是对已有问题换了一个实验设置？",
        "核心结论是否依赖特定模型、数据集或 prompt 模板？",
    ]
    if "Agent" in tags or "Skill/Tool" in tags:
        questions.append("如果放到更长任务链路里，工具调用错误、状态漂移和权限边界如何处理？")
    elif "多模态" in tags:
        questions.append("跨模态对齐收益来自模型结构、训练数据，还是评测集偏好？")
    elif "RAG/Memory" in tags:
        questions.append("检索/记忆模块在噪声、过期信息和长上下文压力下是否仍然稳定？")
    elif "Safety/Eval" in tags:
        questions.append("评测指标能否解释真实使用风险，还是只覆盖了可测的表层行为？")
    else:
        questions.append("论文有没有足够消融证明每个模块确实必要？")
    return questions


def build_deep_paper_section(paper: Paper, alternatives: list[Paper], outline: tuple[str, ...] = ()) -> str:
    score, reasons = paper_score(paper)
    reasons_text = "、".join(reasons) if reasons else "主题相关，但需要进一步检查方法和实验扎实程度"
    tags = "、".join(topic_tags(paper))
    categories = "、".join(paper.categories) if paper.categories else paper.primary_category or "未标注"
    questions = "\n".join(f"- {question}" for question in questions_for(paper))
    problem_lens, method_lens, experiment_lens, limitation_lens = contribution_lens(paper)
    alternative_rows = "\n".join(
        f"- [{markdown_escape(item.title)}]({item.abs_url})：评分 {paper_score(item)[0]}/20，{', '.join(topic_tags(item))}"
        for item in alternatives[:5]
    )
    outline_text = "\n".join(f"- {markdown_escape(heading)}" for heading in outline[:10])

    return f"""## 今日只读这篇：[{markdown_escape(paper.title)}]({paper.abs_url})

- arXiv：[{paper.arxiv_id}]({paper.abs_url})
- PDF：[{paper.pdf_url}]({paper.pdf_url})
- 作者：{markdown_escape(authors_text(paper))}
- 发布时间：{date_only(paper.published)}，更新时间：{date_only(paper.updated)}
- 类别：{categories}
- 主题标签：{tags}
- 阅读价值评分：{score}/20

### 摘要速读

{markdown_escape(first_sentences(paper.abstract))}

### 为什么今天选它

{reasons_text}。今天的目标不是把候选论文都过一遍，而是挑一篇最值得投入精力的论文，把它读到能回答“问题是什么、方法凭什么有效、实验是否支撑结论、工程上能带走什么”。

### 先抓住问题定义

{problem_lens}

从摘要看，这篇论文最应该先确认的不是具体指标，而是它把问题边界划在哪里：输入是什么，输出是什么，系统/模型在什么约束下工作，和已有路线相比到底难在哪里。

### 全文结构线索

{outline_text if outline_text else "没有从 ar5iv 抓到可靠章节结构，因此这次先基于 arXiv 元数据和摘要做精读入口判断。正式阅读时仍应打开 PDF 核对 introduction、method、experiment 和 limitation。"}

### 方法部分怎么读

{method_lens}

阅读时建议把方法拆成三层：

1. **核心假设**：作者相信哪个瓶颈最重要，这个假设是否合理。
2. **关键机制**：真正带来收益的是模型结构、数据构造、检索/记忆、训练目标，还是推理流程。
3. **工程代价**：额外 token、额外模型调用、额外标注、额外存储或延迟是否可接受。

### 实验部分怎么判断

{experiment_lens}

至少要检查四块：主结果是否稳定，消融是否能证明关键模块必要，失败案例是否诚实，结论是否跨模型或跨数据集成立。

### 局限和追问

{limitation_lens}

精读时重点追问：

{questions}

### 可以带走的东西

如果论文读完之后只能沉淀一页笔记，建议记这三类内容：问题定义的抽象方式、核心机制为什么可能有效、实验设计里哪些指标或失败分析可以复用到自己的项目中。

### 其它候选为什么先不展开

{alternative_rows if alternative_rows else "- 今天没有足够多的其它候选。"}
"""


def write_report(papers: list[Paper]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    path = POST_DIR / f"{date}-arxiv-llm-agent-papers.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    ranked = sorted(papers, key=lambda paper: paper_score(paper)[0], reverse=True)
    pick = ranked[0]
    outline = fetch_paper_outline(pick)
    top_section = build_deep_paper_section(pick, ranked[1:], outline)
    table_rows = "\n".join(
        f"| [{markdown_escape(paper.title)}]({paper.abs_url}) | {', '.join(topic_tags(paper))} | {paper_score(paper)[0]} | {date_only(paper.published)} | {markdown_escape(first_sentences(paper.abstract, 1))} |"
        for paper in ranked[:MAX_TABLE_PAPERS]
    )

    content = f"""---
layout: post
title: "arXiv 论文精读：{yaml_escape(pick.title)} ({date})"
subtitle: "每天只选一篇论文深读"
date: {date} 10:30:00 +0800
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
{{:toc}}

# 0. 说明

数据来源：[arXiv API]({ARXIV_API})。本篇自动检索近期与 LLM、多模态、Agent、工具使用、Skill、RAG、长上下文和模型评测相关的论文，但正文只选一篇深读；其它论文只保留在候选表里。

筛选不是简单看标题热词，而是优先考虑：

1. 是否切中 LLM / multimodal / agent 方向的关键问题；
2. 是否有清晰的方法贡献、评测基准或系统实现；
3. 是否能给实际工程带来可迁移经验；
4. 是否值得进一步精读 introduction、method、experiment 和 limitation。

# 1. 今日最值得读的论文

{top_section}

# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
{table_rows if table_rows else "| - | - | - | - | - |"}

# 3. 阅读建议

今天只建议先读正文选中的这一篇。候选表的作用是校准选择，而不是制造阅读负担；如果主选论文读完发现问题定义不成立，再从候选表里换下一篇。

生成时间：{now.strftime("%Y-%m-%d %H:%M:%S %Z")}
"""
    path.write_text(content, encoding="utf-8")
    return path


def write_data(papers: list[Paper]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    ranked = sorted(papers, key=lambda paper: paper_score(paper)[0], reverse=True)
    DATA_PATH.write_text(
        json.dumps(
            [
                {
                    "arxiv_id": paper.arxiv_id,
                    "title": paper.title,
                    "authors": list(paper.authors),
                    "abs_url": paper.abs_url,
                    "pdf_url": paper.pdf_url,
                    "published": paper.published,
                    "updated": paper.updated,
                    "primary_category": paper.primary_category,
                    "categories": list(paper.categories),
                    "comment": paper.comment,
                    "topics": topic_tags(paper),
                    "score": paper_score(paper)[0],
                    "reasons": paper_score(paper)[1],
                    "abstract": paper.abstract,
                }
                for paper in ranked
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    papers = fetch_papers()
    if not papers:
        print("error: no papers parsed from arXiv", file=sys.stderr)
        return 1

    report_path = write_report(papers)
    write_data(papers)
    print(f"wrote {report_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
