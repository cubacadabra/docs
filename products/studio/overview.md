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

Overview and Showcase start by framing the world's presentation bounds and
support left-drag orbit, right- or middle-drag pan, and wheel/pinch zoom.
Clicking the selected preset again reframes the world. Navigation works while
the preview is stopped and does not change gameplay camera state or snapshots.
All embedded preview views fill the editor viewport; Gameplay keeps the player
camera. This does not change the letterboxing policy of standalone player hosts.
These renderer entry points and camera state are gated by `studio-ui`.

Selecting a placeable scene object brings the local preview character near that
object and turns the Gameplay camera toward it. This works while Play is
running and while the preview is stopped; it only changes the in-memory preview
state and does not change authored spawn data.

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
