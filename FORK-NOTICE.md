# Source provenance and modification notice

**Distribution:** Kortix V2.0 Public  
**Maintainer:** Ashwin D / Hackstar1337  
**Repository:** https://github.com/Hackstar1337/KortixV2.0-public

This is an independently maintained source snapshot based on [kortix-ai/CompanyOS](https://github.com/kortix-ai/CompanyOS), revision `1f58c106d02140c4b050c539904d9410b438ab5f`. It is not an official Kortix release, and its repository name does not change the underlying upstream application version.

Upstream copyright notices and the Elastic License 2.0 remain in force. The original licensing files and a copy of the upstream README are retained. These changes do not grant hosted-service, white-label or trademark rights beyond the applicable licenses. The upstream white-label permission requires Platinum as the exclusive compute provider.

## Modification scope

- Docker Cloud provider, managed image builder, SDK client and resource ownership checks.
- Persistent workspace attachment, bounded lifecycle operations and authorized renewal through the existing session reaper.
- Protected guest ingress, compressed-response transport and Docker-specific forwarded-host compatibility.
- Provider registration, additive database enum migration, API/SDK types and source build integration.
- Portable private configuration, valid Supabase token generation, complete bootstrap Compose graph, 2 CPU / 4 GiB Docker baseline and plan-first service management.
- Named-tunnel token-file handling, stable callback validation, disabled stock auto-updater and full-source frontend builds.
- Credential-free regression tests, source manifest, CI and operator documentation.

Operational environment files, local credentials, customer databases, captured traffic, private validation logs, and upstream deployment workflows are not distributed. No existing running installation is deployed or migrated by creating this repository.

See `selfhost/source-manifest.json` for the integration payload hashes. The provider contract tests are not a claim of full Platinum feature parity, hostile-guest security, capacity, availability or disaster-recovery certification.
