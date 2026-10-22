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
- Runtime arc classifier `0xd51010`: `b=1`, `s=0`, `si=2`, `so=3`, `sisi=4`, `sosi=5`, `siso=6`, `soso=7`, unknown -> 0. Curve equations were not established in Expedition 002.
- **Authorized correction (2026-10-22):** Expedition 002 originally reversed the `b` and `s` IDs (`b=0, s=1`). Expedition 003 reinspection and isolated native execution established the mapping `b=1, s=0` in this binary: `b` matches at `0xd51058` and returns 1 via `0xd511b8`; `s` matches at `0xd51098` and returns 0 at `0xd511fc`. The user explicitly authorized correcting the old entry. Original wording remains available in history at commit `34dfe214fed3f618a0c61dc2ca4383554a536c69`.
- Scene classifier `0x1090060`: `trackdisplay=0`, `redline=1`, `arcahvdistort=2`, `arcahvdebris=3`, `hidegroup=4`, `enwidencamera=5`, `enwidenlanes=6`, other -> 7. Parser aliases `trackhide/trackshow` become `trackdisplay` records with integer 0/255. Parsing an arbitrary scene-control identifier does not prove an effect exists.
- Camera handler `0x192b5c8` includes `reset`, separates two triples of components, and calls action builders with `qi/qo` branches. Duration-to-seconds division by 1000 is visible in `0x10a2b94`.
- Lexer-only tokens `at` and `rgb` are not additional top-level events. Negative-number lexing, comments, exponent notation, malformed-input compatibility, complete camera/effect semantics, and all possible header consumers are not fully characterized.

### What I Found — milliseconds, eligibility, and tap outcomes

- `Cocos2dxGLSurfaceView.smali::getTouchTimestampNow` converts `SystemClock.elapsedRealtimeNanos()` to milliseconds. The touch handler supplies pointer IDs, X/Y, and size times pressure. Native `0x1271200` calls `std::chrono::steady_clock::now()` and converts nanoseconds to milliseconds. Timeline updater `0x16c90bc` supplies the integer time/compensation fields used by judges. Cross-clock epoch equivalence and the final audio-offset sign are not assumed.
- Effective judge time is `timeline.i32_20 - i32_28` when byte `0x2d` is nonzero; otherwise it is `i32_34 - i32_28`, with an additional `-3000` when `i32_34 <= 0`. Field names/lifecycle remain provisional.
- Touch routine `0xeec024` performs projection and candidate selection. Floor taps require matching a computed lane candidate. Arc-taps are spatially tested through their parent arc's child list and `0x927384`, then use the tap classifier. Input-enabled logic byte `+0x54` gates normal processing.
- Candidate sorting calls `0xf6b514`; its exact comparator/tie-breaking policy was not reconstructed. The spatial helper uses resolution/camera/configuration-dependent strict bounds, not a proven fixed screen-pixel hitbox.
- **Authorized spatial-depth correction (2026-10-22):** The Expedition 002 subject document originally identified `0x927384`'s depth cutoff as `-4000`. Expedition 004 decoded `0x927620` as float32 `-1000.0` (bits `0xc47a0000`) and `0x92762c` as rejecting `point.z <= -1000`, supported by isolated ARM64 testing. The user approved correction to the subject document; its earlier wording remains accessible in commit `e2796f27f970e30d94b4ad121ad99024cdebbd86`. The remainder of Expedition 002's earlier findings is preserved.

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

**Resolution (2026-10-22):** The user subsequently authorized this specific correction. Expedition 002's curve-ID entry in `context.md` and `excavations/002_aff_parser_and_note_judgment.md` has been corrected to `b=1, s=0` with provenance notes. The preceding preservation notice is retained as a historical account of the discrepancy before approval; its pending-confirmation status is no longer current.

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

---

## Expedition 004 — Touch Projection, Spatial Judgment & Input Arbitration — 2026-10-22

### Result

Recovered Android/JNI contact transport, viewport coordinate conversion, camera unprojection and gameplay-plane intersections, lane boundaries/width expansion, arc and arc-tap spatial predicates, initial candidate ordering and consumption, and layered duplicate prevention. Executed isolated ARM64 routines and a synthetic full initial-touch-to-tap-judgment chain.

