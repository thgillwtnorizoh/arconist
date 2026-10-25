# Expedition 023 — Ordinary Solo Session-to-Results Integration

## Result

**Strong success; Phase B is complete within the declared controlled environment.** One fresh ARM64 execution starts at the original ordinary solo `SongSelectScene::startGameScene`, passes native eligibility, constructs/initializes/activates GameScene, delivers JNI taps, creates the native GameResult, runs the resource-loaded ending and native results transition, saves through bundled SQLite, and activates NormalGameResultScene. The cached GameResult and GameSession result pointers are identical.

No second GameScene, replacement model, fabricated/copied GameResult, manual GameSession, direct animation/shutter callback, driver-assigned save gate, direct writer call or forced final Director pointer bridges the stages. Full Android startup, Play Widget delivery, artwork fidelity and production account/catalog startup remain outside this result.

## What I Found

### Preparation and evidence scope

The project introduction, current GitHub context, complete022 report and relevant017/019/020 integration sections were consulted. Main was `9315b04bf4b6388d6f44f0b6c707d821c7f302fa`, tree `113a248e989f21c6446c7cc1db18eeb7f11fe013`; the recursive tree contained no023 report. Actual available018–022 Python/Unicorn adapters were reused; no previous live emulator was assumed recovered.

The supplied ZIP's `lib/arm64-v8a/libcocos2dcpp.so` SHA-256 is `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, matching the extracted execution copy byte-for-byte. Binaries and archive assets are unchanged. All addresses are original ELF VAs.

**Native-integrated** denotes original ARM64 routines executing together across the stated handoff. **Native-isolated** denotes native routines entered with supplied surroundings. **Instruction-backed** denotes decoded relationships without execution of an enclosing producer. **Interpretation** and **Unknown** do not imply execution. Host ABI/platform adapters are disclosed below; the result is not full Android or GPU emulation.

### Experiment budget and continuity

One diagnostic compatibility pass completed successfully using the022 entry and019–020 ending/results adapters. The only integration bookkeeping adjustment was accounting for the loading shutter before the results shutter: the results request is the second recorded TransitionShutter, and `0x963094` legitimately executes twice across the whole session. No new native material blocker was encountered. Missing local Python dependencies were installed; this was tooling setup, not a native application fix.

A fresh authoritative emulator then repeated the entire chain with read-only observations at `0x891684`, `0x89219c` and `0x8921b8`. It passed independently, followed only by the limited additional Scheduler/Director updates for uniqueness. The authoritative trace is the source of the values below; it is not assembled from separate runs. Temporary adapters/traces/databases are not published.

### Ordinary solo entry reused from022

The external catalog fixture supplies `sayonarahatsukoi`, difficulty0, set `base`, empty purchase, metadata BPM178, null purchase descriptor, the022 availability/restriction fields and controlled local/profile storage. The archived `assets/songs/songlist` justifies that base-song selection; full catalog parsing/installed-chart detection remains external. App mode/context is0, multiplayer active byte0, character49 has no ability, map/modifier are null, speed40, and PlayParameters is an explicit40-byte zero input. Its canonical UI producer remains unknown.

Original registry initializer `0x1054f24` executes before entry. Original menu constructor `0x1754440` and setter `0x14ef098` create coherent native selection state. The driver enters `0xee197c` once; original `0x17c45f4` returns1 at `0xee2214`, `0xee25bc` sets the request latch, `0xee29a8` allocates0x4e0, and `0xee29e8` calls original constructor `0xe4e4dc`, LR=`0xee29ec`. There are zero `0xdd0f90` entries and no ready-up segment invocation.

Constructor registers are X0=`0x4326ec0`, X1=`0x42bfdc0`, W2–W5=0, W6=40, X7=null. Native ordinary caller stack arguments retain022's values: word0 at+0, word0 at+8, null at+0x10, byte0 at+0x18, byte0 at+0x20, word100 at+0x28. Higher bytes above byte-width stores are not meaningful arguments. Original entry copies40 zero parameter bytes to scene+0x34c.

