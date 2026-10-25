# Expedition 019 — Native GameScene Resource Initialization & End-to-End Runtime Integration

## Result

**Strong success: the native-owned gameplay world from Expedition 018 and the ending/results lifecycle from Expedition 017 now execute as one continuous controlled ARM64 regression.** One original GameScene constructs its chart, model, camera and presentation objects; Director visitation advances that model; original JNI delivery judges two taps; native completion, resource-loaded GameEnd animation, continuation, results factory, shutter actions and results initialization reach the bundled SQLite engine. Director finally activates NormalGameResultScene and restores EventDispatcher.

The GameScene initializer `0xe2ea48` genuinely returned **1 through `0xe2f948`**. This is a successful return under explicit boundaries, **not complete unmodified visual initialization**: the TrackLayer suffix `0x12968b0 → 0x1297788` remains skipped. The old BackgroundLayer/HUD-region skip was removed. Rendering, textures, several application services and results/shutter UI regions remain supplied or omitted below. Thus excellent/full-visual success is not claimed.

Major removed dependencies are the prepared GameEnd Node proxies, host child/name/action-tag construction, host timeline-to-Node binding, driver-entered model frames, and the bridge between separately prepared gameplay and ending fixtures. No second GameScene/model/result was substituted, no GameSession was fabricated, and no ending, continuation, shutter or closing callback was manually invoked in the successful joined run.

## What I Found

### Evidence scope and source identity

All addresses are main-library ELF virtual addresses before relocation. The unchanged archive has 9,658 members. `lib/arm64-v8a/libcocos2dcpp.so` has SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`.

The introduction, current cumulative context, complete Expeditions 018 and 017, and relevant chart-loading, Director/action and rendering evidence were consulted. Actually available scratch adapters from earlier expeditions were reused and extended; no inaccessible conversation state was presumed recovered. The final joined experiment started with a new Unicorn instance. Preliminary fault/resume probes were diagnostic only. The published joined values come from the subsequent fresh run with services installed before entry, not from stitched diagnostic traces.

Evidence labels used here:

- **Native-integrated:** original instructions execute together through the stated scoped path.
- **Native-isolated:** original code executes with a prepared caller/environment.
- **Instruction-backed:** decoded instructions/RTTI/data establish the relationship without complete enclosing execution.
- **Interpretation:** an explanation grounded in that evidence.
- **Unknown:** not established.

Controlled clock values are experiment inputs, not device latency observations. JNI was entered with synthetic arguments; Java/Android queues and real GLThread scheduling were not executed. Local SQLite writes are not online submission.

## Initial GameScene/GameLayer state

Expedition 018 stopped the enclosing GameScene initializer at `0xe2f44c`, skipped `0xe2f304 → 0xe2f3bc`, and skipped `0x12968b0 → 0x1297788` within the layer initializer. Its chart/model/timeline/score/camera/listener relationships were already native. Expedition 017's ending timing and continuation were native, but its ending visual hierarchy and some bindings were supplied.

RTTI gives useful refinements to the earlier descriptive names; historical reports are preserved:

| Interface/region | Native identity | Evidence |
|---|---|---|
| Factory `0x1877ebc`, initializer `0x12967e4`, scene `+0x3b0` | `TrackLayer`, primary vtable `0x1b92a28` | Native execution and RTTI; called “GameLayer” in earlier descriptions |
| Previously skipped `0xe2f304 → 0xe2f3bc`, scene `+0x3b8` | `BackgroundLayer`, vtable `0x1b46038`; also constructs `BackgroundImage`, vtable `0x1b0aa88` | Native execution; broader than just a life-bar operation |
| Factory `0xa96440`, scene `+0x3c0` | `UILayer`, vtable `0x1af4e98` | Native execution |
| Initializer `0xa3937c`, scene `+0x300` | `GameSceneVisualControlHandler`, vtable `0x1afd288` | Native execution |
| Initializer `0xc03e34`, scene `+0x4d8` | `ClearFinishAnimationLayer`, vtable `0x1b6b980` | Native execution |

These clarifications do not turn a skipped TrackLayer into a fully initialized one.

## Recovered initializer continuation

The successful path executed `0xe4e4dc` and entered the ordinary `0xe2ea48` initializer. It retained Expedition 018's original AFF loader, model initializer, index producer, camera and listener creation. It then executed the formerly omitted BackgroundLayer region and the continuation after `0xe2f44c`.

Important original callsites and ownership operations:

| Callsite or range | Producer/output | Owner/consumer | Observed scope |
|---|---|---|---|
| `0xe2f404 → 0x1877ebc → 0x12967e4` | TrackLayer and CameraController | Scene `+0x3b0`; camera attached by native virtual addChild | Native prefix; rendering suffix still skipped |
| Former `0xe2f304 → 0xe2f3bc` region; `0xaa0400 → 0x100ed9c` | BackgroundLayer/BackgroundImage | Scene `+0x3b8`, native child graph | Executed, no PC skip |
| `0xe2f480 → 0xa96440` | UILayer, in-game UI resources | Store at `0xe2f488` to Scene `+0x3c0`; native virtual addChild at `0xe2f4a4` | Executed |
| `0xe2f574–0xe2f628`, call `0xe2f5d8 → 0xa3937c` | Visual control handler receives actual model, camera, background, TrackLayer and chart | Store Scene `+0x300` at `0xe2f608`, native attachment at `0xe2f628` | Executed |
| `0xe2f674 → 0x95af50` | GameEnd root | Store Scene `+0x3c8` at `0xe2f67c`, original retain at `0xe2f690` | Executed |
| `0xe2f6c0 → 0xd54254` | GameEnd ActionTimeline | Store Scene `+0x3d0` at `0xe2f6c8`, original retain at `0xe2f6dc` | Executed |
| `0xe2f864–0xe2f914`, initializer through virtual dispatch to `0xc03e34` | ClearFinishAnimationLayer | Store Scene `+0x4d8` at `0xe2f904`, native attachment at `0xe2f914` | Executed |
| `0xe2f918–0xe2f948` | Canary check, `W0 = W20 & 1`, real stack/register restoration and RET | Enclosing caller receives 1 | Executed; no epilogue jump |

The continuation also executes normal configuration/scene setup, native UI value propagation, ordinary mode branches and background/presentation queries. Special-mode layers around `0xe2f4b4–0xe2f574`, mode-specific audio preloads and alternative initialization/error paths were not exhaustively tested. Factory failure branches include virtual destruction and null substitution; observing those instructions does not prove every caller tolerates a null product.

Instruction-budget continuation is not a code skip: the initializer needed more than the harness's initial five-million-instruction budget because native fonts/glyphs were now constructed. Three further five-million budgets resumed at the exact stopped PC with CPU/memory state intact. No successful-return register or scene field was supplied to finish it.

## Native resource-loading call graph

**Native-integrated within the resource and joined regressions:**

```text
GameScene initializer
  e2f674 -> 95af50(path)
    -> CSLoader construction 7efae0, registration 18771c8
    -> .csb dispatch 95b0e4 -> 107ff80
    -> provider path / existence / Data interfaces [supplied archived bytes]
    -> 1080070 -> afc688
    -> recursive reader afc7f8 -> aff3f8
    -> native reader factories, Node/Sprite construction and addChild
  e2f6c0 -> d54254(path)
    -> ActionTimelineCache 1312338 -> 121a198 -> f9c42c
    -> unchanged archived Data -> 1a0b5fc -> native timeline clone
