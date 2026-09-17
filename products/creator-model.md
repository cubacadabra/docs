# Creator model

## Creator independence

A game creator should be able to install supported tools, create a project in
any directory, build and preview it without the platform maintainer's special
checkout, credentials, or private cloud assets. Project-owned source and
dependencies must be explicit and reproducible. Shared dependencies may be
external when versioned or content-addressed and available to the build.

This is different from contributing to Cubacadabra itself. A platform
contributor may need a coordinated multi-repository checkout and native SDKs;
those requirements must not leak into the ordinary creator workflow.

## Ownership and sharing

Local import, preview, and editing are project operations and should not
require sign-in. Sharing or publishing to a community catalog is a separate,
explicit authenticated action with a license, attribution, visibility, and
version. A published catalog update must not silently change a game that
already references an asset.

The game repository remains the source of truth for authored art. Compiled
runtime assets are derived outputs. Community hosting may distribute immutable
assets, but a game must not depend on an author's mutable private path or
account.

## Onboarding

Keep project creation and project building distinct. Studio's New Project
flow creates the project and embeds SDK modules without an external runtime.
Building raw source projects uses the shared Rust builder in-process; the
native CLI exposes the same library for terminal workflows. The clean-machine
reproducibility criterion applies to the complete create/build/preview path and is listed in
[acceptance criteria](../quality/verification/acceptance-criteria.md).
