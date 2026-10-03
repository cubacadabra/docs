# Cubacadabra current state

Last updated: 2026-10-02

Cubacadabra is a pre-launch, GPL-3.0-or-later game platform. The public goal is
to make the source understandable, get creators into a local preview, and
invite useful contributions. A public code review does not imply a stable SDK
or a production-ready service.

## Start with Cuboom

[Cuboom](https://github.com/cubacadabra/examples/tree/main/cuboom) is the
featured game. Players collect loose letter strokes, restore a wall of
pushable cubes, and build the next layer together. Its source exercises native
scene authoring, physics, effects, cooperative state, touch controls, and
Studio's local multiplayer preview.

The source directory is `examples/cuboom`; its existing package ID is `heavy2`.
Keep that identity when building or loading it. The legacy schoolyard, relay,
and capability-probe games now live in `examples/first-game`,
`examples/second-game`, and `examples/third-game`. Their package IDs and hosted
`/games/<id>/` paths remain unchanged.

The first Web release packages Cuboom, Schoolyard, and Signal Run. Full local
Web builds include all examples. Maze and Vegas remain import/geometry
experiments; their large generated runtime JSON needs a different distribution
representation before it can be committed under the 4 MB file limit.

## Working foundations

- The native Rust CLI and Studio share project creation, validation, Luau
  bundling, and package construction. Package format 3 and SDK versions
  `0.3.0` through `0.6.0` have separate explicit contracts.
- Studio opens editable source, supports scene hierarchy and properties,
  grouping, selection and transforms, save/rebuild, undo, Play/Stop, and local
  multiplayer previews. World, Files, and Morphs are its available workspaces.
- Web, iOS, Android, and Desktop load portable packages through shared Rust
  simulation, Luau, rendering, and session code. Each host still needs its own
  behavioral and device evidence.
- The backend provides identity, package delivery, presence, and ordered
  cooperative retained state. Retained state does not enforce game rules.

## Help wanted

- Play and improve Cuboom: movement, physics, multiplayer convergence,
  onboarding, readable feedback, and touch controls.
- Make the local creator loop easier to reproduce on a clean machine.
- Complete project-local Morph assets through manifest, build, and host loading.
- Prove shared behavior at the real Web, Swift/C, and Kotlin/JNI boundaries.
- Integrate trusted game authority and durable game data before rewards or
  competitive progression depend on them.

See [contributing](CONTRIBUTING.md), the [roadmap](reference/roadmap.md), and
[release readiness](quality/verification/release-readiness.md) for ownership
and evidence. The [2026-10-02 public review record](quality/verification/public-review-2026-10-02.md)
lists the cleanup, verified boundaries, and remaining device checks.
Update this snapshot in place; Git history records older states.
