# Expedition 012 — Android Lifecycle, Pause/Resume & Gameplay State Preservation

Date: 2026-10-24. Project Arconist; repository `thgillwtnorizoh/arconist`, branch `main`.

## Result

**Strong success, with bounded UI/runtime services.** Original Cocos renderer lifecycle JNI executes through the original AppDelegate, GameScene pause method, model pause wrapper and GameTimeline. Original backgrounding pauses the gameplay timeline and stops Director animation. Foreground restarts Director animation but leaves the tested GameScene paused. A separately executed original PauseLayer resume-button function object reaches the GameScene delegate, native timeline resume, seek and unpause requests.

A controlled60,000ms interruption preserves effective chart time. Hold/arc contacts supplied through011's original JNI dispatch survive ordinary background/foreground in the tested path. Native foreground frames clear their per-frame active flags while gameplay remains paused; resuming gameplay restores activity from retained contacts. Deliberately delivered JNI UP/CANCEL can still release contacts while Director is stopped. The two-tap interrupted regression matches the uninterrupted run's judgment, gauge, score, completion and effective time exactly.

This is not execution of an Android VM/GLThread queue, actual FMOD playback or complete scene destruction. Java submission/call order is reconstructed from smali. Native callback order is driver-controlled and reported as such. Native pause-menu acceptance executes on a prepared Node/widget hierarchy; dismissal animation and external provider/platform services remain boundaries. Full scene teardown/resource ownership is partial, not an achieved excellent-success claim.

## What I Found

### 1. Preparation, identity and evidence

Read the supplied project instructions, current cumulative context, complete011 report, and relevant005/008/009 timeline/pause/contact/destructor evidence. Inspected original AppActivity/Cocos lifecycle smali and both relevant ARM64 libraries. Starting main is **`e4deb6866843f523425a8be1d47e404888f93fc0`**, tree `8ad04d475e1a33655e2717d839fed71814ad7d94`; no012 report existed at the starting check. Earlier scratch loaders/fixtures actually remained available and were inspected/reused; new012 lifecycle fixtures/observers were written. No unavailable prior state is assumed recovered.

| Original source | SHA-256 |
|---|---|
| supplied archive | `5dc2f3d1f5387d0c5da06ad72694105cdd7fa4b7ff80f981f77998e89eb2b4cb` |
| instruction text | `8a9bea2e002d6ce282dc7b92592379927088a2ecbab2e451b585aea4c921f1e8` |
| libcocos2dcpp.so | `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` |
| libfmodProvider.so | `db07590708c1e2b7ed3a17800a8839392d5a7a8322cd102d5b35bda05b251bfb` |

Main Build ID is `17d660edbf37ca78beefc32e07672c97419ddce6`. Native addresses and field offsets below are hexadecimal **main-library ELF VAs before relocation**, unless explicitly identified as provider-library or synthetic arena addresses. Times, coordinates, state values and IDs are decimal.

**Native-integrated** means original routines execute together on the stated scoped path. **Native-isolated** means original code executes with surrounding interfaces supplied. **Instruction-backed** means decoded native/smali support without execution of the entire enclosing path. **Interpretation** identifies an explanatory role; **Unknown** identifies a missing producer or path. Function labels are researcher descriptions unless supported by original RTTI or JNI symbols.

## Java/Android lifecycle call chain

### 2. AppActivity and Cocos responsibilities — Instruction-backed

Sources: `smali/low/moe/AppActivity.smali`, `smali_classes3/org/cocos2dx/lib/Cocos2dxActivity.smali`, `Cocos2dxGLSurfaceView.smali`, `Cocos2dxRenderer.smali`, `Cocos2dxHelper.smali`, and GLView nested Runnables$3/$4.

| Activity transition | Bundled synchronous Java calls / queue submissions |
|---|---|
| AppActivity.onPause | Cocos superclass: Android Activity.onPause → Helper.onPause → GLView.onPause; then **AppActivity.nativePause** |
| GLView.onPause | submit Runnable$4 via inherited queueEvent, then setRenderMode(0); this override does **not** call platform GLSurfaceView.onPause |
| Runnable$4.run | view.renderer.handleOnPause |
| renderer.handleOnPause | if mNativeInitCompleted=false, return; otherwise Helper.onEnterBackground → nativeOnPause |
| AppActivity.onResume | Cocos superclass.onResume → makeImmersive → **AppActivity.nativeResume** |
| CocosActivity.onResume | Android superclass → hideVirtualButton → resumeIfHasFocus |
| resumeIfHasFocus | only if hasFocus: hideVirtualButton → Helper.onResume → GLView.onResume |
| GLView.onResume | platform superclass.onResume → setRenderMode(1) → submit Runnable$3 |
| Runnable$3.run | renderer.handleOnResume → Helper.onEnterForeground → nativeOnResume; no equivalent renderer mNativeInitCompleted check in this method |
| onWindowFocusChanged | Cocos superclass call, store hasFocus, call resumeIfHasFocus; AppActivity additionally makes immersive UI on focus gain |
| AppActivity.onStart | superclass.onStart → setStateStart → JVM analytics/platform and other manager setup |
| AppActivity.onStop | setStateStop → superclass.onStop |
| AppActivity.onDestroy | superclass.onDestroy → nativeDestroy → org.fmod.FMOD.close |

