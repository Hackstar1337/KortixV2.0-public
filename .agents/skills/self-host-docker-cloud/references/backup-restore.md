# Backup and restore

Treat `/workspace` as persistent application data, separate from ephemeral sandbox compute. The provider integration is designed to retain that volume across sandbox stop, replacement, and deletion when the volume remains owned by the instance. Retention is not a substitute for backups.

## What to back up

Create an operator-owned, encrypted backup set containing:

- The contents of `/workspace`, using an application-consistent snapshot or a quiesced copy.
- The instance configuration and compose/manifests required to recreate the service.
- The approved source revision, image digest, provider, and mode.
- The backup policy metadata needed to identify the instance and restore point.

Do **not** include Docker Cloud PATs, Cloudflare tunnel tokens, TLS private keys, backend signing keys, customer credentials, or raw private logs in a public repository or an unencrypted archive. Store secrets separately in the approved secret manager and rotate them if an archive may have exposed them.

## Before a backup

1. Announce or schedule a brief write quiescence for workloads that require consistency.
2. Confirm `status` and identify the exact instance and workspace volume privately.
3. Confirm the destination has enough capacity and encryption.
4. Run `doctor` and record blocking findings.
5. Create a timestamped backup outside the source checkout.
6. Verify the archive can be listed without printing secrets.

Use synthetic names in runbooks. The actual volume name and instance path are deployment-specific and must not be copied into public documentation.

## Example copy pattern

The exact backup tooling is an operator choice. A Docker-based pattern can mount the persistent volume read-only into a temporary utility container and write to a host-mounted encrypted destination:

```bash
# Synthetic placeholders only; replace with the approved volume and destination.
docker run --rm \
  -v kortix_workspace_example:/workspace:ro \
  -v /srv/kortix-backups:/backup \
  alpine:latest \
  sh -c 'tar -czf /backup/workspace-example.tar.gz -C /workspace .'
```

Do not run this while the workload is writing unless the resulting consistency model is acceptable. Prefer storage-native snapshots or application-level exports for databases and files that require transactional consistency.

## Restore procedure

1. Stop the affected instance or quiesce writes.
2. Confirm the restore point, source revision, image digest, and target instance.
3. Restore into a new or explicitly authorized workspace volume first; preserve the original volume until validation succeeds.
4. Verify ownership, permissions, expected directory structure, and available capacity.
5. Run `doctor`, then `plan`, and review the proposed start.
6. Start with explicit `--apply` only after the plan is approved.
7. Verify health, authenticated ingress, a representative read/write operation, and the expected workspace contents.
8. Keep the original volume for the agreed retention window before decommissioning it.

A synthetic extraction shape is:

```bash
docker run --rm \
  -v kortix_workspace_restore_example:/workspace \
  -v /srv/kortix-backups:/backup \
  alpine:latest \
  sh -c 'tar -xzf /backup/workspace-example.tar.gz -C /workspace'
```

Use the backup system's integrity and encryption verification rather than assuming a successful `tar` exit proves an application-consistent restore.

## Retained volumes and ambiguous failures

A failed create or network timeout may have succeeded at the provider. The integration may retain the independent workspace rather than deleting user bytes. Inventory retained storage by deployment and logical ownership, check attachment state, and obtain deletion authorization before removing it. A missing application row does not authorize volume deletion.

## Restore acceptance

The current release evidence includes earlier lifecycle, volume-continuity, and HTTP smoke checks. It does not certify every backup driver, database consistency model, or operator storage target. Record a private restore test for the exact workload before relying on the procedure in an incident.
