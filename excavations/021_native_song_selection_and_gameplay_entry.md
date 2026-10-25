# Expedition 021 — Native Song Selection, Gameplay Entry & Scene Navigation

## Result

**Minimum mission success, with a scoped Level B multiplayer-menu-to-gameplay regression. The ordinary solo Play pathway remains partial.** Original SongSelectScene construction, a genuine selected-pair setter, original multiplayer UI construction and callback binding, native GameScene allocation, loading-transition actions, GameScene initialization, Director activation, JNI judgments and a cached GameResult execute in the tested environment. The driver no longer enters the GameScene constructor or initializer in that successful branch.

The distinction matters: the two suggested starting addresses are not the ordinary solo entry chain. `0x10aa678` is a special mode-7 route. The closure leading to `0xdd0f90` belongs to **SongSelectScene::initMultiplayer**, established by original function-object RTTI. Neither a rendered solo menu nor its Play Widget has been demonstrated. A separate original `startGameScene` path was located and a native eligibility rejection executed, without overriding that rejection.

The completed menu branch reaches PURE2/FAR0/LOST0, score 10,000,002, live health 80.4000015258789, integer result health80 and clear3. This is an ordinary two-tap chart/gauge inside a controlled multiplayer-associated entry environment; it is not proof of a real multiplayer session, online authorization or the ordinary solo navigation path. No network operation or result submission was performed. SQLite/results presentation was not extended or claimed in021.

## What I Found

### Preparation, authority and evidence labels

The project introduction, supplied archive, current cumulative context, complete020 report and relevant prior construction/loading/transition evidence were inspected. Available scratch adapters were reused and extended; new emulator instances were created. No earlier live emulator was assumed recovered.

Starting default branch: `main`, commit `fc70e528f05f88c5266dbade9332e356db39ab1c`, tree `a27aa91912aba02471ee99f60c7265af985476c6`. No021 report was present at the initial tree check. Main was checked again before publication.

The unchanged `lib/arm64-v8a/libcocos2dcpp.so` SHA-256 is `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`; expected Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. Addresses below are its unrelocated ELF virtual addresses. Tests use Unicorn ARM64 execution; Capstone/ELF relocations/RTTI supply instruction-backed analysis. The ZIP has9658 members. GPU images, Android/JVM execution and production accounts are outside the experiment.

**Native-integrated** means original routines execute together across the stated connection; **Native-isolated** means original code executes with surrounding state or delivery supplied; **Instruction-backed** means decoded code/relocations/RTTI without execution of the enclosing path; **Interpretation** and **Unknown** retain their usual narrower meanings. A driver-entered initializer segment is not an execution of its omitted enclosing method.

## SongSelectScene identity and native construction

`0x1754440` is the original constructor. Allocation sites such as `0x13d5ff0–0x13d6004` request0x590 bytes before calling it. In021 the driver supplies that storage and calls the entire constructor with X1=0, W2=0. Its native base Scene constructor is `0xab9d60`; primary vtable becomes `0x1ad2260`. The initializer at primary vtable+0x4d8 is `0x161a8c4` and was **not executed completely**.

The constructor initializes interface subobjects, collections, flags and its holder at+0x360, allocates0x20 bytes for the selection controller/holder at scene+0x368, and calls `0x15160b4`. That routine allocates the actual0xd0-byte state and installs its pointer at holder+0. The state is not a fabricated vtable-bearing object.

| Object/field | Native producer | Tested state / meaning |
|---|---|---|
| SongSelectScene primary vtable | `0x1754490` | `0x1ad2260`, RTTI `SongSelectScene` |
| scene+0x368 | `0x175463c` | Native selection holder |
| holder+0 | `0x15160fc` | Native0xd0 selection state |
| state+0x18/+0x1c | `0x1516140` | Constructor integers, both0 here |
| state+0x20 | `0x1516160` | Optional supplied prior/map-related object, null here |
| state+0x28 | `0x1516164` | Active difficulty, initially0 |
| state+0x30/+0x38 | `0x1516154–58`, then setter below | Selected/remembered Song pointer and difficulty pair |
| scene+0x490/+0x491 | Constructor `0x1754534` | Initially0; distinct request/dialog flags |
| scene+0x578/+0x579 | `0x1754524` | Initially0; +0x579 is read as an entry flag in multiplayer callback |
| scene+0x4c0 | Native `initMultiplayer` segment `0x18ce55c` | Actual `MultiplayerReadyUpLayer` |

