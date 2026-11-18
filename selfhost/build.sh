#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
mode="${1:-all}"
version="$(tr -d '\r\n' < VERSION)"
commit="$(git rev-parse HEAD 2>/dev/null || printf unknown)"
api_image="${KORTIX_API_IMAGE:-kortix-v2-api:local}"
frontend_image="${KORTIX_FRONTEND_IMAGE:-kortix-v2-frontend:local}"
gateway_image="${KORTIX_GATEWAY_IMAGE:-kortix-v2-gateway:local}"
case "$mode" in cli|api|frontend|gateway|all) ;; *) echo 'Usage: bash selfhost/build.sh [cli|api|frontend|gateway|all]' >&2;exit 2;; esac
docker info >/dev/null
docker compose version >/dev/null
if [ "$mode" = cli ];then
 image="kortix-v2-cli-build:local"
 docker build --platform linux/amd64 --target sandbox-cli --build-arg SERVICE=apps/api --build-arg KORTIX_VERSION="$version" --build-arg KORTIX_COMMIT="$commit" -f apps/api/Dockerfile -t "$image" .
 container="$(docker create "$image")"
 trap 'docker rm -f "$container" >/dev/null 2>&1 || true' EXIT
 mkdir -p selfhost/bin
 for name in kortix kortix.version kortix-connectors-runtime.attestation.json;do docker cp "$container:/cli/apps/cli/dist/$name" "selfhost/bin/$name";done
 chmod 700 selfhost/bin/kortix
 echo 'Source-built Linux amd64 CLI exported to selfhost/bin/kortix.'
 exit 0
fi
if [ "$mode" = api ] || [ "$mode" = all ];then
 docker build --platform linux/amd64 --build-arg SERVICE=apps/api --build-arg KORTIX_VERSION="$version" --build-arg KORTIX_COMMIT="$commit" -f apps/api/Dockerfile -t "$api_image" .
fi
if [ "$mode" = gateway ] || [ "$mode" = all ];then
 docker build --platform linux/amd64 --build-arg KORTIX_VERSION="$version" --build-arg KORTIX_COMMIT="$commit" -f apps/llm-gateway/Dockerfile -t "$gateway_image" .
fi
if [ "$mode" = frontend ] || [ "$mode" = all ];then
 args=()
 for key in NEXT_PUBLIC_BACKEND_URL NEXT_PUBLIC_URL NEXT_PUBLIC_SUPABASE_URL NEXT_PUBLIC_SUPABASE_ANON_KEY NEXT_PUBLIC_BILLING_ENABLED;do
  if [ -n "${!key:-}" ];then args+=(--build-arg "$key=${!key}");fi
 done
 docker build --platform linux/amd64 "${args[@]}" -f selfhost/Dockerfile.frontend -t "$frontend_image" .
fi
echo 'Build complete. No deployment or registry push was performed.'
