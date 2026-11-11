# Arconist reconstruction — R008

R008 adds one independently judged arc-tap on a trace-mode linear parent to
owner-accepted R007. Parent geometry/child identity are linked; initial mouse DOWN
uses flag1 spatial selection then the same tap-tier classifier. Holding/moving
cannot award the child. Trace parents contribute no checkpoints or color claims.
See [R008 report](../validation/R008.md), [player guide](PLAYER.txt) and
[E025 reference provenance](../../reference_traces/r008/README.md).

Toolchain remains Godot4.7.2.NET / SDK10.0.402 / bundled runtime10.0.13, with
DOTNET_PROCESSOR_COUNT=1. The logged build driver requires clean committed source
and fresh r008-evidence output; it runs all283 prior groups,65 new groups and
three standalone reference comparisons, then Windows export, actual-PCK chart/
audio probes, full dependency/CRC/extracted-file checks. Use the build.py command
below (the historical guide retains older milestone output names).

```sh
python3 reconstructed/godot/build.py --godot /path/to/Godot_mono --pack-probe-godot /path/to/Godot_standard --templates /path/to/templates.tpz --notices /path/to/notices
```

Outputs: Arconist-R008-Windows-x64.zip, Arconist-R008-Technical-Evidence.zip and
r008-evidence/. New first choice is silent R008 practice (child at HUD6s); E025
native diagnostic is separate. All10 earlier chart choices/music are preserved.
Only owner Windows/graphical/physical-input qualification can accept playability.

Historical documentation follows; current supported scope is in R008.md.

# Godot reference prototype — R007

R007 adds bounded ordinary linear sky arcs to accepted R006: typed AFF, native
sample/cache geometry, camera-ray Z0 input, continuous retained mouse contacts,
shared color ownership and checkpoint accounting. See [R007 report](../validation/R007.md),
[owner guide](PLAYER.txt) and
[reference provenance](../../reference_traces/r007/README.md).

Full logged packaging uses Godot4.7.2.NET / SDK10.0.402, DOTNET_PROCESSOR_COUNT=1:

```sh
python3 reconstructed/godot/build.py --godot /path/to/Godot_mono --pack-probe-godot /path/to/Godot_standard --templates /path/to/templates.tpz --notices /path/to/notices
```

Set DOTNET_ROOT/PATH and GODOT_NUPKGS to the chosen toolchain. Fresh hosts restore
with the project NuGet.Config first; no personal absolute NuGet paths are committed.
The full driver requires a clean committed tree and fresh r007-evidence output.
It executes all229 prior groups,54 new groups and three standalone comparisons,
then exports/verifies the actual PCK/runtime, ZIP CRCs and extracted-file hashes.
The new first choice is silent sky practice; all8 earlier charts/music remain.
Technical checks never qualify visible rendering or physical gameplay.

Historical documentation below remains for provenance; the R007 guide/report
specify current build paths and supported arc scope.

# Arconist R006 — pause and audible ordinary practice

Headquarters' R006 authorization records R005 accepted after owner qualification. Windows
launch, audibility, perceived synchronization, physical input, results and replay
remain owner-only qualification for R006. No graphical automation is authorized.

## Complete technical reproduction

Use Godot **4.7.2 .NET**, .NET SDK **10.0.402**, runtime **10.0.13**, Python3.11+
and matching4.7.2 **mono** templates. Put dotnet on PATH. Also obtain matching
**standard** Godot4.7.2 for the standalone exported-PCK headless GDScript probe.
Toolchains: https://godotengine.org/download/archive/4.7.2-stable/ and
https://dotnet.microsoft.com/download/dotnet/10.0.

Prepare a notices directory containing exactly GODOT-LICENSE.txt and
GODOT-COPYRIGHT.txt from Godot4.7.2, DOTNET-LICENSE.txt and
DOTNET-THIRD-PARTY-NOTICES.txt from Microsoft.NETCore.App.Runtime.win-x6410.0.13.
Commit source, then run from repository root:

```text
python reconstructed/godot/build.py --godot /path/to/Godot.NET --pack-probe-godot /path/to/Godot.standard --templates /path/to/mono_templates.tpz --notices /path/to/notices
```

