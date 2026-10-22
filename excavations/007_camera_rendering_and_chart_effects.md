# Expedition 007 — Camera, Rendering & Chart Visual Effects

## Result

The preferred minimum chain is recovered: **AFF camera event → LogicCameraControl → paired Cocos actions → native Camera node position/rotation → cached world/view/projection matrices → scene rendering**. The same primary Camera participates in gameplay input unprojection. Chart camera animation and viewport-to-design conversion are separate mechanisms.

Additional instruction-backed chains connect timing-derived note depth to a tap renderer, arc geometry samples to the current-position cache and arc renderer, `trackdisplay` to track-node opacity, `hidegroup` to render-hidden fields, and widening controls to shared gameplay state. Arc cross-section arithmetic and conflict-color blending were executed under Unicorn. Particle resource creation is established; the precise gameplay trigger for each particle variant remains incomplete.

This is a CPU-side reconstruction, not a complete renderer or a claim of graphical reproduction. Flick rendering, complete hold/arc topology, shader bindings, full action scheduling, and several special-scene consumers remain unresolved.

## What I Found

### Evidence, preservation, and address convention

**Confirmed** means instructions, RTTI/relocations, archive metadata, or the scoped native execution described below. **Interpretation** means a reasoned explanation of those observations. **Unknown** means the connecting implementation is insufficiently established.

Preparation included the authoritative `Introduction-and-the-scheme-of-this-project.txt`, ZIP inventory, current `context.md`, and Expeditions 001–006. Existing main was checked against `a3551928c5d0206ae9b472433e2fb2535e7fc280`. No historical correction is made here. Previously authorized curve-ID and spatial-depth corrections remain in force. In particular, geometry samples are not judgment checkpoints.

Unless explicitly identified as an asset path, every address below is a **library-relative ELF virtual address in `lib/arm64-v8a/libcocos2dcpp.so`, before load relocation**. Addresses are not runtime ASLR pointers or generally interchangeable with file offsets. The relevant `.text` and `.rodata` addresses equal file offsets; `.data.rel.ro` requires the ELF mapping (here VA minus `0x4000`) and RELATIVE relocations.