`0x12539c4`, which also writes this vtable, is a destructor, not a constructor. Vtable writes alone are insufficient constructor identification.

### Original selected-pair setter

`0x14ef098(holder, Song*, difficulty)` executes original stores at `0x14ef0c0` and `0x14ef0c4` into state+0x30/+0x38. Its real selection-initialization caller is `0x1583d64`, inside `0x158332c`, reached by the full menu initializer at `0x161a91c`. Difficulty3/4 additionally update separate remembered strings; those branches were not exercised.

The final fixture invokes this original setter with the supplied Song and difficulty0. Active difficulty remains the constructor-produced0 at state+0x28. No driver writes any of those selection fields. The external session's encoded selection also names that same Song/difficulty. Executing the complete catalog/settings-driven `0x158332c` initializer or a difficulty Widget remains unestablished.

An early probe left the pair null and the permissive host string adapter treated address0 as an empty string. That probe is excluded from the final menu-entry claim. The final fresh run uses the native setter and rejects a null source at the std::string copy service; it completes with no such source. This correction is an environment-validation improvement, not a discovered production fallback.

## Original selection and gameplay-entry call graph

Three paths must remain distinct.

| Path | Evidence | Consequence |
|---|---|---|
| SongSelectScene virtual+0x570 → `0x10aa678` | Instruction-backed; interface thunk `0x157d31c → 0x157d320` also branches there | Hardcoded-song/special-scene route; GameScene constructor at `0x10aac8c` uses mode7 and a special scene whose+0x2b8 becomes8 |
| `initMultiplayer` callback `0x1591d00 → 0xdd0f90` | Native-integrated in021 after driver delivery of a native-bound callback | Tested ready-up/session entry, not ordinary solo Play |
| SongSelectScene `startGameScene` `0xee197c` | Instruction-backed identification plus native-isolated eligibility rejection | Separate ordinary/general entry; enclosing Play Widget/selection producer is not executed |

There is no demonstrated direct `0x10aa678 → 0xdd0f90` edge. Static BL references to the latter are `0x1591ea8` and `0xc669bc`.

RTTI of vtable `0x1af3a88` explicitly names `SongSelectScene::initMultiplayer()::$_59`; invoke slot+0x30 is `0x1591d00`. The function-object vtables `0x1aac538` and `0x1ad8ee0` identify its nested OnlineError/PlayParameters and deferred callbacks, respectively. This is stronger evidence of provenance than guessing from a shared final GameScene constructor.

The executed path is:

```text
[driver] full SongSelectScene constructor; native selected-pair setter
[driver-entered native segments] ready-up construction/attachment; callback binding
[driver] deliver that native-created function object through its invoke entry
[native] 1591d00 -> 1591ea8 -> dd0f90
[native] dd0fd4 allocation -> dd1054 GameScene constructor
[native] dd1438 -> 139778c TransitionShutter factory
[native] dd1448 -> 9c90c0 Director replacement request
[native] Director frame -> d0dc14 -> 12157ec onEnter
[native] songLoadIn timer -> 1924a60 -> a50780 action subtree
[native] Scheduler/ActionManager/CallFunc -> 963094
[native] incoming virtual+4d8 -> e2ea48 GameScene initializer
[native] loading timers/closing actions -> Director pending GameScene
[native] Director consumes replacement -> GameScene visitation -> GameModel frame
[native] JNI input -> listener -> judgments -> completion/result cache
```

Visual omissions inside the action-producing function are specified below; this diagram does not assert execution of its full artwork setup.

