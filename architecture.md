# Architecture

## Repository map

The repositories are developed as siblings under `cubacadabra/`.

| Repository | Responsibility |
| --- | --- |
| [`rust`](https://github.com/cubacadabra/rust/blob/main/README.md) | Shared engine, simulation, renderer, Luau runtime, client runtime, app runtime, Morph types, and native/WASM bindings. |
| [`tools`](https://github.com/cubacadabra/tools/blob/main/README.md) | Python CLI, source project creation, package bundling/validation, example uploads, and Morph release tooling. |
| [`backend`](https://github.com/cubacadabra/backend/blob/main/README.md) | Cloudflare Worker HTTP APIs and world WebSockets backed by Durable Objects, D1, and R2. |
| [`web`](https://github.com/cubacadabra/web/blob/main/README.md) | Browser UI, input and transport adapters, static game-package host, and Rust/WASM runtime integration. |
| `ios_app` | SwiftUI shell, iOS services, and Rust C bridge. |
| `android_app` | Compose shell, Android services, and Rust JNI bridge. |
| [`studio`](https://github.com/cubacadabra/studio/blob/main/README.md) | Native Rust editor/desktop host using the Rust runtime directly. |
| `first-game`, `second-game`, `third-game`, `examples/` | Game source and reference packages; game rules remain game-owned. |

## Build and runtime flow

```text
manifest.json + src/main.luau + optional assets
                 │
                 ▼
       tools: validate and bundle
                 │
                 ▼
 package: manifest.json, game.luau,
          package.json, assets/
                 │
       ┌─────────┼───────────┬──────────┐
       ▼         ▼           ▼          ▼
     Studio     Web         iOS       Android
       └─────────┴───────────┴──────────┘
                  Rust runtime
```

The builder follows reachable static-string Luau `require()` calls, bundles
only the imported SDK helpers, checks package content, and emits hashes for
the packaged script, manifest, and assets. `.luaurc` supports editor
navigation/type checking; the builder resolves SDK modules from its canonical
toolchain. Source projects use `src/main.luau`; built packages use the bundled
entry `game.luau`.

When `src/server.luau` exists, the builder automatically bundles it separately
as `authority.luau` and records `package.authorityEntry` in the generated
manifest and package descriptor. Declaring an authority entry without that
source file is an error. This is a rules artifact for a trusted host, not a
secret and not part of the client game entry. See the
[builder implementation at the reviewed revision](https://github.com/cubacadabra/tools/blob/4c2c2f1683c7/src/cubacadabra/game_builder.py#L934-L950).

## Ownership boundaries

### Rust engine and game rules

Rust owns generic simulation, rendering, Luau hosting, engine state, runtime
limits, and cross-client game protocol. A game package owns its specific rules
and state transitions in Luau. The engine should understand generic concepts
such as transforms, interactions, effects, or properties, not the meaning of a
game’s “gate,” “spell,” or “inventory reward.”

The `DataModel` currently supplies a generic entity/property graph and a
bounded ordered mutation feed. Shared property metadata is consumed by
interaction validation and the Luau inspection API. This is an engine
substrate; it is not yet a complete Luau `Instance` system or a universal
renderer/physics/Studio reflection layer. See [the data-model note](https://github.com/cubacadabra/rust/blob/main/docs/data_model.md)
and [the first shared property schema](https://github.com/cubacadabra/rust/blob/main/docs/label-maker.md).

### Client and app state

`cubacadabra-client` owns the common game-session behavior: manifest/package
and script validation for a session, typed network decoding, route and session
identity, remote-player projection into the engine, and Luau network outbox
translation. Hosts own the actual WebSocket, package fetching/caching, input,
renderer surface, audio playback, app navigation, and operating-system UI.
See [the client contract](https://github.com/cubacadabra/rust/blob/main/docs/client-runtime.md).

`cubacadabra-app` is a sibling core for account and product state. It owns
portable validation, reducers, pending operations, request construction,
response decoding, and user-facing semantic status for migrated features.
Hosts execute HTTP effects with their own transport and credentials, then send
the result back to Rust. SwiftUI, Compose, and the DOM remain native
presentations. See [the app runtime](https://github.com/cubacadabra/rust/blob/main/docs/app-runtime.md).

### Host-specific responsibilities

- iOS, Android, and web keep access tokens/cookies, sign-in SDKs, navigation,
  keyboard/text input, and native/DOM presentation outside Rust snapshots.
- Studio calls Rust types and methods directly; it does not need to route
  in-process Rust work through JSON or FFI.
- Browser package hosting and native cache/download behavior are host concerns,
  but package content and runtime contracts must match.

## Multiplayer and authority

The current world service is a cooperative multiplayer coordinator, not a
trusted game simulation. Authority depends on the message:

| Data/action | What the server establishes | Remaining limit |
| --- | --- | --- |
| Socket identity and player presence | Server assigns identity and broadcasts membership. | Presence does not validate game outcomes. |
| Username, appearance, build requests | Backend validates and canonicalizes bounded requests. | Validation applies only to those request schemas. |
| Movement | World checks finite values, rate, respawn state, and a travel envelope, then broadcasts a canonicalized proposal. | It does not simulate world collision or prove the route was traversed. |
| `game_message` | World checks channel/JSON bounds and relays the payload. | Meaning remains client-owned. |
| `game_state_set` | World stores and broadcasts a retained value. | Sender proposes the value. |
| `game_state_compare_set` | World accepts a write only at the expected sequence and increments the sequence. | CAS prevents lost updates; it does not validate scores, inventory, or reward rules. |
| `__player_state` | World attaches player identity to live state. | Health/checkpoint values are client projections and explicitly non-authoritative. |

The shared-state SDK adds client-side queues, retries, and conflict rebasing on
top of CAS. It is suitable for cooperative state. A generic Rust authority
boundary and Luau rules adapter exist, and the builder can package their rules
entry. They are **not wired into the live Durable Object request path**. Do not
call the prototype production authority or use client movement as proof of an
interaction. See the [authority map](https://github.com/cubacadabra/rust/blob/main/docs/authority-map.md).

## State and persistence are separate

`EngineSnapshot` is a versioned engine freeze/restore format tied to package
and script content. It captures simulation state and an optional game-owned
JSON blob through `on_save` / `on_restore`. It is not a storage service: the
caller decides where snapshot bytes go. GPU resources, sockets, host caches,
remote presentation state, and Luau VM/coroutine internals are not included.
See [engine snapshots](https://github.com/cubacadabra/rust/blob/main/docs/snapshots.md).

Backend storage has distinct roles:

| System | Current role |
| --- | --- |
| One SQLite-backed Durable Object per live game instance | WebSocket membership, presence, and retained round/session channels. |
| WebSocket attachment and broadcast | Ephemeral player lifecycle values needed by currently connected peers. |
| D1 | Accounts, sessions, moderation, subscriptions, appearance records, and active Morph catalog metadata. |
| R2 | Immutable game packages and compiled Morph packs/media. |
| Queues | Deferred analytics or maintenance where asynchronous, at-least-once delivery is acceptable. |

Do not put movement or round synchronization through Queues. Current durable
player/game progression beyond account appearance is not a general creator API.
See [backend storage architecture](https://github.com/cubacadabra/backend/blob/main/docs/storage-architecture.md).

## File formats

| Purpose | Current representation |
| --- | --- |
| Authored package/world | JSON manifest and content declarations. |
| Game rules | Bundled Luau source. |
| Distribution | Package directory or ZIP with manifest, generated `game.luau`, `package.json`, and assets. |
| Running engine snapshot | Versioned JSON `EngineSnapshot`, stored only if its caller chooses. |
| Character/morph runtime asset | Custom `.morphpack`, current schema 5, compiled from source assets. |

There is no general-purpose binary scene/prefab format today. `.morphpack` is
not an `.rbxm` equivalent. MessagePack, FlatBuffers, and custom scene encodings
mentioned in idea documents are unselected future options; JSON remains the
current authored format. See [the current Morph pack contract](https://github.com/cubacadabra/rust/blob/main/docs/morph-pack-v5.md).
