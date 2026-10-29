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

## Expedition 033 flick producer gate

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario flick_producer \
  --output /path/to/flick-producer-result.json
```

**Expected outcome: exit1, JSON `status: fail`, `NativeFlickProducerUnresolved`. This is a blocked research diagnostic, not a green flick gameplay test.** `fixtures/native_flick_probe.aff` contains a timing event, `flick(1500,0.00,0.50,1.00,0.00);` and a control tap1500/raw3. All four flick arguments remain float tokens. Original ordinary solo entry, whole-AFF lexer/parser, chart initialization, native GameScene loading and Director activation execute. Inline parser allocation/stores produce the parsed FlickNote at vtable1b653c0 with time1500/floats[0,.5,1,0]/group0.

`src/flick_producer.py` records the entire builder's relevant cast sites. The parsed flick fails SimpleNote/CameraControl/SceneControl/HoldNote/ArcNote checks and takes `1864628→1863d60`, without changing runtime-vector size. The tap is built normally; native N1/end1620/index/renderer/listener remain coherent. Subsequent native bar generation adds503 LogicBars without adding a flick. Those auxiliary objects are distinguished from scoring units and the builder's immediate products.

The bounded static survey uses the existing pyelftools dependency: known LogicFlickNote typeinfo1a89ca0, relative/data references, short ADRP/LDR GOT references, dynamic symbols and direct gesture-helper callers. Its single relocation reference is GOT1b964d0. No concrete LogicFlickNote vtable or constructor is identified. Six recognized GOT-load sites are existing-object consumers. One allocation candidate is disconfirmed: `ae6e38` allocates RenderFlickNote, vtable1b7b680/initializer1315a90, whose native1315ae4 stores the supplied existing logic pointer. It does not construct that logic. Native checks in the ordinary run reject the candidate for the503 bars and one control tap; the flick renderer initializer is not called.

The scenario stops at the producer gate. No alternative mode/catalog is invented; no JNI DOWN/MOVE/UP, flick predicate, acceptance, score or expiry experiment is performed. An entry into the general continuous-input routine during activation does not demonstrate its flick branch. The earlier native-isolated displacement/angle tests remain separate evidence. General indirect construction, other versions/modes and absent installed resources remain unknown; the survey does not prove universal impossibility.

JSON preserves partial observations on unexpected failure and includes parsed allocation/field-write PCs, builder cast/results/edge/vector sizes, native digest, scene/chart/tap relationships, candidate classifications, original entry counts, endpoint and declared boundaries. Standard ABI/RTTI, platform/resource/catalog/profile/settings/clock/audio/graphics services and all inherited PC skips remain unchanged. Base traversal retains its existing boundary here; `cpu_note` still restores traversal only within its own scenario. The new fixture and diagnostic neither alter G-006/G-007 nor weaken existing successful scenarios. Dependencies remain Python3.12/Unicorn2.1.4/pyelftools0.33. Generated JSON, binaries, archive resources and databases are external outputs, not publication files.

## Expedition 034 continuous-gauge producer gates

```bash
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario continuous_gauge \
  --output /path/to/continuous-gauge-result.json
