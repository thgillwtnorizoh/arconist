# Expedition 017 — Native Ending Animation and Continuation Delivery

## Result

**Strong success. Original native execution now invokes continuation `0x147dee8` without driver delivery.** The previously supplied interface at `0x1a51054` is `GameScene::songFinishedShowTrackSplash(std::function<void()>)`. Its ordinary implementation runs a Cocostudio **ActionTimeline**, plays the archived animation named `end`, and installs an end-frame callback. Original Scheduler/ActionManager advancement reaches that callback and invokes the original continuation.

Two complete scoped regressions passed: two PUREs and an ordinary no-hit chart-end result. Both proceeded through the native outro, results-context construction, shutter opening, results initialization and bundled SQLite saving, shutter closing, Director final scene activation and dispatcher restoration. Neither run manually delivered the ending continuation, shutter callback or closing callbacks. The earlier synthetic bridge is removed within this CPU-side integration.

An isolated original Node cleanup before the end frame removed the action and prevented continuation delivery. Original CSB animation parsing and CPU property-frame application also execute. Full graphical object loading, results layouts, account/audio services, Android runtime scheduling and memory reclamation remain outside the executed scope. This is not a claim of a complete application or rendered UI.

## What I Found

### Authority, preparation and evidence labels

Starting GitHub `main` was **`06f97599b1fd086b6cb319ff07aae5d7bdc936c0`**, containing Expedition 016 and no Expedition 017. Preparation read the project introduction, latest cumulative context, complete 016 report, 014's deferred-callback sections, and relevant scheduling/lifecycle/action evidence from 009, 011, 012 and 015. The supplied archive contains 9,658 entries. Existing local native adapters and fixtures were actually available and reused; no unavailable session state is claimed as recovered.

