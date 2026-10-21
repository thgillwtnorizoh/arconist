# Expedition 002 — AFF Parser and Note Judgment

Date: 2026-10-21. Primary evidence: supplied `arccopy.zip`, particularly `lib/arm64-v8a/libcocos2dcpp.so`. This document describes this binary, not every Arcaea version or community AFF tool.

## Result

Recovered the chart text loading pipeline, the central event dispatcher's complete set of branches, parameter order/type checks for those branches, timing-group attributes, runtime arc-curve and scene-control name classifiers, and substantial note judgment behavior. Recovered tap timing bands and ordinary score arithmetic were checked by executing isolated ARM64 instructions in Unicorn with surrounding engine calls stubbed.

This is not a complete replacement parser or a complete running-game reconstruction. Camera/effect semantics, precise screen-to-world geometry, arc-group arbitration, malformed-input behavior, and special-mode exceptions remain partially unresolved. No chart files are supplied in the ZIP, so none of these claims is based on playing a bundled chart.

## What I Found

### Evidence identity and address convention

Binary SHA-256: `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`; GNU Build ID: `17d660edbf37ca78beefc32e07672c97419ddce6`. Addresses are ELF virtual addresses before relocation. The cited code addresses equal file offsets; addresses in `.data.rel.ro` do not. Function names invented for clarity are descriptive labels, not recovered symbols. Recovered class names come from C++ RTTI.

**Confirmed** means file content, instructions, relocation-backed type identity, or an explicitly described isolated execution. **Interpretation** means a researcher-assigned meaning. **Unknown** marks an unfinished reconstruction.

### A. Chart text pipeline

1. Native caller `0x16e67a4` obtains text through a file/resource-provider virtual call and passes it to `0x1870de0`. The separate asset-enumeration routine `0x9d9ac4` references `0.aff` through `4.aff`; its complete filename selection policy was not reconstructed.
2. `0x1870de0` finds the header/body separator, supporting both `\n-\n` and `\r\n-\r\n`. It splits out the header and body, lexes the body through `0xdf4a58`, parses its tokens through `0xb01d6c`, and parses header entries through `0x10dbff8`.
3. Header parser `0x10dbff8` splits lines on newline, splits entries on `:`, removes carriage returns from values, and retains nonempty key/value pairs in a map. This is broader syntactic storage than semantic support: arbitrary stored keys are not automatically game features.
4. Body lexer `0x814384` skips whitespace, tracks newlines, emits punctuation tokens, distinguishes integer/float/identifier tokens, and recognizes reserved words. `0xdf4a58` collects the token stream. This is token parsing rather than a line-per-note reader.
5. `0xb01d6c` repeatedly calls `0x139b96c`. That wrapper distinguishes a timing group from an ordinary event and requires a trailing `;`. The central event dispatcher is `0x923240`.
6. `LogicChart` initializer `0x173b358` consumes metadata and invokes runtime construction at `0x1862a14`, followed by sorting, linking/grouping, checkpoint generation, and timing-position preprocessing calls. These stages are visible; every called routine has not been fully reconstructed.

Header semantics confirmed in `0x173b358`:

| Header | Observed conversion/storage | Scope of confirmation |
|---|---|---|
| `AudioOffset` | Value passed to `atoi`; stored at `LogicChart+0xc4` | Missing/empty value converts to zero; final audible alignment sign remains untraced |
| `TimingPointDensityFactor` | Default `1.0`; nonempty value passed to `atof`, narrowed to float, stored at `+0xc8` | Propagation to long-note interval initialization confirmed |

The two headers are retrieved at `0x173b3f0` and `0x173b560`; conversions occur at `0x173bcfc` and `0x173bd34`. No exhaustive claim about additional header consumers elsewhere in the binary is made.

### B. Recovered event grammar

`I` means an integer token, `F` a float token, `ID` an identifier, and `P` either integer or float. Parameter names are interpretations of stored values; order and type checks are confirmed. These are representative valid forms, not a specification of every malformed string the implementation might accidentally tolerate.

