# Expedition 028 — Native Moving Arc Geometry & Crossing Contact Ownership

Date: 2026-10-27. Scout001 backlog **G-004**. Code/vtable addresses below are original ELF virtual addresses. Heap pointers are emulated observations and are not regression constants.

## Result

**Strong success; both gates pass. G-004 is Verified for the bounded fixtures and declared environment.** Original AFF creates moving ordinary arcs inside solo-created GameScenes; original geometry/current-position updates, native camera projection, JNI movement, retained Touches, spatial eligibility, color ownership and checkpoints execute together. A fresh two-color pair crosses, produces native bypass/release decisions and records both arcs without duplicate awards. Original UP and next-frame cleanup succeed.

The single control gives PURE3/FAR0/LOST0, score10000003, live health80.5999984741211. The crossing gives PURE6/FAR0/LOST0, score10000006, live health81.19999694824219. All existing ordinary/arc-tap/hold/chord regressions and three negative tests pass freshly. No gameplay PC skip, geometry/activation/owner assignment or renderer reconstruction is introduced. Stop at E1876 after cleanup; no results/save extension or Expedition029.

## What I Found

### Preparation and source discipline

Read the supplied introduction, current context/backlog, relevant002–004/008–009/011 evidence,020's native CPU TrackLayer boundary and024–027 runtime/scenario conventions. Actual published bootstrap/resources/solo-entry/lifecycle/arc-tap/hold/chord/config/CLI source is reused. Main was `88e7976f36d2a4a0e4d13052b78202c8a64f8e72`; no028 report existed. Existing local harness blobs match that parent. The prior temporary venv was unavailable; a fresh Python3.12.14 environment installed Unicorn2.1.4/pyelftools0.33 and temporary diagnostic Capstone5.0.9. Package runtime requirements are unchanged.

The external read-only ZIP's ARM64 member `lib/arm64-v8a/libcocos2dcpp.so` matches SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`. ELF loading/relative and symbol relocations, selected static initialization, platform/ABI/resources and CPU engine services retain024–027 scope. No previous live emulator, saved memory or unpublished script is a runtime dependency.

**Native-integrated:** each final gate executes one connected original ARM64 experiment from ordinary solo entry through chart construction, loading/Director activation, geometry, JNI input, ownership, recording and cleanup. Gate B starts a fresh emulator only after Gate A assertions pass. **Instruction-backed:** field meanings, input quantization, cache-update order, proximity branch and bypass timeout interpretation are supported by targeted disassembly. **Supplied:** synthetic AFF, existing external services, clock schedule, projected JNI inputs and the narrow JNIEnv array ABI. **Unknown/unexecuted:** actual Android batching/hardware timing, GPU/audio fidelity, exact200 boundary, alternate curves, additional colors, one-contact-only crossing and arbitrary-chart behavior. Diagnostic failures are excluded from the final traces.

### Construction and the recovered initialization omission

Fixtures preserve the proposed grammar exactly: timing0/120.00/4.00; ordinary `arc(1000,2000,0.20,0.80,s,0.50,0.50,0,none,false);`; the crossing adds `arc(1000,2000,0.80,0.20,s,0.50,0.50,1,none,false);`. Headers are AudioOffset0 and density1.0. These are synthetic bytes at the established resource-provider boundary, not archived production charts. Ordinary selection remains `sayonarahatsukoi`/difficulty0/base, empty purchase, mode0, speed40, no special map/modifier and zeroed PlayParameters.

The first diagnostic constructed the real arc, produced changing caches and delivered original JNI MOVE, but no arc could activate. Original `0xc98490 → 0x927384` rejected because globals `1c0094c/1bef2e0/1bee968/1bf6c9c` were all0. Thus width/height were degenerate and continuous input clamped Y to0. This was an actual missing initialization in the retained runtime, not a reason to replace eligibility.

