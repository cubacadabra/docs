# Roadmap and known gaps

This page summarizes the durable work left before calling the creator
contract stable. It is a current cross-repository view, not a schedule or a
promise that every item in an older plan will ship.

## Working foundations

- One Luau package is built for the Rust runtime shared by Studio, web, iOS,
  and Android.
- The client protocol handles typed world messages, routing, remote-player
  state, and game-owned network output.
- The backend provides live WebSocket worlds, authenticated accounts,
  moderation, subscriptions, basic authenticated Cube uploads, latest-version
  catalogs, and package file delivery.
- The shared app core has migrated username/profile, Morph, cube-catalog, and
  blocked-user decisions to Rust action/snapshot/effect behavior.
- SDK helpers cover cooperative shared state, common obby/survival lifecycle
  behavior, cycles, and disclosure controls.
- Engine snapshots, simulation-tick tasks, headless deterministic runs,
  terrain, package media, and Morph asset delivery have explicit bounded
  contracts.
- Studio provides local project authoring and preview, a Morphs workspace, and
  an optional Codex workflow.

## Work that remains

### 1. Prove multiplayer behavior under real failure

The cooperative compare-and-set path still needs repeatable authenticated
multi-client evidence for reconnects, simultaneous operations, lost replies,
stale actions, malformed messages, and long-running sessions. Keep game rules
in Luau; test a proposed authority mechanism separately from the current
cooperative protocol.

### 2. Integrate trusted game authority before competitive rewards

The Rust `AuthorityBoundary`, Luau adapter, and package `authority.luau` entry
are prototypes. A production path still needs to bind authenticated socket
identity, provide trustworthy world/movement facts, execute constrained
game-owned validation and simulation, persist accepted state/receipts
atomically, and publish only accepted results. Current client movement is not
collision evidence.

### 3. Define durable game-owned state

Engine snapshots can represent a running engine and explicit game-owned state,
but there is no general creator-facing persistent game database contract.
Before offering durable inventory, progression, or rewards, specify schema
migrations, ownership and access checks, quotas, concurrency, reconnect and
restart behavior, deletion, and recovery.

### 4. Finish release and creator operations

The current Cube service accepts authenticated package uploads, checks package
metadata and hashes, stores versioned files, lists latest versions, and serves
launchable packages. A mature workflow still needs an explicit draft/validate/
stage/publish lifecycle, immutable version selection, rollback, visibility
and access rules, clear package diagnostics, and richer discovery. The current
Morph release CLI is an operator workflow; Studio does not yet offer creator
self-service Morph publication to a community catalog.

### 5. Close cross-host contract gaps

Keep the compatibility workflow green from a clean repository set and prove
the real boundaries on each supported host. Native Rust target compilation is
not the same as an Android APK/device test. Account and package tests should
cover the production Kotlin/JNI path as well as Rust, Swift, and the generated
WASM. Recheck the host verification notes in
[the app runtime doc](https://github.com/cubacadabra/rust/blob/main/docs/app-runtime.md) before release.

### 6. Set operational, safety, and performance budgets

Choose targets from measurements for package startup, asset decode, memory,
frame time, network traffic, concurrent sessions, and long-run reliability.
Before broad public user-created content, define permissions, reporting and
review operations, takedown/appeal handling, privacy/data deletion, resource
limits, and useful diagnostics. Existing block/report endpoints are a
foundation, not the whole policy and operations system.

## Suggested order

1. Reconcile the public developer guide with the builder and shipped flows,
   especially package/API versions and what “publish” means.
2. Keep the compatibility suite green and add authenticated multiplayer
   failure tests plus Android production-bridge/device verification.
3. Complete one narrow trusted-authority vertical slice before promising
   competitive outcomes or durable rewards.
4. Define and test durable game data, release/rollback, privacy, moderation,
   support, and performance behavior only as the product commits to them.

The SDK `1.0.0` checklist in
[`rust/docs/features_still_needed.md`](https://github.com/cubacadabra/rust/blob/main/docs/features_still_needed.md)
is a proposed release gate. Its example “labs” for the third game are test
ideas, not a requirement to add UI to the product. Prefer automated tests for
the guarantees those probes are meant to demonstrate.

## Decisions to leave open until evidence requires them

- Whether a general-purpose scene/prefab encoding needs a binary counterpart.
  Current authored worlds remain JSON; `.morphpack` solves Morph assets only.
- Whether trusted game rules first run in a Worker/WASM Durable Object or a
  separate server runtime. The interface should be host-independent; the
  deployment target is not settled by the current prototype.
- Whether to add more Rust app-core features. Keep sharing semantic state and
  decisions where it removes real drift; keep native/web controls, navigation,
  and accessibility presentation in each host.
- What creator, organization, or parent pricing should be. The web pricing
  document is strategy brainstorming, not the public price book.

No release date or pricing tier is established by the plans summarized here.
