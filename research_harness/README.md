# Arconist native ordinary-solo regression

A source-preserved Expedition 023 experiment, packaged in Expedition 024. It executes the original AArch64 game library in Unicorn, using controlled host ABI/platform/catalog services. It is **not** a full Android application, GPU renderer, audio player, production account client or general Cocos emulator.

## Run

Validated with CPython 3.12 on Linux x86_64. Use an isolated environment, without Python `-O` (assertions are required):

```bash
python3.12 -m venv /path/to/venv
/path/to/venv/bin/python -m pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip \
  --output /path/to/regression-result.json
```

The entry point resolves its source and fixture paths from its own location; it can run from any current directory. A full run may take a few minutes. Exit0 means all assertions passed; exit1 means validation/native execution/assertions failed; exit2 means output could not be written. Use `--verbose` for adapter diagnostics on stderr. Default output is `regression-result.json` in the caller's current directory. Outputs inside this package are rejected. Generated results, caches, environments and original resources must not be committed.

Pinned runtime dependencies actually validated: `unicorn==2.1.4`, `pyelftools==0.33`. Capstone was used for historical investigation but is not needed by this runtime package. No ChatGPT tools, API credentials, preexisting kernel, memory snapshot, old scratch script, host SQLite implementation or network service is required at execution time.

