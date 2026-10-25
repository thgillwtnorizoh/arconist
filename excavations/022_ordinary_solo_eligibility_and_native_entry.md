# Expedition 022 — Ordinary Solo Eligibility & Native Gameplay Entry

## Result

**Strong success.** With justified controlled offline metadata, original `SongSelectScene::startGameScene` at `0xee197c` passes its native eligibility decision, sets its own request latch, allocates and constructs GameScene through `0xee29a8 → 0xee29e8`, requests the loading transition, and reaches original GameScene initialization and Director activation. Original scene visitation reaches the model. No eligibility return, request latch or gameplay ownership link is supplied by the driver.

This establishes Phase A under the declared catalog/platform/presentation boundaries. It does not establish a real Play Widget event, complete menu initialization, production catalog parsing, a rendered game screen, or results/local saving. Testing stops in initial gameplay preroll; no input, ending or persistence regression is performed.

## What I Found

### Source, preparation and evidence

Starting main: `b02dd88271d879f7812f4e836a0abe8dc951aa0c`; tree `1f7ec05e93299210f1cbeca3ad2a49308ba01aa3`. The authoritative context and complete021 report were read from GitHub; necessary019–020 construction/loading sections and available018–021 adapters were consulted. The recursive starting tree has no022 publication. The supplied introduction was read.

The archive's `lib/arm64-v8a/libcocos2dcpp.so` hashes to `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, and equals the available extracted harness copy byte-for-byte. Original files/resources are not patched. Addresses are original ELF VAs. Unicorn executes ARM64; Capstone supplies instruction analysis. Existing harness source files, not an earlier live emulator, are reused.

**Native-integrated:** original instructions execute across the stated connection. **Native-isolated:** native routines with prepared surroundings/driver delivery. **Instruction-backed:** decoded relationships without execution of the enclosing producer. **Interpretation:** explanation beyond observation. **Unknown:** unverified behavior. External libc/C++/platform adapters are not described as native Android execution.

### Offline input contract

The archived `assets/songs/songlist` contains `sayonarahatsukoi`, set `base`, empty `purchase`, BPM base178 and ratingClass0/rating1. This justifies an ordinary base-song, difficulty0 fixture with no purchase descriptor. The host maps the consumed fields into the established external Song/difficulty representation. The full JSON-to-Song loader and production installed-chart detector are **not executed**.

A synthetic two-tap AFF is supplied at the path selected by original code, `songs/sayonarahatsukoi/0.aff`. It is not claimed to be the song's archived chart:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

The chart provider supplies those complete bytes; archived CSB/font resources retain their unchanged bytes. Metadata BPM178 and the chart's explicit timing120 are separate consumed inputs. Localized display text remains controlled fixture text, rather than a validation of every catalog field.

