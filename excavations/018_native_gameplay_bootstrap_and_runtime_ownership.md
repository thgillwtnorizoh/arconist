# Expedition 018 — Native Gameplay Bootstrap and Runtime Ownership

## Result

**Strong success. Original gameplay startup now constructs and connects the essential model graph, and that graph runs native frames, dispatched JNI input, two judgments and completion snapshot creation.** The successful test enters the original GameScene constructor and initializer. The initializer itself calls the existing chart loader, allocates/initializes GameModel, constructs GameTimeline and ScoreState/gauge, produces the spatial index and registers the original gameplay listener. A further original GameLayer/CameraController initialization segment supplies the model's camera relationship.

Original Director singleton creation also executes its constructor and complete ordinary initializer, constructing Scheduler, ActionManager, EventDispatcher and supporting CPU-side engine objects. Its initializer registers ActionManager with Scheduler. Original GLView attachment enables EventDispatcher; original scene replacement/pending-scene activation enters GameScene and starts its timeline.

This is a **bounded bootstrap subset**, not complete application or gameplay-screen initialization. GameScene's allocation is supplied, its constructor executes, and its large initializer executes only through `0xe2f44c`, with two explicit visual-code skips. The application context, song/difficulty metadata, platform GLView facade, settings/account/audio/resource interfaces and allocator remain supplied. The driver enters the original scene activation consumer and model frame rather than executing a full rendered Director loop. No manually assembled model/chart/timeline/score/index/camera/listener relationships are used in the successful joined regression.

The two-tap result is PURE2/FAR0/LOST0, score **10,000,002**, live health **80.4000015258789**, integer health **80**, clear category **3**. The original completion handler creates the cached GameResult. The ending/results/SQLite chain from 017 is not rerun in this expedition.

## What I Found

### Authority and preparation

Starting default branch `main` was **`9308f6ef7fac120494da800b68850cb385500879`**, with reports 001–017 and no Expedition 018 publication. Read the project introduction, current cumulative context, complete 017 and 010 reports, and relevant model/input/lifecycle/engine evidence from 009, 011, 012 and 015–016. Inspected the supplied ZIP, including native libraries and Android resources. It contains 9,658 entries. Existing scratch adapters and research fixtures were genuinely present and inspected; this report does not claim recovery of inaccessible Work memory or emulator state.