The original external archive must contain `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

The library is verified before importing/initializing execution adapters, then loaded from an in-memory stream. Resource bytes are read directly from the supplied ZIP. The package does not extract or redistribute `.so`, original CSB, fonts, textures, audio or other application files. Use the same archive examined in the reports; an incomplete archive can pass the library check and still fail later if required resources are absent.

## What is tested

`fixtures/ordinary_two_tap.aff` is synthetic research input, not the archived chart. Selected metadata is `sayonarahatsukoi`, difficulty0, set `base`, no purchase/map/modifier, mode0, speed40, controlled profile/settings and40 zero PlayParameters bytes. The existing inactive difficulty pointer slots alias the prepared object; only difficulty0 is selected/available. Full production catalog/availability/UI parameter generation is not executed.

The runner executes original static registries including `0x1054f24`, native menu constructor/setter, ordinary `0xee197c` eligibility, native request latch and `0xee29a8 → 0xee29e8` construction. Native loading actions invoke initialization and Director activation. Director visitation drives model frames; native timeline E determines two JNI DOWN/UP pairs. Native completion caches GameResult, GameEnd ActionTimeline invokes frame50 continuation, original code creates GameSession/results, native results gate permits bundled SQLite writers, and native closing lifecycle activates results.

Automatic assertions check:

- Original entry, eligibility return1, latch1, allocation/constructor caller and initializer1; no multiplayer helper.
- No direct host entry into GameScene constructor/initializer/model-frame, continuation, shutter callback, GameSession or persistence writers.
- Native visit-driven model updates and two native JNI/listener/judgment pairs.
- PURE2/FAR0/LOST0, score10000002, live health80.4000015258789 (tolerance1e−6), integer health80, clear3.
- One snapshot/cache, native24-track/85-frame ending, frame49 before continuation and frame50 with exactly one continuation.
- `ScoreState+0x68 == GameSession+0x18`, original scene/model identities and native results type. Heap addresses are observations, never required constants.
- Original gate observations, one result initializer and one score/clear writer each, bundled SQLite API execution and expected single rows for the selected song/difficulty.
- Final results running, pending0 and enabled dispatcher. Limited extra Scheduler/Director updates leave rows and callback/save counts unchanged.

Loading and results each use `0x963094` and `0x113af20`: total2 is correct; result initialization, ending continuation and each persistence writer execute once. The private database is `:memory:`; calendar time1700000000 and monotonic times are controlled. The JSON distinguishes original ELF VAs, allocated emulated pointers and relational checks. On failure it emits `status: fail`, not canned expected results.

## Source availability and module inventory

All required source was recovered from actual scratch adapters. No essential module was unavailable and no native subsystem was reconstructed from prose reports. Class names retain provenance; source module names describe service responsibilities. Historical diagnostic entry points, manually assembled scene experiments and manual ending hierarchy helpers were removed. Existing unused compatibility methods may remain where inherited services share implementations; this runner's host-entry assertions guard the tested path.

| Published component | Original source | Classification and purpose |
|---|---|---|
| `src/arm64.py` | recover.py | Existing recovered ELF mapping, relative relocations, CPU/memory/register/call services; consolidated input streams and host-entry observation |
| `src/chart_services.py` | exp010.py | Existing C++ strings/streams/numbers and native AFF resource boundary; synthetic fixture moved to file |
| `src/sqlite_services.py` | exp013.py | Existing native SQLite forwarding, private DB/schema/readback and libc services |
| `src/results_services.py` | exp014.py | Existing results gate/UI boundary, Scheduler inspection/reference services; manual scene builders removed |
| `src/action_services.py` | exp015.py | Existing action inspection and panel proxy boundary; obsolete direct frame/scene setup removed |
| `src/transition_services.py` | exp016.py | Existing transition/action observation, clock/feedback services |
| `src/ending_services.py` | exp017.py | Existing animation observation/math services; manual hierarchy/binding helpers removed |
| `src/bootstrap.py` | exp018.py | Existing native Director/GLView setup, supplied app/catalog/settings/JNI clocks and metadata |
| `src/resources.py` | exp019.py | Existing symbol relocations, CPU CSB/fonts/RTTI/resources/textures/GPU services and runtime support |
| `src/track_services.py` | exp020.py | Existing locale/capability/pixel-format adapters and original CPU TrackLayer support |
| `src/menu_services.py`, `src/solo_entry.py` | exp021/022.py | Existing original menu construction observations, checked strings, input fixture and ordinary entry |
| `src/lifecycle.py` | 019_driver/021_full_driver/023_driver | Consolidated explicit loading, gameplay frame, ending/results/extra-update schedules; no runtime source extraction/exec |
| `src/regression.py` | 023_driver plus strengthened assertions | Consolidated scenario; newly added automatic relational/count/input/save/native-boundary checks |
| `run.py`, `src/config.py`, `src/boundaries.py`, tests and requirements | Expedition024 | Newly implemented packaging, verification, CLI, small JSON output, negative tests and declarations |
| Archive bytes, catalog/profile/settings/ABI/platform services | External input / host adapters | Intentionally supplied; not original Android startup or authorization |

`src` modules are private to this entry point and use local sibling imports. No module requires the historical source filenames or their original locations. Native APIs forwarded to defined ELF symbols are not host implementations of those functions.

## Exact retained boundaries

All addresses below are **unrelocated original-library ELF virtual addresses**, not allocated object addresses. Deliberate skips preserve the behavior validated in023:

| Source → resumed PC | Omitted/supplied scope |
|---|---|
| `0xf72110 → 0xf72158` | Platform GLView attachment |
| `0x16a4238 → 0x16a48d8` | Shutter panel resource creation; two original-constructed native Node proxies |
| `0x121581c → 0x121584c` | Platform loading overlay |
| `0xa507c4 → 0xa519ec` | Song-information artwork prefix; supplied native Node visual target |
| `0xa51adc → 0xa5213c` | Remaining information artwork/actions/canary after native callback action registration |
| `0x196fdac → 0x196ffac` | Information child closing visuals |
| `0x891190 → 0x89164c` | Results UI prefix; X28 application global and X26 scratch restored; original gate producer retained |
| `0x891688 → 0x89219c` | Middle results UI; original save branch retained |
| `0x8921dc → 0x8928e0` | Post-save UI/progression |

Native eligibility, GameScene/TrackLayer construction, CPU updates, GameEnd resource hierarchy/binding, judgments/results, action callback decisions and SQLite writers remain original. Whole-function render/traversal/flush services `0x129c924`, `0x1017a84`, `0x13edf0c` remain inert; TrackLayer update `0x19069a0` executes. Textures use finite native-created placeholder data, not original artwork. Audio/GPU/JNI/platform/account/catalog/settings workers, C/C++ ABI/locale/locks/TLS/clocks, allocator/autorelease/free and bounded null-reference services remain supplied. Pending submission processor `0x1246c98` is inert. Non-null native Ref arithmetic executes; complete reclamation is not tested. No network is contacted by the native experiment.

The source records hook addresses and supplied behavior directly. Reports018–023 provide the detailed historical service provenance. No claim of production save compatibility, online authorization, complete Android emulation, real GPU/audio output or full menu/result UI is made.

## Negative tests

```bash
/path/to/venv/bin/python -m unittest discover -s research_harness/tests -v
ARCONIST_TEST_ARCHIVE=/path/to/arccopy.zip \
  /path/to/venv/bin/python -m unittest discover -s research_harness/tests -v
