# Expedition 040 — Native Settings/Offset Production & Effective Judgment Clock

Date: 2026-10-30. Headquarters selected Scout 002 S2-C06 as **G-016**.

## Result

**Verified within the declared ordinary native-owned gameplay environment.** Four required fresh scenes establish regular/profile selection, an alternate profile and AFF/user addition through original Settings production, original Model/Timeline initialization, native music-start compensation and original JNI tap judgment. A fifth independent optional case joins original legacy migration to the same gameplay chain.

The Settings producer is stronger than a direct isolated loader call: original application initialization executes from `0x1a146a0`, allocates/constructs and publishes its application, allocates Settings, stores application+0x70, and calls the complete loader at its real `0x1a1476c` callsite. The diagnostic stops at the genuine loader-return boundary `0x1a14770`. Later application initialization is not executed or described as having returned. Established external application facades are rebound to that original-created application; its original-produced Settings pointer and offset fields persist into the native-created GameScene.

The four native combined offsets are0/80/80/200. At elapsed1500ms after each native playback request, effective chart times are1500/1420/1420/1300. Aligned E1500 judgments require elapsed1500/1580/1580/1700ms respectively. Each yields one shining PURE, score10000001 and live health80.19999694824219, with original recorder/consumption/contact cleanup and no duplicate. The legacy case natively migrates100 to80 and agrees with the regular80 case.

This is not full native Android application startup, original preferences-file parsing, executed audio-manager/FMOD output, route detection, physical latency or drift measurement. Those distinctions do not replace the executed settings-owner, timeline or gameplay decisions.

## 1. Source identity and preparation

Verified parent/main: `5ec8220e90176bf1d565202793baa17a06b367bc`; parent tree `f1064df8c3df07b702f6831c706f6a6e2250ed1d`. Expedition040 was absent. All107 repository blobs were restored from immutable parent resources after workspace maintenance and matched their original Git blob hashes before changes. Standing introduction, cumulative research/context/backlog, the supplied S2-C06 mission and relevant002/004/005/008–012/018/022–024/026–029/035–039 evidence and harness were reviewed. Scout002's separate complete advisory report is not published in this repository; this mission supplies the selected candidate and permanent objective.

External archive member `lib/arm64-v8a/libcocos2dcpp.so` is29217504 bytes and freshly verifies:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Execution retains Python3.12.14, Unicorn2.1.4 and pyelftools0.33. Capstone5.0.7 is used only as an external targeted-disassembly aid; dependency pins are unchanged. The temporary environment was recreated with the same pins after workspace maintenance. Original addresses below are ELF VAs. Emulated heap pointers are observations, not regression constants.

## 2. Original Settings ownership and the new boundary

A `.text` direct-branch survey identifies one direct caller of `0x1a02b48`, at `0x1a1476c`. Its containing original function has unwind extent `0x1a146a0..0x1a14a4c`. A higher application entry calls it at `0x1136934`; that higher entry is instruction-backed, not executed here.

Executed owner sequence:

| Original instruction/interface | Observed responsibility |
|---|---|
| `0x1a146d0/0x1a146d4` | Test original application singleton at `0x1bf23c0` |
| `0x1a14700 → 0x15779f0` | Allocate0x100 bytes and execute original application constructor |
| `0x1a1470c` | Publish the actual constructed application pointer |
| `0x1a1471c/0x1a14748` | Associate supplied external provider inputs at application+0x40/+0x48 |
| `0x1a1474c` | Original0x90-byte Settings allocation |
| `0x1a14754..0x1a14764` | Original Settings tail/string-state initialization |
| `0x1a14768` | Store actual Settings pointer at application+0x70 |
| `0x1a1476c → 0x1a02b48` | Original owning caller enters complete Settings loader; LR=`0x1a14770` |
| `0x1a031c4 → 0x1a14770` | Native loader returns to its real caller; observation stops before unrelated continuation |

This closes the original caller/ownership edge without synthesizing an instruction or calling the loader directly. Settings is plain data here; it is not assigned a fabricated vtable or claimed to be a Ref-derived object.

