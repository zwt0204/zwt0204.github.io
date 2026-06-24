#!/usr/bin/env python3
"""Fetch GitHub Trending and publish a Chinese learning report."""

from __future__ import annotations

import html
import json
import re
import sys
import time
from base64 import b64decode
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "_posts" / "github"
DATA_PATH = ROOT / "docs" / "trending.json"
TRENDING_URL = "https://github.com/trending?since=daily"
USER_AGENT = "ztw0204.github.io trending learner bot"
MAX_PROJECTS = 15
LOCAL_TZ = ZoneInfo("Asia/Shanghai")


@dataclass
class Repo:
    owner: str
    name: str
    url: str
    description: str = ""
    language: str = ""
    stars: int = 0
    forks: int = 0
    today_stars: int = 0
    topics: tuple[str, ...] = ()
    homepage: str = ""
    default_branch: str = ""
    readme: str = ""
    key_files: tuple[str, ...] = ()

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


class TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.repos: list[Repo] = []
        self._in_article = False
        self._current: dict[str, object] | None = None
        self._capture: str | None = None
        self._text: list[str] = []
        self._link_count = 0
        self._in_lang = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        classes = set(attr.get("class", "").split())

        if tag == "article" and "Box-row" in classes:
            self._in_article = True
            self._current = {
                "owner": "",
                "name": "",
                "url": "",
                "description": "",
                "language": "",
                "stars": 0,
                "forks": 0,
                "today_stars": 0,
            }
            self._link_count = 0
            self._in_title = False
            return

        if not self._in_article or self._current is None:
            return

        if tag == "h2":
            self._in_title = True
            self._capture = "title"
            self._text = []
        elif tag == "p" and "col-9" in classes:
            self._capture = "description"
            self._text = []
        elif tag == "span" and "repo-language-color" in classes:
            self._in_lang = True
        elif tag == "a" and attr.get("href", "").startswith("/"):
            href = attr["href"]
            if self._in_title and is_repo_href(href):
                self._link_count += 1
                parts = href.strip("/").split("/", 1)
                self._current["owner"] = parts[0]
                self._current["name"] = parts[1]
                self._current["url"] = f"https://github.com{href}"
            elif not self._in_title and is_repo_metric_href(href):
                self._link_count += 1
                if self._link_count == 2:
                    self._capture = "stars"
                    self._text = []
                elif self._link_count == 3:
                    self._capture = "forks"
                    self._text = []
        elif tag == "span" and "d-inline-block" in classes and "float-sm-right" in classes:
            self._capture = "today_stars"
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if not self._in_article or self._current is None:
            return

        if tag == "article":
            owner = str(self._current.get("owner", "")).strip()
            name = str(self._current.get("name", "")).strip()
            if owner and name:
                self.repos.append(
                    Repo(
                        owner=owner,
                        name=name,
                        url=str(self._current["url"]),
                        description=str(self._current.get("description", "")).strip(),
                        language=str(self._current.get("language", "")).strip(),
                        stars=int(self._current.get("stars", 0)),
                        forks=int(self._current.get("forks", 0)),
                        today_stars=int(self._current.get("today_stars", 0)),
                    )
                )
            self._in_article = False
            self._current = None
            self._capture = None
            self._text = []
            return

        if self._capture and tag in {"h2", "p", "a", "span"}:
            value = normalize_text(" ".join(self._text))
            if self._capture == "title":
                parts = [part.strip() for part in value.split("/") if part.strip()]
                if len(parts) >= 2:
                    self._current["owner"] = parts[0]
                    self._current["name"] = parts[1]
                    self._current["url"] = f"https://github.com/{parts[0]}/{parts[1]}"
            elif self._capture == "description":
                self._current["description"] = value
            elif self._capture in {"stars", "forks", "today_stars"}:
                self._current[self._capture] = parse_count(value)
            self._capture = None
            self._text = []

        if tag == "h2":
            self._in_title = False
        if tag == "span":
            self._in_lang = False

    def handle_data(self, data: str) -> None:
        if not self._in_article or self._current is None:
            return
        if self._capture:
            self._text.append(data)
        elif self._in_lang:
            value = data.strip()
            if value:
                self._current["language"] = value


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def parse_count(value: str) -> int:
    match = re.search(r"([\d,.]+)\s*([kKmM]?)", value.replace(",", ""))
    if not match:
        return 0
    number = float(match.group(1))
    suffix = match.group(2).lower()
    if suffix == "k":
        number *= 1_000
    elif suffix == "m":
        number *= 1_000_000
    return int(number)