```

The first command checks missing archive and incorrect library hash; the second also executes the native unavailable-song control. Alternatively use `run.py --archive ... --unavailable-song --output ...`. A passing negative output explicitly says `test: unavailable_song_rejected` and `game_scene_constructed: false`; it is not a full-session pass. The unavailable byte0 path must return native eligibility0, latch0, no constructed GameScene and pending0. Fast input tests never substitute for the full regression.

## Clean validation

Copy only this package into an otherwise empty directory (or check out the published commit), create a fresh Python3.12 environment, install this requirements file and run the documented command from another directory with the external archive. No generated source files, extracted native binaries or scratch modules are inputs. The024 report and final handoff record the actual validation outcome and pinned publication.

## Expedition 025 arc-tap scenario

The default command and two-tap fixture/assertions remain unchanged. A separate, bounded scenario loads `fixtures/native_arc_tap.aff` through the original whole-chart path:

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario arc_tap \
  --output /path/to/arc-tap-result.json
```

`--scenario ordinary` is the explicit default. `--unavailable-song` belongs only to that ordinary scenario; combining it with `arc_tap` fails clearly. Dependency versions are unchanged.

The new fixture contains one constant-position trace arc with one embedded child at1500. Native construction must produce the parent/child vector, back-link, geometry and N1; those links/fields are never assigned by the driver. The scenario derives the ordinary Z=0 input-plane target from child geometry XY and quantized parent X, calls original camera projection `0xbdbb70`, then applies the Y-up/design-coordinate conversion. Sampler-local geometry Z is recorded separately and is not assumed to be the ordinary input plane.

Two original JNI contacts use fresh pointer IDs at the same native effective E1500. Both must traverse the same parent's child vector, pass native spatial eligibility and reach the same child's timing classifier. Only one may reach `0xc78814`/the recorder. The duplicate must read consumed=1 through original `0x180cf28`, leave score/counters/health unchanged, and clean up its native contact. The scenario stops here; it does not run ending/results/SQLite or create a GameResult.

Read-only code/memory observations prove the parsed child time/mode, native factory result, native parent-store PC and native geometry-store PCs. All assertions use relational heap pointers. No direct host call to a builder, sampler, model frame, classifier, acceptance or recorder is permitted. Expected score is derived from the native N1/all-PURE result, rather than copied from the earlier prepared-child test. JSON records exact observed geometry, projection, native calls, result deltas, duplicate guard, ABI use and boundaries.

This first arc-tap construction also exercises the original archived `models/tap_l.obj`/`.mtl` CPU reader. `src/arc_tap_services.py` supplies its missing libc interfaces only for this scenario: `strspn`, `strcspn`, `strchr`, double `pow`/`ldexp`, bounded `sscanf`, and checked formatting through the existing formatter. The original mesh reader and game geometry/construction remain native. The finite fixture uses only `%s` scanning; the adapter supports only simple `%f`/`%d`/`%s`, whitespace/slash formats, at most six output pointers and input shorter than256 bytes, failing outside that domain. Linux host libc is accessed through standard-library ctypes; this is a supplied ABI service, not native Bionic or an extra Python dependency. Complete scanf, floating overflow/error semantics and malformed OBJ compatibility are not claimed.

The nine existing PC skips remain declared. No new instruction skip or graphics-object proxy is introduced. Native-created geometry in this controlled environment is not a claim of original-device visual fidelity.

Optional native unittest (the documented CLI itself also performs all scenario assertions):

```bash
ARCONIST_ARC_TAP_TEST_ARCHIVE=/path/to/arccopy.zip \
  /path/to/venv/bin/python -m unittest discover -s research_harness/tests -v
```

Without that environment variable, this expensive native test is explicitly skipped. Original input tests and the optional unavailable-song test retain their separate switches.

## Expedition 026 hold scenario

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario hold \
  --output /path/to/hold-result.json
