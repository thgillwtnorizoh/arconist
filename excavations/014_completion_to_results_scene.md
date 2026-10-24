# Expedition 014 — Gameplay Completion, Results Presentation & Native Save Invocation

Date: 2026-10-24. Project Arconist; `thgillwtnorizoh/arconist`, `main`.

## Result

**Strong success, including substantial native deferred-callback execution.** The manually constructed GameResult→results-context relationship from013 is eliminated. A completed native two-tap run enters the original model delegate, GameScene completion handler, snapshot/cache, native timer registration and Scheduler callbacks. The original transition closure allocates a **GameSession**, obtains its result from **ScoreState+68**, retains that exact pointer, selects and constructs **NormalGameResultScene**, and constructs a scoped **TransitionShutter** carrying the resulting scene.

Original Director scene-replacement code records the transition request. A separately driver-triggered **original TransitionShutter callback `0x963094`** then makes the actual native virtual call into the result initializer. Original initializer segments produce the save gate and call the original save helper/writers/bundled SQLite. Native query readback gives PURE2, FAR0, LOST0, score **10,000,002**, health80 and clearType3. An all-missed native run likewise stores score0, LOST2, health0 and clearType0.

This is **not a fully uninterrupted executed presentation/Director activation sequence**. One UI animation-completion service is supplied; the shutter's activation callback is driver-triggered rather than action-driven; shutter/result UI-heavy blocks are explicitly skipped. These boundaries are enumerated below. The native GameSession/result relationship, result-scene constructor, gate producer, gate branch and saving call are not supplied by the driver. No real player database, authentication, network submission, graphics or full Android runtime is used.

## What I Found

### Preparation and evidence scope

Read the supplied project instructions, inspected the archive, checked current GitHub/context, read013's complete report and consulted006/008/011/012 for completion, snapshots, scheduling and lifecycle state. Existing scratch loader/fixture files were available and inspected; they are reused infrastructure, not a claim to recover inaccessible Work-session memory. New014 adapters and tests were written separately. The persistence matrix was not repeated.

Starting commit: **`96a1a1f039d64cf34d98c85d92e1ea4c5cba8541`**. Starting root tree: **`3d53ae2d8da9bbe9e1070a45cc43ef893c962324`**. Starting context blob: **`5ef344a06746852f805cd725ecf37005dd2196c2`**. No014 report existed.

Archive inspection found9,658 entries. The ZIP member `lib/arm64-v8a/libcocos2dcpp.so` was hashed directly and matches **`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`**. Extracted ELF Build ID is **`17d660edbf37ca78beefc32e07672c97419ddce6`**. All addresses below are main-library ELF virtual addresses before relocation. Unicorn2.1.4 executes original ARM64 PT_LOAD instructions with RELATIVE relocations; Capstone5.0.9/pyelftools0.33 support decoding. No writer/completion decision is reimplemented as a host-language rule.

**Native-integrated** means original routines execute together within the stated scope. **Native-isolated** means original code executes with enclosing state/callers supplied. **Instruction-backed** means decoded binary/RTTI/relocation evidence without execution of its enclosing path. **Interpretation** identifies inferred meaning. **Unknown** marks missing or unverified behavior. A Native-integrated segment can still contain declared external-service adapters; it does not imply complete application execution.

## Native gameplay completion call chain

### Model completion, delegate and scene latches

The two-tap fixture executes original `0x10a7550`. Chart end is1270. At **E1270**, the ordinary completion delegate has not run. At **E1271**, the original strict comparison at `0x10a7ba0–0x10a7ba4` crosses the end. With model+140=0, the ordinary branch:

```text
0x10a7d50       load model+40 delegate
0x10a7d58       store model+139 =1
0x10a7d5c       w1=0 (ordinary end notification)
0x10a7d64–68    call delegate.virtual+10
0xe2c124       subtract secondary-base offset2e8
0xe2c12c       branch to0xc27d34
```

The prepared GameScene has its native secondary-base vtable **`0x1ae7448`** at scene+2e8, and model+40 points there. The vtable's+10 slot is the original thunk `0xe2c124`. Other gameplay UI notifications are bounded services; the finish thunk and handler are not hooked out.

At `0xc27d64`, the handler sets **scene+49a=1**, records a native clock reading at+4a0, calls its declared UI/progression boundaries, invokes `0x1600bb0` at **`0xc27dcc`**, then retrieves the result through model+38→ScoreState+68 at `0xc27dd0–0xc27dd8`. It does not use snapshot X0 as an authoritative result pointer.