```

The asset interface returns a genuine Data-shaped aggregate through X8: pointer `+0`, length `+8`. Path resolution is identity within this controlled archive namespace. Existence queries reflect exact archive membership; raw reads return the exact bytes, or an empty Data value when absent. Provider methods at `0x190bc44`, `0xca7a88`, `0x1730c40` are supplied environment services. Native recursive readers, factories, components, parenting and track binding are not replaced.

CSLoader allocates a `0xc0` object lazily. Native Node creation uses `0x17ec490` and the original Node constructor; native Sprite creation uses `0x86d390` and constructor `0x10204e0`. Root vtable is `0x1b4d3e8`; actual child Sprite vtable is `0x1aa0128`. Native child attachment includes `0x14e9988`.

## GameEnd/HUD/visual resource construction

### Archive inputs actually consumed

Paths below are relative to archive `assets/`; ZIP and resources were not edited.

| Resource | Bytes | SHA-256 |
|---|---:|---|
| `layouts/ingame/end/GameEnd.csb` | 7,380 | `d6b1322d68d011374473afe529180d855c9aa2ac907e09fb95b9f0a4d619b02b` |
| `layouts/ingame/HpBar.csb` | 3,280 | `fceb16374b45d20c5e2b152fbd2ea3805c6c58b3d40dfef33208bf60c8c21031` |
| `layouts/ingame/IngameUILeft.csb` | 1,068 | `c805d9bb672ed95a81c37073bdb503d0577ff998f0dc04bbbfccd9691b651cfa` |
| `layouts/ingame/IngameUIRight.csb` | 7,396 | `822580f96d5097d6af697f567a6919bb42b56536c73f70dfd793bf0d2edf10bd` |
| `layouts/ingame/PauseOverlay.csb` | 7,536 | `07cdd2faa0f2be60a9f9e2413b01ce9c8fd9e58b1b7317df66b1989e42d6bddb` |

The joined trace contains five original `0x95af50` resource loads and one original GameEnd ActionTimeline read at `0x1a0b5fc`. GameEnd bytes were requested separately for visual hierarchy and timeline parsing; this is not two fabricated roots.

Native font setup also consumed archived L2-Regular (708,716 bytes), L2-Semibold (704,656), Exo-Light (98,124), Exo-SemiBold (96,740), GeosansLight (60,072), and Exo-Regular (93,848). Defined FreeType imports were forwarded to their implementations in this ELF, including `FT_Init_FreeType` at `0x18fba08` and `FT_New_Memory_Face` at `0xbcc08c`. Font parsing/glyph work was not replaced by a host FreeType implementation. Empty font-name requests returned empty data and followed native fallback handling.

### Important loader prerequisites recovered

The earlier minimal loader applied only relative relocations. This expedition additionally applied **12,449 defined-symbol `R_AARCH64_ABS64` and 707 defined-symbol `GLOB_DAT` relocations** (`st_value + addend`), and forwarded available same-ELF imported functions unless an explicit boundary already applied. That repairs relocated codecvt/FreeType/reader virtual interfaces without modifying the on-disk executable.

Selected original static initializers matter:

- `0x18931ac` produces the actual `ComExtensionData` name string at `0x1bf6d30` and factory metadata. Without it, a diagnostic CSB load constructed components under an empty name; native timeline enumeration could not find them. Executing the initializer fixed the native lookup; no host renaming was used.
- `0x14c3080` initializes the graphics-context registry list at `0x1bf2278`.
- `0x88a938` and `0x145b1a0` initialize font/cache maps at `0x1bf8328` and `0x1bef818`, including native load factors. Zero-filled headers were not equivalent to those constructed maps.
- Existing Expedition 018 initializers `0x1905bc8`, `0x14c9fe0`, `0x133eedc` remain executed.

The supplied C++ RTTI ABI service was extended to account for Itanium single/multiple/virtual inheritance offsets. It traverses actual native type metadata; it does not unconditionally accept reader casts. Allocator, standard string/stream/numeric/formatting services remain supplied as listed below. This is selective loader/runtime support, not full application ELF startup.

### Graphical resource boundary

The root and all six GameEnd children are native-loaded objects, but artwork/GPU behavior remains controlled. Original empty-Sprite construction creates the built-in white-image texture. A supplied TextureCache file-lookup interface at `0x176b6c4` returns that actual native-created placeholder texture and logs requested names. Some editor texture paths are absent under their logical archive names; native SpriteReader fallback paths execute. Texture dimensions/artwork are therefore not asserted faithful.

GL imports are inert services: unique object IDs, successful shader/link status, zero active introspected uniforms/attributes, locations −1, bounded capability values and no actual GPU work. Original CPU-side Sprite, Widget, Node, component and property logic still executes. Full resolution-directory mapping, sprite-frame caches and actual visual output remain unverified.

## Original Node and ActionTimeline relationships

The joined GameEnd hierarchy is:

| Node name | Native object | Class / vtable | Parent | Action tag |
|---|---|---|---|---:|
| `Layer` | `0x4d29300` | Node / `0x1b4d3e8` | Original GameScene `0x4322600` after ending attachment | Root has no property-track group |
| `Sprite_8` | `0x4d29980` | Sprite / `0x1aa0128` | `0x4d29300` | 952,698,833 |
| `back` | `0x4d2a280` | Sprite / `0x1aa0128` | `0x4d29300` | −974,558,330 |
| `stripeTop` | `0x4d2abc0` | Sprite / `0x1aa0128` | `0x4d29300` | −1,097,685,840 |
| `stripeBottom` | `0x4d2b500` | Sprite / `0x1aa0128` | `0x4d29300` | 1,705,760,127 |
| `mid` | `0x4d2be40` | Sprite / `0x1aa0128` | `0x4d29300` | −421,931,742 |
| `clearImage` | `0x4d2c7c0` | Sprite / `0x1aa0128` | `0x4d29300` | 1,592,711,589 |

Names, ordinary Node tags, action tags and parent pointers came from original readers/attachment code. Ordinary Node tags (root50, children58/51/53/54/56/57) are distinct from action tags. Every node has original `ComExtensionData` and `__ui_layout` components.

Relevant layouts: Node name `+0x160`, ordinary tag `+0x158`, parent `+0x148`, children-header pointer `+0x140`, component container `+0x1c8`. The children vector is reached through that header pointer, not an invented inline field. Component-container map nodes expose key at `+0x10`, component at `+0x28`.

Binding happens when the original ending service starts the action, not by a harness loop during initialization:

1. `0xc7820c` Node::runAction reaches native ActionManager insertion `0xb3dc38` and ActionTimeline::startWithTarget `0xc97694`.
2. Native enumeration `0xa1ce1c → 0x1713774` visits seven nodes.
3. At `0x17137c8`, original `0xdd42b0` looks up `ComExtensionData`; native RTTI and component virtual `+0x78` (`0xe4a360`) recover the archived action tag.
4. At `0x1713958`, Timeline virtual `+0x50` reaches `0x1482d34` **24 times**.
5. That code visits the **85 Frames**, calls their original setNode (`0xd68c24`) **85 times**, and stores the target at **Frame `+0x38`**.

All85 target pointers were read back and belonged to the six actual Sprites above. No name/tag/property-target pointer was installed by the driver. A Timeline object's own `+0x50` is not sufficient evidence of binding; the actual frame targets were checked. The native reader preserves `end` frames0–50 and `out` frames50–80.

## Scene visitation and frame delivery

The fresh test used original Director construction/getInstance, Scheduler/ActionManager/EventDispatcher creation and their native registration established in Expedition018. The platform GLView remains supplied. Initial scene replacement `0x9c90c0` and pending consumer `0xd0dc14` were entered by the driver; their original lifecycle code activated this same constructed scene. No Director running pointer was forced.

Entire `0x1793f8c` calls returned under the render boundaries listed below. The observed original route was Director → Scheduler `0x13d3f44` → registered ActionManager wrapper `0xd630b8`/update `0x9effe0` → scene render `0x1a1319c` → GameScene render `0x15a6814` → base Scene render `0x10dd3d8` → GameScene visit `0x18be2f8`. The call at `0x18be37c` reaches model frame `0x10a7550`.

| Controlled wall ms | Director frame on entry | Scene stamp before/after | Visits / model frames | Effective gameplay E | Observation |
|---:|---:|---|---|---:|---|
| 1,000 | 0 | 0 → 0 | 4 / 0 | 0 | Initial equal counter suppresses model update |
| 4,001 | 1 | 0 → 1 | 4 / 1 | 0 | Native model path establishes music/timeline anchor |
| 5,001 | 2 | 1 → 2 | 4 / 1 | 1,000 | First tap input follows this Director call |
| 6,001 | 3 | 2 → 3 | 4 / 1 | 2,000 | Second tap input follows this Director call |
| 6,122 | 4 | 3 → 4 | 4 / 1 | 2,121 | Original completion delegate and cached result |

Four camera visits naturally exercise the repeated-visit guard. Within each tested Director frame only the first differing-counter visit updates the model; subsequent visits observe the new stamp. Scheduler/ActionManager precede those visits. The driver did **not** call the model frame or timeline-anchor function directly.

The later Director call activating the shutter also visited the outgoing finished scene; this can advance its effective clock without reconstructing its cached result. The cached result pointer remained unchanged. Final results frames execute Scheduler without revisiting gameplay. Native `director_before_update`/`director_after_update` notifications remain custom events, not Android queue drains.

## Expedition 018 → 017 native integration

### Fixture and input provenance

The same original chart-loading chain consumed this complete controlled AFF string:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

Selected song ID is `expedition019`, difficulty2, ordinary mode, supplied speed40/settings and the same ordinary two-tap configuration used previously. Integer AFF lane conversion remains native. Metadata, account/character selection and resource settings are controlled external inputs, not native catalog initialization.

The now-executed HUD requires a localized song title. The supplied metadata includes a valid one-entry `en → Expedition 019` title map at Song `+0x20`, with application locale `en` at App `+0xe8`. An application-status service facade at App `+0x80` supplies zero/absent presentation state. These are explicit additional environment inputs; they are not fabricated model/chart/score/scene connections.

At wall5001 and6001, the driver enters original JNI begin `0xbe31a8` with Android pointer IDs42/43, synthetic captured timestamps987000/987001, pressure0.5, and coordinates `(740,700)` / `(540,700)`. Native GLView allocation/mapping, EventDispatcher, original listener `0x194ff80`, initial input `0xeec024` and tap judgment `0x160ce28` execute. JNI UP `0xdda71c` reaches original cleanup `0xf9a50c`; mapping mask and retained-contact count return to zero.

Both contacts use engine slot0 at different times. Generated gameplay contact identities remain separate; native cleanup releases the first before the second is generated. Android timestamp values do not replace GameTimeline E. Observed native projected ground points match the previous fixture (approximately X±167.1355,Y−185.3521,Z0).

### Continuous original handoffs

| Native entry | Observed caller/return site | Wall ms | Count in joined regression |
|---|---|---:|---:|
| `0xc27d34` GameScene completion | Model call returns to `0x10a7d6c` | 6,122 | 1 |
| `0x1600bb0` cached snapshot | Completion path; authoritative store is ScoreState `+0x68` | 6,122 | 1 |
| `0x19bbdd0` ending callback | Scheduler timer function returns to `0x1875bcc` | 10,122 | 1 |
| `0x1a51054` ending service | Call returns to `0x19bbf74` | 10,122 | 1 |
| `0x147dee8` native continuation | Original function-object dispatch returns to `0x7d6334` | 10,962 | 1 |
| `0xf0b48c` outro | Scheduler timer, `0x1875bcc` | 12,982 | 1 |
| `0x18f11c0` result transition | Scheduler timer, `0x1875bcc` | 13,282 | 1 |
| `0x963094` shutter opening callback | Original CallFunc, `0x189ccf4` | 14,032 | 1 |
| `0x891150` results initializer | Incoming virtual call returns to `0x96311c` | 14,032 | 1 |
| `0xdc2c48` save helper | Original call `0x8921b8`, returns `0x8921bc` | 14,032 | 1 |
| `0x13552d4` score writer | Save helper, `0xdc2cd8` | 14,032 | 1 |
| `0x12a5e60` clear writer | Score writer, `0x1355ab0` | 14,032 | 1 |
| `0x113af20` final transition replacement | Native timer, `0x15986b4` | 14,732 | 1 |

This is one executed object graph. The sole pending-result/account worker boundary at `0x1246c98` is inert in this run; local saving and all listed animation/result handoffs remain original. No queue/network success is claimed.

## Gameplay/result/SQLite regression

Original gameplay produced PURE2, FAR0, LOST0, getter score10,000,002, live health80.4000015258789, integer result health80 and clear category3. The GameResult was retrieved from ScoreState `+0x68`, never from an assumed snapshot return register.

The private database is opened as `:memory:` using **the bundled original ARM64 SQLite engine**. Native schema strings are reused. SQL prepare/bind/step/finalize and subsequent readback execute original SQLite. No user's application database, file-backed score database or server was used.

Readback:

```text
scores:
  id=1, version=1, score=10000002,
  shinyPerfectCount=2, perfectCount=2, nearCount=0, missCount=0,
  date=1700000000, songId="expedition019", songDifficulty=2,
  modifier=0, health=80, ct=0
