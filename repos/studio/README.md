# `cubacadabra/studio`

**Owns:** the native creator host, local projects, source import, builder
integration, and in-process preview.

**Does not own:** end-user Player behavior, shared simulation semantics, or
community publishing policy.

- Runs in: native desktop creator workflows.
- Depends on: [Rust](../rust/README.md), [tools](../tools/README.md), and local source assets.
- Used by: creators; preview uses the same runtime players use.
- Read next: [Studio](../../products/studio/README.md), [asset workflow](../../products/studio/asset-workflow.md), [editing model](../../products/studio/editing-model.md).
- Verify with: [acceptance criteria](../../quality/verification/acceptance-criteria.md) and [host conformance](../../quality/compatibility/host-conformance.md).
- Incomplete: manifest wiring for imported Morph assets and the shared editing pipeline.

Repository: [github.com/cubacadabra/studio](https://github.com/cubacadabra/studio)