## Selected song/difficulty/settings state and gameplay configuration provenance

App+0xb0 was supplied as a private0x1400-byte session/selection service. It is **not established as a generic history object**. The class identities, four-player record processing, multiplayer resources and `game_scene_multiplayer_update` registration associate the tested route with multiplayer. The service's startup and complete class layout were not executed.

Original `0x83bd98` reads service byte+8 and its halfword+0x57d. Disabled lookup or encoded0xffff returns X0=0, X1=0 without a catalog query. Otherwise it computes an index/difficulty decomposition and calls catalog lookup `0x1222a60`. Controlled tests observed:

| byte+8 | encoded+0x57d | Native catalog index | Returned Song / difficulty |
|---:|---:|---:|---|
| 0 | 0 | None | null /0 |
| 1 | 65535 | None | null /0 |
| 1 | 0 | 0 | Supplied test Song /0 |
| 1 | 7 | 1 | Supplied controlled catalog result /2 |

The last case tests decoding, not a full second chart selection. In the joined run only index0 is used, and it resolves to the same Song installed by the original selected-pair setter. The host supplies the catalog result, not this native index/difficulty decision.

`0xdd0f90` takes X0 pointing to a captured SongSelectScene pointer, X1=Song, W2=mode, W3=flag. Passing SongSelectScene directly as X0 would be the wrong contract.

| GameScene constructor input | Actual producer in tested branch | Validation |
|---|---|---|
| X0 storage | Original allocation at `0xdd0fd4`, size0x4e0 | Native-integrated |
| X1 Song | `0x83bd98 → 0x1222a60` external catalog result, passed by `0x1591d00` | Native selection read; supplied catalog |
| W2 difficulty | `*scene+0x368` state+0x28 | Native constructor default0, read at `0xdd0ffc` |
| W3 mode | Callback W23; no character ability selected | Native0, not supplied directly to GameScene |
| W4 configuration/scene-type integer | state+0x18 | Native0; full semantic range unknown |
| W5 flag | Helper W3&1 | Native normalization;0 in joined run; not universally identified as mirror |
| W6 speed | App+0x70 settings integer+0xc, native clamp | Supplied setting40; native output40 |
| X7 special-scene pointer | `0xdd1038` | Native null |
| Stack slots+0,+8,+0x10,+0x18,+0x20,+0x28 | `0xdd103c–50` | Significant values1,0,0,0,0,100; byte stores have their actual widths |

No universal “entry flag equals mirror” conclusion follows. The joined fixture uses no mirror. The actual interpretation of nonzero values needs a consumer-backed follow-up.

Native-isolated argument tests stop immediately before `0xe4e4dc`, so they do not claim constructed GameScenes for each case. Configured speeds −5,0,9,10,11,40,65,66,100 produce10,10,10,10,11,40,65,65,65. Helper flags0,1,2,3 produce constructor flags0,1,0,1. The original SCVTF/FCVTZS and unsigned comparison execute, rather than a host clamp.

## Menu resources, Widgets and callback bindings

The original `initMultiplayer` function is `0x18cd8e4`; its full method is not executed. Two genuine segments are driver-entered:

1. `0x18ce52c → stop0x18ce560`: supplied allocation storage, native zeroing, entire constructor `0x10d5200`, its virtual initializer `0x79bc18`, autorelease request, and native store into SongSelectScene+0x4c0. The allocator call immediately before this segment is not part of the experiment.
2. `0x18cef90 → stop0x18cefe0`: original bound-function construction, capture of the actual SongSelectScene, and copy/assignment `0x17e73dc` into layer+0x360. The function holder at layer+0x380 points to the in-place object; vtable is `0x1af3a88`, invoke is `0x1591d00`, captures+8 and+0x10 both contain the native menu pointer.

