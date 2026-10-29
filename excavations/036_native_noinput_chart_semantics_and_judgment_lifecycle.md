# Expedition 036 — Native `noinput` Chart Semantics, Judgment Count & Expiry

Date: 2026-10-29. Objective: **G-012**, selected by headquarters from Scout 002 S2-C02.

## Result

**Verified for the paired ordinary native-owned tap experiment.** Original parsing and construction preserve the `noinput` tap as a runtime object, with input-enabled byte zero. Original code excludes it from judgment count N, chart-end calculation, JNI candidates and expiry recording. It remains indexed and active through native completion. It does not add a recorded or synthesized LOST to the completion-produced GameResult.

The equal-time control and attribute variant finish at E1621, with native N2/PURE2/LOST0 versus N1/PURE1/LOST0. The chart-end branch filters the disabled object even though the equal timestamps leave the maximum unchanged. A separate group-lifetime pass still consumes its end time. This is a scoped original-native observation, not a rule inferred from the attribute name.

No gameplay state repair, new platform service, dependency or PC skip was added. All established successful gameplay scenarios and all five existing tests pass. Results-scene activation and SQLite saving for these two charts are not run.

## 1. Sources, provenance and environment

Verified parent/main: `d7023df923dc05b2f0f71348ab6d53fe34c715ba`; parent tree `0e92421605787bac48ade38c5fafd0bfc8ece731`. Expedition 036 was absent. The 65 locally present parent files matched their original Git blob hashes before edits. Main was rechecked before publication.

The supplied introduction, complete cumulative context/backlog, relevant reports 002/004/008–011/018/022–024/029/032/035 and current harness were reviewed. Scout 002's supplied S2-C02 mission is the provenance of this objective; no additional Scout candidate is selected.

External read-only archive: `arccopy.zip`; library member `lib/arm64-v8a/libcocos2dcpp.so`. Fresh SHA-256:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Actual runtime: Python 3.12.14, Unicorn 2.1.4, pyelftools 0.33. Existing dependency declarations are unchanged. Capstone 5.0.7 was used outside the package for targeted disassembly only; it is not a scenario dependency. No clean-install milestone is claimed.

All instruction addresses below are **original ELF virtual addresses**. Heap pointers are observations in independent emulated address spaces; assertions use relationships rather than fixed heap constants.

## 2. Paired chart and original scene production

