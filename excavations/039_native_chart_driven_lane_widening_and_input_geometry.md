# Expedition 039 — Native Chart-Driven Lane Widening & Input Geometry

Date: 2026-10-30. **G-015**, selected by headquarters from Scout002 S2-C05.

## Result

**Verified for both original chart controls in three fresh ordinary native-created GameScenes.** Kind5 `enwidencamera` and kind6 `enwidenlanes` parse, pass their original fallback construction branches with chart+0x110=0, dispatch through native gameplay frames, produce separate transition fields and interpolate native G/W. Identical external JNI contacts then acquire different native lane eligibility and judge the corresponding original-created taps.

At E1500 the control yields lane pairs(4,0)/(5,0), with no candidates. Kind5 yields(4,3)/(5,0), accepting lane3 only; kind6 yields(4,0)/(6,0), accepting lane6 only. Sampled primary-camera transforms/FOV/matrix data and projected JNI points agree across cases. This establishes an input-geometry effect without inferring a Camera-FOV or rendered-track-width effect from either identifier.

The new scenario and all prior successful gameplay regressions pass. No gameplay state, permission, note geometry, lane return or score is repaired, and no new runtime service or PC skip is introduced. Stop at E1501, before unplayed-note expiry/completion/results/SQLite.

## 1. Preparation and source identity

Verified main/parent: `b31fcae8975be7802d8f99a04c9d74c987c0f873`; tree `16c296f48d5994948d6c38c8c979125f6b04a8e7`. No039 report existed. All76 locally present original repository blobs matched the parent before edits. The supplied introduction, cumulative context/backlog, supplied S2-C05 proposal, relevant002/004/007–011/018/022–024/027/029/031/035–038 evidence and current harness were reviewed.031's kind0 rejection remains a distinct blocked objective.

External read-only archive member: `lib/arm64-v8a/libcocos2dcpp.so`,29217504 bytes. Fresh SHA-256:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Actual runtime retains Python3.12.14, Unicorn2.1.4 and pyelftools0.33; dependency declarations are unchanged. Capstone5.0.7 is used only outside the package for targeted disassembly. No new clean-install milestone is claimed. All instruction addresses below are **original ELF virtual addresses**. Heap pointers are observations in separate emulated address spaces, not regression constants.

## 2. Fixtures and original ordinary entry