| Construct | Recovered shape before trailing semicolon | Parser VA |
|---|---|---|
| Tap | `(I time, P position)` | `0x11bfd24` |
| Hold | `hold(I start,I end,P position)` | `0xf5369c` |
| Timing | `timing(I time,F tempo,F beats)` | `0x10a4ef4` |
| Flick | `flick(I time,F x,F y,F dx,F dy)` | `0xa3ab64` |
| Camera | `camera(I time,F a,F b,F c,F d,F e,F f,ID easing,I duration)` | `0x138f560` |
| Arc | `arc(I start,I end,F x0,F x1,ID curve,F y0,F y1,I color,ID effect,flag[,F extra])` with optional `[arctap(I time),...]` | `0xc2cb1c` |
| Scene control | `scenecontrol(I time,ID kind)` or `scenecontrol(I time,ID kind,F value,I integer)` | `0x7f2628` |
| Timing group | `timinggroup([ID attributes]){ event; ... }` | `0x8c847c`, via wrapper `0x139b96c` |

Important implementation distinctions:

- The integer helper `0x18905f4` dynamically requires `Tokens::TINT`; float helper `0x19070d8` requires `Tokens::TFLOAT`; identifier helper `0x14be280` requires `Tokens::TIDENT`. There is no implicit integer-to-float coercion in these helpers. For example, authoring a float position as `0.0` versus integer `0` can select a different position representation.
- Position helper `0xa9c1f0` explicitly accepts either integer or float and creates different position objects. Integer positions feed lane-like behavior; floats feed continuous horizontal placement. Do not convert every position to an integer lane.
- Arc flag consumption tests TRUE, then DESIGNANT. TRUE stores mode `1`, DESIGNANT stores `2`, otherwise the consumed token maps to `0`; the routine does not explicitly require FALSE in that final branch. `designant` arcs are discarded by `0x139b96c` when a supplied inclusion flag is zero. Group parsing has a corresponding filter.
- Arc `extra` defaults to `1.0`, is stored at chart `ArcNote+0x88`, and is passed as float argument 3 through the arc factory. Its full gameplay meaning is unresolved; it is not identified here as checkpoint density.
- Arc data initializer `0x924b50` stores start/end at `+0x18/+0x1c`, horizontal endpoints at `+0x20/+0x24`, curve string at `+0x28`, vertical endpoints at `+0x40/+0x44`, color at `+0x48`, effect string at `+0x50`, flag mode at `+0x68`, arc-tap times in the vector at `+0x70`, and the extra float at `+0x88`.
- The group body calls ordinary-event dispatcher `0x923240`, which has no timing-group branch. Recursive group nesting is not implemented in this observed path.
- The lexer also recognizes `rgb` and `at` tokens. Neither is a top-level event branch in `0x923240`; token existence alone does not establish usable event syntax.
- A leading minus has its own lexer branch at `0x814564–0x814628` and produces a float token. Signed-integer, exponent, comment, and malformed-number compatibility is not fully characterized. Do not silently substitute a generic language's number lexer.

### C. Timing-group attributes

`0x8c847c` accepts an optional identifier inside parentheses, splits it on `_`, and inspects the resulting attribute strings. Each ordinary parsed object receives applicable fields; timing objects are handled separately in a group timing collection.

| Attribute | Confirmed action |
|---|---|
| `noinput` | Clears chart object byte `+0x0c`; construction copies it to logic byte `+0x54`; normal input and judgment loops skip objects with that byte zero |
| `fadingholds` | Sets chart object byte `+0x0d`; hold construction copies it to logic `+0xa9`; complete visual effect not traced |
| `anglex...` | Parses substring after six-character prefix with `stoi`, stores at chart object `+0x10` |
| `angley...` | Corresponding integer stored at `+0x14` |
| `tracecol...` | For arc objects, parses suffix with `%02x%02x%02x`, allocates a three-integer color record at `ArcNote+0x90` |

Unknown attribute strings do not have a matching action in these inspected tests. The exact coordinate transformation and angle units downstream remain unresolved. No claim is made that `noinput` means “not rendered.”

### D. Runtime identifiers and effects

Arc-curve classifier `0xd51010`, called on the chart arc's curve string during `0x1862a14`:

| Label | Internal result |
|---|---|
| `b` | 1 |
| `s` | 0 |
| `si` | 2 |
| `so` | 3 |
| `sisi` | 4 |
| `sosi` | 5 |
| `siso` | 6 |
| `soso` | 7 |