The main library is `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256 **`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`**, build ID **`17d660edbf37ca78beefc32e07672c97419ddce6`**. Addresses below are main-library ELF virtual addresses before relocation. Object addresses are explicitly test-arena pointers. ARM64 execution uses Unicorn 2.1.4; decoding uses Capstone 5.0.9 and pyelftools 0.33. Original executable and archived asset bytes remain unchanged.

Evidence categories retain their earlier meanings: **Native-integrated** means original routines execute together over the stated scope; **Native-isolated** means an original routine executes with prepared surrounding interfaces; **Instruction-backed** means decoded instructions/RTTI/archive evidence without complete enclosing execution; **Interpretation** identifies an explanation; **Unknown** marks an unverified path.

The central service, registration, ActionTimeline advancement, callback dispatcher, wrapper and continuation all execute original ARM64 instructions. Observers at those addresses record entry without replacing control flow. Driver-supplied visual resources and other services are inventoried below.

## Ending callback and UI service provenance

### Caller and actual method identity

The ordinary branch of `0x19bbdd0` constructs the continuation in its native stack function object. At `0x19bbf54–0x19bbf70`, original instructions install vtable `0x1aebc68`, capture the GameScene pointer at function-object `+8`, set the active function pointer at container `+0x20`, and call `0x1a51054` with **X0=GameScene, X1=reference to `std::function<void()>`**. Observed return address is `0x19bbf74`.

The service is identified as **GameScene::songFinishedShowTrackSplash** by its native function-object RTTI, including the wrapper lambda associated with this method. GameScene vtable is `0x1ae6ef0`. The ordinary tested application-state branch has application `+0xb0` object's byte 8 clear. An alternative ending branch constructs a different function-object type (`0x1aeec40`); that branch and special-character paths are not executed here.

This refines the earlier description of an unknown UI-animation service. It is a native method using Cocostudio timeline actions, not an unexplained external completion provider. This conclusion was established from this binary before choosing ActionManager as the execution mechanism.

### Production resource source versus fixture preparation

GameScene initialization references **`layouts/ingame/end/GameEnd.csb`** at `0xe2f63c/0xe2f644` (string `0x589521`). Decoded calls show:

| Production callsite | Producer and destination | Evidence here |
|---|---|---|
| `0xe2f674 → 0x95af50` | Resource-backed Node load, stored at GameScene `+0x3c8` at `0xe2f67c`, retained at `0xe2f690` | Instruction-backed full UI load |
| `0xe2f6c0 → 0xd54254` | ActionTimeline load, stored at GameScene `+0x3d0` at `0xe2f6c8`, retained at `0xe2f6dc` | Instruction-backed enclosing loader |
| Fixture → `0x1312338 → 0x1a0b5fc` | Original cache setup and CSB ActionTimeline reader with the actual archived bytes | Native-isolated loading, then joined to ending execution |

The archived member **`assets/layouts/ingame/end/GameEnd.csb`** is 7,380 bytes, SHA-256 **`d6b1322d68d011374473afe529180d855c9aa2ac907e09fb95b9f0a4d619b02b`**, root version string `2.1.0.0`. Its bytes are copied unchanged into mapped memory. A prepared native Data interface supplies buffer `+0`, length `+8`; original Data bytes accessor `0xf235e8` executes.

The original reader `0x1a0b5fc` constructs a real ActionTimeline through `0x898dec`, inserts two AnimationInfo records through `0x1895548`, and executes property parsing `0x97f5e4`, Timeline factory `0x15c1990`, and ActionTimeline insertion `0x88942c` **24 times each**. All 24 property Timelines and **85 frames** are retained. No tracks are filtered or durations invented. There are six action-tag groups with Position, Scale, RotationSkew and Alpha tracks.

The original native metadata yields:

| Value | Observed native value |
|---|---:|
| ActionTimeline duration | 80 frames |
| Playback speed | 1.0 |
| Stored float32 frame interval | 0.01666666753590107 seconds |
| Named `end` | start 0, end 50 |
| Named `out` | start 50, end 80 |

The visual Node hierarchy is a declared resource boundary. Static names, hierarchy and action tags are read from the same CSB. Seven original Node objects are constructed through `0x131419c`, named through original `0x170e4c0`, and added through original child interfaces: root `Layer`, with `Sprite_8`, `back`, `stripeTop`, `stripeBottom`, `mid`, and `clearImage`. They are **plain Node visual proxies**, not native-created Sprites. A copied Node vtable preserves original CPU property methods and RTTI while adding an inert texture-request interface at virtual `+0x518`.

The driver links each original property Timeline to its matching prepared Node through the original Timeline action-tag getter and `setNode` virtuals (`+0x48/+0x50`). It prepares GameScene `+0x3c8/+0x3d0` and calls original retains to match the decoded production resource interface. The full CSLoader Node/ComExtensionData binding path is not executed. This substitution supplies visual targets; it does not implement frame progression, end-frame registration or completion decisions. Original ActionTimeline `startWithTarget` (`0xc97694`) and Node enumeration (`0x1713774`, seven visits) execute.

## Original `0x1a51054` behavior

The ordinary body **`0x1a51054–0x1a51770` executes without a PC skip or service replacement**. It looks up child visual objects through Node virtual `+0x210`, classifies the actual cached result, selects texture names, centers the root in the prepared 1280×720 viewport, starts the native action, adds the root to GameScene, plays `end` non-looping, and installs the completion wrapper.

For clear category 3, actual texture requests are `img/clear_pure.png`, `img/end_mid_p.png`, `img/end_back_p.png`, `img/end_stripe_top_p.png`, and `img/end_stripe_bottom_p.png`. Texture output is inert. The native choice of names and all CPU-side control continue normally.

Key original callsites:

| Callsite | Dispatch | Observed target |
|---|---|---|
| `0x1a515a8` | Root virtual `+0x388`, argument Scene `+0x3d0` | Node runAction `0xc7820c`, original manager insertion `0xb3dc38` |
| `0x1a515bc` | GameScene virtual `+0x1e8` | Add ending root as child; original enter/resume lifecycle |
| `0x1a515e8` | ActionTimeline virtual `+0x50`, string `end`, loop 0 | Named play `0x19039ec` |
| `0x1a516dc` | ActionTimeline virtual `+0x118`, string `end`, native wrapper | End registration `0x1858c3c` |

Root anchor becomes `(0.5,0.5)` and position `(640,360)`. Original property frames affect the prepared Nodes: for example, `mid` opacity is 0 at registration, 110 after the first 0.4-second update, and 255 after the second. Position/scale/rotation/alpha application is original CPU execution, not a host animation substitute.

### Relevant native layouts

These offsets describe the tested binary, not generic Cocos versions.

| Object | Field | Meaning / observed value |
|---|---|---|
| GameScene | `+0x3c8`, `+0x3d0` | Ending visual root, native ActionTimeline |
| GameScene | `+0x488`, `+0x490` | Continuation writes outro state and controlled native clock sample |
| ActionTimeline, vtable `0x1b89a78` | `+0x18`, `+0x20` | Original target / target |
| ActionTimeline | `+0x38/+0x40/+0x48` | Tag-group map begin/root/count; count 6 |
| ActionTimeline | `+0x50/+0x58/+0x60` | Property Timeline vector; 24 entries |
| ActionTimeline | `+0x68`, `+0x70` | Integer duration 80; accumulated double time |
| ActionTimeline | `+0x78`, `+0x7c` | Float32 speed and frame interval |
| ActionTimeline | `+0x80`, `+0x84` | Playing byte and current frame |
| ActionTimeline | `+0x88/+0x8c/+0x90` | Start frame / end frame / loop byte |
| ActionTimeline | `+0x100/+0x108/+0x110` | Frame-end callback tree begin/root/count |
| ActionTimeline | `+0x118/+0x120/+0x128` | AnimationInfo tree begin/root/count |
| Property Timeline, vtable `0x1ac4190` | native frame vector and action tag | Original keyframes and Node binding |
| Original continuation, vtable `0x1aebc68` | `+8` | Raw captured GameScene pointer |
| Wrapper, vtable `0x1aec468` | `+0x10`, `+0x20`, `+0x40` | Raw GameScene, nested function container, active nested function pointer |

RTTI identifies the action as `cocostudio::timeline::ActionTimeline`, and the property objects as `cocostudio::timeline::Timeline`. This is not the shutter's Sequence/CallFunc subtree, although both are advanced by ActionManager.

## Native continuation capture and lifetime

The original continuation is copied using its native function-object interfaces. The service constructs a native heap wrapper of 0x50 bytes at `0x1a51654–0x1a516c0`. Wrapper invocation `0x1677270` reads the nested function pointer at `+0x40`, dispatches virtual `+0x30`, and reaches `0x147dee8`.

| Function object | Heap clone / clone into | Destruction interfaces | Call operator |
|---|---|---|---|
| Original continuation `0x1aebc68` | `0xacbdc4 / 0xb698fc` | `0x1891258 / 0x1556674` | `0x147dee8` |
| Splash wrapper `0x1aec468` | `0x12c4de4 / 0x1326e94` | `0xa05588 / 0xd5b8b8` | `0x1677270` |

`0x1858c3c` finds the named AnimationInfo through `0xf6e9fc`, stores a native function copy in that record, reads its end frame, and calls virtual `+0x120` at `0x1858d64` into **`0xd6f25c`**, installing another native callback copy keyed by frame 50 and name `end`. The outer frame tree node stores frame at `+0x20` and nested callback-map root at `+0x30`; inner nodes store name at `+0x20` and function container at `+0x40` (active pointer `+0x60`). AnimationInfo nodes store name `+0x40`, start/end `+0x58/+0x5c`, and function container `+0x60` (active pointer `+0x80`).

Ordinary-run identities demonstrate real copies, all capturing the same GameScene **`0x4102400`**:

| Stage / owner | Wrapper or function pointer | Nested continuation |
|---|---|---|
| Input stack continuation | `0x60deee0`, vtable `0x1aebc68` | Captures scene at `+8` |
| Registration argument wrapper | `0x415a800` | `0x415a820` |
| AnimationInfo node `0x4151400`, `end[0,50]` | `0x415a880` | `0x415a8a0` |
| FrameEndCallbacks node `0x415a9c0`, `end` at 50 | `0x415aa40` | `0x415aa60` |
| Local callback copy actually invoked | `0x415abc0` | **`0x415abe0`** |

The `out[50,80]` AnimationInfo record has an empty completion function. Original registration temporaries and dispatcher-local copies pass through their original destruction interfaces. The persistent AnimationInfo and frame-map callbacks **remain stored after delivery**, including in the separate cleanup ownership probe. There is no evidence here of automatic callback unregistration.

The wrapper's clone copies raw scene `+0x10` and clones the nested function; the capture itself does not add a GameScene Ref retain. Destruction destroys the nested function, not the captured scene. The fixture retains the outgoing scene as an explicit root, as in 015–016. Scene Ref stays 3 across ending callback delivery and is 1 after the transition releases it. This demonstrates observed reference operations, not unrestricted safety of invoking a saved callback after arbitrary scene destruction.

## Completion mechanism and callback delivery

The executed call chain is:

```text
Scheduler 0x13d3f44
  → registered ActionManager wrapper 0xd630b8
  → ActionManager update 0x9effe0
  → ActionTimeline virtual step 0x15b4c38
  → frame application 0xac9290
  → frame-end callback dispatch 0x7d613c
  → native function wrapper 0x1677270
  → original continuation 0x147dee8