| Condition | Native consumer | Input source | Tested result |
|---|---|---|---|
| Selected Song and difficulty | `0xee197c`; native setter `0x14ef098` | Original menu constructor `0x1754440`; external Song, difficulty0 | State+0x30 is actual Song; +0x38=0; active +0x28 defaults0 |
| Per-difficulty availability | `0x193baa8 → 0x14ac910`, load `0x193bac4` | External installed/playable fixture byte Song+0x250=1 | W0=1; negative byte0 returns0 |
| Difficulty object | `0x19833fc → 0x14ac910` | Song+0x228 points to external difficulty; +0x124=0 | Same requested difficulty object consumed |
| Difficulty predicate, semantics not fully named | `0xacb11c` | Difficulty+0xec=0 | Native jump table selects `0xacb230`; result0, so enclosing eligibility continues |
| Purchase/pack-associated eligibility | `0x10a1b04`; `0x18c898c` reads Song+0x190 | Song+0x256=0, +0x190=null, set `base`; archived purchase is empty | Original predicate returns1 twice; no entitlement-return substitution |
| Additional Song flag | `0x17c46a8` | Song+0x160=0 | Conditional `0x169eb68` path not needed |
| Difficulty resource/restriction predicate | `0x12fd660` | Difficulty+0xf0=0 | Original zero-flag branch returns1 |
| Further difficulty predicate | `0xf7867c` | Difficulty+0xb8 is matching song ID, +0x124=0, +0=null, +0xf0=0 | Original predicate returns1; special ID/difficulty cases unneeded |
| Global/Song gate | `0x17c4774–0x17c4788` | Mapped native global/default fixture | Native path continues; not generalized to every application configuration |
| Optional purchase-object gate | `0x17c478c`, `0xfc2f64` | Song+0x190=null | Native null branch continues |
| Final song-ID/set restrictions | `0x83ca28 → 0x189dafc` | Original initialized registry; `sayonarahatsukoi`, set `base`; supplied local/profile storage | Registry lookup returns−1; original final eligibility returns1 |
| Offline/mode context | Menu virtual+0x608 → `0x126dc1c` | App+0xe0 object's word+0x38=0; App+0xc0 word0; App+0xb0 byte8=0 | Native reads, no active multiplayer entry or special mode |
| Ability/configuration | `0xb688e0`, later native branches | Existing controlled character49 with no ability at character+0xd0; null map/modifier | Ordinary constructor mode/configuration0; no special ability branch |
| Request latch | `0xee25b0 / 0xee25bc` | Native menu constructor sets initial0 | Native entry writes1; driver does not assign it |

These are the tested predicates and field values, not universal semantic names for all flags. Full entitlement/account rules, alternative difficulty states and nonzero purchase descriptors remain untested. An empty purchase descriptor and supplied local chart explain the chosen offline case; the experiment does not assert ownership of paid content.

The Song/difficulty memory producer remains the external catalog boundary. The recovered native consumers above and native selection setter are verified; an offset-only store in an unrelated class is not accepted as proof of a Song producer. Existing inactive difficulty-pointer slots alias the same prepared object, as in the earlier adapter; only difficulty0 is marked available and selected. This is a bounded consumed-input fixture, not a complete multi-difficulty catalog.

### Missing initializer: the one new material blocker

The preliminary available positive probe, after availability was enabled, faulted on a low-page read at `0x189db54`, address0x28. `0x189dafc` walks a native ordered song-ID registry rooted at `0x1bf95e8`, with sentinel `0x1bf95f0`. An all-zero root is not a valid empty initialized container. Null memory must not be treated as a permissive lookup result.

Instruction references identify its real producer in static initializer `0x1054f24`: `0x1055a68–0x1055a98` establishes the header, followed by five original `0x9720b8` insertions, and destructor registration at `0x1055b50`. Executing the entire original static initializer returns normally and creates a five-entry registry. The fresh validation executes it before entering `startGameScene`; no registry nodes, keys or lookup return are supplied by the driver. A diagnostic original lookup for the selected Song returns `0xffffffffffffffff` (−1), as does the lookup reached inside eligibility.

A separate diagnostic then reached actual solo GameScene construction but stopped at the already known shutter-panel adapter because its `left/right` inputs had not been prepared. This was corrected by running the existing runtime preparation before entry in the fresh validation, not by inventing a second gameplay scene or resuming the diagnostic as the success trace. No new renderer, account or catalog subsystem was reconstructed. The ordinary success claim uses only the fresh uninterrupted validation.

### Negative control

A separate fresh emulator executes the native menu constructor and selected-pair setter, then `0xee197c` with Song+0x250=0 and otherwise the same scoped entry arguments. Original `0x193baa8` returns0, enclosing eligibility returns0 at `0x17c4670`, and `0xee2214` rejects it. The method returns normally with no GameScene, latch0 and Director pending0.

This control terminates before the registry is consulted, so its static registry initializer is intentionally unnecessary. The earlier negative log is corroborated by this newly executed control. No rejection or success register is forced.

### Positive ordinary entry and constructor configuration

The driver calls native `0xee197c(menu, Song, 0, null, 0, 40, null, parameters)` once. It does not enter `0xdd0f90`, `initMultiplayer`, its ready-up segments or a GameScene constructor directly. Native eligibility executes:

