#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
"$project_dir/scripts/build.sh"
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$project_dir/dist"
