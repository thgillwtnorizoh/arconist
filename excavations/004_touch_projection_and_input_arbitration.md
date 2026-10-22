# Expedition 004 — Touch Projection, Spatial Judgment & Input Arbitration

Date: 2026-10-22. Primary evidence: supplied `arccopy.zip`. Authoritative instructions and current GitHub `context.md` and Expedition 001–003 subject documents were read before investigation.

## Result

Reconstructed Android/JNI contact transport, viewport-to-design coordinate conversion, camera unprojection and plane intersections, lane selection and width expansion, arc/arc-tap spatial predicates, initial-touch candidate ordering and consumption, and several distinct duplicate-prevention mechanisms. Executed isolated original ARM64 routines, including a synthetic full initial-touch-to-tap-judgment path.

This documents the supplied binary, not every Arcaea version. It does not establish a fixed screen-pixel hitbox, guarantee physical-device behavior, or replace the full renderer/input system.

## What I Found

### Evidence identity, conventions, and historical discrepancy

Main evidence: `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, ELF Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. Extracted bytes were compared directly with the uploaded ZIP. Native addresses are ELF virtual addresses before relocation; executable/rodata addresses cited here equal file offsets. Vtable/GOT locations require segment translation and ELF relocations. Native function labels and field names below are researcher descriptions unless backed by RTTI.

**Confirmed** means decoded instructions, smali, relocation-backed identity, or explicitly scoped native execution. **Interpretation** gives an explanatory meaning; **unknown** marks missing provenance/lifecycle. Equations assume ordinary finite values and nonzero scale/dimensions; float32 rounding and truncation matter at exact boundaries.

**New discrepancy:** Expedition 002 described the spatial depth cutoff as -4000. Instruction `0x927620` loads `w8=-0x3b860000`, i.e. bits `0xc47a0000`, which decode to **-1000.0**, and `0x92762c` rejects `point.z <= -1000`. Isolated execution confirms rejection at -1000 and acceptance immediately above it with other predicates satisfied. Earlier text is preserved; this entry records contradictory evidence separately, without treating it as authorization to edit Expedition 002.

Current context/Expedition 002 already contain an authorized b/s-ID correction (`b=1`, `s=0`). Expedition 003's historical pending-confirmation wording is preserved; it is not a new unresolved blocker.

### 1. Android transport, timestamps, and three kinds of identifier

Exact smali paths:

- `smali_classes3/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali`
- Its `$5`–`$10` Runnable classes, selected by action; each captured-field wrapper forwards to the renderer.
- `smali_classes3/org/cocos2dx/lib/Cocos2dxRenderer.smali`

`onTouchEvent` first captures one `getTouchTimestampNow()` value, using `TimeUnit.MILLISECONDS.convert(SystemClock.elapsedRealtimeNanos(), NANOSECONDS)`. It then reads pointer count, pointer IDs, X/Y, and `getSize(i)*getPressure(i)` into arrays. Action branches handle DOWN/POINTER_DOWN, UP/POINTER_UP, MOVE, and CANCEL. Scalar down/up use the selected pointer; move/cancel forward arrays. Runnables retain the captured timestamp before `queueEvent`, so it is not first sampled after the GL-thread queue delay. The inspected method does not use `MotionEvent.getEventTime()` or a historical motion-sample loop.

Renderer wrappers directly forward to JNI:

| JNI export / VA | Signature | Native GLView virtual target |
|---|---|---|
| `Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeTouchesBegin`, `0xbe31a8` | `(IFFFJ)V` | `+0xe0` -> `0x97d784` |
| `...nativeTouchesMove`, `0x1706960` | `([I[F[F[FJ)V` | `+0xe8` -> `0x160b710` |
| `...nativeTouchesEnd`, `0xdda71c` | `(IFFFJ)V` | `+0xf0` -> `0x15af680` |
| `...nativeTouchesCancel`, `0xd8dc50` | `([I[F[F[FJ)V` | `+0xf8` -> `0x1556de4` |

Scalar JNI sign-extends the Java identifier to 64 bits, passes X/Y and the pressure product unchanged, and supplies an additional float 1.0. Array JNI copies integer/float arrays, sign-extends IDs into a 64-bit array, constructs a corresponding 1.0 array, and forwards count/arrays. No screen-axis swap or pixel-to-game conversion is performed in these JNI stubs. GLView and GLViewImpl vtable address points are `0x1ab6108` and `0x1b20d60`; RTTI names are at `0x45df07` and `0x4b2be9`.

Three IDs must be kept distinct:

1. Android pointer ID: map key from JNI.
2. Engine touch slot: free bit index **0..14** from mask `0x1bfebd4`; pointer map based at `0x1bf1a90` maps Android ID to slot, slot-pointer array at `0x1beef90`. Begin ignores an already-mapped ID (`0x97d874–0x97d8a8`); no free one of these 15 slots means this path skips creation.
3. Gameplay contact ID: begin callback `0x194ff80` assigns a separate incrementing value from global `0x1bf25f4` to touch `+0x34` at `0x195007c–0x195009c`. Arc ownership uses this ID. It is not physical-finger recognition across lifts.

Recovered `cocos2d::Touch` fields (vtable `0x1ad7fd8`, RTTI `0x478dea`):

| Offset | Instruction-backed role |
|---|---|
| `+0x0c` | Engine slot ID |
| `+0x10` | Initial-position latch |
| `+0x14/+0x18` | Initial converted X/Y |
| `+0x1c/+0x20` | Current converted X/Y; gameplay getter `0x13e0324` reads these directly |
| `+0x24/+0x28` | Previous converted X/Y |
| `+0x2c` | Java size-times-pressure value |
| `+0x30` | Additional supplied force-like value, 1.0 from JNI |
| `+0x34` | Generated gameplay contact ID |
| `+0x3c` | Last-frame effective gameplay time copied on begin |
| `+0x40` | 64-bit timestamp stored by native begin |

At `0x10a75c8`, frame update writes effective game time to `0x1bf93e8`, which begin copies to `+0x3c`. This identifies its provenance more precisely than Expedition 003's provisional “timing-related value.”

Move updates current/previous coordinates and force fields (`0x160b83c–0x160b87c`), reusing the mapped object. It does not overwrite `+0x40` in the inspected path. End/cancel wrappers dispatch action IDs 2/3 through `0x95e32c`; their wrapper register rearrangement drops the timestamp argument. Thus transport of a Java timestamp does not mean every action updates a per-contact timestamp, and it does not prove that judgment uses that timestamp.

### 2. Viewport conversion and camera-dependent projection

**Viewport conversion:** begin `0x97da38–0x97da80`, move `0x160b83c–0x160b864`, and end/cancel `0x95e480–0x95e4a4` perform:

```text
designX = (inputX - GLView.float_1c) / GLView.float_48
designY = (inputY - GLView.float_20) / GLView.float_4c
```

These fields act as viewport-origin offsets and X/Y scale factors. The converted coordinates are stored in Touch `+0x1c/+0x20`; Y is not flipped here. Begin copies them into both initial and previous position. These design coordinates are already different from raw device coordinates when scaling/letterboxing is active.

**Camera unprojection chain:** initial touch `0xeec024` reads touch coordinates, calls `0x8a3fac` -> `0xea3e84` -> `0x16d3dcc`. Model `+0x20` points to a wrapper whose `+0x2a8` is the camera. `0xea3e84` obtains dimensions from Director `+0x180` via `0x1970d48`. For finite screen/design dimensions W,H, the core routine builds:

```text
v = (2*x/W - 1, 2*(H-y)/H - 1, 2*zInput - 1, 1)
q = inverse(cameraCombinedMatrix) * v
world = q.xyz/q.w if q.w != 0 else q.xyz
```

This is a real Y flip, NDC mapping, inverse-matrix transform, and homogeneous divide. Helpers:

- `0xe29b94`: obtains camera/node transform through virtual `+0x410`, compares cached matrix at `+0x328`, and when changed stores its inverse at camera `+0x2e8`, setting dirty flags.
- If camera byte `+0x410` is set, `0x16d3e50–0x16d3e60` computes camera matrix `+0x368` from matrices at `+0x2a8` and `+0x2e8` using `0xa57c50` -> `0x11e1bfc`.
- `0x1344f34` -> `0xca3668` computes the inverse; `0x197341c` -> `0x16d4b40` transforms the four-component vector with column-major matrix arithmetic.

Interpretation: projection matrix times view/inverse-world matrix is the usual role of these camera fields; the offsets, multiplication and inversions are directly observed. All chart camera-event and parent-transform producers are not reconstructed here.

**Line construction and intersections:** `0xeec0c8–0xeec198` unprojects `(x,y,-1)` and `(x,y,+1)`; it sets origin to the +1 result and direction to normalized `(minus1Result-plus1Result)`. Note the actual z inputs: core unprojection maps them to NDC z **-3 and +1**. Substituting conventional input endpoints 0 and 1 would not be a literal reconstruction, even though both constructions can describe the same line for ordinary nonsingular cameras.

Plane helper `0xba8b04` stores normalized normal and `d=dot(normal,pointOnPlane)`. Intersection `0x129dee0` computes `t=(d-dot(n,origin))/dot(n,direction)` when the denominator is nonzero, otherwise t=0; result is origin+t*direction. It does not reject negative t and, for exact parallelism, returns the origin rather than an explicit “no intersection.”

- Lane selector `0x130733c` intersects with **Y=0**.
- Initial arc-tap spatial coordinates normally intersect with **Z=0**.
- If chart byte `+0x110` is true and camera position Z is negative, the initial arc-tap path switches to **Y=0** (`0xeec1ec–0xeec298`). Camera position is read via virtual `+0xe0`, resolved to `0x1154d54` in the Camera vtable; it reads node floats `+0x38/+0x3c/+0x40`.
- Continuous input `0x14858d4` independently builds per-contact projected data and invokes lane/arc checks; it is not the same first-consumed candidate loop as initial tap input.

### 3. Lane eligibility, internal units, and boundary asymmetry

`0x130733c` returns a packed pair: low 32 bits primary lane, high 32 bits secondary lane. Let P be the Y=0 intersection, X=trunc(P.x), E=model float `+0x74`, and G=model float `+0x60`. Their product-level labels are not assumed; G affects spatial width and E permits outer lane IDs.

Ordinary depth eligibility is **-500 < P.z < 500**, with both endpoints excluded. If chart `+0x110` is true and camera Z is either negative or strictly greater than 900, an alternate branch instead requires **P.z > -1000**, without the ordinary upper bound. Exactly camera Z=900 remains on the ordinary branch.

For an eligible point, primary classification uses the truncated integer X:

| X | Returned primary ID |
|---|---|
| X < -850, E>0 | 1 |
| Otherwise X < -425 | 2 |
| -425 <= X < 0 | 3 |
| 0 <= X < 425 | 4 |
| **X == 425** | **0** |
| X > 425, except next row | 5 |
| X > 850, E>0 | 6 |

Thus E<=0 leaves unbounded outer X assigned to 2/5 after depth eligibility; there is no fixed outer-edge rejection in this function. Exactly -425 goes to 3, exactly 0 to 4, exactly 850 to 5. Positive values such as 425.9 truncate to 425 and follow its zero-return branch. This is instruction-backed asymmetry, not a conventional lane diagram inferred from appearance.

When G>1 and depth is eligible, let a=(G-1)*425*0.5. The routine classifies float positions X-a and X+a with corresponding -850,-425,0,425,850 tests, including the exact-425 zero case. It returns the left classification if it differs from primary; otherwise the right if that differs; otherwise secondary=0. G<=1 or failed depth leaves secondary=0. Only one secondary value is returned even if a very large G spans several lane boundaries.

**Caller caveat:** zero is frequently the absence of an additional lane. However initial candidate collection simply compares note position integer `+0x10` with the two returned integers. It does not explicitly require either lane result to be nonzero. Therefore a blanket “lane 0 can never match anything” claim is not established; continuous-position or unusual position objects require their own provenance analysis.

A nonzero explicit lane argument to `0xeec024` bypasses computed lane selection and sets secondary=0. Direct callers in `0xcd356c` exercise explicit-lane inputs; ordinary touchscreen begin calls with zero. That alternative must not be mistaken for touch projection behavior.

### 4. Arc and arc-tap spatial predicate

Shared helper `0x927384` receives `(model, point3D, targetXY, flag, suppliedWidthFloat)`. Here point is the projected touch point, and target is note geometry. Ordinary arc caller `0xc98490` passes flag=0; arc-tap caller `0xeec47c` passes flag=1, supplied width=212.0.

Observed global initialization at `0x1930aa4–0x1930ae4` sets:

| Location | Initial value | Use in spatial helper |
|---|---:|---|
| `0x1c0094c` | 180 | Half of this integer contributes horizontal extent |
| `0x1bef2e0` | 100 | Width contribution for flag=0 |
| `0x1bee968` | 250 | Vertical extent |
| `0x1bf6c9c` | 550 | Input Y clamp scale for one flag/mode branch |

These are observed initial globals, not proof that every lifecycle/configuration leaves them immutable.

Let h be GLView frame height obtained through `0xf09110` -> GLView virtual `+0xb0` -> `0xc0d108` (returns GLView `+0x14`, frame size). This is a separate dimension source from Director design size used in unprojection. Set delta=0 when h<=720, h-720 when 720<h<=960, otherwise 240. Define:

```text
base = 900 + (delta / -240) * 100   # ranges from 900 down to 800
scale = 2 if cameraZ < 0 else max(1, cameraZ/base)
```

Float32 operation order is preserved in native tests; exact-boundary predictions cannot simply use double arithmetic.

For flag=0, width contribution B is global 100. For flag=1, B is 212 if chart `+0x110` is false, otherwise trunc(suppliedWidthFloat). Thus the supplied 212 argument is not even used as the ordinary arc's width contribution in this helper.

Let half=floating(scale*trunc(global180/2)), bx=scale*B, by=scale*global250. Horizontal acceptance requires:

```text
target.x-half-bx < point.x < target.x+half+bx
```

Under initialized globals and scale=1: ordinary arc half-extent=190 internal units; ordinary arc-tap half-extent=302 internal units. Neither is a screen-pixel radius. The sums occur separately, affecting float32 edge rounding.

If flag=1 and chart `+0x110` is false, projected input Y is adjusted: Y<=100 becomes 100; Y>100 is capped to G*550 if it reaches/exceeds that cap. For normal G*550>=100 this is clamp(Y,100,G*550). If the cap falls below 100, preserve the literal piecewise behavior rather than using a standard clamp. Other flag/mode combinations leave Y unadjusted. The adjusted Y is then truncated toward zero to an integer and converted back to float for comparisons.

Vertical and depth acceptance require:

```text
target.y - by - (60*scale if flag else 0) < trunc(adjustedY)
trunc(adjustedY) < target.y + by
point.z > -1000
```

Every displayed inequality is strict. For flag=1 there is an extra lower-side margin; it is asymmetric. The Y clamp, integer truncation, frame-height/camera scale, and choice of plane all prevent interpreting these internal constants as a fixed rectangle on the touchscreen.

**Target geometry:** `0xc98490` rejects nonzero arc mode `+0xa4`, consults start time and byte `+0xd0`, and supports a caller-selected 120 ms lookahead. Nonzero-duration target X is `trunc(850*startX-425)+arc.float_d4`, target Y is `arc.float_d8`. For zero duration, target X is the quantized start X and target Y is `startY*global_i32[0x1bf6c9c]` (without the geometry sampler's +100 term). The eligibility branches are more specific than a universal time-window test: nonzero-duration arcs require byte `+0xd0`, or an initial-touch call with `now+120>=start`; zero-duration arcs allow byte `+0xd0` or `now+(initial?120:0)>=start`. This helper contains no separate end-time rejection; candidate-range/lifecycle handling remains relevant. Arc-tap initial input adds the parent's quantized start X to child position `+0x80`, takes child Y from `+0x84`, and calls the shared helper. The full current-cache producer remains outside this reconstruction.

### 5. Collection, ordering, tie-breaking, and consumption

Initial input routine `0xeec024` first rejects model bytes `+0x138/+0x139` when nonzero and updates the timeline. It clears the retained candidate vector at model `+0xb8/+0xc0/+0xc8`, then scans active logic pointer range model `+0xa0/+0xa8`, skipping objects with input byte `+0x54` zero.

Runtime casts, resolved via GOT pointers `0x1b96488/498/4c8/4b8`, identify LogicNote, LogicTapNote, LogicHoldNote, and LogicArcNote:

- **Tap:** compare its position-object integer `+0x10` against primary and secondary lane; append on either match. There is no touch-distance comparator or tap-time window prefilter in this collection branch.
- **Hold:** lane must match, `startTime < now+100`, and `now < endTime`; append. The initial collection threshold is strictly 100, distinct from the continuous hold path's 120 ms lookahead.
- **Arc:** visit child pointer vector `+0x120`, compute each arc-tap target, and append each child whose shared spatial predicate succeeds. The arc body itself is not appended as a tap candidate by this branch.

Append helper `0x1082558` pushes a pointer and retains it; no duplicate search is present in that helper. The collected range is sorted by `0xf6b514`. Its comparisons and sorting helpers `0x16af85c/0x96cc18` read **signed startTime at note+0x18 only**, ascending. No spatial distance, absolute timing error, contact ID, note type, or explicit secondary tie key is used by this sorter.

The implementation has size-dependent small sorting/partition/insertion branches and recursive calls. It is **not stable**: isolated execution produced equal-time reordering in a 31-element case. Equal timestamps therefore have no established source-order or type priority guarantee. No invented “closest first” tie-breaking rule is supplied.

After sorting, `0xeec4f0–0xeec570` scans in order:

- Tap/arc-tap -> `0x160ce28(model,note,touch.i32_34)`. If it returns false, continue. If true, stop the initial candidate loop. True includes the classifier's 101–120 ms miss path; it does not mean successful hit.
- Hold -> set its initial latch byte `+0xa8=1` at `0xeec6ec–0xeec6f4`, then stop. This is activation preparation, not direct tap-score recording.

If no candidate consumes the event, a mode/explicit-lane-gated fallback checks existing arc/hold coverage before requesting a generic sound. That fallback does not make the sorted candidate pass a nearest-note selection algorithm. Full product meaning of its mode fields is unresolved.

### 6. Duplicate prevention is layered

- **Engine contact duplication:** active Android pointer IDs are mapped once; duplicate begin is skipped. Move/end/cancel look up that ID and reuse the slot/object. End/cancel share `0x95e32c`, which updates final coordinates, frees the map/slot entry, and dispatches its action.
- **One initial consumption:** the ordered initial-touch candidate pass stops at the first true tap-classifier return or selected hold latch. This is not a universal one-contact/one-note restriction across continuous frames.
- **Resolved-note duplication:** tap classifier virtual slot 8 (`0x13b73ac`) and slot 6 (`0x180cf28`) inspect note bytes `+0x0c/+0x0d`. Ordinary tap acceptance `0x965e28` sets `+0x0d=1` and stores the supplied contact ID at note `+0x10` after requesting sound. Arc-tap acceptance `0xc78814` also sets `+0x0d` and contact `+0x10`, with parent-mode-dependent return behavior.
- **Arc color ownership:** Expedition 003's `0x15a90c4` uses generated contact ID `touch+0x34`, LogicColor owner `+0x28`, and claimed-ID vector at `0x1bfa3d8` to prevent ordinary cross-color claims. It includes established bypasses/release rules; those are not a universal exclusion for every note type.
- **Bookkeeping is not judgment gating:** callback `0x10e7008` compares pressure-product values within 0.00001 against a model vector; begin also records truncated coordinate pairs. The inspected move callback does not call the initial tap classifier. Those comparisons must not be rebranded as physical-contact identity or proof that same-pressure fingers cannot play notes. Continuous input later processes retained touches through `0x14858d4`.

### 7. Trace into established judgment

Confirmed call path for an ordinary touchscreen begin:

```text
Java onTouchEvent -> queued renderer handleActionDown
 -> JNI 0xbe31a8 -> GLView 0x97d784 -> engine event dispatch
 -> gameplay begin callback 0x194ff80 -> assign generated contact ID
 -> 0xeec024 -> unprojection / lane selection / collection
 -> 0xf6b514 -> 0x160ce28
 -> accepted recorder 0x1730290 or miss recorder 0x868e54
```

Listener binding is directly recovered at `0x130bdf0` (`GameModel::initializeTouchEvents` appears in callback RTTI). Factory `0xb981cc` creates `cocos2d::EventListenerTouchAllAtOnce` (vtable `0x1b8be30`), stored at model `+0x150`. It binds begin/move/end/cancel function objects at listener `+0x80/+0xb0/+0xe0/+0x110`: their vtables `0x1b929c0/0x1abb400/0x1ad9e18/0x1b50a78` resolve call operators `0x194ff80/0x10e7008/0xd88408/0x18ba6d8`. Registration `0x1942fc8` receives integer 20 at `0x130bf54–0x130bf58`; the complete relative ordering against other listeners is not inferred. Both end and cancel callbacks call cleanup `0xf9a50c` (`0xd88494`, `0x18ba764`), gated by model field `+0x148`; cleanup removes retained touch pointers and releases LogicColor ownership. GLView dispatches the constructed touch event via dispatcher `0x1980970` at `0x97dc40`. This is a listener-mediated relationship, not a direct single BL from GLView to the gameplay callback.

The tap classifier uses effective game time from model timeline `+0x30`, rather than reading Touch `+0x40` in this path. The caller has just updated the timeline; it does not demonstrate compensation for all Java queue/device latency.

For an unconsumed tap, absolute error <=25 produces ID0, <=50 ID1, <=100 ID2, 101–120 invokes miss and returns true, >120 returns false. Independent expiry can preempt late handling, as documented in Expedition 002.

**Executed synthetic trace:** identity cached camera, design dimensions 1280x720, touch design point (640,360), normal depth branch, lane 4 tap at 1000, timeline 1008, generated contact 77. The original `0xeec024` executes camera unprojection, line/plane operations, lane matching, native pointer append, candidate sort, and `0x160ce28`, reaching the hooked accepted-result recorder with ID0. Identity-camera projection is a test fixture, not a claim about the in-game camera.

**Executed arbitration example:** two eligible lane-4 taps at 1000 and 1049, collected in reverse order, timeline 1050. The routine sorts by start time and records exactly one result: ID1 for the earlier note's 50 ms error. It does not choose the later note's 1 ms error. Recorder side effects are hooked; this checks routing/classification, not a complete score/gauge update.

### Validation scope

Original ARM64 execution in Unicorn passed:

| Coverage | Cases |
|---|---:|
| Unprojection with native inverse/transform and homogeneous divide, three supplied matrices | 12 |
| Plane intersection, including exact parallelism | 3 |
| Lane boundaries, integer truncation, extended-lane gate, width expansion, depth branches | 115 |
| Spatial strict edges, frame heights, camera scales, flag/mode width choice and Y clamp | 333 |
| Native sort across sizes 0–1001, negative/duplicate timestamps | 65 |
| Shared spatial predicate followed by tap classification | 1 chain |
| Full initial touch -> collection/sort -> tap judgment | 1 chain |
| Two-candidate earlier-versus-closer arbitration | 1 chain |
| Already-blocked classifier rejection | 1 |

Harness supplies synthetic objects, cached camera matrices, frame size and camera-position getter; camera/node world-transform refresh is hooked. Full matrix inverse/vector arithmetic, line/plane routines, lane selector, spatial helper, native sorter and classifier execute. Engine type casts, object retain/release, timeline refresh in the full-input fixture, and result/UI callbacks are hooked. No Android device, real AFF chart, live renderer, or actual score/gauge side effects are executed. The supplied ZIP contains no AFF samples. Validation script/results are research intermediates; only the two authorized documentation files are committed.

## Pseudocode

The following preserves recovered decisions rather than inventing a complete engine. Floating-point operations are float32 unless noted; exact machine-operation ordering is available at the addresses above.

```text
transport_touch(id, inputX, inputY, pressureProduct, timestamp):
    # JNI: sign-extend id; additional force=1.0; no coordinate conversion.
    # GLView begin:
    if id already mapped: skip
    slot = first free bit among 0..14
    if no free slot: skip
    touch.current = ((inputX-view.offsetX)/view.scaleX,
                     (inputY-view.offsetY)/view.scaleY)
    touch.initial = touch.previous = touch.current
    touch.engineSlot = slot
    touch.pressureProduct = pressureProduct
    touch.extraForce = 1.0
    touch.beginTimestamp = timestamp
    map id -> slot -> touch
    dispatch begin event
    # Gameplay callback:
    touch.contactID = nextGeneratedID++
    touch.lastFrameGameTime = globalLastFrameTime
    initial_input(model,touch,explicitLane=0)

unproject(camera, size, p):                    # 0x16d3dcc
    v = (2*p.x/size.w-1, 2*(size.h-p.y)/size.h-1, 2*p.z-1, 1)
    update_cached_camera_matrices_if_needed()
    q = inverse(camera.combinedMatrix) * v
    return q.xyz/q.w if q.w != 0 else q.xyz

make_input_line(x,y):
    a = unproject(camera,designSize,(x,y,-1))
    b = unproject(camera,designSize,(x,y,+1))
    return Line(origin=b,direction=normalize(a-b))

intersect(line,plane):                        # 0x129dee0
    denominator = dot(plane.normal,line.direction)
    t = (plane.d-dot(plane.normal,line.origin))/denominator
        if denominator != 0 else 0
    return line.origin+t*line.direction       # no t>=0 requirement

lane_class(x,E):                              # normal finite inputs
    if E>0 and x < -850: return 1
    if x < -425: return 2
    if x < 0: return 3
    if x < 425: return 4
    if x == 425: return 0
    return 6 if E>0 and x>850 else 5

lanes(model,line):                            # 0x130733c
    P = intersect(line,Y_equals_0)
    alternate = chart.byte_110 and (cameraZ<0 or cameraZ>900)
    valid = P.z>-1000 if alternate else (-500<P.z and P.z<500)
    if not valid: return (0,0)
    X = trunc(P.x)
    primary = lane_class(X,E)
    secondary = 0
    if G>1:
        a = (G-1)*425*0.5
        left = lane_class(X-a,E)
        right = lane_class(X+a,E)
        if left != primary: secondary=left
        else if right != primary: secondary=right
    return (primary,secondary)

spatial(model,P,target,flag,width):            # 0x927384
    delta = 0 if frameHeight<=720 else frameHeight-720 if frameHeight<=960 else 240
    base = 900+(delta/-240)*100
    scale = 2 if cameraZ<0 else max(1,cameraZ/base)
    B = globalWidth100 if not flag else trunc(width) if chart.byte_110 else 212
    half = scale*trunc(globalWidth180/2)
    bx = scale*B
    by = scale*globalHeight250
    Y = P.y
    if flag and not chart.byte_110:
        if Y<=100: Y=100
        else if Y>=G*globalVertical550: Y=G*globalVertical550
    Y = float(trunc(Y))
    return target.x-half-bx < P.x < target.x+half+bx
       and target.y-by-(60*scale if flag else 0) < Y < target.y+by
       and P.z > -1000

initial_input(model,touch,explicitLane):       # 0xeec024
    if model.byte_138 or model.byte_139: return
    update_timeline()
    line = make_input_line(touch.current.x,touch.current.y)
    primary,secondary = (explicitLane,0) if explicitLane else lanes(model,line)
    P = intersect(line, Z_equals_0)
    if chart.byte_110 and cameraZ<0: P=intersect(line,Y_equals_0)
    candidates.clear_and_release()
    for note in activeLogicRange:
        if not note.byte_54: continue
        if note is LogicTapNote:
            if note.position.i32_10 in {primary,secondary}: candidates.append(note)
        else if note is LogicHoldNote:
            if lane_matches(note) and note.start < now+100 and now < note.end:
                candidates.append(note)
        else if note is LogicArcNote:
            for child in note.arcTapChildren:
                target = child.localXY + (quantizedParentStartX,0)
                if spatial(model,P,target,flag=1,width=212): candidates.append(child)
    sort_by_signed_startTime_ascending(candidates) # equal-key stability not guaranteed
    for candidate in candidates:
        if candidate is LogicTapNote:
            if try_tap(model,candidate,touch.contactID): return
        else if candidate is LogicHoldNote:
            candidate.byte_a8=1
            return
    # Mode/explicit-lane-gated coverage and generic-sound fallback omitted.
    # Continuous hold/arc/flick processing remains a separate frame path.
```

## Unresolved Mysteries

Complete parent/chart camera-event producers and runtime viewport policies; nonfinite/singular-matrix behavior; position-object lane-zero provenance; exact product semantics of model width/outer-lane fields and chart special mode; all frame/lifecycle candidate-range maintenance; full platform listener/cancellation scheduling; touch timestamp use elsewhere and queue/audio latency compensation; complete multi-contact hold/flick/arc special-mode behavior on real hardware.

These are open questions, not a plan or authorization for a subsequent expedition.

## GitHub Status

Authorized outputs: this subject document and an appended Expedition 004 entry in `context.md`. Earlier documents are preserved, including historical wording. Commit references and exact read-back results are supplied in the return report after writing.
