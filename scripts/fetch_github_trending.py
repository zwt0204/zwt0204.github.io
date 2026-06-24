#!/usr/bin/env python3
"""Fetch GitHub Trending and publish a Chinese learning report."""

from __future__ import annotations

import html
import json
import os
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
ASSET_DIR = ROOT / "img" / "daily-reports"
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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:80].strip("-") or "github-project"


def svg_escape(value: str) -> str:
    return html.escape(normalize_text(value), quote=True)


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
    headers = {
        "Accept": accept,
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        url,
        headers=headers,
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
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(("<", "[!", "![", "|")):
            continue
        line = normalize_text(stripped.strip("# ").strip())
        if not line:
            continue
        if stripped.startswith("#") and len(headings) < 6:
            headings.append(line)
        elif not stripped.startswith(("-", "*", "[", "!", "`")) and len(paragraphs) < 3:
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


def key_file_breakdown(repo: Repo) -> str:
    if not repo.key_files:
        return "文件树暂时没有抓取到。正式阅读时先找 README、配置文件、入口脚本、核心目录、示例和测试目录，补齐下面的架构判断。"

    rows = ["| 文件/目录 | 阅读重点 |", "| --- | --- |"]
    for path in repo.key_files[:12]:
        lower = path.lower()
        if "readme" in lower:
            focus = "确认项目承诺、安装方式、核心概念和使用边界。"
        elif "/mappings/" in lower or lower.startswith("mappings/"):
            focus = "看领域知识如何映射到外部标准、框架或分类体系。"
        elif "/skills/" in lower or lower.startswith("skills/"):
            focus = "看单个能力单元的目录结构、输入输出、脚本与参考资料如何组合。"
        elif "/scripts/" in lower or lower.endswith(".py"):
            focus = "追踪可执行逻辑，确认脚本承担的是采集、转换、执行还是验证。"
        elif "/tools/" in lower or lower.startswith("tools/"):
            focus = "看项目提供了哪些辅助工具，以及这些工具是否形成稳定维护入口。"
        elif "config" in lower or lower.endswith((".yml", ".yaml", ".toml", ".json")):
            focus = "看配置约束、默认行为、兼容平台和发布/集成方式。"
        elif "test" in lower:
            focus = "看测试覆盖的是数据结构、转换规则、执行脚本还是端到端路径。"
        else:
            focus = "用于定位项目的核心边界和上下游依赖。"
        rows.append(f"| `{path}` | {focus} |")
    return "\n".join(rows)


def write_github_architecture_svg(repo: Repo, date: str) -> str:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{date}-github-{slugify(repo.full_name)}-architecture.svg"
    path = ASSET_DIR / filename
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)} {' '.join(repo.key_files)}".lower()

    if "skill" in text and ("security" in text or "cyber" in text or "mitre" in text):
        boxes = [
            ("Skill 文件", "目标、前提、步骤"),
            ("标准映射", "MITRE / NIST / OWASP"),
            ("参考资料", "API、命令、证据"),
            ("执行脚本", "agent.py / tools"),
            ("平台适配", "Claude / Codex / IDE"),
            ("治理更新", "版本、重复、风险"),
        ]
        caption = "安全技能库的核心链路：把安全领域知识结构化，再映射到标准框架和 agent 可执行入口。"
    elif "agent" in text or "llm" in text or "ai" in text:
        boxes = [
            ("用户入口", "CLI / Web / SDK"),
            ("任务编排", "plan / action / observe"),
            ("工具注册", "schema / permission"),
            ("上下文层", "memory / retrieval"),
            ("模型适配", "provider / cost"),
            ("观测测试", "trace / replay"),
        ]
        caption = "Agent 项目的主链路：用户目标进入系统，经过任务编排、工具调用和状态更新后返回结果。"
    else:
        boxes = [
            ("用户入口", "API / CLI"),
            ("核心抽象", "domain model"),
            ("边界适配", "IO / service"),
            ("配置扩展", "plugin / config"),
            ("质量保障", "tests / CI"),
            ("发布维护", "version / docs"),
        ]
        caption = "开源项目阅读主链路：先找入口，再追核心抽象和边界适配。"

    box_width = 150
    gap = 22
    start_x = 34
    y = 118
    width = start_x * 2 + len(boxes) * box_width + (len(boxes) - 1) * gap
    height = 330

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{svg_escape(repo.full_name)} 架构拆解</title>",
        f"<desc id=\"desc\">{svg_escape(caption)}</desc>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#eef6ff"/></linearGradient>',
        '<filter id="shadow" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.16"/></filter>',
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="18" fill="url(#bg)"/>',
        f'<text x="34" y="42" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">{svg_escape(repo.name)} 架构阅读图</text>',
        f'<text x="34" y="70" font-family="Arial, sans-serif" font-size="14" fill="#475569">{svg_escape(caption)}</text>',
    ]

    for index, (title, subtitle) in enumerate(boxes):
        x = start_x + index * (box_width + gap)
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{box_width}" height="92" rx="12" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>',
                f'<text x="{x + box_width / 2}" y="{y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#0f172a">{svg_escape(title)}</text>',
                f'<text x="{x + box_width / 2}" y="{y + 60}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#475569">{svg_escape(subtitle)}</text>',
            ]
        )
        if index < len(boxes) - 1:
            ax = x + box_width + 5
            bx = x + box_width + gap - 5
            parts.extend(
                [
                    f'<line x1="{ax}" y1="{y + 46}" x2="{bx}" y2="{y + 46}" stroke="#2563eb" stroke-width="2.5"/>',
                    f'<polygon points="{bx},{y + 46} {bx - 8},{y + 41} {bx - 8},{y + 51}" fill="#2563eb"/>',
                ]
            )

    parts.extend(
        [
            f'<rect x="34" y="248" width="{width - 68}" height="48" rx="10" fill="#dbeafe" stroke="#93c5fd"/>',
            f'<text x="54" y="278" font-family="Arial, sans-serif" font-size="14" fill="#1e3a8a">读图顺序：先确认每层输入输出，再看相邻层之间是否有明确格式、权限、错误处理和可观测证据。</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return f"img/daily-reports/{filename}"


def write_github_call_chain_svg(repo: Repo, date: str) -> str:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{date}-github-{slugify(repo.full_name)}-call-chain.svg"
    path = ASSET_DIR / filename
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)} {' '.join(repo.key_files)}".lower()

    if "skill" in text and ("security" in text or "cyber" in text or "mitre" in text):
        boxes = [
            ("index.json", "skill registry"),
            ("SKILL.md", "frontmatter + workflow"),
            ("references/", "standards + API"),
            ("scripts/agent.py", "argparse entry"),
            ("mode branch", "enumerate / impacket / sharpdpapi"),
            ("run_cmd()", "external tool boundary"),
        ]
        caption = "代表性 skill 的代码调用链：先由索引定位，再加载 SKILL.md，最后进入脚本编排外部安全工具。"
    elif "agent" in text or "llm" in text or "ai" in text:
        boxes = [
            ("入口", "CLI / Web / SDK"),
            ("任务对象", "request / context"),
            ("Planner", "plan / step"),
            ("Tool call", "schema / permission"),
            ("Observation", "result / error"),
            ("Trace", "log / replay"),
        ]
        caption = "Agent 项目的代码调用链：用户请求被编排成工具调用，再用 observation 更新状态。"
    else:
        boxes = [
            ("入口", "API / CLI"),
            ("解析", "config / args"),
            ("核心对象", "domain model"),
            ("执行", "service / adapter"),
            ("错误处理", "result / exception"),
            ("输出", "report / state"),
        ]
        caption = "项目代码调用链：从入口参数到核心对象，再到边界适配和输出。"

    box_width = 150
    gap = 22
    start_x = 34
    y = 118
    width = start_x * 2 + len(boxes) * box_width + (len(boxes) - 1) * gap
    height = 330

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{svg_escape(repo.full_name)} 代码调用链</title>",
        f"<desc id=\"desc\">{svg_escape(caption)}</desc>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#fff7ed"/><stop offset="100%" stop-color="#eff6ff"/></linearGradient>',
        '<filter id="shadow" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.15"/></filter>',
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="18" fill="url(#bg)"/>',
        f'<text x="34" y="42" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">代码调用链阅读图</text>',
        f'<text x="34" y="70" font-family="Arial, sans-serif" font-size="14" fill="#475569">{svg_escape(caption)}</text>',
    ]

    for index, (title, subtitle) in enumerate(boxes):
        x = start_x + index * (box_width + gap)
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{box_width}" height="92" rx="12" fill="#ffffff" stroke="#fed7aa" filter="url(#shadow)"/>',
                f'<text x="{x + box_width / 2}" y="{y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#7c2d12">{svg_escape(title)}</text>',
                f'<text x="{x + box_width / 2}" y="{y + 60}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#475569">{svg_escape(subtitle)}</text>',
            ]
        )
        if index < len(boxes) - 1:
            ax = x + box_width + 5
            bx = x + box_width + gap - 5
            parts.extend(
                [
                    f'<line x1="{ax}" y1="{y + 46}" x2="{bx}" y2="{y + 46}" stroke="#ea580c" stroke-width="2.5"/>',
                    f'<polygon points="{bx},{y + 46} {bx - 8},{y + 41} {bx - 8},{y + 51}" fill="#ea580c"/>',
                ]
            )

    parts.extend(
        [
            f'<rect x="34" y="248" width="{width - 68}" height="48" rx="10" fill="#ffedd5" stroke="#fdba74"/>',
            f'<text x="54" y="278" font-family="Arial, sans-serif" font-size="14" fill="#7c2d12">读图顺序：把每个文件当成调用链上的一环，重点看输入、分支、外部命令边界和错误返回。</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return f"img/daily-reports/{filename}"


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


def architecture_breakdown(repo: Repo) -> str:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)} {' '.join(repo.key_files)}".lower()
    if "skill" in text and ("security" in text or "cyber" in text or "mitre" in text):
        return """1. **领域知识层**：仓库的核心不是一个单一运行时，而是一批结构化安全技能。需要先看每个 skill 如何描述目标、适用场景、参考资料和执行步骤。
2. **标准映射层**：`mappings/` 这类目录通常负责把技能映射到 MITRE ATT&CK、NIST、OWASP 等外部框架。这里决定了项目是否只是文件集合，还是可检索、可治理的知识库。
3. **执行脚本层**：`skills/*/scripts/agent.py` 这类文件是关键细节。它们说明 skill 是否只是一段说明文字，还是包含可执行的检查、采集或分析动作。
4. **参考资料层**：`references/api-reference.md` 这类文件用于把操作步骤落到具体 API、命令或工具上。这里要看引用是否足够具体，是否能被 agent 稳定消费。
5. **工具与平台适配层**：README 里提到多个 AI coding/agent 平台时，要确认仓库是否提供统一格式，还是每个平台靠人工约定兼容。
6. **维护与质量层**：这类知识库的长期价值取决于版本同步、重复技能治理、标准更新和安全误用边界，而不只是条目数量。"""
    if "agent" in text or "llm" in text or "ai" in text:
        return """1. **用户入口层**：先确认项目暴露的是 CLI、Web、SDK、插件还是配置文件。入口决定用户目标如何进入系统。
2. **任务编排层**：看任务如何被拆成 plan、tool call、observation、state update，以及失败后如何回到上一层。
3. **工具注册层**：关注工具 schema、权限、参数校验、超时、重试和日志。agent 项目的稳定性通常卡在这里。
4. **上下文/记忆层**：看 prompt、短期状态、长期记忆、检索结果如何合并，以及是否有预算控制。
5. **模型适配层**：看不同模型 provider 是否被隔离，错误码、速率限制、流式输出和成本统计是否有统一封装。
6. **观测与测试层**：重点看 trace、事件日志、回放、fixtures 和端到端测试，否则很难复盘长任务失败。"""
    if "database" in text or "postgres" in text or "db" in text:
        return """1. **API 层**：确认读写入口和用户能控制的参数。
2. **事务/状态层**：看状态如何落盘，失败时如何恢复。
3. **并发控制层**：重点看锁、隔离级别、队列和幂等。
4. **索引/查询层**：确认性能收益来自数据结构、缓存还是查询重写。
5. **运维层**：看迁移、备份、监控和压测方式。"""
    return """1. **入口层**：确认用户通过什么接口使用项目。
2. **核心抽象层**：找最稳定的数据结构、服务对象或领域模型。
3. **边界适配层**：看外部 API、文件系统、数据库和网络请求如何被隔离。
4. **配置与扩展层**：看默认配置、插件点和兼容策略。
5. **质量保障层**：看测试、示例、CI 和发布脚本是否覆盖真实路径。"""


