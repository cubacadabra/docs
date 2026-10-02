# Local room camera reconstruction and alignment

**Status:** Current contract
**Maturity:** Preview

Initial sparse camera recovery, version 1. Creator source only; no runtime
package changes.

The shared `tools` crate `cubacadabra-room-capture` owns camera recovery,
evidence validation, and alignment math. Studio and the native CLI consume the
same types. The input is a completed [room capture](room-capture.md).

## Local workflow

Studio's **File → Import From → Room Video…** can open an existing
`capture.json`, extract a new capture, or open `reconstruction.json` directly.
**Recover cameras** runs the optional local COLMAP executable in a background
worker. Closing the dialog or Studio cancels the worker; active subprocesses
are killed and reaped. The UI displays the current stage and elapsed time;
it does not fabricate a completion percentage or remaining-time estimate.

```sh
cubacadabra recover-cameras --capture /path/to/capture.json \
  --output /path/to/new-reconstruction
```

Optional `--colmap /path/to/executable` and `--threads 1..16` select the CLI
backend and CPU concurrency. Defaults are `colmap` on `PATH` and four threads.
On macOS, standard Homebrew and MacPorts executable locations are also checked
when the application was launched without their directories on `PATH`.
COLMAP is optional creator tooling, outside the ordinary Studio build and all
player packages. This initial adapter was exercised with COLMAP 4.2.1 on
macOS; other versions and operating systems need their own integration checks.
The adapter recognizes the newer `FeatureExtraction`/`FeatureMatching` and
older `SiftExtraction`/`SiftMatching` CPU option namespaces from executable
help. An incompatible CLI fails explicitly rather than silently dropping
settings. Commands use argument arrays, without a shell.

Only frames whose `evaluation` field is false are copied into a new workspace
and supplied to feature extraction, matching, and mapping. Evaluation frames
are absent from its image folder and database; their poses are not recovered.
Later evaluation-view localization must keep the fitted geometry and cameras
fixed rather than feeding those images back into reconstruction or training.

The initial adapter uses one shared `SIMPLE_RADIAL` camera, CPU SIFT, sequential
matching with overlap 20 and loop detection disabled, incremental mapping with
minimum model size 3, and seed 0 for feature extraction, geometric verification,
and mapping. Tool version and adapter settings are retained. This is an
estimated calibration: zoom, lens changes, stabilization, and variable
intrinsics can violate the shared-camera assumption. No learned model download,
cloud job, dense reconstruction, or Gaussian training is invoked.

## Storage and completion

```text
reconstruction/
  reconstruction.json
  frames/                   # copied reconstruction JPEGs only
  points/                   # bounded JSON evidence shards
  logs/                     # local backend help and processing logs
  colmap/                   # backend database, binary models, text exports
  alignment-000.json        # optional reviewed alignment for components[0]
  alignment-001.json
  measurements.json         # optional creator-supplied object dimensions
```

The capture and its original frames remain unchanged. The result retains its
own frame snapshots so it can be reopened independently of the input folder.
Frame and point-shard SHA-256 values detect changed evidence. Bulk backend
data stays in ordinary files; every generated JSON file is at most 4,000,000
bytes. Sparse evidence is capped at 500,000 points per component, 300 views,
4,096 feature observations per point, and 1,000 points per shard. Individual JPEG
snapshots are at most 32,000,000 bytes and are checked against the capture's
declared dimensions before decoding. Imported COLMAP text files are capped at
512,000,000 bytes. Paths must remain inside their evidence folder, including
after resolving symlinks.

Existing outputs are refused. Work occurs in a sibling temporary directory.
Finalization exclusively reserves the destination, moves evidence, and writes
`reconstruction.json` last as the completion marker. Readers must ignore
folders without that marker. Cancellation and recoverable failures clean
staged work and do not replace existing results. A failed backend may leave a
bounded sibling `<output>.failed.log` for local diagnosis; it is not a valid
reconstruction. A crash can leave an incomplete folder, which must not be
silently reused.

