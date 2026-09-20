# Roblox-style scene authoring plan

**Status:** Proposed product and implementation plan

This plan describes how Studio should approach the useful parts of Roblox
Studio's Explorer and viewport authoring workflow without making Roblox's
`Instance` model, services, or runtime behavior a Cubacadabra dependency.

## Goal

Make a creator able to understand and edit a large world from one coherent
scene hierarchy:

1. Find a named object in a searchable, expandable tree.
2. Select the same object from either the tree or the viewport.
3. Drag a visible gizmo to move, rotate, or scale it, with snapping and
   numeric editing available when precision matters.
4. Inspect the object's properties, duplicate/reparent/group it, and see the
   change reflected in the viewport.
5. Save, undo, rebuild, and preview through the same validated edit pipeline.

The target is the interaction quality visible in the supplied Roblox Studio
screenshots: dense rows, type icons, disclosure controls, selection highlight,
search, stable hierarchy, and direct manipulation. The target is not a visual
copy of Roblox Studio and not a request to expose Roblox services in the
Cubacadabra runtime.

## Evidence and current gap

The reference Vegas scene contains enough scale to expose the problem:

| Evidence | What it tells us |
| --- | --- |
| `other-examples/vegas.json` | 68,873 source instances, 17,420 geometry records, 12,275 non-transparent geometry records, 10,566 `Part`s, 4,412 `MeshPart`s, 3,025 `Model`s, 2,041 `Folder`s, 1,825 `UnionOperation`s, 610 lights, 135 textures, and 3,676 text objects. Each geometry record has a source `path` and `parentPath`. |
| `other-examples/vegas.rbxlx` | The full source instance hierarchy, including non-geometric folders, models, services, scripts, UI, lights, and properties. |
| `examples/vegas-101/manifest.json` | The current Cubacadabra package has one `vegas-floor` world, three baked environment meshes plus 245 promoted editable chairs backed by eight reusable chair assets, five signs, seven interactions, and no blocks. |
| Current Studio shell | `SceneNode` is recursive and selectable, with authoring-scene nodes using stable imported IDs while runtime-only fallback content still comes from typed manifest arrays. |
| Current viewport | Selection and limited X/Z Move/Resize already work for projected placeable objects. The viewport is still primarily a runtime preview; it is not a general authoring surface with a transform gizmo. |

`vegas.json` is therefore a valuable geometry/reference artifact but not, by
itself, a complete Explorer source. It does not carry every non-geometric
instance as a tree record. The importer must use the `.rbxlx` source when full
hierarchy fidelity is required, while keeping `vegas.json` as the normalized
geometry/reference evidence and parity input.

### The current Vegas render is an exporter-fidelity problem too

The current import/export bridge is a good temporary runtime boundary:

```text
vegas.rbxlx
    -> import-roblox-reference
    -> vegas.json                         [reference/evidence]
    -> export-reference-mesh
       -> vegas_map.glb / vegas_tables.glb / vegas_slots.glb
          + eight deduplicated local-space chair GLBs
       -> vegas-collision.json
    -> vegas-101 manifest
    -> normal Cubacadabra runtime
```

`vegas-101` remains compact after compilation: three baked environment mesh
decorations, 245 chair mesh decorations sharing eight reusable local-space
assets, five signs, seven interaction zones, and one collision file. The source place
does not need to remain a live runtime object graph. However, the current
`export-reference-mesh` path discards substantial source fidelity before the
runtime ever sees the scene:

| Source feature in the three Vegas export prefixes | Current result |
| --- | --- |
| 16,443 source geometry instances | Selected for the three exported areas |
| 4,417 instances with a source `meshId` | Box approximation when no mesh overrides are supplied |
| 1,798 `UnionOperation`s | Box approximation |
| Approximately 1,780 non-block `Part.Shape` values | Box approximation because shape is recorded but not exported |
| 564 `CylinderMesh` uses | Box approximation |
| MeshPart texture IDs, Decals, and textures | Captured by the reference importer but not emitted as textured GLB surfaces |
| 610 source lights | Captured but not emitted into the three GLBs |
| 3,676 text instances | Captured but not emitted into the three GLBs |

The current GLB writer emits `POSITION`, `NORMAL`, and `COLOR_0`, but not
`TEXCOORD_0`, images, samplers, or base-color textures. This is why the
reference casino carpet and other textured surfaces cannot be reproduced by
this exporter, regardless of how polished Studio's tree is. The material
mapping is also intentionally coarse for the current reference workflow:
metal and concrete become built-in rock, wood becomes built-in mud, and brick
becomes built-in ground. That remains an import approximation, not a runtime
material rule, but it is too lossy for a fidelity-oriented Vegas scene.

Studio hierarchy authoring and source-render fidelity are separate workstreams.
Both are needed, but improving the tree cannot compensate for geometry,
texture, union, shape, lighting, or text data discarded by the exporter.

## Product shape

### One World workspace with three synchronized surfaces

The World workspace should have the following stable relationship:

```text
Scene tree  <---- selection / expansion / rename / hierarchy actions ---->  Viewport
    |                                                                         |
    +--------------------------> Inspector <--------------------------------+
```

The tree is the primary navigation surface. The viewport is the primary
spatial editing surface. The Inspector is the precision and property surface.
Each surface must update the same selected entity; none should maintain a
second private interpretation of the scene.

The scene tree should feel Explorer-like:

- compact rows with a disclosure chevron, type-specific icon, display name,
  optional visibility/lock state, and a strong selected-row highlight;
- search with ancestor-preserving results and a clear way to reveal the
  selected match in context;
- lazy expansion and row virtualization for large source trees;
- multi-selection with keyboard modifiers, range selection for contiguous
  rows, and a visible count when more than one item is selected;