- Primary-library SHA-256: `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.
- Build ID: `17d660edbf37ca78beefc32e07672c97419ddce6`.
- The ZIP member was byte-compared with the analysis copy. No binaries or source assets were modified.
- Class names explicitly labeled RTTI below are recovered names. Function descriptions and field names such as `homePosition`, `groupOffset`, and `renderHidden` are researcher labels.

### 1. AFF camera parameters and runtime delivery

**Confirmed.** Parser `0x138f560` consumes:

```text
camera(I time, F a, F b, F c, F d, F e, F f, ID easing, I duration)
```

The typed token helpers distinguish integer and floating tokens as documented in Expedition 002; this expedition's parser test hooks those helpers, rather than re-executing the lexer.

| Object / evidence | Fields |
|---|---|
| CameraControl, RTTI `0x1b57740`, vtable `0x1b17318`, allocation `0x58` | `+0x18 i32 time`; `+0x1c..0x30 six f32`; `+0x38 std::string easing`; `+0x50 i32 duration` |
| LogicCameraControl, RTTI `0x1b1a3a8`, vtable `0x1ac16f0`; initializer `0x81d3e4` | `+0x18/+0x1c event time`; `+0x64/+0x68/+0x6c a,b,c`; `+0x70/+0x74/+0x78 d,e,f`; `+0x80 string`; `+0x98 i32 duration` |
| Chart builder `0x1862a14` | Constructs the corresponding runtime logic objects; initializer writes confirm the mapping |

The event-processing loop `0xf8056c` recognizes LogicCameraControl using RTTI through GOT `0x1b964d8`. It tests the processed predicate (vtable `+0x28`, implementation `0x13edae0`) and requires **effective GameTimeline time E strictly greater than `event+0x1c`**. It calls the ordinary acceptance/marking virtual (`+0x20`, `0xcafff8`) and then `0xf805dc → 0x192b5c8`.

The handler owner is the object addressed through the scene's `+0x300` relationship, not an assumed Camera itself. Its `+0x2a8` points to CameraController.

At `0x192b5c8`:

1. If any of `(a,b,c)` is nonzero, pass `(a,b,c)` to translation builder `0x10a2b94`.
2. If any of `(d,e,f)` is nonzero, pass **`(e,d,f)`** to rotation builder `0x13a7938`.
3. If the easing identifier equals the exact string `reset`, call `0xb0bd74`.

Therefore the first three numeric values are world-position deltas in native scene units. The second three are Euler-angle deltas in degrees, with the first two exchanged on delivery to the Camera node. There is no pixel conversion or degrees-to-radians conversion in this event handler. A reset event with nonzero triples can enqueue actions before executing the reset; reset is not an early return.

### 2. Camera rig, action construction, easing, and reset

**Confirmed.** CameraController RTTI is `0x1b4c578`, vtable `0x1a846a8`; factory `0x1393474` allocates `0x2e0` bytes and calls initializer `0x851514`.

| CameraController offset | Recovered role |
|---|---|
| `+0x2a0 byte` | Restore-look-at latch; initialized/set by reset |
| `+0x2a8 pointer` | Primary cocos2d::Camera |
| `+0x2b0 pointer` | Secondary cocos2d::Camera |
| `+0x2b8 Vec3` | Look-at target |
| `+0x2c4 Vec3` | Home position |
| inherited `+0x1b0` | Action-manager relationship used by stop-target path |

Initializer `0x851514` calls camera factory `0x13491b4` twice. The two cameras receive masks **4 and 16** at Camera `+0x412`. Their complete layer membership is not recovered here.

The resolution helper `0x9e2b60(lo,hi)` uses frame height H:

```text
D = clamp(H - 720, 0, 240)
result = trunc_i32(f32(lo + f32((hi-lo) * f32(D/240))))
```

The caller uses `(50,65)` for FOV, `(720,960)` for the denominator of `frameWidth / denominator`, and `(900,800)` for home Z. Both cameras start at `(0,900,interpolatedZ)` and look toward `(0,-550,-2000)` with up `(0,1,0)`. Near plane is 1; far planes are 10000 and 9000. These initializer values are instruction-backed; the whole initializer and resolution-dependent scene have not been run as a complete application.

#### Paired actions

Builders `0x10a2b94` and `0x13a7938` restore look-at on both cameras when the rig latch is set, then clear it. They convert the i32 chart duration to f32 seconds by division by 1000.

- Translation factory `0xf1b510`: RTTI `cocos2d::MoveBy`, vtable `0x1b40200`.
- Rotation factory `0x16c5bc8`: RTTI `cocos2d::RotateBy`, vtable `0x1b159d0`, 3D flag `+0x39 = 1`.
- Stored duration at action `+0x30` is `max(durationSeconds, 2^-23)`; the minimum f32 bits are `0x34000000`.
- Delta vector is at action `+0x3c`.
- `qi` wraps the action using `0x121253c`, RTTI `cocos2d::EaseCubicActionIn`, vtable `0x1abedf0`.
- `qo` wraps using `0x8c9d24`, RTTI `cocos2d::EaseCubicActionOut`, vtable `0x1aae190`.
- Other identifiers take the bare action path. The exact `reset` operation is additionally handled by the event handler.

An action is run on the primary camera through Node virtual `+0x388` (`0xc7820c`), cloned through action virtual `+0x18`, and the clone run on the secondary camera.

**The `qi` and `qo` functions here are cubic, not quadratic.** Leaves `0x9aa5a8` and `0xf0b7e0`, called by wrapper updates `0xc3f3dc` and `0x150d8d0`, evaluate with f32 arithmetic:

```text
qi(u) = (u*u)*u
qo(u) = ((u-1)*(u-1))*(u-1) + 1
```

ActionInterval step `0x12a5a80` first consumes its first-tick flag `+0x38`, setting elapsed `+0x34` to zero without adding the supplied dt. Later steps add f32 dt and call the action update with elapsed/duration clamped to `[0,1]` for the finite test cases. Thus interpolation is action elapsed time, supplied in seconds, **not a fresh evaluation of AFF event time against E on every frame**. No lateness/catch-up adjustment is passed by these builders. Full Scheduler/ActionManager pause ordering and arbitrary seeking were not executed.

MoveBy start `0x144471c` records the target's starting position at `+0x48` and last written position at `+0x54`. Update `0x8e2b70` incorporates `target.current - lastWritten` into the base before applying `delta*u`. RotateBy start `0x836ea8` records starting Euler angles; 3D update `0x11c0c9c` applies `startEuler + delta*u`. These are relative actions, not absolute AFF positions.

#### Reset boundaries

Reset `0xb0bd74` calls `0x15beb20 → 0xf14f9c`, passing **the rig** as the stop-target argument. It restores both cameras' look-at, then home position, then sets the rig latch. The observed operation order matters: look-at precedes restoring position. It does not justify a universal reset Euler constant.

**Unknown:** whether stopping this rig target also cancels every already queued child-camera action in the complete scene. The stop-target operation was captured in synthetic execution; no claim of global action cancellation is made.

### 3. Camera matrices and their actual rendering consumer

**Confirmed.** Camera constructor `0x11a6474` installs cocos2d::Camera vtable `0x1adf2d0`.

| Camera/Node offset | Recovered state |
|---|---|
| `+0x0c/+0x10/+0x14` | Node Euler angles, f32 degrees |
| `+0x1c..+0x28` | Quaternion |
| `+0x38/+0x3c/+0x40` | Node position |
| `+0xa4` | Node local transform matrix |
| `+0x130 i32` | Transform flags; changed position/rotation ORs `0x31` |
| `+0x2a8` | Projection P, 16 f32 |
| `+0x2e8` | View V, 16 f32 |
| `+0x328` | Cached camera world matrix W |
| `+0x368` | Cached combined matrix PV |
| `+0x3f8/+0x404/+0x408/+0x40c` | FOV / aspect / near / far |
| `+0x410`, `+0x478` | Camera matrix invalidation bytes written by view refresh |
| `+0x412` | Camera mask |

Node position setter `0x835b44` delegates Z to `0xd3d138` and XY to `0x12543f8`. Changed coordinates invalidate the Node transform. Rotation setter `0xd415dc` stores Euler angles and builds a quaternion using half-angles, `sincosf`, and f32 `pi/180` (`0x3c8efa35`). Z uses the negative angular factor.

For column-vector conventions and unit scale, the tested rotation is equivalent to:

```text
R = Rz(-zDegrees) * Ry(yDegrees) * Rx(xDegrees)
local = T(position) * R
```

Node transform routine `0xdc4348` also contains scale, anchor, skew, and additional-transform branches. This equation describes the tested unit-scale/zero-anchor case, not every Node configuration. Native single-axis checks establish the signs: X +90 sends +Y to +Z; Y +90 sends +Z to +X; Z +90 sends +X to −Y.

World helper `0x17c5b74` walks ancestors and premultiplies their local transforms. Camera refresh `0xe29b94` obtains W through Node virtual `+0x410` (wrapper `0x18f408c`, underlying world-transform virtual relationship `+0x3d8`), bitwise-compares all 64 bytes with the cached W, and on change copies it, sets camera dirty bytes, and computes:

```text
V = inverse(W)       // 0x1344f34 → 0xca3668
```

Combined getter `0x10eff1c` refreshes V, then if `+0x410` is dirty clears that byte and calls matrix multiply `0xa57c50 → 0x11e1bfc`:

```text
PV = P * V
clip = PV * worldPosition
```

`0x11e1bfc` is a column-major native multiply kernel using fused multiply-add instructions. This is not evidence for reversing the multiplication order.

Perspective builder `0x1410688`, reached by `0x13491b4`, produces the conventional-looking matrix **because the instructions establish these entries**:

```text
f = 1 / tan(FOVdegrees * pi/180 / 2)
P00 = f/aspect; P11 = f
P22 = -(near+far)/(far-near)
P23 = -2*far*near/(far-near)
P32 = -1; P33 = 0
```

Subscripts above are row,column. In flat column-major storage, `P32` is index 11 and `P23` index 14. Other entries are zero. The equation is a readable description; native f32 operation order, not algebraic reassociation, defines exact bits.

#### The rendering link is observed, not assumed

Scene rendering routine `0x10dd3d8` gets a camera vector through `0x1374ca4`, checks camera visibility, sets the visiting-camera global through GOT `0x1b973d8`, and obtains PV through `0x10dd46c → 0x10eff1c`. It passes the matrix to Director routine `0x18c56b8` with matrix-stack argument 1, invokes scene virtual `+0x338` with the camera mask, and flushes the renderer through `0xe49110`, with camera setup/cleanup surrounding the traversal.

This closes **camera animation → matrix → render traversal state**. Individual shader uniform uploads and GPU draw execution are not closed by this evidence.

#### Relationship to input

Expedition 004's input path retrieves the same primary camera through the gameplay model `+0x20` rig / rig `+0x2a8` relationship. This camera is also obtained by `0x10fd1c0`. Unprojection `0x16d3dcc` uses the inverse of its P*V. Controlled native tests applied camera actions, refreshed the actual matrices, projected a world point, and unprojected it back.

**Interpretation supported by the shared object and matrix chain:** changing this camera changes the camera-dependent projection used by gameplay input. This does not replace or alter the separately established Android/view/design-coordinate conversion. Camera-world movement is not a fixed screen-pixel hitbox transformation.

### 4. Timeline-dependent depth and note rendering

**Confirmed.** Scroll integrator `0xcf918c(chart,E,groupIndex)` selects a timing list through chart `+0x38` and accumulates f32 contributions. Timing records use `+0x10 start`, `+0x14 end`, `+0x28 scale`:

```text
acc = 0
for timing in selectedGroup:
    if timing.end < E: bound = timing.end
    else if timing.start < E: bound = E
    else: continue
    acc -= f32(f32(bound - max(timing.start,0)) / timing.scale)
