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