004 already located the native constant producers `0x1930aa4–0x1930ae4`. ELF `.init_array` entry **`0x1b95c90` points to complete initializer `0x1930604`**. The new scenario executes that entire routine before GameScene construction; it returns normally using existing ABI services. Original stores produce:

| Native global | Result | Original store PC |
|---|---:|---|
|`0x1c0094c`|180|`0x1930abc`|
|`0x1bf6c9c`|550|`0x1930ac8`|
|`0x1bee968`|250|`0x1930adc`|
|`0x1bef2e0`|100|`0x1930ae4`|

No Python writes these values, and no interior block or branch is skipped. This is reuse of an established original producer, scoped to the new scenario; old scenarios are unchanged. The only new supplied interface is the bounded JNI array contract described below. No separate major renderer/platform dependency appears. Geometry-height global `0x1bf6d80` remains0, so native geometry Y is50, not an assumed300. It is recorded and followed, not visually repaired. Full device geometry initialization remains outside this controlled environment.

Preparatory packaging assertions also corrected the parsed layout to **X0/X1 at+0x20/+0x24, Y0/Y1 at+0x40/+0x44**. A geometry vector append helper is called on capacity-growth paths; inline copies also produce samples, so its call count is not misreported as total sample count. These are observer-contract corrections, not changes to original parser/builder behavior.

### Native objects and geometry provenance

| Connection | Final executed evidence |
|---|---|
|Ordinary startup|Original registry1054f24/menu/setter; ee197c eligibility1/latch1; ee29a8→ee29e8 construction, constructor LRee29ec; no multiplayer helper/direct host scene constructor|
|Loading/activation|Original actions invoke e2ea48; genuine return1; same scene activated through Director, registered/enabled unpaused input listener|
|AFF parsing|1870de0/c2cb1c/924b50; parsed endpoints contain actual f32 .20/.80, y.50/.50, curve string`s`, colors0/1 and false→mode0|
|Arc factory|Original178f7fc→c664f8→17cb97c returns to1865468; RTTI12LogicArcNote/vtable1b91500, native mode0/curveID0|
|Color/linking|Originald93594 creates LogicColor; single mapped0, pair distinct mapped0/1; no successors and group pointer0, so no connected-arc fixture is substituted|
|Samples/checkpoints/index|Original1925084, checkpoint generation and1576aa4 execute; native sample vector and three weight1 records per arc; actual N3/N6 and end2500|
|Current cache|Original scene visit→10a7550→19f3d4c; read-only memory hooks observe cache stores at19f423c, never host interpolation|

Each arc has9 native local samples. Increasing-X samples run `(0,50,0)` to `(510,50,-8089)`; decreasing-X samples run to `(-510,50,-8089)`. The final endpoint is repeated in the actual vector. No sample is removed or regenerated by Python. Checkpoint interval250 and times1250/1500/1750 are original products; native chart counts include only their weight units, not auxiliary bars.

Representative emulated identities:

|Case|GameScene / model / chart / current camera|Arc → color|
|---|---|---|
|Single|4328340 /4357100 /43321c0 /4369e00|4332b40→4332ac0|
|Crossing|4328340 /43580c0 /4332780 /436ae40|4333100→4333080;43333c0→4333340|

Equal scene numbers belong to independent address spaces, not retained state. The model owns the native chart/camera relationship produced by the existing full initializer; the driver does not install a prepared camera or feedback shell. Regression checks use actual factory returns and relational pointers.

### Current geometry, input plane and JNI MOVE

For nonzero-duration ordinary arcs, original consumer `0xc985e0–0xc98618` forms targetX from `trunc(f32(f32(startX*850)-425)) + arc.cache_d4`, and targetY from cache+d8. Native start coordinates quantize to−255/+255. The host reproduces only that input-target composition, with float32 operation order, from original-produced values. It does not compute AFF interpolation. Sample-local Z−8089 is not the input plane: original input projection/spatial observations use Z0.