```

The loop does not simply stop at the first timing change. `0x10fd1c0` negates this return value to obtain the current group offset; it also computes an E+120 look-ahead. It calls note virtual `+0x18` with E and the offset. Basic updater `0x1017d80` writes:

```text
logic.depthStart = trunc_i32(f32(f32(logic.precomputedStart_i32) + groupOffset))
logic.depthEnd   = trunc_i32(f32(f32(logic.precomputedEnd_i32)   + groupOffset))
// +0x30/+0x34 outputs, +0x38/+0x3c inputs
```

Hold updater `0x1866030` and arc updater `0x95d61c` participate in the same update system; the latter also clears contact latches before input processing. The complete production of the precomputed start/end depth integers is not newly closed here. The tested expression must not be simplified to `(noteTime-E)*constant` for arbitrary timing changes or negative speeds.

Model frame routine `0x10a7550` calls timeline update `0x16c90bc`, updates widening state, then `0x10a7804 → 0x10fd1c0`, then `0x10a780c → 0x19f3d4c` for the arc-position cache. Continuous input/checkpoints (`0x14858d4` and `0xf8056c`) follow in that frame path. This establishes logic/cache ordering; it is not a complete proof of every render/action scheduler callback order.

#### Logic-to-render links and tap placement

RenderNote-family objects hold the logic pointer at render `+0x2a8`, retrieved by virtual `+0x508` (`0xd5dc48`). Arc initializer `0x13b5ff8` writes that link at `0x13b6128`.

Tap render vtable `0x1acde18` uses update virtual `+0x510 = 0xf20c28` and initializer `+0x538 = 0xd7e290`. The updater computes the following integer-lane placement:

```text
x = 425*(lane-1) - 1063       // lanes 1..6
x = 212                      // other integer lane case
node.position = (x, 4, logic.depthStart)
```

The floating-position branch instead uses:

```text
x = trunc_i32(f32(f32(f32(normalized*1700)-850)-212)) + 212
```

Render `+0x2a0/+0x2a4` cache X/Y. Native tests covered lanes 1,3,4,6 at depths −10000, −5000, 0,300 and executed the actual Node position setters. The updater also writes four child quad positions at child `+0x3dc`, stride 24, including X offsets ±191 and depth-dependent height calculations. Complete quad format, UV assignment, texture state, and all opacity branches are not reconstructed here.

The initial expiry branch hides the tap renderer when it is visible, logic end depth is **at least 301**, and the logic processed predicate is true. It is not an unconditional depth-only disappearance rule. Separately, logic `+0x55` forces opacity zero. The renderer accesses depth-fade/opacity branches too; their entire boundary behavior remains incomplete.

Hold vtable `0x1a9eb80` has update `0x192b268` and geometry update `0x13ea188` at `+0x518`. The latter reads the `fadingholds` flag at logic `+0xa9`, start/end depths, held/contact state, and constructs sprite extents using a negative-Y scale path. Complete hold vertex dimensions and all fade cycles remain untested. Arc-tap vtable `0x1aacc40` uses `0x1073160`; it is a separate renderer, not the hold renderer. Flick RTTI was already identified in Expedition 001, but its complete visual pipeline was not recovered in this expedition.

### 5. Arc samples, the current-position cache, and segments

**Confirmed.** Geometry generator `0x1925084` and the corrected curve mappings remain as documented in Expedition 003. Logic vectors at `+0xe8` and `+0x100` contain sampled Vec3 geometry; optional sampling density does not create scoring checkpoints.

The previously unresolved current-position producer is **`0x19f3d4c`**, called by `0x10a780c`. It identifies ArcNote through RTTI/GOT `0x1b964b8`, reads adjacent Vec3 samples from logic `+0xe8/+0xf0`, translates sample Z by logic start depth `+0x30`, and solves for an intersection with the world Z=0 plane using dot helper `0x16da57c` and normal `(0,0,-1)`.

For a nondegenerate ordered segment P0→P1, the instruction sequence is equivalent to:

```text
raw = 1 - dot(n, O-P1) / dot(n, P0-P1)
u = clamp(raw,0,1)
position = P0 + (P1-P0)*u
```

There are orientation/segment-selection and degenerate branches; this expression alone is not a complete replacement for the iterator. The active predicate includes raw fraction in `[0,1]` and chart start ≤ E ≤ end, and reaches flag setter `0xad11b0` for logic `+0xd0`. While E ≤ end, store helper `0x19f423c` writes current X/Y at **logic `+0xd4/+0xd8`**. After end, the observed path leaves that cache unchanged. Normal colored arcs additionally perform connected/proximity/release handling; trace-mode tests deliberately avoid that ownership subpath.

With samples `(0,100,0)` and `(100,200,-1000)`, the original producer yielded `(0,100)`, `(50,150)`, `(100,200)` for parent depths 0,500,1000. Thus the cache is derived from the sampled geometry, not a separate speculative AFF curve evaluator.

Arc renderer `0x11b7d78` consumes that cache. Its position/cache block `0x11b7e6c..0x11b7f3c` places the parent at:

```text
(trunc_i32(f32(850*arcStartX-425)), 0, logic.depthStart)
```

and derives render cached X/Y `+0x2a0/+0x2a4` from the parent/start offset and logic `+0xd4/+0xd8`. In the tested start-X=0.5 case, parent position was `(0,0,500)` and cached current XY `(50,150)`.

#### Segment construction and a verified cross-section

Arc render initializer `0x13b5ff8` builds containers using `0x17ec490` at render `+0x2b8/+0x2c0`. Adjacent points from logic render-geometry vector `+0x100` are passed to segment factory `0x14f3f40`, then initializer `0x16a7e5c`, with first/last flags.

Recovered RTTI **ArcSegment** is at `0x1b93400`, vtable `0x1b00768`, allocation `0x360`. Endpoints are stored at `+0x2f4/+0x300`; two three-point cross-sections are stored at `+0x30c/+0x330`.

Cross-section routine `0xd06628` reads global i32 width `0x1c01094`. If its arc-mode argument is nonzero, it uses signed integer width division **by 6**, with truncation toward zero. Then:

```text
h = trunc_i32(width/2)
v = trunc_i32(width/4)
left  = (x-h, y-v, z)
apex  = (x,   y+v, z)
right = (x+h, y-v, z)
```

This builder uses a fixed XY cross-section. It does not itself calculate a tangent-aligned frame. Width=90 was a **synthetic test input**, not a recovered universal default. At P=(10,20,−30), mode 0 produced `(-35,-2,-30),(10,42,-30),(55,-2,-30)`; mode 1 produced `(3,17,-30),(10,23,-30),(17,17,-30)`.

**Unknown:** complete triangle/index topology, UVs, every cap/connection rule, zero-duration topology, width initialization across scenes, and actual arc shader/material selection. Two triangular cross-sections do not by themselves establish the full mesh.

Initializer `0x16a7e5c` creates sprite components through `0x16fd3c0` and references `img/arc_body_hi.png` and `img/1080/arc_cap.png`. Both textures are absent from this ZIP. Trace-color metadata is recognized, but the final override chain is not completely closed.

### 6. Timing-group angles are a separate transform

**Confirmed.** Timing-group parser `0x8c847c` stores integer `anglex`/`angley` at parsed object `+0x10/+0x14`. Conditional chart-builder blocks `0x1864e4c..0x1864e74` and `0x1865040..0x1865068`, controlled by chart `+0x110`, convert through double arithmetic:

```text
logic.angleX = f32(double(integerAngleX)*pi/180/10)
logic.angleY = f32(double(integerAngleY)*pi/180/10)
// logic +0x58/+0x5c, radians
```

900 input units become 90 degrees. These fields are radians, unlike the Camera Node Euler fields.

Arc-tap adjustment routine `0x1893f3c` constructs identity, calls `0x134fc8c` with angleY, then `0x1653a54` with angleX, transforms `(0,0,childDepth,1)`, and applies the result through `0x1873cfc` relative to the parent. Native matrix-helper execution establishes **Ry(angleY)*Rx(angleX)** for this path. The complete group transform of every renderer is not inferred from this single arc-tap path.

### 7. Scene-control dispatch and visible-state changes

**Confirmed.** Parser `0x7f2628` / classifier `0x1090060` recognizes the mapping below. Runtime LogicSceneControl has RTTI `0x1b8a6b0`, vtable `0x1aff8e8`, initializer `0x1792e18`; relevant fields are `+0x18 time`, `+0x50 group index`, `+0x64 kind`, `+0x68 f32 value`, `+0x6c i32 value`. Event processing uses the strict-time/processed guard in `0xf8056c`, then **`0xf80824 → 0x1514c64`**.

Handler-owner fields include model `+0x2a0`, rig `+0x2a8`, visual wrapper `+0x2b0`, track collection `+0x2b8`, chart `+0x2c0`, visual-feature enable byte `+0x2c8`, and current track opacity i32 `+0x2cc`.

| Kind / identifier | Verified handler behavior | Limits |
|---|---|---|
| 0 `trackdisplay` | Replace key `trackFadeControl`; schedule opacity callback; update track-node collection | Visibility helper and complete scene membership remain partial |
| 1 `redline` | Create `img/redline.png` sprite; set position/scale/opacity/mask; queue fade/sequence actions; schedule removal with `scene_redline_…` key and float parameter as delay | Texture absent; full randomized flicker sequence not reproduced |
| 2 `arcahvdistort` | Find `ARCAHV_DISTORT` node, make visible, stop actions, enqueue fade-to using float duration and integer target | Shader/content of that node not established |
| 3 `arcahvdebris` | Same control pattern for `ARCAHV_DEBRIS` | Debris geometry and complete node lifetime unresolved |
| 4 `hidegroup` | `0x160a828(chart,group,int!=0)` writes group/note render-hidden state | Does not itself write tested input-enabled byte |
| 5 `enwidencamera` | `0xd59c24` stores model transition fields `+0x54/+0x58/+0x5c` | Full connection to actual camera FOV not established |
| 6 `enwidenlanes` | Stores transition fields `+0x68/+0x6c/+0x70` | Complete visible lane-geometry consumer not established |
| 7 other | No recognized effect established | Recognition is not proof of a visual implementation |

Kinds 0–3 are gated by owner `+0x2c8`; kinds 4–6 take their state paths independently of that gate. `trackhide`/`trackshow` parse as `trackdisplay` with integer 0/255.

#### Track opacity: a complete scene-control chain

Handler `0x1514c64` first unschedules `trackFadeControl` through `0x10846c0`. The new closure (vtable `0x1a96b30`) captures:

```text
+0x08 owner; +0x10 i32 counter=0; +0x14 i32 limit=100;
+0x18 i32 startingOpacity; +0x20 event pointer
```

Constant pool `0x417760` contains exactly `{0,100}`. Scheduling call `0x81565c` receives interval `f32(event.floatValue/100)`, zero delay, repeat argument 99, and the same key. Callback **`0x1501dfc`** ignores its dt for interpolation and computes:

```text
counter += 1
u = min(f32(counter)/f32(limit),1)
opacity = trunc_i32(f32(start + f32(u*f32(f32(target-start)*u))))
owner.currentTrackOpacity = opacity
0xef18e8(owner.trackCollection, opacity)
```

`0xef18e8` traverses its pointer vector at `+0x300/+0x308` and calls each node's opacity virtual `+0x470`. This closes event → scheduled callback → native arithmetic → visible-node opacity state. For a 255→0 ramp, ticks 1/25/50/75/100 give 254/239/191/111/0. For 0→255 they give 0/15/63/143/255. The original callback and propagation loop were executed; the scheduler itself was not.

The handler additionally calls `0xd5588c` for target ≤254 and `0xd52508` for target ≥255 on the visual wrapper. Their complete visibility consequences are not reconstructed. Redline removal closure `0xfa0570` stops its captured sprite's actions and removes it through virtual `+0x258(false)`.

Overlap evidence is bounded: the track key is explicitly replaced; distort/debris stop existing actions on their target node before a new fade; widening overwrites shared transition state; hidegroup writes the latest boolean immediately. No general stack/restoration policy is established. The distort/debris handler does not show an automatic return to the previous opacity.

#### Hidegroup and widening must not be called presentation-only

`0x160a828` writes a byte at group descriptor `+0x02` and logic `+0x55` for matching group indices; ArcNote children in `+0x120/+0x128` receive the same render-hidden byte. Tap, hold, and arc renderers read it. Synthetic hide/unhide tests preserved logic input-enabled `+0x54`. This establishes the specific field behavior, not universal behavior of every gameplay modifier.

For the widening controls, native frame blocks in `0x10a7550` compute:

```text
u = f32(f32(E-startTime)*0.5 / durationValue)
G = direction>=1 ? clamp(1+u,1,1.5) : clamp(1.5-u,1,1.5)
model[+0x60] = G; previous G copied to +0x64

