# Expedition 035 — Native JNI Late-Input vs Expiry Arbitration

Date: 2026-10-28. Parent: `4ab959546accee3ee18c0870198f5b01e7942471`. Headquarters selected Scout002 S2-C01 as permanent **G-011**.

## Result

**Verified — G-011, within this controlled ordinary native-owned scene and two event/frame interleavings.** Two fresh emulators independently construct the same chart and admit both unresolved same-lane taps at E1000. Delivering original JNI DOWN at E1110 before the model's expiry frame consumes iteration as LOST on the older note; running the original Director frame first expires that note and allows the same projected contact to judge the newer note as shining PURE. Original recorder/caller/guard/write evidence establishes the cause. Both UPs clean native mappings/slots/retention.

| At E1110, after both scheduled operations | Input first | Frame first |
|---|---:|---:|
| Recorded PURE / FAR / LOST | 0 / 0 / 1 | 1 / 0 / 1 |
| Shining PURE | 0 | 1 |
| Score | 0 | 5,000,001 |
| Current combo | 0 | 1 |
| Live health | 0 | 40.20000076293945 |
| Older note missed / successful-consumption byte | 1 / 0 | 1 / 0 |
| Newer note missed / successful-consumption byte | 0 / 0 | 0 / 1 |
| Initial candidate that stops iteration | older1000, LOST | newer1109, shining PURE |

A classifier return true means initial input was consumed; it is not equivalent to the ordinary successful-hit byte at note+0xd. The comparison outcome was recorded, not required as a historical expected value. No gameplay state was repaired.

## Preparation, identity and source provenance

Original project instructions, cumulative context/backlog and Scout002 findings were reviewed, together with relevant002/004/008 Section11/009/010/011/018/022–024/027/032 reports and actual harness source/fixtures/assertions. Main matched the stated parent, no035/late_input_expiry path existed, and all62 locally present parent files matched their GitHub Git-blob hashes before editing. Historical content is retained through the parent tree.

The actual local execution environment is available again; no vanished emulator state is presumed recovered. The original read-only ZIP member `lib/arm64-v8a/libcocos2dcpp.so` was freshly verified as SHA-256:

`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

Original code addresses below are **ELF virtual addresses**. Object pointers are **emulated runtime observations**, not regression constants. Python3.12.14/Unicorn2.1.4/pyelftools0.33 pins remain unchanged. External Capstone5.0.7 performs targeted disassembly only; it is not a new harness dependency.

**Native-integrated:** original connected scene/loading/Director/JNI/gameplay instructions. **Instruction-backed:** decoded decision semantics. **External supplied input:** catalog/platform/ABI/resource services, synthetic chart, wall clock and JNI values. **Interpretation:** conclusions beyond observations. **Unknown/not_run:** actual Android queue scheduling, hardware/audio/GPU behavior, later chart completion/results for this fixture.

## Synthetic AFF and original construction

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(1109,3);
```

Fixture SHA-256: `6171b14b3abd096e494183206ac7465adf6ab694a573f14b1b55b9ba0ed85f71`. This is research input, not an archived song chart. Existing ordinary metadata remains sayonarahatsukoi/difficulty0/base/no purchase/mode0/speed40/no map or modifier and forty zero PlayParameters bytes. The resource-provider boundary supplies the full bytes, not parsed objects. Complete original static1930604 and registry1054f24 are reused.

In each run original ee197c eligibility returns1 at ee2214, native latch becomes1, allocationee29a8 calls constructoree29e8→e4e4dc with LR ee29ec. Loading Scheduler/ActionManager invokes original e2ea48, genuinely returning1; Director activates that same GameScene. No multiplayer helper or direct driver scene/model construction/initialization is used.

Whole parser1870de0/body lexerdf4a58/parserb01d6c/chart initializer173b358/builder1862a14 produce two parsed10SimpleNote and two original12LogicTapNote products. At18640d8 raw integer3 and time1000/1109 feed the native initializer;18640dc returns1 on both. Original converted NotePosition stores internal lane4, equal start/end times and input-enabled byte1. Native count11ea120 gives N2; chart end1229. Native MD5 stored at chart+f8 is `436bcfdd8c305c45232b4cb6bb4127eb`, independently compared with the exact fixture bytes.

One native timing list contains start INT_MIN/end1001229, raw BPM120, scaled BPM485.39324951171875 and float32 scale0.12361110746860504. Native metadata BPM178 normalizes requested speed4 to4.044943809509277 as in earlier ordinary scenarios. Original index1576aa4 executes505 times including auxiliary bars; both taps are members of group0 bucket0. Bars do not increase N.