- context actions for add, duplicate, rename, delete, group, ungroup,
  reparent, focus in viewport, isolate, hide, and lock;
- persistent expansion and selection keyed by stable IDs, not array indices;
- a source/provenance badge where an item is imported or read-only.

The tree may use a familiar `Workspace`/`World` root for orientation, but it
must use Cubacadabra concepts beneath it. Do not invent Roblox-only service
roots such as `ReplicatedStorage` or `ServerScriptService` unless a future
Cubacadabra contract gives those roots real semantics.

### Edit mode and Preview mode

Studio should make the mode distinction explicit:

- **Edit:** stopped authoring viewport; clicks select scene objects and drags
  manipulate the selected object or gizmo.
- **Preview:** the current built package runs with gameplay input, camera, UI,
  physics, and Luau behavior.

Overview and Showcase remain useful review-camera presets, but they should not
be the only way to navigate a stopped world. Entering Edit must suspend
gameplay input capture for the viewport. Play/Stop must preserve the authoring
selection and camera state unless the creator explicitly resets them.

## Authoring data direction

### Preserve source hierarchy; adapt explicitly to the package

The current runtime package contract is intentionally compact: worlds contain
typed collections such as blocks, signs, interactions, decorations, and
terrain, while imported GLBs are visual-only and collision is supplied as a
separate baked asset. That contract should remain the runtime boundary.

For a Roblox import or a similarly detailed source asset, tools should produce
a project-owned, normalized scene graph with:

- a stable node ID and source path;
- display name and source class (`Folder`, `Model`, `Part`, `MeshPart`, etc.);
- parent ID and ordered children;
- local transform and derived world transform;
- visibility, lock, and editability state;
- supported geometry/material/collision references;
- source provenance and unsupported-property diagnostics.

The graph should be derived from the source `.rbxlx` hierarchy. The normalized
`vegas.json` geometry records should attach geometry facts to those nodes and
provide parity checks for transforms, bounds, materials, visibility, and
collision selection. Duplicate names are normal; identity must never depend on
the display name alone.

### Source hierarchy versus compiled runtime

The imported source graph and the player package intentionally preserve
different kinds of information. The source graph describes the scene as an
authoring dataset: objects, names, classes, parent relationships, stable
source IDs, transforms, provenance, and diagnostics. The compiler reduces that
dataset to the smallest runtime representations that preserve what the game
needs:

```text
Roblox/source hierarchy
68,873 source instances in the Vegas reference
        |
        +-- visual geometry ------> flattened GLB meshes
        +-- collision geometry ---> runtime collision data
        +-- runtime meaning ------> manifest data
        |                           signs, spawn, interactions,
        |                           lighting, bounds, and camera
        +-- game behavior ---------> game.luau
        +-- source-only detail ----> retained only in the authoring project
                                    names, Roblox classes, hierarchy,
                                    source IDs, and provenance
```

The Vegas package makes this reduction concrete: three baked environment GLBs
and eight reusable chair GLBs preserve
roughly 135,000 rendered triangles while each large exported scene mesh is
represented by one mesh node with a small number of material groups, rather
than thousands of runtime entities. Its 47,852 environment collision triangles remain
available to physics, currently inline in the compiled manifest, while the
source collision document remains authoring-only. Signs, interactions, spawn,
presentation bounds, lighting, fog, and camera settings remain manifest data
because they carry runtime meaning that geometry alone cannot express.

This is a deliberate lossy boundary. A shipped package must not be expected to
reconstruct the full editable imported scene; Studio uses the project-owned
`scene.json` and `imports/` datasets for that source-level understanding. The
runtime compiler may flatten, batch, instance, or spatially partition content
without making those implementation details part of the authoring model.

### Current transition: manifest-first projects and scene authoring

The two files answer different questions:

```text
manifest.json
    What does this game need at runtime?

scene.json
    What is the editable world in Studio?
```

Today, a simple project can still use the original manifest-native authoring
path:

```text
my-game/
  manifest.json
  src/main.luau
```

For example, a block may still be authored directly in a manifest world:

```json
{
  "id": "my-game",
  "version": "1",
  "blocks": [
    {
      "position": [0, 2, 0],
      "size": [4, 4, 4]
    }
  ]
}
```

No `scene.json` is required for that project. Studio's current simple-object
editing path can update the manifest, and the builder can package it directly.
This is supported compatibility behavior, not the intended long-term model for
large editable worlds.

When a project has a native authoring scene, the boundary becomes:

```text
manifest.json       game and runtime configuration
scene.json          editable world root and nodes
imports/            original imported hierarchy and provenance
src/                game behavior
assets/             meshes, textures, audio, and other source assets
studio.json         editor-only state and preferences
```

The current builder performs this transition at build time:

```text
read manifest.json
        |
        +-- if scene.json exists:
        |       validate it
        |       compile supported scene components into the manifest
        |
        +-- package the resulting runtime manifest and assets
```

The resulting manifest is the runtime representation. Player hosts do not load
`scene.json`, `scene/nodes/`, or `imports/`. Studio, the CLI, and future editors
must operate on the project-owned authoring data instead of reconstructing a
second scene interpretation from compiled runtime output.

This means a project may legitimately be in either state during the migration:

```text
manifest-only project
    manifest.json owns the authored world objects
    Studio's manifest editor reads and writes that data

scene-backed project
    scene.json owns the represented editable world objects
    manifest.json owns package/runtime configuration and any content not
    represented by the scene
    the builder compiles the scene into the runtime manifest
```

