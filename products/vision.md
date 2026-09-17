# Product vision

Cubacadabra is an open, portable platform for making and playing multiplayer
games. Creators should be able to keep their editable source, build locally,
and run the same game rules on supported clients. Players should get a coherent
experience across web, desktop, and mobile without each host redefining the
game.

That experience is delivered by two distinct products:

- **Cubacadabra Studio** is creator software for macOS, Windows, and Linux. It
  authors projects, builds packages, imports assets, and embeds the real runtime
  for preview and testing.
- **Cubacadabra Player** is end-user software with no authoring/editor
  machinery. Player targets are web, iOS, Android, and the native desktop
  Player for macOS, Windows, and Linux, separately from Studio.

See the [platform model](platforms.md) for the product/host matrix. Studio and
Desktop Player can both be Rust desktop hosts, but they are different products:
Player reuses the shared runtime, not the Studio editor.

The platform provides generic engine concepts and services. Creators own game
rules, content, and visual identity. Shared platform behavior should make
creator choices portable without turning the backend or engine into a catalog
of game-specific concepts.

This is a direction, not a claim that publishing, trusted competitive
authority, durable game databases, community asset distribution, or every
target host is complete. See [roadmap](../reference/roadmap.md).
