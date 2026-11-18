# Compatibility and verification matrix

Compatibility here means behavior enforced or observed for this release candidate. It does not mean full upstream or Platinum parity.

## Platform matrix

| Platform or component | Status | Notes |
| --- | --- | --- |
| Linux amd64 VPS | Supported target | Required for production deployment over SSH, subject to host and workload acceptance testing. |
| Windows with WSL2 and Docker Desktop | Development supported | Use for local development and checks; not a production certification. Follow Docker's WSL2 requirements. |
| Native Windows without WSL2 | Not verified | No production claim. |
| macOS | Not verified | No production claim. |
| ARM-only hosts | Not verified | The documented production image path targets Linux amd64. |
| Other operating systems and architectures | Not verified | Validate privately before relying on them. |

## Capability matrix

| Capability | Status | Evidence or boundary |
| --- | --- | --- |
| `selfhost/manage.py init` | Contracted | Initializes the selected instance directory. |
| `doctor` | Contracted | Performs preflight checks; a pass is not a production certification. |
| `plan` | Contracted | Prints the intended change without applying it. |
| `start --apply` | Contracted | Explicit apply boundary for an approved plan. |
| `stop` and `status` | Contracted | Operator lifecycle and state inspection commands. |
| Docker Cloud provider selection | Supported with constraints | Use `--provider docker-cloud`; credentials stay backend-only. |
| Production mode | Supported target | Use `--mode production` only with a stable HTTPS origin and SSH VPS. |
| Persistent `/workspace` | Supported design | Treat as user data; retain and back it up independently of sandbox compute. |
| 60-minute lifetime | Supported default | Renewal is for authorized active work and must not wake stopped sandboxes. |
| Cold image builds | Supported with operational caveat | Builds and remote registration can take minutes. |
| HTTP/HTTPS ingress | Verified in earlier native smoke; stable public E2E not verified | Use authenticated ingress through a stable named HTTPS origin. |
| Gzip/host/ingress regressions | Verified | 12 regression tests passed. |
| Native lifecycle and volume smoke | Verified earlier | Stop/resume and persistent-volume continuity were exercised earlier. |
| Custom-provider Hello inference | Verified once | A real configured custom-provider Hello inference completed. |
| Public API health | Partially verified | Replacement public API health passed after the temporary tunnel failure. |
| Fresh stable-hostname inference | Not verified | A DNS-dead temporary tunnel prevented later inference; old sessions were rejected as `staleDevTunnelBox`. |
| Named Cloudflare Tunnel | Supported deployment pattern | Follow current Cloudflare prerequisites and use a named tunnel, not a Quick Tunnel. |
| VPS reverse proxy | Supported deployment pattern | Operator-owned TLS and forwarding; test host and WebSocket behavior. |
| GitHub automatic production deployment | Not provided | Production deployment is SSH VPS only. |
| Vercel automatic production deployment | Not provided | Vercel is not the production deployment path for this integration. |
| Quick Tunnels | Development only | Temporary URLs are not stable callback origins. |
| Interactive Cloudflare Access callback challenge | Unsupported for agents | Unattended callbacks cannot complete an interactive challenge. |
| Full Platinum parity | Not claimed | Docker integration does not reproduce every Platinum capability. |
| Hostile-guest or multi-tenant isolation | Not supported by this candidate | Guest root can read the derived ingress key or replace the listener. |
| Hosted SaaS resale or white-label rights | Not granted | Upstream white-label terms require Platinum as the exclusive compute provider. |

## Official host references

- Docker Engine on Ubuntu: <https://docs.docker.com/engine/install/ubuntu/>
- Docker Desktop WSL2 backend: <https://docs.docker.com/desktop/features/wsl/>
- Cloudflare Tunnel getting started: <https://developers.cloudflare.com/tunnel/get-started/>

## Acceptance guidance

Before relying on a capability, test the exact source revision, image digest, host, callback origin, model provider, workload, traffic profile, and backup target that the operator will use. Keep private records of the test and distinguish **Verified**, **Rejected**, **Constrained**, and **Not verified** outcomes.

The evidence in this document is release-candidate evidence, not a service-level guarantee. Preserve the upstream Elastic License 2.0 and white-label terms with the source; Docker integration does not alter those legal boundaries.