The new synthetic fixtures differ only by `timinggroup()` versus `timinggroup(noinput)`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1500,4);
timinggroup(noinput){
    timing(0,60.00,4.00);
    (1500,1);
};
```

Native-computed MD5 is `c63168a49504901a37c1d0b8165d0377` for control and `1a280c340a78b91adfef65f44c427454` for `noinput`; no digest/property is patched. These are research charts, not archived released charts.

Each fresh emulator uses unchanged `sayonarahatsukoi`, difficulty0/base/no purchase, ordinary mode0, speed40 tenths, null modifiers/map and zero PlayParameters. Original static initialization `0x1930604` and song registry `0x1054f24` are retained. Original solo entry `0xee197c` passes eligibility, sets the request latch and reaches `0xee29a8 → 0xee29e8`. Original loading invokes GameScene initialization `0xe2ea48`, returning1. Director activates the same scene; its original gameplay listener is registered/enabled and unpaused.

Whole-file parser `0x1870de0`, chart initializer `0x173b358` and runtime builder `0x1862a14` execute through that lifecycle. Both scenes contain two distinct `LogicTapNote` objects at1500: raw lane4 becomes native lane5/group0; raw lane1 becomes native lane2/group1. Each note's timing pointer at+0x48 belongs to its corresponding original timing list. Original group stores at `0x18640ec` write+0x50. Native type/vtable evidence includes `12LogicTapNote` and vtable VA `0x1af4278`; initializer `0x1902ffc` returns1.

Representative runtime identities, not required constants:

| Object | Control | `noinput` |
|---|---|---|
| GameScene | `0x4327c40` | `0x4327c40` in a fresh address space |
| GameModel | `0x4356680` | `0x4356700` |
| Chart | `0x4331e80` | `0x4331f00` |
| ScoreState | `0x4356840` | `0x43568c0` |
| Default / grouped tap | `0x4332980` / `0x4332a80` | `0x4332a00` / `0x4332b00` |
| Native cached GameResult | `0x4ed3740` | `0x4ed3680` |

## 3. Attribute and flag producers

At `0x8c85c0`, original parser attribute tokens are empty versus `["noinput"]`. The original string comparison at `0x8c89f4` returns0 for the latter. At `0x8c8a14`, `strb wzr,[x25,#0xc]` changes the grouped parsed SimpleNote flag from1 to0; the next instruction observation confirms zero. Control parsed flags remain1.

Builder `0x18640f4` copies that parsed byte into the original-created logic object's+0x54. Read-only memory hooks attribute the stores to the original instructions. Default/grouped input bytes are `[1,1]` versus `[1,0]`. Python neither constructs the notes nor assigns either flag.

## 4. Count, chart end, group lifetime and index

Original `0x11ea120(chart,0,INT_MAX)`, called with LR `0x173bf2c`, observes two main objects before auxiliary bars. Its `0x11ea184/0x11ea188` flag read/branch counts both enabled control taps, but skips the disabled grouped tap. Native return2 versus1 is stored to chart+0xb8 at `0x173bf2c`, and agrees with ScoreState N. Auxiliary generation subsequently raises the main-vector size to505 in both cases; this is not N.

The original chart-end pass resets chart+0xbc at `0x18655c0`. At `0x1865608/0x186560c`, it checks each tap's input flag. Enabled taps reach end-time observation `0x1865628` with W20=1500 and candidate observation `0x1865658` with W28=1620. The default tap causes the native maximum store at `0x1865678`. The disabled grouped tap takes the loop continuation `0x18655f8` before those end/candidate observations. Thus its exclusion is directly observed, not inferred solely from the equal final1620 values.

The optional later-note pair is **not run**: per-object branch and operand evidence answers the filtering question for the tested path. No later-timestamp execution is claimed.

A different pass at `0x173c22c` still uses the grouped object's end plus1200 and writes group1 lifetime2700 in both scenes. `0x173c24c` gives the default group INT_MAX. Descriptor leading bytes are `[1,0,0,0]` in both groups. Exclusion from chart-end calculation does not imply exclusion from group lifetime processing.

Original timing lists contain native scales0.12361110746860504 for120 BPM and0.24722221493721008 for60 BPM. Their observed record bounds are INT_MIN through1001620. Original `0x1576aa4` runs505 times including bars; filtered tap observations at `0x1576b98` show default group0/key1 and grouped group1/key0 in both original maps. No input-flag filtering occurs in these observed tap insertions.

Original active-range processing `0x10fd1c0` admits the grouped tap during preroll, even with flag0; both taps are active at E1500. Index membership, active membership, input eligibility and N are separately recorded. The JSON admission field `native_min_depth` is a raw unsigned32 register snapshot, not a signed positive-depth interpretation.

## 5. JNI input, candidates and recorder provenance

Native music anchor is wall9452/E0; E1500 occurs at wall10952. Original Director/scene/model frames establish both taps active, unresolved and unconsumed. Original primary-camera projection `0xbdbb70` derives the following external inputs, with native Y-up converted using Director height:

| Target | Native world point | External JNI point |
|---|---|---|
| Group1 / native lane2 | (−637.5,0,0) | (232.40264892578125,617.340705871582) |
| Default / native lane5 | (637.5,0,0) | (1047.597412109375,617.340705871582) |

Original unprojection and lane results agree with the intended native targets. The same schedule runs in both scenes: DOWN42/UP42 for group1, then DOWN43/UP43 for default, all atE1500, with no intervening model frame or clock change.

Original JNI `0xbe31a8`/`0xdda71c`, EventDispatcher and gameplay listener `0x194ff80` execute. Pointer42 creates engine slot0, a native Touch and generated gameplayID0. After cleanup, pointer43 reuses slot0 with a distinct native Touch and generatedID1. Even the disabled target's DOWN creates and retains a Touch; that is not note acceptance.

Collector `0xeec300/0xeec304` reads/checks logic+0x54. In the attribute case group1's zero flag skips its candidate path. Before/after-sort observations at `0xeec4e0/0xeec4f0`, around original sorter `0xf6b514`, are empty for that input. No classifier or recorder runs for the disabled tap. Control group1 and both default inputs instead have singleton correct-note candidate vectors. Classifier `0x160ce28` returns a consuming result for each accepted tap; original accepted recorder `0x1730290` and acceptance `0x965e28` execute. Native `0x965e68/0x965e6c` write consumed byte/contact ID. The disabled tap keeps consumed0, missed0 and acceptedID−1.

Each original UP empties the Android map, slot pointer, active mask and model retained-contact vector without changing notes or score. Input outcomes are observations, not driver-supplied success rules.

## 6. Expiry, original completion and GameResult

Original Director frames visit E1501/1600/1601/1620/1621. Consumed taps leave active processing at1501. The disabled grouped tap remains active through1621. At `0xf80650/0xf80654`, each relevant expiry pass observes its zero input flag and skips it. Original miss recorder `0x868e54` executes zero times in both scenes. The no-miss claim is supported by the per-object native flag predicate, not only by unchanged counters.

Finished remains0 at1620 and becomes1 at1621. Native completion block `0x10a7d50` reaches `0xc27d34` with LR `0x10a7d6c`; that original delegate calls snapshot `0x1600bb0` with LR `0xc27dd0`. Original `0x1600d80` stores its result into the original ScoreState+0x68. Delegate and snapshot each execute once. Each scene has nine model/expiry entries,36 scene visits and10 Director entries: the scene guard preserves one model update across repeated visits.

At snapshot reconciliation `0x1600c4c`, N−PURE−FAR=0 and recordedLOST=0 in both scenes. The disabled tap contributes neither a recorder LOST nor an additional final synthesized LOST.

| Observation | Control | `noinput` |
|---|---:|---:|
| Runtime taps / N | 2 / 2 | 2 / 1 |
| Chart end / first finished E | 1620 / 1621 | 1620 / 1621 |
| Accepted / miss recorder entries | 2 / 0 | 1 / 0 |
| PURE / FAR / LOST | 2 / 0 / 0 | 1 / 0 / 0 |
| Shining / combo | 2 / 2 | 1 / 1 |
| Native score | 10000002 | 10000001 |
| Live health | 80.4000015258789 | 80.19999694824219 |
| Result integer health / clear | 80 / 3 | 80 / 3 |
| Grouped tap at finish | consumed, inactive | unconsumed, unmissed, active |

The original score getter `0x1315038` uses a native result-counter denominator2 versus1, observed at `0x131505c`. Read-only native score/clear getters inspect the completion-produced cache; clear classifier `0x12a5574` is queried once by the driver. Its clear3 result is **not** evidence of natural results-scene activation. The score getter has two entries, one original completion caller plus one inspection query. The scenario stops with the ending timer pending; ending/results UI and SQLite are explicitly not run for this pair. No snapshot factory is called directly by Python.

## 7. Reusable scenario and actual validation

New `src/noinput_semantics.py` runs both cases independently and retains partial evidence on unexpected exceptions. Construction, input and expiry/completion gates pass in the authoritative fresh paired run; `native_failures` is empty. Per-instruction observations and relational assertions preserve original producers/callers. Count, score, JNI rejection and final counters are observed, not fabricated expected events. An initial successful diagnostic pair preceded an independent final pair with additional read-only end-loop operand observations; traces are not spliced.

Documented command:

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario noinput_semantics \
  --output /path/outside/research_harness/noinput-result.json
```

Actual final command used `/tmp/arconist036/bin/python`, archive `project_sources/01-arccopy.zip`, scenario `noinput_semantics`, output `audit/036/final.json`: exit0, status pass, all three gates pass per case. Generated JSON remains outside publication.

Fresh previous CLI commands used that same Python/archive, `--scenario NAME --output audit/036/NAME.json`:

| Scenario NAME | Exit / JSON status | Seconds |
|---|---|---:|
| ordinary (full session/results/SQLite) | 0 / pass | 27.677 |
| chord (both orders) | 0 / pass | 40.389 |
| moving_arc (moving and crossing) | 0 / pass | 44.165 |
| timing_group (control and reverse) | 0 / pass | 49.977 |
| cpu_note (CPU refresh/expiry) | 0 / pass | 51.151 |
| late_input_expiry (both orderings) | 0 / pass | 45.182 |

With `ARCONIST_TEST_ARCHIVE`, `ARCONIST_ARC_TAP_TEST_ARCHIVE` and `ARCONIST_HOLD_TEST_ARCHIVE` pointing to the supplied archive:

```bash
/tmp/arconist036/bin/python -m unittest discover -s research_harness/tests -v
```

All five existing tests pass in60.234s, exit0, **no skips**: actual arc-tap CLI, actual hold dual-case CLI, missing archive, unavailable song native negative, wrong binary hash. Thus arc-tap and hold are executed regressions, not skipped wrappers. Previously blocked camera/track/flick/continuous-gauge/Designant diagnostics are preserved and not rerun or counted as successful gameplay.

## 8. Scientific boundaries and publication

External supplied services remain ordinary catalog/account/profile/settings, synthetic AFF bytes, clock/JNI inputs, libc/C++/math/locale/platform interfaces, archive resource/font/CSB/audio/GPU/presentation adapters and existing allocation/autorelease services. No native timing, flag, count, depth, index, active membership, note guard, score or result state is repaired. The existing inert base Node visitation/render/flush boundary remains; this scenario does not adopt CPU-note's separate traversal restoration or claim rendered output.

Exact inherited PC skips, with no additions:

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

The last three are inherited results-only boundaries and are not entered by this new scenario. No actual Android queue/hardware latency, audio-device timing, GPU output, reclamation, production-account compatibility or arbitrary timing-group combination is verified.

Publication is a narrow non-forced child of the verified parent: this report; append-only context; G-012 backlog row/history; harness README/CLI/config; new scenario; two new synthetic fixtures. The exact child SHA and immutable links are returned to headquarters. All nine uploaded contents are read back and compared; parent/child blob trees and context prefix are checked. Prior reports, fixtures, tests/assertions, successful scenario implementations, dependency pins, blocked diagnostics, root instructions and unrelated files remain unchanged. No original archive/library/assets, generated evidence, databases, environments or secrets are committed. G-001–G-011 statuses/history remain intact; G-012 is Verified only within this paired tap lifecycle. Stop after036.

## 9. Observed pseudocode

```text
for control, then fresh noinput scene:
    supply external AFF and unchanged ordinary services
    original solo entry -> native GameScene loading
    original parser creates both SimpleNotes and timing group
    if original attribute comparison finds noinput:
        original parser clears grouped parsed flag
    original builder creates both LogicTapNotes
        -> original group, timing and input-flag stores
    native count/end passes skip input-disabled objects
    separate native group-lifetime pass still consumes grouped end
    original spatial index contains both taps
    Director activates scene; native frames admit both

    at native E1500, for grouped then default lane:
        original camera projects external JNI coordinates
        supplied JNI DOWN -> original Touch/listener/collector
        original input flag filters candidates
        if native candidate/classifier accepts:
            original recorder and consumed/contact-ID writes
        JNI UP -> native mapping/slot/retention cleanup

    Director frames -> original expiry flag check
        disabled grouped tap skips miss recording
    strict native completion at E1621
        -> original delegate/snapshot -> ScoreState result cache
    inspect native result with read-only original getters
compare native N, end, membership, recorder and final counters
results-scene activation/SQLite for these charts: NOT RUN
```

No further experiment is needed to establish this scoped tap result. Later-note variants, other note types/attributes and object reclamation remain outside the executed evidence, not implied extensions of G-012.
