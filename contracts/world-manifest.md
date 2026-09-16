# World and manifest contract

**Status:** Current contract

**Maturity:** Preview

The manifest owns package content and generic world data, not engine code.
The current builder validates the exact accepted shape. The contract examples
below describe current preview capabilities; package/SDK version distinctions
are in [compatibility](../compatibility/versions.md).

## Assets and world content

Worlds can declare palettes, blocks, signs, clouds, interaction zones, launch
pads, and image billboards. Package images may be JPG, JPEG, or PNG files under
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

Static terrain is an SDK `0.4.0` capability. It accepts ordered block/ball
fills, carves, and material-paint operations with semantic materials
`builtin:grass`, `builtin:ground`, `builtin:rock`, `builtin:sand`,
`builtin:mud`, and `builtin:snow` (bare names are also accepted). Terrain art
is engine-owned; the package does not carry duplicate textures. Terrain is
static package content, chunked and bounded at load. Luau terrain editing,
streaming edits, and saving modified terrain are not in this contract.

`materialArt: false` selects procedural color fallback. `hideDefaultGround`
controls whether the legacy flat ground remains below the terrain.

## Procedural maze declaration

The builder turns a bounded `maze` declaration into deterministic terrain,
interactions, and checkpoints. The current preview bounds mazes to 12×12 cells
and 64 collectibles. A given seed yields the same layout; change the seed when
authoring a new release rather than depending on runtime randomness.

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

These are static authored capabilities; they do not provide a general
creator-facing persistence API. For exact build behavior, use the
[game package contract](game-package.md) and [creator guide](creator-guide.md).
