# `cubacadabra/rust`

**Owns:** platform-neutral simulation, movement, collision, Luau execution,
rendering, client session, and selected application state.

**Does not own:** host UI, credentials, device APIs, game-specific rules, or
backend persistence.

- Runs in: Studio directly; Web through WASM; iOS/Android through native bridges.
- Depends on: game packages, [tools](../tools/README.md) for build output.
- Used by: [Studio](../studio/README.md), [Web](../web/README.md),
  [iOS](../ios_app/README.md), [Android](../android_app/README.md), and [Desktop](../desktop/README.md).
- Read next: [runtime overview](../../systems/runtime/overview.md),
  [runtime decision](../../decisions/0003-rust-shared-runtime.md),
  [host conformance](../../quality/compatibility/host-conformance.md).
- Verify with: [testing](../../quality/verification/testing.md),
  [headless proof](../../quality/verification/headless.md), and [performance](../../quality/verification/performance.md).
- Incomplete: live trusted game authority and full cross-host behavioral proof; see the [roadmap](../../reference/roadmap.md).

Repository: [github.com/cubacadabra/rust](https://github.com/cubacadabra/rust)
