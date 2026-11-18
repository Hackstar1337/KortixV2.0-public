#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
image="kortix-v2-contract:local"
docker build --platform linux/amd64 -f "$root/selfhost/Dockerfile.contract" -t "$image" "$root"
docker run --rm --network none --read-only --tmpfs /tmp "$image"
