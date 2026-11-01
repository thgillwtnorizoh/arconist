# Expedition 041 — Native Gameplay Interruption, Pause/Resume & Contact-State Continuity

Date: 2026-11-01. Headquarters selected Scout 002 S2-C07 as **G-017**.

## Result

**Verified for the ordinary native-created hold scope, including the optional CANCEL comparison.** Four independent native scenes establish original hold construction and checkpoint production, JNI contact creation, renderer background/GameScene pause acceptance, stopped-Director behavior, frozen native effective time, foreground without automatic gameplay resume, and original PauseLayer callback/delegate resume. Retaining the first contact and releasing/repressing through either UP or CANCEL all produce three genuine native accepted checkpoint callbacks with identical score/gauge outputs and complete cleanup.

A consequential integration difference from012 was found and closed: the native-created scene owns actual pause UI input machinery. Keeping012's inert hide-menu boundary permits a retained contact to recover but prevents the new DOWN from reaching gameplay. Executing the **original** `0xb9e0d0 → 0x18d60cc` dismissal path resolves that limitation. No Python listener removal, UI-active reset or gameplay-state repair is used. Original UI/callback objects are produced by the scene, rather than replaced by012's prepared hierarchy/capture.

All cases finish at E1627, with PURE3/shining3/FAR0/LOST0/combo3, score10000003 and live health80.5999984741211. Completion/results/SQLite and the optional arc case are not executed. Android VM/GLThread delivery, physical finger persistence and audio output remain outside coverage.

## 1. Preparation and original identity

Parent/main was verified as `9cacc57053062dc3554e90313c92e854d4aefae1`; no041 publication existed. The112 immutable parent blobs were restored after workspace maintenance and individually matched their Git blob hashes before changes. Standing introduction, cumulative context/backlog, supplied S2-C07 mission, relevant005/009/011/012/018/022–024/026/028/035/037/038/040 evidence and current harness were reviewed. The complete Scout002 advisory is not a repository artifact; the supplied mission provides this candidate's authorization and scope.

External original ZIP member `lib/arm64-v8a/libcocos2dcpp.so`,29217504 bytes, freshly verifies:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Pinned Python3.12/Unicorn2.1.4/pyelftools0.33 are retained; Capstone5.0.7 is only an external disassembly aid. All instruction addresses are original ELF VAs; heap addresses below are observations, not fixed regression expectations. No original assets or generated traces are published.

## 2. Native scene, hold and input production

