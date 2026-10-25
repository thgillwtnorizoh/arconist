# Expedition 020 — TrackLayer Completion, Locale ABI & Native Rendering Foundations

## Result

**Strong success, with a continuous completion/results/SQLite extension.** The entire ordinary TrackLayer initializer executes inside original GameScene initialization, including the previously skipped `0x12968b0–0x1297788` suffix, and genuinely returns1. The native TrackLayer graphical update `0x19069a0` also executes completely in the tested path. Both former boundaries are removed from the successful fresh bootstrap.

The resulting scene owns an original TrackBase, CameraController, supporting Nodes/Sprites, note-renderer collection and NoteBurstRenderer/particle systems. Director-driven gameplay and JNI input remain functional. The same native scene/model/result continues through GameEnd ActionTimeline, native continuation, GameSession/results construction, TransitionShutter, original save gate, bundled SQLite and final Director activation. Result: PURE2/FAR0/LOST0, score10,000,002, live health80.4000015258789, stored integer health80, clear3.

This is **CPU-side native construction and update success**, not graphical reproduction. Base draw/child traversal, actual GPU work, texture artwork, selected application/account services, results UI regions and complete reclamation remain bounded. A newly exposed zero-dimension placeholder-texture problem was traced and corrected through an original pixel-format registry initializer plus an explicit GPU-capability service; the final regression has finite inspected track transforms.

## What I Found

### Evidence and source integrity

All native code addresses are main-library ELF virtual addresses before relocation. Heap pointers in tables are observations from a controlled allocation order, not ASLR addresses or stable API values.

- Starting `main`: `fabbe7cda54f4652a0986352b10284d7507d17a8`; default branch main; no020 publication present.
- Binary: `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`.
- Archive:9,658 members, unchanged; original archived resources were used at the supplied provider boundary.
- The introduction, latest context and019 report were read. Relevant018 bootstrap,017 ending resources,007 camera/visual objects and009 scheduling evidence were consulted. Available scratch adapters and saved traces were reused. A live diagnostic emulator was not recoverable after conversation continuation; its saved outputs remained available. Final integration was rerun in a new emulator instance rather than inventing recovered live state.

Evidence categories: **Native-integrated** means original routines execute together through the stated scoped chain; **Native-isolated** means original code executes with a prepared enclosing caller/environment; **Instruction-backed** denotes decoded code/RTTI/data without complete enclosing execution; **Interpretation** is a grounded explanation; **Unknown** is not established. External ABI adapters are supplied services, never described as native Bionic execution.

The authoritative final joined run completed without an unsupported-service fault or diagnostic PC restart. Earlier fault/resume probes located missing services; they are not stitched into that run. Instruction-budget extensions resume at the current PC with unchanged CPU/memory state and are not initializer skips.

## Initial TrackLayer blocker and exact skipped path

Expedition019's successful scene initialized the TrackLayer/camera prefix but redirected `0x12968b0 → 0x1297788`. It also replaced `0x19069a0` with an inert interface. The omitted suffix constructs more than a decorative track bitmap: it builds TrackBase, retained Sprite vectors, chart render objects and particle/render-support Nodes consumed by subsequent scene updates.

The starting diagnostic reached `newlocale` at import `0x1a7c950`, native callsite `0x18c04c8`, after encountering `sincosf` and a pthread condition broadcast. These were external-runtime boundaries, not evidence that native TrackLayer logic was wrong.

A naming refinement: **`0xa5d3dc` is the TrackBase initializer body**, called on already allocated native storage. TrackLayer's original instructions allocate `0x3a0`, execute the Node constructor, install TrackBase vtable `0x1aa1050`, then call this initializer through the vtable. It is not itself an allocation factory. The input prompt's “TrackBase factory” label should be read with this refinement; historical files are unchanged.

## Locale ABI and runtime-service recovery

### Original call and actual consumers

At `0x18c04b8–0x18c04c8`, original libc++ locale/facet initialization sets:

```text
W0 = 0x1fbf
X1 = 0x539f57 -> C string "C"
X2 = null
BL 0x1a7c950  // newlocale
```

`0x18c04cc` stores the returned locale handle at the original enclosing static/facet location addressed by X21+0x50. `0x18c04d8` completes the original guard-release operation, and control rejoins at `0x18bf208`; `0x18bf20c` reloads the stored handle and `0x18bf21c` propagates it into another original facet/static field. This is native libc++ setup reached by original construction, not a custom TrackLayer locale flag.

The final run observes one `newlocale` call and no native reads inside the returned8-byte OS locale object. It is stored as an external handle in the executed path. `uselocale` and `freelocale` do not occur in that joined run, so successful startup does not establish all future locale consumers or teardown.

### Adapter contract and representation

The supplied service follows the relevant Android C-locale ABI: a mapped emulated locale object with `size_t mb_cur_max=1` for `C`/`POSIX`, rather than an unmapped host pointer or arbitrary success flag. UTF-8 names supported by the adapter use4. A registry tracks handle identity and lifetime. Invalid mask/null name returns null with EINVAL22; unsupported name returns null with ENOENT2. Success does not clear an earlier errno. `uselocale(0)` queries, a non-null handle replaces thread-local selection and returns the prior selection, and `LC_GLOBAL_LOCALE` is pointer−1. Free marks the service handle inactive; underlying research allocator reclamation is separate.