```

This scenario runs **two fresh Unicorn/native runtimes** with `fixtures/native_hold.aff`: one uninterrupted contact and one JNI UP/repress comparison. Python3.12 and the pinned024 dependencies are unchanged. No025 arc-tap-specific ABI service is needed, and no new service, instruction skip or proxy is introduced. The default and arc-tap scenarios retain their fixtures and assertions.

Original parser/chart builders create the hold, lane conversion,250 ms interval, three12-byte checkpoint records, N3, chart end and spatial index. Read-only observations record the original factory return, generated record inputs, actual index keys, native checkpoint-resolution writes, resolved guards, contact reset/activation writes and recorder entries. Heap identities are relational. The existing ordinary entry/loading/Director driver supplies all native scene/model handoffs.

The external contact target is derived from the native-created lane4 and the original ordinary lane selector's world interval `[0,425)` at `0x13074d0..0x13074e0`. Its center `(212.5,0,0)` is projected through the scene's original camera `0xbdbb70`, with native Director height/Y-up conversion. This is an external input-plane target, not host-assigned hold geometry. Original JNI/continuous input must independently unproject it into the correct lane. No old screen coordinate is presumed valid.

The native clock anchor supplies wall times for E1000/1001,1124/1125,1200/1201,1300/1301,1374/1375 and1624/1625/1626. The interrupted case sends UP42 at E1200 and DOWN43 at E1300. Assertions distinguish Android ID, generated gameplay ID, Touch allocation, engine map/mask, model retention, initial latch and current activity. E1201 must clear activity with no retained contact; E1301 must activate using the new Touch. Both cases clean up through terminal JNI UP and a final E1627 Director frame.

Both must record PURE3/FAR0/LOST0, score10000003 and native live health approximately80.5999985. Every checkpoint must have exactly one native0→1 resolution write at `0xf80924`, and later native `0xf80904` guards must observe it resolved. Native accepted recorder calls must total3 on the original hold at E1125/1375/1625; misses must total0. JSON includes each complete trace and the comparison. It stops before completion, GameResult, ending, results or SQLite for this fixture.

Optional original-native unittest (the CLI itself performs all assertions):

```bash
ARCONIST_HOLD_TEST_ARCHIVE=/path/to/arccopy.zip \
  /path/to/venv/bin/python -m unittest discover -s research_harness/tests -v
```

Existing `ARCONIST_TEST_ARCHIVE` and `ARCONIST_ARC_TAP_TEST_ARCHIVE` switches remain independent. Tests without an archive switch explicitly skip the corresponding native run; they never emit canned success.

## Expedition 027 chord scenario

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario chord \
  --output /path/to/chord-result.json
```

`fixtures/native_chord.aff` contains `(1500,1);` and `(1500,4);`. Original parsing and runtime construction must produce two distinct equal-time LogicTapNotes, native lanes2/5, N2 and index membership for both. The existing ordinary solo entry, original loading initializer and Director activation remain unchanged. There is no new ABI service, proxy, PC skip or dependency.

`src/chord.py` runs two fresh emulators. Android42 always targets native lane2 and Android43 lane5. Forward sends DOWN42/DOWN43/UP42/UP43; reverse sends DOWN43/DOWN42/UP43/UP42. Both DOWNs occur at the same observed native E1500 and wall time, without an intervening Director frame or clock advance. Native begin refreshes are observed after `0xeec07c`; supplied event timestamps do not determine chart time. This is overlapping contact lifetime across sequential JNI calls, not atomic Android MotionEvent batching.

External input-plane centers `(-637.5,0,0)` and `(637.5,0,0)` are chosen from native-created lane IDs and original selector semantics, projected through current native camera `0xbdbb70`, then Y-converted using native Director height. These conservative interior targets do not assert universal outer hitbox bounds. Original unprojection must independently return lane2/5 with secondary0; each native candidate vector must contain only the matching note.

After the first DOWN, exactly one note/contact/judgment may exist. After the second and before any UP, both Android IDs, distinct slots, native Touch allocations and generated gameplay IDs must coexist. Each note's original accepted-ID field must match its corresponding contact; the first contact must remain retained. Original `0x965e68` consumed-byte and `0x965e6c` contact-ID writes, `0x965e28` acceptance and `0x1730290` recorder provenance are observed without modifying them. Each note is accepted once, with two accepted units and no miss.

Both cases must finish with PURE2/FAR0/LOST0, shining2, score10000002 and native live health approximately80.4000015. Original UPs must remove both mappings, slot pointers, mask and gameplay retention without another judgment. The JSON compares note identities by native lane/time, not equal-time vector order or cross-emulator heap addresses/generated-ID assignment. It stops at E1500 after cleanup; no chord GameResult/results/SQLite replay is performed.

The CLI performs every chord assertion; no extra unittest wrapper is required. To execute all existing opt-in scenario/input tests (in addition to the ordinary and chord CLI commands):

