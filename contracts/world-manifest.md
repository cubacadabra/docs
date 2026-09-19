# World and manifest contract

**Status:** Current contract

**Maturity:** Preview

The manifest owns package content and generic world data, not engine code.
The current builder validates the exact accepted shape. The contract examples
below describe current preview capabilities; package/SDK version distinctions
are in [compatibility](../quality/compatibility/versions.md).

## Assets and world content

Worlds can declare palettes, blocks, signs, clouds, interaction zones, launch
pads, decorations, imported mesh instances, and image billboards. Package images may be JPG, JPEG, or PNG files under
`assets.images`. A world billboard references the image asset ID and supplies
position, width, and height. Named world materials can reference image assets
and `tileU`/`tileV` repeat them in world units per tile; image materials are
for surfaces, while billboards suit posters/signs.

The manifest's `effects` value may contain an inline effect library or
`{ "source": "effects.json" }`; the builder validates the relative path and
inlines the library so runtime packages stay self-contained. See
[effects](effects.md).

Keep state schemas and interaction IDs stable within a package version. Use
small semantic IDs that form the bridge between manifest, Luau, and retained
presentation.

## Terrain

Static terrain is an SDK `0.4.0`/`0.5.0` capability. It accepts ordered block, ball,
and ellipsoid fills, carves, and material-paint operations with semantic materials
`builtin:grass`, `builtin:ground`, `builtin:rock`, `builtin:sand`,
`builtin:mud`, `builtin:snow`, and `builtin:leafygrass` (bare names are also accepted). Terrain art
is engine-owned; the package does not carry duplicate textures. Terrain is
static package content, chunked and bounded at load. Luau terrain editing,
streaming edits, and saving modified terrain are not in this contract.

`leafygrass` uses grass surface detail on every face, including vertical walls;
`grass` retains its grass-top/soil-side treatment. Both reuse engine-owned art.

`materialArt: false` selects procedural color fallback. `hideDefaultGround`
controls whether the legacy flat ground remains below the terrain.

World presentation bounds are authored under `world`, while lighting and
atmosphere controls live under `world.visual`:

```json
{
  "world": {
    "presentationBounds": {
      "minimum": [-44, -9.3, -44],
      "maximum": [44, 7, 44]
    },
    "visual": {
      "colorCorrection": {
        "brightness": 0.12,
        "contrast": 0.20,
        "saturation": 0.60
      },
      "daylight": {
        "timeOfDay": 6.5,
        "geographicLatitude": 45,
        "brightness": 2,
        "outdoorAmbient": [0.5, 0.5, 0.5],
        "shadowSoftness": 0.5
      },
      "sunRays": { "intensity": 0.058, "spread": 0.463 },
      "fogStart": 52,
      "fogEnd": 120
    }
  }
}
```

`colorCorrection` applies once to the completed 3D scene, before UI. Its
`brightness` is additive; `contrast` and `saturation` are deltas from the
neutral value, so zero for all three fields is identity. `sunRays` is a bounded
radial-scattering pass from the visible sun: `intensity` and `spread` both lie
in 0 through 1, and zero intensity bypasses its work. It is rendered after
color correction and before UI. Bloom and blur are not part of this contract.

`daylight` is optional portable directional-environment data. `timeOfDay` is
local decimal hours in the half-open range 0 through 24, `geographicLatitude`
is degrees (-89 through 89), `brightness` is 0 through 4, each
`outdoorAmbient` component is 0 through 1, and `shadowSoftness` is 0 through
1. The runtime derives a deterministic equinox sun direction from time and
latitude; when `daylight` is present it overrides the legacy `sunDirection`.
The existing 3×3 shadow filter expands its radius as softness increases rather
than adding a second shadow map.

`exposure`, `contrast`, `saturation`, and `sunDirection` remain accepted for
existing SDK 0.5 packages. In the absence of `colorCorrection`, the first
three are mapped to the scene pass as legacy multipliers relative to neutral;
new packages should use `colorCorrection`. In the absence of `daylight`,
`sunDirection` continues to provide the directional light. These presentation
controls do not alter simulation or the gameplay camera.

`colorCorrection`, `daylight`, and `sunRays` require manifest SDK `0.5.0`.

`presentationBounds` optionally defines the primary authored subject used by
Studio's Overview and Showcase review cameras. Each array is an inclusive
world-space corner, with `minimum` strictly below `maximum` on all three axes.
Background scenery can remain outside these bounds and still renders normally;
it no longer forces the review camera to pull back. When the field is absent,
Studio derives bounds from all authored terrain and world geometry as before.