Helper.onPause/onResume update sActivityVisible and accelerometer/compass services. Helper.onEnterBackground/Foreground call the separate Java Cocos2dxSound and Cocos2dxMusic handlers. These Java audio helpers are not equated with native GameTimeline or the FMOD provider.

Focus loss alone does not call native pause in the inspected focus method. Focus gain can submit the renderer resume Runnable independently of AppActivity.onResume. If Activity.onResume has no focus, its Cocos GLView-resume branch is skipped, while AppActivity's own nativeResume is still called after returning from the superclass. Actual Android callback selection/timing is outside coverage.

### 3. What ordering is, and is not, established

The superclass pause path **submits** Runnable$4 before AppActivity.nativePause is invoked. It does not wait for that Runnable. Resume likewise may submit$3 before the app-specific nativeResume call. Both Runnables retain only the view reference and call the renderer when run; they do not capture a GameTimeline timestamp.

The full platform GLSurfaceView GLThread/event-loop implementation is absent. Submission order, synchronous Java order and native execution order are therefore separate facts. Controlled tests execute both app-first and renderer-first native pause/resume orders; neither is described as a measured Android scheduling policy. No automatic CANCEL, touch-queue drain, hardware latency distribution or extra lifecycle serialization is invented.

Director's `director_before_update`/`director_after_update` remain native custom notifications, not Android event-queue consumers.

## Native lifecycle JNI handlers

### 4. Export identities and distinct effects

| JNI export | Main VA | Original effect / boundary |
|---|---|---|
| AppActivity.nativePause | `18a015c` | if native-ready global1bf9040==1: optional app+10 AudioManager suspend; set pending latch1bfbe98=1 |
| AppActivity.nativeResume | `10a09fc` | requires native-ready and pending latch==1; optional AudioManager virtual+3a8 resume; clear pending latch |
| AppActivity.nativeDestroy | `1887d50` | if ready and app/app+b0 exist: tail-call11b0b28 on that subsystem; not a direct GameScene destructor call |
| Cocos2dxRenderer.nativeOnPause | `e0e5f4` | if Director.GLView nonnull: application singleton virtual+18, then dispatch event_come_to_background |
| Cocos2dxRenderer.nativeOnResume | `f4f2e0` | if GLView nonnull: application virtual+20, then dispatch event_come_to_foreground |
| AppActivity.notifyNativeStartupComplete | `196f7c0` | writes1 to field+60 of object referenced by global1beb7e0; **different from1bf9040** |

The app-context native-ready global is written1 at `16dc408`, after the enclosing native initialization work; that whole initializer is not executed here. The separate notifyNativeStartupComplete method is called from Java `AppActivity.startSceneLoadFinished`. Renderer mNativeInitCompleted is yet another flag, set after nativeInit returns in onSurfaceCreated. These three completion mechanisms are not interchangeable.

AppActivity nativePause's original `12a7aa8` forwards AudioManager+2c0 provider virtual+b8. NativeResume uses original AudioManager virtual+3a8=`ea630c`, forwarding provider+c0. Neither successful app-specific JNI path calls the model or timeline pause wrapper. A native-isolated app-only test confirms this distinction: pause at wall1000 requests suspend; after advancing to61000 and calling original timeline update, E becomes61000, model+138 remains0 and Director remains running. This is not the normal full Android lifecycle sequence and does not assert a deployed60s timing jump.

**Provider-library addresses, instruction-backed:** AppActivity.setStateStart=`libfmodProvider.so:0x21b38` forwards its global FMOD System to mixerResume through PLT4b6f0; setStateStop=`0x3f0d0` forwards to mixerSuspend through PLT4b700. These onStart/onStop interfaces are separate from the main-library pause JNI, renderer events and BGM pause/seek requests. Actual FMOD mixer/hardware state is not executed.

### 5. Joined renderer-background path — Native-integrated

Original singleton `d7654c` reads1be4b90. The fixture object carries the original **AppDelegate vtable1a9a2d0**, whose background virtual+18 resolves to **f46250**:

```text
e0e5f4
  → d7654c → AppDelegate.virtual+18 = f46250
      → Director.runningScene(+140)
      → original dynamic_cast Scene → GameScene
      → GameScene.virtual+510 = 165211c(scene,true,true)
          → virtual+520 = 1503bf8, reads scene finished latch+49a
          → 10f5288 original UILayer pause-menu acceptance
          → 190cf7c original UI listener-pause helper
          → scene+4b0 = true
          → e31764(model,true) → 9e74f4(timeline,true)
      → Director.virtual+20 = 1091204, stopped+220 = true
      → optional FinaleSongIntroLayer/other app service branches
  → original EventCustom construction ffa914
  → EventDispatcher1980970("event_come_to_background")
```

