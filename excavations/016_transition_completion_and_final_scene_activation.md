# Expedition 016 — TransitionShutter Completion, Final Scene Activation & Input Restoration

## Result

**Strong success, plus a bounded event-delivery probe.** The successful regression removes015's `0x963130 → 0x963354` bypass. The original ordinary callback suffix, additional Scheduler timers, reveal-action construction, both closing/reveal CallFuncs, selector timer, Director replacement and Director lifecycle consumption now execute. Director ends on **NormalGameResultScene**, pending is null, its scene-stack tail contains that result scene, and original transition exit restores EventDispatcher enabled state.

The native-generated GameResult remains the same object through GameSession, results scene, shutter, save helper and bundled SQLite. Two-PURE and no-hit runs both complete the new transition; their original results initialization and save operation occur once. Additional Scheduler updates and scoped Director frames do not repeat the callbacks or change the saved rows.

A prepared native EventListenerCustom associated with the incoming result scene receives a harmless custom event through the original dispatcher only after restoration. Its observation sink/function-object services are supplied. This establishes delivery to that registered listener, **not an actual results-screen button or complete touch-enabled visual UI**.

Full Android/GPU execution, panel artwork, most results UI, earlier ending-animation completion and final memory reclamation remain outside scope. A newly exposed result-enter character/audio feedback interface is explicitly bounded. There is no new bypass inside the ordinary shutter suffix, reveal-action builders, finish callback, selector or transition lifecycle methods.

## What I Found

### Preparation, source identity and evidence labels

Starting `main`: **`6381de72c7858d11ce5416cbfda14150a1ed7bef`**. Repository inspection found no016 publication. The project introduction and supplied ZIP were read/inspected; current cumulative context and complete015 report were fetched at that commit, with relevant014/013/012/009 completion, persistence, lifecycle and scheduling evidence consulted. Existing local fixture modules were available, inspected and reused; this does not imply recovery of an inaccessible prior conversation or emulator state. New processes prepared their own native objects and databases.

ZIP entries:9,658. Both the original ZIP member and extracted `lib/arm64-v8a/libcocos2dcpp.so` hash to **`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`**. ELF Build ID: **`17d660edbf37ca78beefc32e07672c97419ddce6`**. Addresses below are unrelocated main-library ELF virtual addresses; heap pointers are fixture identities, not production constants.

**Native-integrated:** original ARM64 routines execute together within declared boundaries. **Native-isolated:** original routine executes with enclosing interfaces supplied. **Instruction-backed:** original decoded code establishes behavior without execution of the enclosing branch. **Interpretation:** grounded explanation. **Unknown:** unverified producer/consumer or behavior. Routine names are descriptive research labels unless established by RTTI or imported symbols.

### Recovered shutter callback suffix

The entire normal body `0x963094–0x963378` was decoded. Its existing prefix exits/releases the outgoing scene, initializes the incoming result scene through virtual`+0x4d8`, and makes it visible. The removed bypass starts immediately after that visibility call.

| Original block | Recovered behavior | Evidence |
|---|---|---|
| `0x963130–0x963210` | If shutter`+0x399` is nonzero, create/configure `img/white.png` overlay at`+0x3a0`, scale/place/color it and add it above the scene | Instruction-backed alternative; ordinary native initializer writes399=0 |
| `0x963214–0x963250` | Measure initialization interval using `0x11a7ae0`; derive finite ordinary delay from .4f, or3.0f when`+0x358==1` | Native-integrated ordinary .4f path |
| `0x963254–0x963284` | Store deadline at global`0x1bf26e0` using current native time plus truncated double(delay×1000) | Native-integrated |
| `0x963288–0x9632c8` | If global function pointer`0x1bfb070` exists, call it, clear its active pointer and destroy its function object | Instruction-backed; tested active pointer null |
| `0x9632cc–0x963314` | Construct captured shutter callback, key `framedeltaconsumer`, and call original scheduling helper`0x159bdec` | Native-integrated |
| `0x963318–0x963378` | Dispose native temporary function/string state and return through original epilogue | Native-integrated |

