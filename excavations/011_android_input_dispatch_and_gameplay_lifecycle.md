# Expedition 011 — Android Input Dispatch, Frame Scheduling & Gameplay Lifecycle

Date: 2026-10-24. Project Arconist; repository `thgillwtnorizoh/arconist`, branch `main`.

## Result

**Strong success in a bounded native environment.** Original JNI begin/move/end/cancel exports now execute with original GLView pointer mapping, native Touch allocation/update, original EventDispatcher, native gameplay-listener construction/registration, and actual gameplay callbacks. A dispatched begin reaches projection, native tap judgment, recorder and gauge. Hold and ordinary arc contacts are acquired through that delivery chain and removed through original UP and CANCEL dispatch. No activation/owner flags or retained Touch vectors are supplied to those successful delivery tests.

Original Director scheduling is additionally joined to the dispatched-input fixtures through a scoped Director frame path: native before-update event, Scheduler, registered ActionManager callback, native after-update event, original GameScene visit guard and model frame. Renderer/matrix-stack preparation and HUD/base drawing are explicit excluded blocks. The test is not a complete rendered Director frame.

**Java transport is reconstructed from the supplied smali, not executed in Android.** The inherited platform `android.opengl.GLSurfaceView.queueEvent`/GLThread implementation is absent from this archive. No real Java queue, MotionEvent object, GL thread or physical latency distribution is claimed. Controlled calls around native frames establish the consequences of delivery order, not the operating system's selection of that order.

The important scheduling clarification is that Director's two recovered event-dispatch points are **`director_before_update` and `director_after_update` custom notifications**, not Android touch-queue drains. Original native touch delivery is synchronous once JNI is entered.

## What I Found

### Preparation and identity

Read the supplied project instructions, latest cumulative context, the complete010 report, and relevant004/005/008/009 transport, clock, dispatch, continuous-contact and scheduling sections. Inspected the archive's native image and original Cocos smali. Starting main is the expected **`8bc7dd7420efc28ed8b68f6131f2f4bc255d0fbf`**, tree `497c3a3aa8e23404e1a6be231376b6876b148a26`; no011 publication existed at the initial check.

Main executable `lib/arm64-v8a/libcocos2dcpp.so` has verified SHA-256 **`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`**, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. All native addresses/offsets below are hexadecimal **main-library ELF virtual addresses before relocation**, unless explicitly called synthetic arena addresses. Time/coordinates and test IDs are decimal. Researcher function names are descriptive labels except where original RTTI identifies the class.

The supplied archive SHA-256 remains `5dc2f3d1f5387d0c5da06ad72694105cdd7fa4b7ff80f981f77998e89eb2b4cb`; instruction text remains `8a9bea2e002d6ce282dc7b92592379927088a2ecbab2e451b585aea4c921f1e8`. Neither source is edited.

Prior scratch files actually remained available and were inspected. The010 runtime-service loader and009 minimal gameplay fixtures were reused; a new011 JNI/dispatch fixture and observers were written. There is no claim of recovering inaccessible Java/emulator state or missing scripts. No old report is treated as a newly executed011 test.

Evidence labels: **Native-integrated** = original routines execute together on the stated path; **Native-isolated** = original routine executes with surrounding interfaces supplied; **Instruction-backed** = decoded native/smali path without complete execution; **Interpretation** = explanation grounded in that evidence; **Unknown** = unverified interface or reachability.

## Java/JNI/GLView dispatch chain

### 1. Captured Java data and Runnable actions — Instruction-backed

Source: `smali_classes3/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali`, `onTouchEvent`, source-line annotations214–310; nested classes `$5`–`$10`; `Cocos2dxRenderer.smali` wrappers. The view extends platform `android.opengl.GLSurfaceView` and does not implement a local replacement of its event queue.

Before selecting an action, `onTouchEvent` captures one timestamp through `getTouchTimestampNow`: `TimeUnit.MILLISECONDS.convert(SystemClock.elapsedRealtimeNanos(), NANOSECONDS)`. It creates arrays containing every current pointer's ID, X, Y and **f32(size × pressure)**. It reads `getAction() & 0xff`; pointer-down/up select the index using `getAction() >> 8`. Ordinary down/up select pointer index0. A shown soft keyboard is hidden and focus requested before queuing; that branch is not an input-rejection branch.

| Android action | Queued class | Stored payload | Runnable → renderer |
|---|---|---|---|
| DOWN, 0 | `$6` | view reference, pointer0 ID/X/Y/product, captured long timestamp | `handleActionDown(IFFFJ)` |
| POINTER_DOWN, 5 | `$5` | selected ID/X/Y/product, same captured timestamp | same down wrapper |
| MOVE, 2 | `$7` | ID/X/Y/product arrays and captured timestamp | `handleActionMove([I[F[F[FJ)` |
| UP, 1 | `$9` | pointer0 scalar data and timestamp | `handleActionUp(IFFFJ)` |
| POINTER_UP, 6 | `$8` | selected scalar data and timestamp | same up wrapper |
| CANCEL, 3 | `$10` | all current arrays and timestamp | `handleActionCancel([I[F[F[FJ)` |

