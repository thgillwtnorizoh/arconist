# Arconist R003 — native-informed 3D tap foundation

**Current mission result: FAIL / incomplete acceptance.** Source compiles and the
mandatory automated suites pass, but graphical inspection, controlled OS-input
sessions, and a launch of the final Windows export were not completed. Computer
Use reported a physical Escape stop; no further UI actions were issued. This is
preserved partial work for targeted repair, not an accepted playable milestone.
See `../validation/R003.md` for observed evidence and remaining gates.

## Build and run

Use Godot 4.7.2 .NET and the existing .NET 10 SDK. From the repository root:

```powershell
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File reconstructed/godot/build.ps1 -GodotExecutable C:/path/to/Godot_v4.7.2-stable_mono_win64_console.exe
```

`-OfflineRestore` is an explicit option when packages/runtime packs are already
cached and the online NuGet vulnerability-advisory endpoint cannot be reached.
It disables only that online lookup for this build process. The ordinary build
retains the default lookup. All compiler checks and mandatory tests remain enabled.
RTK is the installed wrapper; remove `rtk proxy` if it is unavailable elsewhere.
The script uses existing 4.7.2 templates under `../out/r002-tools`, runs 36 R001
tests/three native comparisons, builds/runs 15 bridge tests, imports the Godot
project, executes 30 Camera3D spatial tests, and exports `../out/r003-windows`.
It rejects nonzero exits and Godot ERROR lines. Export is not launch validation.

```powershell
# Source graphical run; forward-slash absolute log/evidence paths are recommended.
& $Godot --path reconstructed/godot --log-file C:/path/to/source.log -- --evidence-dir=C:/path/to/evidence
# Runtime geometry tests, no OS gameplay input or GPU validation implied.
& $Godot --headless --path reconstructed/godot -- --spatial-tests --evidence-dir=C:/path/to/tests
```

The test runner returns 1 on any failed check, with no skip path. Its JSON report
is `spatial-tests.json`. The source and export include no original assets/music.
Keep `Arconist.exe`, `Arconist.pck`, and the entire adjacent
`data_Arconist.Godot_windows_x86_64` directory together. The export contains .NET.

## Controls and session behavior

Select the 16-tap synthetic practice or byte-identical two-tap native reference,
then Start chart. Three seconds of preroll precede effective gameplay time.
D/F/J/K resolve to internal lanes 2/3/4/5. Press/release each tap; repeated DOWN
and key echoes do not create extra hits. Mouse clicks near the green judgment
line project through the actual track camera to the ground plane. Click the
lane's ground region; the input plane is Y=0 while the thin tap mesh is centered
at native Y=4. Only ground intersections strictly within native -500<Z<500 and
-850<=X<=850 are supported. A far-away click is deliberately rejected.

F6 switches between two controlled camera poses, F7 toggles 1100x740/1320x888,
and F8 saves the real viewport with projection metadata. HUD, judgments, combo,
health, completion/results and replay come from the existing shared core. Focus
loss releases contacts without pausing time. Mouse pointer100 stays distinct from
keyboard contacts. UP cleans the retained pointer even outside the track.

## Native facts and engineering mapping

E007/E032 ordinary tap placement is `(425*(lane-1)-1063, 4, currentDepth)`;
lanes2..5 therefore use X -638/-213/212/637. Godot retains all axis directions and
uniformly divides every native coordinate by425. Ground is Y=0; judgment is Z=0.
Negative Z is distant, approaching Z=0 as core effective time advances.

The renderer uses `trunc(trunc(core.DepthAt(note.Time))-core.DepthAt(E))`, exactly
the existing integer-predepth/float-add ordering, without integrating frame delta.
The core owns chart time, offsets, effective time, candidate membership, expiry,
judgments and results. Rendering does not mutate any of them. Presentation hides
consumed/missed notes immediately and clips depth to[-9500,1000]; this explicit
engineering policy is not E032's retained native renderer lifecycle or GPU output.

Camera home `(0,900,900)` and target `(0,-550,-2000)`, up+Y, are E007-informed.
Near1/far10000 are uniformly scaled. Vertical FOV65 is an engineering selection
from the recovered50..65 range to fit the narrower610x550 viewport; it is not the
native resolution interpolation or a calibrated original camera. One perspective
camera replaces the original paired-camera/layer arrangement. Alternate pose
`(220,1100,1050)` is solely a controlled viewing aid. Track BoxMeshes, sizes,
lighting, colors, depth guides and Label3D key labels are original placeholders.

Picking uses Camera3D.ProjectRayOrigin/ProjectRayNormal, intersects Y=0 and applies
E004's signed-X truncation/thresholds, including X==425 -> no lane. Four-lane outer
clipping, finite checks, epsilon-parallel and backwards-ray rejection are bounded
engineering substitutions. No fixed screen rectangles determine lane identity.
The surrounding UI container is only a viewport-coordinate transform.

## Boundaries

30 automated geometry/timing/projection groups pass in the actual Godot runtime.
This is not a completed graphical/interactive acceptance. G-006 camera reset and
G-007 track fade remain historically blocked. No widening/scene camera actions,
holds/arcs/flicks, physical multitouch, Android, audio, exact FOV calibration,
original shaders/GPU reproduction, pixel fidelity or Unity is implemented.
