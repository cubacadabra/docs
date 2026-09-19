# Compatibility and version matrix

## Current package and SDK support

| Dimension | Current value/evidence | Compatibility rule |
| --- | --- | --- |
| Package descriptor | Format version 3 emitted by the tools builder | Do not infer it from `sdkVersion`; keep package parsing and SDK APIs separately versioned. |
| SDK | Runtime/native builder accept `0.3.0`, `0.4.0`, and `0.5.0` | Terrain authoring requires `0.4.0` or `0.5.0`; collision, authored gameplay camera, and horizontal bounds require explicit `0.5.0`. The default creator still emits `0.3.0`; the retired Python builder rejects `0.5.0`. |
| Static collision | Manifest format 1, SDK `0.5.0` | Reject unknown versions and reject collision data without SDK `0.5.0`; the collision format remains separately versioned. |
| MorphPack | Schema v5 only | Schemas 1–4 fail with `MORPH_PACK_UNSUPPORTED_SCHEMA`; rebuild from source. |
| Snapshot | `EngineSnapshot` v1 | Fingerprinted package/script must match before restore; reject before state mutation. |
| Remote character protocol | Envelope v1 | 64 KiB maximum and 17 remote slots, with stable IDs, generation, and sequence. |
| UI document | Current bounded retained UI contract | 512 nodes and 32 levels; see [UI contract](../../contracts/ui.md). |

Values above are a current checked-out snapshot, not a promise that every
host/release supports every value. Release support requires host verification.
The compatibility build and conformance tests must exercise the real loaders,
not only shared validators.

## Migration rules

- Never silently interpret an unknown or unsupported binary schema.
- Pin runtime asset identities to immutable versions/content hashes.
- Keep legacy appearance IDs as explicit inputs/projections only where a
  compatibility adapter documents their mapping.
- A migration must define rejection behavior for unknown values and must not
  reinterpret a published value silently.
- Update this matrix, the normative contract, and host conformance checks in
  the same contract change.

Detailed Morph baseline mappings are in
[Morph migrations](morph-migrations.md). Cross-host parity requirements are
in [host conformance](host-conformance.md).