The existing bootstrap initially prepares unused application/Settings shells. The isolated adapter discards their use by restoring the original singleton's zero-initialized state **before** native creation. Native instructions then produce a different application and Settings allocation. The shells never become the Model's settings source. After the native prefix, only the established external audio/profile/local/provider/status/control/multiplayer/mode/framework interfaces are rebound to the native application. Application+0x70 is not rebound or repaired. The original0x40/0x48 provider associations already agree with the supplied inputs.

This is an explicit execution boundary: the application initializer is suspended at its post-loader instruction, not falsely described as a completed full initialization. Subsequent original scene entry uses the established driver call boundary and fresh call stack. No new **gameplay** branch is skipped. Later audio/account/session/UI initialization inside the application owner is unexecuted; supplied facades retain their historical scope. Completing those unrelated systems is not required to execute the original settings owner and its actual native gameplay consumer.

Host-write guards protect the new Settings offset fields, application+0x70, the published singleton and subsequently observed Timeline result fields. Read-only native memory hooks record actual stores. No driver writes preset, regular/alternate results, O, clock origins, C, E, note guards or score/gauge outputs.

Representative final-run relationships, independently re-created in each emulator:

```text
singleton 0x1bf23c0 -> application 0x4104a80
application+0x70   -> Settings    0x4104c40
GameScene         0x4327f00 -> Model 0x4355f00
Model+0x28        -> Chart       0x4331a00
Model+0x30        -> Timeline    0x4356080
Model+0x38        -> ScoreState  0x43560c0 -> LifeBarState 0x4356240
```

Repeated heap values reflect deterministic independent allocators, not one reused or cloned heap. Assertions check relationships within each fresh execution.

## 3. External backend versus native loading

`settings_backend_services.py` is an isolated040 adapter. It preserves the old scenarios' bootstrap unchanged. Existing backend getter `0x18a6b8c` remains the external persistence boundary. Native virtual calls use+0x00 bool, +0x08 integer, +0x10 float and +0x20 string getter contracts. The adapter returns explicitly supplied values or the original call's default; it does not parse a native preferences file or calculate Settings outputs.

All cases additionally supply the same grounded non-offset inputs: `language="en"`, synthetic diagnostic `installId="expedition040-synthetic"`, and `highspeed_int=40`. These are research inputs, not recovered personal preferences or an ownership/unlock grant. Other loader getters return the defaults actually passed by original instructions. Original bool/int/string conversion/default branches and Settings stores execute. Setter/other facade methods retain their existing inert service scope.

The application constructor consumes the language getter. Its earlier resource-directory initialization additionally needs the already established raw-provider `0xb99da4`, resource-prefix `0x1a1ad2c` and provider string-return interfaces earlier than ordinary `load_chart`. The isolated adapter supplies those existing boundaries at that earlier point. It does not reconstruct a filesystem, platform preference manager or a new account subsystem.

Actual offset getter calls:

| Key | Original virtual integer getter return address | Native default argument | Native store |
|---|---|---:|---|
| `audio_preset` | `0x1a02b88` |0 | `0x1a02b88 → Settings+0x00` |
| `offset_int_2` | `0x1a02c2c` |−2147483648 | `0x1a02c30 → +0x04` |
| `offset_int`, only missing-current case | `0x1a02c58` |−2147483648 | `0x1a02c58` subtraction, then `0x1a02c64 → +0x04` |
| `bt_offset` | `0x1a02c88` |−2147483648 | `0x1a02c94 → +0x08` |
| `highspeed_int` | `0x1a02cb4` |−2147483648 | Native+0x0c store |

The regular current key is present in A–D; legacy `offset_int` is not read in those executions. In the optional legacy case, the backend returns INT_MIN for missing `offset_int_2`; native code first stores that sentinel, then reads legacy100 and stores80. There is no second runtime−20 subtraction when current80 is present.

All five cases explicitly supply `bt_offset`; the missing-alternate default200 branch remains prior005/instruction-backed coverage, not a newly executed040 absence case. The both-regular-keys-missing zero fallback likewise is not part of this matrix. Their static/default support does not imply that a real account selected them.

## 4. Fixtures and native combined offset

