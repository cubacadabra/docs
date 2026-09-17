# Player / iOS

The iOS host owns Swift lifecycle and presentation concerns, touch input,
Metal view integration, credentials, and the Rust C bridge. Gameplay semantics
remain in the shared runtime and package.

- Repository: [`cubacadabra/ios_app`](../../repos/ios_app/README.md)
- Canonical system docs: [runtime](../../systems/runtime/overview.md),
  [authentication](../../systems/backend/authentication.md)
- Verification: [host conformance](../../quality/compatibility/host-conformance.md)
