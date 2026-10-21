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
