# Public source review — 2026-10-02

**Status:** Local verification record

**Maturity:** Preview

This cleanup prepares the source for public review and contributions. It does
not declare a stable SDK or approve a production launch. Every active sibling
repository was inventoried; code review focused on creator entry points,
package construction, host consumers, available Studio workflows, licensing,
documentation, and release preparation. This was not an exhaustive audit of
every line or a security assessment.

## Resulting source layout

`examples` now owns all editable example games. The former `first-game`,
`second-game`, and `third-game` sources live under that repository, with their
package IDs, asset bytes, and hosted paths preserved. Native host build inputs,
catalogs, conformance checks, and reusable release workflows follow the new
locations. Complete original checkouts and verified Git bundles were retained
outside the working checkout before the old local directories were removed.
Remote repository retirement is a separate operation.

[Cuboom](https://github.com/cubacadabra/examples/tree/main/cuboom) is the
featured game and default player choice. Its package ID remains `heavy2`; its
display title is Cuboom. It has a short authored goal and progress HUD, a
gameplay camera preference, and a README with build instructions, known limits,
and contribution priorities.

| Repository | Cleanup scope |
| --- | --- |
| `docs` | Canonical pre-launch scope, contributor setup, ownership map, current versus proposed Studio workflows, and collision-source contract |
| `.github` (`dot-github` locally) | Organization profile, full checkout instructions, contribution entry point, and pull-request template |
| `examples` | Three consolidated games, Cuboom entry point and HUD, explicit experiment status, and bounded Maze collision-source shards |
| `tools` | One native builder entry point for hosts, all-example conformance, collision split/merge commands, actual host paths, upload guards, source hygiene check, and release consumers |
| `rust` | Current workspace/host documentation, GPL metadata, lockfile-matched WASM tooling, feature-gated test/showcase helpers, and fixture tests aligned with built source; shared runtime behavior preserved |
| `studio` | Removed dormant mock Assets/Materials/Test panels; retained World/Files/Morphs; clarified local Morph limits and labeled Room Video experimental in menus and its dialog |
| `desktop` | Bundled sources from examples, Cuboom first, compact example list, and current release inputs |
| `ios` | Native build phase and four bundled projects from examples; shared catalog default is Cuboom |
| `android` | Matching source paths and catalog default; manifest download limit aligned with the current package limit |
| `web` | Practical developer guide, compact navigation, current source links, Cuboom catalog/default, bounded graphics startup, empty sign-in credentials, featured release profile, and reviewable deployment preparation |
| `backend` | Current ownership/scope documentation, GPL notices, and local checks in CI; service behavior unchanged |
| `developer` | Small resource gateway and legacy redirects to canonical docs; local static check and CI |
| `font` | GPL creation-source/OFL font distinction and regenerated 0.1.1 archive including both licenses; glyphs and metrics preserved |
| `deployed` | GPL notices and generated-output instructions; existing published runtime bytes preserved |

The `developer` site presents links and setup entry points. It no longer
competes with `docs` as a hand-written contract corpus. Existing implementation
repositories' historical documentation directories remain intact.

## Package and source evidence

All eleven examples were built with the native CLI, loaded through the native
Rust client and actual generated browser WASM, and validated as raw Studio
projects. The shared scripted native/browser behavior trace matched. This
checks package and runtime boundaries; it does not prove GPU rendering,
physical input, or every device adapter.

Maze's former 18.2 MB authoring collision JSON became an ordered index and five
source shards, each at most 4,000,000 bytes. All 186,622 triangles retained
their original values and order. The builder expands the source index into
the existing inline runtime representation. Tests cover ordered merging,
rounding validation, duplicate/nested references, traversal, symlink escape,
relative CLI paths, and preserving prior output on validation failure.

The public Web build includes Cuboom, Schoolyard, and Signal Run. Its six JSON
files are below the limit; the largest is under 100 KB. GPL and embedded-runtime
font notices are included.
Full development builds still include geometry/import experiments. Maze and
Vegas generate large inline runtime manifests and need a different
distribution representation before those outputs can be committed. The
unchanged historical `deployed` artifacts were not patched or republished.

## Verification completed locally

| Boundary | Evidence |
| --- | --- |
| Tools native workspace | 95 Rust tests passed |
| Maintainer Python tooling | 67 tests passed, including all-example built-package checks and uploads against an isolated local HTTP fixture |
| Shared Rust workspace | 253 library tests passed; seven package-dependent tests skipped in the normal headless run |
| Real Maze collision package | Opt-in bridge-walk check passed against native-built Maze output |
| Studio | 112 tests passed; two GPU-dependent tests skipped in the unit run, with separate real GPU probes below |
| Studio native GPU | Cuboom gameplay and stopped review captures; orbit, pan, zoom, reset, and unchanged gameplay camera assertions passed; experimental Room Video native menu dispatch and dialog probe passed |
| Studio local multiplayer | Nine local clients connected to an isolated local Worker; repeated player swaps, stable preview slots, input routing, and idle control checks passed |
| Desktop | Eight tests passed; macOS default-startup smoke loaded Cuboom, initialized the Metal renderer, and connected to the local backend |
| iOS | Generic iOS Simulator Debug Xcode build succeeded, including Rust bridges, four native-built example bundles, and unchanged font notices |
| Android source consumers | All eleven static world-model host checks passed across the workspace; matching game sources were built through the native builder |
| Backend | Generated binding check, strict TypeScript check, and 29 tests passed |
| Web application WASM | 18 shared scenarios and production account-adapter lifecycle checks passed |
| Web startup/deployment | Four graphics startup lifecycle tests and three local deployment preparation tests passed |
| Web release artifact | Release WASM build, Vite build, featured normalization, and actual WASM loading of all three featured packages passed |
| WASM tool setup | Missing or mismatched binding CLI fails before compilation with the version from the Rust lockfile; actual matching release build passed |
| Web developer surfaces | Both developer entry points checked in WebKit at 390×844, 768×1024, 1280×800, and 1440×900; no document horizontal overflow; copy-command feedback exercised |
| Web failure UI | Invalid-game startup exercised in the real DOM; retry, Studio guide, and download controls present with 44 px targets |
| Standalone developer site | Two pages and fifteen canonical redirects passed the static check |
| Font | TTF/WOFF2 coverage, all 26 authored letter shapes, FreeType rendering, OpenType/CoreText shaping, archive checksums, and included license checks passed; original glyph outlines/mappings/metrics matched |
| Source hygiene | Active-repository license, canonical link, retired game link, tracked credential filename, changed JSON-size, formatting, and whitespace checks passed |

The native framebuffer probes use production renderer/UI code but do not prove
OS event delivery or physical trackpad behavior. The short multiplayer probe
does not establish full Cuboom progression, reconnect convergence, or a soak
budget. The iOS build does not establish simulator/device interaction.
Native release workflow changes were syntax-checked locally; remote GitHub CI,
signing, notarization, and publication were not run. Development-only showcase
builds still have compiler warnings; this cleanup keeps their helpers outside
ordinary native runtime builds.

## Remaining launch evidence

- Verify real browser graphics and gameplay on the supported browser/device
  matrix. Local WebKit reached the ready state but captured a blank canvas;
  investigate rendering versus capture support. Successful WASM package loading
  is a narrower result.
- Run Android Studio builds and device checks. Repository instructions prohibit
  agent-driven Gradle/ADB runs; neither was performed here.
- Run actual iOS device play and Desktop player workflows on macOS, Windows,
  and Linux. Native host compilation and Studio captures are separate evidence.
- Exercise Cuboom's full cooperative progression, competing pickups, late joins,
  reconnects, latency, and long sessions. Record convergence and resource use.
- Finish trusted game-rule execution, durable game data, asset wiring, and
  transactional release activation before making claims that depend on them.

See [release readiness](release-readiness.md) for the broader production gate
and [current state](../../CURRENT_STATE.md) for contribution priorities.

## Reproducing the focused checks

Keep the repositories as siblings and use their READMEs for prerequisites.
From the checkout root:

```sh
python3 docs/scripts/check_docs.py
python3 tools/scripts/check_public_review.py
python3 tools/scripts/check_world_model_hosts.py
cargo test --manifest-path tools/Cargo.toml --workspace
PYTHONPATH=tools/src python3 -m unittest discover -s tools/tests
cargo test --manifest-path rust/Cargo.toml --workspace --lib --no-default-features
cargo test --manifest-path studio/Cargo.toml --no-default-features
cargo test --manifest-path desktop/Cargo.toml
```

Build Web WASM before the all-example compatibility harness:

```sh
cd web
npm ci
npm run build:release
npm run check:app
npm run check:startup
npm run check:deployment
cd ..
python3 tools/scripts/check_workspace_compatibility.py
```

The cleanup remains a coordinated set of local repository changes. Land the
consolidated examples and tools/workflow changes with their host consumers
before creating release tags; reusable workflows otherwise fetch incompatible
`main` revisions. No commit, push, remote repository removal, deployment,
remote migration, or production upload was performed during this review.
