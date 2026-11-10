# Arconist R004 — ordinary taps, holds and continuous contacts

The owner exclusively qualifies Windows launch, graphical appearance, physical
input, results and restart. This build is **READY FOR HUMAN QUALIFICATION** only
after the complete logged technical delivery. No GUI automation, input injection,
graphical playthrough or automated screenshot inspection is authorized.

## Build and delivery

Use Godot **4.7.2 .NET**, **.NET SDK10.0.402**, Python3.11+ and matching **mono**
export templates. `dotnet` must be on PATH. Godot packages are resolved from
`GODOT_NUPKGS` set by the driver to the editor's GodotSharp/Tools/nupkgs folder;
no developer absolute paths are committed. Explicit restore supplies fresh hosts'
missing .NET Standard2.1 targeting pack through the project NuGet configuration.

Obtain toolchains from https://godotengine.org/download/archive/4.7.2-stable/ and
https://dotnet.microsoft.com/download/dotnet/10.0. Prepare a notices directory with
GODOT-LICENSE.txt/GODOT-COPYRIGHT.txt from the Godot4.7.2 tag and
DOTNET-LICENSE.txt/DOTNET-THIRD-PARTY-NOTICES.txt from the
Microsoft.NETCore.App.Runtime.win-x64 10.0.13 NuGet package.

Commit all source, then from repository root:

```text
python reconstructed/godot/build.py --godot /path/to/Godot.NET --templates /path/to/templates.tpz --notices /path/to/notices
```

The driver rejects an uncommitted tree, runs the unchanged36 core/three reference/
15 bridge/30 spatial regressions, new33 core/bridge groups and15 headless Godot
hold groups, then imports/exports and verifies the Windows package. It preserves
the R003-C01 **DOTNET_PROCESSOR_COUNT=1** child-SDK mitigation and `.gdignore`
resource exclusions. It rejects nonzero exits AND Godot ERROR lines. No graphical
Windows application is launched. The Windows PowerShell build/export wrapper is
also available; the Python driver produces the verified ZIP and evidence package.

Outputs under `reconstructed/out`:

- `Arconist-R004-Windows-x64.zip`: executable/PCK/self-contained .NET10.0.13,
  owner instructions, notices, SOURCE.txt and per-file SHA256SUMS.txt.
- `Arconist-R004-Technical-Evidence.zip`: command/exit logs, actual MSBuild export
  diagnostics, native comparison traces, spatial/hold reports and package checks.
- `r004-evidence/`: logs, integrity JSON and extracted verification copy.

An existing evidence directory is never overwritten. Archive it before repeating
the full driver. A prior export is moved aside before a clean one is created.
Do not distribute previous-export as the new prototype. ZIP checks validate CRCs
and every extracted payload hash; the runtime's exported dependency closure is
checked, rather than trusting the EXE alone. All six AFF resource bytes are verified
inside the actual PCK. Publication target is **main**, without force pushing.

## Owner play

See [PLAYER.txt](PLAYER.txt). Extract everything and open Arconist.exe.
The default mixed practice contains taps and four holds. D/F/J/K retain one
contact each until UP; left mouse provides a separate contact in a projected lane.
Holding J plus left mouse on the J ground region, then releasing J, tests
same-lane continuation. Briefly release and press again to test reacquisition.
Mouse movement updates retained lane membership without classifying a fresh tap.

Selectable charts: new mixed practice; unchanged16-tap practice; unchanged two-tap
reference; byte-identical E026 hold; E037 hold-first and tap-first fixtures.
The HUD includes chart descriptions, hold activity/contact/unit status, checkpoint
feedback, results and replay. F6/F7/F8 remain owner-operated view/resize/capture.
Focus loss releases contacts while chart time continues; pause is deferred.

## Native evidence and engineering boundary

[Reference ledger](../../reference_traces/r004/README.md) identifies E001/002/008–010/
026/027/035/037. `core/Chart.cs` creates ordinary flag0 interior hold records with
f32 stages. Raw integer lanes1..4 map to internal2..5. The supported hold domain
has duration>=2ms, nonnegative times below INT_MAX−1,000,000, finite interval>=1ms,
unique strictly interior integer checkpoints, <=100000 generation steps and a
bounded positive-depth bucket span. Unsupported forms fail explicitly. This keeps
the original R0011ms invalid-domain regression intact; it does not claim arbitrary
short/large/native malformed AFF compatibility. Positive timing changes are retained;
hold interval uses the timing at start. No groups/reverse-scroll expansion occurs.

N=taps+checkpoint weights; end=max(tap+120,hold.end+500). Initial latch requires
start<E+100 and E<end; continuous activity requires latch and start<E<end and
matching retained contacts. DOWN never inserts FRAME. Activity resets every frame;
UP removes retention, leaves latch and does not advance E. All matching contacts
can sustain the same hold. Initial chronology and the unconditional hold latch
stop reproduce E037 A1/A2/B. Source order breaks equal-start ties as an existing
engineering rule, not a universal native priority claim.

Checkpoint handling uses due trunc(f32(E+interval/2)) and the original inactive
half/overdue cutoff distinction. Ordinary factory+6c starts0; advanced flag/mode
producers are not supported. Records resolve backwards through a pending prefix;
per-unit recorder/clamp calls apply gain or2HP damage once. The renderer only reads
these results. Native E026/E037 stop before results; composed full hold sessions are
reconstruction tests. E008/009 independently supply the overdue-to-results case.

Hold bodies/heads/checkpoint marks are real BoxMeshes; body endpoints use the same
integer-predepth/float-add depth model as taps. After the start crosses the line,
the visible front is clamped to Z0 while the tail approaches. Amber/green/red,
geometry sizes, clipping, shrink policy and brief checkpoint markers are functional
presentation choices, not native mesh/material fidelity. Fresh kernels replace old
note/hold visual trees. Native coordinates/425, FOV65, single camera and safe ground
ray picking remain the accepted R003 approximation.

No audio, arc/arc-tap/flick, widening, special gauge, character, full pause, Android,
persistence, original shader fidelity or Unity work is included. Headless evidence
never establishes visible graphical correctness or human playability.