v = f32(f32(E-laneStartTime)/laneDurationValue)
W = laneDirection>=1 ? clamp(v,0,1) : clamp(1-v,0,1)
model[+0x74] = W
```

The raw f32 durationValue is used here: this code does **not** divide it by 1000 like the camera action builders. Tested finite positive-duration boundaries are reported below; zero duration/NaN behavior is not generalized.

These shared G/W fields already feed spatial eligibility in Expedition 004. Thus widening cannot safely be described as a purely visual effect. A newly traced rendering consumer at `0x10a7810..0x10a78c4` reacts when G changes and calls **`0x1554a84`** with `1-(2/3)*G` for relevant note child collections. That helper sets opacity `trunc_i32(130*t)` on children after the first. A special-song restoration branch involving `rivenpilgrim` exists at `0x10a7640..0x10a76a8`, but its complete conditions and restoration behavior were not tested. No claim that `enwidencamera` directly changes projection FOV is made.

### 8. Feedback colors and particle resource evidence

**Confirmed.** Accepted arc feedback reaches `0x155241c`, which sets render byte `+0x300`; updater `0x11b7d78` reads that state. This expedition does not close the full accepted-latch release lifecycle. A render-start call through `0x18ed2c4` was captured, not executed as a complete graphics effect.

Conflict handling in `0x11b7d78` loads RGB **(230,50,50)** around `0x11b83a4` and calls `0x15a0eac`. The latter reads segment base RGB at `+0x354..+0x356` and computes, per component:

```text
baseFactor = (t==0) ? 1 : max(1-t,0)
component = trunc_i32(target*t + base*baseFactor)
```

It forwards the constructed color through child color virtual `+0x4a0` for segment children `+0x2a8/+0x2a0` and optional `+0x2d8/+0x2e0`. For t in `[0,1]`, this is linear interpolation toward the conflict color, returning to the stored base at t=0. It is not a white reset. The tested child output is detailed below; behavior for out-of-range values and downstream byte conversion is not generalized.

The caller's blend weight uses its feedback counter and a denominator derived from the judgment interval (including a special −1 branch), with an upper clamp to 1. Full counter lifecycle and all interval cases are not reconstructed here.

#### Assets, loads, and triggers are different evidence levels

The ZIP contains these plist assets:

- `assets/particle/particle_arc.plist`
- `assets/particle/particle_arc_mirai_conflict.plist`
- `assets/particle/particle_arc_mirai_light.plist`

Metadata establishes maxParticles=5, particle lifespan 0.49, duration −1, emitterType=1, blend source/destination 770/1, and `textureFileName=particle_arc.png`, with different color parameters. This describes assets, not runtime selection by itself.

Native initialization **`0x7ab65c`**, reached in renderer construction `0x12967e4` (call near `0x129766c`), belongs to recovered RTTI **NoteBurstRenderer** (`0x1a8af68`, vtable `0x1b89e48`). It references the three resource strings at `0x576851`, `0x57e39c`, and `0x53727f`, respectively, and calls factory **`0xd3d8c8`** at `0x7ab8c4/0x7aba80/0x7abb00`.

Factory `0xd3d8c8` allocates `0x5b0` bytes for recovered RTTI **cocos2d::ParticleSystemQuad** (RTTI `0x1a8c820`, vtable `0x1abd450`), reaching initialization `0x11de120`. Special resource-key branches and a side-like renderer field select variants; initialization sets scales 1.9 for the special variants and 2.1 for the normal path. A subsequent `0x9ad0d8` sets active byte `+0x41c`, elapsed `+0x2d0` to zero, and clears particle-count buffer state. The particle pointers are retained in the NoteBurstRenderer vector beginning at `+0x2b0` (end `+0x2b8`, capacity `+0x2c0`).

**Unknown:** the complete contact/success/release call paths that activate each stored particle system during gameplay. In particular, filenames alone do not prove that a particular judgment or conflict always selects a particular plist. `none`, `arcahv`, and `desive` are not assigned a newly proven complete effect pipeline here.

The partial archive contains **zero PNG files**, 199 `.csb` files, and 27 `.fsh` files. Referenced note textures (`img/note.png` and variants), arc body/cap textures, redline texture, and `particle_arc.png` are absent. Available shader assets include glitch-related files, but no instruction-backed assignment of a particular arc shader was established. Their existence cannot substitute for missing texture/shader binding evidence.

## Recovered Pseudocode

All functions below are researcher descriptions. Arithmetic helpers `f32` and `trunc_i32` preserve the identified f32 and FCVTZS boundaries. Pseudocode intentionally stops at unresolved interfaces.

### Camera event, paired relative actions, and reset

```text
dispatchCamera(owner, event):                    // 0x192b5c8
    rig = owner.ptr_2a8
    if anyNonzero(event.f32_64,68,6c):
        addPairedAction(rig, MoveBy, (a,b,c), event.duration_98, event.easing_80)
    if anyNonzero(event.f32_70,74,78):
        addPairedAction(rig, RotateBy3D, (e,d,f), event.duration_98, event.easing_80)
    if event.easing_80 == "reset": resetRig(rig)

