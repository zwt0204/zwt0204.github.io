#!/usr/bin/env python3
"""Fetch recent arXiv papers and publish a Chinese reading report."""

from __future__ import annotations

import html
import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date as Date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "_posts" / "paper"
DATA_PATH = ROOT / "docs" / "arxiv-papers.json"
ASSET_DIR = ROOT / "img" / "daily-reports"
ARXIV_API = "https://export.arxiv.org/api/query"
AR5IV_HTML = "https://ar5iv.labs.arxiv.org/html/{arxiv_id}"
USER_AGENT = "zwt0204.github.io arxiv paper learner bot"
LOCAL_TZ = ZoneInfo("Asia/Shanghai")
MAX_RESULTS = 60

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


def svg_escape(value: str) -> str:
    return html.escape(normalize_text(value), quote=True)


def extract_urls(value: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\]]+", value or "")


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


def fetch_papers_by_ids(arxiv_ids: list[str]) -> list[Paper]:
    if not arxiv_ids:
        return []
    url = ARXIV_API + "?" + urlencode({"id_list": ",".join(arxiv_ids)})
    root = ET.fromstring(get_url(url))
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        paper = paper_from_entry(entry)
        if paper.arxiv_id:
            papers.append(paper)
    return papers


def paper_from_entry(entry: ET.Element) -> Paper:
    abs_url = text_of(entry, "atom:id")
    arxiv_id = parse_arxiv_id(abs_url)
    links = entry.findall("atom:link", ATOM_NS)
    pdf_url = ""
    for link in links:
        if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
            pdf_url = link.attrib.get("href", "")
            break
    if not pdf_url and arxiv_id:
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

    return Paper(
        arxiv_id=arxiv_id,
        title=normalize_text(text_of(entry, "atom:title")),
        abstract=normalize_text(text_of(entry, "atom:summary")),
        authors=tuple(author for author in authors if author),
        abs_url=abs_url or f"http://arxiv.org/abs/{arxiv_id}",
        pdf_url=pdf_url,
        published=text_of(entry, "atom:published"),
        updated=text_of(entry, "atom:updated"),
        primary_category=primary.attrib.get("term", "") if primary is not None else "",
        categories=categories,
        comment=normalize_text(text_of(entry, "arxiv:comment")),
    )


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
        return tuple(filter_outline_headings(parser.headings)[:12])
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        print(f"warning: failed to fetch ar5iv outline for {paper.arxiv_id}: {exc}", file=sys.stderr)
        return ()


def filter_outline_headings(headings: list[str]) -> list[str]:
    blocked_exact = {
        "quick links",
        "submission history",
        "access paper:",
        "current browse context:",
        "references & citations",
        "bibtex formatted citation",
        "bookmark",
        "bibliographic and citation tools",
        "code, data and media associated with this article",
        "demos",
        "recommenders and search tools",
        "arxivlabs: experimental projects with community collaborators",
    }
    blocked_prefixes = (
        "computer science >",
        "title:",
    )
    result: list[str] = []
    for heading in headings:
        normalized = heading.strip()
        lower = normalized.lower()
        if lower in blocked_exact:
            continue
        if any(lower.startswith(prefix) for prefix in blocked_prefixes):
            continue
        if re.fullmatch(r"\d+(\.\d+)*\.?", normalized):
            continue
        result.append(normalized)
    return result


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


def paper_text(paper: Paper) -> str:
    return f"{paper.title} {paper.abstract}".lower()


def is_unidrive(paper: Paper) -> bool:
    text = paper_text(paper)
    return "unidrive" in text or "autonomous driving" in text or "driving" in text


def is_long_video_memory(paper: Paper) -> bool:
    text = paper_text(paper)
    return "memdreamer" in text or ("long video" in text and ("memory" in text or "retrieval" in text))


def is_spatial_reasoning_benchmark(paper: Paper) -> bool:
    text = paper_text(paper)
    return "spatialworld" in text or ("spatial reasoning" in text and "benchmark" in text)


def is_tool_calling_knowledge(paper: Paper) -> bool:
    text = paper_text(paper)
    return "tool calling" in text or ("experiential knowledge" in text and "tool" in text)


def is_interleaved_generation(paper: Paper) -> bool:
    text = paper_text(paper)
    return "interleavethinker" in text or "interleaved generation" in text


def is_medical_hallucination(paper: Paper) -> bool:
    text = paper_text(paper)
    return "clinhallu" in text or ("hallucination" in text and "medical" in text)


def is_iqa_alignment(paper: Paper) -> bool:
    text = paper_text(paper)
    return "image quality assessment" in text or ("semantics" in text and "distortions" in text)


def is_skill_scanner_security(paper: Paper) -> bool:
    text = paper_text(paper)
    return "skill scanner" in text or "malicious agent skills" in text or "hidden instruction" in text


def is_active_perception(paper: Paper) -> bool:
    text = paper_text(paper)
    return "active perception" in text or "omni-modal" in text


def is_remote_sensing_dataset(paper: Paper) -> bool:
    text = paper_text(paper)
    return "sarlo" in text or "remote sensing" in text or "sar " in text


def method_guess(paper: Paper) -> str:
    text = paper_text(paper)
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


