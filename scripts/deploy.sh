#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ssh_key=${HUG61B_SSH_KEY:-/home/everlasting/.ssh/aliyun_astrbot}
server=root@39.107.112.250
ssh_port=2222
remote_root=/opt/1panel/www/sites/docs.everlasting.xin
git_sha=$(git -C "$project_dir" rev-parse --short=12 HEAD 2>/dev/null || printf '%s' uncommitted)
release_id=$(date -u +%Y%m%dT%H%M%SZ)-$git_sha
release_dir="$remote_root/releases/$release_id"

if [[ ! -f "$project_dir/dist/index.html" || ! -f "$project_dir/dist/CS61B/2021Spring/index.html" ]]; then
  echo "Missing aggregate build; run ./scripts/build.sh first." >&2
  exit 1
fi

ssh -p "$ssh_port" -i "$ssh_key" "$server" \
  "install -d -m 755 '$release_dir' '$remote_root/releases' '$remote_root/acme' '$remote_root/ssl'"

rsync --archive --delete \
  --chmod=D755,F644 \
  --rsh="ssh -p $ssh_port -i $ssh_key" \
  "$project_dir/dist/" "$server:$release_dir/"

ssh -p "$ssh_port" -i "$ssh_key" "$server" \
  "ln -sfn 'releases/$release_id' '$remote_root/current.next' && mv -Tf '$remote_root/current.next' '$remote_root/current'"

echo "DEPLOYED_RELEASE=$release_id"