def detail_breakdown(repo: Repo) -> str:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)} {' '.join(repo.key_files)}".lower()
    if "skill" in text and ("security" in text or "cyber" in text or "mitre" in text):
        return """- **技能粒度**：检查一个 skill 是否足够小，能被 agent 独立调用；如果一个 skill 同时覆盖侦察、利用、检测和报告，执行边界就会变模糊。
- **输入输出**：每个 skill 应该明确需要哪些上下文、凭据、日志、文件或环境信息，以及产出是结论、命令、报告还是证据。
- **安全边界**：安全技能库必须区分防御、检测、演练和可能被滥用的攻击步骤。最好能在 skill 元数据里表达风险等级和授权前提。
- **标准映射质量**：映射到 MITRE/NIST 不应只是标签堆叠，要能解释 skill 对应哪个 tactic、technique、control 或风险场景。
- **可执行性**：`scripts/agent.py` 这类脚本要看是否有参数校验、错误处理、dry-run、日志和最小依赖；否则 skill 很难稳定接入自动化 agent。
- **更新机制**：安全框架会变，工具命令会变，API 会变。项目需要能批量发现过期引用、重复技能和断链文档。"""
    if "agent" in text or "llm" in text or "ai" in text:
        return """- **状态对象**：确认任务状态是否有显式结构，而不是散落在 prompt 字符串里。
- **工具 schema**：看工具参数是否强类型、是否有权限描述、是否能表达危险操作。
- **失败恢复**：重点找 timeout、rate limit、tool error、模型拒答、上下文过长时的处理。
- **可观测性**：长任务必须能回放每一步输入、输出、工具结果和中间状态。
- **扩展点**：判断新增工具、模型 provider、memory backend 是否需要改核心代码。"""
    return """- **核心对象**：找出项目真正反复传递的数据结构。
- **依赖边界**：确认外部服务是否通过 adapter 封装。
- **错误模型**：看异常是结构化返回，还是直接抛出字符串。
- **测试样例**：优先读覆盖真实链路的测试，而不是只测工具函数。
- **发布路径**：看版本、配置迁移和兼容性说明是否清楚。"""


