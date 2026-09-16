# Cross-platform acceptance criteria

These are durable design constraints and test proposals distilled from design
notes and historical reviews. They do not claim the associated feature is
implemented. Current execution status belongs in [roadmap](../roadmap.md) and
the subject contract.

## Prefabs, references, and import

- Duplicate a nested object graph. Internal object references point to the
  duplicated objects; references to shared immutable mesh/material assets
  remain shared.
- Keep document-local IDs distinct from runtime entity IDs.
- Reject or explicitly report unsupported component schemas and unresolved
  dependencies; do not silently drop them.
- Parse/import a document containing a script without executing it.
- Save and reload supported content and compare semantic structure and
  references, not only serialized bytes.

## Shared mutation/editing model

- Make an equivalent edit via Luau and the Studio inspector. Both pass the
  same validation and emit coherent mutation records for runtime consumers.
- Undo a successful edit and recover the last valid project state.
- Invalid edits leave source and last-good preview intact.
- Renderer/physics/network/persistence integrations subscribe to the common
  change feed rather than scanning the whole model each frame.
- Exercise the texture → viewport → placement/material → two-player preview →
  undo end-to-end workflow described in
  [Studio editing model](../studio/editing-model.md).

## Transactional builds and releases

- Reject output paths that overlap or could remove creator source.
- Inject failures at every build/write/rename step; keep the previous
  successful package usable when replacement fails.
- Validate all package files, including assets, against one descriptor before
  activation.
- Interrupt download/update at each step. The client must end with a complete
  old release or a complete new release, never a mixed manifest/script/asset
  set.
- Pin assets to immutable versions or content hashes. Never combine an older
  script with a mutable “latest” texture or package asset.
- Make directory plus archive output one recoverable transaction before
  claiming both outputs are atomic; current builder behavior is documented in
  [game package](../contracts/game-package.md).

## Host behavioral conformance

- Run the same inputs through native and browser Luau runtimes and compare
  decisions, callback ordering, task ordering, API state, emitted commands,
  JSON conversion, and error classification.
- Exercise actual web/WASM, iOS Swift/C, Android JNI/Kotlin, and Studio loading
  and caching paths. A shared validator test or target compile is insufficient.
- Preserve structured semantic error fields when a host adapts them for UI.
- Test missing, malformed, stale, and partially downloaded assets on each
  real loader path.

## Trusted authority and sandbox

- Reject invalid trusted commands without changing state, sequence, or
  receipts.
- Attempt to bypass a protected rule through every other exposed mutation
  path, including generic state setters, retained-state CAS, messages, and
  other public APIs. No alternate path may write the protected result.
- Bind actor identity from authenticated host context; never trust a client
  supplied actor ID or client movement as canonical collision evidence.
- Apply execution budgets to module initialization, every lifecycle callback,
  save/restore, UI/network callbacks, scheduled tasks, and authority handlers.
- Test exhaustion, non-yielding work, raw yields, and callback errors on native
  and browser runtimes.

## Creator reproducibility

- Create, build, and preview a game in a clean environment using only creator
  prerequisites documented in one place.
- Build without maintainer-specific paths, credentials, caches, or private
  asset IDs.
- Pin shared dependencies and prove that rebuilding the same source produces
  a package with the expected files and hashes.

## Product policy proposals

Pricing and discovery principles requiring owner confirmation are listed in
[product principles](../product/principles.md). They must be converted into
explicit product-policy tests only after approval.
