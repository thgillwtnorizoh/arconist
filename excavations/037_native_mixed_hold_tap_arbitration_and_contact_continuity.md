# Expedition 037 — Native Mixed Hold/Tap Arbitration & Contact Continuity

Date: 2026-10-29. Permanent objective **G-013**, selected by headquarters from Scout 002 S2-C03.

## Result

**Verified within three specified ordinary native-owned mixed-note executions.** Original AFF construction, hold checkpoints, spatial index/admission, JNI initial arbitration, retained-contact processing, native recording and cleanup are connected without gameplay-state repair.

With hold1000 preceding tap1250, the initial hold-latch branch stops candidate iteration. A previously set latch does not exempt the hold: a second same-lane DOWN writes latch1 again and still does not reach the tap. With tap950 preceding hold1000, the first E1000 DOWN judges the tap; a second DOWN at unchanged E1000 reads its consumed guard, continues and latches the hold.

Initial selection is not exclusive long-term contact ownership. Both retained same-lane Touches reach native hold activation in a frame. After releasing one, the other sustains activity. In the tap-first case, the Touch that originally judged the tap sustains the hold after the separate latching Touch is removed. Every native checkpoint resolves once. Final cleanup empties all native mappings/slots/mask/retention, and the next frame clears activity while latch1 survives.

All nine previously successful gameplay scenarios and five existing tests pass. The new scenario passes all gates in three fresh emulators. No new platform dependency or PC skip is introduced. Stop at E1627, before completion/results/SQLite for these charts.

## 1. Source identity and preparation

Main and expected parent were verified as `c9d8bbfe71631e7989cd9891518389bb2609e075`, tree `1687b7b472c03f4a09a3f4dce07203056906bd21`; no037 report existed. All69 locally present original repository blobs matched their Git hashes before edits. Original instructions, cumulative context/backlog, the supplied S2-C03 proposal, relevant002–004/008–012/018/022–024/026/027/035/036 evidence and actual current harness were reviewed. Older002's unqualified hold-lookahead wording is not substituted for the later distinct initial and continuous predicates.

The external read-only ZIP's `lib/arm64-v8a/libcocos2dcpp.so` is29217504 bytes, SHA-256:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Actual Python3.12.14, Unicorn2.1.4 and pyelftools0.33 match the unchanged pins. A fresh local environment was prepared. Capstone5.0.7 supported targeted disassembly outside the package; it is not a runtime dependency. This is not a new clean-install milestone.

Instruction addresses in this report are **original ELF virtual addresses**. Heap addresses are observations in independent emulated address spaces, never regression constants. No prior heap snapshot or emulator instance is reused.

## 2. Synthetic charts and native producers

Both fixtures use unchanged ordinary `sayonarahatsukoi`, difficulty0, base/no purchase, mode0, speed40 tenths, null map/modifiers and40 zero PlayParameters bytes.