```

**Expected outcome: exit1 / JSON `status: fail` / `NativeContinuousGaugeProducerBlocked`.** This is a producer diagnostic, not a passing Tempest or Insight gameplay regression. It reuses the unchanged ordinary two-tap fixture. `ordinary_control` executes original solo entry/loading/ScoreState/LifeBarState factories, Director frames and one camera-derived JNI DOWN/UP. Native mode0 gets PURE1, score5000001/H40.20000076293945 at E1001. Original mode0 temporal wrapper/update entries are observed; neither special branch or `expf` executes. Gauge initialization and field-write PCs distinguish external allocator zeroing from native bulk/default zero stores and later judgment/time writes.

`mode6_producer` and `mode11_producer` each inspect a **fresh** unchanged fixture and archived character35/98 metadata. Neither phase attempts target selection: account+18 contains no owned-character objects, fallback+68 is null, and selected character49 is a supplied shell with null vtable/ability. The original `96b358` update path first locates an existing character by ID or fallback, then consumes enriched `frag/prog/overdrive/level/exp` records; the archive's base/max-stat catalog is not that input. Its missing-owner skip is instruction-backed, not a claimed executed rejection of either target. No account row, unlock, level, ability pointer or special mode is supplied to get past this gate.

Both metadata records retain `is_available:false`. That byte is not equated to an executed entitlement/activation verdict; archived character49 is also false. Original skill branches, concrete ability vtables, base activation checks and selector constants are documented as **instruction-backed/unexecuted**: Tempest35/gauge_tempest→ca5ec8/vtable1ac18f0/selector179727c(6); Insight98/skill_insight_konzetsu→af8734/vtable1b5a168/selector1003b90(11). The actual solo selector call is virtual+58 at ee264c. Address13b5c2c instead constructs SpecialSceneArcahvChallenge; it is not called as a gauge selector.

Tempest gauge p is deliberately zeroed by the common native factory at12c5144 before the initializer reads it. This was observed for mode0 and is instruction-backed for a hypothetical mode6 allocation; it does not establish a valid Tempest session or exclude later writers. Optional character-record `prog_tempest` is separately subtracted from `prog` by96b780; equivalence to gauge p is unverified. Insight initialization conditionally reads context mode/difficulty/profile relief and, only for a particular context mode6, timing-window data. That context-mode namespace is distinct from gauge ID6. Ordinary context+38 is0, so the extra profile lookup would be skipped; the mode11 initializer branch itself is not executed. Do not describe an unconditional World-state dependency.

JSON keeps ordinary native construction/field/time/JNI evidence separate from fresh producer-phase boundary reads, archived metadata and instruction-backed contracts. Special activation, selection results, gauge objects, parameters, temporal evolution and failure/completion are `null` or `not_run`; overall success is not fabricated. Existing ABI/platform/account/catalog/profile/settings/resource/clock/graphics/audio/allocator boundaries and all nine PC skips remain unchanged. No special callback, recorder, H/F/p/cap write or direct ability constructor is used. Existing fixtures/assertions/dependencies and the camera_reset/track_fade/flick_producer diagnostics remain intact; generated reports/resources/databases are excluded from source publication.


## Expedition 030-R: external Designant material/provenance diagnostic

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario camera_designant \
  --designant-materials /path/to/designant-materials \
  --output /path/outside/research_harness/camera-designant-result.json
```

The external directory contains the supplied original `0.aff`, `1.aff`, `2.aff`,
`3.aff` and `base.ogg`, with unchanged filenames/bytes. They are not distributed
with this package. The scenario inventories their hashes/formats and camera
records, reads the archived Designant catalog, and executes an unchanged
`sayonarahatsukoi` ordinary entry/loading/Director control. The configured AFF
remains `ordinary_two_tap.aff` for that explicitly separate native control.

**Expected result: exit 1**, `status: fail`,
`NativeDesignantSelectionProvenanceUnavailable`. Gate A stops before native
Designant selection: the current adapter has no produced purchased-Song
descriptor or justified ownership/unlock input for `purchase: lephon`. The
observed purchase count in the supplied local-state storage is zero. The diagnostic does not manufacture
these inputs or rename the ordinary Song. This is a bounded source-state
blocker, not an executed rejection of Designant or proof of a universal access
rule. No missing-packlist requirement is established.

Supplied charts are inspected lexically only; native parsing/digest/construction
of them, camera overlap/reset and target JNI projection are `not_run`. Both the
original `camera_reset` diagnostic and all earlier fixtures/assertions remain
unchanged. No new runtime dependency, service substitution or PC skip is added.


## Expedition 035: JNI late-input versus frame expiry

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario late_input_expiry \
  --output /path/outside/research_harness/late-input-expiry-result.json
```

`fixtures/native_late_input_expiry.aff` is synthetic: two same-lane taps at
1000/1109, timing120. Two fresh ordinary solo-created GameScenes independently
establish native E1000 with both notes admitted, enabled and unresolved.
Native camera projection derives the same JNI input point in both cases.

The input_first case advances only the external clock to comparison time,
delivers original JNI DOWN/UP, then runs an original Director frame at the same
E1110. The frame_first case runs that frame before DOWN/UP. No timeline field,
active vector, candidate list, guard, score or gauge state is assigned.

The observed result is different: input_first records one LOST on the older
note and consumes iteration without a successful hit (score0/H0/combo0).
Frame_first expires the older note, then the initial classifier rejects its
missed guard and accepts the newer note as shining PURE
(score5000001/H40.20000076293945/combo1, PURE1/LOST1). Both candidate vectors
include both notes; input consumption is distinct from the successful-hit byte.
Both contacts clean up. There is no completion/result snapshot in this scenario.

The scenario does not assert the historical result before observation. It
checks native construction/index/ownership, equivalent preconditions and
projection, JNI/Director provenance, classifier returns, recorder-derived
counter changes, native guard writes and cleanup, and reports whether outcomes
differ. Read-only hooks retain before/after-sort candidates, missed/consumed
guards, caller branch/stop, note/contact identities, recorder caller PCs,
score/combo/health snapshots and writes. Exceptions preserve partial evidence
and fail. `status: pass` means the comparison and its provenance gates pass;
it is not a hardware Android input-queue timing claim. No new service, runtime
dependency or gameplay skip is introduced. Existing boundaries remain declared
in the JSON; outputs must remain outside this package.


## Expedition 036: native noinput semantics

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario noinput_semantics \
  --output /path/outside/research_harness/noinput-result.json
```