Each constructor stores the payload in its `val$...` fields; `run()` retrieves those fields and invokes the renderer directly. The arrays are allocated by this event invocation, rather than later rereading MotionEvent from the GL thread. Unrecognized actions queue nothing in this method and still return true. No `getEventTime()` or historical-sample iteration appears in this method. These are smali findings, not executed Java runtime behavior.

Renderer wrappers immediately invoke the corresponding native methods; no extra renderer-side input queue is present. `onDrawFrame` calls `nativeRender` directly. Its alternate frame-pacing branch uses `System.nanoTime`, an optional `Thread.sleep`, then `nativeRender`; it does not call the touch Runnables from inside native rendering.

### 2. Original JNI entries — Native-integrated

| Export operation | Entry | GLView virtual slot → original target |
|---|---|---|
| nativeTouchesBegin `(IFFFJ)V` | `0xbe31a8` | +e0 → `0x97d784` |
| nativeTouchesMove `([I[F[F[FJ)V` | `0x1706960` | +e8 → `0x160b710` |
| nativeTouchesEnd `(IFFFJ)V` | `0xdda71c` | +f0 → `0x15af680` |
| nativeTouchesCancel `([I[F[F[FJ)V` | `0xd8dc50` | +f8 → `0x1556de4` |

The exact original entries execute. Scalar JNI uses **SXTW** to widen the Java ID, packs X/Y/product and an additional float1.0 on its stack, obtains Director via `0xa4227c`, checks Director+f0 for a GLView, and invokes its real virtual. The fixture uses original GLViewImpl vtable `0x1b20d60`; its four touch targets match the GLView vtable `0x1ab6108`.

Array JNI executes its own length/region calls, stack buffers, float1.0-array filling, signed ID widening, Director lookup and virtual dispatch. Its synthetic JNIEnv implements only virtual+558 GetArrayLength, +658 GetIntArrayRegion and +668 GetFloatArrayRegion; the input arrays are supplied data. The native SIMD paths for larger arrays execute in the 16-element cancel test. This begins at JNI, not after it, but does not execute Java array objects or a VM. Mismatched lengths, exceptions, nonfinite coordinates and unbounded counts are not validated.

### 3. Original event-dispatch and listener chain — Native-integrated

Successful begin path:

```text
be31a8 → Director.GLView.virtual+e0 → 97d784
  → ef7d24 EventTouch construction
  → native pointer map / first-free engine slot / allocate Touch
  → 1980970 EventDispatcher::dispatchEvent                 callsite97dc40
  → 18feb24 touch-event dispatch
  → 8865a0 listener iteration → c2bf98 all-at-once callback
  → 194ff80 gameplay begin function object
  → eec024 initial input → original projection/candidate/judge/recorder/gauge
```

Original dispatcher constructor `0xf9f040` initializes the fixture dispatcher. **Original `0x130bdf0`** constructs the listener with factory `0xb981cc`, binds all four real function objects, and registers it through **`0x1942fc8` with fixed priority20**, at callsite `0x130bf58`. No replacement dispatcher calls the gameplay callback on the driver's behalf.

| Listener state | Native field / function |
|---|---|
| model listener | model+150 |
| type | EventListenerTouchAllAtOnce, vtable `0x1b8be30` |
| begin / move / end / cancel function storage | listener+80 / +b0 / +e0 / +110 |
| call operators | `194ff80` / `10e7008` / `d88408` / `18ba6d8` |
| function-object vtables | `1b929c0` / `1abb400` / `1ad9e18` / `1b50a78` |
| registered / fixed priority / associated node | listener+60 / +64 / +68 |
| paused / enabled | listener+70 / +71 |
| dispatcher enabled / dispatch nesting | dispatcher+124 / +120 |
| EventTouch base type / action / pointer vector | event+c =0; event+20 =0/1/2/3; event+28/+30/+38 |

Dispatcher+124 is enabled by the fixture; Director+140 running-scene pointer is null for fixed-priority listener dispatch. Other scene-priority listeners and swallowing/stop-propagation interactions are not established by these tests. Native checks at `1980990..94`, `88661c..658`, and `c2bfb8..bc` remain in execution.

## Touch object and contact-ID lifecycle

### 4. Three distinct identities and native fields

| Identity or field | Producer / storage / tested meaning |
|---|---|
| Android pointer ID | supplied JNI Java-ID argument; signed64 map key at node+20 |
| engine slot | lowest free bit0..14 in global `1bfebd4`; map node+28; Touch+c |
| slot → Touch | pointer array `1beef90 + slot*8` |
| Android ID map | native ordered tree; leftmost `1bf1a88`, root `1bf1a90`, count `1bf1a98` |
| Touch allocation/vtable | 0x48-byte original allocation at `97da20`; original vtable `1ad7fd8` |
| initial-position latch | Touch+10 |
| initial / current / previous X,Y | +14/+18; +1c/+20; +24/+28 |
| size×pressure / extra force | +2c / +30; JNI extra force1.0 |
| generated gameplay ID | Touch+34; begin copies global `1bf25f4`, then increments it at `195007c..9c` |
| frame time captured by begin | Touch+3c; copied from last-model-frame global `1bf93e8` |
| Android timestamp stored on begin | Touch+40, 64-bit |
| retained gameplay contacts | model+d0/+d8/+e0 Touch-pointer vector, produced by native begin |

