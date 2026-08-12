#!/usr/bin/env python3
"""Import the archived Spring 2021 Chinese coursework.

The source directory is treated as immutable. Generated files live under the course
docs tree, so CI only needs the repository and never depends on the local download.
The archived course homepage is refreshed only when explicitly requested.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import math
import re
import shutil
import time
import unicodedata
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "courses" / "CS61B" / "2021Spring"
DOCS = COURSE / "docs"
DEFAULT_SOURCE = Path("/home/everlasting/下载/CS61B_SP21_逐字对应中文翻译")
ORIGINAL_HOME = "https://sp21.datastructur.es/"
TERM_START = datetime(2021, 1, 19, tzinfo=ZoneInfo("America/Los_Angeles"))
TERM_END = datetime(2021, 5, 15, tzinfo=ZoneInfo("America/Los_Angeles"))

CALENDARS = {
    "lab-discussions": {
        "title": "实验与讨论安排",
        "url": "https://calendar.google.com/calendar/ical/c_c5oaq8so2c92ket6ok26710fk0%40group.calendar.google.com/public/basic.ics",
        "embed": "https://calendar.google.com/calendar/embed?src=c_c5oaq8so2c92ket6ok26710fk0@group.calendar.google.com&ctz=America%2FLos_Angeles",
    },
    "office-hours": {
        "title": "答疑时间",
        "url": "https://calendar.google.com/calendar/ical/c_e8roo1rcdghmffghilhvcrko0o%40group.calendar.google.com/public/basic.ics",
        "embed": "https://calendar.google.com/calendar/embed?src=c_e8roo1rcdghmffghilhvcrko0o@group.calendar.google.com&ctz=America%2FLos_Angeles",
    },
}

# source folder, source filename, output group, output slug, Chinese navigation title
ITEMS = [
    ("Labs", "Lab01A_配置你的电脑.md", "labs", "lab-1-setup", "Lab 1 Setup：配置计算机"),
    ("Labs", "Lab01B_IntelliJ_Java_Git.md", "labs", "lab-1-intellij-java-git", "Lab 1：IntelliJ、Java 与 Git"),
    ("Labs", "Lab02_JUnit测试与调试.md", "labs", "lab-2-junit-debugging", "Lab 2：JUnit 与调试"),
    ("Labs", "Lab03_计时测试与随机比较测试.md", "labs", "lab-3-timing-randomized-tests", "Lab 3：计时与随机测试"),
    ("Labs", "Lab04_Git与调试.md", "labs", "lab-4-git-debugging", "Lab 4：Git 与调试"),
    ("Labs", "Lab05_Project1同伴代码审查.md", "labs", "lab-5-peer-code-review", "Lab 5：同伴代码审查"),
    ("Labs", "Lab06_Project2入门.md", "labs", "lab-6-project-2", "Lab 6：Project 2 入门"),
    ("Labs", "Lab07_BSTMap.md", "labs", "lab-7-bstmap", "Lab 7：BSTMap"),
    ("Labs", "Lab08_HashMap.md", "labs", "lab-8-hashmap", "Lab 8：HashMap"),
    ("Labs", "Lab12_Project3入门.md", "labs", "lab-12-project-3-rendering", "Lab 12：Project 3 入门"),
    ("Labs", "Lab13_Project3第二阶段入门.md", "labs", "lab-13-project-3-interactivity", "Lab 13：Project 3 交互"),
    ("Homeworks", "HW0_Java速成.md", "homeworks", "hw-0-java", "HW 0：Java 速成"),
    ("Homeworks", "HW2_概念复习.md", "homeworks", "hw-2-conceptual-review", "HW 2：概念复习"),
    ("Homeworks", "HW3_概念复习.md", "homeworks", "hw-3-conceptual-review", "HW 3：概念复习"),
    ("Projects", "Project0_2048.md", "projects", "project-0-2048", "Project 0：2048"),
    ("Projects", "Project1_数据结构.md", "projects", "project-1-data-structures", "Project 1：数据结构"),
    ("Projects", "Project1EC_自动评分器.md", "projects", "project-1ec-autograder", "Project 1 EC：自动评分器"),
    ("Projects", "Project2_Gitlet.md", "projects", "project-2-gitlet", "Project 2：Gitlet"),
    ("Projects", "Project3_BYOW.md", "projects", "project-3-byow", "Project 3：CS61BYoW"),
    ("Projects", "Project3_游戏共享.md", "projects", "project-3-game-sharing", "Project 3：游戏共享"),
]

GROUPS = {
    "labs": ("实验", "课程实验、准备工作与实作周的中文资料。"),
    "homeworks": ("作业", "课程家庭作业的中文资料。"),
    "projects": ("项目", "课程编程项目、阶段说明与展示要求的中文资料。"),
}

IMAGE_RE = re.compile(
    r"!\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+([\"'][^\"']*[\"']))?\)"
)
INTERNAL_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(#([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
IMAGE_URL_ALIASES = {
    "https://sp21.datastructur.es/materials/lab/lab3/img/exception_breakpoint_1.png":
        "https://sp21.datastructur.es/materials/lab/lab3/img/breakpoints.png",
    "https://sp21.datastructur.es/materials/lab/lab3/img/exception_breakpoint_2.png":
        "https://sp21.datastructur.es/materials/lab/lab3/img/breakpoints_filled_in.png",
    "https://sp21.datastructur.es/materials/proj/proj1/img/java_visualizer.png":
        "https://sp21.datastructur.es/materials/proj/proj1/java_visualizer.png",
    "https://sp21.datastructur.es/materials/proj/proj1/img/karplus-strong.png":
        "https://sp21.datastructur.es/materials/proj/proj1/karplus-strong.png",
}

LECTURE_TRANSLATIONS = {
    "Intro, Hello World Java": "导论与 Hello World Java",
    "Defining and Using Classes": "定义与使用类",
    "Testing": "测试",
    "References, Recursion, and Lists": "引用、递归与链表",
    "SLLists, Nested Classes, Sentinel Nodes": "SLList、嵌套类与哨兵节点",
    "DLLists, Arrays": "双向链表与数组",
    "ALists, Resizing, vs. SLists": "AList、扩容与 SList 对比",
    "Inheritance, Implements": "继承与接口实现",
    "Extends, Casting, Higher Order Functions": "继承、类型转换与高阶函数",
    "Subtype Polymorphism vs. HoFs": "子类型多态与高阶函数",
    "Exceptions, Iterators, Object Methods": "异常、迭代器与 Object 方法",
    "Command Line Programming, Git, Project 2 Preview": "命令行编程、Git 与 Project 2 预览",
    "Asymptotics I": "渐近分析（一）",
    "Disjoint Sets": "并查集",
    "Asymptotics II": "渐近分析（二）",
    "ADTs, Sets, Maps, BSTs": "抽象数据类型、集合、映射与二叉搜索树",
    "B-Trees (2-3, 2-3-4 Trees)": "B 树（2-3 树与 2-3-4 树）",
    "Red Black Trees": "红黑树",
    "Hashing": "哈希",
    "Heaps and PQs": "堆与优先队列",
    "Tree and Graph Traversals": "树与图的遍历",
    "Graph Traversals and Implementations": "图遍历与实现",
    "Shortest Paths": "最短路径",
    "Minimum Spanning Trees": "最小生成树",
    "Range Searching and Multi-Dimensional Data": "范围搜索与多维数据",
    "Prefix Operations and Tries": "前缀操作与 Trie",
    "Software Engineering I": "软件工程（一）",
    "Reductions and Decomposition": "归约与分解",
    "Basic Sorts": "基础排序",
    "Quick Sort": "快速排序",
    "Software Engineering II": "软件工程（二）",
    "More Quick Sort, Sorting Summary": "快速排序进阶与排序总结",
    "Software Engineering III": "软件工程（三）",
    "Sorting and Algorithmic Bounds": "排序与算法界限",
    "Radix Sorts": "基数排序",
    "Sorting and Data Structures Conclusion": "排序与数据结构总结",
    "Software Engineering IV": "软件工程（四）",
    "Compression": "压缩",
    "Compression, Complexity, and P=NP?": "压缩、复杂度与 P=NP？",
    "Summary, Fun": "课程总结与趣味内容",
}

TEXT_TRANSLATIONS = {
    "Week": "周次", "Date": "日期", "Reading": "阅读", "Lecture": "讲座",
    "Discussion": "讨论", "Lab": "实验", "Assignments/Exams": "作业 / 考试",
    "No Classes": "停课", "No discussion week 1.": "第一周无讨论课。",
    "No Discussion": "无讨论课", "No Lab": "无实验", "Spring Break": "春假",
    "Academic Holiday": "学术假日", "RRR Week": "复习周",
    "Finals Week": "期末考试周", "survey": "问卷", "None": "无",
    "video": "视频", "slides": "幻灯片", "guide": "讲义",
    "solution": "答案", "live Q&A": "在线答疑", "Live Lecture": "直播讲座",
    "check in": "签到", "optional": "可选", "due": "截止",
    "Mon": "周一", "Tue": "周二", "Wed": "周三", "Thu": "周四", "Fri": "周五",
    "Setting Up Your Computer": "配置你的计算机", "IntelliJ Setup": "IntelliJ 配置",
    "HW0: Basic Java Programs": "HW0：基础 Java 程序", "Debugging": "调试",
    "Randomizing Testing and Timing": "随机化测试与计时",
    "Peer Code Review": "同伴代码审查", "Project 2 Getting Started": "Project 2 入门",
    "Introduction To Java": "Java 入门", "Scope, Pass by Value, Static": "作用域、值传递与静态成员",
    "Scope, Static, Linked Lists": "作用域、静态成员与链表",
    "Linked Lists Exam Prep": "链表考试准备",
    "Inheritance and Implements": "继承与接口实现",
    "Polymorphism, Iterators, and Iterables": "多态、迭代器与可迭代对象",
    "Disjoint Sets and Asymptotics": "并查集与渐近分析",
    "ADTs and Asymptotics II": "抽象数据类型与渐近分析（二）",
    "B-Trees, Red Black Trees, and Hashing": "B 树、红黑树与哈希",
    "Heaps and Graphs": "堆与图", "Shortest Paths and MSTs": "最短路径与最小生成树",
    "More Graphs and Tries": "图与 Trie 进阶", "Basic Sorts": "基础排序",
    "More Sorting": "排序进阶", "Exam Prep": "考试准备",
    "Midterm 1 Practice Assessment": "期中考试 1 模拟评测",
    "Midterm 1": "期中考试 1", "Midterm 2": "期中考试 2",
    "Final exam": "期末考试", "Final": "期末考试",
    "Project 2 Workday": "Project 2 实作日", "Project 3 Work Day": "Project 3 实作日",
    "Getting Started on Project 3": "Project 3 入门", "Goodbye, Fun": "告别与趣味活动",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, attempts: int = 4) -> bytes:
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "docs.everlasting.xin importer/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as error:  # noqa: BLE001 - preserve the final network failure
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(attempt + 1)
    raise RuntimeError(f"failed to download {url} after {attempts} attempts") from last_error


def validate_source(source: Path) -> dict:
    expected = {
        "Labs": {filename for folder, filename, *_ in ITEMS if folder == "Labs"},
        "Homeworks": {
            *(filename for folder, filename, *_ in ITEMS if folder == "Homeworks"),
            "HW1_已取消.md",
        },
        "Projects": {filename for folder, filename, *_ in ITEMS if folder == "Projects"},
    }
    for folder, expected_files in expected.items():
        actual_files = {path.name for path in (source / folder).glob("*.md")}
        if actual_files != expected_files:
            missing = sorted(expected_files - actual_files)
            extra = sorted(actual_files - expected_files)
            raise SystemExit(f"unexpected {folder} file set; missing={missing}, extra={extra}")
    readme = source / "README_文件清单.md"
    if not readme.is_file():
        raise SystemExit(f"missing source inventory: {readme}")
    source_hashes = {
        str(path.relative_to(source)): sha256(path.read_bytes())
        for path in sorted(source.rglob("*.md"))
    }
    return {
        "source": str(source),
        "translation_profile": "逐字对应中文翻译",
        "source_inventory_sha256": sha256(readme.read_bytes()),
        "source_document_count": len(source_hashes),
        "imported_content_count": len(ITEMS),
        "ignored_documents": ["Homeworks/HW1_已取消.md", "README_文件清单.md"],
        "source_sha256": source_hashes,
    }


def source_url(text: str) -> str:
    match = re.search(
        r"(?:原文|原始页面|原页面|原文件)[：:]\s*(?:<|`)?(https?://[^\s>`)<]+)",
        text,
    )
    return match.group(1) if match else ORIGINAL_HOME


def normalize_markdown(text: str) -> str:
    """Keep Markdown hard breaks without committing invisible trailing spaces."""
    normalized: list[str] = []
    in_fence = False
    for line in text.strip().splitlines():
        if re.match(r"^\s*(?:```|~~~)", line):
            in_fence = not in_fence
        if not in_fence and re.search(r" {2,}$", line):
            line = line.rstrip() + "<br>"
        elif not in_fence:
            line = line.rstrip()
        normalized.append(line)
    return "\n".join(normalized)


def remove_introductory_source_note(text: str) -> str:
    lines = text.splitlines()
    first_section = next(
        (index for index, line in enumerate(lines) if line.startswith("## ")),
        len(lines),
    )
    filtered: list[str] = []
    for index, line in enumerate(lines):
        quote = line[1:].strip() if line.startswith(">") else ""
        remove = index < first_section and (
            re.match(r"^(?:原文|原始页面|原页面|原文件)[：:]", quote) is not None
            or ("翻译" in quote and ("原页面" in quote or "原 PDF" in quote or "原PDF" in quote))
            or line == ">"
        )
        if not remove:
            filtered.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(filtered)).strip()


def vendor_images(
    source_texts: dict[tuple[str, str], str],
    refresh_images: bool = False,
) -> tuple[dict[str, str], dict]:
    urls = sorted(
        {
            match.group(2)
            for text in source_texts.values()
            for match in IMAGE_RE.finditer(text)
        }
    )

    signatures = {
        ".gif": (b"GIF87a", b"GIF89a"),
        ".jpg": (b"\xff\xd8\xff",),
        ".jpeg": (b"\xff\xd8\xff",),
        ".png": (b"\x89PNG\r\n\x1a\n",),
    }

    def validate_image(data: bytes, filename: str, url: str) -> None:
        suffix = Path(filename).suffix.lower()
        if not data or (suffix in signatures and not data.startswith(signatures[suffix])):
            raise RuntimeError(f"downloaded coursework image is invalid: {url}")

    def download(url: str) -> tuple[str, bytes, str, str]:
        retrieval_url = IMAGE_URL_ALIASES.get(url, url)
        data = fetch(retrieval_url)
        basename = Path(urlsplit(url).path).name or "image"
        safe_basename = re.sub(r"[^A-Za-z0-9._-]+", "-", basename).strip("-") or "image"
        filename = f"{hashlib.sha256(url.encode()).hexdigest()[:12]}-{safe_basename}"
        validate_image(data, filename, url)
        return url, data, filename, retrieval_url

    downloads: dict[str, tuple[bytes, str, str]] = {}
    previous_items: dict[str, dict] = {}
    previous_manifest = DOCS / "coursework-import-manifest.json"
    if not refresh_images and previous_manifest.is_file():
        try:
            previous_items = json.loads(previous_manifest.read_text(encoding="utf-8")).get(
                "localized_images", {}
            ).get("items", {})
        except (TypeError, ValueError, json.JSONDecodeError):
            previous_items = {}

    for url in urls:
        details = previous_items.get(url, {})
        cached_path = DOCS / str(details.get("path", ""))
        if not cached_path.is_file():
            continue
        data = cached_path.read_bytes()
        if len(data) != details.get("bytes") or sha256(data) != details.get("sha256"):
            continue
        validate_image(data, cached_path.name, url)
        downloads[url] = (
            data,
            cached_path.name,
            str(details.get("retrieved_from", IMAGE_URL_ALIASES.get(url, url))),
        )

    pending_urls = [url for url in urls if url not in downloads]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(download, url) for url in pending_urls]
        for future in concurrent.futures.as_completed(futures):
            url, data, filename, retrieval_url = future.result()
            downloads[url] = (data, filename, retrieval_url)

    assets = DOCS / "assets" / "coursework"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True)

    replacements: dict[str, str] = {}
    manifest: dict[str, dict[str, str | int]] = {}
    for url in urls:
        data, filename, retrieval_url = downloads[url]
        (assets / filename).write_bytes(data)
        replacements[url] = f"../assets/coursework/{filename}"
        manifest[url] = {
            "path": f"assets/coursework/{filename}",
            "sha256": sha256(data),
            "bytes": len(data),
        }
        if retrieval_url != url:
            manifest[url]["retrieved_from"] = retrieval_url
    return replacements, {"count": len(urls), "items": manifest}


def set_heading_anchor(body: str, heading_pattern: str, anchor: str) -> str:
    updated, replacements = re.subn(
        rf"(?m)^({heading_pattern})(?:\s+\{{\s*#[^}}]+\s*\}})?$",
        rf"\1 {{ #{anchor} }}",
        body,
        count=1,
    )
    if replacements != 1:
        raise SystemExit(f"expected one heading for anchor {anchor}, got {replacements}")
    return updated


def normalize_manual_toc(body: str, remove_targets: set[str]) -> str:
    """Use the same compact two-space TOC nesting as the rest of the site."""
    lines = body.splitlines()
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^## 目录(?:\s+\{[^}]+\})?$", line)
        ),
        None,
    )
    if start is None:
        return body

    end = next(
        (index for index in range(start + 1, len(lines)) if HEADING_RE.match(lines[index])),
        len(lines),
    )
    lines[start] = "## 目录"
    item_re = re.compile(r"^(\s*)-\s+(.+\]\((#[^)]+)\))\s*$")
    items: list[tuple[int, int]] = []
    filtered: list[str] = []
    for line in lines[start + 1 : end]:
        match = item_re.match(line)
        if match and match.group(3) in remove_targets:
            continue
        if match:
            items.append((len(filtered), len(match.group(1))))
        filtered.append(line)

    if items:
        minimum = min(indent for _, indent in items)
        positive = [indent - minimum for _, indent in items if indent > minimum]
        unit = math.gcd(*positive) if positive else 2
        unit = unit or 2
        for index, indent in items:
            filtered[index] = re.sub(
                r"^\s*",
                " " * (((indent - minimum) // unit) * 2),
                filtered[index],
                count=1,
            )

    return "\n".join(lines[: start + 1] + filtered + lines[end:])


def heading_key(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text)
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return "".join(character for character in normalized if character.isalnum())


def preserve_internal_anchors(body: str) -> str:
    anchors_by_heading: dict[str, set[str]] = defaultdict(set)
    for label, anchor in INTERNAL_LINK_RE.findall(body):
        anchors_by_heading[heading_key(label)].add(anchor)

    found: set[str] = set()
    output: list[str] = []
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        anchors = anchors_by_heading.get(heading_key(match.group(2)), set()) if match else set()
        if len(anchors) > 1:
            raise SystemExit(f"multiple internal anchors map to one heading: {sorted(anchors)}")
        if anchors:
            anchor = next(iter(anchors))
            if anchor not in found:
                line = f"{line} {{ #{anchor} }}"
                found.add(anchor)
        output.append(line)

    expected = {anchor for anchors in anchors_by_heading.values() for anchor in anchors}
    missing = sorted(expected - found)
    if missing:
        raise SystemExit(f"internal anchors have no matching headings: {missing}")
    return "\n".join(output)


def import_markdown(
    source_texts: dict[tuple[str, str], str],
    image_replacements: dict[str, str],
) -> None:
    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for group in GROUPS:
        destination = DOCS / group
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True)

    for folder, filename, group, slug, title in ITEMS:
        raw_body = source_texts[(folder, filename)]
        original_url = source_url(raw_body)
        body = remove_introductory_source_note(normalize_markdown(raw_body))
        body = IMAGE_RE.sub(
            lambda match: (
                f"![{match.group(1)}]({image_replacements[match.group(2)]}"
                f"{' ' + match.group(3) if match.group(3) else ''})"
            ),
            body,
        )
        for remote_url, local_path in image_replacements.items():
            body = body.replace(f"]({remote_url})", f"]({local_path})")

        if slug == "project-2-gitlet":
            body = body.replace("](#阶段检查评分器)", "](#checkpoint-grader)")
            body = normalize_manual_toc(body, {"#project-2gitlet", "#目录"})
            body = re.sub(
                r"\n+---\n+\*\*翻译说明：\*\*[^\n]*\s*$",
                "",
                body,
            )
        elif slug == "project-3-byow":
            body = body.replace("](#phase-1-world-generation)", "](#phase-1)")
            body = body.replace("](#phase-2-interactivity)", "](#phase-2)")
            body = body.replace("](#submission-and-grading)", "](#submission)")
            body = normalize_manual_toc(body, set())
        elif slug == "project-3-game-sharing":
            body = normalize_manual_toc(
                body,
                {"#项目-3游戏共享", "#目录", "#author-boren-tsai"},
            )
            body = re.sub(
                r"(?m)^#{2,6} 作者：Boren Tsai(?:\s+\{[^}]+\})?$",
                "**作者：Boren Tsai**",
                body,
                count=1,
            )

        body = preserve_internal_anchors(body)
        if slug == "project-3-byow":
            body = set_heading_anchor(
                body,
                r"#{2,3} (?:四、)?(?:Phase|阶段) 1：世界生成",
                "phase-1",
            )
            body = set_heading_anchor(
                body,
                r"#{2,3} (?:九、)?(?:Phase|阶段) 2：交互性",
                "phase-2",
            )
            body = set_heading_anchor(body, r"## (?:十七、)?提交与评分", "submission")
        elif slug == "project-2-gitlet":
            body = set_heading_anchor(
                body,
                r"### (?:阶段检查评分器|Checkpoint Grader)",
                "checkpoint-grader",
            )
        description = f"CS61B Spring 2021 {title}中文学习资料。"
        output = (
            "---\n"
            f"title: {json.dumps(title, ensure_ascii=False)}\n"
            f"description: {json.dumps(description, ensure_ascii=False)}\n"
            "---\n\n"
            f"{body}\n\n---\n\n"
            f"原始页面：[{original_url}]({original_url})\n"
        )
        (DOCS / group / f"{slug}.md").write_text(output, encoding="utf-8")
        grouped[group].append((title, slug))

    for group, (title, description) in GROUPS.items():
        links = "\n".join(f"- [{item_title}]({slug}.md)" for item_title, slug in grouped[group])
        index = (
            "---\n"
            f"title: {title}\n"
            f"description: {description}\n"
            "---\n\n"
            f"# {title}\n\n{description}\n\n"
            f"{links}\n"
        )
        (DOCS / group / "index.md").write_text(index, encoding="utf-8")


def update_course_home_links() -> None:
    """Point archived schedule entries at the new complete single-page specs."""
    course_home = DOCS / "course" / "index.md"
    text = course_home.read_text(encoding="utf-8")
    replacements = {
        '/CS61B/2021Spring/projects/project-2-checkpoint/':
            '/CS61B/2021Spring/projects/project-2-gitlet/#checkpoint-grader',
        '/CS61B/2021Spring/labs/project-2-workday/':
            '/CS61B/2021Spring/projects/project-2-gitlet/',
        '/CS61B/2021Spring/labs/project-3-workday/':
            '/CS61B/2021Spring/projects/project-3-byow/',
        '<a href="/CS61B/2021Spring/projects/project-3-phase-1/">Project 3 Phase 1</a>':
            '<a href="/CS61B/2021Spring/projects/project-3-byow/#phase-1">Project 3 Phase 1</a>',
        '<a href="/CS61B/2021Spring/projects/project-3-phase-2/">Project 3 Phase 2</a>':
            '<a href="/CS61B/2021Spring/projects/project-3-byow/#phase-2">Project 3 Phase 2</a>',
        '<a href="/CS61B/2021Spring/projects/project-3-demos/">Project 3 Game Sharing</a>':
            '<a href="/CS61B/2021Spring/projects/project-3-game-sharing/">Project 3 Game Sharing</a>',
        '<a href="/CS61B/2021Spring/projects/project-3-demos/">BYOW Demos</a>':
            '<a href="/CS61B/2021Spring/projects/project-3-byow/#submission">BYOW Demos</a>',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    course_home.write_text(text, encoding="utf-8")


def internal_url(group: str, slug: str, anchor: str = "") -> str:
    base = f"/CS61B/2021Spring/{group}/{slug}/"
    return base + (f"#{anchor}" if anchor else "")


def reading_url(label: str) -> str:
    from markdown.extensions.toc import slugify

    number = label.strip()
    chapter = int(number.split(".", 1)[0])
    chapter_files = {
        1: "01-java-basics", 2: "02-lists", 3: "03-testing",
        4: "04-inheritance-and-interfaces", 5: "05-generics-and-autoboxing",
        6: "06-exceptions-iterators-object-methods", 7: "07-packages-and-access-control",
        8: "08-efficient-programming-and-asymptotic-analysis", 9: "09-disjoint-sets",
        10: "10-adts-and-trees", 11: "11-balanced-trees", 12: "12-hashing",
        13: "13-heaps-and-priority-queues", 14: "14-data-structures-summary", 15: "15-tries",
        16: "16-quadtrees-and-kd-trees", 17: "17-tree-traversals-and-graphs",
        18: "18-graph-traversal-and-representation", 19: "19-shortest-paths",
        20: "20-minimum-spanning-trees", 21: "21-reductions-and-decomposition",
    }
    chapter_slug = chapter_files[chapter]
    chapter_source = DOCS / "chapters" / f"{chapter_slug}.md"
    heading = next(
        (line[3:].strip() for line in chapter_source.read_text(encoding="utf-8").splitlines()
         if line.startswith(f"## {number} ")),
        "",
    )
    if not heading:
        raise SystemExit(f"reading {number} has no matching chapter heading in {chapter_source.name}")
    return internal_url("chapters", chapter_slug, slugify(heading, "-"))


LINK_RULES = [
    (re.compile(r"/materials/lab/lab1setup"), ("labs", "lab-1-setup")),
    (re.compile(r"/materials/lab/lab1(?:/|$)"), ("labs", "lab-1-intellij-java-git")),
    (re.compile(r"/materials/lab/lab2(?:/|$)"), ("labs", "lab-2-junit-debugging")),
    (re.compile(r"/materials/lab/lab3(?:/|$)"), ("labs", "lab-3-timing-randomized-tests")),
    (re.compile(r"/materials/lab/lab4(?:/|$)"), ("labs", "lab-4-git-debugging")),
    (re.compile(r"/materials/lab/lab5(?:/|$)"), ("labs", "lab-5-peer-code-review")),
    (re.compile(r"/materials/lab/lab6(?:/|$)"), ("labs", "lab-6-project-2")),
    (re.compile(r"/materials/lab/lab7(?:/|$)"), ("labs", "lab-7-bstmap")),
    (re.compile(r"/materials/lab/lab8(?:/|$)"), ("labs", "lab-8-hashmap")),
    (re.compile(r"/materials/lab/lab12(?:/|$)"), ("labs", "lab-12-project-3-rendering")),
    (re.compile(r"/materials/lab/lab13(?:/|$)"), ("labs", "lab-13-project-3-interactivity")),
    (re.compile(r"/materials/hw/hw0"), ("homeworks", "hw-0-java")),
    (re.compile(r"/materials/hw/hw2"), ("homeworks", "hw-2-conceptual-review")),
    (re.compile(r"/materials/hw/hw3"), ("homeworks", "hw-3-conceptual-review")),
    (re.compile(r"/materials/proj/proj0"), ("projects", "project-0-2048")),
    (re.compile(r"/materials/proj/proj1ec"), ("projects", "project-1ec-autograder")),
    (re.compile(r"/materials/proj/proj1"), ("projects", "project-1-data-structures")),
    (re.compile(r"/materials/proj/proj2"), ("projects", "project-2-gitlet")),
    (re.compile(r"/materials/proj/proj3/proj3GameSharing"), ("projects", "project-3-game-sharing")),
    (re.compile(r"/materials/proj/proj3"), ("projects", "project-3-byow")),
]

TEXT_LINKS = {
    "Midterm 1 Practice Assessment": ("exams", "midterm-1-practice"),
    "Midterm 1 (2/10)": ("exams", "midterm-1"),
    "Midterm 2 (03/17)": ("exams", "midterm-2"),
    "Final exam": ("exams", "final"),
    "Project 2 Checkpoint": ("projects", "project-2-gitlet", "checkpoint-grader"),
    "Project 3 Phase 1": ("projects", "project-3-byow", "phase-1"),
    "Project 3 Phase 2": ("projects", "project-3-byow", "phase-2"),
    "BYOW Demos": ("projects", "project-3-byow", "submission"),
    "Project 2 Workday": ("projects", "project-2-gitlet"),
    "Project 3 Work Day": ("projects", "project-3-byow"),
}


def translate_text(text: str) -> str:
    result = text
    for source, translated in LECTURE_TRANSLATIONS.items():
        result = result.replace(source, translated)
    for source, translated in sorted(TEXT_TRANSLATIONS.items(), key=lambda item: -len(item[0])):
        result = re.sub(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", translated, result, flags=re.I)
    return result


def build_main_calendar(home_html: bytes) -> str:
    from bs4 import BeautifulSoup, Comment, NavigableString

    soup = BeautifulSoup(home_html, "html.parser")
    table = soup.select_one("table#calendar")
    if table is None:
        raise SystemExit("original homepage no longer contains table#calendar")

    # The archived page contains Liquid trace comments ("if …", "for …").
    # They are implementation residue, not visible course content.
    for comment in table.find_all(string=lambda value: isinstance(value, Comment)):
        comment.extract()

    for anchor in table.select("a"):
        href = anchor.get("href", "")
        label = anchor.get_text(" ", strip=True)
        if re.fullmatch(r"\d{1,2}\.\d", label) and "joshhug.gitbooks.io" in href:
            anchor["href"] = reading_url(label)
        else:
            absolute = urljoin(ORIGINAL_HOME, href)
            mapped = None
            for pattern, target in LINK_RULES:
                if pattern.search(urlsplit(absolute).path):
                    mapped = target
                    break
            if mapped:
                anchor["href"] = internal_url(*mapped)
            else:
                anchor["href"] = absolute
                anchor["target"] = "_blank"
                anchor["rel"] = "noopener"

    # Some exam/checkpoint/phase cells were plain text or empty links on the old site.
    for cell in table.select("td"):
        cell_text = cell.get_text(" ", strip=True)
        for phrase, target in TEXT_LINKS.items():
            if phrase.lower() in cell_text.lower() and not any(
                link.get("href", "").startswith("/CS61B/") for link in cell.select("a")
            ):
                link = soup.new_tag("a", href=internal_url(*target))
                link.string = phrase
                cell.append(" ")
                cell.append(link)
                break

    for node in table.find_all(string=True):
        if isinstance(node, NavigableString) and node.strip():
            node.replace_with(translate_text(str(node)))
    table["aria-label"] = "CS61B Spring 2021 中文课程日历"
    return f'<div class="calendar-scroll">{table}</div>'


def unfold_ics(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith((" ", "\t")) and lines:
            lines[-1] += line[1:]
        else:
            lines.append(line)
    return lines


def normalize_ics(data: bytes) -> bytes:
    """Remove volatile stamps, normalize line endings, and sort VEVENT blocks."""
    lines = [line.rstrip() for line in data.decode("utf-8").replace("\r\n", "\n").split("\n")]
    lines = [line for line in lines if not line.startswith("DTSTAMP:")]
    base: list[str] = []
    events: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if line == "BEGIN:VEVENT":
            current = [line]
        elif current is not None:
            current.append(line)
            if line == "END:VEVENT":
                events.append(current)
                current = None
        else:
            base.append(line)
    end_index = base.index("END:VCALENDAR")
    normalized = base[:end_index]
    for event in sorted(events, key=lambda block: "\n".join(block)):
        normalized.extend(event)
    normalized.extend(base[end_index:])
    return ("\n".join(normalized).rstrip() + "\n").encode("utf-8")


def parse_dt(value: str) -> datetime:
    raw = value.rstrip("Z")
    fmt = "%Y%m%dT%H%M%S" if "T" in raw else "%Y%m%d"
    parsed = datetime.strptime(raw, fmt)
    if value.endswith("Z"):
        return parsed.replace(tzinfo=ZoneInfo("UTC")).astimezone(TERM_START.tzinfo)
    return parsed.replace(tzinfo=TERM_START.tzinfo)


def parse_events(data: bytes) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in unfold_ics(data.decode("utf-8")):
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT" and current is not None:
            events.append(current)
            current = None
        elif current is not None and ":" in line:
            key, value = line.split(":", 1)
            base = key.split(";", 1)[0]
            if base == "EXDATE":
                current[base] = ",".join(filter(None, [current.get(base), value]))
            else:
                current[base] = value
    return events


def expand_events(data: bytes) -> list[tuple[datetime, datetime, str, str]]:
    events = parse_events(data)
    overrides = {(event.get("UID", "").split("_R", 1)[0], event.get("RECURRENCE-ID", "")): event for event in events if event.get("RECURRENCE-ID")}
    expanded: list[tuple[datetime, datetime, str, str]] = []
    weekdays = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    for event in events:
        if "DTSTART" not in event or event.get("RECURRENCE-ID"):
            continue
        start = parse_dt(event["DTSTART"])
        end = parse_dt(event.get("DTEND", event["DTSTART"]))
        duration = end - start
        occurrences = [start]
        if "RRULE" in event:
            rule = dict(part.split("=", 1) for part in event["RRULE"].split(";") if "=" in part)
            until = parse_dt(rule.get("UNTIL", "20210515T000000"))
            days = [weekdays[item] for item in rule.get("BYDAY", "").split(",") if item in weekdays] or [start.weekday()]
            occurrences = []
            cursor = start.replace(hour=0, minute=0, second=0)
            while cursor <= min(until, TERM_END):
                if cursor.weekday() in days:
                    candidate = cursor.replace(hour=start.hour, minute=start.minute, second=start.second)
                    if candidate >= start:
                        occurrences.append(candidate)
                cursor += timedelta(days=1)
        excluded = {parse_dt(value) for value in event.get("EXDATE", "").split(",") if value}
        uid = event.get("UID", "").split("_R", 1)[0]
        for occurrence in occurrences:
            if occurrence in excluded or not (TERM_START <= occurrence < TERM_END):
                continue
            recurrence_key = occurrence.strftime("%Y%m%dT%H%M%S")
            override = overrides.get((uid, recurrence_key))
            active = override or event
            active_start = parse_dt(active["DTSTART"]) if override else occurrence
            active_end = parse_dt(active.get("DTEND", active["DTSTART"])) if override else occurrence + duration
            if active.get("STATUS") == "CANCELLED":
                continue
            description = html.unescape(active.get("DESCRIPTION", "").replace("\\n", " "))
            url_match = re.search(r"https?://[^\s<\"]+", description)
            expanded.append((active_start, active_end, active.get("SUMMARY", "课程安排"), url_match.group(0) if url_match else ""))
    return sorted(set(expanded), key=lambda item: (item[0], item[2]))


def render_archive_calendar(slug: str, title: str, data: bytes, source_url_value: str, embed_url: str) -> str:
    events = expand_events(data)
    week_start = datetime(2021, 1, 17, tzinfo=TERM_START.tzinfo)
    week_end = week_start + timedelta(days=7)
    visible_events = [event for event in events if week_start <= event[0] < week_end]
    by_day: dict[int, list[tuple[datetime, datetime, str, str]]] = defaultdict(list)
    for event in visible_events:
        by_day[(event[0].date() - week_start.date()).days].append(event)

    day_columns: list[str] = []
    for day in range(7):
        day_events = sorted(by_day[day], key=lambda event: (event[0], event[1], event[2]))
        clusters: list[list[tuple[datetime, datetime, str, str]]] = []
        for event in day_events:
            if not clusters or event[0] >= max(item[1] for item in clusters[-1]):
                clusters.append([event])
            else:
                clusters[-1].append(event)
        rendered_events: list[str] = []
        for cluster in clusters:
            lanes: list[datetime] = []
            placements: list[tuple[tuple[datetime, datetime, str, str], int]] = []
            for event in cluster:
                lane = next((index for index, lane_end in enumerate(lanes) if event[0] >= lane_end), len(lanes))
                if lane == len(lanes):
                    lanes.append(event[1])
                else:
                    lanes[lane] = event[1]
                placements.append((event, lane))
            lane_count = len(lanes)
            for (start, end, summary, link), lane in placements:
                translated_summary = summary.replace("Office Hours", "答疑时间")
                translated_summary = re.sub(r"'s Lab$", " 的实验", translated_summary)
                translated_summary = re.sub(r"s' Lab$", "s 的实验", translated_summary)
                translated_summary = re.sub(r"'s Discussion$", " 的讨论课", translated_summary)
                translated_summary = re.sub(r"s' Discussion$", "s 的讨论课", translated_summary)
                translated_summary = translated_summary.replace(" and ", " 与 ")
                label = html.escape(translated_summary)
                if link:
                    label = f'<a href="{html.escape(link, quote=True)}" target="_blank" rel="noopener">{label}</a>'
                start_minutes = max(0, int((start.hour * 60 + start.minute) - 9 * 60))
                duration_minutes = max(30, int((end - start).total_seconds() / 60))
                left = lane * 100 / lane_count
                width = 100 / lane_count
                rendered_events.append(
                    f'<div class="week-event" style="--start:{start_minutes};--duration:{duration_minutes};'
                    f'--left:{left:.4f};--width:{width:.4f}"><span>{start.strftime("%-I:%M")}–{end.strftime("%-I:%M")}</span>{label}</div>'
                )
        day_columns.append(f'<div class="week-day-column">{"".join(rendered_events)}</div>')

    headers = "".join(
        f'<div class="week-day-heading">{label} {date}</div>'
        for label, date in zip(("周日", "周一", "周二", "周三", "周四", "周五", "周六"), ("1/17", "1/18", "1/19", "1/20", "1/21", "1/22", "1/23"))
    )
    times = "".join(f'<span style="--hour:{hour - 9}">{hour if hour <= 12 else hour - 12}{"am" if hour < 12 else "pm"}</span>' for hour in range(9, 21))

    original_copy = (
        '<p>每个讨论课现在分为<strong>常规讨论</strong>或<strong>考试准备讨论</strong>。</p>'
        '<ol><li>常规讨论侧重回顾课程内容并完成基础问题。</li>'
        '<li>考试准备讨论减少概念回顾，侧重练习考试难度的问题。</li></ol>'
        if slug == "lab-discussions" else
        '<p><strong>注意：</strong>答疑时间安排在周一、周三和周五。周三、周四和周五也可以带着问题参加实验课。</p>'
    )
    anchor = "disccal" if slug == "lab-discussions" else "ohcal"
    return (
        f'<div class="segment calendar-segment" id="{anchor}"><div class="segmenttitle">{title}</div>{original_copy}'
        '<div class="week-toolbar"><h3>2021 年 1 月 17–23 日</h3><span>今天　‹　›</span></div>'
        f'<div class="week-calendar"><div class="week-corner"></div>{headers}'
        f'<div class="week-time-axis">{times}</div>{"".join(day_columns)}</div>'
        '<div class="calendar-source-links">'
        f'<a href="{embed_url}" target="_blank" rel="noopener">Google 日历</a> · '
        f'<a href="{source_url_value}" target="_blank" rel="noopener">iCal</a>'
        '</div></div>'
    )


def generate_course_home() -> dict:
    home = fetch(ORIGINAL_HOME)
    data_dir = COURSE / "data" / "calendars"
    data_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"homepage": {"url": ORIGINAL_HOME, "sha256": sha256(home)}}
    archived_sections = []
    for slug, details in CALENDARS.items():
        data = normalize_ics(fetch(details["url"]))
        (data_dir / f"{slug}.ics").write_bytes(data)
        manifest[slug] = {"url": details["url"], "sha256": sha256(data), "bytes": len(data)}
        archived_sections.append(
            render_archive_calendar(slug, details["title"], data, details["url"], details["embed"])
        )
    (data_dir / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    page = (
        "---\n"
        "title: CS 61B 数据结构，2021 春季\n"
        "description: CS61B Spring 2021 原课程主页的中文归档版。\n"
        "template: course-home.html\n"
        "hide:\n  - navigation\n  - toc\n---\n\n"
        '<div class="segment" id="announcements">\n'
        '<div class="segmenttitle">公告 [<a href="https://sp21.datastructur.es/announcements.html" target="_blank" rel="noopener">查看全部</a>]</div>\n'
        '<div class="announcement-wrapper"><ul class="announcements"><li class="announcement-item">'
        '<div class="announcement-title-wrapper"><div class="tr"><div class="prev unreleased">«</div>'
        '<div class="td title">第 17 周公告</div><div class="td next">»</div></div></div>'
        '<p class="post-metadata">发布于 2021 年 5 月 9 日</p>'
        '<h3>期末考试</h3><p>大家好！期末考试安排在 5 月 11 日（周二）太平洋时间 8:10–11:00。请仔细阅读课程公告和相关文档中的全部信息。</p>'
        '<p>如果你以 P/NP 方式修读本课，并且不参加期末考试也已经取得及格所需分数，则无需参加期末考试。本科生的及格线为 C-，在 CS 61B 中对应 6,000 分。</p>'
        '<p>关于监考的更多细节将在次日上午发布。</p>'
        '<h3>课程评价（32 分额外加分）</h3><p>课程评价完成率为 75.84%，当晚截止。如果完成率达到 80%，所有学生都将获得 32 分额外加分。请在截止前填写'
        '<a href="https://course-evaluations.berkeley.edu/" target="_blank" rel="noopener">课程评价</a>。</p>'
        '<h3>期末问卷（32 分额外加分）</h3><p><a href="https://forms.gle/3dF8kSQXW1gtR6i57" target="_blank" rel="noopener">期末问卷</a>'
        '已经发布，完成后可获得 32 分额外加分。问卷于本周五截止，而且没有参与率要求。</p>'
        '<h3>Project 3 复核</h3><p>提交复核申请的同学，其 Beacon 分数已经更新。当前显示的就是 Project 3 检查环节最终分数，课程不再接受新的复核申请；仍有异议可在期末问卷中说明。</p>'
        '<h3>重要日期汇总</h3><ul><li>课程评价：当晚截止</li><li>期末考试：5 月 11 日 8:10–11:00（PT）</li>'
        '<li>期末问卷：5 月 14 日 23:59（PT）</li></ul></li></ul></div>\n'
        '</div>\n\n'
        '<div class="segment schedule" id="cal"><div class="segmenttitle">课程日历</div>\n'
        f'{build_main_calendar(home)}\n</div>\n\n'
        f'{"".join(archived_sections)}\n'
        '<div id="build_time"><em>最后构建：2021-05-15 03:55 UTC</em></div>\n'
    )
    course_dir = DOCS / "course"
    course_dir.mkdir(parents=True, exist_ok=True)
    (course_dir / "index.md").write_text(page, encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--refresh-course-home",
        action="store_true",
        help="also download and regenerate the archived original-style homepage and calendars",
    )
    parser.add_argument(
        "--refresh-images",
        action="store_true",
        help="redownload coursework images instead of reusing the verified local copies",
    )
    args = parser.parse_args()
    import_record = validate_source(args.source)
    source_texts = {
        (folder, filename): (args.source / folder / filename).read_text(encoding="utf-8")
        for folder, filename, *_ in ITEMS
    }
    image_replacements, image_manifest = vendor_images(source_texts, args.refresh_images)
    import_record["localized_images"] = image_manifest
    import_markdown(source_texts, image_replacements)
    if args.refresh_course_home:
        import_record["calendar_sources"] = generate_course_home()
    else:
        update_course_home_links()
        previous_manifest = DOCS / "coursework-import-manifest.json"
        if previous_manifest.is_file():
            previous = json.loads(previous_manifest.read_text(encoding="utf-8"))
            if "calendar_sources" in previous:
                import_record["calendar_sources"] = previous["calendar_sources"]
    (DOCS / "coursework-import-manifest.json").write_text(
        json.dumps(import_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Imported {len(ITEMS)} Lab, homework, and project pages plus 3 indexes.")


if __name__ == "__main__":
    main()
