# Expedition 026 — Native Hold Reacquisition & Checkpoint Continuity

Date: 2026-10-26. Backlog item: **G-002**. Original-library addresses below are ELF virtual addresses; allocated object addresses are explicitly emulated observations.

## Result

**Strong success; G-002 Verified for the tested fixture and interruption schedule.** Two fresh ARM64 emulators independently execute ordinary solo entry, native GameScene loading/activation, original AFF hold/checkpoint/index construction, Director-driven frames and JNI input. The uninterrupted control and UP/repress case both produce three shining PURE checkpoint judgments, score10000003 and live health80.5999984741211. A new native Touch reacquires the hold after the old contact is removed and a real intervening model frame clears activity. Each checkpoint is resolved exactly once by original instructions.

No hold, checkpoint vector, latch, contact flag, ownership link, resolved byte, score/gauge counter or timeline field is assigned by the driver. No new native dependency, ABI service, rendering proxy or PC skip is required. Investigation stops after terminal JNI cleanup/E1627. No hold GameResult, ending, results scene or save is claimed. Existing ordinary two-tap end-to-end and arc-tap regressions remain green.

## What I Found

### Preparation and evidence scope

Read the supplied introduction, current context/backlog, hold-specific008–012 sections,024/025 reports and published harness. Main was `a369e93c43b895d0bfe4430a232f13abad3b4e22`, tree `ade3a107445447eb5aca7ef1b6f33cbbdfd0a54d`; no026 report existed. All existing local harness files matched the parent's Git blob identities before edits. The supplied ZIP is an external read-only dependency. Its ARM64 member `lib/arm64-v8a/libcocos2dcpp.so` hashes to `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` before execution.

Python3.12.14, Unicorn2.1.4 and pyelftools0.33 were used. Capstone5.0.9 was a temporary disassembly aid only; package requirements remain unchanged. Existing setup, resources, ABI, native engine, menu, loading, clock and JNI adapters are reused. No live emulator or prepared memory is recovered from an earlier conversation.

**Native-integrated:** all successful observations below belong to the single final `--scenario hold` invocation, which creates a new Unicorn instance, ELF/global state and native heap for each case. Equal emulated addresses across cases reflect deterministic allocation in separate address spaces, not shared objects or restored snapshots. Preparatory diagnostic traces and assertion-calibration failures are not spliced into either case.

**Instruction-backed:** explanations of strict hold timing, lane intervals and resolved-guard branches are checked against original instructions. **Supplied:** offline metadata/settings/profile/platform/ABI services, synthetic chart bytes, clock progression and external screen contacts. **Interpretation:** equivalence is established for this gap and cadence; arbitrary interruptions and charts are not implied. **Unknown/unexecuted:** no-repress misses, pause UI, unusual holds, physical Android/audio timing and hold results integration are outside this test.

Prior evidence is reused by reference:008 §6/§12 and hold-start boundaries;009 §10/§20;010 whole-file parser/full chart initialization;011 §10 JNI release;012 §15 pause retention. This experiment closes fresh-contact reacquisition inside the native-owned scene, rather than repeating prepared-model or retained-contact pause recovery.

### Original construction and ordinary scene ownership

