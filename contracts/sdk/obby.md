# Obby SDK v1

**Status:** Current contract

**Maturity:** Preview

The runtime owns physics, ladder volumes, checkpoints, fall detection, and
respawn. The helper keeps game-owned course status and routes the lifecycle
events to optional callbacks.

```luau
local CubaObby = require("@cubacadabra/obby")
local obby = CubaObby.create({
    onSpawn = function(api, event, state) end,
    onCheckpoint = function(api, event, state) end,
    onDeath = function(api, event, state) end,
    onRespawn = function(api, event, state) end,
})

function Game.on_player_event(api, event)
    obby:handle(api, event)
end

local status = obby:status()
```

Initial values are `checkpoint = "start"`, `deaths = 0`, and `state = "ready"`.
`handle` accepts `spawn`, `checkpoint`, `death`, and `respawn`, invokes the
matching callback if configured, publishes a live `__player_state` snapshot,
and returns whether it handled the event. Status returns `state`, `checkpoint`,
and `deaths`.

The snapshot contains `kind = "obby"`, checkpoint, deaths, and alive state. It
is ephemeral connection state, not a save file or trusted progression record.