**Authorized correction (2026-10-22):** The original Expedition 002 version mistakenly recorded `b=0, s=1`. Expedition 003 re-examined and executed the original native classifier `0xd51010`: the `b` match at `0xd51058` branches to `0xd511b8` and returns `1`; the `s` match at `0xd51098` returns `0` through `0xd511fc`. The corrected IDs above are `b=1, s=0`. The earlier mapping remains traceable in Git commit `e2796f27f970e30d94b4ad121ad99024cdebbd86`; the user explicitly authorized this correction. Other curve IDs remain unchanged.

Unrecognized curve names fall back to `0` in this classifier. The precise curve equations are not reconstructed here; assigning Bezier/sine formulas solely from these labels would be an inference.

Scene-control classifier `0x1090060` recognizes `trackdisplay` (0), `redline` (1), `arcahvdistort` (2), `arcahvdebris` (3), `hidegroup` (4), `enwidencamera` (5), and `enwidenlanes` (6); other names return 7. Parser `0x7f2628` converts no-argument `trackhide` and `trackshow` into `trackdisplay` records with integer values 0 and 255 respectively. An arbitrary syntactically accepted scene-control ID does not guarantee a runtime effect.

Camera events reach handler `0x192b5c8`. Translation/rotation-like triples are separately dispatched; `reset` triggers a reset path. Action builders `0x10a2b94` and `0x13a7938` branch on easing strings `qi` and `qo`; the inspected first builder divides duration by `1000.0` before creating the action. Exact axis conventions and every easing behavior remain partially unresolved.

Arc effect strings are retained and inspected during construction, with visible branches involving `none`, `arcahv`, and `desive`. An exhaustive effect/audio implementation was not recovered.

### E. Time and input

- `smali_classes3/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali`, `getTouchTimestampNow`, converts `SystemClock.elapsedRealtimeNanos()` to milliseconds. `onTouchEvent` collects pointer ID, X, Y, and `getSize()*getPressure()` and passes a timestamp through the renderer/JNI path. This is the handler's current timestamp, not a read of `MotionEvent.getEventTime()` in the inspected method.
- Game timing helper `0x1271200` calls `std::chrono::steady_clock::now()` then divides the nanosecond count by 1,000,000. `GameTimeline` logic `0x16c90bc` updates integer time and compensation fields. Thus milliseconds are supported by executable evidence, not just the conventional AFF format.
- Judgment repeatedly uses this effective-time expression, where names are provisional:

```text
if timeline.byte_2d != 0:
    now = timeline.i32_20 - timeline.i32_28
else:
    now = timeline.i32_34 - timeline.i32_28
    if timeline.i32_34 <= 0:
        now -= 3000
```

The complete lifecycle of these clock modes, pause/resume synchronization, and the sign of chart `AudioOffset` in audible alignment are not fully traced. Java and C++ monotonic clocks must not be assumed to have identical epochs.

### F. Tap and arc-tap eligibility and timing

Normal touch path `0xeec024` rejects disabled input states, projects touch coordinates, derives lane candidates, and builds a candidate list. It skips logic objects whose input-enabled byte `+0x54` is zero.

- A `LogicTapNote` candidate must match one of the computed lane candidates.
- Arc-taps are reached through a `LogicArcNote`'s arc-tap children. Their spatial eligibility calls `0x927384` with the child position and a width-like value `212.0`. The resulting candidate is still a `LogicTapNote` subclass and reaches the same timing classifier.
- The candidate list is passed through `0xf6b514` before judgment. Exact tie-breaking/comparator semantics are unresolved; a full “always nearest note” rule is not asserted.
- Timing classifier `0x160ce28` rejects notes whose virtual slot 8 or slot 6 is already true. For ordinary taps these read bytes `+0x0c` and `+0x0d`, preventing duplicate consumption. Separately, arc-tap miss-acceptance slot 7 consults its parent arc state.

After spatial eligibility, the confirmed timing bands are:

| Absolute integer error | Action | Display interpretation |
|---|---|---|
| 0–25 ms | Accept, judgment ID 0 | Shining PURE; increments both shining and total-PURE counters |
| 26–50 ms | Accept, judgment ID 1 | Other PURE |
| 51–100 ms | Accept, judgment ID 2 | FAR |
| 101–120 ms | Call miss-recording path; return consumed/true | LOST, not a successful hit |
| Above 120 ms | Return false without recording through this routine | Candidate not consumed here |

