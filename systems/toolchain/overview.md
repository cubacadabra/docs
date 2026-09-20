# Creator build toolchain

**Status:** Core Studio migration landed; command-surface migration in progress

The `tools` repository owns project creation, source validation, SDK bundling,
and portable game-package construction. The package format and creator-facing
validation behavior are defined by the [game package contract](../../contracts/game-package.md);
the implementation language is not part of that contract.

## Current state

The Rust workspace in `tools` now owns the canonical `cubacadabra-scene`,
`cubacadabra-builder`, `cubacadabra-project`, and native `cubacadabra` CLI
crates. `cubacadabra-scene` owns the editable authoring model; the builder
consumes it to produce runtime package content. Studio calls the builder
library in-process and depends on the scene model directly. The Python implementation remains for commands
and the compatibility harness that have not yet moved into Rust; it is not
required by Studio or its release packaging.

The first migrated surface is the creator-critical path: native project
creation, source building, Luau dependency resolution, SDK bundling, package
metadata, asset copying, hashes, and guarded transactional output. The CLI
currently exposes `create-game` and `build-game`; maintainer-only upload,
local-service, and morph-release commands remain queued for their own Rust
library migrations.

## Target boundary

The Studio-required project and build path is delivered by the shared Rust
crates in `tools`. Studio builds a raw project into a temporary package and
loads the result through the existing Rust runtime. The Studio release does
not need a Python interpreter, a Python zipapp, or `PYTHONPATH` for this path.

This is a toolchain implementation migration, not a change to game rules,
Luau SDK semantics, package layout, package hashes, or host runtime ownership.
Maintainer-facing commands such as uploads, local service setup, asset
authoring helpers, and the compatibility harness may remain Python until they
have their own migration plan; they must not be required by an installed Studio
build.

## Local Roblox project import boundary

**Status:** Proposed product and implementation policy; not legal advice

The shared importer may support creator-supplied local `.rbxl` and `.rbxlx`
files. The native CLI/library is the source of truth for parsing, provenance,
conversion, and diagnostics; Studio should call that same logic in-process
rather than implement a second importer. The intended boundary is:

```text
Roblox Studio
    -> creator saves MyGame.rbxl / MyGame.rbxlx locally
    -> Cubacadabra native importer
    -> scene.json + .luau source + project-owned assets
    -> normal validation and package build
```

This is a migration tool for a project the user owns or is authorized to
migrate. It is not a Roblox experience downloader. Cubacadabra must not log
into Roblox to scrape experiences, reconstruct a game from an Experience ID,
download arbitrary CDN assets, or present public playability as permission to
reproduce a game's scripts, artwork, or models.

### Ownership and provenance

The importer must distinguish the creator's work from material merely licensed
for use inside Roblox. A creator may retain copyrights in their own UGC, but a
`.rbxl` file can also contain Creator Store assets, Roblox-owned content,
licensed music, or other third-party material. Those resources must not be
treated as portable just because they are present in the source file. See
[Roblox's Terms of Use](https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use)
and [Creator Store Terms](https://en.help.roblox.com/hc/articles/21308223046932)
for the source-platform policies that inform this boundary.

Every imported resource should receive one of these provenance classes:

```text
CREATOR_OWNED_LOCAL
UNKNOWN
CREATOR_STORE
ROBLOX_OWNED
LICENSED_MUSIC
EXTERNAL_ASSET
```

The import flow must require an affirmation such as:

> I own this project or have permission to migrate its contents.

That affirmation does not override resource-level restrictions. For
`UNKNOWN`, platform-specific, or third-party resources, the conservative
default is to retain the source identifier and a placeholder or diagnostic,
but not copy the binary into the Cubacadabra project unless the user supplies
appropriate rights or a replacement.

The importer must preserve an audit trail for each resource. A minimal record
is:

```json
{
  "source": "rbxl",
  "originalAssetId": "12345",
  "provenance": "CREATOR_STORE",
  "imported": false,
  "reason": "third-party Roblox Creator Store asset"
}
```

The completion report should make conversion and omission visible, for example:

```text
IMPORT COMPLETE

✓ 3,821 Parts
✓ 129 Models
✓ 87 creator-written Luau scripts
✓ 42 creator-uploaded images

⚠ 14 externally licensed assets were not copied
  12345678  Creator Store mesh       replace or provide permission
  98765432  Roblox R15 character     replaced with a Cubacadabra character
  48392018  Licensed audio           omitted

✓ 98.7% of supported scene content converted
```

The exact counts and wording are implementation details, but a successful
import must never imply complete visual or legal portability. The report must
also identify unsupported classes, approximations, missing dependencies, and
source-only scripts. Parsing and inspection remain non-executing; imported
Luau is source data until a separate explicit build/preview operation runs it.

### Product and launch safeguards

The importer should use a descriptive file-format label such as **Import
`.rbxl` / `.rbxlx` Project** and avoid Roblox logos or language that implies
affiliation or endorsement. The [Roblox Name and Logo Community Usage
Guidelines](https://en.help.roblox.com/hc/articles/115001708126) should be
reviewed with counsel before commercial launch.

If Cubacadabra later hosts public converted projects, publishing becomes a
separate UGC risk boundary. Before meaningful public uploads, define
`/copyright` and `/dmca` pages, designate a DMCA agent, and implement notice,
counter-notice, and repeat-infringer procedures appropriate to the service.
The [U.S. Copyright Office DMCA overview](https://www.copyright.gov/dmca/)
and [Chapter 12](https://www.copyright.gov/title17/92chap12.html) are useful
starting references, not substitutes for a focused legal review.

Commercial launch requires an IP/software attorney to review the importer
architecture, current source-platform terms, and exact UI/marketing language.
The toolchain can enforce conservative technical defaults, but it cannot
determine ownership or grant a user rights they do not have.

## Completion evidence

The migration is complete for Studio only when all of the following are true:

- the native CLI preserves the current project/build command behavior and
  package-contract outputs, including validation failures and integrity data;
- the compatibility workflow builds representative projects from
  `first-game`, `second-game`, `third-game`, and `examples` with the native
  builder and compares the resulting package semantics;
- Studio's raw-project preview succeeds on macOS, Windows, and Linux on a
  clean machine with Python unavailable;
- Studio release archives contain the native builder and no
  `cubacadabra.pyz` dependency; and
- the old Python fallback is removed or explicitly isolated to development and
  migration diagnostics rather than the shipped Studio path.

See the [Studio overview](../../products/studio/overview.md), [roadmap](../../reference/roadmap.md),
and [release-readiness checklist](../../quality/verification/release-readiness.md) for
the product and verification implications.
