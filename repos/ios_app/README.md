# `cubacadabra/ios_app`

**Owns:** Swift/iOS lifecycle, touch input, Metal view integration, credentials,
networking, and the Rust native bridge.

**Does not own:** gameplay rules, package validation semantics, or shared state meaning.

- Runs in: iOS devices and simulators supported by the app.
- Depends on: [Rust](../rust/README.md), published packages, and [backend](../backend/README.md).
- Used by: iOS Player.
- Read next: [Player/iOS](../../products/player/ios.md), [runtime](../../systems/runtime/overview.md), [authentication](../../systems/backend/authentication.md).
- Verify with: real host checks in [host conformance](../../quality/compatibility/host-conformance.md).
- Incomplete: device-level proof for full package, asset, and network parity.

Repository: [github.com/cubacadabra/ios_app](https://github.com/cubacadabra/ios_app)
