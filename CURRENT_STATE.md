# Cubacadabra Current State

Last updated: 2026-09-18

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

Maze 101 three-island progression and visual parity with MayGo/maze-world
screenshots.

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
- Engine-owned palm and grass-clump decorations use tapered, palette-aware
  silhouettes instead of rectangular leaf blocks
- Maze package generation is native Rust-only
- Game scripts can read the host `DEBUG`/`RELEASE` build mode for development-only controls
- DEBUG game scripts can request local player teleports for fast preview checks; RELEASE omits that API
- Maze expansion keeps generated floor/walls separate from package-owned environment art
- Coplanar authored block-terrain fills use exact unions so overlapping floors
  do not create invisible player-collision ridges
- Maze 101 opens in a terrain-backed archipelago hub with five visible island
  landforms, authored cliff shells and rope bridges, destination gates, palms,
  rocks, and explicit presentation bounds
- Maze 101 is a three-island run: Sunshore, Coral Cay, and Cloudpeak increase in
  maze size, share a grass-hedge-and-sand art language, and the first two exits
  automatically route players to the next island
- Maze 101 removes authoring grids from every shipped world, uses a two-line
  top-center objective/timer HUD, keeps mobile controls out of Studio DEBUG
  captures, and has denser vegetation, explicit difficulty landmarks, and
  authored rope bridges with sagging decks and rails
- Studio review cameras temporarily bypass gameplay distance fog
- Shared third-person camera occlusion sweeps against terrain and solid blocks;
  forced close views drive the same local-avatar hide/fade transition as zoom
- Maze 101 corridors use the playable 8-by-7 cell-to-wall proportions
- The native tools CLI can deterministically extract Maze World's Roblox XML
  place data into a static reference-scene JSON with authored hierarchy,
  geometry transforms, materials, mesh/texture references, lights, cameras,
  text, spawn areas, project lighting/post effects, bounds, and source hashes
- A development-only Rust capture command consumes that reference scene and
  produces a real PNG plus a machine-readable approximation report; its first
  pass renders the 1,323 visible Main Island BaseParts/WedgeParts from their
  source transforms, dimensions, colors, and project lighting

## Current visual gaps

- The reference screenshots still need a fresh Studio capture after the
  tightened review-camera framing and grid/UI cleanup; headless proof cannot
  validate final pixels or creator-host overlay composition
- Maze 101's imported rope meshes remain visual-only, with package-owned
  terrain strips beneath the decks making every hub bridge traversable
- The first source-derived Maze World PNG can now be regenerated, but a fixed
  golden camera, checked-in target metadata, and automatic image diff are not
  established yet
- The reference-scene importer records Roblox smooth-terrain blobs but does not
  yet decode their voxels; external meshes, textures, local lights, shadows,
  skyboxes, and Roblox post effects remain explicit capture-report gaps

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