Each chart contains:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1500,2);
(1500,5);
```

The two variants insert exactly one line before the taps:

```aff
scenecontrol(500,enwidencamera,500.00,1);
```

or:

```aff
scenecontrol(500,enwidenlanes,500.00,1);
```

Float500.00 and integer1 preserve the original typed grammar; no syntax adjustment is needed. These are synthetic research charts, not shipped song charts.

| Fixture | SHA-256 | Native complete-text MD5 |
|---|---|---|
| `native_widen_control.aff` | `ed24ad498f97fdee73258c5d1ba8cf2e37e9934237196221818b8b02b9eb0ec5` | `d155c18b426b27e448f40352f009a1fe` |
| `native_widen_camera.aff` | `78554144eafca66fd45c3aa054d2976cb923376cf1210da2ea28b14ee2059093` | `3559571ab9d68e279627cc3ad8ea82a6` |
| `native_widen_lanes.aff` | `d8e6cfd800d0d8697854f28d5add18e2eaa9a85ebd432f3ba9eb33b604dd5a28` | `16f6fffc033585fa76a75ce515e02fd1` |

All three use unchanged sayonarahatsukoi/difficulty0/base/no purchase, ordinary mode0, speed40 tenths, null map/modifiers and40 zero PlayParameters bytes. Original static initialization `0x1930604`, registry `0x1054f24`, ordinary entry `0xee197c`, eligibility1/request latch, allocation `0xee29a8` and constructor `0xee29e8` execute. Original loading Scheduler/ActionManager invokes `0xe2ea48`, returning1. Director activates the same GameScene; its native gameplay listener is registered/enabled/unpaused.

Original `0x1870de0 → 0x173b358/0x1862a14` construction produces two distinct `LogicTapNote` objects. Raw positions2/5 become internal lanes3/6; both preserve time1500/group0/input-enabled1. Original count producer `0x11ea120`, LR `0x173bf2c`, returns N2 in every case; native chart end is1620. Main-object counts after bars are505 for control and506 for each variant. The additional SceneControl is not an additional judgment unit in these charts.

## 3. SceneControl admission and ownership

Original parser `0x7f2628` creates a parsed `12SceneControl` with time500, the exact identifier, float500 and integer1. Original classifier `0x1090060` returns5 or6. Runtime initializer `0x1792e18` executes with the corresponding native arguments and returns1 at `0x18641b4`; RTTI is `17LogicSceneControl`, vtable VA `0x1aff8e8`. Native stores `0x1792eec/0x1792ef0/0x1792efc` write kind/value/integer at+0x64/+0x68/+0x6c. Event time/end are500 and group index0.

Chart property+0x110 is natively0, including observed producer `0x173c3cc`. The builder sees that value at `0x1864134` and executes these original fallback comparisons:

| Variant | Observed classifier returns at comparisons | Original admission |
|---|---|---|
| Kind5 |5 against4 at `0x18645f4`, then5 against5 at `0x18648f8` | Continue to `0x1864138` and native construction |
| Kind6 |6 against4,6 against5, then6 against6 at `0x18649fc` | Continue to `0x1864138` and native construction |

No feature byte or song exception is supplied.031 tested a real kind0 event which failed these alternatives; it did not establish rejection of kinds5/6. G-007 remains Blocked and its diagnostic is unchanged.

The native GameScene control-owner points to the same model at+0x2a0 and chart at+0x2c0. Its visual-feature byte+0x2c8 is also0. Original handler kind5/6 state paths execute before the kinds0–3 visual gate, so admission and dispatch do not require changing that permission.

Representative runtime pointers, not required constants:

| Object | Control | Either event variant, fresh address space |
|---|---|---|
| Scene / model | `0x4327c40` / `0x4355f40` | `0x4327c40` / `0x4356280` |
| Chart / ScoreState | `0x4331980` / `0x4356100` | `0x4331bc0` / `0x4356440` |
| Primary camera | `0x4368bc0` | `0x4368f40` |
| Lane3 / lane6 tap | `0x4332240` / `0x4332340` | `0x43325c0` / `0x43326c0` |
| SceneControl | none | `0x4332440` |

Original `0x1576aa4` inserts505/506 objects including bars. Both taps occupy group0 bucket1; the event occupies bucket0. Both taps are active before either E1500 probe. The event is active by the music anchor, remains active immediately after dispatch and is removed from the active vector on the E502 frame. Indexed presence and processed/active state are separately recorded.

## 4. Original dispatch and transition producers

The native music anchor is wall9452/E0. Original Director frames sample E500/501/502/750/1000/1500/1501. Native effective time, last-model E and the guarded one-model-update-per-frame relationship are checked; no timeline field is assigned by the driver.

At E500 the event remains unprocessed and the handler does not run. The executed ordinary clock branch compares E against end/time500 at **`0xf8071c`**; equality exits via `0xf80720`. At E501 it proceeds through original acceptance/marking and `0xf80824 → 0x1514c64`, LR `0xf80828`. Original `0x897e98` changes event processed byte+0x0d from0 to1. This event marking is not a scored judgment: counters remain0.

Kind5 handler path `0x1514cd0..0x1514ce4` passes model, event time500, direction1 and duration500 to **`0xd59c24`**, LR `0x1514ce8`. Its original stores write duration at model+0x5c and time/direction at+0x54/+0x58.

Kind6 has no call to that setter. Original **`0x1514d08/0x1514d0c`** directly write duration at+0x70 and time/direction at+0x68/+0x6c. Both kinds use the event's500 start, not actual dispatch E501. Each dispatch occurs once; the processed guard prevents repetition.

The fresh model's observed ordinary transition defaults are start−1073741824, direction−1, duration1 for both transitions, producing G1/W0. Those values already exist at the observed initializer entry; their initial stores are not newly traced by this scenario. The special transition writes above, their original caller/operands and subsequent scalar stores are directly observed. No driver default or widening value is written.

## 5. Native interpolation and frame ordering

Original `0x10a7550` updates the timeline and interpolates widening **before** expiry/scene-control processing. Scalar store PCs are `0x10a763c` for model+0x60/G and `0x10a76f8` for model+0x74/W; `0x10a75d4` preserves previous G at+0x64. Native memory-write order in the E501 frame places both scalar stores before the event's transition-field stores.

| Effective E | Control G/W | Kind5 G/W | Kind6 G/W |
|---:|---|---|---|
| 0 /500 |1 /0 |1 /0 |1 /0 |
| 501, after dispatch |1 /0 |1 /0 |1 /0 |
| 502 |1 /0 |1.0019999742507935 /0 |1 /0.004000000189989805 |
| 750 |1 /0 |1.25 /0 |1 /0.5 |
| 1000 /1500 /1501 |1 /0 |1.5 /0 |1 /1 |

The E501 frame has already used the old parameters before dispatch. E502 uses two milliseconds elapsed from the native event start500. The other transition remains at its original values. Parameters persist after the outputs clamp; no new transition-active flag is inferred. Previous-G observations track the actual preceding sampled G.

These finite positive-duration outputs agree with007's prepared-equation evidence. The new evidence joins their native event producer and original frame caller; Python neither evaluates those formulas to write state nor invokes the interpolation block.

## 6. Matched projection and native lane selection

At the anchor and E1500, original `0xbdbb70` projects the two supplied world points using the native primary camera, then Director height converts Y-up into JNI coordinates:

| Probe | World point | Identical external JNI coordinates in all cases | Native unprojection / truncated X |
|---|---|---|---|
| Secondary |(40,0,0) |(665.57470703125,617.340705871582) |(39.998565673828125,−0.00048828125,−0.00048828125) /39 |
| Outer |(950,0,0) |(1247.39990234375,617.340705871582) |(949.96630859375,0,0) /949 |

Both original strict depth checks −500<Z<500 pass. No input-point adjustment is needed. The user-suggested contacts are valid experimental probes, not tap-center substitutions or host-returned lane IDs.

Native `0x130733c`, reached from JNI collection, produces:

| Case | G/W at E1500 | Secondary probe primary/secondary | Outer probe primary/secondary |
|---|---|---|---|
| Ordinary control |1 /0 |4 /0 |5 /0 |
| `enwidencamera` |1.5 /0 |**4 /3** |5 /0 |
| `enwidenlanes` |1 /1 |4 /0 |**6 /0** |

The signed-X/lane predicates and G-dependent secondary-region calculation are instruction-backed by004 and execute here with native scalar inputs. Kind5 does not change this probe's primary lane; it adds lane3 as secondary. Kind6 changes the outer primary lane when W is positive. No equal-key sorting stability or general input-boundary enumeration is claimed.

At the sampled anchor and judgment endpoints, the primary Camera position(0,900,900), Euler(−26.565061569213867,0,−0), FOV50 and native P/V/world/PV numeric arrays agree within each case and across cases. Heap pointers differ and are excluded from value comparisons. JSON preserves all matrices. Only those endpoints are compared; this is not continuous-camera monitoring or proof about all visual consumers. The decisive E1500 JNI coordinates themselves are exactly matched across scenes, so these judgment differences are attributable to the original widening/lane path rather than moving the supplied contact.

## 7. JNI candidate and recorder comparison

Each scene delivers secondary DOWN42/UP42, then outer DOWN43/UP43, all at native E1500 with no intervening model frame or clock advance. Original `0xbe31a8 → EventDispatcher → 0x194ff80 → 0xeec024` executes. Both negative and positive inputs create a retained native Touch. Original pointer42 uses slot0/generatedID0; after UP, pointer43 reuses slot0 with a distinct Touch/generatedID1. Native mapping/retained/slot identities are checked within each scene, never equated across emulator heaps.

Original candidate vectors are observed before/after sorter `0xf6b514`:

| Case | Secondary candidates | Outer candidates | Native result |
|---|---|---|---|
| Control |empty |empty |No classifier/recorder; both notes unresolved |
| Kind5 |singleton lane3 tap |empty |Lane3 accepts once with generatedID0 |
| Kind6 |empty |singleton lane6 tap |Lane6 accepts once with generatedID1 |

For the accepted singleton, original classifier `0x160ce28` sees absolute error0, returns consuming true and calls `0x1730290`, LR `0x160cf48`, judgmentID0. Original acceptance `0x965e28` and native stores `0x965e68/0x965e6c` write consumed1/correct contact ID on that exact original-produced tap. No other note is classified or consumed by these probes. Sorting executes on empty/singleton lists; it establishes no new tie-order policy.

| State after both inputs and E1501 | Control | Kind5 | Kind6 |
|---|---:|---:|---:|
| PURE / FAR / LOST |0 /0 /0 |1 /0 /0 |1 /0 /0 |
| Shining / combo |0 /0 |1 /1 |1 /1 |
| Score |0 |5000001 |5000001 |
| Live health |0 |40.20000076293945 |40.20000076293945 |
| Classifier / accepted recorder entries |0 /0 |1 /1 |1 /1 |
| Miss recorder entries |0 |0 |0 |

Native N remains2. These are live recorder outputs, not a final full-chart result or Python arithmetic. The unplayed taps remain unconsumed/unmissed; LOST0 at E1501 is not an exemption from later ordinary expiry. The optional expiry extension is not run because there is no counter discrepancy.

## 8. Cleanup, original ownership and scope

Each original UP `0xdda71c → 0xf9a50c` empties its Android mapping, slot pointer, active mask and retained-contact vector without changing note/score/gauge state. The following original E1501 Director frame produces no duplicate judgment; consumed taps leave active processing while unplayed taps remain unresolved. All scenes remain unfinished with result cache null; completion/snapshot counts0.

Every case has10 model-frame entries and two actual JNI DOWN/UP/listener/selector/sorter entries. Handler/setter counts distinguish the variants: handler0/1/1; `0xd59c24`0/1/0. Original parser/runtime-control initializer counts0/1/1. No direct driver call replaces a constructor, frame, handler/setter, lane selector, classifier, recorder or cleanup. Read-only camera projection is an explicitly allowed native observation/input-derivation interface.

G-015 therefore extends008's prepared widening-to-input evidence through authentic whole-chart event production and ordinary native scene ownership. It does not close G-006 camera-action admission/reset or G-007 track-fade scheduling, and neither blocked diagnostic is modified.

## 9. Reproducible scenario and validation

New `src/lane_widening.py` runs control first, then two fresh variants. Each case retains independent native ownership and preserves partial evidence on exceptions. A rejected variant remains failed/incomplete while the other can still be investigated; control failure leaves later cases not_run. Cross-case projection mismatches preserve all cases and mark failure rather than replacing the result with expected events.

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario lane_widening \
  --output /path/outside/research_harness/lane-widening-result.json
```

