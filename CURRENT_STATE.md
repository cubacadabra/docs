# Cubacadabra Current State

Last updated: 2026-09-17

This is the short, current snapshot of Cubacadabra. It complements the
normative contracts, decisions, and roadmap; it is not a tutorial, architecture
deep-dive, or release promise.

## Active milestone

Maze 101 visual parity with MayGo/maze-world screenshots.

## Recently completed

- Generic imported GLB world meshes
- GLB world-mesh host parity across Studio, Web, Desktop, iOS, and Android
- Shared directional shadow mapping
- Shadow stabilization and flicker fix
- Maze package generation is native Rust-only
- Tapered floating-island generation
- Seeded wall-side dressing

## Current visual gaps

- Flat sky and weak atmosphere
- Terrain is too orange and saturated
- Island silhouette still needs refinement
- Sparse vegetation and landmarks
- Background composition is too empty
- Deterministic Studio comparison cameras are still needed

## Canonical repositories

- `rust` — shared engine, renderer, and runtime
- `tools` — builder and CLI
- `examples` — example games, including Maze 101
- `studio` — desktop creator app
- `web`, `ios_app`, `android_app`, `desktop` — player hosts
- `docs` — canonical project documentation

## Important constraints

- Shared capabilities belong in Rust/platform, not Maze-specific renderer
  hacks.
- Maze source builds must be deterministic.
- The native Rust builder is canonical.
- Screenshot quality, not feature count, is the current acceptance criterion.