Background's GameScene cast is conditional. Scene absence, another scene type, scene+49a finished, unchanged pause state, or pause-menu rejection can bypass the model pause. Director animation stop is still reached in those inspected branches. Native ready1bf9040 is not a guard in this renderer JNI path; it belongs to the separate app-specific exports. A supplied ready0 guard matrix confirms renderer pause can reach the prepared scene independently, without claiming that every such flag/scene combination occurs in product startup.

The original pause-menu body10f5288 executes, not a supplied “accept=true” result. Its tested gate is UI+41b==0; +41b==1 executes the original reject branch. Prepared native Node hierarchy supplies the UI container/pause root, an already initialized decoration state at root+2d8, and a widget virtual+558 service. Actual UI layout/assets and decoration startup are outside coverage. Original Node add-child/action/container operations and the caller's acceptance branch execute. UI control objects passed to190cf7c are prepared and have no target listeners; the original helper and dispatcher operations execute.

### 6. Foreground and explicit gameplay resume — Native-integrated with UI boundaries

AppDelegate foreground virtual+20 is **170fafc**. It calls Director virtual+28=`979fe0`, which obtains time, clears stopped+220, records pthread_self at+1b8, updates animation interval and sets next-delta reset+178. It does **not** call GameScene.setPaused(false).

If a running scene exists,170fafc uses original Node scheduling helper159bdec to schedule two zero-delay callbacks on it. Callback bodies145502c (settings+1b/opaque app+48 service) andf1cc14→AudioManager1631d78→provider+b0 update are **instruction-backed targets**. Their registration executes, but the first foreground Scheduler tick in the reported trace does not invoke those callback bodies. Later timer draining is not claimed. The optional app+48/provider-update interfaces are prepared but unexercised here; no account subsystem is reconstructed. Foreground then performs its optional scene/app checks and renderer JNI dispatches `event_come_to_foreground`.

The tested gameplay resume uses original **PauseLayer callback1632d78**, identified by its original function-object RTTI/vtable1b7d700. It requires widget event enum2, PauseLayer active byte+2d8 and an AudioManager/provider predicate. Original `f6c964` forwards provider virtual+c8; provider-library function35dc4 reads its byte+10. The fixture supplies this predicate as true. A false-predicate test leaves scene/timeline/model paused and issues no seek/unpause. This widget event enum is not an Android MotionEvent action or a Cocos EventTouch action.

Successful callback path:

```text
prepared PauseLayer widget callback context + event enum2
  → original1632d78
  → original provider-predicate forwarding f6c964
  → PauseLayer.delegate(+2e0).virtual0(false,false)
  → original GameScene secondary vtable1ae7470 at scene+2f0
  → thunk17effac subtracts2f0
  → 165211c(scene,false,false)
      → b9e0d0 UILayer.hidePause boundary
      → original a48168 UI listener-resume helper
      → e31764(model,false) → 9e74f4
```

The function-object capture and PauseLayer/widget hierarchy are prepared, not produced by full PauseLayer asset initialization or the Widget input-dispatch system. UILayer.hidePause animationb9e0d0 is stubbed to return; its visual action/callback subtree is not claimed executed. No timeline/model pause bytes are assigned by this boundary. The GameScene/model/timeline resume instructions and audio seek/pause forwarding all execute normally. Thus this is an original native resume-control path under a supplied UI environment, not automatic foreground unpause.

## Director and GameTimeline interaction

### 7. Independent states and producers

| State | Confirmed producer / consumer |
|---|---|
| GameScene+4b0 paused latch | read/compared at165212c..38; stored by1652194; unchanged requests return early |
| GameScene+49a finished latch | getter1503bf8 blocks this pause transition |
| model+138 pause/input gate | e3176c stores requested bool; initial inputeec024 rejects while set |
| model+139 finished | ordinary model initialization clears the pair138/139 atfbfd54; frame completion/failure produces finished; not set by ordinary lifecycle tests |
| model+148 input mode/gate | initializerfbfe38 stores entry stack+10 i32; not written by the executed ordinary pause/resume path |
| timeline+2c paused | native9e75d4 stores requested bool |
| Director+220 animation stopped |1091208 sets1;979ffc clears; wrapper17371d8 returns while stopped |
| Director+130 scheduler paused | separate native Director pause1046fe4 sets1; resume12a3640 clears; native frame skips Scheduler/update notifications but can still visit scene |
| listener paused/enabled | model listener+70/+71; observed0/1 across ordinary pause/foreground/resume |
| dispatcher enabled |+124; observed1 throughout the ordinary tested lifecycle |

**Model+148 provenance:** original initializer prefixfbfd04..fbfe3c executes with entry stack+10 arguments0 and1 and writes those exact values. LDR atfbfdd4 obtains the argument; STR atfbfe38 produces the field. The rest of initialization is not rerun for this isolated ABI test. Its mode1 branch registers additional input-related data through1706048; full mode semantics remain outside scope. This is an initializer input, not a discovered Android-pause setter.