GLView performs `(inputXY − view[1c,20]) / view[48,4c]` with native vector FSUB/FDIV before storing converted coordinates. The main tests supply viewport origin0 and scale1; a general viewport matrix is not inferred from that fixture. Original gameplay getter `13e0324` reads current converted coordinates. No engine slot or Android ID is substituted for the generated contact ID.

Begin ignores an already mapped ID before allocating/updating a Touch. MOVE and terminal events look up the existing mapping; an unmapped ID is omitted. A released Android ID can be reused with the same engine slot but a new Touch allocation and a new gameplay ID. The allocator does not reclaim addresses in this harness, so allocation-address reuse itself is not tested.

### 5. Boundary trace: allocation, move, duplication, reuse and capacity

Fixture: two native taps at1000/raw1 and1150/raw2; original timing tempo120/speed6, native index, mode0/no ability, synthetic scene/timeline/camera. Director counter0; no Scheduler update during this boundary trace. Controlled wall times900..909; initial last-frame global0. Timestamp=700000+event index; size×pressure values listed below. Native begin refreshes timeline; MOVE/UP/CANCEL do not independently refresh it in these paths.

| Event | Resulting native state |
|---|---|
| DOWN42 at(290,360), product.5 | mask1; Android42→slot0→Touch `0x4106640`; gameplay1000; initial/current/previous(290,360); timestamp700000; retained1 |
| MOVE42 to(300,350), product.75 | same Touch/contact; current(300,350), previous(290,360), initial unchanged; timestamp still700000 |
| duplicate DOWN42 at(999,888) | complete captured mapping/Touch/retained/counter state unchanged |
| MOVE99; UP99 | unmapped; same complete state; no terminal dispatch for99 |
| UP42 at(310,340), product.9 | original final-coordinate update, then mask0/map empty/retained empty; next gameplay counter1001 |
| reuse DOWN42 at(320,330), product.4 | slot0, new Touch `0x4107140`, gameplay1001, timestamp700006 |
| POINTER_DOWN-equivalent scalar77 at(640,360), product.6 | slot1, Touch `0x41073c0`, gameplay1002; mask3; both retained |
| POINTER_UP-equivalent UP42 | mask2; Android77/slot1/contact1002 remains retained |
| CANCEL77 | mask0/map empty/retained empty |

The native entries for Android POINTER_DOWN/UP are the same scalar entries as down/up; the Java action-index selection above is reconstructed, not exercised as MotionEvent code.

Capacity continuation uses IDs100..115: the first15 occupy slots0..14 and mask32767; ID115 is not mapped and no sixteenth gameplay ID is assigned. A 16-element JNI CANCEL removes the15 mapped contacts and ignores unmapped115; map/mask/retained vector become empty, next gameplay counter1018. Native tree insertion/balancing/removal and slot clearing execute; membership is not manufactured by the harness.

Separate two-contact array test: DOWN42 timestamp111 and DOWN77 timestamp222, both at wall1000 after a model frame. MOVE arrays ordered[77,42] update slot1 to(550,350)/product.7 and slot0 to(300,340)/product.8; timestamps remain222/111. CANCEL arrays[77,42] deliver a native event vector in **slot order[1,0]**, final coordinates(551,351)/(301,341), products.1/.2, timestamps222/111. The mask is already0 at EventDispatcher entry. Mapping order in the tree does not reorder this event vector. Both gameplay contacts are removed.

## Frame/event scheduling evidence

### 6. Queue boundaries and the two Director events

**Instruction-backed Java:** UI-side event capture precedes inherited `queueEvent`. Runnable execution calls renderer→JNI synchronously. The archive has no platform GLThread/mEventQueue consumer implementation, so this expedition cannot establish its exact event-versus-draw loop, batching policy or pause-time draining from the bundled files. A Runnable delivered on the GL thread and `onDrawFrame` are distinct work items; no nested Java Runnable pump is found in the native render path. A controlled driver invocation is not evidence that a queued UI touch can preempt a running nativeRender call.

**Native-integrated/Instruction-backed native:** JNI render `e181d0` calls Director virtual+38, normally `17371d8`, which gates purge/restart/stopped state and calls `1793f8c`. Its ordinary scheduling prefix is:

| Callsite | Original operation |
|---|---|
| `1793fd4` | GLView virtual+40; both recovered vtables resolve to **`88bb84: RET`** |
| `1793fe8` | EventDispatcher dispatch of Director+d0, named **director_before_update** |
| `1793ff4` | Scheduler `13d3f44` |
| `1794000` | EventDispatcher dispatch of Director+d8, named **director_after_update** |
| `17940f4` | scene virtual+338 → GameScene visit `18be2f8` in fixture |
| `18be37c` | model frame `10a7550` if Director+134 differs from scene+4d0 |
| `1794198` | increment Director frame counter later in the full frame; instruction-backed here |