The executable is `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256 **`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`**, Build ID **`17d660edbf37ca78beefc32e07672c97419ddce6`**. Archive/extracted executable bytes were checked and remain unchanged. Addresses are main-library ELF virtual addresses before relocation; explicitly identified `0x4...` pointers are test-arena identities. Unicorn 2.1.4 executes ARM64, Capstone 5.0.9 decodes it, and pyelftools 0.33 reads ELF metadata.

Evidence labels: **Native-integrated** means original routines execute together over the stated scope; **Native-isolated** means original code executes with prepared surroundings; **Instruction-backed** means original instructions/RTTI/relocations without execution of the enclosing path; **Interpretation** denotes a grounded explanation; **Unknown** denotes an unverified producer or behavior. Named RTTI below is original metadata; other descriptive function names are research labels.

## Original gameplay-entry call graph

### Production entry above the executed boundary

RTTI identifies the vtable beginning at `0x1ad2260` as **SongSelectScene**. Its virtual entry at `0x1ad27d0` points to `0x10aa678`. That method contains song-selection/eligibility branches and a genuine GameScene construction call at `0x10aac8c`. A related entry at `0xdd0f90` allocates `0x4e0` bytes at `0xdd0fd4` and calls GameScene constructor `0xe4e4dc` at `0xdd1054`, passing selected song/difficulty and configuration. It reads selection state through the menu object and settings speed, including clamping the settings value to 10–65. Later `0xdd1438 → 0x139778c` wraps the new scene in the loading-transition path and retrieves Director at `0xdd1440`.

These upstream menu/loading operations are **instruction-backed**, not executed in the successful bootstrap. The concrete semantic name of every intermediate closure and loading-transition class is not established here. Special/tutorial callers also construct GameScene; they are not substituted for evidence of ordinary startup. This expedition selects the deeper ordinary GameScene constructor/initializer boundary to avoid reconstructing menu assets, account eligibility and a whole catalog.

| Connection | Evidence in 018 |
|---|---|
| SongSelectScene selection/entry → GameScene allocation/construction | Instruction-backed; production allocation not executed |
| Driver-provided scene storage/arguments → original `0xe4e4dc` | Native-isolated entry; full constructor executes |
| Original GameScene initializer `0xe2ea48` → chart load `0x16e67a4` | Native-integrated |
| Initializer → GameModel factory `0xc9f6f0` → `0xfbfd04` | Native-integrated, full ordinary model construction |
| Model initializer → timeline/score/gauge/index | Native-integrated |
| GameScene initializer → gameplay listener registration | Native-integrated |
| GameScene/GameLayer initializer segments → CameraController → model camera link | Native-integrated with disclosed visual omissions |
| Driver request → original Director replace/activate → Scene onEnter/start | Native-integrated native lifecycle, driver-controlled entry |
| Driver frame call → original model update → JNI listener/judgment | Native-integrated over those calls; not a rendered Director frame |

## GameScene construction

### Constructor and original base objects

The test supplies a zeroed `0x4e0` allocation and calls **`0xe4e4dc`** with X0=scene storage, X1=requested song, W2=difficulty 2, W3=ordinary mode 0, W4=scene-type 0, W5=0, W6=speed 40 tenths, X7=null special scene. Additional entry-SP slots are `{0:1,8:0,16:0,24:0,32:0,40:100}`. These are explicit external startup choices, not recovered account defaults for every mode.

The complete constructor executes through its real return. It calls base Scene `0xab9d60` and Node `0x131419c`, creates the default camera through `0x12a1654 → 0x11a6474 → 0x196c000`, and attaches it through original child interfaces. It also creates/registers the base Scene custom listener. Camera background-brush creation is an inert graphics boundary; CPU camera construction remains original.

The resulting GameScene has primary vtable **`0x1ae6ef0`**, default camera at `+0x2b8`, and embedded delegate interfaces at `+0x2e8/+0x2f0`. The constructor initializes model/chart/UI pointers and container headers rather than accepting driver-written model fields. Selected song is at `+0x318`, difficulty at `+0x320`, gauge/mode at `+0x324`, scene type at `+0x310`, and requested speed at `+0x4bc`.

### Initializer segment and chart handoff

Execution enters real initializer **`0xe2ea48`** (GameScene virtual `+0x4d8`). Its prefix inserts native history state, reads supplied settings/account interfaces, takes the ordinary no-special-scene branch, chooses the supplied character, and performs native base initialization.

At **`0xe2f0dc`** it calls original chart loader `0x16e67a4`; **`0xe2f0e0`** stores the returned chart at Scene `+0x3e8`, followed by the original retain. It constructs a native pending-result object through `0xa9e36c` when appropriate, but no pending packet is sent or completion-side queue processing executed. Previous-record service `0x1513c24` reports no previous record. Account/catalog/pending-service startup is not claimed complete.

At **`0xe2f2f0`**, original code calls model factory `0xc9f6f0`. At **`0xe2f2f4`** it stores the result at Scene `+0x3e0`; **`0xe2f2f8`** invokes model listener setup `0x130bdf0`; **`0xe2f300`** retains the model. These are executed native stores, not test assignments.

The initializer does **not** return in the successful test: execution stops at `0xe2f44c` after camera attachment. No whole-GameScene-initializer success return is fabricated. Allocation, constructor return, this initialized subset, scene activation and first frame remain distinct observations.

## Gameplay model construction

### Factory and initializer execute completely

**`0xc9f6f0`** allocates a `0x158` GameModel, calls the original Ref constructor `0x121a0ec`, installs GameModel vtable **`0x1b79978`**, initializes constants/containers, and calls **`0xfbfd04`** at `0xc9f81c`. The ordinary factory/initializer execute to their actual returns without a PC skip. The returned object has RTTI **GameModel**.

Observed factory arguments from the original GameScene call are precision 10,000, Scene `+0x2e8` delegate, actual loaded LogicChart, selected song, difficulty 2, mode 0, null ability, scene-type 0. Additional flags, input-mode setting and initial/carry/best values are produced by the native scene caller; ScoreState factory is observed with ordinary flags 0, health input 100, carry -1 and best 0. A requested health argument is not a guarantee that every subsequent live-gauge field starts at that number.

Significant executed producers:

| Native producer / callsite | Destination | Observed role |
|---|---|---|
| `0xfbfd04` prefix | Model `+0x40` | Scene's real embedded delegate |
| `0xfbfec4–0xfbfecc` | Model `+0x28` and retain | Actual loaded chart |
| Timeline allocation/`0x1636640`, store at `0xfbff78` | Model `+0x30` | New GameTimeline, vtable `0x1af5e60` |
| `0x14f0a94 → 0x13e00b4`, store at `0xfbffa4` | Model `+0x38` | New ScoreState |
| `0x12c5070` under score construction | ScoreState gauge vector | Ordinary LifeBarState |
| `0xfc0184–0xfc02a4 → 0x1576aa4` | Model `+0x88` group-index vector | Native headers and bucket membership |
| `0x130bdf0` from `0xe2f2f8` | Model `+0x150` | New registered all-at-once gameplay listener |

Model pause/finished/related flags at `+0x138/+0x139/+0x13a` initialize clear on this branch; `+0x148` comes from the scene/configuration input and is 0. Active-note and retained-contact containers start empty. Index building runs **506** producer calls for all runtime objects, including generated bars, rather than merely inserting the two playable notes.

### Runtime dependency ownership and concrete identities

The successful JNI run produced the following **test-arena pointers**:

| Object / relationship | Pointer or value |
|---|---|
| GameScene | `0x42bf940` |
| Scene `+0x3e0` → GameModel | `0x42eb580` |
| Scene `+0x3e8` and Model `+0x28` → same LogicChart | `0x42c6ec0` |
| Model `+0x40` → Scene `+0x2e8` | `0x42bfc28` |
| Model `+0x30` → GameTimeline | `0x42eb700`, RTTI GameTimeline |
| Model `+0x38` → ScoreState | `0x42eb740`, RTTI ScoreState |
| ScoreState ordinary LifeBarState | `0x42eb8c0` |
| Model `+0x20` → CameraController | `0x42fc6c0` |
| Native timing-group index header | `0x42ebb40` |
| Model `+0x150` → gameplay listener | `0x42fb880` |
| ScoreState `+0x68` → completed GameResult | `0x42fe900` |

Native retain/release instructions execute for non-null references. At the observed post-construction/playing boundary, chart reference count is 4, timeline and ScoreState counts are 2 each. This establishes native reference operations and pointer continuity, not complete owner enumeration, allocator reclamation or autorelease-pool draining. The test supplies allocation/free/pool services; no leak conclusion follows.

## Camera and GameLayer construction

The initial constructor-created Scene camera is distinct from the **CameraController** used by gameplay projection. The latter has a genuine producer: **`0x1393474`**, allocating `0x2e0` and initializing the controller with cameras at `+0x2a8/+0x2b0`.

After model/listener construction, the joined test continues the original Scene initializer into its game-layer setup. Original **`0x1877ebc`** constructs GameLayer (`0x3f0`) and enters initializer **`0x12967e4`**. Native base initialization `0x16567ac` succeeds; the layer stores its model at `+0x2f0`, calls CameraController factory, stores it at `+0x2f8` (`0x129689c`) and attaches it as a child (`0x12968ac`). The Scene caller stores/attaches GameLayer and **`0xe2f434–0xe2f448` retrieves the controller and stores it at Model `+0x20`**.

Two explicit PC skips bound this path:

- **`0xe2f304 → 0xe2f3bc`** omits the life-bar HUD visual object construction.
- **`0x12968b0 → 0x1297788`** omits GameLayer's extensive note/sprite/decorative rendering suffix, returning through its real epilogue with the native base-initialization result preserved. It is not evidence that complete GameLayer visual initialization ran.

Neither skip assigns a model, chart, timeline, scoring, index, camera or listener relationship. The native camera-controller creation and ownership/link stores occur outside the skipped regions and execute. GameScene's remaining visual/UI/ending-resource initialization after `0xe2f44c` is unexecuted. This is a partial internal GameLayer, and that limitation remains material despite the successful gameplay-core regression.

## Chart and metadata integration

The actual GameScene initializer reuses the previously established loader unchanged:

`0x16e67a4 → 0x1371744 → provider wrapper 0x10f45e8 → 0x1870de0 → original MD5 → 0xc052f4 → complete ordinary 0x173b358`.

Only resource-provider lookup/byte delivery and its enclosing metadata/settings environment remain supplied. The native caller requests **`songs/expedition018/2.aff`**. Exact fixture (final LF present):

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

Observed native chart fields: AudioOffset 0 (`+0xc4`), density 1 (`+0xc8`), judgment units 2 (`+0xb8`), chart end 2120 (`+0xbc`), effective timing speed 6 (`+0xf4`) from requested speed 4. The scene's actual ordinary inclusion argument is used; it is not silently copied from the earlier standalone loader test. Integer lane conversion gives the runtime lanes 4 and 3. Sorting, timing groups, count, generated bars, depths and chart initialization remain native.

| Input/value | Immediate producer | Source boundary / validation |
|---|---|---|
| Song ID and difficulty object | Supplied metadata shaped as in 010; selected by native scene/loader | Catalog/parser production not newly executed |
| Song BPM 120, selected class 2, timing override 0 | Supplied song/difficulty records | Explicit fixture inputs, not inferred global defaults |
| Song/difficulty transfer into model | GameScene `0xe2ea48 → 0xc9f6f0` | Native-integrated |
| Chart bytes | Provider lower-reader boundary `0xd7845c` | Supplied complete AFF text; original wrapper/parser execute |
| Resource root `songs` | Supplied directory configuration `0x1bef230` | Production root initialization remains unexecuted |
| AudioOffset/density | Original AFF header parser and LogicChart initializer | Native-integrated, then consumed by model/timing/score |
| Speed | Explicit scene request 40 tenths; original loader normalization | Native-derived effective speed 6; settings fallback not exercised here |
| Mirror, mode, scene type | Requested ordinary constructor arguments and native scene propagation | Values 0, not account-derived defaults established for all paths |
| Offset settings | Supplied settings block at application `+0x70`; original model reads | Ordinary supplied offsets 0; chart-to-timeline propagation native |
| Selected character/ability | Native account getter reads supplied account/character | Character ID 49, null ability; full account initialization absent |
| Missing previous best | `0x1513c24` supplied query result null | No real player database consulted |
| Gauge-mode map / touch globals | Original selected ELF initializers | Native-built globals, replacing earlier fabricated headers/values |

Three original static initializers run once in each fresh test: **`0x1905bc8`** (init-array slot `0x1b95528`) constructs the gauge-mode map at `0x1bf9648`, including ordinary key 0 → vector `[0]`; **`0x14c9fe0`** (`0x1b94ba8`) constructs the two touch listener-ID strings; **`0x133eedc`** (`0x1b95b40`) constructs the GLView pointer-map header at `0x1bf1a88`. No manually inserted gauge-map node, touch-string value or pointer-map header is needed. This is selected initializer execution, not a claim that every ELF constructor or Android startup executes.

## Director, Scheduler and EventDispatcher relationships

### Native singleton and service production

**`0xa4227c`** retrieves the singleton at `0x1bee0a0`. When absent it allocates `0x230`, calls **`0x18942c4`**, installs DisplayLinkDirector vtable **`0x1b5eaf8`**, stores the singleton, and calls **`0x18b3b6c`**. The original ordinary initializer returns success 1; no PC skip is used in this constructor/initializer. Configuration/GPU capability population is supplied, while original Configuration allocation, containers and default value readers execute.

Native initialization constructs Scheduler through **`0xda7a90`** and stores it at Director `+0xa0`; ActionManager through **`0x81a0b8`**, stored at `+0xa8`; EventDispatcher through **`0xf9f040`**, stored at `+0xb0`. At **`0x18b3d00 → 0xdb9674`**, it registers ActionManager's native function object (vtable `0x1b37d48`, capture = actual manager), priority `INT_MIN`, unpaused. The call operator is **`0xd630b8 → 0x9effe0`**. Director also constructs native notification events, TextureCache (`0x1090254`) and Renderer (`0xadf370`) with controlled graphics/platform services.

Final joined pointers are Director **`0x4104000`**, Scheduler **`0x4107740`**, ActionManager **`0x4107dc0`**, EventDispatcher **`0x4108180`**. These services are not fabricated buffers with driver-installed inter-service pointers.

### Native GLView attachment enables input

EventDispatcher's constructor initializes **`+0x124=0`**; simply creating/registering the listener is insufficient. An initial JNI probe mapped/released touches but produced no gameplay callback with this native disabled state. This was a startup-dependency observation, not a touch/judgment failure.

The production enabling step is **Director GLView attachment `0xf720a8`**. It retains/stores the supplied platform GLView at Director `+0xf0`, obtains its original frame size through virtual `+0xb0`, copies 1280×720 into Director `+0x180`, and calls **`0xf7216c → 0x925c68(dispatcher,1)`**. The final regression executes those stores/calls. It does not manually enable the dispatcher or write the Director viewport.

The GLView facade itself remains prepared: original vtable `0x1b20d60`, frame size 1280×720, scale factors 1. This is not native GLView construction. The graphics-only segment **`0xf72110 → 0xf72158`** is skipped; GPU capability gather `0x1929dd0`, renderer buffer setup `0x16d80f8` and default framebuffer service `0xf1e53c` are bounded services (framebuffer null). Camera CPU setup still runs from original constructors and actual viewport reads `0xf09110`. Full GL projection-stack/render initialization is not claimed.

### Listener and scene activation

**`0x130bdf0`** creates the actual all-at-once listener (`0xb981cc`), installs original native captures for begin `0x194ff80`, move `0x10e7008`, end `0xd88408`, cancel `0x18ba6d8`, and calls **`0x130bf58 → 0x1942fc8`** to register it at fixed priority 20. Observed listener states: registered 1, paused 0, enabled 1. Model `+0x150` owns the native result of this setup.

The driver calls original **`0x9c90c0(Director,scene)`**. With no running scene, its **`0xf46b3c`** path pushes the scene into the real stack, sets pending state and starts animation through **`0x979fe0`**. The platform Application animation-interval interface is supplied. Driver entry into original pending-scene consumer **`0xd0dc14`** makes the scene running and dispatches its original enter callbacks. Node **`0x1597d14`** recursively marks the seven created Nodes running/resumes their native services. GameScene enter-finished **`0x14b2910`** takes the ordinary direct-start branch and calls **`0x8db04c`** at `0x14b29e4`.

At wall clock 1000, actual timeline epochs become `[1000,1000]`; Scene running is 1, Director running is the actual GameScene, pending is null, and scene stack contains that scene. These fields and timeline started state are native-produced. The driver does not overwrite the running-scene pointer, scene running byte or timeline epochs. This is original lifecycle activation under a controlled driver schedule, not Android queue scheduling or a full GPU Director frame.

## Native bootstrap execution traces

### A. Construction to first frame

After native entry/activation, controlled wall time advances to 4001. An original timeline update `0x16c90bc` performs music-start anchoring; its audio-provider request is inert. Effective chart time becomes 0 rather than treating startup overshoot as immediate chart progress. Original model frame **`0x10a7550`** at wall 5001 observes E=1000, native index/active-note management and camera geometry. Before judgments, pause/finished/input-mode bytes are 0; the first frame has three active objects, including generated auxiliary content.

There are **three full original model-frame calls** in the final regression: wall 5001, 6001 and 6122. They are driver-entered model frames. `GameScene::visit`'s once-per-Director-frame path is established earlier but not newly used to dispatch these three calls. No Director frame counter is fabricated as evidence of rendered-frame integration.

### B. Native registered JNI input and cleanup

The test calls original JNI begin **`0xbe31a8`** and end **`0xdda71c`**, supplying scalar Java-equivalent event fields. These entries do not need JNI array services; the inert JNIEnv handle is not a Java VM. Original GLView mapping/allocation, native Touch, EventDispatcher **`0x1980970 → 0x18feb24 → 0xc2bf98`**, listener **`0x194ff80`**, projection/initial input **`0xeec024`**, tap classifier **`0x160ce28`** and recorder **`0x1730290`** execute together. No gameplay callback replaces this delivery chain.

| Wall / E | Android pointer ID | Native Touch / engine slot | Native gameplay contact ID | Coordinates / pressure | Observation |
|---|---:|---|---:|---|---|
| 5001 / 1000 | 42 | `0x42fd6c0` / 0 | 0 | `(740,700)` / 0.5 | PURE1, health 40.20000076293945, one retained contact |
| 5001 / 1000, UP | 42 | same Touch / 0 | 0 | same coordinates / 0 | Native cleanup; retained vector empty, slot mask 0 |
| 6001 / 2000 | 43 | `0x42fe0c0` / reused slot 0 | 1 | `(540,700)` / 0.5 | PURE2, health 80.4000015258789, one retained contact |
| 6001 / 2000, UP | 43 | same Touch / 0 | 1 | same coordinates / 0 | Native cleanup; retained vector empty, slot mask 0 |

Touch vtable is **`0x1ad7fd8`**. Native fields observed: slot `+0xc`, coordinates `+0x1c/+0x20`, pressure `+0x2c`, generated contact ID `+0x34`, captured timestamp `+0x40`. Captured timestamps are 987000 and 987001; UP leaves the stored begin timestamps unchanged. They do not replace effective GameTimeline judgment time. The first contact's valid generated ID 0 must not be mistaken for a missing contact, and Android ID 42/43 must not be conflated with slot 0 or generated IDs 0/1.

Actual constructed camera geometry differs from earlier prepared orthographic fixtures. At original `0xeec1ec`, the ground-Z0 points are approximately `(167.135498046875,-185.35205078125,0)` and `(-167.135498046875,-185.35205078125,0)`. Native lane projection selects lanes 4 and 3. Earlier exploratory center-height inputs did not hit this constructed camera's floor region; the test selects valid screen coordinates rather than patching native matrices.

Observed entry counts: JNI begin/end 2 each; dispatcher/listener adapter 4 each; begin listener/initial input/classifier/recorder 2 each; end cleanup **`0xf9a50c`** 2. Actual scene-created listeners and native pointer maps are used.

### C. Completion and authoritative cached result

At wall **6122**, E=**2121**, beyond native chart end 2120, the third frame sets Model `+0x139=1` and reaches **`0xe2c124 → 0xc27d34`** through the actual embedded Scene delegate. The handler sets the scene completion latch and calls **`0xc27dcc → 0x1600bb0`**. Execution stops at **`0xc27dd0`**, immediately after snapshot creation, before further history/pending/ending work. The missing pause-UI hide call **`0xfa4320`** is an inert presentation service.

The authoritative result is read from **ScoreState `+0x68`**, never inferred from the snapshot routine's X0 return. Native getters **`0x1315038`** and **`0x12a5574`** report score **10,000,002** and category **3**; result PURE/FAR/LOST are **2/0/0**, integer health **80**. Active count and retained contact count are 0; pause/input-mode remain 0, finished is 1. No driver snapshot construction or direct result installation occurs.

The handler prefix/snapshot executes once in this run. Repeated initialization, repeated completion, full ending UI and save behavior are not newly tested here. The established 017 results chain remains previous evidence, not an 018 execution claim.

### D. Comparison against scoped direct input

A fresh native bootstrap was repeated with identical chart, constructor choices, clock and screen inputs, replacing JNI delivery only with original **`0xeec024`** and prepared Touch-like input storage. That comparison also produced PURE2/FAR0/LOST0, score 10,000,002, health 80.4000015258789, integer health 80 and category 3; its separate native cached result was `0x42fe280`.

This establishes equal judgment/result fields, not identical transport state. Direct input does not allocate/map engine Touch objects, generate/retain gameplay contacts through the listener or perform JNI UP cleanup. Its supplied contact IDs differ. The successful JNI test is the stronger bootstrap/input integration.

### E. Native-created Scheduler registration

A separate fresh native Director bootstrap constructs a Node through `0x131419c`, enters it through `0x1597d14`, constructs original MoveBy **`0xf1b510`** (+600 X over two seconds) and registers it through **`0xc7820c → 0xb3dc38`**. No Scheduler linked entry or bound ActionManager function is manually installed. The original Director initializer's registration suffices: Scheduler **`0x13d3f44`** invokes **`0xd630b8 → 0x9effe0`** three times. Controlled dt values 0, 0.5, 0.5 produce native Node X values **0,150,300**. This advances the earlier 009 action test by removing the supplied Scheduler-to-ActionManager registration, without repeating shutter/result animations.

### F. Absent/empty resource boundary

A fresh constructor/initializer run supplies empty resource bytes. The original lower reader is called for `songs/expedition018/2.aff`; the original loader returns null before whole-file parsing. Scene `+0x3e8` is null, model `+0x3e0` remains null, parser calls 0, model-factory calls 0. Execution reaches the original **`0xe2f0e4`** null-chart branch and stops at its destination **`0xe2fa4c`**.

The following error-reporting/exception path is not executed. This is neither a clean-failure-return assertion nor evidence of a game crash/hang. Null song/difficulty, allocation failure, repeated/partial initialization and special scenes are not tested; such invalid fixtures would not justify production-failure conclusions.

## Synthetic dependency audit: before and after

The initial audit is based on the actually present 017 adapter and its earlier fixture helpers: prepared application/Director/frame surroundings, manual model/chart/timeline/score/delegate/camera wiring, prepared Scheduler registration and gameplay input setup. Their original chart/action/result routines were real, but those internal relationship producers were not all executed. This expedition changes that foundation; it does not withdraw prior scoped findings.

| Dependency | Before 018 integration | Native producer executed in 018? | Remaining substitute / limit |
|---|---|---|---|
| Application context/global root | Prepared singleton and service pointers | No full application constructor | Prepared application/settings/account/audio context remains |
| Director | Prepared singleton/state | **Yes**, `0xa4227c/0x18942c4/0x18b3b6c` | GPU configuration/population and platform Application interface supplied |
| Scheduler | Prepared surroundings/registration around original updates | **Yes**, native ctor and Director attachment | Driver supplies update timing; full platform loop absent |
| ActionManager | Original update, prepared Director/Scheduler link | **Yes**, native ctor, store and `0xdb9674` registration | No manually installed callback/list entry in successful startup |
| EventDispatcher | Native operations, prepared owner/enabled state | **Yes**, native ctor/attachment; enable through native GLView attachment | Platform GLView object remains prepared |
| GameScene | Prepared scene/gameplay context | **Full constructor**, partial original initializer | Scene allocation/entry driver-supplied; HUD/UI initializer omissions remain |
| GameModel | Manually assembled core links around native routines | **Full original factory and ordinary initializer**, called by Scene | No manual core model wiring; special branches not exercised |
| LogicChart | Already native-loaded, manually attached to prepared model | **Existing full loader now called/attached by native Scene/model** | AFF bytes/song/difficulty/resource root still supplied |
| ScoreState / gauge | Native factories with supplied model attachment | **Native model initializer creates and attaches** | Ordinary gauge only; no full account/ability setup |
| GameTimeline | Original mechanics with prepared object/link/epoch state | **Native allocation/init/attachment and Scene start** | Controlled external clock/audio service |
| Spatial index | Native producer with prepared surrounding headers/start | **Whole native model index setup**, 506 producer calls | No manually supplied bucket membership/header vector |
| CameraController | Prepared projection/model link | **Native factory and GameLayer-to-model attachment** | GameLayer visual suffix skipped; brush/framebuffer/graphics supplied |
| Gameplay listener | Native callbacks with prepared registration environment | **Native Scene-triggered construction/registration** | Real Java/GL queue not executed |
| Gauge/touch static globals | Prepared map nodes/strings/header | **Selected original ELF initializers** | Not all global startup constructors executed |
| Audio manager | Supplied | No complete native service startup | Logged/inert audio requests; native timing state remains original |
| Resource/catalog/configuration | Supplied metadata and reader interfaces | Loader consumes them natively | Native song catalog production still outside scope |
| Ending/results scene | Native-produced in 014–017 | Not rerun here | Previous validated chain; missing new scene UI resources preclude claiming whole 017 replay |
| Allocator/pool/thread/runtime | Supplied | Original non-null Ref constructor/retain/release now execute | Free/autorelease draining/threading/external ABI remain controlled |

Concrete removed driver assignments include Scene.model, Scene.chart, Model.chart, Model.timeline, Model.score, Model.delegate, Model.cameraRig, model index headers, model listener, Director scheduler/manager/dispatcher pointers, Scheduler's ActionManager callback entry, dispatcher enabled byte and timeline epochs. Scene storage, external input metadata and graphical facades are still prepared and are not counted as eliminated.

## Recovered pseudocode

```text
# Instruction-backed upstream; menu/loading UI not executed in 018:
SongSelectScene entry (0x10aa678 and related 0xdd0f90):
    collect selected song, difficulty, mode, speed, optional scene state
    allocate GameScene storage (production caller)
    GameScene.constructor(0xe4e4dc, arguments)
    wrap/request loading transition (0x139778c)
    # exact enclosing loading-runtime delivery remains unexecuted

