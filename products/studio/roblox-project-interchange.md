# Roblox project interchange

**Status:** Current narrow implementation and forward contract

Cubacadabra Studio treats Roblox as an import and export target, not as its
internal object model. This lets a creator use Cubacadabra's editor and normal
source files without making an immediate platform decision:

```text
Roblox XML place ──> Cubacadabra authoring project ──┬──> Cubacadabra package
                                                     └──> Roblox XML place
```

The near-term product promise is deliberately smaller than complete Roblox
compatibility:

> Edit the supported parts of a Roblox place in Cubacadabra, preserve the
> unsupported source, and export a place Roblox Studio can continue editing.

## Product model

Projects have targets rather than mutually exclusive platform modes. A project
may eventually target Cubacadabra, Roblox, and other hosts at the same time.
The native `scene.json` remains the editable source of truth for Cubacadabra
entities; Roblox XML is an interchange format and preservation layer.

The three intended workflows are:

1. **Migrate:** import a Roblox place and publish it on Cubacadabra.
2. **Edit and return:** import, edit supported content, then export to Roblox.
3. **Multi-target:** author once and produce both Cubacadabra and Roblox output.

The third workflow is the long-term direction. It must not turn Roblox class
names, services, or runtime rules into Cubacadabra's native schema.

## Studio commands

Studio exposes the first target through the File menu on every desktop host:

```text
File
  Import From
    Roblox Place (.rbxlx)…
  Export To
    Roblox Place (.rbxlx)…
```

On macOS these commands live in the native application menu. On Windows and
Linux they live in Studio's in-window File menu. Both dispatch the same shared
Studio commands and use native file dialogs.

Import adds content to the open source project. It does not silently replace
the project. Export writes a generated artifact chosen by the creator; it does
not change the native project or publish anything.

## Compatibility states

Every Roblox feature should eventually have one explicit state:

| State | Meaning |
| --- | --- |
| Native | Studio understands, displays, and edits the feature. |
| Preserved | Studio does not edit the feature, but retains it in the preserved Roblox XML for export. |
| Converted | Studio substitutes a documented native or Roblox representation. |
| Omitted | No safe representation exists; export reports the omission instead of hiding it. |

Compatibility feedback should use these states in import/export reports and,
later, in a persistent target-status surface. “Roblox ready” must mean that no
unreviewed omissions remain, not that the two platforms are identical.

## Current `.rbxlx` slice

The first implementation supports a deliberately small vertical slice:

- File → Import From → Roblox Place reads XML `.rbxlx` files.
- Ordinary block `Part` instances under `Workspace` become editable native
  primitive nodes when they are anchored, opaque,
  non-reflective, use a supported material, and have a valid size. Their names,
  transforms, size, color, collision, and shadow state are editable; the source
  hierarchy is represented by native groups but remains preservation-owned.
- Source `Model` and `Folder` ancestors become native groups.
- The original `.rbxlx` bytes are copied under
  `imports/roblox/<name>-<hash>/source.rbxlx` and referenced as project-relative
  provenance from generated scene nodes.
- Unsupported Roblox instances remain in that preserved source. Export starts
  from the preserved DOM, updates supported source-linked Parts, and serializes
  the rest of the decoded Roblox instances and properties unchanged.
- The decoder reads properties missing from the pinned reflection database and
  the encoder writes them back. Known properties still use reflection-backed
  canonical Roblox names and types.
- Native Cubacadabra block primitives without a Roblox source link export as
  anchored Roblox Parts under a `Cubacadabra Export` model.
- Export reports updated Parts, new Parts, omitted native components, and
  compatibility warnings.

This is not full round-tripping yet. Current limitations are explicit:

- MeshParts, unions, non-block shapes, dynamic Parts,
  Parts with unmapped materials, transparent/reflective Parts, terrain, GUI,
  constraints, lights, effects, characters, and scripts are preserved in the
  Roblox source but are not editable through this interchange path.
