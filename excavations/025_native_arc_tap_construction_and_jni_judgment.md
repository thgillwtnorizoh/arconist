# Expedition 025 — Native Arc-Tap Construction & JNI Judgment Integration

## Result

**Strong success.** Original whole-chart parsing/building creates a trace arc and its embedded arc-tap inside an ordinary native-created GameScene. Original code installs the parent/child relationship and produces geometry. JNI input accepts that same child once. A fresh-ID contact at the same effective time passes spatial eligibility, reaches the same classifier and reads the native consumed guard, without another acceptance or score change.

A separate reproducible `--scenario arc_tap` passes; the default two-tap regression remains green through results/SQLite/final activation. The arc-tap test stops after duplicate contact cleanup, before gameplay completion/results. G-001 is Verified in the new ten-item research backlog; other items retain their queued/research-gated states. No026 is initiated.

## What I Found

### Preparation and scientific scope

The introduction, supplied native executable, current GitHub context, relevant002–004/008–011/020/023–024 evidence and Scout001 findings were reviewed. Actual published024 harness source is reused. Parent main was `5eb900ddd4d6d5307526e978a147fc362c2acf23`, tree `fb0d7944cd88230397bc8e6f29961d927a8d5d14`; no025 or backlog existed. The supplied `lib/arm64-v8a/libcocos2dcpp.so` hashes to `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`. Original archive/resources/executable remain unchanged.

Native-integrated means original ARM64 routines execute together across the described handoff. Native-isolated means original routines with supplied surroundings/callers. Instruction-backed denotes decoded but unexecuted connections. Scout001's builder locations were static leads, not a previous successful construction experiment. All PCs below are unrelocated ELF VAs; pointer samples are allocation-dependent emulated observations, never required constants.

### Minimal AFF and grammar gate

