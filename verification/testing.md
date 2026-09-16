# Verification strategy

Use the narrowest test that exercises the real contract, and state exactly
which boundary the evidence covers.

| Evidence | Proves | Does not prove by itself |
| --- | --- | --- |
| Unit test | The tested function/module behavior | That an app calls it or a host adapter preserves behavior |
| Integration test | The connected components and path exercised | Production availability or other host parity |
| Compile/check for a target | Code type-checks/builds for that target | Device execution, performance, input, lifecycle, or release packaging |
| Host conformance test | The named real adapter/loader path behaves as specified | Untested hosts or production scale |
| Release evidence | The shipped artifact and declared release path | Unmeasured reliability beyond the sampled evidence |

## Minimum contract test groups

- Manifest/package validation and deterministic package outputs.
- Module resolution, bundling, cache behavior, and execution limits.
- UI layout, safe areas, pointer consumption, modal blocking, and multi-pointer
  behavior.
- Effects/audio/task bounds and deterministic tick semantics.
- Snapshot restore atomicity and run/capture/restore equivalence.
- Native/browser behavior parity and real host loader/cache paths.
- Asset hashes, missing dependency behavior, package rollback and cache
  activation.
- Authority denial through every exposed mutation route.
- Clean-machine creator workflow and public docs consistency.

For platform-specific current commands and exact test scope, see
[headless](headless.md), [character runtime](character-runtime.md),
[host conformance](../compatibility/host-conformance.md), and the local
README/CI for each implementation repository. Repository-local build/run
instructions are intentionally operational rather than a second contract.
