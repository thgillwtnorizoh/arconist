# Expedition 003 — Arc geometry, effects, synchronization, and finger tracking

## Result

Recovered local arc equations, coordinate conversion and mesh sampling, color-level contact ownership/release rules, connected-arc timing coordination, render feedback, and audio-start scheduling. This is a static native investigation with isolated ARM64 execution, not an Android runtime reproduction. Full spatial transforms, special-mode semantics, and audio drift correction remain unresolved.

Primary evidence: `arccopy.zip`, particularly `lib/arm64-v8a/libcocos2dcpp.so` and `lib/arm64-v8a/libfmodProvider.so`. The authoritative project instruction text was read before investigation; archive and repository access were verified. Main library SHA-256: `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`; ELF Build ID: `17d660edbf37ca78beefc32e07672c97419ddce6`.

Addresses below are library-relative virtual addresses. Main-library executable/rodata addresses also equal file offsets; relocated data needs ELF segment/relocation interpretation. FMOD-provider addresses belong to a separate ELF and must not be applied to the main library. Names for unknown fields are explanatory, not recovered source names.

## What I Found

### Evidence conflict with the prior record — preserve pending confirmation

Expedition 002 recorded `b=0, s=1`. New direct inspection and isolated execution of classifier `0xd51010` establish **`b=1, s=0`** in this binary. At `0xd51058`, equality with `b` branches to `0xd511b8`, which writes `w0=1`. Equality with `s` at `0xd51098` jumps directly to the return at `0xd511fc`, preserving comparison result zero. All other recorded curve IDs agree with the new checks.

The old context and Expedition 002 document are preserved verbatim. This section records conflicting new evidence; editing the earlier entries requires explicit user confirmation under the project's preservation rule. Equations here use the newly verified IDs.

### Geometry and curve equations

