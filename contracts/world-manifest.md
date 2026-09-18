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

Static terrain is an SDK `0.4.0` capability. It accepts ordered block, ball,
and ellipsoid fills, carves, and material-paint operations with semantic materials
`builtin:grass`, `builtin:ground`, `builtin:rock`, `builtin:sand`,
`builtin:mud`, and `builtin:snow` (bare names are also accepted). Terrain art
is engine-owned; the package does not carry duplicate textures. Terrain is
static package content, chunked and bounded at load. Luau terrain editing,
streaming edits, and saving modified terrain are not in this contract.

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
      "exposure": 1.1,
      "contrast": 1.1,
      "saturation": 1.2,
      "fogStart": 52,
      "fogEnd": 120,
      "sunDirection": [-0.45, -0.82, 0.32]
    }
  }
}
```

`presentationBounds` optionally defines the primary authored subject used by
Studio's Overview and Showcase review cameras. Each array is an inclusive
world-space corner, with `minimum` strictly below `maximum` on all three axes.
Background scenery can remain outside these bounds and still renders normally;
it no longer forces the review camera to pull back. When the field is absent,
Studio derives bounds from all authored terrain and world geometry as before.

These settings are renderer presentation controls. They do not change terrain
materials, collision, simulation state, or gameplay cameras. `decorations`
are static, deterministically authored visual instances. The legacy preview kinds are
`rock`, `palm`, `grass-clump`, `crate`, `bridge`, and `gate`; new content should
prefer an imported mesh decoration with an `asset` ID. Imported mesh instances
share indexed GLB geometry and carry independent position, scale, yaw, and tint
values. A mesh decoration may also set `material` to a named world material;
that material's image is sampled through the package image atlas using the
GLB's UVs. When `COLOR_0` is present, its normalized RGB/alpha value multiplies
the instance tint, allowing one baked source mesh to preserve authored part
colors. Meshes remain visual-only: mesh collision, animation, and prefab
behavior are separate capabilities.

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
interactions, and checkpoints. The current preview bounds mazes to 12×12 cells
and 64 collectibles. A given seed yields the same layout; change the seed when
authoring a new release rather than depending on runtime randomness.

Maze terrain is sampled at the declared `maze.terrain.cellSize`. To keep the
generated floor and wall features representable, that value must not exceed
`maze.wallThickness`. The builder rejects incompatible combinations before a
package is emitted.

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
