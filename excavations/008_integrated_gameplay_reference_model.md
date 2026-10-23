# Expedition 008 — Integrated Gameplay Reconstruction & Validation

Date: 2026-10-23. Repository: `thgillwtnorizoh/arconist`, existing branch `main`.

## Result

**The minimum outcome and the principal strong outcomes are met in bounded synthetic native execution.** The original AFF **body** lexer/parser, runtime builder, timing/depth preprocessing, note activation, input projection/collection/sorting, tap judgments, native note guards, score/gauge updates, enclosing model frame, scene termination callback, and GameResult construction/classification execute together for a multi-note fixture. Header/file loading, configuration, and the model's spatial-index construction are supplied boundaries, not claimed as integrated.

New experiments also join a parsed hold to continuous contact/checkpoint processing and final results, camera actions to actual touch eligibility and judgments, scene-control state to input/render behavior, and one exact character-skill key to timed judgments and gauge changes. A generated weight-2 arc checkpoint reaches two original recorder/clamp calls, with its activation state explicitly supplied.

The integration changes several conclusions one might incorrectly draw from isolated tests:

- AFF integer positions and internal lane IDs are different representations.
- The ordinary hold branch tested here does not activate at its start timestamp, despite a broader 120 ms lookahead characterization in Expedition 002.
- Final synthesized LOST does not imply that the missing gauge callbacks ran.
- An isolated 70-success health threshold is not a complete replay: subsequent expiry changes health.
- In the tested frame, song completion precedes the health-failure branch; a same-frame completion can retain H=0 rather than producing the failure sentinel −1.
- Moving the projected picture of a note does not necessarily make its old screen point ineligible: the actual lane/depth predicate still decides.

This is a reference model of the executed paths, not a recreated Android application. Actual audio output, GPU drawing, device latency, complete character selection, every special mode, and database/network effects remain outside the execution coverage.

## What I Found

### 1. Sources, identity, and preservation

The authoritative project instruction text, supplied ZIP, current `context.md`, and reports 001–007 were reviewed before integration. An internal dependency map was made before executing the new replay. Repository main matched starting commit `506c4e849fb5d6be215ea7f3132abd440d6704b4`.

| Evidence | SHA-256 |
|---|---|
| ZIP member `lib/arm64-v8a/libcocos2dcpp.so` | `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` |
| ZIP member `lib/arm64-v8a/libfmodProvider.so` | `db07590708c1e2b7ed3a17800a8839392d5a7a8322cd102d5b35bda05b251bfb` |

Main-library Build ID is `17d660edbf37ca78beefc32e07672c97419ddce6`. The ZIP has 9,658 entries and no `.aff` samples. Fresh extraction was necessary because an older scratch analysis copy was truncated; the ZIP member itself matches the historical identity. No uploaded archive, existing binary, source asset, project instruction, or earlier report was modified.

**Address convention:** unless explicitly prefixed “provider,” every native address below belongs to **`lib/arm64-v8a/libcocos2dcpp.so` and is an ELF virtual address before load relocation**. Code/rodata addresses discussed here equal file offsets; relocated data does not generally do so. PT_LOAD mapping and RELATIVE relocations were applied. Provider addresses refer to the separate `libfmodProvider.so` ELF; that provider was not newly executed in this expedition.

Names for reference interfaces, routines, and fields are researcher descriptions. Class names such as LogicTapNote, LogicHoldNote, ScoreState, LifeBarState, GameResult, and cocos2d::MoveBy are recovered RTTI associations established in the archive; they are not recovered source-level function names.

Evidence labels:

- **Confirmed:** instructions/relocations/metadata or the scoped original-code execution stated here.
- **Synthetic:** a supplied object, configuration, clock reading, index, event schedule, or environment service.
- **Interpretation:** an explanation supported by those observations.
- **Unknown:** an unrecovered producer, callback, lifecycle, or broader policy.

Previously authorized curve-ID and spatial-depth corrections remain resolved. No earlier documentation is rewritten.

### 2. Integrated dependency table

“Direct” below means a native call/virtual dispatch; “driver” means a test invokes a native interface or reproduces an identified caller sequence. A driver-supplied connection is not silently promoted to a direct call.

| Subsystem / native entry | Required inputs/state | Outputs and modified fields | Downstream consumer / relationship | Prior evidence | Expedition 008 status and remaining connection |
|---|---|---|---|---|---|
| AFF body lexer `0xdf4a58 → 0x814384` | C++ string, lexer state, ASCII runtime services | Native token pointer vector, typed numeric/identifier objects | `0xb01d6c`, driver passes actual output | 002 | Native-integrated for tested body grammar; numeric stream imports supplied; whole-file/header path omitted |
| Body parser `0xb01d6c → 0x139b96c → 0x923240` | Actual token vector, include flag1 | Parsed object vector at parsed-chart `+0x18/+0x20` | Runtime builder `0x1862a14`, driver | 002 | Native-integrated for taps, timing, hold fixtures; malformed syntax not tested |
| Runtime assembly `0x1862a14` | Parsed objects, chart speed `+0xf4`, density `+0xc8`, mirror/configuration | Logic vector `+0x20`, timing lists `+0x38`, group descriptors `+0x50`, end `+0xbc` | Initializer postprocessing and model frame | 002, 003, 007 | Original builder executes; enclosing metadata/account initializer omitted |
| Count/depth preprocessing: initializer blocks `0x173bd50`, `0x173bf1c`, `0x173bfb0` | Live chart register/caller state, built timing/notes | Checkpoint records; native count at chart `+0xb8`; note depths `+0x30/+0x34/+0x38/+0x3c`; default group end | Score factory and `0x10fd1c0` | 001, 002, 007 | Original functions/blocks execute; not a claim to execute all of `0x173b358` |
| Score/gauge creation `0x14f0a94 → 0x13e00b4 → 0x12c5070 → 0x160a3b8` | Native N, song flags, supplied mode-map tree, ability, initial-health argument | Actual ScoreState/gauge objects; H/gain/mode/vector | Recorders and frame | 006 | Native-integrated; one-node mode-map fixture, selected ordinary/easy/hard modes |
| Timeline start/update `0x8db04c`, `0x16c90bc`, `0x1271200` | Synthetic imported monotonic count, epochs, offset/flags | R/C/P/B and effective E | Both model frame and begin input call update directly | 005 | Native-integrated with judgment; hardware audio boundaries recorded only |
| View-to-design conversion block `0x160b83c..0x160b87c` | GLView origin/scales, raw coordinates, Touch state | Touch current/initial/previous coordinates | `0xeec024`, driver supplies the same Touch | 004 | Native-integrated block→input; actual Android/JNI transport/listener queue unexecuted |
| Model frame `0x10a7550` | Chart/timing/groups, spatial buckets, timeline, scene/delegate | Updated depths/ranges/cache, checkpoints, gauges, finished state | Direct calls described below | 002–007 | Whole routine executes in ordinary/hard fixtures; post-snapshot external work omitted |
| Depth/range maintenance `0x10fd1c0 → 0xcf918c` | Native timing/depth data and **supplied bucket index** | Logic depth and retained active range `model+0xa0/+0xa8` | Initial/continuous input and expiry | 007 | Native-integrated; production of bucket index not executed |
| Camera actions/cache `0x192b5c8`, `0xe29b94`, `0x10eff1c` | Prepared event/rig, original actions, dt | Camera Node position/Euler, W/V/PV | Native projection/unprojection/input | 007 | Native-integrated action→matrix→judgment; ActionManager scheduling is a driver boundary |
| Initial input `0xeec024` | Touch, E, camera, active notes, gates | Candidate vector `+0xb8/+0xc0`; hold initial latch | Direct sorter `0xf6b514`, judge `0x160ce28` | 004 | Native-integrated, actual note guards/recorders no longer stubbed |
| Continuous input `0x14858d4` | Retained contacts `+0xd0/+0xd8`, projected records `+0x120/+0x128`, active notes | Hold active latches, separate arc/flick paths | Direct checkpoint pass later in frame | 002, 003 | Native-integrated for hold; ordinary arc ownership and flick replay not joined |
| Tap/arc-tap judge `0x160ce28` | Current E, timing, native resolved/consumed predicates | Calls actual recorder and acceptance guard | `0x1730290`, `0x868e54`, direct | 002, 004 | Native-integrated for tap and prepared trace-parent arc-tap |
| Checkpoints `0xd92558`, `0xba81e8`, `0xf8056c`, `0xc6e938` | Interval, record flags/weights, active/contact state | Resolved records; one recorder call per unit | Direct accepted/miss recorders | 001–003, 006 | Parsed hold integrated; weighted arc conditional on supplied active state |
| Score/gauge `0x1730290`, `0x868e54`, `0x16e4ab0`, `0x1869e90`, `0x133fac8` | Native note RTTI, counters, mode/ability | Consumption, counters, combo, score, f32 H and clamps | Frame/final snapshot, direct | 002, 006 | Native-integrated without acceptance/result arithmetic hooks |
| Failure/completion in `0x10a7550` | E/end, H/F, mode, scene flags, finished latch | H=−1 on health failure or normal completion; delegate | Actual `0xe2c124 → 0xc27d34` | 006 | Native-integrated; ordering distinction newly tested |
| Result `0xc27d34 → 0x1600bb0 → 0xcab7fc`, `0x12a5574` | Native score/gauge state, synthetic song/character environment | Cached result, floored health, selected/recorded LOST, class | Result getter/persistence | 006 | Native-integrated snapshot/classification; later work deliberately skipped |
| Representative skill `0x7ac3cc` and ability virtuals | Exact whole key, supplied selection | Mode1, initial H30, gain multiplier .7 | Native score/gauge factory and timed judgment | 006 | Effect native-integrated; account/level/awakening selection gate bypassed |
| Visual state `0x1514c64`, `0xf20c28`, `0x1501dfc → 0xef18e8` | Scene events, logic/render links, native Nodes | Hidden bytes, rendered opacity, transition state | Input predicates or Node state | 007 | CPU paths integrated; scheduler dispatch/GPU not executed |
| Audio manager/provider | Timeline→`0x1735d7c`; provider `0x270a8` | Start/pause/seek request; DSP state | Audio output | 005 | Request boundary logged; no newly integrated provider/hardware execution |
| Persistence `0x13552d4`, `0x12a5e60` | GameResult, database/account context | Stored best scores/clear types | External state | 006 | Instruction-backed prior evidence; no DB/network effects executed |