The new external fixture `research_harness/fixtures/native_hold.aff` is:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
hold(1000,2000,3);
```

It is synthetic research input at the established selected-chart resource boundary, not an archived production chart. The ordinary selection remains `sayonarahatsukoi`, difficulty0, set `base`, no purchase descriptor, mode0, no map/modifier and speed40 with zeroed PlayParameters. The original song-ID registry initializer `0x1054f24` executes.

| Native connection | Observed evidence in each fresh case |
|---|---|
| Ordinary entry `0xee197c` | Eligibility1; native request latch1; allocation `0xee29a8` and constructor call `0xee29e8` once; GameScene constructor LR=`0xee29ec`; multiplayer helper0 entries |
| Loading → initializer | Existing original loading actions invoke GameScene initializer `0xe2ea48`; genuine return1; same GameScene activated by Director, pending0 |
| Whole AFF → parsed hold | `0x1870de0 → 0xdf4a58 → 0xb01d6c → 0x139b96c/0x923240`; whole parser/lexer/body wrapper once, statement-parser entries2 for timing+hold |
| Parsed hold → runtime factory | At `0x18649b8`, parsed RTTI `8HoldNote`, start1000/end2000, typed raw integer3; factory arguments preserve these values and native-converted position |
| Runtime factory | `0x18649b8 → 0x1446490`, return `0x18649bc`; original allocates0xb0 and initializes `13LogicHoldNote`, vtable `0x1b2eda8` |
| Checkpoint generation | Original chart initializer `0x173b358 → 0x1862a14`; long-note generator `0xd92558` once; native append callsite `0xd925fc` supplies three initially unresolved weight1 records |
| Native count/end/index | `0x11ea120` returns N3; chart end2500;505 main objects including auxiliary bars; original index producer `0x1576aa4` receives the same model/hold |
| Model/listener/frame | Scene+0x3e0=model, scene+0x3e8=model+0x28=chart; registered/enabled listener, paused0; each scheduled Director frame visits original `0x10a7550` once |

Original output: internal lane4, normalized position1.0, interval250, records `(1250,1,0)`, `(1500,1,0)`, `(1750,1,0)`, timing group0. The record tuple is time/weight/resolved. Native chart count, record flags, timing and spatial buckets are never forced.

The current scene's effective speed is4.044943809509277; precomputed hold depths are−8089/−16179 and native index keys are0/1. These differ from009's older prepared fixture's keys1/2. An early packaging assertion that reused those keys was corrected to require actual native index admission and record its keys. Arc-specific parser addresses from025 are not used as hold-parser assertions, and recursive statement parsing is not incorrectly counted as one call. These were observation/assertion-contract corrections, not eligibility, timing, index or judgment substitutions. No substantial new native blocker was encountered.

Emulated pointer observations in each independent case:

| Object | Pointer |
|---|---|
| GameScene / GameModel | `0x4326ec0` / `0x4355200` |
| LogicChart / GameTimeline / ScoreState | `0x4330b00` / `0x4355380` / `0x43553c0` |
| LogicHoldNote / native position | `0x43313c0` / `0x4331380` |
| Checkpoint record addresses | `0x4331540`, `0x433154c`, `0x4331558` |

Regression assertions compare relationships and native factory returns, never those heap constants. Native index production runs505 times across all main objects; only one input-enabled LogicHoldNote is present.

### Current camera and native effective clock

The external contact target is derived from the native-created hold's lane4 and the original ordinary selector's world-X interval `[0,425)` at `0x13074d0–0x13074e0`. Choose its center `(212.5,0,0)` on the input plane. This is a supplied input target; it is not a host-written hold position or a claim of rendered note geometry.

Original camera projection `0xbdbb70` uses the current model camera (`model+0x20 → rig+0x2a8`). Native Director height720 converts its Y-up result to Android/design input. New JNI coordinates are **`(775.8657836914062,617.340705871582)`**, independently verified by original input unprojection. At `0x13073c4` the original ground intersection is `(212.4925537109375,0,0)`, inside native lane4. The older `(740,360)` coordinate is not reused.

Native activation occurs at wall6450; preroll6451; original music anchor9452/E0. All target walls use the observed native timeline's E, not a host write to that timeline:

| E | Wall | Purpose |
|---:|---:|---|
|1000/1001|10452/10453|Initial DOWN; then strict continuous start boundary crossed |
|1124/1125|10576/10577|Checkpoint1250 not due / due |
|1200/1201|10652/10653|Release case UP; then real clearing frame |
|1300/1301|10752/10753|Replacement DOWN; then native reactivation |
|1374/1375|10826/10827|Checkpoint1500 not due / due |
|1624/1625|11076/11077|Checkpoint1750 not due / due |
|1626/1627|11078/11079|No duplicate award; terminal UP; next-frame cleanup |

Original initial collection has `start < E+100` and `E < end`; tested continuous activation additionally requires `start < E < end` and initial latch+a8. The positive case starts at E1000 and activates at E1001, retaining the distinct predicates. Model frames are invoked through original Director visitation, never by a direct host model-frame call.

### Control versus release/reacquisition

JNI DOWN `0xbe31a8` / UP `0xdda71c` traverse original GLView/EventDispatcher and registered gameplay listener. Initial begin `0x194ff80 → 0xeec024` produces latch+a8; observed original store PC is `0xeec6f0`. Original continuous processing `0x14858d4` receives retained contacts and calls the hold's activation virtual at `0x1485e60 → 0x14557b4`. Its original `0x14557ec` store sets contact bytes+0x64/+0x65 to1/1. Original reset `0x1866038` clears them before continuous input can restore them.

| Point | Uninterrupted control | UP/repress case | Counters in both |
|---|---|---|---|
| First DOWN/E1000 | Android42, one retained Touch; latch1/activity0/0 | Same native initial transition | PURE0 |
| E1001 | Original Touch activates1/1 | Original Touch activates1/1 | PURE0 |
| E1125 | Contact retained/activity1/1 | Contact retained/activity1/1 | PURE1, record1250 resolved |
| E1200 after optional UP | Retention/map/mask remain1 | JNI UP42 removes retention/map; mask0; activity still1/1 immediately | PURE1 unchanged |
| E1201 | Native reset then contact restores1/1 | Native reset leaves0/0; latch remains1; no retained contact | PURE1 unchanged |
| E1300 after optional DOWN | Same original Touch/activity1/1 | JNI DOWN43 creates distinct Touch/generated ID; retained1, latch1, activity still0/0 | PURE1; records1500/1750 unresolved |
| E1301 | Original contact continues | Activation virtual receives the new Touch; activity1/1 | PURE1 unchanged |
| E1375 / E1625 | Remaining records resolved | Remaining records resolved through reacquired contact | PURE2 / PURE3 |
| Terminal UP/E1626 → frame1627 | Retention/map empty, mask0; then activity0/0 | Same cleanup for replacement | PURE3 unchanged; latch1 |

First native Touch is `0x4ecab40`, generated gameplay ID0, Android pointer42/engine slot0. Replacement is `0x4ecfa00`, generated ID1, Android43/slot0. Engine slot reuse does not imply Touch or generated-ID reuse. These addresses/IDs are observations, not required constants. Initial latch is a note flag independent of native contact identity; this experiment does not invent a persistent per-hold owner field. At E1301 the original activation arguments identify the replacement object directly.

Original UP cleanup `0xf9a50c` executes once in control and twice in the interrupted case. Native tree/map removal, engine mask and model retained-vector observations agree. Reference release executes within the inherited allocator/reclamation boundary; this is not proof of final physical object destruction. JNI event timestamps are supplied transport inputs; effective chart time is derived from native model frames, not those timestamps.

### Checkpoint recording, gauge and duplicate exclusion

The active checkpoint branch in original `0xf8056c` uses `time <= trunc(E+interval/2)` in this fixture. At `0xf80904`, resolved records branch away. The original store at **`0xf80924`** writes each record's resolved byte0→1 exactly once. Original callsite `0xf809a4 → 0x1730290` records each weight1 unit; recorder LR=`0xf809a8`, X1 is the original hold, E1125/1375/1625, native contact argument−1. Upstream continuous matching, not a fabricated recorder contact ID, establishes activity.

| Native E | Resolved vector | PURE/shining | Score | Live health |
|---:|---|---:|---:|---:|
|1000–1124|0/0/0|0|0|0 |
|1125|1/0/0|1|3333334|26.866666793823242 |
|1375|1/1/0|2|6666668|53.733333587646484 |
|1625–1627|1/1/1|3|10000003|80.5999984741211 |

Both cases have FAR0/recorded LOST0 throughout. The all-PURE score expectation is checked against native N3 and recorded shining units; score and gauge are original outputs. Accepted recorder count3, miss recorder `0x868e54` count0. The original inactive/overdue routine `0xc6e938` executes3 times in control and5 in interrupted frames but produces no miss record: entering that routine is not itself a penalty.

Later original guards observe all three records already resolved. The control has12 resolved-guard entries and12 activation entries; interrupted has10/10 because it lacks contact on two recorded frames. In both, only three resolution writes and three accepted recorder entries occur. E1626 and the terminal cleanup frame add no score/gauge change. No-repress failure was optional and is not run; no claims about a missed checkpoint are borrowed from a different trace.

### Reusable package and validation

Added `fixtures/native_hold.aff`, `src/hold.py` and optional `tests/test_hold.py`. Only config/CLI selection and harness README are extended. `--scenario hold` executes both fresh cases and compares native counts, checkpoint identities/flags, generated contacts, latch/activity transitions, recorder deltas, output state and cleanup. Read-only code/memory hooks collect evidence; no native callback, checkpoint function or recorder is directly invoked by the host.

```bash
python -m venv /path/to/venv
/path/to/venv/bin/pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario hold \
  --output /path/to/hold-result.json