clearTypes:
  id=1, songId="expedition019", songDifficulty=2, clearType=3, ct=0
```

The date is supplied wall-calendar input through the proper `time(time_t*)` ABI. A preliminary run exposed an adapter that returned the time but failed to write through the non-null pointer passed at `0x1600bf8`; its stale-stack date was rejected as harness evidence. The service was corrected and the entire joined regression rerun from fresh state. The final snapshot reads the native-written local at `0x1600cec`, and the stored date above is verified. This was not a change to score/result decision logic.

The ordinary save-gate producer `0x89164c–0x891684` and branch `0x89219c–0x8921dc` execute unchanged. Neither scene byte `+0x2f8` nor result save-control bytes were assigned by the driver. SQLite writers were entered only from the original initializer/helper call chain. Their previously established replacement matrices were not redundantly re-tested.

## Object identity and ownership

Addresses below are observed emulated allocations, not ELF addresses or portable allocation promises.

| Object | Joined-run pointer | Native relationship verified |
|---|---|---|
| GameScene | `0x4322600` | Constructed once; remains the same source scene through ending |
| GameModel | `0x434e240` | Scene `+0x3e0`; original initializer/factory |
| LogicChart | `0x4329b80` | Scene `+0x3e8` equals Model `+0x28` |
| GameTimeline | `0x434e3c0` | Model `+0x30`, native construction |
| ScoreState | `0x434e400` | Model `+0x38`, native construction |
| GameResult | `0x4d4a800` | ScoreState `+0x68`, preserved through all later calls |
| GameEnd root / timeline | `0x4d29300` / `0x4d347c0` | Scene `+0x3c8` / `+0x3d0`, native resource producers |
| GameSession | `0x4d51b00` | Original result transition; `+0x18` equals `0x4d4a800` |
| NormalGameResultScene | `0x4d51c00` | `+0x2e8` equals native GameSession |
| TransitionShutter | `0x4d52740` | Native factory; incoming `+0x2e8` is result scene, outgoing is original GameScene before callback release |
| Director | `0x4104540` | Original singleton producer |
| Scheduler / ActionManager | `0x4107c80` / `0x4108300` | Director `+0xa0` / `+0xa8`, original creation and registration |
| EventDispatcher | `0x41086c0` | Director `+0xb0`, original creation |

The continuation registration at `0x1858c3c`, caller `0x1a516e0`, observes wrapper `0x4d511c0` and continuation `0x4d511e0`; both captured scene identities equal `0x4322600`. At actual `0x147dee8` entry the capture still equals that original scene.

Original retain/release arithmetic executes for valid native objects. For example, GameEnd root and timeline are retained from the initializer and again as the ending graph/action is attached; result retain calls accompany caching/completion and native GameSession/result-scene construction. Outgoing-scene release runs during shutter callback/lifecycle, rather than a host pointer swap. Null environment references are inert. Autorelease insertion and actual heap reclamation remain supplied; reference counts alone do not establish complete destruction or leak freedom.

## Timing, repetition and final scene state

Original Scheduler is driven with explicit dt values; this is a controlled runtime schedule, not measured Android frame delivery.

After completion, `[0,4]` lets the original ordinary ending timer fire. Ending ActionTimeline observations:

| Wall ms | Additional dt | Native frame | Playing | Continuation entries |
|---:|---:|---:|---:|---:|
| 10,122 | registration, then0 | 0 | 1 | 0 |
| 10,522 | 0.4 | 23 | 1 | 0 |
| 10,922 | 0.4 | 47 | 1 | 0 |
| 10,952 | 0.03 | 49 | 1 | 0 |
| 10,962 | 0.01 | 50 | 1 | 1 |
| 10,982 | 0.02 | 50 | 0 | 1 |

Original ActionTimeline frame-end delivery invokes `0x1677270` and `0x147dee8`; no driver callback bridge exists. Subsequent dt2 and0.3 produce the native outro/scene-change timers. Director's full original frame activates the pending shutter. Opening `[0,.25,.25,.25]` reaches CallFunc, initializer and save. Closing/reveal `[0,.2,.2,0,0,.1,.1,.1,0]` reaches native final replacement.

At wall14732 the final original Director frame produces:

- Running scene `0x4d51c00` (NormalGameResultScene).
- Pending scene null.
- Scene stack exactly `[0x4d51c00]`.
- EventDispatcher enabled byte `+0x124 = 1`.

Further Scheduler dt `[0,.25,1,5]` and an additional Director frame preserve those states and the exact SQLite rows. Continuation, shutter opening callback, result initializer, save helper and both writers each remain at one entry. Native completion is not inferred unique merely from equal-score database behavior.

Some original outgoing UI and ending actions remain in ActionManager as paused entries after scene exit, including the stopped GameEnd ActionTimeline. This is observed retained state under a supplied autorelease/reclamation environment, not proof of a leak. Complete transition cancellation on this new full graph and no-hit replay were not repeated; Expedition017's isolated cancellation evidence is preserved, not relabeled as a new joined cancellation test.

## Dependency audit: before and after

| Dependency | Expedition018/017 boundary | Expedition019 result | Remaining boundary |
|---|---|---|---|
| GameScene constructor | Original | Preserved | Driver allocates storage/enters constructor |
| GameScene initializer | Stopped at `0xe2f44c` | Genuine return1 after original suffix | Inner TrackLayer skip; application/platform interfaces |
| Background/HUD region | `0xe2f304 → 0xe2f3bc` skipped | Entire region executed | Texture/artwork fidelity |
| GameLayer/TrackLayer | Original prefix/camera, skipped visual suffix | Prefix preserved; suffix decoded and bounded separately | `0x12968b0 → 0x1297788` remains in joined run |
| UILayer, HP bar, pause overlay, clear-finish layer | Not reached in018 | Native factories/loaders/attachment executed | Some account/presentation services inert |
| Chart/model/timeline/score/index/listener | Native-owned in018 | Preserved in same scene through completion | Controlled metadata/configuration |
| GameEnd root/children | Prepared Node proxies in017 | Original CSLoader creates Node + six Sprites | Placeholder textures/GPU |
| Names/components/action tags | Prepared/link-assisted | Original CSB readers/static initialization | ABI services only |
| GameEnd property tracks | Native parsed in017 | Preserved, original reader + clone | Raw archive provider |
| Track-to-Node relationship | Host-installed in017 | Native enumeration/component lookup/setNode, all85 verified | No host property-target assignment |
| Model updates | Driver-entered model frames in018 | Entire Director frame reaches original visit/model call | Render boundaries; driver controls time and frame entry |
| Ending/results runtime | Separate prepared fixture | Joined to actual native-created scene/model/result | Results UI/shutter artwork skips retained |
| SQLite | Original engine/writers | Original results initializer invokes same engine | Private memory DB, allocator/OS services |
| Director/engine services | Native production in018 | Preserved | Supplied platform GLView; selected startup initializers |
| Account/catalog/settings/audio | Prepared services | Explicit and audited | Still supplied; pending submission inert |
| Autorelease/allocator | Supplied | Still supplied | No full reclamation claim |

## Exact PC skips and supplied services

### PC redirections in the successful joined experiment

Ranges use source-PC → resumed-PC notation; no omitted instructions in them are claimed executed.

| Redirection | Missing work/state | Consequence |
|---|---|---|
| `0xf72110 → 0xf72158` | Existing controlled GLView attachment/platform setup boundary from018 | Native Director/service creation and subsequent attachment/lifecycle execute; platform view startup not complete |
| **`0x12968b0 → 0x1297788`** | TrackLayer visual suffix: TrackBase children, additional track/render resources, caches and presentation objects | Track/camera prefix retained; TrackLayer graphical update must remain inert |
| `0x16a4238 → 0x16a48d8` | Shutter graphic-panel creation | Two supplied original-constructed Node panels installed at shutter `+0x300/+0x308`, width100; action/control logic original |
| `0x121581c → 0x121584c` | Shutter loading overlay | No full overlay resource/layout claim |
| `0x891190 → 0x89164c` | Results initializer leading UI/account region | As before, boundary also supplies X28=application global address and X26=FP−0x60; original gate producer executes |
| `0x891688 → 0x89219c` | Results UI/layout/progression region | Original save-eligibility branch/helper call preserved |
| `0x8921dc → 0x8928e0` | Results initializer trailing UI/progression region | Ancillary call at8921dc is logged/inert; saving already occurred |

**Removed:** the old `0xe2f304 → 0xe2f3bc` skip. **Not present:** an `0xe2f44c` stop, a jump to GameScene's successful epilogue, a host GameEnd construction/binding loop, or manual calls to `0x147dee8`/`0x963094`/closing callbacks/SQLite writers.

### Whole-function/native-interface boundaries

These are separately disclosed even where they are convenient services inside this ELF; an inert native interface is not an externally executed subsystem.

| Group | Hooked native addresses / behavior |
|---|---|
| Scene initialization ancillary application/presentation interfaces | `0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, `0x11b35fc` return0/inert; `0x14ac9c4` returns no catalog background override |
| Render/frame boundaries | `0x19069a0` TrackLayer graphical update; `0x129c924` base traversal/draw boundary; `0x13edf0c` framebuffer-registry clear; `0x1017a84` platform swap callback are inert. GameScene guard, HUD updates, camera/Scene render traversal to the override, model frame and Director counter remain original |
| Completion/account/presentation | `0x1186f70`, `0xc464e4`, `0x19becc0`, **`0x1246c98`** pending-result processor return0; no completion queue/worker execution claim |
| Results/transition ancillary services | `0x1019c18`, `0x1049858`, `0xc800b0`, `0x9d2518`, `0x9c8190`, `0xacf898` inert; native results/context/transition factories and callbacks execute |
| Audio/feedback | `0x1735d7c` playback start and `0x107af5c` SFX inert; configured feedback boundaries `0x7ebcf0`, `0x1715728` not entered in this successful trace; `0x18dcd1c` clock/audio-adjacent service inert |
| Existing bootstrap/platform interfaces | `0x18fdcf0`, `0x1929dd0`, `0x16d80f8`, `0xf1e53c`, `0xcff9cc` inert; `0xd7654c` supplies platform application interface |
| Account/settings/resources | `0xb688e0` supplies controlled account; `0x18a6b8c` settings backend; `0x1513c24` absent optional resource state; `0xb99da4` asset provider; `0xd7845c` supplies AFF/archive strings; `0xb9d4a4` empty optional path. Opaque provider/status virtuals and control virtual `+0x508` are inert |
| Asset/texture services | `0x190bc44` path, `0xca7a88` existence, `0x1730c40` exact archive Data, `0x176b6c4` native placeholder texture. No CSLoader reader/parent/tag/Frame.setNode substitute |
| Lifetime | `0x10ac6e8` autorelease insertion inert; allocator/free/realloc supplied; non-null Ref retain/release execute original arithmetic, null references return safely |
| AFF standard runtime | Existing `0x1087f14` stream adapter and `0xb06728` stream cleanup boundary, C++ strings/streams/numeric conversions supplied. AFF header/body parsing and chart building remain original |