### 3. Actual frame order and the separate begin-input callback

**Confirmed in original `0x10a7550`, including new enclosing-frame execution:**

1. Update GameTimeline (`0x10a7580 → 0x16c90bc`).
2. Compute shared widening state; publish last-frame E at global `0x1bf93e8`; maintain projected-contact records.
3. Depth/range maintenance (`0x10a7804 → 0x10fd1c0`).
4. Arc current-position producer (`0x10a780c → 0x19f3d4c`). In tap/hold fixtures its arc branches are not exercised.
5. Width-dependent render-child opacity updates when applicable.
6. If not paused, run continuous input while not finished (`0x10a78dc → 0x14858d4`), then expiry/checkpoint/camera/scene events (`0x10a78e8 → 0xf8056c`). Finished-state event behavior has additional branches; it is not modeled as universal continued judgment.
7. Score consistency/continuous gauge update (`0x10a78f4 → 0xa126f4`).
8. Mode transitions, then chart-completion/ability-completion logic.
9. Health-threshold failure logic, respecting the finished latch.
10. Remaining notification/presentation-related branches.

Initial touch is a **separate callback**. `0xeec024` first checks model pause/finished bytes `+0x138/+0x139`, then updates GameTimeline again, projects current Touch coordinates, collects/sorts candidates, and judges. It does not perform the full depth/range/expiry frame before each tap.

New execution: after a native frame at E=1000, advancing the imported monotonic clock by110 ms and calling begin input without a second model frame gives **judge E=1110 while last-frame global E remains1000**. The earlier eligible tap takes the late LOST-consumption branch. Neither the stored touch timestamp nor the last-frame timestamp replaces the current E in that judge.

This establishes a real ordering dependency. It does not establish where Android callbacks, Scheduler actions, or rendering sit relative to every platform frame.

### 4. New chart-to-runtime integration evidence

#### Integer chart positions are translated

Parser position helper `0xa9c1f0` preserves a typed integer position with raw value at its `+0x08`. Runtime conversion `0x13a84ec`, reached by builder callsite `0x186400c`, invokes integer constructor **`0xddd644`**. Original execution for raw integers0..5 establishes:

| AFF raw integer | Internal ID, mirror0 | Internal ID, mirror1 |
|---:|---:|---:|
| 0 | 1 | 6 |
| 1 | 2 | 5 |
| 2 | 3 | 4 |
| 3 | 4 | 3 |
| 4 | 5 | 2 |
| 5 | 6 | 1 |

Within that tested domain, `id=raw+1` without mirroring and `id=6-raw` with mirroring. Native normalized X at position `+0x14` is `0.5*(id-2)`. Internal ID is stored at `+0x10` and integer discriminator at `+0x0c`.

The float-position conversion branch is different (`1-x` when mirrored); integer authoring must not be converted to a float lane before parsing. The constructor's out-of-domain behavior is not generalized. Support for these six constructor inputs does not prove ordinary input can play all six IDs without extended-lane state.

This extends the earlier internal-lane findings; it does not contradict their measured internal boundaries.

#### Timing scale needs an initialized speed input

Builder `0x1862a14` passes chart f32 `+0xf4` to timing initializer **`0xbe2b98`**, alongside tempo and beat values. The decisive operations are:

```text
m = f32(tempo * suppliedSpeed)      // stored +0x18
scale = f32(f32(1.0 / m) * 60.0)   // stored +0x28
beats -> +0x1c; original tempo -> +0x20
```

Tempo120, speed6 yields scale **0.0833333358168602**. An omitted/zero speed yielded positive infinity in the isolated native initializer; there is no zero-speed guard in this fragment. This is a required fixture precondition, not permission to invent a zero-speed fallback.

The actual chart-initializer preprocessing loop `0x173bfb0..0x173c1d8` integrates timing records at each note's start/end, truncates, and writes both current and precomputed depth fields. For fixture A below, pre-depths are −12000,−24000,−24588,−36000. No Python timestamp-times-speed calculation supplies those values in the compiled fixtures.

#### Counts, ends, and group state

Native count helper `0x11ea120` is called and its return stored by original block `0x173bf1c..0x173bf2c`. Hold records are generated through original initializer postprocessing `0x173bd50..0x173bdfc`, which dispatches long-note virtual `+0x50` after sorting/link preparation.

In the tested builder tail `0x18655b4..0x1865698`, input-enabled ordinary taps contribute end+120 to chart `+0xbc`, while the tested hold contributes end+500. Therefore fixture A's last tap at3000 yields **end3120**; the hold ending2000 yields **end2500**. This is not a universal audio-length/completion formula for every chart entity or special mode.

The default group descriptor initially has an active byte but needs the native initializer tail: block `0x173c1dc..0x173c24c` sets its end field to INT_MAX. Omitting that tail made the group expire immediately in an early incomplete fixture. The successful compiled replays execute that block; they do not patch a guessed lifetime into the group.

## Synthetic Fixtures and Harness

### 5. Fixture A — parsed four-tap chart

This is researcher-authored synthetic text, not an official or bundled chart:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
(2049,2);
(3000,4);
```

**Parsing scope:** body text from `timing` onward goes through original lexer/parser. Header splitting and header-map parsing do not execute; AudioOffset0 and density1 are supplied to the native chart fields. Speed6, mirror0, song flag0, mode0, default initial-health sentinel−1, and no ability are explicit configuration.

Native body output: **33 tokens**, five parsed objects (one timing plus four taps). Native runtime IDs are4,3,3,5. Native N=4; end3120; default gauge H=0, g=20.200000762939453.

The controlled baseline camera has unit Node transform and a supplied projection diagonal `(1/1280,1/720,1,1)`, design size1280×720. It is not the production perspective camera. Input X740/540 correspond approximately to internal X200/−200. The line is parallel to Y=0 and uses the native exact-parallel return-origin behavior, producing eligible depth1. Separate perspective-camera tests below exercise nonparallel intersections and actual camera actions.

### 6. Fixture C — parsed hold and checkpoints

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
hold(1000,2000,3);
```

Original body parsing and runtime assembly produce an internal-lane4 hold. The native initializer reads tempo120/density1 and produces interval250. Original record generation with flag0 gives:

```text
(time1250,weight1,resolved0)
(time1500,weight1,resolved0)
(time1750,weight1,resolved0)
```

Native N=3, chart end2500, H=0, g=26.866666793823242. The driver supplies a retained Touch and invokes the original begin/continuous/end interfaces; it does not assign the hold's active latch in this compiled replay.

### 7. Large fixture and reproducible event schedules

For the ordinary-clear boundary, replace the body with this exact generator:

```python
body = 'timing(0,120.00,4.00);' + ''.join(
    f'({1000+i*150},{1+i%4});' for i in range(100)
)
```

This is also parsed and built natively. N=100; end15970; speed6; g=1; initial H=0. For the first89 or90 taps, advance a native model frame to the note time and issue a touch using design X `[290,540,740,990][i%4]`, Y360, with distinct generated contact IDs `100+i`. Then run tail model frames every100 ms from the last played event until end, followed by frames at end and end+1. The remaining taps receive native expiry misses.

A separate **jump-tail** experiment omits intermediate tail frames. It deliberately tests a different frame schedule with the same supplied index. Its missing recorded miss must not be hidden by changing expected gauge arithmetic.

### 8. Execution environment and supplied layouts