addPairedAction(rig, kind, delta, durationMs, easing):
    if rig.lookAtLatch:
        lookAt(rig.primary, rig.target, (0,1,0))
        lookAt(rig.secondary, rig.target, (0,1,0))
        rig.lookAtLatch = false
    duration = max(f32(f32(durationMs)/1000), 2^-23)
    action = constructNativeRelativeAction(kind, duration, delta)
    if easing == "qi": action = EaseCubicActionIn(action)
    else if easing == "qo": action = EaseCubicActionOut(action)
    runAction(rig.primary, action)
    runAction(rig.secondary, action.clone())

stepInterval(action, dt):                         // 0x12a5a80
    if action.firstTick:
        action.firstTick = false
        action.elapsed = 0
    else: action.elapsed = f32(action.elapsed + dt)
    u = clamp(f32(action.elapsed/action.duration), 0, 1)
    action.update(u)                              // wrapper applies cubic if present

updateMoveBy(action, u):                          // 0x8e2b70
    action.base += target.position - action.lastWritten
    p = action.base + action.delta*u
    target.setPosition3D(p)
    action.lastWritten = p

updateRotateBy3D(action, u):                      // 0x11c0c9c, 3D branch
    target.setRotation3D(action.startEuler + action.delta*u)

resetRig(rig):                                   // 0xb0bd74
    stopActionsForTarget(rig)                     // child cancellation NOT established
    for camera in [rig.primary, rig.secondary]:
        camera.lookAt(rig.target, (0,1,0))        // before restoring home position
        camera.setPosition3D(rig.homePosition)
    rig.lookAtLatch = true