The two synthetic charts are identical except AudioOffset0 versus120:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1500,3);
```

| Fixture | SHA-256 | Original complete-text MD5 |
|---|---|---|
| `native_offset_control.aff` | `113dd112fbcba61ac98c1f432080a97236d06c2043e1c72d51191c8b985d8ac1` | `0f898315637e96698109cabd5896fe15` |
| `native_offset_aff120.aff` | `a9886573261c66b7c555125adefb59011ad452de8d3f029d2980abd559e036b5` | `f3fca2ed28ddb06a657197a9fff29ee0` |

Every scene uses the unchanged ordinary sayonarahatsukoi/difficulty0/base/no-purchase/mode0/speed40-tenths/null-modifier/40-zero-PlayParameters context. Original static1930604 and registry1054f24 initialization, ordinary eligibility/ee197c entry, native allocation/constructor/loading and e2ea48 initializer return1 execute. Director activates the same GameScene, and its original listener is registered/enabled/unpaused.

Original1870de0 whole-file parsing,173b358 chart initialization and1862a14 runtime construction produce one LogicTapNote at1500. Raw lane3 becomes native lane4, group0/input-enabled1. Original native count N1, chart end1620, group0 index bucket1 and eventual active membership are observed. No count, lane, time, index or active pointer is supplied.

`0x173bcfc` calls the original AFF integer conversion interface; actual chart+0xc4 **store is `0x173bd0c`**. This refines the shorthand address rather than claiming the call itself is a store.

Model initializer `0xfbfd04` reads the same application/Settings chain. At `0xfbfed0`, its original global application points to0x4104a80 and Settings to0x4104c40. `0xfbfef8` reads Settings+4 for preset0 and+8 for preset1. Actual native addition operands at `0xfbff4c` and O store at `0xfbff54` are:

| Case | AFF | Native preset / regular / alternate | Selected user | Native O |
|---|---:|---|---:|---:|
| A baseline |0 |0 /0 /80 |0 |0 |
| B regular |0 |0 /80 /200 |80 |80 |
| C alternate |0 |1 /0 /80 |80 |80 |
| D combined |120 |0 /80 /200 |80 |200 |
| Legacy optional |0 |0 /80 /200 |80 |80 |

Original code allocates/initializes the Timeline, writes O at+0x30 and stores that same pointer into Model+0x30 at `0xfbff78`. Settings pointer identity and loaded values are checked throughout input/cleanup. Arithmetic is native signed32 for these small tested integers; no overflow/general-wrap claim is made.

## 5. Native clock origin, strict startup and compensation order

Original model start wrapper `0x8db04c`, LR=`0x14b29e8`, executes at wall6450. Native `0x8db088` stores steady/system origins6450/6450; `0x8db090` sets steady mode. The host supplies clock samples through the unchanged chrono boundary. Original `0x1271200` converts nanoseconds to native integer milliseconds; recorded examples are6451000000→6451 and10951000000→10951. No Timeline origin is assigned by the diagnostic.

Ordinary `0x16c90bc` executes through actual Director/GameScene/GameModel updates. In this steady/unpaused/A0 branch, native R is steady elapsed minus3000 and effective E=R−C. The startup comparison at `0x16c9170` tests E against−O, with equality returning through `0x16c9174`. Each case samples that exact equality frame and observes no playback request/latch.

A subsequent supplied1ms step makes the native predicate true. `0x16c9190` sets the music-started latch; original BL at **`0x16c9194 → 0x1735d7c`** requests playback, return address16c9198. The actual manager argument is the established external application+0x10 pointer0x4101780. It is captured **before** the inherited audio service executes. The audio-manager body/provider output remain inert/unexecuted; no actual BGM output is claimed. The manager's loop/index/delay internals remain prior005 instruction-backed evidence, not newly observed arguments to this no-extra-argument wrapper call.

Crucially, request entry precedes compensation. At that instruction E=1−O; after the request returns, original `0x16c91d8` writes C=R+O, and `0x16c91dc` writes B=−O. Those native stores make E exactly−O. The report does not conflate these moments.

| Case | Equality wall / E, no request | Request wall / R / pre-C | Request-entry E | Native post-request C / B / E |
|---|---|---|---:|---|
| A |9450 /0 |9451 /1 /0 |1 |1 /0 /0 |
| B |9370 /−80 |9371 /−79 /0 |−79 |1 /−80 /−80 |
| C |9370 /−80 |9371 /−79 /0 |−79 |1 /−80 /−80 |
| D |9250 /−200 |9251 /−199 /0 |−199 |1 /−200 /−200 |
| Legacy |9370 /−80 |9371 /−79 /0 |−79 |1 /−80 /−80 |

The common C1 is an observed consequence of scheduling a1ms crossing, not a supplied compensation value. Larger startup overshoot, pauses, adjustment modes and hardware/backend scheduling are not new040 experiments.

## 6. Equal elapsed time and aligned native judgment

External measurement Δ is wall time minus the **observed native request wall**, not a field written to the Timeline. First sample Δ1500 without input, then advance only if necessary until original native E reaches1500:

| Case | Wall at Δ1500 | Native R / C / E | Diagnostic note−E | Δ at aligned E1500 | Absolute aligned wall |
|---|---:|---|---:|---:|---:|
| A |10951 |1501 /1 /1500 |0 |1500 |10951 |
| B |10871 |1421 /1 /1420 |80 |1580 |10951 |
| C |10871 |1421 /1 /1420 |80 |1580 |10951 |
| D |10751 |1301 /1 /1300 |200 |1700 |10951 |
| Legacy |10871 |1421 /1 /1420 |80 |1580 |10951 |

This controlled schedule has equal original start epochs and a1ms startup crossing in each case. Consequently absolute aligned wall time agrees; music-request-relative elapsed time differs. It would be misleading to claim these runs require different absolute host times or measured speaker latencies. The measured causal effect is the native settings-derived offset's request alignment and effective E at equivalent elapsed intervals since that request.

No contact occurs at the equal-Δ sample. Every tap is unresolved/active, counters0 and chart unfinished. The separate fixed-Δ input control is unnecessary and not run. No tap is consumed early and reused for aligned testing.

Original native primary Camera0x4368ac0 projects lane4's ordinary input-plane target(212.5,0,0) through `0xbdbb70`, using Director1280×720. Y conversion gives identical JNI coordinates in all five scenes:

```text
(775.8657836914062, 617.340705871582)
```

These are external test inputs derived using native projection and original lane semantics, not host-assigned note geometry. Original unprojection returns the target within0.5 units and native selector returns lanes(4,0). The note is genuinely active/indexed/input-enabled at E1500.

## 7. JNI classifier, recorder, gauge and cleanup

At aligned E1500, original `0xbe31a8 → GLView/EventDispatcher → 0x194ff80 → 0xeec024` executes with Android pointer42 and controlled stored event timestamp987042. The input's native timeline refresh is observed separately from its enclosing Director model frame; no direct Timeline/model/classifier call substitutes for that path.

Before/after native sorter `0xf6b514`, the candidate vector contains only the original tap. Original `0x160ce28` reads native E1500 and note1500; `0x160cec0` observes absolute error0, hence signed timing error0. `0x160ce74` reports consumption true. Accepted recorder `0x1730290` is called once from LR=`0x160cf48`, judgment ID0; native acceptance `0x965e28` writes consumed state and generated contact ID. The independent miss recorder868e54 is never entered for this note. No final synthesized result counter is substituted for a real callback.

Identity after DOWN:

- Android42 → native engine slot0 → generated gameplay ID0.
- One original-allocated native Touch, retained by the Model; its stored input timestamp is987042.
- The accepted note stores that generated ID0.
- JNI input executes no intervening full Model frame; its Timeline update still reads E1500.

The timestamp987042 is deliberately distinct from native E1500. This proves the tested callback uses the native Timeline, not that physical Android latency or all timestamp consumers have been characterized.

All five live results:

```text
N1; PURE1 / FAR0 / LOST0; shining1; combo1
score10000001; H80.19999694824219
```

Original JNI UP `0xdda71c` clears Android mapping, slot pointer, active mask and retained vector. Cleanup leaves score/gauge and note consumption unchanged. An original E1501 Director frame removes consumed active processing without another recorder/miss. Settings remain unchanged; O remains original-produced; charts are unfinished with null result cache. Completion/result/SQLite are not required and are not executed for this new chart.

Final native counts per case: baseline7 Director entries/6 model entries/7 Timeline updates/9 steady-ms samples; other cases8/7/8/10 because they require the additional aligned frame. Every case has one native start request, JNI DOWN/UP/listener/classifier/acceptance/accepted recorder; miss/finish/snapshot0. Repeated visits are not counted as extra model updates.

## 8. Reproducible implementation and validation

New scenario: `src/settings_offset_clock.py`; isolated producer/backend adapter: `src/settings_backend_services.py`; two synthetic fixtures. Only run.py/config.py registration and appended harness documentation alter established harness files. No old scenario, fixture, assertion or dependency declaration changes.

The driver runs five independent fresh emulators. Assertions check original caller/global/Settings stores, same-pointer consumer/profile/addition operands, actual chart/index/active/listener products, strict startup and writer order, R/C/O samples, native projected input/candidate/classifier/recorder identity and cleanup. Expected arithmetic is a comparison/schedule oracle, never written into native outputs. Failures preserve accumulated native evidence and distinguish blocked later stages.

The first isolated owner probe lacked the already established resource-provider/prefix boundaries at their earlier application-initialization point. Binding those existing services closes that prepared-interface omission; no new filesystem/account/graphics reconstruction follows. The first integrated diagnostic reached judgment/cleanup but failed its final audit because it incorrectly forbade the inherited inert1735d7c audio service. The corrected audit explicitly preserves that boundary. A subsequent complete diagnostic passes. Final verification additionally observes the original singleton write and captures the manager argument at the original BL before the earlier-registered service hook can replace X0 with its zero return. The preliminary entry-only manager0 was an observer-order artifact, not a native missing-manager finding. Independent final execution passes all five gates in all five cases, with no native failures. Failed traces are not spliced into it, and no gameplay state is repaired.

Actual final invocation, exit0 / JSON status pass:

```bash
/tmp/arconist040/bin/python research_harness/run.py \
  --archive project_sources/01-arccopy.zip \
  --scenario settings_offset_clock --output audit/040/final.json
