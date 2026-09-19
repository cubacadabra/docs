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
| `examples/vegas-101/manifest.json` | The current Cubacadabra package has one `vegas-floor` world, three baked mesh decorations plus one extracted editable chair, five signs, seven interactions, and no blocks. |
| Current Studio shell | `SceneNode` is already recursive and selectable, but it is synthesized from a small set of typed manifest arrays. IDs are collection/index paths such as `world/vegas-floor/signs/2`. |
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
       -> vegas-collision.json
    -> vegas-101 manifest
    -> normal Cubacadabra runtime
```

`vegas-101` remains compact after compilation: three baked mesh decorations,
one extracted chair mesh decoration, five signs, seven interaction zones, and
one collision file. The source place
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

The native authoring scene is a project format, not a Studio-specific format:

```text
manifest.json       game and package configuration
scene.json          canonical editable world and source graph
src/                Luau source
assets/             source assets and compiler inputs
studio.json         editor-only state such as previewWorld and reviewCamera
```

`scene.json` is the canonical editable world. Studio is one editor of it;
Codex, the CLI, scripts, other editors, and future web tooling must be able to
read and write the same format. `manifest.json` remains the package/config
boundary used by current projects, while the builder compiles the supported
`scene.json` subset into the existing manifest, asset, and collision outputs.
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
- Show current Vegas content honestly: three mesh decorations, five signs, and
  seven interactions, with no fake rows for the 10,566 source Parts.

**Exit gate:** tree navigation remains responsive with a synthetic 10k-node
fixture, search reveals ancestor context, and selection survives rebuild.

### Phase 2 — direct manipulation vertical slice

- Add Edit mode and the Select/Move tool strip.
- Generalize viewport projections and hit testing beyond blocks/signs to all
  supported authored instances.
- Add selection outlines, pivot, X/Z axis handles, grid snapping, drag preview,
  cancel-on-Escape, one-transaction undo, and Inspector synchronization.
- Keep Play as a separate Preview state with gameplay input routing.

The first working slice now covers one extracted Vegas chair: after stopping
Preview, select **Chair — Roulette Player 3** in the Scene tree, choose Resize,
and drag its corner handles for X/Z size or the top-edge handle for height.
The same non-uniform scale is editable numerically in the Inspector and is
compiled back into the mesh decoration. The rest of the imported Vegas source
remains intentionally read-only until source hierarchy import and picking
metadata are available.

**Exit gate:** in Vegas or the fixture, a creator can select a supported object
  from either surface, drag it, undo it, save it, rebuild, and observe the same
  result in Preview.

### Phase 3 — source hierarchy and imported Vegas tree

- Add the normalized source graph produced from `vegas.rbxlx` to `scene.json`,
  with `vegas.json` geometry attached by source path and stable IDs assigned to
  records rather than derived from paths.
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

1. `scene.json` is the project-owned canonical authoring format. It is not
   `studio.scene.json`, and it is separate from `manifest.json` package/config
   data and `studio.json` editor preferences.
2. The authoring graph and compiled runtime are different representations.
   The runtime must not receive one live entity per source object. Static
   batching, repeated-mesh instancing, spatial chunks, collision chunks, and
   compact lighting/text output are builder decisions.
3. `NodeRecord.id` is editor identity; `sourcePath` is provenance. Rename,
   reparent, and save/reload preserve IDs; duplicate creates a new ID.
4. Every node exposes an explicit representation, capability, compile status,
   and diagnostics. Unsupported or approximate output is visible to creators.
5. `import-roblox-reference` remains the exhaustive reference/evidence path.
   A separate native authoring import creates/updates `scene.json`.
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
