# Contributing to Cubacadabra

Start by running [Cuboom](https://github.com/cubacadabra/examples/tree/main/cuboom)
and reading the source behind something you would like to improve. We welcome
game development feedback, small fixes, documentation, art, and platform work.
The project is pre-launch; report rough edges with a reproducible example.

## Local checkout

Keep the repositories as siblings. The shell examples use a macOS/Linux shell
or Git Bash on Windows. The smallest checkout for the native
creator loop is:

```sh
mkdir cubacadabra
cd cubacadabra
for repo in docs rust tools examples studio; do
  git clone "https://github.com/cubacadabra/$repo.git"
done
cargo run --manifest-path tools/Cargo.toml --bin cubacadabra -- \
  build-game examples/cuboom --output examples/cuboom/build/package
cargo run --manifest-path studio/Cargo.toml -- --path examples/cuboom
```

Install a current stable Rust toolchain. See the
[Studio README](https://github.com/cubacadabra/studio#readme) for native build
prerequisites. This local build and single-player preview do not require a
cloud account, Python, or a paid subscription. Multiplayer presence and shared
state require a reachable backend; follow the
[backend README](https://github.com/cubacadabra/backend#readme) for local setup.

For browser or mobile work, also clone `backend`, `web`, and the host you are
changing (`ios`, `android`, or `desktop`). Their READMEs own platform setup.
`developer` presents the developer landing page and redirects; this repository
owns the documentation. `deployed` is generated distribution output.

## Choose the owner

| Change | Repository |
| --- | --- |
| Cuboom or another game's rules, scene, HUD, or artwork | `examples` |
| Simulation, Luau APIs, rendering semantics, shared session behavior | `rust` |
| Scene source, validation, package building, import/export tooling | `tools` |
| Explorer, Properties, picking, editing, preview workflows | `studio` |
| Browser, Swift, Kotlin, or desktop presentation and device integration | The matching player host |
| Authentication, storage, package delivery, service validation | `backend` |
| Cross-repository contracts, tutorials, product status | `docs` |

Read the matching [repository entry](repos/README.md) before changing a shared
boundary. Search sibling producers and consumers, and update the canonical
contract with the implementation. Game rules belong in Luau; hosts should not
invent a second interpretation of a package or runtime API.

## Send a useful change

- Open an issue in the repository that owns the problem. Include the host,
  revision, package/game ID, steps, expected behavior, and actual behavior.
  Screenshots help with visual issues; redact credentials and personal data.
- Keep pull requests focused. Explain the resulting behavior and include the
  command or device workflow used to verify it. State which hosts were not
  tested. A compile check alone does not prove a host workflow.
- Preserve stable source IDs and ordering. Edit source and regenerate output;
  do not patch hashed packages or `deployed` assets by hand. Keep checked-in
  JSON at or below 4,000,000 bytes per file.
- Keep new UI useful and proportionate. Hide unavailable actions or explain
  their limits close to the control; do not present mock data as working tools.
- Run the relevant local checks from the owning repository's README. For
  package changes, use the native builder and verify the built package.

Platform source and project-owned examples use **GPL-3.0-or-later**. Preserve
third-party attribution and asset notices. See
[licensing](systems/publishing/licensing.md) and each repository's `LICENSE`.