```text
17c45f4
  → 193baa8 = 1
  → 19833fc → acb11c = 0
  → 10a1b04 = 1
  → 12fd660 = 1
  → 10a1b04 = 1
  → 19833fc → f7867c = 1
  → remaining native global/optional-object gates
  → 83ca28 → 189dafc (−1) → final eligibility1
return to ee2214 with W0=1
```

`0xee25b0` reads the original latch; `0xee25bc` writes it1. `0xee29a8` calls allocation for0x4e0 bytes. `0xee29e8` calls original constructor `0xe4e4dc`; constructor LR=`0xee29ec`. It returns to that caller, which copies PlayParameters and requests the loading transition at `0xee2abc / 0xee2ac8`.

| Constructor location | Observed value | Producer |
|---|---|---|
| X0 | `0x4326ec0` | Original allocation at `0xee29a8` |
| X1 | `0x42bfdc0` | Same external Song passed through ordinary entry/native selection |
| W2 | 0 | Requested difficulty, original stack reload |
| W3 / W4 / W5 | 0 / 0 / 0 | Native ordinary no-map/no-ability configuration |
| W6 | 40 | Controlled entry speed copied by original code |
| X7 | null | Entry's null modifier |
| Stack+0, +8, +0x10 | 0, 0, null | Native ordinary caller stores |
| Stack+0x18 | byte0 | Native byte store; higher bytes are unspecified caller stack residue |
| Stack+0x20 | byte0 | Native flag store |
| Stack+0x28 | word100 | Native default configuration |

Unlike021's multiplayer helper, the ordinary caller's stack+0 value is0. The parameter block is an explicit40-byte all-zero external value input, not a claimed canonical default constructor. `0xee2a10–0xee2a24` copies its complete40 bytes to GameScene+0x34c; all40 are still zero at the endpoint. In this null-map path it is transferred without the map-specific update at `0xee2a0c`. Upstream UI production and all nonzero field meanings remain Unknown. Native acceptance and the consumed ordinary path justify this bounded absent-options case.

### Loading, native ownership and first gameplay update

The established021 loading adapter is reused, including its explicit presentation omissions. The original `0x139778c` factory makes the shutter for **this** GameScene, original `0x9c90c0` requests Director replacement, and original Director/Scheduler/ActionManager run the loading actions. Native CallFunc reaches `0x963094`, whose virtual initializer call reaches `0xe2ea48`. At original return site `0x96311c`, W0=1. The complete previously established TrackLayer construction remains enabled.

| Object | Fresh validation identity / state |
|---|---|
| SongSelectScene / selection state | `0x42db8c0` / `0x42dcb40` |
| Selected Song / difficulty | `0x42bfdc0` / `0x42c00c0`; difficulty0 |
| GameScene / primary vtable | `0x4326ec0` / `0x1ae6ef0` |
| Loading shutter | `0x4327b00` |
| Model / primary vtable | `0x43552c0` / `0x1b79978` |
| LogicChart | `0x4330c00`; Scene+0x3e8 and model+0x28 agree |
| GameTimeline / ScoreState | `0x4355440` / `0x4355480` |
| TrackLayer / background / UI | `0x4367840` / `0x4365b00` / `0x44e2440` |
| Model delegate / camera rig | `0x43271a8` = Scene+0x2e8 / `0x4367c80` |
| Gameplay listener | `0x4365580`; registered1, priority20, paused0, enabled1 |
| Final Director | Running `0x4326ec0`; pending0; EventDispatcher enabled1 |

Native chart/model/timeline/score/listener/camera/TrackLayer relationships are neither copied from an older fixture nor driver-assigned. Native retain/release arithmetic remains active for non-null objects; observed chart/timeline/score references are4/2/2. Pool insertion/free and complete reclamation remain inherited boundaries.

Controlled time follows the reused loading schedule: wall1000 activates the shutter; wall2450 delivers the native initializer callback; wall6450 consumes final GameScene replacement. The activation Director frame already enters the model. One immediate frame at6451 validates the visitation chain explicitly:

