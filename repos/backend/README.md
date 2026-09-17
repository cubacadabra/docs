# `cubacadabra/backend`

**Owns:** the Cloudflare Worker, `/world/:worldId` WebSocket service, live
world Durable Objects, health endpoint, and service-side checks.

**Does not own:** browser delivery, package contents, host UI, or game-rule
authority execution.

- Runs in: Cloudflare Workers and Durable Objects.
- Depends on: host-authenticated requests and published package/service records.
- Used by: [Web](../web/README.md), [iOS](../ios_app/README.md), [Android](../android_app/README.md), and [Desktop](../desktop/README.md).
- Read next: [backend systems](../../systems/backend/README.md), [network contract](../../contracts/network.md), [authority](../../systems/authority/README.md).
- Verify with: [testing](../../quality/verification/testing.md) and [release readiness](../../quality/verification/release-readiness.md).
- Incomplete: live execution of game-owned trusted authority and complete safety operations.

Repository: [github.com/cubacadabra/backend](https://github.com/cubacadabra/backend)