Keep this evidence outside runtime `assets/` and `runtime/` trees. It contains
private images and local backend logs, and must not enter published packages.

## Reconstruction version 1

JSON uses camelCase. All listed fields are required. Readers reject unknown
`formatVersion`, unsupported camera models, invalid dimensions, non-finite or
unbounded numbers, non-unit pose quaternions, and inconsistent identities.
Versioning is independent of the capture, Cube, SDK, and network versions.

| Field | Meaning |
| --- | --- |
| `formatVersion` | Integer `1`. |
| `captureSha256` | SHA-256 of the exact input `capture.json` bytes. |
| `sourceVideoSha256` | Original video identity from the capture. |
| `backend` | `name`, executable `version`, `adapter` (`colmap-sparse-v1`), `threads`, `cameraModel`, `sharedIntrinsics`, `useGpu`, `sequentialOverlap`, and `randomSeed`. |
| `inputs` | Reconstruction frame `id`, relative copied `file`, `sha256`, `width`, and `height`. IDs preserve capture identity. |
| `evaluationFrameIds` | Withheld capture IDs, disjoint from `inputs`. |
| `unregisteredFrameIds` | Input IDs absent from every returned component. |
| `components` | Separate camera/point solutions, ordered by descending registered-frame count, then ID. |
| `diagnostics` | Review limitations and explicit capture/calibration warnings. |

Each component has `id`, `cameras`, `frames`, `pointShards`, `pointCount`,
`meanPointReprojectionErrorPixels`, `medianPointReprojectionErrorPixels`, and
`medianTrackAngleDegrees`. Components have independent coordinate frames and
scales. They may share input frames as overlapping alternative solutions;
they must not be concatenated into one world. Registered counts use the union
of frame IDs, rather than summing component sizes. A backend run that completes
without a model may retain an empty `components` list and explicit no-result
diagnostics; an operational backend failure is an error.

Camera intrinsics contain `id` (component-local), `model` (`SIMPLE_RADIAL`),
`width`, `height`, `focalLengthPixels`, `principalPointPixels: [cx, cy]`, and
`radialDistortion: k1`. For normalized camera coordinates x and y:

```text
r² = x² + y²
u = f * x * (1 + k1*r²) + cx
v = f * y * (1 + k1*r²) + cy
```

Each registered frame contains `frameId`, `cameraId`, `rotationWxyz`, and
`translation`. The Hamilton quaternion is scalar-first and maps reconstruction
coordinates into camera coordinates: `pCamera = R * pReconstruction + t`.
Camera axes point right, down, and forward. The camera center is `-Rᵀ * t`.
Reconstruction units and world orientation are arbitrary until reviewed.

Each point-shard declaration has relative `file`, `sha256`, and `count`.
Its JSON array contains points with component-local `id`, `position: [x,y,z]`,
`color: [r,g,b]` (bytes), `reprojectionErrorPixels`, and `observations`.
An observation retains `frameId`, COLMAP's zero-based `pointIndex`, and original
selected-image `pixel: [u,v]`. Multiple feature observations in the same frame
are preserved with distinct point indices. Tracks must contain at least two
distinct registered views. Point IDs are
backend evidence identity within this run; they do not promise stability
across reconstruction reruns and are not native scene-node IDs.

Reprojection summaries are the unweighted mean and upper-middle median of
COLMAP's per-point pixel errors. Track angle is computed per point as the
largest angle between the ray from its first chronological observation and
the rays from its other observations, then summarized by upper-middle median.
It is a lower bound on the maximum pairwise triangulation angle. A median below
5° and radial distortion magnitude above 0.5 produce review warnings. These
are heuristics, not calibrated confidence thresholds. Small reprojection
errors do not establish correct depth, coverage, or physical dimensions.

## Reviewed alignment version 1

Creator measurements can be retained before suitable reconstructed anchors are
available. `measure-capture` atomically updates one measured object and preserves
other entries:

```sh
cubacadabra measure-capture --reconstruction /path/to/reconstruction.json \
  --object desk --label Desk --dimensions-meters 1.8288,0.9144,0.9144
```

`measurements.json` is a separate version 1 creator-source record with
`formatVersion`, `captureSha256`, and `objects`. Each object has a unique local
`id`, readable `label`, `lengthMeters`, `depthMeters`, and `heightMeters`.
Object IDs are 1–128 ASCII letters, digits, hyphens, or underscores; labels are
nonempty, at most 200 UTF-8 bytes, and contain no control characters. Dimensions
are finite positive meters, each at most 10,000. There are at most 300 objects,
ordered by ID. Readers reject unsupported versions, duplicate IDs, and a capture
identity mismatch. This record is a physical measurement supplied by the
creator; it does not identify a native scene node or claim an inferred object
boundary, calibrated reconstruction, or approved alignment. Measurements bind
to the capture rather than one stochastic reconstruction, so they may be
explicitly carried into a rerun of that same capture.

Studio exposes stored length, depth, and height as choices for the measured
distance input. The creator must still match the chosen dimension to two
appropriate point anchors and review the floor orientation. Dimensions alone
do not establish `metersPerUnit` or gravity.

Studio displays a sparse cloud and recovered cameras with orbit and zoom
controls. Selecting a point marks its observed pixel in a source photograph.
Keyboard-accessible frame menus, view sliders, and point-ID inputs complement
pointer picking. Clouds above 20,000 points use a deterministic display sample;
all anchors remain addressable by point ID.

Choose two points whose physical distance is measured, enter meters, and choose
three non-collinear floor points. The first floor point is the origin, the
first-to-second vector defines +X, and their ordered cross product with the
first-to-third vector defines +Y. Check the upward Y arrow and scale in
**Preview alignment**, then **Save reviewed alignment**. **Flip floor up**
swaps the second and third floor points; this also changes the X direction.
Creator review establishes that the selected points actually lie on a floor.
The software does not infer gravity from the photographs.

The CLI uses the same computation:

```sh
cubacadabra align-capture --reconstruction /path/to/reconstruction.json \
  --component component-001 --distance-points 123,456 --meters 1.2 \
  --floor-points 789,1011,1213
```

An alignment contains `formatVersion: 1`, `reconstructionSha256`,
`componentId`, `distancePointIds: [a,b]`, `distanceMeters`,
`floorPointIds: [origin,x,third]`, `metersPerUnit`, `rotation` (row-major 3×3),
and `translationMeters: [x,y,z]`:

```text
pWorld = metersPerUnit * rotation * pReconstruction + translationMeters
```

World coordinates are right-handed, in meters, with +Y up. The first floor
point maps to the origin, and the selected floor plane maps to y=0. Apply the
same similarity transform to future visual geometry, collision, and object
positions. Transform camera centers as points and camera basis directions by
the rotation; do not apply a point translation to a direction or blindly scale
a world-to-camera pose's translation field.

Alignment files bind anchors and transforms to the exact reconstruction bytes
and one component. Readers reject incompatible versions, stale identity,
degenerate anchors, reflected/non-orthonormal rotations, and transforms that
do not agree with the reviewed anchors. Saves atomically replace only the
alignment file for that component. Camera evidence and capture metadata remain
immutable. A rerun is a new result; existing corrections are not silently
transferred to new backend point IDs.

## Verification boundary

Tools tests exercise camera conventions, COLMAP text parsing, observation
consistency, evaluation exclusion across the subprocess adapter, hash/path
validation, bounded sharding, existing-output preservation, child cancellation,
failure cleanup, and persisted metric alignment. Studio checks worker states
and responsive review layout; its opt-in native framebuffer probe loads actual
camera evidence and photographic source views. Real recovery on a supplied
video is separate evidence from parser fixtures.

This stage does not establish dense surfaces, a mesh, splats, collision,
playable-world conversion, or cross-host runtime compatibility. The next
boundary is reviewed dense geometry and supported visual/collision preparation
through the normal toolchain.