World gameplay may optionally author its third-person camera under
`world.camera`:

```json
{
  "world": {
    "camera": { "yaw": 1.25, "pitch": 0.4, "distance": 18 }
  }
}
```

Authored gameplay camera data requires manifest SDK `0.5.0`. The field is
optional so packages without it retain the legacy camera defaults.

The three values are required together and are radians/world units. `yaw` is
bounded to ±τ, `pitch` to the engine orbit pitch limit, and `distance` to the
inclusive range 0–120. Invalid or non-finite values reject the package. An
authored camera is applied when entering that world, including portal and
launch travel, and `reset_view` restores it. Worlds without `camera` retain
the existing runtime defaults and transition behavior. Snapshot restore
restores the captured camera after selecting the already-loaded world.

The presentation bounds and visual settings are renderer presentation controls;
unlike `world.camera`, they do not change the gameplay camera or simulation.
`decorations`
are static, deterministically authored visual instances. The legacy preview kinds are
`rock`, `palm`, `grass-clump`, `crate`, `bridge`, and `gate`; new content should
prefer an imported mesh decoration with an `asset` ID. Imported mesh instances
share indexed GLB geometry and carry independent position, scale, yaw, and tint
values. `scale` remains the legacy uniform value; authoring compilers may also
emit optional `scale3: [x, y, z]` for non-uniform mesh scaling, with missing
axes falling back to `scale`. A mesh decoration may also set `material` to a named world material;
that material's image is sampled through the package image atlas using the
GLB's UVs. When `COLOR_0` is present, its normalized RGB/alpha value multiplies
the instance tint, allowing one baked source mesh to preserve authored part
colors. GLB primitives may explicitly opt into engine-owned terrain surface
detail with a `builtin:` material name: `builtin:grass`, `builtin:ground`,
`builtin:rock`, `builtin:sand`, `builtin:mud`, `builtin:snow`, or
`builtin:leafygrass` (the terrain
alias `builtin:dirt` also selects ground). Ordinary artist names such as
`Grass`, `Slate`, or `Sand`, other namespaces, and unknown names do not opt in.
The glTF base-color factor still multiplies vertex color and instance tint;
an explicitly assigned package image material takes precedence over built-in
surface detail. The GPU material selector is an integer with flat interpolation.
Two-sided world-mesh faces use the visible face's normal for lighting.

The reference importer emits white `[1, 1, 1, 1]` base-color factors, preserves
source Color3 in `COLOR_0`, and records the source material name in
`material.extras.robloxMaterial`. Its mappings are import approximations:
Grass → grass; LeafyGrass → leafygrass; Ground/Brick → ground; Slate/stone/concrete/metals → rock;
Sand → sand; Wood/WoodPlanks → mud; Snow/Ice → snow. They are not additional
renderer aliases or promises of matching Roblox surface appearance.

This replaces the short-lived unnamespaced material-name experiment. Re-export
reference GLBs with the updated tool and rebuild packages to opt into textures;
old GLBs still load, but ordinary names no longer activate terrain textures.
The maze-101 source GLB is regenerated with this change. Published immutable
assets must receive new content identities. Meshes remain visual-only: the
runtime never derives collision from a GLB. Packages that need imported
scenery to be walkable provide the portable static triangle collision data
described below. Animation and prefab behavior remain separate capabilities.

## Static triangle collision

A world may contain an optional, renderer-independent collision mesh alongside
its terrain and visual content:

```json
{
  "collision": {
    "formatVersion": 1,
    "triangles": [
      [[-8, 0, -8], [8, 0, -8], [8, 0, 8]],
      [[-8, 0, -8], [8, 0, 8], [-8, 0, 8]]
    ]
  },
  "world": {
    "physics": {
      "groundCollision": false,
      "horizontalBounds": {
        "minimum": [-80, -64],
        "maximum": [96, 72]
      }
    }
  }
}
```

`collision.formatVersion` is required when collision is present and must be
`1`. Each entry is one triangle containing exactly three world-space XYZ
vertices. Creator tooling must bake source transforms and scaling into these
coordinates. Collision does not reference a model asset and hosts must not
load, inspect, or reinterpret GLB geometry to produce it.