```

One final CLI invocation passes both complete cases and emits a65153-byte JSON with the verified binary hash, fixture, construction observations, actual heap relationships, native clock/input/projection/state traces, original writes/guards/recorder entries, comparison and declared boundaries. No generated JSON or trace is a published source input. Failures raise into the existing CLI's fail report; no expected-event playback is used.

| Executed check | Result |
|---|---|
| New hold CLI: two independent complete cases | PASS; all construction/contact/checkpoint/identity/comparison assertions |
| Unchanged default two-tap full session | PASS: PURE2, score10000002, liveH80.4000015258789, native results/SQLite and final scene intact |
| Existing optional arc-tap unittest enabled with external archive | PASS: original construction/JNI/meaningful duplicate assertions unchanged |
| Missing archive / wrong binary hash / native unavailable song | All3 PASS |
| New optional hold unittest wrapper | Explicitly skipped in discovery; the same real CLI scenario/assertions were executed separately, not replaced by this skip |

The unittest invocation ran5 discovered tests:4 passed (arc-tap plus3 input/negative checks),1 explicitly skipped. `ARCONIST_HOLD_TEST_ARCHIVE` enables the separate hold wrapper when desired. Neither historical fixture nor `arc_tap.py`, its services/test, `regression.py`, lifecycle, ABI/platform/resource modules, requirements or old assertions is modified. There is no new runtime dependency or unresolved execution blocker. After success, only evidence review/publication remains; no additional gameplay scenario is investigated.

### Scientific boundaries and publication

Retained exact PC ranges are `0xf72110→0xf72158`, `0x16a4238→0x16a48d8`, `0x121581c→0x121584c`, `0xa507c4→0xa519ec`, `0xa51adc→0xa5213c`, `0x196fdac→0x196ffac`, `0x891190→0x89164c`, `0x891688→0x89219c`, `0x8921dc→0x8928e0`. The last three results regions are not reached in hold. Existing base traversal/render/flush boundaries (`0x129c924`, `0x1017a84`, `0x13edf0c`), loading information/panel proxies, textures, catalog/profile/settings/platform/JNI/libc/C++/clock/resource/audio/GPU/allocator/autorelease services remain supplied as documented in024–025. Native TrackLayer CPU update `0x19069a0` stays enabled. The inherited private in-memory database setup is not a hold save experiment.

No full Android startup/hardware scheduling, real GPU output, sound playback, arbitrary holds, early release misses, pause UI or results integration is newly verified. The renderer is not reconstructed. The one-substantial-new-dependency budget is unused.

G-001 remains Verified. G-002 is updated to Verified — Expedition026 and decision history appended; G-003–G-010 retain their previous statuses. No027 is initiated.

Publication uses the user's026-specific exception. Exactly9 paths are authorized candidates: this report, append-only context, backlog, harness README/run/config and the3 new hold fixture/source/test files. Historical context is required to remain an exact prefix. All other old blobs, including reports001–025, root README/instructions, historical fixtures/tests and original resources, are preserved. No ZIP/.so, proprietary resources, memory dump, database, generated output, secret or environment is included. The final handoff records the exact published commit and readback/parent-comparison result; links below resolve inside that commit when pinned by headquarters.

Report: `excavations/026_native_hold_reacquisition_and_checkpoint_continuity.md`; backlog: [research_backlog.md](../research_backlog.md); harness: [README](../research_harness/README.md). The commit cannot contain its own SHA without changing that SHA.

## Pseudocode

```text
verify external archive's original ARM64 binary hash
for case in [uninterrupted, release_reacquisition]:
    create fresh emulator/native globals/heap
    supply established offline metadata/settings/platform/ABI/resource services
    original registry + menu construction + selected pair setter
    original ordinary startGameScene -> eligibility1 -> latch -> GameScene allocation/constructor
    original loading actions invoke GameScene initializer
    inside initializer: original whole AFF parser -> parsed HoldNote(integer3,1000..2000)
        -> runtime builder/LogicHoldNote factory -> original250ms checkpoints
        -> native N3/end2500/depths/index/model/listener
    initializer returns1 -> Director activates that same GameScene
    derive external lane-plane contact from native position + original selector interval
    original camera projection -> external JNI coordinates
    Director frames derive native wall/E schedule
    JNI DOWN42 at E1000 -> native Touch/generated ID/retention/initial latch
    Director E1001 -> original reset/continuous matching -> activity1/1
    E1124 no award; E1125 -> original record1250 resolved/recorder
    if release_reacquisition:
        E1200 frame, JNI UP42 -> native retention/map removal; activity still1/1
        E1201 frame -> original reset -> activity0/0; initial latch remains1
        E1300 frame, JNI DOWN43 -> distinct native Touch/generated ID/retention
        E1301 frame -> original matching/activation using replacement Touch
    else:
        retain original contact through same Director frame schedule
    E1374/1375 and E1624/1625 -> original due predicates and remaining records
    later original resolved guards prevent repeat awards
    JNI terminal UP at E1626; E1627 frame clears stale activity
    assert native recorder3/miss0, PURE3, native score/gauge, unique resolution writes
compare both independent native traces and outputs
verify unchanged ordinary and arc-tap regressions plus input negatives
publish scoped source/evidence; update only G-002 status/history
STOP before hold completion/results; do not initiate027
```