**The handler itself has no entry check of scene+49a.** The tested normal repeat is suppressed earlier by model+139 at `0x10a7c0c–0x10a7c10`. Scene+49a additionally participates in the lifecycle guards established in012. These are separate roles, not interchangeable pause/finished flags.

### Completion-side processing retained in scope

The handler's history insertion/retain and `0xbb5640` result attachment execute. The history vector reached through GOT `0x1b964f0` is prepared with one16-byte placeholder entry because the handler unconditionally slides/removes the first entry before appending; this is an explicit startup-state precondition, not a newly discovered default. The native inserted record contains the cached result and scene+310 mode.

`0x1246c98` executes its **scene+380==null early return**. The fixture has no completion packet. Consequently, packet enrichment, serialization, queue insertion and worker activation are not exercised in014. `0xbb5640` attaches the null packet at result+e8. Completion's unrelated UI/audio/progression services are logged boundaries. With no special scene, the original handler reaches delayed presentation `0xe5c700` at `0xc27f1c`.

The failure notification path uses the same delegate with true and has other state handling. The ordinary no-hit test below finishes through the normal end branch with notification=false but classifier0; these observations must not be conflated.

## Deferred callback/scheduler reconstruction

### Original timer creation and dispatch

`0xe5c700` builds the native function object with vtable **`0x1b65058`**, captures the actual GameScene pointer and finish boolean, and calls Node helper **`0x159bdec` at `0xe5c7d0`** with key **`endingAnimation`**. Its ordinary delay is4.0f. The helper reads scene+1a8 Scheduler and scene+1c0 running flag and tail-calls **`0xea937c`** with interval0, repeat0, chosen delay and paused=!running.

The fixture supplies a constructed Scheduler (`0xda7a90`) and running GameScene. Original registration creates a **cocos2d::TimerTargetCallback**, vtable **`0x1b18a18`**, and copies the native function object; it is not an injected callback vector.

Relevant observed layout:

| Object | Fields |
|---|---|
| Scheduler | +c time scale1; +30 native target/timer hash-list; +38 current target during update |
| Target entry | +0 timer array, +8 target, +10 iteration index, +18 current timer, +21 paused, +38 next list entry |
| Timer array | +0 count, +8 capacity, +10 pointer buffer |
| Timer | +18 float elapsed (initial−1); +1c infinite flag; +1d waiting-for-delay flag; +20 execution count; +24 repeat count; +28 delay; +2c interval; +30 target; +60 active function-object pointer; +70 libc++ key string |
| Function object | native vtable; captured scene at+8; finish boolean at+10 for the first closure; virtual+30 invokes the original body |

Original Scheduler update **`0x13d3f44`**, callsite **`0x13d413c`**, runs Timer update **`0x15985d4`**. Timer trigger virtual+10 resolves to **`0x1875b94`**, whose callsite **`0x1875bc8`** invokes the function object's virtual+30. The first ending body is **`0x19bbdd0`**. Native repeat/cancellation code removes the one-shot timer after it fires.

The first Timer update recognizes elapsed−1 and writes0 without accumulating that tick's dt (`0x15985f0–0x159860c`). Later updates add float32 dt and compare against the native delay. Thus “4 seconds” is a timer parameter, not a measurement of physical Android queue latency or an assertion that elapsed wall time always equals4.0 from chart completion.

### Executed ending sequence and explicit UI handoff

| Stage | Registration/producer | Key / delay | Actual invocation |
|---|---|---|---|
| Ending delay | `0xe5c700 → 0x159bdec → 0xea937c` | endingAnimation /4.0f | Original Scheduler→Timer→`0x19bbdd0` |
| Finish UI/animation completion | `0x19bbdd0` constructs its original continuation and calls `0x1a51054` | UI duration not asserted | UI service substitutes for animation; original continuation clone/body retained |
| Outro | Original continuation **`0x147dee8`**, delivered at that service boundary, calls159bdec | outro /2.0f | Original Scheduler→Timer→**`0xf0b48c`** |
| Scene-change delay | `0xf0b48c` calls an inert animation widget's virtual+50, then159bdec | changescene /float32 **0.30000001192092896** | Original Scheduler→Timer→**`0x18f11c0`** |

