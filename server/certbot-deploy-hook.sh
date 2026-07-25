#!/usr/bin/env bash
set -euo pipefail

certificate_source=/etc/letsencrypt/live/docs.everlasting.xin
certificate_target=/opt/1panel/www/sites/docs.everlasting.xin/ssl
openresty_container=1Panel-openresty-j1tG

install -d -m 700 "$certificate_target"
install -m 644 "$certificate_source/fullchain.pem" "$certificate_target/fullchain.pem"
install -m 600 "$certificate_source/privkey.pem" "$certificate_target/privkey.pem"

if ! validation_output=$(docker exec "$openresty_container" openresty -t 2>&1); then
    printf '%s\n' "$validation_output" >&2
    exit 1
fi

if ! reload_output=$(docker exec "$openresty_container" openresty -s reload 2>&1); then
    printf '%s\n' "$reload_output" >&2
    exit 1
fi