The suffix itself does **not** construct a reverse .75s MoveTo action. It creates a timer, which leads to another timer and then a different action tree.

For finite tested clock values, the original instruction order is:

```text
base = (shutter+358 == 1) ? 3.0f : float32(0.4)
candidate = float32(base + float32(float32(end-start) / -1000.0f))
delay = (base < candidate) ? candidate : base
stamp = now + trunc_toward_zero(double(delay) * 1000.0)
```

This follows `FCMP s1,s0` / `FCSEL s8,s0,s1,MI`; it must not silently be rewritten as a minimum or ordinary positive elapsed-time subtraction. Here no service advances the clock during initialization, so interval0 yields delay **0.4000000059604645**, and native time8321 gives deadline**8721**. Backward clocks, NaNs, nonzero initialization cost and mode358=1 were not separately tested.

`0x11a7ae0` calls imported libc++ system_clock and uses signed multiply-high/shift to divide the returned integer by1000. The supplied system_clock service returns `controlledMilliseconds×1000`, and the original conversion executes. This clock is distinct from steady-clock GameTimeline input and persisted epoch date. No hardware clock-resolution claim follows.

### Timer provenance and ordinary branch selection

The native factory `0x9ff610` writes **shutter`+0x388=1` at `0x9ff67c`**. This is actual native construction, not a driver-assigned readiness flag. Its initial `+0x38c` accumulator and `+0x390` decoration pointer are zero. Original initializer prefix produces358=0 and399=0. The test leaves those values unchanged.

The new timer chain is:

| Producer | Native object / capture | Original invocation |
|---|---|---|
| Callback suffix call`0x963314 → 0x159bdec → 0xea937c` | TimerTargetCallback, vtable`0x1b18a18`; key `framedeltaconsumer`; delay .4f; function vtable`0x1b149c0`, capture shutter at`+8` | Scheduler`0x13d3f44` → Timer`0x15985d4` → trigger`0x1875b94` → function`0x18f83ec` |
| `0x18f83ec`,388!=0 branch | Compute clamp((deadline−now)/1000,0,10); schedule `scheduled_open_shutters`; function vtable`0x1a92880`, capture shutter`+8` | Scheduler/Timer → callback`0x186e018` → builder`0xb126b8` |
| `0xa9eea4 → 0xe14d8c → 0x18c89ec` after reveal action | TimerTargetSelector, vtable`0x1ad9968`; target shutter; selector`0x113af20`; zero interval | Scheduler/Timer → trigger`0x193f4f0` → selector`0x113af20` |

At wall8721, `framedeltaconsumer` fires and computes remaining delay0. Original Scheduler initializes the newly registered callback timer to elapsed0; a subsequent dt0 invokes `scheduled_open_shutters`. This is observed timer behavior, not a host call to the builder.

**Instruction-backed alternative:** if388==0, `0x18f83ec` instead invokes decoration helper`0xcf3490` and registers repeating `transition_shutter_check_network_done` through `0x9d7224`. Callback`0x83b8b0` accumulates dt at`+0x38c`, watches388, and can remove the poll/fade the decoration and invoke the reveal builder when readiness changes. Its >7s branch may restore dispatch and build a dialog. The strings/branches support this bounded interpretation; no account/network operation, timeout dialog or production writer changing388 was executed. Default388=1 is sufficient for the ordinary tested transition.

### Native closing/reveal action construction

Builder **`0xb126b8`** runs from the original `scheduled_open_shutters` callback. It creates three actions combined by native Sequence factory`0x14be12c`:

1. CallFunc bound to shutter method **`0x196fcf4`**.
2. **EaseIn(rate1.5, MoveBy(duration float32(.3), delta(-leftWidth,0)))**.
3. CallFunc bound to TransitionScene method **`0xa9eea4`**, captured on the actual shutter.