For non-tightest tiers, early/late discriminator is `1` when `now < noteTime` and `2` otherwise. The tightest tier passes discriminator 0 into score-state recording, while the UI delegate also receives the timing-side discriminator.

Miss/expiry pass `0xf8056c` independently records ordinary tap misses once `now > endTime + 100`; arc-tap expiry is checked against `endTime + 100` within parent processing. Consequently the tap classifier's mathematical `101–120` late band is not a promise that a note survives that long in every frame/input ordering.

Spatial checker `0x927384` is resolution/camera/configuration dependent. It tests strict horizontal and vertical bounds and a depth condition against `-4000`. Its width argument is not a fixed screen-pixel radius. Complete geometry and lane boundary behavior are not claimed here.

### G. Holds and arcs

Continuous-input routine `0x14858d4` visits current touch records before the expiry/checkpoint pass. For holds it checks lane membership, activation before the end time, a start lookahead of 120 ms, and a latch set by the initial-touch path; accepted input invokes hold virtual slot 12, `0x14557b4`, setting bytes `+0x64/+0x65` to one. For arcs it calls the spatial/eligibility routine `0xc98490` and then the arc slot-12 override `0x15dfe2c`.

`0xc98490` rejects nonzero arc mode `+0xa4`, uses current or stored arc positions, and calls `0x927384`; an initial-touch call has a 120 ms lookahead. Traces/non-playable arc modes are therefore not interchangeable with normal scoring arcs. Precise arc-group/color arbitration in `0x15dfe2c` is only partly reconstructed.

Checkpoint density linkage is now established:

```text
header TimingPointDensityFactor
  -> LogicChart.float_0xc8
  -> hold factory 0x1446490 / arc factory 0x178f7fc
  -> hold/arc virtual initializer
  -> shared initializer 0x17cb97c
  -> interval stored at longNote+0x70
```

Representative loads are `0x18649b0` for holds and `0x1865154` for arcs. The shared interval arithmetic and record generation documented in Expedition 001 remain unchanged.

The additional recovered behavior gives those records operational meaning:

- `record+0` is checkpoint time; `record+4` is the number of judgment units represented; `record+8` is a resolved/consumed flag.
- In `0xf8056c`, an actively held long note resolves pending records up to `truncate(now + interval/2)`, sums their units, and calls the accepted-result recorder with judgment ID 0 once per unit. Repeated checkpoints therefore use the tightest success tier directly.
- When not active, virtual slot 11 is consulted. If enabled, `0xc6e938` resolves overdue pending records using a cutoff based on `now - min(2*interval,500)`. A special first-record flag `+0x6c` modifies one boundary case; the full condition is preserved in pseudocode below. Misses are then recorded once per judgment unit.
- Long notes do not require every frame to stay perfect without tolerance; checkpoint timing, state flags, and arc-specific overrides matter. This report does not infer a universal grace period from one constant.

### H. Flicks

`flick` syntax and a live processing branch are confirmed. In `0x14858d4`, a flick candidate must be unconsumed, pass its spatial region test, and satisfy `now > startTime - 200`. Its missing-input expiry path uses `endTime + 200`.

Flick helper `0x16e0548` binds an initially unassigned finger identifier, remembers its origin, and rejects other finger IDs. For the same finger it computes displacement versus the stored chart direction. It requires angular difference strictly below **45 degrees** and displacement strictly above **106 internal coordinate units**. It does not divide displacement by elapsed time in this helper; calling this a speed threshold would be incorrect. A successful flick reaches accepted judgment ID 0. Mode availability and actual chart usage remain unverified.

### I. Result state and ordinary score arithmetic

Accepted-result recorder `0x1730290` first asks the note's virtual slot 4 to accept the event. On acceptance, ID 0 increments score state `+0x20` and `+0x24`, ID 1 increments `+0x24`, and ID 2 increments `+0x28`. These are interpreted as shining PURE, total PURE, and FAR respectively, consistent with the score formula and result vocabulary. Accepted records increment the current combo at `+0x1c`.

Miss recorder `0x868e54` consults note virtual slot 7, increments `+0x2c`, and resets combo at `+0x1c` to zero when the miss is accepted.

Native score helper `0xe43b80`, as called at `0x1730504`, supports this ordinary nonnegative-count expression for a positive total:

```text
score = floor(10_000_000 * (PURE + FAR/2) / totalJudgmentUnits) + shiningPURE
```

Its implementation uses integer arithmetic, an all-PURE shortcut, and a cap selected by a flag; this document preserves the literal implementation below. The boolean special-mode flag's product meaning is not identified. Do not extend the ordinary expression to malformed totals, overflow, or every game mode.

### Validation and limits

Unicorn executed the original tap classifier with synthetic objects and hooked eligibility/result callbacks: **34 boundary cases** across both clock branches, plus an already-blocked-note case. Inputs included both sides of 25, 50, 100, and 120. All matched the documented classification and return values.

The original leaf score routine was executed for **500 deterministic randomized ordinary count combinations**, all matching the ordinary formula. This validates isolated machine-code behavior under those assumptions. It does not validate real touchscreen projection, scheduling, audio latency, game-mode configuration, or the complete parser on a device.

## Pseudocode

### Chart reader and dispatch

```text
read_chart_text(text, include_designant):
    headerText, bodyText = split_at_supported_dash_line(text)
    tokens = lex_body(bodyText)                # 0xdf4a58 -> 0x814384
    chartData = new parsed chart
    while tokens remain:
        if peek() is TIMINGGROUP:
            parse_timing_group(tokens, chartData, include_designant)
        else:
            event = parse_event(tokens)
            if event is designant arc and not include_designant:
                discard(event)
            else:
                chartData.add(event)
        expect(SEMI)
    chartData.headers = parse_colon_header_map(headerText)
    return chartData

parse_event(tokens):                         # 0x923240
    switch token kind:
        HOLD:         parse_hold()
        FLICK:        parse_flick()
        CAMERA:       parse_camera()
        LPAREN:       parse_tap()
        SCENECONTROL: parse_scene_control()
        TIMING:       parse_timing()
        ARC:          parse_arc()
        otherwise:    throw ArcParser_error("Unparsable note starting with ...")

build_runtime_chart(parsed):
    chart.audioOffset = atoi(headers["AudioOffset"])
    chart.density = 1.0
    if headers["TimingPointDensityFactor"] is nonempty:
        chart.density = float32(atof(that value))
    construct_logic_objects_and_group_timing(parsed, chart)
    sort_link_group_and_generate_checkpoints(chart)
    preprocess_timing_positions(chart)
    # Names summarize observed stages; full internals not reconstructed here.
```

### Arc parsing fragment

```text
parse_arc():
    expect(ARC); expect(LPAREN)
    start = require_int(); expect(COMMA)
    end = require_int(); expect(COMMA)
    x0 = require_float(); expect(COMMA)
    x1 = require_float(); expect(COMMA)
    curve = require_identifier(); expect(COMMA)
    y0 = require_float(); expect(COMMA)
    y1 = require_float(); expect(COMMA)
    color = require_int(); expect(COMMA)
    effect = require_identifier(); expect(COMMA)
    flagToken = consume()
    mode = 2 if flagToken is DESIGNANT else 1 if flagToken is TRUE else 0
    extra = 1.0
    if peek() is COMMA:
        consume(); extra = require_float()
    expect(RPAREN)
    arctaps = []
    if peek() is LBRACK:
        consume()
        repeat:
            expect(ARCTAP); expect(LPAREN)
            arctaps.append(require_int())
            expect(RPAREN)
            separator = consume()
            if separator is RBRACK: break
            if separator is not COMMA: throw ArcParser_error
    return ArcNote(start,end,x0,x1,curve,y0,y1,color,effect,mode,extra,arctaps)
```

### Tap timing classification

```text
try_tap(model, note, fingerID):               # 0x160ce28
    # Spatial/candidate selection has already happened.
    if note.virtual_slot8() or note.virtual_slot6(): return false
    now = effective_timeline_time(model.timeline)
    error = abs(note.startTime - now)
    side = 2 if now >= note.startTime else 1

    if error <= 25:
        record_accepted(note, id=0, scoreSide=0, now=now, fingerID=fingerID)
        notify_hit(note, id=0, side=side)
    else if error <= 50:
        record_accepted(note, id=1, scoreSide=side, now=now, fingerID=fingerID)
        notify_hit(note, id=1, side=side)
    else if error <= 100:
        record_accepted(note, id=2, scoreSide=side, now=now, fingerID=fingerID)
        notify_hit(note, id=2, side=side)
    else if error <= 120:
        record_miss(note, now)
        notify_miss(note)
    else:
        return false
    return true     # Consumed, including the miss branch.
```

