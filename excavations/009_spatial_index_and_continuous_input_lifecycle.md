# Expedition 009 — Runtime Spatial Index, Scheduling & Continuous Note Lifecycle

Date: 2026-10-23. Project Arconist, repository `thgillwtnorizoh/arconist`, existing `main`.

## Result

**The minimum objective is met.** Original model-initializer instructions allocate the per-timing-group maps, original producer **`0x1576aa4`** inserts runtime objects, and original active-range updater **`0x10fd1c0`** consumes their output. No note-to-bucket assignment, map node, balancing operation, or active-range membership is supplied by the successful replay harness.

**Strong outcomes:** four-tap and 100-tap replays reach native score/gauge and GameResult classification with the native-produced index. The regular-tail versus large-jump discrepancy **survives**: 90 accurate hits give recorded/final LOST **10/10, H70** with regular tail frames, versus **9/10, H72** with one tail jump. This is now scoped execution of the actual index producer and consumer, not an extrapolation from Expedition 008's fixture.

**Additional integration milestones:** ordinary arcs acquire LogicColor ownership from native projection/continuous input, then resolve native checkpoints into score/gauge/results without a supplied activation flag. Original connected-arc linking/group production joins a weight-2 checkpoint to two actual recorder calls. Native Scheduler → ActionManager → MoveBy execution replaces the earlier captured action queue in a separate camera test. The outer frame is located in **GameScene's scene-visit path**, after the Director's Scheduler phase, with a once-per-Director-frame guard.

Flick construction remains a concrete gap: a prepared parsed FlickNote is discarded by the tested original chart builder, and no LogicFlickNote vtable was found in the inspected relocation relationships. Native flick-predicate boundary execution is retained as **Native-isolated**, not misrepresented as a full playable flick replay.

These are synthetic-environment ARM64 executions. Android/GL-thread queues, real input hardware, audio output, complete scene teardown, GPU drawing, persistence, and special-mode reachability are not emulated.

## What I Found

### 1. Fresh preparation, identities, and evidence conventions

Read the supplied project instructions, inspected the ZIP/native libraries and relevant smali, read current `context.md` and Expedition 008's full report, and consulted reports 001–007 for parser layouts, clocks, projections, ownership, gauges, and rendering. No temporary state from an earlier conversation was available or used. Fresh local harnesses were constructed for this expedition.

Initial repository commit: **`d1e211494375fe17d9d4e27fc4f4c096ba2a6c92`**. Initial root tree: `8841c04c0a072454688e2ba450f01812c474d09d`. Initial working tree was clean on `main`.

| Source | Verified SHA-256 |
|---|---|
| Supplied `arccopy.zip` | `5dc2f3d1f5387d0c5da06ad72694105cdd7fa4b7ff80f981f77998e89eb2b4cb` |
| Supplied project instruction text | `8a9bea2e002d6ce282dc7b92592379927088a2ecbab2e451b585aea4c921f1e8` |
| `lib/arm64-v8a/libcocos2dcpp.so` | `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` |
| `lib/arm64-v8a/libfmodProvider.so` | `db07590708c1e2b7ed3a17800a8839392d5a7a8322cd102d5b35bda05b251bfb` |

Main-library Build ID: **`17d660edbf37ca78beefc32e07672c97419ddce6`**. All native addresses below are **main-library ELF virtual addresses before relocation**. No provider execution is newly claimed. PT_LOAD mapping is used; data file offsets are not assumed equal to VAs.

- **Confirmed:** decoded instructions, original metadata/relocations, or the specifically scoped execution described.
- **Synthetic:** supplied fixture data, object shells, configuration, clocks, driver scheduling, or runtime services.
- **Interpretation:** meaning inferred from those observations.
- **Unknown:** missing producer, reachable mode, thread relationship, or unexecuted path.

Descriptive function names/interfaces are researcher labels; RTTI names are recovered identities. Original binaries, assets, project instructions, README, reports 001–008, and previous context text are preserved.

## Spatial-index construction and object layouts

### 2. Allocation, callers, and exact producer

**Confirmed original construction chain:**

```text
model factory 0xc9f6f0
  -> initializer 0xfbfd04
     -> block 0xfc0184..0xfc0280: allocate one map header per chart timing list
     -> block 0xfc0280..0xfc02a4: traverse chart main object vector
        -> 0xfc0294: call 0x1576aa4(model, object)
```

The successful index-building call executes **`0xfc0184` through just before `0xfc02a4`**, with X19=model and model+28=chart. It runs the native outer vector growth, map-header initialization, object traversal, producer, map insertion/balancing, and bucket-vector retain/append. It does not execute unrelated earlier account/score/audio initialization in `0xfbfd04`.

A whole-text direct B/BL scan finds a second producer callsite **`0xea5934`**, inside `0xea5474`. That caller constructs additional holds, generates records, calculates their depths, appends them to chart+20, then calls the same producer. This establishes an incremental insertion path beyond initial chart loading; that enclosing scene-specific path was not executed as a complete scene.

The other confirmed map modifier is **the updater itself**: `0x10fd78c..0x10fd7ec` inserts an empty map node when a queried key does not exist. Therefore a map dump after gameplay contains lookup-created empty buckets as well as producer-populated buckets. No original bucket-member removal was found in these producer/updater paths. This is a scoped writer/callsite inventory, not a claim to have proved the absence of every indirect writer in the binary.

### 3. Layouts

| Owner | Offset | Native role |
|---|---|---|
| Model | +28 | chart pointer |
| Model | +88/+90/+98 | vector begin/end/capacity of **map-header pointers**, one per timing group |
| Model | +a0/+a8/+b0 | retained active-object pointer vector |
| Model | +18 | signed lookahead-depth configuration; fixture 10000 |
| Chart | +20/+28/+30 | main runtime object vector |
| Chart | +38/+40/+48 | vector of pointers to per-group timing-list headers |
| Chart | +50/+58/+60 | timing-group descriptor vector |
| Group descriptor | +0/+4 | active byte / signed end time |
| Runtime note | +18/+1c | signed start/end time |
| Runtime note | +30/+34 | current signed start/end depth |
| Runtime note | +38/+3c | precomputed signed start/end depth |
| Runtime note | +50/+54 | signed timing-group index / input-enabled byte |
| Map header, 24 bytes | +0/+8/+10 | leftmost / root (sentinel is header+8) / node count |
| Map node, 64 bytes | +0/+8/+10/+18 | left/right/parent / tree color byte |
| Map node | +20 | signed i32 key |
| Map node | +28/+30/+38 | vector begin/end/capacity of retained object pointers |

Header construction at `0xfc01d8..0xfc01e4` sets root=0, size=0, leftmost=header+8. Nodes are allocated by original code and balanced through **`0x1257490`**. Bucket and active vectors append through **`0x1082558`**, which calls retain helper `0x147fe48`. Allocator/refcount services are supplied, but their callsites and native container mutations execute.