The varargs factory yields nested `Sequence(Sequence(firstCallFunc, easedMoveBy), finalCallFunc)`. There is no DelayTime in this ordinary tree. It is registered on the **left panel** by original virtual runAction at`0xb127e8` → `0xc7820c` → ActionManager insertion`0xb3dc38`.

The initial CallFunc **`0x196fcf4`** runs at the first native action update. Its ordinary399=0/358=0 branch requests a sound through the existing inert audio interface, then constructs **right-panel EaseIn(rate1.5, MoveBy(.3f,(rightWidth,0)))** at`0x196ffac–0x196ffe8`. Alternative399 overlay fading and358==1 decorative action branches remain instruction-backed. The right action is created by this original callback, not separately injected by the driver.

| Action / captured function | Ordinary fixture pointer | Vtable / relevant layout |
|---|---|---|
| Left outer / inner Sequence | `0x4161c40 / 0x4161bc0` | `0x1aa5508`; children`+0x40/+0x48`; duration`+0x30` |
| Initial CallFunc | `0x41619c0` | `0x1acbd78`; function active pointer`+0x70` |
| Initial bound object | `0x4161a10` | `0x1b1bec0`; method`+8=0x196fcf4`, adjustment`+0x10=0`, shutter`+0x18=0x4150c80` |
| Left EaseIn / MoveBy | `0x4161ac0 / 0x4161a40` | EaseIn`0x1b452b8`, rate`+0x48=1.5`, inner`+0x40`; MoveBy`0x1b40200`, deltaXYZ`+0x3c/+0x40/+0x44=(-100,0,0)` |
| Final CallFunc / bound object | `0x4161b40 / 0x4161b90` | CallFunc`0x1acbd78`; bound vtable`0x1aa0a40`, method`+8=0xa9eea4`, adjustment0, same shutter`+0x18` |
| Right EaseIn / MoveBy | `0x4162080 / 0x4162000` | Same respective action vtables; deltaXYZ=(100,0,0) |

These action snapshots were taken at runAction entry, before manager startWithTarget initialized Sequence split/target state. Their initial zero split/targets are not assertions about the running action. Both have original native duration **0.30000001192092896**.

Factories **`0x18c4dd0`** (MoveBy) and **`0xdaad00`** (EaseIn) execute. Native EaseIn update`0xb40c9c` invokes power helper`0xdd7010` → imported `powf`, then inner MoveBy update`0x8e2b70`. The powf import is a declared host math service: double host power rounded into S0 float32. Original action normalization, target state, movement arithmetic, registration and completion branching execute. Exact bionic/libm powf behavior for every input is not claimed.

### Original Scheduler/ActionManager execution and final callback

The reused native Scheduler has the original ActionManager wrapper`0xd630b8` registered at INT_MIN priority. No host timer calls any new closure. The original path is:

```text
Scheduler13d3f44 → ActionManager wrapperd630b8 → ActionManager9effe0
 → ActionInterval12a5a80 → Sequence189cba0
 → CallFunc130cb2c → execute1935ccc
 → bound invoker1188cbc → start-reveal callback196fcf4
 ... native movement updates ...
 → CallFunc execute → bound invoker12d6f2c → finisha9eea4
```

The final bound-function type is the native libc++ binder for a `cocos2d::TransitionScene` member with a captured `TransitionShutter*`; it is not015's results-init binder reused with an invented callback.

`0xa9eea4` makes incoming visible and resets its transform state through original virtuals, handling an outgoing scene only when its pointer remains nonnull. This fixture's outgoing pointer was already released by963094. It then **schedules** selector **`0x113af20`** with interval0 through `0xe14d8c`; it does not synchronously set Director running.

`TimerTargetSelector` trigger **`0x193f4f0`** reads target at`+0x30` and member selector/adjustment at`+0x38/+0x40`, then dispatches it. The observed selector entry's LR is`0x15986b4` across the trigger tail branch. Selector`0x113af20`:

- Unschedules itself using`0xfbf528`.
- Copies Director cleanup byte`+0x150` into shutter`+0x2fd`.
- Calls original Director replacement **`0x9c90c0` at `0x113af50`** with incoming scene.
- Has an outgoing-visibility branch, skipped naturally because outgoing is null.

Replacement updates the scene-stack tail and pending scene; current remains shutter until Director consumes it. None of these fields or stack entries is assigned by the driver.

### Director scene ownership and input restoration

The next scoped original Director frame reaches pending consumer **`0xd0dc14`**. For old TransitionShutter → ordinary NormalGameResultScene, incoming is not a TransitionScene, so it executes old exit-transition-start, old exit and cleanup before replacing current. The oldWasTransition condition then prevents another incoming onEnter or enter-finished dispatch: transition exit already performed the latter.

| Actual virtual relationship | Executed original function |
|---|---|
| Shutter virtual`+0x318` | `0x9aa2d8` exit-transition-start notification |
| Shutter virtual`+0x310` | `0x8ff7cc` shutter exit override |
| Exit override base call at`0x8ff7dc` | TransitionScene exit`0x15840a8` |
| Base exit calls Node exit at`0x15840b8` | `0xd75c68`, recursively pauses/exits shutter children |
| Base exit enables dispatcher at`0x15840c4` | **`0x925c68(dispatcher,1)`** writes enabled`+0x124` |
| Base exit incoming virtual`+0x308` at`0x15840f0` | Normal results enter-finished **`0x1a1b1e8`** |
| Shutter override resumes after base | Remove both panels via virtual`+0x260` with cleanup1, release panel references |
| Override final app interface | App`+0x88`.virtual`+0x508` receives1; supplied UI-control service |
| Shutter virtual`+0x320` | `0x158dc2c`, original Node cleanup and conditional outgoing cleanup |

The dispatcher restoration therefore occurs **during transition exit inside Director consumption**, before its final running/pending assignment. The replacement selector alone leaves dispatch disabled. Visibility and event enable are separate state changes.

`0x1a1b1e8` calls native base enter-finished`0x783c2c`, reads/classifies the actual result and forwards a category-dependent character/audio feedback request to`0xacf898`. The reduced results-UI fixture leaves its character pointer and application audio interface absent. A preliminary no-hit run reached that service and failed on the absent interface. The final two regressions explicitly log and return at **`0xacf898`**, preserving base lifecycle, classification, transition exit, dispatcher restoration and all scene-management code. They do not claim that feedback output executes. The ordinary preliminary path happened not to require its unavailable provider; the final claimed ordinary run uses the same explicit boundary as failure, avoiding dependence on partial/null data.

### Observed state matrix

Ordinary object identities: **S=shutter`0x4150c80`**, **R=result scene`0x4150100`**, session`0x4150000`, GameResult`0x414f580`. Shutter vtable`0x1af1868`, NormalGameResultScene vtable`0x1afe2a0`. Scene stack is read directly from Director vector`+0x158/+0x160`.

| State | Initialized, before reveal | Movement elapsed.2 | Finish CallFunc returned | Selector replaced tail | Director consumed |
|---|---|---|---|---|---|
| Controlled wall ms | 8321 | 8921 | 9021 | 9021 | 9021 |
| Director running`+0x140` | S | S | S | S | **R** |
| Director pending`+0x148` | null | null | null | **R** | null |
| Native scene stack | [S] | [S] | [S] | **[R]** | [R] |
| Incoming running / visible | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| Shutter / panel running | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 | **0 / 0 / 0** |
| Shutter Ref | 3 | 3 | 3 | 2 | **1** |
| Result scene Ref | 2 | 2 | 2 | 3 | **4** |
| Dispatcher enabled`+0x124` | 0 | 0 | 0 | 0 | **1** |
| Observer registered / paused / enabled | 1 / 0 / 1 | same | same | same | same |
| Active action target entries | 0 | 2 | 0 | 0 | 0 |
| Pending work | framedeltaconsumer | movement | selector timer | Director pending | none |

