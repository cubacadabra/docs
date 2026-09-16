# 0003: Share portable runtime semantics in Rust

- **Status:** Accepted where it removes real semantic drift
- **Decision date:** Current checked-in architecture; formal record added 2026-09-16

## Decision

Use shared Rust runtime modules for platform-neutral simulation, client
protocol state, generic application decisions, and data-model behavior where
multiple hosts need the same semantics. Native, web, and Studio hosts retain
their presentation, transport, OS integration, and accessibility behavior.

## Rationale

Shared semantic decisions reduce drift across hosts. Duplicating trivial UI or
host APIs in Rust without a demonstrated cross-host contract adds complexity
without the same benefit.

## Consequences

Hosts must preserve shared semantic results and structured errors. Validate the
real bindings and loaders, not just shared modules. Rust-to-Rust Studio calls
use direct Rust APIs, not JSON or the C ABI. See
[app runtime](../architecture/app-runtime.md),
[client runtime](../architecture/client-runtime.md), and
[host conformance](../compatibility/host-conformance.md).