- Preservation covers instances and properties decoded by the pinned Roblox
  XML/reflection libraries. Data unknown to those libraries cannot be promised
  byte-for-byte preservation.
- Native blocks added in Cubacadabra currently export beneath one generated
  Roblox model rather than recreating the full native group tree.
- Named Cubacadabra palette colors without a literal hex value may retain the
  imported source color or use a neutral fallback for a newly exported Part;
  export reports that compatibility warning.
- `.rbxmx` selection export and binary `.rbxl`/`.rbxm` are not implemented.
- Import/export currently runs as a synchronous desktop operation. Large-place
  progress and cancellation are required before this path is suitable for
  Vegas-scale projects.
- Studio currently requires exactly one preserved Roblox place when exporting.
  A scene containing multiple imports is rejected until the UI can select an
  explicit export target; overlapping source paths are never merged implicitly.
- Duplicating an imported node creates new authored content and severs its
  Roblox source identity, so the duplicate exports as a new object. Deleting a
  Roblox-linked node is rejected until explicit source tombstones are added.
- Source-derived groups that contain preserved, unsupported descendants are
  locked for transform operations; this prevents editable and preserved Roblox
  children from silently separating. Unsupported native materials produce an
  export warning instead of silently becoming Plastic.
- Export refuses a preserved source whose bytes no longer match the import
  identity recorded in the scene, and it retains absent default-valued Part
  properties when an unrelated edit is exported.

## Preservation rules

Preservation is the safety mechanism that makes progressive compatibility
usable:

> Anything Cubacadabra does not intentionally convert must survive an
> import → supported edit → export cycle with the same Roblox semantics as
> closely as the pinned XML and reflection libraries allow.

This is semantic preservation, not byte identity. XML formatting, property
ordering, explicit defaults, and referent spelling may change. Instance class,
hierarchy, decoded properties, attributes, tags, scripts, and references must
not be silently discarded or retargeted.

1. Keep the original Roblox XML inside the project as provenance.
2. Link native representations to stable Roblox hierarchy paths.
3. On export, mutate only the properties owned by a supported adapter. A visual
   fallback such as a Cubacadabra material must not replace the preserved
   Roblox source property unless the creator intentionally edits that property.
4. Preserve unsupported decoded instances and properties in place, including
   unsupported children of a natively editable parent.
5. Preserve instance references as relationships, not merely as serialized
   referent text.
6. Never claim successful compatibility for an omitted native feature.
7. Never require a Roblox XML round trip to build or run a Cubacadabra package.

Export updates only properties whose editable native values actually changed.
An untouched promoted Part is not rewritten, avoiding color quantization,
floating-point transform churn, and insertion of explicit defaults. Missing,
class-mismatched, or foreign-import source links produce compatibility warnings
and are never reclassified as newly authored native Parts.

Scripts remain embedded in the preserved XML in the current slice. A later
script adapter may materialize them as ordinary `.luau` files with mapping
metadata, but that mapping must retain Roblox container placement and must not
make Roblox service roots part of the Cubacadabra runtime model.

## Project and runtime boundary

```text
scene.json                         native editable entities/components
imports/roblox/.../source.rbxlx   preserved source and round-trip base
manifest.json + src/ + assets/    Cubacadabra game source
            │
            ├── Cubacadabra builder ──> portable runtime package
            └── Roblox exporter ──────> generated .rbxlx
```

The Roblox conversion code belongs to the shared creator tools layer. Studio
owns the desktop workflow, dialogs, status, and project integration; it does
not maintain a second interpretation of Roblox XML.

## Compatibility ladder

Work should expand through fixtures and measured promises rather than a broad
“supports Roblox” claim:

1. hierarchy, Models, Folders, and block Parts;
2. transforms, names, grouping, colors, and materials;
3. MeshParts and images;
4. Luau extraction and placement-preserving regeneration;
5. basic GUI;
6. attachments and common constraints;
7. lights and effects;
8. common character objects;
9. less common classes based on real project evidence.

