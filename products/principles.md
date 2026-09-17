# Product and design principles

Each item is labeled **Established**, **Proposed**, or **Superseded**. These
labels describe design authority, not whether code implements the idea.

## Established

### Creator-owned, reproducible source

Game-authored material should be rebuildable from source and explicit pinned
dependencies on a clean supported machine. Runtime binaries are derived
artifacts. No platform account, private cloud asset ID, or maintainer-local
environment should be a hidden requirement for local creation and preview.

**Prevents:** projects that stop building when an account, asset URL, local
cache, or maintainer checkout disappears. **Test:** build and preview from a
clean checkout with only documented creator prerequisites.

### Generic engine, game-owned rules

Rust owns concepts every game shares, such as entities, transforms, meshes,
colliders, properties, state changes, and platform-neutral runtime behavior.
Luau owns game-specific concepts and transitions such as gates, captures,
scores, rounds, and inventory rules.

**Prevents:** game-specific rule growth inside the engine and forced engine
releases for creator rule changes. **Test:** add a game-specific mechanic in
Luau using generic engine facilities without adding a game-named Rust API.

## Proposed

### One mutation path for editing and runtime consumers

**Status: Proposed.**

Luau, manual Studio edits, and future AI-assisted edits should converge on a
validated, observable mutation/command model. Renderer, physics, networking,
persistence, undo, hot reload, and inspectors should consume coherent changes
from that model rather than introducing parallel setters or per-frame scans.

**Prevents:** different tools producing conflicting state, changes that cannot
be undone, and subsystems missing updates. **Test:** the same property edit
from script and Studio reaches the same validation/change feed and undo path.

### Explicit, safe import

**Status: Proposed.**

Parsing content must not execute scripts. Unsupported components and missing
dependencies must produce actionable reports; supported round trips must
preserve semantics and identity/reference relationships.

**Prevents:** silent data loss, dependency surprises, and code execution during
asset inspection. **Test:** import unknown components, missing assets, nested
object references, and attached scripts; assert explicit errors, correct
reference remapping, and no script side effects.

### Product policies needing owner confirmation

### Monetization boundaries

**Status: Proposed for owner confirmation.**

The pricing brainstorm proposes free creation and publishing, no advertising,
no paid discovery placement, no artificial in-game currency as a required
platform mechanic, and charging for professional tools/services or optional
parent-facing features rather than making children the product being
monetized. These are product-policy proposals, not approved public promises.

Exact prices, quotas, and subscription tiers in the source discussion are
discarded from the canonical contract because they were speculative and may
change. An owner should explicitly accept, revise, or reject the principles
before they become public commitments.

### Fast visual iteration

**Status: Proposed.**

Art parameters that creators tune frequently should be data-driven and reload
without rebuilding the Rust engine where practical. This does not select a
particular file format or require a generalized hot-reload system.

**Test:** change an authored visual parameter and observe the preview update
without compiling Rust; measure where a code rebuild remains necessary.

## Superseded

### Mandatory enchanted-toy construction

**Status: Superseded.**

Older character direction treated visible assembly and “enchanted toy”
construction as requirements. The current art direction explicitly removes
those requirements: clothing and anatomy should connect naturally, and a plain
character should work with effects disabled. See
[character direction](characters/art-direction.md).

### MessagePack as a selected scene format

**Status: Superseded as a proposal.**

MessagePack and other binary counterparts were suggestions only. No general
binary authored scene/prefab format is selected; JSON remains the current
format. See [decision 0001](../decisions/0001-json-authored-content.md).

## Historical principles that remain useful as constraints

The exact proposal documents and issue snapshots are tracked in
[the source ledger](../reference/migration-sources.md). The enduring acceptance tests are in
[verification/acceptance-criteria.md](../quality/verification/acceptance-criteria.md).
