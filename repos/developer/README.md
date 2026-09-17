# `cubacadabra/developer`

**Owns:** the public developer site, static assets, routes, and redirects for
legacy documentation URLs.

**Does not own:** the canonical hand-written cross-repository contracts.

- Runs in: Cloudflare Workers Static Assets.
- Depends on: this [canonical docs repository](../../README.md) for cross-repository documentation.
- Used by: developers arriving through `developer.cubacadabra.com`.
- Read next: [documentation authority](../../reference/README.md), [creator guide](../../contracts/creator-guide.md).
- Verify with: site build, route checks, and docs checker.
- Incomplete: presentation may later move to a dedicated docs frontend; GitHub remains source of truth.

Repository: [github.com/cubacadabra/developer](https://github.com/cubacadabra/developer)
