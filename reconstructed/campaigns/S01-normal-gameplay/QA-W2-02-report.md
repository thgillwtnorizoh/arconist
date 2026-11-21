# QA-W2-02 — independent widening verification

2026-11-21. **BLOCKED — INDEPENDENT VERIFICATION INCOMPLETE.**
No production comparison executed. Two bounded build attempts failed; stopped under
the Hard-Rock rule. No additional package/configuration repair or runtime retry.

## UEP-001 checkpoint

|Field|Actual outcome|
|---|---|
|Project / Campaign / Actor / Assignment|Arconist / S01 Normal Gameplay / Work1 Independent Verification / QA-W2-02, issue12|
|Status|BLOCKED; no numerical/native-equivalence or production PASS claimed|
|Starting SHA|`e82f65c189bdc1a6bdc073c821e5300878334e90`, matched remote main|
|Exact production selected|`068a2f09698417b0ddd09e81ec274e758109a0bf`, isolated detached checkout, source bytes verified; **runtime tested SHA: NONE / NOT RUN**|
|Published SHA|Final non-forced main child, exact SHA and remote readback in handoff / Git history|
|Objective / supported profile / changes|Independent E039 widening, world-input and integration QA for S01Mixed; new external driver, frozen expectations and fixture copies only. Production unchanged.|
|Evidence / confidence|E039 original observed scalars/pairs/recorder values reused; E004 instruction-backed normal spatial boundaries; E007 binary32 staging. Authored runtime assertions remain NOT VERIFIED. Pause/MOVE/replay, invalid inputs and unsupported grammar cases explicitly RECONSTRUCTED/ENGINEERING.|
|Tests|Build1 exit1 NU1301; targeted recovery build2 exit1 NU1100. Runtime0PASS/0FAIL/0SKIP; all new/historical executable cases NOT RUN. Static source/fixture identities verified separately.|
|Coverage gained / remaining|Reproducible independent suite and concrete toolchain prerequisite; **no new production verification coverage**. Gates A–E runtime and F independent disposition remain incomplete.|
|Discrepancy / limitations|Missing NETStandard.Library.Ref2.1.0 in CLI restore environment. No production divergence observed; absence of a runtime first difference is not equivalence.|
|Updated records / reproduction|qa-w2-02/v1 source/expectations/fixtures/logs/receipt; this report; appended coverage/dependency/discrepancy/history.|
|Next bounded task / Actor / dependencies|HQ separately authorizes Work1 toolchain recovery with official netstandard2.1 reference pack/package and reviewed NuGet setup, then frozen QA plus historical drivers. No recovery executed beyond attempt2.|
|Subsystem|OPEN|

## Source and independence

Fresh workspace required cloning the repository; main matched assigned e82f65c.
Exact production068a2f0 is an ancestor and was checked out separately. Later main
changes are documentation, not substituted gameplay source. Core/bridge file
hashes and three original fixture hashes are in [receipt.json](qa-w2-02/v1/receipt.json).
All original identities match the assignment. No original ELF execution, asin
recovery, W102-P03 continuation, graph/candidate expedition or GUI operation.

Reused standing instructions/history and Hard-Rock amendment, campaign records,
E039 sections2–8 and supporting E004 sections3–6 / E007 widening/frame equations,
actual Chart/Kernel/Widening/GameplaySession source and historical Work1 adapters.
W2 report/source inspected as implementation documentation; no W2 oracles.json or
development outputs were copied into independent expected values.
[expectations.json](qa-w2-02/v1/expectations.json) freezes native time/G/W samples,
world pairs, raw fixture provenance, positive note/contact/score/health values and
boundary cases. Exact fixture bytes copied from preserved original research sources.

## Authored executable scope — ALL NOT RUN

The C# adapter references the actual core and bridge projects at the explicit
ProductionRoot, not a reimplemented widening kernel or injected candidate result.
It compares intermediate binary32 G/W/previousG, event processed/dispatch state,
original start time, typed controls/N/end/lanes, actual world GroundPointer contact
IDs and once-only note recording, UP/CANCEL and E1501; E004 signed truncation,
asymmetric425 and strict depth boundaries; negative invalid coordinates; default
R010 and unsupported grammar rejection.

