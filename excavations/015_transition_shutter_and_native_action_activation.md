# Expedition 015 — TransitionShutter Activation, Native Actions & Results-Scene Lifecycle

## Result

**Strong success, with a scoped Director-driven activation and a bounded native cleanup test.** Original TransitionShutter actions now invoke `0x963094` through the original Scheduler, ActionManager, Sequence, CallFunc and bound-function invoker. That callback enters the original incoming results initializer, whose original gate invokes native saving and the bundled SQLite engine. The successful regression never directly calls `0x963094`, constructs a GameSession, installs its GameResult, assigns the save gate, or calls the save helper from the driver.

A scoped original Director frame consumes the pending shutter and dispatches its original `onEnter`. This adds Director lifecycle integration beyond the central action objective. It is not a complete rendered frame or complete visual transition: graphics work is bounded, panel artwork is supplied as inert native Nodes, and the existing results-UI and callback-suffix omissions remain explicit below. The earlier ending-animation completion service at `0x1a51054` also remains supplied.

Ordinary native gameplay again produces PURE2, FAR0, LOST0, score **10,000,002**, live health **80.4000015258789**, integer result health **80**, clear type **3**. Action-driven results activation saves those values. A separate native no-hit run saves score0, LOST2, health0, clear type0 through the same path. Original panel cleanup before the CallFunc removes its Sequence and prevents initialization/saving in that controlled test.

## What I Found

### Source identity and evidence categories

Starting `main`: **`2cad15d5e146ae7d97ec0282d9472bc9266aa46f`**. Expedition015 was absent at the initial repository inspection. The project introduction, supplied archive, current cumulative context, complete Expedition014 report, and relevant009/011/013 scheduling and persistence evidence were consulted. Existing local research modules were inspected and reused; their presence is not treated as evidence that inaccessible earlier conversations were recovered.

The archive contains 9,658 entries. The primary `lib/arm64-v8a/libcocos2dcpp.so` was checked against the ZIP member and extracted ELF:

- SHA-256: `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.
- Build ID: `17d660edbf37ca78beefc32e07672c97419ddce6`.
- All code/vtable addresses below are main-library ELF virtual addresses before relocation. Heap addresses identify this deterministic controlled run and are not application constants.

**Native-integrated** means original routines executed together within the stated scope, including disclosed service hooks and skipped blocks. **Native-isolated** means original code executed with its surrounding interface supplied. **Instruction-backed** denotes decoded binary relationships without execution of the enclosing path. **Interpretation** and **Unknown** retain their earlier meanings. No Java/Android VM, GPU, real audio, account, network or leaderboard operation executed.

### Original Director scene-activation path

The existing native ending chain was reused rather than reconstructed wholesale:

| Connection | Evidence in this expedition |
|---|---|
| Model frame `0x10a7550` → completion delegate → `0xc27d34` → snapshot `0x1600bb0` | Native-integrated; cached result read from ScoreState`+0x68` |
| Completion setup `0xe5c700` → Scheduler timers → `0x19bbdd0` | Native-integrated |
| UI service `0x1a51054` → original continuation `0x147dee8` | Supplied animation completion; original function-object clone and continuation body execute |
| Subsequent Scheduler timers → `0xf0b48c` → `0x18f11c0` | Native-integrated |
| Transition closure → native GameSession → selector `0xd11738` → constructor `0x187c0c8` | Native-integrated; no driver-made result/context relationship |
| Factory `0x9ff610` → initializer `0x16a41c4` / base `0x170c208` → replacement `0x9c90c0` | Native-integrated with panel-resource boundary |
| Director frame `0x1793f8c` → pending consumer `0xd0dc14` → shutter `onEnter` `0x12157ec` | Newly native-integrated, within the frame segment below |

The prepared Director starts with a one-entry scene stack (vector beginning at`+0x158`, end at`+0x160`) containing the old GameScene. Instruction-backed stack behavior in executed replacement`0x9c90c0` is explicit: `0x9c9124` reads the vector, `0x9c9138` releases the prior tail, `0x9c9148` writes the shutter into that same tail slot, `0x9c914c` retains it, and `0x9c9150` stores pending. This path replaces the tail rather than pushing a second scene. The final regressions separately read running/pending/ownership state; they do not include a separate serialized stack dump.

The frame starts at its original entry. Controlled `gettimeofday` supplies its time input; the original prologue, time calculation, null GL polling branch, before-update notification, Scheduler update and after-update notification execute. The two notifications are native custom events, **not Android queue drains**. Only the graphics flush at `0x1794004–0x179400c` is skipped to `0x1794010`. The original pending-scene check and call at `0x179401c` execute. Execution stops at `0x1794020`, before matrix/render traversal. Consequently the later Director frame-counter increment and drawing are outside this experiment.

`0xd0dc14` uses RTTI casts to distinguish outgoing/incoming TransitionScene state. The supplied C++ runtime cast adapter follows the ELF RTTI hierarchy; it is not execution of the original C++ runtime. For old ordinary GameScene → new TransitionShutter, the consumer:

1. Recognizes the pending scene as a transition and avoids the generic immediate old-scene exit block.
2. Releases the Director's old running reference at `0xd0dcd8`.
3. Copies pending`+0x148` into running`+0x140`, retains it, then clears pending.
4. Since the outgoing scene was not a TransitionScene, calls the new scene's virtual`+0x300` at `0xd0dd18`: actual target `0x12157ec`.
5. Dispatches new virtual`+0x308` through `0xd0dd34` for the inherited enter-transition-finished notification.

Observed ordinary pointers:

| State | Before activation | After activation | After action callback |
|---|---|---|---|
| Director running `+0x140` | old GameScene `0x4102400` | shutter `0x4150c80` | shutter `0x4150c80` |
| Director pending `+0x148` | `0x4150c80` | null | null |
| Shutter incoming `+0x2e8` | result scene `0x4150100` | same | same |
| Shutter outgoing `+0x2f0` | `0x4102400` | same | null |
| Shutter / left / right Node running byte`+0x1c0` | 0 / 0 / 0 | 1 / 1 / 1 | 1 / 1 / 1 |
| Incoming running / visible (`+0x1c0/+0x1c1`) | 0 / 1 | 1 / 0 | 1 / 1 |
| Outgoing running | 1 | 1 | 0 |

Shutter vtable is **`0x1af1868`**; incoming NormalGameResultScene vtable is **`0x1afe2a0`**. There was one original Director consumer entry and one shutter `onEnter` entry.

Original transition-base enter `0x1767a88` first calls Node enter `0x1597d14`, disables its EventDispatcher via `0x925c68`, dispatches outgoing virtual`+0x318`, then incoming virtual`+0x300`. The actual incoming dispatch is inherited Node enter, not the later results initializer. Original Node enter resumes scheduler/action/listener participation. Original child addition later makes both supplied panel Nodes running.

The callback's outgoing virtual`+0x310` reaches original Node exit **`0xd75c68`**, now executed instead of014's inert exit service. It pauses native Node participation and clears outgoing running`+0x1c0`. This fixture has no populated visual child tree; an extra harness root reference prevents complete old-scene destruction. This is not a GameScene destructor test.

### TransitionShutter onEnter and native action construction

The factory's original initializer prefix now executes through `0x16a4234`, producing the native flags including `+0x358=0`. Resource construction is bounded at `0x16a4238`; two original-constructed plain Nodes are supplied at `+0x300/+0x308`, then original initialization resumes at `0x16a48d8`. Its scaling, anchor, positioning and retain operations execute. A 1280×720 environment and inert panel-width interface value100 produce initial positions left **(-100,720)** and right **(1380,720)**. Real Sprite textures/art are not created.

`onEnter` executes its base call at `0x1215818`. The loading-overlay creation/addition block `0x121581c–0x1215848` is skipped to `0x121584c`. The subsequent ordinary action code executes without replacement:

| Original operation | Address / callsite |
|---|---|
| Left MoveTo, duration0.75f | `0x1215994–0x121599c` → `0xf6ae00` |
| Wrap in EaseCubicActionOut | `0x12159a0` → `0x8c9d24` |
| Build bound shutter/method function object | `0x12159b8–0x12159d4` |
| Construct CallFunc | `0x12159dc` → `0x10de878` |
| Combine left movement and CallFunc | `0x12159f0` → `0x14be12c` |
| Left virtual runAction | `0x1215b64` → `0xc7820c` → `0xb3dc38` |
| Right MoveTo / cubic easing | `0x1215b98/0x1215b9c` → same factories |
| Right virtual runAction | `0x1215bb0` → same native registration |

The actual tree is **Sequence(EaseCubicActionOut(MoveTo), CallFunc)** on the left panel and **EaseCubicActionOut(MoveTo)** on the right. There is **no DelayTime in this ordinary subtree**. The callback waits for the movement's duration through Sequence semantics. `+0x358 != 0` branches, including additional scheduled behavior, were decoded but not exercised; do not generalize this tree to them.

| Native object | Ordinary pointer | Vtable | Relevant fields |
|---|---|---|---|
| Left Node | `0x414d940` | `0x1b4d3e8` | Actual original Node constructor `0x131419c` |
| Left Sequence | `0x4151580` | `0x1aa5508` | duration`+0x30=.75`; children`+0x40/+0x48`; split`+0x50=1`; last`+0x54=-1` initially |
| Left EaseCubicActionOut | `0x4151480` | `0x1aae190` | inner action`+0x40` |
| Left MoveTo | `0x4151400` | `0x1aaa160` | endpoint`+0x60=(0,720)` |
| CallFunc | `0x4151500` | `0x1acbd78` | duration0; active function pointer`+0x70` |
| Right Node | `0x414df40` | `0x1b4d3e8` | Original Node, inert panel art |
| Right Ease / MoveTo | `0x41519c0 / 0x4151940` | same respective vtables | endpoint `(1280,720)` |

The CallFunc owns an inline function object at **`0x4151550`** (CallFunc`+0x50`), with vtable **`0x1b1bec0`**, active pointer at CallFunc`+0x70`. RTTI identifies the libc++ `__function::__func<__bind<void(TransitionShutter::*)(),TransitionShutter*>,…>` specialization. Its fields are:

| Offset from function object | Observed value |
|---|---|
| `+0x00` | vtable `0x1b1bec0` |
| `+0x08` | method `0x963094` |
| `+0x10` | member-pointer adjustment0 |
| `+0x18` | captured `this = 0x4150c80`, the actual native-created shutter |

Original function-object construction/copy occurs inside native CallFunc creation. The stack temporary is destroyed normally; the action's captured function remains valid. No host timer or Python callback dispatches the shutter method.

### Scheduler and ActionManager execution

Original Scheduler registration `0xdb9674` registers the native ActionManager wrapper (function vtable`0x1b37d48`, capture manager at`+8`) at priority **INT_MIN**, unpaused. Director/Scheduler/ActionManager objects use original constructors with supplied singleton/environment links. The prepared Camera's Scheduler`+0x1a8` and dispatcher`+0x1b8` links are supplied because it was constructed before those services existed in this fixture.

The executed action invocation chain is:

```text
Scheduler.update 0x13d3f44
  → registered native wrapper 0xd630b8
  → ActionManager.update 0x9effe0
  → ActionInterval.step 0x12a5a80
  → Sequence.update 0x189cba0
  → CallFunc.update 0x130cb2c
  → CallFunc.execute 0x1935ccc
  → bound function invoker 0x1188cbc
  → TransitionShutter callback 0x963094