The CPU resource machinery consumes unchanged archived `assets/layouts/multiplayer/MultiplayerReadyUpLayer.csb` (5412 bytes) and `MultiplayerReadyUpPlayer.csb` (6152 bytes, three reads). Font resources execute through the already recovered native CPU font path. Actual texture artwork/GPU operations remain supplied. The layer's initializer returns to its original caller; its W0 return was not separately asserted as a success criterion.

The driver delivers the installed function object's invocation. This does not demonstrate a real ready button's Widget event, hit testing, or complete parent attachment of the menu UI. Most of `initMultiplayer` and the full SongSelectScene initializer remain outside coverage.

## Loading-transition construction, GameScene initialization and Director activation

`0x139778c` allocates0x3d0 bytes, calls base constructor `0x19f2e84`, installs TransitionShutter vtable `0x1af1868`, executes `0x16a41c4`/`0x170c208`, and calls `0x1927bd0` to record Song/difficulty. The latter sets shutter+0x358=1, stores Song at+0x368 and difficulty at+0x370, and sets+0x388=1. The immediate caller uses W3=0, W4=2. Transition duration is the native0.75f set by `0x16a41ec`.

The existing inert panel resource boundary is retained, together with a new explicitly supplied native-constructed visual Node at shutter+0x310. Original parent attachment is called on that Node. It substitutes the song-information visual target, not GameScene, its model or its selected configuration.

`0x12157ec` schedules the native `songLoadIn` timer with delay0.1f. Its function object reaches `0x1924a60 → 0xa50780`. The retained original action-producing segment `0xa519ec–0xa51adc` constructs FadeIn/MoveBy/easing/composite actions, a delay from shutter+0x374 and the native-bound CallFunc for method `0x963094`. The native runAction target is the supplied visual Node. Scheduler/ActionManager, not the driver, invokes that CallFunc.

At `0x963118`, incoming virtual+0x4d8 calls **this same GameScene's** `0xe2ea48`. At return site `0x96311c`, observed W0=1. The GameScene initializer's HUD, GameLayer and TrackLayer paths established in019–020 execute; their earlier visual suffix skips are not reintroduced.

After initialization, `0x963214–0x963314` selects a native3.0-second delay when shutter+0x358==1, rather than the other branch's approximately0.4 seconds. It records a clock-derived deadline and schedules `framedeltaconsumer`. The chain through `0x18f83ec`, `0x186e018 → 0xb126b8`, native closing actions and the original transition finish requests GameScene replacement. Driver-supplied Scheduler dt controls elapsed time, not the callback's branch/eligibility.

Observed transition states in the final fresh run:

| Controlled wall ms | State |
|---:|---|
| 1000 | Director running shutter; pending0; dispatcher disabled; `songLoadIn` pending |
| 1250 | songLoadIn consumed; information action pending; model still null |
| 1650,2050 | Initializer callback count0 |
| 2450 | Native CallFunc count1; GameScene initializer returns1; native model exists;3-second timer registered |
| 6450 before Director consumption | Running shutter; pending actual GameScene |
| 6450 after original Director frame | Running actual GameScene; pending0; dispatcher enabled |

An earlier attempt advanced only the shorter results-transition schedule and stopped with the native three-second timer still pending. That was insufficient supplied elapsed time, not a failed production initializer. A separate early fault identified the omitted song-information visual hierarchy; those diagnostic traces are not spliced into the final fresh regression.

## Menu-to-gameplay execution regression

The native whole-file chart loader reads `songs/expedition021/0.aff` through its original filename-selection/parser/LogicChart initialization chain. Raw AFF bytes and Song/difficulty metadata are supplied external inputs. The ordinary fixture is:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

Native menu entry supplies difficulty0 in this experiment, whereas the earlier020 control used difficulty2. No score counter or health value is forced to the earlier expectation. All five metadata slots initially resolve to the controlled difficulty object; its requested difficulty field is explicitly0 for this run. This is a minimal supplied catalog, not a catalog parser validation.