Detailed evidence and pseudocode: [004_touch_projection_and_input_arbitration.md](excavations/004_touch_projection_and_input_arbitration.md).

Sources: supplied `arccopy.zip`, `smali_classes3/org/cocos2dx/lib/` touch/renderer classes and `lib/arm64-v8a/libcocos2dcpp.so`. Main binary SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`; extracted bytes matched the ZIP. Addresses are ELF VAs before relocation. Instruction/smali-backed facts, interpretations, and unknowns are separated in the subject file. Prior instructions and Expedition 001–003 documents were read first.

### What I Found — discrepancy notice; previous text preserved

Expedition 002's -4000 spatial depth cutoff conflicts with direct decoding and execution: at `0x927620`, immediate `-0x3b860000` is bits `0xc47a0000`, **-1000.0**. `0x92762c` rejects projected `point.z <= -1000`; isolated checks confirm equality rejects and values immediately above can pass. The old entry is unchanged pending separately authorized correction. This append records new contradictory evidence rather than silently rewriting history.

**Resolution (2026-10-22):** The user explicitly authorized the `-4000` to `-1000` correction. The Expedition 002 subject file was updated with a provenance note, and the cumulative Expedition 002 entry above now records the correction. The preceding discrepancy statement is retained as a historical record of the pending state prior to authorization; that pending status is no longer current. The original incorrect claim remains inspectable through Git history.

Current context/Expedition 002 already contain the authorized b/s correction (`b=1,s=0`); Expedition 003's historical pending-confirmation wording remains preserved.

### What I Found — identifiers, transport and clocks

- Exact Java sources are under `smali_classes3/org/cocos2dx/lib/`. `Cocos2dxGLSurfaceView::onTouchEvent` captures one current elapsed-realtime timestamp in milliseconds before queueing; collects pointer IDs, X/Y, size*pressure; and queues `$5`–`$10` Runnable wrappers. It does not read MotionEvent event time/history in this method. Renderer forwards `(IFFFJ)` scalar down/up and `([I[F[F[FJ)` move/cancel to JNI.
- JNI begin `0xbe31a8`, move `0x1706960`, end `0xdda71c`, cancel `0xd8dc50` sign-extend Java IDs to 64 bits, pass coordinate/pressure values, and supply additional force-like floats 1.0. There is no axis or game-coordinate conversion in these stubs.
- GLView/GLViewImpl vtables `0x1ab6108/0x1b20d60`: begin virtual `+0xe0` -> `0x97d784`, move `+0xe8` -> `0x160b710`, end/cancel `+0xf0/+0xf8` -> wrappers `0x15af680/0x1556de4` -> common `0x95e32c` with action IDs 2/3.
- Three IDs: Android pointer ID map key; engine slot 0..14; generated gameplay contact ID. Global map `0x1bf1a90`, slot-pointer array `0x1beef90`, bitmask `0x1bfebd4`. Duplicate active pointer begin is skipped; creation also stops when all 15 inspected slots are occupied. Move/end/cancel reuse the mapped object.
- Touch fields: engine slot `+0x0c`; initial latch `+0x10`; initial XY `+0x14`; current XY `+0x1c`; previous XY `+0x24`; pressure product `+0x2c`; supplied extra force `+0x30`; gameplay ID `+0x34`; last-frame game time `+0x3c`; 64-bit begin timestamp `+0x40`.
- Gameplay callback `0x194ff80` assigns generated ID from `0x1bf25f4` and copies `0x1bf93e8` to touch `+0x3c`. Frame update `0x10a75c8` writes effective game time to that global, refining the previous provisional field description. Native move does not refresh `+0x40`; end/cancel wrappers drop their timestamp argument. Initial tap judgment reads the timeline, not touch `+0x40`; complete input-latency compensation is unproven.

### What I Found — coordinate pipeline

- GLView converts coordinates: `(inputX-view.float_1c)/view.float_48`, `(inputY-view.float_20)/view.float_4c`, storing converted current/initial/previous coordinates. These are viewport origin/scales by observed arithmetic; there is no Y flip at this stage.
- Gameplay current-coordinate getter `0x13e0324` reads touch `+0x1c`. Initial routine `0xeec024` -> `0x8a3fac` -> `0xea3e84` -> `0x16d3dcc` unprojects using camera at model `+0x20` wrapper `+0x2a8`, dimensions from Director `+0x180`.
- Core formula: `v=(2*x/W-1, 2*(H-y)/H-1, 2*zInput-1, 1)`; `q=inverse(cameraCombinedMatrix)*v`; return q.xyz/q.w when W component nonzero, otherwise q.xyz. Inverse helper `0x1344f34 -> 0xca3668`; vector transform `0x197341c -> 0x16d4b40`. Camera/node cache refresh `0xe29b94` derives inverse world/view at camera `+0x2e8`; combined matrix `+0x368` multiplies camera `+0x2a8` by `+0x2e8` when dirty.
- Input unprojects zInput -1 and +1 (actual NDC depths -3 and +1), origin=+1 result, direction=normalized(minus1Result-plus1Result). Do not silently substitute conventional 0/1 input endpoints.
- Plane intersection `0x129dee0`: t=(d-dot(n,O))/dot(n,D), or t=0 for exact zero denominator; return O+tD. It does not reject negative t; exact parallelism returns origin. Lanes use Y=0. Arc-taps normally use Z=0; chart byte `+0x110` plus negative camera Z selects Y=0 in the initial path. Camera position getter virtual `+0xe0` -> `0x1154d54` reads node `+0x38/+0x3c/+0x40`.

### What I Found — lane and spatial comparisons

- Lane helper `0x130733c` returns primary low32/secondary high32. Ordinary eligibility is strict **-500<P.z<500**. With chart `+0x110` and cameraZ<0 or cameraZ>900, alternate eligibility is strict **P.z>-1000**, without the ordinary upper bound.
- Let X=trunc(P.x), E=model.float_74, G=model.float_60. Primary classification: if E>0 and X<-850 ->1; otherwise X<-425 ->2; -425<=X<0 ->3; 0<=X<425 ->4; **X==425 ->0**; X>425 ->5, except X>850 and E>0 ->6. Exactly 850 remains5. X=425.9 truncates425. Outer X is not rejected by this function when E<=0; IDs2/5 extend outward after depth eligibility.
- G>1 adds possible secondary using X±(G-1)*425/2 and float boundary tests: choose left classification if different from primary, else right if different, else0. Only one secondary is returned. Failed depth or G<=1 leaves secondary0. Product meaning of G/E is provisional.
- Caller matches raw position integer `+0x10` against both returned values without explicit nonzero checks; therefore “lane0 can never match any object” is unproven. An explicit nonzero lane argument bypasses computed lanes; normal touch begin passes0.
- Shared arc/arc-tap spatial helper `0x927384` uses initialized globals: `0x1c0094c=180`, `0x1bef2e0=100`, `0x1bee968=250`, `0x1bf6c9c=550` (initializer `0x1930aa4–0x1930ae4`). It gets frame height via `0xf09110` -> GLView virtual+b0 -> `0xc0d108`; this differs from the Director design dimensions used for unprojection.
- Let delta=clamp(frameHeight-720,0,240), base=900+(delta/-240)*100, S=2 if cameraZ<0 else max(1,cameraZ/base). Native operation order is float32. B=global100 for flag0; flag1 uses212 when chart+110false, otherwise trunc(suppliedWidth). Horizontal strict bounds: `targetX-S*trunc(global180/2)-S*B < pointX < targetX+S*trunc(global180/2)+S*B`. Defaults at S=1 give ordinary arc half-extent190 and arc-tap302 internal units, not pixels.
- Flag1/chart+110false adjusts Y: Y<=100 ->100; otherwise Y>=G*550 ->G*550. With normal cap>=100 this is a clamp; low-cap exceptional ordering remains literal. Other combinations do not clamp. Then truncate Y toward zero. Strict vertical bounds: `targetY-S*250-(flag?S*60:0) < trunc(Y) < targetY+S*250`. Depth must be **pointZ>-1000**.
- Ordinary arc caller `0xc98490` passes flag0; arc-tap caller `0xeec47c` flag1/width212. Arc checker rejects nonzero mode+a4. Nonzero-duration arcs require byte+d0 or initial-call `now+120>=start`; zero duration permits byte+d0 or `now+(initial?120:0)>=start`. No separate end-time rejection is present in this helper. Normal arc target is quantized startX+float_d4, float_d8; zero duration uses quantized startX and startY*global550. Arc-tap target adds parent startX to child localXY at+80.

### What I Found — collection, sorting, arbitration and duplicates

- Initial routine `0xeec024` gates on model bytes+138/+139, updates timeline, clears candidate vector+b8/+c0/+c8 and scans active logic range+a0/+a8, skipping note.byte54==0. Tap lane match appends without a tap-time prefilter. Hold appends on lane match plus **start<now+100 and now<end**. Arc branch spatially tests child vector+120 and appends eligible arc-taps, rather than treating the arc body as a tap.
- Append `0x1082558` pushes/retains; it does not search for duplicates. Sort `0xf6b514` and helpers `0x16af85c/0x96cc18` compare **signed note.startTime(+18) ascending only**. No spatial-distance, absolute-error, type or contact tie key is present. Native execution demonstrates instability for equal timestamps (31-element example), so source-order/type-priority guarantees are unsupported.
- Ordered loop `0xeec4f0–0xeec570`: taps/arc-taps call `0x160ce28` with touch generated ID+34; false continues, true stops, including a miss/consumed return. Hold branch sets initial latch+a8 and stops without directly scoring a tap. Continuous routine `0x14858d4` is separate; first-consumed stopping is not a universal contact exclusivity rule.
- Duplicate prevention layers: engine active-pointer map; first initial consumption; note resolved bytes+c/+d; ordinary arc color claim `0x15a90c4` with global claimed IDs. Ordinary tap acceptance `0x965e28` sets note+d=1 and contactID+10; arc-tap acceptance `0xc78814` does likewise with a parent-mode exception. Callback pressure comparisons within 0.00001 are bookkeeping, not proof of physical-finger identity or same-pressure input rejection.
- Listener binding `0x130bdf0` is identified by callback RTTI as `GameModel::initializeTouchEvents`. Factory `0xb981cc` creates EventListenerTouchAllAtOnce (vtable `0x1b8be30`), model+150. Listener fields+80/+b0/+e0/+110 bind begin194ff80/move10e7008/endd88408/cancel18ba6d8 through std::function vtables; registration1942fc8 receives integer20. Both end/cancel invoke cleanup f9a50c, gated by model+148, releasing retained touches/color ownership. Relative ordering against other listeners remains unestablished.
- Established judgment chain: Java queued down -> JNI be31a8 -> GLView97d784 -> listener dispatch -> gameplay begin194ff80 -> eec024 -> projection/lane/collection -> f6b514 ->160ce28 -> accepted recorder1730290 or miss868e54. Existing tap timing tiers remain unchanged; classifier true includes101–120 ms miss handling and independent expiry can preempt late candidates.

### Pseudocode and validation

Subject document contains transport, unprojection, exact line-plane intersection, lane classification/expansion, spatial predicate and initial candidate-pass pseudocode with unknown branches explicitly bounded.

Original ARM64 Unicorn checks passed: **12** unprojection cases with native matrix inverse/transform, **3** line-plane cases, **115** lane cases, **333** spatial cases, **65** native-sort cases. Also passed spatial-to-classifier routing, full synthetic initial-touch-to-tap path, an earlier-versus-closer candidate case, and blocked-note rejection.

Full-input fixture: cached identity camera/design1280x720, touch(640,360), lane4 note1000, timeline1008 -> ID0. Two eligible lane4 notes1000/1049 collected in reverse order at timeline1050 -> exactly one result, ID1 for the earlier note's50ms error, despite the later note's1ms error. This verifies chronological arbitration rather than closest-error selection.

Tests supply synthetic cached camera/objects and hook node refresh, camera getter/frame size, type casts, retain/release, timeline refresh and result/UI callbacks. Core inverse/transform, plane, lane, spatial, sort, collection and classifier instructions execute. No actual hardware/renderer/audio/score side effects or real AFF chart were run; archive contains no AFF samples. Only authorized docs are committed.

### Unresolved Mysteries

Complete camera/viewport producers and runtime policies; nonfinite/singular matrices; lane-zero position provenance; product meanings/lifecycle of width and special-mode fields; active-range/frame-maintenance rules; complete platform dispatch/cancellation scheduling; timestamp uses elsewhere and input/audio-latency compensation; all continuous multi-contact special cases on real hardware. These are unresolved questions, not scheduled future directions or authorization for another expedition.

---

## Expedition 005 — Audio Timeline, Offsets & Synchronization — 2026-10-22

### Result

Recovered normal judgment-clock initialization/start/update/pause/resume behavior; concrete AFF/user offset sources and signs; timeline adjustments; FMOD start/seek/SFX arithmetic; and touch-age correction in offset calibration. No periodic audio-position feedback was found in the inspected running gameplay clock/frame/input chain. Explicit resume/seek alignment is confirmed and distinct from continuous drift correction.

Subject evidence/pseudocode: [005_audio_timeline_offsets_and_synchronization.md](excavations/005_audio_timeline_offsets_and_synchronization.md).

Sources: supplied `arccopy.zip`; authoritative instructions and current cumulative/relevant Expedition 002–004 records read first. Main `lib/arm64-v8a/libcocos2dcpp.so` SHA-256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`; separate `lib/arm64-v8a/libfmodProvider.so` SHA-256 `db07590708c1e2b7ed3a17800a8839392d5a7a8322cd102d5b35bda05b251bfb`. Extracted files matched ZIP bytes. Addresses are library-relative ELF VAs; provider addresses explicitly belong to the second ELF. Earlier text remains unchanged; newly resolved questions below do not rewrite historical unknowns.

### What I Found — judgment clock and lifecycle

- Authoritative normal judgment time is effective **GameTimeline** time, not a direct FMOD playhead or stored touch timestamp. RTTI name `0x4d6216`, typeinfo `0x1b09aa0`, vtable point `0x1af5e60`; model timeline pointer+30. Factory/model initialization `0xfbfd04` allocates/zeroes timeline, clears cursor/anchor/flags and sets combined offset.
- Timeline fields: +10 steady epoch Osteady (i64), +18 system epoch Osystem (i64), +20 raw R (i32), +24 pause reference P, +28 compensation C, bytes+2c paused/+2d steady mode/+2e music-started/+2f adjustment/fade flag, +30 combined offset O, +34 cursor/adjustment A, +38 startup effective anchor B. A is not established as a frame delta.
- Effective getter: steady mode -> E=R-C; otherwise E=A-C-(A<=0?3000:0). Tap160ce28, initial inputeec024, continuous14858d4 and frame10a7550 use these fields. Manual/prestart branch uses A rather than R.
- Helper1271200 calls `std::chrono::steady_clock::now` (PLT1a6dc60), converts nanoseconds/1,000,000 to ms. Updater16c90bc uses low32 origin and signed32 arithmetic. Helper11a7ae0 instead calls `system_clock::now` (PLT1a6dbe0) and converts its native count/1000 to ms. Epochs are not assumed interchangeable with Android elapsed realtime.
- Start wrapper8db04c stores supplied epochs+10/+18 and sets steady flag+2d, without recalculating R/C. Callers192d8a0,14b2910,9605f8 supply current or deferred origins using the two helpers. Full network/deferred-start policy is not reconstructed.
- Updater16c90bc normal steady path: base=steadyNow-low32(Osteady)-(A<=0?3000:0); R=base; if paused C=base-P. If music not started and effective time (before final R+=A) is **strictly greater than -O**, and unpaused, request BGM start, set latch, C=base+O, B=-O; optional fade branch. Finally R+=A. With ordinary A=0, startup anchors E exactly to -O and discards crossing-frame overshoot. Subsequent E advances with steady elapsed time. The3000 term is explicit count-in/pre-roll, not measured DAC latency.
- Model pausee31764 sets input gate+138 then calls9e74f4. Pause routine first updates under old state. Pause true stores P=E-A, requests audio pause and sets paused flag. Paused updates make E=P+A fixed while C absorbs elapsed OS time.
- Resume false after music start seeks to **E-B**, then unpauses and clears flag; with ordinary B=-O this is **E+O**. Resume before start clears pause without the started-music seek branch. This is explicit timeline-derived realignment, not an audio-drift measurement.
- Adjustmenta19088 via model15a0238: mode0/other subtracts delta from both64-bit epochs without immediate seek; mode1/2 adds delta to A, updates and seeks with **E**; mode2 also sets+2f and model wrapper handles note/checkpoint state. Resume E-B and adjustment E are distinct. A sign/zero changes affect the3000 branch, so cursor changes are not universally plain deltas to E. Observed callers include special-song triggers and initialization/multiplayer skips, not a recovered periodic drift loop.

### What I Found — offset sources and signs

- AFF AudioOffset: atoi at173bcfc -> LogicChart signed+c4 (as previously traced). Atfbfed0–fbff54, model initialization selects user value settings+4 when settings.i32_0==0, otherwise+8; stores **O=AFF+selectedUserOffset** at timeline+30. No sign reversal/sample conversion occurs in that sum.
- Settings loader1a02b48: field0 key `audio_preset` default0. Field4 prefers `offset_int_2`; if missing, legacy `offset_int` minus**20**, or0 if both missing. Field8 key `bt_offset`, default**200**. INT_MIN is the missing sentinel. Setter169e288 writes selected field to `offset_int_2` or `bt_offset`. Legacy migration is not an additional subtraction on every current offset.
- Inference from ordinary anchored path, ignoring backend/output latency: logical music playhead M and chart E satisfy **E≈M-(AFF+user)**; chart note n nominally matches at **M≈n+AFF+user**. A positive selected offset therefore moves nominal matching input later on the logical music timeline. This is not a physical speaker/touch-latency measurement. Example AFF120+user30 ->O150 and E=-150 at the music-start request.

### What I Found — playback, SFX and device configuration

- Main startup1735d7c dispatches provider virtual+28 with loop=false,index0,delay0 after clearing queued/fade settings and restoring volume. In separate provider ELF: +28->270a8 playBGM; +30->22124 pause; +38->32da0 position getter; +40->35b38 seek; +58->26e04 scheduled SFX; +70->39b8c interactive SFX; +a8->39ea0 update; +b8/+c0->3f708/49118 mixer suspend/resume.
- Provider270a8 queries software sample rate Fs and main channel parent DSP clock; computes `samples=f32(f32(f32(delayMs)/1000)*f32(Fs))`, `start=uint64(f32(samples+f32(parentDSP)))`; calls setDelay(start,0,true), then unpauses selected channel/main group. Normal GameTimeline startup supplies delay0; API support for a future delay is not proof that normal start requests one. Float32 clock conversion is real: tested parent536870929/delay0 schedules536870912.
- Getter32da0 uses FMOD Channel.getPosition(...,unit1); seek35b38 uses setPosition(...,unit1). Unit1 and surrounding conversions support milliseconds. Main wrappers1947af4 read index0, fbf24c seek,18c9ba4 pause. No external manual substituted for binary evidence.
- Mainc81b18 copies/prefixes resource/time pairs and dispatches+58, without adding offsets in that inspected copy path. Provider26e04 pauses main group, prepares channels, reads Fs/main parentDSP, schedules supplied times as parent+time/1000*Fs, assigns channels to main group and retains records. Every upstream timestamp producer is not reconstructed.
- Main seek35b38 first reads old main/index0 position, then sets requested channel. For index0, each scheduled SFX start is shifted by `-f32((newPos-oldMainPos)/1000)*Fs` with native float32 rounding; if shifted start<parentDSP, stop it, else setDelay; equality reschedules. Nonzero index skips main-SFX adjustment. Interactive39b8c unpauses immediately and has no DSP scheduling calls in its inspected body.
- `smali/low/moe/AppActivity.smali` reads OUTPUT_SAMPLE_RATE/OUTPUT_FRAMES_PER_BUFFER and a Bluetooth-related adapter/profile boolean. Provider JNI3cc90 stores buffer size58510 and bool584e4 plus JNI/VM state; its inspected body does not add sample rate to timeline compensation. Init30af0 conditionally setOutput(enum11), setDSPBufferSize(bufferSize,4), then init512 channels. Playback separately queries actual software rate. No bufferSize/Fs or measured output-latency term was traced into O or tap error; automatic physical-latency correction remains unestablished.

### What I Found — input age and drift

- Positive timestamp-age consumer: calibration callback192410c, RTTI `SettingsLayerV2Offset::showSync` dialog touch lambda, function-object vtable1b32250. It reads Touch+40 timestamp T, GLView virtual+100 current Android time N, main audio position M, and stores **M+T-N-expectedBeat**. Beats1000/3000/5000/7000 selected across playback thresholds1999/3999/5999. Thus touch age is subtracted in calibration.
- GLViewImpl+100 resolves12e0d48, which calls Java Cocos2dxGLSurfaceView.getTouchTimestampNow through JNI. This shares the timestamp source, rather than assuming the C++ system-clock epoch equals Android elapsed realtime. Timestamp is Java onTouchEvent sampling, not necessarily the sensor's original event time.
- Ordinary begin194ff80 ->eec024 ->160ce28 updates/reads GameTimeline; classifier receives note/contactID, not Touch. Continuous14858d4 also uses E. No Touch+40 age subtraction was found in those inspected gameplay paths. Static calibrated offset is confirmed; per-event gameplay queue-age compensation remains unestablished. Calibration behavior must not be imported into judgment pseudocode.
- Running updater16c90bc does not call audio-position getter; after startup, pause and explicit adjustments account for recovered clock corrections. Main getter1947af4 direct callers are calibration192410c and StartScene::init touch lambda1591420 (one branch enforces static music position15930). Other inspected position accesses concern seeks, queued system BGM, and TopBar login state, not a demonstrated normal-gameplay drift controller.
- Provider39ea0 calls FMOD System.update then error handling48240 (zero result returns). No audio-position query/application timeline mutation occurs there. Mixer suspend/resume3f708/49118 is separate from timeline pause/resume; complete platform ordering is unknown.
- Supported model: steady-derived judge time, startup anchor, configured offsets, paused-time compensation, explicit seek/resume alignment, and shared DSP scheduling. **No continuous application-level audio-playhead drift correction was found in the recovered normal clock/frame/input chain.** This is a bounded negative finding, not proof across all indirect callers/modes or FMOD internals.

### Pseudocode and validation

Subject document contains source-key migration, offset sum, effective getter, literal update/startup fallback, pause/resume, adjustment modes, DSP conversion and calibration pseudocode.

Unicorn executed original ARM64 with synthetic clock/settings/audio data:4 relevant settings-prefix cases;9 offset-selection/sum basic-block cases;5 startup-offset boundary scenarios;4 paused elapsed jumps;resume seek/unpause/progression;5 long-duration elapsed intervals;3 adjustment modes/manual branch;21 calibration beat/age cases. Separate provider passed45 rate/delay/parent-clock combinations,2 group-pause cases,4 seek-SFX shift/stop cases. FMOD APIs/map bookkeeping, node/UI/spatial calibration wrappers and external clocks are hooked; native timing/calibration/provider arithmetic executes. No actual Android queue/audio hardware, live score effects, measured oscillator drift or full scheduled-SFX loading was executed. Archive contains no AFF samples. Only the two authorized docs are committed.

### Unresolved Mysteries

Full deferred/multiplayer-start and special-song semantics; every scheduled-SFX timestamp producer; automatic preset/route selection; all indirect timestamp/audio-position consumers; physical latency/clock drift on hardware; unusual overflow/mode transitions; complete app-background ordering between timeline pause and mixer suspension. These are bounded unknowns, not future plans or authorization for another expedition.
