# Studio and character assets

## Studio today

Studio is the native Rust desktop host and editor. It runs the shared engine,
loads a built package or a raw source project, supports a focused world
authoring/preview loop, and has a Morphs workspace. It calls the Rust API
directly. Its optional Codex integration edits the open project source and
lets Studio rebuild and preview the result.

The editor is not an OS-neutral UI layer: the desktop application is Rust/egui,
while account-facing and gameplay UI in web/iOS/Android remains native to each
host and in-game UI uses the shared runtime document.

Project creation and project building are separate steps. **File → New
Project** creates a source layout and embeds the current Luau SDK modules; it
does not require Python or an external CLI. Building a raw source project
invokes the game builder. Current Studio release artifacts ship that builder
as a Python zipapp, so Python 3 is required for raw-project builds on the
target machine. A built package can be opened directly without rebuilding.
See the [Studio setup and build notes](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/README.md#run-a-game),
[native project creation](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/src/game_creator.rs#L162-L268),
and [raw-project build invocation](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/src/project.rs#L239-L304).

## Morph workflow and ownership

The intended asset flow keeps source art with its game and separates it from
shared distribution:

```text
project-owned GLB + .morph.json sidecar
                 │
                 ▼
        Studio validation/compiler
                 │
                 ▼
        runtime .morphpack
                 │
        ┌────────┴────────┐
        ▼                 ▼
local game files     release tooling
                       │
                       ├─ immutable SHA-addressed pack in R2
                       └─ active catalog document in D1
```

Local GLB import and preview validate an asset in Studio. **Add to this game**
does not need authentication or upload the source; it writes the source GLB,
sidecar, compiled pack, thumbnail, and local character-catalog entry in the
game repository, then registers the pack in Studio's live renderer. These
steps prove local preview, not cross-client delivery.

The current builder copies the project `assets/` directory into a package and
records its files and hashes. Web, iOS, and Android package loaders resolve
game Morph packs from explicit `manifest.assets.morphPacks` entries. Studio's
**Add to this game** action currently updates only
`assets/characters/catalog.json`; it does not add those manifest entries.
Therefore imported files can be included in a package, but their automatic
cross-client wiring and a reproducible Studio-import-to-client run are still
open integration work. See the
[Studio import implementation](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/src/app_morphs.rs#L224-L262),
[builder asset packaging](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/src/cubacadabra/game_builder.py#L1028-L1065),
the [web package loader](https://github.com/cubacadabra/web/blob/cb720600a6db/src/game/loadGamePackage.js#L204-L228),
[iOS package loader](https://github.com/cubacadabra/ios_app/blob/a05217bcbd98/cubacadabra/GamePackage.swift#L425-L440),
and [Android package loader](https://github.com/cubacadabra/android_app/blob/34c114b1fe25/app/src/main/java/dev/andrewarrow/cubacadabra/game/GamePackageLoader.kt#L350-L375).

The editor importer documented in the public quickstart starts with the
supported rigid-wearable contract. The compiler/runtime also have skinned
asset support, but that does not mean the full body/outfit classification and
authoring flow is finished for creators.

The current tools `morph build` / `morph publish` commands are a maintainer
release pipeline: compile authored parts, generate immutable release files,
upload packs, and activate the catalog. They are distinct from the
creator-facing “share with community” Studio workflow. That self-service
community publishing flow remains a target, not an available editor action.

## Catalog, appearance, and pack format

- D1 `morph_catalog` stores an active JSON catalog document and its release
  identity/hash per channel. It is not currently a row-per-asset schema.
- R2 stores immutable runtime packs by SHA-256. D1 metadata points to those
  pack hashes. Clients fetch catalog pages and download only needed assets.
- Saved appearance is a separate D1 record with a monotonic revision and
  expected-revision checks. The current shared appearance is the V2
  data-driven loadout (base, parts, parameters, and optional face data); old
  body/outfit/equipment forms remain compatibility inputs/projections.
- `.morphpack` is the compiled character runtime format. Current compiler and
  shared runtime use schema 5; schemas 1–4 are rejected and must be rebuilt
  from source. This pack contract is independent of the appearance schema.
- GLB source must provide authored, valid normals for each rendered LOD.
  Morph runtime limits bound pack size, textures, geometry, surfaces,
  attachments, and uploads. See the source contract for exact field layouts
  and limits.

Use [the schema 5 format document](https://github.com/cubacadabra/rust/blob/main/docs/morph-pack-v5.md) for the
current binary contract; older schema 1–3 work-log entries in
[`morph_plan.md`](https://github.com/cubacadabra/rust/blob/main/docs/morph_plan.md) are historical implementation
steps. The backend’s original [D1/R2 area plan](https://github.com/cubacadabra/backend/blob/main/docs/morph_D1_R2.md)
is useful for product intent but its proposed catalog shape and example
`AppearanceSpec` should not override the implementation’s current D1 and V2
loadout contracts.

## Character visual direction

The engine can render data-driven bodies and wearables, but renderer fixtures
are not proof of product appeal. Current direction is a friendly casual person
with connected anatomy/clothing, readable motion, and a plain look that works
without decorative effects. Existing species and outfit entries are
compatibility/rendering fixtures; they are not all visually approved.

Visual approval is still open, and there is no validated preference study with
players or children. The art brief asks reviewers to compare idle silhouette,
ordinary gameplay distance, and motion, including reduced/no effects. See
[art direction](https://github.com/cubacadabra/rust/blob/main/docs/character_art_direction.md),
[runtime limits](https://github.com/cubacadabra/rust/blob/main/docs/character_runtime.md), and
[selected person captures](https://github.com/cubacadabra/rust/blob/main/docs/art/person/README.md).

## Studio references

- [Studio README](https://github.com/cubacadabra/studio/blob/main/README.md) — project opening, preview, Codex, and
  platform configuration.
- [Character asset flow](https://github.com/cubacadabra/studio/blob/main/docs/character-asset-flow.md) — local
  ownership decision, current rigid import slice, and proposed sharing flow.
- [Developer site quickstart](https://github.com/cubacadabra/developer/blob/main/dist/docs/index.html) — served
  onboarding content; its community-publishing claims need alignment with the
  implemented Studio UI.
