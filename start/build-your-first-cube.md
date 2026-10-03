# Build your first Cube

Start with [Cuboom](https://github.com/cubacadabra/examples/tree/main/cuboom),
the featured example. You can inspect its scene and Luau, build it, and open it
in Studio before changing anything.

## Build and preview

Follow the [local checkout instructions](../CONTRIBUTING.md#local-checkout),
then run these commands from the directory containing the sibling repositories:

```sh
cargo run --manifest-path tools/Cargo.toml --bin cubacadabra -- \
  build-game examples/cuboom --output examples/cuboom/build/package
cargo run --manifest-path studio/Cargo.toml -- --path examples/cuboom
```

Studio opens editable projects stopped. Use **Play** to enter the game and
**Stop** to return to editing. Move with WASD or arrows, jump with Space, and
run with Shift. Walk over a loose letter stroke to restore it to a cube.
The Play menu can start multiple local clients; shared game state requires a
reachable local backend.

Cuboom's package ID is currently `heavy2`. The folder name is an authoring
location; package IDs identify sessions and published content. Keep the ID
unchanged when following this example.

## Make a project of your own

Choose **File → New Project** in Studio, or use the same native project
generator from the terminal:

```sh
cargo run --manifest-path tools/Cargo.toml --bin cubacadabra -- \
  create-game --title "My Game" --path ./my-games
```

The generator reports the created project directory. Open that directory in
Studio. Edit the native `scene.json` and Luau source, save, and rebuild. Studio
and the CLI use the same builder; the resulting package is what Player hosts
load.

Read the [creator guide](../contracts/creator-guide.md) for the source/package
shape, then [world manifest](../contracts/world-manifest.md),
[Luau API](../contracts/luau-api.md), and [SDK modules](../contracts/sdk/README.md)
as you need them. Roblox import is partial: supported scene data can be
converted, while scripts and unsupported assets need review and adaptation.
See [Roblox interchange](../products/studio/roblox-project-interchange.md).

Publishing is a separate authenticated workflow. Local creation and preview
remain available without it. See [publishing](../systems/publishing/README.md).