def is_repo_href(href: str) -> bool:
    if not re.fullmatch(r"/[^/\s]+/[^/\s#?]+", href):
        return False
    owner, name = href.strip("/").split("/", 1)
    blocked = {"account", "apps", "collections", "customer-stories", "events", "explore", "features", "marketplace", "new", "notifications", "orgs", "pricing", "sponsors", "topics", "trending"}
    return owner not in blocked and not name.startswith(("-", "."))


def is_repo_metric_href(href: str) -> bool:
    if not re.fullmatch(r"/[^/\s]+/[^/\s#?]+/(stargazers|forks)", href):
        return False
    owner = href.strip("/").split("/", 1)[0]
    return owner not in {"sponsors", "orgs"}


def get_url(url: str, accept: str = "text/html") -> str:
    request = Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and 400 <= exc.code < 500:
                raise
            time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def fetch_trending() -> list[Repo]:
    parser = TrendingParser()
    parser.feed(get_url(TRENDING_URL))
    return parser.repos[:MAX_PROJECTS]


def enrich_repo(repo: Repo) -> Repo:
    api_url = f"https://api.github.com/repos/{quote(repo.owner)}/{quote(repo.name)}"
    try:
        payload = json.loads(get_url(api_url, accept="application/vnd.github+json"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"warning: failed to enrich {repo.full_name}: {exc}", file=sys.stderr)
        return repo

    return Repo(
        owner=repo.owner,
        name=repo.name,
        url=repo.url,
        description=payload.get("description") or repo.description,
        language=payload.get("language") or repo.language,
        stars=int(payload.get("stargazers_count") or repo.stars),
        forks=int(payload.get("forks_count") or repo.forks),
        today_stars=repo.today_stars,
        topics=tuple(payload.get("topics") or ()),
        homepage=payload.get("homepage") or "",
        default_branch=payload.get("default_branch") or "",
        readme=repo.readme,
        key_files=repo.key_files,
    )


def enrich_reading_context(repo: Repo) -> Repo:
    readme = fetch_readme(repo)
    key_files = fetch_key_files(repo)
    return replace(repo, readme=readme, key_files=key_files)


def fetch_readme(repo: Repo) -> str:
    api_url = f"https://api.github.com/repos/{quote(repo.owner)}/{quote(repo.name)}/readme"
    try:
        payload = json.loads(get_url(api_url, accept="application/vnd.github+json"))
        content = payload.get("content") or ""
        if payload.get("encoding") == "base64" and content:
            return b64decode(content).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        print(f"warning: failed to fetch README for {repo.full_name}: {exc}", file=sys.stderr)
    return ""


def fetch_key_files(repo: Repo) -> tuple[str, ...]:
    if not repo.default_branch:
        return ()
    branch = quote(repo.default_branch, safe="")
    api_url = f"https://api.github.com/repos/{quote(repo.owner)}/{quote(repo.name)}/git/trees/{branch}?recursive=1"
    try:
        payload = json.loads(get_url(api_url, accept="application/vnd.github+json"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"warning: failed to fetch file tree for {repo.full_name}: {exc}", file=sys.stderr)
        return ()
    paths = [
        item.get("path", "")
        for item in payload.get("tree", [])
        if item.get("type") == "blob" and item.get("path")
    ]
    return select_key_files(paths)


def select_key_files(paths: list[str], limit: int = 18) -> tuple[str, ...]:
    priority: list[tuple[int, str]] = []
    for path in paths:
        lower = path.lower()
        name = lower.rsplit("/", 1)[-1]
        score = 0
        if name in {"readme.md", "package.json", "pyproject.toml", "cargo.toml", "go.mod", "setup.py", "makefile", "dockerfile"}:
            score += 10
        if lower.startswith(("src/", "app/", "lib/", "crates/", "packages/", "cmd/", "internal/", "cli/")):
            score += 5
        if lower.startswith(("tests/", "test/", "examples/", "docs/")):
            score += 3
        if any(token in name for token in ("main", "cli", "agent", "tool", "memory", "server", "api", "config", "test")):
            score += 4
        if score:
            priority.append((score, path))
    priority.sort(key=lambda item: (-item[0], item[1]))
    return tuple(path for _, path in priority[:limit])


def learning_value(repo: Repo) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    text = f"{repo.full_name} {repo.description}".lower()
    topics = {topic.lower() for topic in repo.topics}
    signals = (
        (("ai", "artificial-intelligence"), "AI / LLM", 4),
        (("llm", "large-language-model"), "大模型工程", 4),
        (("agent", "agents", "ai-agent", "ai-agents"), "智能体实践", 4),
        (("rust",), "Rust 系统能力", 3),
        (("go", "golang"), "Go 后端工程", 3),
        (("typescript", "ts"), "TypeScript 前端工程", 3),
        (("python",), "Python 生态", 3),
        (("database", "db", "postgres", "postgresql"), "数据系统", 3),
        (("compiler", "parser", "runtime"), "编译器/语言实现", 4),
        (("security", "sec", "osint"), "安全工程", 4),
        (("kubernetes", "k8s"), "云原生", 3),
        (("observability", "tracing", "metrics"), "可观测性", 3),
        (("framework",), "框架设计", 2),
        (("cli", "command-line"), "命令行工具设计", 2),
    )
    for keys, reason, weight in signals:
        if any(has_signal(text, topics, key) for key in keys):
            score += weight
            reasons.append(reason)

    if repo.today_stars >= 500:
        score += 4
        reasons.append("今日关注度极高")
    elif repo.today_stars >= 150:
        score += 2
        reasons.append("今日增长明显")
    if repo.stars >= 10_000:
        score += 2
        reasons.append("社区验证充分")
    if repo.topics:
        score += 1
        reasons.append("主题标签清晰")

    return min(score, 20), dedupe(reasons)


def has_signal(text: str, topics: set[str], key: str) -> bool:
    if key in topics:
        return True
    return re.search(rf"(?<![a-z0-9]){re.escape(key)}(?![a-z0-9])", text) is not None


def reading_focus_for(repo: Repo) -> str:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)}".lower()
    language = (repo.language or "").lower()
    focus = [
        "1. 入口层：看它把 CLI、Web、SDK 或配置文件暴露成怎样的用户接口。",
        "2. 核心层：找最稳定的领域模型、调度逻辑、状态管理或数据结构。",
        "3. 边界层：关注外部服务、文件系统、网络请求、模型调用或数据库访问如何被隔离。",
    ]

    if "agent" in text or "llm" in text or "ai" in repo.topics:
        focus.append("4. Agent/LLM 链路：重点看工具调用、上下文管理、权限控制、失败重试和可观测日志。")
    elif "database" in text or "postgres" in text or "db" in repo.topics:
        focus.append("4. 数据链路：重点看事务边界、索引/存储结构、并发控制、恢复策略和压测方式。")
    elif "security" in text or "osint" in text or "sec" in repo.topics:
        focus.append("4. 安全链路：重点看输入校验、权限边界、敏感信息处理和误报/漏报控制。")
    elif language in {"rust", "c", "c++", "go"}:
        focus.append("4. 系统链路：重点看内存/并发模型、错误类型、性能基准和平台兼容性。")
    elif language in {"typescript", "javascript"}:
        focus.append("4. 前端/Node 链路：重点看状态组织、构建配置、插件机制、组件边界和端到端测试。")
    elif language == "python":
        focus.append("4. Python 链路：重点看包结构、类型标注、异步/并发处理、依赖隔离和测试夹具。")
    else:
        focus.append("4. 质量链路：重点看测试、示例、CI、发布脚本和文档是否能支撑长期维护。")

    return "\n".join(focus)


