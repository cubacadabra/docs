# Source disposition ledger

This is the migration inventory for files found under sibling repository `docs/` directories and the served developer-site `dist/docs/` directory. It records where useful material went and the disposition of the source copies. It is provenance, not a prerequisite for understanding Cubacadabra.

Path note: row descriptions preserve historical source and pre-restructure
names so the migration remains auditable. The live canonical destinations are
the paths in this repository's current [root map](../README.md) and
[repository map](../repos/README.md); historical names in this ledger are not
links or competing homes.

The reviewed hand-written documents were moved or distilled here, and their
source `docs/` directories were retired after checking code, CI, fixtures, and
public routes for dependencies. The headless fixture remains with Rust tests;
character evidence remains under this repository's `evidence/`; public
developer documentation URLs are configured to redirect to their canonical
pages. This is
provenance for the migration, not a prerequisite for understanding the platform.

## Status meanings

- `MIGRATED` — useful content moved or distilled to the listed canonical destination.
- `SUPERSEDED` — replaced by a current contract/decision or obsolete proposal; the reason records what was kept and why the original is no longer canonical.
- `DISCARDED` — generated metadata or material with no durable product/engineering value.
- `MOVE-FIXTURE` — executable or structured test input copied to the implementation test tree.
- `MOVE-EVIDENCE` — non-executable visual/measurement evidence copied to central `evidence/`.
- `UNRESOLVED` — migration decision still missing. There are currently **0** such rows.

## Reviewed revisions

The inventory and source-document review used the checked-out source snapshots below before cleanup. Commit IDs are recorded as text so this ledger preserves provenance without making source repositories a reading dependency.

| Repository | Reviewed revision |
| --- | --- |
| `rust` | `0ef7ccd34ff6` |
| `tools` | `4c2c2f1683c7` |
| `backend` | `e45ebdf2ad69` |
| `studio` | `5b6df3db1c30` |
| `ios_app` | `a05217bcbd98` |
| `web` | `cb720600a6db` |
| `developer` | `8b1ed22185c6` |
| `other-examples/racer` | `fa491dfb7954` |

No `android_app/docs/` directory or source files were present. The separate generated OpenAPI/schema references remain with the backend generator, as allowed by the documentation policy.

The workspace also contained duplicate local checkouts `rust2` and `studio2`
of the same Rust and Studio remotes at matching revisions. Their duplicate
`docs/` trees were retired with the primary checkouts; they were not separate
documentation sources.

## File-by-file disposition

### `backend`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `backend/docs/morph_D1_R2.md` | `MIGRATED` | architecture/avatar-editor.md preserves the proposed cross-platform editor and host boundary; platform/morph-catalog.md, platform/moderation.md, platform/publishing.md, and verification/acceptance-criteria.md preserve current D1/R2 behavior and durable content-safety, revision, immutable-asset, and publish-atomicity requirements. Unverified UI details remain labeled proposed. |
| `backend/docs/storage-architecture.md` | `MIGRATED` | platform/backend-storage.md preserves data placement, operational rules, measurement needs, and dated free-plan allocations. |

### `developer/dist`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `developer/dist/docs/first-game/index.html` | `SUPERSEDED` | This served page duplicated the stale SDK 0.3 preview body; its public URL is configured to permanently redirect to contracts/creator-guide.md. |
| `developer/dist/docs/game-facing-api/index.html` | `SUPERSEDED` | This served page duplicated the stale SDK 0.3 preview body; its public URL is configured to permanently redirect to contracts/luau-api.md. |
| `developer/dist/docs/game-lifecycle/index.html` | `SUPERSEDED` | This served page duplicated the stale SDK 0.3 preview body; its public URL is configured to permanently redirect to contracts/lifecycle.md. |
| `developer/dist/docs/index.html` | `MIGRATED` | The public docs index is configured to permanently redirect to this repository's README and table of contents. |
| `developer/dist/docs/package-format/index.html` | `SUPERSEDED` | This served page duplicated the stale SDK 0.3 preview body; its public URL is configured to permanently redirect to contracts/game-package.md. |