`0xee2abc → 0x139778c` constructs the loading shutter; `0xee2ac8 → 0x9c90c0` requests Director replacement. Loading actions invoke `0x963094`, whose incoming virtual call reaches the same scene's `0xe2ea48`. At `0x96311c`, initializer return1 is observed. Full native TrackLayer construction and CPU updates remain enabled, as in020–022. Director activates the same scene with pending0 and EventDispatcher enabled. The driver calls neither GameScene constructor/initializer nor GameModel frame directly.

### Gameplay schedule and result

The original resource chain selects `songs/sayonarahatsukoi/0.aff`. The supplied chart is explicitly synthetic, not the archived song's chart:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

Director frame `0x1793f8c` executes Scheduler before original GameScene visit `0x18be2f8`, whose frame guard invokes model `0x10a7550`. The native timeline determines the input schedule:

| Controlled wall ms | Native effective E | Observation |
|---:|---:|---|
| 6450 | Initial activation | Same solo-created GameScene becomes running |
| 6451 | −2999 | Original visit/model preroll |
| 9452 | 0 | Native music anchor |
| 10452 | 1000 | JNI DOWN/UP, pointer42, coordinates740,700 |
| 11452 | 2000 | JNI DOWN/UP, pointer43, coordinates540,700 |
| 11574 | 2122 | Native completion and cached GameResult |

Tap walls are computed from the observed native E, rather than copied from020. JNI DOWN `0xbe31a8` uses pressure0.5, UP `0xdda71c` pressure0, with distinct Android pointer IDs and controlled capture timestamps987042/988042 and987043/988043. GLView/EventDispatcher/listener `0x194ff80`, initial-input `0xeec024`, tap judgment and contact cleanup remain native. The coordinates are reconfirmed functionally by two PUREs under this solo configuration; no new numeric ground-projection measurement is claimed.

| Native output | Authoritative result |
|---|---:|
| PURE / FAR / LOST | 2 / 0 / 0 |
| Score | 10,000,002 |
| Live health | 80.4000015258789 |
| Integer result health | 80 |
| Clear category | 3 |

Completion `0xc27d34` executes once, called by the model with LR=`0x10a7d6c`. Snapshot `0x1600bb0` executes once, LR=`0xc27dd0`. Its authoritative product is read from ScoreState+0x68, not an assumed return register. No result/scoring/health counter is assigned by the driver.

### Native ending and results handoffs

The ending root and ActionTimeline are the original GameScene initializer's CSLoader products, using unchanged `assets/layouts/ingame/end/GameEnd.csb`. Native hierarchy/action-tag/component relationships use the existing019–020 CPU resource construction and binding. The driver does not create another ending hierarchy or install timeline-to-Node links. The original24 property tracks/85 keyframes are retained.

| Entry | Caller/return site | Controlled wall ms | Count |
|---|---|---:|---:|
| `0x19bbdd0` ending timer | Scheduler `0x1875bcc` | 15574 | 1 |
| `0x1a51054` ending animation handler | `0x19bbf74` | 15574 | 1 |
| `0x147dee8` continuation | Original dispatch `0x7d6334` | 16414 | 1 |
| `0xf0b48c` outro | Scheduler `0x1875bcc` | 18434 | 1 |
| `0x18f11c0` results transition | Scheduler `0x1875bcc` | 18734 | 1 |
| `0xd11738` GameSession construction | `0x18f14b4` | 18734 | 1 |
| `0x187c0c8` results factory path | `0xd11858` | 18734 | 1 |
| `0x963094` results shutter CallFunc | Action dispatch `0x189ccf4` | 19484 | 1 results; 2 including loading |
| `0x891150` results initializer | Incoming virtual `0x96311c` | 19484 | 1 |
| `0xdc2c48` save helper | Native call `0x8921b8`, return`0x8921bc` | 19484 | 1 |
| `0x13552d4` score writer | `0xdc2cd8` | 19484 | 1 |
| `0x12a5e60` clear writer | `0x1355ab0` | 19484 | 1 |
| `0x113af20` final replacement | Native timer `0x15986b4` | 20184 | 1 results; 2 including loading |

