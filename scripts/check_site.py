#!/usr/bin/env python3
"""Validate the aggregated static documentation site without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = PROJECT_ROOT / "courses" / "CS61B" / "2021Spring"
DOCS_ROOT = COURSE_ROOT / "docs"
SITE_ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else PROJECT_ROOT / "dist"
COURSE_SITE = SITE_ROOT / "CS61B" / "2021Spring"
REMOTE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(https?://", re.IGNORECASE)
EXPECTED_CHAPTERS = 22
EXPECTED_LEGACY_REDIRECTS = EXPECTED_CHAPTERS + 2
EXPECTED_HTML_PAGES = 56 + EXPECTED_LEGACY_REDIRECTS
EXPECTED_COURSEWORK = {"labs": 11, "homeworks": 3, "projects": 6, "exams": 4}
SEARCH_TERMS = ("并查集", "最短路径", "泛型", "JUnit", "Gitlet", "BYOW", "期中考试")
PAGES_RECOMMENDED_MAX_BYTES = 1_000_000_000


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.anchors: list[dict[str, str | None]] = []
        self.toc_links: list[str] = []
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.ignored_depth = 0
        self.toc_list_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if tag == "a" and values.get("href"):
            self.anchors.append(values)
            if self.toc_list_depth:
                self.toc_links.append(values["href"] or "")
        if tag == "ul":
            if self.toc_list_depth:
                self.toc_list_depth += 1
            elif values.get("data-md-component") == "toc":
                self.toc_list_depth = 1
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append(("src", values["src"] or ""))
        if tag in {"script", "style"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.ignored_depth:
            self.ignored_depth -= 1
        if tag == "ul" and self.toc_list_depth:
            self.toc_list_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.text.append(data)


def html_target(current: Path, raw_url: str) -> tuple[Path | None, str]:
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, ""
    path_text = unquote(parsed.path)
    if not path_text:
        target = current
    elif path_text.startswith("/"):
        target = SITE_ROOT / path_text.lstrip("/")
    else:
        target = current.parent / path_text
    if path_text.endswith("/") or (target.exists() and target.is_dir()):
        target = target / "index.html"
    return target.resolve(), unquote(parsed.fragment)


def main() -> None:
    errors: list[str] = []
    chapter_files = sorted((DOCS_ROOT / "chapters").glob("*.md"))
    if len(chapter_files) != EXPECTED_CHAPTERS:
        errors.append(f"expected {EXPECTED_CHAPTERS} chapter sources, got {len(chapter_files)}")

    for group, expected_count in EXPECTED_COURSEWORK.items():
        content_files = [path for path in (DOCS_ROOT / group).glob("*.md") if path.name != "index.md"]
        if len(content_files) != expected_count:
            errors.append(f"expected {expected_count} {group} sources, got {len(content_files)}")

    expected_new_coursework = (
        DOCS_ROOT / "projects" / "project-1ec-autograder.md",
        DOCS_ROOT / "projects" / "project-3-game-sharing.md",
    )
    for source_file in expected_new_coursework:
        if not source_file.is_file():
            errors.append(f"missing updated coursework source {source_file.relative_to(PROJECT_ROOT)}")
    if (DOCS_ROOT / "homeworks" / "hw-1-cancelled.md").exists():
        errors.append("HW 1 must not be published")

    attribution_lines = (
        "原作：Josh Hug，UC Berkeley CS61B Spring 2021 配套读本。",
        "中文翻译版，仅供非商业学习；采用 CC BY-NC-SA 4.0 许可。",
        "原始网站：https://joshhug.gitbooks.io/hug61b/content/",
    )
    for chapter_file in chapter_files:
        source = chapter_file.read_text(encoding="utf-8")
        for line in attribution_lines:
            if source.count(line) != 1:
                errors.append(f"chapter attribution must occur once in {chapter_file.name}: {line}")
        footer_start = source.rfind("\n---\n\n> 原作：Josh Hug")
        if (
            footer_start < 0
            or any(line in source[:footer_start] for line in attribution_lines)
            or not source.rstrip().endswith(attribution_lines[-1])
        ):
            errors.append(f"chapter attribution is not confined to the bottom of {chapter_file.name}")

    for markdown in DOCS_ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        if REMOTE_IMAGE_RE.search(text):
            errors.append(f"remote image remains in {markdown.relative_to(PROJECT_ROOT)}")

    required = [
        SITE_ROOT / "index.html",
        SITE_ROOT / "404.html",
        SITE_ROOT / "robots.txt",
        SITE_ROOT / "sitemap.xml",
        SITE_ROOT / "site-version.json",
        COURSE_SITE / "index.html",
        COURSE_SITE / "course" / "index.html",
        COURSE_SITE / "labs" / "index.html",
        COURSE_SITE / "homeworks" / "index.html",
        COURSE_SITE / "projects" / "index.html",
        COURSE_SITE / "exams" / "index.html",
        COURSE_SITE / "about" / "index.html",
        COURSE_SITE / "search" / "search_index.json",
        COURSE_SITE / "sitemap.xml",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing generated file {path.relative_to(SITE_ROOT)}")

    release = ""
    version_path = SITE_ROOT / "site-version.json"
    if version_path.is_file():
        try:
            release = str(json.loads(version_path.read_text(encoding="utf-8"))["version"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            errors.append("site-version.json is invalid")
        if release and not re.fullmatch(r"[0-9a-f]{16}", release):
            errors.append(f"invalid site release fingerprint: {release}")

    symlinks = list(SITE_ROOT.rglob("*")) if SITE_ROOT.exists() else []
    symlinks = [path for path in symlinks if path.is_symlink()]
    if symlinks:
        errors.append("GitHub Pages artifact contains symbolic links: " + ", ".join(str(path) for path in symlinks))
    artifact_bytes = sum(path.stat().st_size for path in SITE_ROOT.rglob("*") if path.is_file())
    if artifact_bytes >= PAGES_RECOMMENDED_MAX_BYTES:
        errors.append(f"GitHub Pages artifact is too large: {artifact_bytes} bytes")

    pages: dict[Path, PageParser] = {}
    for html_file in SITE_ROOT.rglob("*.html"):
        parser = PageParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        pages[html_file.resolve()] = parser

    rendered_attribution = re.compile(
        r"<blockquote>\s*<p>原作：Josh Hug，UC Berkeley CS61B Spring 2021 配套读本。"
        r".*?原始网站：https://joshhug\.gitbooks\.io/hug61b/content/</p>\s*"
        r"</blockquote>\s*</article>",
        re.DOTALL,
    )
    for chapter_file in chapter_files:
        rendered_chapter = COURSE_SITE / "chapters" / chapter_file.stem / "index.html"
        if not rendered_chapter.is_file():
            continue
        rendered_html = rendered_chapter.read_text(encoding="utf-8")
        if len(rendered_attribution.findall(rendered_html)) != 1:
            errors.append(
                f"rendered chapter attribution is not the final article block in {chapter_file.name}"
            )

    if len(pages) != EXPECTED_HTML_PAGES:
        errors.append(f"expected {EXPECTED_HTML_PAGES} generated HTML pages, got {len(pages)}")

    legacy_redirects = {
        SITE_ROOT / "about" / "index.html": "/CS61B/2021Spring/about/",
        SITE_ROOT / "chapters" / "index.html": "/CS61B/2021Spring/",
    }
    for chapter_file in chapter_files:
        slug = chapter_file.stem
        legacy_redirects[SITE_ROOT / "chapters" / slug / "index.html"] = (
            f"/CS61B/2021Spring/chapters/{slug}/"
        )
    if len(legacy_redirects) != EXPECTED_LEGACY_REDIRECTS:
        errors.append(f"expected {EXPECTED_LEGACY_REDIRECTS} legacy redirects, got {len(legacy_redirects)}")
    for redirect_path, target in legacy_redirects.items():
        if not redirect_path.is_file():
            errors.append(f"missing legacy redirect {redirect_path.relative_to(SITE_ROOT)}")
            continue
        redirect_html = redirect_path.read_text(encoding="utf-8")
        for marker in ('name="robots" content="noindex"', 'http-equiv="refresh"', "window.location.replace", target):
            if marker not in redirect_html:
                errors.append(f"invalid legacy redirect {redirect_path.relative_to(SITE_ROOT)}: missing {marker}")

    normal_pages = set(pages) - {path.resolve() for path in legacy_redirects}
    for html_file in normal_pages:
        html_text = html_file.read_text(encoding="utf-8")
        if "__SITE_RELEASE__" in html_text:
            errors.append(f"unstamped release placeholder in {html_file.relative_to(SITE_ROOT)}")
        for marker in (
            f'name="site-release" content="{release}"',
            'http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"',
            'site-version.json',
            '_docs_release',
        ):
            if release and marker not in html_text:
                errors.append(f"cache refresh marker missing in {html_file.relative_to(SITE_ROOT)}: {marker}")
        parser = pages[html_file]
        for attribute, url in parser.links:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path.endswith((".css", ".js")):
                continue
            if release and parse_qs(parsed.query).get("sitev") != [release]:
                errors.append(f"unversioned runtime asset in {html_file.relative_to(SITE_ROOT)}: {url}")

    search_bundles = list((COURSE_SITE / "assets" / "javascripts").glob("bundle.*.min.js"))
    if len(search_bundles) != 1:
        errors.append(f"expected one Material runtime bundle, got {len(search_bundles)}")
    elif release and f"search/search_index.json?sitev={release}" not in search_bundles[0].read_text(encoding="utf-8"):
        errors.append("Material runtime does not use the versioned search index")

    for group in ("labs", "homeworks", "projects"):
        for html_file in (COURSE_SITE / group).glob("*/index.html"):
            html_text = html_file.read_text(encoding="utf-8")
            if 'class="md-sidebar md-sidebar--secondary"' not in html_text:
                errors.append(f"{group} page is missing the standard right-side table of contents: {html_file.parent.name}")

    for html_file, parser in list(pages.items()):
        visible_text = " ".join(parser.text)
        if "Spring 2019" in visible_text:
            errors.append(f"stale visible course year in {html_file.relative_to(SITE_ROOT)}")
        for attribute, url in parser.links:
            target, fragment = html_target(html_file, url)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"broken {attribute} in {html_file.relative_to(SITE_ROOT)}: {url}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    pages[target] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(f"missing anchor in {html_file.relative_to(SITE_ROOT)}: {url}")

    search_path = COURSE_SITE / "search" / "search_index.json"
    if search_path.is_file():
        search_text = json.dumps(json.loads(search_path.read_text(encoding="utf-8")), ensure_ascii=False)
        search_text = search_text.replace("\u200b", "")
        for term in SEARCH_TERMS:
            if term not in search_text:
                errors.append(f"search index does not contain {term}")

    external_scripts: list[str] = []
    for html_file, parser in pages.items():
        for attribute, url in parser.links:
            if attribute == "src" and urlsplit(url).scheme in {"http", "https"}:
                external_scripts.append(f"{html_file.relative_to(SITE_ROOT)}: {url}")
    if external_scripts:
        errors.append("external runtime assets found:\n" + "\n".join(external_scripts))

    portal_html = (SITE_ROOT / "index.html").read_text(encoding="utf-8") if (SITE_ROOT / "index.html").is_file() else ""
    if "CS61B/2021Spring/" not in portal_html:
        errors.append("portal does not link to CS61B Spring 2021")
    if "CS自学材料" not in portal_html:
        errors.append("portal does not use the CS自学材料 site name")
    if "Everlasting 中文教程" in portal_html:
        errors.append("portal still contains the previous site name")
    if 'id="课程"' not in portal_html:
        errors.append("portal does not contain the 课程 section")

    chapter_four = COURSE_SITE / "chapters" / "04-inheritance-and-interfaces" / "index.html"
    if chapter_four.is_file():
        chapter_four_html = chapter_four.read_text(encoding="utf-8")
        for section in ("4.1", "4.2", "4.3", "4.4"):
            if section not in chapter_four_html:
                errors.append(f"chapter 4 navigation does not contain {section}")

    course_home_path = COURSE_SITE / "index.html"
    if course_home_path.is_file():
        course_home_html = course_home_path.read_text(encoding="utf-8")
        for label in ("临时首页", "开始阅读", "中文课程主页", "返回教程总目录", "课程教材"):
            if label not in course_home_html:
                errors.append(f"course Material homepage is missing {label}")
        if "课程章节" in course_home_html:
            errors.append("course Material homepage still contains 课程章节")
        if "navigation.instant" in course_home_html:
            errors.append("instant navigation must stay disabled because /course/ uses a standalone template")
        if "navigation.tabs.sticky" in course_home_html:
            errors.append("top navigation tabs must scroll away with the page")

    original_style_path = COURSE_SITE / "course" / "index.html"
    if original_style_path.is_file():
        original_style_html = original_style_path.read_text(encoding="utf-8")
        for marker in (
            'class="sp21-course-home"', "CS 61B", "数据结构，2021 春季", "第 17 周公告",
            "周次", "日期", "阅读", "讲座", "讨论", "实验", "作业 / 考试",
            "实验与讨论安排", "答疑时间", "期末考试周", "最后构建：2021-05-15 03:55 UTC",
        ):
            if marker not in original_style_html:
                errors.append(f"original-style course homepage is missing {marker}")
        if 'class="md-header' in original_style_html or 'class="md-sidebar' in original_style_html:
            errors.append("original-style course homepage unexpectedly contains Material chrome")
        if original_style_html.count('class="week-calendar"') != 2:
            errors.append("course homepage does not contain the two original-style weekly calendars")
        if "calendar-scroll compact" in original_style_html:
            errors.append("course homepage still contains the incorrect long-list calendar")
        for extra_copy in ("中文归档说明", "下列内容由两份公开 ICS", "会议链接按原记录保留"):
            if extra_copy in original_style_html:
                errors.append(f"course homepage contains non-original explanatory copy: {extra_copy}")
        if re.search(r"sp21\.datastructur\.es/materials/(?:lab|hw|proj)/", original_style_html):
            errors.append("coursework link on original-style homepage was not mapped to the Chinese site")
        course_parser = pages.get(original_style_path.resolve())
        if course_parser:
            for anchor in course_parser.anchors:
                href = anchor.get("href") or ""
                if urlsplit(href).scheme in {"http", "https"}:
                    rel = anchor.get("rel") or ""
                    if anchor.get("target") != "_blank" or "noopener" not in rel:
                        errors.append(f"external link lacks safe new-window attributes on course homepage: {href}")

    calendar_data = COURSE_ROOT / "data" / "calendars"
    for filename in ("lab-discussions.ics", "office-hours.ics", "sources.json"):
        if not (calendar_data / filename).is_file():
            errors.append(f"missing archived calendar source {filename}")

    if errors:
        print("Site validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"Validated {len(pages)} HTML pages, {len(chapter_files)} chapters, "
        f"{len(legacy_redirects)} legacy redirects, a {artifact_bytes}-byte Pages artifact, "
        "two site roots, and local-only runtime assets."
    )


if __name__ == "__main__":
    main()