The names are read through the actual relocated Director-init references at `18b3eb8`/`18b3f64`; original EventCustom constructor `ffa914` creates both fixture events. **These calls are custom notifications, not two input-queue consumers.** Suggested clarification to historical shorthand: “dispatch before-update notification → Scheduler → dispatch after-update notification → scene traversal.” Earlier reports/context are preserved.

Scheduler additionally has a distinct native deferred-function vector at+48/+50/+58: `13d3fdc..13d4210` locks, copies/clears it, unlocks, and invokes original function objects at `13d422c`. Its mutex imports are `1a6e000/1a6e010`. This deferred queue's nonempty path is decoded, not executed here, and is **not identified with Android GLSurfaceView.queueEvent**. JNI touch delivery in the successful tests neither enqueues into it nor waits for Scheduler.

### 7. Executed joined Director scope and test preconditions

Each A–C schedule begins with original model frame1000 to populate active notes and cached depths[0,−1800]. Prepared Director counter5; camera X0; design1280×720; ordinary mode0/no ability; Native timing anchor−3000, steady/music-started flags1. Android timestamps in this matrix are supplied as880000+wallTime and never substituted into the clock.

Director scope starts at original entry `1793f8c`, executes time calculation, original no-op poll, both native notification dispatches, native Scheduler and original ActionManager through an **originally registered** callback, then scene virtual dispatch and original once-per-counter model frame. Scheduler constructor `da7a90` and registration `db9674` execute, using the original wrapper vtable `1b37d48` and call operator `d630b8 → 9effe0`, priority INT_MIN.

Explicit exclusions: at `1794004` the driver skips renderer/matrix-stack preparation to `17940d0`; it stops at `17940f8`, before later render/counter-increment work. At `18be380`, it skips HUD/base-drawing work to `18be470`, preserving the native scene-counter store. Base drawing `129c924` is a no-op boundary for repeat visits. Thus counter5 is intentionally held by the fixture, not claimed as a full Director-generated consecutive-frame sequence.

| Scenario / step | Wall / GameTimeline E / last model frame | Cached depths | Native outcome |
|---|---|---|---|
| A: JNI DOWN42 |1020 /1020 /1000|[0,−1800]|PURE1, H40.20000076293945; Touch+3c1000 |
| A: JNI DOWN77 |1150 /1150 /1000|[0,−1800]|PURE2, H80.4000015258789; Touch+3c1000 |
| A: Director notifications→Scheduler/ActionManager→visit |1150 /1150 /1150|[1800,0]|scene stamp becomes5; PURE2 unchanged |
| B: Director scope before input |1020 /1020 /1020|[240,−1560]|PURE0, scene stamp5 |
| B: JNI DOWN42 |1026 /1026 /1020|[240,−1560]|PURE1, H40.20000076293945; Touch+3c1020 |
| B: repeat visit at counter5 |1026 /1026 /1020|[240,−1560]|native guard skips model frame |
| C: JNI DOWN42 |1000 /1000 /1000|[0,−1800]|PURE1, H40.20000076293945 |
| C: MOVE42, MOVE42, UP42 |walls1005/1010/1015; E remains1000|[0,−1800]|no new judgment; final(320,330), contact removed before visit |
| C: Director scope/visit |1015 /1015 /1015|[180,−1620]|PURE1 unchanged; retained vector empty |

Event C starts(290,360), then moves(300,350), then(310,340), then ends(320,330), products.5/.6/.7/.8. All use Android42→slot0→gameplay1000. A's second input is Android77→slot1→1001 at(540,360). All JNI calls are external to the native Director invocation; they are controlled schedules. They demonstrate that multiple fully dispatched callbacks can occur before a model frame, and that a later callback can refresh effective time without updating cached note geometry. They do not measure hardware event frequency or prove which Android queue iteration selects A/B/C.

### 8. Camera actions and scenario D

Controlled D runs original Scheduler/ActionManager on a Camera Node MoveBy of+600X over2s, then JNI down, then GameScene visit. Native first tick0 and next0.5s update produce X0 and X150. Node runAction `c7820c → b3dc38`, MoveBy factory `f1b510`, Scheduler and ActionManager execute. No camera position150 is assigned by the driver.

At wall/E1000, Director counter5, last frame1000, cached note depths[0,−1800], input Android42/slot0/generated1000 at(290,360), timestamp999999: original input projection rebuilds the camera's cached view-projection matrix at+368. With Camera X150 its X-translation component becomes **−0.1171875**; stationary control gives0. Projection diagonal is1/1280,1/720,1,1. Both this particular widened-lane fixture and its stationary control score one PURE/H40.20000076293945; the matrix difference demonstrates camera-action visibility, not an assertion that every150-unit move changes the selected lane.

**D is a synthetic interleaving proof.** No production UI-touch queue drain between Scheduler and scene visit has been recovered. A UI Runnable cannot be claimed to execute at that point merely because the driver can call JNI there. The supported production interpretation is that an input delivered after a completed native action update can observe the updated Camera through original lazy matrix computation; exact platform queue/draw ordering remains unknown.

## Release and cancellation behavior

### 9. Engine release precedes listener cleanup

