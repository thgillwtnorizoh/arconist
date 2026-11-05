# Arconist R002 — first playable Godot tap prototype

Windows x64, Godot4.7.2 .NET stable, .NET SDK10.0.402 and runtime10.0.13 were
actually built and executed. Game/adapter tests target .NET10; bridge and the
unchanged Arconist.Core target .NET Standard2.1. ProjectReference dependencies
build the same core source; no manually copied gameplay DLL is used.

## Play the Windows package

Get `Arconist-R002-Windows-x64.zip` from the repository release `reconstruction-r002`.
Extract the whole ZIP and double-click `Arconist.exe`. Keep `Arconist.pck` and
`data_Arconist.Godot_windows_x86_64` beside the executable. The .NET runtime is
included; neither the Godot editor nor a separately installed .NET SDK is required.
The tested renderer is OpenGL3.3 compatibility on Windows x64.

Choose Practice and press **Start chart**. After a3-second preroll, use D/F/J/K
for internal lanes2/3/4/5 as notes reach the lime judgment line. Press and release
each key; holding does not generate repeat taps. Lane clicking also uses the core's
contact path. Watch actual judgments, combo, score and health. The16-note original
practice chart spans24.62 gameplay seconds, with its first note at2seconds and
subsequent taps spaced1.5seconds apart. It intentionally has no audio.

At completion, results show PURE/FAR/LOST, shining PURE, score, maximum combo,
integer health and category. **Play again** creates a new Kernel/Timeline and fresh
contacts/results. **Back to start** cleans input and returns to chart selection.
The selectable native reference uses the original two-tap fixture unchanged.

This is an unsigned development prototype, not a production release. Category0
is ordinary failure,1 a clear with LOST,2 a no-LOST clear with FAR,3 an all-PURE
clear, as determined by the shared core after the health threshold.

## Build and export from source

Install/extract the official4.7.2 .NET editor and .NET10.0.402 SDK. From the repo:

```powershell
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File reconstructed/godot/build.ps1 -GodotExecutable C:/path/to/Godot_v4.7.2-stable_mono_win64_console.exe
```

The script verifies the editor/template version, obtains the official .NET template
archive if absent (about1.11GiB), extracts only Windows x64 templates into ignored
`reconstructed/out/r002-tools`, runs all unchanged R001 regressions and15 bridge
tests, builds/imports the project, and exports `reconstructed/out/r002-windows`.
NuGet uses the bundled Godot SDK package directory via GODOT_NUPKGS and nuget.org
for runtime packs. R001's package-free config is untouched. RTK is the local
standing wrapper; on another machine remove `rtk proxy` from commands if unavailable.
Use the4.7.2 .NET editor to import `project.godot` for editor-based development.

Equivalent important commands (GODOT_NUPKGS must point to the editor's
GodotSharp/Tools/nupkgs; Windows workload resolver is disabled by build.ps1):

```powershell
# Repository root
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File reconstructed/validate.ps1
# Working directory reconstructed/godot
rtk proxy dotnet build Arconist.Godot.csproj -c Debug -m:1 -nr:false
rtk proxy dotnet run --project tests/Arconist.Bridge.Tests.csproj
# Repository root, with Godot console executable in $Godot
rtk proxy $Godot --headless --editor --path reconstructed/godot --import --quit
rtk proxy $Godot --path reconstructed/godot
rtk proxy $Godot --headless --path reconstructed/godot --export-release "Windows x64"
```

Build success alone does not establish R002 PASS: separately launch the graphical
application and exported executable and verify input, completion and replay.
The validation report records actual three-level testing, not inferred playability.

## Gameplay bridge and clock policy

`Main.cs` receives Godot InputEventKey DOWN/UP events in callback order. It prefers
physical D/F/J/K and falls back to logical key/Unicode for real Windows input whose
physical metadata does not identify a letter. Echo/duplicate DOWN is filtered by
the bridge; UP removes the matching contact. Mouse uses pointer100, distinct from
keyboard lane contacts2..5. Focus loss releases contacts; gameplay continues,
without pause compensation. Pause/lifecycle reconstruction is outside R002.

One clock source, Godot Time.GetTicksMsec, supplies both input and frame calls.
Start creates a new core with the current tick origin and calls its first Frame.
The core owns the3-second preroll, strict music-start anchor and effective time.
`_Process` calls Frame; `_Input` calls Down/Up immediately, without first inserting
a Frame. This retains035's input-versus-expiry distinction. Input samples callback
reception time, not a claimed OS/hardware event timestamp or calibrated latency.

The renderer reads `core.Timeline.EffectiveTime`. A note's visual Y is
`590-(noteTime-E)*0.18` in the1100x740 logical canvas. This is a simple engineering
visual mapping, not native scroll/camera reconstruction; it cannot accumulate an
independent animation-clock drift. Consumed/missed notes disappear from the shared
state. The HUD and results read actual core values; no UI score/judgment algorithm
exists. `Feedback` copies accepted classifications or actual Frame expirations.

## Evidence capture

F8 saves the actual rendered viewport PNG. Session JSONL records callback order,
E/last-frame E, core candidates/classifications/expiry, per-note flags, counters,
contacts and final results. Default location is Godot's user-data `evidence` folder.
For repeatable audit output, launch with:

```powershell
Arconist.exe -- --evidence-dir=C:/path/to/evidence
```

This flag changes only output location, never gameplay rules, clock speed, charts,
input or scores. There is no autoplay or test judgment mode. Published demonstrations
use controlled real OS key injection, not internal Godot Input.ParseInputEvent or
direct recorder calls. They are not a claim of owner/human hands-on acceptance.

No proprietary music/artwork/resources, original ELF, Unity, Android, holds/arcs/
flicks, skills, special gauges, faithful3D visuals, audio synchronization or production
persistence are implemented. See `../validation/R002.md` and append-only contexts.