```

ActionManager calls action step virtual`+0x40` at `0x9f00b0`, tests done virtual`+0x28` at `0x9f00cc`, stops virtual`+0x38` at `0x9f00e4` and removes through `0x1869c50` at `0x9f00f8`. Sequence dispatches the child update at `0x189ccf0`. CallFunc update tail-dispatches execute virtual`+0x50`; execute reads the active function pointer and dispatches function virtual`+0x30`. Invoker `0x1188cbc` loads the captured member pointer, adjustment and shutter pointer, then branches to `0x963094`. The observed callback return address can therefore be `0x189ccf4` across these tail calls; the intermediate native invokers also executed once.

ActionInterval's first step clears its first-tick flag`+0x38` and resets elapsed`+0x34` to0 rather than consuming that tick's dt. Later steps add float32 dt, divide by duration and clamp for update. The test explicitly primes with dt0. Ease update `0x150d8d0` calls cubic-out `0xf0b7e0`, then native MoveTo update `0x8e2b70`. The original scalar order is `u=float32(t-1); q=float32(u*u); r=float32(u*q); eased=float32(r+1)`. Observed positions come from ARM64 execution, not a host approximation.

#### Normal completion / insufficient time / additional updates

After native Director activation, the driver advances original Scheduler with `[0, .25, .25, .25, .001, 1, 5]` seconds:

| Action elapsed after priming | Left X | Right X | `0x963094` entries | Score-writer entries | Active target entries |
|---|---:|---:|---:|---:|---:|
| 0 | -100 | 1380 | 0 | 0 | 2 |
| .25 | -29.629623413085938 | 1309.629638671875 | 0 | 0 | 2 |
| .50 | -3.703704833984375 | 1283.7037353515625 | 0 | 0 | 2 |
| .75 | 0 | 1280 | 1 | 1 | 0 |
| .751 | 0 | 1280 | 1 | 1 | 0 |
| 1.751 | 0 | 1280 | 1 | 1 | 0 |
| 6.751 | 0 | 1280 | 1 | 1 | 0 |

Each ordinary test has one entry to CallFunc update, execute, bound invoker, shutter callback, result initializer, ordinary helper and each writer. Both native action target entries disappear. Additional updates do not repeat the callback or saving. This proves one-shot behavior for these registered instances; it does not prove that arbitrary re-entry into `onEnter` cannot create new actions.

The controlled monotonic value progresses from7571 to14322ms during this stage. Completed GameTimeline E and last model-frame effective time remain **1271ms**. Scheduler action time, gameplay effective time and persisted epoch date are separate observations.

### Original callback, results initialization and SQLite regression

Pointer continuity is checked before and after actions:

```text
ScoreState+0x68 = GameResult 0x414f580
GameSession 0x4150000 +0x18 = that same GameResult
NormalGameResultScene 0x4150100 +0x2e8 = that GameSession
TransitionShutter 0x4150c80 +0x2e8 = that results scene
CallFunc capture+0x18 = that TransitionShutter
```

The native closure constructs these relationships; the driver only observes them. The snapshot routine's return X0 is not used as a result pointer.

Callback `0x963094` dispatches outgoing exit, releases outgoing, clears shutter`+0x2f0`, and dispatches incoming virtual`+0x4d8` to **`0x891150`**. Original save-gate producer `0x89164c–0x891684` reads GameSession`+0x20`; its ordinary value0 produces scene`+0x2f8=0`. The actual predicate is unsigned `(contextValue-9)<2`, so values9/10 set the gate; this is not a runtime-gauge equality test. Original eligibility code `0x89219c–0x8921dc` ORs this gate with GameResult`+0xb0`. Both are naturally0 in these ordinary fixtures. Original callsite **`0x8921b8`** invokes **`0xdc2c48`**, followed by original writer **`0x13552d4`** and clear writer **`0x12a5e60`**. The initializer skips are enumerated below; their boundaries do not supply those predicates or replace their callsites.

A fresh private `:memory:` database uses the bundled original ARM64 SQLite exports, native statements/bindings/step/finalize and native schema strings reused from013. Host services supply libc allocation, strings, time and synchronization, not SQL decisions or a host database. Before action completion the queried scores table is empty. Native writer SQL includes:

```sql
SELECT id, score FROM scores WHERE songId = "expedition015"
 AND songDifficulty = "2" AND ct = "0";
