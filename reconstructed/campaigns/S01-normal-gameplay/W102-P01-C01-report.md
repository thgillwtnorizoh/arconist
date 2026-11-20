# W102-P01-C01 — single-scene native judgment recovery

2026-11-20. **VERIFIED CHECKPOINT / PASS for this bounded research execution. S01 OPEN.**

## UEP-001 checkpoint

| Field | Result |
|---|---|
|Project / Campaign / Actor / Assignment|Arconist / S01 Normal Gameplay / Work1 Original Research and Independent Verification / W102-P01-C01, issue #9|
|Starting SHA|`c4e4c219214e3a55a4ffcab550ec59485d67e550`, verified remote main|
|Exact executed harness SHA|`fd11c2e013831f010412d4457fca04d85df7c2e9`, source published before execution; driver hash in ledger|
|Published SHA|Final evidence child of fd11c2e; exact final SHA and remote readback supplied in handoff / Git history|
|Objective / profile / changes|Recover raw-false/two-child child-input and cleanup ledger. One new observation driver; no reconstruction production changes. Linear color0, children1250/1500, group0, ordinary solo profile only.|
|Evidence / confidence|CONFIRMED ORIGINAL / native-integrated construction, normalization store, input, recording, cleanup. Synthetic fixture/schedule and inherited platform/ABI skips are ENGINEERING boundaries. No production independent QA claim.|
|Tests|Exactly one fresh native scene, exit0, completed. Offline audit385 PASS/0FAIL/0SKIP; zero additional native scenes. Source-integrity/preservation checks separate below.|
|Coverage gained|S01-05.01 / W102-C01–C05 / D07 B01: missing raw-false fixture judgment/negative controls now observed. No entire S01 category closed.|
|Discrepancies / limits|No differing compared gameplay field versus P01 trace Scene2. Historical mode0/N5 hypothesis remains refuted; actual prepared mode1/N2. Ordinary body+children, simultaneous ties, arbitrary child timing/modes, graphs, results NOT VERIFIED.|
|Updated records / reproduction|This report, w102-p01-c01/, appended coverage/dependency/discrepancy/history. Prior P01 assertion/source/budget/logs/fixtures untouched.|
|Next bounded task / Actor / dependencies|HQ review then separately authorize W102-P03 / Work1 if general child/mixed candidate conflicts remain required. Native collected/sorted vector and stopping ledger are still missing. No P03 executed.|
|Subsystem|OPEN|

## Preparation and original provenance

Remote matched assigned start; ancestry of P01 62e50fc and executed e780629 and
accepted reconstruction49e7c26 verified. Reused standing instructions, complete
previously read history plus new HQ checkpoint, S01 charter/registers, W1-02 and
P01 reports, source and native ledgers. Original E025 owning chain and read-only
Observer remain unchanged. New driver is derived from P01 run_two, uses only its
child schedule, and no longer requires a hypothesis about prepared mode or N.
Research-state differences are nonfatal observations. Missing ownership/backlinks,
nonfinite projection, broken clocks/ABI, results entry and budget violations remain
execution-integrity hard stops. Dead ordinary-body branches are retained source
heritage but disabled by a constant child-only schedule; none executes.

Original `lib/arm64-v8a/libcocos2dcpp.so` SHA256
`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`,
Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. Both verified.
Fixture is the unchanged [ordinary_two.aff](w102-p01/fixtures/ordinary_two.aff),
SHA256 `cbf47e5c83e070533bee8bc1b1e31b59209e452d43b612832f3cd02fad2cb0e1`.
Exact raw bytes also appear in the ledger; no replacement fixture was authored.
Original ownership: ee197c -> e2ea48 ->173b358 ->1862a14, factory173a778,
backlink writer1865514, sampler1925084 and geometry stores1925888/192588c,
count11ea120. Direct semantic host-call/replacement exclusions checked by the
unchanged Observer. Native-created scene/model/chart/parent/children/index/listener
and ownership relations are preserved in [native-ledger.json](w102-p01-c01/native-ledger.json).

The source was committed locally first (09a4bf6); shell push failed with missing
credentials. Connected GitHub publication supplied fd11c2e with identical source,
fetched and selected before native execution. No VM was created by these checks.

## Actual original observations

Parsed mode0 with children1250/1500. Read-only code hooks observed:

| PC | Parent | Stored +a4 | W24 supplied | W8 store operand |
|---|---|---|---|---|
|c66654, before STR|0x4331e40|0|0|1|
|c66658, after STR|same|1|0|1|