New `research_harness/fixtures/native_arc_tap.aff`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
arc(1000,2000,0.50,0.50,s,0.50,0.50,0,none,true)[arctap(1500)];
```

Float tokens are preserved for positions/heights/BPM/beats; times/color are integers. Original parser `0xc2cb1c` and data initializer `0x924b50` execute once. At builder callsite `0x1864e18`, read-only observation of the parsed ArcNote finds mode1, endpoints(.5,.5,.5,.5), exactly one embedded time1500 and child factory time argument1500. Here TRUE is the arc's trace-style mode1; the overall game mode remains ordinary0. No parsed objects are injected.

The original resource chain chooses `songs/sayonarahatsukoi/0.aff`; external chart bytes come from the selected synthetic fixture. Metadata/profile/settings/resource/clock interfaces remain controlled as in022–024. This is not the archived song's original chart.

### Native construction gates A1 and B

The uninterrupted scenario enters original ordinary `0xee197c`, which passes eligibility and allocates/constructs GameScene through the established solo caller. Native loading actions invoke `0xe2ea48`, whose real caller receives return1. Its chart loader executes `0x173b358 → 0x1862a14`; observed parser, initializer, builder, child factory, parent factory, count producer and geometry producer each enter once.

| Native operation | New execution evidence |
|---|---|
| Child call `0x1864e18 → 0x173a778` | Original child factory returns at `0x1864e1c`; RTTI `15LogicArcTapNote`, vtable `0x1acac18`, initial Ref1 |
| Parent factory `0x178f7fc` | Original LogicArcNote product is in the native chart main vector; vtable `0x1b91500`, mode1 |
| Parent child vector | Native parent+0x120 contains exactly the factory-returned child |
| Child parent link | Memory-write observation proves original `0x1865514` stores that parent into child+0x90 |
| Child geometry | Original `0x1925084` executes; stores at `0x1925888`/`0x192588c` populate child+0x80/+0x88 |
| Child timing/group | Native child start1500 equals parsed time/factory argument; child and parent timing-group fields agree at0 |
| Count/lifetime | Original `0x11ea120` produces N1; chart end2500;505 main objects including the parent and auxiliary objects |
| Scene ownership | Scene+0x3e0 points to this model; Scene+0x3e8 equals model+0x28 chart; native child link remains unchanged after input |

**Branch clarification:** Scout001's `0x1865204–0x1865210` parent-link loop exists, but this fixture takes the other ordinary construction branch and stores at **`0x1865514`**. The test asserts the actually executed store. It does not silently substitute the Scout address or claim both branches executed.

Authoritative emulated identity samples:

| Object | Pointer |
|---|---|
| GameScene | `0x4326ec0` |
| GameModel / LogicChart | `0x4355cc0` / `0x43310c0` |
| Arc parent | `0x4331c40` |
| Factory-produced child | `0x4331980` |
| Child+0x90 | `0x4331c40`, identical parent |

The child's observed Ref is3 at the endpoint; native vector/reference operations execute while allocator/autorelease/reclamation boundaries remain inherited. This is not a complete destruction proof. No driver sets a vtable, child-vector member, back-link, child geometry, activation/consumption byte or judgment denominator.

### Narrow construction-service dependency

The first diagnostic passes parsed child creation but encounters unsupported libc calls in resource loading. One bounded resource-reader ABI dependency was investigated; no renderer subsystem was reconstructed. The native CPU path consumes archived `models/tap_l.obj` and `models/tap_l.mtl`. The following imports surfaced incrementally and are installed before entry in the complete reproducible run:

| Supplied libc interface | Representative native return/caller | Scenario calls |
|---|---|---:|
| strspn | `0x10084a8` |174|
| sscanf | `0x1009570` |4|
| strcspn | `0x18d9644` |176|
| double pow | `0x18d975c` |430|
| double ldexp | `0x18d96dc` |66|
| strchr | `0xa61da4` |1|
| __vsprintf_chk | `0x16ac09c` |2|

These are host ABI services, not original Bionic execution. The original mesh parser, constructors, geometry sampler and ownership logic remain native. No new PC skip or graphics-object proxy was added.

The scanner maps emulated output pointers to bounded host buffers, invokes Linux libc through standard-library ctypes, and copies only successful output conversions back. It permits only simple `%f`/`%d`/`%s`, whitespace/slash formats, at most six output arguments and input shorter than256 bytes; other requests fail. This fixture actually uses only `%s`. pow/ldexp use double register contracts and host math; checked formatting reuses the existing AArch64 va_list formatter and checks its destination bound. Complete scanf/Bionic error semantics, floating overflow compatibility and malformed OBJ behavior are outside this finite fixture.

Fault-at-import diagnostic traces are not spliced into the successful run. The CLI scenario begins with all required services installed and runs from a fresh emulator. Dependency versions remain Python3.12, Unicorn2.1.4 and pyelftools0.33; no new third-party runtime package is added. Capstone was used only for targeted instruction inspection.

### Native geometry, projection and input timing

Original sampler output in this controlled environment is `(0,50,-4044.5)` in child+0x80. Its exact native stores are observed; no claim of original-device rendering fidelity or the earlier prepared geometry is made.

The ordinary initial arc-tap consumer reads geometry XY and adds quantized parent-start X. Chart+0x110 is0, so it intersects the input ray with Z=0. Thus the test constructs a separate external projection-input point `(0,50,0)`; it does **not** overwrite the sampler-local child Z or assume the full sampled vector is the input plane.

Original camera projection `0xbdbb70` runs on the native model's CameraController camera. Output Y-up is converted using native Director height720 to the design-coordinate input. Resulting JNI contact is:

```text
X = 640.0
Y = 593.0632781982422
```

These are newly derived coordinates, not008's prepared-child coordinates or024's lane-tap coordinates. Original input unprojection returns approximately `(0,50.017578125,0)` before the spatial helper's own clamp/comparisons; native target XY is `(0,50)`.

Director-driven schedule: activation at wall6450, preroll at6451/E−2999, native music anchor at9452/E0, original model visit at10952/E1500. The input wall is computed from observed effective time and native child time. No direct host model-frame or timeline-field write replaces visitation.

### Positive JNI judgment and duplicate control

At E1500, fresh Android pointer42 enters `0xbe31a8`, original GLView/EventDispatcher/gameplay listener `0x194ff80`, initial input `0xeec024`, parent-child traversal, spatial call `0xeec47c → 0x927384`, classifier `0x160ce28`, recorder `0x1730290` and child acceptance `0xc78814`. Both classifier and acceptance receive the exact factory-returned child. JNI UP `0xdda71c` cleans up the retained contact and engine mask.

Without advancing wall or chart time, pointer43 repeats the same DOWN/UP at the same coordinates. It traverses the same parent, passes native spatial eligibility again, and reaches the same child's classifier. A read-only memory observation records original `0x180cf28` reading child+0x0d as1 during the duplicate phase. There is no second `0xc78814` or recorder entry.

| State | Before hit | After first hit | After duplicate |
|---|---:|---:|---:|
| Native score |0|10,000,001|10,000,001|
| Shining / PURE |0 /0|1 /1|1 /1|
| FAR / recorded LOST |0 /0|0 /0|0 /0|
| Live health |0|80.19999694824219|80.19999694824219|
| Child consumed byte |0|1|1|

N1 is obtained from the native chart before deriving the all-PURE score expectation. The test does not assume008's denominator or assign counters/health.

Counts: JNI DOWN2, UP2, gameplay begin2, initial input2, spatial checks2 (both true), classifier2 (same child), acceptance1, recorder1. Each event uses a fresh Android pointer ID; duplicate suppression is not duplicate-ID filtering or an out-of-window rejection. Both UPs leave retained contacts empty and engine mask0.

The test stops immediately after this control. Completion handler count is0 and ScoreState+0x68 remains null. No GameResult, ending/results/SQLite assertion is claimed for this arc-tap chart.

### Harness extension and validation

Minimal changes:

- Add `fixtures/native_arc_tap.aff`, `src/arc_tap.py`, `src/arc_tap_services.py` and an optional native unittest.
- Add scenario selection to config/CLI; the default remains ordinary.
- Append scenario documentation to the harness README.
- Leave the two-tap fixture, `src/regression.py`, lifecycle driver, old assertions and requirements unchanged.

Command:

```bash
python research_harness/run.py --archive /path/to/arccopy.zip \
  --scenario arc_tap --output /path/to/arc-tap-result.json