GODOT_NUPKGS is derived from the editor's GodotSharp/Tools/nupkgs. The driver retains
**DOTNET_PROCESSOR_COUNT=1** for direct builds AND the exporter child SDK. Explicit
NuGet configuration supplies targeting packs on a fresh host; no personal path is
committed. Python assertions must remain enabled.

The driver generates32-second original WAV bytes, compares the published manifest,
checks64 beat windows, runs36 R001/15 R002/30 R003/33+15 R004 and37+17 R005 groups
plus29 R006 portable and17 R006 Godot groups (229 total) and three standalone R001 comparisons, compiles/imports/exports the real project,
probes music from the actual PCK and verifies self-contained dependency closure,
PE architecture, CRCs and every extracted hash. A nonzero command or Godot ERROR
line fails the driver. Existing evidence is never overwritten; archive it before
another complete run. No graphical Windows application is launched.

Outputs under reconstructed/out:

- Arconist-R006-Windows-x64.zip: EXE/PCK/complete runtime, README.txt, SOURCE.txt,
  notices and SHA256SUMS.txt.
- Arconist-R006-Technical-Evidence.zip: exact commands/exits, actual exporter
  MSBuild log, native comparisons, all group reports, waveform/exported-audio
  checks, integrity data and validation report.
- r006-evidence/: logs and extracted integrity copy. A prior export is moved aside
  and excluded from the evidence ZIP.

build.ps1 is the Windows build/export wrapper, including soundtrack generation and
serialization. Its PowerShell execution is NOT RUN on the Linux host. Use build.py
for complete logged ZIP packaging. Publication target is main without force.

## Audio and controls

See [PLAYER.txt](PLAYER.txt). Clockwork Steps has four count-in beats before the
first tap at music2s with O0. Second R005 choice has AFF+120; user−120 cancels it.
User offset is explicit integer milliseconds,−500..500,next run only,not persisted.
All six prior choices remain selectable and silent.

Kernel events expose latch→request→compensation at strict E>−O. The bridge loads
before creating the fresh clock origin and forwards one request synchronously to
one non-looping AudioStreamPlayer. Results/menu/replay stop and unload. Errors
are visible/logged and cannot write judgments/time. Playhead is diagnostic only.
Godot output substitutes for FMOD; hardware latency/audibility remain unverified.

Raw WAV uses a .wav.bytes carrier and explicit include_filter so export retains
raw data. Actual-PCK hash/decoder/player checks use Dummy output, not speakers.
See [audio source](../audio/README.md). No SFX, drift correction, profiles/legacy
migration, Bluetooth detection, full Android lifecycle, arcs/flicks, Android deployment or Unity.
R006 deliberately revises focus loss: pause and CANCEL all uncertain contacts;
focus gain never resumes. Manual pause retains contacts until delivered UP/CANCEL.

## R006 interruption contract

Escape/P or Pause activates a separate modal and freezes the model/timeline;
R/Resume explicitly refreshes paused compensation, seeks E−B=E+O, unpauses audio
and dismisses the modal. Godot's tree stays running; it is not a Director clone.
Paused frames clear activity but preserve retained IDs/latches/resolved records.
UP/CANCEL clean up during pause; new DOWN/mouse movement are gated. Resume samples
the current retained mouse location through the existing camera ray before the
next frame, preventing stale pre-pause lane support. No new DOWN is invented.

Optional IPausableBgmBackend leaves old R005 fake backend contracts/tests untouched.
The production backend retains one PCM playback. Godot4.7.2 player-level Seek is
ignored when paused; the adapter instead locks AudioServer, seeks the retained
playback, checks its cursor within one PCM sample and clears resampler history.
No Play(0) is used on resume. Diagnostics distinguish requested logical cursor,
verified pre-prefetch readback and decoder position including lookahead. This
engineering backend substitution is not physical sample-accurate scheduling.

A failed seek/unpause re-pauses audio, leaves model/timeline/modal paused and allows
retry or menu. Failed initial/pause output stops/unloads and requires a new run.
Audio errors do not reset E or award/expire notes. See PLAYER.txt for60-second,
retained/released/two-contact/offset/replay owner checks. All preexisting charts,
music, reference expectations and old test sources remain unchanged.
