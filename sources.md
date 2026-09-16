# Sources and resolved conflicts

## Scope reviewed

I reviewed the project-owned documentation under the sibling repositories:

- 23 Markdown files in `rust/docs/`
- 13 Markdown files in `tools/docs/`
- 2 Markdown files each in `backend/docs/` and `studio/docs/`
- 5 Markdown files in `ios_app/docs/`
- 2 Markdown files in `web/docs/`
- the 5 generated HTML pages in `developer/dist/docs/`
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
4. Generated public-site output, checked against its source and current
   implementation.

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

### `server.luau` has a package artifact, not live authority

[`tools/docs/server_side.md`](https://github.com/cubacadabra/tools/blob/main/docs/server_side.md) includes an older
statement that the server entry was not yet in the package builder. The
current builder and preview guide package `src/server.luau` as
`authority.luau`. The Rust boundary and server runtime are still prototypes;
the live Durable Object does not execute them. Package support must not be
reported as production authority.

### Current Cube upload exists, but full release management is incomplete

Older preview/roadmap text says there is no publishing/discovery product. The
current backend has authenticated `/cubes/upload`, versioned package storage,
catalog/list/detail APIs, and package launch/file delivery; the web client has
upload and browse flows. The remaining gap is a more complete draft/stage/
publish/rollback/visibility/release-selection workflow and richer discovery.
These statements refer to different levels of maturity, not a contradiction
about whether any upload endpoint exists.

### Morph format and D1 catalog

Earlier `morph_plan.md` work-log entries describe pack schemas 1–3 and refer to
catalog seeding in a migration number that is now used for a different
migration. The current pack contract is schema 5; rebuild older packs from
source. D1 stores an active JSON catalog document per channel plus separate
revisioned appearance rows, while R2 stores immutable SHA-addressed assets.
The old Morph area plan is useful for product intent, but its illustrative
slot-based `AppearanceSpec` is not the current Rust/backend V2 loadout
contract.

### Binary scene format proposals

[`big_direction.md`](https://github.com/cubacadabra/tools/blob/main/docs/big_direction.md),
[`right_for_2026.md`](https://github.com/cubacadabra/tools/blob/main/docs/right_for_2026.md), and
[`explain_5.md`](https://github.com/cubacadabra/tools/blob/main/docs/explain_5.md) explore competing binary options.
The implemented state is simpler: authored world/package definitions are
JSON, packages are directories or ZIPs, and `.morphpack` is a separate
character asset format. No general binary prefab format has been selected.

### Current character direction supersedes older visual metaphors

The active [art brief](https://github.com/cubacadabra/rust/blob/main/docs/character_art_direction.md) says the
“enchanted toy” construction is not a requirement and asks for a friendly
casual person whose appeal works without effects. Older `direction.md` and
`five_ideas.md` contain useful historical reasoning but should not override
that current brief. Visual approval remains open.

### Sharing product logic in Rust is an implemented direction, not a line-count promise

The iOS docs [`more_rust_idea.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea.md),
[`more_rust_idea2.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea2.md),
[`more_rust_idea3.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/more_rust_idea3.md),
[`rust_idea.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/rust_idea.md), and
[`https_calls.md`](https://github.com/cubacadabra/ios_app/blob/main/docs/https_calls.md) are architecture discussions
and point-in-time estimates. The current app-core behavior is described in
`rust/docs/app-runtime.md`: Rust shares semantic state and request/result
decisions, while each host executes transport and renders its own UI. Do not
carry forward historical line-savings or confidence percentages as current
metrics.

### Publishing a Morph to the community is not the same as importing one locally

The public developer-site pages in `developer/dist/docs/` are generated HTML,
not their source of truth. Their local GLB instructions match the current
Studio slice, but wording about an available authenticated community publish
action goes beyond the editor implementation. The Studio asset-flow document
still describes sharing as a future explicit action. Local import/add-to-game
works without an account; the current Morph CLI is a repository/operator
release path.

### Point-in-time reviews and brainstorms are not a live issue tracker

[`top_10_fixes.md`](https://github.com/cubacadabra/tools/blob/main/docs/top_10_fixes.md),
[`top_10_fixes_2nd_round.md`](https://github.com/cubacadabra/tools/blob/main/docs/top_10_fixes_2nd_round.md), and
[`bot_feedback.md`](https://github.com/cubacadabra/tools/blob/main/docs/bot_feedback.md) report code observations
from particular snapshots, some of which have since changed. For example,
shared state now documents distinct operation IDs and round/session expiry,
and the current web package loader supports local packages beyond the built-in
examples. Recheck an item against current code before reopening it as a bug.
The first review’s examples-license mismatch is also resolved in the checked-out
state: `examples/LICENSE`, its readme statement, and the current preview
licensing matrix use GPL-3.0-or-later.

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