Every fresh emulator uses unchanged ordinary sayonarahatsukoi/difficulty0/base/no-purchase/mode0/speed40 tenths/null modifiers/40 zero PlayParameters. The immutable026 `native_hold.aff` is reused without byte changes:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
hold(1000,2000,3);
```

Fixture SHA-256 is `603c78c37c228436bf47e37d0826aa8b2efa0d5c93177b3fefbfb253379cee6e`; original complete-text MD5 is `e769e8e050230862964f67f47754c2f5`.

Original static1930604/registry1054f24 initialization, ordinary solo eligibility/entry, native GameScene allocation/constructor/loading and initializer return1 execute. Director activates that same GameScene. Original whole AFF/parser/runtime construction allocates one LogicHoldNote, type `13LogicHoldNote`, vtable1b2eda8. Builder operands at18649b8/return18649bc preserve1000–2000 and raw lane3→native lane4. Native checkpoint generation throughd925fc produces records1250/1500/1750, each weight1/unresolved0; interval250, N3 and chart end2500. Original spatial insertion includes the hold in group0 buckets0/1. No hold, checkpoint, denominator or index membership is injected.

Representative independently reproduced relationships:

| Object | Observed pointer |
|---|---|
| GameScene | `0x4327c40` |
| Model / Timeline | `0x4355f80` / `0x4356100` |
| Chart / hold | `0x4331880` / `0x4332140` |
| ScoreState / gauge | `0x4356140` / `0x43562c0` |
| Native UILayer / PauseLayer | `0x44e2d80` / `0x4c63800` |
| Resume function capture | `0x4e470b0` |
| Native secondary delegate | scene+0x2f0=`0x4327f30` |

Each case starts with a new Uc/image/globals/heap. Repeated addresses arise from deterministic independent allocation and are not cross-run identity assertions.

Native primary Camera projection `0xbdbb70` maps the ordinary lane4 input-plane target(212.5,0,0) to JNI(775.8657836914062,617.340705871582), using1280×720/Y-up conversion. Original unprojection and lane return(4,0) execute. JNI DOWN42 at native E1000 creates the native Touch and latch; E1001 continuous processing activates it. Initial latch+0xa8 and activity+0x64/+0x65 are independently observed. No prepared geometry or accepted lane is returned by a host hook.

## 3. Lifecycle owner and actual native UI prerequisites

`interruption_services.py` isolates the documented012 AppDelegate/platform/audio facade. It supplies a small AppDelegate object carrying original vtable1a9a2d0 at original singleton1be4b90, and removes the old generic d7654c facade so the **original singleton getter** executes. Its actual virtual+18/+20 targets aref46250/170fafc. Full AppDelegate/Android application startup is not claimed. Native-ready globals are not assigned, and optional AppActivity nativePause/nativeResume are not executed.

The **GameScene and UI are not supplied substitutes**. Original scene+3c0 owns a real UILayer, whose+300 points to the actual PauseLayer; TrackLayer/control helpers are native products. UILayer rejection byte+41b and scene finished+49a are observed0. PauseLayer active+2d8 is originally0. Its delegate+2e0 already points to the same scene+2f0, with original secondary vtable1ae7470 and thunk17effac. The diagnostic does not write these relationships or UI gates.

The native resume function object is found by read-only inspection, then matched to its original construction writes. Original stack capture ata5b8ac and copy writer **a56170** produce vtable1b7d700/captured PauseLayer, including the heap capture0x4e470b0. Its virtual+30 is1632d78. The separately located clone candidatef2914c is not needed or claimed executed. The driver supplies Widget enum2 to this actual native callback; complete Widget event transport is outside coverage. No synthetic resume capture or active byte is prepared.

External audio support supplies provider pause+30, seek+40, update+b0 and ready predicate+c8=true, as bounded in012. The original AudioManager wrappers remain enabled. A source-backed empty query header at AudioManager+1a8 supplies the missing facade pointer consumed by10884ac→ae2138. Native header+30==0 returns false, avoiding an unrelated loop/fade branch while retaining ordinary seek forwarding. This is external audio-query state, not a recovered full AudioManager producer or account subsystem. Android interval setterfc3450 remains an inert platform service. No FMOD output or hardware readiness is inferred.

## 4. Original background acceptance and state producers

At native E1200, the retained Touch is active and first checkpoint resolved. Original renderer background executes:

```text
e0e5f4 → original d7654c getter → AppDelegate f46250
  → original running-scene RTTI check → same GameScene165211c(true,true)
  → original finished guard and UILayer10f5288 acceptance
  → native PauseLayer show/decoration and UI listener helper190cf7c
  → scene/model/Timeline pause
  → original Director stopAnimation1091204
  → native event_come_to_background construction/dispatch
