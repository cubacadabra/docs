# Products and platforms

See the [Player host map](player/README.md) for the implementation-facing view.

Cubacadabra has two product boundaries. **Studio** is creator software.
**Player** is end-user software. They share portable packages and Rust runtime
semantics, but a player does not open projects, edit assets, or expose build
machinery.

## Product definitions

### Cubacadabra Studio

Studio is the creator application for macOS, Windows, and Linux. It owns local
project authoring, asset import, package construction, diagnostics, and preview
workflows. Play mode embeds the real shared runtime so creators can test the
package boundary players will use.

The current Studio release publishes desktop artifacts for macOS arm64, Windows
x86_64, and Linux x86_64. Release support remains distinct from host-conformance
claims for every feature inside the application.

### Cubacadabra Player

Player is the end-user runtime application. It loads a catalog or portable game
package, restores account/product state through host-owned services, and runs
game sessions. It does not include Studio's editor, project store, asset
importer, or build UI.

Current player hosts are web, iOS, Android, and the native desktop Player for
macOS, Windows, and Linux. They reuse the shared Rust engine/client/app crates
through one desktop-player product boundary rather than turning Studio into
the way desktop users play.

## Target matrix

| Product | macOS | Windows | Linux | Web | iOS | Android |
| --- | --- | --- | --- | --- | --- | --- |
| Studio | Current | Current | Current | — | — | — |
| Player | Current | Current | Current | Current | Current | Current |

“Current” identifies an active product/host path in the checked-in architecture;
it does not by itself claim release readiness for every contract.

## Shared desktop architecture

Studio and Desktop Player are both native desktop hosts around shared Rust
crates, but their shells remain separate:

| Shared Rust runtime | Studio | Desktop Player |
| --- | --- | --- |
| engine, client, app state, renderer-facing semantics | editor, project store, build/import, diagnostics, test sessions | catalog/launch, account/settings, player shell, game sessions |

The Desktop Player implementation lives in the `desktop` repository. The
product boundary remains explicit so code organization does not imply that
creators and players use the same application.