Actual invocations use `/tmp/arconist039/bin/python`, external archive `project_sources/01-arccopy.zip`, scenario `lane_widening`, outputs under `audit/039/`. Final evidence includes all four gates per case, no native failures, scalar trajectories, native instruction/store/candidate/recorder evidence and normalized camera/projection comparisons. No generated JSON is committed.

Preparatory failures are preserved separately: the first invocation has a Python SyntaxError before native execution, corrected before the successful diagnostic. Subsequent added time-predicate assertions initially watched the untaken alternate branch `0xf807fc`; cases preserved native execution evidence but failed with an observer KeyError. Targeted disassembly identified the ordinary branch `0xf8071c`. Only read-only observation coverage was corrected, followed by an independent final run. No native outcome or state is repaired, and failed observations are not spliced into the final trace.

Assertions require original construction/feature-state provenance, dispatch identity and strict boundary, native writer order/parameters, observed interpolation trajectories, exact paired inputs/camera values, lane/candidate/note identities, original acceptance/contact IDs, recorder deltas and cleanup. Final score equality alone is insufficient. The historical formulas are not used to implement native gameplay.

All invocations below completed against the modified source tree. The new final CLI exited0, JSON status pass, native_failures empty, with construction/dispatch-interpolation/JNI-geometry-judgment/cleanup gates passing in all three independent cases.

