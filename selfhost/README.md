# Portable self-host tooling

Start with the [repository setup guide](../README.md) and [installation reference](../.agents/skills/self-host-docker-cloud/references/installation.md).

`manage.py` is a Python 3.10+ standard-library tool for an operator-managed Linux Compose installation. Use SSH on a VPS for production and Ubuntu WSL2 for Windows development. It does not deploy through GitHub or automatically upgrade from the upstream registry.

## Commands

| Command | Behavior |
| --- | --- |
| `init` | Create private configuration, compatible auth tokens and a complete Compose instance. Does not start containers. |
| `doctor` | Validate configuration and safety gates. `--check-docker` checks the complete Compose graph. |
| `plan` | Print the intended start plan. |
| `start` | Print a plan; `--apply` starts/reconciles services. |
| `stop` | Print a plan; `--apply` stops services without removing volumes. |
| `status` | Show the local Compose service state. |

Configure provider, public origins and credential file paths through **init**. `--api-url` aliases `--callback-url`; `--provider` aliases `--providers`. API URLs must be origins without route suffixes. Source-built image tags match `build.sh`.

The default provider order is `docker-cloud,platinum`. This retains another selectable provider, not automatic failover. Platinum still needs its own credentials and license entitlements. Docker Cloud image defaults are 2 CPU / 4 GiB.

## Private files

The instance directory is owner-only on Linux. The manager creates real random encryption secrets and signed Supabase auth tokens; it does not rotate existing managed secrets during reinitialization. It refuses fresh initialization over an unmanaged existing `.env`.

Docker Cloud credentials are read from a private input file containing `DOCKER_CLOUD_USERNAME` and `DOCKER_CLOUD_PAT`. The API-only `.docker-cloud.env` is materialized during initialization when the input flag is supplied, and refreshed on apply. Docker credentials must not appear in shared `.env`, frontend configuration or guest workloads.

Named-tunnel tokens are mounted read-only by file path, never printed or placed as token-valued command arguments. The connector uses HTTP/2. Production without a named tunnel requires your own stable reverse proxy and excludes the temporary tunnel service. The stock updater is disabled.

## Build and checks

```bash
bash selfhost/build.sh all
python3 selfhost/verify_source.py
python3 -m unittest discover -s selfhost/tests -v
bash selfhost/test-contract.sh
```

The build compiles application artifacts from source. Provider tests cannot contact cloud services. The manager retains the pinned source-owned Supabase assets and `kortix-migrate` bootstrap.

Compose validation is not a Docker Cloud access check, health wait or transactional rollback. Confirm running service health, public DNS/TLS, model connection selection, fresh inference, persistence and restore before production acceptance. No local command proves all remote cloud resources have stopped; verify provider state during maintenance.