Static collision and `world.physics.horizontalBounds` are SDK `0.5.0`
capabilities. Packages using either field must declare `sdkVersion: "0.5.0"`.

In creator source manifests only, `collision: {"source":
"reference/hub-collision.json"}` may replace the inline object. The Rust
builder resolves this JSON file inside the project root (including symlink
containment), validates format 1, and inlines it into the built manifest.
Absolute paths, parent traversal, files larger than 64 MiB, and mixing `source`
with inline fields are rejected. Runtime manifests must contain inline data;
hosts do not follow these authoring paths. The retired Python builder rejects
this capability rather than emitting unresolved collision.

The reference mesh exporter can emit the same baked geometry as a separate
collision document. Source `canCollide` controls inclusion, independently of
visual transparency; source transforms, mesh overrides, exclusions, and the
explicit export scale apply identically to both outputs. This conversion is
owned by tools, not a Roblox interpretation inside the runtime or Studio.

Format 1 is bounded to 200,000 non-degenerate triangles per world. Coordinates
must be finite and within -4096 through 4096 on every axis. Unsupported
versions, invalid triangles, and content that exceeds the bounded broadphase
limits fail world loading rather than silently losing collision. The runtime
indexes triangles in XZ buckets once at load; large triangles use a bounded
fallback list instead of expanding across an unbounded number of buckets.

Triangle faces are two-sided for collision. They support walkable floors and
slopes, walls, ceilings, landing/grounded state, and gameplay-camera sphere
occlusion. The character controller may make a small, bounded upward support
correction across ramps or closely spaced plank seams; this is not a general
wall-climbing surface. Areas with no collision triangle remain void. In
particular, triangle collision does not imply a flat floor: set
`world.physics.groundCollision` to `false` when the legacy ground plane should
not fill gaps between authored islands.

`world.physics.horizontalBounds` is optional. `minimum` and `maximum` are
strictly ordered finite world-space XZ pairs. They constrain the character
capsule horizontally; the capsule radius stays inside the authored edges. When
the field is absent, the existing -57.5 through 57.5 limits remain in effect.
These gameplay bounds are authored explicitly. The runtime does not derive
them from `presentationBounds`, terrain allocation, collision extents, or
decorative/render-mesh bounds.

The native Rust builder is the only supported expander for the bounded `maze`
declaration below. It emits the playable maze floor and walls, interaction
zones, checkpoints, generic start/finish landmarks, and generated maze effects
before packaging. It does not create an environment or choose an art direction:
an example that needs an authored island, props, or landmarks declares those as
ordinary package terrain, decorations, or assets. The retired Python builder
rejects maze declarations rather than producing a different-looking package.
The runtime consumes only expanded package data and does not execute the
authoring shorthand.

## Procedural maze declaration

The builder turns a bounded `maze` declaration into deterministic terrain,
interactions, and checkpoints. The current preview bounds mazes to 20×20 cells
and 64 collectibles. A given seed yields the same layout; change the seed when
authoring a new release rather than depending on runtime randomness.

`maze.landmarks` defaults to `true`. Setting it to `false` omits the generated
decorative start/finish gates without removing the finish interaction, floor,
walls, collectibles, or checkpoints. A source-faithful game can supply its own
landmark art without a generic gate obscuring the player's starting view.

Maze terrain is sampled at the declared `maze.terrain.cellSize`. To keep the
generated floor and wall features representable, that value must not exceed
`maze.wallThickness`. The builder rejects incompatible combinations before a
package is emitted. Generated walls overlap the floor by one terrain cell to
avoid gaps in the sampled surface, without changing their authored top height.

```json
{
  "worlds": {
    "starter-world": {
      "maze": {
        "width": 10,
        "height": 10,
        "cellSize": 8,
        "wallHeight": 7,
        "seed": 101,
        "start": [0, 0],
        "finish": [9, 9],
        "checkpointEvery": 12,
        "collectibles": { "count": 12, "color": "butter" }
      }
    }
  }
}
```

The native maze builder keeps the maze floor and wall geometry separate from
environment presentation. A package may add a visual-only imported mesh shell
or other authored scenery around the generated maze while leaving generated
terrain as the gameplay collision surface. If review cameras should frame a
specific subject, the package owns `world.presentationBounds` explicitly;
background scenery does not need to affect that framing.

These are static authored capabilities; they do not provide a general
creator-facing persistence API. For exact build behavior, use the
[game package contract](game-package.md) and [creator guide](creator-guide.md).