Do not edit the same object independently in both files. A block or other
world object must have one authoritative source. Existing manifest-only
projects can continue to build while the native scene workflow expands, but a
new Studio feature should add or migrate data into the scene model rather than
creating another copy in the manifest.

The difference is especially visible at Vegas scale. A small game containing a
few blocks, a sign, and a spawn point fits naturally in manifest collections.
The Vegas reference contains 68,873 source objects, including 3,025 models,
2,041 folders, 10,566 parts, 4,412 mesh parts, and 610 lights. At that scale,
stable IDs, parent/child relationships, folders, selection, reparenting,
duplication, transforms, undo/redo, and import provenance belong in a scene
graph rather than in growing runtime arrays.

The intended end state is that even a one-block project uses the same authoring
model as Vegas:

```text
manifest.json
scene.json
scene/nodes/...
src/main.luau
```

The exact sharded layout is still a storage migration. The currently supported
`scene.json` format is a single `formatVersion: 1` document with a `nodes`
array, as used by the Vegas authoring scene. The larger-project target is a
small root/index document plus stable-ID shards under `scene/nodes/`; it must
not be treated as live until its format and migration tooling are versioned.

### What Studio can create today

Studio's **New Project** workflow creates a minimal `scene.json` with one
`Starter World` root and no authored objects. It does not offer scene template
selection yet: a new project is intentionally blank, and **Scene → Add →
Block** is the first authored world object. The native import pipeline can also
create a scene through `cubacadabra import-roblox-scene`, as it did for the
Vegas authoring scene. There is still no equivalent `cubacadabra create-scene`
command for arbitrary existing projects.

When Studio opens a project, its current decision is effectively:

```text
Does scene.json exist?
        |
   +----+----+
   no       yes
   |         |
   v         v
preview    scene.json editing
manifest   + manifest configuration
```

If `scene.json` is absent, Studio can still preview the manifest-owned objects.
The first supported world edit creates a native scene, converts the active
world's Blocks, asset-backed mesh Decorations, Signs, Interactions, Ladders,
Checkpoints, Hazards, and Safe Zones into component nodes, and removes those
collections from the source manifest. Migration is prepared and validated
before either in-memory source changes. Unsupported legacy decorations stop
the conversion rather than disappearing.

If `scene.json` is present, Studio parses the authoring scene and uses its
component-node editing path. `primitive`, `text`, `interaction`, `ladder`,
`checkpoint`, `hazard`, and `safeZone` components support the corresponding Add
menu entries; asset-backed `render` components cover migrated mesh decorations.
The builder always regenerates all corresponding runtime arrays from the scene,
including empty arrays.

This split remains for compatibility with existing projects, but new projects
now start with the smallest valid native scene:

```text
new-game/
  manifest.json
  scene.json       # initially contains a World root
  src/main.luau
```

**Scene → Add → Block** creates a native scene node, and the builder compiles
that node into the runtime manifest. The scene root is deliberately empty so
this flow tests the authoring-to-runtime boundary directly; a genre-specific
starter such as an obby should be a separate future template choice.

The automatic migration now:

1. creates a native `World` root and deterministic stable IDs for the existing
   manifest objects;
2. converts supported blocks, signs, ladders, interactions, and other world
   collections into scene nodes, preserving order and supported properties;
3. reports unsupported or lossy fields instead of silently dropping them;
4. makes the scene source authoritative for the converted objects;
5. leaves package/runtime configuration and non-converted content in the
   manifest; and
6. removes the corresponding manifest arrays after successful conversion.

The conversion does not leave the same object independently editable in both
files. A future explicit conversion command may still be useful for reviewable
batch migration before the first edit, but it is no longer required to
establish the single-source rule.

The native authoring scene is a project format, not a Studio-specific format.
The format is text-first and sharded so that a large imported project remains
reviewable and editable in Git:

```text
manifest.json       game and package configuration
scene.json          small root/index document for the canonical scene dataset
scene/nodes/        sharded native NodeRecord files
imports/            sharded source/provenance datasets, grouped by importer
src/                Luau source
assets/             source assets and compiler inputs
studio.json         editor-only state such as previewWorld and reviewCamera
```

`scene.json` is the root document for the canonical editable world. In the
target sharded layout it declares the format version, roots, and node stores;
it does not require every `NodeRecord` to be physically embedded in one JSON
document. The currently supported v1 compatibility form embeds its `nodes`
array directly in `scene.json`. Studio is one editor of the dataset; Codex, the
CLI, scripts, other editors, and future web tooling must be able to read and
write the same files. `manifest.json` remains the package/config boundary used
by current projects, while the builder compiles the supported authoring dataset
into the existing manifest, asset, and collision outputs.

The target native storage contract is sharded JSON rather than a binary scene
format. A target root document may look like:

```json
{
  "formatVersion": 2,
  "worldId": "vegas",
  "roots": ["01K..."],
  "nodeStore": {
    "kind": "sharded-json",
    "path": "scene/nodes"
  },
  "imports": [
    { "kind": "roblox", "path": "imports/roblox/vegas/index.json" }
  ]
}
```

Shards should target 2–3 MiB and have an absolute 4 MiB ceiling. They must be
selected by stable ID prefixes rather than sequential record ranges, so adding
or editing one node does not renumber every later file. A bucket that exceeds
the target is split by the next ID prefix only; unchanged buckets retain their
paths. Each generated dataset must list its shard paths and byte sizes in its
index, and the writer/CI must fail rather than silently emit an oversized JSON
file.

Imported source records should store a stable ID, parent ID, source segment,
class/name, and only the local data needed by the inspector. Full source paths
are reconstructed by following parents; repeating `path` and `parentPath` on
every descendant is explicitly not part of the native representation.