### 4. Exact key generation

Let `D(chart,t,g)` be original float32 timing/depth integrator **`0xcf918c`**. Its confirmed per-timing contribution is:

```text
bound = timing.end if timing.end < t else t if timing.start < t else SKIP
D -= f32(f32(bound - max(timing.start,0)) / timing.scale)
```

The producer first chooses **min/max endpoint TIMES**, evaluates D twice for the object's group, divides each result by **float32 −10000.0**, then uses **FCVTZS W** (signed conversion toward zero). It sorts those two converted keys and appends the object to **every integer key inclusively** between them:

```text
t0 = min_i32(object.start, object.end)
t1 = max_i32(object.start, object.end)
k0 = fcvtzs_i32(f32(D(chart,t0,object.group) / f32(-10000)))
k1 = fcvtzs_i32(f32(D(chart,t1,object.group) / f32(-10000)))
for k = min_i32(k0,k1) through max_i32(k0,k1):
    native_map[object.group][k].push_back_retain(object)
```

Decisive instructions: time selection `0x1576acc..0x1576ae4`; integrator calls `0x1576b58/0x1576b6c`; divisions/conversions/range selection `0x1576b70..0x1576b94`; bucket loop and append `0x1576bbc..0x1576bd0`.

**Important distinctions:**

- The producer does **not** read precomputed integer depths +38/+3c. Replacing it with a key computed from already-truncated depth is not the recovered operation.
- It does not sample every timing change inside a long note. Reversing scroll can have an interior depth extremum absent from its endpoint-key interval.
- Ordinary insertion has no note-type/input-enabled filter. It indexes objects passed by the chart-main-vector caller, including nonjudgment events. Timing records live in separate timing lists in the tested builder. Children are not recursively traversed by `0x1576aa4`; arc-taps are reached through parent/child handling unless independently present in the main vector.
- Within a bucket, order is **producer-call order**, not a new timing sort. Initial traversal follows chart+20 order. Keys are tree-ordered signed integers. Repeating producer insertion appends a duplicate; the producer does not deduplicate. The updater separately suppresses duplicate active pointers.

**Mode-4 exception:** if global configuration getter `0xbda064` returns 4 and dynamic_cast to **LogicSceneControl** succeeds, local t1 becomes **180000**, and that group's end is raised to at least 180000 (`0x1576b18..0x1576b48`). The object's own +1c is not changed. This is a fixed local upper-time override, not a universal max-with-note-end formula. The setting's complete product/mode reachability remains unverified.

### 5. Executed producer tests

All entries below come from original insertion, not Python-created nodes or assigned buckets. Times are synthetic chart inputs.

| Fixture | Native-produced membership |
|---|---|
| Four taps 1000/2000/2049/3000; tempo120, speed6 | key1:[1000], key2:[2000,2049], key3:[3000] |
| Hold 1000..2000; same timing | keys1 and2 both contain that hold |
| Hold 3000..23000; tempo60/speed1 | keys0,1,2 all contain that hold |
| Separate group, tempo60/speed2, arc at10000 | group1 key2; group0 unaffected |
| Ordinary synthetic noinput tap at1000 | remains present in key1 |
| Reinsert first object into an existing bucket | previous [object0,object1,object7] becomes [object0,object1,object7,object0] |
| SceneControl at1000, mode4, tempo60/speed1, initial group end100 | keys0..18 inclusive; group end180000 |
| Flick-shaped layout at12345, tempo60/speed1, ordinary mode | key1; **descriptor-only**, not an original constructed LogicFlickNote |

Exact signed boundary checks, native timing initializer `0xbe2b98`:

| Timing | t9999 | t10000 | t10001 |
|---|---:|---:|---:|
| tempo60, speed1 | 0 | 1 | 1 |
| tempo60, speed2 | 1 | 2 | 2 |
| tempo120, speed6 | 11 | 12 | 12 |
| tempo−60, speed1 | 0 | −1 | −1 |
| tempo60, speed0 | 0 | 0 | 0 |

With tempo−60/speed1: times0/1/9999 → key0; 10000/10001/19999 → key−1; 20000/20001 → key−2. Thus negative noninteger quotients truncate toward zero, not floor. Negative timestamps under the ordinary timing starting at0 also map to0 because this integrator contributes nothing before that timing starts; negative timestamps and negative scroll depth are different tests.

Reverse fixture: timing0..10000 at scale1, timing10000 onward at scale−1, hold5000..15000. D at both endpoints is −5000, but D at10000 is −10000. **Only bucket0 is populated**, not bucket1. This confirms endpoint-only coverage, not a swept-depth-extrema index. Mixed-group test also executed an arc5000..25000 and equal-time taps in the reversed group; their endpoint keys were0 and same-key insertion order was preserved.

Original ArcNote/ArcTapNote identities were used in the mixed-layout producer test. The complete original arc factories and native links also feed the index in the joined arc tests below. Full AFF arc-tap factory/child-generation integration is not newly closed.

### 6. Lifetime and destruction: bounded findings

The model factory zeroes the index vector at `0xc9f794..0xc9f7d4`; initializer allocation follows. The tested initializer block appends headers; it is not a standalone reusable clear-and-rebuild API. The start of `0xfbfd04` explicitly releases/clears the active vector and projected-contact records, while the inspected index-building block assumes appropriate existing index state. Production repeated initialization was not established.

Normal model destructor **`0x16d3f20`** releases chart/timeline/score and retained active/candidate/contact vectors. Its index tail **`0x16d4118..0x16d4124`** resets index-vector end and deletes the **pointer buffer**. It does not iterate/delete pointed-to map headers or their nodes in that normal path. Scoped execution `0x16d3ffc..0x16d4128` logged freeing the active buffer and index pointer buffer, with map-header address absent from frees. It does not prove a complete application leak or exclude an earlier external owner/cleanup path. **Complete map/header reclamation remains unknown.** Do not silently give the reference model an owning-map destructor that these instructions do not show.

## Active-note admission/expiry equations

### 7. Query interval and admission are separate from judgment expiry

For each active group, the updater computes:

```text
A = f32(-D(chart,E,group))
B = f32(-D(chart,signed32(E+120),group))
back = 700                       # ordinary chart+110==0 query configuration
lo = min(fcvtzs(f32((A-back)/10000)), fcvtzs(f32((B-back)/10000)))
hi = max(fcvtzs(f32((A+lookaheadDepth)/10000)), fcvtzs(f32((B-back)/10000)))
```

Each subtraction/addition/division uses the original f32 boundaries. `0x10fd6a4..0x10fd704` implements this range. Extended chart+110 takes camera-derived values instead of the ordinary constants; that branch is instruction-backed here, not newly executed.