| Identity | Final fresh run pointer |
|---|---|
| SongSelectScene / selection state | `0x4323fc0` / `0x4325240` |
| external Song | `0x42bfdc0` |
| native ready-up layer / native function object | `0x4325340` / `0x43256a0` |
| menu-allocated GameScene / loading shutter | `0x492bc00` / `0x492cac0` |
| native model / LogicChart | `0x495a000` / `0x4935940` |
| native GameTimeline / ScoreState | `0x495a180` / `0x495a1c0` |
| gauge / gameplay listener | `0x495a340` / `0x496a300` |
| cached ScoreState+0x68 GameResult | `0x5715f80` |

The model's delegate is the scene interface at `0x492bee8`; camera rig `0x496ca00`; spatial-index group header `0x495a5c0`. Native listener is registered, enabled and unpaused with priority20. At completion the model flags+0x138/+0x139/+0x148 are0/1/0, retained contacts0 and active-note count0. Inspected model/chart/timeline/score/listener/camera links are native-produced, not driver assignments.

Director-driven timing, with clocks supplied only as external monotonic values:

| Wall ms | Effective E / last model E | Observation |
|---:|---:|---|
| 6451 | −3000 | First explicit active-gameplay observation |
| 9452 | 0 | Native startup/music boundary |
| 9453 | 1 | Preroll complete |
| 10453 | 1001 | Original JNI DOWN/UP, Android pointer42, lane-target coordinates740,700 |
| 11453 | 2001 | Original JNI DOWN/UP, pointer43, coordinates540,700 |
| 11574 | 2122 | Native completion and result cache |

JNI calls use `0xbe31a8` and `0xdda71c` with controlled JNI/environment boundary, pressure0.5 then0 and supplied capture timestamps987000+i/988000+i. Those timestamps do not replace GameTimeline. Original EventDispatcher/listener and judgment entries execute; no direct judgment invocation is used.

Observed result: **PURE2, FAR0, LOST0; score10,000,002; live health80.4000015258789; result integer health80; clear3.** The original cache at ScoreState+0x68 supplies the result pointer. `0x1600bb0` is not treated as returning that pointer in X0.

Across the joined run, one loading CallFunc enters `0x963094`, one GameScene initializer executes, seven model-frame entries are recorded, and each of `0x194ff80`/`0xeec024` executes twice. Completion handler `0xc27d34` and snapshot `0x1600bb0` execute once. On a representative Director frame, four GameScene visit entries share the frame stamp and only one enters the model: the original guard remains active.

## Ordinary startGameScene, eligibility and repeated-selection boundaries

RTTI of the nested callback at vtable `0x1b06288` names `SongSelectScene::startGameScene(Song*, DifficultyClass, MapStep*, GameMode, int, SpecialSceneModifier*, PlayParameters)`. Native callsites `0xa4e1ac`, `0xc4b040` and `0xf6e304` reach `0xee197c`; its body/captures agree with that signature. This identifies a separate general/ordinary entry rather than relabeling the multiplayer closure.

**Native-isolated negative test:** call `0xee197c` on a native-constructed menu with native-selected pair, the controlled Song, difficulty0, null MapStep/modifier, mode0, speed40 and an explicit zero-valued40-byte PlayParameters input. The supplied metadata's availability byte at Song+0x250 is0. Original `0x17c45f4 → 0x193baa8 → 0x14ac910` checks availability and takes rejection `0x17c4644`. At `0xee2214` the eligibility result is0. The entry returns normally to the harness; no GameScene is allocated/constructed and menu+0x490 remains0. This does not show that an archived playable song is rejected or that all eligibility is represented by one byte. It shows the precise first blocking interface of this minimal metadata fixture. No eligibility hook was substituted.

Instruction-backed positive path: `0xee25b0` tests menu+0x490, `0xee25bc` sets it1 before the general construction branch, `0xee29a8` allocates GameScene, and `0xee29e8` calls its constructor. Unlike the tested multiplayer helper, this branch writes stack+0=0. It copies actual PlayParameters into GameScene+0x34c and calls `0x139778c`/Director at `0xee2abc`/`0xee2ac8`. These enclosing success branches were not executed in021. The upstream solo Play Widget and its complete field producers remain Unknown.