New integration test combines a retained world contact, 60-second pause, resumed
E751 staged float32 interpolation, CANCEL, MOVE without fresh DOWN, fresh judgment,
replay reset and Home cleanup. This is RECONSTRUCTED/ENGINEERING, not an original
E039 whole-session observation. No emitted result/expectation was fitted to actual
production: no executable result exists. Compilation itself remains NOT VERIFIED.
This is a preserved partial driver, not a claim that every gate's instrumentation
is complete. Strict DOWN-versus-transition chronology and relevant historical
46+37 tests must be checked in the resumed execution before a PASS disposition.

## Attempts, commands and first blocker

Official SDK10.0.402 installed nonprivileged in /tmp/qa202-dotnet from the Microsoft
blob URL in receipt, archive hash recorded; [SDK info](qa-w2-02/v1/sdk-info.txt).
The shell environment was fresh; two initial shell calls addressed expired prior
workspace paths and failed before any build, then a fresh clone succeeded.

With PATH=/tmp/qa202-dotnet:$PATH, DOTNET_ROOT=/tmp/qa202-dotnet,
DOTNET_PROCESSOR_COUNT=1, from repository root:

```bash
dotnet build reconstructed/campaigns/S01-normal-gameplay/qa-w2-02/v1/driver/Driver.csproj -c Release -p:ProductionRoot=/workspace/scratch/e83b3992fd3d/qa202-production -m:1 -nr:false
```

Attempt1 [log](qa-w2-02/v1/build-primary.log): NU1301, repository Godot NuGet
configuration expands to nonexistent local `%GODOT_NUPKGS%` source.

One materially different recovery used the temporary CLI config with package
sources cleared, leaving repository/production unchanged:

```bash
dotnet build reconstructed/campaigns/S01-normal-gameplay/qa-w2-02/v1/driver/Driver.csproj -c Release -p:ProductionRoot=/workspace/scratch/e83b3992fd3d/qa202-production -p:RestoreConfigFile=/tmp/qa202-nuget.config -m:1 -nr:false
```

Attempt2 [log](qa-w2-02/v1/build-recovery.log): NU1100, cannot resolve
`NETStandard.Library.Ref (=2.1.0)` for netstandard2.1 core/bridge. SDK10 presence
alone does not establish that reference prerequisite. The cleared config was an
unsuccessful recovery, not a recommended final restore setup. **Stop here: no
additional download/source change/build attempt was made.** No DLL test invocation,
historical runtime regression, CI or export occurred.

After separately authorized prerequisite recovery, proposed runtime command:

```bash
dotnet reconstructed/campaigns/S01-normal-gameplay/qa-w2-02/v1/driver/bin/Release/net10.0/Driver.dll reconstructed/campaigns/S01-normal-gameplay/qa-w2-02/v1 /tmp/qa-w2-02-runtime.json
```

This command is **NOT RUN**. Historical drivers are source-pinned to earlier
production in their Python wrappers; use an independently reviewed compatibility
adapter/project to run their immutable C# expectations against068a2f0, explicitly
recording actual production identity. Do not edit old manifests or silently bypass
provenance labels. Their 83 cases remain NOT RUN by Work1 on this assignment.

## Owner boundary, preservation and disposition

Owner-submitted Windows desktop qualification:68PASS/0FAIL/1NOT TESTED, F10 physical
touchscreen NOT VERIFIED. Evidence:
https://github.com/thgillwtnorizoh/arconist/issues/11#issuecomment-7059883251.
Accepted as submitted; Work1 did not independently witness or repeat those cases.
The owner has no reported defect and is not asked to repeat successful tests.

[Preservation receipt](qa-w2-02/v1/preservation.json) lists every changed path,
protected file identity and exact four append-only record prefixes. Production,
Work2 report/oracles, original research and prior QA expectations unchanged.
Non-forced main publication, ancestry and full remote byte readback in handoff.
No W2-02 independent acceptance recommendation yet. Headquarters may resume after
an explicitly bounded toolchain recovery; no new production or native task follows.
W102-P03 remains PARKED, G006/007/009/010 and S01 remain OPEN.