Original current camera `0xbdbb70` and native Director height720 yield external screen coordinates. At E1000, single target(−255,50,0) projects to `(473.8848876953125,593.0632781982422)`; the second crossing target(+255,50,0) projects to `(806.1151123046875,593.0632781982422)`. Positions are reprojected from changing native caches at every movement sample. Original continuous input clamps Y to100; the first spatial comparison observes point(−254.989501953125,100,0), target(−255,50), and returns1 under native extents. It does not overwrite the arc's native Y50.

Native anchorwall9452/E0 gives wall10452/E1000,10577/E1125,10827/E1375,10952/E1500,11077/E1625,11327/E1875. Sample times are1000/1001/1125/1250/1300/1375/1500/1625/1750/1875. At each time an original Director frame updates caches and processes the previously retained contact, then supplied DOWN/MOVE follows the new target and another original Director frame executes at the same E. Repeated-time frames exercise native record guards. No direct host model-frame, continuous-input or acceptance call is used.

New `src/jni_arrays.py` recovers011's array ABI: synthetic JNIEnv vtable+0x558 GetArrayLength, +0x658 GetIntArrayRegion, +0x668 GetFloatArrayRegion. Its trampolines0x4000400/0x4000410/0x4000420 are emulated host-service addresses, not ELF routines. Only checked one/two-element typed arrays are supported. Host copies external IDs/X/Y/products into JNI-owned staging buffers; it never updates Touch fields. Original JNI MOVE1706960, GLView160b710, EventDispatcher and gameplay MOVE10e7008 execute9 times per case. Each case makes9 length,9 integer-region and27 float-region service calls; no Java VM/framework queue is claimed.

Single Android42 creates native Touch`0x4edaa40`, generatedID0; it remains identical through9 MOVEs. Crossing Android42/43 create Touches`0x4eea900`/`0x4eeaf00`, generatedIDs0/1; both remain retained and coherent through all two-contact MOVE arrays. Current/previous coordinates are original outputs and checked against the delivered float32 inputs/preceding native state. These IDs/pointers are observations, not constants or assignments.

### Gate A — moving control

|Native E|World input-target X from original cache|Owner / bypass|PURE / score / live health|
|---:|---:|---|---|
|1000|−255|0 /0|0 /0 /0|
|1125|−191.1948357|0 /0|1 /3333334 /26.8666667938|
|1300|−101.9810944|0 /0|1 /3333334 /26.8666667938|
|1375|−63.7106018|0 /0|2 /6666668 /53.7333335876|
|1500|0.0315247|0 /0|2 /6666668 /53.7333335876|
|1625|63.8367004|0 /0|3 /10000003 /80.5999984741|
|1875|191.3209229|0 /0|3 /10000003 /80.5999984741|

All19 ordinary arc spatial tests accept; original15dfe2c/15a90c4 perform19 acceptance/claim attempts. Native owner0 matches the retained contact, claimed vector[0], activity1/1 after each following frame. Original recorder1730290 runs3 times;868e54 runs0. Each checkpoint flag has exactly one native0→1 write atf80924.

UP42 atE1875 executes original13db7a0 throughf9a50c, clears owner/claimed ID/retention/map/mask and records native release1875. The next frame1876 clears activity0/0 while score remains unchanged. Gate A completes all assertions before Gate B is created.

The pre-MOVE position frames sometimes score using the previous contact coordinates, which remain inside the broad native spatial region. Therefore this is evidence of joined moving geometry/JNI/ownership, not evidence that every MOVE is indispensable or that a fixed stale point must miss. A separate fresh stale/displaced negative and one-contact crossing are not run; no hypothetical rejection is asserted.

### Gate B — crossing proximity, ownership and cache order

Both native arcs have distinct ordinary colors0/1, independent native samples/records and no successor/group link. Initially generated IDs0/1 own colors0/1. Read-only observations at original `0x19f439c` record the actual distance operand and200 threshold; original branch at19f43a0 rejects distance≥200. Below it, native19f43e4/19f42bc set bypass, and13db7a0 releases owners through the original callsites. Host code only observes these decisions.

