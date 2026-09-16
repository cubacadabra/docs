# Create and build a game

**Status:** Current contract

**Maturity:** Preview

This is a practical entry point. Normative API details and limits live in the
linked contract pages; this guide is not a competing schema.

## Project shape

```text
my-game/
  manifest.json
  src/main.luau
  assets/                 optional local content
  effects.json            optional effect library source
```

Use Studio's **File → New Project** to create and open a starter project
without an external CLI or Python installation. The native `cubacadabra` CLI
in the `tools` repository uses the same Rust project and builder crates.

## Build from the native tools repository

```sh
cargo run --release --manifest-path Cargo.toml --bin cubacadabra -- \
  build-game --source /path/to/my-game --output /path/to/build/package
```

Add `--zip /path/to/package.zip` when an archive is needed. Directory and ZIP
outputs are not currently an atomic pair if a failure occurs between their
replacements. Keep the source project outside output paths.

The builder validates the manifest, resolves static-string `require()` calls,
bundles reachable game and SDK modules, copies declared/package assets, and
writes integrity metadata. Dynamic `require()` paths are not package
dependency declarations. `.luaurc` supports editor navigation/type checking;
the builder uses the canonical SDK shipped with its toolchain.

## Core loop

Return a table from `src/main.luau` and implement only the lifecycle callbacks
the game needs. Keep game-specific state transitions in Luau. Use generic
runtime APIs for interactions, UI, effects, audio, networking, and scheduled
work. See the [Luau API index](luau-api.md) and the detailed
[SDK contracts](sdk/).

## Before sharing a build

- Build from a clean source checkout using documented creator prerequisites.
- Include project-owned source assets and explicit runtime asset declarations.
- Validate the resulting package, not only the editor's source view.
- Pin dependencies and verify hashes before running a downloaded package.
- Do not treat cooperative retained state as trusted competitive game state.

Use [the package contract](game-package.md) for compatibility and authority
metadata, [network contract](network.md) for cooperative semantics, and
[publishing](../platform/publishing.md) for current distribution boundaries.
