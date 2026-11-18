# Stable HTTPS hostname and callbacks

Production needs stable, publicly reachable HTTPS origins. Temporary Quick Tunnel hostnames can disappear or change; existing sessions can retain their old callback URL. The manager rejects `trycloudflare.com`, localhost, private IP addresses and route-valued API URLs in production mode.

Do not put the agent-facing API behind an interactive login challenge. Preserve the application's signed request and user authentication controls. Non-interactive perimeter controls require explicit application support and end-to-end testing.

## Named Cloudflare Tunnel

Use a Cloudflare account, a domain you control and a remotely managed named tunnel. Follow [Cloudflare's official setup guide](https://developers.cloudflare.com/tunnel/get-started/). The VPS needs outbound tunnel connectivity; the bundled connector selects HTTP/2, using TCP rather than QUIC.

Save the named-tunnel token as one line in a private file on the VPS:

```bash
mkdir -p "$HOME/.config/kortix-v2-private"
chmod 700 "$HOME/.config/kortix-v2-private"
# Save the token using your private secret workflow, not shell history.
chmod 600 "$HOME/.config/kortix-v2-private/tunnel-token.txt"
```

Add this flag to the installation guide's `init` command:

```text
--named-tunnel-token-file /absolute/path/to/private/tunnel-token.txt
```

The manager mounts the file read-only at `/run/secrets/named-tunnel-token`. Only its path enters argv. The connector runs with dropped Linux capabilities and no-new-privileges so it can read the owner-only file without publishing its token. Do not run a second host connector or copy the token into a Compose command.

In the named tunnel's application routing configuration, use these Compose-network targets:

```text
https://app.example.com -> http://frontend:3000
https://api.example.com -> http://kortix-api:8008
```

Configure the required DNS records and a catch-all rule. The frontend build includes `/supabase/*` and `/v1/*` rewrites to the internal Supabase and API services. The separate API hostname is the public callback origin. Do not route the application hostname directly to the database or Supabase dashboard.

## VPS reverse proxy

Alternatively, terminate HTTPS with your existing Nginx, Caddy or other operator-managed proxy on the VPS. The stack's default host mappings are loopback-only:

```text
https://app.example.com -> http://127.0.0.1:13737
https://api.example.com -> http://127.0.0.1:13738
```

Preserve `Host`, `X-Forwarded-Proto`, WebSocket upgrade semantics and streaming. Do not buffer long-lived event streams or use a short idle timeout. Keep TLS keys private and expose only the public TLS listener. If instance ports are changed, update your proxy accordingly.

The upstream Caddy asset is retained for source completeness; the portable default template does not enable automatic host TLS. Your external proxy or named tunnel owns the stable HTTPS edge.

## Acceptance and failures

After services start, test from another network:

```bash
curl --fail --silent --show-error https://api.example.com/v1/health
curl --fail --silent --show-error -I https://app.example.com/
```

Then test an authorized conversation and an unauthorized ingress request. Health alone does not establish inference or persistence.

For DNS failures, fix DNS/routing and use a fresh conversation. A session rejected as `staleDevTunnelBox` must not be forced onto an unrelated replacement temporary tunnel. For API-health success with inference failure, check the actual runtime callback origin, model connection and session key selection, without publishing keys or raw provider logs.

Fresh stable-hostname end-to-end operation remains an environment-specific acceptance requirement for this release candidate.