This observes the requested incomplete-transition condition: initialized/visible results and even a completed reveal action do not by themselves imply final Director control or enabled dispatch. No cancellation/scene-interruption policy is inferred from pausing the test schedule at intermediate rows.

## Native validation traces and persistence regression

### Controlled schedule

The original two-tap chart/model preparation from015 is reused: notes1000/1150ms, original judgment at those times, native completion at GameTimeline E1271. Chart loading and JNI transport are not repeated. Ordinary completion still constructs and caches its result through original code.

Native ending Scheduler inputs `[0,4]`, supplied earlier UI-completion delivery, then `[0,2,.3]` construct GameSession/results scene/shutter. A scoped Director frame activates shutter. New stage inputs:

| Scheduler input / phase | Observation |
|---|---|
| `[0,.25,.25,.25]` | Existing opening action covers panels;963094 runs once, initializes/saves, now executes its complete ordinary suffix |
| `[0,.2,.2]` | Native framedeltaconsumer elapsed0/.2/.4; at8721 schedules scheduled_open_shutters delay0 |
| Next dt0 | Native scheduled_open_shutters invokes186e018→b126b8; left reveal tree registered |
| Next dt0 | Native first action tick invokes196fcf4 and registers right action; both begin at elapsed0 |
| dt.1 | LeftX−19.24500846862793; rightX1299.2449951171875; dispatcher0 |
| dt.1 | LeftX−54.433101654052734; rightX1334.43310546875; finish callback still0 |
| dt.1 | LeftX−100; rightX1380; finisha9eea4 count1; native selector timer registered/primed |
| Next dt0 | Selector113af20 count1; native replacement records pending R and stack[R]; dispatcher still0 |
| Scoped original Director frame | Native exit/cleanup, enabled dispatcher, running R, pending null |
| Extra Scheduler dt `[0,.25,1,5]`, each followed by scoped Director frame | No callback/save repeats; final state stable |

Manual Scheduler dt and Director's own wall-derived dt remain separate. The final scoped Director frame computes its own1.45s since the prior scoped frame; by then action/timer work has drained. No physical frame cadence/Android latency follows. GameTimeline E and last model-frame effective time remain1271 throughout presentation. Persisted date remains controlled epoch1700000000.

### Persistence and identity checks

The unchanged fixture deliberately retains its prior song key **`expedition015`**, difficulty2, modifier0, ct0, to compare with015. Each test uses a fresh private original SQLite `:memory:` database. Native schema strings, SQL writer decisions, bind/step/finalize and independent query readback execute; host SQLite is not used.

| Observation | Two-PURE | No-hit ordinary chart-end |
|---|---:|---:|
| GameResult pointer | `0x414f580` | `0x414ee80` |
| GameSession pointer | `0x4150000` | `0x414f900` |
| Normal results scene | `0x4150100` | `0x414fa00` |
| Shutter | `0x4150c80` | `0x4150580` |
| PURE / FAR / final LOST | 2 / 0 / 0 | 0 / 0 / 2 |
| Score getter | 10000002 | 0 |
| Live / integer health | 80.4000015258789 / 80 | 0 / 0 |
| Clear type | 3 | 0 |
| SQL score / shinyPerfectCount / perfectCount | 10000002 / 2 / 2 | 0 / 0 / 0 |
| SQL nearCount / missCount / health | 0 / 0 / 80 | 0 / 2 / 0 |
| SQL clearTypes.clearType | 3 | 0 |
| SQL id / version / date | 1 / 1 / 1700000000 | 1 / 1 / 1700000000 |

For each process, snapshots of both SQL tables immediately after963094 are exactly equal to final readback after transition and extra updates. The same pointer remains in ScoreState`+0x68`, GameSession`+0x18`, result scene`+0x2e8`→session, and shutter`+0x2e8`→result scene. No driver installs these relationships or supplies the save gate.