def code_call_chain_breakdown(repo: Repo) -> str:
    text = f"{repo.full_name} {repo.description} {' '.join(repo.topics)} {' '.join(repo.key_files)}".lower()
    if "skill" in text and ("security" in text or "cyber" in text or "mitre" in text):
        return """1. **发现阶段：`index.json`**
   这是仓库级索引，记录 skill 名称、描述、路径和生成时间。agent 或平台不用一开始加载 800 多个完整 Markdown，而是先扫这个索引或 frontmatter，快速缩小候选技能集合。

2. **加载阶段：`skills/<name>/SKILL.md`**
   每个 skill 的 YAML frontmatter 承担“机器可检索元数据”：`name`、`description`、`domain`、`subdomain`、`tags`、`mitre_attack`、`nist_csf` 等。Markdown 正文承担“人和 agent 都能读的执行剧本”：Overview、Prerequisites、Objectives、Workflow、Validation Criteria。

3. **补充上下文：`references/*.md`**
   `references/standards.md` 和 `references/api-reference.md` 把 skill 从“步骤说明”变成“有依据的操作单元”。前者负责标准映射，后者负责工具/API/命令字段解释。

4. **执行入口：`skills/*/scripts/agent.py`**
   代表性脚本使用 `argparse` 定义参数和模式，然后进入 `main()`。这说明它不是被框架强绑定的服务，而是可以被 agent、人工 operator 或自动化流程独立调用的 helper。

5. **模式分支：`enumerate` / `impacket` / `sharpdpapi`**
   以 DPAPI skill 为例，脚本先校验 `--profile`、`--pvk` 等输入，再进入不同模式：`enumerate_artifacts()` 只枚举文件；`impacket` 模式在枚举后调用 `decrypt_masterkey_impacket()`；`sharpdpapi` 模式走 `sharpdpapi_triage()`。

6. **外部命令边界：`run_cmd()`**
   脚本没有重写 DPAPI 密码学，而是通过 `subprocess.run()` 编排 SharpDPAPI 或 Impacket。这个边界很重要：仓库提供的是“安全工作流编排”，不是重新实现所有底层安全工具。

7. **质量门禁：`tools/validate-skill.py`**
   PR 或批量维护时，`main()` 会遍历 skill 目录，调用 `validate_skill()`，再由 `parse_frontmatter()` 解析 YAML-like frontmatter。它检查必填字段、kebab-case、描述长度、domain、subdomain 和 tags。这个脚本是知识库长期不失控的关键。"""
    if "agent" in text or "llm" in text or "ai" in text:
        return """1. **入口函数**：找到 CLI/Web/API 如何把用户输入变成任务对象。
2. **任务编排**：追踪任务对象如何进入 planner 或 executor。
3. **工具调用**：看 tool schema、权限校验和参数序列化。
4. **结果回流**：看 observation 如何更新上下文、记忆或状态机。
5. **错误处理**：找 timeout、rate limit、tool error 的分支。
6. **日志与回放**：确认能否复盘每一步模型输入、工具输出和最终决策。"""
    return """1. **入口**：找到 CLI/API 主函数。
2. **解析**：看配置、参数和输入文件如何变成内部对象。
3. **核心调用**：追踪核心对象进入服务层或算法层。
4. **边界调用**：看外部进程、网络、数据库或文件系统如何隔离。
5. **返回**：确认错误、日志和输出格式。"""


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


