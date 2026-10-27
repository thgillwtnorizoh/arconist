# Expedition 031 — Native Track-Fade Scheduler, Callback Replacement & Node Opacity

Date: 2026-10-27. Parent: `08bccf21cac301b263ee5b9a4eb290ba10783217`. Headquarters selected Scout001 backlog **G-007**, explicitly keeping G-006 Blocked.

## Result

**Blocked before Gate A; the minimum runtime-construction/dispatch criterion is not met.** Original whole AFF parsing accepts the proposed track-display event, but native chart construction excludes it in the unchanged ordinary `sayonarahatsukoi` fixture. No LogicSceneControl is created, so no fade handler, keyed timer, callback, opacity propagation or replacement executes. The second runtime is not started. G-007 becomes **Blocked — Expedition031**. G-006 remains **Blocked — Expedition030** without resumed investigation or altered source/status. No Expedition032 is initiated.

The new result establishes both the exact original **construction filter** and the **native handler feature-byte producer**, in one ordinary solo-created scene. A genuine native-connected track collection exists, but its existence and initial opacity are not Scheduler-delivered propagation evidence. Earlier007/008 isolated callback/Node tests remain valid with their original boundaries.

## Preparation, source provenance and scope

The original project introduction, latest context/backlog,002 scene-control grammar,007 handler/callback/propagation/gating,008 isolated validation,009 Director/Scheduler visitation,010–011 full chart/input/lifecycle findings and024–030 published harness/scenario evidence were reviewed. Existing actual source is available. GitHub main matched the expected parent;031 was absent. Locally present parent-version files matched published Git-blob hashes before changes.

External read-only archive member `lib/arm64-v8a/libcocos2dcpp.so` was inspected and SHA-256 verified:

`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

A fresh Python3.12 virtual environment installs the unchanged published requirements, Unicorn2.1.4 and pyelftools0.33. Capstone5.0.7 is used only in an external diagnostic directory for targeted original-code inspection, not added to the runtime package. Existing loading, original static initialization, native scene construction, resources, Scheduler/ActionManager and inspection adapters are reused; no new subsystem is reconstructed.

Original function addresses are ELF VAs. Object pointers below are observed emulated allocations, not asserted constants. **Native-integrated** means connected original execution in the new ordinary scene. **Instruction-backed** identifies inspected but unexecuted downstream decisions. **Unknown** marks actual timer/callback/replacement behavior not established here. No actual-device or GPU behavior is claimed.

## Inputs and original parsing

Established ordinary metadata is unchanged: Song`sayonarahatsukoi`, difficulty0, set`base`, no purchase descriptor, ordinary mode0, speed40 tenths, no map/modifier,40 zero PlayParameters bytes and existing controlled catalog/settings/profile/platform services. Complete original initializer`1930604` and song-ID registry initializer`1054f24` execute normally.

Single-fade fixture `fixtures/native_track_fade.aff`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
scenecontrol(600,trackdisplay,2.00,0);
(1500,3);
```

Synthetic AFF bytes enter the original resource-provider interface. Native chart MD5 is `e4653ebb4a8e87a6330487d8936ed7ab`, independently compared with these exact bytes; no fake digest is supplied. The archive is a partial source of original materials and is not assumed to contain every installed chart.

Replacement candidate `fixtures/native_track_fade_replace.aff` adds only `scenecontrol(900,trackdisplay,2.00,255);`. It is preserved as an **unexecuted candidate** because the single-fade gate fails. No second parser/runtime result is claimed. Initial owner opacity is natively255, so the proposed first target0 would have been informative if admitted; no fixture-target adjustment or initial-opacity patch is needed or attempted.

Original parser`7f2628` executes once within whole parser`1870de0`, producing parsed `12SceneControl` at emulated`0x432ea00`, vtable`0x1a94588`. Actual fields read at the builder's successful RTTI-recognition branch:

| Field | Observed original value |
|---|---|
| time+18 | 600 |
| identifier string+20 | `trackdisplay` |
| float+38 | 2.0 |
| integer+3c | 0 |

Native classifier`1090060` executes three times in the construction fallback, each returning0. Thus parser grammar and kind identification succeed. This is not proof that an original runtime event exists.

## Native construction exclusion

The original scene-control builder branch differs from the camera branch and is inspected independently:

```text
1864128: parsed SceneControl recognized
1864130: read chart+110
1864134: zero → fallback at18645e0
18645f0→1090060;18645f4 compares kind with4
18648f4→1090060;18648f8 compares kind with5
18649f8→1090060;18649fc compares kind with6
if none matches, test original Song exceptions arcahv/desive
186558c: zero keep-result → next parsed object1863d60
```

The authoritative trace records chart`0x4331a40`, property byte0, parsed pointer`0x432ea00`, classifier results0 against4/5/6, final W19 keep-result0 and actual edge **`186558c→1863d60`**. Original property store`173c3cc` had written a one-byte0 to emulated chart+110=`0x4331b50`. That is an executed producer, not a presumed allocator default.

