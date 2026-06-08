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
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "_posts" / "paper"
DATA_PATH = ROOT / "docs" / "arxiv-papers.json"
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "zwt0204.github.io arxiv paper learner bot"
LOCAL_TZ = ZoneInfo("Asia/Shanghai")
MAX_RESULTS = 60
MAX_REPORT_PAPERS = 6
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


def build_paper_section(paper: Paper) -> str:
    score, reasons = paper_score(paper)
    reasons_text = "、".join(reasons) if reasons else "主题相关，但需要进一步检查方法和实验扎实程度"
    tags = "、".join(topic_tags(paper))
    categories = "、".join(paper.categories) if paper.categories else paper.primary_category or "未标注"
    questions = "\n".join(f"- {question}" for question in questions_for(paper))

    return f"""## [{markdown_escape(paper.title)}]({paper.abs_url})

- arXiv：[{paper.arxiv_id}]({paper.abs_url})
- PDF：[{paper.pdf_url}]({paper.pdf_url})
- 作者：{markdown_escape(authors_text(paper))}
- 发布时间：{date_only(paper.published)}，更新时间：{date_only(paper.updated)}
- 类别：{categories}
- 主题标签：{tags}
- 阅读价值评分：{score}/20

### 摘要速读

{markdown_escape(first_sentences(paper.abstract))}

### 为什么值得读

{reasons_text}。如果时间有限，建议先看 introduction 的问题定义，再看方法图和实验主表，最后检查限制条件与失败案例。

### 方法与贡献线索

{method_guess(paper)}

### 精读时重点追问

{questions}
"""


def write_report(papers: list[Paper]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    path = POST_DIR / f"{date}-arxiv-llm-agent-papers.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    ranked = sorted(papers, key=lambda paper: paper_score(paper)[0], reverse=True)
    top = ranked[:MAX_REPORT_PAPERS]
    top_sections = "\n".join(build_paper_section(paper) for paper in top)
    table_rows = "\n".join(
        f"| [{markdown_escape(paper.title)}]({paper.abs_url}) | {', '.join(topic_tags(paper))} | {paper_score(paper)[0]} | {date_only(paper.published)} | {markdown_escape(first_sentences(paper.abstract, 1))} |"
        for paper in ranked[:MAX_TABLE_PAPERS]
    )

    content = f"""---
layout: post
title: "arXiv 论文学习日报：LLM、多模态与 Agent ({date})"
subtitle: "自动筛选值得精读的新论文"
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

数据来源：[arXiv API]({ARXIV_API})。本篇自动检索近期与 LLM、多模态、Agent、工具使用、Skill、RAG、长上下文和模型评测相关的论文，并按研究价值、工程启发和可复现线索进行排序。

筛选不是简单看标题热词，而是优先考虑：

1. 是否切中 LLM / multimodal / agent 方向的关键问题；
2. 是否有清晰的方法贡献、评测基准或系统实现；
3. 是否能给实际工程带来可迁移经验；
4. 是否值得进一步精读 introduction、method、experiment 和 limitation。

# 1. 今日最值得读的论文

{top_sections if top_sections else "今天没有抓取到足够相关的论文。"}

# 2. 候选论文列表

| 论文 | 主题 | 评分 | 发布时间 | 摘要一句话 |
| --- | --- | ---: | --- | --- |
{table_rows if table_rows else "| - | - | - | - | - |"}

# 3. 阅读建议

建议先读评分最高的 3 篇。对 agent / skill 类论文，重点看任务设定是否真实、工具调用是否可控、状态管理是否清楚；对多模态论文，重点看数据配比、模态对齐和评测是否覆盖真实使用场景；对 RAG / memory 论文，重点看检索粒度、噪声控制、时效性和长上下文成本。

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