Hooks at `0x9ff610` and `0x9c90c0` only observe actual objects; they neither return early nor change PC. Hook-entry bookkeeping can count an observation twice through layered instrumentation; callback counts in this report use the single original-entry event stream. The resource and gameplay call counts above likewise distinguish actual execution from observer mechanics.

Host ABI services include allocation/memory, C++ string copy/append/substr/compare/reserve/insert/rfind, formatting, character/numeric conversion, RTTI traversal, setjmp/longjmp state when required, mutex/TLS/once environment support, clocks, math and GL stubs. Newly supplied checked strlen/strstr/realloc/malloc-size and AArch64 va_list formatting support preserve their service contracts rather than replacing game decisions. Defined imported FreeType and other available library implementations execute original code. SQLite native APIs are forwarded to this ELF, not implemented with host SQL.

The underlying monotonic clock, C++ wall/system-clock interfaces, Java event timestamp and GameTimeline E are separately supplied/observed. `time(time_t*)` returns and writes1700000000; no Java event timestamp is used as gameplay E. GPU status success is an explicit environment response, not shader-validation evidence.

## Native bootstrap execution recipe

The final successful run used one fresh little-endian ARM64 Unicorn memory image with original PT_LOAD bytes, relative plus the defined-symbol relocations described above, zeroed supplied allocations and controlled TLS/stack. Emulated heap starts at `0x4100000`; object addresses are observations of that allocation order. Native function calls return to a harness sentinel; no sentinel substitutes a game callback.