Measured native entry counts are **one each** for963094,18f83ec,186e018,b126b8,196fcf4,a9eea4,113af20,891150,dc2c48,13552d4 and12a5e60. There are two native Director replacement calls, two pending-consumer entries, one shutter onEnter and one ordinary results enter-finished callback. Database equality alone is not used to infer uniqueness. Forced onEnter re-entry or arbitrary repeat scene initialization is outside this test.

### Safe event-delivery validation

After shutter activation, the harness constructs a **real native EventListenerCustom** using original factory`0xdd6004`, constructor`0x1976098`, initializer`0x8a2f3c` and base listener initialization`0x7ddfd0`. Original scene-graph registration **`0x13321bc`** associates it with R, priority0. The original listener initialization/registration supplies registered1, paused0, enabled1; no test assignment flips those flags.

A prepared observation `std::function<void(EventCustom*)>` supplies clone/destructor/sink services. The callback performs no gameplay, UI or Director mutation. Original custom event constructor`0xffa914` creates `expedition016_observer`. Each probe calls original **`0x1980970`**; native EventListenerCustom wrapper **`0x16551f0`** forwards the actual event to the supplied sink.

| Probe | Dispatcher | Listener reg/paused/enabled | Observed sink deliveries |
|---|---:|---|---:|
| During initial shutter | 0 | 1 / 0 / 1, node R | 0 |
| After replacement selector, before Director consumption | 0 | 1 / 0 / 1, node R | 0 |
| After Director transition exit/consumption | 1 | 1 / 0 / 1, node R | **1** |

The exact event pointer/type/name and current target are observed by the sink. This is native dispatch to a prepared results-associated listener with a supplied endpoint. The real results-widget listeners are omitted by the UI boundaries; actual button routing, touch hit-testing and all production listener states remain unknown. No fake results-screen press or Android event is generated.

## Reference and action cleanup

Original Ref arithmetic executes for valid objects. Native scene-stack replacement drops one shutter reference and retains R; Director consumption drops another shutter reference and retains R. Observed shutter3→2→1 and R2→3→4 match those separate owners. Session remains2 and cached result5. The harness retains the outgoing gameplay scene as a root, so it stays at1 after963094 releases its transition reference.

On final Director consumption, shutter Node exit recursively sets panel running0. Original shutter override removes both panel children with cleanup1 and releases its explicit panel references. Original cleanup includes `0x7dbebc`, ActionManager removal`0xf14f9c`, and shutter cleanup`0x158dc2c`. The active actions were already finished/removed by native manager completion; final Scheduler timer lists are also empty. The callback captures are ordinary native function/member-pointer captures, not explicit extra shutter ownership supplied by the driver.

Pools are not drained and host arena frees do not reclaim memory. Remaining Ref1 does not establish actual deletion, a leak or complete resource reclamation. This expedition verifies lifecycle/control transitions and reference operations, not full destructor behavior.

## Remaining synthetic dependencies and hook inventory

Execution uses Unicorn2.1.4, Capstone5.0.9 and pyelftools0.33. Original executable bytes are unchanged. The **ordinary closing suffix and subsequent timers/actions/lifecycle code have no new PC-skip boundary**. Exact retained skips:

| Retained boundary | Supplied scope |
|---|---|
| `0x16a4238 → 0x16a48d8` | Resource creation replaced by original-constructed inert plain Node panels; width interface100,1280×720; native initializer prefix/positioning suffix execute |
| `0x121581c → 0x121584c` | Loading-overlay construction/addition omitted |
| `0x891190 → 0x89164c` | Results-UI prefix omitted; restore X28 application-global address/X26 scratch for native gate producer |
| `0x891688 → 0x89219c` | Middle result UI omitted; original gate branch retained |
| `0x8921dc → 0x8928e0` | Post-save UI/progression omitted |
| `0x1794004 → 0x1794010`; stop`0x1794020` | Graphics flush/render traversal/frame-finalization omitted; original pending consumer included |
| `0x1a51054` | Earlier ending animation completion still supplied; clone and actual native continuation147dee8 execute |