```text
1793f8c Director frame, counter2 / scene stamp1
  → 13d3f44 Scheduler
  → 9effe0 scene processing
  → 18be2f8 GameScene visit
  → 10a7550 GameModel frame
  → three more visits, scene stamp2, no duplicate model entry
```

There are two model-frame entries total: activation and its immediate verification frame. There is one entry, constructor, initializer and loading CallFunc; zero `0xdd0f90` entries and zero completion-handler `0xc27d34` entries. The driver calls neither model-frame nor GameScene initializer directly. The endpoint remains initial preroll, with completion flags0, retained contacts0 and activeCount1; gauge health is still0 at this early point. No judgment, completed score or later health behavior is inferred.

### Exact boundaries and dependency change

No eligibility function, `startGameScene`, latch store, GameScene allocation/constructor/initializer or TrackLayer initializer is replaced/skipped. `0x189dafc` also remains original. Observation hooks record constructor/callsite identity without changing execution.

| Retained PC boundary | Meaning |
|---|---|
| `0xf72110 → 0xf72158` | Platform GLView attachment boundary |
| `0x16a4238 → 0x16a48d8` | Existing supplied native shutter-panel Nodes |
| `0x121581c → 0x121584c` | Platform overlay attachment omitted |
| `0xa507c4 → 0xa519ec` | Loading-information artwork/text omitted; supplied native visual Node at shutter+0x310 |
| `0xa51adc → 0xa5213c` | Remaining informational decoration/canary omitted after native action registration |
| `0x196fdac → 0x196ffac` | Information-child closing visuals omitted; native enclosing transition remains |

The GameScene/GameLayer/TrackLayer suffix skips from older expeditions are not reintroduced. Neither021 ready-up segment is entered. Results-UI hooks may exist in the inherited adapter but are not reached and are not used as evidence here.

External services remain as documented in019–021: controlled catalog lookup `0x14ac9c4`, account/character getter `0xb688e0`, settings backend `0x18a6b8c`, raw AFF/provider services `0xb99da4`/`0xd7845c`, archived bytes `0x1730c40`, path/existence `0x190bc44`/`0xca7a88`, finite placeholder texture `0x176b6c4`, max texture capability4096 at `0x1589238`, and supplied application facade storage (local state at App+0x38, profile at+0x28, mode/settings at+0xc0, disabled multiplayer state at+0xb0). These supply consumed data/interfaces; no native eligibility outcome is replaced. The local/profile stores are bounded zero-initialized storage, not full account startup.