No claim of repeated-play idempotence is made. The ordinary request latch is instruction-backed; repeated successful requests, failed-dialog recovery, complete difficulty switching and return-to-selection were not executed. Disabled/sentinel session selection and native speed/flag boundaries above are the bounded negative/variation tests.

## Object identity, ownership and optional results continuation

The native ready-up binding stores the actual menu pointer in its function object. Native entry passes the selected Song to the GameScene constructor, then to the shutter. Transition initialization retains incoming/outgoing scenes, Director owns the pending/running handoff, and `0x963094` calls outgoing exit/release and clears its pointer before initializing incoming GameScene. Non-null native retain/release arithmetic executes; autorelease-pool insertion/free and complete reclamation remain supplied. Raw captures are not automatically described as owning strong references.

The final GameResult belongs to the same native-created GameScene/model. The experiment stops after its cache/classification observation. It does not manually construct GameSession, trigger ending callbacks or call SQLite writers. A private in-memory database is opened as inherited runtime infrastructure, but **no021 persistence regression or local saved-row assertion is claimed**. The existing020 results/SQLite evidence remains historical, not an experiment silently appended to this trace.

## Synthetic dependency audit: before and after

| Dependency | Before021 |021 outcome |
|---|---|---|
| SongSelectScene | Absent from joined gameplay | Entire original constructor; full initializer still omitted |
| Selection holder/state | Supplied constructor arguments bypassed it | Native allocations/defaults and original selected-pair setter |
| Active difficulty | Driver GameScene argument2 | Native state+0x28 default0 read by helper |
| Song/catalog/session inputs | Supplied metadata | Still supplied external catalog and session encoding; native lookup/decomposition |
| Selected pair | Not used | Native setter installs actual Song/difficulty; full UI selection unexecuted |
| Speed | Driver GameScene argument40 | Controlled external setting40; native read/clamp supplies constructor argument |
| GameScene allocation/constructor | Driver entered | Original multiplayer-menu helper allocates and calls it |
| GameScene initialization | Driver entered | Native loading CallFunc calls incoming virtual initializer; return1 observed |
| Ready-up layer/callback | Absent | Native constructor/resource initializer/binding segments; event delivery still driver-entered |
| Loading transition | Gameplay scene activated directly | Native menu factory/request, timer/action initialization and closing/Director activation |
| Model/chart/timeline/score/camera/listener | Native020 | Preserved in newly menu-created scene |
| Loading information visuals | Not needed by020 startup | One supplied native Node plus explicit visual skips; not eliminated |
| Director/Scheduler/ActionManager/dispatcher | Native020 with platform boundaries | Reused original creation/registration/activation |
| Ordinary solo eligibility/Play | Unexecuted | Actual start method and rejection executed; success still partial |
| GPU/audio/account/allocator/platform | Supplied | Remain supplied |
| Ending/results/SQLite | Native020 | Not rerun downstream in021 |

## Exact PC skips and supplied services

The successful regression does not skip the GameScene/TrackLayer initializer bodies or replace their native internal links. Its deliberate instruction-range boundaries are:

| Boundary | Supplied behavior / omitted state |
|---|---|
| `0xf72110 → 0xf72158` | Established platform GLView interface boundary |
| Driver-enter `0x18ce52c`, stop`0x18ce560` | Ready-up construction/attachment segment only; omitted enclosing initMultiplayer setup |
| Driver-enter `0x18cef90`, stop`0x18cefe0` | Genuine selected callback binding only; omitted other UI callback setup/attachment |
| `0x16a4238 → 0x16a48d8` | Inert native left/right shutter panel Nodes at+0x300/+0x308 |
| `0x121581c → 0x121584c` | Omitted platform overlay attachment |
| `0xa507c4 → 0xa519ec` | Omitted loading-information artwork/text setup; supplied native visual target at shutter+0x310 |
| `0xa51adc → 0xa5213c` | Omitted remaining decorative information actions/hierarchy and final canary check; execute original register/stack epilogue after native callback-action registration |
| `0x196fdac → 0x196ffac` | Omitted song-information child closing actions on unavailable visuals; preserve original enclosing closing/transition machinery |

