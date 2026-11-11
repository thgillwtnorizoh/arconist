# Arconist R005 — audible ordinary practice

The owner accepted R004 according to Headquarters' R005 authorization. Windows
launch, audibility, perceived synchronization, physical input, results and replay
remain owner-only qualification for R005. No graphical automation is authorized.

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
plus three standalone R001 comparisons, compiles/imports/exports the real project,
probes music from the actual PCK and verifies self-contained dependency closure,
PE architecture, CRCs and every extracted hash. A nonzero command or Godot ERROR
line fails the driver. Existing evidence is never overwritten; archive it before
another complete run. No graphical Windows application is launched.

Outputs under reconstructed/out:

- Arconist-R005-Windows-x64.zip: EXE/PCK/complete runtime, README.txt, SOURCE.txt,
  notices and SHA256SUMS.txt.
- Arconist-R005-Technical-Evidence.zip: exact commands/exits, actual exporter
  MSBuild log, native comparisons, all group reports, waveform/exported-audio
  checks, integrity data and validation report.
- r005-evidence/: logs and extracted integrity copy. A prior export is moved aside
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
migration, Bluetooth detection, native pause, arcs/flicks, Android or Unity.
Focus loss releases contacts while time/music continue, preserving R004 policy.