Hold-first fixture:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
hold(1000,2000,3);
(1250,3);
```

The tap-first fixture changes only `(1250,3)` to `(950,3)`. These are synthetic research bytes, not released charts. SHA-256 hashes are:

| Fixture | SHA-256 | Native MD5 |
|---|---|---|
| `native_mixed_hold_tap_hold_first.aff` | `32e3d87fe3a547d66b3f5c1f8e6f1abd06d4097a9708f166de8f6d101a2e3539` | `1358beb0a0fce32abb62b86c6408f75a` |
| `native_mixed_hold_tap_tap_first.aff` | `2be8778065223f9ea6170beed1250dbe9b7201f079294e44203b38ec12e55fc1` | `ddea602abd52ad50e790f01a733471bc` |

Every case executes original static initializers `0x1930604`/song registry `0x1054f24`, ordinary entry `0xee197c`, eligibility1/request latch and native allocation/constructor `0xee29a8 → 0xee29e8`. Original loading Scheduler/ActionManager invokes `0xe2ea48`, returning1. Director activates that same native scene. Its original listener is registered1/enabled1/paused0.

Original whole parser `0x1870de0`, body/statement path and chart initialization `0x173b358 → 0x1862a14` construct:

| Product | Native provenance and observation |
|---|---|
| Hold | Parsed `8HoldNote`,1000..2000/raw integer3; builder `0x18649b8 → 0x1446490`, return `0x18649bc`; runtime `13LogicHoldNote`, vtable VA `0x1b2eda8` |
| Tap | Parsed `10SimpleNote`,1250 or950/raw integer3; `0x18640d8` invokes native initializer `0x1902ffc`, return1 at `0x18640dc`; runtime `12LogicTapNote`, vtable VA `0x1af4278` |
| Position/timing | Both native positions map raw3 to internal lane4, group0/input-enabled1. Native timing record120 BPM, scale0.12361110746860504; runtime tap start/end both equal its parsed start. Parsed SimpleNote's separate end field is0, not the runtime end |
| Checkpoints | Original `0xd92558` and three append observations at `0xd925fc`:1250/1500/1750, each weight1/unresolved0; interval250 |
| Count/end | Original `0x11ea120` observes two main objects before bars, returnsN4 through `0x173bf2c`; chart end2500;506 main objects after auxiliary generation |
| Index | Original `0x1576aa4` runs506 times including bars; original hold in group0 buckets0/1, tap in bucket1 for1250 or0 for950 |

Each original scene owns the corresponding model/chart; the model references its original chart/timeline/ScoreState, native gauge and CameraController. Representative addresses are identical numerically across fresh address spaces: scene `0x4327c40`, model `0x4356180`, chart `0x43319c0`, timeline `0x4356300`, ScoreState `0x4356340`, gauge `0x43564c0`, hold `0x4332280`, tap `0x43323c0`, rig `0x4368b80`, primary camera `0x4368ec0`. This is deterministic independent allocation, not shared ownership. Checkpoint vector records begin at `0x4332500`, stride12. Relational assertions verify all identities.

## 3. Projection, timing and mixed candidate selection

Original Director frames establish the music anchor wall9452/E0. E1000 is wall10452; E1250 is wall10702. Effective time is read from the native GameTimeline, not assigned into it. Each Director frame reaches exactly one guarded GameModel update despite repeated scene visits. JNI refreshes the timeline without invoking a full model frame.

Native lane4's input-plane center is(212.5,0,0). Original projection `0xbdbb70` and Director height conversion produce external JNI(775.8657836914062,617.340705871582). Original unprojection agrees within0.5 world units and selects lane4. Python supplies only projection buffers, clock and JNI inputs, not camera matrices, note positions or lane results.

JNI `0xbe31a8 → EventDispatcher → 0x194ff80 → 0xeec024` executes for every DOWN. Both original note pointers occur in every observed before/after-sort candidate vector. The collector's hold predicate operands are recorded at `0xeec4c0/0xeec4cc`: initial eligibility requires lane match, `start < E+100` and `E < end`. It does not exclude this hold for an existing latch.

Original sorter `0xf6b514` runs. Hold-first vectors are `[hold1000,tap1250]`; tap-first vectors are `[tap950,hold1000]`. Native iteration observations at `0xeec53c` identify visited pointers. Collection already has chronological order in these examples, so execution proves sorter invocation/output, not an actual reordering. Signed-start-only comparison is separately instruction-backed by004; no equal-key stability or note-type priority is inferred.

The relevant original exit instructions are disassembled and executed:

```text
tap call 0xeec568 -> 0x160ce28
0xeec56c: if classifier bit0 is false, continue at0xeec530
0xeec570: otherwise branch to initial-loop exit0xeec744