INSERT INTO scores (version, score,shinyPerfectCount, perfectCount,
 nearCount, missCount, date, songId, songDifficulty, modifier, health, ct)
 VALUES (?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13);
INSERT INTO clearTypes (songId, songDifficulty, clearType, ct)
 VALUES (?2, ?3, ?4, ?5);
```

For ordinary score insert, actual bound values at indices2–13 are respectively `[1,10000002,2,2,0,0,1700000000,"expedition015",2,0,80,0]`. Clear bindings2–5 are `["expedition015",2,3,0]`. Original SELECT/INSERT prepare callsites include `0x13554ec/0x1355810` and clear insert prepare `0x12a636c`; native step callsites include `0x1355960/0x12a6404`.

Readback through original SQLite prepare/step/column routines:

| Stored field | Ordinary two-PURE run | Native no-hit run |
|---|---:|---:|
| id / version | 1 / 1 | 1 / 1 |
| score | 10000002 | 0 |
| shinyPerfectCount / perfectCount | 2 / 2 | 0 / 0 |
| nearCount / missCount | 0 / 0 | 0 / 2 |
| date | 1700000000 | 1700000000 |
| songId / songDifficulty | expedition015 / 2 | expedition015 / 2 |
| modifier / health / ct | 0 / 80 / 0 | 0 / 0 / 0 |
| separate clearTypes.clearType | 3 | 0 |

These are separate fresh databases. The no-hit result is produced by native frames without judgments, not manually fabricated result fields. It has result `0x414ee80`, GameSession`0x414f900`, incoming scene`0x414fa00`, shutter`0x4150580`; its own action capture points to that shutter. It also invokes callback/initializer/helper/writers once. This is ordinary chart-end failure classification, not a reconstruction of every early hard-failure scene path. No network submission occurred; unchanged records after later updates are supported by the observed absence of another save call, rather than by relying on equal-score rejection.

### Reference ownership and callback lifetime

Valid-object Ref initialization/retain/release instructions execute. Null environment references are explicitly inert. The harness adds one root retain to the old GameScene to avoid expanding into complete scene destruction.

| Refcount / field | Pending | Activated | After successful callback |
|---|---:|---:|---:|
| Old GameScene Ref | 3 | 2 | 1 (harness root) |
| Shutter Ref | 2 | 3 | 3 |
| Cached GameResult Ref | 4 | 4 | 5 |
| GameSession Ref | 2 | 2 | 2 |
| Left Sequence / right Ease Ref | not yet created | 2 / 2 | 1 / 1 |

Native saving's retained result/cache relationship accounts for the additional observed result reference; no result replacement was observed. ActionManager release removes its root-action references. Autorelease pools are not drained and allocator frees are supplied as inert services, so Ref1 is not proof of object deletion or a leak. Original base action stop `0x1888934` clears action`+0x20`; `+0x18` remains the original target pointer in these observations. The binder captures a plain shutter pointer; its construction does not itself establish an extra shutter retain. Director ownership keeps this shutter valid throughout the tested action lifetime.

### Repeated and canceled action behavior

In a separate two-PURE fixture, after action elapsed.5 the driver calls the left panel's **original cleanup virtual`+0x320 = 0x7dbebc`**. Original cleanup reaches ActionManager removal **`0xf14f9c`**. The Sequence is removed from the manager, its Ref falls2→1, and left X stays **-3.703704833984375**. The independent right Ease completes to1280. Additional identical updates produce:

- callback0, incoming initializer0, ordinary helper0, score writer0;
- scores/clearTypes both empty;
- action target list empty after the right action finishes;
- incoming still hidden and outgoing pointer still retained by the shutter.

Removal is real native cleanup and native manager mutation, not a driver edit to an action array. It is a **harness-requested original Node cleanup test**, not proof that every production scene replacement/background transition issues that cleanup at this point. Unlike normal completion stop, the removed Sequence retains its target field in this test; do not infer that removal calls stop or clears all child targets. Complete interrupted-transition recovery and re-enabling input remain unknown.

## Native validation setup and boundaries

### Reproducible fixture and executed scope

ARM64 execution used Unicorn2.1.4; Capstone5.0.9 decoded instructions; pyelftools0.33 read ELF segments, relocations and RTTI. No binary bytes were patched; instruction-block skips redirect the emulator PC at the listed boundaries. Existing native constructors, prepared chart/model geometry, score/gauge and two-tap fixture were reused. Chart notes are at1000/1150ms, judgment inputs use prepared Touch objects at those times, and model frame E1271 reaches ordinary completion. This expedition does not claim to execute AFF loading or JNI dispatch anew.

After completion, native Scheduler inputs `[0,4]` deliver the ending timer. The UI service clones the original completion function using its native clone virtual and the driver delivers that original continuation once. Scheduler `[0,2,.3]` then reaches the native scene-transition closure. The new scoped Director frame activates the pending shutter. The action Scheduler sequence and readback follow the table above. Three fresh processes independently completed ordinary, no-hit and cleanup-before-callback regressions; all assertions passed.

### Explicit control-flow and environmental inventory

| Boundary / service | Supplied behavior and limit |
|---|---|
| `0x16a4238 → 0x16a48d8` | Supply original-constructed plain Node panels at shutter`+0x300/+0x308`; art/texture/widget construction omitted; native initializer prefix and positioning suffix execute |
| `0x121581c → 0x121584c` | Omit loading-overlay factory, opacity and child-add block; base enter and all ordinary movement/CallFunc code execute |
| `0x1794004 → 0x1794010`; stop`0x1794020` | Omit graphics flush and later render/matrix/frame-finalization work; original pending consumer executes |
| `0x891190 → 0x89164c` | Omit first results-UI block; restore X28=application-global address and X26=X29−0x60 for original gate-producing instructions |
| `0x891688 → 0x89219c` | Omit middle results UI/layout/progression block; preserve native gate producer and later save branch |
| `0x8921dc → 0x8928e0` | Omit post-save results-UI block; original epilogue executes |
| `0x963130 → 0x963354` | Omit post-initialization shutter closing/final-transition setup; callback entry, outgoing exit/release, incoming initialization and visibility work execute |
| `0x1a51054` | Earlier ending UI animation-completion service; native function clone, driver-delivered original `0x147dee8` continuation; still synthetic |
| `0xa4227c`, `0xf09110`, `0x12a1654` | Director singleton, 1280×720 size, prepared default Camera services |
| `0xb688e0`, `0xb99da4`; synthetic virtuals`0x4000800/0x4000810/0x4000820` | Prepared account/provider/widget/input-control interfaces; log/inert return; no external state or audiovisual output |
| `0xfa4320`, `0x1186f70`, `0xc464e4`, `0x19becc0`, `0xe2388c` | Completion-side ancillary services inert; do not claim populated pending-submission integration |
| `0xc800b0`, `0x107af5c`, `0x9c8190`, `0x9d2518`, `0x1019c18`, `0x1049858` | Scoped application/UI/audio/progression side services logged/inert; no replacement of action callback or save branch |
| `0xbda064`, `0x10ac6e8`, `0x19f2e40` | Existing Node/runtime/pool-support boundaries; full platform startup, autorelease reclamation and graphics environment not reconstructed |
| `0x147fe48`, `0xd6dc98` | Observed original retain/release for valid objects; null environment requests return without dereference |
| SQLite imported calls | Resolved to original bundled exports, with observers; not host SQL |

Factory`0x9ff610` and replacement`0x9c90c0` have entry observers that leave PC unchanged. Shutter callback, action factories, runAction, insertion, Scheduler, ActionManager, Sequence/CallFunc updates, outgoing Node exit, gate producer/branch and writers are not substituted.

The inherited runtime also supplies allocation/copy/zero/string operations, integer formatting, RTTI cast, native-clock/epoch-time inputs, errno/process/randomness interfaces and inert single-thread mutexes. All are environment services, not original libc execution. `/dev/urandom` open fails deliberately into SQLite's native fallback; there is no application-file access. Original schema and in-memory SQLite storage execute. The hook inventory below records visited imported boundaries for the ordinary regression; no exception/malformed-input behavior is claimed.

### Visited imported-service inventory

Addresses are PLT boundaries. Counts are hook encounters in the ordinary process, including preparation, schema initialization and readback; they are not action callback counts. SQLite-import observers redirect into bundled exports separately.

| Address | Imported service | Encounters |
|---|---|---:|
| `0x1a6d9c0` | `_Znwm` | 71 |
| `0x1a6d9d0` | `memcpy` | 1059 |
| `0x1a6d9e0` | `_ZdlPv` | 14 |
| `0x1a6e6e0` | `pthread_mutex_lock` | 1511 |
| `0x1a6df10` | `malloc` | 686 |
| `0x1a6e700` | `pthread_mutex_unlock` | 1511 |
| `0x1a6e690` | `pthread_mutexattr_init` | 2 |
| `0x1a6e6a0` | `pthread_mutexattr_settype` | 2 |
| `0x1a6e6b0` | `pthread_mutex_init` | 2 |
| `0x1a6e6c0` | `pthread_mutexattr_destroy` | 2 |
| `0x1a6dad0` | `strlen` | 465 |
| `0x1a6ded0` | `free` | 584 |
| `0x1a6e6d0` | `pthread_mutex_destroy` | 1 |
| `0x1a6db30` | `memset` | 249 |
| `0x1a6e100` | `strcmp` | 31 |
| `0x1a6df00` | `realloc` | 47 |
| `0x1a6e520` | `getpid` | 1 |
| `0x1a6e720` | `open` | 1 |
| `0x1a6e540` | `__errno` | 1 |
| `0x1a6de50` | `time` | 2 |
| `0x1a6daf0` | `memmove` | 18 |
| `0x1a6da80` | `memcmp` | 34 |
| `0x1a6dc60` | `_ZNSt6__ndk16chrono12steady_clock3nowEv` | 6 |
| `0x1a6e090` | `_Znam` | 6 |
| `0x1a6db90` | `__dynamic_cast` | 41 |
| `0x1a6e0a0` | `_ZdaPv` | 6 |
| `0x1a6dd40` | `_ZnwmRKSt9nothrow_t` | 13 |
| `0x1a6ee10` | `calloc` | 9 |
| `0x1a6dbe0` | `_ZNSt6__ndk16chrono12system_clock3nowEv` | 2 |
| `0x1a6da50` | `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEC1ERKS5_` | 16 |
| `0x1a6db80` | `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_` | 10 |
| `0x1a6e5c0` | `gettimeofday` | 1 |
| `0x1a6dc00` | `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc` | 1 |
| `0x1a6db20` | `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc` | 20 |
| `0x1a6db60` | `_ZNSt6__ndk19to_stringEi` | 4 |
| `0x1a6db00` | `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm` | 4 |
| `0x1a6dc50` | `__strlen_chk` | 6 |
| `0x1a6dc10` | `_ZNSt6__ndk1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_` | 1 |

## Pseudocode

The pseudocode describes executed ordinary branches, with omissions marked explicitly. Float expressions denote native float32 order.

```cpp
// Original ending chain; earlier animation completion remains supplied.
modelFrame(E = 1271):
    if ordinaryCompletion:
        GameScene_completion();        // c27d34
        // Native snapshot stores authoritative pointer in ScoreState+68.
        scheduleOriginalEndingCallbacks();
