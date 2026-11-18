# Kortix V2.0 Public

A complete, independently maintained Kortix source distribution with **Docker Cloud Sandboxes** and portable self-host setup tooling.

Maintained by **Ashwin D** · [Hackstar1337](https://github.com/Hackstar1337) · [Elastic License 2.0](LICENSE)

> **Release candidate.** This repository contains the full modified application source, not a patch-only kit. It is not an official Kortix release or a production certification. Validate your own deployment before production use.

## Included

The repository contains the frontend, API, SDK, CLI, sandbox agent, LLM gateway, database migrations and complete source-owned Supabase bootstrap. Docker Cloud joins the existing provider implementations. Setup defaults to Docker Cloud and can retain Platinum as another selectable provider.

The Docker integration includes managed runtime-image builds, session creation, authorized lifetime renewal, stop/restart, persistent `/workspace` storage, protected HTTP/WebSocket ingress and deployment ownership checks. It also includes the tested compressed-response and forwarded-host fixes. Fresh setup uses the validated **2 CPU / 4 GiB** image baseline.

**GitHub hosts source and runs checks only. Production deployments use SSH on your VPS.** No workflow deploys to a server or modifies your existing installation.

## Requirements

Use Linux amd64 with Docker Engine and Compose, or Ubuntu WSL2 on Windows with a working Linux Docker engine for development. Python 3.10+ is required. Node, Bun and build dependencies run inside containers.

You need Docker Cloud Sandboxes access, a Docker ID and a Cloud-enabled PAT, stable public HTTPS API and application hostnames, and a model-provider connection such as OpenRouter. Compute, storage and model-provider charges are separate. Other architectures and native Windows/macOS deployments are not verified. See [compatibility](.agents/skills/self-host-docker-cloud/references/compatibility.md).

## Setup

### 1. Get the source

```bash
git clone https://github.com/Hackstar1337/KortixV2.0-public.git
cd KortixV2.0-public
```

For production, run the commands inside your **SSH session on the VPS**. For Windows development, use Ubuntu WSL2.

### 2. Save private credentials

```bash
mkdir -p "$HOME/.config/kortix-v2-private"
chmod 700 "$HOME/.config/kortix-v2-private"
cp selfhost/.env.example "$HOME/.config/kortix-v2-private/docker-cloud.env"
chmod 600 "$HOME/.config/kortix-v2-private/docker-cloud.env"
```

Edit that private file and set `DOCKER_CLOUD_USERNAME` and `DOCKER_CLOUD_PAT`. Do not commit it, upload it, or pass the PAT on a command line.

### 3. Configure the instance

Replace these example hostnames and operator address with your own values:

```bash
python3 selfhost/manage.py init \
  --instance-dir "$HOME/kortix-v2-instance" \
  --project-name kortix-v2 \
  --mode production \
  --api-url https://api.example.com \
  --frontend-url https://app.example.com \
  --admin-email operator@example.com \
  --providers docker-cloud,platinum \
  --docker-cloud-credentials "$HOME/.config/kortix-v2-private/docker-cloud.env"
```

The first provider is the default. Use `--provider docker-cloud` for Docker-only operation. Keeping Platinum selectable does **not** supply its credentials or enable automatic failover.

`init` creates a private directory, signed Supabase auth tokens, encryption keys, complete Compose configuration and backend-only Docker credentials. It refuses an existing unmanaged instance. It does not start containers or delete data. Configure an operator address to authorize organization creation.

The API URL must be an **origin**, not `/v1`, `/v1/health`, or another route. Production rejects localhost, private IPs and temporary `trycloudflare.com` hostnames.

### 4. Configure stable HTTPS ingress

Use your VPS reverse proxy or a named Cloudflare Tunnel. Route the application hostname to the loopback frontend port and the API hostname to the loopback API port. The frontend proxies `/supabase/*` to Supabase and `/v1/*` to the API.

For a named tunnel, save its token in a private file and add `--named-tunnel-token-file /path/to/private/token.txt` to `init`. The manager mounts the token read-only, passes only its file path, and uses HTTP/2. Configure named-tunnel application routes to `http://frontend:3000` and `http://kortix-api:8008` on the Compose network.

Do not put an interactive login challenge in front of the agent-facing API. Keep application authentication and signed requests enabled. See the [stable hostname guide](.agents/skills/self-host-docker-cloud/references/stable-hostname.md).

### 5. Build and start

```bash
bash selfhost/build.sh all
python3 selfhost/manage.py doctor --instance-dir "$HOME/kortix-v2-instance" --check-docker

# Review only; no containers start.
python3 selfhost/manage.py start --instance-dir "$HOME/kortix-v2-instance"

# Apply the reviewed plan.
python3 selfhost/manage.py start --instance-dir "$HOME/kortix-v2-instance" --apply
python3 selfhost/manage.py status --instance-dir "$HOME/kortix-v2-instance"
```

The build creates `kortix-v2-api:local`, `kortix-v2-frontend:local` and `kortix-v2-gateway:local` from this source. API builds compile the sandbox agent, source-attested CLI and guest ingress executable. Frontend builds do not need a host-generated `.next` directory. Source builds download dependencies and need adequate memory and disk space.

The stock updater is disabled. Review upgrades and deploy them yourself over SSH. `stop` is also plan-first and requires `--apply`; it does not remove volumes.

### 6. Connect a model and test

Register the configured operator address using password signup. Default self-host auth does not need SMTP for first signup. Configure SMTP and registration policy before inviting other users.

Add your model-provider connection. **Saving an OpenRouter key alone does not necessarily select it for a conversation.** Select the connection in the conversation's **Provider keys** control and choose a model served by that provider.

Use a new conversation to verify a reply, terminal access, workspace files, previews and stop/restart continuity. The first runtime image build is slower than subsequent conversations using the cached image. API health alone does not prove model inference or sandbox readiness.

## Checks and operations

```bash
python3 selfhost/verify_source.py
python3 -m unittest discover -s selfhost/tests -v
bash selfhost/test-contract.sh
```

Provider tests run in a container without external network access. CI never receives production or Docker Cloud credentials and never creates paid cloud resources. `selfhost/source-manifest.json` records source provenance and integration hashes.

- [Installation](.agents/skills/self-host-docker-cloud/references/installation.md)
- [Stable hostname](.agents/skills/self-host-docker-cloud/references/stable-hostname.md)
- [SSH VPS operations](.agents/skills/self-host-docker-cloud/references/ssh-vps.md)
- [Backup and restore](.agents/skills/self-host-docker-cloud/references/backup-restore.md)
- [Troubleshooting](.agents/skills/self-host-docker-cloud/references/troubleshooting.md)
- [Compatibility](.agents/skills/self-host-docker-cloud/references/compatibility.md)
- [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md) · [Changes](CHANGELOG.md)

Volume retention is **not a backup**. Back up database, object-store, configuration and cloud-workspace data separately. Test restore procedures. Do not delete retained volumes to resolve an ambiguous create operation.

## Security and licensing

The guest ingress listener shares the sandbox with the workload. **Guest root can read its derived ingress key or replace the listener.** This is not an independently trusted ingress boundary for hostile multi-tenant workloads. Docker account management credentials remain backend-only.

Kortix is **source-available under Elastic License 2.0**, not an unrestricted hosted-SaaS grant. Preserve notices and license functionality. The separate [white-label terms](WHITE-LABEL-LICENSE.md) require Platinum as the exclusive compute provider for those permissions. Docker Cloud support does not grant white-label, trademark, or hosted resale rights.

See [FORK-NOTICE.md](FORK-NOTICE.md) for provenance. Fresh stable-hostname end-to-end deployment, capacity, adversarial isolation and disaster recovery require environment-specific acceptance testing. This candidate makes no universal Platinum-parity or availability promise.