At `0x1a51054`, the supplied UI service reads the **actual** function object passed by native code. It allocates copy storage and tail-calls that object's **original virtual+18 clone routine**, preserving native capture copying. The ordinary continuation's vtable is `0x1aebc68`, whose virtual+30 is147dee8. The driver later delivers this copied native continuation when declaring the omitted UI animation complete. It neither fabricates the continuation nor calls18f11c0 as a replacement for the intermediate callbacks. The animation implementation and its real completion timing are unexecuted.

Controlled ordinary trace:

| Input to original Scheduler / service | Observed state |
|---|---|
| Immediately after gameplay completion | endingAnimation elapsed−1, delay4; result cached |
| dt0 | elapsed0, no ending callback |
| dt3.999 | elapsed **3.999000072479248**, no ending callback |
| dt0.001 | 19bbdd0 invoked once; ending timer removed; UI continuation captured |
| Driver delivers captured UI completion | 147dee8 invokes native registration; outro elapsed−1/delay2 |
| dt0 | outro elapsed0 |
| dt2 | f0b48c invoked once; changescene registered; native loop initializes its elapsed0 during this update |
| dt0.3 | 18f11c0 invoked once; results context/scene/shutter constructed; replacement requested |
| Additional dt10 after tested activation | no repeated ending/scene-change callback |

Scheduler dt is driver-controlled, independent of GameTimeline E and the fixed result date. No full Director draw loop, platform event queue or hardware scheduling distribution is measured. The two native Director update notifications remain notifications, not queue drains.

## GameResult lifetime and ownership

Unlike013's supplied Ref counters,014 executes original **Ref initialization `0x121a0ec`**, retain **`0x147fe48`** and release **`0xd6dc98`** for valid objects. Their actual +8 arithmetic is observed. Two null pointers arising from the deliberately partial environment are handled as inert environment boundaries; valid result/context/scene reference operations execute original instructions.

Ordinary regression pointer and counter trace:

| Step | Original callsite / operation | Result reference count |
|---|---|---:|
| Factory initialization | `0x180ea0c → 0x121a0ec` | 1 |
| ScoreState caches/retains snapshot | `0x1600e18 → 0x147fe48` | 2 |
| Completion history retains same result | `0xc27e84 → 0x147fe48` | 3 |
| Native GameSession stores/retains it | `0x18f133c` store; `0x18f1340` retain | 4 |
| Original score-cache insertion retains it | writer cache helper returns at0x1355970 | 5 |

Observed ordinary result pointer is **`0x414da40`**, context **`0x414e540`**, NormalGameResultScene **`0x414e640`**, TransitionShutter **`0x414f1c0`**. These are **synthetic arena addresses**, not ELF VAs or production heap constants. Identity stays unchanged from ScoreState+68 through GameSession+18, scene+2e8→GameSession, writer input and DB cache.

GameSession starts with Ref1 and constructor187c0c8 retains it to2. The result scene starts1 and incoming-transition retain makes2. TransitionShutter starts1 and Director replacement retain makes2. Native timer reference releases/cancellation also execute. Autorelease `0x10ac6e8` remains an inert pool boundary, and allocator frees do not reclaim the arena; these counts are a controlled ownership trace, not proof of final production destruction, absence of leaks or a complete lifetime graph.

## Results-context construction

The original context is identified by native RTTI **`11GameSession`**, vtable **`0x1a9fee8`**. The ordinary branch of **`0x18f11c0`** allocates **0xf8 bytes**, zeroes it, initializes Ref and native fields, and calls its original trivial success initializer `0x13fd7c4`. No GameResult pointer is assigned by the harness.

Executed producers:

| GameSession field | Original source / store |
|---|---|
| +c | GameScene+310 at18f1324..2c |
| +10 | GameScene+328 at18f1358/64 |
| +14 | selected gauge+40 float at18f135c/68 |
| **+18** | **model+38→ScoreState+68** loaded18f1268..74, stored18f133c, retained18f1340 |
| **+20** | special-scene pointer at GameScene+308; its+2b8 when present, otherwise0; stored18f1378 |
| +24 | `(scene+34c || (scene+34d && model+13c))`; original branches18f1374..13a0 |

In the ordinary fixture, session+c/+20/+24 are all0. The account snapshot branch is supplied a selected-character metadata object rather than changing scene+34c to avoid account lookup. Character ID49 suppresses unrelated character-specific completion counter branches; this identity/configuration choice is disclosed, not a recovered universal account default. Model/result scoring mode remains ordinary0.