Unicorn maps original ELF PT_LOAD segments and applies `R_AARCH64_RELATIVE` relocations. Main-library arithmetic, Node transforms, inverse/multiply kernels, judges, native note guards, recorders, gauge routines, count logic, model frame, snapshot constructor, and classifier are original instructions.

A minimal loader/reference call shape is:

```python
u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
u.mem_map(0, 0x2100000)
for s in elf.iter_segments():
    if s['p_type'] == 'PT_LOAD':
        u.mem_write(s['p_vaddr'], file_bytes[s['p_offset']:s['p_offset']+s['p_filesz']])
for r in elf.get_section_by_name('.rela.dyn').iter_relocations():
    if r['r_info_type'] == 1027:  # R_AARCH64_RELATIVE, load bias0
        write_u64(r['r_offset'], r['r_addend'])
u.mem_map(0x4000000, 0x400000)
u.mem_map(0x6000000, 0x10000)
# Set TPIDR_EL0=0x43ff000; synthetic SP=0x600f000; LR=stop sentinel0x4000100.
# Load integer arguments into X0..X7 and float arguments into S0... .
# X8 supplies aggregate-return storage where required.
# Install only the boundary hooks listed below; stop at the designated return/block boundary.
```

Relevant synthetic arena addresses in the actual replay:

| Object/state | Address or layout |
|---|---|
| Chart / song | `0x4012000` / `0x4013000` |
| Model / scene / timeline | `0x4017000` / `0x4018000` / `0x4019000` |
| Character / application / account | `0x401d000` / `0x401e000` / `0x4020000` |
| Rig / primary / secondary camera | `0x4200000` / `0x4202000` / `0x4204000` |
| Touch / active pointer storage / candidate pointer storage | `0x4206000` / `0x4208000` / `0x420a000` |
| Scratch vectors / aggregate output / design-size memory | `0x420c000` / `0x420e000` / `0x4210000` |
| Heap | Bump allocation beginning `0x4100000`, aligned64, zeroed |
| Native note identities | LogicTapNote vtable `0x1af4278`; LogicHoldNote `0x1b2eda8`; LogicArcNote `0x1b91500`; LogicArcTapNote `0x1acac18` |
| Scene delegate | Model `+0x40 = scene+0x2e8`; its virtual `+0x10` points to original thunk `0xe2c124` |

The chart/model initialization boundaries are important:

- Chart has a synthetic song pointer/string/difficulty environment. Metadata/header initialization is not executed as a whole.
- Chart `+0xf4=6`, `+0xc8=1`, `+0xc4=offset`, `+0xcd=0`, and special byte `+0x110=0` are explicit fixture inputs.
- Score factory arguments are `(chart,mode,ability,0,0,100,initialH,0)`. This preserves the native argument transfer to damage percentage100 and the explicit initial-health argument. InitialH=−1 selects the native default; the hard-boundary fixture uses1 intentionally.
- The mode lookup tree supplied to ScoreState has key at tree node `+0x20`, vector at `+0x28/+0x30`, and the original lookup starts at global `0x1bf9650`. It contains the tested mode's single gauge ID. Staged-mode construction is not claimed.
- Native compiled notes start with an **empty active range**. The original `0x10fd1c0` discovers/removes notes using a supplied native-layout bucket index at model `+0x88/+0x90`, and maintains `+0xa0/+0xa8`. This producer boundary is not a hook returning already-selected candidates.
- Bucket index: one timing group; balanced binary tree with keys0..6 for the small fixture,0..30 for the100-tap fixture. Map header contains leftmost pointer at+0, root at+8, size at+0x10. Node fields are left/right/parent at+0/+8/+0x10, black byte+0x18, signed key+0x20, vector begin/end/capacity at+0x28/+0x30/+0x38. All-black perfect trees are used. Each playable note is assigned to key `trunc(-precomputedStartDepth/10000)` for these fixtures. The **original producer of this assignment is unverified**; tests are conditional on this supplied index.
- Model `+0x18=10000` supplies the tested look-ahead depth. Candidate capacity is preallocated; the original collection/sort still executes. Retain/free boundaries are no-ops.
- Inactive widening transitions are supplied as completed reverse transitions `(start0,direction0,duration1)`, giving G1/W0 for the positive E values tested. They are not claimed as factory defaults. The reference frame driver does not reset transition start times each frame.
- For direct block execution inside the chart initializer, X20 is chart, X29 is valid synthetic frame storage `0x600f100`, and the described stop address excludes unrelated metadata/cleanup. This is scoped block execution, not a successful call of the entire initializer.

### 9. Every observable boundary hook

| Boundary | Supplied/suppressed behavior | Scope/limitation |
|---|---|---|
| `operator new` imports `0x1a6d9c0`, `0x1a6dd40`, `0x1a6e090` | Zeroed bump allocation | No allocator failure or real ownership/lifetime validation |
| Memory/string imports, including `0x1a6d9d0`, `0x1a6daf0`, `0x1a6db30`, `0x1a6da50`, `0x1a6db80`, `0x1a6da60`, `0x1a6dad0` | Copy/move/set, tested libc++ string copy/compare/length semantics | Fixture strings only; no general C++ runtime implementation |
| Parser string append/push imports `0x1a6dda0`, `0x1a6db20`, `0x1a6db00` | Mutate synthetic libc++ strings | No grammar decisions delegated to Python |
| Parser `iswspace` `0x1a6e200` and ctype pointer via GOT `0x1b96168` | ASCII whitespace/classification table; byte index char+1, upper1/lower2/digit4 | Only ASCII fixture domain established |
| C++ stringstream constructor `0x1087f14`, destructor `0xb06728`, numeric extraction imports `0x1a6e210/0x1a6e230` | Capture native-scanned numeric substring, supply f32/int conversion | Explicit **numeric-runtime boundary**. Native lexer decides substring/token class; locale, malformed numbers and general conversion compatibility untested |
| `__dynamic_cast` import `0x1a6db90` | Resolve prepared single-inheritance identities using original relocated RTTI/base pointers | No multiple-inheritance/foreign-object correctness claim |
| Ref constructor `0x121a0ec`, refcount/autorelease/free helpers (`0x147fe48`, `0xd6dc98`, `0x10ac6e8`, delete/array-delete imports), and destructors `0x19f2e40/0x9fc7fc/0xc7fd5c` | No-op lifetime operations | Base reference-count/object-ID initialization and destruction are omitted; no lifetime correctness claim; finite-run leaks allowed |
| Imported steady-clock `0x1a6dc60` | Return controlled `nowMs*1,000,000` | Original `0x1271200` division and timeline math execute |
| Imported system-clock `0x1a6dbe0` and time import `0x1a6de50` | Deterministic system count/date | Not a device epoch/synchronization measurement |
| Audio boundaries `0x1735d7c`, `0x18c9ba4`, `0xfbf24c`, `0xefb804`, `0x107af5c` | Log start/pause/seek/fade/SFX request; return a harmless synthetic sound handle | Suppresses actual audio-manager/provider/hardware effects. Full FMOD scheduling is not integrated |
| Director/frame size `0xa4227c`, `0xf09110` | Synthetic Director/design1280×720 and frame1280×720 | Viewport policies and actual window not measured |
| Account/optional character helpers `0xb688e0`, `0xe2388c` | Return fixture account / optional-null | Full external state/analytics omitted |
| Delegate hit/miss UI methods | Record notifications and return | Do **not** replace `0x1730290`, `0x868e54`, `0x965e28`, `0xc78814`, or long-note guards |
| Scene feedback stop `0xfa4320` | No-op external feedback shutdown | Before snapshot; no tested score/gauge mutation supplied |
| Scene control-flow boundary `0xc27e18 → 0xc27f20` | Skip post-snapshot queueing, persistence/presentation, optional special termination, and ending animation; execute original epilogue | Actual scene callback and `0x1600bb0` have executed by this point. No save/remote/presentation claim |
| Node runAction `0xc7820c` in camera tests | Capture target/action pair; driver invokes original clone/start/step/update virtuals | Full ActionManager/Scheduler omitted; action interpolation arithmetic is native |
| Math imports `sincosf`, `fmodf`, `tanf`, `atan2f`, `asinf` at `0x1a6e1b0`, `0x1a6de80`, `0x1a6f000`, `0x1a6ed10`, `0x1a6efe0` | Host libm with f32 register/memory boundaries | Native quaternion/matrix/vector arithmetic executes; Android libm bit identity unclaimed |

Entry/return observers record calls, plane intersections, and gauge before/gain/damage/after values without replacing those calculations. The inherited score-history hook was removed: original `0x899c50` runs, as does original string-equality helper `0x172e248` (using the listed string imports). The actual main-library `0xe29b94`, `0x16c90bc`, `0x160ce28`, recorders, native note acceptance predicates, gauge application, model frame, snapshot and classifier are **not** hooked in the integrated chains.