```

### Matrix cache and render use

```text
refreshView(camera):                             // 0xe29b94
    W = camera.nodeToWorldTransform()
    if bytes(W) != bytes(camera.cachedWorld_328):
        camera.cachedWorld_328 = W
        camera.byte_410 = 1; camera.byte_478 = 1
        camera.view_2e8 = nativeInverse(W)

getPV(camera):                                   // 0x10eff1c
    refreshView(camera)
    if camera.byte_410:
        camera.byte_410 = 0
        camera.combined_368 = nativeMultiply(camera.projection_2a8, camera.view_2e8)
    return camera.combined_368

renderScene(scene):                              // recovered core of 0x10dd3d8
    for camera in scene.cameraVector:
        if not camera.isVisible(): continue
        visitingCamera = camera
        director.setMatrix(stack=1, matrix=getPV(camera))
        camera.prepare()
        scene.visit(renderer, camera.mask_412, otherNativeArguments)
        renderer.flush()
        camera.finish()
    // Exact GPU commands and shader bindings intentionally unresolved.
```

### Note depth and arc geometry consumers

```text
updateBasicDepth(note, groupOffset):              // 0x1017d80
    note.i32_30 = trunc_i32(f32(f32(note.i32_38) + groupOffset))
    note.i32_34 = trunc_i32(f32(f32(note.i32_3c) + groupOffset))

updateTapRender(render, E):                       // bounded core of 0xf20c28
    logic = render.logic_2a8
    if render.visible and logic.i32_34 >= 301 and logic.isProcessed():
        render.setVisible(false)
    x = integerOrFloatingPlacement(logic.chartNote) // equations above
    render.cachedXY = (x,4)
    render.setPosition3D(x,4,logic.i32_30)
    if logic.byte_55: render.setOpacity(0)
    updateQuadAndDepthOpacity_UnrecoveredBranches()

updateArcCurrentPosition(model):                  // bounded core of 0x19f3d4c
    for arc in model.selectedNotes recognized as ArcNote:
        samples = arc.vec_e8
        segment = selectAdjacentSegmentNative(samples, arc.i32_30)
        // selection, degenerate, orientation and ownership branches not expanded
        P0,P1 = segment with parent depth added to Z
        raw = 1 - dot((0,0,-1), -P1) / dot((0,0,-1), P0-P1)
        u = clamp(raw,0,1)
        p = P0 + (P1-P0)*u
        active = 0<=raw<=1 and arc.startTime<=E<=arc.endTime
        arc.setActivePlaneFlag(active)
        if E<=arc.endTime: arc.currentXY_d4_d8 = p.xy
        normalArcConnectedAndReleaseHandling_NotFullyRecovered()