|E after following frame|Post-frame separation|Owners|Bypass|Claimed IDs|PURE|
|---:|---:|---|---|---|---:|
|1000|510|0/1|0/0|[0,1]|0|
|1125|382.3896713|0/1|0/0|[0,1]|2|
|1250|254.9054413|0/1|0/0|[0,1]|2|
|1300|203.9621887|0/1|0/0|[0,1]|2|
|1375|127.4212036|−1/−1|1/1|[]|4|
|1500|0.0630493|−1/−1|1/1|[]|4|
|1625|127.6734009|−1/−1|1/1|[]|6|
|1750|255.1575928|−1/−1|1/1|[]|6|
|1875|382.6418457|−1/−1|1/1|[]|6|

At1500 the native X order has reversed, with targets+0.0315246582/−0.0315246582; this is a near-crossing observation, not a claim that mathematical midpoint and native intersection are bit-identical. Atfollow1375 the original color-claim routine accepts **both generated IDs for both bypassed colors**, leaving owners−1. Two contacts are present; no separate one-contact-only trial is implied. Checkpoint recorders use their native frame route, not an invented exclusive contact attribution.

**Important cache-order result:** atposition1750, original proximity first compares distance **191.4154968262**, then255.1575927734. The loop updates one arc cache and compares against the neighbor before that neighbor's cache is updated. The first value combines fresh X127.5787964 with the neighbor's preceding X−63.8367004. It legitimately passes the original<200 comparison and refreshes both bypass timestamps to1750, even though the complete frame's separation is255.1575928. The two subsequent follow1750 comparisons both see255.1575928. These native comparison operands are distinct from the host-derived post-frame separation column; they must not be conflated.

This mixed-cache explanation is instruction-backed by19f423c's cache store followed by19f429c's active-arc comparison loop and the stored native distance trace. It is not a rewritten proximity rule. Original color updater1482cb0 clears bypass only when its recorded time+500<E (absent other resets); atE1876, timestamp1750 has not expired. Thus persistence after separation is expected from this observed schedule. Future end/reset behavior is not executed here.

All recorded post-follow conflict bytes are0. Native color-claim attempts total50;76 arc spatial tests and41 native proximity comparisons execute. Some foreign-contact spatial tests reject while arcs are separated. There are30 release-routine entries, including repeated already-unowned releases and4 terminal color callbacks; that count is not30 distinct ownership changes. The initial proximity releases use time argument0 while bypass is set and leave release fields−1. Subsequent UPs also leave those already-unowned fields−1.

Original checkpoint decisions yield PURE2/score3333335/H27.0666656494 at1125, PURE4/6666670/H54.1333312988 at1375, PURE6/10000006/H81.1999969482 at1625. Both arcs resolve1250/1500/1750 once through originalf80924→1730290. FAR/LOST remain0. Color bypass permits shared acceptance, while checkpoint resolved flags prevent duplicated awards across two contacts and repeated-time frames.

After both UPs, native mappings/slot pointers/mask/retention/claimed vector are empty; both owners−1. Next-frame1876 activity is0/0. Bypass remains1/1 and timestamps1750; it is not manually cleared to make cleanup look complete. Score/gauge are unchanged by cleanup. No results object is created: completion count0 and ScoreState+68 null.

### Reproducible source, validation and boundaries

New source: `src/moving_arc.py`, `src/jni_arrays.py`; new fixtures: `native_moving_arc.aff`, `native_crossing_arcs.aff`; CLI/config/README add the bounded scenario. Config's `crossing_arc` is internal selection, not another exposed command. The CLI rechecks the external archive for each fresh case, executes Gate A before Gate B, and returns a truthful partial-control/failure report if B raises. Assertions require original constructor/initializer/index paths, cache writes, persistent Touch identity, native spatial/claim/activity, unique record writes, recorder outputs and cleanup. Direct host calls/replacements of gameplay construction, geometry, continuous input, arbitration or recording are prohibited by assertions.