For every queried bucket, existing active pointers are skipped. A new candidate gets its original depth-update virtual called before admission. Ordinary admission requires **min(currentStartDepth,currentEndDepth) < limit**, with **limit700 for an exact LogicArcNote identity, 300 otherwise**, followed by native resolved/special-type handling (`0x10fd880..0x10fd980`). Do not apply the arc's700 to taps. LogicBar and trace/zero-duration arc branches have special retention conditions; not every resolved object is rejected identically.

Retained objects are updated first. An inactive group removes its retained objects. Otherwise removal depends on native vtable+28 terminal state (or model.finished), an arc-child condition where applicable, and **E > object.end** (`0x10fd558..0x10fd638`). The retained path does not reapply the new-admission depth threshold. This hysteresis is central to the frame-gap result.

**Visible depth, indexed presence, active membership, and judgment eligibility are four different states.** Whole-bucket querying also means lookahead is not a precise admission front plane: at E0 a tap1000 with depth−12000 is admitted in the lookahead10000 fixture because queried bucket1 contains it.

### 8. Exact admission, expiry, and catch-up tests

Tempo120/speed6, tap time1000:

| Schedule | Active at tested frame | Actual recorded LOST |
|---|---|---:|
| First frame1024, depth288 | yes | 0 |
| First frame1025, depth300 | no | 0 |
| First frame1100 or1101 | no | 0 |
| Admit at1000, then1100 | yes | 0 |
| Admit at1000, then1101 | yes during expiry pass | 1 |

The last row invokes original miss recorder **`0x868e54`** and gauge path; later range maintenance removes the resolved note. The expiry threshold remains strict **E>end+100**. A never-admitted note cannot receive that callback merely because its timestamp has become old.

For a fresh first frame2000, followed by2001/2100/10000/19999, with chart end deliberately20000, the time1000 note remains inactive and recorded LOST stays0. No catch-up sweep appears in this executed path. Conversely, a note admitted atE0 is retained through a jump to10000 and does receive its miss. Retained state, rather than jump size alone, determines the difference.

Native pause wrapper/timeline tests at E1026 freeze effective time through5000 ms; active membership remains the two admitted notes, and resume plus1 ms yieldsE1027. The model pause gate is1 then0. Audio pause/seek are supplied service boundaries. This demonstrates retained state across pause, not every foreground/seek transition.

### 9. Native-index replays and actual counters

Four-tap fixture from008: times1000/2000/2049/3000, same timing/speed, N4. Native frames and selected native judgment entries at1008/2051/2051 reproduce:

| E | Native active times before input | PURE/FAR/recorded LOST | Score | Live H |
|---:|---|---|---:|---:|
| 1008 | 1000,2000,2049 | 1/0/0 | 2,500,001 | 20.200000762939453 |
| 2051 | 2000,2049,3000 | 1/1/0 | 3,750,001 | 30.30000114440918 |
| 2051, second input | 2049,3000 | 2/1/0 | 6,250,002 | 50.5 |
| 3100 | 3000 retained | 2/1/0 | 6,250,002 | 50.5 |
| 3101 | 3000 receives miss | 2/1/1 | 6,250,002 | 48.5 |
| 3121 | finished | 2/1/1 | 6,250,002 | 48.5 |

The native GameResult query gives final LOST1, integer H48, category0. Index construction uses the original initializer block/producer. The direct selected-judge four-tap replay is distinct from the fully projected100-tap replay below; no candidate-selection coverage is invented from the direct calls.

100-tap generator: time `1000+i*150`, raw lane `1+i%4`, i0..99; N100, end15970, ordinary mode0, H0, no ability. Original timing/position/tap initialization, native pre-depth integration, producer/index/range, whole model frame, actual note guards/recorders/gauge and native final snapshot/query execute. In the projected replay, screen/design X cycles290/540/740/990, Y360, contact IDs100+i, and **`0xeec024`** performs projection, collection, sorting and judgment. No tap acceptance is supplied.

| Hits | Missed-tail frame interval | Recorded LOST | Final LOST | Live H | Final integer H / category |
|---:|---|---:|---:|---:|---|
| 89 | 16,100,500,1000 ms, each tested | 11 | 11 | 67 | 67 / 0 |
| 89 | single jump to15970, then15971 | 10 | 11 | 69 | 69 / 0 |
| 90 | 16,100,500,1000 ms, each tested | 10 | 10 | 70 | 70 / 1 |
| 90 | single jump to15970, then15971 | 9 | 10 | 72 | 72 / 1 |

For each regular schedule, start tail frames one interval after the final hit and stop before15970, then run15970 and15971. Separate projected-input100 ms and jump replays give the same90-hit rows. Scores are8,900,089 /9,000,090 respectively. The unrecorded note in the jump cases is **time15850**. It is in the native map but was not retained before the jump; at15970 its depth is already beyond new admission. Synthesized LOST does not invoke retroactive gauge damage. These are controlled native schedules, not a claim about frequency on actual devices.

Native N is obtained with **`0x11ea120(chart,INT_MIN,INT_MAX)`**, asserted against fixture expectations and stored before original score/gauge factories. Finalization is a driver call of `0x1600bb0` after the native frame's finished transition; the scene delegate is a logging/no-op boundary in these009 replays. **Do not mislabel the final snapshot as a direct GameScene termination chain in this expedition.** Expedition008's earlier real-scene snapshot evidence remains separately scoped.

### 10. Hold fixture and boundary distinction

Rebuilt the008 hold fixture through **`0x1862a14` from prepared parsed Timing/HoldNote objects**, with original numeric-position conversion, hold factory, checkpoint generator, group-end tail, and native index. This does not rerun the AFF lexer/body parser; the prepared parsed-data boundary is explicit. Original builder output is one LogicHoldNote, records1250/1500/1750, N3, end2500, keys1/2.

Begin at1000 acquires the initial latch; retained Touch processing through native frames activates at1001. At1124 there is no score;1125/1375 resolve the first two records. Native end cleanup receives a **vector of Touch pointers**, following a timeline refresh to1375. Frames2249/2250 demonstrate no miss / one actual overdue miss;2501 finishes. Native final result: score6,666,668, PURE2/LOST1, H51, category0; live H51.733333587646484.

Additional ordinary hold probes:

| E | Initial latch after fresh begin | Active after continuous processing |
|---:|---:|---:|
| 880,900 | 0 | 0 |
| 901,999,1000 | 1 | 0 |
| 1001,1999 | 1 | 1 |
| 2000,2001, fresh late begin | 0 | 0 |

A separately already-latched hold remains latch1 at1999/2000/2001, but active changes1→0→0. Thus equality at end rejects continuous activation even with a retained latch. Full fixture state/cadence matters; the late fresh-boundary cases are not presented as clean complete-song scores.

