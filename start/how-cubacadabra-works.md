# How Cubacadabra works

Cubacadabra separates portable game meaning from the host that presents it.

1. **Studio and tools** author JSON, Luau, and assets locally.
2. **The build boundary** validates those sources and produces an immutable,
   hashed [Cube package](../contracts/game-package.md).
3. **Rust** owns shared simulation, Luau execution, rendering, client session,
   and selected application state.
4. **Player hosts** own touch, windowing, credentials, transport, and device
   APIs on [Web, iOS, Android, and Desktop](../products/player/README.md).
5. **Platform services** coordinate live worlds, authentication, publishing,
   durable records, and moderation.

![Cubacadabra platform overview](../media/diagrams/platform-overview.svg)

The important boundary is the package: game-specific rules stay in the game
package, shared semantics stay in Rust, and a host cannot silently reinterpret
the artifact. Read the [runtime overview](../systems/runtime/overview.md) and
the [package contract](../contracts/game-package.md) for exact behavior.
