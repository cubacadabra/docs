# Player

Player is the end-user product: it loads a built Cube, presents it on a target
device, and connects to platform services through host-owned boundaries. It is
not Studio, even when both embed the shared Rust runtime.

| Host | Owns | Start here |
| --- | --- | --- |
| [Web](web.md) | browser shell, DOM/HUD, WASM boundary, package host | `cubacadabra/web` |
| [iOS](ios.md) | Swift lifecycle, touch, Metal view, native bridge | `cubacadabra/ios_app` |
| [Android](android.md) | Compose UI, lifecycle, JNI bridge, NDK integration | `cubacadabra/android_app` |
| [Desktop](desktop.md) | window, keyboard/mouse input, native player shell | `cubacadabra/desktop` |

All hosts depend on [Rust runtime](../../systems/runtime/overview.md), the
[package contract](../../contracts/game-package.md), and the applicable
[host-conformance checks](../../quality/compatibility/host-conformance.md).