// Scheduler invokes 19bbdd0; supplied UI animation service delivers native
// continuation147dee8; Scheduler then invokes f0b48c and18f11c0.
transitionClosure():
    session = nativeGameSession(cachedResult, selectedSceneValue);
    incoming = nativeResultSceneFactory(session);
    shutter = nativeTransitionShutter(incoming, .75f);
    director.replaceScene(shutter);     // running unchanged; pending=shutter

// Original Director frame segment, with graphics omitted after updates.
directorFrameSegment():
    calculateDt();
    if !director.paused:
        dispatch(beforeUpdate);
        scheduler.update(dt);
        dispatch(afterUpdate);
    // supplied graphics boundary
    if director.pending:
        consumePending();
    // stop before matrix/render/finalization

consumePending():                         // d0dc14, ordinary -> transition
    oldWasTransition = rttiCast(old, TransitionScene) != nullptr;
    if pendingIsTransition:
        // old exit deferred to transition lifecycle
    release(oldRunning);
    running = retain(pending);
    pending = nullptr;
    if running && !oldWasTransition:
        running.virtual_onEnter();         // 12157ec
        running.virtual_enterFinished();

TransitionShutter.onEnter():
    TransitionScene.onEnter();             // original Node enter + lifecycle
    // loading-overlay block omitted
    addChild(rightPanel); addChild(leftPanel);
    incoming.setVisible(false);
    // ordinary native +358==0 branch
    left.runAction(Sequence(
        EaseCubicActionOut(MoveTo(.75f, leftEndpoint)),
        CallFunc(bind(&TransitionShutter::activateIncoming, this))));
    right.runAction(EaseCubicActionOut(MoveTo(.75f, rightEndpoint)));