```

No pause-acceptance result is stubbed. Original bd4e90 sets PauseLayer active0→1. Original show/add-child/control machinery executes on the native-created hierarchy.

| Native state | Actual producer | Background / explicit resume |
|---|---|---|
| Scene+4b0 |1652194 |0→1 /1→0 |
| Model+138 |e3176c |0→1 /1→0 |
| Timeline+2c |9e75d4 |0→1 /1→0 |
| Timeline pause reference P |9e7584 |1200 |
| Director+220 |1091208 /979ffc |0→1 /1→0 on foreground |
| PauseLayer+2d8 |bd4e90 /18d60fc |0→1 /1→0 on native dismissal |

Model+148 remains0 with no observed writes. Director scheduler-pause+130 remains0; it is distinct from animation stopped+220. Gameplay listener remains registered/enabled/unpaused at priority20 and dispatcher enabled1. Original helper calls pause/resume UI controls without silently making the Model listener the lifecycle pause bit.

Both native EventCustom notifications are constructed throughffa914 and dispatched through1980970 with type6 to the same dispatcher: event_come_to_background and event_come_to_foreground. They are notifications, not queue drains or fabricated CANCEL events.

## 5. Stopped wrapper, foreground and Timeline compensation

Music starts through the inherited native lifecycle at wall9452/E0, origins6450/6450, O0/A0/B0 and compensation C2. Each case advances through original guarded Director/GameModel frames. Initial held contact has Android42→slot0→generated ID0; initial timestamp987042.

At background wall10652/E1200, R1202/P1200/C2. The external clock then advances60000ms. Calling original Director wrapper17371d8 with the actual Director observes stopped+220 and returns: **zero additional1793f8c/Scheduler13d3f44/Model10a7550/Timeline16c90bc entries**. Its cached R/C/E remain unchanged. This is not a direct Director call bypassing the stop guard.

Original renderer foregroundf4f2e0→170fafc→979fe0 clears stopped state, resets animation timing and registers its native callbacks. It does not clear gameplay pause. The next original Director frame runs the paused Model and native Timeline updater: R/C advance together and E remains frozen.

| Step, interrupted cases | Wall | R / P / C | E | Scene / Model / Timeline paused | Hold activity |
|---|---:|---|---:|---|---|
| Background complete |10652 |1202 /1200 /2 |1200 |1 /1 /1 |1 /1 |
| Stopped wrapper after delay |70652 |1202 /1200 /2 |1200 |1 /1 /1 |1 /1 |
| Foreground, before frame |70652 |1202 /1200 /2 |1200 |1 /1 /1 |1 /1 |
| Foreground paused frame |70652 |61202 /1200 /60002 |1200 |1 /1 /1 |0 /0 |
| Explicit native resume complete |70652 |61202 /1200 /60002 |1200 |0 /0 /0 |0 /0 |
| Next running frame, contact retained |70653 |61203 /1200 /60002 |1201 |0 /0 /0 |1 /1 |

Origins/O/A/B are preserved; compensation is native-produced, not assigned. The stopped interval itself performs no update; absorption into C occurs when native paused updating resumes. Score and resolved records remain unchanged throughout the interval.

## 6. Resume callback and the necessary original dismissal consumer

Original callback1632d78 sees enum2 and the natively active PauseLayer. Original f6c964 forwards the supplied provider+c8 predicate; then original secondary delegate/thunk17effac reaches **the same GameScene**165211c(false,false), followed by native UI listener resume, e31764 and9e74f4. Tail-call return addresses may retain the external callback invocation sentinel; they are not invented ordinary function-call LRs.

Timeline resume updates while still paused, then computes seek **E−B=1200**. Original fbf24c forwards provider+40 with1200/index0;18c9ba4 forwards provider+30 withfalse/index0. The audio request ledger is pause(true), readiness predicate, seek1200, pause(false). These are observed original requests at supplied provider interfaces, not measured playback.

A significant boundary mismatch was found in the first integrated run. Reusing012's inert hidePauseb9e0d0 service allowed the same retained Touch to resume, but after UP/CANCEL a new JNI DOWN was only engine-mapped: generated ID still default0, no second194ff80/eec024 entry and no Model retention. Gameplay pause flags/listener state were already correct. The actual modal UI created in these scenes was still participating in input.

Read-only disassembly showed that the real hide path first calls18d60cc, whose **18d60fc** clears active+2d8 and removes its decoration child through original Node logic, before scheduling remaining hide/fade actions. The final scenario removes the inert hide boundary in its own fresh instances and executes **all of b9e0d0/18d60cc normally**. New-contact delivery then succeeds at E1300. No host active-state change, listener removal, parent repair or timing workaround is supplied. This is the directly necessary original consumer, not a new renderer reconstruction.

The previous failed run remains a bounded diagnostic of that supplied-interface omission; it is not a game-engine failure or a claim012's prepared hierarchy behaved identically. Successful final traces are independent, not assembled from earlier probes. Detailed identity of every modal listener is not generalized from this contrast.

Unlike012's first paused foreground tick, later frames here also execute the native scheduled145502c/f1cc14/1631d78 foreground service bodies once; provider update+b0 is logged at E1201. No new callback body is substituted.

## 7. Four contact histories and hold activity

All required cases use the same native chart and equivalent gameplay-time cadence:1000 DOWN,1001 activity,1125 checkpoint1,1200 comparison,1201,1300/1301,1375 checkpoint2,1625 checkpoint3,1626 terminal UP,1627 reset. Interrupted cases additionally have the paused foreground frame at frozen1200. Deliberate histories are not falsely described as identical contact states.

### Uninterrupted control

One JNI Touch remains retained through all checkpoints. Its latch becomes1 at DOWN1000; activity remains0/0 until original frame1001. It sustains every checkpoint. UP1626 empties retention/mapping; frame1627 clears activity while latch1 remains.

### Contact retained through background/foreground

No UP/CANCEL/MOVE or new DOWN is supplied during interruption. The exact Touch pointer, generated ID0, timestamp and engine mapping survive. The paused foreground frame clears activity, not retention or latch. After explicit resume, original14557b4 activates that **same pointer** at E1201 without another DOWN and sustains the remaining checkpoints.

### UP during pause, followed by fresh contact

Original JNI UP42 after background at E1200 clears map/mask/slot and invokes original gameplay terminal cleanupf9a50c despite gameplay pause. Latch1 and activity1/1 remain immediately; the paused foreground frame clears activity0/0. Foreground/resume creates no automatic contact.

At E1300, original JNI DOWN43 creates a distinct Touch, slot0 reused, generated ID1. Native hold latch remains1; activity is0/0 until frame1301. The original continuous activation receives that replacement pointer and sustains the remaining checkpoints. This is reacquisition, not survival of Touch42.

### Optional CANCEL during pause

Existing InputArrays supplies one ID/X/Y/pressure array set to originald8dc50, not an internal cleanup call. Original1556de4 terminal path dispatches Cocos action3; UP uses action2. Both remove engine state before terminal dispatch and clear Model retention through original cleanup. CANCEL does not clear the persistent hold latch. Subsequent genuine DOWN43/ID1 and E1301 activation agree with the UP case. No Android-generated CANCEL is inferred.

Representative Touch pointers: first0x4ecc340 in each independent heap; UP replacement0x4ed2e40; CANCEL replacement0x4ed2f40. Assertions compare native relationships within each run, not hardcoded addresses.

## 8. Native checkpoint and recorder reconciliation

Every case observes three native resolved writes at **f80924**, each before0→value1/size1 for a distinct record. Original guardf80904 later reads resolved1, and no record resolves twice. Accepted recorder1730290 is called from **LRf809a8** with the same original hold at E1125/1375/1625. Miss recorder868e54 is never called. No pause/terminal event awards a judgment.

| Native E | Resolved records | PURE / shining / combo | Score | Live H |
|---:|---|---|---:|---:|
| 1125 |1 /0 /0 |1 /1 /1 |3333334 |26.866666793823242 |
| 1375 |1 /1 /0 |2 /2 /2 |6666668 |53.733333587646484 |
| 1625 |1 /1 /1 |3 /3 /3 |10000003 |80.5999984741211 |

FAR/LOST remain0. These are original recorder/gauge outputs and delta observations, not final-result reconciliation or host scoring arithmetic.

Native activity reset1866038 and retained-contact activation14557b4/14557ec are observed independently from latch writes. Retained control/interruption cases have9 activation calls in this cadence; UP/CANCEL cases have7 because no Touch exists at1201/1300. Latch survival alone never substitutes for an activation call or accepted checkpoint.

At terminal UP1626 all mappings, slots, mask and retention clear without score change. Original1627 frame leaves activity0/0, latch1, all three records resolved, no duplicate recorder and null result cache. All scenes remain unfinished before native chart end2500. No completed hold results/SQLite flow, object destruction or physical reclamation is claimed.

Compared with026, this adds original renderer/UI pause and resume around the already established hold release path. Compared with037, there is no competing tap and no new exclusivity claim: Model retention, hold latch and per-frame activity remain distinct. Compared with012, the scene, UI, callback and checkpoint lifecycle are original-owned throughout, original hide processing is required for new input, and remaining hold checkpoints are actually reconciled. Earlier reports retain their stated scopes.

## 9. Reproducible scenario and validation

New `gameplay_interruption.py` runs the three required cases plus optional CANCEL in fresh emulators. New isolated `interruption_services.py` supplies only the necessary process/audio facades and reads native UI/callback products. No new fixture is added. CLI/config registration and README append are minimal. Full cases, construction products, native writes/callers/callback pointers, clock/flags, contacts, checkpoint guards/recorders and explicit failures/not_run stages are retained. Cross-case mismatches preserve the cases rather than throwing away their evidence.

The native-owned UI/audible-service qualification probes first reached a missing provider+2c0, then the AudioManager query header+1a8. Narrow source-backed external interfaces closed these omissions. The first full diagnostic with inert hide returned fail with both successful retained/control traces and exact rejected fresh-contact states. The original-hide run then passed all four cases. A final independent invocation adds native dismissal/identity/action-code assertions and UI state observations; no gameplay outcome is forced or repaired.

Actual final command:

```bash
/tmp/arconist041/bin/python research_harness/run.py \
  --archive project_sources/01-arccopy.zip --scenario gameplay_interruption \
  --output audit/041/final.json
