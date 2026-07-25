#!/usr/bin/env python3
"""Import the immutable Hug61B Markdown source and vendor remote assets."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import mimetypes
import os
import re
import shutil
import tarfile
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get("HUG61B_SOURCE", "/home/everlasting/下载/Hug61B_分章Markdown"))
COURSE_ROOT = PROJECT_ROOT / "courses" / "CS61B" / "2021Spring"
DOCS_ROOT = COURSE_ROOT / "docs"
CHAPTERS_ROOT = DOCS_ROOT / "chapters"
IMAGES_ROOT = DOCS_ROOT / "assets" / "images"
VENDOR_ROOT = DOCS_ROOT / "assets" / "vendor"
MATHJAX_VERSION = "3.2.2"
MATHJAX_URL = f"https://registry.npmjs.org/mathjax/-/mathjax-{MATHJAX_VERSION}.tgz"
FALLBACK_URLS = {
    "https://wcs.smartdraw.com/organizational-chart/img/org-chart-software-maker.png?bn=1510011143":
        "https://web.archive.org/web/20220120174958id_/https://wcs.smartdraw.com/organizational-chart/img/org-chart-software-maker.png"
}

CHAPTERS = [
    ("00_导论.md", "00-introduction.md"),
    ("01_Java入门.md", "01-java-basics.md"),
    ("02_列表.md", "02-lists.md"),
    ("03_测试.md", "03-testing.md"),
    ("04_继承与接口.md", "04-inheritance-and-interfaces.md"),
    ("05_泛型与自动装箱.md", "05-generics-and-autoboxing.md"),
    ("06_异常迭代器与Object方法.md", "06-exceptions-iterators-object-methods.md"),
    ("07_包与访问控制.md", "07-packages-and-access-control.md"),
    ("08_高效编程与渐近分析.md", "08-efficient-programming-and-asymptotic-analysis.md"),
    ("09_并查集.md", "09-disjoint-sets.md"),
    ("10_抽象数据类型与树.md", "10-adts-and-trees.md"),
    ("11_平衡树.md", "11-balanced-trees.md"),
    ("12_哈希.md", "12-hashing.md"),
    ("13_堆与优先队列.md", "13-heaps-and-priority-queues.md"),
    ("14_数据结构总结.md", "14-data-structures-summary.md"),
    ("15_Trie字典树.md", "15-tries.md"),
    ("16_四叉树与KD树.md", "16-quadtrees-and-kd-trees.md"),
    ("17_树遍历与图.md", "17-tree-traversals-and-graphs.md"),
    ("18_图遍历与表示.md", "18-graph-traversal-and-representation.md"),
    ("19_最短路径.md", "19-shortest-paths.md"),
    ("20_最小生成树.md", "20-minimum-spanning-trees.md"),
    ("21_归约与分解.md", "21-reductions-and-decomposition.md"),
]

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+([\"'][^\"']*[\"']))?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def normalize_course_text(text: str) -> str:
    """Normalize rendered course metadata and heading levels without touching the source."""
    text = text.replace("UC Berkeley CS61B Spring 2019", "UC Berkeley CS61B Spring 2021")
    text = text.replace("课程 2019 年春季版本", "课程 2021 年春季版本")
    text = text.replace(
        "[https://sp19.datastructur.es/](https://sp19.datastructur.es/)",
        "[https://sp21.datastructur.es/](https://sp21.datastructur.es/)",
    )
    normalized: list[str] = []
    chapter_title_seen = False
    section_seen = False

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match is None:
            normalized.append(line)
            continue

        hashes, title = match.groups()
        level = len(hashes)
        if level == 1 and not chapter_title_seen:
            chapter_title_seen = True
        elif level == 1:
            if not re.match(r"\d+\.\d+\s+", title):
                title = title if title.startswith("附录：") else f"附录：{title}"
            level = 2
            section_seen = True
        elif section_seen:
            level = min(level + 1, 6)

        normalized.append(f"{'#' * level} {title}")

    return "\n".join(normalized) + "\n"


def fetch(url: str, attempts: int = 4) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "CS61B-docs-builder/1.0 (+https://docs.everlasting.xin/CS61B/2021Spring/)"},
            )
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read()
                content_type = response.headers.get_content_type()
                if not data:
                    raise RuntimeError("empty response")
                return data, content_type
        except Exception as exc:  # noqa: BLE001 - include network failures in the report
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed after {attempts} attempts: {last_error}")


def extension_for(url: str, content_type: str) -> str:
    suffix = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    guessed = mimetypes.guess_extension(content_type) or ".bin"
    return ".jpg" if guessed == ".jpe" else guessed


def image_name(url: str, content_type: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    raw_name = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).stem
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", raw_name).strip("-._")[:64] or "image"
    return f"{digest}-{safe_name}{extension_for(url, content_type)}"


def vendor_images(chapter_texts: dict[str, str]) -> tuple[dict[str, str], list[dict[str, object]]]:
    urls = sorted({match.group(2) for text in chapter_texts.values() for match in IMAGE_RE.finditer(text)})
    downloaded: dict[str, tuple[bytes, str, str]] = {}
    failures: list[str] = []

    def download(url: str) -> tuple[str, bytes, str, str]:
        retrieval_url = FALLBACK_URLS.get(url, url)
        data, content_type = fetch(retrieval_url)
        return url, data, content_type, retrieval_url

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                fetched_url, data, content_type, retrieval_url = future.result()
                downloaded[fetched_url] = (data, content_type, retrieval_url)
                print(f"downloaded {len(downloaded):3d}/{len(urls)} {url}")
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{url}: {exc}")

    if failures:
        raise RuntimeError("Image download failures:\n" + "\n".join(failures))

    if IMAGES_ROOT.exists():
        shutil.rmtree(IMAGES_ROOT)
    IMAGES_ROOT.mkdir(parents=True)

    replacements: dict[str, str] = {}
    manifest: list[dict[str, object]] = []
    for url in urls:
        data, content_type, retrieval_url = downloaded[url]
        filename = image_name(url, content_type)
        output = IMAGES_ROOT / filename
        output.write_bytes(data)
        local_path = f"../assets/images/{filename}"
        replacements[url] = local_path
        manifest.append(
            {
                "source_url": url,
                "retrieved_from": retrieval_url,
                "local_path": f"assets/images/{filename}",
                "content_type": content_type,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    (IMAGES_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return replacements, manifest


def vendor_mathjax() -> None:
    destination = VENDOR_ROOT / "mathjax"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    archive_data, _ = fetch(MATHJAX_URL)
    with tempfile.NamedTemporaryFile(suffix=".tgz") as archive_file:
        archive_file.write(archive_data)
        archive_file.flush()
        with tarfile.open(archive_file.name, "r:gz") as archive:
            members = [member for member in archive.getmembers() if member.name.startswith("package/es5/")]
            for member in members:
                relative = Path(member.name).relative_to("package")
                target = destination / relative
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    source = archive.extractfile(member)
                    if source is None:
                        raise RuntimeError(f"Cannot extract {member.name}")
                    target.write_bytes(source.read())
    (destination / "VERSION").write_text(MATHJAX_VERSION + "\n", encoding="utf-8")


def main() -> None:
    missing = [str(SOURCE_ROOT / source) for source, _ in CHAPTERS if not (SOURCE_ROOT / source).is_file()]
    if missing:
        raise SystemExit("Missing source files:\n" + "\n".join(missing))

    chapter_texts = {
        source: (SOURCE_ROOT / source).read_text(encoding="utf-8") for source, _ in CHAPTERS
    }
    replacements, manifest = vendor_images(chapter_texts)
    vendor_mathjax()

    if CHAPTERS_ROOT.exists():
        shutil.rmtree(CHAPTERS_ROOT)
    CHAPTERS_ROOT.mkdir(parents=True)

    for source, destination in CHAPTERS:
        text = normalize_course_text(chapter_texts[source])

        def replace_image(match: re.Match[str]) -> str:
            alt, url, title = match.groups()
            title_suffix = f" {title}" if title else ""
            return f"![{alt}]({replacements[url]}{title_suffix})"

        rendered = IMAGE_RE.sub(replace_image, text)
        (CHAPTERS_ROOT / destination).write_text(rendered, encoding="utf-8")

    summary = {
        "source_root": SOURCE_ROOT.name,
        "chapters": len(CHAPTERS),
        "images": len(manifest),
        "mathjax_version": MATHJAX_VERSION,
    }
    (DOCS_ROOT / "import-manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