```

All connections in this chain are **Native-integrated** within the prepared runtime. Driver code advances Scheduler and the scoped Director frame; it does not select or invoke the continuation.

`0x15b4c38` checks playing state and valid timeline data, advances accumulated time using the native float32 speed×dt calculation, derives current frame with the stored interval, applies original property frames, and dispatches frame-end callbacks. The ordinary in-range dispatch is virtual `+0x158` at **`0x15b4d00`**; observed dispatcher LR is `0x15b4d04`. A non-looping end-cap path can also dispatch at `0x15b4d7c`, LR `0x15b4d80`, when changing to the terminal frame.

`0x7d613c` finds the exact frame's callback map, copies the callbacks locally and invokes function virtual `+0x30` at **`0x7d6330`**. The observed wrapper and continuation both have LR **`0x7d6334`**, because the wrapper forwards through a tail dispatch. This identifies the native invocation source independently of final score or timer state.

At `0x147dee8`, the actual captured scene is retrieved from function `+8`; original code changes scene state, records the native clock, and schedules the two-second `outro` through **`0x147df58 → 0x159bdec`**. The former service queue is empty throughout the successful regression. No driver invokes `0x147dee8` or its function object.

## Timing and cancellation tests

### Before completion, completion, and extra updates

The two-tap fixture reaches native gameplay completion at effective GameTimeline **E=1271ms**. Scheduler inputs `[0,4]` invoke the original ending timer at controlled wall 5271ms. The native action is now registered and playing `end[0,50]`. Wall clock values, Scheduler dt and GameTimeline E remain distinct.

| Subsequent Scheduler dt | Native accumulated time | Current frame | Playing | Continuation count |
|---:|---:|---:|---:|---:|
| registration / 0 | 0 | 0 | 1 | 0 |
| 0.4 | 0.4000000059604645 | 23 | 1 | 0 |
| 0.4 | 0.800000011920929 | 47 | 1 | 0 |
| 0.03 | 0.8300000112503767 | 49 | 1 | 0 |
| 0.01 | 0.8400000110268593 | **50** | **1** | **1** |
| 0.02 | 0.8333333730697632 | 50 | 0 | 1 |

The callback runs at wall 6111ms in this controlled sequence. It is eligible at **the registered frame 50**, and can run while playing is still 1. The next update caps native time to float32 `50×interval` converted to double and stops non-looping playback. It does not repeat the callback when the old current frame is already 50. The nominal 50-frame range and the observed discrete update crossing must not be simplified into a hardware latency claim or an arbitrary host timer of 0.833 seconds.

Scheduler dt 2 subsequently executes the original outro; `0xf0b48c` plays actual native `out[50,80]` through `0x19039ec`, replacing the previous inert widget boundary as well. Dt 0.3 executes the scene-change timer. Native `out` advances to frame 67 and then 80 without repeating the end callback at 50. Further Scheduler inputs `[0,0.25,1,5]`, with scoped Director frames, produce no repeated continuation, initializer or save. This is uniqueness for the tested forward ordinary sequence; persistent registration does not establish uniqueness under forced replay or rewinding.

### Original cleanup before frame 50

At frame 49/time 0.8300000112503767, with no delivered continuation, the driver requests **original Node cleanup `0x7dbebc`** on the ending root. It reaches original **ActionManager removeAllActionsForTarget `0xf14f9c`** and recursive child cleanup. After Scheduler dt `[0.01,0.02,0.5,2,5]`:

| Observation | Before cleanup | After cleanup and updates |
|---|---:|---:|
| Ending action entries | 1 | 0 |
| ActionTimeline Ref | 3 | 2 |
| Ending root Ref | 4 | 3 |
| Current frame / playing | 49 / 1 | 49 / 1 |
| Continuation entries | 0 | 0 |
| Results scenes / SQL score rows | 0 / 0 | 0 / 0 |

The registration remains stored; removing the manager dispatch source prevents advancement. Cleanup does not itself clear this timeline's playing byte. This is **Native-isolated cancellation** through an actual native cleanup interface requested by the driver. It is not proof of an Android cancellation sequence or of which production interruption chooses this operation.

### State after successful scene exit

ActionTimeline `isDone` **`0x102de94` returns false** on the tested action, even after its playing flag becomes 0. At final results activation the ending action remains in **one paused ActionManager target entry**, root running 0, frame 80/range `[50,80]`, playing 0. Shutter action entries are removed and Scheduler timers have drained. The ending root still has the old GameScene parent in this retained fixture; its callback-map count is 1 and AnimationInfo count 2.

Thus successful completion does not mean ActionManager is globally empty or callback storage is destroyed. No memory leak conclusion follows: pools and allocator reclamation are supplied, and full original scene destruction is not tested.

## Uninterrupted native completion-to-results regression

### Scope and reproducible driver sequence

The prepared native ordinary chart/model from 014–016 is reused: two tap notes at 1000/1150ms, native model frames, native initial input and native score/gauge/result construction. Whole-file AFF parsing and JNI transport are established earlier but not re-executed here. The fixture deliberately retains song ID **`expedition014`**, difficulty 2, modifier 0 and ct 0; this is a fixture key, not evidence of chart metadata loading.

Each regression creates a fresh private bundled SQLite `:memory:` database. Native schema strings, native writers and native SQLite query/step/readback execute; host SQLite does not perform the storage. Epoch date is supplied as 1700000000.

After the native ending delivery above, driver operations are Scheduler `[2,0.3]`, scoped Director activation, opening Scheduler `[0,0.25,0.25,0.25]`, and the established 016 reveal schedule `[0,0.2,0.2,0,0,0.1,0.1,0.1,0]`, followed by scoped Director consumption and extra updates. Driver dt and Director wall-derived dt are separate inputs. The driver does not construct GameSession, install its GameResult, assign save gates or final Director scene pointers, or call presentation/closing callbacks.

Native gameplay completion `0x10a7550 → 0xc27d34` caches GameResult through `0x1600bb0` at **ScoreState `+0x68`**. Native continuation/outro/scene-change proceeds through `0xf0b48c → 0x18f11c0`, constructs GameSession with result `+0x18`, creates NormalGameResultScene retaining session `+0x2e8`, and constructs TransitionShutter. Original Director pending consumption activates shutter and original actions invoke **`0x963094`**. The incoming initialization virtual reaches **`0x891150`**, including its native save-gate producer `0x89164c–0x891684` and original eligibility branch `0x89219c–0x8921dc`. Callsite `0x8921b8` invokes **`0xdc2c48 → 0x13552d4 / 0x12a5e60`**, then bundled SQLite.

The 016 native closing suffix remains enabled: frame-delta consumer `0x18f83ec`, scheduled opening `0x186e018`, reveal builder `0xb126b8`, first CallFunc `0x196fcf4`, finish `0xa9eea4`, selector `0x113af20`, Director replacement and transition exit. The native exit enables EventDispatcher before final results-scene control. These are re-executed downstream, not newly inferred from documentation.

### Identity, records and final state

| Observation | Two-PURE run | No-hit ordinary chart-end run |
|---|---:|---:|
| Cached native GameResult | `0x4159ec0` | `0x41597c0` |
| Native GameSession | `0x415b140` | `0x415a9c0` |
| Native NormalGameResultScene | `0x415b240` | `0x415aac0` |
| Native TransitionShutter | `0x415bdc0` | `0x415b640` |
| PURE / FAR / final LOST | 2 / 0 / 0 | 0 / 0 / 2 |
| Native score getter | 10000002 | 0 |
| Live / result integer health | 80.4000015258789 / 80 | 0 / 0 |
| Native clear category | 3 | 0 |
| SQL score / shinyPerfectCount / perfectCount | 10000002 / 2 / 2 | 0 / 0 / 0 |
| SQL nearCount / missCount / health | 0 / 0 / 80 | 0 / 2 / 0 |
| SQL clearTypes.clearType | 3 | 0 |

Each score row also reads id 1, version 1, date 1700000000, songId `expedition014`, songDifficulty 2, modifier 0, ct 0. Each clearTypes row has id 1 and the same song/difficulty/ct key. Both tables' readback immediately after result initialization exactly matches final readback after closing and extra updates. Failure did not suppress this ordinary local save path.

The same actual GameResult pointer remains in ScoreState `+0x68` and native GameSession `+0x18`; the results scene retains that session, and shutter retains that results scene. Final Director state is running=result scene, pending=null, stack=[result scene], incoming running/visible=1/1, shutter and panels running=0, dispatcher enabled=1. GameTimeline E and last model-frame E remain 1271 throughout presentation; controlled wall reaches 16131ms after extra updates.

Measured native entry counts are **one each** for `0x19bbdd0`, `0x1a51054`, `0x1677270`, `0x147dee8`, `0xf0b48c`, `0x18f11c0`, `0x963094`, `0x891150`, `0xdc2c48`, `0x13552d4`, `0x12a5e60`, `0x18f83ec`, `0x186e018`, `0xb126b8`, `0x196fcf4`, `0xa9eea4`, and `0x113af20`. Named play `0x19039ec` executes twice (`end`, `out`). ActionTimeline step executes 13 times; frame-end dispatcher executes eight times, but invokes the wrapper/continuation only once. Database equality alone is not the callback-uniqueness test.

A prepared native results-associated EventListenerCustom receives one safe custom event after original dispatcher restoration through original `0x1980970`. Its endpoint is supplied. This reuses the 016 observer and is not discovery or execution of a real results-button listener.

## Remaining synthetic dependencies and hook inventory

### Removed and retained control boundaries

**Removed:** the `0x1a51054` service/captured-completion delivery. No PC skips occur in this method, `0x1858c3c`, `0xd6f25c`, `0x15b4c38`, `0x7d613c`, `0x1677270` or `0x147dee8`. The old inert virtual at `0x4000800` is unvisited because actual ActionTimeline handles `out`. The 016 removal of the `0x963130` suffix bypass remains intact.

Exact retained skips from the previously bounded UI environment:

| Boundary | Supplied scope |
|---|---|
| `0x16a4238 → 0x16a48d8` | Shutter panel resource creation replaced by original-constructed inert Nodes, width interface 100, viewport 1280×720 |
| `0x121581c → 0x121584c` | Loading overlay omitted |
| `0x891190 → 0x89164c` | Results UI prefix omitted; X28 application-global/X26 scratch restored for original gate producer |
| `0x891688 → 0x89219c` | Middle results UI omitted; native save gate/branch retained |
| `0x8921dc → 0x8928e0` | Post-save UI/progression omitted |
| `0x1794004 → 0x1794010`, stop `0x1794020` | GPU flush/render traversal/frame finalization omitted; original Director pending consumer retained |

### Resource and service boundaries

- **New ending visual boundary:** original Node proxies and manual metadata-based Timeline-to-Node binding described above; inert texture virtual `+0x518 → 0x4000900` logs five ordinary requests. Full native CSB ActionTimeline loading, property frames and continuation logic are original. No host supplies a current frame, end condition, callback registration or callback call.
- **New imported support:** C-string constructor PLT `0x1a6dba0` supplies two native CSB metadata string constructions. `sinf` PLT `0x1a6de70` supplies 69 math calls in the ordinary run; original native interpolation and completion branching remain intact. Additional cosf/acosf/sqrtf adapters were installed but unvisited. Existing `powf` PLT `0x1a6e080` supplies eight shutter easing calls. Results are written back as float32.
- **Clocks:** steady clock `0x1a6dc60`, system clock `0x1a6dbe0`, gettimeofday `0x1a6e5c0`, and epoch-date services are controlled separately. Original clock conversions/deadline logic execute. No Java timestamp substitutes for GameTimeline time.
- **Original runtime support retained:** autorelease/pool services `0x10ac6e8/0x19f2e40`, Node support `0xbda064`, valid-object original retain/release with null-only boundaries `0x147fe48/0xd6dc98`. Arena free/destruction support does not reclaim memory or drain pools.
- **Prepared application interfaces retained:** Director/size/camera `0xa4227c/0xf09110/0x12a1654`; account/provider `0xb688e0/0xb99da4`; control/provider virtuals `0x4000810/0x4000820`. Ancillary service boundaries `0xfa4320/0x1186f70/0xc464e4/0x19becc0/0xe2388c`, audiovisual/progression boundaries `0xc800b0/0x107af5c/0x9c8190/0x9d2518/0x1019c18/0x1049858`, and results-enter feedback `0xacf898` remain scoped/inert. Their production subsystems are not claimed executed.
- **Observer only:** factory `0x9ff610` and Director replacement `0x9c90c0` hooks record entry and leave PC unchanged. Prepared safe-listener function services `0x4000840–0x4000880` clone, destroy inertly and record delivery; they do not drive ending completion.
- **External runtime:** allocations, reallocations, libc memory/string/integer formatting, RTTI hierarchy casts, single-thread pthread/mutex services, process/errno and failed `/dev/urandom` open remain supplied as in 013–016. SQLite exports and decision logic execute in the bundled library, with no real database/account/network access.

No driver manually calls `0x147dee8`, creates GameSession, assigns its result, calls shutter `0x963094` or closing callbacks, writes the save gate, or assigns final Director running/pending/stack/dispatcher state in the successful regression. Driver work is initial chart/model/environment/resource preparation, controlled clocks, Scheduler/scoped Director advancement, observation/readback, and the explicitly isolated cleanup test.

## Pseudocode

The following is instruction-backed pseudocode for the executed ordinary branch. Resource preparation and clocks are labeled separately. Float32 and double conversions remain significant; this is not a replacement implementation.

```cpp
// Supplied environment: native prepared chart/model, private native SQLite,
// original-CSB ActionTimeline, inert Node visual targets and original setNode links.
// Original gameplay and ending Scheduler path:
onGameplayComplete():                          // c27d34, native frame delegate
    cacheSnapshotInScoreState68();             // 1600bb0, not an X0 return contract
    scheduleEndingAnimation();                 // e5c700, ordinary delay 4 seconds

