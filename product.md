# Product and current scope

## What Cubacadabra is

Cubacadabra is a code-first platform for making small, portable multiplayer
games. Creators write game rules in Luau, describe worlds and package metadata
in JSON, and use the shared Rust runtime across Studio and the web, iOS, and
Android clients. The current product strength is a short path from source to a
playable cooperative experience with predictable behavior across hosts.

The main examples show different parts of that contract:

| Project | Current role |
| --- | --- |
| `first-game` | Cooperative charm-collection game. |
| `second-game` | Signal Run relay race; demonstrates game-owned rules and retained shared state. |
| `third-game` | SDK capability and cross-feature probe. |
| `examples/the-wild-west` | Obstacle-course mechanics and Studio project workflow. |
| `examples/survival-101`, `examples/adventure-101` | Survival and generated-world capabilities. |

The full supported creator API is in the [Developer Preview 0.3 guide](https://github.com/cubacadabra/tools/blob/main/docs/cubacadabra-game-developer-guide-preview-0.3.md).

## What exists today

- The Python `cubacadabra` tools create projects and build portable game
  packages. Studio can create/open a project, edit supported world content,
  build and run it, and use the Morphs workspace.
- The Rust engine handles simulation, Luau execution, rendering, and bounded
  runtime APIs. A shared Rust client handles game-session protocol and state;
  a separate Rust app core handles account-facing state on web and native
  clients.
- The web client uses the shared runtime compiled to WebAssembly. iOS and
  Android use native shells and Rust bridges. Studio calls Rust directly.
- The backend supplies authentication and account APIs, moderation endpoints,
  subscriptions, and live world WebSockets. Durable Objects coordinate live
  world instances; D1 stores product data; R2 serves immutable content.
- Studio also has an optional Codex integration. It works against the open
  project source and keeps the native editor and game-building loop in Studio.

These are separate products and contracts: an account subscription is not a
game economy, a Morph asset catalog is not game discovery, and the existing
Cube upload/catalog path is a basic release flow rather than a complete
staging, rollback, visibility, and release-management system.

## Preview boundary

The current package format is version 3. The tools accept SDK contract
versions `0.3.0` and `0.4.0`; terrain is a `0.4.0` capability. The public
developer guide remains labeled Developer Preview 0.3 because that is the
preview release framing, not the full set of SDK versions accepted by the
builder.

Do not describe the platform as a stable `1.0.0` contract. Authenticated Cube
upload, latest-version listing/detail, and launch paths exist, alongside
example upload tooling. Full release management (draft/stage/rollback,
visibility and immutable version selection), richer discovery, trusted
multiplayer authority, and durable game-owned storage remain incomplete.
Studio is a real editor, but its current workbench and asset import paths do
not amount to Roblox Studio feature parity.

There is a community Morph asset catalog and an internal/operator release
workflow. The public developer-site text currently suggests an authenticated
creator-facing community publish action; the Studio asset-flow document still
describes that action as a target, and the editor code exposes local import and
pack export. Treat creator self-service Morph publishing as **not yet
available** until the product flow is implemented and documented in the
Studio source of truth.

## Product and visual direction

The short-term product fits small cooperative games and experiments. The
platform should make generic capabilities portable while leaving the game’s
theme and rules to its creators. Do not promise arbitrary trusted server code,
a full data-store API, public game discovery, a creator marketplace, or a
virtual economy as current creator features.

The active character direction is friendly, expressive people and creatures
with a soft-cube influence. Current art work focuses on one casual person.
That implementation is still a working study, not an approved visual style;
player preference has not been validated. “Enchanted toy” construction is no
longer a requirement. See [Character art direction](https://github.com/cubacadabra/rust/blob/main/docs/character_art_direction.md)
and [the person studies](https://github.com/cubacadabra/rust/blob/main/docs/art/person/README.md).

## Owner references

- [Tools README](https://github.com/cubacadabra/tools/blob/main/README.md)
- [Rust README](https://github.com/cubacadabra/rust/blob/main/README.md)
- [Studio README](https://github.com/cubacadabra/studio/blob/main/README.md)
- [Web README](https://github.com/cubacadabra/web/blob/main/README.md)
- [Developer site output](https://github.com/cubacadabra/developer/blob/main/dist/docs/index.html)
