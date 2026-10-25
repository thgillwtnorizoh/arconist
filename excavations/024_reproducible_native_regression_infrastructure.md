# Expedition 024 — Reproducible Native Regression Infrastructure

## Result

**Strong success. Phase C achieved: the complete ordinary offline solo regression passes from a clean source copy and fresh Python environment.** The reusable package is published under `research_harness/`; it uses the external original ZIP, not saved emulator memory or scripts from earlier Work sessions. Native execution, automatic assertions and the generated JSON reproduce Expedition023's full solo-entry-to-results/SQLite session.

This is an engineering preservation of the existing experiment. No new gameplay, menu, graphics or account behavior was investigated. No major new native blocker was encountered. Implementation stopped after clean validation; publication verification is separate from exploratory work.

## What I Found

### Preparation and source availability gate

The supplied introduction, current GitHub context and complete023 report were read; only required018–022 adapter evidence was consulted. Starting main was `91001779c427f1929d1a1775407f4c8d2e2ec2b8`, tree `4f7124cfd804b085130a19e50739fb126102f457`; no024 or `research_harness` package was present. Available local adapter source was inventoried before implementation. No live emulator instance was assumed available.

**All essential Python/Unicorn adapter source was recoverable.** There are no missing modules and no report-based substitute for an unavailable implementation. The working dependency chain covers recover.py, exp010.py, exp013–022.py, and the019/021/023 drivers. Only the relevant class implementations, fixture helpers and exercised lifecycle portions are retained. Earlier standalone diagnostic experiments, manually assembled scene setup and manual ending hierarchy/binding helpers were removed.

The supplied ZIP's `lib/arm64-v8a/libcocos2dcpp.so` matches SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` and the prior extracted execution copy byte-for-byte. The new package instead reads the verified ELF into an in-memory stream directly from the external ZIP; no extracted `.so` is a package dependency.

### Recovery and classification inventory

The package README contains the per-module inventory and original-source mapping. Summary:

| Published module(s) | Classification | Responsibility |
|---|---|---|
| `src/arm64.py` | Existing recovered source, consolidated | ARM64 CPU/memory/register/call environment, ELF PT_LOAD and relative relocations; added host-entry observation and external stream input |
| `src/chart_services.py` | Existing recovered source | C++ strings/streams/numbers, AFF boundary and metadata helper |
| `src/sqlite_services.py` | Existing recovered source | Bundled native SQLite API forwarding, private DB/schema/query support, libc services |
| `src/results_services.py`, `action_services.py`, `transition_services.py`, `ending_services.py` | Existing recovered source, pruned | Results UI/gate boundary, panel proxies, action/timer/animation observation and services |
| `src/bootstrap.py` | Existing recovered source | Original Director/GLView startup, app/settings/catalog/JNI clocks and native chart bootstrap |
| `src/resources.py` | Existing recovered source | Symbol relocations, resource-provider, original CPU CSB/font/RTTI/texture support, GL and runtime services |
| `src/track_services.py` | Existing recovered source | Locale ABI, GPU capability/pixel-format services and original TrackLayer CPU support |
| `src/menu_services.py`, `solo_entry.py` | Existing recovered source | Native menu/selection/ordinary entry and checked strings; controlled offline fixture |
| `src/lifecycle.py` | Consolidated existing driver source | Explicit loading/frame/ending/results schedules; replaces runtime extraction/exec of scratch scripts |
| `src/regression.py` | Consolidated023 plus new assertions | Whole-session scenario and automatic identity/count/result/save/lifecycle verification |
| `run.py`, `config.py`, `boundaries.py`, tests/dependencies/docs | Newly implemented support | CLI, archive verification, configurable small JSON output, boundary declaration and negative tests |
| Original ZIP resources, catalog/profile/settings/platform/ABI responses | External resource / intentionally supplied services | Same scientific boundaries as023; not full native Android startup |
| Unavailable implementation | None | No reconstruction from missing executable state required |

There are22 published package files,106,691 source/documentation bytes. Class names retain provenance while module names describe responsibilities. Necessary service implementations are preserved rather than removed to inflate native coverage. Some inherited compatibility definitions remain unentered; explicit regression checks prohibit direct host entry into critical handoffs.

### Package and execution interface

The package includes one CLI, pinned dependencies, a synthetic AFF fixture, private source modules, a README and standard-library tests. Its own `.gitignore` excludes Python caches/environments/default generated results. No root configuration or workflow is changed.

Validated interpreter: **CPython3.12.14, Linux x86_64**. Fresh environment installs only the documented third-party runtime dependencies:

```text
pyelftools==0.33
unicorn==2.1.4
```

These are actual tested versions. Capstone is unnecessary for runtime reproduction and is not required. The documented setup/run commands are:

```bash
python3.12 -m venv /path/to/venv
/path/to/venv/bin/python -m pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip \
  --output /path/to/regression-result.json
```

Source/fixture paths resolve relative to the package; the caller may use another working directory. `--verbose` sends inherited diagnostic prints to stderr. Default output is `regression-result.json` in the caller's current directory; output inside the source package or overwriting the input archive is rejected. Python `-O` is rejected because this package requires assertions. Exit0 means pass,1 means input/native/assertion failure,2 means report output failed.

The configured ZIP is read-only. Its target binary hash is checked before execution adapters are imported/initialized. Native resources are read unchanged from that ZIP. The synthetic chart remains `fixtures/ordinary_two_tap.aff`, not the archived chart for the selected song. The catalog fixture, selection, speed40, mode0, empty purchase/null map/modifier and40 zero PlayParameters match022–023. Original registry initializer `0x1054f24` and ordinary `0xee197c` still execute.

### Automatic native assertions

The runner separates the recovered execution services, lifecycle schedule, assertions and CLI/output handling. It does not load source through runtime `exec`, import old audit modules or consume generated JSON from an earlier experiment. New assertions inspect real native observations and relational identities; expected values are never written into game results.

The complete run checks:

1. One `0xee197c`; native eligibility1 at `0xee2214`; latch1; original allocation/constructor sites `0xee29a8/0xee29e8`; constructor LR=`0xee29ec`; zero multiplayer-helper entries.
2. One native GameScene initializer, return1 and activation of the same scene; Director/scene-visitation model execution. A new host-call observation list confirms no direct driver calls to GameScene constructor/initializer/model-frame, ending/shutter callbacks, GameSession or writers.
3. Two original JNI DOWN/UP pairs, original gameplay listener/initial input/tap judgment entries, two PUREs and the reference result/health/classification.
4. One native completion/snapshot, cached result,24 ActionTimeline tracks/85 frames, observed frame49 before continuation and frame50 with exactly one continuation.
5. Native GameSession/results construction; unchanged scene/model and `ScoreState+0x68 == GameSession+0x18`. Heap pointers are recorded as emulated observations, not hardcoded expected constants.
6. Original save-gate checkpoints, original result initializer/helper and each persistence writer once, plus native SQLite API execution/readback.
7. Expected single score/clear rows; final native results-scene type, running identity, pending0 and enabled dispatcher. Existing extra-update checks prove rows and callback/save counts remain unchanged.

Across the full session `0x963094` and `0x113af20` each execute twice, once for gameplay loading and once for results; results initialization, continuation and writers execute once. No game-stage callback is directly delivered by the host.

### Observed clean-run results

| Check | Observation |
|---|---|
| Overall JSON status | `pass` |
| PURE / FAR / LOST | 2 /0 /0 |
| Score | 10,000,002 |
| Live health | 80.4000015258789, verified with absolute tolerance1e−6 |
| Integer result health / clear | 80 /3 |
| Identity checks | Same native GameScene/model; original constructor caller; cached result equals retained session result; no direct host handoffs |
| Final scene | RTTI `21NormalGameResultScene`; running is native result scene |
| Final pending / dispatcher | 0 /enabled |
| Saved rows | One score row and one clear-type row |
| Extra updates | No repeated saving; exact row equality preserved |
| Native failures | Empty |

Score row: id1, version1, songId=`sayonarahatsukoi`, songDifficulty0, score10000002, shinyPerfectCount2, perfectCount2, nearCount0, missCount0, date1700000000, modifier0, health80, ct0. Clear row: id1, same song/difficulty/ct, clearType3. Calendar time is supplied; SQLite saving is original ARM64 execution against the private in-memory database.

The generated report is4052 bytes in this validation. It contains binary SHA, fixture ID, original entry and key counts, relational identity checks and observed emulated pointers, result values, native SQLite API counts/rows, final Director state, gate observations, remaining ELF PC skips and failure information. It does not embed full traces, memory, native code or original resources. Failed input/native/assertion execution emits fail status and error type/message/location, never scripted success.

### Clean-environment validation and negative tests

A development package run first passed the native regression. Then only the22 reviewable package files were copied to a clean directory, excluding caches; no `audit`, previous experiment outputs, extracted library, snapshot or original resource file was copied. A new isolated Python environment was created and installed only the pinned requirements. `PYTHONPATH` was unset. The runner received the original ZIP externally and passed the complete automatic regression in a separate process.

Every clean-copy source/documentation file was compared byte-for-byte against the publication candidate. The published tree is built from exactly those reviewed bytes. Publication verification additionally retrieves the committed package for a fresh process run from another working directory when feasible; the exact outcome is stated in the final handoff, not inferred from the development test.