### Long-note resolution fragments

```text
resolve_active_long_note_fragment(note, now): # branch inside 0xf8056c
    cutoff = trunc(float32(now) + float32(note.interval * 0.5))
    units = resolve_pending_prefix_through_time(note.records, cutoff)
    for each unit:
        record_accepted(note, id=0, scoreSide=0, now=now, fingerID=-1)

count_overdue_units(note, now):              # 0xc6e938
    if records.empty(): return 0
    halfCutoff = trunc(double(now) - min(double(interval)*0.5, 500.0))
    count = number_of_records_with_time_at_most(halfCutoff)
    if count == 1 and note.byte_0x6c != 0:
        lastIndex = 0
    else:
        cutoff = trunc(float32(now) - min(float32(interval*2), 500.0))
        lastIndex = number_of_records_with_time_at_most(cutoff) - 1
        if lastIndex < 0: return 0
    units = 0
    for i from lastIndex down to 0:
        if records[i].resolved: break
        records[i].resolved = true
        units += records[i].weight
    if units != 0: note.byte_0x66 = 0
    return units
```

The calling frame pass checks active state and a virtual eligibility predicate before these paths. Arc overrides and input latches mean these fragments must not be treated as a full hold/arc judge.

### Flick displacement test

```text
test_flick_fragment(flick, fingerID, point):  # 0x16e0548
    if flick.boundFinger == -1:
        flick.boundFinger = fingerID
        flick.origin = point
    else if flick.boundFinger != fingerID:
        return false
    delta = point - flick.origin
    distance = length(delta)
    angle = acos(dot(flick.direction,delta) /
                 (length(flick.direction)*length(delta))) * 180 / pi
    return angle < 45 and distance > 106
```

Finite nonzero vectors are assumed here; exceptional NaN/zero-vector behavior is not characterized. Surrounding time, position, enabled-state, and consumed-state checks remain required.

### Ordinary result state and literal score helper

```text
record_accepted_fragment(state,note,id,side,now,fingerID):
    if not note.virtual_slot4(now,fingerID): return
    if id == 0: state.shiningPURE += 1
    if id == 0 or id == 1: state.PURE += 1
    if id == 2: state.FAR += 1
    # Gauge/ability, early/late, analytics and logging code omitted.
    state.score = score_helper(state.LOST,state.FAR,state.PURE,
                              state.shiningPURE,total,state.specialFlag)
    state.currentCombo += 1

record_miss_fragment(state,note,now):
    if not note.virtual_slot7(true): return
    state.LOST += 1
    state.currentCombo = 0
    # Gauge/ability callbacks and other bookkeeping omitted.

score_helper(lost,far,pure,shining,total,special): # 0xe43b80
    if pure == total and not (special & 1):
        return 10000000 + shining
    weighted = signed32(10*pure + 5*far)
    quotient = signed_divide(int64(weighted)*1000000000, total)
    base = signed_divide(quotient, 1000)  # Compiler uses multiply-high division.
    cap = 99999999 if (special & 1) else 10000000
    return signed32(min(base,cap) + shining)
```

`lost` is passed but not used directly by this leaf helper; it affects attainable counts. Normal-score equivalence was tested for positive valid totals, without integer overflow.

## Unresolved Mysteries

- Exact arc-curve equations, arc connection/color/finger arbitration, every arc effect and special-mode behavior.
- All coordinate transforms, lane-boundary tie-breaking, touch-size configuration, and camera-dependent hit regions.
- Complete camera axis/easing semantics, scene-control effects, and group-angle downstream processing.
- Full malformed-input compatibility, negative integer behavior, unsupported header consumers, and handling of unusual chart encodings.
- Final chart audio-offset sign and the complete audio/monotonic/touch clock synchronization lifecycle.
- In-device validation against actual charts; the supplied ZIP contains none.

## GitHub Status

Authorized outputs are this file and an appended Expedition 002 entry in `context.md`. Previous documentation is preserved; unresolved items above are not a plan or authorization for another excavation.