scheduler.update(dt):
    nativeActionManagerWrapper(dt);
ActionInterval.step(dt):
    if firstTick: firstTick=false; elapsed=0;
    else: elapsed=float32(elapsed+dt);
    update(clamp(float32(elapsed/duration)));
Sequence.update(t):
    // Native split=1; when movement finishes, start/update instant CallFunc.
    updateNativeChildren(t);
CallFunc.execute():
    activeFunction.virtual_call();          // 1188cbc -> captured963094

TransitionShutter.activateIncoming():       // 963094, ActionManager-driven
    outgoing.virtual_onExit();              // original d75c68
    release(outgoing);
    outgoing = nullptr;
    incoming.virtual_initializeResults();   // 891150, UI blocks omitted
    incoming.setVisible(true);
    // closing/final-transition block omitted

NormalGameResultScene.initializeResults():
    // omitted UI prefix
    saveGate = unsigned(session.selectedSceneValue - 9) < 2;
    // omitted UI middle
    if !(saveGate | session.result.byte_b0):
        ordinarySaveHelper(this);           // dc2c48, native writers/SQLite
    // omitted UI suffix

// Separate controlled cancellation test, requested by driver at elapsed .5.
leftPanel.cleanup():                        // original 7dbebc
    nativeActionManager.removeAllActionsForTarget(leftPanel); // f14f9c
    // removed Sequence no longer updates; captured activation never runs