# Executed native startup, with supplied external application/config interfaces:
Director.getInstance(0xa4227c):
    if singleton absent:
        d = native_allocate(0x230)
        native_Director_constructor(d)
        install DisplayLinkDirector type and singleton
        native_Director_init(d):
            d.scheduler = native_new_Scheduler()
            d.actionManager = native_new_ActionManager()
            scheduler.register(original_bound_manager_update,
                               priority=INT_MIN, paused=false)
            d.dispatcher = native_new_EventDispatcher()  # initially disabled
            construct native notification/render/cache CPU objects
    return d

native_setOpenGLView(d, supplied_platform_view):
    retain/store view; copy its real supplied frame size
    [graphics setup omitted at the documented boundary]
    native_dispatcher_setEnabled(true)

# Driver provides scene allocation and constructor arguments, not core links:
native_GameScene_constructor(scene, selected_song, difficulty, ...):
    native_Scene_and_Node_constructors()
    create/attach default camera and base scene listener
    initialize scene fields and embedded gameplay delegate interfaces

native_GameScene_initializer_prefix(scene):
    read supplied account/settings/resource interfaces
    chart = original_complete_chart_loader(selected_song, difficulty, ...)
    scene.chart = retain(chart)
    if chart == null: enter original error branch  # tested only to its entry
    model = original_GameModel_factory(precision, scene.delegate, chart, ...)
        native_GameModel_initializer:
            model.delegate = scene.delegate
            model.chart = retain(chart)
            model.timeline = retain(native_new_GameTimeline(offsets, ...))
            model.score = retain(native_new_ScoreState_and_gauge(chart, ...))
            construct native per-group spatial indexes from runtime objects
            initialize model flags and active/contact vectors
    scene.model = retain(model)
    model.listener = native_create_and_register_gameplay_callbacks(priority=20)
    [HUD visual constructor omitted]
    layer = original_GameLayer_factory_and_initializer_prefix(model)
        controller = native_new_CameraController_with_cameras()
        layer.controller = controller; native_addChild(controller)
        [GameLayer render suffix omitted; original epilogue]
    scene.layer = layer
    model.cameraRig = layer.controller  # original Scene instructions
    STOP before remaining GameScene UI initialization

