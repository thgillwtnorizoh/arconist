# QA-W2-03 — read-only persistence QA preflight

2026-11-22 (Asia/Bangkok). **BLOCKED / NOT RUN — INDEPENDENT VERIFICATION INCOMPLETE.**
The mandatory prerequisite gate failed. No restore, build, SDK/package installation,
production assembly execution or QA-W2-02 recovery retry was attempted.

## UEP-001 checkpoint

|Field|Actual result|
|---|---|
|Project / Campaign / Actor / Assignment|Arconist / S01 Normal Gameplay / Work1 Independent Verification / QA-W2-03, issue14|
|Status|BLOCKED at mandatory read-only preflight, not a production FAIL|
|Starting SHA|`60cb46ec2b0edde5b9efc4548fc91e048dad9895`, matched fetched main|
|Production selected / exact tested SHA|`0007c7719eb9b3ea377230a55d6fcfaedbe29898`, detached checkout and18tracked core/bridge/records file hashes verified. **Runtime-tested SHA NONE / NOT RUN.**|
|Published SHA|Non-forced main evidence child; exact SHA and remote readback in checkpoint handoff / Git history|
|Objective / supported profile / changes|Preflight-gated E013 original-rule and actual JSON/session persistence verification. Partial independent expectations and reproducible preflight only; no production changes.|
|Evidence / confidence|E01342clear comparator pairs are CONFIRMED ORIGINAL, native-isolated authority reused; strict score writer/clear progression native-integrated at original private in-memory SQLite boundary. Six-step sequence is RECONSTRUCTED; JSON durability/lifecycle are ENGINEERING. No production verification obtained.|
|Tests|One read-only preflight command exit2 (expected blocker disposition).0build/restore/install attempts;0runtimePASS/0FAIL/0SKIP; gates A–D NOT RUN. Separate static expectation validation is not a runtime pass.|
|Coverage gained / remaining|Toolchain state, exact source/archive identity and independently frozen42-row table/sequence. No new executable persistence, session, durability, regression or mutation coverage.|
|Discrepancies / limitations|No .NET host/SDK/runtime found in enumerated locations; no netstandard2.1ref package/cache or local Core/Bridge/Records assembly set. No production first difference can be established.|
|Updated records / reproduction|This report, qa-w2-03/v1 preflight/source/expectations/receipts/preservation; appended campaign registers/history.|
|Next bounded task / actor / dependencies|Headquarters resource decision: provide an already validated .NET10+netstandard2.1 environment or verifiable runnable exact-build dependency set before reauthorizing Work1 runtime QA. No installation/repair or next issue started.|
|Subsystem|OPEN|

## Authority, source identity and read-only scope

Read Issue14 in full (zero comments), including its explicit stop before build and
prohibition on third QA-W2-02 recovery. Fetched remote main exactly60cb46e; isolated
0007c77 checkout. Read standing instructions and Hard-Rock addendum, retained history
and new W2-03 entries; S01/previous QA context, original E013 report and inspected
actual records/SessionRecords/project/NuGet interfaces plus the Work2 handoff as
implementation context. No Work2 `E013-oracles.json`/record-test expected outputs
were used to prepare the independent table.