Native end wrapper `15af680` selects action2, cancel `1556de4` selects action3; both tail-call **`95e32c`**. Their register rearrangement replaces the original timestamp argument with the extra-force array pointer; no terminal timestamp is stored to Touch+40 in this path. MOVE likewise preserves begin's timestamp.

Shared terminal code updates final coordinates/pressure and previous position, appends the actual Touch to its event vector, clears slot pointer/mask at `95e5c8..5ec`, removes the Android-ID map node through original tree removal `a993b8`, then dispatches at `95e6b0`. **At EventDispatcher entry the engine mappings are already gone.** After synchronous listener delivery it calls Ref release for each event Touch at `95e6c4`; real reclamation is outside the supplied reference-service environment.

Gameplay end/cancel operators `d88408`/`18ba6d8` copy the pointer vector and, if model+148 is0, call **`f9a50c` at d88494/18ba764**. Cleanup removes matching retained pointers and releases them, then iterates chart colors and calls **`13db7a0(color,generatedID,currentEffectiveTime)`**. It does not call the timeline updater. Release changes matching color owner+28 to−1, removes its claimed ID from global `1bfa3d8`, and conditionally records release time+2c. It is not a loop clearing every note's contact/latch bytes.

### 10. Hold trace — Native-integrated through JNI and cleanup

The small hold1000..2000/raw3 is created through010's original full AFF parser/factory/ordinary initializer, yielding N3/end2500 and records1250/1500/1750. This construction is reused solely as a fixture; metadata/digest/services retain010's stated synthetic boundaries. Native model/index and camera are prepared, and the retained Touch vector starts empty. Input(740,360) receives gameplay3000 through native begin; no hold latch/contact flag is assigned.

| Step | E | initial latch+a8 | contact bytes+64/+65 | judgment |
|---|---:|---:|---|---|
| DOWN at1000 |1000|1|0/0|none |
| frame1001 |1001|1|1/1|none |
| frame1125 |1125|1|1/1|PURE1 |
| UP delivered at wall1200, timestamp200 |**1125**|1|**1/1 remains immediately**|no additional judgment; retained vector becomes empty |
| next frame1201 |1201|1|0/0|PURE1/LOST0 |

Replacing UP with original JNI CANCEL yields the same observed gameplay state transitions through the separate action3/operator route. Initial latch survives release; per-frame reset and absence of a retained matching contact clear active-contact state on the next frame. “Release clears every latch immediately” would be incorrect for this tested hold.

### 11. Ordinary arc ownership — Native-integrated through dispatch

Reuse009's original arc factory/color/geometry/checkpoint setup: arc1000..4000, linear(.5,.5), tempo120/speed6/density1, interval250, supplied spatial defaults and feedback shell; orthographic design1280×720, Camera Z900; contact design(640,210). The fixture's old prepared contact vector is removed **before** testing, and actual JNI begin supplies the new retained native Touch. Native ownership/cache/activation is never replaced by flags.

| Step | Owner / active / evidence |
|---|---|
| DOWN42 at1000 → generated2000 | owner−1/active0 initially; contact retained natively |
| model frame1001 | owner2000/active1 |
| frame1125 | first checkpoint PURE; H7.472726821899414 in this N11 long-arc fixture |
| JNI MOVE toX1200; frame1150 | active0, **owner still2000** |
| JNI MOVE backX640; frame1175 | active1, owner2000 |
| refresh timeline natively to1200, then JNI UP | owner−1, release1200, retained empty, mask/map empty; active byte remains1 immediately |
| reuse Android42 at1200 | new engine Touch/slot0, generated2001; no manual ownership |
| frame2199 /2200 | owner−1 /2001; active0 /1; at2200 PURE count4, H27.890907287597656 |

Replacing UP with **JNI CANCEL** reproduces the ownership release and reacquisition trace. With interval250, the tested rejection uses `now − release < min(4*intervalInteger,1000)`, as009 established; no universal1000ms delay independent of interval is inferred.

A second UP experiment deliberately omits the independent timeline refresh: wall1200 UP sees **E1175**, stores release1175, and the new generated2001 contact rejects2174 but accepts2175. Begin of the replacement contact refreshes E1200; it does not retroactively correct release time. This is now verified through JNI→GLView→listener cleanup, rather than only a direct cleanup call. Android timestamp999 does not override E in the cleanup.

The active byte remaining1 immediately after cleanup must be distinguished from released ownership and absent retention. A following native frame resets/recomputes contact state. Temporary spatial departure preserves the owner; actual UP/CANCEL removes it under the tested conditions.

### 12. Suppression and rejected-event state

| Controlled condition | Native observation |
|---|---|
| Director.GLView null | JNI returns without mapping/Touch/listener calls |
| duplicate ID / unknown MOVE or UP / full15-slot pool | ignored as specified in section5; no replacement contact for skipped input |
| dispatcher+124=0 | engine still maps/updates/releases the Touch; no gameplay callback, generated counter unchanged |
| model+148 nonzero before DOWN | begin operator runs but skips assignment/initial input/retention; engine mapping still exists until UP; no cleanup call |
| model pause byte+138=1 | gameplay begin still assigns generated ID and retains Touch; eec024 rejects judgment; UP removes retention through cleanup |
| model finished byte+139=1 | same tested assignment/retention/no judgment/UP-cleanup outcome |
| model+148 changed to1 while already owning arc | UP clears engine mapping but gameplay cleanup is suppressed; old Touch remains retained and owner2000 remains |

