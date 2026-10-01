# Studio

Studio is the local authoring and preview host. It imports and validates
supported assets, builds a portable Cube, and embeds the same runtime Player
uses so creators can test the package boundary honestly.

- [Overview](overview.md) — purpose, prerequisites, and current limits.
- [Asset workflow](asset-workflow.md) — local GLB import and Morph handling.
- [Room capture to playable world](room-capture-to-playable-world.md) — proposed
  reconstruction, editable geometry, and optional native-splat pipeline.
- [Editing model](editing-model.md) — proposed shared edit path.
- [Unified Add palette](add-palette.md) — contextual creation UX and the
  capability map for future authoring systems.
- [Wizard Training Yard parity](wizard-training-yard-parity.md) — workflow
  coverage against a compact Roblox Studio authoring benchmark.
- [Roblox-style scene authoring plan](roblox-style-scene-authoring-plan.md) —
  proposed hierarchy, viewport, import, and validation path for large worlds.
- [Roblox project interchange](roblox-project-interchange.md) — Roblox as an
  import/export target, preservation rules, and the current `.rbxlx` slice.
- [Toolchain](../../systems/toolchain/overview.md) — native builder migration.
- [Studio repository](../../repos/studio/README.md)

Studio is creator software, not the end-user desktop Player. A signed-in creator
can use **File → Publish Game** to save the open project, build a portable Cube
ZIP with the shared native builder, and upload it. The backend checks the
developer-plan entitlement and package validity before accepting the version.