```bash
ARCONIST_TEST_ARCHIVE=/path/to/arccopy.zip \
ARCONIST_ARC_TAP_TEST_ARCHIVE=/path/to/arccopy.zip \
ARCONIST_HOLD_TEST_ARCHIVE=/path/to/arccopy.zip \
  /path/to/venv/bin/python -m unittest discover -s research_harness/tests -v
```

Historical fixtures, scenario source/assertions, tests and pinned requirements are preserved.

## Expedition 028 moving arc and crossing scenario

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario moving_arc \
  --output /path/to/moving-arc-result.json
```

This runs `fixtures/native_moving_arc.aff` first, then `fixtures/native_crossing_arcs.aff` in a fresh native runtime only after the moving control passes. Both use ordinary arcs1000..2000, linear`s`, X.20→.80, Y.50; the pair adds the reverse direction in color1. Original parser/builders create geometry, checkpoints, colors and spatial index inside ordinary solo-created GameScenes. `crossing_arc` is an internal fixture selection used by this driver, not another exposed CLI scenario.

The scenario additionally executes **complete original ELF initializer `0x1930604`**, the `.init_array` member referenced at`0x1b95c90`, before chart construction. Its native stores at`0x1930abc/0x1930ac8/0x1930adc/0x1930ae4` produce the established spatial globals180/550/250/100. Earlier scenarios leave those globals at zero; ordinary arc width would then be degenerate. No Python global assignment or gameplay skip repairs that rejection. This initialization is scoped to the new scenario; old scenario source/assertions remain unchanged. The native geometry-height global remains0 in this controlled environment, producing sampled/cache Y50. Rendering fidelity is not asserted.

`src/jni_arrays.py` recovers only011's minimal JNIEnv array contract: GetArrayLength(+0x558), GetIntArrayRegion(+0x658), GetFloatArrayRegion(+0x668), bounded to one/two elements and checked types/regions. Its `0x4000400/0x4000410/0x4000420` trampolines are emulated host-service addresses, not ELF code. It copies external ID/float arrays to native JNI staging buffers; original JNI MOVE `0x1706960`, GLView `0x160b710` and gameplay callback `0x10e7008` update all Touch fields. It never assigns a gameplay Touch, owner, geometry/cache, active flag or score. The unchanged025 OBJ/libc helper is installed for reuse; these fixtures make zero calls to it. No new third-party dependency, renderer proxy or PC skip is added.

Director frames sample E1000/1001/1125/1250/1300/1375/1500/1625/1750/1875. Each first computes original caches; the host projects targets derived from those caches, delivers DOWN or one MOVE array, then visits another original Director frame at the same E. Repeated-time frames execute native duplicate guards. This sparse following schedule is supplied input, not host AFF interpolation or Android queue/hardware emulation. Native consumer float32 quantization combines parent-start X with local cache displacement; Z=0 is the input plane, separately from sampled local Z. Original continuous input may clamp Y before its native spatial test.

Read-only observations record parsed X/Y/mode/curve, factory returns, native geometry appends/sample vectors, original cache writes`0x19f423c`, camera/projection, retained Touch identity and current/previous coordinates, spatial results, native color claims/releases, actual proximity comparisons and record-resolution writes. N3/N6 and the original record weights determine result assertions. Both cases require unique native checkpoint writes and original recording with no misses; cleanup must empty mappings/slots/retention/claimed IDs and clear arc activity without another award.

The crossing comparison distinguishes the original comparison distance from the post-frame separation. The original loop can compare one updated arc cache with its neighbor's older cache; bypass can also persist under the native500 ms reset condition. The scenario records actual owners/bypass/conflict/release state rather than forcing exclusive owners or immediate restoration after separation. It stops at E1876 after UP and next-frame cleanup; completion/results/SQLite are not exercised for these charts. No extra optional native unittest wrapper is added; the CLI runs both complete gates and all assertions.

## Expedition 029 timing-group and reverse-scroll scenario

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario timing_group \
  --output /path/to/timing-group-result.json
```

`src/timing_group.py` first runs `fixtures/native_timing_group.aff`, then creates a fresh runtime for `fixtures/native_reverse_scroll.aff` only after the complete control assertions pass. Both have default-group tempo120/tap1500/raw4 and separate-group tempo60/tap1500/raw1. The reverse fixture adds only `timing(1200,-60.00,4.00);` inside the separate group. `reverse_scroll` is an internal fixture selector, not an additional CLI option. Both fixtures are synthetic research input.

