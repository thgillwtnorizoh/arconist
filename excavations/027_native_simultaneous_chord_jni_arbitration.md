# Expedition 027 — Native Simultaneous Chord Judgment & Contact Identity

Date: 2026-10-26. Scout001 backlog **G-003**. Original code/vtable addresses are **ELF virtual addresses**; object pointers below are explicitly emulated runtime observations.

## Result

**Strong success; G-003 Verified for the tested two-lane chord.** Two fresh native runtimes execute ordinary solo startup, original AFF-to-tap construction, loading/Director activation and JNI chord judgment. Both DOWNs have native E1500 with overlapping contact lifetimes. Each native note is independently consumed once by its assigned contact. Reversing delivery order changes native slot/generated-ID assignment while preserving the correct note/contact relationships, score, gauge and cleanup.

Forward and reverse both produce PURE2/FAR0/LOST0, shining2, score10000002 and live health80.4000015258789. The unchanged ordinary full session, native arc-tap and hold dual-case regressions pass, as do all3 input/negative tests. No new native dependency, ABI service, proxy or PC skip is introduced. The new scenario passes on its first complete invocation. Investigation stops at E1500 after both UPs; no chord completion/results/SQLite replay or Expedition028 is initiated.

## What I Found

### Preparation, fixture and evidence scope

Read the supplied introduction, latest context/backlog, relevant002/004/008/011 input/judgment evidence and024–026 runtime/regression conventions. Inspected the committed solo-entry/lifecycle/regression/arc-tap/hold/config/CLI source and targeted original instructions. Main matched `fd5038f84893666533efa5a210e6f3b656a16c4a`, tree `a0a5b203d52340031d03bda5db17a1ab30be1f2c`; no027 report existed. All29 local harness file blobs matched that parent before editing.

The external read-only ZIP's `lib/arm64-v8a/libcocos2dcpp.so` matches SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`. Runtime dependencies remain CPython3.12.14, Unicorn2.1.4 and pyelftools0.33. Temporary Capstone5.0.9 inspection is not a runtime dependency. No old emulator, snapshot or unpublished scratch module is an input to the scenario.

