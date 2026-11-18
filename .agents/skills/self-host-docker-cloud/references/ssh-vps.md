# Production deployment over SSH to a VPS

Production deployments are operator-controlled SSH deployments to a Linux amd64 VPS. GitHub runs source checks only; there is no automatic GitHub or Vercel deployment.

## Host posture

Patch the host, use SSH keys and a dedicated operator account, restrict SSH to approved administration networks, and keep application/database ports bound to loopback. Docker socket access is host-root-equivalent. Keep credentials and backups outside the source tree.

Use separate paths for source and instance data. A synthetic example:

```bash
ssh ops@vps.example.com
mkdir -p "$HOME/src"
cd "$HOME/src"
git clone https://github.com/Hackstar1337/KortixV2.0-public.git
cd KortixV2.0-public
```

Review the source commit and licenses. Save private Docker credentials on the VPS, not in the checkout. Follow [installation](installation.md) to initialize an instance with your real API and application origins, operator email and private credential-file path.

## Build and deploy

Run inside the SSH session:

```bash
bash selfhost/build.sh all
python3 selfhost/manage.py doctor --instance-dir "$HOME/kortix-v2-instance" --check-docker
python3 selfhost/manage.py plan --instance-dir "$HOME/kortix-v2-instance"
# Apply only the reviewed plan:
python3 selfhost/manage.py start --instance-dir "$HOME/kortix-v2-instance" --apply
python3 selfhost/manage.py status --instance-dir "$HOME/kortix-v2-instance"
```

Provider, mode and public-origin flags belong to **init**, not plan/start. `--apply` is the explicit service-change boundary. The manager does not remove volumes, deploy through a connector, or silently update images from upstream. Capture the source revision and image IDs in a private release record.

Configure stable DNS and your reverse proxy or named tunnel before rollout; verify public health **after** services start. See [stable hostname](stable-hostname.md). Do not require an interactive browser challenge on the agent callback path.

## Post-deploy checks

Verify local service state, independent-network API/frontend reachability, rejection of unauthorized ingress, a new authorized conversation, model inference, workspace/preview behavior, authorized renewal and stop/restart continuity. Validate backups and restore credentials. A health response alone does not certify production readiness.

## Upgrades and rollback

Before upgrade, record current image IDs and instance configuration and take database, object-store and cloud-workspace backups. Review source changes and migrations. Build the new revision separately, then apply it over SSH during your change window.

The manager does not implement transactional rollback. To roll back application images, restore the recorded `API_IMAGE`, `FRONTEND_IMAGE` and `GATEWAY_IMAGE` values in the private instance `.env`, review the plan, and start with `--apply`. Database migrations may not be reversible; reconcile schema compatibility before restoring older code. Do not overwrite persisted encryption keys or delete `/workspace` as a rollback shortcut.

```bash
python3 selfhost/manage.py stop --instance-dir "$HOME/kortix-v2-instance"
python3 selfhost/manage.py stop --instance-dir "$HOME/kortix-v2-instance" --apply
```

Preserve private diagnostics and reconcile ambiguous remote resources before retrying. Fresh stable-hostname end-to-end and disaster recovery remain deployment-specific acceptance requirements.
