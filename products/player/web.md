# Player / Web

The browser host owns the page, HUD, input, networking adapter, and static
package hosting. Rust compiled to WebAssembly owns simulation, Luau, and the
shared renderer.

The public preview opens Cuboom by default (package ID `heavy2`). The browser
uses WebGPU or the renderer's WebGL fallback where available. Graphics startup
has a 30-second deadline; failure offers retry, the local Studio guide, and
downloads. An unavailable identity request falls back to guest play after
five seconds. These host behaviors do not establish browser/device rendering
parity; see the dated verification evidence for tested boundaries.

- Repository: [`cubacadabra/web`](../../repos/web/README.md)
- Canonical system docs: [runtime](../../systems/runtime/overview.md),
  [network](../../contracts/network.md)
- Verification: [host conformance](../../quality/compatibility/host-conformance.md)
