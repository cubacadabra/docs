# `cubacadabra/font`

**Owns:** the Cubacadabra decorative display font, editable alphabet source,
font builds, specimens, and release assembly.

**Does not own:** Cubacadabra platform runtime or UI contracts.

- Produces: installable TTF, self-hosted WOFF2/CSS, SVG specimens, and a
  versioned source archive.
- Uses: original square Latin letterforms and selected conventional glyphs
  derived from vendored Arimo Regular under the SIL Open Font License.
- Read next: the repository [README](https://github.com/cubacadabra/font) for
  installation, build, and release guidance.
- Status: version 0.1.1 local preview; 144 Unicode characters, with A–Z/a–z
  sharing 26 original designs. Font parsing, FreeType rendering,
  HarfBuzz/CoreText shaping, and Chrome WOFF2 loading have been verified on
  macOS. Windows app installation and other browser/host paths remain unverified.
- The 0.1.1 archive adds the creation-source GPL notice alongside the font's
  OFL notice and preserves the original outlines, mappings, and metrics. See
  the [public review record](../../quality/verification/public-review-2026-10-02.md)
  for current local verification.
