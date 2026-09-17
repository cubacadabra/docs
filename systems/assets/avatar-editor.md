# Avatar editor boundary

**Status:** Proposed cross-platform product and runtime direction. The backend
catalog and saved-appearance API are current; this page does not claim that a
standalone editor surface is shipped or verified on every host.

## Ownership

The avatar editor is a first-class platform surface, separate from a game
package. The target entry points are the web, iOS, and Android My Cube areas.
Each host owns navigation, authentication, and persistence requests. The
shared Rust runtime owns character composition and rendering. The backend owns
the durable catalog and saved appearance. Current catalog, asset, and save
behavior is specified in the [Morph catalog contract](./morph-catalog.md).

The target uses the same Rust character renderer as games while opening a
lightweight editor session. It loads the renderer, Morph assets, catalog data,
animation, camera, lighting, and editor controls. It does not load a game
package, terrain, multiplayer world, Luau scripts, NPCs, or full physics.

Runtime clients receive compiled, validated `.morphpack` assets. They do not
receive arbitrary GLB or Blender source files, source sidecars, executable
Rust, shaders, or scripts. Asset IDs remain stable and data-driven so adding a
body or wearable does not require a renderer code change. The existing
`users.body_id` value and legacy appearance messages remain compatibility
projections during migration.

## Host event seam

The host loads the saved appearance and opens the editor with that initial
value. The editor reports local preview changes and user intent; it does not
own credentials or perform platform navigation.

```text
openAvatarEditor(initialAppearance)
  → AppearanceChanged(appearance)       // local preview only
  → SaveRequested(appearance, expectedRevision)
  → CloseRequested
```

The host performs the save with the expected revision and reports the result
back through the app runtime. A stale revision must remain visible as a
conflict; hosts must not silently overwrite a newer saved appearance. The
versioned request and conflict behavior is defined by the
[saved-appearance contract](./morph-catalog.md#saved-appearance).

## Preview and browsing

The live 3D composition is authoritative. Thumbnails help browse individual
assets; they do not stand in for every possible outfit combination. The
target preview supports direct rotation, camera reset and zoom, immediate
selection updates, a clear current-item state, and a `None` choice for optional
slots. Useful poses such as idle, walk, run, jump, and wave expose clipping
that a static preview can miss.

Catalog browsing should use categories and metadata filters, lazy thumbnails,
and bounded pages or cursors. It should not download the entire catalog before
showing the editor. The exact category layout and presentation remain product
choices; hosts retain responsibility for accessibility and native navigation.

## Verification status

The backend read and revision-checked save paths are documented in the
[current backend contract](./morph-catalog.md). The standalone
cross-host editor session, matching preview composition, interaction flow, and
save-conflict presentation require host-level verification before being
described as shipped. See [host conformance](../../quality/compatibility/host-conformance.md)
for the evidence standard.