Standard-library unittest results: **3 tests passed**:

- Missing archive: nonzero exit and explicit `Archive not found` failure JSON, before native execution.
- Wrong binary: a ZIP with a deliberately incorrect library payload fails SHA validation, before execution.
- Unavailable-song native control: original ordinary eligibility returns0, latch0, no GameScene and pending0. Its JSON explicitly labels the negative test and `game_scene_constructed: false`; it is not presented as a full-session success.

Commands are documented in the package README. `ARCONIST_TEST_ARCHIVE` enables the native negative unittest; without it only the fast input tests execute. No new gameplay or graphics scenario was introduced. No new native blocker was investigated.

### Preserved execution boundaries

All following PCs are original unrelocated ELF addresses, distinct from allocated emulated object pointers:

| Source → resumed PC | Boundary |
|---|---|
| `0xf72110 → 0xf72158` | Platform GLView attachment |
| `0x16a4238 → 0x16a48d8` | Shutter panel resource construction replaced by native Node proxies |
| `0x121581c → 0x121584c` | Loading overlay |
| `0xa507c4 → 0xa519ec` | Information artwork prefix; supplied native visual target |
| `0xa51adc → 0xa5213c` | Remaining information artwork/actions/canary after native callback registration |
| `0x196fdac → 0x196ffac` | Information child closing visuals |
| `0x891190 → 0x89164c` | Results prefix UI; X28 application global/X26 scratch restored; native gate producer retained |
| `0x891688 → 0x89219c` | Middle results UI; native save decision retained |
| `0x8921dc → 0x8928e0` | Post-save UI/progression |

The package preserves native eligibility, GameScene/TrackLayer construction and CPU updates, archived GameEnd CPU construction/binding, gameplay judgments/result creation, scheduling/action callbacks, original save gate and SQLite writers. Whole-function base rendering/traversal/flush `0x129c924`, `0x1017a84`, `0x13edf0c` remain inert; TrackLayer update `0x19069a0` remains original.

Supplied services remain: catalog/settings/profile/account/application data, raw resource access, finite placeholder textures/capability, panel/information Node proxies, JNI/platform/GPU/audio, allocator/autorelease/free, libc/C++ strings/streams/numbers/formatting/RTTI, locale/math/clocks/TLS/locks and bounded null references. Pending submission worker `0x1246c98` is inert. Non-null native Ref operations execute; defined FreeType and SQLite APIs forward into the ELF. The package README and source inventory identify these implementations. None is described as native Android authorization, full GPU/audio, production catalog startup, complete reclamation or production save compatibility.

### Publication scope and exclusions

This expedition's explicit Phase C exception authorizes `research_harness/**` in addition to the024 report and append-only context. It is not treated as a permanent change to project policy.

Reviewed publication files contain only research Python source, dependency declarations, documentation, tests and synthetic AFF data. No original archive, `.so`, CSB, font, artwork/audio, native memory snapshot, database, virtual environment, generated output/cache, account credential/key/token or personal save is committed. Runtime uses no ChatGPT-specific functions or external network service. Requirements installation may need normal package access.

No missing source/dependency blocks reproduction. Further menu/UI/platform/online fidelity and return-navigation remain outside scope; no025 is initiated.

## Pseudocode

```text
CLI accepts external ZIP and external output location
  → verify required ARM64 member SHA-256 before native execution
  → read ELF through memory stream; resources remain external ZIP inputs
  → load recovered scoped runtime/ABI/platform/catalog adapters
  → execute original registries and native menu/selection preparation
  → enter original ordinary solo startGameScene
  → native eligibility/latch/allocation/GameScene construction
  → original loading actions → initializer1 → Director activation
  → Director/Scheduler/scene visit → original model frames
  → supplied JNI values → native judgment/completion/cached GameResult
  → archived GameEnd + original native frame50 continuation
  → original GameSession/results/shutter/gate/SQLite chain
  → native final Director results activation
  → bounded extra updates and native database readback
  → assert counts, values, relational identities and native boundaries
  → emit small pass JSON; on failure emit fail JSON and nonzero exit

Supplied: external bytes, ABI/platform services, catalog/profile/settings,
          clocks/JNI inputs, placeholder textures and declared UI PC skips
Original: all tested application handoff decisions and result/save computation
```

## GitHub Status

Publication parent: `91001779c427f1929d1a1775407f4c8d2e2ec2b8`. Authorized changes are22 package files, this new024 report and an append-only024 context entry. Committed report/context readback, exact historical prefix and tree preservation are verified after publication and reported with the pinned SHA. Reports001–023, root README, instructions and unrelated paths remain unchanged. Generated validation JSON is deliberately not a publication file.