endingAnimation():                             // 19bbdd0, native TimerTargetCallback
    continuation = nativeFunction([scene] {    // vtable 1aebc68; raw scene capture
        scene.enterOutro();                    // 147dee8
    });
    scene.songFinishedShowTrackSplash(continuation); // 1a51054, fully executed here

songFinishedShowTrackSplash(continuation):
    chooseVisualTexturesFromNativeResult();    // actual classifier; inert texture output
    root.setAnchorPoint(.5f,.5f);
    root.setPosition(viewportCenter);
    root.runAction(actionTimeline);            // c7820c -> b3dc38
    scene.addChild(root);                      // native enter/resume action target
    actionTimeline.play("end", false);         // 19039ec, archived range [0,50]
    wrapper = nativeFunction([scene, continuation] {
        continuation();                       // 1677270 -> original 147dee8
    });
    actionTimeline.setAnimationEndCallFunc("end", wrapper); // 1858c3c

setAnimationEndCallFunc(name, fn):
    info = findAnimationInfo(name);
    info.callback = nativeCopy(fn);
    addFrameEndCallFunc(info.endFrame, name, info.callback); // d6f25c

// Driver advances original Scheduler with controlled dt; no host completion test.
scheduler.update(dt):                          // 13d3f44
    actionManager.update(dt);                  // d630b8 -> 9effe0