1. Supply application/settings/account/resource interfaces; execute the seven selected static initializers listed above. Call original Director getInstance, then its original GLView attachment interface with the controlled1280×720 view and declared platform skip. Native engine singleton/service relationships are not written by the driver.
2. Supply the selected metadata/difficulty and complete AFF string. For the GameScene constructor `0xe4e4dc`, X0 is newly allocated zeroed `0x4e0` storage, X1 is the selected song pointer, X2–X7 are respectively `2,0,0,0,40,0`. Caller-stack arguments at offsets `0,8,16,24,32,40` are respectively `1,0,0,0,0,100`. These are scoped ordinary startup inputs, not claims of every constructor parameter's meaning. Enter original initializer `0xe2ea48(scene)` at clock0; require actual return1. Only the TrackLayer PC skip in the table applies inside this initializer.
3. Enter original `0x9c90c0(director,scene)` and `0xd0dc14(director)` at wall1000. Invoke the entire original Director frame at the five gameplay wall times in the visitation table. Deliver the two scalar JNI begin/end pairs after the5001/6001 frames. No model/timeline/judgment entry is called directly by the driver.
4. Require the native cached result and counters stated above, then drive original Scheduler dt values from the timing table. The native completion-registration owner and native property targets must come from the scene, not from a separate prepared ending fixture.
5. Let native result-transition code create session/result scene/shutter. Enter whole original Director frames to consume pending activation, drive opening/reveal/closing with the stated dt list, and enter Director again to consume final activation. Keep the declared results/shutter UI and external service boundaries stable.
6. Check pointer equalities, native callback-entry counts, all85 Frame targets, running/pending/stack/dispatcher fields, and original SQLite readback. Add the extra updates and repeat those assertions without modifying the objects.

