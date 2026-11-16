# W1-01-C01 — Toolchain recovery and independent runtime execution

## UEP-001 checkpoint

**Project / Campaign / Actor / Assignment:** Arconist / S01 Normal Gameplay / Work1 Independent Verification / W1-01-C01 (issue4).

**Status: VERIFIED CHECKPOINT** for the declared executable R010 CLI corpus. **Subsystem: OPEN.**

**Starting SHA:** `34d489ebcc9167f6f10a64be833a2226ced6d412`, matched remote main. **Published SHA:** final handoff. **Exact independently runtime-tested production SHA:** `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`. Prior partial `8efecf48638ecd7d963277a644501594e41b0636` and production are ancestors. Separate detached checkout preserved earlier workspace changes. Core/bridge production source bytes and project files match the tested SHA; no production mutation.

**Objective / supported profile / functional changes:** recover SDK10.0.402 and execute the existing independent C# driver against R010's bounded accepted profile. No harness correction, expected-value change or gameplay implementation was necessary.38 runtime-baseline scenarios plus8 declared rejection scenarios executed successfully. Four producer-blocked scenarios were deliberately not executed and remain NOT VERIFIED.

**Evidence / confidence:** INDEPENDENTLY VERIFIED only for the fields actually asserted in these case ledgers, using previously authored original-derived values; original NI/NX/IB/reconstructed distinctions remain. Fake audio, relative wall origin and already projected sky coordinates are ENGINEERING boundaries. The thirteen historical suites retain Work2 test provenance and are counted separately. No fresh original ARM64 experiment.

**Tests:** Release build0, zero warnings/errors. Independent46/46 PASS, failures0/skips0; four research-blocked NOT RUN. Confirmatory run46/46 PASS with byte-identical full serialized snapshots. Historical13 CLI suites319/319 PASS, failures0/skips0; three standalone native-normalized comparisons pass with9/6/6events. Logs and receipts are linked below. Godot projection/spatial suites, export, audible output and physical Windows qualification NOT RUN.

**Coverage gained / remaining:** closes the missing CLI SDK/execution gate for the selected corpus; independently checks actual intermediate time/contacts/candidates/records/health/result state where specified. It does not independently verify every exposed snapshot field or entire S01 requirement. Curves/crossing bypass/general graph/group/child combinations remain outside the supported baseline. G006/007/009/010 unresolved.

**Discrepancies / limitations / blockers:** no actual first difference in the46 executable cases. Empty firstDivergences is a result of executed comparisons, not the former blocked preflight. SDK blocker recovered. Godot4.7.2.NET remains unavailable locally but is not needed for this driver and is not a CLI-baseline blocker. Original normal-play completeness and broader platform qualification remain open.

**Updated records / reproduction:** new report and results/c01 receipts/logs; append-only coverage/dependency/discrepancy/history updates. Existing preflight.json, all50 specification files, raw AFFs, references, test source and driver source preserved unchanged.

**Next bounded task / actor / dependencies:** Headquarters may authorize Work2 W2-01 coherent typed-chart/group/curve/crossing/contact integration using existing original evidence and this verified baseline. Work1 W1-02 must close demanded graph/child conflict expectations before extending claims. Work1 independently verifies each exact production delta; owner later qualifies final integrated Windows corpus. No next task started here.

## Isolated official toolchain recovery

Linux x64 Debian13, glibc2.41, Python3.12.14. Installed below `/workspace/scratch/e83b3992fd3d/toolchain-c01/dotnet`; no system directories changed. SDK10.0.402/runtime10.0.13/MSBuild18.9.15. The SDK10 tar lacks NETStandard.Library.Ref. Retrieved SDK6.0.428 solely to extract `packs/NETStandard.Library.Ref/2.1.0`; did not install/use SDK6 or change project targets.

Archives and metadata came from Microsoft's HTTPS `dotnetcli.blob.core.windows.net/dotnet/` distribution. For each SDK, SHA512 equals the exact linux-x64 tar hash in official `release-metadata/{10.0,6.0}/releases.json`. Metadata lists the equivalent builds.dotnet.microsoft.com artifact. That host's diagnostic HEAD timed out once; the official blob download succeeded, with no repeated installation loop. See sdk-provenance.json and reference-pack-provenance.json for complete URLs/hashes. dotnet-info.log records actual SDK/runtime/RID. Archives/SDK/binaries are not committed.

Reproduction (set `C01_SDK` to the isolated verified installation; run from repo root):