```

Final verification returned exit0/status pass/native_failures empty. Construction, hold baseline, contact continuity and checkpoint/cleanup gates pass in all four fresh cases; lifecycle passes in the three interrupted cases and is explicitly not applicable to the uninterrupted control. No generated output is committed.

Each prior CLI command used this exact form, with the scenario/output substitutions in the table:

```bash
/tmp/arconist041/bin/python research_harness/run.py \
  --archive /workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
  --scenario SCENARIO \
  --output /workspace/scratch/90d77f091ffe/audit/041/SCENARIO.json
```

| Scenario | Exit | JSON status | Seconds |
|---|---:|---|---:|
| ordinary |0 |pass |18.371 |
| chord |0 |pass |36.177 |
| moving_arc |0 |pass |39.083 |
| timing_group |0 |pass |38.607 |
| cpu_note |0 |pass |47.988 |
| late_input_expiry |0 |pass |41.987 |
| noinput_semantics |0 |pass |45.079 |
| linked_arc |0 |pass |27.459 |
| mixed_hold_tap |0 |pass |70.183 |
| lane_widening |0 |pass |65.74 |
| settings_offset_clock |0 |pass |108.995 |

All five existing unit tests execute using the three native-test opt-ins:

```bash
ARCONIST_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_ARC_TAP_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_HOLD_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
/tmp/arconist041/bin/python -m unittest discover -s research_harness/tests -v
```

Exit0; 5 tests run, all OK, zero skips,56.951s (57.003s including process overhead). These actually execute native arc-tap construction/judgment and hold release/reacquisition, plus missing archive, unavailable song and wrong ELF hash controls. Together with the eleven prior CLIs, all thirteen previous successful gameplay scenarios ran freshly against the modified CLI/config tree. Later changes affect only the new041 observation/assertion modules and are covered by the independent final run.

Generated JSON/logs remain outside the published package. Existing blocked camera/track/flick/gauge/Designant diagnostics are unchanged, not rerun and not counted as green gameplay. Existing fixtures/scenarios/assertions and dependency pins are preserved.

## 10. Scientific and platform boundaries

**Original-native integrated:** ordinary scene/chart/hold/checkpoint/index creation; native UI/PauseLayer/capture/delegate production; lifecycle getter/virtual/type-check/pause acceptance; Director stop/start/guard; native Timeline pause compensation/seek decision; original resume/dismissal/UI and foreground callbacks; JNI Touch mapping/terminal cleanup/reacquisition; continuous hold processing and three unique recorder/gauge operations.

**Externally supplied:** ordinary catalog/account/settings/profile/platform/resource/ABI/allocator/autorelease/graphics/audio services, AppDelegate facade singleton/original-vtable setup, Android animation interval setter, provider readiness and pause/seek/update responses, empty audio-query header, clock, Widget enum2 invocation and explicit JNI contacts/lifecycle order. Full Widget dispatch is not executed; the supplied event is delivered to a genuinely native-created callback capture.

**Instruction-backed, not newly executed:** Java lifecycle/Runnable submission relationships, AppActivity ready-gated JNI paths, alternative scene/finished/rejection/ready-false branches and provider/FMOD implementation. **Interpretation:** the failed inert-hide contrast identifies a needed modal-input dismissal consumer; it does not characterize every UI listener policy. **Unknown/unexecuted:** Android callback/GLThread order, physical finger preservation, device clocks/audio output/latency, arbitrary pause/seek/mode/offset combinations, complete GPU/visual fidelity, optional arc ownership and full results/destruction.

The existing nine exact PC skips remain:

```text
0xf72110  -> 0xf72158
0x16a4238 -> 0x16a48d8
0x121581c -> 0x121584c
0xa507c4  -> 0xa519ec
0xa51adc  -> 0xa5213c
0x196fdac -> 0x196ffac
0x891190 -> 0x89164c
0x891688 -> 0x89219c
0x8921dc -> 0x8928e0
```

The last three results-only ranges are unentered. Existing Node visit/draw/flush, loading presentation proxies, resource/font/CSB/texture, graphics/audio/platform/ABI/reference services keep their established scope. Original pause/dismissal/callback/Timeline/contact/judgment routines are neither hooked to outcomes nor directly invoked internally by the driver. The driver invokes only the owning renderer lifecycle entries, original registered resume callback, ordinary Director entries, original JNI inputs and read-only projection. No new gameplay PC skip, native-ready patch, state restoration or account adapter is supplied.

## 11. Publication and preservation

Publication is a narrow non-forced child of9cacc57053062dc3554e90313c92e854d4aefae1. Eight authorized paths change: this report, append-only context, G-017/history backlog addition, README/run/config and the two new isolated source modules. The original hold fixture, hold.py/mixed_hold_tap.py/lifecycle.py, all previous scenarios/reports/tests/assertions/pins/blocked diagnostics and unrelated blobs remain exact. Historical context and README remain exact prefixes; G-001–G-016 rows/status/history are preserved.

Every changed committed file is fetched by immutable SHA and compared exactly; ancestry/main, changed paths and all other parent/child blobs are verified. No game archive/ELF/assets, generated traces/logs/JSON/dumps, databases/environments, personal/account settings or credentials are committed. Exact child SHA and pinned links are returned separately to headquarters.

## Pseudocode — observed original path

```text
for uninterrupted, retained interruption, UP interruption, CANCEL interruption:
    fresh verified ELF + established external ordinary environment
    original solo entry/loading -> native GameScene
    native AFF hold/checkpoints/index/N3/end2500
    native UILayer/PauseLayer/registered resume capture/delegate
    original camera projection -> supplied JNI DOWN42 atE1000
    native latch -> retained Touch -> continuous activity -> first checkpoint

    if interrupted:
        renderer background -> original AppDelegate -> same GameScene
        original UI acceptance -> native pause state -> Timeline pause
        original Director stops; native background notification
        if UP/CANCEL case:
            original terminal JNI -> engine and Model cleanup
        external wall advances60000
        stopped Director wrapper -> no model/clock advancement
        renderer foreground -> Director restart; gameplay remains paused
        original paused frame -> C absorbs delay; E1200, activity clears
        supply Widget enum2 to original native-produced PauseLayer callback
        native delegate -> original dismissal and GameScene/Timeline resume
        original seek(E-B)/unpause requests -> supplied audio interface

    retained case: original Touch reactivates atE1201, no new DOWN
    released case: no retained contact until genuine DOWN43 atE1300
                   new Touch/ID1 -> native activity atE1301
    original remaining checkpoint guards/writes/recorders
    JNI UP -> original complete contact cleanup
    frame1627 -> activity0, latch1, no duplicate judgment
compare actual checkpoint/score/gauge trajectories and identities
run previous successful regressions, preserve blocked diagnostics
publish G-017 evidence
STOP before042/S2-C08
```

## Final research boundary

Original native-created ordinary gameplay preserves the tested hold's scoring continuity across the supplied interruption schedule, either with the same retained Touch or genuine post-resume reacquisition after UP/CANCEL. Foreground alone is not gameplay resume, latch is not active contact, and native dismissal cannot be replaced by an inert visual stub when its real input consumers exist. No broader Android/device/contact-type/render/audio or universal ownership claim follows. The hold objective is complete; optional arc research and Expedition042 are not initiated.