The ordinary selected Song satisfies none of those exceptions. The nonzero-property or admitted-fallback branch would enter runtime initialization at`1864138..18641b0`, but original LogicSceneControl initializer`1792e18` executes0 times and the native chart contains zero`17LogicSceneControl` objects. Native runtime time/group/input/kind fields therefore cannot be claimed validated for this event.

The exact prerequisite is original permission to construct a kind0 event in a coherent chart/catalog context. It is not a timer-ABI or graphics-resource failure. Existing010/030 evidence ties chart+110 to native digest/named-song decisions; this expedition does not resume camera work, explore compatible camera materials or rename catalog metadata. No chart property, digest, runtime event or admission state is supplied to force this branch.

## Native handler feature provenance and track relationship

Ordinary original solo entry succeeds: `ee197c` eligibility1/native request latch1, allocation`ee29a8`, constructor call`ee29e8`, original loading actions, `e2ea48` initializer return1 and Director activation of that same scene. These native handoffs are preserved, not called directly from the diagnostic driver.

| Native object/relationship | Observed emulated pointer |
|---|---|
| GameScene | `0x4327c40` |
| GameModel | `0x4355f40` |
| LogicChart | `0x4331a40` |
| GameSceneVisualControlHandler | `0x4ea9340` |
| Visual wrapper | `0x43666c0` |
| TrackLayer collection | `0x4368400` |
| Native TrackBase member | `0x4369600` |
| Scheduler / ActionManager | `0x41081c0` / `0x4108840` |

The actual owner type is `29GameSceneVisualControlHandler`. Scene+300 points to it; original initializer`a3937c` receives and stores the model, rig, visual wrapper, TrackLayer and chart at owner+2a0/+2a8/+2b0/+2b8/+2c0. Entry LR is`e2f5dc`. Arguments and resulting pointer relationships agree within this runtime.

Read-only memory-write observations establish:

| Original PC | Native write | Value |
|---|---|---:|
| `e2f5cc` | owner+2c8 initial byte | 0 |
| `e2f5d4` | owner+2cc current opacity i32 | 255 |
| `e2f618` | owner+2c8 copied property byte | 0 |

Instructions`e2f600..e2f618` load the original chart, call`16a3a6c`, mask its return bit and store the result. Getter`16a3a6c` is original `LDRB W0,[X0,#110]; RET`. Actual store operands and final memory are0. No driver write enables the feature or initializes opacity.

**The later handler gate is not executed here.** Instruction-backed `1514ce8` loads owner+2c8, `1514cec` requires nonzero to reach kind0–3 processing, otherwise`1514cf0→1515174` returns. Because construction already excluded the event, this is a documented second guard with native-produced input0, not a claimed dynamic handler rejection. Song exceptions that only retain a runtime control do not by themselves establish feature enablement.

Original initialization connects a nonempty TrackLayer vector: collection+300/+308 is `0x4371780..0x4371788`, containing native `9TrackBase` pointer`0x4369600`. Its opacity virtual at+470 resolves to ELF`1608014`; Node RGBA bytes at+1d1/+1d0 are255/255. These are passive identity/field observations. No arbitrary Node is allocated/inserted, no opacity getter/setter or propagation helper is host-invoked, and no timer-driven change is established. Earlier native TrackLayer/resource construction boundaries remain inherited from020–024.

The native chart is otherwise coherent: one tap1500/raw3→native lane4, N1/end1620, original spatial index contains it (504 producer calls including auxiliary bars). Scene+3e0/+3e8 references model/chart; gameplay listener is registered1/enabled1/paused0. Final Director runs the same scene, pending0, dispatcher enabled1. Optional JNI gameplay is not attempted after the required eligibility gate fails.

## Scheduler observations and explicit unexecuted stages

The authoritative diagnostic allows original loading/initialization and final Director activation to complete, so the native owner/feature producers can be inspected, then stops. Original Scheduler`13d3f44`, registered callback`d630b8` and ActionManager`9effe0` each execute24 times during this connected setup. Actual dt, phase, wall clock and caller PCs are recorded. They establish reuse of the native scheduling connection, not a track timer.

At the endpoint `timers()` is empty. Track-owner schedule/unschedule observations are empty; native`81565c` and`10846c0` entries are0 in this run. Runtime scene-control dispatch callsite`f80824`, handler`1514c64`, callback`1501dfc` and propagation`ef18e8` entries are all0. Global Node opacity setter`18ebfa4` executes739 times in resource/UI setup and loading; those calls are not presented as track-fade propagation. The fade closure is never allocated, so no counter, captured starting opacity, interval0.02, repeat99, callback interpolation or timer replacement is newly observed.

The earlier exploratory single-fade probe advanced through E600/601 and approximately20ms steps toE661: owner opacity stayed255, feature0 and timer list empty. Its observations are not spliced into the final fresh construction/producer trace. They do not turn an omitted event into a Scheduler cadence test. The final reproducible diagnostic stops at native scene activation once the cause is established.

