#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
image_name=everlasting-docs:9.7.7
dist_dir="$project_dir/dist"

docker build --tag "$image_name" "$project_dir"
rm -rf "$dist_dir"
mkdir -p "$dist_dir/CS61B/2021Spring"
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --volume "$project_dir:/site" \
  --workdir /site \
  "$image_name" build --config-file portal/mkdocs.yml --strict --clean --site-dir /site/dist
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --volume "$project_dir:/site" \
  --workdir /site \
  "$image_name" build --config-file courses/CS61B/2021Spring/mkdocs.yml --strict --clean \
  --site-dir /site/dist/CS61B/2021Spring
python3 "$project_dir/scripts/normalize_sitemaps.py" "$dist_dir"
python3 "$project_dir/scripts/generate_legacy_redirects.py" "$dist_dir"
python3 "$project_dir/scripts/stamp_release.py" "$dist_dir"
python3 "$project_dir/scripts/check_site.py" "$dist_dir"