# Driver requests/advances original CPU lifecycle, not an Android GL queue:
native_Director_replaceScene(d, scene)
native_Director_consumePendingScene(d)
    update scene stack/running/pending natively
    native_Node_onEnter_tree()
    native_GameScene_enterFinished()
        native_model_start_and_timeline_epochs()

for controlled_wall_time, input in fixture:
    native_GameTimeline_update_when_needed()
    native_GameModel_frame(model, scene)  # driver entry, entire model frame
    original_JNI_begin(pointerID, capture_timestamp, x, y, pressure)
        native_GLView_mapping_and_Touch_allocation()
        native_EventDispatcher_and_registered_gameplay_listener()
        native_projection_and_judgment_using_GameTimeline_E()
    original_JNI_end(...)
        native_slot_release_and_gameplay_contact_cleanup()

native_frame_after_chart_end():
    model.finished = true
    original_scene_delegate -> GameScene_completion_handler
    original_snapshot_constructor(scoreState)
    result = scoreState.cachedResult  # +0x68; not assumed X0 return
    STOP before pending/ending/results work
```

## Remaining synthetic dependencies and exact execution boundaries

### Supplied services and hooks

The essential model constructor/initializer, full ordinary chart initializer, scene-to-model stores, timeline/score/gauge creation, index producer, listener registration, controller attachment, native scene-entry state and judgment decisions are original instructions. No binary bytes are patched. PC control changes are the three skips listed above, plus explicit stop boundaries `0xe2f44c`, `0xc27dd0` and the empty-chart test's `0xe2fa4c`.

| Supplied boundary | Actual scope |
|---|---|
| Allocation, libc/libc++ and RTTI ABI | Zeroed 64-byte-aligned bump allocation, memory/string operations, ASCII/numeric/stream services and scoped dynamic-cast support; no host implementation of constructor or judgment branching |
| Reference services | Original Ref ctor `0x121a0ec` and non-null `0x147fe48/0xd6dc98` execute. Null retain/release is tolerated at supplied graphics boundaries; autorelease `0x10ac6e8`, delete/free and pool draining remain supplied/inert |
| Resource parsing ABI | `0x1087f14/0xb06728` stream interface and numeric imports supplied, as in 010; lexer/parser/chart/MD5 native |
| Configuration | `0x18fdcf0` GPU/config population inert; original Configuration constructors/default readers execute; `0x18a6b8c` returns supplied settings backend with default-return interfaces |
| Account/history context | `0xb688e0` supplied account; `0xe2388c` returns null selected context; native history insertion executes; `0x1513c24` returns missing previous best |
| Scene ancillary services | `0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, `0x11b35fc` logged/inert; their complete UI/application-side behavior is outside the claim |
| Resources/storage | `0xb99da4` supplies provider with original vtable; `0xd7845c` supplies AFF bytes; directory interface `0xb9d4a4` returns empty and `0x1a1ad2c` is inert. Original filename/wrapper/cache control executes |
| Audio | Model audio request `0xcff9cc` logged/inert in successful trace; `0x1735d7c` music-start service and judgment sound `0x107af5c` inert. No FMOD hardware output |
| Presentation | Camera brush `0x18dcd1c` null; ordinary judgment feedback `0x7ebcf0` inert twice; completion pause-UI hide `0xfa4320` inert once; skipped visual regions separately inventoried |
| GLView/GL/platform | Prepared original-vtable GLView facade; `0x1929dd0/0x16d80f8/0xf1e53c` GPU services; supplied platform Application getter `0xd7654c` and animation-interval interface |
| Clock/date/thread/random | Controlled steady/system/gettimeofday clocks, fixed result date 1700000000, single-thread pthread services, deterministic random-device value `0x12345678`; no real concurrency/entropy claim |
| Selected import math | Host float32-return math/trigonometric services where imported; native instruction order and object state remain original |