The complete intended downstream path—handler unschedule, native closure allocation, Scheduler registration/delivery, float32 squared-progress computation, TrackBase propagation, retirement of the old timer and replacement closure—remains **Unknown in this native-owned integration**. Prior007/008 original-isolated callback arithmetic is referenced, not rerun as a substitute. No second runtime begins, and no timer, closure counter, opacity or feature field is repaired.

This one construction/feature-permission dependency is the bounded stop. The smallest future prerequisite is genuinely scene-control-permitted original materials/context whose native producer supplies the necessary permission. No general renderer, new callback ABI, alternative scene-control matrix, account system or G-006 recovery is investigated.

## Reproduction and validation

```bash
python -m venv /path/to/venv
/path/to/venv/bin/pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario track_fade \
  --output /path/to/track-fade-result.json
```

Actual new outcome: **exit1 / JSON status`fail` / `NativeTrackDisplayConstructionExcluded`**, single_fade`blocked_at_original_runtime_construction`, replacement`not_run`. JSON18850 bytes preserves original parsed fields, classifier/skip decisions, native property and feature writes, owner/collection/node relationships, Scheduler trace, native call counts and unexecuted endpoints. Eligibility-characterization assertions pass; the requested fade regression still fails. Unexpected exceptions retain available partial evidence instead of emitting scripted success.

New package changes are limited to `src/track_fade.py`, two synthetic fixture files and minimal config/CLI/README additions. Internal`track_fade_replace` selects the unexecuted replacement candidate, not an exposed tested second case. No new passing unittest wrapper masks the failed gate.

Fresh ordinary full-session, chord both orders, moving/crossing and timing-group/reverse CLI regressions pass. Existing arc-tap and hold dual-case native unittests plus missing-archive/wrong-hash/unavailable-song controls also pass. All5 discovered tests finish in111.925s with all3 archive switches enabled and zero skips. The new diagnostic fail is kept separate from green gameplay regressions. Expedition030's camera_reset.py, its fixtures/assertions and blocked backlog row remain byte-for-byte unchanged; it is not rerun or resumed during031.

## Scientific and publication boundaries

No new ABI/platform/graphics service or PC skip is added. Existing catalog/settings/profile storage, external synthetic AFF, archive resource provider, libc/C++/math/JNI/platform interfaces, clock, CPU resource/texture/presentation proxies, audio services, allocation/autorelease and incomplete reclamation retain previous contracts. Native TrackLayer CPU updater19069a0 stays enabled. No GPU output, actual-device event-loop timing, original production-chart compatibility or results/SQLite test is claimed for these fixtures.

Exact inherited ELF PC ranges:

```text
f72110→f72158       platform GLView attachment
16a4238→16a48d8     shutter panels/native Node proxies
121581c→121584c     loading overlay
a507c4→a519ec       loading artwork prefix
a51adc→a5213c       information artwork/canary
196fdac→196ffac     closing information visuals
891190→89164c      results UI prefix
891688→89219c      middle results UI
8921dc→8928e0      post-save progression/UI
```

The last3 are not entered by the new diagnostic. Existing inert base traversal/render/flush129c924/1017a84/13edf0c remain explicit. Inherited private DB preparation is not a031 saving experiment.

Nine authorized paths change: report/context/backlog, harness README/config/CLI, new diagnostic source and two synthetic fixtures. Historical context is preserved as an exact prefix; reports001–030, root README/instructions, prior fixtures/scenarios/assertions/tests/dependency pins and unrelated entries are unchanged. G-001–G-005 remain Verified; G-006 stays Blocked—030; only G-007 becomes Blocked—031; G-008–G-010 unchanged. No original ZIP/library/resources, generated JSON/trace/database/dump, environment or secret is committed. Publication uses the verified expected parent/non-forced head update; all changed files and the context prefix are read back and compared after commit. Exact SHA and pinned links are returned in the final answer.

## Pseudocode — observed mechanism and stop

```text
verify original external ELF and repository parent
supply established ordinary metadata/services and single-fade AFF bytes
original solo eligibility/latch → native GameScene construction/loading
original whole parser creates SceneControl600/trackdisplay/2.00/0
native chart property producer writes+110=0
original builder:
    kind0 fails fallback kinds4/5/6 and Song exceptions
    original186558c→1863d60 omits runtime control
original scene initialization connects visual handler and native TrackLayer/TrackBase
native getter copies chart property0 to owner feature+2c8; opacity starts255
original loading Scheduler/callback/ActionManager and Director activation finish
read original-connected collection, unchanged opacity and empty timer state
emit failed track-fade diagnostic with exact native construction/feature evidence

NOT EXECUTED:
    runtime scene-control dispatch, handler feature branch, fade timer/closure,
    Scheduler-delivered fade callbacks, opacity propagation or replacement runtime

run previous successful regressions without weakening them
preserve G-006 blocked diagnostic unchanged
mark G-007 Blocked; publish bounded evidence
STOP before Expedition032
```
