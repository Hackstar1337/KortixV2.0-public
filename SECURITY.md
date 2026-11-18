# Security policy

**Repository:** `Hackstar1337/KortixV2.0-public`  
**Maintainer:** Ashwin D.

## Scope and release position

This policy covers the self-host deployment path, the Docker Cloud provider integration, authenticated ingress, lifecycle handling, persistent workspace operations, build guidance, and public operator documentation. The current code and evidence are a **release candidate, not a production certification**. This policy does not certify Docker Cloud, Cloudflare, an operator's VPS, an end-user workload, or any compliance program.

Report suspected vulnerabilities privately through the repository's GitHub Security reporting channel when available. Do not put credentials, customer data, private hostnames, session identifiers, raw logs, or exploit details in a public issue or pull request. If private reporting is unavailable, open a minimal issue requesting a private channel without sensitive details.

Include the affected commit or release label, impact, reproduction steps using synthetic data, and a proposed mitigation. Test only systems you own or are explicitly authorized to assess. Stop if testing exposes another user's data. Keep details private until the maintainer and reporter agree on disclosure timing.

## Trust boundaries

The deployment has these boundaries:

- The **backend control plane** holds Docker Cloud management credentials and is the only component allowed to use them.
- Docker Cloud is the provider boundary for sandbox compute, images, ingress exposure, and volumes.
- The **guest workload** must not receive Docker Cloud credentials or backend signing secrets.
- The public route must terminate at a stable HTTPS tunnel or reverse proxy and then reach the authenticated ingress path.
- `/workspace` is persistent user data. It intentionally survives sandbox replacement or deletion when the provider supports retained volumes.
- The ingress listener and workload share the guest. Guest root can read the derived ingress key or replace the listener.

The guest-root limitation means this release is for trusted workloads. It is not a hostile-guest or multi-tenant isolation guarantee. A readiness response from a listener inside the guest is not attestation against a malicious local process.

## Credential handling

Treat the Docker Cloud personal access token as a backend-only secret:

- Store it in a private backend environment or secret manager with least privilege and restrictive permissions.
- Never commit it, place it in `selfhost/`, bake it into an image, include it in a staged build context, inject it into a guest, or pass it to browser code.
- Never place secrets in shell history, screenshots, issue text, test fixtures, public CI artifacts, or copied logs.
- Sanitize provider errors and diagnostics so that tokens, signed URLs, authorization headers, and private endpoints do not appear.
- Rotate credentials after accidental exposure and preserve only the minimum incident evidence needed for investigation.

Stable hostname credentials and tunnel tokens are also secrets. A named tunnel token should be installed on the VPS through a private channel and should not be pasted into this repository.

## Ingress and callback requirements

The public application origin must be HTTPS. The ingress layer must preserve the application's required host and upgrade behavior while removing unsafe hop-by-hop or routing headers as appropriate. Reject unauthenticated ingress and do not publish a raw application port that bypasses authentication.

Callbacks must use a stable named hostname. Do not put an agent callback behind an interactive Cloudflare Access challenge; an unattended agent cannot complete a browser challenge. Quick Tunnels are temporary development conveniences and are not a stable production callback mechanism.

## Lifecycle and data safety

The default lifetime is 60 minutes. Renewal is allowed only for authorized active work and must not wake stopped sandboxes. Stop, start, and deletion operations can be ambiguous during provider or network failures; reconcile provider state before retrying a create, delete, or restore.

A failed or ambiguous operation may leave an independent workspace volume. Operators must inventory retained storage, verify deployment and logical ownership, and obtain deletion authorization before removing it. A missing application row is not authorization to delete provider data.

Backups must cover `/workspace` and the deployment configuration required to recreate the service. Do not back up Docker Cloud credentials into the same public or broadly accessible archive.

## Contributor security rules

Contributors must use synthetic data and placeholder hostnames. Do not add customer exports, private runbooks, credentials, host-specific paths, or screenshots. Security-sensitive changes require tests for both success and rejection paths, including invalid credentials, ingress bypass, ownership mismatch, unsafe target ports, and cleanup behavior where relevant.

Preserve the upstream Elastic License 2.0, copyright notices, license-key functionality, and modification notices. The upstream white-label terms require Platinum as the exclusive compute provider; Docker integration does not grant hosted SaaS resale or white-label rights.
