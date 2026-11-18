# Spawned workers and drive access

## Symptom

The parent My Kortix conversation works, but a spawned worker fails with:

> This project's sessions mount drives, and drives run on Platinum only.

Regular worker sessions use the drive-aware provisioning path; the My Kortix parent has a different path. Without the operator's cross-provider sync switch, a regular Docker worker refuses to start rather than silently lose its files.

## Supported configuration

Set this on the **Kortix API**:

```dotenv
KORTIX_DRIVES_SYNC=on
```

The provider-neutral daemon then copies authorized drive folders into `/drives` and synchronizes through authenticated Kortix API endpoints. Recorded folder grants and read-only permissions still apply. The guest does not receive a Platinum storage credential.

**Compute is on Docker Cloud, but these drives still use Platinum-backed storage.** This setting does not migrate drive data to Docker volumes, grant Platinum entitlements or make all drive-backed workflows Platinum-independent. Storage access must remain configured and reachable. Sync is not identical to a native shared filesystem mount, and concurrent writes across replicas or other writers still require conflict handling.

Persistent Docker `/workspace` storage is separate from these shared drives. Do not turn off drive mounting merely to hide a startup error, and do not remove drive volumes to fix it.

## Fresh installation

The portable manager enables this setting by default when `docker-cloud` is selected. An explicit existing value, including `off`, is preserved during reinitialization.

## Existing installation

Back up private configuration and review it on the target computer over SSH. Add `KORTIX_DRIVES_SYNC=on` to the API's environment in the existing deployment overlay, or to its private instance `.env` if the API consumes that file and no overlay overrides the setting.

Do not start a second Compose project accidentally. Use the existing instance and its actual project name. For a manager-created instance:

```bash
python3 selfhost/manage.py doctor --instance-dir /path/to/existing-instance --check-docker
python3 selfhost/manage.py start --instance-dir /path/to/existing-instance
# After review; recreates affected services when their environment changed:
python3 selfhost/manage.py start --instance-dir /path/to/existing-instance --apply
```

Check API health and the effective setting, then click Retry on the failed child or create a fresh worker. Reinitialization and an API restart do not themselves replay a failed research task. If startup next reports unreachable file storage, diagnose the Platinum storage path instead of assuming sync solved all prerequisites.

## Evidence boundary

Installer tests cover the default and explicit opt-out preservation. Drive-sync unit tests cover folder permissions, read-only grants and conditional-write locking. These do not prove the failed child completed its task; a retried worker and file-continuity check are still required.