Example relational identities within each independent emulator: scene4327c40/model4355f40/chart4331980/timeline43560c0/ScoreState4356100/gauge4356280/rig4368880/primary camera4368bc0; older tap4332240, newer4332340. Scene+3e0/+3e8 and model+28 agree. The same numeric addresses in fresh emulators do not imply shared memory or cloned state. Assertions compare identities within runs and normalize pointers for precondition comparison.

## Shared precondition and original projection

Native loading activation is followed by Director preroll, original music anchorwall9452/E0, and a Director framewall10452/E1000. Each ordinary listener is registered1/enabled1/paused0. Both native taps are active, input-enabled, missed0/consumed0/contactID−1; depths0 and−881. Score/PURE/FAR/LOST/shining/combo/H are0, engine mapping/mask/retained contacts empty, finished0 and result cache null. Director counter5/scene stamp4 reflect the original post-frame counter increment, not host counter assignment. Both normalized preconditions match exactly.

Using native lane4 semantics gives an external input-plane center(212.5,0,0). Original camera projectionbdbb70 and Director height720 produce JNI(775.8657836914062,617.340705871582) in both runs. These are derived in the common precondition; no camera action changes this scene. At DOWN the original unprojection returns approximately(212.4925537109375,0,0), primary lane4/secondary0. The host supplies only the projection input buffer and resulting JNI event coordinates, not a note position, matrix, lane result or candidate vector.

## Case A — input before E1110 frame

Only the external clock advances110ms towall10562. Before input, native timeline/last-model time remain1000. JNI DOWN42 atbe31a8 reaches original GLView, EventDispatcher, registered listener194ff80 andeec024. The initial routine updates native timeline toE1110 without a model frame; Director counter/stamp and last-modelE remain5/4/1000.

At eec4e0 and after original f6b514 at eec4f0, the candidate vector is [older1000,newer1109]. This fixture already has chronological collection order; execution proves sorter invocation and output, not an actual reorder in this two-element sample. Original sorter instruction evidence from004/008 establishes its signed-start-time key, not absolute timing-error priority.

Older tap classifier160ce28 observes missed guard0 at160ce58, successful-consumption guard0 at160ce6c and native absolute error110 at160cec0. Its >100/≤120 branch reaches **160cff4→868e54**, observed recorder LR **160cff8**, on the older native pointer at nativeE1110. Original guard virtual+38 calls7e995c and stores note+c=1 at7e9968. Original868eac increments LOST0→1;133fb50 stores health0 after ordinary damage/clamping;868fdc stores combo0. Health at its lower clamp does not mean no native gauge application occurred.

Classifier reaches160ce74 with consumption result1; eec56c observesW0=1 and original eec570 stops on the older pointer. No classifier call reaches the newer tap; accepted recorder1730290 and acceptance965e28 counts0. Older successful-hit byte+d stays0 and acceptedID stays−1. This is a real recorder-produced LOST consuming the initial event.

UP throughdda71c/f9a50c clears engine mapping/slot0/mask and retained vector without changing note or score state. The subsequent original Director frame runs at the samewall10562/E1110: one model entry despite four scene visits. Range processing removes the already-missed older tap before expiry processing; no duplicate miss occurs. Newer tap remains active/unresolved at depth8. Final score0/combo0/PURE0/FAR0/LOST1/H0.

## Case B — E1110 frame before input

A fresh emulator independently reproduces the same precondition and projection. Atwall10562 the original Director→GameScene visit→GameModel frame executes first. Original f8056c processes the active taps. At f80a58 the observed operands are older E1110/cutoff1100, newer E1110/cutoff1209. Original BLE means equality would not expire; the older passes the strict E>end+100 decision.

Original **f80b70→868e54**, LR **f80b74**, records the older LOST atE1110. It uses the same original7e9968 missed-byte write and LOST/health/combo writes as Case A, but with different native caller provenance. Immediately after this frame the older is **still in the active vector**, now missed1/depth890. The range updater ran before this frame's expiry write. Newer remains active/unresolved/depth8.

JNI DOWN42 then observesE1110/last-modelE1110. Candidate collection and sorting still contain **both taps** [1000,1109]. The older classifier reads missed guard1 and returns0, so eec56c continues. The newer classifier reads missed0/consumed0, computes native error1, calls **160cf44→1730290** (LR160cf48), judgmentID0, native time1110/generated contact0. The recorder's original virtual acceptance reaches965e28;965e68 writes newer+d=1 and965e6c writes its accepted contactID0. Original173030c/1730318 increment shining/PURE; native gauge and score/combo writes produce score5000001/combo1/PURE1/FAR0/LOST1/H40.20000076293945.