[Read-only preflight receipt](qa-w2-03/v1/preflight.json) records18direct file hashes
at the exact production revision; no newer code substituted. Original archive member
SHA256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`
confirmed by ZIP read, with no extraction/emulator/native execution. Archive is not
a .NET dependency or redistributable asset. Local source checkouts and
project_sources were the available workspace inputs; no W2-03 release package or
technical archive was attached locally. No external package was downloaded.

## Deterministic preflight blocker

Python3.12.14 on Linux6.18.57/glibc2.41. `dotnet` is absent from PATH. Checked:

- Prior `/tmp/qa202-dotnet` SDK location: absent in this session.
- `/usr/share/dotnet`, `/usr/lib/dotnet`, `/usr/local/share/dotnet`, `/opt/dotnet`
  and current-user `.dotnet`: absent.
- `NETStandard.Library.Ref/2.1.0` in those SDK roots and current-user NuGet cache:
  absent at enumerated locations.
- Workspace Core/Bridge/Records DLL candidates: none. No local verifiable exact-build
  assembly fallback and no runnable .NET host found.
- `GODOT_NUPKGS` is unset. Tracked Godot NuGet config contains that placeholder
  plus nuget.org; root reconstructed NuGet config clears sources. Neither was changed.

These are bounded availability observations, not a claim about all machines or the
owner's installed toolchain. Work2's prior successful environment is not evidence
that its dependencies exist here. The previous SDK was transient; its disappearance
is recorded instead of silently reinstalling it. The first missing prerequisite
is already a hard stop; no speculative restore was used to rediscover NU1301/NU1100.

Exact command, from repository root:

```bash
python reconstructed/campaigns/S01-normal-gameplay/qa-w2-03/v1/preflight.py --production-root ../qa203-production --workspace .. --output reconstructed/campaigns/S01-normal-gameplay/qa-w2-03/v1/preflight.json
```

Exit2. The script only reads Git/source, dependency paths/configs and archive member;
it writes the requested evidence JSON. It never invokes dotnet, restore, build,
production assemblies or native routines. Source checkout creation and evidence
publication are separate repository operations, not toolchain repair. The old
QA-W2-02 failures/source/expectations remain untouched.

## Frozen independent original expectations — not executed

[expectations.json](qa-w2-03/v1/expectations.json) preserves all42booleans with
old−1..5 and incoming0..5. Each row comes from E013's explicit accepted-new-type
sets, not production's rank switch or Work2's generated expected values.

|Stored old|Accepted incoming types, E013|
|---|---|
|−1|0,1,2,3,4,5|
|0|1,2,3,4,5|
|4|1,2,3,5|
|1|2,3,5|
|5|2,3|
|2|3|
|3|none|

Original comparator `0xe3c054`, normalization `0x196b22c`; strength interpretation
0<4<1<5<2<3. Original score writer `0x13552d4` skips score DML when signed old>=new;
score snapshot/date remain unchanged. Clear writer follows separately when
`w2&1` permits it, including lower/equal score. Category0 may save through the
supported ordinary helper when its outer gates allow it; early quit is not that
completed result path. Original final LOST+20 differs from recorded LOST+24.
These native SQLite rules do not establish JSON bytes, lock/backup/crash policy,
full chart catalog identity or real session integration.

The independently authored six-step proposed sequence covers first save, equal
score with stronger clear, lower score with stronger clear, higher score with
weaker clear, further higher score and equal score promoting strongest clear while
retaining the entire prior best-score snapshot/date. It is a RECONSTRUCTED rule
composition, not a new native six-step observation. Invalid stored JSON category
handling remains an explicit ENGINEERING contract. Static validation checks its
provenance/shape; no actual production comparison is represented by it.

## Static expectation validation (no toolchain or production)

The first offline helper invocation failed before checking expectations because its
relative repository-root index pointed to reconstructed/ instead of repository root.
Corrected that helper path only, without changing expectations, production or any
dependency. The final `python .../qa-w2-03/v1/validate.py` receipt is
[static-validation.json](qa-w2-03/v1/static-validation.json). These are static
source-table/sequence/provenance checks, not executable production QA or a retry of
the blocked prerequisite. Preflight was run once; no dotnet command was issued.

## Mandatory gates: actual disposition

|Gate|Disposition|
|---|---|
|A original rule fidelity|42-row expectations and proposed sequence frozen; production comparator/snapshot tests NOT RUN|
|B actual integrated session|Completed GameResult→SessionRecords→disk, once-only writes, final/recorded LOST/category0 and26chart identity isolation NOT RUN|
|C engineering disk durability|Fresh writer/reader processes, lock/conflict/schema/errors/backup/in-memory rollback NOT RUN|
|D regressions/mutations|Preserved46R010+37W2-01 corpora and earlier QA-W2-02 files; execution and both required mutations NOT RUN|
|E publication|Partial static evidence and blocked checkpoint published; no independent runtime acceptance|

No executable verifier was built or run because the prerequisite gate forbids it.
No file durability ledger, fresh-process production record hashes, numerical
production verdict or first runtime divergence exists. `firstProductionDifference`
null in the receipt means NOT OBSERVED, not equality. Work2's590groups/83cases/
3references/62commands/two-process proof retain Work2 provenance only.

## Owner boundary, preservation and stop

W2-03 owner physical record-save/relaunch qualification remains PENDING; not
simulated. W2-02's owner68PASS/0FAIL/F10touchscreen NOT TESTED remains a separate
historical desktop result, not W2-03 persistence acceptance. No GUI, Windows export,
ARM64, asin recovery, W102-P03 continuation or scope exclusion.

[Preservation receipt](qa-w2-03/v1/preservation.json) inventories every changed path,
protected file identity and all four prior record byte prefixes. Exact non-forced
main ancestry and remote-byte readback supplied in handoff. Original research,
production/Work2 evidence, historical test expectations and prior blockers intact.
No new independent runtime coverage gained; D13/S01-14.05 and QA remain OPEN.

Stop at this deterministic blocker. Headquarters should decide whether to supply a
validated environment or exact-build runtime dependency package with verifiable
provenance, then separately authorize resumed Work1 QA. This is not permission to
install/reference-pack-repair under the old blocked QA-W2-02 budget or start another
issue. S01 remains OPEN.