## Results-scene selection and initialization

### Original construction and scene replacement request

Original **`0xd11738`** receives the native GameSession at `0x18f14b0`. Ordinary context+c=0, +20=0 and empty contextual vectors select constructor **`0x187c0c8`**. This executes original base constructor **`0xab9d60`**, Node constructor131419c, retains the GameSession at **scene+2e8**, installs **NormalGameResultScene vtable `0x1afe2a0`** through GOT1b96690 and writes **scene+2f8=0** at187c114. Default-camera factory12a1654 is supplied the already constructed fixture Camera; actual resource-backed default-camera construction is not repeated.

`0x18f14d4` calls original factory **`0x9ff610`**, which constructs **TransitionShutter**, vtable **`0x1af1868`**, and invokes `0x16a41c4`. Its original prefix sets duration0.75f and calls **`0x170c208`**. That original base-transition initializer stores/retains:

- incoming result scene at **transition+2e8** (`0x170c23c`);
- current Director scene at **transition+2f0** (`0x170c248–0x170c25c`);
- duration at **transition+2f8** (`0x170c238`).

Shutter child/resource preparation after this prefix is skipped explicitly below. The enclosing9ff610 factory and its return still execute, returning the actual TransitionShutter, not the result scene as a substitute.

At **`0x18f14f8`**, original Director replacement **`0x9c90c0`** executes with that shutter. Prepared Director+140 is the running GameScene and its native scene-stack vector contains the same scene. Native replacement updates the stack/reference state and stores **Director+148 = TransitionShutter**. Observed next-scene pointer is0x414f1c0. This is an actual **replacement request**, not proof that the complete Director scene activation/drawing cycle ran.

### Production initializer caller newly identified

A targeted indirect-call investigation locates **`0x963094`**, the original TransitionShutter incoming-initialization callback. Its essential native path:

```text
0x9630e8–fc     outgoing Scene.virtual+310 (teardown service boundary here)
0x963100–104    release outgoing Scene
0x963108       load incoming result scene from shutter+2e8
0x96310c       clear outgoing pointer at shutter+2f0
0x963110–118    incoming.virtual+4d8 → NormalGameResultScene initializer891150
0x96311c–12c    incoming.virtual+150(true)
```

The real callback source is instruction-backed in **TransitionShutter onEnter `0x12157ec`**: at `0x12159b8–0x12159dc`, it builds a native bound function object containing method963094 and `this`, and creates a CallFunc action through10de878; action combination follows14be12c. **This onEnter/action subtree is not executed in the final regression.** The driver invokes original963094 with the native-created shutter when declaring the omitted shutter activation ready. This replaces a direct driver call to the result initializer with its original native production caller, but does not establish action-driven or full Director-driven activation.

### Exact executable scopes and omissions

The following instruction redirections are deliberate. They do not modify the ELF file, result/context links, gate values, writer or SQL rules.

| Scope | Executed | Skipped / supplied |
|---|---|---|
| Shutter initializer16a41c4 | Original prologue,0.75-duration selection, entire170c208 incoming/outgoing initialization; epilogue | At **16a420c →16a4a4c**, skip the remaining shutter flags/progression/layout/resource/widget preparation. Its zeroed allocation supplies those unexecuted state defaults. Not a full shutter initializer validation. |
| Incoming-init callback963094 | Original prologue, bounded audio/resource prelude, outgoing release/clear, original incoming virtual dispatch, visibility and epilogue | Outgoing virtual310 targetd75c68 logged/returned; audio9d2518/provider virtual20 supplied. At **963130 →963354**, skip subsequent shutter art, closing-delay/callback/global timing work. |
| Normal initializer891150 | Original prologue; original base initac6d1c; original gate producer89164c..684; original save block89219c..1d8; original epilogue8928e0..914 | At **891190 →89164c**, skip initial UI/account/layout work. Supply X28=existing application-global address and X26=X29−60, the native stack scratch address normally prepared there. At **891688 →89219c**, skip further UI/progression construction. At **8921dc →8928e0**, skip remaining UI/animation setup. No category, result pointer or gate Boolean is assigned. |

This is a **genuine original initializer segment**, not execution of all891150. Native base success remains W27 and the scoped initializer returns1 through its actual epilogue; that does not claim successful construction of the omitted complete screen.

## Original save-eligibility invocation

### Newly recovered producer of scene+2f8