No core result is produced by a Python score/gauge formula. Host equations are assertions against native output. No real device, actual audio, GPU, database, or network execution is claimed.

## Native Execution Traces and Cross-System Validation

### 10. Scenario A — ordinary multi-note replay through final GameResult

Each input is preceded by the original model frame at that E. Both lane3 notes are eligible at2051; the earlier2000 note has51 ms error versus the later2049 note's2 ms. The native sorter selects the earlier one first.

| Event | Native active tap times before input | Shining / PURE / FAR / recorded LOST | Combo / max | Stored score | Live H | Finished |
|---|---|---|---|---:|---:|---:|
| Initialized compiled chart | empty | 0/0/0/0 | 0/0 | 0 | 0 | 0 |
| E1008, input X740 | 1000,2000,2049 | 1/1/0/0 | 1/1 | 2,500,001 | 20.200000762939453 | 0 |
| E2051, input X540 | 2000,2049,3000 | 1/1/1/0 | 2/2 | 3,750,001 | 30.30000114440918 | 0 |
| E2051, second input X540 | 2049,3000 | 2/2/1/0 | 3/3 | 6,250,002 | 50.5 | 0 |
| Frame E3100 | — | 2/2/1/0 | 3/3 | 6,250,002 | 50.5 | 0 |
| Frame E3101 | — | 2/2/1/1 | 0/3 | 6,250,002 | 48.5 | 0 |
| Frame E3120 | — | 2/2/1/1 | 0/3 | 6,250,002 | 48.5 | 0 |
| Frame E3121 | — | 2/2/1/1 | 0/3 | 6,250,002 | 48.5 | 1 |

Observed final GameResult: stored score=getter score6,250,002; PURE2/FAR1/final LOST1/recorded LOST1; integer health48; classification0 (interpreted fail). Native model frame invokes original scene thunk and snapshot; the result is not constructed in Python.

The observed native accepted path includes:

```text
0xeec024 → 0x16c90bc → projection/lane/collection
 → 0xf6b514 → 0x160ce28 → 0x1730290
 → note.v20 = 0x965e28
 → 0x16e4ab0 → 0x133fac8
 → 0xe43b80 and combo bookkeeping
```

Miss/final paths include:

```text
0x10a7550 → 0xf8056c → 0x868e54
 → note.v38 = 0x7e995c → 0x1869e90 → 0x133fac8

0x10a7550 → scene-delegate.v10 = 0xe2c124 → 0xc27d34
 → 0x1600bb0 → 0xcab7fc
 → separately queried 0x1315038 / 0x12a5574
```

The final query of score/category is a driver query of the native result, not a claim that the frame directly calls the classifier. UI notification methods are isolated, while note consumption and all score/gauge changes execute natively.

### 11. Scenario B — collection order, consumption, and expiry ordering

Direct initial-input fixtures retain both notes in reversed collection order. The actual sorter and predicates run. This separates resolved-note rejection from the compiled replay's active-range removal of processed notes.

| Fixture (all internal lane4) | E / precondition | Observed result of the tested touch |
|---|---|---|
| Earlier1000, later1049 | E1051; neither consumed | Earlier takes FAR; later's2 ms error does not win |
| Earlier1000, later1049 | Earlier already accepted natively; E1051 | Classifier rejects consumed earlier; later takes shining PURE |
| Earlier900, later1049 | E1051; earlier error151 | Earlier returns false without recording; later takes shining PURE |
| Earlier1000, later1109 | E1110; input before expiry | Earlier consumes input as LOST; later remains unplayed |
| Same two notes | E1110; expiry before input | Earlier is marked missed first; the touch reaches later and gives shining PURE |

A true tap-classifier return means **consumed**, including LOST. It does not promise a successful judgment. A repeated touch after native consumption does not add a second score/gauge callback for that tap; a distinct unconsumed candidate can still be selected.

Equal-time stability was not newly guaranteed. Expedition004's unstable equal-key sort remains the applicable evidence. These fixtures deliberately use unequal timestamps.

### 12. Scenario C — parsed hold, release, and weighted checkpoints

The parsed hold is latched by native begin input at1000. A retained Touch is then processed by original continuous input inside the model frame. Native `0x1866030` clears per-frame contact state before continuous input restores it when eligible.

| E / operation | Native behavior | PURE / recorded LOST | Score | H |
|---|---|---|---:|---:|
| 1000 begin, then continuous frame | Initial latch set; active check rejects equality at start | 0/0 | 0 | 0 |
| 1001 continuous frame | Active/contact flags set | 0/0 | 0 | 0 |
| 1124 | E+125=1249, no record due | 0/0 | 0 | 0 |
| 1125 | Record1250 resolves inclusively | 1/0 | 3,333,334 | 26.866666793823242 |
| 1375 | Record1500 resolves | 2/0 | 6,666,668 | 53.733333587646484 |
| Native end cleanup `0xf9a50c`, then frame2250 | Contact removed; record1750 is overdue at cutoff1750 | 2/1 | 6,666,668 | 51.733333587646484 |
| Frame2501 | Chart end2500 crossed; native finalization | 2/1 | 6,666,668 | unchanged |

Final GameResult: PURE2/FAR0/LOST1/recorded LOST1, floored health51, score6,666,668, category0. This derived LogicHoldNote takes the literal nonmatching exact-RTTI damage branch described in Expedition006; its LOST costs2 here, not an assumed reduced long-note damage of1.

#### New hold-start boundary evidence

For start1000/end2000, internal lane4, ordinary model `+0x148=0`, an unconsumed hold and a matching retained contact:

| E | Initial latch after `0xeec024` | Active after native model frame |
|---:|---:|---:|
| 880 | 0 | 0 |
| 900 | 0 | 0 |
| 901 | 1 | 0 |
| 1000 | 1 | 0 |
| 1001 | 1 | 1 |

Initial collection requires `start < E+100` and `E < end`. The tested continuous branch at **`0x1485d74..0x1485db0`** requires **`start < E < end`**, then the initial latch. In particular, `0x1485d74` compares start against E and `0x1485d78` branches away on start≥E. See the separately recorded historical discrepancy below.

#### Native weight2 generation and repeated clamping

A separate prepared ArcNote has start1000/end2001, interval250, one successor with mode0, and generation flag1. Actual `0xba81e8` invokes `0xd92558`, removes the last record under its recovered condition, and yields:

```text
(1000,1,0), (1250,1,0), (1500,2,0)  // total units4
```

With native gauge initialization N4, explicit starting H70, and the arc active byte supplied, `0xf8056c` resolves these at E1000/1250/1500 with **1/1/2 accepted-recorder calls**. Per-call audits from the actual gauge routine:

| Callback | H before | Native gain | H after clamp |
|---:|---:|---:|---:|
| 1 | 70 | 20.200000762939453 | 90.19999694824219 |
| 2 | 90.19999694824219 | 20.200000762939453 | 100 |
| 3, first unit of weight2 | 100 | 20.200000762939453 | 100 |
| 4, second unit of weight2 | 100 | 20.200000762939453 | 100 |

Final PURE4/shining4, score10,000,004, health100, LOST0, category3. The weight2 record was generated by native code, not manually assigned or aggregated into one gain. **Arc contact/ownership activation is not validated by this test:** the supplied active flag is an essential boundary. The parsed hold test above has no such active-latch substitution.

### 13. Scenario D — ordinary clearing, failure sentinel, and completion priority

#### Complete ordinary replay versus isolated acceptance counts

For the natively parsed100-tap chart, with native frames through the missed tail:

| Shining/PURE hits | Native expiry LOST | H before missed tail | Final H | Final category | Final score |
|---:|---:|---:|---:|---:|---:|
| 89 | 11 | 89 | 67 | 0 | 8,900,089 |
| 90 | 10 | 90 | **70** | **1** | 9,000,090 |

All100 judgment units are reconciled; recorded LOST equals final LOST in these regular-tail schedules. This is an actual timed-input-to-result clear boundary, not a direct write of H70.

For comparison, repeating the earlier scoped69/70 accepted-unit setup without processing missing units gives H69/70 and final synthesized LOST31/30, categories0/1. With all100 runtime notes active and expiry processed first, the same hit counts instead end at H7/10 and both fail. Both outputs obey the native routines; the difference is the omitted miss callbacks in the isolated setup. No historical formula is contradicted.

#### Ordinary zero versus hard failure

Prepared N3 charts, no ability/grace, F=0:

- Mode0, starting H0, miss at1101: H remains0; frame does not immediately finish.
- Mode2, explicit starting H1, miss at1101 before chart end5000: original miss gives H0; original frame writes **H=−1**, calls the real termination callback, and constructs a failed result. Final LOST3 includes two unplayed units; recorded LOST1 remains separate. Final integer health−1/category0.

This joined test no longer relies on a fake note guard or an end delegate that merely logs and returns.

#### Same-frame completion changes the result