The representation and mask were checked against primary Android sources: [Bionic locale.cpp, android-12.0.0_r1](https://github.com/aosp-mirror/platform_bionic/blob/android-12.0.0_r1/libc/bionic/locale.cpp) and [locale.h](https://github.com/aosp-mirror/platform_bionic/blob/android-12.0.0_r1/libc/include/locale.h). That version documents a one-size_t locale object, the C/POSIX/UTF-8 names and the category masks summing to0x1fbf. It supports the scoped service contract; it is **not identification of the actual device's libc build**. The bundled main library remains behavioral authority for its caller and consumers.

### New service evidence table

| Import/interface | Native callsite and input | Return/consumer | Supplied behavior and validation | Limits |
|---|---|---|---|---|
| `newlocale`, `0x1a7c950` | `0x18c04c8`; W0=0x1fbf, X1 points to raw `C`, X2=0 | X0 locale_t; original store at18c04cc and reloading/propagation after18bf208 | Mapped8-byte object, mb_cur_max1; one actual native request; initialization proceeds | No native in-object read, alternate locales and allocation failure in this enclosing native path untested |
| `sincosf`, `0x1a6e1b0` | e.g. `0xd41698`, `0xd416ac`, `0xd416c0`; float argument S0, output pointers X0/X1 | Void, float32 values written through pointers; original quaternion/rotation consumers | Host sin/cos with f32 stores;66 calls in final joined run. Example input−0.7853981852531433 gives sin−0.7071067690849304 and cos0.7071067690849304 | Not a bit-for-bit validation against device libm for all inputs |
| `pthread_cond_broadcast`, `0x1a7c5c0` | `0x87d530`, condition address0x1bf0f68 in native libc++ once setup | W0 status; original once/control code continues | Return0 with no waiting worker threads in the single-thread harness;28 calls | No real thread wakeup or contention behavior |
| `strncmp`, `0x1a6e5f0` | `0xf1b3ec`, original XML/plist parser | W0 lexical comparison, NUL/length bounded | Standard byte comparison;12 calls, archived particle plist parsing continues | General libc not reconstructed |
| Maximum-texture capability getter `0x1589238` | `0x10f711c`; native Configuration object | W0 maximum dimension; native image-width/height validation | Explicit controlled capability4096; no TrackLayer field assignment | Hardware capability setup itself remains supplied |

`uselocale` import `0x1a7c960` and `freelocale` `0x1a7cd20` have coherent supplied service contracts but are not entered by the final native bootstrap. Native `__ndk1::__call_once` and locale constructors/virtuals already defined in this ELF continue to execute; only their external synchronization/OS interfaces are bounded.

### Scoped ABI contract checks

Separate service-boundary tests, **not native Bionic tests**, observed:

| Input | Output |
|---|---|
| newlocale(mask0x2000, `C`, null) | null, errno22 |
| newlocale(mask0x1fbf, unsupported name, null) | null, errno2 |
| newlocale(mask0x1fbf, `C`, null) | mapped handle with mb_cur_max1; previous errno2 retained |
| query → select handle → query → restore global | returns −1, −1, handle, handle |
| free that test handle | registry lifetime becomes inactive |

A preliminary service test passed a std::string object instead of a C-string data pointer and was discarded/corrected. The production native call uses the original raw `C` pointer and was unaffected. These tests do not prove the native locale initializer handles a newlocale failure gracefully; that surrounding error path remains untested.

## TrackBase construction

### Production chain and arguments

**Native-integrated in the final GameScene run:**

```text
GameScene initializer e2ea48
  e2f400 -> TrackLayer factory1877ebc
    allocation0x3f0 -> base constructor16917cc -> TrackLayer vtable1b92a28
    1877f80 -> initializer12967e4
      native base initialization16567ac
      store original model at TrackLayer+2f0
      copy native song ID/string input
      1296894 -> CameraController factory1393474, native attachment
      [NO12968b0 skip]
      native TrackBase allocation0x3a0, Node constructor131419c, vtable1aa1050
      12969fc -> virtual initializer a5d3dc (ordinary branch)
      native success/autorelease/container insertion/addChild
      remaining original track resource/pool/node/particle construction
      actual return12977c0 ->1877f84, W0=1
    factory returns actual TrackLayer to GameScene
  native attachment through intermediate scene-owned layer
  ordinary GameScene continuation -> actual returne2f948, W0=1
```

The original TrackLayer factory receives X0=model, W1=10000, X2=selected song object, X3=scene string/configuration input, W4=scene field+0x348, W5=the special-scene-derived branch value. In the ordinary fixture, X3/W4/W5 are zero. The integer10000 comes directly from `0xe2f3fc`, not a fabricated TrackBase default.

At the ordinary TrackBase initializer call, X0 is new0x3a0 storage, W1=10000, X2=song, W3=2, X4=the actual model, X5=0, W6=0, W7=0, with the stack-carried boolean zero on the tested branch. Original getter `0x8f7140` supplies W3 by following Model+0x28 → LogicChart+0x18 → metadata integer+0x124. That is the difficulty field established in010, so this initializer input is natively traced chart difficulty2, not an assumed equality.

The initializer stores its model at TrackBase+0x358, the10000 input at+0x350 and configuration flags at+0x340/+0x360/+0x364/+0x365. Song optional metadata is read through `0x15c5b5c`, including song+0x190 when present; the ordinary controlled metadata selects the normal branch. Special-song comparisons and alternative modes exist but were not exhaustively executed.

### Number, hierarchy and native ownership

Ordinary gameplay constructs **one TrackBase** in this fixture. Its vector is TrackLayer+0x300/+0x308/+0x310, and its parent is the actual TrackLayer. Native retain/autorelease/child-attachment instructions produce that relationship; no host vector insertion or parent-pointer write is used.

The TrackBase has21 Sprite children in the observed ordinary graph. Native vectors retain:

| TrackBase vector | Count | Native resource role established by requests/construction |
|---|---:|---|
| `+0x2a0` | 6 | `img/lane_hit.png` Sprites |
| `+0x2b8` | 5 | `img/track_lane_divider.png` Sprites |
| `+0x2d0` | 6 | Critical-line Sprites: four ordinary critical-line and two extra-lane-light variants |
| `+0x2e8` | 2 | `img/track_extralane_light.png` Sprites |

Two additional directly owned Sprite children provide the main track and break-mask resources. Descriptive lane/resource roles are supported by actual native resource requests and vector construction; complete renderer topology/shader output is not inferred from the names alone.

Native initial positions include extra-lane Sprites at X±1062.5,Y0,Z500 and lane-hit sample X−1275,Y1,Z−10. Ordinary track/break-related geometry is initialized through original setters. Actual dimensions are scaled against the controlled2×2 placeholder texture, so these are native arithmetic observations under that environment, not faithful artwork dimensions.

## TrackLayer object graph and ownership

| Owner field / object | Pointer | RTTI / vtable | Allocation / producer | Parent / initial Ref |
|---|---|---|---|---|
| GameScene+0x3b0 / TrackLayer | `0x43606c0` | `10TrackLayer` / `0x1b92a28` | 0x3f0; `1877ebc →12967e4` | `0x4360240` / 2 |
| TrackLayer+0x300[0] / TrackBase | `0x43618c0` | `9TrackBase` / `0x1aa1050` | 0x3a0; `native allocation/Node ctor →a5d3dc` | `0x43606c0` / 2 |
| TrackLayer+0x2f8 / CameraController | `0x4360b00` | `16CameraController` / `0x1a846a8` | 0x2e0; `1393474 →851514` | `0x43606c0` / 2 |
| TrackLayer+0x320 | `0x447c400` | `17NoteBurstRenderer` / `0x1b89e48` | 0x310; `native allocation/ctor →7ab65c` | `0x43606c0` / 2 |
| TrackLayer+0x328 | `0x447b640` | `N7cocos2d4NodeE` / `0x1b4d3e8` | 0x2a0; `17ec490` | `0x43606c0` / 2 |
| TrackLayer+0x348 | `0x44daf40` | `N7cocos2d4NodeE` / `0x1b4d3e8` | 0x2a0; `17ec490` | `0x43606c0` / 2 |
| TrackLayer+0x350 | `0x4479e40` | `N7cocos2d4NodeE` / `0x1b4d3e8` | 0x2a0; `17ec490` | `0x43606c0` / 2 |
| TrackLayer+0x358 | `0x447a140` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x0` / 2 |
| TrackLayer+0x360 | `0x447a680` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x0` / 2 |
| TrackLayer+0x368 | `0x447abc0` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x0` / 2 |
| TrackLayer+0x370 | `0x447b100` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x0` / 2 |
| TrackLayer+0x388 | `0x447b940` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x447b640` / 2 |
| TrackLayer+0x390 | `0x447bec0` | `N7cocos2d6SpriteE` / `0x1aa0128` | 0x4b0; `196c810` | `0x447b640` / 2 |


The camera rig is parented to TrackLayer and owns its original primary/secondary cameras. Primary camera begins at `(0,900,900)` for the controlled1280×720 view. The TrackLayer itself is attached to an intermediate scene-owned layer via original `0xe2f41c`; the driver does not assume its parent is directly GameScene.

The suffix's additional products include:

- Four actual Sprites in retained vector+0x330, constructed at `0x1296ed8 → 0x196c810`; request `img/white.png`. Original code sets opacity30, camera mask4 and global Z order20. They are retained but unparented in the initial snapshot; they are not falsely drawn as initial child attachments.
- The renderer collection at+0x3b8 contains **506 native objects:504 RenderBar and2 RenderTapNote** for this initialized chart. The count is observed from native production, not a claim that all506 are scoring notes or simultaneously visible. `0x86a104` obtains the original model collection, and `0x12970c4 → 0xae6740` builds its render objects. The existing native chart distinguishes bars from the two judgment units.
- Auxiliary Nodes at+0x350 and+0x348 are factory-created by `0x17ec490`, then attached. Original virtual+0x40 sets **global Z order−9**, not Node position Z. Their position Z remains0 in the snapshot.
- Four retained directional indicator Sprites at+0x358/+0x360/+0x368/+0x370 request `img/left_up.png`, `img/left_down.png`, `img/right_up.png`, `img/right_down.png`. Initial X/Y are `(420,670)` for the left pair and `(860,670)` for the right pair. All three scale components are native f32 `0.30000001192092896`. They remain unparented initially; later production use is not fully traced here.
- Node+0x328 owns two Sprite children at+0x388/+0x390, requesting `img/air_input.png` and `img/1080/skylabel.png`; the graphical updater uses this Node for opacity/action control.
- NoteBurstRenderer at+0x320 is allocated0x310 and initialized through `0x7ab65c`, callsite`0x129766c`. It creates original ParticleSystemQuad objects through `0xd3d8c8`, allocation0x5b0, initializer`0x11de120`; the ordinary trace loads the archived particle_arc plist six times. This advances007's constructor evidence without claiming complete effect-trigger or particle-draw behavior.

Node layouts verified by instructions/readback: scales+0x2c/+0x30/+0x34; position+0x38/+0x3c/+0x40; content size+0x5c/+0x60; opacity byte+0x1d0; global-Z order+0x138; parent+0x148; children-header pointer+0x140; running/visible bytes+0x1c0/+0x1c1. Reading the content-size fields as scale would be an erroneous analysis; final snapshots use the actual native scale fields.

Reference counts in the initial graph are generally2 for retained/attached products. Native non-null Ref arithmetic executes. Objects such as retained-but-unparented indicators demonstrate that ownership and parenting are separate operations. Pool/autorelease insertion and actual heap reclamation remain supplied; no leak or complete-destruction conclusion follows.

## Native resource/material/texture dependencies

The TrackBase path requests actual original filenames, including `img/track.png`, `img/track_break_mask.png`, `img/track_extralane_light.png`, lane-hit/divider/critical-line resources, directional indicators, air-input/skylabel images and `particle/note_light.png`. Requests are logged from original factory calls; assets are not invented to match them. The archive contains zero PNG files. The presence of archived model/shader files alone does not prove they are selected by this ordinary path.

The archived `assets/particle/particle_arc.plist` is2679 bytes, SHA-256 `5e41a59f513db6d40de93675fde99642e82ef7ef7111adbd5c09b8d508794bef`. Native FileUtils/XML/property-map parsing executes; only raw bytes, missing-file results and external libc interfaces are supplied. The six ordinary particle loads retain the original resource and parameter selection. No live audio, actual GPU upload/output or particle display is established.

### Native texture foundation recovered during this expedition

The inherited019 placeholder had a real native Texture2D object but zero dimensions. Inspection of the newly executed track suffix exposed an infinite X scale at the air-input Sprite: `0x12974d4–0x12974e8` computes `(6*viewWidth)/spriteWidth`, and the controlled width was0. This is a harness initialization limitation, not a production divide-by-zero claim.

Original white-image setup `0xa429c0` creates an original Image through `0x10eb724 → 0x1188184`, using the binary's own16 raw white bytes for2×2 RGBA data, then calls TextureCache `0x193489c`. That routine constructs Texture2D via `0x16be68c` and calls native image initialization `0xacac18 → 0x10f70c4`.

Two missing prerequisites were isolated:

1. The native Configuration maximum-texture getter `0x1589238` reads+0x0c. Because full GPU capability startup remains suppressed, it returned0; native width/height validation at `0x10f7124/0x10f7130` rejected the2×2 image. The scoped GPU capability interface now returns4096.
2. Once that validation proceeds, native Image lookup `0x130889c → 0x157d7cc` needs the pixel-format map at`0x1bf5e10`. Without its constructor, original `map::at` throws from `0x12449b8`. Original static initializer **`0xcabe24`** builds the21-entry registry and accompanying native format descriptions. It is now executed before resource construction; no format-map nodes are supplied manually.

With both prerequisites, the original native texture/image/data path runs. `0xc3fdfc` executes21 times in the final run (including the white texture and font-atlas paths). Native placeholder pixel/content dimensions are all2. The former infinite air-input X scale is now **3840**, exactly `(6*1280)/2`; all inspected TrackBase/support-object positions/scales are finite. That large scale reflects the deliberately tiny placeholder, not real image fidelity.

The new environment boundary is explicit: maximum-texture capability4096 plus existing inert GL imports. Shader compile/link statuses, GL IDs and upload/draw calls remain controlled, not tested on a GPU. TextureCache file lookup`0x176b6c4` still returns the original-created white Texture2D for artwork. Native resource selection, Sprite construction, CPU metadata and ownership remain original. The019 same-ELF relocation/reader/font support is preserved, not replaced with host rendering.

## TrackLayer graphical update

The whole function `0x19069a0–0x1906b28` executes in the final joined test, with **no inert hook and no interior PC skip**. Its ordinary caller is GameScene visit at`0x18be420`; another instruction-backed caller/tail branch is`0x1396eac` in closure`0x1396dc8` and is not the ordinary path claimed here.

The native visit supplies:

```text
X0 = scene's actual TrackLayer
X1 = model+0xa0            // active-object vector header
X2 = model+0x120           // additional control collection
W3 = original0x7ddc0c(model) effective-time getter
S0 = model f32+0x4c
S1 = model f32+0x50
```

Original update behavior:

1. Store the active-collection header pointer at TrackLayer+0x2c8. When needed, copy the additional collection through original`0x18ca46c` into TrackLayer+0x2d0. The two-tap fixture has no additional control entries; arbitrary nonempty collection behavior is not exhaustively tested.
2. Store W3 at+0x2e8. Native getter`0x7ddc0c` reads the GameTimeline and subtracts the native baseline; this is not a Java capture timestamp.
3. Set the opacity-control Node+0x328 positionY to `float(globalI32[0x1bf2610]) * model.f32+0x60` through its original virtual+0xc8 setter (`0x1026dd4`, forwarding unchanged X and new Y to position virtual+0xa8). In the selected startup image the global integer is0 and this Node Y remains0; the producer of its nonzero production values is not recovered here.
4. Compare prior+0x2ec with S1; on change, stop that Node's actions and create an original RepeatForever(Sequence(FadeIn, FadeTo(200))) action from native factories`0xdca67c`, `0xe55d64`, `0x14be12c`, `0x1775868`, then native runAction. The native duration arithmetic starts with f32`120/max(S1,50)`, then computes0.3 and0.7 portions through double multiplication and f32 narrowing.
5. Store S1 at+0x2ec and propagate S0 into every TrackBase+0x34c using the original scalar/vectorized loop at`0x1906ab8–0x1906b10`.

S1 is observed120 in this chart and drives the beat-like pulse interval; treating it as tempo is grounded interpretation. S0 is720 and is reported as the **model-provided render scalar**, not casually renamed depth or speed without its full producer proof. TrackBase+0x34c receives that scalar. Timestamp+0x2e8 is separately observed1000/2000/2121.

| Wall ms | Effective field+0x2e8 | Tempo-input cache+0x2ec | TrackBase scalar+0x34c | Pulse Node opacity |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 255 |
| 1000 | 0 | 0 | 0 | 255 |
| 4001 | 0 | 120 | 720 | 255 |
| 5001 | 1000 | 120 | 720 | 255 |
| 6001 | 2000 | 120 | 720 | 200 |
| 6122 | 2121 | 120 | 720 | 222 |
| 13282 | 9281 | 120 | 720 | 243 |


Opacity values arise from original Scheduler/ActionManager progression and the native action built by this update. No host opacity animation or time-triggered Python callback is used. The Node continues to expose a changed opacity while outgoing actions later become paused during scene exit.

### Rendering boundary remains explicit

Executing this updater does **not** execute every TrackBase/note child's visit/update/draw routine. Base traversal `0x129c924` remains inert, so the new506-object renderer collection is native-produced and retained but full per-renderer refresh, mesh submission, shader uniforms and draw output are not established. The update function itself contains CPU state/action preparation; subsequent GPU rendering is a separate boundary. This is the closest genuine engine boundary now, after removal of the TrackLayer initializer/updater substitutes.

## GameScene bootstrap integration

The final test starts in a new emulator, supplies the existing application/metadata/settings/resource/clock/platform boundaries, executes selected original ELF constructors plus new`0xcabe24`, and calls original Director construction/GLView attachment. It allocates zeroed GameScene storage0x4e0 and executes the original`0xe4e4dc` constructor and`0xe2ea48` initializer.

Constructor inputs are the019 ordinary fixture: X0=scene storage, X1=song pointer; X2–X7=`2,0,0,0,40,0`; caller-stack slots at0,8,16,24,32,40=`1,0,0,0,0,100`. Selected song ID is`expedition020`, difficulty2; localized title/configuration/account/provider inputs remain supplied. All scene/model/chart/timeline/score/camera/listener/track ownership links are produced by original code. No driver writes the TrackBase vector, Sprite fields, model dependencies or save gate.

The complete controlled AFF input remains:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

Original loader`0x16e67a4`, whole-file/header/body parsing, LogicChart initializer, model factory/initializer and spatial index execute unchanged. TrackLayer is reached through actual callsite`0xe2f400`; its full initializer return is recorded at`0x12977c0`, X0=1, LR=`0x1877f84`. Enclosing GameScene reaches its real return1 as well. The intermediate `0x1297788` address is reached by sequential native control flow, not a hook redirect.

Original replacement`0x9c90c0` and pending consumer`0xd0dc14` activate the scene. These are driver-entered original lifecycle calls; they do not constitute executed Android menu/GLThread startup. Entire Director frames`0x1793f8c` run under the retained base-render/swap boundaries.

The original GameScene visit guard remains effective: four camera visits per Director frame produce one model/update block once the frame counter differs. Initial Director counter0/scene stamp0 produces no model or TrackLayer update. Scheduler/ActionManager precede visits. Final trace:24 GameScene visits,5 model frames and5 original TrackLayer graphical updates. The driver calls neither`0x10a7550` nor`0x19069a0` directly in the joined regression.

## Gameplay and optional results regression

### Ordinary joined test — native-integrated within declared services

Driver clocks are1000,4001,5001,6001,6122ms for initial gameplay Director calls. At4001 original gameplay establishes the music anchor at effectiveE0. At5001/E1000 and6001/E2000 the driver enters native JNI begin`0xbe31a8`, pointer IDs42/43, coordinates`(740,700)`/`(540,700)`, pressure0.5 and distinct synthetic capture timestamps987000/987001, followed by original JNI UP`0xdda71c`.

Original GLView mapping, Touch allocation, EventDispatcher/gameplay listener, projection/judgment and contact cleanup execute. Pointer IDs, slot0 reuse and generated gameplay contacts remain distinct. Java timestamps do not replace E. Both judgments are PURE, with original gauge/scoring transitions.

At6122/E2121, the model reaches actual GameScene completion`0xc27d34`. Snapshot`0x1600bb0` stores the authoritative result at ScoreState+0x68. The result is not taken from an assumed snapshot return register.

| Object | Pointer | Native relationship checked |
|---|---|---|
| gameScene | `0x4322b40` | Original source scene throughout ending |
| model | `0x434e780` | Scene+0x3e0 |
| chart | `0x432a0c0` | Scene+0x3e8 = Model+0x28 |
| timeline | `0x434e900` | Model+0x30 |
| scoreState | `0x434e940` | Model+0x38 |
| result | `0x4ec4900` | ScoreState+0x68 = GameSession+0x18 |
| endingRoot | `0x4ea3140` | Scene+0x3c8, original CSLoader product |
| endingTimeline | `0x4eae600` | Scene+0x3d0, original CSB ActionTimeline product |
| session | `0x4ecbc00` | Native transition creates; retains original result |
| resultScene | `0x4ecbd00` | Scene+0x2e8 retains GameSession; final running scene |
| shutter | `0x4ecc840` | Original transition factory; incoming original result scene |
| director | `0x4104a80` | Original singleton |
| scheduler | `0x41081c0` | Director+0xa0 |
| manager | `0x4108840` | Director+0xa8 |
| dispatcher | `0x4108c00` | Director+0xb0 |


Original ending Scheduler registration/callback`0x19bbdd0 → 0x1a51054` starts the original-loaded GameEnd root and ActionTimeline; native component/action-tag enumeration binds all85 Frames. Native frame49 has zero continuation entries and frame50 invokes`0x147dee8` once with the original scene capture. Original outro and scene-change timers create GameSession/results/TransitionShutter. Director activates the shutter, native opening CallFunc invokes`0x963094`, and incoming virtual initialization reaches`0x891150` and its original save-gate producer/branch.

The same result identity is verified at ScoreState+0x68 and GameSession+0x18; the result scene's+0x2e8 retains that native session. No prepared result or second gameplay environment is substituted. No continuation/shutter/closing callback, GameSession construction, save gate or SQLite writer is manually triggered.

### SQLite and final state

Bundled original ARM64 SQLite runs against a private`:memory:` database and original schema strings. Original helper`0xdc2c48` invokes score writer`0x13552d4`, which reaches clear writer`0x12a5e60`. Native prepare/bind/step/finalize and readback—not host SQL—produce:

```text
scores:
  id=1, version=1, songId="expedition020", songDifficulty=2,
  score=10000002, shinyPerfectCount=2, perfectCount=2,
  nearCount=0, missCount=0, date=1700000000,
  modifier=0, health=80, ct=0
clearTypes:
  id=1, songId="expedition020", songDifficulty=2, clearType=3, ct=0
```

GameResult: PURE2/FAR0/LOST0, score10,000,002, live health80.4000015258789, integer health80, clear3. The controlled calendar time service writes its out-pointer correctly; no native counters/result fields are patched.

Native closing timers/actions request the final result scene, and original Director processing makes it running, pending=null, scene stack=[result scene], EventDispatcher+0x124=1. Additional Scheduler dt`[0,.25,1,5]` and a Director call preserve the rows and final state. Ending continuation, shutter opening callback, results initializer, save helper and both writers each enter once; uniqueness is not inferred solely from an equal-score write being ignored.

The integration extends019 rather than repeating its storage matrices. It does not execute pending online work: the existing account/pending-result processor`0x1246c98` remains inert and no server is contacted.

### Separate camera coexistence probe

A diagnostic constructed-scene run invokes the original paired camera-action builder`0x10a2b94` with a supplied Vec3 delta`(600,0,0)`, linear identifier and duration2000ms. Original MoveBy creation/cloning/runAction and Scheduler/ActionManager update execute on both cameras while the original TrackLayer updater remains active. Both cameras progress X0→300→600, cached world X matches0/300/600, and view translation X becomes0/−300/−600; TrackLayer effective timestamp progresses0/500/1000 and its model-provided scalar remains720.

This probe's driver calls a standalone Scheduler update and then a whole Director frame, whose own Scheduler update also runs. Thus each listed0.5s step supplies **two0.5s advances**, explaining300 units per combined step for a600-unit/two-second action. It is not a claim that one0.5s update moves300 or that real Android scheduling doubles time. The ordinary two-PURE joined regression does not include this extra camera driver or altered projection. This is a separate native-isolated/coexistence probe, not a second fabricated part of the uninterrupted score trace.

## Synthetic dependency audit

| Dependency |019 state |020 outcome | Remaining boundary |
|---|---|---|---|
| TrackLayer suffix | Skipped12968b0→1297788 | Entire ordinary initializer executes and returns1 inside GameScene | Other modes/error paths not exhaustive |
| TrackBase | Instruction-backed/diagnostic | One original-allocated/initialized0x3a0 product, native vector/parentage | Complete TrackBase child rendering not executed |
| Supporting Nodes/Sprites | Missing in joined graph | Native production, retained vectors/attachments/initial transforms | Real artwork and later indicator attachment semantics |
| Renderer collection | Not established in joined graph | Native506-object collection,504 RenderBar/2 RenderTapNote | Base visit/render traversal remains bounded |
| NoteBurstRenderer | Earlier isolated evidence | Native construction and six original particle resource loads in startup | Full effect triggering/particle draw |
| Locale | Unsupported newlocale import | Correct scoped mapped OS object and observed original caller propagation | Alternative callers/destruction/error handling |
| TrackLayer update | Whole-function inert | Complete19069a0 executes five times through GameScene visit | No actual GPU output/per-child draw claim |
| Texture foundation | Native object with zero dimensions | Original pixel registry and native2×2 initialization, finite inspected scales | GPU-capability getter/GL/artwork still supplied |
| GameScene return | Return1 under TrackLayer skip | Return1 without that skip | Application/results/platform boundaries retained |
| Director/model/input | Native-integrated | Preserved | Driver clocks/frame/JNI inputs, no Android queue execution |
| GameEnd/results/SQLite | Native-integrated019 | Preserved in same new full-track graph | Declared results/shutter UI regions |
| Ownership/reclamation | Native Ref arithmetic, supplied pool/free | Preserved, observed retained versus parented distinctions | Complete destruction not established |

## Native execution traces and failure behavior

| Original entry | Entries in final joined run | Meaning |
|---|---:|---|
| `0xe4e4dc` | 1 | GameScene constructor |
| `0xe2ea48` | 1 | GameScene initializer |
| `0x1877ebc` | 1 | TrackLayer factory |
| `0x12967e4` | 1 | Full TrackLayer initializer |
| `0xa5d3dc` | 1 | TrackBase initializer |
| `0x12977c0` | 1 | Actual TrackLayer RET; X0=1 |
| `0x19069a0` | 5 | Original graphical update |
| `0xcabe24` | 1 | Native pixel-format registry initializer |
| `0xc3fdfc` | 21 | Native texture-data initialization |
| `0x1793f8c` | 8 | Whole Director frames |
| `0x13d3f44` | 35 | Original Scheduler updates |
| `0x18be2f8` | 24 | GameScene visits |
| `0x10a7550` | 5 | Visit-driven model frames |
| `0xbe31a8` | 2 | JNI begin |
| `0xdda71c` | 2 | JNI end |
| `0x160ce28` | 2 | Native tap judgment |
| `0x1600bb0` | 1 | Cached snapshot |
| `0x147dee8` | 1 | Native ending continuation |
| `0x963094` | 1 | Native shutter opening callback |
| `0x891150` | 1 | Results initializer |
| `0xdc2c48` | 1 | Original save helper |
| `0x13552d4` | 1 | Original score writer |
| `0x12a5e60` | 1 | Original clear writer |


### Focused negative and partial tests

- **Missing particle asset, native-isolated:** original ParticleSystemQuad factory`0xd3d8c8` was called with std::string`particle/missing020.plist`. Supplied provider returned empty Data at original reader return site`0x1501cac`. Under the existing FileUtils/texture services, original initializer/factory returned a **non-null ParticleSystemQuad**, vtable`0x1abd450`, rather than a fabricated failure return or host-created emitter. This is an observed controlled-path outcome, not proof of valid particle emission or universal missing-file fallback. No complete missing-resource propagation through GameScene was asserted.
- **Sprite allocation failure, native-isolated:** the nothrow allocator boundary returned null for original Sprite factory`0x196c810`'s0x4b0 request. Original branch`0x196c834 → 0x196c878` returned null. No invalid native pointer was supplied, and caller tolerance within the entire TrackLayer was not assumed.
- **Locale errors/lifetime:** separate supplied-ABI contract tests above; no claim that the enclosing native locale initializer's failure path executed.
- **Zero texture capability and omitted pixel registry:** diagnostic native image validation rejects the former; enabling the capability alone exposes original map::at error. Final registry/capability setup resolves these before entry, and the full regression is rerun fresh. The failed probes are not mislabeled as game crashes.
- **Repeat initialization/complete destructor:** not tested. Native initialization is reached once through ordinary factory control flow; repeated visits and post-completion Scheduler updates are tested separately. Native retain/release operations and scene exit are not proof of full cleanup or allocator reclamation.

## Reproduction procedure

1. Verify the binary/archive identities. Reuse019's loader with original relative/defined-symbol relocations, selected original static initializers and same-ELF function forwarding. Add original pixel-format static initializer`0xcabe24`; do not manually populate its map.
2. Install the scoped C-locale/math/condition/string services in the ABI table and the controlled maximum-texture capability4096 before any resource initialization. Let original white Image/Texture2D initialization run; assert pixel/content sizes2×2.
3. Supply019's explicit platform/application/configuration/metadata/resource interfaces, selecting song`expedition020`. Call original constructor/initializer with the register/stack inputs above. **Do not install12968b0 or19069a0 hooks.** Require the actual TrackLayer RET X0=1 and GameScene return1.
4. Inspect native field/vector/parentage/RTTI, read actual scale fields+2c/+30/+34 and opacity+1d0, and require finite inspected initial transforms. Preserve original model/chart/timeline/score/camera/listener identity.
5. Enter original scene replacement/pending activation and whole Director frames at the stated clocks. Let the native visit reach model and TrackLayer updater; deliver only the two original JNI begin/end pairs from the driver.
6. Continue completion/ending/outro/results with original Scheduler dt values reused from019: ending`[0,4]`, timeline`[0,.4,.4,.03,.01,.02]`, then`[2,.3]`; activate pending shutter with original Director; opening`[0,.25,.25,.25]`; closing`[0,.2,.2,0,0,.1,.1,.1,0]`; consume final activation with original Director. The callback identities/ordering come from native scheduling, not driver callback calls.
7. Check result pointer equalities, callback counts, actual SQL readback and final Director/dispatcher fields; advance the additional updates and compare unchanged rows/state.

The final native run did not require arbitrary successful initializer flags, TrackLayer vector/Sprite writes, manual model frames, patched counters, host completion callbacks or direct SQLite save invocation. No renderer or game binary instruction bytes were edited.

## Pseudocode

```cpp
// External services: allocator, clocks, OS ABI, raw archive/provider, controlled GPU.
// Original CPU setup:
runPreviouslyRecoveredNativeStatics();
runOriginalPixelFormatRegistryInitializer_cabe24();
provideMaxTextureCapability(4096);                  // explicit GPU interface boundary
nativeWhiteImageAndTextureInitialization();         // native2x2 pixels/content; GL inert

GameScene::init() {                                 // original e2ea48
    chart = originalWholeAFFLoadAndLogicChartInit();
    model = originalGameModelFactoryAndInit(chart);
    // existing native background/scene/control setup
    track = TrackLayer::create(model, 10000, song, ...);
    nativeAttachTrackAndContinueHUDGameEndSetup();
    return originalStatus;                         // actual returned1
}
TrackLayer::create(args) {                          // original1877ebc
    p = nativeAllocate(0x3f0);
    originalBaseConstructorAndTrackVtable(p);
    if (!p->init(args)) { originalVirtualDelete(p); return null; }
    originalAutorelease(p); return p;
}
TrackLayer::init(model, value10000, song, ...) {     // original12967e4, NO suffix skip
    if (!originalBaseInit()) return false;
    storeNativeModelAndConfiguration();
    camera = CameraController::create();
    addChild(camera);
    base = originalAllocateAndNodeConstructTrackBase(0x3a0);
    // actual initializer a5d3dc receives the already allocated object
    if (originalTrackBaseInit(base, value10000, song, selector, model, ...))
        originalAutoreleaseAndRetainVector(base);
    else originalVirtualDelete(base);               // instruction-backed failure branch
    addChild(base);                                 // executed ordinary success
    originalCreateLaneAndTrackSpritesAndVectors();
    originalRetainFourEffectSprites();
    originalBuildChartRenderObjects();              //506 here; not506 scoring units
    originalCreateSupportNodesAndIndicators();
    originalCreatePulseNodeAndTwoSprites();
    originalCreateNoteBurstRendererAndParticles();
    originalAttachChildrenAndAssignCameraMasks();
    return originalBaseStatus & 1;                  // actual RET12977c0, W0=1
}

// Driver enters Director frames; no direct model/update call in joined test.
Director::frame() {
    nativeSchedulerAndActionManagerUpdate(dt);
    nativeSceneCameraRenderTraversal();
    // actual GPU/base-child draw boundary still supplied
}
GameScene::visit() {
    if (directorFrame != lastUpdatedFrame) {
        model->frame(this);                         // original judgment/completion
        originalHUDAndFrameStateUpdates();
        track->update(&model.active, &model.controls,
                      nativeEffectiveTime(model), model.f4c, model.f50);
        // exact guard/stamp control remains original
    }
    suppliedBaseDrawTraversal();
}
TrackLayer::update(active, controls, E, scalar, tempoInput) { // original19069a0
    nativeStoreActiveHeaderAndCopyControls();
    effectiveField2e8 = E;
    pulseNode.positionY = float(globalInteger) * model.f60;
    if (tempoInput != oldTempoField2ec) {
        originalStopPulseActions();
        period = f32(120 / max(tempoInput, 50));
        originalRunRepeatingFadeInFadeTo200Sequence(period); // original double/f32 boundaries
    }
    oldTempoField2ec = tempoInput;
    for (base : originalBaseVector) base.f34c = scalar;
}

// OS interface called by original native libc++ setup, not native Bionic execution:
newlocale_service(mask, rawName, base) {
    validateSupportedMaskAndNameOrReturnNullWithErrno();
    return mappedLocaleWithCoherentMbCurMaxAndLifetime();
}
sincosf_service(S0, X0_sinOut, X1_cosOut) {
    storeF32(X0_sinOut, sin(S0)); storeF32(X1_cosOut, cos(S0));
}

// Same scene/model/result; all subsequent handoffs original within declared UI services:
JNI_input -> EventDispatcher -> gameplayListener -> nativeJudgment;
modelCompletion -> originalGameSceneCompletion -> cachedResultAtScoreStatePlus68;
Scheduler -> endingCallback -> resourceLoadedGameEndActionTimeline;
nativeFrameEnd -> continuation147dee8 -> outroAndSceneChangeTimers;
nativeGameSession(cachedResult) -> nativeResultScene -> TransitionShutter;
DirectorActivation -> originalActions -> CallFunc -> incomingResultInitializer;
originalSaveGate -> nativeSaveHelper -> bundledSQLitePrivateMemoryDatabase;
originalClosingActionsAndTimers -> DirectorFinalResultsActivation;
```

## Exact remaining PC skips and external services

**Removed in the successful final run:** `0x12968b0 → 0x1297788` and whole-function inert`0x19069a0`. No replacements for TrackBase initialization, chart renderer construction or TrackLayer update were introduced.

Retained PC redirections from019:

| Source → resume | Omitted work |
|---|---|
| `0xf72110 → 0xf72158` | Controlled platform GLView attachment/setup segment |
| `0x16a4238 → 0x16a48d8` | Shutter graphic-panel creation; supplied original-constructed Node panels |
| `0x121581c → 0x121584c` | Shutter loading overlay |
| `0x891190 → 0x89164c` | Results leading UI/account region; X28 application-global address and X26=FP−0x60 supplied as before |
| `0x891688 → 0x89219c` | Results layout/progression region |
| `0x8921dc → 0x8928e0` | Results trailing UI/progression region |

The save-gate producer`0x89164c–0x891684`, branch`0x89219c–0x8921dc` and helper call`0x8921b8` remain original. GameScene/TrackLayer epilogues, model frame, continuation/shutter/closing callbacks and Director final state are not driver jumps.

Retained whole-interface boundaries, including ones not entered in a particular trace:

- Render/base traversal`0x129c924`, framebuffer-registry clear`0x13edf0c`, swap interface`0x1017a84`; full GPU output and per-child drawing remain unexecuted.
- Ancillary scene/application calls`0x18c7a40`, `0x86d018`, `0xbe2cf8`, `0x16e11c0`, `0xfc77a8`, `0xacf9e0`, `0x11b35fc`; catalog override lookup`0x14ac9c4` returns absent.
- Completion/account/result ancillary interfaces`0x1186f70`, `0xc464e4`, `0x19becc0`, `0x1246c98`, `0x1019c18`, `0x1049858`, `0xc800b0`, `0x9d2518`, `0x9c8190`, `0xacf898` inert. No pending-result worker/server execution is claimed.
- Audio/playback/SFX`0x1735d7c`, `0x107af5c`; configured feedback`0x7ebcf0`, `0x1715728`; clock/audio-adjacent`0x18dcd1c` bounded.
- Existing platform/bootstrap services`0x18fdcf0`, `0x1929dd0`, `0x16d80f8`, `0xf1e53c`, `0xcff9cc`, platform interface`0xd7654c`; new maximum-texture getter`0x1589238` explicitly supplies4096 while full GPU capability gathering remains outside scope.
- Account/settings/resource boundaries`0xb688e0`, `0x18a6b8c`, `0x1513c24`, `0xb99da4`, `0xd7845c`, `0xb9d4a4`; provider/status opaque virtuals and control+0x508. Metadata/localized title/configuration remain prepared external inputs.
- Asset-provider path/existence/Data at`0x190bc44`, `0xca7a88`, `0x1730c40`; TextureCache artwork lookup`0x176b6c4` supplies the native white texture. Original CSLoader/readers/component/tag binding and the new original texture/pixel-registry construction are not replaced.
- Ref arithmetic executes for non-null original objects; null environment references, allocator/free/realloc/autorelease pool boundaries remain supplied. `0x10ac6e8` pool insertion is inert. Existing AFF stream interfaces`0x1087f14`/`0xb06728`, C++ string/stream/numeric/memory/formatting/RTTI/clock/math/TLS/locking services remain documented019 boundaries.
- New OS services are the locale/sincosf/condition/strncmp adapters described above. Native same-ELF locale/FreeType/SQLite implementations remain forwarded as before; no host SQL or host FreeType is substituted.

Observer hooks at result/Director factories collect identity without early returns or PC changes. Entry counts here use the original-entry event stream rather than double-counting layered observer bookkeeping.

## Unresolved Mysteries

1. The production writer of global integer`0x1bf2610` (zero in this selected startup) and complete TrackBase/note-renderer per-child visit/update, mesh/UV/material/shader uniforms, actual draw execution and accurate artwork remain outside the demonstrated chain. Native object construction is not proof of a rendered image.
2. The precise full producer/semantic name of model.f32+0x4c and every special-song/TrackBase mode branch remains bounded; exact fields/observed values are recorded without invented labels.
3. Later parenting/use of retained directional/effect Sprites and all particle activation conditions are incomplete. Initially null parent pointers are reported honestly.
4. Native locale error handling, actual device-libc version, concurrent once/condition behavior, every locale facet and process-exit destructor/free behavior are not established by the scoped C-locale service.
5. Reinitializing an already initialized TrackLayer and complete destructor/reclamation were not tested. Scene exit/paused outgoing actions and non-reclaiming harness allocations do not justify leak conclusions.
6. Results layout/account/progression, Android Activity/GLThread execution, hardware timing/audio, real user databases, network submission, special modes and FlickNote gameplay were not expanded into this expedition.

## GitHub Status

Expected starting/main commit: **`fabbe7cda54f4652a0986352b10284d7507d17a8`**, root tree`745fa7a760b465d53ffdfe5aaf433c661b383258`. Default branch and absence of020 are checked again before publication. Only this report and an append-only020 context entry are authorized changes.

Publication uses a main-ref expected-head lease. The commit containing this report is the publication identity; its exact SHA and pinned links are returned in the headquarters handoff. Both committed files are read back and compared exactly, prior context must remain an exact prefix, and historical001–019/README blobs are compared with the starting tree. Harnesses, logs, databases, extracted binaries and resources are not published. No021 is initiated.