hold cast selects0xeec6ec
0xeec6ec: W8=1
0xeec6f0: store byte1 to hold+0xa8
0xeec6f4: branch to initial-loop exit0xeec744
```

The latch branch does not inspect its prior value before the store. This is tested dynamically by the1→1 case below.

## 4. A1 — Previously unlatched hold

No earlier DOWN is delivered. The Director E1250 frame leaves both objects active/input-enabled/unresolved, hold latch0/activity0/0, all checkpoint flags0, no contacts and untouched counters/H0.

DOWN42 creates slot0/native Touch `0x4ecc400`/generatedID0. Both candidates exist, but only hold1000 is visited. Original `0xeec6f0` writes latch0→1; `0xeec6f4` stops initial iteration. There is no tap classifier or recorder during this DOWN. The tap remains available and unconsumed; the latch itself awards no checkpoint.

E1251 resets activity, processes the retained Touch, calls original hold activation and resolves checkpoint1250 once. A repeated E1252 frame reads its resolved guard and does not repeat recording. No retained-frame path substitutes for fresh tap classification: the competing tap remains unplayed. E1350 produces no tap miss; E1351's original expiry calls `0x868e54`, LR `0xf80b74`, for that tap. This is a frame-produced LOST, not initial classifier LOST or result synthesis.

Subsequent E1375 and1625 frames resolve checkpoints1500/1750 once. Terminal UP42 atE1626 empties contact state; E1627 leaves activity0/0/latch1 without another record.

## 5. A2 — Previously latched and active hold

DOWN42 atE1000 stops on the hold and writes latch0→1. E1001 establishes continuous activity1/1; E1125 resolves checkpoint1250, so the later comparison starts with PURE1 and health20.200000762939453. This is deliberately a different history from A1.

AtE1250 both notes remain active, original Touch42 is retained and hold latch/activity are1/1/1. DOWN43 creates slot1/a distinct Touch `0x4eceec0`/generatedID1 while Touch42 `0x4ecc3c0`/ID0 remains retained. Candidate vectors again contain hold then tap. Only the hold is visited: the same original store writes **latch1→1**, and iteration stops. Tap classifier count remains0; no judgment occurs during the second DOWN.

E1251 original continuous processing invokes `0x14557b4` for **both Touch pointers**, on the same hold. The first invocation sees activity0/0 after reset; the second sees1/1. No checkpoint is awarded twice. UP42 removes only its original mapping/slot/retention, preserving Touch43. E1252 resets activity and reactivates using **Touch43 alone**; later checkpoint recording continues normally. Thus the first latching Touch is not indispensable in this ordinary path.

The unplayed tap expires once atE1351. Checkpoints1500/1750 resolve atE1375/1625. Terminal UP43 and E1627 clear all remaining contact state/activity while preserving latch1 and counters.

## 6. B — Tap-earlier comparator

This fresh fixture has tap950, not1250. AtE1000 both notes are active/unresolved and hold latch0. DOWN42 creates slot0/Touch `0x4ecc3c0`/generatedID0. Original sorter output is tap950 then hold1000. The tap's native error50 produces judgmentID1, **PURE but not shining**, through `0x1730290` with LR `0x160cf90`. Native ordinary acceptance writes tap consumed1/contactID0. Classifier return1 stops at `0xeec570`; the hold is not visited and latch remains0. Score2500000/H20.200000762939453 comes from native recording.

DOWN43 is delivered at the **same wall/E1000**, without another model frame. Both notes still appear in the candidate list. Tap classifier reads consumed guard1 and returns0, so `0xeec56c` continues to the hold. Original latch0→1 and hold exit execute. There is no duplicate tap award.

The two retained contacts coexist through E1001, and both independently reach original hold activation. Then UP43 removes the separate latching contact. AtE1002 original continuous processing resets activity and reactivates the hold using **Touch42**, the contact that originally judged the tap. That same remaining contact sustains all three checkpoint judgments. The first DOWN did not simultaneously latch the hold; the second DOWN legitimately supplied the latch before these continuous frames. A separate frame with only the first Touch and latch0 is not run; the latch requirement itself is instruction-backed at `0x1485dac/0x1485db0`.

Original terminal UP42/E1627 completes cleanup. No miss is recorded in this case.

## 7. Continuous state, checkpoint provenance and score/gauge

Original `0x1866038` writes activity+0x64/+0x65 to0 for each new model frame. Retained-contact processing `0x14858d4` evaluates the original lane, strict `start < E < end` and latch predicates. At original virtual callsite `0x1485e60`, X0 is the same native hold, X1 the observed native Touch and the vtable target is `0x14557b4`. Original `0x14557ec` writes0x0101 to the activity bytes. No host latch, contact, activity or owner assignment is used.

Checkpoint resolution is distinct: original `0xf80904` guards each record, `0xf80924` writes resolved0→1 once, and `0xf809a4 → 0x1730290` (LR `0xf809a8`) records each weight1 with judgmentID0. The recorder's raw contact argument is0xffffffff (signed−1); upstream activation pointer evidence establishes which retained Touch sustained activity. It must not be misrepresented as a checkpoint's stored owner ID.

| Native event | A1 unlatched | A2 previously active | B tap-earlier |
|---|---|---|---|
| Tap acceptance | None | None | E1000, ID1, Touch42 |
| Checkpoint1250 | E1251, ID0 | E1125, ID0 | E1125, ID0 |
| Tap expiry | E1351, one LOST | E1351, one LOST | None |
| Checkpoint1500 | E1375, ID0 | E1375, ID0 | E1375, ID0 |
| Checkpoint1750 | E1625, ID0 | E1625, ID0 | E1625, ID0 |

Hold-first native health progression is0→20.200000762939453→18.200000762939453 after the tap miss→38.400001525878906→58.60000228881836. Tap-first progression is0→20.200000762939453 on the tap→40.400001525878906→60.60000228881836→80.80000305175781. These are original writes, not independently computed health assignments. The tap's non-shining PURE differs in score bonus, not in the observed first health gain.

| Final native state atE1627 | A1 | A2 | B |
|---|---:|---:|---:|
| N / chart end | 4 / 2500 | 4 / 2500 | 4 / 2500 |
| PURE / FAR / LOST | 3 / 0 / 1 | 3 / 0 / 1 | 4 / 0 / 0 |
| Shining / combo | 3 / 2 | 3 / 2 | 3 / 4 |
| Score | 7500003 | 7500003 | 10000003 |
| Live health | 58.60000228881836 | 58.60000228881836 | 80.80000305175781 |
| Accepted / miss recorder entries | 3 / 1 | 3 / 1 | 4 / 0 |
| Checkpoint0→1 stores | 3 | 3 | 3 |
| Finished / cached result | 0 / null | 0 / null | 0 / null |

A2's pre-second-DOWN counters differ from A1's pre-first-DOWN counters; the report/JSON preserve those intermediate states and recorder deltas. Equal final totals do not establish identical preconditions.

## 8. Cleanup, native counts and earlier evidence

Every UP uses original `0xdda71c → 0xf9a50c`. Android-ID map, slot pointers, active mask and model retained vector agree. A2 partial release preserves pointer43/slot1/ID1; B partial release preserves pointer42/slot0/ID0. Each UP leaves note/checkpoint/score/gauge state unchanged immediately. After the final UP atE1626, the next original Director frame leaves activity0/0/latch1 and unchanged score. Reference release runs within the inherited reclamation boundary; physical destruction is not proven.

Per-case original counts:

| Entry | A1 | A2 | B |
|---|---:|---:|---:|
| Whole AFF / runtime builder / hold factory | 1 each | 1 each | 1 each |
| Spatial index insertion, including bars | 506 | 506 | 506 |
| GameModel frames | 13 | 16 | 15 |
| JNI DOWN / UP / listener begin | 1 each | 2 each | 2 each |
| Candidate sorter | 1 | 2 | 2 |
| Tap classifier | 0 | 0 | 2 |
| Hold activation virtual | 8 | 12 | 11 |
| Completion delegate / result snapshot | 0 / 0 | 0 / 0 | 0 / 0 |

This extends026's hold reacquisition with actual same-lane tap competition and continuous use of the other retained contact. It extends027's separated-lane contact coexistence without assuming independent judgments when both contacts select the same older hold. Like035, chronological order and native consumed/missed guards matter; here a latch branch, rather than a tap classifier, can stop the event before an on-time competing tap is classified. Previous verified scopes remain valid.

## 9. Scenario, assertions and actual regressions

New `src/mixed_hold_tap.py` implements `hold_unlatched`, `hold_latched` and `tap_first` in independent fresh emulators. It reuses existing solo-entry/lifecycle/ABI/resource services unchanged. CLI/config gain only scenario/fixture registration; README appends instructions. No old fixture, test, assertion or successful scenario implementation changes.

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario mixed_hold_tap \
  --output /path/outside/research_harness/mixed-hold-tap-result.json
```

