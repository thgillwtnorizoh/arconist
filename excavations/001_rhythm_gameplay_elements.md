# Excavation 001 — Rhythm Gameplay Elements: Pseudocode

Date: 2026-10-21. Source: supplied `arccopy.zip`, primarily `lib/arm64-v8a/libcocos2dcpp.so`.

## Result

Recovered bounded pieces of native long-note and tap-render behavior plus Android frame dispatch. These fragments do not form a complete game engine. See [context.md](../context.md) for evidence, class relationships, source identity, and limitations.

## What I Found

The binary is stripped AArch64. Names below are researcher labels unless explicitly identified as recovered class names. Native addresses are ELF virtual addresses; the code addresses cited here also equal file offsets. `.eh_frame` ranges and relocation-backed RTTI/vtables establish the cited routines' locations and class associations.

| Fragment | Evidence |
|---|---|
| Shared long-note initializer | `0x17cb97c–0x17cba40`; called by hold initializer `0xd75e54` and arc initializer `0xc664f8` |
| Base checkpoint generator | `0xd92558–0xd92694`; `LogicHoldNote` vtable `0x1b2eda8`, slot 10 |
| Arc-specific adjustment | `0xba81e8–0xba8284`; calls base generator then adjusts records conditionally |
| Tap horizontal placement | `0xf20cd4–0xf20d40`; within `0xf20c28`, `RenderTapNote` vtable `0x1acde18`, slot 162 |
| Frame dispatch | `smali_classes3/org/cocos2dx/lib/Cocos2dxRenderer.smali`, `onDrawFrame` |

## Pseudocode

### 1. Shared long-note interval initialization

**Confirmed:** arithmetic, offsets, and direct hold/arc callers. **Interpretation:** `tempo_like` is BPM, interval units are milliseconds, and the float argument is density. The link between this argument and the chart header named `TimingPointDensityFactor` is not yet established.

```text
initialize_long_note_fragment(this, start, end, timing_object, supplied_float):
    this.i32_at_0x18 = start
    this.i32_at_0x1c = end

    magnitude = abs(float32(timing_object + 0x20))
    divisor = 1.0 if magnitude >= 255.0 else 2.0
    interval = float32(60000.0 / magnitude)
    interval = float32(interval / divisor)
    interval = float32(interval / supplied_float)
    this.f32_at_0x70 = interval

    # Other initialization/retention omitted; this is a bounded fragment.
    # No zero-tempo or zero-factor guard is visible in this routine.
```

For illustration of the arithmetic only, magnitude `120` and factor `1` yield `250`; magnitude `300` and factor `1` yield `200`. These examples are not measurements from an included chart.

### 2. Base long-note record generation

**Confirmed:** generator arithmetic, integer truncation, 12-byte record layout, and midpoint fallback. Meaning of the input flag and record fields beyond time remains provisional. Pseudocode describes ordinary finite positive intervals and ordered start/end values; exceptional float conversion behavior is not modeled.

```text
generate_base_records(this, flag):
    records = clear_and_release_existing_vector_at_0x78(this)
    start = this.i32_at_0x18
    end = this.i32_at_0x1c
    interval = this.f32_at_0x70
    duration = end - start

    limit = trunc_toward_zero(float32(duration) / interval)
    first_index = (~flag) & 1

    for i from first_index to limit - 1:
        time = trunc_toward_zero(
            float32(float32(start) + float32(interval * float32(i)))
        )
        if time < end:
            records.append({i32_time: time, i32_unknown: 1, byte_unknown: 0})

    this.u16_at_0x64 = 0

    if records.empty() and duration != 0:
        time = trunc_toward_zero(
            float32(float32(start) + float32(float32(duration) * 0.5))
        )
        records.append({i32_time: time, i32_unknown: 1, byte_unknown: 0})
```

The exclusive upper bound matters: this does not append the end timestamp as a general rule. If start equals end, the fallback does not add a record.

**Confirmed arc override fragment, `0xba81e8`:**

```text
generate_arc_records_fragment(this, flag):
    generate_base_records(this, flag & 1)

    if any pointer in this.vector_at_0x138 has i32_at_0xa4 == 0:
        duration = this.i32_at_0x1c - this.i32_at_0x18
        interval = this.f32_at_0x70
        a = trunc_toward_zero(float32(duration) / interval) - 1
        b = trunc_toward_zero(float32(duration - 2) / interval)
        if a == b and records.size >= 2:
            records.remove_last()
            records.last.i32_unknown = 2
```

The vector and discriminator meanings are unresolved. This is evidence of extra arc handling, not a complete account of arc linkage or scoring.

### 3. Tap renderer horizontal placement fragment

**Confirmed:** fields, branches, constants, and arithmetic. **Interpretation:** the discriminator selects continuous positioning versus a numbered lane. Internal coordinates are not proven screen pixels or touch regions.

```text
update_tap_horizontal_fragment(render_note):
    logic = virtual_call(render_note, slot=161)
    data = pointer_at(logic + 0x20)

    if i32_at(data + 0x0c) != 0:
        lane_like = i32_at(data + 0x10)
        if 1 <= lane_like <= 6:
            x = 425 * (lane_like - 1) - 1063
        else:
            x = 212
    else:
        normalized_like = f32_at(data + 0x14)
        x = trunc_toward_zero(
            float32(float32(normalized_like * 1700.0) - 850.0) - 212.0
        ) + 212

    render_note.i32_at_0x2a0 = x
    render_note.i32_at_0x2a4 = 4
    # Further visual transformations and opacity logic omitted.
```

The distinction between `trunc(x - 212) + 212` and `trunc(x)` is preserved deliberately. Six supported lane values do not establish a universal chart lane count.

### 4. Android frame-dispatch fragment

**Confirmed smali control flow:** this covers the dispatch portion of `onDrawFrame`; subsequent video-surface handling is omitted.

```text
onDrawFrame_dispatch_fragment():
    if sAnimationInterval <= 16666666.666666666:
        nativeRender()
        videoFrameCount += 1
    else:
        elapsed = System.nanoTime() - mLastTickInNanoSeconds
        if elapsed < sAnimationInterval:
            try:
                Thread.sleep((sAnimationInterval - elapsed) / 1000000)
                # Integer division, milliseconds.
            catch Exception:
                pass
        mLastTickInNanoSeconds = System.nanoTime()
        nativeRender()
```

This does not recover the native update cadence, guarantee 60 FPS, or identify the timing source used to judge a note.

### 5. Architecture interpretation and scoring boundary

```text
# Interpretation of the recovered class families; not recovered call order:
chart/event data: Note, SimpleNote, HoldNote, ArcNote, FlickNote, Timing, CameraControl
logic: LogicChart, LogicNote subclasses, LogicArcGroup
visuals: RenderNote subclasses, TrackLayer, TrackBase, ArcSegment, NoteBurstRenderer
results/state: ScoreState, score database fields, gameplay/results HUD labels

# UNKNOWN: score equation, hit-window comparisons, complete per-frame game loop,
# arc interpolation, touch-to-note selection, gauge and combo arithmetic.
# No invented implementation is supplied for these gaps.
```

## Unresolved Mysteries

Exact judgment windows and score weights; score-counter semantics; audio clock and offset application; full chart grammar; tempo/density propagation; arc linkage, curves and hit regions; renderer integration and runtime asset availability. These are unresolved questions, not a new work assignment.

## GitHub Status

This document and the appended Excavation 001 section in `context.md` are the only repository changes authorized for this excavation. Prior documentation is preserved.
