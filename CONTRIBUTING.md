# Contributing

Thank you for contributing to `Hackstar1337/KortixV2.0-public`, maintained by Ashwin D. This is a public full-source repository with a self-host operator path. Contributions should make the source, deployment, or documentation more reproducible without overstating the current evidence.

## Before opening a change

1. Read `README.md`, `SECURITY.md`, and the operator references under `.agents/skills/self-host-docker-cloud/references/`.
2. Understand the supported deployment model: production is an operator-controlled SSH VPS deployment; GitHub and Vercel are not automatic production deployment targets.
3. Preserve the CLI contract:
   - `python3 selfhost/manage.py init`
   - `python3 selfhost/manage.py doctor`
   - `python3 selfhost/manage.py plan`
   - `python3 selfhost/manage.py start --apply`
   - `python3 selfhost/manage.py stop`
   - `python3 selfhost/manage.py status`
   - supported options include `--instance-dir`, `--api-url`, `--frontend-url`, `--provider docker-cloud`, and `--mode production`.
4. Use the parent-owned `selfhost/build.sh` entry point for source builds. Do not invent a second public build path in documentation.
5. Use synthetic data and `example.invalid` hostnames. Remove customer data, secrets, private logs, real hostnames, session IDs, and screenshots before committing.

## Changes we welcome

- Clear operator documentation with exact prerequisites, rollback boundaries, and evidence labels.
- Provider and ingress hardening that keeps Docker Cloud credentials backend-only.
- Tests for lifecycle idempotency, `/workspace` retention, authenticated ingress, safe header handling, ownership checks, and cleanup.
- Compatibility improvements that are accompanied by a reproducible test and an honest status update.
- Build and deployment changes that preserve the stable HTTPS callback requirement and the SSH-VPS production boundary.

## Changes that need special care

Do not:

- Publish a raw application port that bypasses authenticated ingress.
- Put Docker Cloud management credentials into a guest workload, image, frontend bundle, or build context.
- Treat a Quick Tunnel as a production hostname or place callbacks behind an interactive Cloudflare Access challenge.
- Claim full Platinum parity, certification, hostile-guest isolation, guaranteed regions, or hosted SaaS rights without a separately reviewed legal and technical basis.
- Remove or bypass upstream Elastic License 2.0 license-key or notice functionality.
- Present Docker Cloud integration as permission to use the upstream white-label terms; those terms require Platinum as the exclusive compute provider.
- Add an automatic GitHub or Vercel deployment path for production without an explicit architecture and security review.

## Local verification

Run the repository's available checks from a clean checkout and record the exact commands and results in the pull request. At minimum, exercise the relevant `selfhost/manage.py` path in a disposable instance directory:

```bash
python3 selfhost/manage.py doctor --instance-dir ./tmp/kortix-instance
python3 selfhost/manage.py plan \
  --instance-dir ./tmp/kortix-instance \
  --provider docker-cloud \
  --mode production \
  --api-url https://api.example.invalid/v1/health \
  --frontend-url https://app.example.invalid/
```

A plan is not an apply. Do not run `start --apply` against a shared or production instance from a contribution branch without explicit operator authorization. If a change touches the build or runtime, use `selfhost/build.sh` and include the image architecture, digest, and test evidence privately where they cannot expose secrets.

The current release evidence includes 12 gzip/host/ingress regression tests, an earlier native lifecycle/volume/HTTP smoke, and one real configured custom-provider Hello inference. That evidence is not a blanket pass for every contribution. A replacement public API health check passed after a temporary tunnel became unusable, but a fresh stable-hostname end-to-end deployment remains unverified.

## Pull requests

A useful pull request includes:

1. The problem and the smallest coherent scope.
2. The files and interfaces changed.
3. Reproduction or verification commands with honest pass/fail/not-verified status.
4. Security, compatibility, backup, and licensing implications.
5. Any new operational prerequisite or rollback step.

Keep documentation claims specific. Prefer **Verified**, **Rejected**, **Constrained**, and **Not verified** labels. Never convert a test result into a service-level guarantee.

## Documentation changes

Use relative links that will remain valid after the parent integration places the operator references under `.agents/skills/self-host-docker-cloud/references/`. Do not link to private runbooks or files that are not part of the public repository. Keep examples synthetic and avoid committing generated credentials or instance state.

## License and notices

This repository modifies upstream Kortix source. Keep the upstream Elastic License 2.0, copyright and license notices, license-key functionality, white-label terms, and prominent modification notices with redistributed copies. Consult legal counsel before offering a hosted or managed service.