buildArcCrossSection(P, mode):                    // 0xd06628
    width = global_i32_1c01094
    if mode != 0: width = signedTruncDivide(width,6)
    h = signedTruncDivide(width,2)
    v = signedTruncDivide(width,4)
    return [(P.x-h,P.y-v,P.z), (P.x,P.y+v,P.z), (P.x+h,P.y-v,P.z)]

constructArcRender(render, logic):                // bounded 0x13b5ff8
    render.logic_2a8 = logic
    createNativeContainers_17ec490()
    for adjacent points in logic.vec_100:
        segment = factory_14f3f40(points, firstFlag, lastFlag, nativeOtherArguments)
        // initializer stores endpoints/cross-sections and creates sprite components
        // complete indices/UVs/material state unresolved
```

### Scene-control state and feedback

```text
sceneControl(owner,event):                        // 0x1514c64
    if event.kind == 4:
        setGroupRenderHidden(owner.chart,event.group,event.intValue!=0)
    else if event.kind == 5:
        model.cameraTransition = (event.time,event.intValue,event.floatValue)
    else if event.kind == 6:
        model.laneTransition = (event.time,event.intValue,event.floatValue)
    else if owner.visualFeatureEnabled:
        if event.kind == 0:
            unschedule("trackFadeControl")
            scheduleTrackOpacityRamp(start=owner.opacity,target=event.intValue,
                                     interval=f32(event.floatValue/100),repeat=99)
            additionalTrackVisibilityHelper(event.intValue) // incomplete
        else if event.kind in [2,3]:
            node = findNode(event.kind==2 ? "ARCAHV_DISTORT" : "ARCAHV_DEBRIS")
            node.setVisible(true)
            node.stopActions()
            node.runAction(FadeTo(event.floatValue,event.intValue))
        else if event.kind == 1:
            createRedlineSpriteAndActions_PartiallyRecovered()

trackOpacityCallback(capture):                    // 0x1501dfc → 0xef18e8
    capture.counter += 1
    u = min(f32(capture.counter)/f32(capture.limit),1)
    d = f32(f32(capture.event.intValue)-f32(capture.startOpacity))
    opacity = trunc_i32(f32(f32(capture.startOpacity)+f32(u*f32(d*u))))
    capture.owner.opacity = opacity
    for node in capture.owner.trackCollection.vector_300:
        node.setOpacity(opacity)

blendArcColor(segment,target,t):                  // 0x15a0eac, tested t in [0,1]
    b = (t==0) ? 1 : max(1-t,0)
    rgb = truncComponents(target*t + segment.baseRGB_354*b)
    setColorOnNativeSegmentChildren(rgb)
