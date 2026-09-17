# 0002: Keep game-specific rules in Luau

- **Status:** Accepted architectural boundary
- **Decision date:** Current checked-in architecture; formal record added 2026-09-16

## Decision

Luau owns game-specific concepts and rules. Rust owns generic runtime concepts
that are shared by games. A trusted host may execute constrained game-owned
rules for authority, but those rules do not move into game-named Rust APIs.

## Rationale

Creators should be able to change game rules without rebuilding the shared
engine. The engine should not accumulate APIs such as `capture_gate` or
`finish_race` that only make sense to one game.

## Consequences

Rust may supply entities, transforms, physics facts, generic commands/events,
state storage, validation primitives, and execution budgets. Each game's
Luau decides what a validated action means. Current trusted execution remains
a prototype; see [authority](../systems/authority/overview.md).