The two menu segments are separate driver entries, not a single run of the full `0x18cd8e4`. The final registered callback is delivered by the driver through its original invoke address. All following GameScene constructor/initializer and loading callbacks in the successful chain are reached by native calls/actions.

Called application/provider boundaries are explicit: controlled account/character getter`0xb688e0` (character49, no ability object); settings backend`0x18a6b8c`; session catalog index lookup`0x1222a60`; ID lookup`0x14ac9c4`; resource-provider getter`0xb99da4`, AFF string`0xd7845c`, archive bytes`0x1730c40`, path/existence`0x190bc44`/`0xca7a88`; texture lookup`0x176b6c4` returns the finite native-created2x2 placeholder; `0x1589238` reports maximum texture size4096. Raw CSB/font bytes come unchanged from the archive.

Other called inert application/audio/platform services inherited from020 are `0x107af5c`, `0x18dcd1c`, `0x1186f70`, `0xc464e4`, `0x19becc0`, `0xc800b0`, `0x9d2518`, `0x9c8190`, `0x1513c24`, `0xd7654c`, `0xcff9cc`, `0x18fdcf0`, `0x1929dd0`, `0x16d80f8`, `0xf1e53c`, `0x1735d7c`, `0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, plus controlled facade virtual services. Pending completion/account work`0x1246c98` is inert. Base draw/traversal/flush boundaries`0x129c924`, `0x1017a84`, `0x13edf0c` remain supplied; TrackLayer update`0x19069a0` remains original.

Allocator/free/realloc, C++ ABI strings/streams/numbers/formatting/RTTI, clocks, locale, TLS/locking, inert GL requests and deterministic random services retain the019–020 contracts. Native exported FreeType implementations are forwarded to original library code, not all treated as host stubs. AFF stream boundaries`0x1087f14`/`0xb06728` and pool insertion`0x10ac6e8` remain supplied. Null retain/release is bounded; non-null reference arithmetic executes. `0x9c90c0` has an observation hook which does not return/replace its body. Original PLT-to-defined-symbol forwarders are not evidence of host implementation of those defined functions.

Instruction-budget extensions resume at the current PC without changing native state. Final tracing samples entries/services rather than every BL; original instruction execution is unchanged. Diagnostic fault/resume probes and the earlier null-pair/permissive-string test are excluded from the final fresh successful regression.

## Recovered pseudocode

```cpp
// Original constructor + original setter; driver supplies storage/selection request.
SongSelectScene::constructor(prior=null, arg=0) { // 1754440
    Scene::constructor();
    selectionHolder = native_new(0x20);
    selectionHolder.construct(/*native defaults*/); // 15160b4 -> new State(0xd0)
    // state.difficulty=0; state.selectedSong=null; state.selectedDifficulty=0
}
setSelectedPair(holder, song, difficulty) { //14ef098, native; real caller1583d64
    holder->state->selectedSong = song;       //+30
    holder->state->selectedDifficulty = difficulty; //+38
    if (difficulty==3 || difficulty==4) updateRememberedString(); // untested
}

// Two actual initMultiplayer segments execute, not the entire method.
ready = nativeReadyLayerConstructorAndInit(); //10d5200 ->79bc18
menu->ready = ready;                         //native18ce55c
ready->callback = native_bind(menu, initMultiplayer_lambda59); //18cef90..fe0