Observed ending frame49 at wall16404 has zero continuations. Frame50 at16414 has exactly one. Native `out` playback and timers proceed without directly calling continuation/outro/shutter methods. Driver Scheduler dt controls elapsed time, not callback decisions. Scheduler advances and Director's wall-derived frame dt are separate explicit driver inputs, as in017–020; these times are not claims about hardware frame pacing.

### Object identity and ownership

| Object | Pointer | Continuity assertion |
|---|---|---|
| SongSelectScene / selected Song | `0x42db8c0` / `0x42bfdc0` | Original menu/setter/entry agreement |
| GameScene | `0x4326ec0` | Only gameplay scene constructor; original solo caller |
| GameModel | `0x43552c0` | Scene+0x3e0 unchanged through endpoint |
| LogicChart | `0x4330c00` | Scene+0x3e8 = Model+0x28 |
| GameTimeline / ScoreState | `0x4355440` / `0x4355480` | Native Model+0x30/+0x38 |
| GameEnd root / ActionTimeline | `0x4eaba80` / `0x4eb6f40` | Scene+0x3c8/+0x3d0; same initialization products |
| GameResult | `0x4ece1c0` | ScoreState+0x68 = GameSession+0x18, before/after transition |
| GameSession | `0x4ed5740` | Original constructor; retained by resultScene+0x2e8 |
| NormalGameResultScene | `0x4ed5840` | Original results factory product; final Director running scene |
| Loading / results shutters | `0x4327b00` / `0x4ed6380` | Original factories and native Director replacement requests |
| Director / Scheduler / ActionManager | `0x4104a80` / `0x41081c0` / `0x4108840` | Original singleton/owned runtime reused |
| EventDispatcher | `0x4108c00` | Final enabled1 |

Non-null retain/release arithmetic executes; GameSession's result retention and results scene's session ownership are native. Allocator/autorelease/free boundaries remain supplied, so this does not prove complete destruction or production reclamation. The endpoint assertions verify the original scene/model/cache still agree; no fixture copy restores them after results.

### Save gate and original SQLite

Read-only checkpoints establish the actual native gate:

- At `0x891684`, GameSession mode+0x20=0; original computation `(unsigned)(mode−9)<2` produces W8=0 and performs the native store to resultScene+0x2f8.
- At `0x89219c` and native save call `0x8921b8`, scene+0x2f8=0 and original GameResult+0xb0=0.
- Original `0x8921a0–0x8921b0` OR/branch therefore allows the save helper. Neither byte nor the decision register is assigned by the driver.
- Writer `0x13552d4` receives X1=`0x4ece1c0`, the same cached result, through the original save helper. Bundled SQLite APIs execute in the ARM64 ELF; host SQL does not implement the save.

A private `:memory:` database uses the existing native schema/open/query support. Native SQLite API observation records177 calls across initialization/schema, original saving and readback. The complete authoritative rows are:

```text
scores:
  id=1, version=1, songId="sayonarahatsukoi", songDifficulty=0,
  score=10000002, shinyPerfectCount=2, perfectCount=2,
  nearCount=0, missCount=0, date=1700000000,
  modifier=0, health=80, ct=0
clearTypes:
  id=1, songId="sayonarahatsukoi", songDifficulty=0,
  clearType=3, ct=0
```

Date1700000000 is the existing controlled calendar service. Both tables contain exactly one row. Results initialization's original save helper invokes each writer once; database readback occurs through the bundled native query path. Additional Scheduler dt `[0,0.25,1,5]` and one Director frame leave rows exactly unchanged and do not repeat continuation, results initialization or writers.