def readme_signals(repo: Repo) -> str:
    if not repo.readme:
        return "README 暂时没有抓取到，先从仓库目录、示例和测试进入。"

    headings: list[str] = []
    paragraphs: list[str] = []
    for raw_line in repo.readme.splitlines():
        line = normalize_text(raw_line.strip("# ").strip())
        if not line:
            continue
        if raw_line.lstrip().startswith("#") and len(headings) < 6:
            headings.append(line)
        elif not raw_line.lstrip().startswith(("-", "*", "[", "!", "`", "|")) and len(paragraphs) < 3:
            paragraphs.append(line)

    parts: list[str] = []
    if headings:
        parts.append("README 结构：" + " / ".join(headings[:6]))
    if paragraphs:
        parts.append("开篇信息：" + " ".join(paragraphs)[:520].rstrip())
    return "\n".join(f"- {part}" for part in parts) if parts else "README 已抓取，但没有提取到明显标题或开篇段落。"


def key_file_signals(repo: Repo) -> str:
    if not repo.key_files:
        return "- 暂时没有抓取到文件树，先从 README、示例目录和测试目录进入。"
    return "\n".join(f"- `{path}`" for path in repo.key_files[:12])


def project_type(repo: Repo) -> str:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)}".lower()
    language = (repo.language or "").lower()
    if "agent" in text or "llm" in text or "ai" in text:
        return "AI/Agent 工程项目"
    if "database" in text or "postgres" in text or "db" in text:
        return "数据系统项目"
    if "compiler" in text or "runtime" in text or "parser" in text:
        return "编译器/运行时项目"
    if "security" in text or "osint" in text:
        return "安全工具项目"
    if language in {"rust", "c", "c++", "go"}:
        return "系统工程项目"
    if language in {"typescript", "javascript"}:
        return "前端/Node 工程项目"
    if language == "python":
        return "Python 工具或框架项目"
    return "开源工程项目"