def build_deep_analysis(repo: Repo, architecture_image: str, call_chain_image: str) -> str:
    topics = "、".join(repo.topics[:6]) if repo.topics else "暂无"
    homepage = f"\n- 官网/演示：[{repo.homepage}]({repo.homepage})" if repo.homepage else ""
    description = (repo.description or "项目暂未提供简介，需要从 README 和代码结构进一步判断。").strip()
    language = repo.language or "未标注"
    reading_focus = reading_focus_for(repo)
    core_question, architecture_path, risk_points, reusable_lessons = deep_reading_sections(repo)

    return f"""## [{repo.full_name}]({repo.url})

- 语言：{language}
- Stars：{repo.stars:,}，Forks：{repo.forks:,}，今日新增：{repo.today_stars:,}
- Topics：{topics}{homepage}
- 项目类型：{project_type(repo)}

**项目简介**：{description}

### 项目定位

从仓库描述、主题标签和语言栈看，这是一个 {project_type(repo)}。拆解它时，重点放在它如何定义用户入口、组织核心抽象、隔离外部依赖，以及是否具备可复用的工程边界。

### 核心问题

{core_question}

如果读完只能留下一个判断，就应该是：这个项目到底靠什么建立护城河，是工程设计、生态位置、领域知识组织，还是某个可复用的技术抽象。

### 一张图看架构

![{repo.full_name} 架构拆解图](/{architecture_image})

这张图的读法是从左到右追输入、加工、执行和反馈：每一层都要问清楚“它吃什么、产出什么、失败时谁兜底”。只有这条链路清楚，后面的源码阅读才不会停留在目录浏览。

### 架构拆分

{architecture_breakdown(repo)}

### 关键细节拆解

{detail_breakdown(repo)}

### 代码调用链路

![{repo.full_name} 代码调用链图](/{call_chain_image})

{code_call_chain_breakdown(repo)}

### 建议顺着这条链路读

{architecture_path}

### README 和代码结构线索

{readme_signals(repo)}

值得优先打开的文件或目录：

{key_file_signals(repo)}

### 关键文件怎么读

{key_file_breakdown(repo)}

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
"""


def write_report(repos: list[Repo]) -> Path:
    now = datetime.now(timezone.utc).astimezone(LOCAL_TZ)
    date = now.strftime("%Y-%m-%d")
    path = POST_DIR / f"{date}-github-trending-learning-report.md"
    POST_DIR.mkdir(parents=True, exist_ok=True)

    ranked = sorted(repos, key=lambda item: learning_value(item)[0], reverse=True)
    pick = enrich_reading_context(ranked[0])
    architecture_image = write_github_architecture_svg(pick, date)
    call_chain_image = write_github_call_chain_svg(pick, date)
    body = build_deep_analysis(pick, architecture_image, call_chain_image)

    content = f"""---
layout: post
title: "GitHub Trending 精读：{pick.full_name} ({date})"
subtitle: "单个开源项目深度拆解"
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

数据来源：[GitHub Trending Daily]({TRENDING_URL})。本篇围绕一个开源项目做介绍、结构线索梳理和源码阅读拆解。

## 分析目标

这篇文章关注四类问题：

1. 项目试图解决什么具体问题。
2. README 和目录结构透露了怎样的实现边界。
3. 源码阅读应该从哪条主链路进入。
4. 哪些工程经验可以迁移到自己的项目里。

## 项目拆解

{body}

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