```

Prior CLI command form, with actual scenario/output substitutions below:

```bash
/tmp/arconist040/bin/python research_harness/run.py \
  --archive /workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
  --scenario SCENARIO \
  --output /workspace/scratch/90d77f091ffe/audit/040/SCENARIO.json
```

| SCENARIO | Exit | JSON | Seconds |
|---|---:|---|---:|
| ordinary |0 |pass |31.425 |
| chord |0 |pass |59.663 |
| moving_arc |0 |pass |63.616 |
| timing_group |0 |pass |58.884 |
| cpu_note |0 |pass |72.071 |
| late_input_expiry |0 |pass |62.072 |
| noinput_semantics |0 |pass |63.966 |
| mixed_hold_tap |0 |pass |98.103 |
| linked_arc |0 |pass |37.287 |
| lane_widening |0 |pass |79.675 |

The existing five tests actually execute using all three archive opt-ins:

```bash
ARCONIST_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_ARC_TAP_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
ARCONIST_HOLD_TEST_ARCHIVE=/workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
/tmp/arconist040/bin/python -m unittest discover -s research_harness/tests -v
```

Exit0; **5 tests, all OK, zero skips**,67.190s (67.262s including process overhead). Native arc-tap and hold cases actually run, plus missing archive/unavailable song/wrong ELF hash controls. Thus all twelve previous successful gameplay scenarios remain green, including ordinary results/SQLite. These runs use the modified CLI/config tree; subsequent changes only add read-only evidence/relational checks to the new040-only modules and are covered by the independent final040 run. Existing blocked camera/track/flick/continuous-gauge/Designant diagnostics are unchanged, not rerun and not counted as green gameplay.

## 9. Evidence classes and preserved boundaries

**Native-integrated:** original application/Settings producer prefix, complete native loader and typed getter calls/default/migration/store logic, same-pointer scene/model consumer, AFF offset/count/index/tap creation, Timeline origins/profile/addition, Director-driven startup comparison/latch/compensation/progression, original JNI lane/candidate/classifier/recorder/consumption and cleanup.

**Externally supplied:** synthetic AFF, research persistence dictionary and typed getter returns, established catalog/account/profile/local/application/platform/clock/JNI/ABI/resources/audio/graphics/allocator/autorelease interfaces. These are not original preference-file contents or a new actual user account.

**Instruction-backed but not executed here:** higher application caller1136934, later owner body after1a14770, untaken offset/default/fallback branches, nonordinary clock/mode branches and actual audio-manager/provider scheduling internals.005's prior isolated findings keep their historical scope.

**Interpretation:** the logical music-relative offset sign follows the observed request anchor/progression; it is not physical output timing. **Unknown/unexecuted:** actual persisted on-disk format, UI calibration/session startup, automatic Bluetooth routing, DAC/speaker output, Android queue/device latency, oscillator drift correction, arbitrary signed overflow, negative-offset matrix, pause/resume interactions in these new cases and completion/persistence for this fixture.

Exact inherited PC skips are unchanged:

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

The last three results-only ranges are unentered. Existing base Node visit/draw/flush, presentation proxies, resource/font/CSB/texture services, original CPU TrackLayer updates, audio start/SFX, libc/C++/math/locale/TLS/locks, allocator/autorelease and JNI interfaces retain their existing scope. The additional application-prefix observation stop is explicitly recorded separately; it does not skip a gameplay settings/clock/judgment decision. No new gameplay PC skip, original instruction patch, account adapter, entitlement, mode or derived-state override is introduced.

## 10. Publication and preservation

Publication is a narrow, non-forced child of the verified parent. Ten changed paths: this report, append-only context, G-016/history backlog addition, harness README/run/config, new040 scenario/adapter and two synthetic fixtures. Only those five established files change; all other parent blobs, reports001–039, old fixtures/scenarios/tests/assertions/pins, blocked diagnostics, root instructions and unrelated files remain exact. Historical context remains a byte-for-byte prefix. G-001–G-015 rows/status/history are preserved; G-016 is Verified within this bounded scope.

Changed committed files are fetched by immutable SHA and compared exactly; parent/child trees and ancestry/main are verified. No archive/ELF/proprietary resources, generated JSON/logs/traces/dumps, databases/environments, account data, saved personal preferences or credentials are committed. Exact child SHA and pinned report/context/backlog links are returned to headquarters separately.

## Pseudocode — observed original chain

```text
for baseline, regular80, alternate80, AFF120+regular80, optional legacy100:
    create fresh emulator with verified original ELF
    supply controlled persistence getter data and established external services
    restore original empty application-singleton input state
    original application initialization prefix:
        native application allocation/constructor/publication
        native Settings allocation -> application+0x70
        real owning callsite -> complete original loader
        original getters/defaults/current-or-legacy logic -> Settings fields
    stop at genuine post-loader boundary; later app initialization NOT RUN
    bind only established external application facades
    preserve native application and loaded Settings pointer

    original ordinary solo entry/loading -> native GameScene
    original AFF parser/runtime builder -> chart offset and tap/index/N
    original Model reads same Settings:
        native preset selection + AFF offset -> Timeline O
    original scene activation -> native clock origins/steady mode

    Director frame at startup equality -> no music request
    next1ms frame:
        original Timeline sets latch and requests external audio service
        then native compensation stores -> E=-O
    frame at observed music-request elapsed1500 -> sample native E, no input
    advance original Director until native E1500
    native camera projection -> supplied JNI DOWN
        original Timeline refresh/lane/candidate/sort/classifier
        native accepted recorder/consumption/score/gauge
    JNI UP -> original mapping/slot/mask/retention cleanup
    next Director frame -> no duplicate judgment
compare observed offsets, request anchors, elapsed times and native outcomes
run prior successful regressions; preserve blocked diagnostics
update G-016 and publish bounded evidence
STOP before041/S2-C07
```

## Final research boundary

The original Settings owner/loader and original ordinary GameScene consumer are joined for regular, alternate, AFF-combined and one legacy-migration input. Their native-produced offsets determine music-request-relative E and the elapsed interval required for a genuine JNI judgment. Complete later application startup, preference storage format, executed audio output, device route/latency, universal modes and drift correction are not established. No further gameplay experiment is required for this bounded objective. Stop after040 without041 or reopening deferred objectives.