`imports/<kind>/<name>/index.json` is the provenance boundary for an imported
dataset. It may contain sibling `nodes/`, `geometry/`, `lights/`, `textures/`,
and `diagnostics.json` stores. Conversion tools and Studio should consume this
same normalized dataset rather than generating overlapping monolithic JSON
copies. A disposable local cache may be added later for load performance, but
it must never become the canonical project format.
Existing projects may use a compatibility adapter during migration; Studio
must not silently create a second source of truth.

`scene.json` is not a player package contract and must not be loaded by player
hosts. If a rich scene graph later becomes a portable package capability, that
is a separate versioned contract decision with producer, builder, Rust, host,
and compatibility evidence. It must not happen implicitly as part of the tree
UI.

The shared legal and provenance boundary for `.rbxl`/`.rbxlx` importing lives
in the [toolchain import policy](../../systems/toolchain/overview.md#local-roblox-project-import-boundary).
Studio must surface the native importer's ownership affirmation, provenance
classifications, placeholders, omissions, and conversion diagnostics rather
than reinterpret them locally.

### Native `NodeRecord` identity and compilation status

The authoring graph should establish `NodeRecord` before the Explorer UI is
expanded. Source paths such as
`Model:Casino[1]/Folder:Furniture[1]/Part:Part[7]` are useful provenance, but
they are not editor identity: renaming, reparenting, or inserting an identical
sibling changes the path. Every record therefore needs an editor ID that
survives those operations:

```json
{
  "id": "01K...",
  "sourcePath": "Workspace:Workspace[1]/Model:Casino[1]/Part:Part[7]",
  "sourceKey": "rbx:part:source-guid-or-import-key",
  "sourceClass": "Part",
  "name": "Part",
  "parent": "01J...",
  "children": [],
  "transform": {
    "position": [0, 0, 0],
    "rotation": [0, 0, 0, 1],
    "scale": [1, 1, 1],
    "pivot": [0, 0, 0]
  },
  "representation": "primitive",
  "compile": {
    "capability": "editable",
    "status": "compiled",
    "diagnostics": []
  }
}
```

The exact serialized ID algorithm is an implementation decision, but the
semantics are fixed: a newly created duplicate gets a new ID; rename and
reparent preserve the ID; `sourcePath` is provenance only. IDs must be stable
across save/reload and deterministic import must not accidentally regenerate
them.

Every node also needs explicit representation and compile status. At minimum,
the representation vocabulary should distinguish `group`, `primitive`,
`meshInstance`, `light`, `surface`, `baked`, and `unsupported`. Capability and
status should explain what Studio can do and what the builder will emit, for
example:

| Source node | Capability | Compile result |
| --- | --- | --- |
| Normal `Part` | `editable` | `primitive` |
| Supported mesh instance | `editable` or `replaceable` | `meshInstance` |
| `UnionOperation` before union support | `readOnly` | bounding-box approximation, with a warning |
| Roblox script | `sourceOnly` | not executed by the scene compiler |
| Source light | `preserved` | runtime light when supported, otherwise explicit pending status |
| Grouped static chair | `editable` as a group | optimized baked mesh plus picking metadata |

Studio must be able to show this status in the tree and Inspector. A build
that approximates or drops source data should report it; a successful export
must not imply visual parity.

This keeps ownership clear:

- `tools` owns source import, normalization, stable IDs, geometry export, and
  conversion diagnostics, and scene compilation;
- `studio` owns tree, selection, gizmos, inspector, edit transactions, and
  preview integration;
- `rust` owns portable runtime/rendering semantics only when the existing
  package output requires a genuinely shared capability;
- `docs` owns the cross-repository contract and compatibility evidence.

### Import presentation versus editable scene content

A large imported mesh must not falsely imply that every triangle is an
independent editable Part. The tree should show two explicit levels:

```text
Imported asset / Vegas map                    [asset]
  Source hierarchy                            [source]
    Casino                                    [Model]
      Floor                                   [Folder]
        Part: ...                             [Part, editable if supported]
  Render mesh                                 [read-only or asset-level]
  Collision mesh                              [separate baked source]
```

In the first vertical slice, imported source nodes can be selected and
inspected, while only supported primitive/instance nodes are directly
editable. A read-only node must say why: “mesh is baked as one asset,”
“collision is generated output,” or “property is not supported.” This is more
trustworthy than exposing a Part row that cannot affect the package.

The normal authoring tree should not show all 68,873 source instances as equal
peers. Poses, `CFrameValue`s, keyframes, attachments, constraints, scripts,
GUI internals, and similar source details remain available in the import index
and provenance layer, but the default tree should prioritize:

```text
World
  Buildings / Models
  Parts
  Meshes
  Lights
  Surfaces / Signs
  Interactions
  Gameplay objects
```

Add a **Show Source Internals** mode for the complete imported hierarchy. This
keeps normal authoring useful while preserving forensic access to every source
object.

### Promotion is the migration path

The goal of import is not to make every source row unlocked. The durable goal
is:

> Every meaningful Roblox thing should either have a native, editable
> Cubacadabra representation or be clearly treated as source/reference data.

An imported row being locked is therefore not, by itself, a failure. It is a
temporary or intentional capability state. The importer should not pretend
that a source object is an editable scene object when the builder has no native
representation for its geometry, behavior, or properties.

The current importer already demonstrates this transition. Ordinary imported
nodes initially carry an explicit reason such as:

```text
Imported source node has no editable native representation yet
```

The chair pipeline then promotes a source subtree into a native node with
preserved provenance:

```text
representation = editable-imported-instance
render mesh    = vegas-chair-N
locked         = false
source         = roblox
source path    = Workspace:...
```

That is the general mechanism for imported-scene migration. The native node
retains where it came from without requiring the runtime or the authoring tree
to treat the original Roblox object model as Cubacadabra's type system.

#### Translate meaning, not just class names

The next useful promotion after chairs is ordinary geometry. A Roblox `Part`
such as `OuterRing` should eventually become a native primitive or render node
with its transform, size, material/color, and collision. It should then be
possible to select it, move it, resize it, rotate it, and have its collision
follow the same authoring transform. `DirtTrack` objects should follow the same
path when their source data is a supported `Part`, `MeshPart`, or `Model`.

The mapping is conceptual rather than a new Roblox-shaped native hierarchy:

| Roblox source class or concept | Native Cubacadabra representation |
| --- | --- |
| `Part` | Primitive or supported render node |
| `MeshPart` | Reusable mesh instance |
| `Model` | Group or asset instance |
| `SpawnLocation` | Spawn object/component |
| `PointLight`, `SpotLight`, `SurfaceLight` | Native light component |
| `Decal`, `Texture` | Surface/material data |
| `Seat` | Seat or interaction component |
| Trigger `Part` or zone | Editable trigger volume |
| Teleport marker or logic | Portal/teleport component plus game logic |
| `Script`, `LocalScript`, `ModuleScript` | Luau migration candidate, not scene geometry |
| `Folder` | Organizational group when it has authoring value |

This lets the importer preserve source provenance while translating useful
meaning into native components. A `Trigger` should not remain a list of locked
parts forever if its meaning can be represented as a movable, resizable
translucent trigger volume. Likewise, a `SpawnLocation` should become a
spawn, and a light should become a light. These are authoring concepts, not
requests to reproduce Roblox classes in the runtime.

The same distinction applies to game-specific source such as a blackjack
table. The table, chairs, trigger volume, dealer position, and lights may be
editable scene objects. Names such as `AlreadySplit`, `Bust`, `Hit`,
`DealerBlackjack`, and `Player1NoCredits` are more likely scripts, events,
values, folders, or state/configuration records. Their destination may be
Luau, game state, events, editable properties, or source-only provenance. They
should not become draggable objects with transform handles merely because they
appear in the imported hierarchy.

#### Separate the useful scene from source archaeology

The default Studio tree should distinguish the native authoring scene from the
complete imported source dataset:

```text
Scene
  Vegas Floor
    Environment
    Furniture
      Vegas Chair 1
      Vegas Chair 2
    Tables
    Triggers
    Lights
    Spawns

Imported Source
  Roblox
    Workspace
      Games
        ...
```

The native `Scene` tree should contain the useful editable game. `Imported
Source` should retain the original hierarchy, including `RemoteEvent`,
`BindableEvent`, value objects, scripts, GUI internals, and other implementation
artifacts for migration and debugging. Source-only records remain inspectable
through **Show Source Internals**, but they should not make the normal Scene
tree look like a wall of locked objects.

#### Promotion can be explicit

The importer does not need to explode every geometry record into a native node
on the first pass. It can retain an efficient baked representation and promote
objects as their authoring value becomes clear. The current ordinary-Part
milestone now provides a bounded automatic promotion path: anchored, ordinary
block Parts with axis-aligned rotations and no unsupported mesh, transparency,
or reflectance behavior become native box primitives. Dynamic Parts, non-block
shapes, arbitrary rotations, and other unsupported cases remain fallback
geometry with a diagnostic reason. Name filters remain available for focused
imports, but are no longer required for the default conversion.

The chair and primitive pipelines provide the sequence:

```text
identify source instances
  -> fingerprint repeated geometry
  -> create or reuse local-space assets
  -> retain each instance transform
  -> exclude promoted instances from the baked mesh
  -> create native authoring nodes with source links
  -> select the promoted node
```

Studio can expose the same operation for a supported source object as **Make
Editable**. The operation must locate or extract the source geometry, reuse an
asset when possible, remove the promoted content from the baked
representation, create the native node, preserve the source link, and select
the result. A failed promotion must leave the baked representation and source
data unchanged while reporting the unsupported property or missing asset.

Import presets can make the tradeoff explicit:

```text
Optimized       Keep most supported geometry baked
Balanced        Promote common furniture, lights, spawns, and gameplay objects
Fully editable  Promote all supported geometry and authoring concepts
```

`Balanced` is the sensible default for a large Vegas world. It preserves load
and editor performance while making the objects a creator is likely to move,
resize, or configure available as native nodes. Promotion status and source
links must remain deterministic so the result is reviewable in Git and can be
reproduced by the CLI.

Success should not be measured by driving the locked count to zero. The better
metric is whether every object a game developer reasonably expects to
manipulate has a native representation, while everything else is clearly
labeled source/reference data and stays out of the way.

### Authoring graph versus final scene compiler

`export-reference-mesh` should remain a reference baking tool. It is useful for
the current Vegas bridge, but grouping thousands of source objects into one GLB
by material loses the relationship between a triangle and its authoring node.
It should not become the final scene compiler by accretion.

The future compiler should be allowed to turn a rich graph such as:

```text
Casino
  Room
    Table 1
      top
      base
      stools
    Table 2
      top
      base
      stools
```

into an optimized runtime representation such as:

```text
static chunk A
static chunk B
shared table mesh × 12
shared stool mesh × 48
local lights
collision chunk A
collision chunk B
```

The authoring IDs must survive compilation through an editor-only picking and
diagnostic map. At minimum it should map compiled chunks, instances, and
pickable bounds back to one or more `NodeRecord` IDs, with a deterministic
tie-breaker for merged geometry. This lets Studio click a baked scene and
select the original source object without making each source object a live
runtime entity. The map may be a Studio-side derived artifact or optional
debug metadata; it must not become mandatory player runtime state.

## Viewport interaction plan

### Selection and hit testing

1. Build a scene selection index once per loaded/editable scene. It maps stable
   node IDs to world bounds, render references, and edit capabilities.
2. Hit-test visible editable instances in viewport order, with a predictable
   tie-breaker for nested/grouped objects and an option to cycle through
   overlapping hits.
3. Clicking an object selects it and highlights its tree row. Clicking a tree
   row focuses the object or group in the viewport. `F`/Frame Selected should
   work for one or many selected nodes.
4. Support click-empty-space deselection and modifier-based additive/toggle
   selection. Add marquee selection only after single-object selection is
   reliable.
5. Keep runtime UI hit testing and edit hit testing separate. A game button in
   Preview must never steal a drag intended for an Edit gizmo.

### Transform tools

Add an explicit viewport tool strip modeled on the useful Roblox tools:

- Select;
- Move, with axis and plane handles;
- Rotate, with axis rings;
- Scale, with axis and uniform handles;
- Transform, a combined mode where appropriate.

Every drag must be a transaction with an origin snapshot. Apply grid and angle
snapping during the drag, show live numeric deltas, and commit once on release.
Escape cancels the transaction. The Inspector remains available for exact XYZ
position, rotation, scale/size, pivot, and parent-space values. The initial
Vegas slice can support world X/Z movement and primitive size changes, but the
tool API should be designed around full transforms so the first implementation
does not hard-code another collection-specific path.

Use a small, consistent set of defaults: one-stud-equivalent grid snapping,
optional angle snapping, world/local axis toggle, and a visible pivot. Defaults
must be configurable later without changing the scene data model.

### Hierarchy operations

After selection and transforms are solid, add rename, duplicate, delete,
group/ungroup, and reparent. Reparenting must preserve world transform by
default and show a validation error when the target parent cannot contain the
selected node. Operations on imported read-only nodes should offer “duplicate
as editable instance” only when the builder can produce valid package output.

## Inspector plan

The Inspector should use the selected node's actual schema rather than a
collection-specific switch. Sections should appear only when relevant:

- Identity: name, stable ID, class/kind, parent, source path;
- Transform: position, rotation, scale/size, pivot, coordinate space;
- Appearance: color, material, transparency, cast shadow, visibility;
- Physics: anchored/static, can collide, collision source, bounds;
- Children: child count and hierarchy actions;
- Diagnostics: imported, read-only, unsupported, stale, or build error.

For multi-selection, show common values and mixed-value controls. For values
that are runtime-derived or baked, show them as read-only with their source.
The current sign text and primitive transform editors should become adapters for
this schema-driven inspector rather than remain separate special cases.

## Edit pipeline and persistence

All tree actions, Inspector edits, viewport drags, and future Codex edits should
enter one Studio command/mutation path:

```text
Input gesture / Inspector / Codex
        -> validate command
        -> mutate authoring graph
        -> append undoable transaction
        -> update tree, inspector, and viewport
        -> mark source dirty
        -> save / builder expansion / preview reload
```

The existing editing-model proposal is the architectural destination. The
first slice may implement the command path locally in Studio, but it should
use stable node IDs and transaction boundaries that can later feed the shared
mutation pipeline. Do not add one setter per UI control or write directly to
array indices from the viewport.

Save behavior must be explicit:

- edits update the source graph immediately and show a concise dirty state;
- undo/redo works across a complete drag or hierarchy operation, not every
  pointer move;
- invalid edits preserve the last valid state and explain the problem;
- rebuild expands the source graph to the current package contract;
- a failed build leaves the last working Preview running;
- imported derived GLBs, collision files, and hashes are regenerated rather
  than hand-edited.

## Delivery phases

### Phase 0 — establish the contract seam and benchmark

- Add an explicit decision record for `scene.json` as the project-owned
  authoring format, separate from `manifest.json`, `studio.json`, and compiled
  package output.
- Define and test the native `NodeRecord` contract, stable-ID behavior, source
  provenance, representation vocabulary, capability, and compile status before
  building more Explorer UI.
- Add a small Vegas fixture containing nested folders/models, repeated `Part`
  names, one imported mesh, one read-only/baked node, and one supported
  primitive.
- Add a native authoring import command, initially named `import-roblox-scene`,
  that creates/updates `scene.json` from the full source hierarchy. Keep
  `import-roblox-reference` as the exhaustive reference/evidence importer.
- Define the sharded JSON storage contract before writing a full imported
  hierarchy: stable-ID prefix buckets, 2–3 MiB targets, a 4 MiB hard ceiling,
  deterministic shard manifests, and parent-ID/source-segment records.
- Enforce the shared local-file, non-downloader, provenance, and non-executing
  import boundary described in the [toolchain import policy](../../systems/toolchain/overview.md#local-roblox-project-import-boundary).
- Extend importer and exporter diagnostics so the fixture reports source
  hierarchy counts, geometry parity, unsupported properties, approximations,
  unresolved mesh references, and stable IDs.
- Define selection, transform, save, undo, and rebuild telemetry-free test
  scenarios before changing the UI.

**Exit gate:** the fixture can be imported deterministically, and a reviewer
can explain which tree nodes are editable, read-only, or build-derived.

### Phase 1 — Explorer-quality tree on the current package model

- Rework the World tree into a dense, searchable, virtualized outline.
- Replace collection/index identity with stable IDs while keeping adapters for
  the current manifest arrays.
- Add tree-to-viewport and viewport-to-tree selection synchronization,
  expansion persistence, focus, visibility, lock, and clear read-only states.
- Show current Vegas content honestly: three baked mesh decorations, the
  promoted chair instances, five signs, and seven interactions, with no fake
  rows for the 10,566 source Parts.

**Exit gate:** tree navigation remains responsive with a synthetic 10k-node
fixture, search reveals ancestor context, and selection survives rebuild.

### Phase 2 — direct manipulation vertical slice

- Add Edit mode and the Select/Move tool strip.
- Generalize viewport projections and hit testing beyond blocks/signs to all
  supported authored instances.
- Add selection outlines, pivot, X/Z axis handles, grid snapping, drag preview,
  cancel-on-Escape, one-transaction undo, and Inspector synchronization.
- Keep Play as a separate Preview state with gameplay input routing.

The first working slice now covers every extracted Vegas `SofaChair`: after
stopping Preview, select any of the 245 promoted chairs in the Scene tree,
choose Resize, and drag its corner handles for X/Z size or the top-edge handle
for height.
The same non-uniform scale is editable numerically in the Inspector and is
compiled back into the mesh decoration. Extracted chairs carry reusable
instance-local collision sidecars: the source baked collision continues to
exclude them, while Play/build expands each sidecar at the editable node's
current transform into the one world-space static collision structure. Viewport
drags are transient and commit one source transaction on release. Other
imported Vegas source nodes remain intentionally read-only because their visible
geometry is still baked into the environment assets; chair source paths and
picking metadata are now available for the promoted instances.

The Phase 2 contract also rejects unsupported parent/shear compositions,
suppresses manipulation handles for locked baked assets, and gates non-uniform
runtime mesh scale behind SDK `0.6.0`. Promoted imported instances may now carry
an authoring `collision: {"kind": "mesh", "asset": "..."}` component. The
builder expands each reusable asset's local collision sidecar through the
instance world transform and merges it into the existing inline world collision;
the runtime still receives one static triangle structure rather than one
physics body per instance. These constraints keep the first
editable furniture set honest while broader source hierarchy editing remains
future work.

**Exit gate:** in Vegas or the fixture, a creator can select a supported object
  from either surface, drag it, undo it, save it, rebuild, and observe the same
  result in Preview.

### Phase 3 — source hierarchy and imported Vegas tree

- Extend the bounded normalized source graph produced from `vegas.rbxlx` in
  `scene.json`, with `vegas.json` geometry attached by source path and stable
  IDs assigned to records rather than derived from paths.
- Display folders, models, parts, mesh parts, lights, and UI under an imported
  source root with type icons and provenance.
- Add source-path search and “focus in source” navigation.
- Expose supported `Part` properties in the Inspector; keep baked mesh and
  unsupported classes read-only with diagnostics.
- Add the explicit builder adapter from editable source nodes to the current
  package decorations, primitives, collision, and assets.
- Add **Show Source Internals** for source nodes that are preserved for
  provenance but not shown as equal peers in the normal authoring tree.

**Exit gate:** a creator can find a named Vegas `Part`, see its parent chain,
  inspect its source properties, and either edit it successfully or understand
  exactly why it is read-only. The generated package remains valid and the
  existing Vegas gameplay loop still runs.

The current import milestone implements this boundary in two layers:
`import-roblox-reference` normalizes source instances and specialized geometry
facts, and `import-roblox-scene` writes a deterministic sharded import dataset
(`imports/roblox/<name>/index.json` plus `nodes/` shards) and a bounded
read-only source tree in `scene.json`. The default tree depth is intentionally
limited until Studio's source-internals view is virtualized. The reference
dataset and the Studio import should share one normalized representation rather
than copying every source instance into a second monolithic index. Geometry
exporters also emit local GLB bounds sidecars; manifest model declarations may
carry those generated bounds so Studio can size handles without hand-authored
`render.bounds` values.

For the Vegas fixture, the same importer promotes every `SofaChair` under
the table hierarchy into an unlocked authoring node and every supported
ordinary Part into a native primitive. Promoted primitives are organized under
native groups derived from meaningful source Models/Folders, linked from the
locked source tree, and excluded from the relevant baked meshes and collision
outputs. The importer writes actual promotion counts and fallback reasons. The
chair promotion preserves each source path and transform and deduplicates the
245 instances into eight reusable local-space chair assets; chair collision is
still intentionally deferred because the current collision contract is
world-static.

The source dataset uses SHA-256-derived IDs from source paths, keeps duplicate
names distinct, records geometry counts by source ID, and reconstructs source
paths through parent IDs and local source segments. It is an
inspection/provenance dataset, not a runtime entity list. Imported source nodes
remain locked until a native representation and an explicit builder adapter
exist for their properties.

### Phase 4 — source fidelity and compiled scene pipeline

This phase runs in parallel with the Studio tree work. It is not a prerequisite
for making the Explorer interaction model useful, but it is necessary for
judging Vegas against the Roblox reference screenshot.

- Keep `export-reference-mesh` as a bounded reference baking tool and improve
  its diagnostics immediately: unresolved mesh IDs, approximated unions,
  unsupported shapes, missing textures/UVs, dropped lights, and dropped text.
- Resolve the 27 unique Vegas mesh IDs used by the three export prefixes rather
  than treating 4,417 mesh-bearing instances as 4,417 unique assets.
- Add real primitive-shape export for supported `Part.Shape` and
  `CylinderMesh` cases, and add a measured path for `UnionOperation` rather
  than silently boxing it.
- Preserve UVs, textures, Decals, and material provenance where the native
  renderer can support them. Do not turn Roblox material names into new global
  runtime aliases; retain source material identity and use an explicit
  conversion policy.
- Define the compact runtime outputs for static batching, repeated mesh
  instancing, spatial render chunks, collision chunks, local lights, text, and
  editor picking metadata.
- Build from `scene.json` through a native scene compiler. Do not use the
  material-grouped GLB from `export-reference-mesh` as the final authoring
  representation.

**Exit gate:** a compiled Vegas slice reports every approximation and dropped
  feature, preserves real meshes/shapes/textures for the supported subset, and
  produces a compact runtime scene plus a Studio-only map back to `NodeRecord`
  IDs. The player/runtime does not receive one live entity per source object.

### Phase 5 — full transform and hierarchy authoring

- Add Rotate, Scale, combined Transform, local/world axes, angle snapping, and
  numeric drag readouts.
- Add multi-selection, marquee selection, duplicate, rename, group, ungroup,
  reparent, isolate, hide, lock, and frame selected.
- Add schema-driven Inspector sections and mixed-value editing.
- Move the local Studio command path onto the shared editing mutation feed when
  the shared contract is ready; do not duplicate runtime semantics in Studio.

**Exit gate:** the Vegas fixture supports a complete small-scene authoring loop
  with undo/redo and no collection-specific viewport code paths.

## Verification matrix

### Functional

- Tree rows for repeated names remain uniquely selectable and stable after
  save, reload, rebuild, duplicate, and reparent.
- Search handles case-insensitive names, class names, and source paths; it
  preserves enough ancestors to explain each result.
- Tree selection, viewport selection, Inspector selection, and `Frame Selected`
  remain synchronized.
- A drag creates exactly one undoable transaction; cancel restores the origin.
- Selecting a group offers group-level manipulation without accidentally
  editing an unsupported child.
- Read-only imported nodes cannot create silent package changes.
- Rebuild rejects invalid source data and leaves the last good preview intact.

### Vegas parity

- Import counts match the source fixture and `vegas.json` geometry summary.
- A sample of `Part`, `MeshPart`, `Model`, and `Folder` paths retains parent,
  name, occurrence, transform, and source provenance.
- Export diagnostics report unresolved mesh references, approximated unions and
  shapes, missing UVs/textures, dropped lights, and dropped text rather than
  presenting a lossy export as complete.
- Supported primitive shapes, real mesh references, UVs/textures, local lights,
  text, and unions are each tested against the source reference or explicitly
  marked unsupported.
- The compiled picking map selects the correct `NodeRecord` from a baked or
  instanced render representation.
- Exported visual and collision results are compared against the existing
  `vegas-101` package and its reference collision documents.
- The source `vegas.json` remains an evidence/reference artifact; generated
  package output is validated by the native builder and loaded through the
  same runtime used by Preview.

### UI and host behavior

Verify at 390×844, 768×1024, 1280×800, and 1440×900. At minimum, check that:

- the tree can be widened without making the viewport unusable;
- long names and deep paths truncate without losing the type icon or selected
  state;
- the Inspector remains usable for numeric edits on narrow windows;
- pointer, keyboard, modifier selection, focus, and Escape behavior are
  accessible and visible;
- Edit mode never routes clicks into game UI, and Preview never mutates source
  content through gameplay input;
- macOS, Windows, and Linux retain the same shared scene interaction model.

### Performance

Measure load, first paint, search, expansion, selection, and drag latency for
the 10k-node fixture and a full imported Vegas hierarchy. The tree must use
lazy/virtualized presentation, and selection/hit-test indexes must be built or
updated on scene changes rather than scanned recursively every frame. Large
meshes remain asset-level render data; the editor must not turn every triangle
into a live runtime entity.

## Decisions resolved by this plan

1. The project-owned canonical authoring format is a versioned text dataset
   rooted at `scene.json`; large node and import stores are sharded JSON, not a
   binary scene blob. It is not `studio.scene.json`, and it is separate from
   `manifest.json` package/config data and `studio.json` editor preferences.
2. The authoring graph and compiled runtime are different representations.
   The runtime must not receive one live entity per source object. Static
   batching, repeated-mesh instancing, spatial chunks, collision chunks, and
   compact lighting/text output are builder decisions.
3. `NodeRecord.id` is editor identity; `sourcePath` is provenance. Rename,
   reparent, and save/reload preserve IDs; duplicate creates a new ID.
4. Every node exposes an explicit representation, capability, compile status,
   and diagnostics. Unsupported or approximate output is visible to creators.
5. `import-roblox-reference` remains the exhaustive reference/evidence path,
   but its normalized source dataset is shared with the native authoring import
   rather than copied into a second path-heavy hierarchy file. The native
   authoring import creates/updates the `scene.json` root and sharded stores.
6. `export-reference-mesh` remains a temporary/reference baking tool. The
   final scene compiler owns optimized output and an editor-only mapping back
   to authoring IDs.
7. The default tree prioritizes useful authoring objects. Complete source
   internals remain available through **Show Source Internals**.

## Remaining implementation decisions

1. Which source classes are editable in the first imported-scene milestone?
   The recommended minimum is `Folder`, `Model`, primitive `Part`, and a
   supported mesh instance, with lights/UI/scripts initially read-only or
   source-only.
2. Does reparenting or transforming an imported Part compile as an individual
   primitive, an instanced mesh, or part of a rebuilt grouped asset?
3. What exact ID generation and merge policy handles imports, source refreshes,
   renamed source nodes, and two source files being combined?
4. Which operations belong in the shared Rust mutation feed, and which remain
   project-format operations owned by tools and Studio?
5. What are the node-count, mesh-size, collision-triangle, texture, lighting,
   text, and interaction-latency budgets for imported projects?

The first implementation should resolve the remaining decisions with the
small Vegas fixture, not with the full 68k-instance place. Once the seam is
proven, the full Vegas hierarchy becomes a scale and fidelity validation case
rather than the first source of truth for the editor architecture.