```bash
/tmp/arconist039/bin/python research_harness/run.py \
  --archive project_sources/01-arccopy.zip --scenario lane_widening \
  --output audit/039/final.json
```

The prior CLI executions used the following exact command form, with each scenario/output substitution listed in the table. The archive and outputs were absolute paths rooted at `/workspace/scratch/90d77f091ffe`:

```bash
/tmp/arconist039/bin/python research_harness/run.py \
  --archive /workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
  --scenario SCENARIO \
  --output /workspace/scratch/90d77f091ffe/audit/039/SCENARIO.json
```

| SCENARIO | Exit | JSON status | Elapsed seconds |
|---|---:|---|---:|
| ordinary |0 |pass |46.797 |
| chord |0 |pass |86.684 |
| moving_arc |0 |pass |75.015 |
| timing_group |0 |pass |67.307 |
| cpu_note |0 |pass |122.358 |
| late_input_expiry |0 |pass |119.552 |
| noinput_semantics |0 |pass |82.096 |
| mixed_hold_tap |0 |pass |137.844 |
| linked_arc |0 |pass |47.392 |

The existing five unittest cases were then executed, with all three archive opt-in variables set to the same absolute original archive path:

```bash
ARCONIST_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_ARC_TAP_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_HOLD_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
/tmp/arconist039/bin/python -m unittest discover -s research_harness/tests -v
```