The scenario reuses ordinary native solo entry/loading/Director activation and complete original static initializer `0x1930604` from028. It adds no service, dependency or gameplay PC skip. Original whole-file/group parsing, timing initialization, tap construction, group-index and timing-pointer stores, precomputed-depth writes, descriptor lifetime stores, native index insertion and active-range updates remain native. Native pointers are checked relationally, not against fixed heap addresses.

Director frames sample E0/1000/1100/1199/1200/1201/1300/1499/1500 using the native timeline/music anchor. Read-only observers record actual `0xcf918c` inputs, contributing timing records and float32 returns, `0x1017d80` inputs/native depth stores, signed producer keys and query intervals, the new-admission depth predicate and retained membership independently. This fixture's tap insertion keys are1 and0 in both cases; negative-tempo parsing does not imply a negative insertion key. Native preroll queries also exercise negative signed intervals, separately from the negative-tempo transition.

The reverse tap is admitted during preroll and remains retained while its depth rises above the300 new-admission limit, then reverses at E1200 and returns to zero atE1500. This does not assert successful fresh admission after an arbitrary frame jump. Input-enabled, resolved, index, query and active states are reported separately.

At E1500 native lane5/2 centers on the input plane are projected through current original camera `0xbdbb70`, converted using Director height, and delivered as DOWN42/UP42 then DOWN43/UP43 without advancing chart time. Original unprojection, lane-specific candidate vectors, classifier, recorder, consumed-byte/contact-ID writes and cleanup must agree. Both cases require N2, PURE2/shining2/FAR0/LOST0, score10000002 and live health80.4000015258789. The JSON retains available partial observations and emits failure if a gate fails; no scripted native success is substituted. CLI assertions cover both gates without another optional unittest wrapper. Stop atE1500 after native UP cleanup; no new results/SQLite run or audio-reversal claim.

## Expedition 030 camera construction blocker

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario camera_reset \
  --output /path/to/camera-reset-result.json
```

**This is a reproducible blocked diagnostic, not a passing camera/reset regression.** It returns exit1/JSON `status: fail` with `NativeCameraConstructionExcluded` when the verified original rejection is reproduced. `src/camera_reset.py` runs only the overlap control using `fixtures/native_camera_overlap.aff`. The original whole parser accepts camera600/translation600X/linear2000ms and camera900/rotation15Z/qi2000ms, but original chart construction omits both for the unchanged ordinary `sayonarahatsukoi` fixture. Native `1863e58` reads chart+110=0; the original exact-song exception is also false; `186453c→1863d60` skips each parsed record. Original `173c3cc` produced the zero property byte. No host assignment repairs it.

The diagnostic records parsed objects, actual builder decisions/property write, native scene/rig/child-camera relationships, tap/index state, original Scheduler→ActionManager dt and target snapshots atE500/600/601/900/901. It distinguishes other loading/UI actions from camera actions: no rig or child-camera target entry exists at those snapshots, and no camera handler/builders/reset/JNI judgment execute. Child transforms remain unchanged. Cached matrices are reported as read; no observation getter forces a refresh.

`fixtures/native_camera_reset.aff` preserves the control and adds the proposed zero-triple reset at1200. It remains an **unexecuted candidate** because Gate A failed. `camera_reset_variant` is an internal fixture mapping, not a tested second scenario. The package neither fabricates camera logic/actions nor starts Gate B or judges a stationary-camera tap as evidence of camera integration.

Native chart+110 can be enabled by original digest/named-song decisions, and the builder separately recognizes exact Song ID`designant`. Those alternatives need a justified ordinary catalog/chart/eligibility fixture before another integrated attempt. Do not supply a fake digest, assign chart+110, rename the baseline song while retaining false metadata, or skip the original branch. The reset/child-action survival question remains unknown in an ordinary native-owned GameScene. Original007–011 isolated action evidence retains its stated limits.

No new dependency, platform/renderer service or PC skip is added. Existing scenarios, fixtures, assertions and dependency pins are preserved; run their commands and existing opt-in unittests normally. The expected failing camera diagnostic must not be counted as an end-to-end passing regression.

## Expedition 031 track-display construction blocker

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario track_fade \
  --output /path/to/track-fade-result.json
```