At wall20184, final native Director consumption makes `0x4ed5840` running, pending0, scene stack solely that result scene and EventDispatcher enabled1. These remain true at wall26434 after extra updates. The driver never assigns final running/pending/stack/dispatcher fields.

### Connection audit

| Connection | Authoritative evidence | Remaining supplied boundary |
|---|---|---|
| Solo selection → GameScene | `ee197c → eligibility1 → ee29a8 → ee29e8`; latch native | Entry delivery; catalog/selection request data; full Widget/menu omitted |
| Loading → initialization | Native Scheduler/ActionManager CallFunc `963094 → e2ea48`, return1 | Loading information/panel artwork proxies/skips |
| Scene → model frames | Director/Scheduler/guarded `18be2f8 → 10a7550` | Time/platform/render services |
| Gameplay → GameResult | Two JNI PUREs; completion/snapshot once; cache+68 | JNI environment and touch values |
| GameResult → GameSession | Identical `0x4ece1c0` pointer; native constructor/retention | Account worker remains inert; no result bridge |
| GameSession → results | Native `d11738 → 187c0c8`, resultScene+2e8 | Results UI omitted regions |
| Results → save gate | Original gate producer/store and branch observed | Prefix register/scratch restoration for omitted UI |
| Gate → SQLite | Original `8921b8 → dc2c48 →13552d4/12a5e60` | Private database, clock and libc platform services |
| Results transition → Director | Native closing actions/timer/request and final activation | Supplied dt/platform/render boundaries |

Compared with022, this executes all previously untested ordinary-session downstream handoffs. Compared with020, it removes the direct driver gameplay construction/activation starting point by using the native ordinary solo caller. No historical claim that full application startup or every external service has been eliminated is made.

### Exact PC skips and external services

The fresh authoritative execution retains these boundaries, without claiming skipped instructions executed:

| Source PC → resumed PC | Supplied/omitted work |
|---|---|
| `0xf72110 → 0xf72158` | Platform GLView attachment boundary |
| `0x16a4238 → 0x16a48d8` | Two original-constructed inert shutter panel Nodes, width100 |
| `0x121581c → 0x121584c` | Platform loading overlay omitted |
| `0xa507c4 → 0xa519ec` | Loading song-information artwork/text omitted; native Node proxy at shutter+0x310 |
| `0xa51adc → 0xa5213c` | Remaining information artwork/actions/canary omitted after native callback action registration |
| `0x196fdac → 0x196ffac` | Information-child closing visuals omitted |
| `0x891190 → 0x89164c` | Results UI prefix omitted; X28 restored to application-global address and X26=FP−0x60; native gate calculation retained |
| `0x891688 → 0x89219c` | Middle results UI/progression omitted |
| `0x8921dc → 0x8928e0` | Post-save ancillary UI/progression omitted |

No GameScene/TrackLayer initializer skip, GameEnd construction/binding substitute, eligibility skip, completion/continuation replacement, save-gate assignment, or forced Director activation is present. Whole-function base render/traversal/flush boundaries `0x129c924`, `0x1017a84`, `0x13edf0c` remain inert; actual GPU output is untested. TrackLayer `0x19069a0` is original. The older017 scoped Director PC skip is not used in this whole-frame driver.

The existing019–022 catalog/settings/account/application/resource services remain supplied: `0x14ac9c4`, `0x18a6b8c`, `0xb688e0`, `0xb99da4`, `0xd7845c`, `0x1730c40`, `0x190bc44`, `0xca7a88`, finite placeholder texture `0x176b6c4`, capability4096 at `0x1589238`, and bounded application facade/local/profile/mode storage. AFF bytes are synthetic; consumed CSB/font bytes are unchanged archive resources. Resource CPU construction/parenting/action-tag binding stays original. Pending submission/account processor `0x1246c98` is inert; no network submission success is claimed.