Using the same hard fixture but withholding intermediate frames until E5001, the original frame resolves all three misses, reaches H0, then **normal completion first**. At `0x10a7d50..0x10a7d68`, it sets finished and invokes the delegate with false. The later health-failure branch sees finished at `0x10a7db8..0x10a7dbc` and does not write−1.

Observed result: H0, LOST3/recorded LOST3, category**5** with ScoreState `+0xd2=0`. The native factory initializes that flag to0. Repeating with supplied `+0xd2=1`, copied into result `+0xb3`, yields H0/category0 instead.

This is **confirmed conditional native ordering**, not a universal claim that hard zero clears. Normal frame cadence, original index construction, scene setup, and producers of the zero-health flag matter. The fixture's end5000 and explicit H1 are synthetic; it is not a device exploit or a proof of every production chart's reachable scheduling.

### 14. Final LOST, activation windows, and result-score getters

#### Large frame jump under the supplied index

The same parsed100-tap chart and90 accurate hits produce:

| Tail schedule | PURE | Recorded LOST | Final synthesized LOST | Final H | Class |
|---|---:|---:|---:|---:|---:|
| Native tail frames every100 ms | 90 | 10 | 10 | 70 | 1 |
| Jump directly from last hit to end | 90 | **9** | **10** | **72** | 1 |

The newly encountered note missed the active-range admission window in the supplied bucket/index fixture, so no miss recorder/gauge callback ran for that unit. `0x1600bb0` still reconciles final LOST as N−PURE−FAR. It does **not** retroactively call the missing gauge damage operation.

This is an integration result conditional on the documented **synthetic index assignment**. Since the original index producer was not executed, the exact production consequences of large frame gaps remain unknown. It is evidence that a reference model must represent active membership and callbacks separately from final counters, not permission to call every final LOST a recorded native miss.

#### Stored versus recomputed score and idempotent snapshots

Native result getter `0x1315038` ordinarily uses PURE+FAR+final LOST as its denominator. A supplied flag test makes the distinction visible:

| State before snapshot: N4, one shining PURE | Result LOST | Recorded LOST | Stored score | Getter score | Getter after result `+0xb1=1` |
|---|---:|---:|---:|---:|---:|
| ScoreState `+0xd1=0` | 3 | 0 | 2,500,001 | 2,500,001 | 2,500,001 |
| ScoreState `+0xd1=1` | 0 | 0 | 2,500,001 | **10,000,001** | 2,500,001 |

The flags are deliberately supplied; their production lifecycle is not established by this test. Do not generalize the second row to ordinary sessions. Repeating native finalization without intervening mutation returns the same cached GameResult pointer; it does not produce a second snapshot.

### 15. Timing/input integration and clock boundaries

Original settings-selection/sum blocks `0xfbfed0..0xfbfef8` and `0xfbff4c..0xfbff54` combine supplied chart/player settings. Original clock helper/import conversion, timeline start/update, begin input, judge, recorder, and gauge run together.

For origin1,000,000 ms, A0, pause false, threshold=`origin+3000-O`:

| AFF offset / selected regular offset | O | E at threshold−1, music latch | E at threshold, latch | E at threshold+1, latch |
|---|---:|---|---|---|
| +120 / +30 | +150 | −151,0 | −150,0 | **−150,1** |
| −100 / −25 | −125 | 124,0 | 125,0 | **125,1** |
| +100 / −200 | −100 | 99,0 | 100,0 | **100,1** |

Startup requires strict E>−O, then anchors back to E=−O. Each scenario subsequently reaches an ordinary note1000 at E1025 and records shining PURE with native score/gauge changes. Current regular offset is supplied directly; no legacy20 ms migration is silently added.

Timestamps1 and999,999,999 supplied to Touch `+0x40` give identical state at E1025/1026/1100/1101/1120/1121. Observed tiers are shining PURE / other PURE / FAR / consumed LOST / consumed LOST / no recorded judgment respectively. These tests call input before an expiry frame where necessary; they do not claim late notes always survive until120 ms.

Pause/resume joined test, O150:

1. Reach E1025 with an unplayed note1000.
2. Execute model pause wrapper `0xe31764 → 0x9e74f4`; model gate `+0x138` becomes1.
3. Advance underlying clock5000 ms, update timeline, and issue an old-timestamp touch. E remains1025, input is gated, counters/gauge unchanged.
4. Execute native resume. Captured audio requests are **seek1175**, then pause(false), because resume uses E−B=E+O.
5. Advance underlying clock1 ms and issue input. E1026 produces other PURE, not shining PURE; H becomes40.20000076293945 for N2.

Separate clocks remain separate:

- E is original effective GameTimeline time and judges notes.
- FMOD position is not returned by the clock source here; audio boundaries only log requests.
- Android Touch timestamp is prepared data, not the imported steady-clock epoch.
- Calibration's M+T−AndroidNow−beat formula is prior evidence from005 and is **not** inserted into ordinary input.

There is no device audio-latency, actual queue-delay, oscillator-drift, or full Android lifecycle measurement. Alternate profile selection, hardware FMOD position/seek execution, and calibration integration are not newly exercised.

### 16. Camera/projection/eligibility and visual-state integration

#### Camera actions into actual tap judgment

Controlled perspective cameras use native position `(0,900,900)`, native lookAt target `(0,-550,-2000)` and up `(0,1,0)`, then original perspective builder FOV60/aspect1280/720/near1/far10000. The FOV is a test input, not the rig initializer's universal default.

Known lane-plane target is world `(212,0,0)`, distinct from the renderer's elevated Y4. Original camera projection **`0xbdbb70`** returns Y-up coordinates; the driver explicitly adapts Y to design input as `720-projectY`. Original begin input then runs its own `-1/+1` unprojections, normalized line, Y=0 lane intersection, collection and judge. It uses NDC Z−3/+1 as established earlier, not substituted endpoints0/1.

Original event handler/builders create paired camera actions. The driver runs the original start/first step/second step until completion; no ActionManager cadence claim is made. Each stale/new-position test uses a fresh native tap to separate eligibility from consumption.

| Native action input | Original design point | Reprojected design point | Stale point: observed lane-plane intersection / eligibility | New point: observed intersection |
|---|---|---|---|---|
| Translation(+600,0,0), linear | (749.4763,567.8460) | (439.6376,567.8460) | (811.9808,0,0), different lane; no hit | (211.9956,−.00049,−.00049), hit |
| AFF rotation(0,−10,0), `qi` | same | (744.9940,452.4647) | (183.0056,0,269.8042), **still eligible** lane4/depth; hit | (212.0034,.00049,.03857), hit |
| AFF rotation(0,0,+15), `qo` | same | (873.4293,533.8459) | (−27.4139,0,23.6138), different lane; no hit | (212.0295,0,0), hit |

All matrix arrays before/after were recorded. Original `0xe29b94`, `0x10eff1c`, `0x11e1bfc`, inverse/vector kernels, and actual plane helper execute; plane outputs are observed at native return without replacing them. Reprojected points return within0.5 internal units of `(212,0,0)` in these libm/scoped tests.

The pitch case is valuable: camera movement changes projection, but stale coordinates can remain inside the native lane/depth region. There is no fixed pixel rectangle centered solely on the visible note.

A separate prepared trace-parent ArcTap uses actual vtable `0x1acac18`, parent mode1, parent startX.5, child local position `(212,300,0)`, and child time1000. Original projection gives design approximately `(763.1609,437.9422)`; full initial collection traverses parent arc-tap children, calls spatial eligibility, and native acceptance `0xc78814` produces one shining PURE, score10,000,001, H80.19999694824219. Repeating touch does not duplicate it. Child geometry/parent construction is supplied, not generated from an AFF arc in this test.

#### Dynamic extents and viewport conversion

With actual Camera Z900 versus1800 and initialized globals, original `0x927384` ordinary arc half-extent grows190→380. At each positive boundary, x=radius−.125 passes, equality and radius+.125 fail. This uses Camera Node state, not a camera-position getter stub.

Original move conversion block `0x160b83c..0x160b87c` receives raw `(1580,590)`, viewport origin `(100,50)`, scales `(2,1.5)`, and produces Touch design `(740,360)`. Passing that same Touch to native begin input yields shining PURE and native score/gauge gain. Android pointer-map/listener dispatch is omitted; this is an explicit conversion-block integration.

#### Hidden/rendered/input state are distinct

Native hidegroup dispatcher `0x1514c64 → 0x160a828` writes logic `+0x55=1` while `+0x54` remains1. Original tap depth update and **whole `0xf20c28`** run with a synthetic render object/child, linked to that logic. Actual Node opacity getter `0xfcb94c` returns0; original input still records shining PURE. No setOpacity output hook supplies this result.

Widening tests execute handler `0x1514c64`, then the actual model frame and begin input at E1000:

- Internal-lane3 note, design X650: G1/W0 initially gives no hit; `enwidencamera` transition(start0,direction1,floatDuration1000) yields **G1.5/W0**, enables secondary-lane eligibility, and the same point takes PURE.
- Internal-lane1 note, design X140: W0 initially gives no hit; corresponding `enwidenlanes` transition yields **G1/W1** and the same point takes PURE.