Thus P01's instruction-backed writer attribution now has direct native execution
support for this exact input. Prepared mode1/N2; three underlying parent records
1250/1500/1750, weight1 remain unresolved and do not add body awards. Two real
factory children have distinct identities and common native backlink. Geometry
(0,50,-2022.25)/(0,50,-4044.5), native camera projection on input plane Z0 gives
(640,593.0632781982422). Sampled Z is preserved. Source order1250 then1500 observed.

| Effective time / input | Native observation |
|---|---|
|1000 FRAME|parent admitted, both children unconsumed|
|1250 displaced DOWN/UP, generated ID0|spatial rejection, no recorder|
|1250 fresh DOWN/UP, ID1|child1250 PURE, consumed, score5000001, health bits1109445837|
|1250 fresh duplicate DOWN, ID2|first consumed guard, second error250; no award; ID2 retained|
|1375/1500 FRAME; MOVE ID2; repeat FRAME|child1500 stays unconsumed; no new recorder|
|1500 UP ID2; fresh DOWN/UP ID3|child1500 PURE, consumed, score10000002, health bits1117834445|
|1500 fresh duplicate DOWN/UP ID4|both consumed guards; no award|
|1501 cleanup FRAME|contacts/map/mask empty, result null|

Seven classifier entries, ten spatial observations, two accepted recorder callbacks
1730290. Intermediate health40.20000076293945 then80.4000015258789; final PURE2,
FAR0, LOST0, combo2, shining2. No body acceptance, results constructor or completion
path entered. [Normalized reference](w102-p01-c01/normalized-reference.json) keeps
raw/parsed/prepared/event observations separate. Allocation pointers are identities
within a scene, not portable regression constants.

## Independent offline verification and commands

Linux/Python3.12.14; isolated Unicorn2.1.4 / pyelftools0.33. Setup:

```bash
python -m pip install --target /tmp/c01-native-libs -r research_harness/requirements.txt
```

Exactly one native invocation from fd11c2e:

```bash
PYTHONPATH=/tmp/c01-native-libs python reconstructed/campaigns/S01-normal-gameplay/w102-p01-c01/run.py --archive ../project_sources/01-arccopy.zip --budget /tmp/c01-one-scene-budget.json --output /tmp/c01-native-ledger.json > /tmp/c01-native-host.log 2>&1
```

Exit0; budget1/1, no retry. **Do not rerun: authorization exhausted.** Host service
log remains outside source, its SHA256 in [command.json](w102-p01-c01/command.json).
The curated ledger captures original semantic observations, not a full memory dump.
A default-Python elftools import failed without isolated PYTHONPATH; corrected
isolated import/Build ID check passed. No native execution was repeated.

Safe offline audit:

```bash
python reconstructed/campaigns/S01-normal-gameplay/w102-p01-c01/audit.py
```

385/385 comparisons PASS, 0fail/skip. Independent oracle: immutable P01 Scene2
original-native ledger plus E006 binary32 arithmetic, never Work2 output. Compares
each scheduled event's E, counters/score/health, contacts/IDs, consumed/missed state,
parent state, candidates, classifiers, spatial and guard ledgers, callbacks and
cleanup; pointer identities excluded across scenes. No compared gameplay difference.
[Audit receipt](w102-p01-c01/audit-receipt.json) and
[first differences](w102-p01-c01/first-differences.json) preserve that distinction
from the raw0/prepared1 historical hypothesis difference. Native pass count1;
385 offline comparisons are not 385 native scenes or production tests.

Production at49e7c26 NOT RUN; historical regression, Godot, Windows, physical/audio,
results, P02/P03/P04 NOT RUN. No new owner qualification required for research.
Inherited E025 service/OBJ/math/JNI/render/audio/reclamation boundaries remain;
no original child/mode/count/judgment/score writes or semantic patches introduced.

## Preservation and next dependency

[Preservation receipt](w102-p01-c01/preservation.json) inventories all changed paths,
all original protected files and exact prefixes of the four appended records.
Executed driver stays byte-identical to fd11c2e. Non-forced main publication,
ancestry and exact remote-byte readback checked in handoff. All old P01 evidence,
research harness, fixtures, QA expectations and reconstruction code unchanged.

B01's specific missing raw-false/two-child execution is recovered. Parent W1-02
and P01 historical BLOCKED reports stay unchanged, not retrospectively relabeled.
P03 remains necessary for general mixed/tied candidate arbitration: these two
unequal-time children with sequential contacts establish neither equal-time sort
permutation nor tap/hold/child competing winners. Recommend HQ authorize P03 only
for that missing collected/sorted candidate-and-stop evidence; do not repeat these
solved construction/count/fresh-DOWN primitives. Graph P02/P04, widening and
G006/007/009/010 remain separate OPEN dependencies. No next task executed.
