# `cubacadabra/examples`

**Owns:** the collection of self-contained example games and their content
source. It demonstrates platform features without moving game rules into Rust.

**Does not own:** the shared engine, builder, or host adapters.

- Runs in: the package builder and any Player host.
- Depends on: [tools](../tools/README.md) and [Rust](../rust/README.md) through the package contract.
- Used by: creators, compatibility checks, and product evidence.
- Featured game: [Cuboom](https://github.com/cubacadabra/examples/tree/main/cuboom); start here for gameplay and creator-workflow contributions.
- Also owns: the former `first-game`, `second-game`, and `third-game` sources; their package IDs are unchanged.
- Read next: [creator guide](../../contracts/creator-guide.md), [game package](../../contracts/game-package.md), [SDK contracts](../../contracts/sdk/README.md).
- Verify with: package builds and [headless proof](../../quality/verification/headless.md).
- Incomplete: examples remain demonstrations, not a claim of full production release coverage.

Repository: [github.com/cubacadabra/examples](https://github.com/cubacadabra/examples)
