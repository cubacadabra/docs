# Performance and resource budgets

Do not turn a point-in-time benchmark into a timeless contract. Record the
device, build, scene, asset set, resolution, and capture method with every
measurement. Distinguish engineering safety ceilings from product targets.

## Current known budgets

- MorphPack v5 limits and per-asset bounds are normative in
  [MorphPack v5](../../contracts/morph-pack-v5.md).
- Character renderer counts and buffer limits, and their distinction from
  mobile frame-time targets, are in
  [character runtime evidence](character-runtime.md).
- Current mobile first-preview art targets and starter part ceilings are
  recorded in [character direction](../../products/characters/art-direction.md) and
  the character study evidence README.
- Backend published free-tier quota figures change over time; the values and
  checked date are stated in [backend storage](../../systems/backend/storage.md).

## Measurement rules

- Measure a complete first-preview loadout, not isolated parts only.
- Include decode, package transfer, residency, and composed geometry where
  each is relevant.
- Recheck on physical devices; desktop GPU captures do not establish mobile
  frame time or input feel.
- Do not raise a single asset budget to mask a shape problem without measuring
  the whole composed loadout and showing that geometry is the limiting factor.
- Keep large temporary renders and traces outside canonical docs; retain only
  selected evidence and compact metrics with reproducible context.
