# Game lifecycle contract

**Status:** Current contract

**Maturity:** Preview

The source entry `src/main.luau` returns a table. The runtime invokes the
following callbacks when the corresponding event occurs:

```luau
local Game = {}

function Game.on_start(api) end
function Game.on_tick(api, delta_seconds) end
function Game.on_interaction(api, event) end
function Game.on_network_message(api, event) end
function Game.on_ui_event(api, event) end
function Game.on_launch(api, launch) end
function Game.on_player_event(api, event) end
function Game.on_save(api) return nil end
function Game.on_restore(api, state) end

return Game
```

`on_start` runs once after the package/script loads. Tick delta is simulation
elapsed seconds. The runtime execution budget and callback error behavior are
part of the [Luau API](luau-api.md) and
[task scheduler contract](tasks.md).

## World transition timing

`api.world:enter(world_id)` is a deferred script request. The runtime validates
the ID against the immutable world list from the loaded package, then consumes
at most one valid request after the current callback/tick finishes. Entry uses
the destination world's authored spawn and resets movement state safely. The
runtime emits the ordinary world/session transition notification and queues a
`player` `spawn` event for a later callback; it never calls a spawn callback
recursively from inside `world:enter`. A rejected ID raises a script error and
leaves the active world and player state unchanged.

## Event shapes

- **Interaction:** `id`, `phase` (`enter` or `exit`), `players`, and the
  interaction world `position` as three numbers.
- **UI:** `node_id`, `action`, and `phase`; sliders/toggles also include
  `value`. A consumed UI pointer must not also reach camera handling; see
  [UI](ui.md).
- **Launch:** `pad_id` and `player_ids`.
- **Player lifecycle:** `type = "player"` and `kind` of `spawn`,
  `checkpoint`, `damage`, `heal`, `death`, or `respawn`. Spawn, damage, heal,
  death, and respawn contain health, maxHealth, and deaths. Damage/heal also
  identify source and accumulated amount. Death includes cause (`fall` or a
  hazard ID).
- **Network:** game message/state or live player-state events; see
  [network](network.md) and the SDK lifecycle docs.

Player lifecycle events may be observed by multiple SDK helpers; handling one
must not prevent other subscribers from seeing it.

`on_save` must return a JSON-compatible value. `on_restore` receives that
value after snapshot compatibility validation and before restored runtime
state commits. See [snapshots](snapshots.md) for atomicity and conformance.