Some adapters expose additional interfaces not visited in the successful trace; their presence is not evidence those branches execute. Original getter `0xbda064` and native no-op `0x19f2e40` execute rather than inheriting their earlier fixture stubs. The old loader's overly broad import-address guard was corrected: actual ELF `.text` continues to `0x1a6d970`; original code in `0x1a6d000–0x1a6d96f` must execute rather than being mislabeled as PLT imports. Executable bytes are unchanged.

### Reproduction outline

Map original ELF PT_LOADs with bias 0 and apply AArch64 RELATIVE relocations. Supply the established ABI services above. Use mapped image `0..0x2100000`, scratch arena starting `0x4100000`, stack SP `0x60df000`, TPIDR_EL0 `0x60f0000`, return sentinel `0x4000100`; per-entry instruction budget 5,000,000 is only an observation limit. Run the three selected native static initializers; prepare explicit external context/metadata/settings/resource inputs. Call native Director singleton and bounded GLView attachment. Allocate Scene storage, execute its full constructor, then its documented initializer subset with precisely the two visual skips. Check pointer identities before activation. Request original replacement, enter original pending consumer, anchor timeline at controlled wall 4001 and execute the described wall/input sequence. Read cached result from ScoreState `+0x68`. Repeat in a fresh instance for direct-callback comparison and empty-resource test; keep the Scheduler/MoveBy ownership test separate.