// Driver delivers this native-created function; real Widget delivery untested.
initMultiplayer_lambda59() { //1591d00
    song = session.getEncodedSelectedSong(); //83bd98; external catalog lookup
    pair = menu->state->selectedPair;        //valid native-set Song/difficulty
    mode = resolveTestedModeOrCharacterAbility(); //0 here; other branches not executed
    if (optionalMapConditionNeedsAsyncWork()) {
        requestExternalWork(/*native callback1074814 -> scheduled c6679c*/);
        // Instruction-backed only. c6679c status0 can reach dd0f90.
    } else {
        multiplayerStart(&capturedMenu, song, mode, menu->flag579); //dd0f90
    }
}
multiplayerStart(menuCapture, song, mode, flag) { //original body executes
    menu = *menuCapture;
    speed = nativeClamp10to65(settings.speed);
    game = native_new(0x4e0);
    game.constructor(song, state.difficulty, mode, state.kind,
                     flag&1, speed, null, /*native stack args*/);
    nativeBuildPlayerRecordsAndDetachMenuListeners();
    shutter = nativeLoadingFactory(game, song, state.difficulty, false, 2); //139778c
    Director::replaceScene(shutter);
}

// Original runtime, with information artwork omitted as tabulated above.
Director.frame() -> activatePendingShutter() -> shutter.onEnter();
Scheduler.after(0.1, "songLoadIn", nativeShowInformation);
nativeShowInformation() {
    // omitted visual prefix; target is an explicitly supplied native visual Node
    target.runAction(originalCompositeActionsAndDelay(
        CallFunc(bind(shutter, 0x963094)))); //a519ec..a51adc
}
963094() { incoming->virtualInit(); /*e2ea48 returns1 here*/
           scheduleNativeLoadingDeadline(/*3 seconds on this branch*/); }
Scheduler/ActionManager -> originalClosingActions -> requestGameSceneReplacement();
Director.frame() -> nativeTransitionExit/dispatcherRestore -> runningGameScene;
GameScene.visit() { if (newDirectorFrame) model.frame(); }
JNI.begin/end -> GLView -> EventDispatcher -> nativeListener -> nativeJudgment();
model.complete() -> GameScene.complete() -> ScoreState.cachedResult; //native021 endpoint

// Separate ordinary/general startGameScene, native rejection + static success path:
startGameScene(song, difficulty, map, mode, speed, modifier, playParameters) { //ee197c
    // Original surrounding account/special branches: only scoped subset tested.
    if (!nativeCanPlay(song, difficulty)) return; //17c45f4; tested unavailable metadata
    if (menu.requestLatch490) return;             //instruction-backed positive branch
    menu.requestLatch490 = true;
    game = native_new(0x4e0);                     //ee29a8; unexecuted in021
    game.constructor(/*native general configuration*/); //ee29e8
    game.playParameters = playParameters;
    Director.replaceScene(nativeLoadingFactory(game, ...));
}
```

## Remaining synthetic dependencies and unresolved mysteries

The principal missing advance is still **ordinary solo selection-to-Play success**: actual difficulty-selection producer, complete SongSelectScene initializer, ordinary catalog availability/entitlement state, real Play Widget dispatch and the upstream construction of PlayParameters. The final native selected-pair setter closes a genuine internal relationship but does not establish an entire menu selection workflow.

`initMultiplayer` has an optional OnlineError/PlayParameters branch via`0x18894cc`, callback`0x1074814`, deferred`0xc6679c` and status-dependent dialogs. These are instruction-backed, not tested online behavior. No submission, authentication or external network interaction occurred.

Full song-information visuals, complete ready-up parent attachment and real multiplayer manager startup remain missing. The loading-action success uses explicit presentation substitutions and does not validate its complete graphical display or cancellation. Repeated Play success, changing difficulty through a Widget, returning from results to selection, final scene destruction/autorelease reclamation and gameplay-reachable FlickNote remain unestablished. No bug or leak is inferred from these incomplete fixtures.

## GitHub Status

Only this report and an append-only021 cumulative-context section are authorized publication changes. Reports001–020, README, instructions and original assets/binary are preserved. Publication is based on parent `fc70e528f05f88c5266dbade9332e356db39ab1c`; the exact new commit SHA and pinned report/context links are supplied in the final handoff after readback and tree/prefix verification. A file cannot embed the SHA of its own containing commit without changing that SHA.
