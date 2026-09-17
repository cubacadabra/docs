# Build your first Cube

Creators need only three layers to begin:

- [Creator guide](../contracts/creator-guide.md) — package shape and authoring rules.
- [Tools](../repos/tools/README.md) — the native builder and CLI entry points.
- [Game package contract](../contracts/game-package.md) — what hosts accept.

Then add the [world manifest](../contracts/world-manifest.md), [Luau API](../contracts/luau-api.md), and the focused [SDK modules](../contracts/sdk/README.md) as your game needs them.

The safe loop is local source → validate → build → run in Studio → load the
same package in Player. Publishing is a separate release boundary; see
[publishing](../systems/publishing/README.md).