No executed ordinary lifecycle transition changes model+148 from0; a native memory-write observer over that field records no writes in the checked joined background/foreground/resume path. It pauses through+138 instead, leaving UP/CANCEL cleanup available. The mid-owned-contact0→1 mutation used to isolate011's gate behavior is **not reproduced by this normal interruption sequence**. A bounded search/trace is not proof that every indirect writer or reinitialization path is absent.

### 8. Timeline fields and native arithmetic

| Offset | Recovered role |
|---|---|
| +10/+18 | steady/system epoch words; ordinary updater uses origin's low32 bits |
| +20 R / +24 P / +28 C | raw time / pause reference / compensation |
| +2c/+2d/+2e | paused / steady-started mode / music-started latch |
| +30 O / +34 A / +38 B | combined offset / cursor adjustment / music-start effective anchor |

Original9e74f4 first calls original16c90bc. Pause records **P=E−A**, then requests BGM pause and sets the pause flag. While paused, native updates adjust C so E is preserved despite the advancing monotonic input. Resume calls the updater **while still paused**, so elapsed interruption time becomes compensation before the flag is cleared. If music has started it requests **seek=E−B**, then BGM unpause. If music has not started, the resume branch skips both seek and unpause. The actual epoch words are preserved in these tests; compensation changes.

The source of pause time is native effective time at callback execution, not the Java lifecycle submission time or a stored touch timestamp. No Android capture timestamp is substituted for E. Other explicit timeline-adjustment modes from005 remain separate.

### 9. A/D: running song, empty contacts,60-second delay

Fixture:009 minimal native two-tap chart at1000/raw1 and1150/raw2, N2/end1270, timing120/speed6, mode0/no ability; original spatial index and011 dispatcher; prepared GameScene/Director/Node UI environment. Timeline steady and music-started flags1, A/O/B initially0; origin low32=−3000 (fixture raw word0x00000000fffff448), system epoch0. No contacts initially. Original model frame1000 populates geometry. Driver wall milliseconds are converted to nanoseconds by the steady-clock service.

