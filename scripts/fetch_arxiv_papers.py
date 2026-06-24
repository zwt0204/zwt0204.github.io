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


def paper_architecture_breakdown(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "driving" in text or "autonomous driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "driving" in text or "autonomous driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "driving" in text or "autonomous driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "driving" in text or "autonomous driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
        return """这篇论文的核心不是再做一个“会描述驾驶场景”的多模态模型，而是在处理自动驾驶风险理解里一个很具体的矛盾：**视频模型有时间信息，但容易牺牲空间精度；高分辨率单帧模型看得清，但容易缺少动态上下文。**

UniDrive 的思路是把这两个能力拆开，再重新融合：一条分支负责多帧时序语义，一条分支负责最新帧的高分辨率空间细节，最后用 gated cross-attention 把“动态上下文”和“精确视觉证据”对齐。它最后不是只输出一句 caption，而是同时生成自然语言风险描述和风险对象的 bounding box。这个设计使它更像一个 **可解释风险理解框架**，而不只是自动驾驶场景 captioner。"""
    if "agent" in text or "tool" in text or "skill" in text:
        return """这篇论文要看的不是模型答题能力，而是 agent 在长程任务里如何维护状态、选择动作、接收反馈，并把失败路径变成下一步决策依据。解读时应该把它当作一个执行系统，而不是单轮推理模型。"""
    if "video" in text or "multimodal" in text or "vision" in text or "image" in text:
        return """这篇论文的重点在多模态信息如何被保留、对齐和验证。解读时不要只看最终指标，要追问视觉证据在进入语言模型之后是否仍然可定位、可解释、可复核。"""
    return """这篇论文需要按“问题矛盾 -> 方法主线 -> 实验证据 -> 边界条件”的顺序读。先判断它抓住的问题是否真实，再看方法是否针对这个问题，而不是被复杂模块带着走。"""


def paper_core_claims(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
        return """UniDrive 抓住的是自动驾驶场景理解里很典型的“鱼和熊掌”问题：

- 如果模型主要看视频，它能理解目标运动和场景变化，但为了控制 token / feature 成本，往往会降低分辨率或稀释空间细节。
- 如果模型主要看最新高分辨率单帧，它能看清小目标、远目标和遮挡区域，但缺少“这个风险是怎么形成的”的动态上下文。
- 如果模型只输出自然语言解释，即使文字合理，也很难判断它到底看到了哪个风险对象。

所以这篇论文的真正问题不是“让 MLLM 更会 caption”，而是：**能不能同时保留时间语义、空间精度和可验证 grounding。**"""
    return """这篇论文需要先拆清楚它面对的核心矛盾：现有方法到底缺的是数据、表示、推理、执行反馈，还是评测方式。只有矛盾明确，后面的模块才有判断标准。"""


def paper_module_interpretation(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
        return """UniDrive 的方法是否成立，主要看三个点：

1. **双分支是不是各司其职**
   temporal branch 应该负责动态语义，high-resolution branch 应该负责空间细节。正文里最好有消融能证明：去掉 temporal branch 会伤害时序/风险推理，去掉 high-resolution branch 会伤害小目标定位。

2. **gated cross-attention 是否真的在融合，而不是装饰模块**
   如果 gate 只是让参数变多，收益可能来自容量；如果 gate 在复杂场景、小目标场景、运动风险场景下表现出不同权重或显著消融收益，才说明它解决了“动态语义对齐空间证据”的问题。

3. **输出是不是形成解释闭环**
   自然语言风险描述和 bounding box grounding 必须互相支撑：文本说某个对象危险，框就要能定位到对应对象；框定位错了，文本解释的可信度也应该下降。"""
    return """方法是否成立，不能只看模块名称。要看每个模块是否对应问题矛盾，消融是否证明必要性，输出是否能被实验指标直接验证。"""


def paper_result_interpretation(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
        return """这篇论文真正值得带走的点，是把“自动驾驶解释”从纯文本描述拉回到 **时序证据 + 空间证据 + grounded object** 的闭环。对安全关键场景来说，解释不是越像人话越好，而是越能回指证据越好。

我会把它归类为一篇值得读方法结构的论文：不一定要照搬 UniDrive 的具体模块，但“动态语义一条支路、精细感知一条支路、再用 gated fusion 对齐”的问题拆法，对很多多模态风险理解任务都有参考价值。"""
    return """这篇论文的价值不只在最终指标，而在它如何拆问题、设计中间表示、把结果变成可验证证据。读完后应该能回答：它解决了什么矛盾，哪个模块真正解决这个矛盾，实验有没有支撑这个解释。"""


def paper_experiment_questions(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "unidrive" in text or "autonomous driving" in text or "driving" in text:
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
    text = f"{paper.title} {paper.abstract}".lower()

    if "driving" in text or "autonomous driving" in text:
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


def write_report(papers: list[Paper]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    path = POST_DIR / f"{date}-arxiv-llm-agent-papers.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    ranked = sorted(papers, key=lambda paper: paper_score(paper)[0], reverse=True)
    pick = ranked[0]
    outline = fetch_paper_outline(pick)
    architecture_image = write_paper_architecture_svg(pick, date)
    top_section = build_deep_paper_section(pick, architecture_image, outline)

    content = f"""---
layout: post
title: "arXiv 论文精读：{yaml_escape(pick.title)} ({date})"
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