```bash
python research_harness/run.py --archive /path/to/arccopy.zip \
  --scenario moving_arc --output /path/to/moving-arc-result.json
```

The final two-gate invocation passes, with275189-byte JSON containing both original traces, native geometry/caches, camera/input projections, actual proximity operands, ownership/writes, array-service calls, checkpoint/score evidence and boundaries. Earlier zero-global diagnostic and parser-observer assertion failure are not spliced into this execution. No generated output is committed. The existing025 OBJ/libc helper is installed unchanged for reuse but receives **zero calls** in both fixtures; no new resource-reader ABI is needed.

Fresh current-source validation: ordinary two-tap end-to-end PASS; chord forward/reverse PASS; existing arc-tap native unittest PASS; hold dual-case native unittest PASS; missing archive/wrong hash/native unavailable-song controls all PASS. All existing native test switches were enabled:5 discovered tests passed, no skips. The new CLI itself performs both complete gate assertions; no redundant wrapper is added. No previous fixture, scenario source/assertion, test or requirement is changed.

Exact inherited PC skips remain f72110→f72158,16a4238→16a48d8,121581c→121584c,a507c4→a519ec,a51adc→a5213c,196fdac→196ffac,891190→89164c,891688→89219c,8921dc→8928e0. Last3 results ranges are not reached by these fixtures. Base traversal/render/flush129c924/1017a84/13edf0c remain inert; native TrackLayer CPU19069a0 stays enabled. Existing catalog/profile/settings/platform/JNI/libc/C++/math/clock/resource, presentation/texture proxies, GPU/audio and allocator/autorelease/reclamation limits remain. Native static spatial initialization is now executed only for this scenario; geometry-height0/Y50 remains explicit. Inherited private DB preparation is not a save experiment. No full Android application, GPU picture, production audio, device timing or arbitrary arc compatibility is claimed.

G-001–G-003 remain Verified; G-004 becomes Verified—028 with appended decision history; G-005–G-010 statuses are unchanged. Publication is restricted to10 authorized paths: this report/context/backlog, harness CLI/config/README,2 new fixtures and2 new source files. Historical context remains an exact prefix; reports001–027, root README/instructions, all prior fixtures/assertions/tests and unrelated old blobs are preserved. No ZIP/library/assets/dump/database/generated output/environment/secret is included. The final handoff records the exact publication SHA, readback and parent-tree checks. No029 is initiated.

## Pseudocode

```text
for single_control, then crossing_pair only after control passes:
    verify external archive; create fresh original ARM64 runtime
    execute complete original1930604 static initializer; observe native spatial globals
    supply established offline/platform/ABI resources and bounded JNIEnv array methods
    original registry/menu/ordinary solo entry → native GameScene/loading initializer
    original AFF parser → ordinary arc factories/colors
        → original sampled geometry/checkpoints/count/index/model/camera
    original initializer returns1 → Director activates same scene

    for each sparse native E:
        Director visit → original current-position caches/proximity/color logic
        derive external target from native start quantization + current cache, Z0 input plane
        original camera projection + native height/Y conversion → supplied JNI coordinates
        first sample: JNI DOWN → original Touch retained/generated ID
        later samples: JNI MOVE arrays → same original Touch current/previous coordinates
        another Director frame at same E:
            original spatial eligibility → native color claim/bypass/activity
            original checkpoint guards/recorders/gauge

    crossing observations:
        separate owners initially
        native<200 comparison → bypass → owner release
        original sequential cache order can compare fresh versus older neighbor
        both bypassed colors accept either retained ID; records still resolve once
        post-separation bypass persists under native timestamp reset rule

    JNI UP → original ownership/contact cleanup
    next original frame clears activity; preserve actual remaining bypass state
    assert unique native record writes, score/gauge and no host gameplay-state substitution

run unchanged ordinary/arc-tap/hold/chord regressions and negatives
update only G-004 status/history; publish scoped source/evidence; STOP before029
```