Exit0; **5 tests run, all OK, zero skipped**,115.560 seconds: native arc-tap construction/consumption, native hold release/reacquisition/checkpoints, missing archive, unavailable song and wrong binary hash. Arc-tap and hold therefore actually execute their native scenarios; they are not counted from skipped optional tests or stale JSON. Together with the nine previous CLI scenarios, all eleven prior successful gameplay scenarios remain green. Their unchanged native assertions cover ordinary results/SQLite, moving/crossing arcs, reverse scroll, CPU lifecycle, late-input ordering, noinput completion, mixed notes and linked successors as documented by their own reports.

Existing blocked camera/track/flick/gauge/Designant diagnostics remain intact and are not rerun or counted as green gameplay. No old fixture, scenario assertion, test or dependency pin changes.

## 10. Scientific and publication boundaries

**Native-integrated:** original solo entry, AFF SceneControls/taps, kind classification/admission, count/index/active lifecycle, native frame dispatch/transition stores/interpolation, camera projection/unprojection/lane selection, JNI candidates/classifier/recorder/consumption and cleanup. **Instruction-backed:** general selector/formula interpretation and untaken transition/feature branches outside this finite positive-duration fixture. **Externally supplied:** synthetic AFF, catalog/profile/settings/platform/resource/ABI services, clock and JNI event data. **Unexecuted/unknown:** negative/zero durations, closing transitions, mixed kinds, intermediate Camera matrices, complete visible track geometry/shaders/GPU, real device scheduling/latency, later expiry/result/persistence and physical reclamation.

Exact inherited PC skips, unchanged:

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

The last three results-only ranges are unentered. Existing loading/presentation proxies, base Node visit/render/flush, archive/font/CSB/audio/GPU, libc/C++/math/locale, clock/platform and allocator/autorelease boundaries retain their established scope. No new runtime service, account adapter, feature permission or gameplay skip is introduced. Original native TrackLayer initialization/CPU updates remain enabled; rendered width/FOV consumers are not reconstructed.

Publication is a non-forced child of the verified parent, limited to ten paths: report/context/backlog, harness README/run/config, new source and three new synthetic fixtures. All changed committed contents are read back and compared, parent/child blob trees are checked, and historical context remains an exact byte prefix. G-001–G-014 rows/status/history, prior reports/fixtures/scenarios/tests/assertions/pins/blocked diagnostics/root instructions and unrelated blobs are preserved. G-015 is Verified for this paired input-geometry scope. No original archive/ELF/assets, generated output/traces/dumps, databases/environments/credentials or account data are committed. Exact child SHA and immutable links are returned separately.

## Pseudocode — observed original path

```text
for control, kind5, kind6 in independent fresh native scenes:
    external synthetic AFF -> original parser and kind classifier
    original ordinary solo entry/loading -> native GameScene
    original fallback admits kind5/6 with chart feature0
    native SceneControl/taps -> count/index/active admission
    Director activates same native scene

    atE500: original event guard does not dispatch
    atE501:
        native interpolation still uses old transition fields
        original event processing marks control processed
        original handler writes selected transition(start500,direction1,duration500)
    later Director frames:
        original float32 interpolation changes only selected G or W

    atE1500, same world probes/projected JNI points in every scene:
        JNI DOWN -> original Touch/listener/unprojection
        original lane selector reads native G/W
        original candidate collection/sort
        if matching tap admitted:
            native classifier/recorder/consumption/contact-ID stores
        JNI UP -> original mapping/slot/retention cleanup
    E1501 Director frame -> no duplicate judgment
compare matched coordinates, matrices, native lane/candidate changes and scores
stop before expiry/completion/results/SQLite
```

## Final research boundary

Both original chart-driven controls affect JNI gameplay in this ordinary scene, through different native scalar/selector paths. The same external contact can fail under ordinary geometry and judge the intended tap after the corresponding event. This does not establish Camera-FOV changes, complete rendering, arbitrary charts/parameters or Android scheduling. No further experiment is needed for the bounded objective. Stop after039, without040/S2-C06 or reopening deferred work.
