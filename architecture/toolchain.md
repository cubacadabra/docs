# Creator build toolchain

**Status:** Migration in progress

The `tools` repository owns project creation, source validation, SDK bundling,
and portable game-package construction. The package format and creator-facing
validation behavior are defined by the [game package contract](../contracts/game-package.md);
the implementation language is not part of that contract.

## Current state

The Python CLI remains the current implementation for the shared tools
commands. Studio already creates starter projects through native Rust code,
but its raw-project preview still invokes the shared `cubacadabra` builder. A
release Studio package currently carries `cubacadabra.pyz`, and the host uses
Python 3 to run it. Development checkouts can also fall back directly to
`../tools/src` when no CLI executable is available. `CUBACADABRA_CLI_PATH`
remains the diagnostic override for selecting a builder explicitly.

The migration has started in `tools` with Rust workspace scaffolding for
`cubacadabra-project`, `cubacadabra-builder`, and the `cubacadabra` CLI binary.
That scaffolding is not yet a replacement: the Rust crates do not currently
provide the complete command surface or the compatibility evidence required to
change the Studio release artifact.

## Target boundary

The Studio-required project and build path should be delivered as a native
`cubacadabra` executable built from `tools` Rust crates. Studio should resolve
that executable from its configured override or bundled resources, build a raw
project into a temporary package, and load the result through the existing Rust
runtime. The Studio release must not need a Python interpreter, a Python
zipapp, or `PYTHONPATH` for this path.

This is a toolchain implementation migration, not a change to game rules,
Luau SDK semantics, package layout, package hashes, or host runtime ownership.
Maintainer-facing commands such as uploads, local service setup, or asset
authoring helpers may remain Python until they have their own migration plan;
they must not be required by an installed Studio build.

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