Original render Nodes/child-vector headers are supplied for width-dependent visual consumers. This confirms shared state reaches judgment; it does not establish a direct FOV change from the event name.

Original track callback `0x1501dfc → 0xef18e8` is also joined to actual Node opacity setters `0x18ebfa4`, rather than captured fake color methods. For start255,target0, ticks1/25/50/75/100, both child Nodes store opacity254/239/191/111/0. Dispatcher→Scheduler timing remains a prior instruction-backed relationship; the callback is invoked by the driver.

### 17. Representative skill effect through timed judgment

Original whole-key factory `0x7ac3cc` builds **`gaugestart_30|gaugegain_70`**. The actual ability selector returns mode1. A fresh native ScoreState/gauge factory receives that ability, producing H30, N100/g1. Timed initial input at note1000 reaches native accepted processing and changes H to **30.700000762939453**, with gain0.699999988079071. Native miss of another tap at2101 changes H to**29.5**, with returned damage1.2000007629394531. Native cancellation-rounding is retained.

The account-selected character, unlock/awakening gate, skill lifecycle and other character effects are not simulated as though recovered. This proves the supplied ability's actual dispatch/effect in the joined judgment chain; it does not prove the ability is equipped in any real account or every mode.

## Pseudocode

### 18. State that the reference model must keep distinct

| State | Authoritative storage / transition in tested paths | Distinction |
|---|---|---|
| Input enabled | Logic byte `+0x54`, copied by native builder | Not render-hidden byte `+0x55` |
| Tap missed/resolved | `+0x0c`, set by native miss guard `0x7e995c` | Not successful-consumption byte `+0x0d` |
| Tap accepted | `+0x0d`, contact at `+0x10`, set by `0x965e28` | Candidate collection may still include it until the classifier/range removes it |
| Hold initial latch | `+0xa8`, set by begin input | Does not itself produce a score or guarantee active hold state |
| Long-note contact state | `+0x64/+0x65`, updated by native logic/continuous input | Separate from record resolved flags and chart-time expiry |
| Checkpoint record | 12 bytes: time i32, weight i32, resolved byte | One weight2 record can cause two recorder/clamp calls |
| Current chart time | Timeline effective getter from R/C or cursor branch | Not Android timestamp, last-frame global, or FMOD position |
| Active logic membership | Model retained pointer range `+0xa0/+0xa8` | A chart object can exist without receiving a miss callback in a particular supplied-index schedule |
| Health | LifeBarState f32 `+0x10`; threshold `+0x40` | Final integer health is floored; −1 sentinel is written outside normal lower clamping |
| Runtime score | ScoreState `+0x14`, native helper `0xe43b80` | Final getter can recompute using final counters |
| Recorded LOST | ScoreState `+0x2c`, result `+0x24` | Final selected LOST at result `+0x20` can be synthesized |
| Finished | Model `+0x139`; scene termination latch `+0x49a` | Normal completion and HP failure set/observe it in different order |
| Cached result | ScoreState pointer `+0x68` | Repeated finalization does not create a fresh result |

### 19. Reference interfaces and their limits

These are proposed researcher interfaces, not original symbols. `native(...)` means execute the original routine with native state; it is not a Python approximation. The readable excerpts after the interfaces explain recovered behavior and do not replace the machine-code implementation in the harness.

| Interface | Native functions represented | Preconditions / mutations / ordering | Explicit omission |
|---|---|---|---|
| `load_chart(body, suppliedMetadata)` | `0xdf4a58`, `0xb01d6c`, `0x1862a14`, initializer postprocessing blocks | ASCII fixture body, header fields/speed/mirror supplied; returns native objects/count/depths/end | File provider, complete header parsing and metadata initializer |
| `initialize_gameplay(chart,mode,ability,initialH)` | `0x14f0a94`, native gauge factories | N established first; binds actual score/gauge to model; supplies scene delegate | Full scene/character selection and original spatial-index producer |
| `initialize_timeline(...)` | Offset selection/sum blocks, `0x8db04c`, `0x16c90bc` | Controlled imported counts and epochs; native anchor/pre-roll | Android/FMOD hardware clocks and route policy |
| `advance_frame(steadyCount)` | **Whole `0x10a7550`** | Updates clock, ranges, continuous input, expiry, gauge, completion/failure; post-snapshot boundary omitted | Actual outer Scheduler/Android callback ordering |
| `process_touch_begin(touch)` | `0xeec024` | Touch already exists with supplied contact ID/design coordinates; gates and E refresh native | Android pointer allocation, generated-ID callback, listener queue |
| `process_touch_move(raw,view,touch)` | Conversion block `0x160b83c..0x160b87c` | Updates Touch initial/current/previous and force fields; continuous processing occurs in frame | Whole pointer-map/move-event dispatch |
| `process_touch_end(touch)` | `0xf9a50c` | Native retained-contact/ownership cleanup; following frame removes active contact state | Whole Android/GLView end/cancel delivery |
| `update_long_notes(...)` | `0x1866030`, `0x14858d4`, `0xf8056c`, `0xc6e938` | Use actual frame order; records/weights native | General arc ownership/flick combination |
| `update_camera_and_geometry(...)` | Original action virtuals, `0xe29b94`, `0x10eff1c`; model depth/cache functions | Camera action queue scheduled by driver; Node/matrix arithmetic native | Full ActionManager/GPU; arc meshes not newly joined |
| `apply_judgment(...)` | Tap classifier or checkpoint's direct recorder route | Caller must already establish the relevant eligibility/contact path | No single invented classifier for every note type |
| `update_score_and_gauges(...)` | Actual recorders/gauge/core and frame `0xa126f4` | Do not call twice for the same already-executed judgment | Complete Tempest/Insight/other special-mode equations |
| `check_failure(...)` | Actual branch within `0x10a7550` | Must retain completion-before-HP-check order | No blanket H0 immediate failure for every mode |
| `finalize_result(...)` | Real scene callback→`0x1600bb0`, then native getter/classifier queries | Existing cached pointer returned; final count selection and health flooring native | Save/queues/network/ending animation |

```text
load_chart(body, metadata):
    # Header map/file read are an explicit supplied boundary.
    require metadata.AudioOffset, density, speed, mirror, syntheticSong
    tokens = native_lexer_0xdf4a58(body, ASCII_runtime_and_stream_imports)
    parsed = native_body_parser_0xb01d6c(tokens, includeDesignant=1)
    chart = prepared_chart_shell(metadata)
    native_0x1862a14(chart, parsed, fixtureFlag0)
    native_initializer_postprocess_sort_link_generate_records(chart)
    native_block_0x173bf1c_to_0x173bf2c(chart)  # count and actual store of N
    native_remaining_tested_postprocessors(chart)
    native_block_0x173bfb0_to_0x173c24c(chart)  # depths + default group lifetime
    return chart
    # Original spatial-bucket producer UNKNOWN; supply documented index separately.

initialize_gameplay(chart, mode, ability, initialH=-1):
    require chart.N > 0 and valid native timing/group data
    require prepared mode-map tree, scene/account shell and native-layout index
    score = native_0x14f0a94(chart,mode,ability,0,0,100,initialH,0)
    model.chart = chart; model.score = score
    model.delegate = scene+0x2e8 with native end thunk0xe2c124
    return model

initialize_timeline(model, AFF, settings, steadyEpoch, systemEpoch):
    # Settings values supplied; original selection/sum instructions execute.
    O = signed32(AFF + (settings.regular if settings.preset==0 else settings.alternate))
    prepare_timeline_storage_and_native_offset_store(O)
    native_0x8db04c(model,steadyEpoch,systemEpoch)
    native_0x16c90bc(model.timeline)

advance_frame(importedSteadyNanoseconds):
    clock_import = importedSteadyNanoseconds  # only the imported source is supplied
    native_0x10a7550(model,scene)
    # This calls the real frame order. Do not independently repeat its recorders.

process_touch_begin(touch):
    require prepared Touch and generated contact ID, native camera, active index
    native_0xeec024(model,touch,explicitLane=0)

process_touch_move(rawX,rawY,pressureProduct,view,touch):
    execute_original_move_conversion_block(view,touch,rawX,rawY,pressureProduct,1.0)
    # No initial-touch candidate sort here; later native frame uses retained contact.

process_touch_end(touch):
    native_0xf9a50c(model,touch)
    # Android map removal and dispatch wrappers are outside this interface.

update_long_notes_within_frame():
    native_depth_and_contact_reset()
    native_0x14858d4(model)      # continuous contacts, not the initial candidate loop
    native_0xf8056c(model,scene) # resolve/expire records, then repeated recorder calls

apply_tap_after_spatial_selection(note,contact):
    return native_0x160ce28(model,note,contact)

apply_checkpoint_units(note,units,E):
    # Description of the actual loop in0xf8056c, not a substituted harness loop.
    repeat units times:
        native_0x1730290(score,note,0,0,E,-1)
    # Native long-note guard and per-call gauge/clamping execute each iteration.

finalize_result_query():
    # Normal tests arrive here through native frame→scene callback.
    result = model.score.cachedResult
    require result != null
    return (result, native_0x1315038(result), native_0x12a5574(result))
```