def paper_architecture_breakdown(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """1. **长视频输入层**：先确认论文处理的是分钟级、小时级还是多片段视频。长视频的核心压力不是“看不懂画面”，而是视觉 token 爆炸、注意力稀释和稀疏证据难召回。
2. **感知缓存层**：MemDreamer 这类方法会把低层感知从最终推理里拆出来。重点看它如何把片段、对象、事件或场景变化写入层次化记忆，而不是每次都把原始帧重新喂给模型。
3. **图记忆层**：标题里的 hierarchical graph memory 是关键。要看节点代表什么、边代表什么、时间关系如何编码，以及记忆是否支持增量更新。
4. **Agentic retrieval 层**：推理阶段不再一次性读完整视频，而是像 agent 一样带着问题检索记忆。这里要看检索动作、停止条件、查询改写和失败重试。
5. **推理生成层**：最终回答应来自检索到的证据链，而不是模型凭常识补全。需要关注答案是否能回指到片段、对象或事件。
6. **验证层**：实验必须覆盖长程依赖、稀疏证据、多跳事件和干扰片段，否则不能证明它真的解决长视频问题。"""
    if is_spatial_reasoning_benchmark(paper):
        return """1. **任务环境层**：确认 SpatialWorld 里的任务是静态图片问答、可交互环境，还是需要连续操作的真实空间任务。
2. **空间状态层**：看论文如何表达位置、方向、相对关系、遮挡、距离和可达性；空间推理的核心往往在状态表示。
3. **交互动作层**：benchmark 如果强调 interactive，就要看 agent 能执行哪些观察、移动、选择或操作动作。
4. **反馈层**：每次交互后环境给什么反馈，反馈是视觉、文本、坐标还是成功/失败信号。
5. **评价层**：指标需要区分语言理解错误、空间关系错误、动作规划错误和执行错误。"""
    if is_tool_calling_knowledge(paper):
        return """1. **任务输入层**：先看 benchmark 或训练任务如何要求模型选择工具、填参数、解释调用结果。
2. **经验采集层**：experiential knowledge 的重点是模型从历史调用、错误反馈或成功轨迹里沉淀什么知识。
3. **知识激活层**：重点看这些经验在推理时如何被召回，是检索、prompt 注入、参数化记忆，还是策略模块。
4. **工具执行层**：工具 schema、参数约束、调用顺序和异常返回必须清楚，否则提升很可能只是 prompt 技巧。
5. **评测层**：实验要分开看工具选择、参数正确率、多步调用成功率和错误恢复能力。"""
    if is_interleaved_generation(paper):
        return """1. **生成状态层**：interleaved generation 的关键是模型不是一次性输出答案，而是在思考、动作、观察、生成之间切换。
2. **强化信号层**：看奖励如何定义，奖励是否能区分“会写中间过程”和“真的完成任务”。
3. **动作/文本交错层**：需要确认模型何时写 reasoning，何时调用工具或生成内容，是否有显式控制 token。
4. **训练稳定层**：强化这类交错行为容易出现格式崩坏、过度思考或无效动作，需要看约束和采样策略。
5. **评测层**：实验必须比较端到端答案质量、交互效率、调用次数和失败轨迹。"""
    if is_medical_hallucination(paper):
        return """1. **临床任务层**：先确认 benchmark 覆盖诊断、影像描述、病历推理还是治疗建议。医疗幻觉必须按任务阶段拆。
2. **阶段划分层**：ClinHallu 的价值应在 stage-wise diagnosis：是观察阶段错、证据归纳错、推理链错，还是最终建议错。
3. **证据绑定层**：医疗 MLLM 的回答必须回到影像区域、病例文本、检查结果或指南依据。
4. **幻觉标注层**：看论文如何定义 hallucination，是否区分事实错误、过度推断、遗漏证据和不安全建议。
5. **风险评估层**：医疗评测不能只看准确率，还要看错误严重度、可解释性和人工一致性。"""
    if is_skill_scanner_security(paper):
        return """1. **输入层**：agent skill 通常是 Markdown、YAML frontmatter、脚本、参考资料和命令片段的混合体，攻击面不只在自然语言。
2. **隐藏指令层**：重点看 malicious instruction 如何藏在注释、链接、代码块、图片 alt、配置字段或长文档深处。
3. **扫描模型层**：skill scanner 要判断哪些内容是能力说明，哪些是越权、泄露、持久化或绕过检查的指令。
4. **注意力/证据层**：如果论文用 attention 辅助检测，要看它是解释工具、特征来源，还是训练目标的一部分。
5. **评测层**：必须覆盖真实野外 skill、混淆样本、良性高危技能和对抗改写，否则很容易只检测到关键词。"""
    if is_active_perception(paper):
        return """1. **感知动作层**：active perception 的关键是模型能主动选择看哪里、听哪里、放大哪里或请求哪种模态。
2. **跨模态状态层**：omni-modal 不是模态堆叠，而是不同模态证据如何进入同一个推理状态。
3. **推理控制层**：看模型如何决定下一步感知动作，是否有不确定性、信息增益或任务目标驱动。
4. **成本层**：主动感知会增加交互和计算成本，必须看动作次数、延迟和 token/feature 预算。
5. **验证层**：实验要证明主动感知比被动全量输入更有效，而不是只靠更多信息取胜。"""
    if is_remote_sensing_dataset(paper):
        return """1. **数据采集层**：SAR/遥感数据的价值首先取决于覆盖区域、传感器类型、分辨率、成像角度和时间跨度。
2. **光学-雷达对齐层**：如果数据集同时涉及 SAR、optical 和 language，要看跨模态配准误差如何处理。
3. **语言标注层**：自然语言描述是否只是类别标签扩写，还是包含地物关系、空间布局、场景用途和变化线索。
4. **任务定义层**：数据集应明确支持检索、caption、定位、变化检测、VQA 还是 foundation model 预训练。
5. **评测层**：需要看跨地区、跨地貌、跨传感器和长尾目标上的泛化，而不只是随机划分得分。"""
    if is_unidrive(paper):
        return """1. **输入层**：先确认论文使用的是单帧、多帧、视频片段、传感器融合结果，还是已有感知模型输出。自动驾驶风险理解的难点往往来自长时序和小目标同时存在。
2. **视觉表示层**：看图像/视频特征如何进入语言模型，是否保留空间坐标、框、mask、轨迹或区域级证据。
3. **Grounding 层**：标题里的 grounding 是关键。需要确认模型是否能把语言解释绑定回具体目标、位置、时间片段或风险区域。
4. **语言推理层**：看模型如何把视觉证据转成风险判断，是直接生成解释，还是先生成结构化中间状态再输出语言。
5. **风险输出层**：确认输出是风险分类、自然语言解释、对象定位、时序证据，还是多个目标联合输出。
6. **验证层**：自动驾驶场景不能只看问答准确率，还要看空间定位、时序一致性、置信度和失败案例。"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """1. **输入层**：确认输入是图片、视频、音频还是多模态组合，以及上下文长度如何控制。
2. **编码层**：看视觉/音频编码器输出如何压缩、采样或对齐到语言 token。
3. **跨模态对齐层**：重点看空间、时间、对象和文本概念之间是否有显式绑定。
4. **推理层**：确认模型是直接回答，还是引入检索、记忆、链式推理或结构化中间表示。
5. **输出层**：看输出是分类、caption、定位、计划、解释还是可验证证据。
6. **评测层**：检查指标是否覆盖细粒度理解，而不是只覆盖粗粒度语义匹配。"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """1. **任务定义层**：确认 agent 面对的是静态问答、交互环境、代码仓库、GUI 还是工具链。
2. **状态层**：看 observation、memory、scratchpad、tool result 如何被表示和更新。
3. **动作层**：明确 action/tool schema、权限边界、参数约束和执行反馈。
4. **策略层**：看决策来自 prompt、训练目标、搜索、反思还是外部 verifier。
5. **反馈层**：确认奖励、评价器或错误信号如何进入下一轮决策。
6. **执行保障层**：检查超时、失败恢复、成本控制和 trace 记录。"""
    return """1. **问题输入层**：明确论文处理的输入、约束和目标。
2. **表示层**：找出核心中间表示，它通常决定方法的真实贡献。
3. **机制层**：拆出真正带来收益的算法、模块或训练目标。
4. **输出层**：确认输出形式是否可验证、可解释、可复现。
5. **实验层**：检查主结果、消融、泛化和失败案例是否形成闭环。"""


def paper_detail_breakdown(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """- **记忆写入粒度**：长视频不能把每帧都进记忆。要看节点是 clip、object、event、scene graph 还是 narration，以及粒度过粗时是否会漏稀疏证据。
- **图边语义**：hierarchical graph memory 的边如果只表示相邻片段，价值有限；更有价值的是对象共现、时间先后、因果线索和跨片段引用。
- **检索策略**：agentic retrieval 应该能根据问题动态选择记忆子图，而不是一次性 top-k 检索。重点看是否有多轮查询、query refinement 和停止条件。
- **感知/推理解耦**：解耦的好处是节省 token 和避免注意力稀释，但风险是感知阶段一旦漏写，推理阶段无法补救。
- **证据可追溯**：回答最好能回到视频片段或记忆节点；否则“记忆”只是隐藏 prompt，难以验证。"""
    if is_spatial_reasoning_benchmark(paper):
        return """- **空间关系覆盖**：检查任务是否覆盖左/右、前/后、遮挡、距离、朝向、可达性、多物体关系，而不是只测简单位置词。
- **交互真实性**：interactive benchmark 要看 agent 是否真的需要观察和行动；如果一次截图就能答，大部分交互设计就是噪声。
- **错误归因**：空间任务失败可能来自视觉识别、语言理解、坐标推理或动作规划，评测应能拆开这些错误。
- **真实世界噪声**：Real-world tasks 要覆盖视角变化、遮挡、尺度变化、物体相似和环境杂乱。"""
    if is_tool_calling_knowledge(paper):
        return """- **经验来源**：经验知识是从成功轨迹、失败轨迹、人工规则还是模型自反思中来，决定它能不能泛化。
- **激活时机**：工具调用前需要激活工具选择知识，参数填充前需要激活 schema 约束，调用后需要激活错误解释知识。
- **错误恢复**：真正有价值的 tool calling 提升应该体现在多步失败恢复，而不是单步函数名预测。
- **污染风险**：如果经验库直接记住测试工具或任务模板，指标提升会被数据泄漏放大。"""
    if is_interleaved_generation(paper):
        return """- **交错协议**：要看论文是否定义清楚 thought、action、observation、answer 的格式边界，否则模型容易生成看似复杂但不可执行的中间过程。
- **奖励分配**：强化 agentic interleaving 的难点是 credit assignment：到底奖励最终答案、过程格式、工具调用成功，还是中间证据质量。
- **退化模式**：常见失败包括过度思考、重复调用、提前输出、格式漂移和把 observation 编造成文本。
- **效率权衡**：交错生成通常更慢，必须用更高成功率或更强可验证性抵消额外成本。"""
    if is_medical_hallucination(paper):
        return """- **阶段级幻觉**：把错误拆成 observation、evidence selection、reasoning、diagnosis、recommendation，才能知道模型在医疗链路里哪里最危险。
- **临床严重度**：同样是错误，漏掉危急征象和措辞不严谨的风险完全不同。benchmark 应该区分 severity。
- **证据缺失**：医疗 MLLM 容易在影像证据不足时补充常识。需要看标注是否要求“无法判断”或不确定性表达。
- **人工一致性**：医学幻觉标注需要医生一致性或明确指南，否则 judge 噪声会污染结论。"""
    if is_iqa_alignment(paper):
        return """- **语义/失真解耦**：AI 生成图像质量评估不能把“语义好看”和“画质无瑕疵”混在一起；两流设计的价值就在拆开这两个信号。
- **尺度问题**：多尺度分支要证明既能看全局语义，也能抓局部瑕疵，例如纹理、边缘、手部、文字和细小伪影。
- **人类偏好对齐**：IQA 最终要对齐人类质量判断，需看标注来源、主观一致性和跨模型生成图的泛化。
- **评价泄漏**：如果测试图像来自少数生成器，模型可能学到生成器指纹，而不是真正评估质量。"""
    if is_skill_scanner_security(paper):
        return """- **攻击载荷位置**：隐藏指令可以出现在 Markdown 正文、frontmatter、代码块、脚本注释、链接文本和外部引用里，scanner 必须跨结构读取。
- **良恶性边界**：安全 skill 里天然会出现危险命令，难点不是看到 `rm`、token、credential 就报警，而是判断授权前提和执行意图。
- **注意力证据**：attention 如果被用来解释检测结果，需要看它是否稳定指向恶意片段，而不是被标题或关键词带偏。
- **野外分布**：真实 skill 往往写法不规范，benchmark 需要覆盖噪声、混淆、长文档和跨平台格式。"""
    if is_active_perception(paper):
        return """- **看哪里的问题**：主动感知的核心是选择信息，而不是把所有模态都塞进去。要看模型如何决定下一次观察区域或模态。
- **不确定性驱动**：好的 active perception 应该在不确定时获取证据，在确定时停止，而不是固定轮数。
- **多模态冲突**：omni-modal 任务里不同模态可能冲突，论文需要说明如何仲裁视觉、音频、文本或传感器证据。
- **成本收益**：多看一步是否真的提升准确率，还是只增加延迟和 token，这是落地判断的关键。"""
    if is_remote_sensing_dataset(paper):
        return """- **80cm 分辨率含义**：分辨率决定能否看到小型建筑、道路、车辆、农田纹理等细粒度目标，也决定语言标注能细到什么程度。
- **SAR 与光学互补**：SAR 能穿云、对结构敏感，光学更符合人眼语义。数据集若能对齐两者，才有跨模态基础模型价值。
- **全球覆盖**：worldwide 数据集要看区域分布是否均衡，是否覆盖城市、农田、海岸、山地、沙漠等不同地貌。
- **语言质量**：语言描述不能只是“there is a building”，需要体现空间布局、目标关系、场景属性和遥感特有信息。"""
    if is_unidrive(paper):
        return """- **时序推理细节**：摘要强调 temporal reasoning，要看模型处理连续帧时是否真的建模时间关系，还是只把多帧拼成上下文。
- **空间精度细节**：摘要提到 small、distant、partially occluded hazards，实验必须覆盖小目标、遮挡、远距离目标和边缘区域。
- **证据绑定细节**：interpretable risk understanding 不能只生成合理解释，还要能指出解释对应的目标、区域或时间片段。
- **数据标注细节**：风险理解数据集需要明确风险对象、风险原因、发生时刻和可见证据，否则模型容易学到场景先验。
- **评测指标细节**：除了文本匹配，还应关注 grounding accuracy、temporal localization、risk classification、explanation faithfulness。
- **失败案例细节**：最值得看的不是成功样例，而是遮挡、复杂交通参与者、夜间/雨天、长尾风险下模型如何失败。"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """- **采样策略**：看帧/区域/片段如何选择，是否会丢掉稀疏但关键的证据。
- **对齐策略**：确认模态对齐靠训练数据、结构设计、显式坐标，还是 prompt 约束。
- **上下文预算**：长视频或高分辨率输入会带来 token 压力，需要看压缩是否损失细节。
- **可解释性**：生成的文字是否能追溯到视觉证据。
- **泛化边界**：看跨数据集、跨场景、跨模型 backbone 是否仍然有效。"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """- **动作空间**：工具越多，越要看动作定义是否清晰，是否存在危险或重复动作。
- **状态漂移**：长程任务里 memory 和 scratchpad 是否会引入过期信息。
- **错误恢复**：失败后是重新规划、局部重试，还是直接继续生成。
- **评价器可靠性**：如果依赖 LLM judge，要看是否有可验证信号或人工校准。
- **成本控制**：多轮 agent 论文必须说明调用次数、token、环境交互成本。"""
    return """- **核心假设**：方法成立依赖哪些数据、模型或任务假设。
- **关键模块**：消融实验是否证明每个模块必要。
- **对比对象**：baseline 是否足够强，设置是否公平。
- **失败边界**：论文是否解释方法在哪些场景会失效。
- **复现条件**：代码、数据、prompt、超参数是否足够完整。"""


def paper_method_chain(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """```text
long video
  -> clip/object/event perception
  -> hierarchical graph memory write
  -> question-driven agentic retrieval
  -> evidence subgraph assembly
  -> multimodal reasoning
  -> answer with traceable support
```

这条链路要重点看“写入”和“检索”之间是否闭环。长视频理解最怕前面为了省 token 过度压缩，后面再靠语言模型想象缺失证据。"""
    if is_tool_calling_knowledge(paper):
        return """```text
task
  -> infer needed tool
  -> activate experiential knowledge
  -> fill schema-constrained arguments
  -> execute / simulate tool call
  -> read feedback
  -> repair or continue
```

工具调用论文不能只看函数名选择。真正困难的是参数、顺序和错误恢复，尤其是工具返回和下一步推理之间的接口。"""
    if is_interleaved_generation(paper):
        return """```text
task state
  -> generate reasoning segment
  -> choose action or content segment
  -> observe feedback / partial result
  -> update state
  -> repeat until final answer
```

这条链路的关键是交错是否被任务需要。如果中间过程不能改变后续动作，那 interleaving 只是输出格式；如果 observation 能改变策略，才是 agentic generation。"""
    if is_skill_scanner_security(paper):
        return """```text
skill package
  -> parse markdown / metadata / scripts
  -> locate instruction-like spans
  -> classify benign high-risk vs malicious
  -> produce evidence spans
  -> block, quarantine, or request review
```

安全 scanner 的价值取决于证据定位。只给一个风险分数不够，必须指出哪段文本或脚本触发风险，方便人工复核。"""
    if is_remote_sensing_dataset(paper):
        return """```text
SAR / optical imagery
  -> geo-alignment and tiling
  -> language annotation
  -> dataset filtering
  -> benchmark task construction
  -> model evaluation
  -> geographic generalization analysis
```

数据集论文的链路重点不是模型多复杂，而是数据是否可用、可对齐、可复现、能逼出模型短板。"""
    if is_unidrive(paper):
        return """```text
driving scene input
  -> visual / temporal evidence extraction
  -> object or region grounding
  -> language-model risk reasoning
  -> grounded explanation / risk output
  -> metric-level verification
```

这条链路里最容易虚的地方是中间三步：视觉证据是否真的保留了空间和时间信息，grounding 是否能回指到具体目标，语言解释是否只是“听起来合理”而不是忠实于视觉证据。精读时要把每个 claim 都压回这条链上验证。"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """```text
multimodal input
  -> encoder / sampler
  -> token or feature compression
  -> cross-modal alignment
  -> reasoning / generation
  -> task output
  -> metric and failure analysis
```

这条链路的关键是信息有没有在压缩和对齐阶段丢失。很多多模态论文的提升来自更好的采样或数据，而不是模型真的学会了更强推理。"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """```text
task state
  -> planner / policy
  -> tool action
  -> environment feedback
  -> memory or trace update
  -> next action
  -> final answer / success metric
```

Agent 论文要特别注意反馈是否真实。如果 observation 只是文本摘要，或者 judge 本身不可验证，长程任务分数会很容易虚高。"""
    return """```text
input
  -> representation
  -> core mechanism
  -> output
  -> evaluation
  -> limitation analysis
```

精读时把论文所有模块都挂到这条链上：挂不上去的模块，通常就是包装或叙事。"""


def paper_experiment_checklist(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 长程依赖 | 是否覆盖小时级视频、跨片段事件和稀疏证据问题。 |
| 记忆消融 | 去掉 graph memory、层次结构或检索 agent 后性能是否明显下降。 |
| 检索质量 | 是否评估召回到的片段/节点是否真的支持答案。 |
| Token/成本 | 是否报告相比全视频输入节省多少 token、显存或延迟。 |
| 失败案例 | 是否展示漏写记忆、检索错片段、推理错因果的案例。 |"""
    if is_tool_calling_knowledge(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 工具选择 | 是否区分选择正确工具和填对参数。 |
| 多步调用 | 是否覆盖工具链组合，而不只是单函数调用。 |
| 经验消融 | 去掉 experiential knowledge 后是否明显下降。 |
| 错误恢复 | 是否统计调用失败后的修复率。 |
| 泛化 | 是否验证未见工具、未见任务和 schema 变化。 |"""
    if is_interleaved_generation(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 交错必要性 | 相比直接生成，交错过程是否带来稳定收益。 |
| 奖励设计 | 奖励是否避免只优化格式而不优化任务成功。 |
| 成本 | 是否报告额外轮数、token、工具调用和延迟。 |
| 失败轨迹 | 是否展示过度思考、重复行动、格式漂移等问题。 |
| 泛化 | 是否跨任务或跨模型验证。 |"""
    if is_medical_hallucination(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 阶段诊断 | 是否把幻觉定位到观察、证据、推理、结论等阶段。 |
| 临床严重度 | 是否按风险等级区分错误。 |
| 专家标注 | 是否有医生标注、一致性或指南依据。 |
| 多模型覆盖 | 是否覆盖不同 MLLM 和不同医疗子任务。 |
| 失败样例 | 是否展示危险误诊、证据缺失和过度推断。 |"""
    if is_skill_scanner_security(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 真实样本 | 是否包含野外 agent skill，而不只是合成 prompt。 |
| 隐藏位置 | 是否覆盖 frontmatter、Markdown、代码块、脚本、链接和外部引用。 |
| 误报控制 | 是否区分良性安全技能和恶意隐藏指令。 |
| 证据定位 | 是否输出风险片段，方便人工复核。 |
| 对抗改写 | 是否测试 paraphrase、分散载荷和长文档稀释。 |"""
    if is_remote_sensing_dataset(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 覆盖范围 | 是否说明国家/地区、地貌、季节、传感器分布。 |
| 配准质量 | SAR、光学和语言是否可靠对齐。 |
| 标注质量 | 是否有人审、过滤规则和一致性统计。 |
| 任务价值 | 是否支持检索、caption、定位、VQA 或预训练。 |
| 泛化 | 是否跨地区、跨传感器、跨地貌划分评估。 |"""
    if is_unidrive(paper):
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 时序能力 | 是否比较单帧、多帧、长视频窗口；是否展示时间错位或延迟风险案例。 |
| 空间 grounding | 是否有框、mask、区域、轨迹或对象级指标，而不只是文本答案。 |
| 风险解释忠实度 | 解释是否能绑定到视觉证据；错误解释是否被单独分析。 |
| 长尾场景 | 是否覆盖遮挡、远距离、小目标、夜间、雨雪、复杂交互。 |
| Baseline 公平性 | baseline 是否使用同等输入分辨率、帧数和模型规模。 |
| 失败案例 | 是否明确展示模型漏检、误报、错误定位和错误推理。 |"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 数据覆盖 | 是否覆盖多场景、多对象、多时间跨度和难例。 |
| 对齐指标 | 是否有定位、引用、时间段或证据级指标。 |
| 消融实验 | 是否拆开编码器、采样、检索、推理模块分别验证。 |
| 成本指标 | 是否报告 token、延迟、显存或调用次数。 |
| 泛化能力 | 是否跨数据集、跨模型或跨任务验证。 |"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 任务真实性 | 是否是真交互环境，而不是静态问答。 |
| Trace 质量 | 是否公开或分析中间 tool call、observation 和失败路径。 |
| 成本控制 | 是否报告步数、token、工具调用次数和超时率。 |
| 错误恢复 | 是否单独统计重试、回滚、重新规划。 |
| Judge 可靠性 | 是否有人类校验或确定性检查作为对照。 |"""
    return """| 检查点 | 需要看到的证据 |
| --- | --- |
| 主结果 | 是否显著优于强 baseline。 |
| 消融实验 | 是否证明关键模块必要。 |
| 泛化设置 | 是否跨数据或跨模型验证。 |
| 成本分析 | 是否报告额外计算、延迟和资源。 |
| 失败案例 | 是否解释方法边界。 |"""


def paper_interpretation_intro(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """这篇论文抓住的是长视频理解里最现实的瓶颈：模型不是完全看不懂视频，而是 **看完整视频太贵，看压缩视频又容易丢掉关键证据**。MemDreamer 的标题已经把解法说得很清楚：把 perception 和 reasoning 解耦，用层次化图记忆保存视频证据，再让 agentic retrieval 在推理时主动找相关记忆。

所以这篇不是普通的视频问答论文，而是一篇“长视频记忆系统”论文。它真正要证明的是：记忆写入是否足够保真，检索是否能找回稀疏证据，推理是否真的基于这些证据，而不是把长视频问题重新包装成短文本推理。"""
    if is_spatial_reasoning_benchmark(paper):
        return """这篇论文的重点不是再做一个多模态排行榜，而是问一个更扎实的问题：多模态 agent 在真实空间任务里，到底会不会理解位置、方向、距离、遮挡、可达性和交互反馈。

SpatialWorld 作为 benchmark，价值取决于它能否把“看图说话”推进到“带着空间目标行动”。如果任务只需要描述图片，它测不到 agent；如果任务必须通过观察、动作和反馈逐步完成，它才能暴露空间推理系统的短板。"""
    if is_tool_calling_knowledge(paper):
        return """这篇论文把 tool calling 的问题从“模型会不会选函数名”推进到“模型能不能从经验里学会更可靠地调用工具”。标题里的 experiential knowledge integration and activation 是核心：经验如何沉淀、何时激活、如何影响工具选择和参数填写。

真正值得看的不是它把提示词写得多复杂，而是它是否把工具调用变成一个可积累、可检索、可纠错的过程。"""
    if is_interleaved_generation(paper):
        return """InterleaveThinker 关注的是 agentic generation 里的一个关键能力：模型不能只在开头想完、最后输出，而要在推理、生成、观察、修正之间交错推进。

这篇论文要证明的是：强化这种 interleaved 行为是否真的提高任务成功率，而不是让输出变长、格式变复杂。读它时要紧盯奖励设计、交错协议和失败轨迹。"""
    if is_medical_hallucination(paper):
        return """ClinHallu 的价值在于把医疗 MLLM 幻觉从一个总分问题拆成阶段问题。医疗链路里，模型可能在观察影像时错、选择证据时错、推理时错，也可能最后建议时错；这些错误的风险完全不同。

所以这篇更像一篇诊断工具论文：它不是只问模型有没有错，而是问模型在临床推理链的哪一步开始错，以及这个错误会造成多大风险。"""
    if is_iqa_alignment(paper):
        return """这篇论文关注 AI 生成图像质量评估里一个容易被混淆的问题：语义是否正确，和图像是否有失真，并不是同一个信号。一个图可以语义很对但局部细节崩坏，也可以画质很干净但语义不符合指令。

它的 two-stream / multi-scale 设计要证明的是：把 semantics 和 distortions 解耦，是否能更接近人类对 AIGC 图像质量的判断。"""
    if is_skill_scanner_security(paper):
        return """这篇论文非常贴近 agent 工程安全：当 agent 可以安装 skill，skill 本身就变成供应链入口。攻击者不一定直接攻击模型，而是把隐藏指令塞进 Markdown、frontmatter、脚本、链接或参考资料，让 scanner 看漏，让 agent 执行。

读这篇时要把它当成“agent skill 供应链安全”论文。重点不是有没有一个检测分数，而是能否发现隐藏载荷、区分良性高危技能和恶意技能，并给出可复核证据。"""
    if is_active_perception(paper):
        return """这篇论文讨论的是 omni-modal 理解里的主动感知：模型不只是被动接收一堆模态，而是把“下一步该看什么、听什么、放大什么”当成推理动作。

它的核心价值取决于两点：主动获取证据是否比全量被动输入更有效，以及模型是否知道什么时候停止继续感知。"""
    if is_remote_sensing_dataset(paper):
        return """SARLO-80 这类论文要按数据集论文读：重点不是模型结构，而是数据是否足够稀缺、覆盖是否足够广、模态是否对齐、标注是否能支撑后续 foundation model 训练和评测。

80cm 级遥感/SAR-光学-语言数据如果做得扎实，价值在于给遥感多模态模型提供更细粒度、更全球化、更接近真实应用的数据底座。"""
    if is_unidrive(paper):
        return """这篇论文的核心不是再做一个“会描述驾驶场景”的多模态模型，而是在处理自动驾驶风险理解里一个很具体的矛盾：**视频模型有时间信息，但容易牺牲空间精度；高分辨率单帧模型看得清，但容易缺少动态上下文。**

UniDrive 的思路是把这两个能力拆开，再重新融合：一条分支负责多帧时序语义，一条分支负责最新帧的高分辨率空间细节，最后用 gated cross-attention 把“动态上下文”和“精确视觉证据”对齐。它最后不是只输出一句 caption，而是同时生成自然语言风险描述和风险对象的 bounding box。这个设计使它更像一个 **可解释风险理解框架**，而不只是自动驾驶场景 captioner。"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """这篇论文要看的不是模型答题能力，而是 agent 在长程任务里如何维护状态、选择动作、接收反馈，并把失败路径变成下一步决策依据。解读时应该把它当作一个执行系统，而不是单轮推理模型。"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """这篇论文的重点在多模态信息如何被保留、对齐和验证。解读时不要只看最终指标，要追问视觉证据在进入语言模型之后是否仍然可定位、可解释、可复核。"""
    return """这篇论文需要按“问题矛盾 -> 方法主线 -> 实验证据 -> 边界条件”的顺序读。先判断它抓住的问题是否真实，再看方法是否针对这个问题，而不是被复杂模块带着走。"""


def paper_core_claims(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| 长视频直接输入会导致 token explosion 和 attention dilution | 这是全文出发点：长视频不是简单扩大上下文就能解决，计算和注意力都会被大量无关帧稀释。 |
| Decoupling perception and reasoning | 感知阶段先把视频变成可检索记忆，推理阶段再按问题读取证据，避免每个问题都重读全视频。 |
| Hierarchical graph memory | 记忆不是平铺文本摘要，而应保留片段、事件、对象和关系层次。重点看图结构是否真的承载时序/关系信息。 |
| Agentic retrieval | 检索不是一次 top-k，而是带着问题多步探索记忆。它应该提升稀疏证据召回和多跳推理。 |
| 长视频理解能力提升 | 需要用长程依赖、稀疏证据和干扰片段实验来支撑，不能只看普通视频 QA 平均分。 |"""
    if is_tool_calling_knowledge(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| 现有 LLM tool calling 受限于缺少经验 | 工具调用失败常常不是不会说话，而是不知道历史上哪些参数、顺序和错误恢复策略有效。 |
| Experiential knowledge 可以被集成 | 关键要看经验以什么形式保存：示例轨迹、规则、检索库、记忆项还是训练信号。 |
| Activation 决定知识是否有用 | 经验只有在正确任务、正确工具、正确参数阶段被激活才有价值。 |
| 工具调用性能提升 | 应拆成工具选择、参数正确、多步链路、失败恢复和未见工具泛化。 |"""
    if is_interleaved_generation(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| Agentic interleaved generation 值得强化 | 作者认为推理和生成交错出现，比一次性思考后输出更适合复杂任务。 |
| 强化学习可以塑造交错行为 | 重点看奖励是否真的鼓励有效行动，而不是鼓励更长、更像格式的中间过程。 |
| 交错过程提升任务表现 | 需要看成功率、调用效率、失败轨迹和消融，而不是只看最终文字质量。 |
| 方法可迁移到多类 agent 任务 | 需要跨任务验证，否则可能只是某类 benchmark 的格式优化。 |"""
    if is_skill_scanner_security(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| Agent skill scanner 面临隐藏指令攻击 | 攻击面来自 skill 包本身，尤其是 Markdown、metadata、脚本和参考链接混合的结构。 |
| 多模态/文本 scanner 容易漏掉深层载荷 | 如果 scanner 只看摘要或关键词，就会被长文档稀释、格式混淆或间接引用绕过。 |
| Attention 可用于定位恶意片段 | 关键是 attention 是否能稳定指向真正载荷，而不是只提供事后解释。 |
| 野外 skill 检测需要误报控制 | 安全技能本来就包含危险命令，检测器必须理解授权上下文和执行意图。 |"""
    if is_remote_sensing_dataset(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| SARLO-80 提供全球范围 80cm 级遥感数据 | 数据覆盖和分辨率是主要贡献，需要看地理、地貌和传感器分布。 |
| SAR / optical / language 组合有训练价值 | SAR 和光学互补，语言则把地物语义显式化，三者对齐质量决定数据集上限。 |
| 数据可支持遥感 VLM/foundation model | 要看任务定义是否足够丰富，而不只是图片-caption 对。 |
| 可作为跨地区泛化评测 | 真正价值在跨地貌、跨传感器、跨地区，而不是随机划分高分。 |"""
    if is_unidrive(paper):
        return """| 作者主张 | 解读 |
| --- | --- |
| 现有 MLLM 在自动驾驶风险理解中存在 temporal reasoning 与 spatial precision 的 trade-off | 这是全文的问题定义。作者认为单帧/低分辨率方案会漏小目标、远目标、遮挡目标；语言中心的驾驶模型又缺少 grounded evidence。 |
| Temporal reasoning branch 建模多帧动态 | 这条分支负责“事情如何变化”，例如车辆、行人、交通参与者之间的时序关系。它应该提升风险判断的上下文理解。 |
| High-resolution perception branch 保留最新帧细粒度空间细节 | 这条分支负责“风险对象到底在哪里”，尤其是小目标、远距离目标和遮挡目标。 |
| Gated cross-attention fusion 对齐动态上下文和空间证据 | 这是方法核心。重点要看 gate 是否真的学会在不同场景下调节两条分支，而不是简单特征拼接。 |
| 联合生成自然语言风险描述和 bounding-box grounding | 这决定了论文的可解释性标准：解释必须能回到具体对象，而不是只有流畅文本。 |
| 在 DRAMA-Reasoning、NuScenes、BDD100K 上验证 | 这里要看主任务、零样本泛化和人工可解释性评价是否相互支撑。 |"""
    return """| 作者主张 | 解读 |
| --- | --- |
| 论文提出一个具体问题 | 先确认这个问题是否真实存在，而不是已有任务换了名字。 |
| 方法引入新的模块或流程 | 看模块是否直接服务于问题矛盾。 |
| 实验展示性能提升 | 检查提升来自方法本身、数据设置，还是 baseline 较弱。 |
| 作者声称有可迁移价值 | 需要看跨数据集、跨模型或失败案例是否支撑。 |"""


def paper_problem_interpretation(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """MemDreamer 抓住的矛盾是：长视频理解需要保留大量时序证据，但大模型上下文和注意力机制并不适合直接吞下完整视频。

- 全量输入会爆 token，注意力被大量无关帧稀释。
- 预先压缩成摘要会丢掉稀疏但关键的证据。
- 只做一次静态检索，很难完成多跳、跨片段、问题驱动的证据组合。

所以它要回答的问题是：**能不能先把视频变成可查询记忆，再让推理过程像 agent 一样主动探索记忆。**"""
    if is_skill_scanner_security(paper):
        return """这类论文的矛盾在于：agent skill 必须给模型足够详细的步骤和命令，才有实用价值；但越详细，越容易藏入恶意指令、越权动作和供应链风险。

安全 scanner 不能简单禁止危险词，因为防御性安全技能天然包含攻击技术名称和命令。真正问题是：**如何在高风险但良性的安全知识，与伪装成技能的恶意指令之间划线。**"""
    if is_remote_sensing_dataset(paper):
        return """遥感多模态模型常见瓶颈不是缺一个更大的 backbone，而是缺高质量、全球覆盖、跨传感器、带语言语义的数据。

SAR 有全天时全天候优势，但不直观；光学图像语义直观，但受云层和光照影响；语言标注能连接地物与任务，但容易粗糙。SARLO-80 的问题就是：**能不能把这三类信号对齐成可训练、可评测的数据底座。**"""
    if is_unidrive(paper):
        return """UniDrive 抓住的是自动驾驶场景理解里很典型的“鱼和熊掌”问题：

- 如果模型主要看视频，它能理解目标运动和场景变化，但为了控制 token / feature 成本，往往会降低分辨率或稀释空间细节。
- 如果模型主要看最新高分辨率单帧，它能看清小目标、远目标和遮挡区域，但缺少“这个风险是怎么形成的”的动态上下文。
- 如果模型只输出自然语言解释，即使文字合理，也很难判断它到底看到了哪个风险对象。

所以这篇论文的真正问题不是“让 MLLM 更会 caption”，而是：**能不能同时保留时间语义、空间精度和可验证 grounding。**"""
    return """这篇论文需要先拆清楚它面对的核心矛盾：现有方法到底缺的是数据、表示、推理、执行反馈，还是评测方式。只有矛盾明确，后面的模块才有判断标准。"""


def paper_module_interpretation(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| Perception stage | 从长视频中抽取可存储证据，避免推理时重读全视频 | 抽取粒度、覆盖率、是否保留时间和对象关系。 |
| Hierarchical graph memory | 把片段、事件、对象和关系组织成可查询结构 | 节点/边定义、层次结构、更新策略和压缩损失。 |
| Agentic retrieval | 根据问题多步探索相关记忆 | 查询生成、检索停止、错误恢复和证据召回率。 |
| Reasoning stage | 基于检索证据完成问答或理解任务 | 是否能引用证据，是否会脱离记忆编造。 |
| Evaluation protocol | 证明长视频能力和成本优势 | 长程依赖、稀疏证据、消融、token/延迟成本。 |"""
    if is_tool_calling_knowledge(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| Experience collection | 收集工具调用成功/失败轨迹 | 经验来源是否可靠，是否覆盖失败修复。 |
| Knowledge integration | 把经验组织成可用知识 | 是检索库、规则、prompt 片段还是训练信号。 |
| Activation mechanism | 在当前任务中唤起相关经验 | 是否按工具、参数、错误类型精准激活。 |
| Tool execution | 生成并执行工具调用 | schema 约束、参数正确率、多步顺序。 |
| Feedback repair | 根据结果修复下一步 | 是否统计失败恢复，而非只统计首轮正确。 |"""
    if is_interleaved_generation(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| Interleaving protocol | 定义思考、动作、观察、答案如何交替出现 | 格式是否可执行，是否防止状态混乱。 |
| Reinforcement objective | 强化有效交错行为 | 奖励是否绑定任务成功，而非中间过程长度。 |
| Policy behavior | 决定何时继续推理、何时输出或行动 | 是否减少无效循环、重复调用和提前停止。 |
| Evaluation trace | 展示交错过程是否有用 | 轨迹质量、成本、失败模式和消融。 |"""
    if is_skill_scanner_security(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| Skill parser | 读取 Markdown、metadata、脚本和引用 | 是否覆盖真实 skill 包结构。 |
| Risk span detector | 找到隐藏指令或恶意片段 | 是否能跨代码块、链接、注释定位。 |
| Attention mechanism | 提供检测依据或特征 | 是解释、监督还是核心分类信号。 |
| Benign/malicious classifier | 区分良性安全技能和恶意载荷 | 误报率、漏报率、对抗改写。 |
| Review output | 给人工或平台处理结果 | 是否输出证据、风险类型和处置建议。 |"""
    if is_remote_sensing_dataset(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| SAR imagery | 提供全天时、结构敏感遥感视角 | 分辨率、传感器、噪声和地理分布。 |
| Optical imagery | 提供直观语义和视觉纹理 | 与 SAR 的配准误差和时间差。 |
| Language annotation | 把地物、布局和场景用途文本化 | 描述粒度、标注流程、质量控制。 |
| Dataset splits | 支撑训练和评测 | 是否按地区/地貌/传感器做泛化划分。 |
| Benchmarks | 验证数据集用途 | 检索、caption、VQA、定位或预训练指标。 |"""
    if is_unidrive(paper):
        return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| Multi-frame visual input | 给模型动态上下文，避免只看单帧导致误判风险趋势 | 输入帧数、采样间隔、时间窗口是否足够覆盖风险形成过程。 |
| Temporal reasoning branch | 建模场景动态，比如目标运动、相对距离变化、潜在碰撞关系 | 是否有时序消融；去掉该分支后 caption 和风险判断是否明显下降。 |
| High-resolution perception branch | 保留最新帧空间细节，缓解小目标、远目标、遮挡目标漏检 | 是否真的使用更高分辨率；小目标 localization 是否单独统计。 |
| Gated cross-attention fusion | 让动态语义和精细空间证据交互 | gate 的作用是否有消融；是否比较过 concat、普通 cross-attention 等更弱融合方式。 |
| Natural-language risk description | 输出人能读懂的风险解释 | 解释是否忠实于视觉证据，还是只是常识化驾驶描述。 |
| Grounded bounding-box output | 把风险解释绑定到具体对象 | grounding 指标是否和 caption 指标同时提升；错误案例是否分析框错还是文本错。 |"""
    return """| 模块 | 它在解决什么 | 需要重点核对什么 |
| --- | --- | --- |
| 输入表示 | 把原始数据变成模型可处理的形式 | 是否丢失关键上下文。 |
| 核心机制 | 论文真正贡献所在 | 是否有直接消融证明。 |
| 输出格式 | 决定结果是否可验证 | 是否只是自然语言，还是有结构化证据。 |
| 评测协议 | 决定结论可信度 | baseline、指标、数据划分是否公平。 |"""


def paper_method_success_conditions(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """MemDreamer 是否成立，主要看三件事：

1. **记忆是否保真**
   如果层次化图记忆漏掉关键片段，后面的 agentic retrieval 再聪明也找不回来。论文需要证明记忆写入不是简单摘要，而是保留对象、事件和时间关系。

2. **检索是否真的 agentic**
   如果只是一次 top-k 检索，和普通 RAG 差别有限。要看是否有多步查询、根据中间证据改写问题、停止条件和失败恢复。

3. **收益是否来自长视频机制**
   需要消融 graph memory、hierarchy、retrieval agent，并报告 token/延迟成本。否则提升可能来自更强 backbone 或更多上下文。"""
    if is_tool_calling_knowledge(paper):
        return """方法是否成立，关键看经验知识有没有跨任务泛化。如果经验只是在测试集上记住工具模板，价值有限；如果它能帮助模型处理未见参数、工具组合和失败返回，才说明 experiential knowledge 真的进入了 tool calling 策略。"""
    if is_interleaved_generation(paper):
        return """InterleaveThinker 成立的前提是交错过程改变了决策，而不是只改变了输出格式。要看去掉 interleaving 或去掉强化目标后，成功率、轨迹质量和成本是否发生可解释变化。"""
    if is_skill_scanner_security(paper):
        return """这类检测方法成立的关键不是高准确率，而是高风险场景下的可复核证据：能不能定位隐藏载荷，能不能区分防御性安全命令和恶意指令，能不能抵抗改写和长文档稀释。"""
    if is_remote_sensing_dataset(paper):
        return """SARLO-80 是否成立，主要看数据质量而不是模型分数。需要证明 SAR、光学和语言对齐可靠，全球覆盖不是口号，标注粒度足以支撑细粒度遥感理解，并且跨地区划分下仍有评测价值。"""
    if is_unidrive(paper):
        return """UniDrive 的方法是否成立，主要看三个点：

1. **双分支是不是各司其职**
   temporal branch 应该负责动态语义，high-resolution branch 应该负责空间细节。正文里最好有消融能证明：去掉 temporal branch 会伤害时序/风险推理，去掉 high-resolution branch 会伤害小目标定位。

2. **gated cross-attention 是否真的在融合，而不是装饰模块**
   如果 gate 只是让参数变多，收益可能来自容量；如果 gate 在复杂场景、小目标场景、运动风险场景下表现出不同权重或显著消融收益，才说明它解决了“动态语义对齐空间证据”的问题。

3. **输出是不是形成解释闭环**
   自然语言风险描述和 bounding box grounding 必须互相支撑：文本说某个对象危险，框就要能定位到对应对象；框定位错了，文本解释的可信度也应该下降。"""
    return """方法是否成立，不能只看模块名称。要看每个模块是否对应问题矛盾，消融是否证明必要性，输出是否能被实验指标直接验证。"""


def paper_result_interpretation(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """读实验时不要只看总分，要把结果拆成四类：

1. **长视频主结果**
   看 MemDreamer 是否在更长时长、更稀疏证据、更强干扰的视频上提升明显。如果短视频也提升，可能是通用模型增强；如果长视频提升更大，才贴合问题定义。

2. **记忆与检索消融**
   去掉 hierarchical graph memory、去掉 agentic retrieval、改成普通摘要或普通 top-k 检索，性能应该出现有解释的下降。

3. **成本收益**
   长视频方法必须报告 token、显存、推理延迟或检索轮数。否则“更准”可能只是更贵。

4. **失败案例**
   最该看的失败不是答错，而是为什么答错：感知阶段没写入，检索阶段找错，还是推理阶段误解证据。"""
    if is_tool_calling_knowledge(paper):
        return """结果要分层读：工具选择正确率只能说明模型知道用哪个 API；参数正确率说明 schema 理解；多步成功率说明流程控制；失败恢复率才说明经验知识有实际价值。若论文只报告总体 accuracy，需要谨慎。"""
    if is_interleaved_generation(paper):
        return """结果要同时看成功率和效率。Interleaving 如果让任务更稳但 token 翻倍，需要判断是否值得；如果轨迹更长但无法解释失败，那它只是更复杂的输出格式。消融实验应证明强化目标和交错协议都必要。"""
    if is_skill_scanner_security(paper):
        return """安全检测结果要重点看漏报。误报会影响可用性，但漏报会让 agent 执行恶意 skill。最好看按攻击位置、载荷类型、文档长度、混淆方式拆开的结果，以及是否给出风险证据片段。"""
    if is_remote_sensing_dataset(paper):
        return """数据集论文的实验不是为了证明某个模型最强，而是证明数据能支撑有意义的任务。读结果时应看跨地区/跨传感器泛化、SAR 与 optical 的互补收益、语言标注带来的增益，以及长尾地物上的失败。"""
    if is_unidrive(paper):
        return """从摘要看，实验结论分成三组，读正文时应该分开验证：

1. **主 benchmark：DRAMA-Reasoning**
   这里要看 UniDrive 相比 image-based 和 video-based baseline 的提升是否同时出现在 captioning 与 risk-object grounding 上。如果只提升 caption，不提升 grounding，可解释性主张就不稳。

2. **小目标定位优势**
   摘要特别强调 small-object localization。这个点和 high-resolution perception branch 是一一对应的，应该重点找小目标子集、距离分桶、遮挡分桶或 qualitative case。

3. **零样本泛化：NuScenes 和 BDD100K**
   零样本结果用来说明方法不是只适配 DRAMA-Reasoning。这里要看目标数据集任务定义是否一致，输入格式是否一致，以及有没有 domain shift 的失败案例。

4. **人工评价：interpretability and trustworthiness**
   这部分最容易主观。需要看评分准则、评审人数、一致性、是否 blind review，以及 grounding 错误是否会影响人类信任评分。"""
    return """读实验时不要只看总分。至少拆成主结果、消融实验、跨数据泛化、成本分析和失败案例五块。主结果说明“有没有用”，消融说明“哪个模块有用”，泛化说明“是不是只对一个数据集有用”，失败案例说明“什么时候不要用”。"""


def paper_takeaway(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """这篇论文最值得带走的是“长视频不要硬塞上下文”的问题拆法：先把感知结果写成可查询记忆，再让推理过程按问题主动取证。这个思路对长视频、长文档、多轮 agent trace 都有参考价值。

但也要记住它的风险：记忆一旦写错或漏写，后面检索再复杂也只能在错误空间里搜索。"""
    if is_tool_calling_knowledge(paper):
        return """这篇论文的启发是：tool calling 需要经验层。工程上可以把成功调用、失败返回、参数修复和工具组合沉淀成可检索知识，而不是每次都让模型从 schema 零开始猜。"""
    if is_interleaved_generation(paper):
        return """这篇论文值得带走的是：复杂任务里的生成不一定是线性的。让模型在推理、行动、观察和输出之间切换，可能比一次性长答案更可控，但前提是每次切换都能改变状态。"""
    if is_skill_scanner_security(paper):
        return """这篇论文的工程启发很直接：agent skill 需要像依赖包一样做供应链审查。安装前不仅要看能力说明，还要解析 metadata、脚本、链接和隐藏指令，并输出可复核证据。"""
    if is_remote_sensing_dataset(paper):
        return """SARLO-80 的可迁移价值在数据工程：跨传感器对齐、全球覆盖、细粒度语言标注和泛化划分，往往比单个模型结构更能推动遥感多模态能力。"""
    if is_unidrive(paper):
        return """这篇论文真正值得带走的点，是把“自动驾驶解释”从纯文本描述拉回到 **时序证据 + 空间证据 + grounded object** 的闭环。对安全关键场景来说，解释不是越像人话越好，而是越能回指证据越好。

我会把它归类为一篇值得读方法结构的论文：不一定要照搬 UniDrive 的具体模块，但“动态语义一条支路、精细感知一条支路、再用 gated fusion 对齐”的问题拆法，对很多多模态风险理解任务都有参考价值。"""
    return """这篇论文的价值不只在最终指标，而在它如何拆问题、设计中间表示、把结果变成可验证证据。读完后应该能回答：它解决了什么矛盾，哪个模块真正解决这个矛盾，实验有没有支撑这个解释。"""


def paper_experiment_questions(paper: Paper) -> str:
    text = paper_text(paper)
    if is_long_video_memory(paper):
        return """这篇实验最少要回答四个问题：

1. **记忆是否比直接上下文更有效？**
   要比较全视频输入、摘要压缩、普通 RAG 和层次化图记忆。

2. **检索是否找到了正确证据？**
   不能只看答案对错，还要看检索片段是否支持答案。

3. **长视频越长收益是否越明显？**
   如果视频变长后优势不扩大，说明方法可能没有真正解决 token explosion。

4. **成本是否可接受？**
   Agentic retrieval 会带来多轮检索和推理成本，需要量化。"""
    if is_tool_calling_knowledge(paper):
        return """实验至少要回答：经验知识从哪里来，激活是否精准，多步调用是否提升，失败恢复是否提升，未见工具和 schema 变化下是否还能工作。"""
    if is_interleaved_generation(paper):
        return """实验至少要回答：交错生成是否必要，强化信号是否有效，额外 token/步骤是否值得，失败轨迹是否比普通生成更容易诊断。"""
    if is_skill_scanner_security(paper):
        return """实验至少要回答：隐藏指令藏在哪里最难检测，良性安全技能误报率是多少，对抗改写后是否仍能定位证据，人工复核成本是否下降。"""
    if is_remote_sensing_dataset(paper):
        return """实验至少要回答：数据覆盖是否均衡，SAR/optical/language 是否对齐，任务是否真实，跨地区/跨传感器泛化是否比随机划分更有挑战。"""
    if is_unidrive(paper):
        return """这篇实验最少要回答四个问题：

1. **captioning 和 grounding 是否同时提升？**
   如果只有语言描述变好，不能说明风险理解更可信；如果只有框变准，不能说明解释更好。UniDrive 的卖点要求两者同时成立。

2. **小目标收益是否来自 high-resolution branch？**
   摘要强调 small-object localization，因此正文里应该能看到高分辨率分支和小目标指标之间的对应关系。

3. **零样本泛化是否只是数据集相近？**
   NuScenes 和 BDD100K 的零样本结果很重要，但要看输入协议、标注定义和风险类别是否与 DRAMA-Reasoning 足够接近。

4. **人工可解释性评分是否可信？**
   人评需要明确评分准则。否则“trustworthiness”容易变成主观偏好，而不是模型真的更忠实。"""
    return """实验至少要回答：主结果是否稳定、关键模块是否必要、泛化是否成立、失败案例是否解释了方法边界。"""


def write_paper_architecture_svg(paper: Paper, date: str) -> str:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{date}-paper-{slugify(paper.title)}-architecture.svg"
    path = ASSET_DIR / filename
    text = paper_text(paper)

    if is_long_video_memory(paper):
        boxes = [
            ("长视频", "clips / events"),
            ("感知写入", "objects / scenes"),
            ("图记忆", "hierarchy / edges"),
            ("主动检索", "query / evidence"),
            ("推理生成", "answer / trace"),
            ("验证", "long-range / cost"),
        ]
        caption = "长视频记忆论文阅读链路：先看证据如何写入，再看 agentic retrieval 是否能找回关键片段。"
    elif is_tool_calling_knowledge(paper):
        boxes = [
            ("任务", "tool need"),
            ("经验库", "success / failure"),
            ("知识激活", "retrieve / inject"),
            ("工具调用", "schema / args"),
            ("反馈修复", "error / retry"),
            ("评测", "multi-step"),
        ]
        caption = "工具调用论文阅读链路：经验如何进入工具选择、参数填写和失败恢复。"
    elif is_interleaved_generation(paper):
        boxes = [
            ("任务状态", "context"),
            ("思考片段", "reason"),
            ("动作/生成", "act / write"),
            ("观察反馈", "observe"),
            ("状态更新", "policy"),
            ("结果评测", "success / cost"),
        ]
        caption = "交错生成论文阅读链路：判断每次 thought/action/observation 是否改变后续决策。"
    elif is_skill_scanner_security(paper):
        boxes = [
            ("Skill 包", "md / yaml / script"),
            ("结构解析", "spans"),
            ("风险定位", "hidden instruction"),
            ("分类判断", "benign / malicious"),
            ("证据输出", "review"),
            ("部署处置", "block / allow"),
        ]
        caption = "Agent skill 安全论文阅读链路：从包解析到隐藏指令定位，再到可复核处置。"
    elif is_remote_sensing_dataset(paper):
        boxes = [
            ("SAR 图像", "structure"),
            ("光学图像", "semantics"),
            ("地理配准", "alignment"),
            ("语言标注", "caption / tags"),
            ("任务构造", "VQA / retrieval"),
            ("泛化评测", "region / sensor"),
        ]
        caption = "遥感多模态数据集阅读链路：重点看跨传感器对齐、语言质量和泛化划分。"
    elif is_unidrive(paper):
        boxes = [
            ("场景输入", "多帧 / 风险目标"),
            ("视觉表示", "区域 / 坐标 / 轨迹"),
            ("Grounding", "目标-证据绑定"),
            ("语言推理", "风险解释"),
            ("结构输出", "分类 / 定位 / 证据"),
            ("评测验证", "时序 / 空间 / 忠实度"),
        ]
        caption = "自动驾驶风险理解方法链路：从视觉证据到 grounded explanation，再到可验证的风险输出。"
    elif "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        boxes = [
            ("多模态输入", "image / video / audio"),
            ("编码压缩", "features / tokens"),
            ("跨模态对齐", "object / time / text"),
            ("推理模块", "memory / CoT / retrieval"),
            ("任务输出", "answer / caption / locate"),
            ("评测验证", "accuracy / faithfulness"),
        ]
        caption = "多模态论文阅读链路：重点看证据如何被保留、对齐和验证。"
    elif "agent" in text or "tool" in text or "skill" in text:
        boxes = [
            ("任务环境", "repo / GUI / tools"),
            ("状态表示", "memory / observation"),
            ("动作空间", "tool schema"),
            ("策略更新", "plan / feedback"),
            ("执行轨迹", "trace / cost"),
            ("结果评测", "success / failure"),
        ]
        caption = "Agent 论文阅读链路：从状态、动作、反馈到可复盘的执行轨迹。"
    else:
        boxes = [
            ("问题输入", "data / task"),
            ("中间表示", "state / feature"),
            ("核心机制", "module / loss"),
            ("输出结果", "prediction"),
            ("实验验证", "main / ablation"),
            ("边界分析", "failure / cost"),
        ]
        caption = "论文阅读链路：从问题输入到核心机制，再到实验验证和边界分析。"

    box_width = 150
    gap = 22
    start_x = 34
    y = 118
    width = start_x * 2 + len(boxes) * box_width + (len(boxes) - 1) * gap
    height = 330

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{svg_escape(paper.title)} 方法架构</title>",
        f"<desc id=\"desc\">{svg_escape(caption)}</desc>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#f0fdf4"/></linearGradient>',
        '<filter id="shadow" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.15"/></filter>',
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="18" fill="url(#bg)"/>',
        f'<text x="34" y="42" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">论文方法架构图</text>',
        f'<text x="34" y="70" font-family="Arial, sans-serif" font-size="14" fill="#475569">{svg_escape(caption)}</text>',
    ]

    for index, (title, subtitle) in enumerate(boxes):
        x = start_x + index * (box_width + gap)
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{box_width}" height="92" rx="12" fill="#ffffff" stroke="#bbf7d0" filter="url(#shadow)"/>',
                f'<text x="{x + box_width / 2}" y="{y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#14532d">{svg_escape(title)}</text>',
                f'<text x="{x + box_width / 2}" y="{y + 60}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#475569">{svg_escape(subtitle)}</text>',
            ]
        )
        if index < len(boxes) - 1:
            ax = x + box_width + 5
            bx = x + box_width + gap - 5
            parts.extend(
                [
                    f'<line x1="{ax}" y1="{y + 46}" x2="{bx}" y2="{y + 46}" stroke="#16a34a" stroke-width="2.5"/>',
                    f'<polygon points="{bx},{y + 46} {bx - 8},{y + 41} {bx - 8},{y + 51}" fill="#16a34a"/>',
                ]
            )

    parts.extend(
        [
            f'<rect x="34" y="248" width="{width - 68}" height="48" rx="10" fill="#dcfce7" stroke="#86efac"/>',
            f'<text x="54" y="278" font-family="Arial, sans-serif" font-size="14" fill="#14532d">读图顺序：逐层核对论文有没有给出可验证证据，尤其是中间表示、输出约束和实验指标是否闭环。</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return f"img/daily-reports/{filename}"


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


def build_deep_paper_section(paper: Paper, architecture_image: str, outline: tuple[str, ...] = ()) -> str:
    tags = "、".join(topic_tags(paper))
    categories = "、".join(paper.categories) if paper.categories else paper.primary_category or "未标注"
    questions = "\n".join(f"- {question}" for question in questions_for(paper))
    problem_lens, method_lens, experiment_lens, limitation_lens = contribution_lens(paper)
    outline_text = "\n".join(f"- {markdown_escape(heading)}" for heading in outline[:10])

    return f"""## [{markdown_escape(paper.title)}]({paper.abs_url})

- arXiv：[{paper.arxiv_id}]({paper.abs_url})
- PDF：[{paper.pdf_url}]({paper.pdf_url})
- 作者：{markdown_escape(authors_text(paper))}
- 发布时间：{date_only(paper.published)}，更新时间：{date_only(paper.updated)}
- 类别：{categories}
- 主题标签：{tags}

### 摘要速读

{markdown_escape(first_sentences(paper.abstract))}

### 先给结论

{paper_interpretation_intro(paper)}

### 这篇论文的核心主张

{paper_core_claims(paper)}

### 它抓住的矛盾

{paper_problem_interpretation(paper)}

### 全文结构线索

{outline_text if outline_text else "没有从 ar5iv 抓到可靠章节结构，因此这次先基于 arXiv 元数据和摘要做精读入口判断。正式阅读时仍应打开 PDF 核对 introduction、method、experiment 和 limitation。"}

### 一张图看方法

![{markdown_escape(paper.title)} 方法架构图](/{architecture_image})

这张图不是复述论文流程图，而是把阅读时最该盯住的证据链画出来：输入如何被表示，表示如何被 grounding 或推理模块消费，最后输出如何被实验指标验证。

### 方法架构拆分

{paper_architecture_breakdown(paper)}

### 模块拆解

{paper_module_interpretation(paper)}

### 方法链路细读

{paper_method_chain(paper)}

### 关键细节拆解

{paper_detail_breakdown(paper)}

### 方法成败点

{paper_method_success_conditions(paper)}

### 实验必须回答的问题

{paper_experiment_questions(paper)}

### 实验拆解清单

{paper_experiment_checklist(paper)}

### 实验结果怎么解读

{paper_result_interpretation(paper)}

### 局限和追问

{limitation_lens}

精读时重点追问：

{questions}

### 可以带走的东西

{paper_takeaway(paper)}
"""


def write_report_for_paper(paper: Paper, date: str, now: datetime | None = None) -> Path:
    generated_at = now or datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    path = POST_DIR / f"{date}-arxiv-llm-agent-papers.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    outline = fetch_paper_outline(paper)
    architecture_image = write_paper_architecture_svg(paper, date)
    top_section = build_deep_paper_section(paper, architecture_image, outline)

    content = f"""---
layout: post
title: "arXiv 论文精读：{yaml_escape(paper.title)} ({date})"
subtitle: "单篇论文深度拆解"
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

数据来源：[arXiv API]({ARXIV_API})。本篇围绕一篇论文做摘要、问题定义、方法线索、实验判断和局限追问。

阅读时优先关注四类问题：

1. 论文定义的问题是否清楚。
2. 方法里真正起作用的机制是什么。
3. 实验是否足以支撑主要结论。
4. 这篇论文能给工程或研究带来哪些可迁移经验。

# 1. 论文拆解

{top_section}

# 2. 阅读建议

正式阅读时建议按 introduction、method、experiment、limitation 的顺序走一遍，并把摘要里的核心 claim 逐条映射到实验表、消融实验和失败案例上。

生成时间：{generated_at.strftime("%Y-%m-%d %H:%M:%S %Z")}
"""
    path.write_text(content, encoding="utf-8")
    return path


def write_report(papers: list[Paper]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    ranked = sorted(papers, key=lambda paper: paper_score(paper)[0], reverse=True)
    return write_report_for_paper(ranked[0], date, now)


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


def parse_existing_report(path: Path) -> Paper:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^## \[([^\]\n]+)\]\((https?://arxiv\.org/abs/[^)]+)\)", content, re.MULTILINE)
    if not match:
        raise ValueError(f"could not find arXiv paper heading in {path}")

    title = normalize_text(match.group(1))
    abs_url = match.group(2).strip()
    section = content[match.end() :]
    next_heading = re.search(r"^## \[", section, re.MULTILINE)
    if next_heading:
        section = section[: next_heading.start()]

    arxiv_id = extract_arxiv_id(section) or parse_arxiv_id(abs_url)
    pdf_url = extract_markdown_link(section, "PDF") or f"https://arxiv.org/pdf/{arxiv_id}"
    authors = tuple(author for author in split_authors(extract_bullet_value(section, "作者")) if author)
    published, updated = extract_dates(section)
    categories = tuple(split_categories(extract_bullet_value(section, "类别")))
    abstract = extract_abstract(section)

    return Paper(
        arxiv_id=arxiv_id,
        title=title,
        abstract=abstract,
        authors=authors,
        abs_url=abs_url,
        pdf_url=pdf_url,
        published=published,
        updated=updated,
        primary_category=categories[0] if categories else "",
        categories=categories,
    )


def extract_bullet_value(section: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}：(.+)$", section, re.MULTILINE)
    return normalize_text(match.group(1)) if match else ""


def extract_markdown_link(section: str, label: str) -> str:
    value = extract_bullet_value(section, label)
    match = re.search(r"\((https?://[^)]+)\)", value)
    return match.group(1) if match else value


def extract_arxiv_id(section: str) -> str:
    value = extract_bullet_value(section, "arXiv")
    match = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", value)
    return match.group(1) if match else ""


def split_authors(value: str) -> list[str]:
    if not value or value == "未知":
        return ()
    return [
        item.strip()
        for item in re.split(r"[、,，]", value.replace("等", ""))
        if item.strip()
    ]


def split_categories(value: str) -> list[str]:
    if not value or value == "未标注":
        return []
    return [item.strip() for item in re.split(r"[、,，]", value) if item.strip()]


def extract_dates(section: str) -> tuple[str, str]:
    value = extract_bullet_value(section, "发布时间")
    match = re.search(r"(\d{4}-\d{2}-\d{2}).*?更新时间：(\d{4}-\d{2}-\d{2})", value)
    if match:
        return match.group(1), match.group(2)
    match = re.search(r"(\d{4}-\d{2}-\d{2})", value)
    if match:
        return match.group(1), match.group(1)
    return "", ""


def extract_abstract(section: str) -> str:
    match = re.search(r"### 摘要速读\s+(.+?)(?=\n### |\n## |\Z)", section, re.S)
    if not match:
        return ""
    return normalize_text(re.sub(r"\n+", " ", match.group(1)))


def rewrite_existing_report(path: Path, date: str) -> Path:
    parsed = parse_existing_report(path)
    paper = parsed
    try:
        fresh = fetch_papers_by_ids([parsed.arxiv_id])
        if fresh:
            paper = fresh[0]
    except (HTTPError, URLError, TimeoutError, ET.ParseError) as exc:
        print(f"warning: failed to refresh arXiv metadata for {parsed.arxiv_id}: {exc}", file=sys.stderr)
    return write_report_for_paper(paper, date)


def date_range(start: str, end: str) -> Iterable[str]:
    start_date = Date.fromisoformat(start)
    end_date = Date.fromisoformat(end)
    if end_date < start_date:
        raise ValueError("--backfill-to must be on or after --backfill-from")
    current = start_date
    while current <= end_date:
        yield current.isoformat()
        current += timedelta(days=1)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rewrite-existing", action="store_true", help="rewrite existing posts with the current paper-interpretation template")
    parser.add_argument("--date", help="single post date to rewrite, YYYY-MM-DD")
    parser.add_argument("--backfill-from", help="first date to rewrite, YYYY-MM-DD")
    parser.add_argument("--backfill-to", help="last date to rewrite, YYYY-MM-DD")
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    if args.rewrite_existing:
        if args.date:
            dates = [args.date]
        elif args.backfill_from and args.backfill_to:
            dates = list(date_range(args.backfill_from, args.backfill_to))
        else:
            print("error: --rewrite-existing needs --date or --backfill-from/--backfill-to", file=sys.stderr)
            return 2

        for date in dates:
            path = POST_DIR / f"{date}-arxiv-llm-agent-papers.md"
            if not path.exists():
                print(f"warning: skip missing {path.relative_to(ROOT)}", file=sys.stderr)
                continue
            report_path = rewrite_existing_report(path, date)
            print(f"rewrote {report_path.relative_to(ROOT)}")
            time.sleep(0.5)
        return 0

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
