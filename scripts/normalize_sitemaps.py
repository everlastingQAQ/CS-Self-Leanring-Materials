#!/usr/bin/env python3
"""Remove misleading build-wide lastmod values from generated sitemaps."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


LASTMOD_RE = re.compile(r"\s*<lastmod\b[^>]*>.*?</lastmod>", re.DOTALL)


def normalize(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    ET.fromstring(source)
    normalized = LASTMOD_RE.sub("", source)
    ET.fromstring(normalized)
    if "<lastmod" in normalized:
        raise RuntimeError(f"failed to remove lastmod from {path}")
    path.write_text(normalized, encoding="utf-8")
    print(f"Normalized sitemap: {path}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: normalize_sitemaps.py DIST_DIR")
    site_root = Path(sys.argv[1]).resolve()
    sitemap_paths = (
        site_root / "sitemap.xml",
        site_root / "CS61B" / "2021Spring" / "sitemap.xml",
    )
    missing = [str(path) for path in sitemap_paths if not path.is_file()]
    if missing:
        raise SystemExit("Missing generated sitemaps:\n" + "\n".join(missing))
    for sitemap_path in sitemap_paths:
        normalize(sitemap_path)


if __name__ == "__main__":
    main()