### `ios_app`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `ios_app/docs/https_calls.md` | `SUPERSEDED` | The current host-driven action/snapshot/effect boundary is specified in architecture/app-runtime.md; Rust does not own HTTP transport or credentials. |
| `ios_app/docs/more_rust_idea.md` | `SUPERSEDED` | Historical shared-core proposal and estimates are replaced by the current cross-host app-runtime contract and accepted shared-runtime decision. |
| `ios_app/docs/more_rust_idea2.md` | `SUPERSEDED` | Historical follow-up is replaced by the current cross-host app-runtime contract and accepted shared-runtime decision. |
| `ios_app/docs/more_rust_idea3.md` | `SUPERSEDED` | Historical scorecard is replaced by the current app-runtime contract; its caution against moving trivial host presentation into Rust is preserved in decision 0003. |
| `ios_app/docs/rust_idea.md` | `SUPERSEDED` | Early platform-sharing proposal is replaced by architecture/app-runtime.md, architecture/client-runtime.md, and decision 0003. |

### `other-examples/racer`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `other-examples/racer/docs/images/racer-gameplay.png` | `MOVE-EVIDENCE` | Racer gameplay capture copied without editing to evidence/examples/racer-gameplay.png; the example README now links to the central evidence copy and the source duplicate was retired after verification. |
| `other-examples/racer/docs/images/racer-lab.png` | `MOVE-EVIDENCE` | Racer Lab capture copied without editing to evidence/examples/racer-lab.png; the example README now links to the central evidence copy and the source duplicate was retired after verification. |

