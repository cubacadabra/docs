# Wizard Training Yard parity

**Status:** Active capability benchmark

The Wizard Training Yard is a ten-step Roblox Studio workflow used to measure
Cubacadabra Studio's creator coverage. The goal is equivalent creative power
through Cubacadabra's node-and-component model, not Roblox class or service
parity.

## Current coverage

| Step | Cubacadabra workflow | Status |
| --- | --- | --- |
| 1. Arena | Add Blocks, rename them, and use viewport Place, Shape, and Turn tools | Ready |
| 2. Bridge | Duplicate Blocks, rotate them, add a Group, and move the planks below it | Ready |
| 3. Appearance and crystal | Choose primitive color and a portable built-in surface material; a vivid small Block can stand in for the crystal | Partial: emissive/glow appearance is not yet a portable material capability |
| 4. Hinged gate | Add relationship components referencing stable node IDs | Not yet: Bind/hinge runtime semantics are required |
| 5. Swinging hazard | Add a rope relationship between authored bodies | Not yet: Bind plus dynamic-body physics are required |
| 6. Powered obstacle | Add a bounded Motion actuator instead of per-frame transform script | Not yet: shared actuator semantics are required |
| 7. Wizard Guide | Add an Actor, rename it, position it, and edit its appearance properties | Ready for stationary actors; pose authoring remains future work |
| 8. HUD | Author the existing runtime UI document through Luau and inspect its live nodes in Studio | Partial: a dedicated editable UI graph is still required for visual authoring |
| 9. Collectible | Combine an Interaction, game state, and runtime UI updates in project Luau | Partial: supported through code, without a first-class collectible component or debugger |
| 10. Game loop | Use interactions/checkpoints, state, UI, and Play/Stop to build and test the loop | Partial: code-driven today; dedicated reset and flow authoring remain future work |

## Cubacadabra-specific rules

- Groups are ordinary componentless scene nodes. They do not become a runtime
  `Model` class and may be compiled away.
- Color and surface material are properties of a renderable component. They do
  not create hierarchy helper objects.
- Future hinges, ropes, and actuators must reference stable scene-node IDs and
  compile to portable runtime data. Attachments should only exist when they
  carry reusable authored frames, not because a source platform required an
  intermediary object.
- Interface authoring should use a dedicated UI graph. Layout and styling stay
  properties instead of becoming dozens of Explorer objects.
- Game-specific collection rules and completion state stay in project Luau.

## Next acceptance slices

1. **Bind:** author a limited hinge between two primitive nodes, preview it in
   every locally available desktop host, and preserve it through save, undo,
   rebuild, and package validation.
2. **Dynamic bodies:** add a rope relationship and a powered angular actuator
   with bounded deterministic simulation and snapshot coverage.
3. **Interface:** create and edit a small counter panel through a source-backed
   UI graph, then bind its text to game state without duplicating runtime UI
   interpretation in Studio.
4. **Code feedback:** surface runtime Luau diagnostics and output beside the
   source editor, then verify the collectible and completion loop end to end.
