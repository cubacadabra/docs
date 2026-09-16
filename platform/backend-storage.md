# Storage architecture for the first public MVP

**Status:** current MVP storage guidance. Free-plan allocations are a dated snapshot checked September 2026 and must be rechecked before operational budgeting.

The default production layout should remain one SQLite-backed Durable Object
per live game instance, D1 for durable relational product data, R2 for immutable
game content, and Queues only for deferred work. These systems solve different
problems and are not interchangeable tiers for the same data.

## Data placement

| Data | System | Reason |
| --- | --- | --- |
| Connections, presence, current round state, retained game channels | Durable Object | One coordinator gives a game instance ordered, strongly consistent compare-and-set state and hibernatable WebSockets. |
| Live health, deaths, checkpoints, and other per-player snapshots | WebSocket attachment + broadcast | Peers need the current value while connected, but a damage tick must not write storage and the value should disappear with the live instance. |
| Accounts, sessions, moderation, entitlements, durable progression | D1 | Relational queries and migrations fit product records that outlive a game instance. |
| Versioned game packages, WAV files, future thumbnails and large exports | R2 | Blob storage, HTTP caching, and free egress fit immutable content. |
| Analytics batches, report enrichment, cleanup notifications | Queues | At-least-once delivery is useful after the player-facing request, not in the live game loop. |

Do not route moves, casts, round synchronization, or authoritative gameplay
through Queues. Delivery is asynchronous and at least once, and a normally
delivered message consumes three operations: write, read, and delete.

## Free-plan guardrails

As of September 2026, the relevant published free allocations are:

- Durable Objects with SQLite storage: 100,000 requests/day, 13,000 GB-s/day,
  5 million rows read/day, 100,000 rows written/day, and 5 GB stored.
- D1: 5 million rows read/day, 100,000 rows written/day, and 5 GB stored.
- R2: 10 GB-month stored, 1 million Class A operations/month, 10 million Class B
  operations/month, and free Internet egress.
- Queues: 10,000 operations/day, or roughly 3,333 normally delivered messages
  before retries and batching effects.

These limits make the existing hibernatable WebSocket Durable Object the right
hot path. They also make per-movement storage writes, per-event D1 writes, and
per-event Queue messages poor defaults.

## Operational rules

1. Use one Durable Object id per allocated game instance, never one global room
   and never one object per player.
2. Keep frequent state in memory. Persist only the compact retained state needed
   by reconnecting players or an object restart, and coalesce writes.
   Use the reserved live player-state lane for health and lifecycle snapshots;
   never put those updates in retained `game_state`.
3. Delete Durable Object storage when an instance is retired. Empty SQLite
   objects still have storage overhead when left behind at scale.
4. Upload content-addressed or versioned packages to R2 and serve them with long
   immutable cache headers. Store package metadata and publication state in D1.
5. Batch optional analytics before Queue submission. Gameplay must remain
   correct when the queue is delayed, duplicated, unavailable, or disabled.
6. Put durable player progression in D1 only after its schema and write cadence
   are known. Round-local progress belongs to the instance object.

## Next measurements

Before launch, add per-instance counters for WebSocket messages, retained-state
writes, active duration, and peak connections. After real playtests, use those
numbers to set coalescing intervals and retention rather than moving systems in
anticipation of traffic.

Official references: [storage options](https://developers.cloudflare.com/workers/platform/storage-options/),
[Durable Objects pricing](https://developers.cloudflare.com/durable-objects/platform/pricing/),
[D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/),
[R2 pricing](https://developers.cloudflare.com/r2/pricing/), and
[Queues pricing](https://developers.cloudflare.com/queues/platform/pricing/).
