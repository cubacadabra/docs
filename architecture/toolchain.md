# Creator build toolchain

**Status:** Core Studio migration landed; command-surface migration in progress

The `tools` repository owns project creation, source validation, SDK bundling,
and portable game-package construction. The package format and creator-facing
validation behavior are defined by the [game package contract](../contracts/game-package.md);
the implementation language is not part of that contract.

## Current state

The Rust workspace in `tools` now owns the canonical `cubacadabra-builder`,
`cubacadabra-project`, and native `cubacadabra` CLI crates. Studio calls the
builder library in-process. The Python implementation remains for commands
and the compatibility harness that have not yet moved into Rust; it is not
required by Studio or its release packaging.

The first migrated surface is the creator-critical path: native project
creation, source building, Luau dependency resolution, SDK bundling, package
metadata, asset copying, hashes, and guarded transactional output. The CLI
currently exposes `create-game` and `build-game`; maintainer-only upload,
local-service, and morph-release commands remain queued for their own Rust
library migrations.

## Target boundary

The Studio-required project and build path is delivered by the shared Rust
crates in `tools`. Studio builds a raw project into a temporary package and
loads the result through the existing Rust runtime. The Studio release does
not need a Python interpreter, a Python zipapp, or `PYTHONPATH` for this path.

This is a toolchain implementation migration, not a change to game rules,
Luau SDK semantics, package layout, package hashes, or host runtime ownership.
Maintainer-facing commands such as uploads, local service setup, asset
authoring helpers, and the compatibility harness may remain Python until they
have their own migration plan; they must not be required by an installed Studio
build.

## Completion evidence

The migration is complete for Studio only when all of the following are true:

- the native CLI preserves the current project/build command behavior and
  package-contract outputs, including validation failures and integrity data;
- the compatibility workflow builds representative projects from
  `first-game`, `second-game`, `third-game`, and `examples` with the native
  builder and compares the resulting package semantics;
- Studio's raw-project preview succeeds on macOS, Windows, and Linux on a
  clean machine with Python unavailable;
- Studio release archives contain the native builder and no
  `cubacadabra.pyz` dependency; and
- the old Python fallback is removed or explicitly isolated to development and
  migration diagnostics rather than the shipped Studio path.

See the [Studio overview](../studio/overview.md), [roadmap](../roadmap.md),
and [release-readiness checklist](../verification/release-readiness.md) for
the product and verification implications.
