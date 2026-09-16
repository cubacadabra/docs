# 0004: Keep one canonical home for hand-written platform documentation

- **Status:** Accepted
- **Decision date:** 2026-09-16

## Decision

Cross-repository contracts, product principles, architecture, decisions,
migrations, verification strategy, and shared operating guidance live in this
repository. Implementation repositories keep concise READMEs and
implementation-local comments/tests. Generated docs remain with their
generators; executable fixtures remain with tests.

## Rationale

Cubacadabra's contracts cross repository boundaries. Independent `docs/`
directories created competing specifications and made it difficult for
contributors to find the current answer.

## Consequences

Changes to public or cross-repository contracts update this repo in the same
piece of work. Local build/test/release procedures can stay in a repository
README or CONTRIBUTING file. The source ledger tracks this migration and is
not a permanent prerequisite for understanding the product.