Called ancillary application/audio boundaries retain the established inert contracts, including `0x107af5c`, `0x18dcd1c`, `0x1186f70`, `0xc464e4`, `0x19becc0`, `0xc800b0`, `0x9d2518`, `0x9c8190`, `0x1513c24`, `0xd7654c`, `0xcff9cc`, `0x18fdcf0`, `0x1929dd0`, `0x16d80f8`, `0xf1e53c`, `0x1735d7c`, `0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, `0x11b35fc` and results post-save interface `0x1049858`; other inherited unvisited hooks do not establish execution. Observers `0x9c90c0` and `0x9ff610` log native products without returning around them.

Allocator/free/autorelease insertion, libc/C++ string/stream/formatting/RTTI, clocks/TLS/locks, locale/math, JNI and GL services keep prior contracts. AFF stream interfaces `0x1087f14`/`0xb06728` are supplied; native parsing/chart/model logic is preserved. Defined FreeType and SQLite APIs forward into the ELF. Instruction-budget extensions resume at the current PC without changing native state. The only new gate hooks read state; they neither write memory nor alter control flow.

### Reproduction boundary and unresolved work

In a fresh existing022 environment, prepare native Director/GLView and the established transition/private-database services; execute `0x1054f24`, native menu constructor and native selection setter. Supply the documented base-song/difficulty0 fixture and call ordinary `0xee197c`. Reuse021's native-action loading adapter with its declared UI skips. After activation, advance Director to native E0, compute touch walls from observed E, and deliver the two JNI DOWN/UP pairs. Advance original completion/ending timers and ActionTimeline through frame50; use the existing019–020 results transition/open/close schedules, selecting the second shutter and counting two total opening callbacks. Query both native SQLite tables and verify identity/final-state assertions. Do not invoke stage callbacks or writers directly.

Production catalog/availability generation, canonical UI PlayParameters, actual Play Widget delivery, full MainMenu/Android startup, rendering fidelity, online/account services, return navigation and complete reclamation remain unverified. None blocks the demonstrated bounded offline session; none is investigated further here. No024 is initiated.

## Pseudocode

```text
SUPPLIED: offline catalog/settings/profile/platform/ABI services,
          synthetic AFF, unchanged archived CSB/fonts, private SQLite database
ORIGINAL: registry initializer1054f24
DRIVER ENTERS ORIGINAL: SongSelectScene constructor + selection setter
DRIVER ENTERS ORIGINAL: ordinary startGameScene ee197c
  → original eligibility returns1
  → original latch store
  → ee29a8 allocation → ee29e8 GameScene constructor
  → original loading shutter + Director replacement request

DRIVER ADVANCES TIME; retained loading artwork skips apply
  → original Scheduler/ActionManager loading CallFunc
  → original GameScene initializer returns1
  → original closing actions + Director activation
  → Director → Scheduler → GameScene.visit → guarded model frame
  → supplied JNI DOWN/UP → original dispatcher/listener/judgments
  → original completion → ScoreState+68 native GameResult

ORIGINAL native timers + archived GameEnd hierarchy/ActionTimeline
  → native frame50 continuation147dee8 once
  → native outro/scene-change timers
  → native GameSession retains SAME GameResult
  → native NormalGameResultScene + results TransitionShutter
  → native opening action → original results initializer
      [documented results UI skips; native gate preserved]
  → original zero-valued gate permits original save helper
  → original score/clear writers → bundled SQLite
  → native closing actions/request → Director activates results scene

DRIVER: native database readback + bounded extra Scheduler/Director updates
VERIFY: one save, unchanged records, same result pointer, running results,
        pending0, dispatcher enabled
STOP
```

## GitHub Status

Only this report and an append-only023 context entry are publication changes, based on parent `9315b04bf4b6388d6f44f0b6c707d821c7f302fa`. Reports001–022, README, instructions and original assets/binary are preserved. Exact committed readback, prefix/tree checks and publication SHA are supplied in the final handoff. Harnesses, traces and databases remain unpublished.
