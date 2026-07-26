#!/usr/bin/env python3
"""Stamp a static build with a content release and version local runtime assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


PLACEHOLDER = "__SITE_RELEASE__"
VERSION_FILE = "site-version.json"
ASSET_RE = re.compile(
    r'(?P<prefix>\b(?:href|src)=["\'])(?P<url>(?!https?:|//|data:|#)[^"\']+\.(?:css|js)(?:\?[^"\']*)?)(?P<suffix>["\'])'
)
CONFIG_ASSET_RE = re.compile(r'(?P<prefix>"search"\s*:\s*")(?P<url>[^"]+\.js)(?P<suffix>")')


def release_for(site_root: Path) -> str:
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    digest.update(b"\0")
    for path in sorted(item for item in site_root.rglob("*") if item.is_file() and item.name != VERSION_FILE):
        digest.update(path.relative_to(site_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:16]


def versioned_url(url: str, release: str) -> str:
    parsed = urlsplit(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["sitev"] = release
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def stamp_html(path: Path, release: str) -> bool:
    source = path.read_text(encoding="utf-8")
    if PLACEHOLDER not in source:
        return False
    stamped = source.replace(PLACEHOLDER, release)
    stamped = ASSET_RE.sub(
        lambda match: f'{match.group("prefix")}{versioned_url(match.group("url"), release)}{match.group("suffix")}',
        stamped,
    )
    stamped = CONFIG_ASSET_RE.sub(
        lambda match: f'{match.group("prefix")}{versioned_url(match.group("url"), release)}{match.group("suffix")}',
        stamped,
    )
    path.write_text(stamped, encoding="utf-8")
    return True


def stamp_search_index_loader(site_root: Path, release: str) -> int:
    stamped = 0
    needle = 'search/search_index.json'
    replacement = f'{needle}?sitev={release}'
    for bundle in site_root.rglob("bundle.*.min.js"):
        source = bundle.read_text(encoding="utf-8")
        if needle not in source:
            continue
        bundle.write_text(source.replace(needle, replacement), encoding="utf-8")
        stamped += 1
    return stamped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_root", type=Path)
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    release = release_for(site_root)
    search_loaders = stamp_search_index_loader(site_root, release)
    if not search_loaders:
        raise SystemExit("no Material search-index loader was found")
    stamped = sum(stamp_html(path, release) for path in site_root.rglob("*.html"))
    if not stamped:
        raise SystemExit("no generated HTML contained the release placeholder")
    (site_root / VERSION_FILE).write_text(
        json.dumps({"version": release}, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"Stamped {stamped} HTML pages and {search_loaders} search loaders with release {release}.")


if __name__ == "__main__":
    main()
