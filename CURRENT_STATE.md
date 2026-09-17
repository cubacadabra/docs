# Cubacadabra Current State

Last updated: 2026-09-17

This is the short, current snapshot of Cubacadabra. It complements the
normative contracts, decisions, and roadmap; it is not a tutorial, architecture
deep-dive, or release promise.

## Maintenance rule

This file describes only the current state.

Update it in place as the project changes. Remove or rewrite stale items rather
than appending historical sections. Do not use this file as a changelog or
project diary; Git history preserves previous states.

Keep this file short and high-signal. If a detail is no longer useful for
understanding the current project state, delete it.

## Active milestone

Maze 101 visual parity with MayGo/maze-world screenshots.

## Recent context worth carrying forward

Keep only items that materially help someone understand the active work. Older
completed milestones should be removed as they stop being relevant.

- Generic imported GLB world meshes
- GLB world-mesh host parity across Studio, Web, Desktop, iOS, and Android
- Shared directional shadow mapping
- Shadow stabilization and flicker fix
- Deterministic Studio review cameras (`Gameplay`, `Overview`, `Showcase`)
- Shared viewport sky gradient
- Softer engine-owned grass and earth terrain tiles
- Maze package generation is native Rust-only
- Maze expansion keeps generated floor/walls separate from package-owned environment art
- Maze 101 owns authored island shells, sparse rocks/vegetation, and explicit presentation bounds
- Studio review cameras temporarily bypass gameplay distance fog

## Current visual gaps

- Atmosphere still needs depth cues and optional clouds
- Terrain palette needs in-Studio screenshot validation
- Island shells and dressing still need screenshot validation and further art direction
- Vegetation and landmark density still need screenshot-driven iteration
- Background composition needs screenshot validation after floor and grounding fixes
- Baseline/reference screenshot captures still need to be recorded and compared

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