Actual final invocation uses `/tmp/arconist037/bin/python`, `--archive project_sources/01-arccopy.zip`, `--scenario mixed_hold_tap`, `--output audit/037/final.json`: **exit0/status pass**, all three gates per case pass, no native failures. The initial diagnostic also passed; only assertions for its observed causal relationships were added before the independent final run. No gameplay state or observation offset was repaired and no traces were spliced.

Assertions require original construction/ownership/index/admission, both mixed pointers before/after chronological sorting, exact visited/stopping pointers, native latch writes, consumed guard behavior, two distinct Touch/generated IDs, original activation of each and survival of the remaining contact, unique checkpoint writes/guard skips, original recorder delta accounting and complete cleanup. Native scores and health are observed; no Python gameplay equation supplies them. Unexpected exceptions preserve available case evidence and leave later cases not_run.

Fresh existing CLI commands use the same interpreter and archive:

```bash
/tmp/arconist037/bin/python research_harness/run.py \
  --archive /workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
  --scenario NAME \
  --output /workspace/scratch/90d77f091ffe/audit/037/NAME.json
```

| NAME | Actual exit / JSON status | Seconds |
|---|---|---:|
| ordinary — full session/results/SQLite | 0 / pass | 19.850 |
| chord — both orders | 0 / pass | 38.418 |
| moving_arc — moving and crossing | 0 / pass | 45.765 |
| timing_group — grouped and reverse | 0 / pass | 45.329 |
| cpu_note — refresh/expiry | 0 / pass | 52.390 |
| late_input_expiry — both interleavings | 0 / pass | 47.115 |
| noinput_semantics — paired lifecycle | 0 / pass | 53.118 |