Called inert application/audio/platform boundaries are `0x107af5c`, `0x18dcd1c`, `0xc464e4`, `0x9d2518`, `0x9c8190`, `0x1513c24`, `0xd7654c`, `0xcff9cc`, `0x18fdcf0`, `0x1929dd0`, `0x16d80f8`, `0xf1e53c`, `0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, `0x11b35fc`, `0xb9d4a4`, `0x1a1ad2c`, plus existing facade virtual stubs. Base rendering/traversal/flush `0x129c924`, `0x1017a84`, `0x13edf0c` remains bounded. TrackLayer CPU update is original. `0x9c90c0` is observed, not returned around. Allocator, libc/C++ ABI, RTTI, strings, locale, clock/TLS/locking, GL, AFF stream `0x1087f14`/`0xb06728`, autorelease insertion and bounded null reference handling retain earlier explicit contracts. Defined native FreeType calls remain forwarded to the ELF. Instruction-budget continuations resume at the current PC without modifying native state.

Existing `prepare_runtime` opens a private in-memory database as unused inherited infrastructure. This is not results initialization or a persistence experiment. No score/clear writer or SQLite-row assertion is performed.

| Dependency | Before022 | After022 |
|---|---|---|
| Ordinary solo eligibility | Rejected unavailable metadata | Native full scoped decision returns1; negative control preserved |
| Song-ID registry | Uninitialized in prior positive probe | Entire original static initializer executes before entry |
| GameScene construction caller | Multiplayer helper only demonstrated | Actual ordinary caller `0xee29e8` demonstrated |
| Request latch | Positive operations instruction-backed | Native read/store executed |
| Loading/initializer/activation | Proven for multiplayer-associated entry | Reused on same ordinary-entry product |
| Internal gameplay ownership | Native in earlier work | Preserved, no manual bridge |
| Menu UI, catalog/account startup | Supplied/partial | Remain supplied/partial; actual Play Widget out of scope |
| GPU/loading artwork | Supplied/skipped | Unchanged disclosed presentation boundaries |
| Results/local saving | Historical evidence only | Not run in022 |

### Reproduction and bounded conclusion

Use a fresh instance of the available019–021 ARM64 adapters. Prepare the established application/resources/native Director/GLView environment and transition panel services before entry. Supply the listed base Song/difficulty fields, local/profile stores, disabled multiplayer flag and mode0. Execute original `0x1054f24`, original menu constructor `0x1754440`, and native selected-pair setter `0x14ef098` (registry initialization may precede or follow menu construction, but must precede eligibility). Supply40 zero parameter bytes and call original `0xee197c` with the listed arguments. Observe its real predicates, constructor LR and ordinary stack flags. Reuse the loading presentation boundary and advance original timers/actions/Director; stop upon model visitation. A separate unavailable-byte0 control returns before construction. No binary patch, native-return forcing or request-latch assignment is required.

The hypothesis is supported for this controlled offline contract. This is not a claim that changing one byte alone solves every Song's eligibility. Unknowns are the full production Song/availability producer, all alternative restriction/account states, canonical UI PlayParameters construction, real Play Widget delivery, complete menu setup and later ordinary-session results/save continuity. They are not investigated after the first gameplay milestone. No023 is initiated.

## Pseudocode

```cpp
// Driver supplies external catalog, resource bytes and platform/ABI services.
// Original static initializer, not a host-created registry:
original_1054f24(); // initializes song-ID restriction registry

// Driver-entered original menu construction and selection request:
original_SongSelectScene_constructor(menu, null, 0); //1754440
original_setSelectedPair(menu.holder368, song, 0);    //14ef098

// Driver enters this original ordinary method, not a multiplayer closure.
startGameScene(song, difficulty=0, map=null, mode=0,
               speed=40, modifier=null, suppliedZeroParameters40) { //ee197c
    executeOriginalCharacterModeAndMenuContextChecks();
    if (!originalEligibility(song, difficulty)) return; //17c45f4; negative control
    // Native predicates inspect supplied metadata; no forced return.
    executeOriginalOrdinaryConfigurationBranches();
    if (requestLatch490) return; //ee25b0
    requestLatch490 = 1;         //ee25bc, native store
    game = native_new(0x4e0);    //ee29a8
    original_GameScene_constructor(game, song, 0, 0, 0, 0, 40, null,
                                  /*native ordinary stack args*/); //ee29e8
    copy40(game + 0x34c, suppliedParameters);
    shutter = originalLoadingFactory(game, song, difficulty, false,
                                     nativeComputedLoadingFlag); //ee2abc
    originalDirectorReplace(shutter);                            //ee2ac8
}

// Driver advances original lifecycle with controlled time.
// Explicit loading artwork skips remain as tabulated, not eligibility skips.
Director.frame(); Scheduler/ActionManager.update();
originalLoadingCallFunc_963094() {
    incoming.virtualInit(); //same GameScene; original e2ea48 returns1
    originalDeadlineAndClosingActions();
}
Director.frame(); //original replacement activates same GameScene
GameScene.visit() {
    if (originalFrameGuardDetectsNewDirectorFrame())
        originalModelFrame(); //10a7550 reached through visit, not driver call
}
// STOP: initial gameplay milestone. Results and saving unexecuted.
```

## GitHub Status

Publication is based on `b02dd88271d879f7812f4e836a0abe8dc951aa0c`. Only this new report and an append-only022 entry in context.md are authorized changes. Exact committed readback, historical-prefix and tree-preservation results are returned with the publication SHA in the final handoff. Reports001–021, README, instructions, harnesses and executable/resource assets are not publication changes.