New `research_harness/fixtures/native_chord.aff`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1500,1);
(1500,4);
```

These are synthetic chart bytes supplied through the established selected-chart resource-provider boundary. The selection remains `sayonarahatsukoi`, difficulty0, set `base`, no purchase descriptor, ordinary mode0, no special map/modifier and speed40 with zeroed PlayParameters. No parsed notes, positions, index entries, candidate vectors, Touch objects/mappings/IDs, consumption flags or scores are host-assigned.

**Native-integrated:** all forward/reverse evidence belongs to one complete CLI invocation, with a new Unicorn instance, mapped ELF/globals and native heap for each case. Equal heap addresses in independent emulators are observations, not an assertion or reused state. **Instruction-backed:** lane-selector intervals, tap initializer fields, acceptance stores and classifier/recorder relationships were checked against original instructions. **Supplied:** external chart, existing platform/ABI/catalog/settings/profile/resources, clock values and JNI event inputs. **Interpretation:** this establishes software-level order independence for this separated two-lane fixture. **Unknown/unexecuted:** true OS event simultaneity/batching, device latency, overlapping hitboxes, additional fingers and general chord/chart compatibility.

### Original scene and note construction

| Native connection | Evidence in each fresh case |
|---|---|
| Registry/menu/ordinary entry | Original `0x1054f24`, menu/selected-pair setup and `0xee197c`; eligibility1 and native request latch1 |
| GameScene allocation/constructor | Original `0xee29a8 → 0xee29e8`; GameScene constructor entry once, LR=`0xee29ec`, X0 is this scene; no multiplayer helper |
| Loading → GameScene | Original loading actions invoke initializer `0xe2ea48`, genuine return1; Director activates same scene, pending0 |
| Whole AFF → parsed taps | Original `0x1870de0 → 0xdf4a58 → 0xb01d6c`; builder sees two `10SimpleNote` objects, each parsed time1500 and raw integer positions1/4 |
| Runtime tap allocation/init | Builder `0x1862a14` allocates each0x80-byte object at `0x186407c–0x18640b8`; `0x18640d8` calls original initializer `0x1902ffc`; both returns at `0x18640dc` are1 |
| Native tap fields | RTTI `12LogicTapNote`, vtable `0x1af4278`; original initializer stores start=end1500, native position, flags0 and initial accepted ID−1 |
| Count/index/listener | Original `0x11ea120` gives N2, chart end1620; original `0x1576aa4` receives both notes; registered/enabled listener with paused0 |

The chart contains505 main runtime objects including auxiliary objects, not505 scoring units. Both taps are input-enabled, timing1500, native lanes2/5 and admitted to native index key1 in group0. Both are in the active model range before the first DOWN. Assertions identify them by lane/time and original construction returns, not equal-time chart-vector order.

Original `0x1902ffc` stores time with `stp w1,w1,[note+0x18]`, position at+0x20, clears missed/consumed bytes at+0x0c/+0x0d and initializes contact+0x10 to−1. No constructor or chart-loader field is supplied as a substitute.

Emulated observations (same numerical addresses in the two separate address spaces): scene `0x4326ec0`, model `0x43551c0`, chart `0x4330c00`, ScoreState `0x4355380`; lane2 tap `0x43314c0`/position `0x4331480`, lane5 tap `0x43315c0`/position `0x4331580`. Native scene+0x3e0=model and scene+0x3e8=model+0x28=chart relationships hold. Original listener priority20, registered1/enabled1/paused0. No heap address is a required constant.

### Projection and common effective time

External contact targets derive from original-created lane IDs and original ordinary selector `0x130733c`. Choose conservative interior lane-plane centers rather than reuse an earlier screen coordinate. These are input targets, not host-written note geometry. The underlying selector has asymmetric boundary/outer-range behavior documented in004 §3; these selected intervals are not claimed to be universal outer hitbox limits.

| Android ID → raw/native lane | External plane target | Current-camera JNI XY | Original ground intersection | Native primary/secondary |
|---|---|---|---|---|
|42 → 1/2|(-637.5,0,0)|(232.40264892578125,617.340705871582)|(-637.4775390625,0,0)|2/0|
|43 → 4/5|(637.5,0,0)|(1047.597412109375,617.340705871582)|(637.4775390625,0,0)|5/0|

Projection calls original `0xbdbb70` on the current scene camera, then converts Y-up with native Director height720. Ordinary model mode is0, spatial-width field+0x60 is1 and extension field+0x74 is0. Original JNI input independently unprojects and selects the observed lanes; no explicit-lane bypass is used.

Native music anchor is wall9452/E0. A Director-driven frame reaches wall10952/E1500; original scene visitation invokes GameModel. Both DOWN calls retain that wall and Director counter, with no intervening frame or driver clock change. At `0xeec080`, after the original initial-input timeline refresh call, both events independently observe E1500. Recorder E arguments also equal1500. Supplied begin timestamps987042/987043 do not replace chart time. UP timestamps988042/988043 are external transport data.

### Four-level identity and overlapping lifetimes

| Run | Android ID / native lane | Engine slot | Generated gameplay ID | Native Touch | Accepted note+0x10 |
|---|---|---:|---:|---|---:|
|Forward|42 /2|0|0|`0x4eca640`|0|
|Forward|43 /5|1|1|`0x4ecb400`|1|
|Reverse|43 /5|0|0|`0x4eca640`|0|
|Reverse|42 /2|1|1|`0x4ecb400`|1|

Native IDs follow delivery/allocation order. Android-to-lane assignment remains fixed. The comparisons require each run's correct Android ID → engine map/slot → Touch → generated ID → accepted note relationship; they do not compare IDs or heap pointers across emulators.

| Stage | Forward | Reverse | Score state |
|---|---|---|---|
|Before DOWN|Map/retention empty, mask0; both notes unconsumed/ID−1|Same|PURE0/score0/H0|
|First DOWN|42 retained; lane2 consumed, lane5 available; mask1|43 retained; lane5 consumed, lane2 available; mask1|PURE1/shining1, score5000001, H40.20000076293945|
|Second DOWN, before any UP|42+43 mapped; two distinct Touches retained; both notes consumed; mask3|43+42 retained with corresponding native identities; both notes consumed; mask3|PURE2/shining2, score10000002, H80.4000015258789|
|First UP|UP42 removes only first contact;43 remains, mask2|UP43 removes only first contact;42 remains, mask2|Unchanged|
|Second UP|UP43 empties map/retention, clears slots/mask|UP42 empties map/retention, clears slots/mask|Unchanged|

The second DOWN preserves the exact first retained Touch. All four JNI calls in each run occur at the same driver wall/E; the native begin refresh is explicitly observed, not assumed. This is two sequential native deliveries with overlapping lifetimes, **not atomic Android MotionEvent batching**. Real Java event capture/GL-thread queue scheduling is outside this test.

### Original candidate, classification and consumption evidence

The connected original path is:

```text
JNI 0xbe31a8 → original GLView/EventDispatcher
  → registered gameplay begin0x194ff80 → initial input0xeec024
  → original unprojection/lane selector0x130733c
  → tap lane comparisons0xeec32c–0xeec350
  → original candidate sort0xf6b514
  → 0xeec568 → classifier0x160ce28
  → 0x160cf44 → accepted recorder0x1730290
  → virtual acceptance at0x17302e8 → ordinary tap0x965e28