The initializer's original instructions at **`0x89164c–0x891684`** execute before the save block:

```text
89164c  ldr  x8,[x20,#2e8]       # native GameSession
89165c  ldr  w22,[x8,#20]        # special-scene-related integer
89166c  sub  w8,w22,#9
891670  cmp  w8,#2
891678  cset w8,lo               # unsigned difference <2
891684  strb w8,[x20,#2f8]
```

Thus **scene+2f8 = (GameSession+20 is9 or10)** in this producer. This refines013's unresolved gate provenance without modifying that report. It is not the same as the save helper's special-ID8/19 clear-suppression rule, and no runtime gauge equivalence is inferred.

The original block **`0x89219c–0x8921dc`** loads session+18 result, ORs result+b0 with scene+2f8, and if zero calls **`0xdc2c48` at0x8921b8**. The complete native helper invokes score writer13552d4 atdc2cd4, which separately invokes clear writer12a5e60 when its bit0 flag permits. Original bundled SQLite executes as validated in013. The adjacent1049858 progression call and helper's1019c18 service are logged boundaries.

Ordinary inputs produce result+b0=0, session+20=0, and scene+2f8=0 through original instructions. No synthetic zero assignment supplies the decisive initializer gate.

## Native completion-to-SQLite validation

### Test fixture and reproducible environment

Prepared native LogicChart/model infrastructure from009/013: timing120BPM, speed6, density1, two native LogicTapNotes at1000/1150 with raw lanes1/2, count2, end1270; ordinary gauge mode0, no ability. Native timing/note factories, depth evaluation, index construction, ScoreState/gauge factory14f0a94, model frame, projected initial inputeec024 and score/gauge/result logic execute. No AFF/JNI/lifecycle reconstruction is repeated.

The camera projection environment is1280×720. At E1000 and1150, run a model frame then deliver prepared Touch positions(290,360)/(540,360), IDs1000/1001. Underlying steady-clock values are controlled; authoritative judgment time is native GameTimeline E. Result wall-date `time(&t)` separately writes/returns1700000000. Chart song is supplied `expedition014`, difficulty metadata+124=2, raw global partition0. Running scene, Director/Scheduler/dispatcher/scene stack, account identity, inert outro widget, history seed and application/database pointers are prepared environment state.

Private SQLite `:memory:` setup, original schemas and ct migrations, native API PLT resolution and SQL readback are reused from013. This is the bundled native SQLite engine, not host SQLite. No real database file is opened. Physical persistence/crash durability remains untested.

### Test A — Native ordinary result and save invocation

The result reaches GameSession and NormalGameResultScene without a driver-written relationship. Before incoming initialization, no score row exists; after original963094→scoped891150→dc2c48, score and clear rows exist. First writer/helper count is1 each. Native gate fields are0/0.

Actual SQL score row:

| id | version | score | shinyPerfectCount | perfectCount | nearCount | missCount | date | songId | songDifficulty | modifier | health | ct |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 1 | 10000002 | 2 | 2 | 0 | 0 | 1700000000 | expedition014 | 2 | 0 | 80 | 0 |

Clear row: `(id1, songId=expedition014, songDifficulty=2, clearType=3, ct=0)`. Native result live health is80.4000015258789; snapshot floors to80. ScoreState+68, session+18 and the original writer's result argument all refer to0x414da40. Native score getter returns10000002 with stored-score override byte+b1=0. SQL binds and native row queries match. Version1/date are fixture-observed values, not an asserted production build/date policy.

Each original ending body19bbdd0/147dee8/f0b48c/18f11c0 runs once. The original scene selector, Normal constructor, TransitionShutter factory and Director replacement run once. Final recorded ordinary trace has two891150/helper/writer invocations only because of TestB's deliberate second initializer call. Observer-only hooks can also increment a generic hook counter; reported invocation counts use actual function-entry event records, not a sum double-counting an observer and its hook.

### Test B — Repeated handling is not one universal idempotence claim

