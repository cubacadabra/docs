# Roadmap and open work

This is a current cross-repository gap list, not a schedule, release promise,
or requirement to implement every proposal in the historical source material.
Feature terms and evidence labels follow the
[documentation authority rules](README.md#documentation-authority).

**Major unfinished platform areas**

```mermaid
flowchart TB
    Authority["Trusted authority"] --> Readiness["Cross-platform release readiness"]
    Durable["Durable game-owned data"] --> Readiness
    Releases["Transactional releases"] --> Readiness
    Assets["End-to-end asset integration"] --> Readiness
    Hosts["Host conformance"] --> Readiness
    Editing["Shared editing pipeline"] --> Readiness
    Safety["Measured safety and<br/>performance budgets"] --> Readiness
    Avatar["Shared avatar editor"] --> Readiness
```

This is a gap map, not a schedule or an assertion that the areas can be
completed independently. The sections below define their current foundations
and remaining evidence.

## Working foundations

- The tools builder produces package format 3 and accepts SDK `0.3.0` and
  `0.4.0`; terrain requires `0.4.0`. Packages include generated Luau and
  integrity metadata. See [package contract](contracts/game-package.md).
- Rust provides shared engine, client/session, application-state, and bounded
  Luau runtime foundations. Web uses generated WASM; iOS and Android use
  native bridges; Studio calls Rust directly.
- The network service provides server-assigned presence, validated service
  requests, and ordered cooperative retained state. Compare-and-set prevents
  lost writes; it does not validate game-rule meaning.
- Studio creates local projects and imports/validates/previews supported GLB
  assets. Project-local catalog update, manifest declarations, and
  reproducible package use on every client are not yet one integrated path.
- SDK helpers cover cooperative shared state, obby and survival lifecycle,
  disclosure, and a local two-phase cycle. Exact behavior lives in
  [SDK contracts](contracts/sdk/README.md).
- Engine snapshots, deterministic headless runs, bounded UI/effects/audio,
  simulation-time tasks, static terrain, package assets, and MorphPack v5
  have explicit contracts.

## Open work

### 1. Integrate trusted game authority

The Rust `AuthorityBoundary`, Luau adapter, portable server runtime, and
`authority.luau` artifact are prototypes. The live Durable Object does not yet
execute game-owned rules. Production authority needs authenticated actor
binding, trustworthy world/movement facts, bounded game-owned execution,
atomic persistence of accepted state and request receipts, and publication
only after commit. Client-reported movement is not collision evidence. Test
every alternate mutation route for bypasses before protecting rewards.

### 2. Define durable game-owned data

Engine snapshots represent an in-memory running world and optional explicit
game state; they are not a creator database. Durable inventory, progression,
and rewards need ownership/access rules, schema migrations, quotas,
concurrency, reconnect/restart, deletion, recovery, and transactional writes.

### 3. Make build and release activation transactional

The tools builder stages directory output and preserves an earlier successful
package when a build fails. Directory and ZIP outputs are not one atomic
transaction. Hosts validate different portions of package contents and retain
different caches. Stage and verify every required asset, then activate one
immutable package revision. Interruption tests must leave a complete old or
new release, never a mixed set; see
[acceptance criteria](verification/acceptance-criteria.md).

### 4. Complete the remaining native tools command surface

The creator-critical Rust project and builder crates are now implemented, and
Studio uses the builder in-process. Studio release artifacts ship a native
`cubacadabra` builder without Python or `cubacadabra.pyz`. The Python CLI still
provides maintainer-only upload, local-service, and Morph-release commands, and
the compatibility harness still uses its legacy builder module. Migrate those
workflows only where a native path is needed, while preserving the shared
package contract and diagnostics. See the [creator build toolchain](architecture/toolchain.md).

### 5. Finish local Morph asset integration

Studio imports and locally previews supported rigid-wearable GLBs, writes the
source/sidecar/pack/thumbnail, updates the local catalog, and registers the
pack with its renderer. The action does not currently wire the asset into
`manifest.assets.morphPacks`. Prove manifest wiring, package hashes, and the
same asset loading on Studio, web, iOS, and Android. Creator-facing community
publish remains an operator-managed release path, not a self-service Studio
feature.

### 6. Prove host behavioral conformance

Keep native Rust and browser Luau outcomes equivalent and exercise real web,
iOS Swift/C, Android JNI/Kotlin, and Studio loader/cache boundaries. Compare
callback order, module cache behavior, task scheduling, JSON conversion,
structured failures, SDK transitions, and asset loading. Rust target
compilation is not an Android device test. See
[host conformance](compatibility/host-conformance.md).

### 7. Complete the shared editing pipeline

The generic `DataModel` currently supplies a stable entity graph and ordered
mutation feed; it is not yet a Luau `Instance` surface or connected to every
consumer. Manual Studio edits, Luau, and future AI edits should converge on
shared validation, changes, preview, undo, and hot reload. See the proposed
[editing model](studio/editing-model.md).

### 8. Set measured service, safety, and performance budgets

Choose targets from real measurements for package startup, asset decode,
memory, frame time, network traffic, concurrent sessions, and long sessions.
Define public-content permissions, review, reporting, takedown/appeal,
privacy/data deletion, resource limits, and support operations before broad
public creator distribution. Current block/report endpoints do not complete
that policy.

### 9. Deliver the shared avatar editor surface

The backend catalog and revision-checked saved-appearance paths are current
contracts. The standalone editor remains proposed until web, iOS, and Android
prove the same Rust composition, local preview events, catalog browsing, and
save-conflict handling at their real host boundaries. Follow the target
ownership and event seam in [the avatar editor architecture](architecture/avatar-editor.md).

### 10. Close the release-readiness gate

The proposed production checks in [release readiness](verification/release-readiness.md)
need owners, thresholds, and repeatable evidence before a stable SDK release
can be claimed. This includes authenticated soak and malformed-message tests,
host and accessibility conformance, permissions, observability, and measured
performance budgets.

## Open decisions

- Whether a general-purpose scene/prefab encoding needs a binary form. JSON is
  current; identity and reference requirements apply regardless of encoding.
- Whether trusted game rules first run in a Worker/WASM Durable Object or a
  separate host. The generic command boundary is independent of deployment.
- How far more application state should move into shared Rust. Share semantic
  decisions where it removes real drift; keep OS UI and accessibility in hosts.
- Whether to adopt the pricing principles in
  [product principles](product/principles.md). Exact price tables remain
  discarded speculation, not commitments.
- Which platform-facing AI editing integration to use. The durable requirement
  is one validated editor pipeline; Codex/App Server details in old notes are
  not a current product or dependency decision.

No release date, SDK 1.0 gate, or pricing tier is established by historical
plans.
