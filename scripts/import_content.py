#!/usr/bin/env python3
"""Import the immutable Hug61B Markdown source and vendor remote assets."""

from __future__ import annotations

import argparse
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

CHAPTER_DESCRIPTIONS = {
    "00-introduction.md": "CS61B 中文教材导论，介绍课程学习方式、Java 编程环境、数据结构与算法主题以及配套练习的使用方法。",
    "01-java-basics.md": "CS61B Java 入门中文教程，讲解变量、控制流、函数、类、对象、静态成员、构造方法与数组等核心语法。",
    "02-lists.md": "CS61B 列表中文教程，涵盖引用、递归、链表、哨兵节点、双向链表、数组列表与动态扩容策略。",
    "03-testing.md": "CS61B 测试中文教程，介绍 JUnit、单元测试、测试驱动开发、异常测试以及调试程序的基本方法。",
    "04-inheritance-and-interfaces.md": "CS61B 继承与接口中文教程，讲解接口实现、方法重写、动态方法选择、类型转换与高阶函数。",
    "05-generics-and-autoboxing.md": "CS61B 泛型与自动装箱中文教程，介绍泛型类、泛型方法、类型参数、包装类型和 Java 自动装箱机制。",
    "06-exceptions-iterators-object-methods.md": "CS61B Java 进阶中文教程，讲解异常处理、迭代器与 Iterable 接口，以及 Object 类常用方法。",
    "07-packages-and-access-control.md": "CS61B 包与访问控制中文教程，介绍 Java 包结构、导入规则、访问修饰符和模块化代码组织方式。",
    "08-efficient-programming-and-asymptotic-analysis.md": "CS61B 渐近分析中文教程，讲解高效编程、运行时间估算、渐近符号与常见算法复杂度。",
    "09-disjoint-sets.md": "CS61B 并查集中文教程，涵盖 Quick Find、Quick Union、加权合并、路径压缩与复杂度分析。",
    "10-adts-and-trees.md": "CS61B 抽象数据类型与树中文教程，介绍 ADT、二叉树、二叉搜索树以及树结构的基本操作。",
    "11-balanced-trees.md": "CS61B 平衡树中文教程，讲解 2-3 树、旋转操作、左倾红黑树和保持搜索树平衡的方法。",
    "12-hashing.md": "CS61B 哈希中文教程，介绍哈希函数、哈希表、冲突处理、负载因子、扩容与性能分析。",
    "13-heaps-and-priority-queues.md": "CS61B 堆与优先队列中文教程，讲解二叉堆、堆操作、优先队列接口及其渐近运行时间。",
    "14-data-structures-summary.md": "CS61B 数据结构总结中文教程，对比列表、集合、映射、树、哈希表、堆等结构的用途与复杂度。",
    "15-tries.md": "CS61B Trie 字典树中文教程，介绍字符串键集合、前缀查询、Trie 结构及其时间与空间权衡。",
    "16-quadtrees-and-kd-trees.md": "CS61B 空间数据结构中文教程，讲解四叉树、K-D 树、最近邻搜索与多维空间划分。",
    "17-tree-traversals-and-graphs.md": "CS61B 树遍历与图中文教程，介绍深度优先遍历、广度优先遍历以及图模型的基本概念。",
    "18-graph-traversal-and-representation.md": "CS61B 图遍历与表示中文教程，讲解邻接表、邻接矩阵、DFS、BFS 与图算法实现方式。",
    "19-shortest-paths.md": "CS61B 最短路径中文教程，介绍最短路径树、Dijkstra 算法、A* 搜索及边权条件。",
    "20-minimum-spanning-trees.md": "CS61B 最小生成树中文教程，讲解割性质、Prim 算法、Kruskal 算法与并查集的应用。",
    "21-reductions-and-decomposition.md": "CS61B 归约与分解中文教程，介绍问题归约、图算法应用、拓扑排序与复杂问题的分解方法。",
}

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+([\"'][^\"']*[\"']))?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
ATTRIBUTION_RE = re.compile(
    r"(?:\n---\n\n)?"
    r"^> 原作：Josh Hug，UC Berkeley CS61B Spring 2021 配套读本。(?:[ \t]{2}|<br>)?\n"
    r"^> 中文翻译版，仅供非商业学习；采用 CC BY-NC-SA 4.0 许可。(?:[ \t]{2}|<br>)?\n"
    r"^> 原始网站：https://joshhug\.gitbooks\.io/hug61b/content/?\n?",
    re.MULTILINE,
)
ATTRIBUTION_FOOTER = (
    "---\n\n"
    "> 原作：Josh Hug，UC Berkeley CS61B Spring 2021 配套读本。<br>\n"
    "> 中文翻译版，仅供非商业学习；采用 CC BY-NC-SA 4.0 许可。<br>\n"
    "> 原始网站：https://joshhug.gitbooks.io/hug61b/content/"
)
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n+", re.DOTALL)


def apply_chapter_metadata(text: str, destination: str) -> str:
    """Set deterministic SEO metadata while preserving the imported body."""
    description = CHAPTER_DESCRIPTIONS[destination]
    body = FRONT_MATTER_RE.sub("", text, count=1)
    front_matter = f"---\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n"
    return front_matter + body.lstrip()


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


def move_attribution_to_bottom(text: str) -> str:
    """Keep one course attribution block at the very end of a chapter."""
    body = ATTRIBUTION_RE.sub("", text)
    body = re.sub(r"\A(#[^\n]+\n)\n+", r"\1\n", body).rstrip()
    body = re.sub(
        r"\A(#[^\n]+\n\n---\n)(?:[ \t]*\n)+---\n",
        r"\1",
        body,
        count=1,
    )
    return f"{body}\n\n{ATTRIBUTION_FOOTER}\n"


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--attribution-only",
        action="store_true",
        help="move the attribution in existing generated chapters without downloading assets",
    )
    args = parser.parse_args()

    if args.attribution_only:
        missing = [
            str(CHAPTERS_ROOT / destination)
            for _, destination in CHAPTERS
            if not (CHAPTERS_ROOT / destination).is_file()
        ]
        if missing:
            raise SystemExit("Missing generated chapter files:\n" + "\n".join(missing))
        for _, destination in CHAPTERS:
            chapter = CHAPTERS_ROOT / destination
            chapter.write_text(
                apply_chapter_metadata(
                    move_attribution_to_bottom(chapter.read_text(encoding="utf-8")),
                    destination,
                ),
                encoding="utf-8",
            )
        print(f"Updated metadata and attribution in {len(CHAPTERS)} generated chapters.")
        return

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

        rendered = apply_chapter_metadata(
            move_attribution_to_bottom(IMAGE_RE.sub(replace_image, text)),
            destination,
        )
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