### 20. Key recovered decisions, preserving order

```text
initial_input_core(model,touch):                # actual0xeec024, explanatory excerpt
    if model.paused_138 or model.finished_139: return
    update_timeline()
    line = original_camera_input_line(touch.designXY) # actual -1/+1 Z inputs
    primary,secondary = original_lane_selector(line)
    collect_enabled_taps_holds_and_arcTap_children()
    native_sort_by_signed_start_time()          # not absolute timing error
    for candidate in sortedCandidates:
        if candidate is tap-family:
            if native_try_tap(candidate,touch.contactID): return
        else if candidate is hold:
            candidate.initialLatch_a8 = true
            return

ordinary_hold_contact(hold,E,matchedLane):       # tested continuous branch
    if not matchedLane: return
    if not (hold.start < E and E < hold.end): return
    if not hold.initialLatch_a8: return
    native_hold_activate_0x14557b4(hold,touch,E)

checkpoint_active_fragment(note,E):
    cutoff = trunc_i32(f32(f32(E)+f32(note.interval*0.5)))
    units = native_resolve_pending_weighted_prefix(note.records, cutoff)
    repeat units: native_accepted_recorder(note,ID0,E,contact=-1)

ordinary_native_gain(N):                         # finite positive N, song flag0, mode0
    if N<400: T=f32(200+f32(f32(N)*0.5))
    else if N<600: T=f32(280+f32(f32(N-400)*0.5))
    else: T=f32(360+f32(f32(N-600)/5))
    return f32(f32(T/2.5)/f32(N))
    # Song scaling, mode6 and ability branches remain the native implementation.

record_accepted_core(s,note,id,E,contact):        #0x1730290
    if not note.native_v20(E,contact): return
    if id==0: s.shining+=1
    if id in {0,1}: s.PURE+=1
    if id==2: s.FAR+=1
    for gauge in nativeGaugeVector:
        native_accepted_gauge(gauge,note,id,...) # actual f32 gain/damage/hooks/clamps
    s.score = native_0xe43b80(...)
    s.combo+=1; update_max_combo()

record_miss_core(s,note,E):                      #0x868e54
    if not note.native_v38(true): return
    s.recordedLOST+=1
    for gauge in nativeGaugeVector:
        native_miss_gauge(gauge,note,E)
    s.combo=0

ordinary_score(PURE,FAR,shining,N):
    # Readable equivalence for tested valid ordinary counts; native integer helper executes.
    return floor(10000000*(PURE+FAR/2)/N)+shining

frame_termination_excerpt(model,scene,E):
    # Occurs AFTER continuous input, expiry/checkpoints, and gauge-frame update.
    if native_completion_predicate(E,chart.end,ability,mode):
        if not model.finished:
            if model.grace:
                native_failure_completion_path()
            else:
                model.finished=true
                model.delegate.v10(false)      # actual scene snapshot happens here
    if native_mode_allows_HP_failure():
        if active.H<=active.F and not model.finished:
            if scene.graceEnabled:
                native_grace_transition()     # bounded previous evidence; not new ordinary replay
            else:
                for gauge in gauges:
                    gauge.H=-1
                    gauge.continuousEnabled=false
                model.delegate.v10(true)
                model.finished=true
    # Other ability/notification branches are deliberately not invented.

snapshot_core(score):                           #0x1600bb0
    if score.cachedResult: return score.cachedResult
    finalLost = score.recordedLOST if score.byte_d1 else N-PURE-FAR
    disable_continuous_gauge_updates()
    native_update_at_chart_end()
    result = native_GameResult_constructor(
        storedScore,shining,PURE,FAR,finalLost,recordedLOST,
        floor_i32(active.H),mode,flags,otherNativeFields)
    score.cachedResult=result
    return result
    # No extra miss/gauge callbacks are synthesized for finalLost-recordedLOST.

ordinary_or_hard_classification_excerpt(result): #0x12a5574, tested modes0/1/2
    if relevant_scoreClearAbility: native_skill_classification()
    if result.mode==2:
        if result.H<0 or (result.H==0 and result.zeroHealthFails): return 0
        base=5
    else:
        if result.H<70: return 0
        base=4 if result.mode==1 else 1
    if result.LOST==0: return 3 if result.FAR==0 else 2
    return native_remaining_category_rules(base,ability)
```

### 21. Important boundaries checked against actual instructions

| Boundary | Comparison / actual observation | Scope |
|---|---|---|
| Music startup | E strictly >−O; crossing anchors E=−O | New joined timeline/input tests |
| Shining/other PURE/FAR | abs(error)≤25 /≤50 /≤100 | New joined recorders/gauge;25/26 directly contrasted |
| Tap LOST-consumption | 101..120 returns true; >120 false | Input-first fixtures; expiry can preempt it |
| Ordinary tap expiry | E>end+100 | E3100 no miss,3101 miss for note3000 |
| Hold initial latch | start<E+100 and E<end | E900 rejects/E901 latches for start1000 |
| Tested hold active branch | start<E<end plus latch | E1000 inactive/E1001 active |
| Active checkpoint | record time≤trunc(E+interval/2) |1250 resolves at1125, not1124 |
| Tested overdue hold | record time≤trunc(E−min(2*interval,500)) |1750 resolves at2250 after release |
| Camera/scene event due | E>event time | Instruction-backed earlier reports/current disassembly; not newly claimed as an executed AFF-camera scheduling test |
| Ordinary completion | E>chart end |3120 not finished/3121 finished |
| Hard HP failure | H≤F, mode enabled, not already finished | H0→−1 before end; same-frame completion can suppress this transition |
| Ordinary final health | floored integer H≥70 | Parsed100-note H67 fails/H70 clears |
| Arc horizontal extent | strict interior | Radius−.125 passes/equality fails at CameraZ900/1800 |

## Integration Coverage Matrix

Statuses apply to the specified scope, not an entire subsystem merely sharing its name. Earlier isolated execution is explicitly identified where no new joined execution exists.

| Major subsystem | Classification | Evidence and precise limit |
|---|---|---|
| AFF parsing | **Native-integrated: tested body**; headers **Instruction-backed** | Original lexer/type checks/parser into runtime objects; numeric C++ runtime supplied; whole-file/header path omitted |
| Runtime chart construction | **Native-integrated, scoped** | Original builder/count/checkpoint/depth/group tail; full metadata/account initialization and model index producer omitted |
| Timeline initialization/update | **Native-integrated, scoped** | Native selected-offset sum, epoch start, clock conversion, updater and judges; imported counts synthetic |
| Touch transport/projection | **Native-integrated: conversion block/projection→judge**; Android transport **Instruction-backed** | No JNI/Android map/listener/queue emulation |
| Candidate collection/sorting | **Native-integrated** | Original range scan, collection, sorter, rejection and consumption in joined tap chains; source index supplied |
| Tap judgment | **Native-integrated** | Actual note guards, recorders, score/gauge, model completion and GameResult |
| Arc-tap judgment | **Native-integrated, prepared parent/geometry** | Actual parent-child collection/spatial check/acceptance/score/gauge; AFF arc geometry construction not joined |
| Hold checkpoint handling | **Native-integrated** | Parsed hold, native record generation/count, continuous contact/end, frame, score/gauge/result |
| Arc checkpoint handling | **Native-isolated at activation; native-integrated conditional callback chain** | Native weight2 generation→expiry/recorder/clamps/result; active flag supplied; ownership omitted |
| Flick handling | **Instruction-backed**; prior native-isolated fragments | No new complete flick replay; do not transfer tap arbitration rules to it |
| Score calculation | **Native-integrated** | Native integer helper and counters/getter in joined results; overflow/invalid-count domains untested |
| Gauge modification | **Native-integrated: modes0/1/2 and one rate skill** | Native f32 gain/damage/clamps; full special continuous modes/staged configurations not joined |
| Character skill effects | **Native-integrated: one supplied ability effect**; selection gate **Instruction-backed / prior Native-isolated** | Exact compound key factory/selector→timed gain/loss; equipment/level/awakening lifecycle omitted |
| Clear/fail classification | **Native-integrated, scoped** | Actual frame completion/failure→scene snapshot, native getter/classifier queries; zero-health flag producer unknown |
| Camera transformations | **Native-integrated: actions→Node/matrix→input/judgment** | Driver schedules native actions; no complete Scheduler or AFF-event timing replay |
| Tap rendering geometry | **Native-integrated CPU state, scoped** | Logic/depth/hidegroup→whole tap updater/Node opacity; render Scheduler/GPU omitted |
| Arc rendering geometry | **Native-isolated in earlier003/007; Instruction-backed connections** | No newly joined arc mesh/GPU path; prepared samples/child positions do not establish a full renderer |
| Visual feedback | **Native-integrated: opacity/shared-state examples**; judgment bursts **Instruction-backed** | Actual track/tap Node opacity; hit/miss UI delegates isolated; particles not activated |
| Audio scheduling | **Instruction-backed; prior Native-isolated provider tests** |008 logs request boundaries only; no continuous native main→provider→FMOD chain |
| Result persistence | **Instruction-backed** | Prior concrete writers retained; post-snapshot queue/save/presentation work skipped, no external effects |
| Full Android/GPU/device synchronization | **Unknown / unexecuted** | No physical device, screenshot, hardware latency or oscillator validation |

