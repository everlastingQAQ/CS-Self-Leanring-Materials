#!/usr/bin/env python3
"""Generate static redirect pages for URLs formerly handled by OpenResty."""

from __future__ import annotations

import html
import sys
from pathlib import Path


SITE_ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("dist").resolve()
COURSE_PREFIX = "/CS61B/2021Spring"


def redirect_document(target: str) -> str:
    escaped_target = html.escape(target, quote=True)
    javascript_target = target.replace("\\", "\\\\").replace('"', '\\"')
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="robots" content="noindex">
    <meta http-equiv="refresh" content="0; url={escaped_target}">
    <link rel="canonical" href="https://docs.everlasting.xin{escaped_target}">
    <title>页面已迁移</title>
    <script>window.location.replace("{javascript_target}" + window.location.search + window.location.hash);</script>
  </head>
  <body>
    <p>页面已迁移至 <a href="{escaped_target}">{escaped_target}</a>。</p>
  </body>
</html>
"""


def write_redirect(relative_path: str, target: str) -> None:
    destination = SITE_ROOT / relative_path / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(redirect_document(target), encoding="utf-8")


def main() -> None:
    chapters = SITE_ROOT / COURSE_PREFIX.lstrip("/") / "chapters"
    chapter_slugs = sorted(path.name for path in chapters.iterdir() if path.is_dir())
    if len(chapter_slugs) != 22:
        raise SystemExit(f"expected 22 generated chapter directories, got {len(chapter_slugs)}")

    write_redirect("about", f"{COURSE_PREFIX}/about/")
    write_redirect("chapters", f"{COURSE_PREFIX}/")
    for slug in chapter_slugs:
        write_redirect(f"chapters/{slug}", f"{COURSE_PREFIX}/chapters/{slug}/")

    print(f"Generated {len(chapter_slugs) + 2} legacy redirect pages.")


if __name__ == "__main__":
    main()