The fixture ladder should include at least one block, multiple blocks, nested
models, materials, scripts, hinges, ropes, and GUI. Each fixture should prove
both the native facts promised by its adapter and preservation of unrelated
Roblox content across import → edit → export → re-import.

Every preservation fixture must make at least one supported edit. A no-op
import/export can pass by copying the source and does not exercise the merge
boundary. The baseline edit is to rename and transform one promoted Part while
comparing the rest of the decoded Roblox tree semantically.

The regression suite should grow around focused fixtures for unknown children,
scripts, attributes and tags, attachments and constraints, GUI, effects,
lights, sounds, MeshParts, terrain, material variants, unusual property types,
nested models, and root services. It also includes a compact kitchen-sink case:
an editable Part containing an Attachment with a ParticleEmitter and PointLight,
plus a Decal, Sound, Script, value objects, attributes, and an instance
reference. The test edits the Part and verifies that the nested hierarchy,
typed properties, source material, and reference target survive export.

## Genericity audit

The Studio and tools interchange boundary was audited on 2026-09-24. The audit
distinguishes the normalized reference importer—which intentionally recognizes
selected classes for one-way visual extraction—from the preserved XML DOM used
for editable round trips. A class allowlist in the former does not authorize
dropping that class or its properties from the latter.

| Surface | Round-trip rule | Regression evidence |
| --- | --- | --- |
| Native promotion | One shared tools-owned predicate recognizes only conservative block Parts. No project, path, or game name changes the decision. | Block, shape, mesh, dynamic, transform, transparency, reflectance, material, and size cases exercise the shared predicate. |
| Unknown classes and properties | Decode with `ReadUnknown`; encode with `WriteUnknown`; retain reflection for known canonical Roblox migrations. | An unknown future class carries binary, numeric, sequence, range, optional CFrame, physical, protected string, ray, rectangle, shared string, security capability, enum, UI dimension, unique ID, and vector values through export. |
| Unsupported children | Preserve them beneath a promoted parent in original order. | Attachment, ParticleEmitter, PointLight, Decal, Sound, Script, and value objects remain under an edited Part. |
| References | Preserve relationships after serialization assigns new referent text. | Beam attachment links, weld Part links, and ObjectValue links are compared by semantic tree target. |
| Root services | Preserve service trees without treating service names as native scene semantics. | Lighting, ReplicatedStorage, ServerStorage, ServerScriptService, StarterGui, StarterPlayer, SoundService, Teams, and MaterialService survive a Part edit. |
| Scripts and GUI | Preserve decoded source and typed UI properties without making them native runtime components. | Script, LocalScript, ModuleScript, ScreenGui, Frame, and TextLabel properties are compared semantically. |
| Assets and terrain | Preserve source IDs, payloads, and material values even when Studio cannot edit them. | MeshPart content IDs, Terrain binary payload, WoodPlanks, Metal, and Marble values survive export. |
| Ordering and defaults | Retain child ordering and absent properties; do not rewrite untouched promoted Parts. | The semantic DOM comparator walks the entire fixture by child ordinal and compares every non-edited property. |
| Multiple imports and stale links | Bind edits to the selected preserved source identity. Never fall through to native-Part creation. | Overlapping paths from two imports and a missing source path both have dedicated corruption regressions. |

The remaining preservation boundary is explicit: XML tags or value encodings
that the pinned `rbx_xml`/`rbx_types` stack cannot parse still fail import and
cannot be promised byte-for-byte preservation. Such failures must remain loud;
they must not be silently reinterpreted or omitted.

## Product guardrail

Cubacadabra must remain a clean, independent authoring and runtime platform.
Roblox compatibility is valuable because it lowers creator adoption cost, but
it cannot constrain every native capability or make Roblox the canonical
schema. When a Cubacadabra feature has no Roblox equivalent, Studio should show
that incompatibility and offer an explicit omission, conversion, or bake step.