**Removed:** `0x963130 → 0x963354`. It is not retained in any successful016 regression.

Additional/sustained services:

- New `powf` PLT`0x1a6e080` service supplies math only; original EaseIn/MoveBy action state and branching execute.
- System clock PLT`0x1a6dbe0` supplies controlled raw values; original11a7ae0 conversion and deadline math execute. Steady clock, gettimeofday and epoch date are separately supplied.
- New **`0xacf898`** result-enter character/audio feedback service logs category and absent environment inputs; its original caller/lifecycle logic executes. The blocked preliminary no-hit run is not counted as a completed regression. Both final runs use the explicit boundary.
- Prepared custom-observer function services`0x4000840–0x4000880` implement cloning, inert destruction and recording. Factory/registration/dispatch and native listener forwarding are original; the observation endpoint is supplied.
- Existing Director/size/Camera services`0xa4227c/0xf09110/0x12a1654`; prepared account/provider/widget/control interfaces`0xb688e0/0xb99da4`, synthetic virtuals`0x4000800/0x4000810/0x4000820` remain. App control receives native0 during shutter enter and native1 during exit; its full UI subsystem effects are unexecuted.
- Existing ancillary services`0xfa4320/0x1186f70/0xc464e4/0x19becc0/0xe2388c`, audiovisual/progression boundaries`0xc800b0/0x107af5c/0x9c8190/0x9d2518/0x1019c18/0x1049858`, Node/runtime support`0xbda064/0x10ac6e8/0x19f2e40`, null-only Ref boundaries and original valid-object retain/release remain as disclosed in015.
- Allocators, memory/string operations, integer formatting, RTTI hierarchy casts, single-thread mutexes, process/errno and failed entropy-file open are supplied. Native SQLite exports execute. No real application file, account, sound, GPU or network is accessed.

Factory9ff610 and replacement9c90c0 hooks only observe entry and leave original control flow intact. No driver calls963094,18f83ec,186e018,b126b8,196fcf4,a9eea4 or113af20 to advance this successful chain. No driver writes final Director current/pending/stack, dispatcher enable state or save gates. Driver-controlled operations are initial environment preparation, frame/Scheduler advancement and the declared earlier UI-completion boundary.

## Updated integration coverage

| Path | Status after016 |
|---|---|
| Native gameplay/result → GameSession/result scene/shutter | Reused native-integrated; prepared gameplay/UI environment |
| Director activation → opening actions →963094 | Reused native-integrated scoped frame path |
| Original963094 ordinary suffix | **New native-integrated, bypass removed** |
| Framedeltaconsumer → scheduled_open_shutters | **New native-integrated timers/captures** |
| Reveal Sequence/EaseIn/MoveBy/CallFuncs | **New native-integrated**, external powf supplied |
| Finish → selector → native replacement | **New native-integrated** |
| Director consumption → shutter exit/cleanup → running R | **New native-integrated**, rendering omitted |
| Original dispatcher enable / safe custom event delivery | **New native-integrated to prepared listener/supplied sink** |
| Two-PURE and no-hit native SQLite regression | Passed; no repeated initializer/save |
| Readiness=false polling, overlay, special mode | Instruction-backed, unexecuted |
| Actual results widget/touch interaction, complete UI/audio | Unknown/unexecuted |
| Full memory reclamation / Android GL queue | Unexecuted |

## Pseudocode

Original ARM64 ordinary branches are represented below. Controlled clocks/dt, earlier animation completion, math import and UI/resource services remain as listed above.