## Scheduling and lifecycle traces

### 11. Outer scheduler and GameScene visit: newly identified connection

Original Android `Cocos2dxRenderer_nativeRender` **`0xe181d0`** calls Director virtual+38 then+40. The concrete Director vtable `0x1b5eaf8` resolves them to **`0x17371d8`** and `0xcda578` respectively. The ordinary nonstopped branch of the first enters **`0x1793f8c`**.

Inside `0x1793f8c`, clock/dt preparation precedes an event dispatch at `0x1793fe8`, Scheduler **`0x13d3f44`** at `0x1793ff4`, a second event dispatch at `0x1794000`, and scene traversal. Scheduler executes its negative/zero/positive update lists before timers and deferred callbacks. Director initialization registers the ActionManager callback with **priority INT_MIN** (`0x18b3cd0..0x18b3d00`; referenced constant0x4c340c). Its function-object call operator **`0xd630b8`** forwards dt to ActionManager **`0x9effe0`**. This ordering is recovered from this binary, not assumed from another Cocos release.

The new crucial connection is **GameScene vtable `0x1ae6ef0`, virtual+338 = `0x18be2f8`**, a scene-visit override. It checks visibility and compares **Director+134** with **GameScene+4d0**:

- same frame counter: tail into base scene visit `0x129c924`, without a model frame;
- different: **`0x18be37c → 0x10a7550(model=scene+3e0, scene)`**, then HUD/render-state work, base visit, and finally copy current Director counter into scene+4d0 at `0x18be470..0x18be478`.

Thus gameplay update is **visit-driven with a per-Director-frame guard** in this path. Multiple camera visits do not imply repeated gameplay advancement. Scheduler/ActionManager execute before this traversal. Full input-queue positioning relative to those phases is still not executed.

Scoped native visit execution used the original prefix/model-frame/counter-store/epilogue, with only the intervening HUD/base-draw subtree skipped `0x18be380 → 0x18be470`; equal-counter base visit was suppressed. Counters5/5/6 yielded:

```text
visit5: clock -> range -> arc cache -> continuous contacts -> expiry/checkpoints -> gauge -> return
visit5: return, no gameplay frame
visit6: clock -> range -> arc cache -> continuous contacts -> expiry/checkpoints -> gauge -> return
```

No manual frame-counter stamp replaced the original store in the successful final run.

### 12. Original Scheduler → ActionManager → camera action execution

A separate test executes original Node runAction **`0xc7820c → 0xb3dc38`**, original ActionManager insertion, Scheduler `0x13d3f44`, native function-object callback `0xd630b8`, ActionManager `0x9effe0`, and original MoveBy action virtuals. Manager constructor `0x81a0b8` and MoveBy factory `0xf1b510` execute. The Scheduler list entry and Director environment are prepared; the action queue itself is native, not captured and stepped by Python.

| Native Scheduler dt | Camera X after native action update |
|---:|---:|
| 0, first tick | 0 |
| 0.5 s | 150 |
| 0.5 s | 300 |

Action: +600 X over2 seconds, initial X0, running Node. This confirms the earlier first-tick rule inside an actual ActionManager/Scheduler chain. It is a representative translation test, not full scene/Scheduler pause/rotation/reset/GPU integration. Combined with the visit callsites, camera actions can change camera state before subsequent gameplay projection. An Android touch delivered before that Scheduler update may instead observe the previous state; the actual GL queue schedule is not claimed verified.

### 13. Android and input scheduling boundaries

Relevant smali: `smali_classes3/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali`, its `$5`–`$10` Runnable classes, and `Cocos2dxRenderer.smali`. Current inspection agrees with004/005:

- capture elapsedRealtimeNanos converted to milliseconds in `getTouchTimestampNow`, before `queueEvent`;
- Runnable stores IDs/coordinates/pressure product and that captured timestamp; no inspected MotionEvent historical-sample loop or getEventTime substitution;
- renderer forwards to JNI begin/move/end/cancel (`0xbe31a8/0x1706960/0xdda71c/0xd8dc50`), then GLView/listener dispatch;
- begin creates/updates a Touch and generated gameplay contact ID; continuous frames read its current converted coordinates;
- end and cancel are distinct event actions/callbacks, but ordinary model-gated callbacks **`0xd88408` and `0x18ba6d8` both call `0xf9a50c`**. This cleanup takes a **Touch-pointer vector**, not a single Touch object. Native cleanup was executed; the full two Android transports were not.

Multiple queued callbacks are not restricted to one per gameplay visit by the inspected native input callback. Two original begin calls between frames demonstrate the behavior directly:

| Operation after frameE1000 | Last-frame global | Effective input E | Cached note depths | Result |
|---|---:|---:|---|---|
| begin with controlled clock1020 | 1000 | 1020 | 0,−588 | first shining PURE |
| another begin at1026, no intervening frame | 1000 | 1026 | 0,−588 | second shining PURE |

Final PURE2/score10,000,002/H80.4000015258789. Timeline advances while geometry remains cached. This is controlled callback scheduling; Java/GL-thread queue execution and OS wakeups remain unverified. Stored Android timestamp is not the native judge clock.

Foreground/background and arbitrary seek/scene replacement were inspected only through prior005 evidence and current pause/queue wrappers. No complete Android lifecycle reset trace, universal action cancellation, or automatic index rebuild on seek is asserted.

## Arc/flick integration evidence

### 14. Ordinary arc: original object through ownership, checkpoints, gauge, result

New joined chain:

```text
0x178f7fc -> 0xc664f8 -> 0x17cb97c       original arc factory/initializers
0xba81e8 -> 0xd92558                   native records
0x1925084                             native geometry samples
0xfc0184..0xfc02a4 -> 0x1576aa4         native spatial index
0x10a7550 -> 0x10fd1c0 -> 0x95d61c     ranges/depth/contact reset
             -> 0x19f3d4c             current geometry/color state
             -> 0x14858d4             retained Touch projection
                -> 0xc98490 -> 0x927384 -> 0x15dfe2c -> 0x15a90c4
             -> 0xf8056c -> 0x1730290 -> actual arc guard/gauge/score
native snapshot 0x1600bb0; driver queries 0x1315038 / 0x12a5574
```

Fixture: ordinary mode0 arc1000..2000, x0=x1=.5, y0=y1=.5, linear curve0, density1, tempo120/speed6; original LogicColor factory **`0xd93594(0)`**. Geometry height global0x1bf6d80=500 gives Y300. Controlled design1280×720, orthographic projection diagonal(1/1280,1/720,1,1), native Camera Node Z900; retained Touch design(640,210), generated contact ID1 supplied. Spatial defaults180/100/250 are supplied from recovered initializer values. This is not the game's production perspective camera configuration.

