# Reverse-Engineering Context Archive

This file is the cumulative record of project discoveries and notes for future tasks. Preserve previous facts unless correction is necessary; explain any corrections.

## Project initialization — 2026-10-21

### Mission and working rules

- Goal: reverse-engineer a mobile rhythm game to understand mobile games in general and this game in particular.
- Source material made available in the ChatGPT project: `Introduction-and-the-scheme-of-this-project.txt` and `arccopy.zip`, described as a portion of the application.
- Language and report format: English; each agreed excavation task produces sections titled **Result**, **What I Found**, and **Pseudocode**.
- For each agreed excavation task, maintain this cumulative `context.md` and create a task-specific pseudocode file.
- Treat findings as evidence-based, distinguish observations from inference, and do not silently rewrite older observations.

### Confirmed project/repository state

- Repository: `thgillwtnorizoh/arconist`.
- Default branch: `main`.
- GitHub integration authentication and repository access succeeded.
- The project repository began empty and was initialized with `README.md`.
- No game-specific technical excavation has been performed or established at this point.

### Notes for the first excavation

- Inspect the relevant files within `arccopy.zip` before making claims about game internals.
- Record relevant paths, evidence, hypotheses, uncertainties, and any open questions.
- Keep task-specific pseudocode in a separate file and link it from this archive.
- Do not assume the supplied archive represents the complete game.

## Excavation log

_No excavation entries yet._

## Excavation 001 — Rhythm Gameplay Elements — 2026-10-21

### Result

Investigated the supplied archive for note data, note logic, rendering, track structure, timing, and score representation. Recovered native class relationships and executable long-note checkpoint behavior. This is a static investigation of a partial archive, not a complete gameplay implementation or a runtime validation. The earlier exploratory report mentioned in the handoff was not imported as verified evidence.

Task pseudocode: [001_rhythm_gameplay_elements.md](excavations/001_rhythm_gameplay_elements.md).

### Evidence conventions and source identity

