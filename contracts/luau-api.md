# Game-facing Luau API

**Status:** Current contract

**Maturity:** Preview

Game code is a Luau module that returns a table of lifecycle callbacks. The
shared runtime provides generic primitives; individual experiences define
their own rules and compose those primitives. Platform UI, credentials,
filesystem access, and transport objects are not exposed as game-owned APIs.

## Lobby, sessions, and interactions

```luau
api.lobby:set_enabled(false)
api.lobby:set_status("Find the three signal gates")
api.session:start("signal-run", { mode = "cooperative" })

local state = api.interactions:get_state()
local gate = state.zones["gate-a"]
```

`lobby:set_enabled` supplies an optional lobby override and
`lobby:set_status` changes the shared lobby status. `session:start` records a
named session request; options are reserved for future configuration.
Interaction state is generic and includes each zone's inside/nearby/player
state, kind, label, and event cursor. It does not introduce game-specific Rust
types for pickups, gates, doors, or checkpoints.

The public API is versioned through `manifest.sdkVersion`. The detailed
contracts are split by behavior:

- [Game lifecycle callbacks and event shapes](lifecycle.md).
- [World and manifest capabilities](world-manifest.md).
- [Retained in-game UI](ui.md), including document limits and pointer ABI.
- [Game network messages and retained state](network.md).
- [One-shot audio](audio.md).
- [World effects](effects.md).
- [Simulation-time tasks](tasks.md).
- [Engine snapshots and game save/restore hooks](snapshots.md).
- [SDK modules](sdk/README.md).

## Lifecycle and execution safety

The package lifecycle drives game callbacks such as start, tick, player,
interaction, network, and UI events. Exact callback payloads must remain
consistent across native and browser runtimes. Errors must be reported as
structured semantic diagnostics where possible; adapters may format text but
must preserve stable error classification and fields.

Every entry into game-owned code must be subject to the runtime's execution
budget, including module initialization, lifecycle callbacks, save/restore,
scheduled work, and future authority handlers. A scheduler budget alone is not
a complete sandbox budget. See the
[acceptance criteria](../verification/acceptance-criteria.md).

This page is the index, not a replacement for the normative per-API contracts.
