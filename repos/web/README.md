# `cubacadabra/web`

**Owns:** the browser shell, DOM/HUD, input, networking adapter, and static
game-package hosting.

**Does not own:** simulation, Luau semantics, rendering semantics, or backend
world authority.

- Runs in: modern browsers; Rust is compiled to WebAssembly.
- Depends on: [Rust](../rust/README.md), game packages, and [backend](../backend/README.md).
- Used by: Web Player and the public developer distribution path.
- Read next: [Player/Web](../../products/player/web.md), [runtime](../../systems/runtime/overview.md), [package contract](../../contracts/game-package.md).
- Verify with: [host conformance](../../quality/compatibility/host-conformance.md).
- Incomplete: full parity evidence for every host boundary and release artifact.

Repository: [github.com/cubacadabra/web](https://github.com/cubacadabra/web)
