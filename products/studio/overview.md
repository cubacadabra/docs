# Studio

Studio is the local authoring and preview host for Cubacadabra games. It opens
or creates a project, embeds the supported Luau SDK, provides editor and
runtime preview features, and can import supported local Morph assets.

## Project creation and build prerequisites

Studio's **File → New Project** workflow creates and opens a starter project
without an external CLI or Python installation. It writes a manifest, a
starter letter puzzle in `scene.json`, a Luau entry point, embedded SDK, and
asset directories. The starter Luau document includes a left movement joystick
and right Jump and Run buttons for touch play on iPad. Raw source projects use
the shared Rust `cubacadabra-builder` crate in-process, so the complete
create, open, rebuild, and preview loop is self-contained in the installed
Studio release.

Studio and the native CLI both call the shared `cubacadabra-project` generator;
Studio requests its self-contained, vendored-SDK option. Importing a Roblox XML
place from the start screen creates an empty project and builds the imported
scene as its first preview. **Scene → Add** appends
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

Studio hides the engine-owned touch movement joystick in every Play preview
view, including local multiplayer tiles. Its keyboard and mouse controls remain
available. The same package still shows the joystick on touch Player hosts.
In local multiplayer, the touch Run button appears only in the full view of the
controlled player; smaller player previews omit it.

The Play button starts one player. Its adjacent menu starts 3, 6, or 9 local
preview clients in one private backend game namespace. Each client runs its own
game session and camera. The controlled player's view fills the World viewport,
with the other live views shown as smaller previews around it. In a nine-player
preview, eight views surround the full view. Player 1 receives Studio's keyboard
and pointer controls first. Click a smaller view to bring that player to the
full view and control it; the previous full view moves into the selected preview
position. Each preview keeps its own character animation history, including
when its view changes size; taking control stops autopilot input for that player.
Studio mirrors the locally simulated player positions directly between these
views, so a person appears in the same place across cameras while the backend
continues to handle presence and shared game state. Each preview player has a
distinct shirt color tied to their player slot, consistent in every view and
through swaps; these preview colors do not change the game's saved appearance.
Uncontrolled preview players wander, occasionally pause, sprint, and
jump using the same movement input as a player. Stop closes the extra clients
and restores the ordinary editor layout. Private preview sessions require a
reachable backend for player presence and shared game state; the individual game
views still render locally while the backend is unavailable.

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

The available workspaces are **World**, **Files**, and **Morphs**. Mock Assets,
Materials, and Test workspaces have been removed. Edit built-in surface
materials in the Inspector and browse actual project assets in Files. Use the
Play menu for real local multiplayer previews; a session/state/network
inspector is still open work.

**Add to local library** in Morphs saves and previews the local asset. The
control explains that package manifest wiring is unfinished. Room Video is
experimental capture and sparse-camera evidence; it does not yet turn a video
into a playable world. Roblox XML import/export is partial; consult the
[interchange limits](roblox-project-interchange.md).

The existing plan includes panels and visual-authoring ideas that are not
necessarily implemented. Studio directly calls Rust APIs rather than routing
in-process editor calls through C/JSON. See the shared
[client runtime](../../systems/runtime/client-runtime.md),
[editing model](editing-model.md), and the [roadmap](../../reference/roadmap.md).
