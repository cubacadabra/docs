# Cycle SDK v1

**Status:** Current contract

**Maturity:** Preview

`@cubacadabra/cycle` is a local deterministic day/night or other two-phase
clock. It advances from the simulation delta passed by the game; it does not
network or persist state by itself.

```luau
local CubaCycle = require("@cubacadabra/cycle")
local cycle = CubaCycle.create({
    daySeconds = 45,
    nightSeconds = 30,
    startDay = 1,
    startPhase = "day",
    onPhase = function(api, phase, day, cycle) end,
})

function Game.on_tick(api, delta_seconds)
    cycle:update(api, delta_seconds)
end
```

Non-positive or nonnumeric phase durations use the defaults (45 seconds day,
30 seconds night). The starting day is floored and at least 1; only exact
`"night"` selects night, otherwise it starts at day. `update` consumes
nonnegative simulation time, invokes `onPhase` at each transition, increments
the day after night ends, and returns whether at least one phase changed.
`status()` returns phase, day, elapsed, and remaining. `sync(phase, day,
elapsed)` selectively replaces valid values and does not emit `onPhase`.

When several players need one shared clock, the game must replicate and
validate phase state separately, for example through the cooperative
[shared-state SDK](shared-state.md). This helper alone is not authoritative.
