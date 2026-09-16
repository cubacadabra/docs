# Studio

![Studio architecture](../diagrams/studio-system.svg)

Studio is the local authoring and preview host. Its current strongest boundary
is local-first GLB import, validation, compilation, and live renderer preview;
community publishing remains an explicit target workflow rather than a shipped
editor action.

- [Overview](overview.md) — editor purpose, prerequisites, and current limits.
- [Asset workflow](asset-workflow.md) — local GLB import, validation,
  project ownership, and unresolved package wiring.
- [Editing model](editing-model.md) — proposed shared edit path and an
  end-to-end acceptance scenario.