Existing tests were actually executed with all three archive switches set:

```bash
ARCONIST_TEST_ARCHIVE="$ARCHIVE" \
ARCONIST_ARC_TAP_TEST_ARCHIVE="$ARCHIVE" \
ARCONIST_HOLD_TEST_ARCHIVE="$ARCHIVE" \
/tmp/arconist037/bin/python -m unittest discover -s research_harness/tests -v
```

Here ARCHIVE is the same supplied external ZIP, not a new input. All five tests pass in66.276s, process exit0, **no skips**: actual arc-tap CLI, actual hold release/reacquisition dual-case CLI, missing archive, native unavailable-song negative and wrong hash. Together with the seven CLI rows, these execute all nine established successful gameplay scenarios. Generated JSON/logs remain outside publication. Blocked camera/track/flick/continuous-gauge/Designant diagnostics remain unchanged and are not rerun or counted as successful gameplay.

## 10. Scientific boundaries and publication

**Native-executed:** original ordinary entry, AFF/runtime objects/checkpoints/count/index, admission, Director/GameModel updates, JNI listener/collection/sorting, latch/classifier/recorder/expiry, continuous activation and mapping/retention cleanup. **Instruction-backed:** signed-start comparator and untaken alternative branches, including latch0 rejection during continuous input. **External supplied input:** synthetic AFF, wall clock, JNI transport coordinates/IDs and inherited offline catalog/account/settings/platform/resource/ABI interfaces. **Interpretation:** initial-loop consumption is distinct from later contact participation; no persistent exclusive hold owner is established by these observations. **Unexecuted:** equal-key arbitration, arbitrary note-type combinations, more than two contacts, first-contact-only continuous processing with latch0, real Android scheduling, GPU/audio-device output, completion/results/save or physical reclamation for these charts.