```cpp
performNextSceneInit():                         // 963094, action-driven
    exitReleaseOutgoing();
    incoming.initializeResults();              // native save gate/SQLite; UI skips
    incoming.setVisible(true);
    if (overlay399): setupWhiteOverlay();       // instruction-backed alternative
    base = (mode358 == 1) ? 3.0f : float32(.4);
    candidate = f32(base + f32(f32(nowMs() - initStartMs) / -1000.f));
    delay = (base < candidate) ? candidate : base; // finite-input representation
    globalDeadline = nowMs() + trunc(double(delay) * 1000.0);
    if (pendingGlobalFunction): invokeAndDestroyIt(); // unexecuted here
    scheduleOnce("framedeltaconsumer", delay, [this](float) {
        if (ready388) {
            remaining = clamp(f32(double(globalDeadline-nowMs())/1000.0),0,10);
            scheduleOnce("scheduled_open_shutters", remaining,
                         [this](float) { buildRevealActions(); });
        } else {
            setupDecorationAndReadinessPoll(); // instruction-backed only
        }
    });

buildRevealActions():                          // b126b8, native timer-driven
    left.runAction(Sequence(
        CallFunc(bind(startReveal196fcf4, this)),
        EaseIn(MoveBy(float32(.3), {-leftWidth,0}), 1.5f),
        CallFunc(bind(transitionFinishA9eea4, this))));

startReveal196fcf4():                           // native CallFunc
    // ordinary mode: bounded sound request
    right.runAction(EaseIn(MoveBy(float32(.3), {rightWidth,0}),1.5f));

transitionFinishA9eea4():                       // native final CallFunc
    incoming.setVisible(true);
    resetIncomingTransform();
    if (outgoing) resetOutgoingTransformAndVisibility(); // outgoing null here
    scheduleSelector(setNewScene113af20, interval=0);

setNewScene113af20(float):                      // native TimerTargetSelector
    unscheduleSelf();
    shutter.cleanupOutgoing = director.cleanupScene;
    director.replaceScene(incoming);            // stack tail/pending; current unchanged

// Driver advances the original Director frame segment; it does not call exit.
director.consumePending():
    oldWasTransition = castTransition(running) != nullptr;
    if (!castTransition(pending)) {
        running.onExitTransitionDidStart();
        running.onExit();                      // shutter8ff7cc
        if (cleanupScene) running.cleanup();
    }
    release(running);
    running = retain(pending);
    pending = nullptr;
    if (!oldWasTransition) { running.onEnter(); running.enterFinished(); }

TransitionShutter.onExit():
    TransitionScene.onExit();
    removePanelsWithCleanupAndRelease();
    app.inputControl.setEnabled(true);          // original dispatch, supplied endpoint
TransitionScene.onExit():                       // 15840a8
    Node.onExit();
    dispatcher.setEnabled(true);                // 925c68, original state write
    if (outgoing) outgoing.onExit();
    incoming.enterFinished();                   // 1a1b1e8; character/audio bounded

// Safe native event probe, not a real button interaction:
dispatcher.dispatchEvent(preparedCustomEvent);
// Enabled dispatcher → registered native results-associated listener → supplied sink.
```

## Unresolved Mysteries

- Which production asynchronous operations change388 and use the pending global function, and how the polling/timeout branches behave with real services.
- Full resource-backed overlay, special358 modes and final graphical presentation; no assumptions are made from ordinary action symmetry.
- Real results-widget listener installation/hit testing inside omitted initializer blocks. The custom observer does not substitute evidence of button behavior.
- Complete character/audio feedback initialization atacf898; only its category/lifecycle caller and bounded interface are established here.
- Full autorelease/destructor reclamation and cancellation under production scene replacement/interruption. The completed native cleanup trace is narrower than a universal cancellation guarantee.
- Earlier ending-animation completion at1a51054 remains separate. No017, networking, account startup or FlickNote work was undertaken.

## GitHub Status

Prepared against **`6381de72c7858d11ce5416cbfda14150a1ed7bef`**. Only this report and an appended016 cumulative-context entry are authorized. Publication rechecks current main/absence of016 and updates the branch with an expected-head lease. Pinned committed readback, exact historical-context prefix and historical-blob/tree comparison are required after publication. The headquarters return supplies the exact publication commit and pinned links; the containing commit identifies this document without a self-referential SHA in its contents. No harness, database, trace, historical report, README, binary or asset is included in the publication tree changes.
