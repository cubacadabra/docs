# Decisions

These decisions are the load-bearing constraints behind the platform map:
inspectable authored data, game-specific Luau, shared Rust semantics where they
remove drift, and one canonical home for cross-repository documentation.

- [0001: JSON authored content](0001-json-authored-content.md)
- [0002: Luau game rules](0002-luau-game-rules.md)
- [0003: Shared Rust runtime semantics](0003-rust-shared-runtime.md)
- [0004: Central documentation](0004-central-canonical-documentation.md)

Each record identifies whether the decision is accepted or remains proposed.
An ADR describes why and what follows; its status is more authoritative than
the presence of an implementation prototype.
