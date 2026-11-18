# Changelog

All notable public changes to the Kortix V2.0 Public operator and contributor surface are recorded here. This changelog describes documentation and integration boundaries; it is not a production certification.

## Unreleased — spawned-worker drive compatibility

- Fresh Docker setups now default `KORTIX_DRIVES_SYNC=on`, allowing regular workers to use the existing authenticated cross-provider drive-sync path.
- Existing explicit settings, including `off`, are preserved. No drive data is migrated or deleted.
- Added installer regressions for the default and opt-out preservation, plus operator instructions for existing deployments.
- Docker compute does not replace Platinum-backed shared-drive storage. Storage access and an end-to-end retried worker remain required.

## [v2.0 public release candidate] — 2026-11-18

### Added

- Operator documentation for installation, stable HTTPS hostnames, SSH-VPS production deployment, backup and restore, troubleshooting, and compatibility.
- The `python3 selfhost/manage.py` operator contract for `init`, `doctor`, `plan`, `start`, `stop`, and `status`.
- Explicit `--instance-dir`, `--api-url`, `--frontend-url`, `--provider docker-cloud`, `--mode production`, and `start --apply` guidance.
- A source-build boundary at `selfhost/build.sh`.
- Backend-only Docker Cloud credential handling, persistent `/workspace` guidance, and 60-minute lifetime/authorized-renewal documentation.
- Stable-hostname guidance for named Cloudflare Tunnels and VPS reverse proxies.
- Licensing guidance preserving Elastic License 2.0 functionality and documenting that the upstream white-label permission requires Platinum as the exclusive compute provider.

### Evidence recorded

- A real configured custom-provider Hello inference completed.
- Native runtime lifecycle, persistent-volume continuity, and HTTP smoke were verified earlier.
- 12 gzip/host/ingress regression tests passed.
- A replacement public API health check passed after the temporary tunnel became unusable.

### Known limitations

- This is a release candidate, not certified production.
- A later DNS-dead temporary tunnel prevented inference, and `staleDevTunnelBox` rejected old sessions. A fresh stable-hostname end-to-end deployment has not yet been verified.
- No claim is made for full Platinum parity, certification, equal latency, guaranteed regions, adversarial or hostile-guest isolation, load/soak capacity, or universal model-provider support.
- Quick Tunnels are development-only; production callbacks require a stable named HTTPS origin.
- Production deployment is SSH VPS only. GitHub and Vercel do not provide automatic production deployment for this path.

[Unreleased]: https://github.com/Hackstar1337/KortixV2.0-public/compare/v2.0...HEAD