```

## Remaining synthetic dependencies and updated coverage

| Interface | Coverage after015 |
|---|---|
| Native gameplay → cached GameResult | Native-integrated again with prepared chart/model/Touch inputs |
| Cached result → GameSession → ordinary result scene → shutter request | Native-integrated; earlier UI continuation completion supplied |
| Director pending replacement → shutter onEnter | Newly native-integrated within original frame segment; RTTI/runtime services supplied |
| Ordinary shutter movement / Sequence / CallFunc construction | Newly native-integrated on inert native panel Nodes |
| Scheduler → ActionManager → captured `0x963094` | Newly native-integrated; no driver callback invocation |
| Outgoing original Node exit / release | Newly native-integrated in prepared scene; complete destruction excluded |
| Native callback → result initializer → gate → helper → bundled SQLite | Native-integrated with exact UI skips above |
| Callback repetition after action completion | Native-integrated negative observation over additional updates |
| Original Node cleanup removes pending Sequence | Native-isolated request joined to active native manager; no later callback/save |
| Final shutter closing, incoming Director replacement, input re-enable | Unknown in execution; callback suffix omitted |
| Complete rendered frame / real artwork / Android GL queue | Unexecuted |
| Earlier `0x1a51054` animation completion | Supplied; optional investigation deliberately deferred |

At the end of the successful regression, Director still runs the shutter and dispatcher enabled byte`+0x124` is0. Incoming is running/visible, but this is **not proof of a visually complete, input-enabled results screen**. The precise remaining activation work lies beyond the omitted callback suffix and UI resources. The central dependency removed is the manual shutter callback trigger, not all presentation boundaries.

## Unresolved Mysteries

- Execute closing/final-transition actions and final Director replacement/input re-enable without the `0x963130` boundary.
- Replace inert panel artwork and loading overlay with original resource-backed objects without expanding into the renderer.
- Establish production scene-interruption callers and recovery after a pending activation Sequence is removed. Controlled cleanup proves suppression, not a universal scene policy.
- Test deliberate repeated `onEnter` or scene re-entry separately; one-shot completion applies to the observed action instances.
- Drain original autorelease pools and trace complete destruction only in a dedicated ownership scope; current Ref arithmetic does not establish full reclamation.
- The earlier UI continuation's original animation remains unexecuted. No optional packet/network or FlickNote work was undertaken.

## GitHub Status

Prepared against `main` **`2cad15d5e146ae7d97ec0282d9472bc9266aa46f`**. Publication is restricted to this report and one appended Expedition015 entry in `context.md`. No harness, trace, database, binary, asset, README or historical report is authorized for inclusion. The publication commit is the commit containing this report; its exact SHA and pinned document links are returned in the headquarters handoff, avoiding an impossible self-referential commit hash inside its own contents.

Publication verification compares the committed files byte-for-byte with the prepared UTF-8 strings, checks that starting context is an exact prefix, and compares every pre-existing non-context blob with the starting tree. Branch update uses an expected-head lease after checking for concurrent015 publication.