```bash
export C01_SDK=/workspace/scratch/e83b3992fd3d/toolchain-c01/dotnet
export PATH="$C01_SDK:$PATH" DOTNET_ROOT="$C01_SDK"
export DOTNET_CLI_HOME=/workspace/scratch/e83b3992fd3d/toolchain-c01/home
export DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_PROCESSOR_COUNT=1
dotnet build reconstructed/campaigns/S01-normal-gameplay/independent-corpus/driver/Driver.csproj -c Release -p:ProductionRoot="$PWD" -m:1 -nr:false
python reconstructed/campaigns/S01-normal-gameplay/independent-corpus/run.py --production-root . --output /tmp/w1-01-c01-runtime.json
```

Official archive relative paths: `Sdk/10.0.402/dotnet-sdk-10.0.402-linux-x64.tar.gz` and `Sdk/6.0.428/dotnet-sdk-6.0.428-linux-x64.tar.gz`. Verify SHA512 against metadata before extraction; SDK6 extraction is limited to the reference pack. No NuGet packages required; repository source configuration clears remote feeds. global.json selects pinned10.0.402 when resolving the driver project.

## Per-category execution

Counts below are cases, not individual assertions; blocked and NOT RUN overlap on the same four cases. Skipped executable tests:0.

| Category | Pass | Fail | Blocked | NOT RUN |
|---|---:|---:|---:|---:|
| TAP | 17 | 0 | 0 | 0 |
| CHORD | 2 | 0 | 0 | 0 |
| HOLD | 6 | 0 | 0 | 0 |
| ARC | 1 | 0 | 0 | 0 |
| CHILD | 1 | 0 | 0 | 0 |
| LINK | 1 | 0 | 0 | 0 |
| GROUP | 2 | 0 | 0 | 0 |
| NOINPUT | 1 | 0 | 0 | 0 |
| PAUSE | 1 | 0 | 0 | 0 |
| REJECT | 8 | 0 | 0 | 0 |
| BLOCK | 0 | 0 | 4 | 4 |
| OFFSET | 3 | 0 | 0 | 0 |
| SESSION | 1 | 0 | 0 | 0 |
| ORDER | 2 | 0 | 0 | 0 |

Health is compared by exact IEEE754 bits. Arrays retain exact counts/order. The comparator checks the independently specified subset at each event and materializes actual snapshots before further mutation. No compiler errors, observation failures or genuine production divergence required repair; every original expected byte stays identical.

Runnable checks include classifier edges, both native chord orders, E035 chronological ordering/guards, six native-derived hold histories, moving geometry/contact/color/records, eligible child duplicate, natural linked flags0/1/six records/seven units and weighted callbacks, group reverse retention/depth, disabled tap filtering and E036 results, offset startup, frozen pause/seek requests and replay cleanup. Snapshot availability is broader than comparison coverage: e.g. Godot Camera3D ray projection and all signed index/query boundaries are not newly certified by this suite.

## Evidence files

All files under [results/c01](independent-corpus/results/c01/) are separate from the unchanged historical preflight receipt.

- [receipt.json](independent-corpus/results/c01/receipt.json): per-category summary, exact tested SHA and four NOT VERIFIED cases.
- [runtime.json](independent-corpus/results/c01/runtime.json): actual per-event snapshots and per-case firstDifference,46 executed cases.
- [build.log](independent-corpus/results/c01/build.log), [runtime.log](independent-corpus/results/c01/runtime.log): actual Release compilation and wrapper command.
- [repeat.json](independent-corpus/results/c01/repeat.json): recorded command/exit0 and byte-equal repeat SHA256. Identical full trace content is stored once rather than duplicated.
- [dotnet-info.log](independent-corpus/results/c01/dotnet-info.log), [sdk-provenance.json](independent-corpus/results/c01/sdk-provenance.json), [reference-pack-provenance.json](independent-corpus/results/c01/reference-pack-provenance.json): environment and official distribution hashes.
- [historical-commands.json](independent-corpus/results/c01/historical-commands.json): exact26 build/execute commands, exits/stdout/stderr for13 preserved CLI suites.
- [standalone-commands.json](independent-corpus/results/c01/standalone-commands.json): headless build plus three runner commands/exits/reference results.

To reproduce historical checks, use each logged project path with `dotnet build PROJECT -c Release -m:1 -nr:false`, then its Release/net10.0 DLL. Core tests take REPO_ROOT only; Godot bridge tests take no arguments; other logged suites take REPO_ROOT OUTPUT_DIR. Logs retain absolute actual paths; substitute only checkout/output location on another machine. No expectations are regenerated.

## Publication and preservation

The changed-file inventory and prefix/blob preservation check are in preservation.json. Publication is a non-forced child of the verified starting main, checked again immediately before write, with immutable remote file readback and parent-tree allowlist comparison. Exact final SHA is supplied in handoff. Old failed/blocked records remain intact; campaign updates are appended, not historical status rewrites. No binaries, official SDK archives, proprietary resources or new native experiments committed.

Stop at this independent CLI checkpoint. No Work2 implementation, R011, new campaign, graphical automation or S01 acceptance follows.