### `rust`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `rust/docs/.DS_Store` | `DISCARDED` | macOS Finder metadata; no product or implementation information. |
| `rust/docs/README.md` | `SUPERSEDED` | Repository-local index replaced by this repository README and section indexes. Rust build/test instructions remain in rust/README.md. |
| `rust/docs/app-runtime.md` | `MIGRATED` | architecture/app-runtime.md contains the current shared account-runtime ownership, lifecycle, bindings, and verification scope. |
| `rust/docs/art/person/README.md` | `MIGRATED` | evidence/character/README.md preserves the selected study evidence, context, and reproduction notes. |
| `rust/docs/art/person/gait.mp4` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/gait.mp4; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/gameplay-laptop.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/gameplay-laptop.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/gameplay-phone.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/gameplay-phone.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/greeting.mp4` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/greeting.mp4; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-back.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-back.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-curious.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-curious.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-face.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-face.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-front.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-front.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-side.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-side.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-study-gameplay.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-study-gameplay.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-study-silhouette.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-study-silhouette.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-three-quarter.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-three-quarter.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-wave-silhouette.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-wave-silhouette.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-wave.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-wave.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/hero-wink.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/hero-wink.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-back.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-back.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-face.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-face.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-front.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-front.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-gameplay.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-gameplay.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-side.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-side.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-silhouette.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-silhouette.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/longer-three-quarter.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/longer-three-quarter.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/review-metrics.json` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/review-metrics.json; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-back.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-back.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-face.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-face.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-front.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-front.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-gameplay.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-gameplay.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-side.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-side.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-silhouette.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-silhouette.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/soft-three-quarter.png` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/soft-three-quarter.png; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/task6-moving-contact-diagnostic.json` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/task6-moving-contact-diagnostic.json; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/task6-moving-raised-contact-diagnostic.json` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/task6-moving-raised-contact-diagnostic.json; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/task7-moving-contact-diagnostic.json` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/task7-moving-contact-diagnostic.json; source duplicate was retired after the central copy was verified. |
| `rust/docs/art/person/task7-moving-raised-contact-diagnostic.json` | `MOVE-EVIDENCE` | Copied without editing to evidence/character/task7-moving-raised-contact-diagnostic.json; source duplicate was retired after the central copy was verified. |
| `rust/docs/audio-runtime.md` | `MIGRATED` | contracts/audio.md preserves the versioned API, WAV constraints, queue behavior, failure semantics, and exclusions. |
| `rust/docs/authority-map.md` | `MIGRATED` | architecture/authority.md preserves the message trust map, prototype boundary, and live-integration gaps; package auto-detection is corrected. |
| `rust/docs/baselines/.DS_Store` | `DISCARDED` | macOS Finder metadata; the directory held no baseline evidence. |
| `rust/docs/character_art_direction.md` | `MIGRATED` | product/character-direction.md preserves active art direction, open approval status, acceptance questions, and engineering boundaries. |
| `rust/docs/character_runtime.md` | `MIGRATED` | verification/character-runtime.md preserves runtime limits, compatibility rules, and reproducible capture/validation commands. |
| `rust/docs/client-runtime.md` | `MIGRATED` | architecture/client-runtime.md preserves Rust and host responsibilities, transport events, action polling, and binding rules. |
| `rust/docs/data_model.md` | `MIGRATED` | architecture/data-model.md preserves entity/mutation/cursor semantics, the current integration limit, and the one-description property-metadata rule; conversational explanation was distilled. |
| `rust/docs/direction.md` | `MIGRATED` | product/character-direction.md preserves the durable rule that body families need their own silhouette language; superseded toy-construction requirements are identified. |
| `rust/docs/effects-runtime.md` | `MIGRATED` | contracts/effects.md preserves node shapes, animation/variant behavior, one-shot lifetime, names, queues, copy limits, and reduced-effects semantics. |
| `rust/docs/features_still_needed.md` | `MIGRATED` | Its production-readiness checklist is distilled into verification/release-readiness.md and roadmap.md. The old SDK 1.0 scope and kitchen-sink work plan were not carried forward as commitments. |
| `rust/docs/five_ideas.md` | `MIGRATED` | Its durable ideas now live in architecture/data-model.md, verification/headless.md, contracts/snapshots.md, contracts/tasks.md, and architecture/authority.md; agent assignments and outside-product comparisons were omitted. |
| `rust/docs/headless/README.md` | `MIGRATED` | verification/headless.md contains the current command and deterministic-trace contract; executable inputs moved separately to rust/tests/fixtures/headless/. |
| `rust/docs/headless/game.luau` | `MOVE-FIXTURE` | Copied to rust/tests/fixtures/headless/game.luau so test input lives with the engine test tooling. |
| `rust/docs/headless/manifest.json` | `MOVE-FIXTURE` | Copied to rust/tests/fixtures/headless/manifest.json so test input lives with the engine test tooling. |
| `rust/docs/label-maker.md` | `MIGRATED` | architecture/data-model.md preserves the single shared property-description rule and the instruction not to build general reflection before a second real duplicate exists. |
| `rust/docs/morph-pack-v5.md` | `MIGRATED` | contracts/morph-pack-v5.md preserves the normative binary layout, validation rules, failure behavior, build/deploy procedure, and verified scope. |
| `rust/docs/morph_baseline_inventory.md` | `MIGRATED` | compatibility/morph-migrations.md preserves legacy body/appearance ID mappings and unknown-ID rejection; point-in-time inventory/capture status is explicitly dated. |
| `rust/docs/morph_plan.md` | `SUPERSEDED` | The long work log is replaced by the current MorphPack v5 contract, compatibility mapping, Studio asset workflow, and backend Morph catalog contract. Historical step-by-step work log is not needed as a current specification. |
| `rust/docs/network-runtime.md` | `MIGRATED` | contracts/network.md preserves message types, channel/payload bounds, CAS and reconnect semantics, server/client trust limits, and the authority boundary. |
| `rust/docs/snapshots.md` | `MIGRATED` | contracts/snapshots.md preserves snapshot contents/exclusions, fingerprint checks, atomic rejection, save/restore hooks, cursor behavior, and the deterministic run/capture/restore invariant. |
| `rust/docs/split_hot_crates.md` | `MIGRATED` | product/principles.md preserves the data-driven fast visual-iteration proposal. The proposed crate split and hot-reload implementation are explicitly not selected. |
| `rust/docs/task-scheduler.md` | `MIGRATED` | contracts/tasks.md preserves simulation-time semantics, queue ordering, error/raw-yield behavior, resume/safepoint limits, and native/browser contract. |
| `rust/docs/ui-runtime.md` | `MIGRATED` | contracts/ui.md preserves document model, safe area/root regions, event and pointer ABI, multi-pointer behavior, consumed-input rule, accessibility gaps, and exact limits. |

### `studio`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `studio/docs/character-asset-flow.md` | `MIGRATED` | studio/asset-workflow.md preserves local ownership/import behavior and the explicit remaining manifest/reproducible-client integration caveat. |
| `studio/docs/plan.md` | `MIGRATED` | studio/editing-model.md preserves the shared manual/Luau/AI edit pipeline and end-to-end texture/viewport/two-player/undo acceptance scenario. Unselected panel/workspace scope is not made a commitment. |