The fresh final regression passed all six steps without an unsupported-service fault or diagnostic PC restart. Earlier instruction-budget extensions resume exactly at the current PC and do not manufacture an initializer return. The missing-resource and full-TrackLayer diagnostic tests are separate scopes.

## Controlled failures and bounded remaining TrackLayer investigation

**Missing CSB, native-isolated:** a fresh resource test supplied empty Data for `layouts/ingame/end/Missing019.csb`. Original `0x95af50 → 0x107ff80` reached the missing-resource logging branch (`__android_log_print` return site `0x108000c`) and returned **null**. Logger was inert; no replacement Node was invented. Actual Data-reader return site was `0x1080024`. This does not establish whole-GameScene error recovery for a missing required asset.

**Missing localized title, diagnostic:** incomplete supplied song metadata caused original title lookup `0x10f0330` to try the `en` fallback and throw native `std::out_of_range`. The final test supplies the documented valid title map before initialization. This is an invalid research input boundary, not evidence of a production title bug.

**TrackLayer suffix, native-isolated/instruction-backed:** decoded code creates TrackBase objects (vtable `0x1aa1050`) through `0xa5d3dc`, stores/attaches them from the vector at TrackLayer `+0x300`, and constructs additional resources/vectors around `+0x330`, auxiliary Node `+0x350`, and Sprites at `+0x358/+0x360/+0x368/+0x370`. Those outputs are consumed by its graphical update; that explains why merely retaining the native camera does not complete visual state.