`LogicArcNote` stores start/end time at `+0x18/+0x1c`, endpoint-position pointers at `+0x20/+0x28` (normalized x at each object's `+0x14`), normalized y endpoints at `+0xa8/+0xac`, timing object at `+0x48`, and curve ID at `+0x15c`.

Sample generator `0x1925084` converts to internal coordinates:

```text
X0 = trunc(float32(x0 * 850 - 425))
X1 = trunc(float32(x1 * 850 - 425))
H = global_i32[0x1bf6d80]
Y0 = trunc(float32(y0 * (H - 100) + 100))
Y1 = trunc(float32(y1 * (H - 100) + 100))
Tend = max(own endTime, startTime of every successor in vector +0x138)
Z = trunc(float32(-(Tend - startTime) / timing.float_28))
```

These are internal units, not a claim about fixed screen pixels. `timing.float_28` is a traced scaling field; a complete timing/BPM derivation is outside the recovered chain. Arithmetic uses the binary's mixed float/double operations and integer truncation. No validity guarantee is inferred for zero durations or denominators.

Define `u` as the curve parameter, `S(u)=3u²-2u³`, `I(u)=sin(πu/2)`, and `O(u)=1-cos(πu/2)`. For sine curves, evaluator `0x180a190` returns **local x displacement**, absolute internal y, and local z:

```text
p(u) = ((X1-X0)*Ex(u), Y0+(Y1-Y0)*Ey(u), Z*u)
```

| AFF label | Verified ID | Ex(u) | Ey(u) | Evidence |
|---|---:|---|---|---|
| `s` | 0 | u | u | Linear branch `0x19258fc–0x1925a8c` |
| `b` | 1 | Cubic construction below; approximately S(u) | S(u) | `0x1925264–0x19253b8`, helper `0x14f3078` |
| `si` | 2 | I(u) | u | `0x180a190` |
| `so` | 3 | O(u) | u | Same |
| `sisi` | 4 | I(u) | I(u) | Same |
| `sosi` | 5 | O(u) | I(u) | Same |
| `siso` | 6 | I(u) | O(u) | Same |
| `soso` | 7 | O(u) | O(u) | Same |

The implementation computes O as `1-sin((u+1)*π/2)`, algebraically equal to the expression above. Unknown labels fall back to ID 0.

For **`b`**, preserve the actual construction rather than claiming a bit-exact smoothstep shortcut:

```text
dx = X1-X0
D = trunc(sqrt(dx*dx + Z*Z))
angleDegrees = -atan2(dx, -Z) * 180/π - 90
P0 = P1 = (0, Y0)
P2 = P3 = (-D, Y1)
C(u) = (1-u)^3*P0 + 3*(1-u)^2*u*P1
       + 3*(1-u)*u^2*P2 + u^3*P3
Q = rotate_about_Y((C.x, C.y, 0), angleDegrees)
return (Q.x, Q.y, Z*u)
```

`0x14f3078` calls rotation-matrix builder `0x1987f94` and point transform `0xcaf3cc`, then explicitly replaces z with `Z*u`. Because D is truncated, the rotated x result should not be represented as exactly `dx*S(u)` in a faithful reimplementation. This derivation covers the normal construction; degenerate cases have not been exercised.

### Sampling, render positioning, and arc-taps

Generator `0x1925084` fills vectors of 12-byte Vec3 records at `+0xe8` and `+0x100`. It uses `rate=14` if the arc's own duration is less than 1000 ms, otherwise 7; `seconds=(Tend-startTime)/1000`. Parameter steps are `1/(seconds*rate)` and `1/(seconds*rate*extra)` respectively. The optional AFF extra value reaches runtime `+0x118`; initializer `0xc664f8` clamps it to at least 1. This establishes its effect on the second geometry-sampling density; it is distinct from long-note judgment density.

Loops sample while u<1 and explicitly handle endpoints. A mode-dependent ID-0 branch emits only the two endpoints. Embedded arc-tap positions at child `+0x80/+0x88` are populated in this generator; the linear branch uses `(tapTime-startTime)/(Tend-startTime)` to interpolate. Complete special-mode and attachment behavior is not claimed.

Render initializer `0x13b5ff8` iterates adjacent samples from logic vector `+0x100`, constructs segment children through `0x14f3f40`, and supplies first/last-segment flags. It also creates two render containers (`+0x2b8/+0x2c0`) through `0x17ec490`. Segment shaders and triangle topology were not fully reconstructed.

Render update `0x11b7d78` positions the parent at `(trunc(850*x0-425), 0, logic.i32_30)` and reads current x displacement/y at logic float `+0xd4/+0xd8`. Its cached current x at render `+0x2a0` includes the translated start x. These reads support separation between local geometry, scrolling parent placement, and contact coordinates; they do not by themselves establish every camera transform or the producer of the current-position cache.

### Contact identity and spatial eligibility

Android bridge evidence is `smali/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali`: pointer ID, coordinates, and size/pressure-derived data enter the native touch pipeline; touch timestamps use elapsed-realtime nanoseconds divided into milliseconds.

Native begin callback `0x194ff80` assigns a separate incrementing contact ID: `0x195007c–0x1950098` load global counter `0x1bf25f4`, store its old value at touch `+0x34`, increment the counter, and store a timing-related value at touch `+0x3c`. Ownership code uses **touch `+0x34`**, so it must not be described simply as the raw Android pointer ID. This is contact tracking; physical-finger identity, hand identity, and trajectories across lift/re-touch are not established.

Continuous input routine `0x14858d4` checks arc spatial eligibility through `0xc98490`, then invokes arc acceptance `0x15dfe2c`. `0xc98490`:

- Rejects nonzero arc mode `+0xa4` in this ordinary input path.
- Consults start time and byte `+0xd0`; one caller-selected branch permits start lookahead of 120 ms, the other compares directly with the start.
- Uses current x = quantized starting x + float `+0xd4`, y = float `+0xd8` for nonzero-duration arcs. A zero-duration branch uses start endpoints and a separate global vertical scale `0x1bf6c9c`.
- Calls spatial helper `0x927384` with parameter **212.0** (`0x43540000`). This is a helper argument, not proof of a universal 212-pixel hitbox. Projection/configuration affect the actual bounds.

### Ownership belongs to LogicColor; connected timing belongs to LogicArcGroup

These are different objects:

| Object | Evidence | Role recovered here |
|---|---|---|
| `LogicColor`, arc `+0xb0` | Factory `0xd93594` writes vtable address point `0x1aa1b98`; RTTI name at `0x47dd29` | Contact ownership and conflict/release state; shared among matching mapped color IDs |
| `LogicArcGroup`, arc `+0xe0` | Allocation in `0x125e674–0x125e6e0` writes vtable `0x1b85570`; RTTI name at `0x479db7`; setter `0x165286c` | Connected-arc activation and timing state |

Chart helper `0xd51220` looks up/reuses `LogicColor` objects from chart vector `+0x68` by integer color/category at `+0x18`, after mode/mirror-dependent remapping. It allocates only if no matching mapped color exists. Therefore ownership is not independently allocated per arc segment. Do not infer all special colors' product meanings from their numeric IDs.

Claim routine `0x15a90c4` accepts `(LogicColor*, contactID, now, intervalInteger)`. It stores interval at `+0x0c`. Recovered fields: owner ID `+0x28`, release time `+0x2c` (both -1 when unset), acceptance byte `+0x22`, previously-claimed byte `+0x24`, bypass byte `+0x10`, conflict byte `+0x30`, and unresolved feedback fields `+0x34/+0x38`. A global vector of claimed contact IDs is based at `0x1bfa3d8` (begin/end/capacity).

The ordinary path accepts the existing owner, rejects a different owner, and claims an unowned color only if that contact ID is absent from the global vector. A set bypass byte also permits acceptance without changing owner; category 3 returns true after the release-time gate, without ordinary ownership assignment. Arc byte `+0x170` bypasses the call to this color arbitration in `0x15dfe2c`. The conditions that enable all bypasses are not fully established.

For a recorded release, reacquisition is blocked while `now-releaseTime < trunc(min(4*intervalInteger,1000))`; equality exits that gate. This is one ownership gate, not a universal note-hit window or a proven fixed total delay visible to players. Other lifecycle resets exist. In particular, arc update `0x95d61c` clears color `+0x24/+0x30` and resets `+0x2c` to -1 after its end when its successor/mode conditions permit.

Release `0x13db7a0` clears a matching owner and removes its ID from the global claimed vector. With a found entry, `+0x24` set, and bypass byte clear, it records release time. The touch-end route `0xf9a50c` calls it for color objects. A non-owner release does nothing. Cancellation and every per-frame feedback reset are not fully reconstructed.

### Synchronization and effects

**Gameplay coordination:** arc acceptance `0x15dfe2c` first enforces ownership unless bypassed. It scans pending checkpoint records in the current arc and linked predecessors/successors (`+0x150/+0x138`), consults connected-group timestamps at group vector `+0x18`, and conditionally extends group float `+0x14` to `checkpointTime + min(2*interval,500)`. Group bytes `+0x10/+0x12` are set on acceptance. This is explicit connected-note state sharing, not evidence for musical beat snapping or networking.

Connection builder `0x125e474` compares end/start times in a small time neighborhood, x proximity, matching y endpoints, and mode compatibility; it creates/reuses `LogicArcGroup` and links predecessor/successor arcs. The exact complete eligibility predicate, branching behavior, and all tolerance constants are not claimed reconstructed.

**Visual feedback:** accepted arc processing sets logic bytes `+0x64/+0x65`, calls render virtual slot `+0x530` -> `0x155241c`, which sets render byte `+0x300`. Render frame function `0x11b7d78` reads that latch, current geometry, and group state. It also reads color feedback field `+0x34`; the conflict path constructs RGB **(230,50,50)** at `0x11b83a0–0x11b83b4` and applies it through `0x15a0eac` to children. The exact visual blend/transition semantics of that callee remain unknown. A separate branch advances a modulo-5 counter and scales a visual value every fifth update (`0x11b847c–0x11b855c`); a fixed real-time animation frequency cannot be inferred from frame counts alone.

Archive assets include `assets/particle/particle_arc.plist`, `particle_arc_mirai_conflict.plist`, and `particle_arc_mirai_light.plist`. Their presence is confirmed; this investigation does not prove which of the recovered render branches selects each asset. Nor is the AFF arc effect identifier proven to select all these visual effects.

**Contact sound:** on acceptance, if arc sound handle `+0x68` is -1, `0x15e0174–0x15e0198` calls audio dispatcher `0x107af5c` with sound ID 0 and the arc's start time, storing its return value. This traces an accepted-arc sound request. It does not prove that the AFF effect token directly names that sound or that playback always succeeds.

**Game clock/audio start:** main-library `0x1271200` uses steady-clock milliseconds. Timeline updater `0x16c90bc` computes clock fields/compensation; in the unstarted and unpaused branch, effective judge time must be strictly greater than `-timeline.i32_30` before audio start. It sets byte `+0x2e`, calls audio-manager `0x1735d7c`, and updates compensation `+0x28`. That manager dispatches provider virtual `+0x28` with loop=false, BGM index=0, delay=0. The final provenance/sign relationship among AFF AudioOffset, device/user offset, and timeline `+0x30` is still unresolved.

**FMOD clock:** in `lib/arm64-v8a/libfmodProvider.so`, exported `AudioProviderFMODAndroid::playBGM(bool,int,int)` at `0x270a8` reads software sample rate and the parent DSP clock, then computes:

```text
startDSP = uint64(float32(float32(delayMilliseconds)/1000 * sampleRate
                          + float32(parentDSPClock)))
channel.setDelay(startDSP, 0, true)
# then unpause the selected channel or main group
```

The operation order and float32 rounding matter; calling this a mathematically exact sample conversion would overstate the evidence. Exported `loadAndScheduleSfxOnMainBGM(...)` at `0x26e04` likewise converts timestamp offsets with sample rate and parent clock and calls `setDelay`. `getBGMPosition(int)` at `0x32da0` calls `Channel::getPosition(...,1)`; `setBGMPosition(int,int)` at `0x35b38` calls `setPosition(...,1)` and adjusts/stops scheduled channels according to shifted DSP times. Unit value 1 is literal binary evidence; the surrounding /1000 conversions support the millisecond interpretation. The presence of a position getter does not establish continuous drift correction in the game loop.

### Validation

Isolated Unicorn execution of original ARM64 instructions passed:

- Nine classifier inputs: all eight labels plus unknown fallback. Native string comparisons were replaced with equivalent host comparisons.
- 42 samples from `0x180a190`: six sine curves, seven u values including 0 and 1; outputs matched equations within 0.0002 internal units. The external sin call was hooked to host sin; native branch selection/arithmetic/Vec3 construction executed.
- Seven ownership assertions: initial claim, same-owner acceptance, other-owner rejection, release bookkeeping, rejection one millisecond below a 400 ms gate, acceptance exactly at the boundary, category-3 bypass without owner reassignment. Synthetic memory and preallocated vector capacity avoid unrelated allocation paths.

These checks do not execute the full renderer, cubic rotation path, actual multitouch hardware, all lifecycle resets, or an audio device. Archive samples contain no AFF files, so no real-chart end-to-end validation is claimed.

## Pseudocode

These routines reconstruct the recovered behavior only. `field_XX` labels preserve uncertainty.

```text
curve_sine(id, X0, X1, Y0, Y1, Z, u):  # 0x180a190; called for IDs 2..7
    ex = sin(u*pi/2) if id in {2,4,6} else 1-sin((u+1)*pi/2)
    ey = sin(u*pi/2) if id in {4,5} else
         1-sin((u+1)*pi/2) if id in {6,7} else u
    return Vec3((X1-X0)*ex, Y0+(Y1-Y0)*ey, Z*u)

# Linear and cubic paths are given explicitly above.
# Frame/current-position-cache production and complete projection are unresolved.

record_conflict(color, now, global_duplicate=False):
    if color.byte_22 != 0: return false
    color.byte_30 = 1
    # Duplicate-global-ID branch stores this unconditionally;
    # other conflict branches test field_34's sign.
    if global_duplicate or color.i32_34 < 0:
        color.i32_38 = now
    return false

claim_color(color, contactID, now, intervalInteger):  # 0x15a90c4
    color.i32_0c = intervalInteger
    if color.i32_2c != -1:
        if now-color.i32_2c < trunc(min(4*intervalInteger,1000)):
            return record_conflict(color,now)
        color.i32_2c = -1
    if color.i32_18 == 3: return true
    if color.i32_28 == contactID or color.byte_10 != 0:
        color.byte_22 = 1
        color.i32_34 = color.i32_38 = -1
        return true
    if color.i32_28 != -1: return record_conflict(color,now)
    if contactID in GLOBAL_CLAIMED:
        return record_conflict(color,now,global_duplicate=true)
    color.byte_22 = color.byte_24 = 1
    color.i32_28 = contactID
    GLOBAL_CLAIMED.push(contactID)
    color.i32_34 = color.i32_38 = -1
    return true

release_color(color, contactID, now):  # 0x13db7a0
    if color.i32_28 != contactID: return
    color.i32_28 = -1
    if contactID found in GLOBAL_CLAIMED:
        erase matching entry
        if color.byte_24 and not color.byte_10: color.i32_2c = now
        if color.byte_10: color.byte_30 = 0

accept_arc(arc, touch, now):  # 0x15dfe2c, after spatial eligibility
    if not arc.byte_170:
        if not claim_color(arc.color_b0,touch.i32_34,now,trunc(arc.interval)):
            return
    # Native linked-checkpoint/group scan conditionally extends group deadline.
    # Full scan predicate is not replaced with a guessed simplified algorithm.
    arc.byte_64 = arc.byte_65 = 1
    if arc.soundHandle_68 == -1:
        arc.soundHandle_68 = audio_request(soundID=0,time=arc.startTime,...)
    arc.render.virtual_530()  # sets render.byte_300
    if arc.group_e0:
        arc.group_e0.byte_10 = arc.group_e0.byte_12 = 1
```

## Unresolved Mysteries

- Complete current-position-cache producer, camera/group transforms, segment mesh/shader topology, and exact cubic degeneracy behavior.
- Full connected-arc predicate and all special-mode/bypass activation conditions; cancellation handling and feedback-field lifecycle.
- Complete visual effect-token dispatch, particle selection, latch clearing, and color blend semantics.
- Final chart/user/device audio-offset composition, pause/seek lifecycle, and whether/how playback drift is corrected.
- End-to-end behavior with real AFF charts, frame scheduling, actual multitouch, and audible output.

These are unresolved questions, not recorded future plans or authorization for another expedition.

## GitHub Status

This excavation adds this subject document and appends an Expedition 003 entry to `context.md`. Earlier text is preserved; the b/s discrepancy is recorded separately pending confirmation. Exact resulting commits are supplied in the Expedition Return Report after write/read-back verification.
