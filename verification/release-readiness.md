# Release readiness checklist

**Status:** Proposed checklist

**Maturity:** Preview

This is not committed v1 scope.

This page distills the production-readiness checks from the earlier SDK
roadmap. It is a verification target and evidence plan, not a release promise.
Items become part of a release only when the corresponding contract, owner,
and measurable threshold are recorded.

## Sessions and protocol

- Run authenticated multiplayer soak tests with at least two accounts across
  browsers and devices, including world transitions, reconnects, long sessions,
  latency, jitter, packet loss, and temporary backend failures.
- Record joins/leaves, message IDs, server sequence numbers, reconnect time,
  accepted and rejected intents, convergence, memory growth, and subscription
  cleanup. A completed run ends with matching authoritative snapshots and no
  duplicate interactions.
- Send malformed JSON, missing and mistyped fields, unknown intents, oversized
  payloads, stale versions, duplicates, out-of-order messages, equal-version
  conflicts, and concurrent compare-and-set operations through the real
  authenticated transport. Rejection must be safe, deterministic, bounded, and
  observable; fuzz tests cover parser and state boundaries.
- Define acknowledgement, ordering, retry, deduplication, resume-cursor,
  presence, room shutdown, and restart behavior before claiming reliable
  real-time sessions.

## Compatibility and creator diagnostics

- Freeze the public API and manifest contract for a stable release. Record
  semantic-version rules, runtime capability negotiation, unknown-field
  behavior, deprecations, migration rules, package limits, and the distinction
  between SDK and content updates.
- Require reproducible packages with manifest validation, asset inventory,
  content hashes, and trusted provenance when that mechanism is selected.
  Errors identify the package, file, field, and source location where possible.
- Provide a clean-machine initializer, local preview/watch loop, package
  validator, asset diagnostics, logs, fixtures, CI-friendly build commands,
  and runnable examples for the supported APIs. Diagnostics show the API,
  input, result, and useful failure explanation without exposing secrets.
- Define the minimum discovery identity needed for a published game: creator,
  title, description, thumbnail, tags, age rating, supported platforms,
  visibility, version, and basic play analytics. Search and recommendations
  may remain outside the first release.

## Host, UI, and asset conformance

- Exercise decode failures, missing assets, unsupported formats, cache misses,
  autoplay restrictions, rapid audio triggers, concurrent sounds, and package
  size limits. Document one-shot, loop, positional, music, cooldown, and
  polyphony behavior before exposing those modes.
- Verify UI and input at 390x844, 768x1024, 1280x800, and 1440x900, including
  safe areas, keyboard and touch input, focus order, contrast, overflow,
  reduced motion, and accessible names. Test the actual web, iOS, Android, and
  Studio host adapters; target compilation alone is insufficient.
- Run the same package and scripted interaction trace on every supported host
  and compare lifecycle timing, input semantics, audio and image behavior,
  network results, state transitions, emitted events, and errors.

## Trust, permissions, and operations

- Define permissions for owners, collaborators, players, spectators, teams,
  private rooms, invites, and moderation. Enforce them at the backend rather
  than by hiding UI controls. Separate ephemeral session state from durable
  game and player data, including ownership, migrations, quotas, retention,
  deletion/export, and second-device behavior.
- Threat-model scripts, network calls, assets, credentials, origins, and
  resource exhaustion. Enforce CPU, memory, message, storage, asset, and
  session limits, and test adversarial clients for bounded failure and recovery.
- Before public user content, provide reporting, blocking, age/content labels,
  creator ownership, takedown, review or appeals, and privacy controls for
  chat, images, audio, scripts, usernames, and links.
- Operate health checks, structured logs, metrics, correlation IDs, crash and
  error reporting, release health, dashboards, and incident runbooks. Track
  joins, reconnects, conflicts, publish and asset failures, latency, and
  resource usage with secrets and private data redacted.
- Set measured budgets for startup, frame time, memory, package download,
  decode, bandwidth, concurrent players, retained state, and long sessions.
  Test low-end hardware and every supported host.

## Release gate

A stable SDK release requires evidence that the public contracts are versioned,
documented, validated, and covered by compatibility fixtures; authenticated
soak and malformed-message tests meet declared budgets; important state has a
documented authority, persistence, permission, migration, and recovery model;
publishing supports validation, staging, immutable versions, rollback,
visibility, and release identification; creators have a usable preview and
diagnostic workflow; and security, moderation, observability, performance, and
host checks have owners and tested minimum behavior.

The reference game should exercise the supported surface on every release.
Dedicated automated tests remain responsible for scale and failure modes that
are impractical to prove in a visual probe.