Temporary harnesses/traces remain outside GitHub publication, as requested. These explicit entries, fixture values, layouts, skips, hook boundaries and observations describe the reproducible native experiment without representing a host reimplementation as native execution.

## Updated integration coverage

| Area | 018 outcome |
|---|---|
| Original menu-to-loading transition | Instruction-backed; not executed |
| GameScene constructor | Native-isolated entry, complete constructor with graphics service boundary |
| GameScene initializer | Native-integrated **subset**, not full successful initializer |
| GameModel factory/ordinary initializer | Native-integrated through real Scene call, full ordinary path |
| Chart/timeline/score/index ownership | Native-integrated, no manual core relationship stores |
| CameraController ownership | Native-integrated constructor and attachment; partial visual GameLayer |
| Director/service construction and ActionManager registration | Native-integrated startup with supplied external configuration |
| Scene activation/start | Original native lifecycle, driver-entered pending consumer |
| JNI begin/end → gameplay/result | Native-integrated on new graph; Java queue absent |
| First frames and chart-end snapshot | Native-integrated original model/Scene callback prefix |
| Full rendered Director loop / complete gameplay UI | Unexecuted |
| Ending/results/SQLite after new bootstrap | Previous 017 evidence only; not rerun |

## Unresolved Mysteries

- Execute the enclosing ordinary SongSelectScene/loading-transition startup without supplied scene allocation/entry. The immediate producers are located; full delivery remains instruction-backed.
- Finish GameScene/GameLayer visual initialization without skipping essential renderer/resource work; establish true full initializer return and first `GameScene::visit` under a normal Director frame.
- Replace application context, selected metadata/settings/account construction and platform GLView facade with their original startup producers. Native catalog loading is not required to explain this result but remains a real boundary.
- Validate constructor allocation-failure/repeated-initialization/error-reporting behavior and full ownership destruction/autorelease reclamation. No production leak or crash claim follows from scoped constructors.
- Rejoin the newly constructed scene to the 017 ending resources/results pipeline. Missing UI suffix work means the previous complete results integration must not be inferred merely from a matching GameResult.
- Special scene/mode/ability branches and gameplay-reachable FlickNote construction remain outside this expedition.

## GitHub Status

Publication base is **`9308f6ef7fac120494da800b68850cb385500879`**, root tree **`258757efddec60fc9b2389e66d40c893fab776d1`**. The authorized publication is exactly this new report and an appended Expedition 018 section in `context.md`; no harness, trace, database, asset, binary or historical-document changes belong to it. The final headquarters response identifies the exact publication commit and pinned document links after readback verification. Historical context must remain an exact prefix and reports 001–017/README must retain their starting blob identities.