The newer returns1; original eec570 stops on that pointer. UP clears engine mapping/slot/mask and retention without another judgment. No extra post-input model frame is added in this case: the prescribed comparison has one E1110 frame on either side of the event. Thus older active membership at the endpoint differs from Case A; it is not treated as inconsistent state or manually equalized. Further active-range removal in Case B is not executed here.

## Identity, recorder and frame audit

Each DOWN creates Android42→engine slot0→native Touch→generated gameplay0, retained through original listener processing. Observed Touch allocations differ (4ecb300 versus4ecb380), while the within-run mapping/retained-pointer/slot identity checks pass. Neither generated IDs nor heap addresses are required cross-run constants.

| Observed entries per complete case | Input first | Frame first |
|---|---:|---:|
| ordinary entry/allocation/constructor/initializer | 1 each | 1 each |
| parsed-to-runtime tap initialization | 2 | 2 |
| native index producer, including bars | 505 | 505 |
| JNI DOWN / UP / gameplay begin / cleanup | 1 each | 1 each |
| candidate sort | 1 | 1 |
| classifier | 1 | 2 |
| miss recorder | 1 | 1 |
| accepted recorder / ordinary tap acceptance | 0 / 0 | 1 / 1 |
| model frames / expiry passes | 5 / 5 | 5 / 5 |
| GameScene visits | 20 | 20 |
| completion / snapshot | 0 / 0 | 0 / 0 |

Both comparison Director frames yield four scene visits and one guarded model update. JNI causes no model frame. Read-only instruction hooks preserve classifier guard values/returns, callerW0, actual stopping pointer, before/after-sort vectors, recorder caller PCs and native state before/after each recorder. Memory hooks preserve native note flags/contact IDs and score/gauge writes. Automatic assertions check recorder-produced counter deltas, per-note no repeated0→1 resolution writes, original ownership and cleanup. No final synthesized LOST is involved: both result caches are null, E1110 is below chart end1229, and completion/snapshot counts0.

## Relation to Expedition 008 and scientific limits

The two observed outcomes agree with008 Section11, but strengthen its prepared-environment evidence with original ordinary entry, complete AFF construction, native ownership/index/admission, Director frames and JNI transport. The reason is not nearest-note selection. It is chronological candidate order plus distinct missed/consumed guards and frame/input ordering. A true classifier return for LOST must not be described as successful ordinary tap acceptance.

The targeted original disassembly and actual cutoff operands establish the strict expiry decision. No extra E1100/1101 experiment is required for this bounded comparison and none is claimed. No exhaustive judgment-window enumeration, actual GLThread batching or Android queue latency is established.

A diagnostic run completed both cases before the final instrumentation pass. Its timing-record observer initially read start/end at the wrong offsets; the observer was corrected to native+10/+14 and guard/iteration-stop observations added. No native memory or fixture was corrected. The authoritative final CLI independently executes both cases from fresh emulators and contains complete evidence; observations from diagnostic runs are not spliced into it. No substantial new native dependency or service blocker is encountered.

## Reproducibility and regressions

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario late_input_expiry \
  --output /path/outside/research_harness/late-input-expiry-result.json
```

Authoritative modified-source result: **exit0/status pass**, JSON47982 bytes, no native failures; all four per-case provenance gates pass. The JSON reports whether outcomes differ; a different coherent observed result would be evidence, not automatically forced to this table. Original setup/fixture/admission failures or incomplete provenance fail with partial evidence and explicit unstarted case status.

Fresh modified-source ordinary full-session/results/SQLite, chord forward/reverse, moving/crossing arcs, timing-group/reverse-scroll and CPU note refresh/expiry CLI runs all return exit0/status pass (30.249/47.799/61.961/58.089/62.285 seconds respectively). Existing unittest discovery executes native arc-tap, native hold dual-case, missing archive, unavailable-song original negative and wrong-binary-hash: all5 pass in66.583s, process exit0, no skips. New late_input_expiry final CLI returns exit0/pass with both fresh cases and no native failures. These are fresh current-source executions, not historical results or a new clean-install milestone.

Actual command forms, with outputs outside the package:

```bash
python research_harness/run.py --archive "$ARCHIVE" --scenario late_input_expiry --output "$OUT/final.json"
python research_harness/run.py --archive "$ARCHIVE" --scenario ordinary --output "$OUT/ordinary.json"
# Same command for chord, moving_arc, timing_group, cpu_note: each exit0.
ARCONIST_TEST_ARCHIVE="$ARCHIVE" ARCONIST_ARC_TAP_TEST_ARCHIVE="$ARCHIVE" \
ARCONIST_HOLD_TEST_ARCHIVE="$ARCHIVE" \
  python -m unittest discover -s research_harness/tests -v
