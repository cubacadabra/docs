# Moderation and safety

Current backend capabilities include authenticated block/unblock and report
endpoints. Block state can filter peer visibility and movement for the
requesting player. Server-side checks own authentication and accepted state;
clients may keep a projection to filter local presentation.

These endpoints are a foundation, not a complete public user-content policy.
The platform still needs explicit operating procedures for reporting, review,
takedown, appeals, creator permissions, privacy/data deletion, and support
before broad public user-created content. See [roadmap](../../reference/roadmap.md).

## Safety boundaries

- Client validation improves feedback but does not authorize an action.
- A blocked-player projection must not become authority for account identity
  or moderation decisions.
- Report submission and adjudication are different capabilities; the endpoint
  existing does not imply a staffed review/appeal process.
- Resource limits, diagnostics, and safe handling of untrusted packages are
  required as creator distribution expands.