def deep_reading_sections(repo: Repo) -> tuple[str, str, str, str]:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)}".lower()
    language = (repo.language or "").lower()

    if "agent" in text or "llm" in text or "ai" in text:
        core_question = "它是否把“模型调用”包装成了可靠的软件系统：任务状态如何保存，工具权限如何收口，失败后如何重试或回滚，日志是否足够复盘一次 agent 行为。"
        architecture_path = "建议从用户入口读到 agent loop：先找 CLI/Web/API 入口，再追踪 request 如何变成 plan、tool call、observation、memory/context update，最后看结果如何返回给用户。"
        risk_points = "重点警惕三类风险：工具调用边界不清导致越权，长上下文堆叠导致状态漂移，以及错误恢复只靠 prompt 而没有工程级保护。"
        reusable_lessons = "真正可复用的经验通常在 provider 抽象、tool registry、权限模型、执行日志、配置加载和测试夹具里，而不是某个具体 prompt。"
    elif "database" in text or "postgres" in text or "db" in text:
        core_question = "它是否解决了一个明确的数据一致性、性能或运维问题，而不是只在现有数据库外面包一层 API。"
        architecture_path = "建议顺着写入路径读：入口参数如何校验，事务/锁/索引如何组织，异常时如何恢复，再看 benchmark 是否覆盖真实负载。"
        risk_points = "重点看并发、崩溃恢复、数据迁移和边界条件；数据系统的价值不在 happy path，而在异常路径能否解释清楚。"
        reusable_lessons = "可迁移经验主要是状态机设计、持久化边界、测试数据构造、压测方法和可观测指标。"
    elif language in {"rust", "c", "c++", "go"}:
        core_question = "它是否通过语言和架构选择换来了可解释的性能、可靠性或部署优势。"
        architecture_path = "建议先读公开 API，再下钻核心数据结构、并发模型和错误类型，最后看 benchmark 与 CI 覆盖了哪些平台。"
        risk_points = "重点看 unsafe/并发/资源释放/跨平台兼容；系统项目的隐患通常藏在边界条件和性能假设里。"
        reusable_lessons = "可复用的是模块边界、错误建模、压测方式、发布包组织和对外 API 稳定策略。"
    else:
        core_question = "它是否把一个真实用户问题收敛成了清楚、可维护、可扩展的工程接口。"
        architecture_path = "建议先读 README 的最小例子，再找入口文件、核心抽象、配置系统、测试目录和发布流程。"
        risk_points = "重点看项目是否只有 demo 级路径，还是对错误处理、兼容性、版本升级和用户迁移有清楚设计。"
        reusable_lessons = "可复用的是问题切分方式、默认配置、扩展点设计、测试组织和文档写法。"

    return core_question, architecture_path, risk_points, reusable_lessons


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def build_deep_analysis(repo: Repo, alternatives: list[Repo]) -> str:
    score, reasons = learning_value(repo)
    reasons_text = "、".join(reasons) if reasons else "项目方向清晰，适合做源码阅读样本"
    topics = "、".join(repo.topics[:6]) if repo.topics else "暂无"
    homepage = f"\n- 官网/演示：[{repo.homepage}]({repo.homepage})" if repo.homepage else ""
    description = (repo.description or "项目暂未提供简介，需要从 README 和代码结构进一步判断。").strip()
    language = repo.language or "未标注"
    reading_focus = reading_focus_for(repo)
    core_question, architecture_path, risk_points, reusable_lessons = deep_reading_sections(repo)
    alternative_rows = "\n".join(
        f"- [{item.full_name}]({item.url})：评分 {learning_value(item)[0]}/20，{(item.description or '暂无简介').strip()}"
        for item in alternatives[:4]
    )

    return f"""## 今日只读这一个：[{repo.full_name}]({repo.url})

- 语言：{language}
- Stars：{repo.stars:,}，Forks：{repo.forks:,}，今日新增：{repo.today_stars:,}
- Topics：{topics}{homepage}
- 学习价值评分：{score}/20
- 项目类型：{project_type(repo)}

**项目简介**：{description}

### 为什么今天选它，而不是泛读一堆

{reasons_text}。今天的目标不是把 Trending 里所有项目都扫一遍，而是选一个最值得投入 30-60 分钟的样本。这个项目的价值不只在功能本身，更在于它能暴露一组可迁移的工程问题：用户入口如何定义、核心抽象是否稳定、外部依赖如何隔离、失败路径是否可观测。

### 这次精读要回答的核心问题

{core_question}

如果读完只能留下一个判断，就应该是：这个项目到底靠什么建立护城河，是增长热度、工程设计、生态位置，还是某个可复用的技术抽象。

### 建议顺着这条链路读

{architecture_path}

### README 和代码结构线索

{readme_signals(repo)}

值得优先打开的文件或目录：

{key_file_signals(repo)}

具体可以按这个顺序推进：

{reading_focus}

### 读代码时要特别检查的地方

1. 先读 README，确认项目解决的真实问题和目标用户。
2. 找最小可运行例子，顺着入口追到核心实现，不要停在安装命令。
3. 画出核心对象之间的关系：谁负责状态，谁负责 IO，谁负责策略，谁负责错误处理。
4. 对照测试、Issue、Release，看维护者真正花时间处理的是功能扩张、性能、兼容性还是稳定性。
5. 最后回看配置、日志、扩展点和失败回退，这些地方最能反映项目是否可长期维护。

### 风险与局限

{risk_points}

Trending 项目还要额外注意热度偏差：短期 star 增长只能说明被看见，不等于架构成熟。精读时不要只看 README 的宣传语，要至少追一条真实执行路径。

### 可以带走的工程经验

{reusable_lessons}

### 其它候选为什么先不展开

{alternative_rows if alternative_rows else "- 今天没有足够多的其它候选。"}
"""