A bounded diagnostic factory call with the actual model/song/difficulty-related arguments removed that suffix skip and entered native TrackBase setup. It required a `sincosf` OS math service, then pthread condition notification, and stopped at an unimplemented **`newlocale` import `0x1a7c950`, callsite `0x18c04c8`** (eventually reaching the unresolved PLT resolver). Earlier probes were resumed only to locate these interfaces. No successful full TrackLayer return is claimed. A first incorrectly typed isolated argument was discarded; it is not a production failure observation. Completing locale/material/render-resource support is a bounded next infrastructure question, not a reason to claim a necessary GPU blocker or fabricate a successful TrackLayer.

**Time-service diagnostic:** the time pointer ABI correction and complete rerun are described above. Partial diagnostic outputs are excluded from final continuity/date claims.

## Recovered pseudocode

The following is instruction-backed pseudocode for the routines and branches actually identified. `[native]` denotes original execution in the joined experiment; `[service]` is supplied environment; `[skip]` is explicit omitted code. Driver calls are marked separately.

```cpp
// Driver supplies app/config/account/metadata, clock, raw resources and platform GLView.
// It executes selected original ELF static initializers, not the full Android startup.
director = Director::getInstance();                         // native construction/services
Director::setOpenGLView(controlledView);                    // native, declared platform skip
sceneStorage = allocator(sizeof(GameScene));                // service
GameScene::GameScene(sceneStorage, song, difficulty, ...);  // native e4e4dc
ok = scene->init();                                         // native e2ea48
// No driver writes scene.model / model.chart / model.score / model.timeline.

bool GameScene::init() {
    // original chart/config/model/index/listener path from018:
    chart = loadChartThroughOriginalAFFPipeline(...);        // native, service bytes/settings
    model = GameModel::create(..., chart, ...);              // native c9f6f0 / fbfd04
    background = createBackgroundLayerAndImage(...);         // native; old skip removed
    track = TrackLayer::create(model, ..., song, ...);         // native prefix
    // skip12968b0 ->1297788: TrackBase/rendering suffix not executed here
    ui = UILayer::create(song, difficulty, chart->end, ...);  // native a96440 + archived CSBs
    addChild(ui);                                          // native
    visualHandler = createVisualControl(model, track->camera,
                                         background, track, chart); // native
    addChild(visualHandler);
    endingRoot = CSLoader::createNode("layouts/ingame/end/GameEnd.csb");
    retain(endingRoot);                                     // native store+3c8, retain
    endingAction = loadActionTimeline(samePath);             // native parser/clone, store+3d0
    retain(endingAction);
    // ordinary configuration and original finish-layer construction/attachment
    return nativeBaseStatus & 1;                            // actual epilogue returned1
}

Node* loadCSB(path) {
    Data bytes = provider.read(path);                        // service: unchanged archive
    if (nativeMissingResourceCondition(bytes)) return nullptr;
    // native recursive readers:
    node = nativeFactory(archivedType);                      // actual Node/Sprite/Widget
    readNativePropertiesAndComponents(node, archivedOptions);// name, tags, ComExtensionData
    for (childOptions : archivedChildren)
        node->addChild(loadChildNative(childOptions));       // native hierarchy/reference ops
    return node;
}

// Driver enters whole original Director frame with controlled clock.
Director::drawScene() {                                     // native1793f8c
    dispatchNativeBeforeUpdateNotification();
    scheduler->update(dt);                                  // native ActionManager registration
    dispatchNativeAfterUpdateNotification();
    consumePendingSceneIfNeeded();                          // native lifecycle
    runningScene->render(...);                              // native camera traversal
    // GPU/base-draw/swap boundaries remain supplied
    ++directorFrameCounter;                                // native
}
GameScene::visit(...) {                                     // native18be2f8
    if (lastFrameCounter != Director::frameCounter) {
        model->frame(this);                                 // native10a7550 via18be37c
        lastFrameCounter = Director::frameCounter;
    }
    updateNativeHUDAndSceneState();
    // TrackLayer graphical update and base draw traversal inert
}

// Driver supplies JNI arguments after selected Director frames.
JNI_begin(pointerID, timestamp, x, y, pressure) {             // nativebe31a8
    nativeGLViewMapAllocateUpdateTouch(...);
    originalEventDispatcherAndGameplayListener(...);
    originalProjectionCandidateJudgmentUsingGameTimeline();
}
JNI_end(...) { nativeGLViewReleaseAndGameplayCleanup(...); } // nativedda71c /f9a50c

// Completion is reached from that same model and same GameScene.
GameScene::completed() {                                    // nativec27d34
    originalCompletionLatch();
    scoreState->makeCachedResult(...);                       // native1600bb0
    result = scoreState->cachedAt0x68;
    pendingAccountProcessing(...);                          // service1246c98, no queue claim
    originalSchedule("endingAnimation", ordinaryDelay4s);   // nativee5c700
}
endingTimerCallback() {                                     // native19bbdd0, Scheduler invokes
    continuation = nativeFunctionCapturing(thisScene);       // original type/body147dee8
    endingService(continuation);                             // native1a51054
}
endingService(fn) {
    attachOriginalLoadedEndingRootAndRunAction();            // native; no proxy hierarchy
    // ActionTimeline::startWithTarget native traversal:
    for (node : nativeEnumeration(root)) {
        ext = node->getComponent("ComExtensionData");        // native component-name producer
        for (timeline : matchingNativeActionTag(ext))
            for (frame : timeline.frames)
                frame->setNode(node);                       // native Frame+38;85 verified
    }
    originalAnimationCompletionRegistration("end", fn);     // native1858c3c
    originalPlayNamedAnimation("end");                      // frames0..50
}
// Driver advances Scheduler dt; it never invokes the continuation.
ActionTimeline::step(dt) {                                  // native original action execution
    advanceAndApplyOriginalPropertyFrames(dt);
    if (originalFrameEndConditionReached())
        originalStoredFunctionDispatch();                   // native1677270 ->147dee8 once
}
continuation147dee8() { originalScheduleOutro(2s); }          // native
outroCallback() { originalPlayOutAndScheduleSceneChange(); } // nativef0b48c, out50..80
sceneChangeCallback() {                                     // native18f11c0
    session = originalGameSessionFromCachedResult();         // original result pointer retained
    resultScene = originalResultSceneFactory(session);       // native normal scene
    shutter = originalTransitionShutter(resultScene, .75f);
    Director::replaceScene(shutter);                         // native request
}
// Whole original Director frame activates shutter; original actions invoke963094.
shutterOpeningCallFunc() {
    originalOutgoingExitAndRelease();
    incoming->initializeResults();                          // virtual+4d8 ->891150
    // declared results UI skips surround, but do not replace:
    originalSaveGateProducer();
    if (originalSaveGateAllows())
        originalSaveHelper(session);                        // dc2c48 ->13552d4 ->12a5e60
        // bundled ARM64 SQLite against private :memory: DB
    originalRevealAndClosingTimersAndActions();
}
// Native closing action/timer requests final scene; driver enters Director frame.
Director::consumePendingScene() {
    originalExitCleanupEnterTransitionFinished();
    // observed final running=resultScene, pending=null, stack=[resultScene], dispatcher=1
}
```