These flags are supplied test conditions, not execution of Android pause/finish transitions or proof of a deployed stranded-contact bug. Real paths that set+148, disable listeners, replace scenes or subsequently clean contacts can change the outcome. Unassigned gameplay fields are zero in the allocator fixture; zero is **not** an assigned valid contact ID in the suppressed cases.

Two additional original native gate tests separate Director state from model state. With Director+130=1, the scoped Director frame skips both update notifications/Scheduler yet still reaches scene traversal and one model frame. With Director+220=1, original wrapper `17371d8` returns without Scheduler/model frames. A subsequent external JNI DOWN in either fixture still reaches gameplay and scores PURE1: these Director flags do not themselves reject the separate input entry. This does not establish that Android will deliver such a Runnable while paused/stopped, nor that application pause leaves model+138 unset. Only the isolated supplied gate combinations are tested.

### 13. Dispatched versus direct gameplay-input regression

With identical tap1000, projected input(290,360), generated ID1000, frame/E1000 and ordinary mode0/no ability:

| Observation | Original JNI→GLView→listener→eec024 | Direct eec024 with prepared Touch |
|---|---:|---:|
| PURE / note resolved / note contact |1 /1 /1000|1 /1 /1000|
| live gauge |40.20000076293945|40.20000076293945|
| E / last model frame |1000 /1000|1000 /1000|
| retained contact count |**1**|**0**|

Judgment/gauge agree. Overall state is **not identical**: original begin allocates/maps the Touch, assigns ID/frame metadata and retains it; direct initial input alone does not. The retained-contact difference follows original begin's append/retain at `19500b0..19501b0`, not a numerical discrepancy. This is why the JNI/listener integration matters for subsequent continuous input and cleanup.

## Native validation traces and execution inventory

### 14. Executed scopes, expected outputs and confidence

All successful native tests use original ARM64 instructions mapped from ELF PT_LOADs with RELATIVE relocations. Unicorn2.1.4, Capstone5.0.9, pyelftools0.33; library memory0..0x2100000, synthetic arena0x4000000..0x6000000 and stack/TLS to0x6100000, SP0x60df000, TPIDR_EL0=0x60f0000; per-call5M instruction budget. Original generated functions, tree/map logic, listener iteration, clock arithmetic, projection/judgment, ownership and checkpoint loops are not supplied Python equations.

| Validation | Original entries / important calls executed | Expected and observed |
|---|---|---|
| Single begin→tap |be31a8,97d784,1980970,18feb24,8865a0,c2bf98,194ff80,eec024,1730290|native Touch/mapping, contact1000, PURE1, H40.20000076293945 |
| Boundary/multi/capacity |all four JNI entries;160b710;15af680/1556de4→95e32c; native tree operations|move reuses object; duplicates/unmapped ignored;15 slots; array order retained; release/cancel empty maps/retention |
| A–C frames |1793f8c scoped as specified;1980970,13d3f44,d630b8,9effe0,18be2f8,10a7550|event names/order and exact clock/cache/guard trace in section7 |
| Camera D |f1b510,c7820c,b3dc38,13d3f44,9effe0,JNI begin and original camera projection|X0→150 and matrix X translation0→−.1171875; PURE1 in both scoped controls |
| Hold UP/CANCEL |full ordinary native hold construction; native index/frame; all touch transports;f9a50c|native latch/contacts/checkpoint, deferred per-frame contact reset as section10 |
| Arc UP/CANCEL/reuse |178f7fc,d93594,ba81e8,1925084; native index/frame; JNI/listener;14858d4,15a90c4,f9a50c,13db7a0|owner acquired/released/reacquired; temporal/spatial differences in section11 |
| Pause/finished/mode/dispatcher gates |original JNI/dispatcher/operators with stated supplied flags|suppressed layer and remaining state in section12 |
| direct comparison |same input into recovered full transport versus eec024|same judgment/gauge, different retention lifecycle |

Confidence is high for the tested native paths and instruction-backed argument/field relationships; bounded for other listeners, modes and Java scheduling. No test starts after JNI while claiming to execute JNI. No test invokes a direct judge as a substitute for the successful dispatch chain.

### 15. Synthetic objects, hooks and excluded branches

Native Touches, engine map nodes, EventTouch vectors and the gameplay listener/function objects are created by original code. The harness supplies a JNIEnv interface, prepared Director/GLView environment, enabled dispatcher, initialized process-level listener-ID strings and empty static pointer-map header. Those process initializers are not executed. Model/timeline/chart/scene and camera/environment fixtures follow the stated009/010 boundaries. Contact-counter initial values1000/2000/3000 make the identity distinction visible; subsequent increments are original.