```

The new scenario passes with a5048-byte structured report recording parser/builder observations, relational identities, exact geometry/store PCs, projection/spatial checks, recorder changes, duplicate guard, ABI use and declared boundaries. Essential failure raises a failing result; original builder/sampler/judge/recorder addresses are checked against direct host calls and replacement hooks.

The unchanged default command separately passes the entire two-tap session: PURE2/FAR0/LOST0, score10000002, live health80.4000015258789, result health80, clear3, native SQLite and final results activation.

Input/unavailable-song unittest suite:3 executed tests pass; the new opt-in full arc-tap unittest is explicitly skipped in that invocation because the CLI scenario already ran its native assertions. It can be enabled with `ARCONIST_ARC_TAP_TEST_ARCHIVE`; no separate repeated arc-tap experiment is implied by the skip. Both scenario runs report no native failures.

### Remaining supplied services and exact skips

The024 catalog/profile/settings/application, archive-provider, JNI/platform, libc/C++/RTTI/math/locale/clocks/locking, allocator/autorelease/free, texture/capability/GPU/audio and pending-account-worker boundaries remain. New libc services above are scoped to arc_tap only. Original child construction/links/geometry, native spatial/timing decisions and recording remain original.

| Existing source→resume PC | Arc-tap run |
|---|---|
| `0xf72110 → 0xf72158` | Platform GLView attachment boundary exercised |
| `0x16a4238 → 0x16a48d8` | Loading shutter panel proxy boundary exercised |
| `0x121581c → 0x121584c` | Loading overlay omitted |
| `0xa507c4 → 0xa519ec` | Loading information artwork omitted; supplied native target Node |
| `0xa51adc → 0xa5213c` | Remaining information visuals/canary omitted after native callback action registration |
| `0x196fdac → 0x196ffac` | Loading information-child closing visuals omitted |
| `0x891190 → 0x89164c` | Retained results-UI boundary, not reached by arc_tap |
| `0x891688 → 0x89219c` | Retained results-UI boundary, not reached by arc_tap |
| `0x8921dc → 0x8928e0` | Retained post-save boundary, not reached by arc_tap |

Whole-function base traversal/render/flush services `0x129c924`, `0x1017a84`, `0x13edf0c` remain inert; original TrackLayer CPU update `0x19069a0` executes. No drawing/texture fidelity, moving/connected arc behavior, alternative colors or arbitrary chart compatibility is inferred.

### Research backlog and publication

New `research_backlog.md` preserves all ten Scout001 stable IDs/priorities, initial effort, acceptance targets, provenance and decision history. G-001 is **Verified — Expedition025**, limited to this fixture/construction/JNI/duplicate scope. G-002–G-008 remain Queued; G-009/G-010 remain Research-gated. No automatic026 assignment is made.

Only the authorized harness paths, backlog, this report and append-only context are publication changes. Prior reports001–024, historical context, root README, unrelated files and original assets/binaries remain preserved. Generated JSON/logs/environments, proprietary model/texture resources, databases and dumps are excluded. Exact publication SHA, readback and parent-tree preservation checks are returned in the final handoff.

## Pseudocode

```text
SUPPLIED: synthetic AFF bytes; established catalog/platform/ABI/resource services
INSTALL: narrow libc ABI services used by original archived OBJ reader

original ordinary solo entry → original GameScene/loading initializer
  → original AFF parser: trace flag1, one child time1500
  → original runtime builder → child factory173a778
  → original parent factory → parent vector contains child
  → original1865514 stores child.parent
  → original1925084 writes child geometry
  → original chart countN1 / model/index / native camera ownership
  → native loading actions and Director activation

Director/Scheduler/scene visit → native E1500
external input derivation:
  read native geometry XY + native parent-start X relationship
  use ordinary Z=0 input plane; original camera projection + Y conversion
JNI DOWN42 → original dispatch/listener/child traversal
  → spatial true → native classifier/recorder/arc-tap acceptance once
JNI UP42 → original contact cleanup
JNI DOWN43, same E/coordinates → same child/spatial true
  → native consumed-byte guard1 → no second acceptance/record
JNI UP43 → original cleanup

ASSERT relational links, native writes, counts, result deltas and no host bridge
STOP before completion/results/SQLite for this chart
```
