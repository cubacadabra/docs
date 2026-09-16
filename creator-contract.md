# Creator contract

This is a concise cross-repository summary. The detailed API and examples live
in the [Developer Preview 0.3 guide](https://github.com/cubacadabra/tools/blob/main/docs/cubacadabra-game-developer-guide-preview-0.3.md)
and the SDK helper references in [`tools/docs`](https://github.com/cubacadabra/tools/tree/main/docs/).

## Source project and package

A source project conventionally contains:

```text
manifest.json
src/main.luau
assets/                 optional package-local content
effects.json            optional effect library source
```

The manifest identifies the game, content version, SDK contract, package
format, scene, and world(s). Current compatibility is:

| Field | Current contract |
| --- | --- |
| `id` | 3–64 lowercase letters/numbers separated by single dashes. |
| `version` | SemVer; legacy positive integer versions remain accepted. |
| `sdkVersion` | `0.3.0` or `0.4.0` when specified. Terrain requires `0.4.0`. |
| `package.formatVersion` | 3. |
| Source entry | `src/main.luau`, returning the game callback table. |
| Built client entry | `game.luau`. |
| Optional trusted-rules source | `src/server.luau`, bundled separately as `authority.luau`. |

The builder validates the manifest and assets, follows static string imports,
bundles reachable local and SDK modules, and writes `manifest.json`,
`game.luau`, `package.json`, plus packaged assets. The descriptor records file
hashes and which SDK modules/source hashes were included. Local module paths
must remain inside `src/`; dynamic/non-static `require()` is not supported as
a package dependency declaration.

Example build from the workspace root:

```sh
PYTHONPATH=tools/src python3 -m cubacadabra build-game first-game \
  --output /tmp/first-game-package
```

`package.json` checks establish consistency with the package descriptor; they
do not authenticate who published that descriptor. The exact package-loading
and cache behavior remains host-specific.

## Game lifecycle

`src/main.luau` returns a table. Supported optional callbacks are:

```luau
Game.on_start(api)
Game.on_tick(api, delta_seconds)
Game.on_interaction(api, event)
Game.on_network_message(api, event)
Game.on_ui_event(api, event)
Game.on_launch(api, launch)
Game.on_player_event(api, event)
```

Game logic stays in Luau. The engine provides generic primitives and bounded
events. Interaction IDs, game state schemas, and rules belong to the package.
Player lifecycle events expose runtime health/death/respawn projections, but
that does not make the game reward rules trusted by the server.

## Game-facing API

| API area | Use |
| --- | --- |
| `api.lobby`, `api.session` | Set optional lobby status/enabled behavior and request a named game session. |
| `api.interactions` | Read generic zones and their inside/nearby/player state. |
| `api.ui` | Install and mutate a retained in-game UI document; handle actions in `on_ui_event`. |
| `api.network` | Send ephemeral game messages or write retained game channels, including sequence-checked CAS. |
| `api.effects` | Change a declared interaction visual or play a bounded world-effect template. |
| `api.audio` | Request one-shot playback of a manifest-declared sound. |
| `api.task` | Schedule cooperative Luau work against fixed simulation ticks. |

The retained UI supports panels, stacks, text, buttons, menus, modals, toggles,
sliders, and joysticks. Platform shells keep account, payment, OS permission,
text entry, and navigation UI.

SDK helpers currently include:

- `@cubacadabra/shared-state` for cooperative retained-state updates.
- `@cubacadabra/obby` and `@cubacadabra/survival` for small lifecycle/status
  helpers over runtime physics/events.
- `@cubacadabra/cycle` for a local deterministic repeating cycle.
- `@cubacadabra/disclosure` for toggling authored UI details.

The game owns HUD composition, game copy, and game-specific rules. Helpers are
generic logic, not platform UI frameworks.

## Multiplayer state and its limits

`publish(channel, payload)` is ephemeral; players joining later do not receive
old messages. `set_state(channel, payload)` writes the latest retained value.
`compare_set_state(channel, expected_sequence, payload)` succeeds only when the
server sequence matches, then stores the payload at the next sequence. A
conflict returns the current snapshot so the SDK helper can rebase/retry.

The server bounds and orders messages, but accepts the client-authored meaning
of game state. A modified client can still propose an impossible score or
reward. The shared-state helper is for cooperative facts; it is not a secure
leaderboard, inventory, progression, or purchase authority.

The current helper supports both:

- **Coalescing intents**: “make this shared fact true,” such as completing a
  shared objective.
- **Distinct operations**: every operation matters, using a stable caller-made
  ID and an `operationStatus` check against accepted state.

Round/session-specific queues should use `intentExpired` so stale work does not
carry into a later round. Reducers must be deterministic, side-effect-free,
and return a new state. Trigger sound/effects/UI from accepted snapshots, not
while speculatively reducing an intent.

Live player status uses reserved `__player_state` messages and disappears with
the active WebSocket instance. Use retained game channels for compact shared
round facts; neither mechanism is durable player storage.

## Bounded runtime capabilities

- Game network messages are JSON, channels are 1–64 UTF-8 bytes, and complete
  messages are limited to 64 KiB.
- Game audio is one-shot package-local 48 kHz, 16-bit PCM WAV (mono or stereo),
  up to 64 files and 4 MiB per file. Music, looping, spatial audio, and mixer
  buses are not in this contract.
- Effects, templates, nodes, queued commands, and active one-shots are bounded;
  numeric values are clamped. Reduced-effects mode lowers visual movement
  without changing game state.
- `api.task` uses simulation time, not wall-clock sleeps. It caps task resumes
  per tick; a non-yieldable native call cannot be interrupted until Luau
  reaches a VM safepoint.
- Static terrain is a `0.4.0` package capability. Runtime terrain editing and
  saving edited terrain are not part of the preview contract.

Use the detailed owning references for exact per-field limits:
[network](https://github.com/cubacadabra/rust/blob/main/docs/network-runtime.md),
[UI](https://github.com/cubacadabra/rust/blob/main/docs/ui-runtime.md),
[effects](https://github.com/cubacadabra/rust/blob/main/docs/effects-runtime.md),
[audio](https://github.com/cubacadabra/rust/blob/main/docs/audio-runtime.md),
[task scheduling](https://github.com/cubacadabra/rust/blob/main/docs/task-scheduler.md), and
[shared state](https://github.com/cubacadabra/tools/blob/main/docs/shared-state-v1.md).

## Persistence and trust

An engine snapshot can resume compatible engine state and invoke explicit game
`on_save`/`on_restore` hooks. It has no built-in filesystem, D1, account, or
cloud persistence adapter. Persisting durable game progression requires a
separate trusted product contract.

The optional `authority.luau` entry is a prototype surface for a trusted host.
It is not executed by the live Durable Object. Until that integration exists,
use current network APIs only for cooperative play and do not promise
cheat-resistant outcomes.
