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

Games using SDK `0.6.0` can replace the current world's runtime build blocks
with `api.world:set_build_blocks(blocks)`. Each block has a finite `position`
and positive `size` vector, an RGB integer `color` (`0xRRGGBB`), an
optional quarter-turn `rotation` from 0 to 3, and optional `collidable`
(defaults to `true`). The optional `outline` also defaults to `true`; set
`outline = false` when the game draws its own block edges or uses adjacent
blocks as one surface. Set `collidable = false` for decorative geometry such as
paint, borders, or lettering so it does not block players or pushable objects.
Set `attachedTo` to the ID of an authored pushable block when geometry should
move with it in the same collision step. The attached block still uses its
supplied world position; the engine applies push displacement to that position.
An empty list clears the blocks. The
operation accepts at most 2,048 blocks and replaces the previous list after
the script callback returns. Solid blocks render and collide through the same
runtime build-block path used by hosts. Games that use host-managed building
should not also replace that list from Luau. The list is local runtime state;
cooperative games must project it from shared game state on each client.

Game code can read `api.build_mode`, which is either `"DEBUG"` or `"RELEASE"`
and reflects the host runtime's compile profile. It is read-only; use it only
to expose development conveniences such as test controls. Release builds must
not rely on debug-only behavior being available.

## Package-world travel

The generic `api.world` travel API was introduced in SDK `0.5.0`. Bindings may
remain present in older test contexts, but published package content using this
contract should declare SDK `0.5.0`.

Game code can inspect and request travel among worlds already declared by the
loaded package:

```luau
local current_world = api.world:get_id()
api.world:enter("maze")
```

`world:get_id()` returns the active package world ID. `world:enter(world_id)`
accepts only an existing, non-empty package world ID and queues entry at that
world's authored spawn; it does not accept arbitrary coordinates. Empty or
unknown IDs raise a script error and do not change runtime state. A request is
consumed after the current script callback/tick returns, so entering a world
cannot recursively invoke its spawn callback. World entry uses the same
generic world/session notifications and input/velocity reset behavior as a
portal transition. The API is available with the same semantics in DEBUG and
RELEASE and through native and WASM Luau bindings.

DEBUG runtimes additionally expose `api.debug:teleport_to(world_id, position,
yaw)` for local development cheats. The API is absent from RELEASE runtimes
and must never be required by normal game logic.

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
[acceptance criteria](../quality/verification/acceptance-criteria.md).

This page is the index, not a replacement for the normative per-API contracts.
