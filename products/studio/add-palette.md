# Unified Add palette

**Status:** Implemented in Studio

The unified Add palette is the discovery and creation surface for Studio's
authoring capabilities. It captures the useful idea behind large ribbon and
insert-object menus without copying Roblox Studio's tabs, service hierarchy,
or class model.

## Product direction

The palette is a compact utility surface that uses the same visual language as
the Scene tree. It has one contextual title, one focused search field, dense
result rows, and short keyboard guidance. It does not use a ribbon, card grid,
or disabled placeholders for unimplemented features.

The same palette opens from:

- the Scene panel **Add** control;
- **Add…** in the Scene tree context menu;
- **Add…** in the editable viewport context menu; and
- **Shift-A** while Studio is stopped in the World workspace.

Search accepts both Cubacadabra names and restrained familiar aliases. For
example, `cube`, `part`, or `platform` finds **Block**; `text` finds **Sign**;
`trigger` finds **Interaction**; and `damage` finds **Hazard**. Arrow keys move
through the results, Enter creates the selected result, and Escape closes the
palette.

Only capabilities that work end to end are shown. Creating an item uses the
same validated scene edit and history path as other Studio edits, selects the
new item, marks source dirty, and preserves save, rebuild, Preview, undo, and
redo behavior. Creating a Block also enters Craft mode so it can be manipulated
immediately.

## Initial catalog

The initial palette exposes the scene objects Studio already compiles:

| Group | Items |
| --- | --- |
| Build | Block, Sign, Ladder |
| Gameplay | Interaction, Checkpoint, Hazard, Safe Zone |

The catalog owns presentation metadata such as labels, descriptions, aliases,
grouping, and availability. It does not duplicate component validation,
serialization, or runtime semantics. Those remain in the shared authoring
model and builder pipeline.

## Capability map

Future features should enter the palette only after their underlying model,
editing, compilation, and Preview paths work:

| Cubacadabra system | Native representation |
| --- | --- |
| Build | Scene nodes with `primitive`, `render`, and `text` components |
| Looks | Appearance properties and project assets, not hierarchy helper objects |
| Bind | Relationship components referencing stable scene-node IDs |
| Motion | Physics actuator components |
| Interface | A dedicated UI graph; layout and style remain properties |
| Code | Project Luau files, bindings, diagnostics, output, and debugging |
| Character | Actor, Morph, accessory, pose, and animation assets |
| Geometry | Source mesh operations compiled into runtime assets |

This map is a coverage ledger, not a request to display future features as dead
rows. New entries become visible only when they can be created, edited, saved,
compiled, previewed, and undone honestly.

## Deliberate boundary

The initial milestone does not add constraints, forces, new primitive shapes,
materials, Interface authoring, debugging, animation, or constructive solid
geometry. It also does not attach arbitrary components to a selected object.
Component attachment should arrive with a schema-driven Inspector so fields
such as `radius`, `color`, and `size` remain associated with the component that
owns them.

## Acceptance criteria

1. Every entry point opens the same palette and catalog.
2. Search matches names, descriptions, and documented aliases.
3. Keyboard focus, arrow navigation, Enter, and Escape work without affecting
   the stopped-world viewport.
4. Read-only projects and Preview do not permit creation.
5. Creation is one undoable transaction and survives save and rebuild.
6. The new object is selected; a new Block enters Craft mode.
7. The palette remains usable in narrow windows and scrolls instead of
   overflowing.

The next intended capability milestone is **Appearance**: real color and
material selection over the existing source and runtime support, registered in
the palette only when it is no longer a preview-only control.
