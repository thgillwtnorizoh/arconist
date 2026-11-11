# Arconist reconstruction — R005

R005 adds the original CC0 soundtrack **Clockwork Steps**, an audible tap/hold
practice chart and an explicit per-run user offset. The independent kernel still
owns E/R/C; Godot playback position is diagnostic only. R004 is owner-accepted
according to the R005 authorization. R005 audible Windows qualification remains
owner-only. See [R005 report](validation/R005.md), [audio source/license](audio/README.md)
and [build/player guide](godot/README.md). The logged driver preserves all129 prior
groups and adds37 portable audio-contract and17 Godot headless groups.

The following R004 and R001 summaries are preserved historical context.

# Arconist reconstruction — R004

Current implementation adds ordinary holds to the independent core and accepted
Godot3D tap prototype. See [Godot build/player guide](godot/README.md),
[R004 technical report](validation/R004.md), [native hold references](../reference_traces/r004/README.md)
and [append-only history](contexts.md). Main is the final publication target.
Human qualification is owner-only. The R004 Windows package includes all runtime
dependencies; the owner does not need to compile it.

The following section documents the preserved R001 tap runner and its36-test
regression interface. R004 hold-specific tests live separately in `hold-tests/`;
the full Godot build driver executes both plus bridge/headless suites. Historical
R001 scope statements below describe that original runner, not the current Godot
or hold implementation.

# Independent ordinary tap kernel — R001

Portable `core/` targets .NET Standard 2.1. `headless/` and `tests/` target .NET 10;
the tested SDK is 10.0.402, Windows x64. No NuGet packages, engine, original archive,
ELF, Python or network are needed to build and run. The core has no native loading,
emulation, Godot or Unity dependency. `NuGet.Config` clears remote package sources.
The portable target builds against the installed reference pack. Godot and Unity
runtime compatibility has not been tested; no engine integration is claimed.

From the repository root, in PowerShell (RTK is the local standing wrapper; remove
`rtk proxy` on machines without it):

```powershell
rtk proxy dotnet build reconstructed/Arconist.slnx -c Release --configfile reconstructed/NuGet.Config -m:1 -nr:false
rtk proxy dotnet reconstructed/tests/bin/Release/net10.0/Arconist.Tests.dll .
New-Item -ItemType Directory -Force reconstructed/out
rtk proxy dotnet reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll research_harness/fixtures/ordinary_two_tap.aff reference_traces/r001/ordinary.schedule.json reconstructed/out/ordinary.json --reference reference_traces/r001/ordinary.reference.json
rtk proxy dotnet reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll research_harness/fixtures/native_late_input_expiry.aff reference_traces/r001/input-first.schedule.json reconstructed/out/input-first.json --reference reference_traces/r001/input-first.reference.json
rtk proxy dotnet reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll research_harness/fixtures/native_late_input_expiry.aff reference_traces/r001/frame-first.schedule.json reconstructed/out/frame-first.json --reference reference_traces/r001/frame-first.reference.json
```

The regression suite is a dependency-free executable, not a `dotnet test` discovery
project. Its exit code is nonzero for any failure; it prints the complete test
count, failures and skips. Every test is unconditional; no original archive switch
silently skips R001 tests. `validate.ps1` automates build, suite and all three real
runner invocations; outputs remain ignored in `out/`. On this host .NET compilation
requires normal Windows process permissions beyond the restricted tool process.
Workload resolution/telemetry are disabled by that script; no workload installation
or package download is required.

Runner usage: `CHART.aff SCHEDULE.json OUTPUT.json [--reference REFERENCE.json]`.
Exit0 means successful execution (and comparison if requested); exit1 means input,
execution, output or reference-validation failure. A computed trace with failed
comparison is preserved in the requested output and marked `validation: fail`.
The output's `status: computed` alone never claims native compatibility.

Schedules contain optional `epochMs` (default0), `userOffset` (default0),
`requestedSpeed` (default4) and metadata `baseBpm` (default178), plus an `events`
array. Every event has `wallMs` and `kind` (`FRAME`, `DOWN`, `UP`). DOWN has a pointer
ID and internal `lane`2..5; UP has the retained pointer ID. Input payload
`timestampMs` is ignored by ordinary judgment. Array order is authoritative at equal
wall time; no implicit sorting, coalescing or frame insertion occurs. Wall time must
be monotonic. Initial-input refresh advances E independently of last-frame E;
UP cleans contacts without refreshing E or judging notes.

Supported AFF: LF/CRLF headers AudioOffset and TimingPointDensityFactor; positive
ordinary default-group `timing(integer,float,float);`; ordinary taps
`(nonnegativeIntegerTime,integerRawLane);` with raw lanes0..5. Integer positions stay
typed and convert to native lane raw+1. At least one timing at0 and one tap are
required; duplicate timing times, nonpositive timing, unsupported syntax/headers,
float positions and malformed input fail explicitly. This is a bounded parser,
not a claim of full or malformed-native AFF compatibility. Ordinary input lanes2..5
are available; outer lanes1/6 require future widening support.

Frame processing: steady Timeline update -> active-range update using depth buckets
and retained-note state -> strict tap expiry -> strict chart completion/result.
DOWN: refresh Timeline -> collect active lane candidates (including resolved notes)
-> chronological sort -> guard/classifier -> first consuming result. Successful
consumption and missed flags are separate. Equal-time candidate ties use source
ordinal as an engineering choice; native equal-time stability remains unverified.

Ordinary gain, score, combo/max and result classification use 002/006/008/010/035
evidence. Float operations preserve single-precision stages, score uses integer
division, frame expiry does not recompute score, and final LOST reconciliation does
not replay gauge damage. Auxiliary bars and presentation objects are omitted because
they do not contribute judgment units; one default timing group is modeled. The
ordinary index/range path includes strict new-admission depth<300 and retained-note
hysteresis, avoiding a universal catch-up miss sweep.

See [reference authority](../reference_traces/r001/README.md), standing
[contract](Instruction.md), append-only [history](contexts.md), and
[validation evidence](validation/R001.md). Hold/arc/flicks, special gauges/skills,
pause/seek/lifecycle, physical Android input, audio, rendering, persistence, Godot
and Unity are outside the verified reconstruction boundary.