The initial retained Touch vector is a driver boundary. No +64/+65 arc activation, +d0 eligibility/cache flag, owner ID, bypass, or checkpoint resolution flag is injected. Original cache/continuous/ownership code establishes them. Render feedback object is a shell whose +530 virtual points to original **`0x155241c`**; it writes its real feedback latch. Audio request is stubbed.

| E | Active-contact byte | Owner | PURE / LOST | Live H |
|---:|---:|---:|---|---:|
| 999 | 0 | −1 | 0/0 | 0 |
| 1000 | 1 | 1 | 0/0 | 0 |
| 1125 | 1 | 1 | 1/0 | 26.866666793823242 |
| 1375 | 1 | 1 | 2/0 | 53.733333587646484 |
| 1625 | 1 | 1 | 3/0 | 80.5999984741211 |
| 2001 | 0, no longer active-range member | 1 | 3/0 | unchanged |

Final score10,000,003, final LOST0, integer H80, category3. The owner remains1 when this synthetic contact is never lifted; active-range expiry alone must not be described as universal ownership release. Native end cleanup releases matching owners, while other color/end/group reset fields have separate rules.

### 15. Interruption, re-entry, ownership competition, and overlap

Moving the same Touch to designX1200 atE1200 clears active-contact state but retains owner1. Re-entering X640 at1300 restores native activation and all three checkpoints succeed. In another schedule, contact remains outside untilE2000: earlier unresolved checkpoints have not yet hit their overdue cutoff; re-entry resolves both remaining units as PURE. This is a schedule-specific checkpoint tolerance result, not a universal no-penalty interruption duration.

Actual lifting is different. `0xf9a50c` calls **`0x13db7a0`**, removes the retained pointer, clears matching ownership and claimed-ID entry, and records release time when its conditions hold. For a longer1000..4000 arc, native timeline refreshed to1200 before cleanup gives release1200. A new ID2 contact:

| E | Owner / activation | Counter consequence |
|---:|---|---|
| 1200,1300 | −1 / inactive | one earlier PURE remains |
| 2199 | −1 / inactive | overdue processing records one LOST |
| 2200 | 2 / active; release reset−1 | three newly due PURE units; cumulative PURE4/LOST1 |
| 2201 | 2 / active | no duplicate unit |

The gate uses integer interval from the arc and `now-release < trunc(min(4*intervalInteger,1000))`; interval250 gives strict1000, equality accepted. Cleanup uses current GameTimeline E: deliberately releasing before a clock refresh recorded the previous E1125 in an exploratory schedule. That difference is caller scheduling, not Android event-time compensation.

Two colors at x.25/.75 with separate contacts: native owners1/2, PURE6/LOST0, score10,000,006, H81.19999694824219, final integer81/category3. With one contact only at the first location: PURE3/LOST3, H34.599998474121094, category0.

A stronger ownership-arbitration test puts both spatial regions under the same point:

| Arc normalized X pair | Contacts at design(640,210) | Native bypass bytes | Owners | Active arcs atE1000 |
|---|---:|---|---|---|
| .35/.65 (quantized separation254) | 1 | 0/0 | 1/−1 | first only |
| .35/.65 | 2 | 0/0 | 1/2 | both |
| .4/.6 (separation170) | 1 or2, tested | 1/1 | −1/−1 | both |
| .5/.5 (coincident) | 1 or2, tested | 1/1 | −1/−1 | both |

The overlap exception is produced by **`0x19f4390..0x19f43f0`**: different ordinary colors with eligible caches and distance **<200** set the bypass/release state. The same contact then activates both via native code. This newly makes an ownership bypass reachable through geometry, rather than supplying +10 manually. Do not assert an unconditional one-contact-per-color rule or equate every overlap with the same branch. Moving crossing curves and exact distance200 were not separately tested.

### 16. Connected arcs and weight-2 callbacks without supplied activation

Two factory-built ordinary arcs1000..2001 and2001..3001 share the same original LogicColor. Original chart linking/group builder **`0x125e474`** executes on their chart vector; it produces a shared nonnull **LogicArcGroup**, first successor vector containing the second, and corresponding linked state. No group activation flag is supplied.

Native arc generation with explicit generation flag1 yields:

```text
first:  (1000,1), (1250,1), (1500,2)      # four units
second: (2001,1), (2251,1), (2501,1), (2751,1) # four units
```

Generation flag1 is a supplied call parameter, not proof of its selection for every chart mode. Group/link production, record modification, geometry, index, ownership and checkpoint scoring are native.

| E | Native active-contact flags, first/second | Cumulative PURE | Live H |
|---:|---|---:|---:|
| 1000 | 1/0 | 1 | 10.199999809265137 |
| 1250 | 1/0 | 2 | 20.399999618530273 |
| 1500 | 1/0 | **4** | 40.79999923706055 |
| 2001 | 1/1 | 5 | 51 |
| 2126 | 0/1 | 6 | 61.20000076293945 |
| 2376 | 0/1 | 7 | 71.4000015258789 |
| 2626 | 0/1 | 8 | 81.5999984741211 |

At1500 the native loop calls the accepted recorder twice for the weight2 record; it is not one weighted gain supplied by Python. Native N8 and result: PURE8/shining8, LOST0, score10,000,008, H81/category3. The group native active bytes are set through the ownership/activation sequence. Full group scheduling for every branching connection and mixed ordinary/trace child case remains outside this representative chain.

### 17. Flicks: concrete construction blocker and isolated native predicate

Original parser/data RTTI **FlickNote** has vtable `0x1b653c0`. Prepared parsed Timing+FlickNote through **the entire `0x1862a14`** returns an empty runtime main vector and one timing list. Adding FlickNote to prepared timing+four taps or timing+hold leaves exactly four LogicTapNotes / one LogicHoldNote; no flick is created. Inspection of that builder's type dispatch corroborates this missing branch. This is the prepared parsed-data boundary, not an executed AFF lexer test.

Original **LogicFlickNote** typeinfo `0x1a89ca0` and native processing branch exist. In the inspected `.rela.dyn` relationships, the only relative reference to this typeinfo is GOT0x1b964d0, not an identified concrete vtable. **No claim that flicks are impossible in every mode is made**: an alternative construction path remains unknown. The descriptor-only producer test proves the index does not require a special flick predicate; it does not close runtime construction.

Native **`0x16e0548`** executes with a synthetic state record: +74/+78 expected direction, +8c bound contact ID initially−1, +90/+94 stored origin. First call binds ID7 and origin(0,0); later calls with ID8 reject. Original displacement/dot/norm/angle instructions run; imported acosf is supplied by host libm with f32 boundaries.

