# Installation and first start

Use a Linux amd64 VPS over SSH for production. Ubuntu WSL2 is the local Windows development path. Python 3.10+, Docker Engine, Docker Compose, Git, adequate disk space and outbound HTTPS are required.

## Prerequisites

Follow [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) or [Docker Desktop WSL2](https://docs.docker.com/desktop/features/wsl/). Then check:

```bash
uname -m
python3 --version
docker version
docker compose version
docker run --rm hello-world
```

Docker socket access is effectively host-root access. Use an operator account and a dedicated machine. Internal stack ports stay bound to loopback; expose only an operator-managed TLS reverse proxy or named tunnel.

## Source and private configuration

```bash
git clone https://github.com/Hackstar1337/KortixV2.0-public.git
cd KortixV2.0-public
mkdir -p "$HOME/.config/kortix-v2-private"
chmod 700 "$HOME/.config/kortix-v2-private"
cp selfhost/.env.example "$HOME/.config/kortix-v2-private/docker-cloud.env"
chmod 600 "$HOME/.config/kortix-v2-private/docker-cloud.env"
```

Edit the credential file privately. Supply a Docker ID and a Cloud Sandboxes-enabled PAT. Never put production credentials in the checkout.

```bash
python3 selfhost/manage.py init \
  --instance-dir "$HOME/kortix-v2-instance" \
  --project-name kortix-v2 \
  --mode production \
  --api-url https://api.example.com \
  --frontend-url https://app.example.com \
  --admin-email operator@example.com \
  --provider docker-cloud \
  --docker-cloud-credentials "$HOME/.config/kortix-v2-private/docker-cloud.env"
```

Replace hostnames and email. API and frontend values are origins, without route suffixes. Configure stable HTTPS ingress using the [hostname guide](stable-hostname.md). For the bundled named-tunnel connector, include `--named-tunnel-token-file /path/to/private/token.txt` in `init`.

The manager creates the complete Supabase and Kortix configuration and compatible signed auth tokens. It refuses fresh initialization over an unmanaged existing `.env` and retains existing managed secrets on reinitialization. It does not initialize or migrate a running deployment through GitHub.

## Build, plan and apply

```bash
bash selfhost/build.sh all
python3 selfhost/manage.py doctor --instance-dir "$HOME/kortix-v2-instance" --check-docker
python3 selfhost/manage.py plan --instance-dir "$HOME/kortix-v2-instance"
python3 selfhost/manage.py start --instance-dir "$HOME/kortix-v2-instance"
# Only after reviewing the plan:
python3 selfhost/manage.py start --instance-dir "$HOME/kortix-v2-instance" --apply
python3 selfhost/manage.py status --instance-dir "$HOME/kortix-v2-instance"
```

The source build creates the API, frontend and gateway images. The API image contains the sandbox agent, compiled CLI, its source attestation and the ingress executable. Dependencies are downloaded during builds. First startup initializes Supabase and runs the source-owned Kortix migration bootstrap. Cold cloud runtime-image builds can take longer than application startup.

`doctor --check-docker` validates the complete Compose graph. It is not a remote Docker Cloud credential test, DNS validation or inference test.

## Acceptance

After services start, check from an independent network:

```bash
curl --fail --silent --show-error https://api.example.com/v1/health
curl --fail --silent --show-error -I https://app.example.com/
```

Register the operator email with password signup, then configure a model-provider connection. Select that connection in the conversation's Provider keys control. Test a new conversation, a workspace file, terminal execution, preview access, lifetime renewal and stop/restart continuity. Add SMTP and an appropriate registration policy before inviting others.

API health alone does not prove sandbox or model readiness. Do not call the deployment accepted until these workload and restore checks pass.

## Stop

```bash
python3 selfhost/manage.py stop --instance-dir "$HOME/kortix-v2-instance"
# The preceding command is a plan; this one stops services:
python3 selfhost/manage.py stop --instance-dir "$HOME/kortix-v2-instance" --apply
```

Stopping the local stack does not itself prove every remote cloud resource is stopped. Check remote state before maintenance; never remove persistent volumes to resolve an uncertain provider operation. See [backup and restore](backup-restore.md).