def write_report(repos: list[Repo]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    path = POST_DIR / f"{date}-github-trending-learning-report.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    ranked = sorted(repos, key=lambda item: learning_value(item)[0], reverse=True)
    pick = enrich_reading_context(ranked[0])
    body = build_deep_analysis(pick, ranked[1:])
    all_rows = "\n".join(
        f"| [{repo.full_name}]({repo.url}) | {repo.language or '-'} | {repo.stars:,} | {repo.today_stars:,} | {(repo.description or '-').strip()} |"
        for repo in repos
    )

    content = f"""---
layout: post
title: "GitHub Trending 精读：{pick.full_name} ({date})"
subtitle: "每天只选一个开源项目深读"
date: {date}
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

# GitHub Trending 精读 {date}

数据来源：[GitHub Trending Daily]({TRENDING_URL})。本篇自动抓取当日 Trending 仓库，但正文只选一个项目深读；其它项目只保留在候选表里，避免把日报写成一组浅摘要。

## 筛选逻辑

我会优先关注四类信号：

1. 是否代表一个正在变热的技术方向，例如 AI agent、LLM infra、数据库、编译器、云原生或安全工具。
2. 是否有明确的工程入口，适合顺着 README、示例、CLI/API 和测试一路读到核心实现。
3. 是否有足够的社区反馈，包括 star、fork、issue、release 或 topic。
4. 是否能沉淀可迁移经验，例如架构边界、扩展机制、错误处理、性能优化或文档组织。

## 今日重点项目

{body}

## 全量候选列表

| 项目 | 语言 | Stars | 今日新增 | 简介 |
| --- | --- | ---: | ---: | --- |
{all_rows}

---

生成时间：{now.strftime("%Y-%m-%d %H:%M:%S %Z")}
"""
    path.write_text(content, encoding="utf-8")
    return path


def write_data(repos: list[Repo]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(
            [
                {
                    "full_name": repo.full_name,
                    "url": repo.url,
                    "description": repo.description,
                    "language": repo.language,
                    "stars": repo.stars,
                    "forks": repo.forks,
                    "today_stars": repo.today_stars,
                    "topics": list(repo.topics),
                    "homepage": repo.homepage,
                    "learning_score": learning_value(repo)[0],
                }
                for repo in repos
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    repos = fetch_trending()
    if not repos:
        print("error: no repositories parsed from GitHub Trending", file=sys.stderr)
        return 1

    enriched = [enrich_repo(repo) for repo in repos]
    report_path = write_report(enriched)
    write_data(enriched)
    print(f"wrote {report_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