1. **Original model repeat:** frameE1272 after completion leaves result pointer unchanged and c27d34 count1; no second snapshot or ending timer is registered. This exercises the model+139 guard, not a scene-handler49a guard.
2. **Native timer repeat:** after the controlled ending/outro/change sequence and an extra dt10, first/last ending callbacks remain at count1; one-shot timers are consumed.
3. **Forced initializer repeat:** driver invokes the produced scene's original virtual+4d8 initializer again, with the same scoped UI exclusions. The same GameSession/result stay installed; initializer/helper/writer counts1→2; SQL row is exactly unchanged, including id/date, and clear remains3. This is not evidence that production normally initializes the same results scene twice.
4. **Forced handler reentry, separate fixture:** directly invoke c27d34 after a completed model. Handler/snapshot entries1→2; cached result stays **0x414d9c0** and result refs3→4. The existing endingAnimation timer **0x414de40** and function object **0x414de80** remain the same (initial elapsed−1/delay4); registration is revisited without creating a second same-key timer in this tested state. The native result is not allocated again. This is an isolated bypass of the model's guard, not a discovered reachable duplicate-completion bug.

The shutter incoming-init callback clears outgoing+2f0 during its first invocation; the enclosing code assumes a valid outgoing scene on entry. It is not retested as an arbitrarily repeatable callback. Full production duplicate/reentrant callback guarantees remain unknown.

### Test C — Original gate producer and suppression

| Test | Source and evidence boundary | Produced session+20 | Produced scene+2f8 | Result+b0 | Helper/writer count | SQL rows |
|---|---|---:|---:|---:|---:|---|
| Ordinary | Unmodified native result/context; prepared ordinary scene mode | 0 | 0 | 0 | 1 | score+clear |
| Special-source9 | After ordinary completion, supply scene+308 metadata shell with+2b8=9; original18f11c0 reads/stores it | 9 | **1** | 0 | **0** | none |
| Special-source10 | Same isolated source-field setup with10 | 10 | **1** | 0 | **0** | none |
| Expanded result | Explicitly set native-generated result+b0=1 after snapshot; no context-pointer edit | 0 | 0 | **1, supplied** | **0** | none |

The9/10 tests execute the original source-field transfer, selector/constructor, initializer producer and save gate. They do not execute those special scenes' full gameplay, completion virtuals or production entry conditions; the metadata shell is attached only after ordinary completion. The expanded case is explicitly an altered isolated gate test. Neither is presented as an unmodified ordinary play or complete special-mode lifecycle.

### Test D — Native failed classification

Run the same chart with **no input**. Native expiration/recording produces PURE0/FAR0, recorded/final LOST2/2, live/integer health0/0, score0 and **classifier0**. Chart completion atE1271 still uses ordinary end notification=false and delay4. Original deferred/context/Normal/shutter/init/save path executes with gates0/0 and stores:

```text
scores: id1, version1, score0, shining0, PURE0, FAR0, LOST2,
        date1700000000, song expedition014, difficulty2, modifier0, health0, ct0
clearTypes: id1, expedition014, difficulty2, clearType0, ct0
```

The cached result is0x414d340, native GameSession0x414de40, result scene0x414df40 and shutter0x414eac0 in this independent fixture. The native helper/writer runs once. This is a failed final classification through ordinary chart-end completion, not the distinct mid-song hard-failure notification/immediate-ending path. That latter path, mode6 timing and special delay overrides are instruction-backed prior evidence and were not newly executed here.

## Pseudocode