```

Read-only candidate snapshots at `0xeec4f0` contain exactly one matching note for each DOWN, in both orders. The opposite lane's note is absent. Thus separated native lane selection establishes independence before timing classification; no host repair/filter is applied to candidates. The original sorter executes, but this singleton-candidate experiment establishes no new equal-key sorting stability guarantee.

Both native classifier entries receive the matching note and generated gameplay ID. The original classifier's missed/consumed virtual guards remain enabled; both accepted notes begin consumed0/missed0. Recorder LR=`0x160cf48`, X1 is the correct native note, W2/W3=0, W4=1500 and W5 is its matching generated contact ID. Ordinary acceptance LR=`0x17302ec` establishes the native recorder→acceptance call relationship.

The observed original writes are `0x965e68: note+0x0d=1` and `0x965e6c: note+0x10=generatedID`. Each note has exactly one consumed-byte0→1 store and one accepted-ID store from initial−1. Two notes, two accepted recorder entries, two acceptance entries; no note is selected/accepted twice. The second DOWN does not target the first note or replace its contact. No third contact or fabricated duplicate attempt is added.

Per case, JNI DOWN/UP, listener begin, initial collector, sorter, classifier, acceptance, recorder and cleanup `0xf9a50c` each execute2 times. Miss recorder `0x868e54`, multiplayer helper `0xdd0f90` and completion `0xc27d34` execute0 times. UP preserves both notes' consumption/accepted IDs and all score/gauge fields; native Android map, used slot pointers, engine mask and retained contacts are empty afterward. Original release instructions execute within the inherited allocator/autorelease boundary; physical reclamation is not proved.

At the endpoint the same GameScene is running, pending0, effective time1500, ScoreState+0x68 null. No chord GameResult, ending callback or save is claimed.

### Reusable package and regression protection

Added only `fixtures/native_chord.aff` and `src/chord.py`; CLI/config add `chord`, and the harness README documents the scenario. Existing scenario/ABI/resource/lifecycle implementations and requirements remain untouched. `chord.py` separates supplied targets/events from read-only construction, input, candidate, acceptance and memory-write observations. Assertions forbid direct host calls/replacements of native scene/initializer/model-frame, builder/index, collector/sorter/classifier/acceptance/recorder and cleanup handoffs.

```bash
python research_harness/run.py --archive /path/to/arccopy.zip \
  --scenario chord --output /path/to/chord-result.json