| Boundary | Supplied behavior / limit |
|---|---|
| synthetic JNI callbacks `0x4000400/410/420` | array length / integer-region / float-region copies; arena callback addresses, **not ELF VAs** |
| Director getter `a4227c` | prepared Director pointer; virtual GLView touch calls remain original |
| new/malloc/calloc `1a6d9c0,1a6dd40,1a6e090,1a6df10,1a6ee10` | aligned zeroed bump allocations; no allocation failure |
| delete/array-delete/free `1a6d9e0,1a6e0a0,1a6ded0` | no reclamation; lifetime/free correctness not proved |
| Ref ctor/retain/release/autorelease `121a0ec,147fe48,d6dc98,10ac6e8` | return/no-op; original caller paths execute but real reference pools/destruction are outside scope |
| memory `1a6d9d0,1a6daf0,1a6db30` | memcpy/memmove/memset |
| string/compare `1a6da50,1a6db80,1a6da80` | libc++ short/long representation, host copy/assignment/comparison services; native dispatcher containers/sorting are original |
| hold AFF fixture only: `1a6dad0,1a6db40,1a6dc20,1a6da60,1a6db00,1a6db20,1a6dda0,1a6e1a0` | strlen, memchr, substring, string compare/append/push/erase services from010 |
| hold AFF fixture only: `1087f14,b06728,1a6e210,1a6e230,1a6dd80,1a6e150,1a6e200`; ctype GOT `1b96168` | numeric stream capture/destruction and f32/int extraction, atoi/atof, ASCII whitespace/classification; original lexer/grammar/header/body/factory logic remains native |
| dynamic_cast `1a6db90` | original RTTI single-inheritance identity/base-chain resolver; general ABI not claimed |
| steady clock `1a6dc60`; gettimeofday `1a6e5c0` | controlled nanoseconds / timeval derived from supplied wall milliseconds |
| configuration `bda064` | ordinary mode0 when queried |
| audio `107af5c`, optional result/time helpers `e2388c/1a6de50` | external audio suppressed; optional-null/deterministic epoch; no judge/gauge substitution |
| model delegate synthetic `0x4000200` | logging/no-op UI/finish notifications; arena address |
| design/frame size `f09110` when called | supplied1280×720 external dimension helper; native projection stays original |
| inherited `19f2e40` hook | return, matching the inspected original RET at that address; not counted as a newly executed helper body |
| Director `1794004 → 17940d0`, stop17940f8 | skip render/matrix-stack preparation and end scope before later rendering/counter increment |
| GameScene `18be380 → 18be470`, base draw129c924 | suppress HUD/base drawing while preserving actual model call/guard/counter store |
| arc feedback shell | virtual+530 points to original155241c, which writes the feedback latch; no GPU subtree |

The hold fixture's native AFF construction also uses010's documented string/ASCII/number services; it is not a new claim of native libc++ numeric parsing or metadata JSON execution. End/cancel reference-release calls are observed, but actual object destruction cannot be inferred from no-op release services. Slot/map reclamation logic itself is original and observed.

Unexecuted branches include arbitrary one-by-one swallowing, scene-priority ordering, event stop-propagation, registration/removal during dispatch, malformed JNI arrays, nonfinite/overflow coordinates, exceptions, Android Java queue/thread execution, full rendering and complete lifecycle startup/teardown. The native Scheduler's deferred-vector nonempty path remains instruction-backed. The executable Director scope does not include JNI nativeRender or the whole Director main-loop wrapper; those relationships are decoded separately.

## Pseudocode

