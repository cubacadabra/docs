# `cubacadabra/deployed`

**Owns:** the checked-in static deployment output for the public Cubacadabra
site, including generated routes, media, QR assets, and deployment metadata.

**Does not own:** source application behavior, the developer site source, or
cross-repository contracts.

- Runs in: the static hosting environment described by its deployment config.
- Depends on: generated output from the product and service repositories.
- Used by: public Cubacadabra site routes.
- Read next: [developer site](../developer/README.md) and [documentation authority](../../reference/README.md).
- Verify with: deployment route checks and the owning source build.
- Incomplete: generated output should not become a second hand-written docs corpus.

Repository: [github.com/cubacadabra/deployed](https://github.com/cubacadabra/deployed)