```

Install the existing pinned `research_harness/requirements.txt` in Python3.12 as documented in its README. The existing archive hash validation runs before native execution. The29673-byte JSON contains each complete independent trace, native construction/count/index relationships, current projection, time refreshes, contact and retention snapshots, original consumption writes/recorder provenance, final comparison and boundaries. No canned events/results or scratch module is used. Failures propagate to the existing CLI's fail output.

| Required execution | Outcome |
|---|---|
|Chord CLI, forward and reverse fresh runtimes|PASS on first complete invocation; all native/identity/order/cleanup assertions|
|Unchanged ordinary two-tap full session|PASS; original gameplay/results/SQLite/final scene assertions unchanged|
|Existing arc-tap native unittest|PASS; construction/JNI/meaningful duplicate control unchanged|
|Existing hold native dual-case unittest|PASS; native release/reacquisition/checkpoint comparison unchanged|
|Missing archive / wrong binary hash / native unavailable song|All3 PASS|

All existing opt-in native switches were enabled; unittest discovery ran5 tests and all5 passed, no skips. Chord is verified by its full CLI assertions; no redundant optional wrapper was added. Prior two-tap/arc-tap/hold fixtures, prior scenario source/assertions, tests and dependency versions are preserved. No test was weakened and no new dependency/blocker was investigated.

### Remaining boundaries and publication

Inherited exact PC ranges remain `0xf72110→0xf72158`, `0x16a4238→0x16a48d8`, `0x121581c→0x121584c`, `0xa507c4→0xa519ec`, `0xa51adc→0xa5213c`, `0x196fdac→0x196ffac`, `0x891190→0x89164c`, `0x891688→0x89219c`, `0x8921dc→0x8928e0`. The last three results regions are not reached by chord. Existing base traversal/render/flush services `0x129c924`, `0x1017a84`, `0x13edf0c` remain inert, while native TrackLayer CPU update `0x19069a0` remains enabled. Existing offline metadata/settings/profile/catalog, JNI/platform, libc/C++/math/clock/resource, presentation/texture proxies, GPU/audio and allocator/autorelease services retain their024–026 contracts. No additional service is installed for chord. Inherited private DB preparation is not a chord save experiment.

Only8 publication paths are changed: this report, append-only context, backlog, harness README/run/config, and the2 new chord files. G-003 becomes Verified—027 with appended decision history; G-001/G-002 remain Verified and G-004–G-010 statuses remain unchanged. Historical context must remain an exact prefix. All other old blobs, including reports001–026, root README/instructions, prior regression fixtures/assertions and original resources, are preserved. No ZIP/.so/proprietary resource, generated JSON/log, memory dump, database, environment or secret is committed.

The exact publication SHA and committed-file readback/parent-tree checks are returned in the final handoff. This report cannot contain its own immutable commit hash. Report path: `excavations/027_native_simultaneous_chord_jni_arbitration.md`; [backlog](../research_backlog.md); [harness documentation](../research_harness/README.md). Stop after required regression checks; do not initiate028.

## Pseudocode

```text
verify external archive's original ARM64 library hash
for DOWN order in [42→43, 43→42]:
    create fresh emulator/native globals/heap
    supply established offline/platform/ABI/resource services and synthetic AFF
    original registry/menu/ordinary solo entry → eligibility/latch/GameScene constructor
    original loading invokes initializer:
        whole AFF parser → two parsed integer-position taps at1500
        native builder/initializer → distinct lane2/5 LogicTapNotes
        native countN2/index/model/listener
    initializer returns1 → original Director activates that same scene
    derive external lane-plane centers from native positions/selector semantics
    original camera projection + native height/Y conversion → external JNI coordinates
    Director frame reaches original timeline E1500

    JNI DOWN first Android ID
        native Touch/slot/generated ID → original collector/sorter/classifier
        native recorder/acceptance writes corresponding note's consumed flag/contact ID
    JNI DOWN second ID, same wall/E, before any UP or model frame
        second original Touch retained beside first
        native lane-specific candidate independently consumes corresponding other note
    verify both mappings/Touches/generated IDs coexist and two unique notes are consumed

    original JNI UP first then second
        native map/slot/mask/retained-vector cleanup
        no new judgment or score/gauge change

compare native lane/time consumption and score/gauge outcomes across fresh cases
do not compare cross-emulator heap addresses or generated-ID-to-lane assignment
verify unchanged ordinary/arc-tap/hold regressions and input negatives
update G-003, publish scoped evidence, STOP before chord completion/results and028
```
