# `cubacadabra/tools`

**Owns:** the native Rust project and package builder, creator CLI, validation,
and package diagnostics.

**Does not own:** runtime semantics, host presentation, or backend publishing.

- Runs in: local creator and CI environments; Studio calls the builder in-process.
- Depends on: [Rust](../rust/README.md) and the package contracts.
- Used by: [Studio](../studio/README.md), game-package repositories, and Player build workflows.
- Read next: [toolchain](../../systems/toolchain/overview.md),
  [creator guide](../../contracts/creator-guide.md), [game package](../../contracts/game-package.md).
- Verify with: package fixtures and [acceptance criteria](../../quality/verification/acceptance-criteria.md).
- Incomplete: maintainer-only upload, local-service, and Morph-release commands still use legacy Python paths.

Repository: [github.com/cubacadabra/tools](https://github.com/cubacadabra/tools)
