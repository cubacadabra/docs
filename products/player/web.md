# Player / Web

The browser host owns the page, HUD, input, networking adapter, and static
package hosting. Rust compiled to WebAssembly owns simulation, Luau, and the
shared renderer.

- Repository: [`cubacadabra/web`](../../repos/web/README.md)
- Canonical system docs: [runtime](../../systems/runtime/overview.md),
  [network](../../contracts/network.md)
- Verification: [host conformance](../../quality/compatibility/host-conformance.md)
