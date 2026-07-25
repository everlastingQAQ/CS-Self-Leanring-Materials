#!/usr/bin/env python3
"""Validate the aggregated static documentation site without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = PROJECT_ROOT / "courses" / "CS61B" / "2021Spring"
DOCS_ROOT = COURSE_ROOT / "docs"
SITE_ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else PROJECT_ROOT / "dist"
COURSE_SITE = SITE_ROOT / "CS61B" / "2021Spring"
REMOTE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(https?://", re.IGNORECASE)
EXPECTED_CHAPTERS = 22
SEARCH_TERMS = ("并查集", "最短路径", "泛型")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append(("src", values["src"] or ""))
        if tag in {"script", "style"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.ignored_depth:
            self.ignored_depth -= 1

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

    for markdown in DOCS_ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        if REMOTE_IMAGE_RE.search(text):
            errors.append(f"remote image remains in {markdown.relative_to(PROJECT_ROOT)}")

    required = [
        SITE_ROOT / "index.html",
        SITE_ROOT / "404.html",
        SITE_ROOT / "robots.txt",
        SITE_ROOT / "sitemap.xml",
        COURSE_SITE / "index.html",
        COURSE_SITE / "about" / "index.html",
        COURSE_SITE / "search" / "search_index.json",
        COURSE_SITE / "sitemap.xml",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing generated file {path.relative_to(SITE_ROOT)}")

    pages: dict[Path, PageParser] = {}
    for html_file in SITE_ROOT.rglob("*.html"):
        parser = PageParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        pages[html_file.resolve()] = parser

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

    if errors:
        print("Site validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"Validated {len(pages)} HTML pages, {len(chapter_files)} chapters, "
        "two site roots, and local-only runtime assets."
    )


if __name__ == "__main__":
    main()