- **Confirmed:** directly observed file content, ELF metadata/relocations, or decoded instructions.
- **Interpretation:** meaning inferred from those observations; field and routine names supplied by the researcher are explicitly provisional.
- **Unknown:** behavior not established by this investigation.
- Primary binary: `lib/arm64-v8a/libcocos2dcpp.so`, ELF64 little-endian AArch64, stripped; GNU Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`; SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.
- All native addresses below are ELF virtual addresses before runtime relocation. For the cited `.text` and `.rodata` locations, virtual address equals file offset. This does **not** apply to the cited RTTI/vtable addresses: `.data.rel.ro` has file offset = virtual address minus `0x4000`.
- Method labels such as “long-note initializer” describe observed behavior; they are not recovered exported C++ method symbols. RTTI class names are recovered names. Vtable slots are zero-based from the address point.
- Method: ZIP inventory, asset parsing, smali inspection, ELF dynamic symbols and `R_AARCH64_RELATIVE` relocations, Itanium-style RTTI relationships, AArch64 disassembly with `.eh_frame` function ranges. No execution of the game and no external gameplay documentation used.

### What I Found — native object families

**Confirmed RTTI relationships:**

| Family | Derived class | Immediate base | Typeinfo VA |
|---|---|---|---|
| Data | `SimpleNote` | `Note` | `0x1aa5580` |
| Data | `HoldNote` | `Note` | `0x1afb9e8` |
| Data | `ArcNote` | `Note` | `0x1aa53a0` |
| Data | `FlickNote` | `Note` | `0x1b11f78` |
| Data/event | `Timing` | `Note` | `0x1ae5ea0` |
| Data/event | `CameraControl` | `Note` | `0x1b57740` |
| Logic | `LogicTapNote` | `LogicNote` | `0x1b43358` |
| Logic | `LogicArcTapNote` | `LogicTapNote` | `0x1b3c5b8` |
| Logic | `LogicLongNoteBase` | `LogicNote` | `0x1af6c48` |
| Logic | `LogicHoldNote` | `LogicLongNoteBase` | `0x1b44168` |
| Logic | `LogicArcNote` | `LogicLongNoteBase` | `0x1b123e0` |
| Logic | `LogicFlickNote` | `LogicNote` | `0x1a89ca0` |
| Rendering | `RenderTapNote` | `RenderNote` | `0x1b87a08` |
| Rendering | `RenderArcTapNote` | `RenderTapNote` | `0x1b357a0` |
| Rendering | `RenderHoldNote` | `RenderNote` | `0x1b21478` |
| Rendering | `RenderArcNote` | `RenderNote` | `0x1afd790` |
| Rendering | `RenderFlickNote` | `RenderNote` | `0x1af8ab0` |

`RenderNote`, `TrackBase`, `ArcSegment`, and `NoteBurstRenderer` derive from `cocos2d::Node`; `TrackLayer` derives from `cocos2d::Layer`. `LogicNote`, `LogicChart`, `LogicArcGroup`, `NotePosition`, and `ScoreState` derive from `cocos2d::Ref`. For example, `RenderNote` typeinfo `0x1aa9d58` references Node typeinfo `0x1b33f80`; `LogicNote` typeinfo `0x1af0e50` references Ref typeinfo `0x1b57778`.

**Interpretation:** the classes support separate chart data, gameplay logic, and scene rendering. Shared long-note logic is established by inheritance and direct calls, not merely similar names. The presence of flick classes does not establish which released charts or modes use flicks.

### What I Found — chart and timing evidence

- **Confirmed:** no ZIP entry has an `.aff` extension. `assets/songs/songlist` is JSON metadata, not note-event data. Its first song, `sayonarahatsukoi`, includes `bpm: "178"`, `bpm_base: 178`, `side`, `bg`, and `difficulties` entries with `ratingClass`, `chartDesigner`, and `rating`. These metadata do not prove how runtime tempo changes are processed.
- **Confirmed binary strings:** `arc(` at `0x534301`, `hold(` at `0x55abff`, `timing(` at `0x569292`, `arctap` at `0x582d3d`, `timinggroup` at `0x5337e6`, and `flick(` at `0x541d1a`. Parser token RTTI includes `Tokens::ARC`, `HOLD`, `ARCTAP`, `TIMING`, `TIMINGGROUP`, and `CAMERA`. These establish parser vocabulary clues, not a complete chart grammar.
- `AudioOffset` at `0x568461` is referenced at instruction `0x173b3f0`; `TimingPointDensityFactor` at `0x540fda` is referenced at `0x173b560`. Both occur within `0x173b358` (size `0x1318`), reached through `LogicChart` vtable `0x1b31408`, slot 2. Their complete parsing semantics and downstream propagation were not reconstructed.
- **Confirmed executable arithmetic:** long-note initializer `0x17cb97c` (size `0xc8`) reads a float at its fifth explicit integer/pointer argument's `+0x20`, takes its absolute value, and stores `60000.0 / abs(value) / (abs(value) >= 255.0 ? 1.0 : 2.0) / supplied_float` at `this+0x70`. Start/end integer arguments are stored at `+0x18/+0x1c`.
- Hold initializer `0xd75e54` calls this shared initializer at `0xd75e74`; arc initializer `0xc664f8` calls it at `0xc66544`. They are respectively slot 13 in `LogicHoldNote` vtable `0x1b2eda8` and `LogicArcNote` vtable `0x1b91500`.
- **Interpretation:** `value` is a tempo/BPM quantity, the stored interval is in milliseconds, and `supplied_float` is a checkpoint density multiplier. The arithmetic and callers are confirmed; this investigation did not trace that float all the way from the `TimingPointDensityFactor` header. Do not treat that linkage as proven.
- Generator `0xd92558` (size `0x140`, hold vtable slot 10) creates 12-byte records in a vector at `+0x78/+0x80/+0x88`. A record contains a time integer at `+0`, integer `1` at `+4`, and byte `0` at `+8`. The midpoint fallback is confirmed for nonzero durations with no generated records. The integer and byte semantics are not fully named.
- Arc override `0xba81e8` calls that generator and then has a linked-arc-dependent adjustment that can remove the last record and write `2` into the preceding record's integer field. Exact gameplay meaning is unresolved; the base generator must not be presented as the entire arc algorithm.
- Arc method `0x165286c` references `Classes/LogicArcNote.cpp` (`0x52f861`) and `setArcGroup` (`0x559cf8`); it emits an assertion log when `this+0xe0` is already set, then assigns the group pointer. This is a surviving source-location clue, not source code availability.

### What I Found — rendering and track

- Tap renderer vtable `0x1acde18`, slot 162, points to `0xf20c28` (size `0x4f8`). It follows slot 161 (`+0x508`) to obtain a logic object, then reads that object's `+0x20` data pointer.
- Its horizontal branch at `0xf20cd4–0xf20d40` uses data `+0x0c` as a mode discriminator. In the nonzero branch, integer `+0x10` values 1 through 6 produce `425 * (value - 1) - 1063`; values outside that range produce `212`. The zero branch reads float `+0x14` and calculates `trunc((x * 1700 - 850) - 212) + 212` using float arithmetic. Result is stored at render object `+0x2a0`.
- **Interpretation:** these are lane-based and continuous horizontal placement modes. Six handled values establish a renderer capability, not that every chart uses six lanes. The numbers are internal coordinates, not proven screen pixels or hitbox dimensions.
- Tap renderer initializer `0xd7e290` references `img/note_tomato.png`, `img/note.png`, and `img/note_dark.png` at `0xd7e3ac–0xd7e3e8`, then creates a child visual through `0x132e26c`. The assets named by those references are absent from this ZIP.
- **Present assets:** `assets/models/tap_l.obj`, `tap_d.obj`, `tap_tomato.obj`, their `.mtl` files, and `assets/models/track_break2.obj`. `tap_l.obj` contains an eight-vertex cube with twelve triangle faces; `tap_l.mtl` references `tap_l.png`, which is absent. Asset presence alone does not prove a particular runtime renderer uses that mesh.
- `assets/particle/particle_arc.plist` contains `maxParticles=5`, `particleLifespan=0.49`, `textureFileName=particle_arc.png`, source blend `770`, destination blend `1`, and duration `-1`. Mirai light/conflict variants are also present. Runtime overrides are possible; the texture itself is absent.
- Native strings additionally reference `img/arc_body.png` (`0x590425`), `img/track_lane_divider.png` (`0x53404b`), and `img/track_critical_line.png` (`0x553d85`); these strings do not mean those textures are supplied.

### What I Found — input, frame dispatch, score, and HUD

- `smali_classes3/org/cocos2dx/lib/Cocos2dxRenderer.smali` declares `nativeTouchesBegin(IFFFJ)`, `nativeTouchesEnd(IFFFJ)`, and move/cancel variants with identifier/float arrays and a long argument. Smali wrappers directly forward those arguments. Exact meaning and time units of every argument were not traced here.
- `onDrawFrame` calls `nativeRender` immediately when `sAnimationInterval <= 1.6666666666666666e7` nanoseconds. Above that threshold, it compares `System.nanoTime()` against the last tick, sleeps for integer remaining milliseconds if needed, updates the tick, and calls `nativeRender`. This describes the Java frame-dispatch branch, not a guaranteed device frame rate or the judgment clock.
- Exported native render entry: `Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeRender` at `0xe181d0`, size `0x30`; it dispatches two virtual calls via the result of `0xa4227c`. Exported touch begin/move/end/cancel entries are at `0xbe31a8`, `0x1706960`, `0xdda71c`, and `0xd8dc50` respectively.
- **Confirmed score representation:** `ScoreState` RTTI name at `0x48c2fc`, typeinfo `0x1b10180`, vtable `0x1b35178`. SQL string at `0x53a12b` defines a `scores` table with `version`, `score`, `shinyPerfectCount`, `perfectCount`, `nearCount`, `missCount`, `date`, `songId`, `songDifficulty`, `modifier`, and `health`. An insertion fragment at `0x53693d` additionally includes `ct`. This confirms embedded persistence vocabulary, not which schema is active on a device.
- `assets/layouts/ingame/IngameUIRight.csb` contains `pureLabel-fullnolocalize`, `farLabel-fullnolocalize`, `lostLabel-fullnolocalize`, `earlyLabel-fullnolocalize`, `lateLabel-fullnolocalize`, `progress_bar`, and pacemaker labels. `assets/layouts/ingame/HpBar.csb` contains `hpLabel`, `hpBar`, `hpBar2`, and `beyond_marker`. These were extracted as embedded strings; the full CSB structure was not decoded.
- `assets/layouts/results/Results.csb` contains `perfectCountLabel`, `nearCountLabel`, `missCountLabel`, `shiningPerfectCountLabel`, `maxComboCountLabel`, and `lateEarlyCountLabel`, alongside PURE/FAR/LOST UI text. Placeholder values in layout assets are not gameplay results.
- **Interpretation:** internal perfect/near/miss vocabulary corresponds to displayed PURE/FAR/LOST. Numerical score weights, shining-perfect accounting, bonus rules, combo reset rules, hit windows, and gauge changes remain unverified. No standard community scoring formula is being asserted from memory.

### Pseudocode

See the separate excavation document for instruction-backed long-note initialization, checkpoint generation, tap placement, and Android frame dispatch. Broader architecture is an interpretation; no complete judge/scoring/game-loop algorithm was reconstructed.

### Unresolved Mysteries

- Exact score arithmetic, judgment thresholds, shining-perfect inclusion, combo and gauge rules.
- Definitive identification of the native judgment clock and audio-offset sign/units.
- Full AFF grammar, timing-group behavior, tempo changes within long notes, and density-factor propagation.
- Arc curve interpolation, touch tolerance, color/finger association, linked-arc adjustments, and flick activation.
- How the available render classes and meshes participate in the actual draw path, camera projection, culling, and batching.

These are open questions, not scheduled directions or authorization for another excavation. Historical initialization text above remains unchanged and describes the earlier state.

## Excavation 002 — AFF Parsing and Note Judgment — 2026-10-21

### Result

Traced chart text parsing into runtime construction and recovered tap classification, long-note checkpoint consumption, flick displacement checks, result-state changes, and ordinary score arithmetic. This entry adds newly verified information to the historical Expedition 001 record; its previously unresolved items remain preserved above as the state of knowledge at that time.

Detailed evidence, grammar, field layout, pseudocode, and limitations: [002_aff_parser_and_note_judgment.md](excavations/002_aff_parser_and_note_judgment.md).

Same binary as Expedition 001: `lib/arm64-v8a/libcocos2dcpp.so`, SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`. Native addresses are ELF virtual addresses before relocation. All code addresses below equal file offsets. Names assigned to stripped functions are descriptive labels, not recovered C++ function symbols.

### What I Found — chart reader and language surface

**Confirmed pipeline:** resource/text read in `0x16e67a4` -> header/body split at `0x1870de0` -> body token collection `0xdf4a58` / lexer `0x814384` -> chart parser `0xb01d6c` -> statement wrapper `0x139b96c` -> event dispatcher `0x923240` or timing-group parser `0x8c847c`. Header-map parsing uses `0x10dbff8`. Runtime `LogicChart` initializer `0x173b358` calls construction `0x1862a14`, then sorting/linking/checkpoint/timing preprocessing stages.

- Both `\n-\n` and `\r\n-\r\n` separator forms are checked. Header lines split on newline and colon, with carriage returns removed from values and nonempty key/value entries retained.
- `AudioOffset` is converted with `atoi` and stored at `LogicChart+0xc4`. `TimingPointDensityFactor` defaults to `1.0`, uses `atof` for a nonempty value, and is stored at `+0xc8`. Arbitrary stored header keys are not thereby confirmed semantic features.
- Statements require `;`. The complete ordinary-event dispatcher has seven branches: tap, hold, flick, camera, scenecontrol, timing, arc. Group bodies call this dispatcher, so recursive timing-group nesting is not supported by that observed path.

Here `I` is an integer token, `F` a float token, `ID` an identifier, and `P` either integer or float. Parameter names express their interpreted roles; order and parser type requirements are confirmed.

| Event | Parameter sequence | Parser |
|---|---|---|
| Tap | `(I time,P position)` | `0x11bfd24` |
| Hold | `hold(I start,I end,P position)` | `0xf5369c` |
| Timing | `timing(I time,F tempo,F beats)` | `0x10a4ef4` |
| Flick | `flick(I time,F x,F y,F dx,F dy)` | `0xa3ab64` |
| Camera | `camera(I time,F a,F b,F c,F d,F e,F f,ID easing,I duration)` | `0x138f560` |
| Arc | `arc(I start,I end,F x0,F x1,ID curve,F y0,F y1,I color,ID effect,flag[,F extra])[optional arctap list]` | `0xc2cb1c` |
| Scene control | `scenecontrol(I time,ID kind[,F value,I integer])` | `0x7f2628` |

- `0x18905f4`, `0x19070d8`, and `0x14be280` require TINT, TFLOAT, and TIDENT respectively. Float-required parameters are not implicitly coerced from integer tokens by these helpers. Position helper `0xa9c1f0` deliberately accepts both, creating different representations.
- Arc `extra` defaults to `1.0`; it is stored at `ArcNote+0x88` and propagated to the arc factory, but its complete meaning is unknown. It must not be confused with the separately traced checkpoint density header.
- Arc flag token TRUE stores mode 1; DESIGNANT stores mode 2; otherwise the consumed token maps to 0, without an explicit FALSE requirement in that branch. An inclusion flag can discard DESIGNANT arcs (`0x139ba08–0x139ba28`), also handled in groups.
- Arc-tap lists contain `arctap(I time)` items separated by commas. The parser records timestamps, then runtime construction produces child logic objects.
- Timing-group attributes are a single optional identifier split on `_`: `noinput` clears chart byte `+0x0c`; `fadingholds` sets `+0x0d`; `anglex...` and `angley...` parse suffixes with `stoi` into `+0x10/+0x14`; `tracecol...` parses `%02x%02x%02x` for arcs. The cleared input flag propagates to logic `+0x54`, checked by normal input and judgment loops. Rendering is not thereby disabled.
- Runtime arc classifier `0xd51010`: `b=0`, `s=1`, `si=2`, `so=3`, `sisi=4`, `sosi=5`, `siso=6`, `soso=7`, unknown -> 0. Curve equations are not established here.
- Scene classifier `0x1090060`: `trackdisplay=0`, `redline=1`, `arcahvdistort=2`, `arcahvdebris=3`, `hidegroup=4`, `enwidencamera=5`, `enwidenlanes=6`, other -> 7. Parser aliases `trackhide/trackshow` become `trackdisplay` records with integer 0/255. Parsing an arbitrary scene-control identifier does not prove an effect exists.
- Camera handler `0x192b5c8` includes `reset`, separates two triples of components, and calls action builders with `qi/qo` branches. Duration-to-seconds division by 1000 is visible in `0x10a2b94`.
- Lexer-only tokens `at` and `rgb` are not additional top-level events. Negative-number lexing, comments, exponent notation, malformed-input compatibility, complete camera/effect semantics, and all possible header consumers are not fully characterized.

### What I Found — milliseconds, eligibility, and tap outcomes

- `Cocos2dxGLSurfaceView.smali::getTouchTimestampNow` converts `SystemClock.elapsedRealtimeNanos()` to milliseconds. The touch handler supplies pointer IDs, X/Y, and size times pressure. Native `0x1271200` calls `std::chrono::steady_clock::now()` and converts nanoseconds to milliseconds. Timeline updater `0x16c90bc` supplies the integer time/compensation fields used by judges. Cross-clock epoch equivalence and the final audio-offset sign are not assumed.
- Effective judge time is `timeline.i32_20 - i32_28` when byte `0x2d` is nonzero; otherwise it is `i32_34 - i32_28`, with an additional `-3000` when `i32_34 <= 0`. Field names/lifecycle remain provisional.
- Touch routine `0xeec024` performs projection and candidate selection. Floor taps require matching a computed lane candidate. Arc-taps are spatially tested through their parent arc's child list and `0x927384`, then use the tap classifier. Input-enabled logic byte `+0x54` gates normal processing.
- Candidate sorting calls `0xf6b514`; its exact comparator/tie-breaking policy was not reconstructed. The spatial helper uses resolution/camera/configuration-dependent strict bounds, not a proven fixed screen-pixel hitbox.

**Confirmed classifier `0x160ce28`:** checks virtual consumed-state slots 8 and 6 before taking absolute error. For ordinary taps those read bytes `+0x0c/+0x0d`. Arc-tap miss acceptance separately consults parent state via slot 7.

| Absolute timing error | Recorded result | Classifier return |
|---|---|---|
| 0–25 ms inclusive | ID 0, interpreted as shining PURE | true |
| 26–50 ms | ID 1, interpreted as other PURE | true |
| 51–100 ms | ID 2, interpreted as FAR | true |
| 101–120 ms | Miss path, interpreted as LOST | true |
| >120 ms | No event recorded by this routine | false |

The interpretation of tier labels is supported by score-state increments and ordinary score arithmetic. `true` means consumed here, not necessarily successfully played. The separate pass `0xf8056c` expires unconsumed ordinary taps and arc-tap children after `now > endTime + 100`; frame ordering may therefore preempt the late part of the classifier's 120 ms range. This is not a universal ±120 ms successful-hit window.

### What I Found — continuous notes, flicks, and result state

- Continuous-touch routine `0x14858d4` runs before `0xf8056c` in caller `0x10a7550`. Holds use lane, start-lookahead, end-time, and touch-latch checks before setting active flags through `0x14557b4`. Arcs use position/mode checker `0xc98490` and arc-specific slot-12 function `0x15dfe2c`; their full group arbitration is unresolved.
- Density provenance is now confirmed: header -> `LogicChart+0xc8` -> hold factory `0x1446490` / arc factory `0x178f7fc` -> virtual initializer -> `0x17cb97c`. Representative construction loads: `0x18649b0` and `0x1865154`. This adds evidence to the previously uncertain linkage without rewriting Expedition 001.
- The 12-byte checkpoint record's integer at `+4` is a judgment-unit weight and byte `+8` a resolved flag, as shown by unit summation and mutation in `0xf8056c` and `0xc6e938`. Active long-note records up to `truncate(now + interval/2)` are consumed and generate ID-0 accepted events once per unit. Inactive overdue handling uses `now - min(2*interval,500)` with a separate first-checkpoint flag exception preserved in the pseudocode document.
- Flick helper `0x16e0548` binds one finger, compares displacement with the stored chart direction, requires angle <45 degrees and distance >106 internal units, and does not divide by elapsed time. Its surrounding candidate branch checks time and spatial region; it is not just a speed detector. Successful flick processing records ID 0. Actual chart/mode availability is unverified.
- Accepted recorder `0x1730290` consults note virtual slot 4: ID 0 increments `ScoreState+0x20` and `+0x24`, ID 1 increments `+0x24`, ID 2 increments `+0x28`; accepted records increment current combo at `+0x1c`. Miss recorder `0x868e54` consults slot 7, increments `+0x2c`, and resets combo to zero. Interpretations: shining PURE, total PURE, FAR, LOST respectively.
- Score leaf `0xe43b80`, called at `0x1730504`, yields for valid ordinary counts and positive total: `floor(10,000,000 * (PURE + FAR/2) / totalJudgmentUnits) + shiningPURE`. It contains an all-PURE shortcut and a flag-selected cap (10,000,000 versus 99,999,999). The special flag's product meaning is unknown; integer-overflow/invalid-total behavior is not covered by that simplified expression.

### Pseudocode and validation

The separate excavation document contains reader/dispatcher, arc parser, tap classification, long-note record consumption, flick, result-state, and literal score-helper pseudocode. Unknown geometry, effect handlers, and special-mode behavior are explicitly bounded rather than fabricated.

ARM64 Unicorn validation executed original instructions with synthetic objects and hooked surrounding engine calls: 34 tap boundary cases across two clock branches, one blocked-note rejection, and 500 deterministic ordinary-score cases all passed. This is isolated native-code validation, not an in-device test or a full chart-parser execution. No AFF files are present in the supplied archive.

### Unresolved Mysteries

Exact curve equations; complete arc linkage/color/finger arbitration; all spatial transforms and candidate tie-breaking; full camera/effect/special-mode semantics; unusual or malformed chart compatibility; final audio-offset alignment and complete clock lifecycle; real-chart device validation. These are open questions, not scheduled future directions or authorization to start another excavation.

---

## Expedition 003 — Arc geometry, effects, synchronization, and finger tracking

### Result

Recovered local arc equations and sampling, LogicColor contact arbitration/release, LogicArcGroup timing sharing, render feedback, and the game-timeline/audio-provider startup connection. Subject pseudocode/evidence: `excavations/003_arc_geometry_and_finger_tracking.md`. Source: supplied `arccopy.zip`; main `lib/arm64-v8a/libcocos2dcpp.so` SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. Audio-provider evidence comes from the separate `lib/arm64-v8a/libfmodProvider.so`. Addresses are library-relative VAs, with provider addresses explicitly separated.

### What I Found — new evidence conflicts with prior curve-ID entry

**Preservation notice:** Expedition 002's `b=0, s=1` entry conflicts with direct reinspection and isolated native execution. At classifier `0xd51010`, equality with `b` branches via `0xd51058` to `0xd511b8`, returning 1; equality with `s` at `0xd51098` jumps to the return with zero. Thus the newly verified mapping is **b=1, s=0**. Other curve IDs agree. Earlier text has not been changed; changing it awaits explicit user confirmation. This addition records the new evidence and discrepancy separately.

### What I Found — geometry and rendering

- `0x1925084` generates arc geometry. Logic fields: times `+0x18/+0x1c`, x-position objects `+0x20/+0x28` (float x at their `+0x14`), y endpoints `+0xa8/+0xac`, timing object `+0x48`, curve ID `+0x15c`, extra `+0x118`. Vectors `+0xe8/+0x100` store 12-byte Vec3s.
- X endpoints become `trunc(float32(x*850-425))`. Y becomes `trunc(float32(y*(H-100)+100))`, H from global integer `0x1bf6d80`. Effective end is max(own end, successor start times in vector `+0x138`). Local z span is `trunc(-(effectiveEnd-start)/timing.float_28)`. These are internal coordinates, not fixed screen pixels.
- Let I(u)=sin(πu/2), O(u)=1-cos(πu/2), S(u)=3u²-2u³. Sine evaluator `0x180a190` returns `((X1-X0)*Ex, Y0+(Y1-Y0)*Ey, Z*u)`; x is local displacement. Its O implementation is `1-sin((u+1)*π/2)`.

| Label | Newly verified ID | Ex | Ey |
|---|---:|---|---|
| s | 0 | u | u |
| b | 1 | Cubic rotated construction, approximately S | S |
| si | 2 | I | u |
| so | 3 | O | u |
| sisi | 4 | I | I |
| sosi | 5 | O | I |
| siso | 6 | I | O |
| soso | 7 | O | O |

- Cubic helper `0x14f3078`: P0=P1=(0,Y0), P2=P3=(-D,Y1), D=trunc(sqrt(dx²+Z²)); evaluate standard cubic Bezier, rotate its (x,y,0) around Y by `-atan2(dx,-Z)*180/π-90`, return rotated x/y with z replaced by Z*u. D truncation prevents claiming bit-exact `dx*S(u)`. Rotation helpers are `0x1987f94` and `0xcaf3cc`; degeneracies are untested.
- Sampling rate is 14 for own duration<1000 ms, otherwise 7. With seconds=(effectiveEnd-start)/1000, parameter steps are `1/(seconds*rate)` and `1/(seconds*rate*extra)` for the two vectors. Runtime initializer `0xc664f8` clamps extra to >=1. This traces a geometry-density role for the optional arc parameter, separate from judgment checkpoint density.
- Render initializer `0x13b5ff8` turns adjacent `+0x100` samples into segment children via `0x14f3f40`, passing first/last flags. Render update `0x11b7d78` places the parent at `(quantized startX,0,logic.i32_30)` and reads current float displacement/y `+0xd4/+0xd8`. Full current-cache production and camera transforms remain unresolved.

### What I Found — contact tracking and ownership

- Android bridge `smali/org/cocos2dx/lib/Cocos2dxGLSurfaceView.smali` supplies pointer IDs and touch coordinates/timestamps. Native begin callback `0x194ff80`, at `0x195007c–0x195009c`, assigns a separate incrementing ID from `0x1bf25f4` to touch `+0x34`. Color ownership uses that generated ID, not simply the raw Android pointer ID. This establishes contact identity, not physical hand/finger recognition across lifts.
- `0xc98490` checks ordinary arc spatial eligibility, rejects nonzero mode `+0xa4`, consults start time/byte `+0xd0`, and has caller-selected 120 ms start-lookahead versus direct-start branches. Nonzero-duration position uses startX plus `+0xd4`, and float `+0xd8`; zero-duration uses endpoints and separate vertical scale `0x1bf6c9c`. Spatial helper `0x927384` receives 212.0; this is not a proven fixed pixel radius.
- Arc `+0xb0` points to **LogicColor**: factory `0xd93594`, vtable `0x1aa1b98`, RTTI string `0x47dd29`. Chart helper `0xd51220` reuses chart vector `+0x68` entries by mode/mirror-remapped category `+0x18`.
- Arc `+0xe0` points to a separate **LogicArcGroup**: construction `0x125e674–0x125e6e0`, vtable `0x1b85570`, RTTI string `0x479db7`, setter `0x165286c`. Builder `0x125e474` tests time neighborhood, endpoint x proximity/y equality, and mode compatibility while linking arcs; the complete predicate is not reconstructed.
- Claim `0x15a90c4` uses color owner `+0x28`, release time `+0x2c`, interval `+0x0c`, acceptance byte `+0x22`, prior-claim byte `+0x24`, bypass byte `+0x10`, conflict byte `+0x30`, feedback fields `+0x34/+0x38`. Global claimed-contact vector is based at `0x1bfa3d8`.
- Ordinary path: accept same owner; reject another owner; claim unowned color only if generated contact ID is absent from the global vector. Color byte `+0x10` permits acceptance without owner reassignment; category 3 bypasses assignment after the release-time gate. Arc byte `+0x170` bypasses this claim call entirely. Full bypass provenance remains unknown.
- Recorded release blocks reacquisition while `now-releaseTime < trunc(min(4*intervalInteger,1000))`, with equality leaving the gate. This is one ownership gate, not a universal judgment window. Other resets exist: `0x95d61c` clears color prior-claim/conflict bytes and release time after an arc's end when its mode/successor conditions allow.
- Release `0x13db7a0`, called from touch end `0xf9a50c`, clears a matching owner and removes the claimed ID. When a matching global entry is found, prior-claim is set, and bypass clear, it records now as release time. Non-owner release does nothing.

### What I Found — synchronization and effects

- Acceptance `0x15dfe2c` scans pending checkpoints across current/linked arcs, consults connected-group timestamp vector `+0x18`, and conditionally extends group float `+0x14` to `checkpointTime+min(2*interval,500)`. Group bytes `+0x10/+0x12` are activated. This is linked-note coordination, not evidence of beat snapping or network synchronization.
- Acceptance sets logic bytes `+0x64/+0x65` and render virtual `+0x530` -> `0x155241c` -> render byte `+0x300=1`. Render frame `0x11b7d78` reads that state and group/color feedback; one conflict branch constructs RGB (230,50,50) and applies it through `0x15a0eac`. Exact blend semantics remain unknown. Another branch uses a modulo-5 update counter; no fixed real-time effect frequency is established.
- `assets/particle/particle_arc.plist`, `particle_arc_mirai_conflict.plist`, and `particle_arc_mirai_light.plist` exist. Their exact recovered-branch selection and the full AFF effect-token dispatch are unproven.
- Accepted arc with sound handle `+0x68==-1` calls `0x107af5c` with sound ID 0 and arc start time at `0x15e0174–0x15e0198`, storing the result. This is an audio request, not proof of effect-token selection or playback success.
- Timeline updater `0x16c90bc` starts audio when effective time is strictly greater than `-timeline.i32_30` in its unstarted/unpaused branch, sets `+0x2e`, calls audio manager `0x1735d7c`, and updates compensation `+0x28`. Manager dispatches provider virtual `+0x28` with loop=false, index=0, delay=0. AFF/user/device offset composition is still unresolved.
- Separate FMOD provider exported `playBGM` at `0x270a8` reads sample rate/parent DSP clock and calls `setDelay(uint64(float32(parentClock + delayMs/1000*sampleRate)),0,true)` before unpausing. Actual float32 intermediate rounding matters. `loadAndScheduleSfxOnMainBGM` at `0x26e04` also schedules timestamp offsets through sample rate/parent DSP time. Position getter `0x32da0` and setter `0x35b38` use FMOD unit literal 1; setter shifts or stops scheduled channels. Getter existence does not establish continuous drift correction.

### Pseudocode and validation

The subject file contains coordinate/cubic/sine pseudocode and literal color-claim/release/arc-acceptance reconstruction, preserving unknown fields and incomplete scan predicates.

Original ARM64 instructions executed in Unicorn with synthetic objects and hooked external sin/string comparisons: nine classifier inputs, 42 sine samples, and seven ownership assertions passed. Ownership coverage includes release bookkeeping, rejection 1 ms below a 400 ms gate, acceptance at equality, and category-3 acceptance without owner change. Full cubic rotation, renderer, hardware touch, audio output, and real charts were not run; the supplied archive contains no AFF samples.

### Unresolved Mysteries

Full current-position/cache and projection transforms; mesh/shader details; cubic degeneracies; complete linkage predicate; special-mode/bypass provenance; cancellation/feedback lifecycle; full effect/particle dispatch; chart/user/device offset composition, pause/seek and drift correction; end-to-end real-chart/device behavior. These are open questions, not scheduled future directions.