| Step | Wall / E | R / P / C | timeline paused; model138; scene4b0; Director220 |
|---|---|---|---|
| native running frame |1000 /1000|1000 /0 /0|0;0;0;0 |
| AppActivity.nativePause |1000 /1000|1000 /0 /0|unchanged; provider suspend, pending latch1 |
| renderer.nativeOnPause |1000 /1000|1000 /1000 /0|**1;1;1;1**; provider BGM pause(true,0) |
| wall advances; driver original timeline update |61000 /**1000**|61000 /1000 /60000|unchanged paused state |
| AppActivity.nativeResume |61000 /1000|same|provider resume; pending latch0; gameplay remains paused |
| renderer.nativeOnResume |61000 /1000|same|Director220→0; gameplay remains paused |
| original PauseLayer callback |61000 /1000|same|timeline/model/scene pause→0; seek1000,index0; BGM pause(false,0) |
| next original model frame |61001 /1001|61001 /1000 /60000|running |

All lifecycle JNI calls return normally through their original successful paths. No native model field supplies the pause outcome manually. Raw epochs, chart count/end, index header identities, engine mapping and score state remain preserved in the observed ordinary transition.

### 10. B: before music startup

Use the same prepared scene/model but origin low32=0, steady mode1, music-started0. Because the complete preroll scene/render fixture is unavailable, this scenario's initial/next time refreshes are **original timeline updates driven by the harness**, not successful whole model frames. A first attempted preroll model frame stopped at1554aa4 on missing surrounding scene/render state and is not counted as validation.

At wall1000, R/E=−2000. Original renderer background sets P=−2000, model/scene/timeline pause1 and Director stop1, and requests BGM pause(true,0). At wall61000, renderer foreground plus original resume-button path gives R58000/C60000/E−2000 and pause0, while music-started remains0. **No seek or BGM unpause request is added on that resume.** Next original timeline update at61001 gives E−1999. Startup/fade/audio anchoring beyond that negative-time interval is not newly executed here.

### 11. C: scheduler pause, animation stop and gameplay pause differ

Native Director pause **1046fe4** saves interval+100 to+104, calls virtual+18 with0.25, then sets+130=1. Resume **12a3640** restores the interval, clears+130, zeroes dt+e8 and sets next-delta-reset+178. Their virtual interval setterc348b4 can stop/restart animation through the real+20/+28 methods; the external Android interval setter remains supplied.

An isolated original Director-pause comparison leaves timeline/model/scene pause0 and Director stopped0. At wall1050, scoped original Director frame skips Scheduler (count0) but reaches one additional model frame, advancing E1000→1050. Native Director resume clears+130. This demonstrates the distinction without calling the wrong state a GameTimeline suspension; its product callers are not newly established as the Android lifecycle path.

Ordinary renderer background instead sets stopped+220=1 and leaves+130=0. Original wrapper17371d8 at wall61200 then invokes neither Scheduler nor model frame. After renderer foreground, the011-style scoped Director frame invokes Scheduler/ActionManager and model frame once while the GameScene/timeline remain paused: E stays1200. Its two custom notifications still are not Java queue drains.

### 12. Offsets, rejected transitions and callback ordering

- With O120/B−120, the joined running-song resume retains E1000 and requests **seek1120**, confirming E−B rather than E or raw elapsed time.
- Native ready0 suppresses app-specific suspend/resume latch work; direct renderer JNI can independently pause its prepared GameScene. Renderer Java initialization gating is a separate unexecuted Java condition.
- With no running scene, the renderer callback still stops/restarts Director; no model pause is observed. With scene+49a=1 or UI+41b=1, original GameScene pause rejects and Director still stops. Timeline/model remain unpaused in those supplied guard combinations; their complete product reachability is not claimed.
- Original resume-button provider predicate=false leaves model/scene/timeline paused and adds no seek/unpause. Same-state GameScene requests also return before repeating UI/timeline work.
- Four controlled combinations of app-first/renderer-first pause and app-first/renderer-first resume all preserve E1000 after60s and yield model pause0 after the explicit resume callback. Suspend versus BGM-pause order follows the supplied pause order; provider resume versus Director start follows the supplied resume order. They establish native order consequences, not thread races or Android scheduling probabilities.

## Contact and LogicColor ownership transitions

### 13. Ordinary arc retained through interruption — Native-integrated

Reuse009's original arc factory/color/geometry/checkpoints and native index; replace its initially prepared contact with an empty vector before testing. Original011 JNI creates Android42→engine slot0→generated gameplay2000 at design(640,210), timestamp123. Arc1000..2000, linear(.5,.5), tempo120/speed6/density1, interval250, N3/end2500; orthographic1280×720 Camera Z900, original feedback latch shell. No owner, active/contact flag or membership is supplied.

| Step | E / last model frame | Retained / engine mask | owner / active | PURE / health |
|---|---|---|---|---|
| after frame1125 |1125 /1125|1 /1|2000 /1|1 /26.866666793823242 |
| background at wall1200 |1200 /1125|**1 /1 preserved**|**2000 /1 preserved immediately**|unchanged |
| stopped wrapper at61200 |stored1200 /1125|1 /1|2000 /1|unchanged; no frame/Scheduler |
| renderer foreground |stored1200 /1125|1 /1|2000 /1|gameplay still paused |
| foreground native Director scope |1200 /1200|1 /1|**2000 /0**|unchanged; Scheduler count1/model count4 overall |
| original resume-button callback |1200 /1200|1 /1|2000 /0|unchanged |
| model frame at wall61201 |1201 /1201|1 /1|**2000 /1**|unchanged |

The pause-time model frame resets per-frame activity and continuous input is gated while paused; ownership/retention survive. The next running frame recomputes activity from the same native Touch. Listener paused/enabled remains0/1, dispatcher enabled1, model+148 remains0, index-header pointers remain identical, initial Touch coordinates/ID/timestamp remain preserved. No new map, contact vector membership or spatial index is created by these lifecycle callbacks.

This is preservation, not an assertion that physical fingers remain pressed across Android backgrounding. Android may deliver later events; this expedition does not invent them.

### 14. Explicit release/cancel before and after background

Separate runs deliberately deliver original JNI terminal events; the driver does not pretend Android generated them:

| Controlled event | Observed native result |
|---|---|
| CANCEL before pause, E1125 | owner→−1, release1125, retention/map/mask empty; later lifecycle does not recreate contact |
| UP after pause, wall61200/stored E1200 | original end dispatch still reaches cleanup; owner→−1, release1200; map/mask/retention empty |
| CANCEL after pause, same clock state | same ownership/contact result through separate action3/cancel callback |

Model+138 rejects initial judgment/continuous activation but does not block the end/cancel operators' cleanup gate. They inspect+148, which stays0 in this ordinary path. Thus normal backgrounding does not create011's artificially changed+148 cleanup suppression. Active arc byte can remain1 immediately after UP/CANCEL; the following frame clears it. Neither immediate byte persistence nor later recomputation is confused with ownership release.

The prior release/reacquisition timing rule is not rederived here. Release timestamps come from current stored E exactly as011 showed; the lifecycle pause updates E to1200 before the deliberately delayed terminal events in these tests.

### 15. Hold retention and latch preservation

Use011's original full-initialized hold fixture1000..2000/raw3, N3/end2500, native records1250/1500/1750; original JNI supplies generated3000 at(740,360). No latch/contact flag is assigned. Native frame1125 has initial latch+a8=1, contact bytes+64/+65=1/1 and PURE1.

Background at1200 preserves latch1/contact bytes1/1 and one retained/mapped Touch. After60s, foreground scoped Director/model frame at frozen E1200 yields contact bytes0/0 while retaining latch1 and the Touch. Original resume-button callback plus frame1201 restores bytes1/1 with the same generated ID and no new begin. PURE stays1 and health is unchanged during this interruption. This validates retained-contact recovery; a complete interrupted-hold final-result replay is not claimed by this short fixture.

### 16. Listener removal and destruction boundaries

Instruction-backed ordinary model destructor16d3f20 calls **876f6c(EventDispatcher,model.listener)** at16d3f64, then other teardown/reference-release work. A new isolated removal test executes that original dispatcher routine on the actual registered listener while owning an arc. Listener registered+60 becomes0; engine mapping/retained pointer/owner remain. A subsequent original JNI UP clears engine mapping/mask but makes **zero gameplay cleanup calls**, leaving the retained pointer/owner in that still-live model fixture.

This is not a complete scene teardown, production leak or bug. Actual model destruction later releases retained Touch references and chart ownership; reference services are supplied and actual destruction of the chart/color/pools is not established. Removing a listener by itself is not equivalent to dispatching CANCEL or calling f9a50c. No assertion is made that product scene replacement leaves the test model alive in that state.

AppActivity.nativeDestroy additionally has its own opaque app+b0 subsystem interface. With ready1, a prepared subsystem state+c=1, flag+8=0 and external virtual+18 returning, original1887d50→11b0b28→e33830 executes, sets state+c=3, records native clock2000 at+10 and clears+8. Contacts/owner remain in this supplied fixture. **The actual subsystem virtual+18 is a boundary**, so this is not proof that full nativeDestroy cannot indirectly clean gameplay. State7/flagged subsystem networking branches, actual FMOD.close, full GameScene destruction and complete spatial-map reclamation remain unexecuted.

## Native execution traces and regression

### 17. Uninterrupted versus interrupted two-tap run

Same prepared N2 chart, input positions(290,360)/(540,360), ordinary mode0/no ability, original JNI/listener input and native score/gauge/result code. First DOWN at E1000; UP at E1050; second DOWN/UP at E1150; native finish frame1271. The interrupted run inserts the joined app/renderer pause at wall1050, advances the synthetic clock60,000ms, executes both native resume callbacks and original PauseLayer resume control, then delivers the same effective-time input schedule. The first Touch is retained through pause and removed by the scheduled UP after gameplay resume. No epoch/score/contact compensation is assigned manually.

| Observation | uninterrupted | interrupted |
|---|---:|---:|
| final effective time |1271|1271|
| PURE / recorded LOST / final LOST |2 /0 /0|2 /0 /0|
| live health |80.4000015258789|80.4000015258789|
| native final score |10,000,002|10,000,002|
| result category / finished |3 /1|3 /1|
| retained contacts / input mode |0 /0|0 /0|

The interrupted run logs provider suspend, BGM pause(true), provider resume, seek1050 and BGM pause(false). Native result snapshot1600bb0 is driver-invoked after native model completion, as in009–011; score/category queries1315038/12a5574 execute. No full real-scene result-persistence path is claimed.

### 18. Execution inventory, hooks and excluded operations

Unicorn2.1.4, Capstone5.0.9, pyelftools0.33. Main ELF PT_LOAD mapping and RELATIVE relocations; main image0..0x2100000; supplied arena0x4000000..0x6000000, stack/TLS to0x6100000; SP0x60df000, TPIDR_EL0=0x60f0000; return sentinel0x4000100;5M-instruction per-call budget. Synthetic callback addresses below are not ELF VAs.

Original functions that execute together include lifecycle JNI, AppDelegate virtuals, successful GameScene pause/finished guard, UILayer acceptance body10f5288, UI listener helpers190cf7c/a48168, model wrapper, timeline updater/pause logic, native AudioManager forwarding/ordinary seek, Director stop/start, pause/resume comparison functions, event construction/dispatcher, callback registration, the PauseLayer resume callback and selected Scheduler/ActionManager/GameScene frames. Native Touch mapping, contact ownership and judgment are reused original infrastructure, not host equations.

| Supplied object/service or hook | Role and limit |
|---|---|
| AppDelegate/global process setup | original vtable1a9a2d0 installed; singleton1be4b90, context/audio pointers and native-ready flag supplied; full application startup not executed |
| Director/view/model/chart/scene |011 prepared environment; original DisplayLinkDirector vtable1b5eaf8, running scene+140 and scene traversal+190 supplied; does not emulate Activity/GLThread |
| PauseLayer/UILayer/Node hierarchy | native Node constructors run; layout/widget captures/decoration initialized state supplied; original pause acceptance executes; widget virtual+558 returns via service |
| b9e0d0 | UILayer.hidePause visual-animation boundary only; returns; not a substituted model/timeline transition |
| provider callbacks `4000600/610/620/630/640` | BGM pause/seek, mixer suspend/resume, update request logging; original AudioManager wrappers execute; no FMOD backend |
| provider predicate `4000660` | bool from supplied provider+c8 interface, normally1; false test0; provider-library predicate body only instruction-backed |
| `4000650`, app+48 virtual+88 | prepared opaque foreground application service, unexercised by the reported first timer tick; no account/database initialization |
| `4000670`, app+b0 virtual+18 | opaque destroy-subsystem callback in the isolated nativeDestroy test; no real subsystem teardown |
| fc3450 | Android application animation-interval setter at AppDelegate+28; log/return; native Director bookkeeping still executes |
| a4227c / f09110 | prepared Director getter and1280×720 external dimension service |
| 1a6dc60 / 1a6e5c0 | controlled steady nanoseconds / gettimeofday; no device clock measurement |
| pthread_self1a6ec30 | supplied stable thread identity0x1234, recorded by native Director start; this is not a clock |
| allocation `1a6d9c0,1a6dd40,1a6e090,1a6df10,1a6ee10` | zeroed aligned bump new/malloc/calloc; no allocation failures |
| deletion/reference `1a6d9e0,1a6e0a0,1a6ded0,121a0ec,147fe48,d6dc98,10ac6e8` | no real reclamation/Ref pools; original callers observed |
| memory/string `1a6d9d0,1a6daf0,1a6db30,1a6dad0,1a6da50,1a6db80,1a6da80` | host byte/memory/string-copy/compare primitives with libc++ layout; no substituted native lifecycle control flow |
| dynamic_cast1a6db90 | original RTTI single-inheritance identity/base-chain resolver for tested Scene→GameScene; other inheritance/casts not general ABI validation |
| audio107af5c / model delegate4000200 | external SFX/UI/finish notifications suppressed; real judgments/gauges retained |
| inherited19f2e40 | return, matching inspected original RET; not newly claimed executed body |
| JNI array callbacks4000400/410/420 |011 array length/int-region/float-region services used for deliberate input/cancel tests |
| Director scope1794004→17940d0, stop17940f8 | skip renderer/matrix-stack preparation and later rendering/counter increment; excludes a full nativeRender frame |
| GameScene18be380→18be470; base draw129c924 | skip HUD/drawing while preserving model call, once-per-counter guard and stamp store |
| arc feedback shell | virtual+530 calls original155241c; GPU subtree absent |

The hold fixture's native AFF construction additionally uses010's documented ASCII/string/number services: substring1a6dc20, memchr1a6db40, string compare/append/push/erase1a6da60/1a6db00/1a6db20/1a6dda0/1a6e1a0, stream1087f14/b06728, number extraction1a6e210/230, atoi1a6dd80, atof1a6e150, whitespace1a6e200 and ctype GOT1b96168. This expedition does not claim fresh real metadata loading or native libc++ numeric parsing.

Native instruction landmarks include STRB model138 at e3176c; timeline paused flag at9e75d4; pause compensation updater16c9104..10c; resume E−B subtraction9e75b4..bc; Director stop STRB1091208, start clear979ffc and reset97a020; scene finished LDRB1503bf8; original secondary-base subtraction17effac; input-mode LDR/STRfbfdd4/fbfe38. Valid scoped tests return normally; unexecuted exception/error branches are not fabricated as successful paths.

## Recovered pseudocode

```text
# Java: Instruction-backed; not an executed Android queue
AppActivity.onPause():
    super.onPause():
        Activity.onPause(); Helper.onPause()
        GLView.onPause(): queueEvent(Runnable4); setRenderMode(0)
    nativePause()                                # synchronous Java call after submission
Runnable4.run():
    if renderer.nativeInitCompleted:
        Helper.JavaSoundMusic.background()
        renderer.nativeOnPause()

AppActivity.onResume():
    super.onResume():
        Activity.onResume(); hideSystemUI()
        if hasFocus:
            Helper.onResume()
            GLView.super.onResume(); setRenderMode(1); queueEvent(Runnable3)
    makeImmersive(); nativeResume()
Runnable3.run(): Helper.JavaSoundMusic.foreground(); renderer.nativeOnResume()

# Native-integrated under the stated environment
AppActivity_nativePause():
    if nativeReady != 1: return
    if app and app.audio: app.audio.provider.suspend()
    pendingAppResume = 1
AppActivity_nativeResume():
    if nativeReady == 1 and pendingAppResume == 1:
        if app and app.audio: app.audio.provider.resume()
        pendingAppResume = 0

renderer_nativePause():
    if Director.GLView == null: return
    AppDelegate.background():
        if runningScene is GameScene: runningScene.setPaused(true, forceUI=true)
        Director.stopAnimation()                 # +220=1, not +130 pause
        optional_other_scene_and_app_services()
    dispatch("event_come_to_background")          # notification, not CANCEL or queue drain

GameScene.setPaused(p,forceUI):
    if scene.paused4b0 == p or scene.finished49a: return
    if p:
        if not native_UILayer_showPause(forceUI): return
        native_UI_listener_pause()
    else:
        UILayer_hidePause_visual_boundary()
        native_UI_listener_resume()
    scene.paused4b0 = p
    model.pause(p):                              # e31764
        model.inputPause138 = p
        timeline.pause(p):                       # 9e74f4
            timeline.update()                   # still uses prior paused state
            if p:
                P = E - A
            else if musicStarted:
                native_audio_seek(E - B)
            if p or musicStarted: native_BGM_setPaused(p,index0)
            timeline.paused2c = p
    optional_scene_delegate_notification()

renderer_nativeResume():
    if Director.GLView == null: return
    AppDelegate.foreground():
        Director.startAnimation()                # clears220, resets next delta
        schedule_native_foreground_service_callbacks()
        optional_other_scene_and_app_services()
    dispatch("event_come_to_foreground")
    # No automatic GameScene.setPaused(false) in this tested callback.

PauseLayer_resume_widget_callback(eventEnum):
    if eventEnum != 2 or not pauseLayer.active: return
    if not native_provider_predicate(): return
    play_UI_sound_boundary()
    original_delegate_thunk → GameScene.setPaused(false,false)

while timeline.paused:
    native_update_adjusts_C_to_preserve_E()
while Director.stopped220:
    original_frame_wrapper_skips_Scheduler_and_scene()
after foreground but before gameplay resume:
    native_Scheduler_and_scene_frames_can_run()
    E remains frozen; per-frame contact flags clear under model.pause138

# Contacts: existing native dispatch, now exercised around lifecycle callbacks
background_or_foreground_alone:
    no_synthetic_CANCEL()
    # tested engine map/retention/LogicColor owner preserved; mode148 unchanged
deliberately_delivered_JNI_UP_or_CANCEL:
    native_GLView_clears_mapping()
    if gameplay_listener_registered and model.mode148 == 0:
        native_f9a50c_removes_retained_pointer()
        native_13db7a0_releases_matching_owner(contactID,stored_E)
next_running_model_frame:
    recompute_hold_arc_contact_state_from_remaining_retained_Touches()

# Native destroy interface: only the bounded subsystem path is executed
AppActivity_nativeDestroy():
    if nativeReady == 1 and app and app.subsystemB0:
        native_11b0b28_stop_subsystem()            # virtual18 boundary in fixture
# Full GameScene teardown/real Ref destruction is not implied.
```

## Remaining synthetic boundaries

The essential advancement is an original lifecycle-JNI→AppDelegate→GameScene→model→GameTimeline connection and an original resume-control callback, replacing manual pause-byte toggles. Android VM/GLThread delivery order, runtime singletons/startup, UI assets/widget construction, menu-dismissal animation, provider/platform calls, reference pools, full rendering and actual scene ownership remain supplied or unexecuted. Native calls are driver-scheduled; this does not turn them into real Android queue execution.

## Updated coverage matrix

| Interface |012 status | Limit |
|---|---|---|
| Activity→Cocos/helper/GLView Runnable lifecycle | Instruction-backed | platform queue/VM absent |
| App-specific JNI suspend/resume | Native-integrated to original provider forwarding | provider calls logged, backend absent |
| Renderer JNI→AppDelegate→GameScene→GameTimeline pause | **Native-integrated, ordinary guarded path** | prepared process/UI hierarchy and services |
| Foreground→Director restart/event/native callback registration | **Native-integrated scoped** | later scheduled bodies instruction-backed; renderer work excluded |
| PauseLayer callback→delegate→GameScene→timeline resume | **Native-integrated scoped control path** | prepared Widget/function capture; hide animation supplied |
| Delayed-time preservation and E−B seek | **Native-integrated** | controlled clock, offset/anchor fixture |
| JNI-created hold/arc across pause/resume and terminal cleanup | **Native-integrated** | prepared geometry/camera/render shell |
| Basic uninterrupted/interrupted gameplay result | **Native-integrated regression** | two-tap schedule; snapshot driver-invoked |
| Input-mode producer / listener removal | Native-isolated plus instruction-backed production callsites | every writer/full destruction not established |
| App nativeDestroy / onStart/onStop FMOD interface | bounded native subsystem execution / provider-library instruction-backed | actual subsystem virtual/FMOD teardown unexecuted |
| Full scene replacement/map reclamation | partial/Unknown | no memory-leak or ownership-completeness claim |

## Unresolved Mysteries

1. Actual platform GLThread queue policy, lifecycle callback concurrency, device timing and cancellation delivery. The bundled Java does not supply the platform implementation.
2. Complete UI state/layout initialization, pause-menu rejection writers, real Widget delivery/animation sequence and resume-predicate production flag changes. Successful scoped control flow is not every pause mode.
3. All input-mode148 producers/consumers and rare modes or reinitialization while contacts exist. Normal tested lifecycle never changes this field;011's synthetic stale-state combination remains unproven in production.
4. Full nativeDestroy subsystem behavior, GameScene replacement/destruction, actual reference reclamation, spatial-map owners, action teardown and relationship to persistence/results. No leak, bug or universal owner release is inferred from incomplete teardown.
5. Pre-start full model/render lifecycle and all startup/fade branches; scenarioB validates timeline/lifecycle suspension before music, not full preroll rendering.
6. Real Java Cocos sound/music, FMOD mixer/audio cursor/hardware, account/storage/network effects and special scene classes. Those services are deliberately bounded. Flick remains outside scope and gameplay-unproven.

## GitHub Status

Authorized publication is this new012 report and an append-only012 context entry, based on `e4deb6866843f523425a8be1d47e404888f93fc0`. Reports001–011, historical context, README, instructions, original archive/binaries/assets remain unchanged. Harness/trace/provider copies stay scratch intermediates and are not commit contents. Before committing, recheck for another012 publication; the headquarters return records exact publication SHA, pinned read-back equality and final starting-tree comparison. No future self-referential commit SHA is invented here. Expedition013 is not initiated.
