# 0001: Keep authored game content in JSON

- **Status:** Accepted for current authored manifests/world descriptions
- **Decision date:** Current checked-in format; formal record added 2026-09-16

## Decision

Use JSON for current authored package/world descriptions. Use dedicated binary
formats for runtime assets where justified by their data, such as MorphPack.
No general-purpose binary scene/prefab counterpart is selected.

## Rationale

JSON is inspectable, versionable, and compatible with the current authoring and
validation workflow. A binary format proposal does not by itself establish a
need for a second representation.

## Consequences

Future document/prefab work must preserve stable authored identity, object
reference remapping, explicit asset dependencies, schema validation, and
non-executing import regardless of encoding. See
[assets and prefabs](../architecture/assets-and-prefabs.md).
