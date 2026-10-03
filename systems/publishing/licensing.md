# Cubacadabra preview licensing

**Status:** current preview repository reuse policy summary; check individual dependency notices and release obligations.

This is the current repository policy for the developer preview. It is a
project policy summary, not legal advice.

| Material | Current license or obligation |
| --- | --- |
| Platform repositories, including tools, Rust, Studio, all Player hosts, backend, developer site, documentation, and project-owned font source | GPL-3.0-or-later unless a file or dependency carries its own notice. |
| Example game source and artwork | GPL-3.0-or-later; see the example repository `LICENSE`. |
| SDK helpers copied into a generated game package | GPL-3.0-or-later because the builder incorporates their source into `game.luau`. |
| A creator's original game code and artwork | The creator should choose and publish a license for that material; the SDK license still applies to copied SDK source. |

The examples README and `examples/LICENSE` are aligned on GPL-3.0-or-later.
Third-party assets retain their own notices, including Maze 101's MIT-licensed
source artwork. Consolidating example repositories does not remove those notices.
The shared renderer embeds Lilita One and Roboto Condensed under SIL OFL 1.1.
Web normalization, native release packaging, and mobile bundle generation copy
their notices from `rust/assets/fonts` into the output's `licenses/` directory.
The separately distributed Cubacadabra font retains its own OFL notice alongside
the GPL license for its creation source.
Before encouraging redistribution of generated packages, add the applicable
license and attribution notices to the package distribution workflow and keep
those notices alongside the release artifact.