ActionTimeline.step(dt):                       // 15b4c38; simplified forward case
    if (!playing || noTimelineData) return;
    time += double(float32(speed * dt));
    advanceNativeFramesAndProperties(time, interval, start, end, loop);
    if (nativeFrameDispatchNeeded)
        dispatchFrameEndCallbacks(currentFrame); // 7d613c
    // Native terminal branch caps time/clears playing; not the same as isDone().
dispatchFrameEndCallbacks(frame):
    localCallbacks = nativeCopy(callbacksAtExactFrame(frame));
    for (fn : localCallbacks) fn();             // virtual+30 at 7d6330
    // Persistent map entries are not erased in this tested path.

GameScene.enterOutro():                        // 147dee8, runtime-invoked
    updateOutroStateAndClock();
    scheduleOnce("outro", 2, nativeOutro);     // native TimerTargetCallback
nativeOutro():                                // f0b48c
    actionTimeline.play("out", false);         // archived range [50,80]
    scheduleNativeSceneChange();
nativeSceneChange():                          // 18f11c0
    session = nativeGameSession(scoreState.cachedResult68);
    incoming = nativeNormalResultScene(session);
    shutter = nativeTransitionShutter(incoming);
    director.replaceScene(shutter);

// Re-executed established 015–016 code, with declared visual/UI boundaries:
director.consumePendingScene();               // native onEnter lifecycle
shutter.onEnter();                            // original opening action construction
// Scheduler/ActionManager -> original CallFunc, not driver invocation:
shutter.initializeIncoming();                  // 963094
incoming.initializeResults();                 // 891150, original gate/save segments
if (nativeSaveEligible)
    saveHelper();                             // dc2c48 -> native writers -> bundled SQLite
