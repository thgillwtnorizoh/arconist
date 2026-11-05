# Arconist R003-C01 — Windows export recovery

R003 remains unaccepted. Headquarters R003-C01 makes the owner’s human
qualification authoritative. Automated GUI operation, gameplay input injection
and automated screenshot inspection are prohibited. Headless suites establish
technical correctness only. The historical failed R003 report is preserved in
`../validation/R003.md`; the corrective record is `../validation/R003-C01.md`.

## Build and package

Use Godot **4.7.2 .NET**, .NET SDK **10.0.402**, Python 3.11+ and the matching
**mono** export templates. `dotnet` must be on PATH. The SDK needs the .NET
Standard 2.1 reference pack; the explicit restore can acquire it on fresh hosts.
Download Godot/templates from https://godotengine.org/download/archive/4.7.2-stable/.
Prepare a notices folder with GODOT-LICENSE.txt and GODOT-COPYRIGHT.txt from that
Godot source tag, plus DOTNET-LICENSE.txt and DOTNET-THIRD-PARTY-NOTICES.txt from
the Microsoft.NETCore.App.Runtime.win-x64 10.0.13 NuGet package.

From the repository root (Linux or Windows; use your local paths):

```text
python reconstructed/godot/build.py --godot /path/to/Godot.NET --templates /path/to/templates.tpz --notices /path/to/notices
```

The driver runs core/reference/bridge/headless spatial checks, imports and exports
through Godot, validates AMD64 headers and the self-contained runtime, packages
all export files/notices/player instructions and verifies ZIP CRCs and every
extracted file hash. It never launches Windows or operates a graphical game.
Outputs are under `reconstructed/out`: `Arconist-R003-C01-Windows-x64.zip`,
`r003-windows/` and `r003-c01-evidence/` (logs and package-integrity.json).
Each attempt requires a new evidence directory; archive the existing one first.
A prior export is moved aside to evidence before a clean export is created.
Do not distribute `previous-export/` as a prototype.

The Windows PowerShell compilation/export entry remains available:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File reconstructed/godot/build.ps1 -GodotExecutable C:/path/to/Godot_v4.7.2-stable_mono_win64_console.exe
```

No RTK wrapper is required. Both drivers set process-local
`DOTNET_PROCESSOR_COUNT=1` for the exporter’s SDK child. Default exporter Publish
reproduced the silent GetTargetFrameworks failure; serialization completes it.
The underlying SDK/host concurrency defect is not proven. No gameplay code,
compiler checks or regression assertions are changed. `.gdignore` excludes
bridge/tests build artifacts from Godot’s resource scan; their C# project
references still compile normally. The full Python driver is the ZIP delivery path.

`-OfflineRestore` on the PowerShell driver disables only the online advisory
lookup when all required packages are already cached. It does not supply missing
packages, bypass compiler diagnostics or establish qualification.

## Owner launch

Extract the whole ZIP and open `Arconist.exe`. Keep `Arconist.pck` and the entire
adjacent `data_Arconist.Godot_windows_x86_64` folder together. The package includes
.NET 10.0.13; no editor or separate runtime installation is needed. See PLAYER.txt.
Windows launch, graphics, gameplay and restart are pending owner inspection.

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

30 headless geometry/timing/projection groups establish technical correctness.
Human graphical and gameplay qualification remains pending. G-006 camera reset and
G-007 track fade remain historically blocked. No widening/scene camera actions,
holds/arcs/flicks, physical multitouch, Android, audio, exact FOV calibration,
original shaders/GPU reproduction, pixel fidelity or Unity is implemented.
