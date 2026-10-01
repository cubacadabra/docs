# Local room-capture dataset

**Status:** Initial video-intake format, version 1. Creator source only.

The `tools` crate `cubacadabra-room-capture` owns video inspection, frame
selection, and serialization. Studio and `cubacadabra capture-video` call the
same Rust implementation. This format does not change Cube packages or player
loading, and it does not establish a reconstructed world or calibrated camera.

## Intake and storage

Studio exposes **File → Import From → Room Video…**, including when no project
is open. The creator chooses a local video and an existing output parent. The
workflow creates a new capture folder, processes in the background, supports
cancellation, and offers frame review. The CLI requires an explicit new output
folder:

```sh
cubacadabra capture-video --video room.mov --output /path/to/room-capture
```

FFmpeg and ffprobe are optional, local creator prerequisites for this workflow.
They are invoked with argument arrays, without a shell. No Python, COLMAP,
Brush, network service, or GPU training dependency is required for intake.
The current decoder produces JPEG review/reconstruction inputs; calibrated HDR
tone mapping and lens correction are not implemented.

```text
room-capture/
  capture.json
  frames/
    frame-000001.jpg
    ...
```

The original video is not copied or altered. Keep it separately: filename,
byte count, and SHA-256 identify the exact source, without saving an absolute
machine-local path. Exported datasets contain private photographic evidence;
intake does not upload or publish it.

Keep capture folders outside runtime `assets/`. The current builder copies
that tree; undeclared capture images placed there could enter packages.
Only reviewed, explicitly prepared runtime visuals/collision should later
enter a game's runtime assets through the normal authoring/build path.

Existing outputs are refused. Processing uses a sibling temporary directory;
failure and cancellation remove temporary candidates. Finalization exclusively
reserves a new destination, moves selected frames, then writes `capture.json`
as the completion marker. A reader must ignore directories without that marker.
Recoverable finalization failures remove this import's output. A process crash
can leave an incomplete directory; it must not be treated as a valid dataset or
silently overwritten on retry.

## Version 1 fields

JSON uses camelCase. All fields listed below are required, except that the scale
value is explicitly nullable. Readers must reject unknown `formatVersion`
values before interpreting the dataset. Versioning is independent of the Cube,
SDK, and network protocol versions.

| Field | Meaning |
| --- | --- |
| `formatVersion` | Integer `1`. |
| `source.filename`, `source.sha256`, `source.bytes` | Original filename, lowercase SHA-256, and original byte count. |
| `source.video.width`, `height` | Encoded dimensions before display rotation; selected JPEG dimensions are recorded separately. |
| `source.video.durationSeconds`, `codec`, `rotationDegrees` | Probed video-stream duration (format-duration fallback), codec, and reported display rotation. |
| `source.video.frameRate`, `pixelFormat`, `colorTransfer`, `colorPrimaries`, `colorRange`, `sampleAspectRatio` | Probed strings, or `unknown` when absent. Frame rate retains the rational representation. |
| `settings.maxFrames`, `settings.maxDimension` | Selection budget and longest-side pixel bound. Defaults: 180 and 1600. |
| `decoder` | FFmpeg version banner from the installed executable. |
| `selector` | `temporal-laplacian-v1`, the versioned frame-selection algorithm. |
| `scaleMetersPerUnit` | `null` at intake; RGB footage has not established metric scale. |
| `candidateCount` | Number of successfully decoded and scored candidates. |
| `frames` | Chronologically ordered selected frame records, described below. |
| `diagnostics` | Human-readable limitations and image-detail review warnings. |

Each frame has a stable candidate-based `id` (`frame-000001`), a relative
`file` (`frames/frame-000001.jpg`), finite nonnegative `timestampSeconds`,
finite nonnegative `sharpness`, boolean `evaluation`, and positive integer
`width`/`height`. Paths refer only to selected JPEGs inside this dataset;
absolute paths, parent traversal, and external resources are invalid.

`timestampSeconds` is decoded presentation time relative to the first decoded
frame. FFmpeg normalizes timestamps before temporal selection, and `showinfo`
records the selected decoded frames' times. Times are not inferred from file
number or nominal frame rate. FFmpeg applies its default display autorotation.

## Selection and limits

Intake accepts finalized local video with a usable duration from 0.1 seconds to
two hours and encoded dimensions at most 16384 pixels per side. Options allow
10–300 selected frames and a 320–2560 pixel maximum dimension. JPEGs are
downscaled to fit, without intentional upscaling. Metadata must remain at or
below 4,000,000 bytes.

The selector decodes at most three candidates per requested selected frame.
It samples at intervals of `max(duration / (3 × maxFrames), 1/30)` seconds,
using actual presentation timestamps, rather than duplicating low-rate input
frames. Source frame timing can reduce the candidate count.

Divide the capture duration into `maxFrames` temporal windows and choose the
highest-scoring candidate in each nonempty window. Ties retain the earlier
candidate. Score the variance of a discrete grayscale Laplacian after resizing
to fit 320 pixels with the Rust image library's triangle filter. This ranking
retains temporal coverage instead of collecting only the sharpest moment;
it does not prove spatial coverage, useful baseline, or camera registration.

Every tenth selected frame is marked `evaluation: true`; future reconstruction
and training adapters must exclude those images. Adjacent video views are
correlated, so this split alone is not strong evidence of novel-view quality.
The review UI identifies evaluation frames.

Intake always reports unknown camera intrinsics, camera poses, overlap,
coverage, and metric scale. It additionally flags unusually low relative
sharpness, nearly absent image detail, small selected sets, and HDR sources.
These are review heuristics, not calibrated confidence or recapture guarantees.

## Verification and next boundary

The tools test suite checks temporal coverage and tie handling, image-detail
ranking, timestamp parsing, malformed metadata, existing-output preservation,
and cancellation. An FFmpeg integration fixture exercises actual decoding,
JPEG dimensions, timestamps, source identity, evaluation splitting, persisted
metadata, and temporary-output cleanup when FFmpeg is installed.

The next stage consumes reconstruction frames to recover shared camera
intrinsics/poses and a sparse point cloud, records registration diagnostics,
and asks for a measured scale anchor. It needs a separate versioned result
contract and adapters in `tools`. See the
[room-capture product proposal](../products/studio/room-capture-to-playable-world.md)
for geometry, collision, editing, and subsequent splat experiments.