## Remaining synthetic dependencies and unresolved mysteries

1. TrackLayer visual suffix and its locale/material/render-resource initialization remain incomplete in the joined run. The real enclosing GameScene return1 must not be read as proof those omitted objects exist.
2. Textures, artwork resolution/sprite-frame caches, framebuffer registry and GPU draws remain controlled. A visible faithful game screen was not produced.
3. Results initializer UI/progression regions and shutter graphic panels/loading overlay retain earlier boundaries. The native gate, callbacks, lifecycle and writers are preserved, not the complete results layout.
4. Application/account/catalog/settings objects are still prepared services. Added title/status inputs are external metadata/state, not proof of full song catalog or application startup.
5. Pending submission processing/worker startup is suppressed at its explicit native interface. No new network/queue eligibility result is claimed.
6. Allocator/autorelease-pool reclamation and complete teardown of paused outgoing actions are not established. No memory-leak conclusion follows.
7. No real Android queue, physical timing distribution, hardware sound, actual results-button hit testing, special-mode survey, or FlickNote construction was investigated.
8. Cancellation with the new complete ending hierarchy, broader missing-required-resource propagation, and a no-hit joined result are not executed here. Existing historical evidence remains separate.

## GitHub Status

Default branch `main` and absence of Expedition019 were verified before investigation and rechecked before publication. Starting/parent commit: **`1a7c8203148335f04fe80611b185e8fb5e0d6c37`**; starting root tree `6e6142082332b9a3fe2289b652758caeddb6d6f6`.

Only this report and an append-only Expedition019 section in `context.md` are authorized publication changes. The exact publication commit is the commit containing this report, returned with pinned report/context links in the headquarters handoff. Publication uses an expected-head lease; committed contents, historical-context prefix and unchanged historical blobs are checked after branch advancement. No harness, log, database, binary or resource is included. Historical reports are preserved; naming refinements and harness ABI corrections are recorded here instead of rewriting them.