### `tools`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `tools/docs/big_direction.md` | `MIGRATED` | architecture/assets-and-prefabs.md and verification/acceptance-criteria.md preserve identity/reference remapping, schema/dependency rules, safe parse, explicit import errors, and round-trip tests; binary encoding remains undecided. |
| `tools/docs/bot_feedback.md` | `MIGRATED` | compatibility/host-conformance.md and verification/acceptance-criteria.md preserve semantic error-field parity and the requirement to exercise real host adapters; old one-time findings are not asserted as current bugs. |
| `tools/docs/cubacadabra-game-developer-guide-preview-0.3.md` | `MIGRATED` | contracts/creator-guide.md, lifecycle.md, world-manifest.md, luau-api.md, and the focused versioned API pages carry forward current useful contract details. Preview-only wording is not treated as current. |
| `tools/docs/disclosure-v1.md` | `MIGRATED` | contracts/sdk/disclosure.md preserves configuration, visibility synchronization, event handling, and node/name bounds. |
| `tools/docs/explain_5.md` | `MIGRATED` | decisions/0001-json-authored-content.md and architecture/assets-and-prefabs.md preserve JSON as current authored format and distinguish scene documents from compiled Morph assets. |
| `tools/docs/licensing.md` | `MIGRATED` | platform/licensing.md preserves the current GPL-3.0-or-later reuse summary and generated-SDK notice obligation. |
| `tools/docs/right_for_2026.md` | `MIGRATED` | product/creator-model.md and architecture/assets-and-prefabs.md preserve clean-machine creator independence, explicit pinned dependencies, source ownership, and the distinction between game creator and platform contributor. |
| `tools/docs/server_side.md` | `MIGRATED` | architecture/authority.md, contracts/game-package.md, platform/publishing.md, and roadmap.md preserve the automatic authority artifact behavior and the host-independent authority seam; deployment alternatives remain open. |
| `tools/docs/shared-state-v1.md` | `MIGRATED` | contracts/sdk/shared-state.md preserves full v1 configuration, operation status/retry rules, lifecycle, ordering, bounds, and trust caveat. |
| `tools/docs/size_problem.md` | `MIGRATED` | verification/performance.md and product/character-direction.md preserve the current complete-loadout budget and measurement rule. The older 8.30 MB/93,800-triangle measurement is point-in-time and not presented as current. |
| `tools/docs/survival-v1.md` | `MIGRATED` | contracts/sdk/survival.md preserves state/event fields, safe zones, and ephemeral-vs-durable state boundary. |
| `tools/docs/top_10_fixes.md` | `MIGRATED` | verification/acceptance-criteria.md preserves durable safeguards for output paths, last-good builds, budgets, authority bypasses, host parity, package integrity, clean-machine creators, and licensing; individual bugs were not assumed current. |
| `tools/docs/top_10_fixes_2nd_round.md` | `MIGRATED` | verification/acceptance-criteria.md and roadmap.md preserve atomic package activation, complete asset validation, real host-loader tests, and authority bypass tests; individual findings were reclassified rather than repeated as live defects. |

### `web`

| Original file | Status | Canonical destination or rationale |
| --- | --- | --- |
| `web/docs/pricing.md` | `MIGRATED` | product/principles.md preserves the proposed free-creation/free-publishing, no-ads/no-paid-placement, and child-safety monetization principles while explicitly discarding speculative prices and quotas. |
| `web/docs/sign_in_with_chatgpt.md` | `MIGRATED` | studio/editing-model.md preserves the requirement that AI-assisted edits use the same source, validation, preview, undo, and reload path. Codex App Server, subscription, executable bundling, and auth-flow claims are omitted as volatile unselected implementation proposals. |

## Prior central index pages

The first flat consolidation pages in this repository were reorganized and superseded during this pass: `architecture.md` became `architecture/overview.md` plus focused architecture pages; `creator-contract.md` became `contracts/*`; `platform-services.md` became `platform/*`; `product.md` became `product/*`; and `studio-and-assets.md` became `studio/*` plus evidence/compatibility pages. Their useful claims were checked against the reviewed source snapshots and current implementation notes.

## Cleanup completion

The source `docs/` directories in the reviewed backend, iOS, Rust, Studio,
Tools, and Web repositories were removed after checking references outside
those directories. Rust headless inputs remain in `tests/fixtures/headless/`;
generated backend API/schema references remain with their generator; repo
READMEs and contributor instructions keep local build and implementation
guidance. The developer site's established docs URLs are configured with
permanent redirects to this corpus.