| Displacement (direction +X) | Native accepted predicate |
|---|---:|
| (105.999,0) | false |
| (106,0) | false |
| (106.001,0) | true |
| (0,200), (−200,0) | false |
| (200,199.99) | true |
| (200,200), (200,200.01) | false |

The predicate requires distance>106 and angle<45 degrees. It uses displacement from the bound origin, **not velocity**. Its time argument is not a denominator. Continuous caller `0x1485ddc..0x1485de8` separately requires **E>start−200** and spatial eligibility; expiry uses end+200 in the existing native pass. Those timing/consumption transitions are **Instruction-backed**, not new integrated gesture/gauge tests. Early/late multi-frame movement, cancellation/rebinding, candidate competition and native flick score/gauge reachability remain unexecuted. A synthetic vtable was not used to disguise this gap.

## Pseudocode

These reference names are proposed interfaces, not recovered source symbols. Arithmetic below preserves relevant f32 and signed comparisons; machine code remains the executed authority.

```text
build_native_spatial_index(model):                 # initializer block, ordinary initial path
    for groupTimingList in model.chart.timingLists:
        header = native_new_map_header(24)
        header.root = null
        header.leftmost = address(header.root)
        header.size = 0
        native_vector_append(model.indexHeaders, header)
    for object in model.chart.mainObjects:
        native_insert_0x1576aa4(model, object)

insert_object(model, object):
    t0, t1 = signed_minmax(object.start, object.end)
    if native_config_mode()==4 and object is LogicSceneControl:
        t1 = 180000
        group.end = max_i32(group.end,180000)
    k0 = fcvtzs_i32(f32(native_D(t0,group)/f32(-10000)))
    k1 = fcvtzs_i32(f32(native_D(t1,group)/f32(-10000)))
    for k in inclusive_signed_range(min(k0,k1),max(k0,k1)):
        bucket = native_map_find_or_insert(model.indexHeaders[group],k)
        native_append_retain(bucket.objects,object)  # no duplicate test here

update_active_ranges(model,E):                     # explanatory subset of0x10fd1c0
    update_group_active_flags_and_current_timing_fields()
    compute A[group]=-native_D(E,group), B[group]=-native_D(E+120,group)
    for object in model.retainedActive:
        if not group.active: native_remove_release(object); continue
        object.native_depth_update(E,A[group])      # also resets contact latches for long notes
        terminal = object.native_v28() or model.finished
        apply_native_arc_child_terminal_adjustment()
        if terminal and E>object.end: native_remove_release(object)
    for active group:
        lo=min(trunc_f32((A-back)/10000),trunc_f32((B-back)/10000))
        hi=max(trunc_f32((A+lookahead)/10000),trunc_f32((B-back)/10000))
        for key in [lo..hi]:
            for object in native_map_find_or_insert_empty(key):
                if pointer_already_active(object): continue
                object.native_depth_update(E,A)
                limit=700 if exact_LogicArcNote else 300  # ordinary configuration
                apply_native_special_bar_arc_and_mode4_branches()
                if native_admission_predicates_pass: native_append_retain(active,object)
    # No sweep of every unvisited historical bucket is inserted by this reference.

advance_gameplay_frame(model,scene):
    native_timeline_update()
    native_shared_transition_and_contact_record_maintenance()
    native_update_active_ranges()
    native_arc_geometry_cache_color_and_overlap_state()
    if not model.paused:
        if not model.finished: native_continuous_contacts()
        native_expiry_checkpoints_and_chart_events()
    native_score_and_gauge_frame_update()
    native_completion_then_health_failure_checks()   # preserve native order

visit_GameScene(scene,...):                        #0x18be2f8, relevant path
    if not native_visible(scene): return
    if Director.frameCounter != scene.lastVisitedFrame:
        native_advance_gameplay_frame(scene.model,scene)
        native_HUD_and_render_state_updates()
        native_base_scene_visit(...)
        native_remaining_visit_work()
        scene.lastVisitedFrame=Director.frameCounter
    else:
        native_base_scene_visit(...)

dispatch_touch_begin(model,touch):
    native_0xeec024(model,touch,explicitLane=0)      # gates, fresh E, projection, sort/judge
    # Does not first perform a full range/geometry/expiry frame.

dispatch_touch_end_or_cancel(model,touchVector):
    native_0xf9a50c(model,touchVector)               # vector, not a Touch pointer
    # Native ordinary end/cancel wrappers share this boundary; transport remains outside.

continuous_arc_contact(model,arc,touch):
    # Actual continuous routine also builds/intersects/project-clamps contact records.
    if native_0xc98490(model,projectedContact,arc,initial=false):
        native_0x15dfe2c(arc,touch,E)
        # Original LogicColor arbitration or geometry-produced bypass, no supplied active flag.
    native_later_checkpoint_pass()                 # once per frame, not once per contact

finalize_result(score):
    native_0x1600bb0(score,fixtureCharacterFlag)
    result=score.cachedResult_68                   # observe storage; do not rely on X0
    return native_result_queries(result)
```

### Reference interfaces and coverage contracts

| Interface | Native addresses | Inputs / outputs / clocks / lifetime |009 coverage and remaining boundary|
|---|---|---|---|
| initialize_chart |1862a14; be2b98;1902ffc;1446490;178f7fc;173c1dc..173c250;11ea120 | prepared parsed objects or native constructor inputs → chart objects/timing/end/count; depths use chart time | Native-integrated scoped builder/constructors; no new lexer/header/metadata run |
| build_native_spatial_index |fc0184..fc02a4;1576aa4;1257490;1082558 | chart main vector/group timings → native map vectors; retains bucket members | Native-integrated, no manual keys/nodes; complete reclamation unknown |
| initialize_active_note_ranges |fbfd74..fbfdc4;10fd1c0 | empty retained vector → native admissions; E/depth-dependent | Native-integrated admission; full initializer/account boundary supplied |
| advance_gameplay_frame |10a7550 | model/scene/timeline → ranges, contacts, judgments/gauges, finished | Native-integrated ordinary replay; delegate UI/end notification supplied |
| dispatch_touch_begin |eec024 | prepared Touch/design/contact ID → candidate/judgment, fresh E | Native-integrated projected100 taps; JNI/listener creation not joined |
| dispatch_touch_move |160b83c..160b87c transport evidence;14858d4 | current Touch coordinates → projected per-frame records | Coordinate mutation driver supplied in009; whole move transport Instruction-backed |
| dispatch_touch_end/cancel |d88408;18ba6d8;f9a50c;13db7a0 | Touch-pointer vector, current E → retention/owner release | Native-integrated cleanup; cancel wrapper/Android transport Instruction-backed |
| update_arc_contact_ownership |19f3d4c;c98490;927384;15dfe2c;15a90c4 | factory-built arc/color, native geometry, projected contacts → owner/bypass/contact/group flags | Native-integrated ordinary, connected and static-overlap examples; full mode catalog unknown |
| evaluate_flick_gesture |16e0548;1485ddc..1485ee8 | bound origin/ID/direction + current point → native boolean; caller E gate | Native-isolated predicate; original construction and end-to-end gesture unknown |
| resolve_long_note_checkpoints |d92558;ba81e8;f8056c;c6e938 | native records/weights/contact/E → actual unit callbacks | Native-integrated holds/arcs/connected weight2; generation flag selection partly supplied |
| expire_inactive_notes |10fd1c0;f8056c;868e54 | retained active objects, E → terminal removal and eligible misses | Native-integrated; no invented global historical catch-up |
| update_score_and_gauge |1730290;868e54;16e4ab0;1869e90;133fac8;a126f4 | native N/counters/gauges → scores/f32 H | Native-integrated ordinary mode0; special modes retain006/008 scopes |
| check_completion_and_failure |10a7b38..10a8018 | chart end/E/mode/H/finished → delegate and finish flags | Ordinary completion executed; completion-before-failure instructions rechecked; no new full special-mode matrix |
| finalize_result |1600bb0;1315038;12a5574 | ScoreState → cached result/counter selection/floored H/class | Native-integrated driver snapshot; external scene/persistence omitted |
| update_camera_actions |13d3f44;d630b8;9effe0;c7820c;b3dc38;f1b510 | prepared Scheduler entry, native action/Node, supplied dt → Camera position | Native-integrated translation queue; full Director/GPU/OS scheduling not executed |

