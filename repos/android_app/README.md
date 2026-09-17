# `cubacadabra/android_app`

**Owns:** Kotlin/Compose presentation, lifecycle, input, JNI shim, and NDK
integration for the shared Rust engine.

**Does not own:** gameplay semantics, package format, or service authority.

- Runs in: Android devices and supported emulator ABIs.
- Depends on: [Rust](../rust/README.md), [backend](../backend/README.md), and game packages.
- Used by: Android Player.
- Read next: [Player/Android](../../products/player/android.md), [runtime](../../systems/runtime/overview.md), [package contract](../../contracts/game-package.md).
- Verify with: real Android checks in [host conformance](../../quality/compatibility/host-conformance.md).
- Incomplete: device-level host conformance beyond target compilation.

Repository: [github.com/cubacadabra/android_app](https://github.com/cubacadabra/android_app)
