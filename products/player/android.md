# Player / Android

The Android host owns Kotlin/Compose presentation, lifecycle, JNI integration,
and device input. Gradle builds the Rust `cdylib` for the supported Android
ABIs; the package and simulation rules stay portable.

- Repository: [`cubacadabra/android`](../../repos/android/README.md)
- Canonical system docs: [runtime](../../systems/runtime/overview.md),
  [package contract](../../contracts/game-package.md)
- Verification: [host conformance](../../quality/compatibility/host-conformance.md)