## Native validation

### 18. Execution environment, hooks, and reproducibility

Unicorn2.1.4, Capstone5.0.9, pyelftools0.33. Fresh loader maps ELF PT_LOADs and applies **R_AARCH64_RELATIVE** with load bias0. Main image memory0..0x2100000; synthetic arena0x4000000..0x6000000; stack/TLS0x6000000..0x6100000, SP0x60df000, TPIDR_EL0=0x60f0000; return sentinel0x4000100. Bump heap starts0x4100000, 64-byte alignment, allocations zeroed. Integer/float arguments use X/W/S registers; aggregate returns use X8; arc factory additional arguments use original entry SP slots. Synthetic arena addresses do not replace code addresses.

RTTI uses original relocated typeinfo/vtable/name associations. Hooked dynamic_cast resolves the tested single-inheritance chains only; no multiple-inheritance/general ABI guarantee. Ordinary taps use vtable1af4278, holds1b2eda8, arcs1b91500, children1acac18, Camera1adf2d0. Prepared parsed types use original data vtables; parsed integer position uses1a95808, raw integer+8. Native compiler/factory paths produce real runtime vtable/field writes. Ref base initialization/lifetime remains supplied.

| Hook/boundary | Exact supplied behavior / scope |
|---|---|
| new/new[]/nothrow new0x1a6d9c0/1a6dd40/1a6e090; malloc1a6df10; calloc1a6ee10 | zeroed aligned bump allocation; no allocation failures |
| memcpy/memmove1a6d9d0/1a6daf0; memset1a6db30; strlen1a6dad0 | host memory primitives; native container growth/trees/loops remain original |
| string copy/assignment1a6da50/1a6db80 | fixture libc++ string copying; successful current fixtures use empty/short strings; no general long-string ownership claim |
| dynamic_cast1a6db90 | original RTTI single-inheritance identity walk; unknown layouts not generalized |
| Ref constructor121a0ec; retain147fe48; release d6dc98; autorelease10ac6e8; delete1a6d9e0/array-delete1a6e0a0; value destructor19f2e40 | no-op lifetime services; observed calls still identify retention/removal, real reclamation unverified |
| steady-clock1a6dc60 | controlled nanoseconds=`nowMs*1000000`; native1271200 and timeline math execute |
| system-clock1a6dbe0; time1a6de50 | deterministic fixture epoch/date |
| audio107af5c; pause18c9ba4; seek fbf24c | suppress external audio effects; pause/seek boundaries used only in relevant tests |
| Director a4227c; frame-size f09110 | prepared Director/design1280×720 and aggregate frame-size1280×720; no real window |
| optional result helper e2388c | null; snapshot flag1 selects fixture character72, avoiding account retrieval |
| Model delegate vtable slots | no-op/log notifications, including finish; actual judges/recorders/gauges are not stubbed; result requested separately |
| Arc feedback shell | original155241c at render virtual+530, actual latch write; GPU/segments/particles not executed |
| acosf1a6e160 | host acos, f32 register boundary; zero-displacement NaN preserved; Android libm bit identity unclaimed |
| GameScene visit scoped skip |18be380→18be470, skipping HUD/base-draw subtree; original counter store executes; same-counter base draw suppressed |
| Scheduler entry | prepared linked update entry calls original d630b8/9effe0; original runAction/add/step mutate actual queue/Node |

Observational hooks at native entries record ordering without replacing instructions. Score/gauge/count/index/ownership/contact/checkpoint arithmetic is not replaced by host formulas. Main initializer block calls, explicit native constructor/postprocessing calls, whole frame calls, begin/end calls, and result queries are distinguished above. The driver writes pre-depth outputs from **native integrator returns** in constructor-only fixtures; the full original preprocessing loop is not claimed executed in every009 fixture.

A native ArcTap identity in a mixed-layout index test or a flick-shaped descriptor does not prove its complete factory/transport lifecycle. Likewise supplied chart-end, no-ability/mode0 configuration and imported clocks are real synthetic boundaries. An early exploratory fixture accidentally overwrote the native hold end2500 with a tap-style2120; it was corrected before final validation. Successful hold results preserve original builder end2500. That failure was a harness precondition error, not an engine discovery.

### 19. Updated integration coverage matrix

Statuses concern specific scopes; they are not blanket subsystem completion labels.