```python
# Original native frame/handler execute together.
def ordinary_model_frame(model, scene):
    update_native_gameplay()
    if effective_E > chart_end and not model.finished139:
        model.finished139 = True
        model.delegate40.virtual10(False)  # e2c124 -> c27d34

def c27d34(scene, failed_notification):
    scene.finished49a = True               # no entry latch check here
    native_snapshot_1600bb0(scene.model.scoreState, native_snapshot_mode(scene))
    r = scene.model.scoreState.cached68    # authoritative storage contract
    native_history_append_and_retain(r)
    native_pending_processing_1246c98(scene) # null-packet branch in014
    native_result_packet_attach_bb5640(r, scene.packet380)
    completion_services_boundary()
    e5c700(scene, failed_notification)

def e5c700(scene, failed):
    delay = choose_original_delay_and_special_addition(scene, failed)
    native_schedule_once(scene, key='endingAnimation', delay=delay,
                         callback=native_capture(scene, failed, body=native_19bbdd0))

# Original Scheduler/Timer performs timing/dispatch for all three timers.
def timer_update(timer, dt):
    if timer.elapsed == -1:
        timer.elapsed = 0
        return
    timer.elapsed = float32(timer.elapsed + dt)
    if timer.waiting_delay and timer.elapsed >= timer.delay:
        timer.native_callback_virtual10(timer.delay)
        native_repeat_and_cancellation_bookkeeping()

# 19bbdd0 and each following original body execute; UI handoff is supplied.
def ending_19bbdd0(native_capture):
    original_character_and_finish_checks()
    ui_animation_boundary(native_continuation(body=native_147dee8, scene=scene))
    # Service copies with original virtual+18; driver delivers completion.

def outro_147dee8(capture):
    native_schedule_once(scene, 'outro', 2.0, native_capture(body=native_f0b48c))

def f0b48c(capture):
    inert_widget_animation_request_boundary()
    native_schedule_once(scene, 'changescene', float32(0.3),
                         native_capture(body=native_18f11c0))

def transition_18f11c0(capture):
    r = scene.model.scoreState.cached68
    session = native_allocate_GameSession() # actual RTTI/Ref/factory code
    session.result18 = r
    native_retain(r)
    session.special20 = scene.special308.id2b8 if scene.special308 else 0
    session.flag24 = native_snapshot_mode(scene)
    result_scene = native_d11738(session)          # Normal ctor187c0c8 in ordinary fixture
    shutter = native_9ff610(result_scene)   # scoped original factory/init
    native_Director_replaceScene_9c90c0(shutter) # request; not full activation

# Driver triggers this original production callback; its action source is decoded.
def shutter_callback_963094(shutter):
    supplied_audio_resource_and_outgoing_exit_services()
    native_release(shutter.outgoing2f0)
    shutter.outgoing2f0 = None
    shutter.incoming2e8.virtual4d8()        # original callsite963118 ->891150
    native_show_incoming_scene()
    # Remaining shutter presentation work skipped in014.

def scoped_normal_initializer_891150(scene):
    original_prologue_and_base_init()
    # Explicit UI-block skips; scratch registers restored, no gate assignment.
    scene.gate2f8 = unsigned(scene.session2e8.special20 - 9) < 2
    r = scene.session2e8.result18
    if not (r.expandedB0 or scene.gate2f8):
        native_dc2c48(scene)               # caller decides; helper/writers untouched
        progression_service_boundary()
    original_epilogue()

# Original helper ->13552d4 ->12a5e60 ->bundled SQLite, as established in013.
# Equal-score preservation is a writer property, not whole-transition idempotence.
```

## Remaining synthetic dependencies

### Runtime services and exact integration boundary

- **Reusable013 runtime:** private original SQLite engine/open/schema/migrations/prepare/bind/step/column/finalize/query; same-library sqlite3 PLT resolution; memory/string primitives; aligned bump allocator/free boundary; single-threaded mutex adapters; fixed epoch time; controlled steady clock; `/dev/urandom` unavailable with original SQLite fallback. No host SQLite or host save rule. Original binary/assets remain unchanged.
- **Reference changes in014:** original121a0ec,147fe48,d6dc98 execute for valid objects. Entry observers at retain/release do not replace those instructions. The two null environment Ref calls return; autorelease10ac6e8/pool destruction and actual arena reclamation remain supplied. No full model/scene teardown claim.
- **Prepared process/scene environment:** existing native chart/model factories, GameScene/secondary delegate, Director fields, Scheduler/dispatcher, scene stack, camera/projection, selected-character/account metadata, history vector and SQLite wrapper. `0xa4227c` returns the prepared Director; `0xb688e0` returns prepared account; `0x12a1654` returns the native fixture Camera. Underlying application/account startup is not executed.
- **Logged UI/progression/audio:** `0xfa4320`, `0x1186f70`, `0xc464e4`, `0x19becc0`, gameplay notification thunks `0xb3ab3c/0xc800b0`, post-save1019c18/1049858, shutter audio9d2518 and outgoing exitd75c68. Configured but unhit alternatives are not counted as executed validation. No such adapter stores a result/context relationship, gate value or score.
- **UI continuation:** `0x1a51054` is the supplied completion-animation interface, using original function-object clone/invocation. Synthetic inert widget target **0x4000800** logs the outro request; provider lookupb99da4 and virtual20 target **0x4000810** supply the shutter resource boundary. These synthetic addresses are not library VAs.
- **Gameplay visual/provider services retained from prior fixtures:** optional107af5c, bda064,19f2e40,e2388c and RTTI/libc++/logging interfaces retain their declared bounded behavior. They do not implement judgment, snapshot, GameSession construction or persistence. Full input dispatch is intentionally not repeated.
- **No-op observation hooks:**9ff610 and9c90c0 entry logging records identities but leaves PC unchanged, so the original factory/replacement instructions execute. Generic hook-counter totals can count an observed entry twice; actual-entry traces establish the counts reported above.
- **Explicit block skips:**16a420c→16a4a4c,963130→963354,891190→89164c,891688→89219c,8921dc→8928e0. Their contents and supplied scratch registers are described above; complete results UI initialization is not claimed.

