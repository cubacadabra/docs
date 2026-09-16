# Sources and resolved conflicts

## Scope reviewed

I reviewed the project-owned documentation under the sibling repositories:

- 23 Markdown files in `rust/docs/`
- 13 Markdown files in `tools/docs/`
- 2 Markdown files each in `backend/docs/` and `studio/docs/`
- 5 Markdown files in `ios_app/docs/`
- 2 Markdown files in `web/docs/`
- the 5 maintained static HTML pages in `developer/dist/docs/`
- two image assets inventoried under `other-examples/racer/docs/images/`

I did not treat documentation shipped by `node_modules` as Cubacadabra
guidance. The racer docs directory contains screenshots rather than product
or engineering documentation, so those images were not imported into this
guide. No source document in another repository was edited or removed.

## Source precedence

When documents disagree, use this order:

1. Current implementation and its contract tests in the owning repository.
2. A maintained, implementation-focused contract document in that repository.
3. A dated plan or review, interpreted only as the state/opinion at that time.
4. Public onboarding pages, checked against owner contracts and current
   implementation. They do not override technical contracts.

The pages in this repository summarize cross-repository behavior. They do not
replace the owning repository’s precise API schema or host-specific build and
release instructions.

## Current contract sources

- Runtime/app/client boundaries: [`rust/docs/app-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/app-runtime.md),
  [`client-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/client-runtime.md),
  [`ui-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/ui-runtime.md),
  [`network-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/network-runtime.md),
  [`audio-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/audio-runtime.md),
  [`effects-runtime.md`](https://github.com/cubacadabra/rust/blob/main/docs/effects-runtime.md),
  [`snapshots.md`](https://github.com/cubacadabra/rust/blob/main/docs/snapshots.md),
  [`task-scheduler.md`](https://github.com/cubacadabra/rust/blob/main/docs/task-scheduler.md), and
  [`authority-map.md`](https://github.com/cubacadabra/rust/blob/main/docs/authority-map.md).
- Creator package and helpers: [`tools/docs/cubacadabra-game-developer-guide-preview-0.3.md`](https://github.com/cubacadabra/tools/blob/main/docs/cubacadabra-game-developer-guide-preview-0.3.md),
  [`shared-state-v1.md`](https://github.com/cubacadabra/tools/blob/main/docs/shared-state-v1.md),
  [`survival-v1.md`](https://github.com/cubacadabra/tools/blob/main/docs/survival-v1.md),
  [`disclosure-v1.md`](https://github.com/cubacadabra/tools/blob/main/docs/disclosure-v1.md), and
  [`licensing.md`](https://github.com/cubacadabra/tools/blob/main/docs/licensing.md).
- Backend storage: [`backend/docs/storage-architecture.md`](https://github.com/cubacadabra/backend/blob/main/docs/storage-architecture.md).
- Studio source ownership and local asset workflow:
  [`studio/docs/character-asset-flow.md`](https://github.com/cubacadabra/studio/blob/main/docs/character-asset-flow.md)
  and [`studio/README.md`](https://github.com/cubacadabra/studio/blob/main/README.md).
- Current Morph pack format: [`rust/docs/morph-pack-v5.md`](https://github.com/cubacadabra/rust/blob/main/docs/morph-pack-v5.md).

## Conflicts resolved in this guide

### Cooperative retained state versus “authoritative” game outcomes

Some documents use “authoritative” loosely for the latest retained snapshot.
The current contract is narrower: the Durable Object assigns sequence numbers
and performs compare-and-set ordering, while clients still propose game-state
payloads. The server does not decide whether a score, pickup, or reward is
legitimate. The [authority map](https://github.com/cubacadabra/rust/blob/main/docs/authority-map.md) and
[shared-state guide](https://github.com/cubacadabra/tools/blob/main/docs/shared-state-v1.md) define this boundary.
This was checked against the [Rust authority contract at the reviewed revision](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/authority-map.md)
and the [shared-state helper contract](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/docs/shared-state-v1.md).

### `server.luau` has a package artifact, not live authority

[`tools/docs/server_side.md`](https://github.com/cubacadabra/tools/blob/main/docs/server_side.md) includes an older
statement that the server entry was not yet in the package builder. The
current builder automatically detects `src/server.luau`, emits
`authority.luau`, and records the authority entry in generated metadata. The
Rust boundary and server runtime are still prototypes; the live Durable Object
does not execute them. Package support must not be reported as production
authority. See the [builder code](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/src/cubacadabra/game_builder.py#L934-L950)
and [Rust authority contract](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/authority-map.md).

### Current Cube upload exists, but full release management is incomplete

Older preview/roadmap text says there is no publishing/discovery product. The
current backend has authenticated `/cubes/upload`, versioned package storage,
catalog/list/detail APIs, and package launch/file delivery; the web client has
upload and browse flows. The remaining gap is a more complete draft/stage/
publish/rollback/visibility/release-selection workflow and richer discovery.
These statements refer to different levels of maturity, not a contradiction
about whether any upload endpoint exists. This was checked against the
[backend package API](https://github.com/cubacadabra/backend/blob/e45ebdf2ad69/worker/app/cubes.js)
and [web package flow](https://github.com/cubacadabra/web/blob/cb720600a6db/src/game/loadGamePackage.js).

### Morph format and D1 catalog

Earlier `morph_plan.md` work-log entries describe pack schemas 1–3 and refer to
catalog seeding in a migration number that is now used for a different
migration. The current pack contract is schema 5; rebuild older packs from
source. D1 stores an active JSON catalog document per channel plus separate
revisioned appearance rows, while R2 stores immutable SHA-addressed assets.
The old Morph area plan is useful for product intent, but its illustrative
slot-based `AppearanceSpec` is not the current Rust/backend V2 loadout
contract. See the [schema 5 contract](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/morph-pack-v5.md)
and [current backend storage description](https://github.com/cubacadabra/backend/blob/e45ebdf2ad69/docs/storage-architecture.md).

### Binary scene format proposals

[`big_direction.md`](https://github.com/cubacadabra/tools/blob/main/docs/big_direction.md),
[`right_for_2026.md`](https://github.com/cubacadabra/tools/blob/main/docs/right_for_2026.md), and
[`explain_5.md`](https://github.com/cubacadabra/tools/blob/main/docs/explain_5.md) explore competing binary options.
The implemented state is simpler: authored world/package definitions are
JSON, packages are directories or ZIPs, and `.morphpack` is a separate
character asset format. No general binary prefab format has been selected.
This is recorded in the [reviewed creator package contract](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/docs/cubacadabra-game-developer-guide-preview-0.3.md)
and [schema 5 format](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/morph-pack-v5.md).

### Current character direction supersedes older visual metaphors

The active [art brief](https://github.com/cubacadabra/rust/blob/main/docs/character_art_direction.md) says the
“enchanted toy” construction is not a requirement and asks for a friendly
casual person whose appeal works without effects. Older `direction.md` and
`five_ideas.md` contain useful historical reasoning but should not override
that [current art brief](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/character_art_direction.md). Visual approval remains open.

### Sharing product logic in Rust is an implemented direction, not a line-count promise

The iOS docs [`more_rust_idea.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea.md),
[`more_rust_idea2.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea2.md),
[`more_rust_idea3.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea3.md),
[`rust_idea.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/rust_idea.md), and
[`https_calls.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/https_calls.md) are architecture discussions
and point-in-time estimates. The current app-core behavior is described in
[`rust/docs/app-runtime.md`](https://github.com/cubacadabra/rust/blob/0ef7ccd34ff6/docs/app-runtime.md): Rust shares semantic state and request/result
decisions, while each host executes transport and renders its own UI. Do not
carry forward historical line-savings or confidence percentages as current
metrics.

### Publishing a Morph to the community is not the same as importing one locally

The public developer-site pages in `developer/dist/docs/` are the maintained
static HTML served by the developer site, so they are public onboarding
content, not generated output. Their local GLB instructions match the current
Studio slice, but wording about an available authenticated community publish
action goes beyond the editor implementation. The Studio asset-flow document
still describes sharing as a future explicit action. Local import/add-to-game
works without an account; the current Morph CLI is a repository/operator
release path. The source boundary is recorded in the
[Studio asset-flow document](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/docs/character-asset-flow.md)
and [current import implementation](https://github.com/cubacadabra/studio/blob/5b6df3db1c30/src/app_morphs.rs),
compared with the [served site at the reviewed revision](https://github.com/cubacadabra/developer/blob/8b1ed22185c6/dist/docs/index.html).

### Point-in-time reviews and brainstorms are not a live issue tracker

[`top_10_fixes.md`](https://github.com/cubacadabra/tools/blob/main/docs/top_10_fixes.md),
[`top_10_fixes_2nd_round.md`](https://github.com/cubacadabra/tools/blob/main/docs/top_10_fixes_2nd_round.md), and
[`bot_feedback.md`](https://github.com/cubacadabra/tools/blob/main/docs/bot_feedback.md) report code observations
from particular snapshots, some of which have since changed. For example,
shared state now documents distinct operation IDs and round/session expiry,
and the current web package loader supports local packages beyond the built-in
examples. See the [current shared-state contract](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/docs/shared-state-v1.md)
and [web package loader](https://github.com/cubacadabra/web/blob/cb720600a6db/src/game/loadGamePackage.js).
Recheck an item against current code before reopening it as a bug.
The first review’s examples-license mismatch is also resolved in the checked-out
state: [`examples/LICENSE`](https://github.com/cubacadabra/examples/blob/0547ec41b6c1/LICENSE),
its readme statement, and the current preview licensing matrix use
GPL-3.0-or-later.

`web/docs/pricing.md` is a proposed pricing strategy, not an approved price
book. `web/docs/sign_in_with_chatgpt.md` is a historical Codex/App Server
proposal; Studio now documents an optional Codex integration in its README,
which is the current user-facing reference. `studio/docs/plan.md` is a vision
document, not a list of shipped editor features.

## Intentionally left out

This guide does not repeat every implementation work log, one-off review,
character capture, code sample, infrastructure price/limit, or product
brainstorm. Those details remain in their owning repositories. In particular,
Cloudflare quota figures were omitted because they change, and proposed
MessagePack/FlatBuffers choices, future hosting-provider choices, and pricing
tiers were not turned into commitments.

## Reviewed source revisions

The file inventory below and the code checks cited in this guide use these
checked-out revisions. The regular `main` links above are for browsing; the
commit links here identify the snapshot used for this review.

| Repository | Reviewed revision | Snapshot |
| --- | --- | --- |
| `docs` | [`8847955ee9bb`](https://github.com/cubacadabra/docs/commit/8847955ee9bb) | Initial consolidation reviewed before this second pass. |
| `rust` | [`0ef7ccd34ff6`](https://github.com/cubacadabra/rust/commit/0ef7ccd34ff6) | 2026-09-16, `adding run_time`. |
| `tools` | [`4c2c2f1683c7`](https://github.com/cubacadabra/tools/commit/4c2c2f1683c7) | 2026-09-16, `server side`. |
| `backend` | [`e45ebdf2ad69`](https://github.com/cubacadabra/backend/commit/e45ebdf2ad69) | 2026-09-16, `sever side`. |
| `studio` | [`5b6df3db1c30`](https://github.com/cubacadabra/studio/commit/5b6df3db1c30) | 2026-09-16, `select mode`. |
| `web` | [`cb720600a6db`](https://github.com/cubacadabra/web/commit/cb720600a6db) | 2026-09-15, `fix windows`. |
| `ios_app` | [`a05217bcbd98`](https://github.com/cubacadabra/ios_app/commit/a05217bcbd98) | 2026-09-13, scoped second-round fixes. |
| `android_app` | [`34c114b1fe25`](https://github.com/cubacadabra/android_app/commit/34c114b1fe25) | 2026-09-13, scoped second-round fixes. |
| `developer` | [`8b1ed22185c6`](https://github.com/cubacadabra/developer/commit/8b1ed22185c6) | 2026-09-15, `update`. |
| `examples` | [`0547ec41b6c1`](https://github.com/cubacadabra/examples/commit/0547ec41b6c1) | 2026-09-16, `adding maze refinements`. |

## Maintenance policy

- The repository that owns a contract keeps its detailed schema, operational
  steps, and tests. This repository keeps a concise cross-repository summary
  and links to that canonical source.
- When code changes a cross-repository contract, update the owning contract
  and relevant tests with the implementation, then update any affected summary
  here. Do not let an old plan or review silently become a second specification.
- Use **implemented**, **integrated**, **host-verified**, and **planned** as
  defined in [README](README.md). Production or user-availability claims also
  need release evidence; tests or prose alone are insufficient.
- At each documentation reconciliation, refresh this revision table and use
  commit-pinned links for evidence behind resolved conflicts. Keep current
  navigation links where they help readers find the latest source.
- “Archive/deletion candidate” below is a future owner decision, not a deletion
  request. No document or asset in another repository was changed or removed.

## Original source-file dispositions

Each Markdown source document reviewed is listed below. “Keep” means retain
the exact detail beside its owning code; the destination points to the summary
or canonical reference here. “Historical” means useful background that must
not be used as a current contract. “Archive/deletion candidate” means its
active value is covered here or it is a one-time discussion/review, subject to
the source owner confirming that no unique work remains. These are proposed
dispositions only; nothing has been moved or deleted in sibling repositories.

### `rust/docs/` — 23 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `rust/docs/README.md` | Keep | Local documentation index for Rust contributors; links to the detailed Rust references below. |
| `rust/docs/app-runtime.md` | Keep | Canonical shared account/product state contract; summarized in [Platform services](platform-services.md). |
| `rust/docs/art/person/README.md` | Keep | Operational index for character captures and art evidence; referenced from [Studio and assets](studio-and-assets.md). |
| `rust/docs/audio-runtime.md` | Keep | Canonical audio API and runtime limits; summarized in [Creator contract](creator-contract.md). |
| `rust/docs/authority-map.md` | Keep | Canonical authority and trust boundary; summarized in [Architecture](architecture.md). |
| `rust/docs/character_art_direction.md` | Keep | Current visual brief; summarized in [Studio and assets](studio-and-assets.md). |
| `rust/docs/character_runtime.md` | Keep | Canonical character runtime limits and validation; referenced from [Studio and assets](studio-and-assets.md). |
| `rust/docs/client-runtime.md` | Keep | Canonical client/session contract; summarized in [Architecture](architecture.md). |
| `rust/docs/data_model.md` | Keep | Detailed engine data-model behavior; summarized in [Architecture](architecture.md). |
| `rust/docs/direction.md` | Historical; archive candidate | Older character/product direction; current visual decision is in `character_art_direction.md` and [Studio and assets](studio-and-assets.md). |
| `rust/docs/effects-runtime.md` | Keep | Canonical effects API and bounds; summarized in [Creator contract](creator-contract.md). |
| `rust/docs/features_still_needed.md` | Keep as proposal | Proposed SDK 1.0 release gate, not current committed scope; selected durable gaps are in [Roadmap](roadmap.md). Revisit after release scope is decided. |
| `rust/docs/five_ideas.md` | Historical; archive/deletion candidate | Brainstorm and old agent assignments; useful rationale is selectively captured in [Studio and assets](studio-and-assets.md). |
| `rust/docs/headless/README.md` | Keep | Reproducible headless commands and deterministic trace check; the operational detail stays here. |
| `rust/docs/label-maker.md` | Keep | Current generic property-description contract; referenced from [Architecture](architecture.md). |
| `rust/docs/morph-pack-v5.md` | Keep | Normative current binary format contract; summarized in [Studio and assets](studio-and-assets.md). |
| `rust/docs/morph_baseline_inventory.md` | Historical; keep for comparison | Point-in-time compatibility and capture baseline; not a current feature checklist. |
| `rust/docs/morph_plan.md` | Historical; keep for implementation history | Work log and migration history; current format and catalog behavior are summarized in [Studio and assets](studio-and-assets.md). |
| `rust/docs/network-runtime.md` | Keep | Canonical client network API and limits; summarized in [Creator contract](creator-contract.md). |
| `rust/docs/snapshots.md` | Keep | Canonical engine snapshot semantics; summarized in [Architecture](architecture.md). |
| `rust/docs/split_hot_crates.md` | Historical; archive/deletion candidate | Architecture/performance discussion, not a committed crate plan; current repository roles are in [Architecture](architecture.md). |
| `rust/docs/task-scheduler.md` | Keep | Canonical tick-scheduler behavior and limits; summarized in [Creator contract](creator-contract.md). |
| `rust/docs/ui-runtime.md` | Keep | Canonical retained UI contract; summarized in [Creator contract](creator-contract.md). |

### `tools/docs/` — 13 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `tools/docs/big_direction.md` | Historical; archive/deletion candidate | Broad format and product discussion; current selected architecture is in [Architecture](architecture.md). |
| `tools/docs/bot_feedback.md` | Historical; archive/deletion candidate | One-time feedback snapshot, not a live issue list; [Roadmap](roadmap.md) contains rechecked durable gaps. |
| `tools/docs/cubacadabra-game-developer-guide-preview-0.3.md` | Keep | Detailed creator guide and examples; concise package/API overview is in [Creator contract](creator-contract.md). It remains versioned 0.3 material while tools also accept SDK 0.4. |
| `tools/docs/disclosure-v1.md` | Keep | Exact disclosure helper contract; linked from [Creator contract](creator-contract.md). |
| `tools/docs/explain_5.md` | Historical; archive/deletion candidate | Binary-format explanation/proposal; no new format was selected, as recorded in [Architecture](architecture.md). |
| `tools/docs/licensing.md` | Keep | Current example/reuse licensing matrix; linked from [Creator contract](creator-contract.md). |
| `tools/docs/right_for_2026.md` | Historical; archive/deletion candidate | Speculative format/product direction; current decisions are in [Architecture](architecture.md). |
| `tools/docs/server_side.md` | Historical; archive candidate | Contains future-hosting ideas and a now-stale builder statement; current packaging and trust limits are in [Architecture](architecture.md). |
| `tools/docs/shared-state-v1.md` | Keep | Exact cooperative retained-state helper contract; summarized in [Creator contract](creator-contract.md). |
| `tools/docs/size_problem.md` | Historical; archive/deletion candidate | Point-in-time package-size/format discussion; no measured format decision is recorded there. Current formats are in [Architecture](architecture.md). |
| `tools/docs/survival-v1.md` | Keep | Exact survival helper contract; linked from [Creator contract](creator-contract.md). |
| `tools/docs/top_10_fixes.md` | Historical; archive/deletion candidate | First review snapshot; recheck any claim against current code and [Roadmap](roadmap.md). |
| `tools/docs/top_10_fixes_2nd_round.md` | Historical; archive/deletion candidate | Second review snapshot; not a current backlog. Rechecked durable work is in [Roadmap](roadmap.md). |

### `backend/docs/` — 2 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `backend/docs/morph_D1_R2.md` | Historical; keep for product rationale | Detailed design and UX intent; current storage and appearance boundaries are in [Architecture](architecture.md) and [Studio and assets](studio-and-assets.md). Its proposed schema is not current. |
| `backend/docs/storage-architecture.md` | Keep | Canonical backend storage and operational description; summarized in [Architecture](architecture.md) and [Platform services](platform-services.md). |

### `studio/docs/` — 2 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `studio/docs/character-asset-flow.md` | Keep, with status caveat | Exact Studio workflow and product intent; summarized in [Studio and assets](studio-and-assets.md). Local catalog update is implemented; manifest-based package use still needs explicit wiring. |
| `studio/docs/plan.md` | Historical; archive candidate | Vision and target workflow, not a shipped-feature list; selected current gaps are in [Roadmap](roadmap.md). |

### `ios_app/docs/` — 5 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `ios_app/docs/https_calls.md` | Historical; archive candidate | Proposed Rust/host networking split; the current contract is `rust/docs/app-runtime.md`, summarized in [Platform services](platform-services.md). |
| `ios_app/docs/more_rust_idea.md` | Historical; archive/deletion candidate | Early shared-app-core proposal and estimates; implemented boundary is documented in the Rust app runtime and [Architecture](architecture.md). |
| `ios_app/docs/more_rust_idea2.md` | Historical; archive/deletion candidate | Follow-up architectural discussion; current boundary is in `rust/docs/app-runtime.md`. |
| `ios_app/docs/more_rust_idea3.md` | Historical; archive/deletion candidate | Follow-up scorecard and implementation critique; current boundary is in `rust/docs/app-runtime.md`. |
| `ios_app/docs/rust_idea.md` | Historical; archive/deletion candidate | Early platform-sharing proposal; current host responsibilities are in [Architecture](architecture.md). |

### `web/docs/` — 2 Markdown files

| Original document | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `web/docs/pricing.md` | Unresolved proposal; keep pending decision | Not an approved price book; the current non-commitment is recorded in [Product](product.md) and [Roadmap](roadmap.md). Retain until a pricing decision replaces it. |
| `web/docs/sign_in_with_chatgpt.md` | Historical; archive/deletion candidate | Proposed Codex/App Server workflow; current optional Studio integration is in the Studio README and summarized in [Studio and assets](studio-and-assets.md). |

### Public docs and inventoried assets

The public docs are maintained HTML rather than Markdown, but they are part of
the served website and the original review scope. They should be kept and
corrected in the developer repository when their user-facing claims drift.

| Original file | Disposition | Canonical destination or reason |
| --- | --- | --- |
| `developer/dist/docs/index.html` | Keep; follow-up correction candidate | Served quickstart; community-sharing wording needs alignment with current Studio behavior. Current scope is summarized in [Studio and assets](studio-and-assets.md). |
| `developer/dist/docs/first-game/index.html` | Keep | Served tutorial; detailed package commands remain in the tools guide. |
| `developer/dist/docs/game-facing-api/index.html` | Keep | Served API guide; canonical helper/runtime references are in [Creator contract](creator-contract.md). |
| `developer/dist/docs/game-lifecycle/index.html` | Keep | Served lifecycle guide; canonical behavior is in the tools guide and Rust runtime contracts. |
| `developer/dist/docs/package-format/index.html` | Keep | Served package guide; canonical summary is [Creator contract](creator-contract.md), with builder details in tools. |
| `other-examples/racer/docs/images/racer-gameplay.png` | Keep as example asset | Screenshot, not product guidance; leave with the racer example. |
| `other-examples/racer/docs/images/racer-lab.png` | Keep as example asset | Screenshot, not product guidance; leave with the racer example. |