**This is a reproducible blocked diagnostic, not a passing fade/replacement regression.** It returns exit1/JSON `status: fail` with `NativeTrackDisplayConstructionExcluded`. Original whole parsing accepts `scenecontrol(600,trackdisplay,2.00,0);` from `fixtures/native_track_fade.aff`, and original classifier `1090060` returns kind0. But native chart+110=0 sends construction through fallback comparisons for kinds4/5/6 and named-song exceptions; the current `sayonarahatsukoi` fixture satisfies none. The observed native `186558c→1863d60` edge omits the control, so no LogicSceneControl or fade timer exists.

`src/track_fade.py` also records the original feature producer: `e2f5cc` initializes handler+2c8 to0, `e2f5d4` sets current opacity255, and `e2f618` copies the original `16a3a6c(chart)` property result into handler+2c8. That result is0. The later kind0 handler gate is instruction-backed and unexecuted here; it must not be described as an executed rejection. Original owner initialization connects the existing TrackLayer collection, whose actual native TrackBase membership and opacity bytes are recorded read-only. No arbitrary Node is inserted and no setter/callback is invoked from Python.

The final diagnostic lets original loading and Director activation finish to inspect those native producers, then stops. It does not advance a fade timeline, manually schedule a timer or run a callback. `fixtures/native_track_fade_replace.aff` adds the proposed900ms replacement toward255 but remains an **unexecuted candidate**; internal `track_fade_replace` selection is not a tested second CLI case. Closure counters, callback interpolation, Node propagation and timer replacement are explicitly unexecuted. Available partial observations survive unexpected failures.

The missing prerequisite is a genuinely scene-control-permitted original chart/catalog context, not a callback ABI or a renderer repair. Do not write chart+110 or owner+2c8, fabricate a digest, rename the song with inconsistent metadata, call the fade handler directly or inject events/Nodes. Previous007/008 isolated callback evidence retains its original scope. G-006 and `camera_reset` remain unchanged and blocked; the existing successful regressions remain separate from both failing diagnostics. No new dependency, service or PC skip is introduced.

## Expedition 032 CPU tap refresh and expiry

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario cpu_note \
  --output /path/to/cpu-note-result.json
```

`src/cpu_note.py` runs the single-tap `fixtures/native_cpu_note.aff` in two fresh ordinary GameScenes: `judged_tap`, then `unjudged_expiry`. It verifies native renderer initialization and reciprocal logic links, the embedded TrackLayer+3b8 renderer vector, original child quad, chart/index/listener and Director activation. This chart produces N1/end1620 and504 renderers (503 bars/one tap); heap pointers are relational observations.

Only this scenario removes the existing inert `0x129c924` Node::visit hook **after original loading/activation**. Complete original base traversal then reaches TrackLayer::visit `960288 → b1638c →` renderer virtual+518 `cf2640 → f20c28`. No selective renderer dispatch, new graphics service or PC skip is introduced. The updater is never called by Python. `cf2640` receives native effective E in W1, then overwrites X1 with the updater address before its tail branch; the raw X1 in `f20c28` must not be interpreted as E. The TrackLayer frame stamp limits each active renderer to one CPU refresh per Director frame despite multiple camera visits.

The CLI asserts native position/quad writes at E1000/1300/1499/1500 before judgment. Native lane4 produces renderer X212/Y4; the separate input-plane center212.5 is projected through the real primary camera. Original JNI DOWN42/UP42 accepts one PURE/shining unit, score10000001/H80.19999694824219, and cleans contacts. At E1501 the processed tap leaves the active vector; its retained renderer stays visible with its last placement and no further refresh/visit. Chart depth can continue changing independently.

The fresh no-input case proves that depth308 at E1538 and809 at E1600 do not hide an unresolved tap. Strict expiry records LOST1 at E1601; the same frame's original processed predicate returns1 at depth817 and native visibility setter writes0 once. E1602 removes the logic from active processing without another miss or refresh. Both renderer objects remain in their TrackLayer collections, with reciprocal links and no observed detach/destructor. Neither removal nor visibility is described as reclamation.

JSON contains construction/caller identities, frame/depth/position/quad/opacity snapshots, original write PCs, processed-predicate results, native call counts, JNI projection, cleanup assertions and declared boundaries. Unexpected failures preserve partial observations and return exit1. Existing allocator/autorelease, GL imports, framebuffer/swap and platform/audio/resource boundaries remain; no GPU pixels or complete reclamation are claimed. G-006/G-007 expected-failure diagnostics and all earlier scenarios are unchanged. Stop at E1602, before this chart's completion/results.