Execution uses main image0..0x2100000, arena0x4000000..0x6000000, stack/TLS through0x6100000; SP0x60df000, TPIDR_EL0=0x60f0000, return sentinel0x4000100,5M-instruction per-call budget. These addresses and service contracts, fixture inputs, original execution scopes and trace tables define the reproducible experiment without publishing temporary harnesses or databases.

Early exploratory failures were environment findings: installing the fresh runtime dependencies was necessary; connecting all native gameplay notification virtuals to an incomplete UI exposed an invalid UI read, so non-finish UI notifications became explicit boundaries. A first constructor-zero-only initializer scope omitted the actual2f8 writer; it was replaced by the final scope that executes89164c..684. Exploratory pass-through transition wrappers were replaced by original9ff610/170c208/9c90c0 execution before the final regression. Those earlier partial probes are not the final coverage claim.

### Updated coverage matrix

| Path |014 evidence | Remaining boundary |
|---|---|---|
| Model end → real scene delegate → completion/snapshot | **Native-integrated** | prepared scene/services/history |
| Ending registration → original Scheduler/Timer → finish callback | **Native-integrated** | dt controlled; no complete Director/Android scheduling |
| Finish callback → UI completion continuation | Native body/clone executed; environment handoff supplied | animation/assets/completion timing omitted |
| Outro/change timers → GameSession construction → result-scene selection | **Native-integrated** | inert outro widget; source scene/config prepared |
| GameSession owns native cached result | **Native-integrated**, exact identity/retain arithmetic | autorelease reclamation unexecuted |
| Normal ctor → scoped shutter ctor → Director replacement request | **Native-integrated scoped** | shutter UI/state blocks omitted; full activation absent |
| Shutter onEnter/CallFunc construction and action-driven963094 invocation | **Instruction-backed** | callback driver-triggered in regression |
| Original963094 → result initializer producer/gate → save helper/SQLite | **Native-integrated scoped** | explicit initializer/UI/suffix skips |
| Failed classification → ordinary result scene/local row | **Native-integrated scoped** | ordinary chart-end failure category; not mid-song hard-failure path |
| Duplicate handling | Native model/timer guards plus isolated forced calls | no universal production reentrancy guarantee |
| Populated pending completion packet/network | **Unexecuted** | null-packet native branch only; optional extension not pursued |

## Unresolved Mysteries

1. Full TransitionShutter onEnter/action sequencing, final Director activation/current-scene update, UI animation assets and screen completion. Original production callback provenance is established, but its action-driven invocation remains the principal presentation boundary.
2. Remaining891150 UI/progression sections, all their side effects and flags, and full shutter initialization. The executed2f8 producer is specific and reliable; scoped initializer success is not full screen success.
3. Actual startup/history initialization and final ownership/autorelease reclamation. Reference counts here establish native transfers under the supplied pool/allocator, not complete production destruction.
4. Full entry conditions and semantics of special-scene IDs9/10, other result variants, early quit/retry, mode6 delay and mid-song hard-failure immediate ending. No ordinary-gauge or submission-policy equivalence is invented from the special integer.
5. Meaningfully populated scene+380 completion packets, serialization/enqueue ownership and consumer scheduling.014 executes only the native missing-packet branch and makes no networking claim.
6. All real account/resource/audio/render services, on-disk persistence and concurrency.013's ct meaning remains unresolved. Flick remains gameplay-unproven and outside scope.

## GitHub Status

Authorized changes are this new report and an append-only014 context entry, based on **`96a1a1f039d64cf34d98c85d92e1ea4c5cba8541`**. Reports001–013, historical context, README, instructions and original archive/assets/binary are preserved. Harnesses, traces and SQLite state are not commit contents. Before publishing, recheck main and absence of an existing014 report; update the ref with the expected starting SHA. After publishing, read both files pinned to the new commit, compare exact content and historical context prefix, and compare trees against the starting commit. The headquarters return records the resulting exact SHA and document links; no future self-referential commit hash is invented here. Expedition015 is not initiated.