Exact inherited PC skips, no additions:

```text
0xf72110  -> 0xf72158   platform GLView attachment
0x16a4238 -> 0x16a48d8  shutter panels/native Node proxies
0x121581c -> 0x121584c  loading overlay
0xa507c4  -> 0xa519ec   loading artwork prefix
0xa51adc  -> 0xa5213c   remaining information artwork/canary
0x196fdac -> 0x196ffac  information closing visuals
0x891190 -> 0x89164c    results UI prefix
0x891688 -> 0x89219c    middle results UI, native save retained
0x8921dc -> 0x8928e0   post-save progression/UI
```

The last three results-only ranges are unentered here. Existing base Node visitation/render/flush, audio/GPU, font/CSB/archive-provider, libc/C++/math/locale/platform, allocator/autorelease and ordinary catalog/profile/settings boundaries remain supplied as documented in024–036. No new service or dependency is required; native TrackLayer initialization/CPU updates remain enabled.

Publication uses a non-forced child of the verified parent and exactly nine authorized paths: this report; append-only context; backlog row/history; harness README/run/config; new scenario and two synthetic fixtures. Every uploaded changed file is read back and compared with prepared content; parent/child trees and historical context's exact prefix are checked. All prior reports, fixtures, tests/assertions, successful scenario implementations, pins, blocked diagnostics, root instructions and unrelated blobs are preserved. G-001–G-012 statuses/history remain unchanged; G-013 is Verified for this scoped comparison. Original ZIP/library/assets, generated evidence, databases/dumps/environments/account information and secrets are excluded. The exact child SHA and immutable links are returned separately because a commit cannot embed its own hash.

## Pseudocode — observed original pathway

```text
for A1, A2, B in independent fresh native environments:
    supply synthetic AFF and unchanged ordinary external services
    original solo entry -> native GameScene constructor/loading
    original parser -> hold/tap builders -> checkpoints, N4/end2500
    original index -> Director activation -> native active membership
    original camera projects the shared lane contact point

    A1: Director E1250, no prior contact
        JNI DOWN42 -> candidates [hold1000,tap1250]
        original latch0->1 -> stop initial iteration
        Director E1251 -> retained42 activates hold -> checkpoint1250

    A2: JNI DOWN42 atE1000 -> hold latch
        Director E1001/1125 -> activity/first checkpoint
        atE1250 JNI DOWN43 -> candidates [hold1000,tap1250]
        original latch1->1 -> stop before tap classifier
        Director E1251 -> both retained Touches activate hold
        JNI UP42 -> Director E1252 -> Touch43 sustains hold

    B: Director E1000, fresh tap950 fixture
        JNI DOWN42 -> [tap950,hold1000]
        original tap ID1/PURE -> consumed/contact0 -> stop, hold latch0
        JNI DOWN43 at same wall/E, no model frame
        consumed tap classifier returnsfalse -> original hold latch0->1
        Director E1001 -> both Touches activate hold
        JNI UP43 -> Director E1002 -> tap-judging Touch42 sustains hold

    subsequent original frames:
        reset activity -> retained-contact activation -> checkpoint guards
        remaining checkpoints -> native ID0 recorders, once per weight
        in A1/A2 only: original tap expiryE1351 -> one miss recorder
    terminal JNI UP -> native map/slot/mask/retention cleanup
    Director E1627 -> activity0/0, latch1, no new judgment
compare native identities, causal calls, counters/gauge and cleanup
completion/results/SQLite for these charts: NOT RUN
STOP after037; no038 or S2-C04 selection
```

## Final research boundary

This establishes mixed chronological initial arbitration and nonexclusive retained-contact participation for one ordinary hold/tap pair in one native lane. It does not establish atomic OS multitouch delivery, a universal one-finger/one-note policy, unrestricted multi-note consumption or equal-start type priority. The bounded objective is complete; no deferred blocker is reopened and no further experiment is initiated.
