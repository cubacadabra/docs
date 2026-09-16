# Cubacadabra documentation

This repository is the cross-repository guide to Cubacadabra’s current product,
runtime, creator contract, and open work. It consolidates the useful, still
relevant material from the sibling repositories as of **September 16, 2026**.

## Start here

- [Product and current scope](product.md) — what Cubacadabra offers today and
  what is still a preview or proposal.
- [Architecture](architecture.md) — repository roles, runtime boundaries,
  data flow, multiplayer authority, and storage.
- [Creator contract](creator-contract.md) — packages, lifecycle, Luau APIs,
  SDK helpers, and the trust limits creators need to understand.
- [Platform services](platform-services.md) — shared account behavior,
  backend responsibilities, data placement, and licensing.
- [Studio and character assets](studio-and-assets.md) — current editor and
  Morph workflow, compiled assets, and character-art status.
- [Roadmap and known gaps](roadmap.md) — the important release work that
  remains, without carrying forward stale review findings as current bugs.
- [Sources and resolved conflicts](sources.md) — what was reviewed, which
  documents establish current behavior, and how conflicting statements were
  resolved.

## Current snapshot

- Cubacadabra is a **developer preview**, not a stable `1.0.0` creator platform.
- A game is authored as JSON manifest/world data, Luau source, and optional
  assets. The tools builder emits a versioned, self-contained package; the same
  Rust runtime powers Studio and the web, iOS, and Android game clients.
- The game builder accepts SDK contracts `0.3.0` and `0.4.0`. Terrain requires
  `0.4.0`; the preview guide is still titled 0.3. The package format is 3.
- Game rules belong to the game’s Luau. Rust provides generic simulation,
  rendering, client, and application mechanisms. Native and web shells own
  platform UI and side effects.
- Multiplayer retained state is ordered by the backend, but game-written
  payloads are still client-authored. Compare-and-set prevents honest clients
  from overwriting one another; it does not make scores or rewards trustworthy.
- The optional `src/server.luau` is packaged as `authority.luau` and can run in
  a Rust authority prototype. The live Durable Object does not execute it yet.
- Morph assets use a custom `.morphpack` format, currently schema 5. It is a
  character-asset format, not a general scene or prefab format.

## How to read this guide

Use these status words carefully:

- **Implemented** means the behavior exists in the current code. A unit test
  can establish a component behavior, but does not show that a product path
  uses it.
- **Integrated** means the behavior is connected to its intended application,
  service, or host path.
- **Host-verified** means that path has been exercised on the named platform or
  device; target compilation alone is not host verification.
- **Planned** means proposed work, not a shipped feature.

“Available to users” or “production” needs evidence of integration and release
status, plus host verification where the claim depends on a platform. A source
document or unit test alone does not establish that status. See
[Sources and resolved conflicts](sources.md) for precedence, reviewed source
revisions, and the disposition of every inventoried document.