A label of “native-integrated” does not erase the runtime-service hooks or supplied index. No percentage of complete-engine coverage is asserted.

## Confirmed Discrepancies, Distinctions, and Limitations

### 22. Historical hold-lookahead discrepancy — recorded separately

**Earlier claim:** Expedition002, “Holds and arcs,” described holds in continuous routine `0x14858d4` as having “a start lookahead of 120 ms.”

**New evidence:** for an actual LogicHoldNote, ordinary model `+0x148=0`, input-enabled byte1, matching lane, unconsumed state, and initial latch set, instructions `0x1485d74..0x1485db0` require start<E<end. Original frame tests at E901/1000/1001 show latched-but-inactive / latched-but-inactive / active. Initial collection's separate strict100 ms predicate is also measured.

**Assessment:** the unqualified120 ms characterization is not correct for this tested ordinary hold-activation branch. Other model/state branches are not ruled out. Arc lookahead evidence remains separate and is not changed.

**Proposed clarification, not applied to historical files:** distinguish the initial hold latch's `<E+100` from the tested continuous hold activation's `start<E<end`; retain120 only for branches that actually implement it. No earlier file or earlier context text is modified without authorization.

### 23. Differences that are not historical contradictions

- **Internal lane versus AFF integer:** new representation mapping fills an earlier gap; it does not invalidate measured internal lane boundaries.
- **69/70 accepted units versus a full missed tail:** different callback schedules, not a different gain or threshold formula.
- **H0 survival classifier versus frame failure:** completion order/finished flag/zero-health flag explain the differing outputs. H0 was never universally equivalent to −1.
- **Synthesized versus recorded LOST:** finalization reconciles counts without replaying all missed gauge operations. The supplied-index jump experiment illustrates that distinction; it does not establish the original index producer's exact behavior.
- **Stored versus getter score:** deliberate flags/denominators differ. The producer of those flags remains unknown.
- **Projection change versus eligibility change:** camera movement and spatial tolerances are different native operations. Pitch can move a target's screen position while stale input remains inside lane/depth bounds.
- **Missing speed/group lifetime:** these were incomplete fixture preconditions, not evidence of an archive bug or a newly discovered production default.

### 24. Validation inventory and reproducibility limits

Every successful group used original ARM64 instructions at the entries/blocks identified above. Observed outputs and assertions are the tables/traces, not simulated equations substituted for native outputs. The final successful runs include:

| Test group | Native coverage and fixture | Expected/observed comparison |
|---|---|---|
| Compiled four-tap replay | Body lexer/parser/runtime/count/depth; full frame; input/score/gauge; scene snapshot | Exact trace in section10; final6,250,002/H48/category0 |
| Compiled hold replay | Body/runtime plus native generator/count; begin/continuous/end/frame/result |3 records/units; two PURE+one LOST;6,666,668/H51/category0 |
| Compiled100-tap ordinary boundary | Original body/runtime/postprocessing and native frame with regular missed-tail updates |89 hits→11 LOST/H67/fail;90 hits→10 LOST/H70/clear |
| Compiled100-tap frame jump | Same native chain and supplied index, no intermediate tail frames |90 hits, recorded9/final10 LOST/H72; expected difference is explicitly retained |
| Candidate competition | Six prepared paired-candidate schedules | Earlier FAR, consumed skip, outside-window skip, and input/expiry order results in section11 |
| Native hold start boundaries | Five E values880/900/901/1000/1001 | Exact latch/active table in section12; original branch comparisons observed |
| Weighted arc checkpoint | Original shared initializer/generator override/checkpoint pass/recorders/gauge/result | Weights1/1/2; callbacks1/1/2; four clamp audits; active state supplied |
| Ordinary/hard failure and finalization | Native miss guard/gauge, enclosing frame or scoped failure block, real scene callback | Ordinary H0 continues; pre-end hard H0→−1 fails; completion-first H0 category5 unless zero-health flag set |
| Timeline offsets/input | Three signed offset combinations × strict trigger before/equal/after; subsequent actual input | Anchor values in section15, then native judgment/gauge at E1025 |
| Touch timestamp boundaries | Six E values × two widely separated stored timestamps | Identical native judgment/score/gauge state for each pair |
| Pause/resume/input gate | Native wrapper/timeline freeze5s/resume/input at next1ms | E1025 fixed, no gated judgment; seek1175/unpause; E1026 other PURE |
| Inter-frame clock refresh | Native frame1000 then begin with imported count110 ms later | Last-frame global1000, judge E1110 and late LOST |
| Integer position conversion | Original constructor0..5 × mirror0/1 |12 exact ID/normalized-X outputs; table in section4 |
| Timing initializer | Original `0xbe2b98`, tempo120, speed0/6 | Positive infinity /0.0833333358168602; no invented fallback |
| Camera-to-tap | Three paired native action cases, original perspective/project/unproject/plane/judge | Reprojected lane-plane point within.5 units; stale-point behavior table in section16 |
| Prepared arc-tap | Actual parent-child spatial path, native child acceptance/score/gauge | One shining PURE; duplicate touch no second unit |
| Dynamic arc extent | CameraZ900/1800; three x-edge probes each | Strict190/380 radii with actual Camera getter |
| Viewport block-to-input | Raw1580/590, origin100/50, scales2/1.5 | Native design740/360 then shining PURE |
| Hidegroup/render/input | Actual dispatcher, logic link/depth updater, whole tap updater and native Node opacity | Render opacity0, input byte1, actual accepted judgment |
| Widen/state/input | Two event kinds, actual model frame, same touch before/after | G1.5 enables secondary lane; W1 enables outer lane; score/gauge execute |
| Track callback/Node output | Original callback/propagation/native opacity setters, two Nodes, five ticks | Both Nodes254/239/191/111/0 |
| Skill factory/effect | Exact compound key, native selector/factories, timed hit and native miss | Mode1/H30→30.700000762939453→29.5 |
| Snapshot flags/getter | Two supplied `+0xd1` states, repeated finalization, `+0xb1` getter flag | Cached pointer stable; stored/getter distinction table in section14 |

Temporary Python harnesses and JSON traces are scratch research intermediates. They are not committed. The fixtures, state layouts, hook inventory, call/range addresses, and schedules here define the reproducible scope without publishing additional repository artifacts.

Remaining unexecuted work includes the full whole-file/header/metadata initializer, original spatial-index producer, full Android event transport, a continuous cross-library FMOD chain, complete colored-arc ownership/checkpoint/render coupling, flick replay, complete skill activation/special scenes, GPU output, and persistence. The report does not substitute familiar rhythm-game behavior for those missing interfaces.

## Unresolved Mysteries

1. The exact original construction and update policy for model spatial buckets, including note insertion across boundaries and long frame gaps; the prepared-index results must remain conditional until that producer is recovered.
2. Producers/ranges of zero-health-fails, selected-LOST, stored-score-return, and other special result flags; their effect on completion/failure ordering in production scenes.
3. Full Scheduler/ActionManager/Android callback order, camera action overlap/reset cancellation, pause/seek/foreground transitions, and fresh-input timing relative to cached geometry on actual devices.
4. Full AFF header/file parsing and metadata integration under native runtime services; malformed/negative/exponent/locale inputs and all chart types.
5. Complete ordinary arc ownership and connected-group contact lifecycle joined to native checkpoint scoring, geometry caches, render feedback, and end cleanup; full flick integration.
6. Complete character equipment/activation/level/awakening and special-scene lifecycle, beyond the supplied representative ability.
7. Main-library→provider→FMOD continuous scheduling/seek integration, output latency and oscillator behavior; actual GPU resources/drawing and database/network submission eligibility.

These are bounded limitations of Expedition008, not a plan or authorization to begin another expedition.

## GitHub Status

Authorized publication consists of this new report and an append-only Expedition008 entry in `context.md`, on existing `main`. No harness, extra artifact, README, project instruction, binary, asset, or report001–007 is included in the publication scope.

Exact publication commit SHAs, pinned read-back equality, historical-file preservation, and the final two-file commit comparison are recorded in the headquarters return report after committing. This document does not invent a self-referential future commit SHA.