```

## Validation

### Method and scope

Unicorn executed the original mapped ARM64 `.text` of the identified library, with ELF RELATIVE relocations applied. Synthetic native objects/vtables, timing vectors, and geometry buffers supplied controlled inputs. Capstone disassembly and `.eh_frame` bounds were used to inspect routines and distinguish function entries from incidental references. Test assertions passed in the final run.

No physical device, game screenshot, GPU draw, audio replay, complete chart/scene playback, or full visual comparison was performed. The paired-action queue, external math imports, resource-loading dependencies, and selected output methods require hooks. Native arithmetic was retained for the calculations being tested.

### Native execution groups and observed results

| Group / executed addresses | Inputs and expected behavior | Observed output |
|---|---|---|
| Camera parser/runtime init `0x138f560`, `0x81d3e4` | Typed tokens time=1000, six floats 1..6, `qi`, duration=2000 | Runtime time=1000, floats 1..6, `qi`, duration=2000; field mapping assertions pass |
| Event handler/builders, native constructors/clone/start/step/update: `0x192b5c8`, `0x10a2b94`, `0x13a7938`, `0xf1b510`, `0x16c5bc8`, `0x144471c`, `0x836ea8`, `0x12a5a80`, `0x8e2b70`, `0x11c0c9c`, wrappers | Start position (10,20,30), Euler (0,0,0), event deltas (1,2,3)/(4,5,6), duration2s; first dt=.7 then1s | Four queued actions (two kinds × two cameras). First tick causes no delta. At second tick: linear/unknown position (10.5,21,31.5), Euler (2.5,2,3); qi position (10.125,20.25,30.375), Euler (.625,.5,.75); qo position (10.875,21.75,32.625), Euler (4.375,3.5,5.25) |
| Easing leaves `0x9aa5a8`, `0xf0b7e0` | u=0,.25,.5,.75,1 | qi=0,.015625,.125,.421875,1; qo=0,.578125,.875,.984375,1 |
| Duration constructor `0xf1b510` | seconds −1,0,.001,2 | `2^-23`, `2^-23`, f32(.001),2 |
| Original setters/local/world/view/PV routines `0xd415dc`, `0xdc4348`, `0x17c5b74`, `0xe29b94`, `0x10eff1c`, `0x1410688`, `0x11e1bfc`; projection `0x197341c`, unprojection `0x16d3dcc` | Controlled position (10,20,30), no rotation; independent axis rotations; then action-modified states with FOV60, aspect1280/720, near1/far10000 | View translation (−10,−20,−30); +90 axis outcomes described above. After each of four easing cases, projected/unprojected world (2,3,−20) returns within .005 world units. PV dirty byte cleared |
| Reset `0xb0bd74` and original look-at/rotation/position helpers | Two synthetic cameras, home (0,900,900), target (0,−550,−2000) | Both return to home; latch set; stop-target captures rig. Euler depends on pre-reset position because look-at precedes home assignment |
| Group angle conversion block `0x1864e4c..0x1864e74`, matrix helpers `0x134fc8c`, `0x1653a54`, vector transform `0x197341c` | (ax,ay)=(0,0),(900,0),(0,900),(900,900),(−900,3600); vector (0,0,1,1) | Converted radians and Ry*Rx results agree with independent equations within f32 tolerance |
| Scroll `0xcf918c` + depth updater `0x1017d80` | Timing [0,1000]/scale2 and [1000,2000]/scale−4; E=0,500,1000,1500,2000; pre-depths −500/−1000 | Integrator 0,−250,−500,−375,−250; depth pairs (−500,−1000),(−250,−750),(0,−500),(−125,−625),(−250,−750) |
| Whole cache producer `0x19f3d4c` | Actual ArcNote RTTI, trace-mode flag1, two samples described above, chart interval1000..2000, E1500, parent depth0/500/1000 | Current XY (0,100)/(50,150)/(100,200) |
| Whole tap updater `0xf20c28` including original Node position and vertex writes | Actual RenderTapNote vtable, synthetic child; lanes1/3/4/6 with depths−10000/−5000/0/300 | Positions (−1063,4,−10000),(−213,4,−5000),(212,4,0),(1062,4,300) |
| Arc render block `0x11b7e6c..0x11b7f3c` | StartX=.5, depth500, cache(50,150) | Parent (0,0,500); cached renderer XY (50,150) |
| Cross-section `0xd06628` | Global width90, P=(10,20,−30), mode0/1 | Exact nine-float sections listed above; signed /6 branch verified |
| Widen handler `0x1514c64`, setter `0xd59c24` | Kinds5/6; time1234,float2.5,int7 | Corresponding time/direction/f32 duration fields set to 1234,7,2.5 |
| Widen frame block `0x10a7584..0x10a76f8` | start0,duration1000; E=0/500/1000/2000; direction1 or0 | Direction1 G=1/1.25/1.5/1.5, W=0/.5/1/1; direction0 G=1.5/1.25/1/1, W=1/.5/0/0 |
| Hidegroup handler/helper `0x1514c64`, `0x160a828` | Group0 with ArcNote and arc-tap child; hide1 then0; input byte+54 initially1 | Both render-hidden bytes become1 then0; input byte remains1; other-group note excluded |
| Color blender `0x15a0eac` | Base(100,150,200), target(230,50,50), t=0/.25/.5/1 | (100,150,200)/(132,125,162)/(165,100,125)/(230,50,50) at captured child setColor |
| Track callback/propagator `0x1501dfc`, `0xef18e8` | start/target255→0 and0→255; ticks1/25/50/75/100/101; two track nodes | Down254/239/191/111/0/0; up0/15/63/143/255/255; both node output calls match stored owner opacity |

### Hooks, stubs, and unexecuted components

- Allocation/new/imported memory, reference-count/autorelease, string, destructor, and unrelated environment helpers were isolated as in the earlier expedition harness. Destructors `0x19f2e40`, `0x9fc7fc`, and `0xc7fd5c` were no-ops in the scoped tests.
- Camera typed-token helpers `0x18905f4/0x19070d8/0x14be280` return prepared values, and punctuation guard `0x8d48e4` is stubbed. Native parser control flow, parsed-object writes, runtime field writes, and the event handler were executed; allocation imports were hooked. This is not a new full-text lexer test.
- `runAction` `0xc7820c` captures the target/action pair. The tests then call the **original** action clone/start/step/update virtuals. The full ActionManager queue and Scheduler are unexecuted.
- `sincosf` PLT `0x1a6e1b0`, `fmodf` `0x1a6de80`, `tanf` `0x1a6f000`, `atan2f` `0x1a6ed10`, and `asinf` `0x1a6efe0` use host math with f32 register/memory boundaries. Native Node quaternion/matrix, inverse, multiplication, action arithmetic, and projection/unprojection instructions execute. Cross-platform libm bit identity is not claimed.
- Director/frame-dimension helpers `0xa4227c/0xf09110` supply controlled dimensions. ActionManager stop `0xf14f9c` captures its target; full cancellation is not executed.
- Synthetic RTTI support recognizes the prepared object types; complete scene object lifetimes and dynamic casts outside the test domain are not validated.
- Arc cache tests use trace mode to avoid colored-arc ownership/feedback branches. Arc renderer execution stops after its position/cache block, before remaining segments and graphics work. Group angle tests enter a conversion block with the original double constants supplied in the expected stack slots; the entire chart builder is not executed.
- Widen frame tests enter after timeline update with a prepared effective clock and avoid the special-song restoration branch. Full pause, seek, and song-transition rendering behavior remains unknown.
- Child `setColor` and track-node `setOpacity` are captured at synthetic virtual output functions. The native color arithmetic and opacity iteration execute; GPU color/opacity behavior does not. `0x185ad00` returns the prepared visual wrapper and `0x18ed2c4` records a render-feedback start.
- No particle-system resource loader or actual shader program was executed under Unicorn. Particle conclusions above are from native callsites/RTTI and plist metadata.

## Unresolved Mysteries

1. Exact ActionManager/Scheduler update ordering relative to the chart clock, pause/resume, and seeking; child-camera action cancellation on reset and arbitrary overlapping camera actions.
2. Full ancestor transforms and special-scene camera paths beyond the controlled unit-scale camera case; complete consumers that visually implement `enwidencamera`/`enwidenlanes` and the special-song restoration branch.
3. Full hold/flick/arc-tap draw geometry, all note opacity/culling boundaries, render object destruction and batching. The tap processed-depth expiry is only one recovered branch.
4. Arc triangle/index/UV topology, complete cap connectivity, zero-duration arcs, default width initialization, trace-color overrides, and shader/material assignments.
5. Complete accepted/conflict latch lifecycle, counter-derived blend timing, and the exact gameplay trigger/selection chain for each stored particle system and `none`/`arcahv`/`desive` effect mode.
6. Actual visible redline/distortion/debris content, unavailable textures, GPU-side correctness, and pixel-level reproduction.

These are bounded gaps in this expedition, not authorization or a plan to begin another expedition. No contradictory historical finding is silently replaced.

## GitHub Status

Authorized changes are limited to this new report and an appended Expedition 007 entry in `context.md`, on the existing `main` branch. Existing report files, README, project instructions, libraries, and assets are outside the modification scope.

Exact publication commit SHAs and pinned read-back/diff verification are recorded in the headquarters return report. They are intentionally not fabricated or inserted as self-referential commit hashes inside this commit's content.