Two independent fresh ordinary solo-created GameScenes load
`native_noinput_control.aff` and `native_noinput_group.aff`, differing only by
the timing-group attribute. Original parsing, flag stores, chart count/end,
index/admission, JNI input, expiry and completion/snapshot remain enabled.

Observed: both create two runtime taps, two timing groups and the same native
index memberships. The parser clears the grouped parsed tap's flag; original
builder18640f4 stores logic+54=0. Native counting excludes it (N2 versus N1).
The disabled object is still indexed and active. Its JNI DOWN produces a native
Touch but no candidate/classifier/recorder; the ordinary tap still judges.
It remains unmissed/unconsumed through expiry checks and native completion.
Native chart end remains1620, completion occurs atE1621, and native snapshots
have PURE2/LOST0 versus PURE1/LOST0. Scores are10000002 versus10000001; live
health80.4000015258789 versus80.19999694824219, result health80/clear3 for both.
Clear3 is read through the original result classifier on the native cache;
this scenario does not run the results scene or save.

Per-note end-loop observations show the disabled tap skipped before its end
time is consumed. The unchanged maximum is therefore not the sole evidence
for end-time filtering. Both group1 lifetime fields still become2700 through
the separate native descriptor pass. No optional later-note pair is needed
for this scoped branch result; no later-note execution is claimed.

JSON preserves native parser/comparison/store PCs, identities, count inputs
and return, object counts before/after bars, timing/descriptor/index data,
active state, original JNI mapping/projection/candidates, recorder deltas,
expiry flag predicates, completion/cache provenance and result reconciliation.
Outcome values are observed rather than supplied as host gameplay rules.
Failure retains partial evidence; the second case stays not_run if the first
cannot complete. Read-only original score/classification getters inspect the
completion-produced cache. Existing services and all inherited PC skips stay
unchanged; dependency pins and prior scenarios/assertions/fixtures are intact.

## Expedition 037: mixed hold/tap arbitration and contact continuity

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario mixed_hold_tap \
  --output /path/outside/research_harness/mixed-hold-tap-result.json
```

Three independent fresh ordinary native-created GameScenes run two synthetic
fixtures. `native_mixed_hold_tap_hold_first.aff` combines hold1000..2000/raw3
with tap1250/raw3; `native_mixed_hold_tap_tap_first.aff` changes the tap to950.
Cases are `hold_unlatched` (first DOWN atE1250), `hold_latched` (DOWN atE1000,
native activation/checkpoint, second DOWN atE1250) and `tap_first` (two DOWNs
at unchangedE1000 before another frame). These are different contact histories
and, for the comparator, different tap times—not identical-precondition trials.

Original AFF/runtime construction produces both notes, native lane4, checkpoints
1250/1500/1750 of weight1, N4/end2500 and original index/admission. Native
camera projection derives the shared contact point. Both mixed candidates are
observed before/after original chronological sorting. In both hold-first cases,
the hold latch branch stops initial iteration before tap classification, even
when latch1 is already set. The unplayed tap later expires natively. In tap-first,
the first contact judges the earlier tap as ID1/PURE at+50; the second reads its
consumed guard, continues and latches the hold. Equal-key stability is untested.

Original continuous processing accepts both retained same-lane Touches. After
one is released, the other sustains activity: second contact43 in hold_latched;
original tap-judging contact42 after the latching contact43 is removed in
tap_first. This is not an exclusive hold-owner model. Native frame reset and
activation writes are observed separately from the initial latch.

Each checkpoint resolves once through original recorder calls. Observed final
PURE/FAR/LOST is3/0/1, score7500003/H58.60000228881836 in both hold-first
histories, versus4/0/0 (shining3), score10000003/H80.80000305175781 in tap-first.
All UPs remove native mappings/slots/mask/retention without scoring; the next
Director frame clears activity while latch1 remains. StopE1627, before chart
completion/results/SQLite. JSON contains construction/fixture hashes, original
call/store provenance, mixed candidate vectors, per-contact identities,
checkpoint guards, recorder deltas, score/gauge writes and cleanup. Causal
identity assertions accompany the observed output; no host score equation or
gameplay-state repair is used. Failures preserve partial cases/not_run stages.
All established external services, PC skips and dependency pins remain unchanged.