```

For these actual runs Python is the isolated Python3.12 interpreter, ARCHIVE is the external supplied ZIP and OUT is a separate audit directory. Arc-tap and hold execute their original CLI subprocesses inside the opt-in native tests. No generated regression JSON/log is published.

No old scenario/assertion/fixture/test is changed. CLI/config gain only scenario registration, README documents it, and new fixture/source retain the comparison. Existing camera_reset/track_fade/flick_producer/continuous_gauge/camera_designant blocked diagnostics remain intact; they are not reopened/rerun or counted as passing gameplay tests.

## Retained services, skips and publication

No new ABI/platform/account adapter, gameplay PC skip, mode override, native state repair or runtime dependency is introduced. Existing external catalog/settings/profile/account storage, resources/CSB/fonts, platform GLView, clocks, JNI inputs, libc/C++/math/locale, allocator/autorelease, audio/graphics/presentation boundaries retain their published scope. Full original GameScene/TrackLayer initialization and CPU model updates remain enabled. Base traversal/render/flush boundaries remain as before; this is not032's separate traversal-restoration scenario.

Exact inherited ELF skip pairs:

```text
f72110→f72158
16a4238→16a48d8
121581c→121584c
a507c4→a519ec
a51adc→a5213c
196fdac→196ffac
891190→89164c
891688→89219c
8921dc→8928e0
```

Last three are results-only and unentered by the new scenario. The source checks that original constructors/initializer/model/expiry/index/input/sorter/classifier/recorders/cleanup are neither host-invoked handoffs nor replaced hooks. Original bdbb70 is deliberately host-invoked solely as a read-only projection interface.

Exactly eight authorized paths: this report, append-only context, backlog G-011/history, harness README/run.py/src/config.py, new src/late_input_expiry.py and fixtures/native_late_input_expiry.aff. G-001–G-010 rows/statuses/history are preserved; G-011 becomes Verified with Scout002 S2-C01 provenance. Previous reports001–034/030-R, root README/instructions, old source/tests/fixtures/assertions/dependency pins and unrelated parent blobs remain unchanged. No ZIP/ELF/proprietary assets, traces/JSON/dumps, databases, account data, secrets or environments are committed. Publication uses expected-parent update and immutable readback/tree/prefix verification; exact SHA/links are returned in the headquarters response.

## Pseudocode — observed original-native flow

```text
for input_first, frame_first in independent fresh emulators:
    supply ordinary metadata/platform services and synthetic complete AFF
    original solo eligibility/latch/allocation/constructor/loading
    original parser/builder/count/timing/index and GameScene initializer
    Director activates same scene and listener
    Director frames establish music anchor and shared E1000 state
    verify both original taps active/enabled/unresolved; counters/contact state empty
    original camera projects common external input target
    advance external wall clock110ms

    if frame_first:
        Director/visit guard -> one GameModel frame atE1110
        original expiry records older tap LOST, missed byte1

    original JNI DOWN42 -> native Touch mapping/retention/listener
    initial input refreshes E1110; original collection/sort contains both taps
    if input_first:
        older classifier error110 -> native miss recorder -> return1
        original iteration stops; newer untouched
    else:
        older missed guard1 -> return0
        newer error1 -> original accepted recorder/acceptance -> return1
        original iteration stops on newer
    original JNI UP42 -> native mapping/slot/mask/retention cleanup

    if input_first:
        Director/visit guard -> one GameModel frame atsameE1110
        remove already-missed older from active range; no duplicate miss

compare pointer-normalized preconditions, native calls/guards/recorders/output
run previous successful regressions and existing tests
publish G-011 Verified within this bounded original-native comparison
STOP without036 or selecting S2-C02
```

## Final research boundary

This establishes causal sensitivity to controlled JNI-versus-frame ordering in the ordinary native-created scene. It does not establish which ordering a physical Android queue uses, hardware latency, arbitrary frame cadence, equal-time sorting stability, other note types, late chart completion or results persistence for this fixture. No further exploration is needed for this objective; future research requires a separate headquarters decision.
