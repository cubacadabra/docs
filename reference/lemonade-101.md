# Lemonade 101

**Status:** Planned next gameplay milestone

**Owner:** `examples`, with platform work landing in the repository that owns
the missing capability

Lemonade 101 is the next small game milestone after the current imported-world
work. It deliberately exercises game behavior instead of another importer or
renderer stress case:

> Customers want lemonade. Make what they ask for. Serve them. Earn enough
> money before sunset and win.

## Why this game

Cubacadabra already has examples for exploration, survival, cooperative state,
and conformance. It does not yet have a tiny world where a player meets
characters, understands a request, performs a task, receives feedback, earns a
reward, and definitively wins. Lemonade 101 fills that gap with a three-minute
single-shift game rather than a persistent tycoon.

The first version stays intentionally small: a sunny park, one stand, four
stationary customers, ingredient stations, three recipes, and a `$30` goal.
Customers do not walk or pathfind initially. That keeps the first gameplay
test focused while making the missing authoritative actor capability visible.

## First playable loop

1. Start behind the stand with a three-minute shift and an empty cup.
2. Read the current customer's order.
3. Visit the lemon, sugar, and ice stations and use explicit context actions.
4. Return to the matching customer and serve the drink.
5. Correct recipes pay `$3` or `$4`, play obvious feedback, and advance the
   next order. Wrong recipes can be dumped and remade.
6. Serve ten customers, earning at least `$30`, or reach the end of the shift.
   Show `YOU WON` with a
   `Play Again` action, or `STAND CLOSED` with the score.

Initial recipes:

| Recipe | Lemons | Sugar | Ice |
| --- | ---: | ---: | :---: |
| Classic | 2 | 1 | no |
| Sweet | 1 | 2 | yes |
| Tart | 3 | 1 | no |

## Capability sequence

The game should be built by hitting the smallest platform wall and adding the
generic capability that clears it.

| Step | Capability | Owner / state |
| --- | --- | --- |
| 0 | Native park, stand, stations, customer zones, HUD, and Luau recipe loop | `examples`; started in `examples/lemonade-101` |
| 1 | Stationary world actors with stable id, name, position, yaw, and appearance | `rust` plus package/runtime contract; next |
| 2 | World-space names and compact order bubbles | shared runtime/renderer; next |
| 3 | Four recognizable customers with rotating orders | `examples`; after actors |
| 4 | Explicit context actions and creator-visible interaction inspection | runtime/Studio; the current slice uses HUD buttons |
| 5 | Intro/open/last-call/won/lost/results state machine and feedback pass | `examples`; initial open/won/lost slice is present |
| 6 | Moving queue and sidewalk waypoints | `rust`; only after stationary play is fun |
| 7 | Cooperative shared orders and trusted action authority | `rust`/`backend`/`examples`; no durable rewards yet |
| 8 | A second shift with one of three upgrades | `examples`; before considering persistence |

Game-specific order, inventory, cash, mistakes, timing, and win rules belong in
Luau. Rust should provide generic actor, interaction, UI, effect, and authority
seams rather than a `Customer` or `LemonadeStand` type.

## Current implementation boundary

The first source slice intentionally contains no imported assets and keeps its
world compact. The current package uses interaction zones and signs as
customer placeholders because `avatars.npcs` currently carries appearance
styles only, while local NPC simulation is disabled pending authoritative
world ownership. This is a deliberate diagnostic boundary, not the finished
game presentation.

Do not add RBXML, a giant GLB, terrain work, procedural crowds, pathfinding,
persistent economy, dialogue trees, a generalized crafting system, or a
generalized quest framework to this milestone.

## Acceptance test

Give the game to someone without explanation. Within roughly 30 seconds they
should understand that people want lemonade. Within a couple of minutes they
should serve someone successfully. Within one short session they should see an
unmistakable win or loss result and want to press `Play Again`.

This is a gameplay milestone. Screenshots, polygon counts, and import
percentages are supporting evidence, not the acceptance criterion.
