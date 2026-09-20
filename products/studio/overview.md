# Studio

Studio is the local authoring and preview host for Cubacadabra games. It opens
or creates a project, embeds the supported Luau SDK, provides editor and
runtime preview features, and can import supported local Morph assets.

## Project creation and build prerequisites

Studio's **File → New Project** workflow creates and opens a starter project
without an external CLI or Python installation. It writes a manifest, a
minimal `scene.json` with one world root, a minimal Luau entry point, embedded
SDK, and asset directories. Raw source projects use the shared Rust
`cubacadabra-builder` crate in-process, so the complete create, open, rebuild,
and preview loop is self-contained in the installed Studio release.

New projects start with a blank world rather than a genre template. Studio and
the native CLI both call the shared `cubacadabra-project` generator; Studio
requests its self-contained, vendored-SDK option. **Scene → Add** appends
Blocks, Signs, Ladders, Interactions, Checkpoints, Hazards, and Safe Zones as
native component nodes in `scene.json`; rebuilding compiles them into the
runtime manifest. The first such edit to an older manifest-only project
migrates those supported collections and removes their source-manifest copies.
See the [scene-authoring plan](roblox-style-scene-authoring-plan.md#what-studio-can-create-today).

A raw project may include `studio.json` with a `previewWorld` and
`reviewCamera` (`gameplay`, `overview`, or `showcase`). These are creator-only
preview preferences: Studio validates the world, applies it to the temporary
runtime manifest, and leaves the authored shipping launch destination intact.

Editable projects open stopped in Build mode. Build mode hides local and remote
players and runtime HUD, reserves left-click and left-drag for object selection
and manipulation, uses right-drag to orbit, middle-drag to pan, and wheel or
pinch to zoom. Overview and Showcase start by framing the world's presentation
bounds; clicking the selected preset again reframes the world. `F` frames the
selected object. Arrow keys nudge it by a quarter-unit along camera-relative
ground axes, and Command-D on macOS or Ctrl-D on Windows and Linux duplicates
and selects a copy.

Selection changes editor state only. It does not move the local player or the
editor camera, and clicking empty viewport space or pressing Escape clears the
object selection. Double-click and `F` are the explicit focus actions.

Play saves and rebuilds stale source before entering Game mode. Game mode uses
the gameplay camera, players, runtime HUD, and gameplay movement controls. Stop
returns to the editor camera position held before Play. Rebuilds of the same
project preserve that editor camera; opening another project or explicitly
choosing a camera preset reframes it. These creator-only controls do not change
gameplay camera state or snapshots. All embedded preview views fill the editor
viewport; this does not change the letterboxing policy of standalone player
hosts. The renderer entry points and editor camera state are gated by
`studio-ui`.

The raw-project path calls the shared Rust builder in-process. The native
`cubacadabra` CLI in `tools` is a thin command-line frontend over the same
library. Installed Studio releases do not require Python, `PYTHONPATH`, or a
separately installed CLI. See the [creator build toolchain](../../systems/toolchain/overview.md).

## Local asset workflow

Importing a GLB, validating a supported mapping, previewing it, and adding it
to a project are local operations. Studio writes source GLB, mapping sidecar,
compiled pack, thumbnail, and local catalog data. Local catalog presence does
not yet guarantee that the game manifest declares the pack or that a rebuilt
package loads it on every client. See [asset workflow](asset-workflow.md).

Community catalog publication is a separate explicit authenticated workflow
and is not implied by local import.

## Current boundaries

The existing plan includes panels and visual-authoring ideas that are not
necessarily implemented. Studio directly calls Rust APIs rather than routing
in-process editor calls through C/JSON. See the shared
[client runtime](../../systems/runtime/client-runtime.md),
[editing model](editing-model.md), and the [roadmap](../../reference/roadmap.md).
