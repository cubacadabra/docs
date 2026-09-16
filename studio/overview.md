# Studio

Studio is the local authoring and preview host for Cubacadabra games. It opens
or creates a project, embeds the supported Luau SDK, provides editor and
runtime preview features, and can import supported local Morph assets.

## Project creation and build prerequisites

Studio's **File → New Project** workflow creates and opens a starter project
without an external CLI or Python installation. It writes a manifest, Luau
entry point, embedded SDK, and asset directories. This does not build a raw
source project. The current release packaging contains a Python zipapp and
requires Python 3 to build raw projects.

The raw-project path currently invokes the shared `cubacadabra` builder, using
`CUBACADABRA_CLI_PATH`, a bundled/adjacent executable, or the development
checkout fallback under `../tools/src`. An in-progress Rust migration in
`tools` is intended to replace that Python zipapp with a native `cubacadabra`
executable. Until the migration passes clean-machine host verification, the
Python requirement remains a current release limitation. See the [creator
build toolchain](../architecture/toolchain.md).

## Local asset workflow

Importing a GLB, validating a supported mapping, previewing it, and adding it
to a project are local operations. Studio writes source GLB, mapping sidecar,
compiled pack, thumbnail, and local catalog data. Local catalog presence does
not yet guarantee that the game manifest declares the pack or that a rebuilt
package loads it on every client. See [asset workflow](asset-workflow.md).

Community catalog publication is a separate explicit authenticated workflow
and is not implied by local import.

## Current boundaries

The existing plan includes panels and visual-authoring ideas that are not
necessarily implemented. Studio directly calls Rust APIs rather than routing
in-process editor calls through C/JSON. See the shared
[client runtime](../architecture/client-runtime.md),
[editing model](editing-model.md), and the [roadmap](../roadmap.md).