// Original timers, reveal actions, finish CallFunc, selector and Director consume:
finishShutterAndActivateIncoming();
// Native transition exit restores dispatcher; running scene is NormalGameResultScene.

// Separate isolated cancellation test, not an asserted Android caller:
driverRequests(root.cleanup());               // 7dbebc -> f14f9c
// Native manager removes action; no later frame progression/continuation in test.
```

## Updated integration coverage

| Path | Status after 017 |
|---|---|
| Original GameEnd.csb → native ActionTimeline, all property frames and named clips | New Native-isolated resource load, then integrated ending execution |
| Full ordinary `0x1a51054` → action/clip/end callback registration | **New Native-integrated; previous service replacement removed** |
| Scheduler/ActionManager → ActionTimeline → native wrapper → `0x147dee8` | **New Native-integrated; no driver delivery** |
| Native property-frame CPU application to supplied visual Nodes | New native execution, full resource-backed Sprite creation omitted |
| Named `out` play from original outro | New native execution replacing inert widget interface |
| Gameplay result → GameSession/results scene/shutter | Re-executed native chain, prepared chart/model |
| Director/shutter opening → original initializer gate → bundled SQLite | Re-executed native chain, disclosed result UI skips |
| Native closing → Director final activation and dispatcher restore | Re-executed 016 native chain |
| Original Node cleanup before frame 50 | Native-isolated cancellation, delivery prevented |
| Ordinary/no-hit storage and non-repetition | Passed, explicit entry counts and record readback |
| Production Android interruption, full CSLoader Node binding, actual results buttons | Unexecuted/unknown |
| GPU artwork, audio, complete UI, pools/destruction | Supplied or omitted; no full application claim |

## Unresolved Mysteries

- The full original resource-backed Node/Sprite/ComExtensionData setup and cache ownership around `0x95af50/0xd54254`. Timeline animation loading itself executes, but production graphical binding remains a fixture boundary.
- Whether other application-state, character or special-scene ending branches use the same ranges and continuation types. Only the two ordinary fixture outcomes are executed.
- Production cancellation/interruption callers for this ending animation. Native cleanup's effect is established, not its automatic invocation by Android or every scene replacement.
- Behavior under forced replay, seeking or re-entry while stored callbacks remain. No universal single-delivery guarantee is inferred from the ordinary forward tests.
- Final destruction/unregistration of persistent callbacks and paused ending ActionTimeline after complete owner teardown. No leak or use-after-free claim follows from retained fixture objects.
- Real results-widget listeners, complete UI/progression, audio/character feedback and readiness=false/special shutter branches remain as bounded in 016. Safe observer delivery is not actual button interaction.

## GitHub Status

Prepared against **`06f97599b1fd086b6cb319ff07aae5d7bdc936c0`**. This report and an append-only Expedition 017 cumulative-context entry are the only publication files. Publication rechecks current main and absence of an existing 017, then uses an expected-head lease. Verification reads both files at the containing commit, compares exact prepared contents, checks the earlier context as an exact prefix, and compares the final tree against the starting commit, including unchanged reports 001–016 and README. The headquarters return provides the exact publication SHA and pinned document links; the containing commit identifies this report without a self-referential SHA inside its contents. No harness, database, trace, binary or archived asset is included.
