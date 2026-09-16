# Platform services

## Shared account runtime

`cubacadabra-app` is separate from the active game-session client. It owns
portable account state and decisions, including username normalization and
save eligibility, birthday validation, Morph loadout saves, catalog pagination,
blocked-user state, request/response decoding, stale-request handling, and
user-facing semantic feedback for the migrated slices.

Hosts own authentication, credential storage, HTTP execution, screen layout,
focus, navigation, and applying accepted snapshots to their native profile or
gameplay projection. Tokens remain outside Rust snapshots. Reporting remains a
host-specific moderation flow. This is not a migration of every platform
feature into Rust.

The app runtime uses a small action/snapshot/effect boundary: host code
dispatches an action, reads the current snapshot, performs emitted HTTP
effects with host credentials, then returns the status/body to Rust for
interpretation. A single shared test fixture covers the Rust decisions and
host projections. See [the app runtime contract](https://github.com/cubacadabra/rust/blob/main/docs/app-runtime.md)
for the current host lifecycle and documented checks.

## Backend data placement

| Data | Owner | Reason |
| --- | --- | --- |
| Live world membership, presence, retained game channels | One Durable Object per game instance | Ordered WebSocket coordination and session lifetime. |
| Current health/death/checkpoint projections | WebSocket attachment and broadcast | Needed by connected peers; not durable and not a storage-write-per-tick path. |
| Accounts, sessions, moderation, subscriptions, saved appearance | D1 | Durable account/product records and migrations. |
| Game package files, Morph packs, large immutable media | R2 | Blob delivery with content-addressed or versioned caching. |
| Analytics and deferred cleanup | Queues | Work that can be delayed, retried, or delivered at least once. |

Keep high-frequency movement and round synchronization on the Durable Object
WebSocket path. Queues are not a real-time gameplay transport. The backend
storage note includes operational guidance; its published free-tier quotas
are a time-sensitive snapshot and are intentionally not repeated here.
See [storage architecture](https://github.com/cubacadabra/backend/blob/main/docs/storage-architecture.md).

## Authentication, moderation, and subscriptions

The backend exposes web cookie sessions and native access/refresh token flows.
Hosts keep those credentials in platform-owned storage and attach them to
authenticated requests. Server-side checks remain authoritative for age
eligibility, username rules, moderation, and saved appearance validity; client
validation improves feedback but is not a security boundary.

Block/unblock and report endpoints exist. The live world uses block state to
filter peer visibility/movement for the blocking player. That is useful
platform safety functionality, but it is not a complete public-content
moderation, appeal, review, or creator-permissions system.

Subscription routes exist in the account platform. They do not imply an
in-game currency, creator payouts, trading, purchase ledger, or full creator
economy.

For the exact current HTTP surface and request shapes, use the backend’s live
OpenAPI contract and endpoint handlers. The older developer preview guide’s
HTTP table is useful as a snapshot, not a substitute for the deployed API
schema.

## Licensing

The current preview policy says Cubacadabra source, tools, runtimes, Studio,
and example game source are GPL-3.0-or-later unless a file or dependency has a
different notice. SDK helper code copied into generated game packages retains
that licensing obligation. Creators choose and publish a license for their
own game code and artwork; third-party assets and dependencies keep their own
terms.

Generated distribution packages should include the notices/attributions
required for redistributed source and assets. See [preview licensing](https://github.com/cubacadabra/tools/blob/main/docs/licensing.md)
and the individual repository `LICENSE` files. This is the project’s current
policy summary, not legal advice.