```text
# Java: reconstructed from bundled smali, not executed
onTouchEvent(event):
    stamp = milliseconds(elapsedRealtimeNanos())
    ids, xs, ys, products = capture_all_pointers(event)  # size*pressure
    action = event.action & 255
    if action in {DOWN, UP}: i=0
    if action in {POINTER_DOWN, POINTER_UP}: i=event.action >> 8
    if action in {DOWN, POINTER_DOWN}: queueEvent(Down(id[i],x[i],y[i],product[i],stamp))
    if action in {UP, POINTER_UP}: queueEvent(Up(id[i],x[i],y[i],product[i],stamp))
    if action == MOVE: queueEvent(Move(ids,xs,ys,products,stamp))
    if action == CANCEL: queueEvent(Cancel(ids,xs,ys,products,stamp))
    return true

Runnable.run(): renderer.handleAction...(captured_fields) → JNI_export(...)
# Platform queue consumer/order is unavailable; do not invent a drain inside Director.

# Native-integrated from original JNI entry
JNI_begin(javaID,x,y,product,stamp):
    if Director.GLView == null: return
    GLView.begin(1, [sign_extend_i32(javaID)], [x], [y], [product], [1.0], stamp)

GLView.begin(...):
    for pointer in input_order:
        if AndroidID_already_mapped(pointer.id): continue
        slot = first_free_bit_0_through_14()
        if none: continue
        touch = native_allocate_Touch()
        native_set_slot_initial_current_previous_force_timestamp(touch)
        native_map_insert(pointer.id,slot,touch)
        event.touches.append(touch)
    if event.touches not empty: EventDispatcher.dispatch(event.action=BEGIN)

gameplay_begin(touchVector):                       # 194ff80
    if model.modeGate148 != 0: return
    for touch in touchVector:
        touch.contactID = generatedCounter++
        touch.lastFrameAtBegin = lastModelFrameGlobal
        initial_input(model,touch)                 # eec024
            if paused138 or finished139: return
            native_update_GameTimeline()
            native_project_select_judge_record()
        native_retain_and_append(model.contacts,touch)
        native_collect_pressure_and_integer_position_statistics()

JNI_move(arrays,stamp): native_read_arrays_sign_extend_and_call_GLView_move()
GLView.move(...):
    update_current_previous_pressure_for_mapped_IDs()
    dispatch(MOVE, actual_updated_Touches)          # no timestamp overwrite
gameplay_move(...): native_pressure_statistics()  # no model frame or clock refresh here

Director_frame():                                  # ordinary decoded/full order
    native_compute_dt(); GLView.pollEvents()       # bundled poll target is RET
    if not Director.paused130:
        dispatch(director_before_update)
        Scheduler.update(dt)                      # ActionManager first-priority callback
        dispatch(director_after_update)
    native_render_preparation_and_scene_traversal()
    GameScene.visit():
        if Director.counter134 != scene.stamp4d0:
            model.frame()                         # refresh E, cached depths, continuous contacts
            native_HUD_and_render_updates()
            scene.stamp4d0 = Director.counter134
    native_later_rendering_and_counter_increment()
# Only the explicitly described scoped Director/visit portions execute in011.

JNI_end_or_cancel(...,stamp):
    GLView.shared_terminal(action = END_or_CANCEL) # original separate wrappers
        update_final_coordinates_for_mapped_IDs()
        collect_actual_Touches_in_input_order()
        clear_engine_slots_and_remove_ID_map_nodes()
        dispatch(action, touchVector)
            if model.modeGate148 == 0:
                native_remove_retained_pointers(touchVector)
                for touch and chartColor:
                    native_release_matching_owner(touch.contactID, CURRENT_STORED_E)
                    # Does not refresh E or substitute Android stamp.
        native_release_event_Touches()
# Hold contact flags are recomputed by a later frame; initial latch may remain.
```

## Updated integration coverage

| Interface |011 evidence | Remaining boundary |
|---|---|---|
| Android MotionEvent→Runnable | Instruction-backed, complete action/payload reconstruction | Android VM/framework queue consumer and physical capture |
| Runnable→renderer→JNI | Instruction-backed Java; original JNI entries execute separately | no executed Java Runnable |
| JNI→GLView→Touch/map→EventDispatcher→gameplay listener | **Native-integrated for all four actions** | supplied JNIEnv/Director/view/global startup/services |
| Native dispatch→tap judgment/gauge | **Native-integrated** | synthetic chart/model/camera/clock environment |
| Native dispatch→hold/arc continuous state→UP/CANCEL cleanup | **Native-integrated, scoped** | geometry/defaults/feedback shell and mode selection |
| Director notifications→Scheduler/ActionManager→GameScene guard/model frame | **Native-integrated scoped frame** | excluded renderer/HUD; counter held by fixture |
| Input order versus model/camera state | Native-integrated consequences under controlled A–D schedules | actual platform queue/draw selection unknown |
| Full Android pause/resume/interruption | Instruction-backed leads; selected native gates tested | full lifecycle intentionally not expanded |
| Flick gameplay | unchanged/unproven, outside mission | no playable construction claim |

## Remaining synthetic dependencies

The principal dependency reduced is the manual creation of gameplay Touch objects and manual retention/removal. JNI/GLView and the original registered listener now produce that state. We still supply MotionEvent-equivalent JNI inputs, native array-access services, process globals, a prepared Director/view and gameplay environment, deterministic clocks, standard-runtime/reference services and selected rendering/audio boundaries. The event sequence itself is supplied, not selected by a real GLThread queue.

## Unresolved Mysteries

1. The exact Android platform GLSurfaceView queue consumer for the target device/build, its batching versus draw/pause state, and actual event latency. The archived app alone does not provide that implementation.
2. Full lifecycle writers of model+148 and listener/dispatcher gates, and subsequent cleanup when those gates change mid-contact. The supplied gated-arc experiment isolates the interface without proving application reachability or a leak/bug.
3. Arbitrary scene-priority/one-by-one listener interaction, swallowing, event stopping and mutation during dispatch; complete reference pools, destruction and process shutdown.
4. Native Scheduler deferred-function producers and nonempty execution joined to product work; no equivalence to the Java touch queue is established.
5. Full nativeRender/Director rendering, camera defaults, Android foreground/background→timeline/audio ordering, queued cancellation around pause/resume, and scene replacement. Optional application-lifecycle expansion is deliberately stopped after useful essential evidence.
6. Malformed JNI arrays/IDs/float values, counter wrap and all unusual modes. Flick remains outside scope.

## GitHub Status

Only this new011 report and an append-only entry in `context.md` are authorized changes, based on `8bc7dd7420efc28ed8b68f6131f2f4bc255d0fbf`. Reports001–010, historical context, README, project instructions, archive/binaries/assets and harness publication are preserved/excluded as requested. A fresh check before publication must reject duplicate/concurrent011 work; the final headquarters return records the exact commit SHA, pinned read-back equality and comparison against the starting tree. No self-referential future SHA is invented in this file. Expedition012 is not initiated.
