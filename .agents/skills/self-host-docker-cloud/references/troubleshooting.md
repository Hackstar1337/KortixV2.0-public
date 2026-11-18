# Troubleshooting

Use this guide with synthetic examples only. Preserve private diagnostics for operators, but do not publish credentials, signed URLs, customer data, hostnames, or session identifiers.

## First response

1. Run `python3 selfhost/manage.py status --instance-dir <INSTANCE_DIR>`.
2. Run `doctor` without changing the instance.
3. Check Docker and Compose availability on the host.
4. Verify the stable public hostname from an independent network.
5. Confirm whether the affected session is fresh or points at an old temporary tunnel.
6. Avoid blind retries for ambiguous create, delete, or restore operations.

## Symptom table

| Symptom | Likely cause | Safe next step |
| --- | --- | --- |
| `manage.py` is not found | Wrong checkout or working directory. | Run from the repository root and verify `selfhost/manage.py` exists. |
| `doctor` reports Docker unavailable | Docker daemon stopped, permissions, or wrong context. | Check `docker version`, `docker compose version`, and the daemon status; fix host access before applying. |
| Plan rejects provider or mode | CLI contract or configuration mismatch. | Use `--provider docker-cloud` and `--mode production` explicitly; inspect `--help` rather than guessing flags. |
| Start refuses without apply | Expected change boundary. | Review the plan and add `--apply` only to an approved `start` command. |
| API health is local but public callback fails | Missing stable route, wrong DNS, or edge forwarding error. | Verify the named tunnel/reverse proxy, HTTPS certificate, host forwarding, and public route from outside the VPS. |
| Public request returns an interactive 403/Access page | Cloudflare Access challenge on an unattended callback. | Remove the interactive challenge from that callback path or use a tested non-interactive control. |
| Old session returns `staleDevTunnelBox` | Session still references a dead temporary tunnel. | Stop using the old session and create a fresh session after the stable hostname is healthy. |
| Temporary tunnel DNS is dead | Quick Tunnel or temporary edge lifecycle ended. | Treat it as development-only; do not promote it. Configure a named tunnel or VPS reverse proxy. |
| API health passes but inference fails | Stale session, callback mismatch, model route, or provider-side issue. | Test a fresh session, verify callback origin, inspect private backend diagnostics, and record model-provider status separately. |
| Image build appears idle | Cold build or remote image registration can take minutes. | Wait through the expected cold-build window; inspect private build status before retrying. |
| Image build fails | Missing Docker access, unsupported architecture, or source/build issue. | Confirm Linux amd64 target, disk space, Docker permissions, and the source revision; preserve the failure privately. |
| Sandbox expires unexpectedly | 60-minute default reached or renewal was not authorized. | Check active-work authorization and lifecycle status; do not assume renewal should wake a stopped sandbox. |
| `/workspace` data is missing | Wrong volume, restore target, or ownership mismatch. | Stop writes, verify the instance/logical volume mapping, inspect backups, and do not delete retained volumes. |
| Ingress returns 401 | Missing or invalid ingress authorization. | Verify the authorized client path and secret injection without printing the token. |
| Ingress returns 400 | Invalid target port or malformed routing request. | Use only the provider-supported target route; do not publish a raw application port. |
| Ingress returns 502 | Listener or application target unavailable. | Check the guest service, expected port, proxy health, and provider state; preserve private logs. |
| SSH works but browser access fails | Edge or DNS configuration, not necessarily the app. | Test local health, then VPS edge, then public hostname in order. |

## Evidence boundary

The release candidate has a completed real configured custom-provider Hello inference, earlier native lifecycle/volume/HTTP smoke, 12 passed gzip/host/ingress regression tests, and a replacement public API health pass. A later DNS-dead temporary tunnel prevented inference and stale sessions were rejected by `staleDevTunnelBox`; a fresh stable-hostname end-to-end deployment remains not verified.

Do not turn any one health response or regression suite into a claim of full Platinum parity, universal model support, hostile-guest isolation, load capacity, or certified production readiness.

## Escalation package

For a private maintainer report, include:

- Release or commit and the exact manager subcommand.
- Synthetic reproduction steps and expected versus actual behavior.
- Host architecture and Docker/Compose versions.
- Stable edge type (named tunnel or reverse proxy), without the real hostname or token.
- Timestamp in the operator's private channel and a sanitized status/doctor excerpt.
- Whether the failure concerns lifecycle, ingress, callback, inference, image build, or backup/restore.

Redact credentials, customer data, raw provider responses, signed URLs, and private infrastructure identifiers before sharing.