| Area | Classification | Current evidence / limit |
|---|---|---|
| Native spatial-index allocation/insertion/tree/vector | **Native-integrated** | Original initializer block/producer feeds original range/frame/input; all buckets native |
| Multi-group/signed/reverse/speed boundary key generation | **Native-integrated, producer scope** | Exact native index outputs; unusual groups not all played through results |
| Index complete ownership/reclamation | **Instruction-backed / Unknown** | retain sites and normal destructor pointer-buffer free confirmed; pointed-map reclamation unknown |
| Active admission/retention/expiry | **Native-integrated** | short/long jumps, exact thresholds, never-admitted versus retained notes, no automatic catch-up in tested path |
| AFF lexer/body parsing | **Prior Native-integrated in008** |009 starts at prepared parsed objects or native factories; no new parser claim |
| Runtime taps/holds from prepared parsed data | **Native-integrated** | original1862a14 and native count/end/position factories; metadata/header supplied |
| Projected tap → result | **Native-integrated, scoped** | native-index100-note replay; final snapshot driver-invoked, scene delegate supplied |
| Hold latch/contact/checkpoints/result | **Native-integrated** | native-builder hold, native index/begin/continuous/end/miss/score/gauge/snapshot |
| Ordinary arc ownership/checkpoints/result | **Native-integrated, scoped** | original factory/color/geometry/cache/projection/ownership/recorders; retained Touch vector and render shell supplied |
| Connected ordinary arc/weight2 | **Native-integrated, scoped** | native link/group producer, native activation and two callback units; generation flag1 supplied |
| Arc static overlap exception | **Native-integrated** | native cache produces bypass for tested <200 geometry; moving crossing and exact200 unknown |
| Arc-tap full child-factory lifecycle | **Prior scoped Native-integrated / current producer scope** |008 prepared child judge retained;009 mixed index identity test; full child production not closed |
| Flick predicate | **Native-isolated** | native distance/angle/ID boundary cases; no velocity substitution |
| Flick construction/input/score lifecycle | **Unknown; Instruction-backed fragments** | tested builder drops parsed FlickNote; alternate constructor/actual playable mode unknown |
| Outer Director/Scheduler/visit order | **Instruction-backed plus scoped Native-integrated** | concrete native chain/counter guard; visit-prefix and Scheduler/action tests; full Director loop not executed |
| Camera action queue/translation | **Native-integrated** | original runAction/add/Scheduler/ActionManager/MoveBy; representative action only |
| Android/JNI/Cocos transport | **Instruction-backed** | current smali/native dispatch inspection; no real threads/queues |
| Multiple begin callbacks/stale geometry | **Native-integrated controlled schedules** | two native begins with fresh E and unchanged range/depths |
| Pause/resume | **Native-integrated, scoped** | native wrapper/timeline freeze/gate/retained state; audio/foreground/seek integration incomplete |
| Score/gauge/result | **Native-integrated ordinary mode0** | native count/factories/guards/recorders/math/snapshot/query; earlier006/008 special-mode evidence not broadened |
| Result flags d1/d2/b1 reachable producers | **Unknown, prior effects retained** | optional work package not expanded; no synthetic flag supplied as proof of reachability |
| GPU/audio hardware/persistence/full Android lifecycle | **Unknown / unexecuted here** | no device, sound output, rendered gameplay, database or network effects |

## Discrepancies and proposed corrections

### 20. Hold lookahead: proposed historical wording, not applied

Rechecked continuous hold instructions **`0x1485d50..0x1485db0`** and both timeline branches. Lane matching precedes **start<E<end** and the +a8 initial latch. Model+148==1 adds an input-record/lane gate; it does not turn this hold timing comparison into120 ms. Initial begin eligibility separately uses strict **start<E+100 and E<end**. The120 ms branch belongs to arc initial eligibility and to range-query lookahead elsewhere. No alternate120 ms continuous-hold activation branch was recovered here; that is not proof about all other modes/callers.

Proposed replacement for the unqualified002 sentence:

> In the recovered continuous hold branch, a matching contact activates an already initially latched hold only while startTime < effectiveTime < endTime. Initial latch collection has a separate strict100 ms start lookahead. Arc initial eligibility and index query lookahead use separate120 ms comparisons.

**No change is made to002 or historical context.** Existing authorized curve/spatial corrections remain preserved.

### 21. Other distinctions discovered while reproducing interfaces

- **Snapshot ABI:** `0x1600bb0` reliably stores/uses ScoreState+68. Its inspected cached-result branch and epilogue do not establish a consistent X0 return-pointer contract. An exploratory wrapper relying on X0 obtained0 despite a valid cached result. The009 interface calls finalization, then reads+68; proposed clarification to008's “returns cached pointer” phrasing is recorded here without editing it.
- **End cleanup argument:** `0xf9a50c` reads begin/end from its second argument and iterates Touch pointers. It must receive a vector/header, not a Touch pointer as a literal reading of the008 shorthand interface might imply. Current native execution uses the vector.
- **Synthetic versus native bucket difference:**008's tap bucket assignments match the tested ordinary tap keys, explaining why its jump discrepancy survives. Long objects occupy endpoint-key ranges, not just a start bucket. Preserve008's result as conditional historical evidence;009 supplies the missing producer validation.
- **Frame entry is visit-driven:** knowing model-internal order was insufficient to identify outer scheduling. The new GameScene visit/counter evidence is stronger than saying gameplay is simply a scheduled update callback.
- **Ownership versus spatial activity:** leaving a hit region need not lift ownership; geometry overlap can produce a native bypass. These prevent a reference implementation from treating every inactive frame as a touch-end event.
- **Completion/failure:** original frame still checks completion before the later health-failure branch. Optional result flag reachability was not solved; no new ordinary-production hard-zero claim is made.

## Unresolved Mysteries

1. Full reclamation/ownership of dynamically allocated map headers/nodes and bucket-retained notes, including restart/scene replacement; normal destructor evidence is bounded.
2. Every indirect index writer, every extended-camera/mode query branch, and broad malformed/out-of-range float/int conversion behavior. No overflow/NaN key-span loop was fabricated or executed as a valid chart.
3. Production creation of LogicFlickNote, its actual vtable/mode, timing/movement cancellation/rebinding, candidate consumption, and complete flick-to-gauge replay. Parsed FlickNote's tested builder omission is preserved as evidence.
4. Full AFF file/lexer/header/account initialization in this new harness;009's native builder begins with prepared parsed data. Full native arc-tap child creation and mixed child/group ownership integration remain open.
5. Real Java/GL queue arbitration, OS scheduling and clock epochs, actual foreground/background/seek reset behavior, every camera reset/action cancellation, and full Director/GPU render execution.
6. Every arc branching/group geometry case, moving crossings, exact200 overlap boundary, and all reactivation-related special state/modes beyond the executed release gate and connected examples.
7. Reachable writers of ScoreState+d1/+d2, GameResult+b1 and special scene/input flags; optional work package6 was not expanded. Their previously measured effects do not prove ordinary reachability.
8. Actual audio/provider/hardware coupling, screen latency, persistent results and network submission. No device bug/exploit frequency or complete-engine equivalence is claimed.

These are limits of009, not authorization or a launch plan for Expedition010.

## GitHub Status

Authorized publication: this new file and an **append-only** Expedition009 entry in `context.md`, existing `main`, based on `d1e211494375fe17d9d4e27fc4f4c096ba2a6c92`. No harness, trace JSON, extra artifact, earlier report, README, instructions, binary, or archived asset belongs to the commit. Publication SHA, pinned read-back equality, full historical blob preservation and final initial-to-final comparison are reported after committing; a self-referential future SHA is not invented in this file.
