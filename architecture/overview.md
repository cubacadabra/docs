# Architecture overview

Cubacadabra is one cross-platform game platform split across repositories.
The Rust engine owns portable simulation and rendering-facing data; the game
package owns game-specific rules in Luau; hosts own operating-system
presentation, credentials, transports, and device integration; the backend
owns identity, routing, storage, and server-validated service behavior.

The product taxonomy is explicit: **Studio is creator software** and
**Cubacadabra Player is end-user software**. Studio can embed the runtime for
preview, but players do not use Studio. See the [product/platform model](../product/platforms.md).

**Cubacadabra at a glance**

```mermaid
flowchart LR
    Source["Creator/game source<br/>manifest, Luau, assets"]
    Tools["Build tooling<br/>validate and bundle"]
    Package["Portable game package<br/>versioned and hashed"]
    Runtime["Shared Rust runtime<br/>engine · client · app"]
    Studio["Creator application<br/>Cubacadabra Studio"]
    Player["Player applications<br/>Web · iOS · Android"]
    Desktop["Desktop Player<br/>macOS · Windows · Linux<br/>current"]
    Backend["Backend/platform services<br/>identity, routing, storage"]

    Source --> Tools --> Package --> Runtime
    Runtime --> Studio
    Runtime --> Player
    Runtime --> Desktop
    Studio <-->|"host-owned transport when used"| Backend
    Player <-->|"host-owned transport"| Backend
    Desktop <-->|"host-owned transport"| Backend
```

## Repository responsibilities

| Area | Owns | Does not own |
| --- | --- | --- |
| `rust` | Shared engine, client and application-runtime behavior, typed contracts, portable simulation | Product rules for an individual game; credentials or OS UI |
| `tools` | Project creation, SDK bundling, validation and package construction; native Rust CLI migration in progress | Runtime authority or host presentation |
| `studio` | Local authoring, preview, asset workflow and editor interactions | A separate interpretation of package validity |
| `backend` | Authentication, world routing, service validation, retained data and package delivery | Game-specific rules such as a particular score or gate |
| `web`, `ios_app`, `android_app` | Current Player host UI, device APIs, credentials, transport and platform decoding | Independent copies of shared gameplay or account decisions where Rust owns them |
| `desktop` | Native desktop Player shell and OS integration | Studio editor, project/build machinery, or a separate gameplay implementation |
| `docs` | Canonical hand-written platform docs, contracts, decisions, and verification criteria | Generated API output or executable fixtures |

**Runtime ownership layers**

```mermaid
flowchart TB
    Creator["Creator host<br/>Studio<br/>editor, project, build, preview"]
    Players["Player hosts<br/>Web, iOS, Android, Desktop"]
    App["cubacadabra-app<br/>portable account behavior"]
    Client["cubacadabra-client<br/>active game session behavior"]
    Engine["cubacadabra-engine<br/>simulation, DataModel, Luau runtime"]

    Creator -->|"preview package + editor actions"| App
    Creator -->|"package, input, and preview transport"| Client
    Players -->|"account actions and effects"| App
    Players -->|"package, input, and transport"| Client
    Client -->|"engine-facing session"| Engine
    Creator -->|"direct Rust / renderer APIs"| Engine
```

`cubacadabra-app` and `cubacadabra-client` are sibling semantic layers. Studio
and Player host bindings adapt them to each platform; they are not separate
implementations of Cubacadabra rules. The Desktop Player reuses the native Rust
boundary without reusing Studio's editor.

The creator build boundary is shared across the game repositories and Studio.
The Rust `tools` project/build crates are now the Studio implementation and the
native `cubacadabra` CLI is their command-line frontend. Python remains in
`tools` for maintainer commands and the compatibility harness that have not
moved yet; installed Studio does not depend on it. See the [creator build
toolchain](toolchain.md) for the migration boundary and remaining evidence.

## Important boundaries

- Game-specific nouns and rules stay in Luau. Rust exposes generic concepts
  shared across games.
- The backend may order and retain client-proposed values without validating
  whether the game rule was legitimate. See [authority](authority.md).
- Hosts adapt platform facilities to shared contracts. They must not create a
  second state machine for the same protocol. See
  [client runtime](client-runtime.md) and [application runtime](app-runtime.md).
- Authored source and immutable runtime assets are distinct. See
  [assets and prefabs](assets-and-prefabs.md) and the normative
  [MorphPack v5 contract](../contracts/morph-pack-v5.md).
- A tested prototype is not production integration. Status definitions are in
  the [documentation README](../README.md#documentation-authority).

## Current implementation boundaries

The shared Rust `DataModel` is a generic entity graph and ordered mutation
feed. It is a foundation, not yet a complete creator-facing `Instance` API or
renderer/physics/network/persistence bridge. The authority boundary and
`authority.luau` package entry are prototypes, not a live trusted two-player
execution path. Studio's local Morph import and preview work, while automatic
manifest wiring and reproducible cross-client use remain unfinished.

These boundaries are deliberately repeated on the specific pages where an
implementer needs them. The [roadmap](../roadmap.md) tracks the cross-platform
gaps.
